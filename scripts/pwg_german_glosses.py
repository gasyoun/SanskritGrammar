#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PWG German sense-gloss layer — the German meaning spans per entry, homonym-precise.

PWG marks every German meaning/translation span with `{%…%}`
(`{#akarman#}¦ … <lex>n.</lex> {%das Nichthandeln%}`). This one-pass extraction pulls
them out per entry, keyed by PWG `L_id` + headword + homonym (`<h>`) — so it is
homonym-precise from the start (unlike the headword-aggregated Pāṇini crosswalk).

Read-only over the committed pwg.txt. Cheap to regenerate. A structured bilingual
gloss / translation-memory seed and a per-sense German inventory; complements (not
duplicates) the pwg_ru full-prose translation — this is the meaning spans alone.

Emits data/pwg_german_glosses/pwg_german_glosses.tsv
(L_id · k1 · hom · n_glosses · glosses[‖-joined]) + a summary. Deterministic.

    python scripts/pwg_german_glosses.py
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

RE_L = re.compile(r'<L>(\d+)')
RE_K1 = re.compile(r'<k1>([^<]*)')
RE_H = re.compile(r'<h>(\d+)')
GLOSS = re.compile(r'\{%([^%]+)%\}')
PAGE = re.compile(r'\s*\[Page[^\]]*\]\s*')      # PWG page-break marker leaking into a gloss
GLOSS_SEP = ' ‖ '          # U+2016; does not occur in the German prose


def clean_gloss(g):
    return re.sub(r'\s+', ' ', PAGE.sub(' ', g)).strip()


def entries(path):
    """Yield (L_id, k1, hom, body) per <L>…<LEND> entry."""
    lid = k1 = hom = None
    buf, on = [], False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('<L>'):
            ml, mk = RE_L.search(ln), RE_K1.search(ln)
            if ml and mk:
                if on and lid:
                    yield lid, k1, hom, '\n'.join(buf)
                mh = RE_H.search(ln)
                lid, k1, hom = ml.group(1), mk.group(1), (mh.group(1) if mh else '')
                buf, on = [], True
                continue
        if on:
            if ln.startswith('<LEND>'):
                yield lid, k1, hom, '\n'.join(buf)
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
    out = Path(args.out) if args.out else repo / 'data' / 'pwg_german_glosses'
    out.mkdir(parents=True, exist_ok=True)

    rows = []
    n_gloss = 0
    entries_with = 0
    for lid, k1, hom, body in entries(pwg):
        gl = [c for c in (clean_gloss(g) for g in GLOSS.findall(body)) if c]
        if not gl:
            continue
        entries_with += 1
        n_gloss += len(gl)
        rows.append((lid, k1, hom, gl))

    rows.sort(key=lambda r: int(r[0]))
    tsv = out / 'pwg_german_glosses.tsv'
    with tsv.open('w', encoding='utf-8', newline='') as f:
        f.write('L_id\tk1\thom\tn_glosses\tglosses\n')
        for lid, k1, hom, gl in rows:
            safe = [g.replace('\t', ' ').replace(GLOSS_SEP.strip(), '/') for g in gl]
            f.write('%s\t%s\t%s\t%d\t%s\n' % (lid, k1, hom, len(gl), GLOSS_SEP.join(safe)))

    summary = {
        'study': 'PWG German sense-gloss layer',
        'as_of': '2026-07-19',
        'source': 'csl-orig/v02/pwg/pwg.txt (read-only)',
        'total_glosses': n_gloss,
        'entries_with_glosses': entries_with,
        'avg_glosses_per_entry': round(n_gloss / entries_with, 2) if entries_with else 0,
        'gloss_separator': GLOSS_SEP.strip(),
    }
    (out / 'pwg_german_glosses_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('glosses %d across %d entries (avg %.2f/entry)'
          % (n_gloss, entries_with, summary['avg_glosses_per_entry']), file=sys.stderr)
    print('wrote %s + summary' % tsv.name, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
