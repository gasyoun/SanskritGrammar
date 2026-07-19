#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PWG compound (samāsa) segmentation layer — cheap high-value splitter gold.

PWG analyses a compound headword in its etymology parenthesis as a `+`-joined chain
of members in SLP1: `{#aMSaka#}¦ ({#aMSa#} + {#karaRa#})`. This extracts the surface
compound → its ordered underlying members — exactly the surface↔underlying pairing a
sandhi/segmentation splitter is trained and evaluated on. One regex pass over the
committed pwg.txt (read-only), so it is cheap to regenerate.

Only the FIRST `+`-chain in the entry head (the etymology paren) is taken, and only
when it has ≥2 members whose first member is a prefix-compatible lead of the headword —
this keeps citation-run `{#..#}` noise out. Members keep PWG's order.

Emits (repo `data/pwg_compound_split/` by default, or --out):
  pwg_compound_splits.tsv   headword_slp1 · headword_iast · L_id · arity · members(+-sep)
  pwg_compound_summary.json counts + arity distribution

Deterministic. Reuse: an independent gold reference for the kosha DCS-sandhi programme
and SanskritSpellCheck splitters; a compound-formation teaching surface; a feed for the
pwg_ru translation. Sibling cheap PWG layers: derivation (`von {#base#}`), the Pāṇini
sūtra crosswalk, and German sense glosses.

Usage:
    python scripts/pwg_compound_split.py
"""
import argparse
import json
import re
import sys
from collections import Counter
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


# a `+`-joined chain of {#..#} members (optional <hom> before a member)
CHAIN = re.compile(r'\{#[^#]+#\}(?:\s*\+\s*(?:<hom>[^<]*</hom>\s*)?\{#[^#]+#\})+')
MEMBER = re.compile(r'\{#([^#]+)#\}')
# a fully-spelled SLP1 member: ASCII letters only. Rejects PWG's abbreviation mark
# `˚` (A˚ = repeat-of-headword-stem, truncated), em-dashes, spaces, digits — those
# members are not usable as splitter gold.
CLEAN_MEMBER = re.compile(r'^[A-Za-z]+$')


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


def lead_ok(hw, first):
    """Headword should begin with the first member's leading (consonant) segment —
    tolerant of vṛddhi/sandhi at the seam, strict enough to reject citation noise."""
    if not first:
        return False
    a = first[:2]
    return hw.startswith(first[:1]) and (hw.startswith(a) or len(first) <= 2 or hw[:1] == first[:1])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pwg", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--head", type=int, default=400, help="chars of entry head to scan")
    args = ap.parse_args()
    here = Path(__file__).resolve()
    repo = here.parents[1]
    github = here.parents[2]
    pwg = Path(args.pwg) if args.pwg else github / "csl-orig" / "v02" / "pwg" / "pwg.txt"
    if not pwg.exists():
        print(f"ERROR: pwg.txt not found: {pwg}", file=sys.stderr)
        return 1
    out = Path(args.out) if args.out else repo / "data" / "pwg_compound_split"
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    by_arity = Counter()
    skipped_abbrev = 0
    for L, hw, body in entries(pwg):
        m = CHAIN.search(body[:args.head])
        if not m:
            continue
        members = MEMBER.findall(m.group(0))
        if len(members) < 2:
            continue
        if not all(CLEAN_MEMBER.match(x) for x in members):
            skipped_abbrev += 1   # abbreviated (A˚) / dash-joined / noisy members
            continue
        if not lead_ok(hw, members[0]):
            continue
        by_arity[len(members)] += 1
        rows.append((hw, L, members))

    rows.sort(key=lambda r: (r[0], int(r[1])))
    tsv = out / "pwg_compound_splits.tsv"
    with tsv.open("w", encoding="utf-8", newline="") as f:
        f.write("headword_slp1\theadword_iast\tL_id\tarity\tmembers_slp1\tmembers_iast\n")
        for hw, L, members in rows:
            f.write(f"{hw}\t{to_iast(hw)}\t{L}\t{len(members)}\t"
                    f"{' + '.join(members)}\t{' + '.join(to_iast(x) for x in members)}\n")

    summary = {
        "study": "PWG compound (samāsa) segmentation layer",
        "as_of": "2026-07-19",
        "source": "csl-orig/v02/pwg/pwg.txt (read-only)",
        "method": "first `+`-joined {#member#} chain in the entry head, ≥2 members, lead-compatible with the headword",
        "compounds": len(rows),
        "arity_distribution": dict(sorted(by_arity.items())),
        "excluded_abbreviated_member_analyses": skipped_abbrev,
        "note": ("PWG abbreviates a repeated stem with `˚` (A˚); such analyses are excluded here "
                 "because the member is truncated — only fully-spelled member splits are kept."),
    }
    (out / "pwg_compound_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"compounds: {len(rows)}")
    print(f"arity: {dict(sorted(by_arity.items()))}")
    print(f"wrote {tsv.name} + pwg_compound_summary.json → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
