#!/usr/bin/env python
"""harvest_quantifiers.py — auto-proxy quantifier tagger for the gradation-metalanguage
register (H800).

Companion to the claim register (H768): where `claims.yml` catalogues *falsifiable
grammatical assertions*, the quantifier register catalogues every *quantifier* — the
metalanguage word a grammarian uses to scope a rule (редко / обычно / только / некоторые /
могут / всегда …) — and tags each instance ANCHORED or UNANCHORED.

    anchored  = the quantifier sits within N tokens of a DECIDABLE target: a named класс /
                тип / § / rule / percentage / numbered category / cited affix. A learner can
                in principle check it.
    unanchored = the quantifier hangs on nothing nameable ("встречается редко" with no class,
                no section, no number) — vague, undecidable.

The thesis (H800): Zalizniak's quantifiers are anchored (he is always naming a class or §);
Kochergina's are not. The metric is ANCHOREDNESS, not raw count.

This is an AUTO-PROXY (D3): the anchor test is a heuristic. A stratified sample per source is
then hand-verified (see `<Book>/quantifiers.sample.yml`) and the proxy's precision/recall is
reported by `scripts/build_quantifiers.py`. Re-running never clobbers a filled sample.

Output per source: `<Book>/quantifiers.yml` (generated — do NOT hand-edit; edit this script
and re-run `npm run quantifiers`). Reads only the committed `.mdx`.

Usage:
    python scripts/harvest_quantifiers.py            # all four sources
    python scripts/harvest_quantifiers.py --emit-sample   # also (re)write sample templates
    python scripts/harvest_quantifiers.py KocherginaUchebnik_1998
"""
import sys
import re
import datetime
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TODAY = datetime.date.today().strftime("%d-%m-%Y")

ANCHOR_WINDOW = 8  # tokens either side (@DECIDE N in the handoff — start 8)

# ---------------------------------------------------------------------------
# Quantifier lexicon.  Each entry: (compiled regex, axis).  Axes follow the H800
# enum: rarity | frequency | productivity | optionality | subset | universal.
# Word boundaries are Cyrillic-aware (\b works on Cyrillic under re.UNICODE).
# Longer phrases are matched too and win over the sub-span they contain (dedup below),
# so "не всегда" is tagged once as a hedge, not double-counted as "всегда".
# ---------------------------------------------------------------------------
def _rx(p):
    return re.compile(p, re.IGNORECASE)

LEXICON_RU = [
    # rarity — the low/rare end
    (_rx(r"не\s+так\s+часто"), "rarity"),
    (_rx(r"\bредко\b"), "rarity"),
    (_rx(r"\bредк(?:ий|ая|ое|ие|их|им|ими|ого|ому|ом)\b"), "rarity"),
    (_rx(r"\bреже\b"), "rarity"),
    (_rx(r"\bизредка\b"), "rarity"),
    (_rx(r"\bнечасто\b"), "rarity"),
    (_rx(r"чрезвычайно\s+редко"), "rarity"),
    # frequency — common / mid-scale / predominance (incl. hedged "как правило")
    (_rx(r"\bчаще\s+всего\b"), "frequency"),
    (_rx(r"\bчасто\b"), "frequency"),
    (_rx(r"\bчаст(?:ый|ая|ое|ые|ого|ым|ом)\b"), "frequency"),
    (_rx(r"\bчаще\b"), "frequency"),
    (_rx(r"\bнередко\b"), "frequency"),
    (_rx(r"\bзачастую\b"), "frequency"),
    (_rx(r"\bобычно\b"), "frequency"),
    (_rx(r"\bобычн(?:ый|ая|ое|ые|ого|ым|ом)\b"), "frequency"),
    (_rx(r"\bраспространённ?\w*\b"), "frequency"),
    (_rx(r"\bраспространен\w*\b"), "frequency"),
    (_rx(r"\bпреимущественно\b"), "frequency"),
    (_rx(r"главным\s+образом"), "frequency"),
    (_rx(r"в\s+основном"), "frequency"),
    (_rx(r"\bиногда\b"), "frequency"),
    (_rx(r"как\s+правило"), "frequency"),
    (_rx(r"в\s+большинстве\s+случаев"), "frequency"),
    # productivity — regular / from-all / productive
    (_rx(r"\bпродуктивн\w*\b"), "productivity"),
    (_rx(r"\bнепродуктивн\w*\b"), "productivity"),
    (_rx(r"\bрегулярн\w*\b"), "productivity"),
    (_rx(r"\bнерегулярн\w*\b"), "productivity"),
    # optionality — can / may / optional / variant
    (_rx(r"\bмогут\b"), "optionality"),
    (_rx(r"\bможет\b"), "optionality"),
    (_rx(r"\bмогло\b|\bмогли\b"), "optionality"),
    (_rx(r"\bвозможн\w*\b"), "optionality"),
    (_rx(r"\bфакультативн\w*\b"), "optionality"),
    (_rx(r"\bвариант\w*\b"), "optionality"),
    # subset — some / few / part-of / a number of
    (_rx(r"лишь\s+от\s+части"), "subset"),
    (_rx(r"\bнекотор\w+\b"), "subset"),
    (_rx(r"\bнемноги\w+\b"), "subset"),
    (_rx(r"\bотдельн\w+\b"), "subset"),
    (_rx(r"\bбольшинств\w*\b"), "subset"),
    (_rx(r"\bменьшинств\w*\b"), "subset"),
    (_rx(r"в\s+ряде\s+(?:случаев|областей|мест)"), "subset"),
    (_rx(r"\bряд(?:\s+(?:корней|основ|глаголов|форм|имён|имен|слов))\b"), "subset"),
    (_rx(r"част(?:ь|и)\s+(?:корней|основ|глаголов|форм|слов)"), "subset"),
    # universal — all / always / only / every (+ hedges почти / не всегда)
    (_rx(r"не\s+всегда"), "universal"),
    (_rx(r"\bвсегда\b"), "universal"),
    (_rx(r"\bникогда\b"), "universal"),
    (_rx(r"\bтолько\b"), "universal"),
    (_rx(r"\bлишь\b"), "universal"),
    (_rx(r"\bединственн\w*\b(?!\s+числ)"), "universal"),  # not "единственное ЧИСЛО" (=singular)
    (_rx(r"\bлюб(?:ой|ого|ому|ая|ое|ые|ым|ом)\b"), "universal"),
    (_rx(r"\bкажд(?:ый|ого|ому|ая|ое|ым|ом)\b"), "universal"),
    (_rx(r"\bпочти\b"), "universal"),
    (_rx(r"\bвсе\b"), "universal"),
    (_rx(r"\bвсех\b"), "universal"),
    (_rx(r"\bвсем\b|\bвсеми\b|\bвсём\b"), "universal"),
    (_rx(r"\bвсяк(?:ий|ого|ая|ое|ие)\b"), "universal"),
]

LEXICON_EN = [
    (_rx(r"\brarely\b"), "rarity"),
    (_rx(r"\bseldom\b"), "rarity"),
    (_rx(r"\binfrequently\b"), "rarity"),
    (_rx(r"\bfrequently\b"), "frequency"),
    (_rx(r"\boften\b"), "frequency"),
    (_rx(r"\busually\b"), "frequency"),
    (_rx(r"\bgenerally\b"), "frequency"),
    (_rx(r"\bcommonly\b"), "frequency"),
    (_rx(r"\bpredominantly\b"), "frequency"),
    (_rx(r"\bprimarily\b"), "frequency"),
    (_rx(r"\bmostly\b"), "frequency"),
    (_rx(r"as\s+a\s+rule"), "frequency"),
    (_rx(r"for\s+the\s+most\s+part"), "frequency"),
    (_rx(r"in\s+general\b"), "frequency"),
    (_rx(r"\bproductive\w*\b"), "productivity"),
    (_rx(r"\bregular(?:ly)?\b"), "productivity"),
    (_rx(r"\bsystematic(?:ally)?\b"), "productivity"),
    (_rx(r"\bmay\b"), "optionality"),
    (_rx(r"\bcan\b"), "optionality"),
    (_rx(r"\boptional(?:ly)?\b"), "optionality"),
    (_rx(r"\bpossible\b"), "optionality"),
    (_rx(r"\bvariant\w*\b"), "optionality"),
    (_rx(r"\bsome\b"), "subset"),
    (_rx(r"\bseveral\b"), "subset"),
    (_rx(r"\bcertain\b"), "subset"),
    (_rx(r"a\s+number\s+of"), "subset"),
    (_rx(r"\bfew\b"), "subset"),
    (_rx(r"\bmajority\b"), "subset"),
    (_rx(r"\bminority\b"), "subset"),
    (_rx(r"\bmost\b"), "subset"),
    (_rx(r"not\s+always"), "universal"),
    (_rx(r"\ball\b"), "universal"),
    (_rx(r"\bevery\b"), "universal"),
    (_rx(r"\balways\b"), "universal"),
    (_rx(r"\bonly\b"), "universal"),
    (_rx(r"\bnever\b"), "universal"),
    (_rx(r"\beach\b"), "universal"),
    (_rx(r"\bsolely\b"), "universal"),
    (_rx(r"\bentirely\b"), "universal"),
    (_rx(r"\balmost\b"), "universal"),
]

# ---------------------------------------------------------------------------
# Anchor lexicon — a DECIDABLE target near the quantifier: a named класс / тип /
# § / rule / percentage / cited affix a learner could in principle check.
#
# Calibrated against the sources (12-07-2026):
#   * "класс" is matched by explicit endings so it does NOT swallow "классический"
#     (Classical Sanskrit) — that is a period label, not a grammatical class.
#   * "Ряд" is case-SENSITIVE (Zalizniak's ablaut series, capital Р) so it does not
#     fire on lower-case "в ряде случаев" (which is itself a subset quantifier).
#   * BARE digits and BARE Roman numerals are NOT anchors: calibration showed they
#     matched print dates ("II тысячелетия"), page markers and list enumerators far
#     more than grammatical references. Grammatical numbers almost always come with a
#     named category (§ 43, тип II, класс 5) which the category word anchors instead.
# Page markers [787] and leading list enumerators are stripped before the scan.
# ---------------------------------------------------------------------------
IAST = r"aāiīuūṛṝḷḹeoṁṃḥkgṅcjñṭḍṇtdnpbmyrlvśṣsh"
RYAD = re.compile(r"\bРяд[аеуы]?\b")   # case-sensitive: the ablaut series, not "в ряде"
ANCHORS_RU = [
    (_rx(r"§"), "§"),
    (_rx(r"\bкласс(?:а|е|ы|ов|у|ам|ами|ах|ификаци\w*)?\b"), "класс"),
    (_rx(r"\bтип(?:а|е|ы|ов|у|ам|ами|ах)?\b"), "тип"),
    (_rx(r"\bразряд\w*\b"), "разряд"),
    (_rx(r"\bспряжени\w*\b"), "спряжение"),
    (_rx(r"\bсклонени\w*\b"), "склонение"),
    (RYAD, "Ряд"),
    (_rx(r"\bправил(?:о|а|у|е|ах|ам)?\b"), "правило"),
    (_rx(r"\bпроцент\w*\b"), "процент"),
    (_rx(r"\d\s*%|%"), "%"),
    (_rx(r"\bп\.\s*\d"), "пункт"),
    (_rx(r"[-‑](?=[" + IAST + r"])"), "аффикс"),          # suffix cite  -tar, -sya
    (_rx(r"(?<=[" + IAST + r"])[-‑]"), "аффикс"),         # prefix cite  vi-, ud-, nis-
]
ANCHORS_EN = [
    (_rx(r"§"), "§"),
    (_rx(r"\bclass(?:es)?\b"), "class"),
    (_rx(r"\btype(?:s)?\b"), "type"),
    (_rx(r"\brow\b|\bseries\b"), "series"),
    (_rx(r"\brule(?:s)?\b"), "rule"),
    (_rx(r"\bparagraph\b|\bsection\b"), "section"),
    (_rx(r"\bpercent\w*\b|\d\s*%|%"), "percent"),
    (_rx(r"\bposition\b"), "position"),           # morphological position 1/2/3 — central to 1975
    (_rx(r"\bgrade\b|\bgu[nṇ]a\b|\bv[rṛ]ddhi\b"), "grade"),
    # NOTE: no affix anchor in English — the hyphen fires on ordinary hyphenated words
    # (Indo-European, root-variant, three-grade); cited affixes co-occur with type/series anyway.
]

PAGE_MARKER = re.compile(r"\\?\[\d{1,4}\\?\]")   # \[787\] print page numbers
LEAD_ENUM = re.compile(r"^[\s>*_]*\d{1,2}\\?[.)]\s")  # "1)", "2\)" list enumerators
DEVANAGARI = re.compile(r"[ऀ-ॿ]")
# markdown/HTML markup that otherwise splits an affix like "-**<u>dhā</u>**" so the
# affix-anchor detector cannot see the "-d…"; stripped from the anchor token stream.
MARKUP = re.compile(r"</?u>|</?mark>|<span[^>]*>|</span>|<!--.*?-->|\[\^[^\]]*\]|[*_`~#]|\\")

# gloss/vocabulary-entry shape: a headword + POS abbreviation or " - gloss".
GLOSS_LINE = re.compile(
    r"^>?\s*[*_]{0,2}[" + IAST + r"A-Za-zĀĪŪṚṜḶ̃·().ऀ-ॿ\s\-]{1,40}[*_]{0,2}\s*"
    r"(?:\b(?:adv|praep|conj|pron|num|interj|pcl|part|pf|ipf|impf|caus|pass|f|m|n|о\.н\.в)\b\.?)\s"
)
# an italic POS tag anywhere (*adv*. / *m* / *n -*) — a strong Kochergina vocab-entry signal
VOCAB_POS = re.compile(r"[*_](?:adv|praep|conj|pron|num|interj|pcl|indecl|m|f|n)[*_.,]")
EXERCISE = re.compile(r"^>?\s*(?:Упражнени|Напишите|Переведите|Прочитайте|Просклоняйте|Проспрягайте)")

# ---------------------------------------------------------------------------
SOURCES = [
    {
        "book": "KocherginaUchebnik_1998",
        "file": "KocherginaUchebnik_1998/Kochergina_unicode.mdx",
        "work": "Kochergina, Учебник санскрита, 1998",
        "lang": "ru",
        "sec_rx": re.compile(r"^Занятие\s+([IVXLC]+)\s*$"),
        "sec_search": False,
        "glossary_from": 11928,   # "# Словарь" — pure lexicon below this
        "body_from": 229,          # "Занятие I" — front-matter preface above is not grammar
    },
    {
        "book": "ZalizniakOcherk_1978",
        "file": "ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx",
        "work": "Zalizniak, Грамматический очерк санскрита, 1978",
        "lang": "ru",
        # match the § HEADING only (span-anchored), never an inline "см. § 43" reference
        "sec_rx": re.compile(r'<span id="s\d+"></span>\s*\*\*§\s*(\d+)'),
        "sec_search": True,
        "glossary_from": None,
        "body_from": 48,           # first "§ 1" heading; title/contents/changelog above
    },
    {
        "book": "ZalizniakKonspekt_2004",
        "file": "ZalizniakKonspekt_2004/zalizniak-konspekt-2015-11-X_bd_t.mdx",
        "work": "Zalizniak, Конспект грамматических сведений, 2004",
        "lang": "ru",
        "sec_rx": re.compile(r"^#{2,4}\s*\**([^*#].*?)\**\s*$"),
        "sec_search": False,
        "glossary_from": None,
        "body_from": 6,            # first "### Из исторической фонетики"
    },
    {
        "book": "ZalizniakMorphology_1975",
        "file": "ZalizniakMorphology_1975/A. Zalizniak Morphophonological Classification (English).mdx",
        "work": "Zalizniak, Morphophonological Classification of Sanskrit Verbal Roots, 1975",
        "lang": "en",
        "sec_rx": re.compile(r"^#{1,4}\s+(.*?)\s*$"),
        "sec_search": False,
        "glossary_from": None,
        "body_from": 6,            # skip the YAML front-matter + translator credit
    },
]

NE_TOLKO = re.compile(r"\bне\s*$", re.IGNORECASE)  # "не только" additive correlative → not a quantifier


def tokenize(s):
    return s.split()


def is_gloss(line, lang):
    if lang != "ru":
        return False
    body = line.strip()
    if not body or body in ("\\", ">"):
        return False
    # A vocabulary line: headword + POS abbrev, and NOT a full grammatical sentence.
    if GLOSS_LINE.match(body):
        # a real grammar sentence is long and Cyrillic-led; a gloss is short.
        return len(body) < 90
    return False


def clean_for_anchor(line):
    line = PAGE_MARKER.sub(" ", line)
    line = LEAD_ENUM.sub("", line)
    line = MARKUP.sub("", line)    # so "-**<u>dhā</u>**" -> "-dhā" (adjacency kept for the affix anchor)
    return line


def find_anchor(window_text, anchors):
    for rx, name in anchors:
        if rx.search(window_text):
            return name
    return None


def harvest(src):
    path = ROOT / src["file"]
    lines = path.read_text(encoding="utf-8").splitlines()
    lexicon = LEXICON_RU if src["lang"] == "ru" else LEXICON_EN
    anchors = ANCHORS_RU if src["lang"] == "ru" else ANCHORS_EN
    sec_rx = src["sec_rx"]
    gloss_from = src["glossary_from"]

    sec_search = src.get("sec_search", False)
    body_from = src.get("body_from", 1)

    # Global token stream (cleaned, line-break-agnostic) so the ±N-token anchor window
    # spans physical line breaks — otherwise Zalizniak's long single-line paragraphs
    # would out-anchor Kochergina's short "\"-terminated lines purely on line length.
    clean_lines = [clean_for_anchor(r) for r in lines]
    toks_per_line = [tokenize(c) for c in clean_lines]
    cum = [0]
    for tl in toks_per_line:
        cum.append(cum[-1] + len(tl))
    flat_tokens = [t for tl in toks_per_line for t in tl]

    cur_sec = None
    entries = []
    seq = 0
    for i, raw in enumerate(lines, start=1):
        m = (sec_rx.search(raw) if sec_search else sec_rx.match(raw)) if sec_rx else None
        if m:
            cur_sec = m.group(1).strip()
            if not sec_search:
                continue   # a pure heading line carries no quantifier of its own

        zone = "grammar"
        if i < body_from:
            zone = "preface"
        elif gloss_from and i >= gloss_from:
            zone = "glossary"
        elif is_gloss(raw, src["lang"]) or (src["lang"] == "ru" and VOCAB_POS.search(raw)):
            zone = "glossary"   # a vocabulary entry (POS-tagged gloss), not grammar prose
        elif EXERCISE.match(raw.lstrip()):
            zone = "exercise"   # drill instruction ("Напишите каждый…"), not a rule statement
        elif DEVANAGARI.search(raw) and len(DEVANAGARI.findall(raw)) > 12 \
                and not re.search(r"[а-яё]", raw, re.IGNORECASE):
            zone = "reading"   # a Devanagari-only verse/table line

        # gather all matches on this line, dedup nested spans (longer wins)
        raw_matches = []
        for rx, axis in lexicon:
            for mo in rx.finditer(raw):
                # "не только" is an additive correlative, not a scope quantifier
                if mo.group(0).lower() == "только" and NE_TOLKO.search(raw[:mo.start()]):
                    continue
                raw_matches.append((mo.start(), mo.end(), mo.group(0), axis))
        raw_matches.sort(key=lambda t: (t[0], -(t[1] - t[0])))
        kept = []
        for st, en, surf, axis in raw_matches:
            if any(st >= k[0] and en <= k[1] for k in kept):
                continue
            kept.append((st, en, surf, axis))

        if not kept:
            continue

        line_base = cum[i - 1]   # global index of this line's first token
        for st, en, surf, axis in kept:
            # global token index of the match = line base + tokens before it on the line
            gidx = line_base + len(tokenize(clean_for_anchor(raw[:st])))
            lo = max(0, gidx - ANCHOR_WINDOW)
            hi = min(len(flat_tokens), gidx + ANCHOR_WINDOW + 1)
            window = " ".join(flat_tokens[lo:hi])
            anchor = find_anchor(window, anchors)
            seq += 1
            ctx = PAGE_MARKER.sub("", raw).strip()
            ctx = re.sub(r"\s+", " ", ctx)
            if len(ctx) > 160:
                # keep the window around the match
                cst = max(0, st - 70)
                ctx = ("…" if cst else "") + re.sub(r"\s+", " ", raw[cst:en + 70].strip()) + "…"
            loc = f"§ {cur_sec} / L{i}" if src["book"] == "ZalizniakOcherk_1978" and cur_sec \
                else (f"Занятие {cur_sec} / L{i}" if src["book"] == "KocherginaUchebnik_1998" and cur_sec
                      else (f"{cur_sec} / L{i}" if cur_sec else f"L{i}"))
            entries.append({
                "id": f"{src['book'][:3].upper()}-Q{seq:04d}",
                "loc": loc,
                "line": i,
                "axis": axis,
                "q": surf.strip(),
                "anchored": anchor is not None,
                "anchor": anchor,
                "zone": zone,
                "ctx": ctx,
            })
    return entries


def dump_yaml(src, entries):
    out = ROOT / src["book"] / "quantifiers.yml"
    header = (
        f"# quantifiers.yml — GENERATED auto-proxy quantifier register for {src['book']}\n"
        f"# Source: {src['file']}\n"
        f"# Generated by scripts/harvest_quantifiers.py on {TODAY} — DO NOT hand-edit.\n"
        f"#   Re-run: npm run quantifiers   (or python scripts/harvest_quantifiers.py {src['book']})\n"
        f"# anchored = quantifier within {ANCHOR_WINDOW} tokens of a decidable target\n"
        f"#            (класс/тип/§/правило/%/numbered category/cited affix); AUTO-PROXY (D3),\n"
        f"#            precision/recall estimated against the hand-verified quantifiers.sample.yml.\n"
        f"# axis: rarity | frequency | productivity | optionality | subset | universal\n"
    )
    payload = {
        "work": src["work"],
        "source_file": src["file"],
        "lang": src["lang"],
        "generated": TODAY,
        "anchor_window_tokens": ANCHOR_WINDOW,
        "entries": entries,
    }
    body = yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=100)
    out.write_text(header + body, encoding="utf-8")
    return out


def stratified_sample(entries, per_axis=6):
    """Deterministic stratified pick (~30): first `per_axis` grammar-zone hits per axis,
    balanced anchored/unanchored where possible. No RNG — reproducible."""
    from collections import defaultdict
    buckets = defaultdict(list)
    for e in entries:
        if e["zone"] == "grammar":
            buckets[e["axis"]].append(e)
    picked = []
    for axis, items in sorted(buckets.items()):
        anc = [e for e in items if e["anchored"]]
        una = [e for e in items if not e["anchored"]]
        take = []
        # alternate anchored/unanchored, evenly spaced across the list for coverage
        for pool in (una, anc):
            if not pool:
                continue
            step = max(1, len(pool) // max(1, per_axis // 2))
            take.extend(pool[::step][: per_axis // 2 + 1])
        picked.extend(take[:per_axis])
    return picked


def emit_sample(src, entries):
    out = ROOT / src["book"] / "quantifiers.sample.yml"
    if out.exists():
        existing = yaml.safe_load(out.read_text(encoding="utf-8")) or {}
        if any(r.get("human_anchored") is not None for r in existing.get("sample", [])):
            print(f"  [skip sample] {out.name} has human verdicts — not overwriting")
            return None
    lines = (ROOT / src["file"]).read_text(encoding="utf-8").splitlines()

    def wide(line_no):
        lo, hi = max(0, line_no - 3), min(len(lines), line_no + 2)
        ctx = " ".join(l.strip() for l in lines[lo:hi] if l.strip() not in ("", "\\"))
        ctx = PAGE_MARKER.sub("", ctx)
        return re.sub(r"\s+", " ", ctx).strip()[:320]

    sample = stratified_sample(entries)
    rows = [{
        "id": e["id"], "loc": e["loc"], "axis": e["axis"], "q": e["q"],
        "auto_anchored": e["anchored"], "auto_anchor": e["anchor"],
        "context": wide(e["line"]),
        "human_anchored": None,   # FILL: true/false
        "human_anchor": None,     # FILL: the real anchor, or null
        "note": None,
    } for e in sample]
    header = (
        f"# quantifiers.sample.yml — stratified hand-verification sample for {src['book']} (H800 D3).\n"
        f"# Fill human_anchored (true/false) + human_anchor for each row; build_quantifiers.py\n"
        f"# then reports the auto-proxy's precision/recall. Re-running harvest will NOT overwrite\n"
        f"# this file once any human_anchored is set.\n"
    )
    payload = {"work": src["work"], "sample_of": f"{src['book']}/quantifiers.yml", "sample": rows}
    out.write_text(header + yaml.safe_dump(payload, allow_unicode=True, sort_keys=False, width=100),
                   encoding="utf-8")
    return out


def stats(src, entries):
    from collections import Counter
    gram = [e for e in entries if e["zone"] == "grammar"]
    anc = sum(1 for e in gram if e["anchored"])
    share = round(100 * anc / len(gram), 1) if gram else 0.0
    byax = Counter(e["axis"] for e in gram)
    zc = Counter(e["zone"] for e in entries)
    print(f"\n{src['book']}: {len(entries)} raw hits, {len(gram)} grammar-zone "
          f"({dict(zc)})")
    print(f"  anchored (grammar): {anc}/{len(gram)} = {share}%")
    print(f"  by axis (grammar): {dict(byax)}")


def sweep():
    """Anchor-window sensitivity — anchored-share per source at several N (handoff @DECIDE)."""
    global ANCHOR_WINDOW
    Ns = [6, 8, 12, 16, 25, 40]
    print("Anchor-window sensitivity (anchored-share of grammar-zone hits):\n")
    print(f"{'source':<26} " + " ".join(f"N={n:<4}" for n in Ns))
    saved = ANCHOR_WINDOW
    rows = {}
    for src in SOURCES:
        rows[src["book"]] = []
        for n in Ns:
            ANCHOR_WINDOW = n
            es = [e for e in harvest(src) if e["zone"] == "grammar"]
            share = round(100 * sum(e["anchored"] for e in es) / len(es), 1) if es else 0
            rows[src["book"]].append(share)
    ANCHOR_WINDOW = saved
    for book, vals in rows.items():
        print(f"{book:<26} " + " ".join(f"{v:<6}" for v in vals))


def main():
    if "--sweep" in sys.argv:
        sweep()
        return
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    do_sample = "--emit-sample" in sys.argv
    targets = [s for s in SOURCES if s["book"] in argv] if argv else SOURCES
    for src in targets:
        entries = harvest(src)
        out = dump_yaml(src, entries)
        stats(src, entries)
        print(f"  -> {out.relative_to(ROOT)} ({len(entries)} entries)")
        if do_sample:
            so = emit_sample(src, entries)
            if so:
                print(f"  -> {so.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
