#!/usr/bin/env python
"""gost_bibliography_check.py — pre-submission ГОСТ pass for the M03 monograph (H2871).

ONE of the two passes that stand between the author's docx review (H1259) and the
31-10-2026 working freeze. It reports; it never edits. The manuscript is human-owned
prose (H275) and the review docx must stay stable under the author, so this script
opens the `.mdx` read-only and writes a dated `.md` report beside itself.

WHAT IT CHECKS

  Bibliography form — ГОСТ Р 7.0.100-2018 «Библиографическая запись.
  Библиографическое описание»:

    G1  numbering integrity — duplicate or missing entry numbers (4.3: each record
        in a numbered list is cited by its number, so a duplicate number makes an
        in-text numeric reference ambiguous)
    G2  sigil year vs imprint year — the bold `**Автор** ГОД` sigil that in-text
        citations resolve against must match the year in the publication area (5.4.6)
    G3  prescribed punctuation of the publication area — «Место : Издательство, Год»
        takes SPACE-colon-SPACE (4.5.4 предписанная пунктуация); `Poona: Deccan` is
        the typewriter form and is corrected at the ГОСТ pass
    G4  area separator — each new area opens with `. —` (4.5.4). The manuscript
        encodes the em dash as pandoc `--`, so the target form is `. -- `
    G5  initials — `Фамилия И. О.` with a space between initials (4.5.4/5.2: the
        initials are separate elements); `Бетлинг О.Н.` is the violation
    G6  terminal full stop — a record ends with `.` (4.5.4)
    G7  hyphen artefacts — `--` BETWEEN LETTERS is an OCR/pandoc dash artefact
        (`Изд--во`, `Пор--Рояля`); between digits it is a legitimate range
    G8  analytic records — an entry with ` // ` must locate the part inside the whole
        with `С. x--y` / `P. x--y` / `Вып.` / `Т.` (ГОСТ Р 7.0.100-2018, 7:
        аналитическое библиографическое описание)
    G9  publisher absent — «Место, Год» with no publisher; ГОСТ wants `[б. и.]`
    G10 markup residue — HTML entities and stray angle brackets left by the 2014
        Word→pandoc conversion, which the print house will typeset literally
    G11 sigil not set in bold, unlike the rest of the list (4.4, uniformity)
    G12 bold emphasis closed and reopened inside the sigil (`**Красухин** 2004a** **--`)
    G0  entry that does not parse as «сигла -- описание» at all

  Reference integrity — in-text `[Автор Год, стр.]` against the bibliography and
  against «Принятые сокращения»:

    R1  citation with no bibliography entry (dangling reference)
    R2  bibliography entry never cited anywhere in the manuscript (dead entry)
    R3  citation that matches an entry only after reordering the surnames or
        normalising the year range — a soft mismatch a human resolves in one look
    A1  source abbreviation whose target has no bibliography entry
    A2  citation through an abbreviation whose year falls outside the range the
        abbreviation declares

AMBIGUITY POLICY (H2871 autonomy contract): default-and-log. Where ГОСТ admits more
than one profile for a source type, the script takes the ONE profile named in the
check's docstring above, cites the clause, and logs the decision in the report
preamble rather than asking.

USAGE
    python gost_bibliography_check.py                 # dry run, writes the dated report
    python gost_bibliography_check.py --stdout        # report to stdout, write nothing
    python gost_bibliography_check.py --out REPORT.md

EXIT CODES
    0  no findings          1  findings reported          2  could not run
"""
import argparse
import re
import sys
from collections import Counter, defaultdict
from datetime import date

from m03_checkers_common import (
    HERE,
    MAIN_TEXT,
    MANUSCRIPT_FILES,
    denoise,
    fenced_ranges,
    manuscript_paths,
    normalise_spaces,
    read_lines,
    strip_frontmatter,
    strip_markup,
)

BIB_HEADING = "# Библиография"
ENTRY_RE = re.compile(r"^(?P<num>\d+)\.\s+(?P<body>\S.*)$")

# A year token: 1500–2049, optionally letter-disambiguated (`2004a`) and optionally a
# range (`1879--1889`, `1953--61`). Restricting the century range is what stops a page
# reference such as «MW 1132» being read as a citation year.
YEAR = r"(?:1[5-9]\d{2}|20[0-4]\d)[a-zа-яё]?(?:\s*(?:--|–|—|-|/)\s*\d{2,4}[a-zа-яё]?)?"
SIGIL_BOLD_RE = re.compile(
    r"^(?P<names>(?:[a-zа-яё]{2,4}\s+)?\*\*[^*]+\*\*(?:\s*,?\s*(?:[a-zа-яё]{2,4}\s+)?"
    r"\*\*[^*]+\*\*)*)"
    rf"\s+(?P<year>{YEAR})\s*--\s*(?P<desc>.*)$"
)
SIGIL_PLAIN_RE = re.compile(
    rf"^(?P<names>[^\d*]{{2,80}}?)\s+(?P<year>{YEAR})\s*--\s*(?P<desc>.*)$"
)
NAME_RE = re.compile(r"\*\*([^*]+)\*\*")
DASH_YEAR_RE = re.compile(r"\b(1[5-9]\d{2}|20[0-4]\d)\b")
INITIALS_TIGHT_RE = re.compile(r"[А-ЯЁA-ZÄÖÜŚṢṚṄÑ]\.[А-ЯЁA-ZÄÖÜŚṢṚṄÑ]\.")
LETTER_DASH_RE = re.compile(r"(?<=[^\W\d_])--(?=[^\W\d_])", re.UNICODE)
ENTITY_RE = re.compile(r"&(?:lt|gt|amp|quot|nbsp|#\d+);")
PLACE_TIGHT_RE = re.compile(r"([^\s:;/]+):(?=\s)")
# `**Красухин** 2004a** **--`, `**Monier**--**Williams**`, `**Бодуэн** **де Куртенэ**`:
# the 2014 Word source closes and reopens bold mid-sigil. Collapsing the seam gives a
# parseable sigil; the seam itself is reported as G12.
BOLD_SEAM_RE = re.compile(r"\*\*(\s*|--)\*\*")
ABBR_HEADING = "# Принятые сокращения"
ABBR_RE = re.compile(r"^(?:>\s*)?(?P<abbr>[^\s—]{1,10}?)\s+--\s+(?P<target>\S.*)$")
CITE_BRACKET_RE = re.compile(r"\[([^\[\]]+)\]")
# Surnames are the trailing run of capitalised tokens immediately before the year, so a
# citation embedded in prose («цит. по Chakravarti 1919», «другую точку зрения у
# Lazzeroni 1998») yields the surname alone rather than the whole run-in phrase.
UPPER = "A-ZА-ЯЁÄÖÜÉÈÁÍÓÚÀÇŚṢṚṆṬḌÑČŠŽŌĀĪŪḤṀṄŚ"
NAME_TOKEN = rf"(?:[a-zа-яё]{{2,4}}\s+)?[{UPPER}][^\s,;\[\]]*"
CITE_BODY_RE = re.compile(
    rf"(?P<names>{NAME_TOKEN}(?:\s*,\s*{NAME_TOKEN})*)\s+(?P<year>{YEAR})(?![\d])"
)


def norm_year(raw):
    """'1879--1889' / '1879–1889' -> '1879-1889'; '1953--61' -> '1953-1961'."""
    raw = normalise_spaces(raw)
    raw = re.sub(r"\s*(?:--|–|—|-)\s*", "-", raw.strip())
    parts = raw.split("-")
    if len(parts) == 2 and len(parts[1]) == 2 and len(parts[0]) >= 4:
        parts[1] = parts[0][:2] + parts[1]  # 1953--61 -> 1953-1961
    return "-".join(parts)


def bare_year(raw):
    """Year key with the disambiguating letter dropped — for soft (R3) matching."""
    return re.sub(r"(?<=\d)[a-zа-яё]", "", norm_year(raw))


def norm_name(raw):
    """Surname as it keys a citation: markup off, spaces collapsed, case folded."""
    return re.sub(r"\s+", " ", strip_markup(raw)).strip(" .,").casefold()


def entry_key(names, year):
    return "|".join(names) + "@" + norm_year(year)


def set_key(names, year):
    return "|".join(sorted(names)) + "@" + bare_year(year)


class Finding:
    __slots__ = ("code", "locus", "message", "clause")

    def __init__(self, code, locus, message, clause=""):
        self.code = code
        self.locus = locus
        self.message = message
        self.clause = clause


def parse_bibliography(lines):
    """(entries, start_line). Entry = dict(num, names, year, desc, raw, line)."""
    start = None
    for no, text in lines:
        if text.strip() == BIB_HEADING:
            start = no
            break
    if start is None:
        raise SystemExit(f"{BIB_HEADING} heading not found in {MAIN_TEXT}")

    entries = []
    for no, text in lines:
        if no <= start:
            continue
        m = ENTRY_RE.match(normalise_spaces(text))
        if not m:
            continue
        body = m.group("body")
        mended = BOLD_SEAM_RE.sub(r"\1", body)
        entry = {
            "num": int(m.group("num")),
            "line": no,
            "raw": body,
            "names": [],
            "display": strip_markup(body)[:60],
            "year": "",
            "desc": body,
            "bold_sigil": True,
            "bold_seam": mended != body,
        }
        sig = SIGIL_BOLD_RE.match(mended)
        if not sig:
            sig = SIGIL_PLAIN_RE.match(mended)
            entry["bold_sigil"] = False
        if sig:
            raw_names = sig.group("names")
            parts = NAME_RE.findall(raw_names) or [raw_names]
            entry["names"] = [norm_name(n) for n in parts if norm_name(n)]
            entry["display"] = ", ".join(strip_markup(n) for n in parts)
            entry["year"] = sig.group("year")
            entry["desc"] = sig.group("desc")
        entries.append(entry)
    return entries, start


def check_entries(entries):
    findings = []

    # G1 — numbering integrity
    counts = Counter(e["num"] for e in entries)
    by_num = defaultdict(list)
    for e in entries:
        by_num[e["num"]].append(e)
    for num, n in sorted(counts.items()):
        if n > 1:
            loci = ", ".join(f"`{MAIN_TEXT}:{e['line']}`" for e in by_num[num])
            findings.append(Finding(
                "G1", loci,
                f"номер {num} использован {n} раза — числовая ссылка на него неоднозначна",
                "ГОСТ Р 7.0.100-2018, 4.3"))
    if entries:
        highest = max(counts)
        missing = [n for n in range(1, highest + 1) if n not in counts]
        if missing:
            findings.append(Finding(
                "G1", f"`{MAIN_TEXT}` (список)",
                f"пропущено {len(missing)} номеров в диапазоне 1--{highest}: "
                + ", ".join(str(n) for n in missing[:40])
                + (" …" if len(missing) > 40 else ""),
                "ГОСТ Р 7.0.100-2018, 4.3"))

    for e in entries:
        locus = f"`{MAIN_TEXT}:{e['line']}`"
        head = strip_markup(e["raw"])[:90]
        desc = e["desc"]

        # G12 — bold emphasis closed and reopened inside the sigil
        if e["bold_seam"]:
            findings.append(Finding(
                "G12", locus,
                f"запись {e['num']}: полужирное выделение сиглы разорвано "
                f"(`{e['raw'][:60]}`) — верстка воспроизведет разрыв",
                "оформительский дефект конвертации 2014 г."))

        if not e["year"]:
            findings.append(Finding(
                "G0", locus,
                f"запись {e['num']} не разбирается как «**Автор** ГОД -- описание»: {head}",
                "ГОСТ Р 7.0.100-2018, 4.4 — единообразие формы записи"))
            continue

        # G11 — the sigil must be set in bold, as everywhere else in the list
        if not e["bold_sigil"]:
            findings.append(Finding(
                "G11", locus,
                f"запись {e['num']}: сигла «{e['display']} {norm_year(e['year'])}» "
                f"не выделена полужирным — единообразие списка нарушено",
                "единообразие оформления списка; ГОСТ Р 7.0.100-2018, 4.4"))

        # G2 — sigil year vs imprint year
        imprint_years = {norm_year(y) for y in DASH_YEAR_RE.findall(desc)}
        sig_years = set(norm_year(e["year"]).split("-"))
        if imprint_years and not (sig_years & imprint_years):
            findings.append(Finding(
                "G2", locus,
                f"запись {e['num']}: сигла «{norm_year(e['year'])}» не совпадает ни с одним "
                f"годом в описании ({', '.join(sorted(imprint_years))}) — {head}",
                "ГОСТ Р 7.0.100-2018, 5.4.6"))

        # G3 — prescribed punctuation: a colon separating areas/elements takes a space
        # on BOTH sides, in the imprint («Место : Издательство») exactly as in the
        # title area («Заглавие : сведения, относящиеся к заглавию»).
        tight_colons = PLACE_TIGHT_RE.findall(desc)
        if tight_colons:
            samples = [s.strip() for s in tight_colons[:3]]
            findings.append(Finding(
                "G3", locus,
                f"запись {e['num']}: {len(tight_colons)} двоеточи"
                f"{'е' if len(tight_colons) == 1 else 'й'} без пробела слева "
                f"({'; '.join(f'«{s}:»' for s in samples)}) — предписанная пунктуация "
                f"требует «X : Y»",
                "ГОСТ Р 7.0.100-2018, 4.5.4 (предписанная пунктуация)"))

        # G4 — area separator `. -- `
        seps = len(re.findall(r"(?<!\.)\s--\s", desc))
        if seps:
            findings.append(Finding(
                "G4", locus,
                f"запись {e['num']}: {seps} разделител{'ь' if seps == 1 else 'ей'} области "
                f"без предшествующей точки (нужно «. -- ») — {head}",
                "ГОСТ Р 7.0.100-2018, 4.5.4"))

        # G5 — initials
        tight = INITIALS_TIGHT_RE.findall(desc)
        if tight:
            findings.append(Finding(
                "G5", locus,
                f"запись {e['num']}: инициалы без пробела ({', '.join(sorted(set(tight))[:4])}) "
                f"— требуется «Фамилия И. О.»",
                "ГОСТ Р 7.0.100-2018, 4.5.4"))

        # G6 — terminal full stop
        if not desc.rstrip().endswith((".", ".)", ".»")):
            findings.append(Finding(
                "G6", locus,
                f"запись {e['num']} не закрыта точкой — {head}",
                "ГОСТ Р 7.0.100-2018, 4.5.4"))

        # G7 — letter--letter dash artefacts
        arte = LETTER_DASH_RE.findall(desc)
        if arte:
            samples = re.findall(r"[^\W\d_]+--[^\W\d_]+", desc, re.UNICODE)
            findings.append(Finding(
                "G7", locus,
                f"запись {e['num']}: {len(arte)} внутрисловн{'ое' if len(arte) == 1 else 'ых'} "
                f"«--» — артефакт конвертации ({', '.join(sorted(set(samples))[:4])})",
                "оформительский дефект, не предусмотренный ГОСТ Р 7.0.100-2018"))

        # G8 — analytic record must locate the part
        if " // " in desc and not re.search(r"(?:С|P|S|Pp|СС)\.\s*\d|Вып\.|Т\.\s*[IVXL0-9]", desc):
            findings.append(Finding(
                "G8", locus,
                f"запись {e['num']}: аналитическое описание без указания местоположения "
                f"части («-- С. x--y») — {head}",
                "ГОСТ Р 7.0.100-2018, 7"))

        # G9 — publisher absent
        if re.search(r"--\s*[^:,;/]{2,40},\s*(?:1[5-9]\d{2}|20[0-4]\d)\s*\.?\s*$", desc) \
                and ":" not in desc.split("--")[-1]:
            findings.append(Finding(
                "G9", locus,
                f"запись {e['num']}: издательство не указано — по ГОСТ ставится «[б. и.]» "
                f"— {head}",
                "ГОСТ Р 7.0.100-2018, 5.4.5"))

        # G10 — markup residue
        residue = ENTITY_RE.findall(e["raw"])
        if residue:
            findings.append(Finding(
                "G10", locus,
                f"запись {e['num']}: HTML-сущности из конвертации 2014 г. "
                f"({', '.join(sorted(set(residue)))}) — наборщик воспроизведет их буквально",
                "оформительский дефект"))

    return findings


def parse_abbreviations(lines):
    """«Принятые сокращения» as {abbr_key: {names, year, line, raw}}.

    Only the entries that name a source (`EWA -- Mayrhofer 1986--2001`) are kept —
    the grammatical abbreviations (`Abl.`, `sg.`) resolve to nothing and are skipped.
    """
    start = end = None
    for no, text in lines:
        if text.strip() == ABBR_HEADING:
            start = no
        elif start is not None and text.startswith("# "):
            end = no
            break
    if start is None:
        return {}

    out = {}
    for no, text in lines:
        if no <= start or (end and no >= end):
            continue
        m = ABBR_RE.match(normalise_spaces(text).rstrip("\\").strip())
        if not m:
            continue
        target = m.group("target")
        tm = CITE_BODY_RE.search(target)
        if not tm:
            continue
        parts = [p.strip() for p in tm.group("names").split(",") if p.strip()]
        out[abbr_key(m.group("abbr"))] = {
            "abbr": m.group("abbr"),
            "names": [norm_name(p) for p in parts if norm_name(p)],
            "display": ", ".join(strip_markup(p) for p in parts),
            "year": tm.group("year"),
            "line": no,
        }
    return out


def abbr_key(raw):
    return strip_markup(raw).strip(" .,").casefold()


def year_span(raw):
    """(first, last) integer years of a normalised year token."""
    digits = [int(p[:4]) for p in norm_year(raw).split("-") if p[:4].isdigit()]
    if not digits:
        return None
    return min(digits), max(digits)


def collect_citations(paths):
    """[(file, line, names_tuple, display, year)] for every in-text bracketed citation."""
    out = []
    for path in paths:
        raw_lines = read_lines(path)
        fenced = fenced_ranges(raw_lines)
        for no, text in strip_frontmatter(raw_lines):
            if no in fenced or text.startswith(("|", "+--", "```")):
                continue
            clean = normalise_spaces(denoise(text))
            for bm in CITE_BRACKET_RE.finditer(clean):
                inner = bm.group(1)
                if inner.startswith("^") or not inner.strip():
                    continue
                for chunk in inner.split(";"):
                    cm = CITE_BODY_RE.search(chunk)
                    if not cm:
                        continue
                    raw_names = cm.group("names")
                    # A Latin particle belongs to the surname (`de Saussure`,
                    # `van Nooten`); a Cyrillic lowercase word before it is running
                    # prose («по Nooten, Holland 1994») and is dropped.
                    raw_names = re.sub(r"^[а-яё]{1,4}\s+", "", raw_names)
                    parts = [p.strip() for p in raw_names.split(",") if p.strip()]
                    names = [norm_name(p) for p in parts if norm_name(p)]
                    if not names or any(len(n) < 2 for n in names):
                        continue
                    display = ", ".join(strip_markup(p) for p in parts)
                    out.append((path.name, no, tuple(names), display, cm.group("year")))
    return out


def check_references(entries, citations, abbrevs):
    findings = []
    exact = {entry_key(e["names"], e["year"]) for e in entries if e["year"]}
    loose = defaultdict(list)
    for e in entries:
        if e["year"]:
            loose[set_key(e["names"], e["year"])].append(e)
    surname_year = defaultdict(list)
    for e in entries:
        if e["year"]:
            for n in e["names"]:
                surname_year[(n, norm_year(e["year"]))].append(e)

    # A1 — every source abbreviation must resolve to a bibliography entry
    for key, ab in sorted(abbrevs.items()):
        if not any(set_key(ab["names"], ab["year"]) == set_key(e["names"], e["year"])
                   for e in entries if e["year"]):
            findings.append(Finding(
                "A1", f"`{MAIN_TEXT}:{ab['line']}`",
                f"сокращение «{ab['abbr']}» отсылает к «{ab['display']} "
                f"{norm_year(ab['year'])}», записи с такой сиглой в библиографии нет",
                "ГОСТ Р 7.0.100-2018, 4.2 — список источников замкнут"))

    cited_exact = set()
    dangling = defaultdict(list)
    soft = defaultdict(list)
    abbr_year = defaultdict(list)
    for fname, no, names, display, year in citations:
        locus = f"{fname}:{no}"
        key = entry_key(list(names), year)
        if key in exact:
            cited_exact.add(key)
            continue

        # An abbreviation from «Принятые сокращения» stands for its target entry.
        ab = abbrevs.get(abbr_key(display)) if len(names) == 1 else None
        if ab:
            for e in entries:
                if e["year"] and set_key(e["names"], e["year"]) == set_key(ab["names"], ab["year"]):
                    cited_exact.add(entry_key(e["names"], e["year"]))
            span, cite = year_span(ab["year"]), year_span(year)
            if span and cite and not (span[0] <= cite[0] and cite[1] <= span[1]):
                abbr_year[(display, norm_year(year), ab["abbr"], norm_year(ab["year"]))].append(locus)
            continue

        skey = set_key(list(names), year)
        if skey in loose:
            for e in loose[skey]:
                cited_exact.add(entry_key(e["names"], e["year"]))
            soft[(display, norm_year(year), "порядок фамилий / буквенный индекс года")].append(locus)
            continue
        hit = surname_year.get((names[-1], norm_year(year)))
        if hit:
            for e in hit:
                cited_exact.add(entry_key(e["names"], e["year"]))
            soft[(display, norm_year(year), "состав фамилий")].append(locus)
            continue
        dangling[(display, norm_year(year))].append(locus)

    def loci_str(loci):
        uniq = sorted(dict.fromkeys(loci))
        return ", ".join(f"`{x}`" for x in uniq[:6]) + (" …" if len(uniq) > 6 else "")

    for (display, year), loci in sorted(dangling.items()):
        findings.append(Finding(
            "R1", loci_str(loci),
            f"ссылка [{display} {year}] не имеет записи в библиографии "
            f"({len(loci)} вхожд.)",
            "ГОСТ Р 7.0.5-2008, 6.2 — ссылка должна разрешаться в список"))

    for (display, year, abbr, target), loci in sorted(abbr_year.items()):
        findings.append(Finding(
            "A2", loci_str(loci),
            f"ссылка [{display} {year}] называет год вне диапазона сокращения "
            f"«{abbr} -- … {target}» ({len(loci)} вхожд.) — сверить с «Принятыми сокращениями»",
            "ГОСТ Р 7.0.5-2008, 6.2"))

    for (display, year, kind), loci in sorted(soft.items()):
        findings.append(Finding(
            "R3", loci_str(loci),
            f"ссылка [{display} {year}] разрешается в библиографию только "
            f"после нормализации ({kind}) — сверить вручную",
            "ГОСТ Р 7.0.5-2008, 6.2"))

    for e in entries:
        if not e["year"]:
            continue
        if entry_key(e["names"], e["year"]) not in cited_exact:
            findings.append(Finding(
                "R2", f"`{MAIN_TEXT}:{e['line']}`",
                f"запись {e['num']} [{e['display']} {norm_year(e['year'])}] "
                f"не цитируется в рукописи",
                "ГОСТ Р 7.0.100-2018, 4.2 — список содержит использованные источники"))
    return findings


CODE_TITLES = {
    "G1": "Нумерация списка",
    "G2": "Год сиглы против года выходных данных",
    "G3": "Двоеточие без пробела слева (предписанная пунктуация)",
    "G4": "Разделитель области «. --»",
    "G5": "Пробел между инициалами",
    "G6": "Завершающая точка записи",
    "G7": "Внутрисловное «--» (артефакт конвертации)",
    "G8": "Аналитическое описание без локализации части",
    "G9": "Издательство не указано",
    "G10": "HTML-сущности из конвертации 2014 г.",
    "G11": "Сигла не выделена полужирным",
    "G12": "Разрыв полужирного выделения сиглы",
    "G0": "Запись не разбирается как «сигла -- описание»",
    "A1": "Сокращение без записи в библиографии",
    "A2": "Год ссылки вне диапазона сокращения",
    "R1": "Ссылка без записи в библиографии",
    "R2": "Запись библиографии без ссылок в тексте",
    "R3": "Ссылка разрешается только после нормализации",
}
ORDER = ["R1", "A1", "A2", "G0", "G2", "G1", "G6", "G8", "G9", "G10", "G11", "G12",
         "G3", "G4", "G5", "G7", "R3", "R2"]


def render(findings, entries, citations, abbrevs, today):
    counts = Counter(f.code for f in findings)
    lines = [
        "# ГОСТ-проход по библиографии M03 — сухой прогон",
        "",
        f"_Created: {today} · Last updated: {today}_",
        "",
        "Отчет генератора "
        "[gost_bibliography_check.py](https://github.com/gasyoun/SanskritGrammar/blob/main/"
        "GasunsDhatu_2014/revision-2026/gost_bibliography_check.py) "
        "([H2871](https://github.com/gasyoun/Uprava/blob/main/handoffs/"
        "H2871-Opus_SanskritGrammar_m03-freeze-harness-gost-numbers-prebuild_16.08.26.md)), "
        "Opus 5 (`claude-opus-5`). **Сухой прогон: рукопись не изменялась.** Находки — "
        "инвентарь к предподачному проходу, а не правки: текст рукописи авторский (H275), "
        "review-docx H1259 под автором и не перегенерируется.",
        "",
        f"**Охват:** {len(entries)} записей библиографии, "
        f"{len(citations)} внутритекстовых ссылок в "
        f"{len({c[0] for c in citations})} файлах рукописи из {len(MANUSCRIPT_FILES)}; "
        f"источниковых сокращений в «Принятых сокращениях» — {len(abbrevs)}.",
        "",
        "## Принятые умолчания (политика default-and-log)",
        "",
        "| Неоднозначность | Принято | Основание |",
        "|---|---|---|",
        "| Форма тире в рукописи | pandoc-овское `--` считается за `—` | исходник — `.mdx`, "
        "тире набирается двумя дефисами во всем тексте |",
        "| Профиль описания | одноуровневое описание монографии; аналитическое — при `//` | "
        "ГОСТ Р 7.0.100-2018, 5 и 7 |",
        "| Ключ ссылки | «фамилия(и) + год» сиглы `**Автор** ГОД` | ссылочный аппарат "
        "рукописи авторский, номерных ссылок в тексте нет |",
        "| Диапазон годов | `1953--61` разворачивается в `1953-1961` | ГОСТ Р 7.0.100-2018, "
        "5.4.6 (полная форма года) |",
        "| Пропуск номера в списке | считается находкой, а не нормой | номер — точка входа "
        "для ссылки и для верстки |",
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
        clause = group[0].clause
        if clause:
            lines.append(f"> Основание: {clause}")
            lines.append("")
        for f in group:
            lines.append(f"- {f.locus} — {f.message}")
        lines.append("")

    lines.append("## Воспроизведение")
    lines.append("")
    lines.append("```")
    lines.append("cd GasunsDhatu_2014/revision-2026 && python gost_bibliography_check.py")
    lines.append("```")
    lines.append("")
    lines.append("_Dr. Mārcis Gasūns_")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default=None, help="report path (default: dated .md beside this script)")
    ap.add_argument("--stdout", action="store_true", help="print the report, write nothing")
    args = ap.parse_args()

    paths = manuscript_paths()
    main_lines = strip_frontmatter(read_lines(paths[0]))
    entries, _start = parse_bibliography(main_lines)
    if not entries:
        print("no bibliography entries parsed", file=sys.stderr)
        return 2

    abbrevs = parse_abbreviations(main_lines)
    citations = collect_citations(paths)
    findings = check_entries(entries) + check_references(entries, citations, abbrevs)

    today = date.today().strftime("%d-%m-%Y")
    report = render(findings, entries, citations, abbrevs, today)

    if args.stdout:
        print(report)
    else:
        out = HERE / (args.out or "GOST_BIBLIOGRAPHY_DRYRUN_REPORT.md")
        out.write_text(report, encoding="utf-8", newline="\n")
        print(f"{len(findings)} findings -> {out}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
