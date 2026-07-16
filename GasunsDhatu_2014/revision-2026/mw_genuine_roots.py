#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M03 Гл.1 Приложение (H1006): подлинные корни словаря Монье-Уильямса.

Consumes the Cologne MW root table (csl-orig v02/mw/mw_roots.tsv), whose own
`verb_type` column already distinguishes genuine roots (`genuineroot`) from
secondary/artificial ones (`root`). Emits:
  * mw_genuine_roots.tsv       — all 2113 MW roots + a `genuine` flag (1/0)
  * mw_genuine_roots_list.md   — print-ready compact list of the 750 genuine roots (★)
  * prints the split summary

Reproducible; no judgement added — the genuine/secondary call is MW's own.
Run from the repo root (paths relative to it).
"""
import csv, io, sys, os
sys.stdout.reconfigure(encoding='utf-8')

SRC = os.environ.get('MW_ROOTS_TSV', '../csl-orig/v02/mw/mw_roots.tsv')
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
TSV_OUT = os.path.join(OUT_DIR, 'mw_genuine_roots.tsv')
LIST_OUT = os.path.join(OUT_DIR, 'mw_genuine_roots_list.md')

with io.open(SRC, encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter='\t'))

for r in rows:
    r['genuine'] = 1 if (r.get('verb_type') or '').strip() == 'genuineroot' else 0

genuine = [r for r in rows if r['genuine']]
secondary = [r for r in rows if not r['genuine']]

# ---- full flagged dataset (MW entry order by mw_L) ----
def as_int(v):
    try: return int(v)
    except: return 1 << 30
rows_sorted = sorted(rows, key=lambda r: as_int(r.get('mw_L')))
cols = ['mw_L', 'root_iast', 'k1_slp1', 'verb_type', 'genuine', 'classes', 'whitney_anchor', 'westergaard']
with io.open(TSV_OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(cols)
    for r in rows_sorted:
        w.writerow([r.get(c, '') for c in cols])

# ---- print-ready compact list of the 750 genuine roots, alpha by IAST ----
gen_sorted = sorted(genuine, key=lambda r: ((r.get('root_iast') or '').lower(), as_int(r.get('mw_L'))))
with io.open(LIST_OUT, 'w', encoding='utf-8', newline='') as f:
    f.write('# Подлинные корни словаря Монье-Уильямса (★ = genuineroot)\n\n')
    f.write('_Сгенерировано `mw_genuine_roots.py` из `csl-orig/v02/mw/mw_roots.tsv`. '
            'Всего %d подлинных из %d корневых статей MW._\n\n' % (len(genuine), len(rows)))
    for r in gen_sorted:
        cl = (r.get('classes') or '').strip()
        f.write('- ★ √*%s*%s\n' % (r.get('root_iast', ''), (' — кл. %s' % cl) if cl else ''))

print('MW root entries:', len(rows))
print('  genuine (verb_type=genuineroot):', len(genuine))
print('  secondary (verb_type=root):', len(secondary))
print('wrote:', os.path.basename(TSV_OUT), '(%d rows)' % len(rows))
print('wrote:', os.path.basename(LIST_OUT), '(%d genuine roots)' % len(genuine))
