#!/usr/bin/env python
"""m03_checkers_common.py — shared substrate for the two M03 freeze-harness checkers
(H2871): the manuscript file set, MDX de-noising, and number normalisation.

Both `gost_bibliography_check.py` and `numbers_crosscheck.py` import from here so the
two reports always talk about the SAME set of files and the SAME notion of "a number".

Neither this module nor its two callers ever writes into a manuscript file. They read
`*.mdx` and emit a dated `.md` report; that is the whole contract (H2871 fence: the
manuscript prose is human-owned, H275).
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent          # .../GasunsDhatu_2014/revision-2026
BOOK = HERE.parent                              # .../GasunsDhatu_2014
REPO = BOOK.parent                              # repo root

# The M03 monograph as it will go to press: Part I + Part II + the appendix articles.
# `ERRATA.mdx` (errata apparatus), `Список файлов.mdx` (supporting-materials note),
# the 2024 Cologne article and the legacy `Распространение рядов согласных.mdx` stub
# are deliberately OUT — they are not manuscript body.
MANUSCRIPT_FILES = [
    "02_gasuns-dhatu-PhD-text2.mdx",
    "04_glava4_kross-uok-omonimiya.mdx",
    "05_glava5_dhatupatha-panini.mdx",
    "06_glava6_korpusnaya-attestaciya.mdx",
    "07_glava7_ukazatel-zaliznyaka.mdx",
    "Приложения издания 2026.mdx",
    "Морфонологическая запись глагольных корней санскрита.mdx",
    "О записи омонимии корней в словарях древнеиндийского языка.mdx",
    "Распределение рядов согласных.mdx",
]

# The main text carries the bibliography, the table-of-contents and the list of
# illustrations; the appendix articles carry neither.
MAIN_TEXT = MANUSCRIPT_FILES[0]

THIN_SPACES = "    ⁠"


def manuscript_paths(names=None):
    """Absolute paths of the manuscript files, in press order. Missing files raise."""
    out = []
    for name in (names or MANUSCRIPT_FILES):
        p = BOOK / name
        if not p.is_file():
            raise SystemExit(f"manuscript file missing: {p}")
        out.append(p)
    return out


def read_lines(path):
    """1-indexed list of (lineno, text) for a manuscript file, newline-stripped."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("﻿"):
        raise SystemExit(f"UTF-8 BOM in {path} — refuse to parse")
    return list(enumerate(text.split("\n"), start=1))


def strip_frontmatter(lines):
    """Drop a leading `---` YAML front-matter block, keeping line numbers intact."""
    if lines and lines[0][1].strip() == "---":
        for idx, (_no, text) in enumerate(lines[1:], start=1):
            if text.strip() == "---":
                return lines[idx + 1:]
    return lines


def fenced_ranges(lines):
    """Set of line numbers inside ``` fenced blocks (rst-table, code)."""
    inside = set()
    open_at = None
    for no, text in lines:
        if text.startswith("```"):
            if open_at is None:
                open_at = no
            else:
                inside.update(range(open_at, no + 1))
                open_at = None
    if open_at is not None:
        inside.update(range(open_at, lines[-1][0] + 1))
    return inside


LINK_RE = re.compile(r"\[[^\]\[]*\]\([^)]*\)")
FOOTNOTE_REF_RE = re.compile(r"\[\^[^\]]*\]")
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def denoise(text):
    """Remove markdown links, footnote refs and inline code from a prose line.

    Everything removed is replaced by a same-length run of spaces so that column
    offsets — and therefore any locus a human is asked to jump to — stay truthful.
    """
    def blank(m):
        return " " * (m.end() - m.start())

    text = LINK_RE.sub(blank, text)
    text = FOOTNOTE_REF_RE.sub(blank, text)
    text = INLINE_CODE_RE.sub(blank, text)
    return text


NUMBER_RE = re.compile(r"(?<![\d.,])(\d{1,3}(?:[     ]\d{3})+|\d+)(?![\d])")


def normalise_spaces(text):
    for ch in THIN_SPACES:
        text = text.replace(ch, " ")
    return text


def parse_number(token):
    """'3 861 721' / '3861721' -> 3861721. Returns None when not an integer."""
    cleaned = normalise_spaces(token).replace(" ", "")
    return int(cleaned) if cleaned.isdigit() else None


def integers_in(text):
    """All integers on a line, thousands-space aware, as a list of ints."""
    out = []
    for m in NUMBER_RE.finditer(normalise_spaces(text)):
        val = parse_number(m.group(1))
        if val is not None:
            out.append(val)
    return out


def number_variants(value):
    """Every surface form the manuscript may use for an integer.

    The book is inconsistent by design — the 2014 tables print `2689255` bare while
    the 2026 prose prints `2 259` with a thousands space — so a value hunt must try
    both, plus the non-breaking-space form the docx round-trip introduces.
    """
    bare = str(value)
    if len(bare) <= 3:
        return {bare}
    grouped = []
    rest = bare
    while len(rest) > 3:
        grouped.insert(0, rest[-3:])
        rest = rest[:-3]
    grouped.insert(0, rest)
    return {bare, " ".join(grouped), " ".join(grouped), " ".join(grouped)}


def find_value(value, haystacks):
    """Loci ('file:line') where an integer appears as a standalone token."""
    hits = []
    variants = sorted(number_variants(value), key=len, reverse=True)
    for name, lines in haystacks:
        for no, text in lines:
            flat = normalise_spaces(text)
            for variant in variants:
                variant = normalise_spaces(variant)
                for m in re.finditer(re.escape(variant), flat):
                    before = flat[m.start() - 1] if m.start() else " "
                    after = flat[m.end()] if m.end() < len(flat) else " "
                    if before.isdigit() or after.isdigit():
                        continue
                    if before in ".," and flat[max(0, m.start() - 2):m.start() - 1].isdigit():
                        continue  # decimal tail, e.g. the 259 of 1,259
                    hits.append(f"{name}:{no}")
                    break
                else:
                    continue
                break
    return hits


def strip_markup(text):
    """Bold/italic markers out, whitespace collapsed — for human-readable loci echoes."""
    text = re.sub(r"\*\*|\*|__|_", "", text)
    return re.sub(r"\s+", " ", normalise_spaces(text)).strip()
