#!/usr/bin/env python3
"""Extract Sanskrit sentences (both Devanagari and IAST) from the three
grammar .mdx files (Buhler 1923, Knauer 1908, Kochergina 1998) and find
cross-book matches.

First-pass tool for the Buhler/Knauer/Kochergina exercise-sentence
concordance (H311). Each extracted sentence keeps a `script` tag
("deva"/"iast") recording which script it was originally set in. Matching
is done within each script pool separately (deva-vs-deva, iast-vs-iast) —
cross-script (Devanagari vs IAST) matching would need a transliteration
step and is a follow-up (see handoff).

Usage:
    python scripts/extract_sentences.py extract   # writes data/sentences.json
    python scripts/extract_sentences.py match      # writes data/matches.json
"""
import json
import os
import re
import sys
from difflib import SequenceMatcher

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "scripts", "data")
os.makedirs(DATA_DIR, exist_ok=True)

BOOKS = {
    "buhler": {
        "label": "Bühler 1923",
        "year": 1878,  # historical first edition; this file is the 1923 reprint proxy
        "path": os.path.join(ROOT, "BuhlerLeitfaden_1923", "Buhler_Unicode.mdx"),
        "lesson_re": re.compile(r"^#\s*УРОК\s+([IVXL]+)\.?\s*$", re.MULTILINE),
    },
    "knauer": {
        "label": "Knauer 1908",
        "year": 1908,
        "path": os.path.join(ROOT, "KnauerFrazy_1908", "Frazy-Knauer-03.05.2023.mdx"),
        "lesson_re": re.compile(r"^#\s*Nr\.\s*(\d+)\s*\(([^)]*)\)\.?\s*$", re.MULTILINE),
    },
    "kochergina": {
        "label": "Kochergina 1998",
        "year": 1998,
        "path": os.path.join(ROOT, "KocherginaUchebnik_1998", "Kochergina_unicode.mdx"),
        "lesson_re": re.compile(r"^Занятие\s+([IVXL]+)\s*$", re.MULTILINE),
    },
}

DEVANAGARI_RUN = re.compile(r"[ऀ-ॿ][ऀ-ॿ\s]*[ऀ-ॿ]")
FOOTNOTE_MARK = re.compile(r"\^\d+\^|\[\^\d+\]")
DEVA_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")

# IAST diacritics — a run of Latin text must contain at least one of these to
# count as Sanskrit (filters out plain English/German glosses, "Nr.", "УРОК",
# footnote Latin abbreviations, etc.)
IAST_DIACRITIC = re.compile(r"[āīūṛṝḷḹṃḥśṣñṅṭḍṇṅçġ]", re.IGNORECASE)
# A run of extended-Latin characters (letters, IAST diacritics, apostrophe/
# hyphen for sandhi elision, digits for verse numbers).
LATIN_RUN = re.compile(r"[A-Za-zĀ-ſāīūṛṝḷḹṃḥśṣñṅṭḍṇçġ][A-Za-zĀ-ſāīūṛṝḷḹṃḥśṣñṅṭḍṇçġ'’\-\.\s]*[A-Za-zĀ-ſāīūṛṝḷḹṃḥśṣñṅṭḍṇçġ]")
IAST_ITEM_SPLIT = re.compile(r"\s*---\s*|\s*—\s*|\n+")
IAST_ITEM_MARKER = re.compile(r"^\d+[\\)\.]\s*|^[IVXL]+[\\)\.]\s*")
# Leading grammar-note abbreviations ("impf. отъ ...", "opt. med. ...") — not
# exercise sentences, strip the run entirely if it starts with one.
GRAMMAR_NOTE_START = re.compile(
    r"^(impf|imper|opt|pass|fut|med|caus|pf|pr|pp|sg|pl|du|Ā|P|V|U)\.?\s",
)


def strip_footnotes(text):
    return FOOTNOTE_MARK.sub("", text)


def lesson_spans(text, lesson_re):
    """Return [(lesson_id, start, end), ...] slicing text by lesson headers."""
    matches = list(lesson_re.finditer(text))
    spans = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        lesson_id = m.group(1)
        spans.append((lesson_id, start, end))
    if not matches:
        spans.append(("_", 0, len(text)))
    return spans


def split_devanagari_sentences(chunk):
    """Pull Devanagari runs out of a chunk of mdx text, split on danda/double-danda."""
    chunk = strip_footnotes(chunk)
    sentences = []
    for run in DEVANAGARI_RUN.findall(chunk):
        for piece in re.split(r"[।॥]", run):
            piece = piece.translate(DEVA_DIGITS).strip()
            piece = re.sub(r"\s+", " ", piece)
            # Drop bare lesson-number markers, single vocab words, digit noise.
            if len(piece) < 6 or piece.isdigit() or len(piece.split()) < 2:
                continue
            sentences.append(piece)
    return sentences


def split_iast_sentences(chunk):
    """Pull IAST (diacritic Latin) sentence-like runs out of a chunk of mdx text."""
    chunk = strip_footnotes(chunk)
    sentences = []
    for run in LATIN_RUN.findall(chunk):
        if not IAST_DIACRITIC.search(run):
            continue  # plain Latin (headings, English/German glosses) — skip
        for piece in IAST_ITEM_SPLIT.split(run):
            piece = IAST_ITEM_MARKER.sub("", piece).strip(" .\\")
            piece = re.sub(r"\s+", " ", piece)
            if len(piece) < 6 or not IAST_DIACRITIC.search(piece):
                continue
            if GRAMMAR_NOTE_START.match(piece):
                continue
            # Require at least two words — single transliterated terms
            # (vocab entries, grammar-example stems like "vad-ā-mi") are noise.
            if len(piece.split()) < 2:
                continue
            sentences.append(piece)
    return sentences


def extract():
    all_sentences = []
    for book_id, cfg in BOOKS.items():
        with open(cfg["path"], encoding="utf-8") as f:
            text = f.read()
        idx = 0
        for lesson_id, start, end in lesson_spans(text, cfg["lesson_re"]):
            chunk = text[start:end]
            for sent in split_devanagari_sentences(chunk):
                idx += 1
                all_sentences.append({
                    "id": f"{book_id}-{lesson_id}-{idx}",
                    "book": book_id,
                    "book_label": cfg["label"],
                    "year": cfg["year"],
                    "lesson": lesson_id,
                    "script": "deva",
                    "text": sent,
                })
            for sent in split_iast_sentences(chunk):
                idx += 1
                all_sentences.append({
                    "id": f"{book_id}-{lesson_id}-{idx}",
                    "book": book_id,
                    "book_label": cfg["label"],
                    "year": cfg["year"],
                    "lesson": lesson_id,
                    "script": "iast",
                    "text": sent,
                })
        n_deva = sum(1 for s in all_sentences if s["book"] == book_id and s["script"] == "deva")
        n_iast = sum(1 for s in all_sentences if s["book"] == book_id and s["script"] == "iast")
        print(f"{book_id}: {n_deva} deva + {n_iast} iast sentence candidates", file=sys.stderr)
    out_path = os.path.join(DATA_DIR, "sentences.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_sentences, f, ensure_ascii=False, indent=2)
    print(f"wrote {out_path}", file=sys.stderr)


def normalize_for_match(text, script):
    text = re.sub(r"[‌‍]", "", text)  # ZWJ/ZWNJ noise from Word
    if script == "iast":
        text = text.lower()
        text = text.replace("’", "'")
        text = re.sub(r"['\-\.]", "", text)
    text = re.sub(r"\s+", "", text)
    return text


def match(threshold=0.82):
    with open(os.path.join(DATA_DIR, "sentences.json"), encoding="utf-8") as f:
        sentences = json.load(f)
    by_key = {}  # (book, script) -> [sentence, ...]
    for s in sentences:
        by_key.setdefault((s["book"], s["script"]), []).append(s)

    book_ids = list(BOOKS.keys())
    book_pairs = [(book_ids[i], book_ids[j]) for i in range(len(book_ids)) for j in range(i + 1, len(book_ids))]

    results = []
    for a, b in book_pairs:
        for script in ("deva", "iast"):
            for sa in by_key.get((a, script), []):
                na = normalize_for_match(sa["text"], script)
                if len(na) < 6:
                    continue
                for sb in by_key.get((b, script), []):
                    nb = normalize_for_match(sb["text"], script)
                    if len(nb) < 6:
                        continue
                    if abs(len(na) - len(nb)) > max(len(na), len(nb)) * 0.4:
                        continue
                    ratio = SequenceMatcher(None, na, nb).ratio()
                    if ratio >= threshold:
                        results.append({
                            "score": round(ratio, 3),
                            "exact": na == nb,
                            "script": script,
                            "a": sa,
                            "b": sb,
                        })
    results.sort(key=lambda r: -r["score"])
    out_path = os.path.join(DATA_DIR, "matches.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    exact_n = sum(1 for r in results if r["exact"])
    print(f"{len(results)} candidate matches ({exact_n} exact) >= {threshold}", file=sys.stderr)
    print(f"wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "extract"
    if cmd == "extract":
        extract()
    elif cmd == "match":
        match()
    else:
        print("usage: extract_sentences.py [extract|match]", file=sys.stderr)
        sys.exit(1)
