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
to the canonical text (and to Whitney's tables, which the flat OCR mangles — see
the caveat block on the index page).
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT, "..", "WhitneyRoots", "src")
OUT_DIR = os.path.join(ROOT, "WhitneyGrammar_1889")
WIKISOURCE = "https://en.wikisource.org/wiki/Sanskrit_Grammar_(Whitney)"

FOOTNOTE = re.compile(r"^\d+\.\s+↑")
SECTION = re.compile(r"^(\d+)\.\s")
ANCHOR = re.compile(r"\{anchor\|[^}]*\}")


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
    idx.append("This rendering is unwrapped from a flat OCR of the print body, so Whitney's "
               "**paradigm tables** (declension/conjugation grids) and some **Vedic accent "
               "marks** are not reconstructed here — follow any **§N** link to Wikisource, or "
               "see the [scanned PDF](https://github.com/gasyoun/WhitneyRoots/blob/main/src/Whitney-Grammar_Wikisource_2023.pdf), "
               "for the authoritative tables. For structured, machine-readable section and "
               "form data see the [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots) repo.")
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
