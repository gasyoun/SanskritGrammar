#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PWG <lex> POS/gender layer — the grammatical category per entry, homonym-precise.

PWG tags each entry's grammatical category with `<lex>m.</lex>` / `<lex>adj.</lex>` etc.
Only 17 distinct raw values across 130,864 tags. This one-pass extraction records, per
entry (L_id · k1 · hom): the raw `<lex>` tags in the entry and a normalised primary POS.
A homonym-precise POS field, and a cross-check surface for the pwg_ru headword index's
own `lex` column.

Read-only over the committed pwg.txt. Emits data/pwg_lex_pos/pwg_lex_pos.tsv
(L_id · k1 · hom · primary_pos · lex_raw[|-joined]) + a summary. Deterministic.

    python scripts/pwg_lex_pos.py
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

LEX = re.compile(r'<lex>([^<]+)</lex>')
RE_L = re.compile(r'<L>(\d+)')
RE_K1 = re.compile(r'<k1>([^<]*)')
RE_H = re.compile(r'<h>(\d+)')

# normalise the 17 raw tags to a compact POS vocabulary
NORM = {
    'm.': 'm', 'mm.': 'm', 'f.': 'f', 'ff.': 'f', 'fem.': 'f', 'femin.': 'f',
    'n.': 'n', 'neutr.': 'n', 'adj.': 'adj', 'adv.': 'adv',
    'indecl.': 'indecl', 'ind.': 'indecl', 'interj.': 'interj',
    'm.n.': 'm.n', 'f.n.': 'f.n', 'm.f.': 'm.f', 'm.f.n.': 'm.f.n',
}


def entries(path):
    lid = k1 = hom = None
    buf, on = [], False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('<L>'):
            ml, mk = RE_L.search(ln), RE_K1.search(ln)
            if ml and mk:
                if on and lid:
                    yield lid, k1, hom, buf
                mh = RE_H.search(ln)
                lid, k1, hom = ml.group(1), mk.group(1), (mh.group(1) if mh else '')
                buf, on = [], True
                continue
        if on:
            if ln.startswith('<LEND>'):
                yield lid, k1, hom, buf
                on = False
            else:
                buf.append(ln)


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
    out = Path(args.out) if args.out else repo / 'data' / 'pwg_lex_pos'
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    pos_ctr = Counter()
    for lid, k1, hom, buf in entries(pwg):
        tags = [t.strip() for t in LEX.findall('\n'.join(buf))]
        if not tags:
            continue
        # primary POS = first tag, normalised
        primary = NORM.get(tags[0], tags[0].rstrip('.'))
        pos_ctr[primary] += 1
        rows.append((lid, k1, hom, primary, '|'.join(tags)))

    rows.sort(key=lambda r: int(r[0]))
    tsv = out / 'pwg_lex_pos.tsv'
    with tsv.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['L_id', 'k1', 'hom', 'primary_pos', 'lex_raw'])
        for r in rows:
            w.writerow(r)

    summary = {
        'study': 'PWG <lex> POS/gender layer',
        'as_of': '2026-07-19',
        'source': 'csl-orig/v02/pwg/pwg.txt (read-only)',
        'entries_with_lex': len(rows),
        'by_primary_pos': dict(pos_ctr.most_common()),
    }
    (out / 'pwg_lex_pos_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('entries %d | primary POS %s' % (len(rows), dict(pos_ctr.most_common())), file=sys.stderr)
    print('wrote %s + summary' % tsv.name, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
