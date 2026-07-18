#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PWG → Aṣṭādhyāyī (Pāṇini sūtra) crosswalk — cheap, high-value derivation layer.

The großes Petersburger Wörterbuch cites the Pāṇinian sūtra that licenses a form as
`P. a,b` (pāda) or `P. a,b,c` (adhyāya.pāda.sūtra). This extracts every reference and
builds both directions — headword ↔ sūtra — a rare corpus↔grammar index that is normally
expensive to assemble. One regex pass over the committed pwg.txt (read-only).

Emits (next to the input by default, or --out):
  pwg_panini_word2sutra.tsv   headword_slp1 · headword_iast · L_id · sutras(|-sep)
  pwg_panini_sutra2word.tsv   sutra · n_words · words_iast(|-sep, capped)
  pwg_panini_summary.json     counts + top-cited sūtras

Deterministic. Reusable for any consumer (pwg_ru translation, an Aṣṭādhyāyī interface,
derivation pedagogy). See also the compound-split and derivation layers from the same source.
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

SLP1 = {'A': 'ā', 'I': 'ī', 'U': 'ū', 'f': 'ṛ', 'F': 'ṝ', 'x': 'ḷ', 'X': 'ḹ',
        'E': 'ai', 'O': 'au', 'M': 'ṃ', 'H': 'ḥ', 'K': 'kh', 'G': 'gh', 'N': 'ṅ',
        'C': 'ch', 'J': 'jh', 'Y': 'ñ', 'w': 'ṭ', 'W': 'ṭh', 'q': 'ḍ', 'Q': 'ḍh',
        'R': 'ṇ', 'T': 'th', 'D': 'dh', 'P': 'ph', 'B': 'bh', 'S': 'ś', 'z': 'ṣ',
        '~': 'm̐', '|': '', '@': ''}


def to_iast(s):
    return ''.join(SLP1.get(c, c) for c in s)


# `P. a,b` or `P. a,b,c` (with an optional `.d` continuation on the sūtra number)
SUTRA = re.compile(r'\bP\.\s*(\d+),\s*(\d+)(?:,\s*(\d+))?')


def entries(path):
    L = hw = None
    buf, on = [], False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        h = re.match(r'<L>(\d+).*?<k1>([^<]*)', ln)
        if h:
            if on and L:
                yield L, hw, '\n'.join(buf)
            L, hw = h.group(1), h.group(2)
            buf, on = [], True
            continue
        if on:
            if ln.startswith('<LEND>'):
                yield L, hw, '\n'.join(buf)
                on = False
            else:
                buf.append(ln)


def sutra_key(a, b, c):
    """Sortable (adhyāya, pāda, sūtra|0) plus a display string."""
    return (int(a), int(b), int(c) if c else 0), (f"{a}.{b}.{c}" if c else f"{a}.{b}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pwg", default=None, help="path to pwg.txt")
    ap.add_argument("--out", default=None, help="output directory")
    args = ap.parse_args()
    here = Path(__file__).resolve()
    repo = here.parents[1]        # SanskritGrammar
    github = here.parents[2]      # GitHub/
    pwg = Path(args.pwg) if args.pwg else github / "csl-orig" / "v02" / "pwg" / "pwg.txt"
    if not pwg.exists():
        print(f"ERROR: pwg.txt not found: {pwg}", file=sys.stderr)
        return 1
    out = Path(args.out) if args.out else repo / "data" / "pwg_panini_crosswalk"
    out.mkdir(parents=True, exist_ok=True)

    word2sutra = {}          # headword_slp1 -> (L_id, sorted set of display sutras)
    sutra2word = defaultdict(set)
    sortkey = {}
    n_refs = full = partial = 0
    for L, hw, body in entries(pwg):
        found = set()
        for m in SUTRA.finditer(body):
            a, b, c = m.groups()
            n_refs += 1
            full += 1 if c else 0
            partial += 0 if c else 1
            sk, disp = sutra_key(a, b, c)
            sortkey[disp] = sk
            found.add(disp)
            sutra2word[disp].add(to_iast(hw))
        if found:
            prev = word2sutra.get(hw)
            merged = (prev[1] if prev else set()) | found
            word2sutra[hw] = (L, merged)

    # word → sūtra
    w2s = out / "pwg_panini_word2sutra.tsv"
    with w2s.open("w", encoding="utf-8", newline="") as f:
        f.write("headword_slp1\theadword_iast\tL_id\tn_sutras\tsutras\n")
        for hw in sorted(word2sutra):
            L, s = word2sutra[hw]
            ss = sorted(s, key=lambda d: sortkey[d])
            f.write(f"{hw}\t{to_iast(hw)}\t{L}\t{len(ss)}\t{'|'.join('P.'+x for x in ss)}\n")

    # sūtra → word
    s2w = out / "pwg_panini_sutra2word.tsv"
    with s2w.open("w", encoding="utf-8", newline="") as f:
        f.write("sutra\tn_words\twords_iast\n")
        for disp in sorted(sutra2word, key=lambda d: sortkey[d]):
            ws = sorted(sutra2word[disp])
            capped = ws[:50]
            more = f"|+{len(ws) - 50}" if len(ws) > 50 else ""
            f.write(f"P.{disp}\t{len(ws)}\t{'|'.join(capped)}{more}\n")

    top = sorted(sutra2word.items(), key=lambda kv: -len(kv[1]))[:25]
    summary = {
        "study": "PWG → Aṣṭādhyāyī (Pāṇini sūtra) crosswalk",
        "as_of": "2026-07-18",
        "source": "csl-orig/v02/pwg/pwg.txt (read-only)",
        "total_sutra_refs": n_refs,
        "full_abc_refs": full,
        "pada_only_refs": partial,
        "distinct_words": len(word2sutra),
        "distinct_sutras": len(sutra2word),
        "top_cited_sutras": [{"sutra": "P." + d, "n_words": len(w)} for d, w in top],
    }
    (out / "pwg_panini_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"sūtra refs {n_refs} (full {full} / pāda-only {partial})")
    print(f"distinct words {len(word2sutra)} · distinct sūtras {len(sutra2word)}")
    print(f"wrote {w2s.name}, {s2w.name}, pwg_panini_summary.json → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
