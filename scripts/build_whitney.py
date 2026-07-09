#!/usr/bin/env python3
"""Build the WhitneyGrammar_1889/ book folder for the SanskritGrammar site from
the WhitneyRoots source data.

Source of truth (sibling repo, never copied wholesale):
  ../WhitneyRoots/src/wg_text.txt          — flat OCR of the 1889/1950 body (§1-1316 + Appendix)
  ../WhitneyRoots/src/whitney_sections.json — 18 chapters with titles + §-ranges

Output (generated — do NOT hand-edit):
  WhitneyGrammar_1889/00_index.mdx         — front page (chapter list, provenance, caveats)
  WhitneyGrammar_1889/NN_<slug>.mdx        — one file per chapter (I..XVIII) + Appendix

Segmentation: the body is a monotonic run of sections numbered `N. ...`. We walk
from the first real §1 ("1. The natives of India write ...") and open a new
section every time a line begins with the next expected integer. Footnotes
(`N. ↑ ...`) restart at 1 and never equal the (large) expected section number, so
they stay inside the section body and are rendered as footnote lines. OCR hard
line-wraps are unwrapped into paragraphs (blank line = paragraph break).

Each §-number links to the authoritative Wikisource section so a student can jump
to the canonical text.

Paradigm-table Devanagari repair (H427): the flat OCR captured Whitney's table cells
in *print reading order* — pre-base i-signs land before the wrong consonant, some
matras are dropped, and conjuncts were encoded as private-use-area glyphs from a
custom PDF font — so the raw Devanagari for tables is unusable. But every table cell
is immediately followed by Whitney's own IAST romanization, which is clean. We
therefore regenerate each corrupt Devanagari cell deterministically from its adjacent
IAST line (Whitney-notation-aware: strip Vedic udatta/anudatta accents, map his
diphthong spellings `āi`/`āu`→ai/au and `ç`→ś, then transliterate IAST→Devanagari).
This recovers ~1830 cells with zero residual PUA. Tables still render as sequential
form-lists rather than reconstructed grids — see the caveat block on the index page.
"""
import json
import os
import re
import sys
import unicodedata

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

try:
    from indic_transliteration import sanscript
    from indic_transliteration.sanscript import transliterate
except ImportError:  # pragma: no cover
    sys.exit("build_whitney.py needs indic_transliteration — `pip install "
             "indic_transliteration` (see scripts/requirements.txt).")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "..", "WhitneyRoots", "src")
OUT_DIR = os.path.join(ROOT, "WhitneyGrammar_1889")
WIKISOURCE = "https://en.wikisource.org/wiki/Sanskrit_Grammar_(Whitney)"

FOOTNOTE = re.compile(r"^\d+\.\s+↑")
SECTION = re.compile(r"^(\d+)\.\s")
ANCHOR = re.compile(r"\{anchor\|[^}]*\}")

# --- paradigm-table Devanagari repair (H427) ---------------------------------
_DEVA = re.compile(r"[ऀ-ॿ]")     # Devanagari block
_PUA = re.compile(r"[-]")      # custom-font glyphs the OCR emitted
_LATIN = re.compile(r"[A-Za-z]")
# inline-pass helpers (chr()-built ranges: PUA literals don't survive an editor)
_IMATRA = chr(0x093F)           # pre-base vowel sign I (the OCR-reordered sign)
_VIRAMA = chr(0x094D)
_CONS = set(chr(c) for c in list(range(0x0915, 0x093A)) + list(range(0x0958, 0x0960)))
_IAST_DIAC = set("āīūṛṝḷḹṅñṭḍṇśṣṃḥçĀĪŪṚṢŚÑ")
_ROOT_SIGN = "√"
_ROMAN_RE = re.compile(r"^[A-Za-zāīūṛṝḷḹṅñṭḍṇśṣṃḥçĀĪŪṚṢŚÑ]+$")
_ACCENTS = ("́", "̀")            # combining acute/grave = udatta/anudatta


def _is_deva_cell(s):
    """A single-token table cell whose text is Devanagari and/or PUA (no romanization)."""
    s = s.strip()
    return bool(s) and " " not in s and not _LATIN.search(s) \
        and (bool(_DEVA.search(s)) or bool(_PUA.search(s)))


def _is_iast_cell(s):
    """A single-token romanization cell (Latin, no Devanagari/PUA)."""
    s = s.strip()
    return bool(s) and " " not in s and not _DEVA.search(s) \
        and not _PUA.search(s) and bool(_LATIN.search(s))


def whitney_iast_to_deva(iast):
    """Whitney-notation-aware IAST -> Devanagari (deterministic)."""
    s = unicodedata.normalize("NFD", iast)
    s = "".join(ch for ch in s if ch not in _ACCENTS)   # drop Vedic accent marks
    s = unicodedata.normalize("NFC", s)
    s = s.replace("āi", "ai").replace("Āi", "Ai")       # Whitney diphthong notation
    s = s.replace("āu", "au").replace("Āu", "Au")
    s = s.replace("ç", "ś").replace("Ç", "Ś")           # Whitney palatal sibilant
    s = s.replace("ṁ", "ṃ").replace("Ṁ", "Ṃ")           # anusvara dot-above -> below
    return transliterate(s, sanscript.IAST, sanscript.DEVANAGARI)


def _has_bad_imatra(tok):
    """True if a pre-base i-sign sits where the OCR mis-ordered it: at token start,
    or after anything that is not a base consonant or virama."""
    for i, ch in enumerate(tok):
        if ch == _IMATRA:
            prev = tok[i - 1] if i > 0 else ""
            if prev not in _CONS and prev != _VIRAMA:
                return True
    return False


def _is_corrupt_deva(tok):
    """A Devanagari token the OCR provably mangled: a PUA glyph or a stray i-sign."""
    return bool(_PUA.search(tok)) or _has_bad_imatra(tok)


def _diacritic_roman(tok):
    """Return the romanization if `tok` is one carrying an IAST diacritic (which no
    English word does — this gate is what makes the inline fix safe), else None."""
    t = tok.strip(".,;:()[]।॥")
    if not t or _DEVA.search(t) or _PUA.search(t):
        return None
    if any(c in _IAST_DIAC for c in t) and _ROMAN_RE.match(t):
        return t
    return None


def regenerate_table_cells(lines):
    """Pass 1 — replace each corrupt Devanagari table cell (one form per line) with
    one regenerated from its adjacent IAST romanization line. Idempotent."""
    out = list(lines)
    n = 0
    for i, ln in enumerate(lines):
        if _is_deva_cell(ln) and i + 1 < len(lines) and _is_iast_cell(lines[i + 1]):
            out[i] = whitney_iast_to_deva(lines[i + 1].strip())
            n += 1
    return out, n


def regenerate_inline_forms(lines):
    """Pass 2 — inside running prose, replace a *provably corrupt* Devanagari token
    with one regenerated from the immediately following romanization, but ONLY when
    that romanization carries an IAST diacritic. The diacritic gate keeps this safe:
    English glosses ('lead', 'and', 'Each') never carry one, so a correct Devanagari
    form followed by an English word is never touched. Idempotent."""
    out = []
    n = 0
    for ln in lines:
        toks = ln.split(" ")
        for i, tok in enumerate(toks):
            prefix, body = "", tok
            if body.startswith(_ROOT_SIGN):
                prefix, body = _ROOT_SIGN, body[1:]
            if not (_DEVA.search(body) or _PUA.search(body)) or not _is_corrupt_deva(body):
                continue
            roman = _diacritic_roman(toks[i + 1]) if i + 1 < len(toks) else None
            if roman is None:
                continue
            tail = re.search(r"[.,;:)।॥]+$", body)
            toks[i] = prefix + whitney_iast_to_deva(roman) + (tail.group(0) if tail else "")
            n += 1
        out.append(" ".join(toks))
    return out, n


def slugify(title):
    s = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    return s


def mdx_safe(text):
    """Neutralize the MDX-v3 hazards in plain prose (same policy as
    mdx_postprocess.py, minus the table machinery Whitney prose doesn't use)."""
    text = ANCHOR.sub("", text)  # drop Wikisource {anchor|N} tokens
    text = text.replace("{", r"\{").replace("}", r"\}")
    # angle brackets that aren't our own markup -> entities
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    return text


def load_chapters():
    with open(os.path.join(SRC_DIR, "whitney_sections.json"), encoding="utf-8") as f:
        meta = json.load(f)["_meta"]
    return meta["chapters_fetched"]


def load_sections():
    """Return {section_number: [raw lines]} for §1..1316, plus appendix lines."""
    with open(os.path.join(SRC_DIR, "wg_text.txt"), encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]

    # repair Devanagari from the adjacent clean IAST (H427): tables first, then
    # provably-corrupt inline prose forms (diacritic-gated, safe against glosses)
    lines, n_cells = regenerate_table_cells(lines)
    lines, n_inline = regenerate_inline_forms(lines)
    print(f"regenerated {n_cells} table cells + {n_inline} inline forms from IAST",
          file=sys.stderr)

    # locate the first real body section
    start = next(i for i, ln in enumerate(lines)
                 if ln.startswith("1. The natives of India write"))

    sections = {}
    appendix = []
    last = 0          # last section number opened
    missing = []
    cur = None
    buf = []
    in_appendix = False
    for ln in lines[start:]:
        if ln.strip() == "APPENDIX." and last >= 1316:
            in_appendix = True
        if in_appendix:
            appendix.append(ln)
            continue
        probe = ANCHOR.sub("", ln).lstrip()   # strip {anchor|N} before matching
        m = SECTION.match(probe)
        # A valid new section is a line-start integer just ahead of the last one.
        # Tolerate a small gap (an OCR-dropped marker) so one bad boundary can't
        # stall the whole walk, but never jump by more than 5 (guards against a
        # stray in-body enumerator being mistaken for a section).
        if m and not FOOTNOTE.match(probe):
            n = int(m.group(1))
            if last < n <= last + 5:
                if cur is not None:
                    sections[cur] = buf
                if n > last + 1:
                    missing.extend(range(last + 1, n))
                cur = n
                buf = [probe[m.end():]]  # drop the leading "N. "
                last = n
                continue
        buf.append(ln)
    if cur is not None:
        sections[cur] = buf
    if missing:
        print(f"  (no discrete marker for §§ {missing} — merged into preceding)",
              file=sys.stderr)
    return sections, appendix


def render_section_body(sec_no, raw_lines):
    """Unwrap OCR hard-wraps into paragraphs; pull out footnote lines."""
    paras = []
    notes = []
    cur = []
    for ln in raw_lines:
        if FOOTNOTE.match(ln):
            notes.append(re.sub(r"^\d+\.\s+↑\s*", "", ln).strip())
            continue
        if not ln.strip():
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        cur.append(ln.strip())
    if cur:
        paras.append(" ".join(cur))

    link = f"[**§{sec_no}**]({WIKISOURCE}/Chapter_{{rn}}#{sec_no})"  # {rn} filled by caller
    out = []
    if paras:
        out.append(link + " " + mdx_safe(paras[0]))
        for p in paras[1:]:
            out.append(mdx_safe(p))
    else:
        out.append(link)
    for n in notes:
        out.append(f"> _[note]_ {mdx_safe(n)}")
    return out


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    chapters = load_chapters()
    sections, appendix = load_sections()
    got = len(sections)
    print(f"parsed {got} sections (expected 1316)", file=sys.stderr)

    # ---- index page ----
    idx = []
    idx.append("---")
    idx.append('title: "Whitney — Sanskrit Grammar (1889)"')
    idx.append('sidebar_label: "Whitney 1889 — overview"')
    idx.append("sidebar_position: 0")
    idx.append("---")
    idx.append("")
    idx.append("# Whitney — *A Sanskrit Grammar* (2nd ed., 1889)")
    idx.append("")
    idx.append("_Generated by [`scripts/build_whitney.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_whitney.py) "
               "from [`WhitneyRoots/src/wg_text.txt`](https://github.com/gasyoun/WhitneyRoots/blob/main/src/wg_text.txt) "
               "+ [`whitney_sections.json`](https://github.com/gasyoun/WhitneyRoots/blob/main/src/whitney_sections.json) — do not hand-edit._")
    idx.append("")
    idx.append("William Dwight Whitney, *A Sanskrit Grammar, including both the Classical "
               "Language and the older Dialects, of Veda and Brahmana* (2nd edition, "
               "Leipzig/Boston 1889; text here from the 7th issue, 1950). Public domain; "
               "this digital text derives from the "
               f"[English Wikisource edition]({WIKISOURCE}) and is offered under CC BY-SA 4.0.")
    idx.append("")
    idx.append(f"The body is presented in Whitney's own 18 chapters and {got} numbered "
               "sections (§). Each **§N** links to the corresponding Wikisource section.")
    idx.append("")
    idx.append(":::caution Tables and accents")
    idx.append("This rendering is unwrapped from a flat OCR of the print body. Whitney's "
               "**paradigm tables** (declension/conjugation grids) are therefore presented as "
               "sequential form-lists rather than reconstructed grids, and **Vedic accent "
               "marks** are not shown. The OCR badly mangled the Devanagari of these forms "
               "(pre-base i-signs misplaced, dropped matras, private-use-area conjunct "
               "glyphs), so wherever Whitney printed a romanization beside a form — every "
               "table cell and most inline examples — the Devanagari is regenerated "
               "deterministically from that romanization and is reliable. A minority of forms "
               "cannot be repaired automatically (romanizations without a distinguishing "
               "diacritic, and Devanagari inside quoted verse) and may still show OCR "
               "artifacts, including a `□` placeholder for a lost glyph. For the original grid "
               "layout follow any **§N** link to Wikisource or see the "
               "[scanned PDF](https://github.com/gasyoun/WhitneyRoots/blob/main/src/Whitney-Grammar_Wikisource_2023.pdf); "
               "for structured, machine-readable section and form data see the "
               "[WhitneyRoots](https://github.com/gasyoun/WhitneyRoots) repo.")
    idx.append(":::")
    idx.append("")
    idx.append("## Chapters")
    idx.append("")
    idx.append("| Ch. | Title | § range |")
    idx.append("|---|---|---|")
    for c in chapters:
        idx.append(f"| {c['chapter']} | {c['title']} | {c['first']}–{c['last']} |")
    idx.append("")
    with open(os.path.join(OUT_DIR, "00_index.mdx"), "w", encoding="utf-8") as f:
        f.write("\n".join(idx))

    # ---- per-chapter pages ----
    for pos, c in enumerate(chapters, start=1):
        rn = c["chapter"]
        title = c["title"]
        lines = []
        lines.append("---")
        lines.append(f'title: "{rn}. {title}"')
        lines.append(f'sidebar_label: "{rn}. {title}"')
        lines.append(f"sidebar_position: {pos}")
        lines.append("---")
        lines.append("")
        lines.append(f"# Chapter {rn}. {title}")
        lines.append("")
        lines.append(f"_Whitney §§ {c['first']}–{c['last']}. "
                     f"[Read this chapter on Wikisource]({WIKISOURCE}/Chapter_{rn})._")
        lines.append("")
        for n in range(c["first"], c["last"] + 1):
            body = sections.get(n)
            if not body:
                continue
            for chunk in render_section_body(n, body):
                lines.append(chunk.replace("{rn}", rn))
                lines.append("")
        fn = f"{pos:02d}_{slugify(title)}.mdx"
        with open(os.path.join(OUT_DIR, fn), "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  wrote {fn} (§{c['first']}-{c['last']})", file=sys.stderr)

    # ---- appendix ----
    if appendix:
        ap = []
        ap.append("---")
        ap.append('title: "Appendix"')
        ap.append('sidebar_label: "Appendix"')
        ap.append("sidebar_position: 19")
        ap.append("---")
        ap.append("")
        ap.append("# Appendix")
        ap.append("")
        ap.append(f"_[On Wikisource]({WIKISOURCE}/Appendix)._")
        ap.append("")
        para = []
        for ln in appendix[1:]:  # skip the literal "APPENDIX." heading line
            if not ln.strip():
                if para:
                    ap.append(mdx_safe(" ".join(para)))
                    ap.append("")
                    para = []
                continue
            para.append(ln.strip())
        if para:
            ap.append(mdx_safe(" ".join(para)))
            ap.append("")
        with open(os.path.join(OUT_DIR, "19_Appendix.mdx"), "w", encoding="utf-8") as f:
            f.write("\n".join(ap))
        print("  wrote 19_Appendix.mdx", file=sys.stderr)


if __name__ == "__main__":
    main()
