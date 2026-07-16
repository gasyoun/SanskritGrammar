#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M03 Гл.1 Приложение (H1006 + enrichment H1006b): подлинные корни словаря
Монье-Уильямса, обогащённые корпусной частотой и межсловарным согласием.

Consumes:
  * csl-orig v02/mw/mw_roots.tsv           — MW `verb_type` (genuineroot / root)
  * WhitneyRoots/crosswalk/roots.csv       — DCS частота/ранг (dcs_freq, dcs_rank)
  * csl-orig v02/etymology_stats/root_oracle.tsv — межсловарное согласие (# словарей)

Emits:
  * mw_genuine_roots.tsv       — все 2113 MW-корней + флаг genuine + dcs_freq/dcs_rank/n_dicts
  * mw_genuine_roots_list.md   — печатный список 750 подлинных (★), с частотой и согласием
  * prints the split + core/tail cross-tab

Join key = root_iast. Частота DCS присвоена поверхностной форме, поэтому омонимы
разделяют одно значение (как в Приложении 3). Разметка подлинный/вторичный — MW,
не наше суждение. Run from the repo root.
"""
import csv, io, sys, os
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

MW = os.environ.get('MW_ROOTS_TSV', '../csl-orig/v02/mw/mw_roots.tsv')
ROOTS_CSV = os.environ.get('WHITNEY_ROOTS_CSV', '../WhitneyRoots/crosswalk/roots.csv')
ORACLE = os.environ.get('ROOT_ORACLE_TSV', '../csl-orig/v02/etymology_stats/root_oracle.tsv')
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
TSV_OUT = os.path.join(OUT_DIR, 'mw_genuine_roots.tsv')
LIST_OUT = os.path.join(OUT_DIR, 'mw_genuine_roots_list.md')

def as_int(v, default=1 << 30):
    try: return int(float(v))
    except: return default

# ---- MW roots + genuine flag ----
with io.open(MW, encoding='utf-8') as f:
    mw = list(csv.DictReader(f, delimiter='\t'))
for r in mw:
    r['genuine'] = 1 if (r.get('verb_type') or '').strip() == 'genuineroot' else 0

# ---- DCS freq/rank by root_iast (best over homonyms) ----
freq, rank = defaultdict(int), {}
with io.open(ROOTS_CSV, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        k = (r.get('root_iast') or '').strip()
        fv = as_int(r.get('dcs_freq'), 0)
        if fv >= freq[k]:
            freq[k] = fv
            rank[k] = as_int(r.get('dcs_rank'), 0)

# ---- root_oracle: distinct dictionaries per root_iast ----
ndict = defaultdict(set)
with io.open(ORACLE, encoding='utf-8') as f:
    h = f.readline().rstrip('\n').split('\t')
    ri, si = h.index('root_iast'), h.index('sources')
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) > max(ri, si):
            for s in p[si].split(','):
                if s.strip():
                    ndict[p[ri]].add(s.strip())

def enrich(r):
    k = (r.get('root_iast') or '').strip()
    r['dcs_freq'] = freq.get(k, 0)
    r['dcs_rank'] = rank.get(k, '') if freq.get(k, 0) else ''
    r['n_dicts'] = len(ndict.get(k, ()))

for r in mw:
    enrich(r)

# ---- full flagged + enriched dataset (MW entry order) ----
cols = ['mw_L', 'root_iast', 'k1_slp1', 'verb_type', 'genuine', 'classes',
        'dcs_freq', 'dcs_rank', 'n_dicts', 'whitney_anchor', 'westergaard']
rows_sorted = sorted(mw, key=lambda r: as_int(r.get('mw_L')))
with io.open(TSV_OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(cols)
    for r in rows_sorted:
        w.writerow([r.get(c, '') for c in cols])

# ---- print-ready enriched list of the 750 genuine, alpha by IAST ----
genuine = [r for r in mw if r['genuine']]
gen_sorted = sorted(genuine, key=lambda r: ((r.get('root_iast') or '').lower(), as_int(r.get('mw_L'))))
with io.open(LIST_OUT, 'w', encoding='utf-8', newline='') as f:
    f.write('# Подлинные корни словаря Монье-Уильямса (★ = genuineroot), обогащённые\n\n')
    f.write('_Сгенерировано `mw_genuine_roots.py` из `mw_roots.tsv` (verb_type) + `roots.csv` '
            '(частота DCS) + `root_oracle.tsv` (число словарей). Всего %d подлинных из %d статей MW. '
            'Формат: ★ √корень — кл. классы · DCS частота (ранг) · N словарей._\n\n' % (len(genuine), len(mw)))
    for r in gen_sorted:
        cl = (r.get('classes') or '').strip()
        fparts = []
        if cl: fparts.append('кл. %s' % cl)
        if r['dcs_freq']: fparts.append('DCS %s%s' % (r['dcs_freq'], (' #%s' % r['dcs_rank']) if r['dcs_rank'] else ''))
        else: fparts.append('DCS —')
        fparts.append('%d слов.' % r['n_dicts'])
        f.write('- ★ √*%s* — %s\n' % (r.get('root_iast', ''), ' · '.join(fparts)))

# ---- summary + core/tail cross-tab (by distinct root_iast) ----
gi = sorted(set((r.get('root_iast') or '').strip() for r in genuine))
att = [k for k in gi if freq.get(k, 0) > 0]
hi = [k for k in gi if len(ndict.get(k, ())) >= 4]
core = [k for k in gi if freq.get(k, 0) > 0 and len(ndict.get(k, ())) >= 4]
tail = [k for k in gi if freq.get(k, 0) == 0 and len(ndict.get(k, ())) <= 1]
print('MW root entries:', len(mw), '| genuine:', len(genuine), '| secondary:', len(mw) - len(genuine))
print('distinct genuine root_iast:', len(gi))
print('  DCS-attested:', len(att), '(%.0f%%)' % (100 * len(att) / len(gi)))
print('  cross-consensus >=4 dicts:', len(hi))
print('  CORE (attested & >=4 dicts):', len(core))
print('  TAIL (unattested & <=1 dict):', len(tail))
print('wrote:', os.path.basename(TSV_OUT), '(%d rows)' % len(mw))
print('wrote:', os.path.basename(LIST_OUT), '(%d genuine)' % len(genuine))
