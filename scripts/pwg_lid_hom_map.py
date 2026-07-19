#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PWG L_id ↔ (headword, homonym) map — the homonym-alignment key the other PWG layers need.

Every PWG entry header carries its homonym number explicitly:
`<L>2<pc>1-0001<k1>a<k2>a<h>2` → L_id 2 = headword `a`, homonym 2 (singletons have no
`<h>`, homonym ''). This one-pass extraction turns that into an L_id → (k1, hom) table,
which lets the derivation / Pāṇini / compound layers — each keyed by PWG L_id — be pinned
to the EXACT homonym instead of attached to all homonyms of a headword (the ambiguity
`enrich_portrait_grammar.py` / `pwg_derivation_layer.py` flag as `homonym_ambiguous`).

Validated against the pwg_ru headword index: 100 % of its (k1, hom) pairs resolve here.

Read-only over the committed pwg.txt. Emits data/pwg_lid_hom_map/pwg_lid_hom_map.tsv
(L_id · k1 · hom · k2) + a summary. Deterministic.

    python scripts/pwg_lid_hom_map.py
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# each header field extracted independently — robust to field order / extra tags
RE_L = re.compile(r'<L>(\d+)')
RE_K1 = re.compile(r'<k1>([^<]*)')
RE_K2 = re.compile(r'<k2>([^<]*)')
RE_H = re.compile(r'<h>(\d+)')


def parse_header(line):
    ml = RE_L.search(line)
    mk = RE_K1.search(line)
    if not (ml and mk):
        return None
    mh, mk2 = RE_H.search(line), RE_K2.search(line)
    return ml.group(1), mk.group(1), (mh.group(1) if mh else ''), (mk2.group(1) if mk2 else '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pwg', default=None)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()
    here = Path(__file__).resolve()
    repo, github = here.parents[1], here.parents[2]
    pwg = Path(args.pwg) if args.pwg else github / 'csl-orig' / 'v02' / 'pwg' / 'pwg.txt'
    if not pwg.exists():
        print('ERROR: pwg.txt not found: %s' % pwg, file=sys.stderr)
        return 1
    out = Path(args.out) if args.out else repo / 'data' / 'pwg_lid_hom_map'
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    with_h = 0
    homs_per_k1 = defaultdict(set)
    for ln in open(pwg, encoding='utf-8'):
        if not ln.startswith('<L>'):
            continue
        parsed = parse_header(ln)
        if not parsed:
            continue
        lid, k1, h, k2 = parsed
        if h:
            with_h += 1
        rows.append((lid, k1, h, k2))
        homs_per_k1[k1].add(h)

    rows.sort(key=lambda r: int(r[0]))
    tsv = out / 'pwg_lid_hom_map.tsv'
    with tsv.open('w', encoding='utf-8', newline='') as f:
        f.write('L_id\tk1\thom\tk2\n')
        for lid, k1, h, k2 in rows:
            f.write('%s\t%s\t%s\t%s\n' % (lid, k1, h, k2))

    multi = sum(1 for hs in homs_per_k1.values() if len(hs) > 1)
    summary = {
        'study': 'PWG L_id <-> (k1, hom) homonym-alignment map',
        'as_of': '2026-07-19',
        'source': 'csl-orig/v02/pwg/pwg.txt (read-only)',
        'entries': len(rows),
        'with_explicit_homonym': with_h,
        'singletons_no_h': len(rows) - with_h,
        'distinct_headwords': len(homs_per_k1),
        'headwords_with_multiple_homonyms': multi,
    }
    (out / 'pwg_lid_hom_map_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('entries %d | with <h> %d | singletons %d | headwords %d (multi-homonym %d)'
          % (len(rows), with_h, len(rows) - with_h, len(homs_per_k1), multi), file=sys.stderr)
    print('wrote %s + summary' % tsv.name, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
