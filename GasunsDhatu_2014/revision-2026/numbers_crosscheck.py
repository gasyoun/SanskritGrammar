#!/usr/bin/env python
"""numbers_crosscheck.py — pre-submission numeric pass for the M03 monograph (H2871).

The second of the two passes that stand between the author's docx review (H1259) and
the 31-10-2026 working freeze. Like its ГОСТ sibling it REPORTS and never edits: the
manuscript is human-owned prose (H275) and the review docx must stay stable.

The H1259 line edit proved its numeric invariants with a throwaway inline script that
lived only in a PR body. This is that machinery made durable and widened, so freeze day
is "run two scripts, read two reports" rather than "re-invent two methodologies".

WHAT IT CHECKS

  N1  derived table columns — where a grid/pipe table carries a column that is the
      ratio (or sum) of two others, every row must satisfy the relation. This is how
      Таблица 1 «Частотность классов гласных и согласных» proves its C/V column.
  N2  percentages restated in prose — «X из Y (Z %)» and «X/Y (Z %)» are recomputed.
      Both rounding and truncation of the last digit are accepted (the DCS ledger
      records truncation as real editorial practice, H1229 REFUTED #1); anything else
      is a finding.
  N3  arithmetic spelled out in prose — «A + B = C».
  N4  internal cross-references — every «§N.N», «раздел N.N», «Глава N», «Таблица N»,
      «Рисунок N», «Приложение N» must resolve to a heading or caption that exists in
      the manuscript file set; and the «Список иллюстративного материала» must agree
      with the captions actually printed. The H1259 pass fixed two references broken by
      the H991 recomposition by hand; this makes that check mechanical.
  N5  provenance anchoring — every leaf integer in the committed `*_provenance.json`
      files beside this script is a fact the 2026 layer computed. `numbers_anchor_map.json`
      pins which of them the manuscript cites and where. On every later run the pin is
      re-verified: a provenance value that moved while its manuscript locus did not is
      exactly the drift this pass exists to catch.
  N6  numeric drift against a git baseline — the multiset of integers per manuscript
      file, compared with any revision (default `origin/main`). At the freeze this is
      the evidence that an editing pass changed no number it did not mean to.

USAGE
    python numbers_crosscheck.py                    # dry run, writes the dated report
    python numbers_crosscheck.py --stdout           # report to stdout, write nothing
    python numbers_crosscheck.py --update-map       # (re)pin numbers_anchor_map.json
    python numbers_crosscheck.py --baseline HEAD~1  # N6 against another revision

EXIT CODES
    0  no findings          1  findings reported          2  could not run
"""
import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal, InvalidOperation

from m03_checkers_common import (
    HERE,
    MAIN_TEXT,
    MANUSCRIPT_FILES,
    REPO,
    denoise,
    fenced_ranges,
    find_value,
    integers_in,
    manuscript_paths,
    normalise_spaces,
    read_lines,
    strip_frontmatter,
    strip_markup,
)

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ANCHOR_MAP = HERE / "numbers_anchor_map.json"

HEADING_RE = re.compile(r"^(?P<hashes>#{1,6})\s+(?P<text>\S.*)$")
SECTION_NO_RE = re.compile(r"^(?P<num>\d+(?:\.\d+)*)\.?\s")
CHAPTER_RE = re.compile(r"^Глава\s+(?P<num>\d+)\b")
CAPTION_RE = re.compile(r"^(?P<kind>Таблица|Рисунок|Приложение)\s+(?P<num>\d+)\b")
APPENDIX_HEAD_RE = re.compile(r"^Приложение\s+(?P<num>\d+)\b")

REF_SECTION_RE = re.compile(r"(?<!§)§\s?(\d+(?:\.\d+)*)")
REF_RAZDEL_RE = re.compile(r"\bраздел[а-я]*\s+(\d+(?:\.\d+)*)")
REF_CHAPTER_RE = re.compile(r"\bГл(?:ав[аеыу]|\.)\s*(\d+)")
REF_TABLE_RE = re.compile(r"\bТаблиц[а-я]*\s+(\d+)")
REF_FIGURE_RE = re.compile(r"\bРисун[а-я]*\s+(\d+)")
# Singular case forms only: «Приложения 224» in the table of contents is a page number,
# not a reference. Appendices are numbered 1–7, so a large number is never one.
REF_APPENDIX_RE = re.compile(r"\bПриложени(?:е|и|ю|ем)\s+(\d{1,2})\b")
# A § that belongs to ANOTHER document — «RWS_REPORT.md §4.4», «BOOK_PLAN §8»,
# «Whitney, Sanskrit Grammar, 1889, §§311–483» — is not an internal cross-reference.
EXTERNAL_REF_RE = re.compile(r"(?:\.mdx?\b|\b[A-Z][A-Z_0-9]{3,}\b)[^.]{0,40}$")

PCT_IZ_RE = re.compile(
    r"(\d[\d  ]*)\s+из\s+(\d[\d  ]*)[^.;]{0,70}?\(?\s*(\d{1,3}(?:[.,]\d+)?)\s*%"
)
PCT_SLASH_RE = re.compile(
    r"(\d[\d  ]*)\s*/\s*(\d[\d  ]*)[^.;]{0,40}?\(\s*(\d{1,3}(?:[.,]\d+)?)\s*%"
)
SUM_RE = re.compile(r"(\d[\d  ]*)\s*\+\s*(\d[\d  ]*)\s*=\s*(\d[\d  ]*)(?!\s*[%,.]\d)")

ILLUSTRATION_HEADING = "# Список иллюстративного материала"
ILLUSTRATION_ROW_RE = re.compile(r"^(?P<kind>Таблица|Рисунок)\s+(?P<num>\d+)\s+(?P<title>.+?)\s+(?P<page>\d+)$")


class Finding:
    __slots__ = ("code", "locus", "message", "note")

    def __init__(self, code, locus, message, note=""):
        self.code = code
        self.locus = locus
        self.message = message
        self.note = note


def dec(token):
    """'1,33' / '74,1' / '2 259' -> Decimal, or None."""
    token = normalise_spaces(str(token)).replace(" ", "").replace(",", ".")
    try:
        return Decimal(token)
    except InvalidOperation:
        return None


def places(token):
    token = normalise_spaces(str(token)).replace(",", ".")
    return len(token.split(".")[1]) if "." in token else 0


def quantise(value, dp):
    """(rounded, truncated) representations of `value` at `dp` decimal places."""
    scale = Decimal(10) ** dp
    scaled = value * scale
    rounded = (scaled.to_integral_value(rounding="ROUND_HALF_UP")) / scale
    truncated = (scaled.to_integral_value(rounding="ROUND_DOWN")) / scale
    return rounded, truncated


# ---------------------------------------------------------------- tables (N1)

def parse_tables(lines, fenced):
    """Every grid or pipe table as {'line': n, 'rows': [[cell, ...], ...]}."""
    tables = []
    current = None
    for no, text in lines:
        raw = normalise_spaces(text.rstrip())
        is_grid_sep = raw.startswith("+-") or raw.startswith("+=")
        is_row = raw.startswith("|") and raw.endswith("|")
        if is_row or is_grid_sep:
            if current is None:
                current = {"line": no, "rows": [], "pending": None}
            if is_grid_sep:
                if current["pending"]:
                    current["rows"].append(current["pending"])
                    current["pending"] = None
                continue
            cells = [c.strip() for c in raw.strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue  # GFM alignment row
            if current["pending"] and no in fenced:
                current["pending"] = [
                    (a + " " + b).strip() for a, b in zip(current["pending"], cells)
                ] if len(current["pending"]) == len(cells) else current["pending"]
            else:
                if current["pending"]:
                    current["rows"].append(current["pending"])
                current["pending"] = cells
        else:
            if current:
                if current["pending"]:
                    current["rows"].append(current["pending"])
                if len(current["rows"]) >= 2:
                    tables.append(current)
                current = None
    if current:
        if current["pending"]:
            current["rows"].append(current["pending"])
        if len(current["rows"]) >= 2:
            tables.append(current)
    return tables


def check_tables(fname, tables):
    findings, confirmed = [], []
    for tbl in tables:
        rows = tbl["rows"]
        width = max(len(r) for r in rows)
        grid = [[(r[i] if i < len(r) else "") for i in range(width)] for r in rows]
        numeric = {}
        for col in range(width):
            vals = [dec(strip_markup(grid[r][col])) for r in range(len(grid))]
            if sum(v is not None for v in vals) >= 3:
                numeric[col] = vals
        cols = sorted(numeric)
        for k in cols:
            dp = max((places(strip_markup(grid[r][k])) for r in range(len(grid))
                      if numeric[k][r] is not None), default=0)
            for i in cols:
                for j in cols:
                    if len({i, j, k}) != 3:
                        continue
                    ok = bad = 0
                    offenders = []
                    for r in range(len(grid)):
                        a, b, c = numeric[i][r], numeric[j][r], numeric[k][r]
                        if a is None or b is None or c is None or a == 0:
                            continue
                        want = quantise(b / a, dp)
                        if c in want:
                            ok += 1
                        else:
                            bad += 1
                            offenders.append((r, a, b, c, want[0]))
                    if ok >= 3 and ok >= 2 * bad:
                        label = (f"{fname}:{tbl['line']} колонка {k + 1} = "
                                 f"колонка {j + 1} / колонка {i + 1}")
                        if bad:
                            for r, a, b, c, want in offenders:
                                findings.append(Finding(
                                    "N1", f"`{fname}:{tbl['line']}` строка {r + 1}",
                                    f"{label}: напечатано {c}, пересчет дает {want} "
                                    f"({b} / {a})"))
                        else:
                            confirmed.append(f"{label} — все {ok} строк сходятся")
                        break
                else:
                    continue
                break
    return findings, confirmed


def check_column_totals(tables, per_file):
    """A table column whose sum is restated in the SURROUNDING prose is CONFIRMED.

    Proximity is the whole point: an integer that merely occurs somewhere else in a
    170-page book is a coincidence, not a cross-check. Only the 30 lines around the
    table can be the sentence that states its total.
    """
    by_file = {name: lines for name, lines, _f in per_file}
    confirmed = []
    for fname, tbl in tables:
        near = [(fname, [(n, t) for n, t in by_file[fname]
                         if abs(n - tbl["line"]) <= 30])]
        rows = tbl["rows"]
        width = max(len(r) for r in rows)
        for col in range(width):
            vals = []
            for r in rows:
                cell = strip_markup(r[col]) if col < len(r) else ""
                v = dec(cell)
                if v is not None and v == v.to_integral_value() and v > 0:
                    vals.append(int(v))
            if len(vals) < 3:
                continue
            total = sum(vals)
            if total < 1000:
                continue
            loci = find_value(total, near)
            if loci:
                confirmed.append(
                    f"`{fname}:{tbl['line']}` колонка {col + 1}: сумма {total:,}".replace(",", " ")
                    + f" повторена в тексте (`{loci[0]}`)")
    return confirmed


# ---------------------------------------------------------------- prose (N2, N3)

def check_prose_arithmetic(fname, lines, fenced):
    findings, confirmed = [], []
    for no, text in lines:
        if no in fenced:
            continue
        line = normalise_spaces(denoise(text))

        for rx, label in ((PCT_IZ_RE, "«X из Y (Z %)»"), (PCT_SLASH_RE, "«X/Y (Z %)»")):
            for m in rx.finditer(line):
                a, b, p = dec(m.group(1)), dec(m.group(2)), dec(m.group(3))
                if not a or not b or p is None or b == 0:
                    continue
                dp = places(m.group(3))
                want = quantise(a / b * 100, dp)
                if p in want:
                    confirmed.append(f"`{fname}:{no}` {label}: {m.group(0).strip()}")
                else:
                    findings.append(Finding(
                        "N2", f"`{fname}:{no}`",
                        f"{label}: напечатано {m.group(3)} %, пересчет дает {want[0]} % "
                        f"({m.group(1).strip()} / {m.group(2).strip()})"))

        for m in SUM_RE.finditer(line):
            a, b, c = dec(m.group(1)), dec(m.group(2)), dec(m.group(3))
            if a is None or b is None or c is None:
                continue
            if a + b == c:
                confirmed.append(f"`{fname}:{no}` сумма: {m.group(0).strip()}")
            else:
                findings.append(Finding(
                    "N3", f"`{fname}:{no}`",
                    f"«{m.group(0).strip()}»: {a} + {b} = {a + b}, а не {c}"))
    return findings, confirmed


# ---------------------------------------------------------------- cross-refs (N4)

def illustration_block(main_lines):
    """(start, end) line numbers of «Список иллюстративного материала», or (None, None).

    Its rows LOOK exactly like captions («Таблица 5 Распределение… 122»), so the block
    must be excluded from caption collection — otherwise the list silently vouches for
    itself and a caption missing from the body is never noticed.
    """
    start = end = None
    for no, text in main_lines:
        if text.strip() == ILLUSTRATION_HEADING:
            start = no
        elif start is not None and text.startswith("# "):
            end = no
            break
    return start, (end or (main_lines[-1][0] + 1 if main_lines else None))


def build_targets(per_file, skip_main=(None, None)):
    """Section numbers, chapter numbers and captions that actually exist."""
    sections, chapters, captions = {}, {}, defaultdict(dict)
    lo, hi = skip_main
    for fname, lines, fenced in per_file:
        for no, text in lines:
            if no in fenced:
                continue
            if fname == MAIN_TEXT and lo and lo <= no < hi:
                continue
            hm = HEADING_RE.match(text)
            if hm:
                head = strip_markup(hm.group("text"))
                sm = SECTION_NO_RE.match(head)
                if sm:
                    sections.setdefault(sm.group("num"), f"{fname}:{no}")
                cm = CHAPTER_RE.match(head)
                if cm:
                    chapters.setdefault(cm.group("num"), f"{fname}:{no}")
                am = APPENDIX_HEAD_RE.match(head)
                if am:
                    captions["Приложение"].setdefault(am.group("num"), f"{fname}:{no}")
                continue
            cap = CAPTION_RE.match(strip_markup(text))
            if cap and fname == MAIN_TEXT:
                captions[cap.group("kind")].setdefault(cap.group("num"), f"{fname}:{no}")
    return sections, chapters, captions


def appendix_numbers(per_file):
    """Appendix numbers declared in the «Состав приложений» table."""
    out = {}
    for fname, lines, _fenced in per_file:
        for no, text in lines:
            raw = normalise_spaces(text.strip())
            if raw.startswith("|"):
                cells = [c.strip() for c in raw.strip("|").split("|")]
                if cells and cells[0].isdigit():
                    out.setdefault(cells[0], f"{fname}:{no}")
    return out


def check_crossrefs(per_file, sections, chapters, captions, appendices, skip_main):
    findings = []
    lo, hi = skip_main
    missing = defaultdict(list)
    for fname, lines, fenced in per_file:
        for no, text in lines:
            if no in fenced:
                continue
            if fname == MAIN_TEXT and lo and lo <= no < hi:
                continue  # the list of illustrations is an index, not a reference
            line = normalise_spaces(denoise(text))
            for rx, kind, table in (
                (REF_SECTION_RE, "§", sections),
                (REF_RAZDEL_RE, "раздел", sections),
                (REF_CHAPTER_RE, "Глава", chapters),
                (REF_TABLE_RE, "Таблица", captions["Таблица"]),
                (REF_FIGURE_RE, "Рисунок", captions["Рисунок"]),
                (REF_APPENDIX_RE, "Приложение", appendices),
            ):
                for m in rx.finditer(line):
                    num = m.group(1)
                    if num in table:
                        continue
                    if kind == "§" and "." not in num and num in chapters:
                        continue  # «§3» addresses the whole chapter
                    if EXTERNAL_REF_RE.search(line[:m.start()]):
                        continue  # the § belongs to another document
                    missing[(kind, num)].append(f"{fname}:{no}")

    for (kind, num), loci in sorted(missing.items()):
        uniq = sorted(dict.fromkeys(loci))
        findings.append(Finding(
            "N4", ", ".join(f"`{x}`" for x in uniq[:6]) + (" …" if len(uniq) > 6 else ""),
            f"ссылка «{kind} {num}» не разрешается: заголовка или подписи с таким "
            f"номером в рукописи нет ({len(loci)} вхожд.)"))
    return findings


def check_illustration_list(main_lines, captions, block):
    """The list of illustrations against the captions actually printed."""
    findings = []
    start, end = block
    if start is None:
        return findings

    listed = {}
    for no, text in main_lines:
        if no <= start or (end and no >= end):
            continue
        m = ILLUSTRATION_ROW_RE.match(strip_markup(normalise_spaces(text)))
        if m:
            listed[(m.group("kind"), m.group("num"))] = (no, m.group("title"))

    for (kind, num), (no, title) in sorted(listed.items()):
        if num not in captions[kind]:
            findings.append(Finding(
                "N4", f"`{MAIN_TEXT}:{no}`",
                f"«{kind} {num}. {title}» стоит в списке иллюстративного материала, "
                f"но подписи «{kind} {num}» в тексте рукописи нет"))
    for kind in ("Таблица", "Рисунок"):
        for num, locus in sorted(captions[kind].items(), key=lambda kv: int(kv[0])):
            if (kind, num) not in listed:
                findings.append(Finding(
                    "N4", f"`{locus}`",
                    f"подпись «{kind} {num}» напечатана в тексте, но в списке "
                    f"иллюстративного материала не значится"))
    return findings


# ---------------------------------------------------------------- provenance (N5)

def provenance_facts():
    """[(source, dotted.key, int)] over every committed *_provenance.json."""
    facts = []
    for path in sorted(HERE.glob("*_provenance.json")):
        data = json.loads(path.read_text(encoding="utf-8"))

        def walk(node, trail):
            if isinstance(node, dict):
                for k, v in node.items():
                    walk(v, trail + [str(k)])
            elif isinstance(node, list):
                for i, v in enumerate(node):
                    walk(v, trail + [str(i)])
            elif isinstance(node, bool):
                return
            elif isinstance(node, int) and node >= 10:
                facts.append((path.name, ".".join(trail), node))

        walk(data, [])
    return facts


def check_provenance(facts, haystacks, update_map):
    findings, confirmed = [], []
    pinned = {}
    if ANCHOR_MAP.is_file():
        pinned = {e["key"]: e for e in json.loads(ANCHOR_MAP.read_text(encoding="utf-8"))["anchors"]}

    fresh = []
    for source, key, value in facts:
        full = f"{source}::{key}"
        loci = find_value(value, haystacks)
        if loci:
            fresh.append({"key": full, "value": value, "loci": loci})
            confirmed.append(f"`{full}` = {value} — цитируется в `{loci[0]}`"
                             + (f" (+{len(loci) - 1})" if len(loci) > 1 else ""))
        old = pinned.get(full)
        if old and old["value"] != value:
            findings.append(Finding(
                "N5", ", ".join(f"`{x}`" for x in old["loci"][:4]),
                f"провенанс `{full}` изменился {old['value']} -> {value}; "
                f"закрепленные локусы рукописи еще несут прежнее значение"))
        elif old and not loci:
            findings.append(Finding(
                "N5", ", ".join(f"`{x}`" for x in old["loci"][:4]),
                f"значение {value} (`{full}`) больше не встречается в рукописи, "
                f"хотя было закреплено картой"))

    if update_map:
        ANCHOR_MAP.write_text(
            json.dumps({
                "generated_by": "numbers_crosscheck.py --update-map (H2871)",
                "note": "Пин: какие числа провенанс-джейсонов цитирует рукопись и где. "
                        "Не редактировать вручную — перегенерировать.",
                "anchors": sorted(fresh, key=lambda e: e["key"]),
            }, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8", newline="\n")
    return findings, confirmed, fresh


# ---------------------------------------------------------------- drift (N6)

def check_drift(baseline, paths):
    findings = []
    for path in paths:
        rel = path.relative_to(REPO).as_posix()
        proc = subprocess.run(
            ["git", "-C", str(REPO), "show", f"{baseline}:{rel}"],
            capture_output=True, encoding="utf-8", errors="replace")
        if proc.returncode != 0:
            findings.append(Finding(
                "N6", f"`{path.name}`",
                f"нет версии `{rel}` в `{baseline}` — сравнение чисел невозможно"))
            continue
        before = Counter()
        for line in proc.stdout.split("\n"):
            before.update(integers_in(line))
        after = Counter()
        for _no, line in read_lines(path):
            after.update(integers_in(line))
        added = after - before
        removed = before - after
        if added or removed:
            def fmt(counter):
                return ", ".join(f"{v}×{n}" if n > 1 else str(v)
                                 for v, n in sorted(counter.items())[:25])
            findings.append(Finding(
                "N6", f"`{path.name}`",
                f"мультимножество чисел разошлось с `{baseline}`: "
                f"добавлено {sum(added.values())} ({fmt(added) or '—'}), "
                f"снято {sum(removed.values())} ({fmt(removed) or '—'})"))
    return findings


# ---------------------------------------------------------------- report

CODE_TITLES = {
    "N1": "Производная колонка таблицы",
    "N2": "Процент, пересчитанный по своим же слагаемым",
    "N3": "Арифметика, выписанная в тексте",
    "N4": "Внутренняя перекрестная ссылка",
    "N5": "Привязка к провенансу данных 2026 г.",
    "N6": "Дрейф чисел против базовой ревизии",
}
ORDER = ["N4", "N2", "N1", "N3", "N5", "N6"]


def render(findings, confirmed, facts, anchors, baseline, today):
    counts = Counter(f.code for f in findings)
    lines = [
        "# Сверка чисел рукописи M03 — сухой прогон",
        "",
        f"_Created: {today} · Last updated: {today}_",
        "",
        "Отчет генератора "
        "[numbers_crosscheck.py](https://github.com/gasyoun/SanskritGrammar/blob/main/"
        "GasunsDhatu_2014/revision-2026/numbers_crosscheck.py) "
        "([H2871](https://github.com/gasyoun/Uprava/blob/main/handoffs/"
        "H2871-Opus_SanskritGrammar_m03-freeze-harness-gost-numbers-prebuild_16.08.26.md)), "
        "Opus 5 (`claude-opus-5`). **Сухой прогон: рукопись не изменялась.** Находки — "
        "инвентарь к предподачному проходу, а не правки.",
        "",
        f"**Охват:** {len(MANUSCRIPT_FILES)} файлов рукописи; "
        f"{len(facts)} числовых фактов в провенанс-джейсонах, из них "
        f"{len(anchors)} закреплено за локусами рукописи; "
        f"базовая ревизия для N6 — `{baseline}`.",
        "",
        "## Классы и умолчания (политика default-and-log)",
        "",
        "| Класс | Что считается сходящимся | Умолчание |",
        "|---|---|---|",
        "| `N1` | связь «колонка = колонка / колонка» держится на всех строках | связь "
        "признается за таблицей, если ей отвечают >= 3 строк и не менее двух третей строк |",
        "| `N2` | напечатанный процент = пересчету по тем же X и Y | принимается и "
        "округление, и усечение последнего знака (усечение — засвидетельствованная "
        "практика издания, DCS-леджер H1229) |",
        "| `N3` | «A + B = C» сходится точно | — |",
        "| `N4` | номер ссылки есть среди заголовков/подписей | «§N» без дробной части "
        "адресует главу целиком |",
        "| `N5` | значение провенанса встречается в рукописи | карта "
        "[numbers_anchor_map.json](https://github.com/gasyoun/SanskritGrammar/blob/main/"
        "GasunsDhatu_2014/revision-2026/numbers_anchor_map.json) — перегенерируется "
        "флагом `--update-map`, руками не правится |",
        "| `N6` | мультимножество чисел файла совпадает с базовой ревизией | база — "
        "`origin/main`; на заморозке база меняется на ревизию «до правок» |",
        "",
        "## Сводка находок",
        "",
        "| Код | Класс | Находок |",
        "|---|---|---:|",
    ]
    for code in ORDER:
        if counts.get(code):
            lines.append(f"| `{code}` | {CODE_TITLES[code]} | {counts[code]} |")
    lines.append(f"| **Итого** | | **{len(findings)}** |")
    lines.append("")
    green = [c for c in ORDER if not counts.get(c)]
    if green:
        lines.append("**Зелено (0 находок):** "
                     + " · ".join(f"`{c}` {CODE_TITLES[c]}" for c in green) + ".")
        lines.append("")

    for code in ORDER:
        group = [f for f in findings if f.code == code]
        if not group:
            continue
        lines.append(f"## `{code}` — {CODE_TITLES[code]} ({len(group)})")
        lines.append("")
        for f in group:
            lines.append(f"- {f.locus} — {f.message}")
        lines.append("")

    lines.append(f"## Подтверждено пересчетом ({len(confirmed)})")
    lines.append("")
    lines.append("Проверки, которые сошлись. Это половина ценности прохода: на заморозке "
                 "они должны сойтись снова.")
    lines.append("")
    for item in confirmed:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Воспроизведение")
    lines.append("")
    lines.append("```")
    lines.append("cd GasunsDhatu_2014/revision-2026 && python numbers_crosscheck.py")
    lines.append("```")
    lines.append("")
    lines.append("_Dr. Mārcis Gasūns_")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=None)
    ap.add_argument("--stdout", action="store_true", help="print the report, write nothing")
    ap.add_argument("--update-map", action="store_true",
                    help="regenerate numbers_anchor_map.json from this run")
    ap.add_argument("--baseline", default="origin/main",
                    help="git revision the N6 numeric multiset is compared against")
    args = ap.parse_args()

    paths = manuscript_paths()
    per_file = []
    haystacks = []
    for path in paths:
        raw = read_lines(path)
        fenced = fenced_ranges(raw)
        body = strip_frontmatter(raw)
        per_file.append((path.name, body, fenced))
        haystacks.append((path.name, body))

    findings, confirmed = [], []
    all_tables = []
    for fname, lines, fenced in per_file:
        tables = parse_tables(lines, fenced)
        all_tables.extend((fname, t) for t in tables)
        f, c = check_tables(fname, tables)
        findings += f
        confirmed += c
        f, c = check_prose_arithmetic(fname, lines, fenced)
        findings += f
        confirmed += c
    confirmed += check_column_totals(all_tables, per_file)

    block = illustration_block(per_file[0][1])
    sections, chapters, captions = build_targets(per_file, skip_main=block)
    appendices = appendix_numbers(per_file)
    findings += check_crossrefs(per_file, sections, chapters, captions, appendices, block)
    findings += check_illustration_list(per_file[0][1], captions, block)

    facts = provenance_facts()
    f, c, anchors = check_provenance(facts, haystacks, args.update_map)
    findings += f
    confirmed += c

    findings += check_drift(args.baseline, paths)

    today = date.today().strftime("%d-%m-%Y")
    report = render(findings, confirmed, facts, anchors, args.baseline, today)

    if args.stdout:
        print(report)
    else:
        out = HERE / (args.out or "NUMBERS_CROSSCHECK_DRYRUN_REPORT.md")
        out.write_text(report, encoding="utf-8", newline="\n")
        print(f"{len(findings)} findings, {len(confirmed)} confirmed -> {out}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
