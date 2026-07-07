#!/usr/bin/env python3
"""Build the SubjectConcordance/ page — a student-reference cross-index of which
grammatical *subject* each grammar in this repo covers, on the spine of Whitney's
18 chapters + 41 fine-grained form categories.

This is the SUBJECT counterpart to the existing sentence-level Concordance/. The
spine is Whitney (1889): its 18 chapters are the top-level subjects and
`form_section_concordance.json` supplies the fine categories with their §-ranges.

Coverage of the other works is detected by a **curated multilingual keyword
lexicon** (EN / RU / DE + Sanskrit technical terms) scanned over each work's full
.mdx text — most editions here are Russian-medium. This is an automated FIRST PASS,
not a philological mapping: a cell reports how many distinct lexicon terms for that
subject occur in the work (≥3 = covered ●, 1–2 = mentioned ○, 0 = —). Treat it as
a finding-aid, not an authority; verify against the work itself before citing.

Generated — do NOT hand-edit SubjectConcordance/catalog.mdx; re-run this script.
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WR_SRC = os.path.join(ROOT, "..", "WhitneyRoots", "src")
OUT_DIR = os.path.join(ROOT, "SubjectConcordance")
GH = "https://github.com/gasyoun/SanskritGrammar/blob/main"
WIKISOURCE = "https://en.wikisource.org/wiki/Sanskrit_Grammar_(Whitney)"

# Works to index (besides Whitney, which is the spine). folder, display, glob, short.
WORKS = [
    ("ApteSyntax_1885",        "Apte — Syntax (1885)",         "ApteSyntax_1885/*.mdx",         "Apte"),
    ("BuhlerLeitfaden_1923",   "Bühler — Leitfaden (1923)",    "BuhlerLeitfaden_1923/*.mdx",    "Bühler"),
    ("GasunsDhatu_2014",       "Gasūns — Dhātu (2014)",        "GasunsDhatu_2014/*.mdx",        "Gasūns"),
    ("KnauerFrazy_1908",       "Knauer — Phrases (1908)",      "KnauerFrazy_1908/*.mdx",        "Knauer"),
    ("KocherginaUchebnik_1998","Kochergina — Uchebnik (1998)", "KocherginaUchebnik_1998/*.mdx", "Kochergina"),
    ("TolchelnikovTalmud_2026","Tolchelnikov — Talmud (2026)", "TolchelnikovTalmud_2026/*.mdx", "Tolchelnikov"),
    ("ZalizniakKonspekt_2004", "Zaliznyak — Konspekt (2004)",  "ZalizniakKonspekt_2004/*.mdx",  "Zal.Konspekt"),
    ("ZalizniakMorphology_1975","Zaliznyak — Morphology (1975)","ZalizniakMorphology_1975/*.mdx","Zal.Morph."),
    ("ZalizniakOcherk_1978",   "Zaliznyak — Ocherk (1978)",    "ZalizniakOcherk_1978/*.mdx",    "Zal.Ocherk"),
]

# Per-chapter (top-level subject) keyword lexicon. Case-insensitive substring
# match; kept deliberately specific to reduce incidental hits. RU + EN + DE +
# Sanskrit technical terms, since most editions here are Russian-medium.
CHAPTER_KW = {
    "I":   ["alphabet", "алфавит", "devanāgarī", "деванагари", "письмен", "графика", "письмо", "Schrift"],
    "II":  ["pronunciation", "произнош", "фонетик", "phonet", "звуков", "Laut", "guttural", "гуттура", "палатал"],
    "III": ["sandhi", "сандхи", "euphonic", "соединен", "сочетаем", "чередован", "Lautverbindung"],
    "IV":  ["declension", "склонен", "Deklination", "падеж", "именное словоизмен"],
    "V":   ["adjective", "прилагательн", "существительн", "основа на", "Nomen", "имя существ", "имена"],
    "VI":  ["numeral", "числительн", "Zahlwort", "числительное"],
    "VII": ["pronoun", "местоимен", "Pronomen"],
    "VIII":["conjugation", "спряжен", "Konjugation", "глагольн систем", "глагольная систем"],
    "IX":  ["present", "настоящее время", "презенс", "презентн", "present-system", "тематическ спряж"],
    "X":   ["perfect", "перфект", "совершенн вид", "reduplicated perfect"],
    "XI":  ["aorist", "аорист", "прекатив", "precative"],
    "XII": ["future", "будущее время", "футурум", "кондиционал", "conditional"],
    "XIII":["participle", "причаст", "infinitive", "инфинитив", "gerund", "деепричаст", "абсолютив", "absolutive", "герундив", "gerundive"],
    "XIV": ["causative", "каузатив", "desiderative", "десидератив", "intensive", "интенсив", "denominative", "деноминатив", "вторичн спряж"],
    "XV":  ["periphrastic", "перифрастическ", "составное спряжен", "compound conjugation"],
    "XVI": ["indeclinable", "неизменяем", "adverb", "наречие", "preposition", "предлог", "particle", "частиц", "союз", "Partikel"],
    "XVII":["derivation", "словообразован", "suffix", "суффикс", "первичн основ", "вторичн основ", "производн основ", "krt", "taddhita", "таддхита"],
    "XVIII":["compound", "сложное слово", "сложн слов", "композит", "samāsa", "самаса", "bahuvrīhi", "бахуврихи", "tatpuruṣa", "татпуруша", "dvandva", "двандва", "kārmadhāraya", "кармадхарая"],
}

WORD = re.compile(r"[A-Za-zА-Яа-яĀāĪīŪūṚṛṜṝḶḷṄṅÑñṬṭḌḍṆṇŚśṢṣḤḥṀṁ]+", re.U)


def load_spine():
    with open(os.path.join(WR_SRC, "whitney_sections.json"), encoding="utf-8") as f:
        chapters = json.load(f)["_meta"]["chapters_fetched"]
    with open(os.path.join(WR_SRC, "form_section_concordance.json"), encoding="utf-8") as f:
        cats = json.load(f)["categories"]
    return chapters, cats


def work_text(pattern):
    txt = []
    for p in sorted(glob.glob(os.path.join(ROOT, pattern))):
        with open(p, encoding="utf-8") as f:
            txt.append(f.read())
    return "\n".join(txt)


def coverage(text, keywords):
    low = text.lower()
    return sum(1 for kw in keywords if kw.lower() in low)


def mark(n):
    if n >= 3:
        return f"● {n}"
    if n >= 1:
        return f"○ {n}"
    return "—"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    chapters, cats = load_spine()

    # pre-load each work's text once
    texts = {w[0]: work_text(w[2]) for w in WORKS}

    L = []
    L.append("---")
    L.append('title: "Subject concordance — what each grammar covers"')
    L.append('sidebar_label: "Subject concordance"')
    L.append("---")
    L.append("")
    L.append("# Subject concordance — where each grammar treats each subject")
    L.append("")
    L.append(f"_Generated by [`scripts/build_subject_concordance.py`]({GH}/scripts/build_subject_concordance.py) "
             f"from [`WhitneyRoots/src/whitney_sections.json`](https://github.com/gasyoun/WhitneyRoots/blob/main/src/whitney_sections.json) "
             f"+ [`form_section_concordance.json`](https://github.com/gasyoun/WhitneyRoots/blob/main/src/form_section_concordance.json) — do not hand-edit._")
    L.append("")
    L.append("A student-reference cross-index of the grammars in this repo, laid out "
             "on the spine of **Whitney's *Sanskrit Grammar* (1889)** — its 18 chapters "
             "are the top-level subjects; the "
             "[Whitney book pages](../WhitneyGrammar_1889/00_index) carry the full text "
             "with each **§N** linking to Wikisource.")
    L.append("")
    L.append(":::note How to read this (automated first pass)")
    L.append("Coverage of the non-Whitney works is detected by a **curated multilingual "
             "keyword lexicon** (English / Russian / German + Sanskrit technical terms — "
             "most editions here are Russian-medium) scanned over each work's full text. "
             "A cell shows how many distinct subject terms occur in that work: "
             "**● = covered (≥3 terms)**, **○ = mentioned (1–2)**, **— = not found**. "
             "This is a finding-aid, **not** a philological mapping — a phrasebook may "
             "score ● on a subject it only drills in exercises, and a term may be absent "
             "under a synonym the lexicon misses. Verify against the work itself before "
             "citing; see the per-work tables of contents at the foot of the page for the "
             "works' own structure.")
    L.append(":::")
    L.append("")

    # ---- top-level matrix (18 chapters x works) ----
    L.append("## Coverage matrix — Whitney's 18 chapters")
    L.append("")
    hdr = "| Whitney chapter (subject) | §§ |"
    sep = "|---|---|"
    for folder, disp, pat, short in WORKS:
        hdr += f" {short} |"
        sep += "---|"
    L.append(hdr)
    L.append(sep)
    for c in chapters:
        rn = c["chapter"]
        subj = f"**{rn}.** [{c['title']}]({WIKISOURCE}/Chapter_{rn})"
        row = f"| {subj} | {c['first']}–{c['last']} |"
        kws = CHAPTER_KW.get(rn, [])
        for folder, _disp, _pat, _short in WORKS:
            row += f" {mark(coverage(texts[folder], kws))} |"
        L.append(row)
    L.append("")

    # ---- fine categories (Whitney §-ranges) ----
    L.append("## Fine-grained form categories (Whitney spine)")
    L.append("")
    L.append("The 41 morphological categories Whitney distinguishes, with their exact "
             "§-ranges — the reference axis a student can hang any other grammar's "
             "treatment onto. Source: "
             "[`form_section_concordance.json`](https://github.com/gasyoun/WhitneyRoots/blob/main/src/form_section_concordance.json).")
    L.append("")
    L.append("| Category | Whitney §§ | Chapter |")
    L.append("|---|---|---|")
    for key, v in cats.items():
        lo, hi = v.get("lo"), v.get("hi")
        rng = f"{lo}–{hi}" if lo != hi else f"{lo}"
        ch = v.get("chapter") or ""
        label = v["label"].replace("|", "\\|")
        L.append(f"| {label} | [{rng}]({WIKISOURCE}/Chapter_{ch}) | {ch} |")
    L.append("")

    # ---- per-work extracted TOC ----
    L.append("## Each work's own structure (extracted headings)")
    L.append("")
    L.append("Whitney supplies the subject spine above; each other grammar organizes its "
             "material differently (thematic sections, numbered lessons, or per-topic "
             "files). These are the headings extracted from each work's `.mdx` so you can "
             "cross to its native structure.")
    L.append("")
    head_re = re.compile(r"^#{1,4}\s+(.+?)\s*$")
    def clean(s):
        s = re.sub(r"<[^>]*>", "", s)          # strip tags
        s = re.sub(r"[*_`\\{}<>|]", "", s)       # strip MDX-hazard chars
        return s.strip()

    for folder, disp, pat, short in WORKS:
        heads = []
        for p in sorted(glob.glob(os.path.join(ROOT, pat))):
            with open(p, encoding="utf-8") as f:
                for ln in f:
                    m = head_re.match(ln)
                    if m:
                        t = clean(m.group(1))
                        if t and len(t) < 80:
                            heads.append(t)
        L.append(f"### {disp} — {len(heads)} headings")
        L.append("")
        if heads:
            for h in heads[:60]:
                L.append(f"- {h}")
            if len(heads) > 60:
                L.append(f"- _…and {len(heads) - 60} more_")
        else:
            L.append("- _(no `#` headings — the work's divisions are in-line, not headed)_")
        L.append("")

    out = os.path.join(OUT_DIR, "catalog.mdx")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"wrote {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
