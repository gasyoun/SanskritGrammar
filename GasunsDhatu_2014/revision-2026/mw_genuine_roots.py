#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M03 Гл.1 Приложение (H1006 + enrichment H1006b, join-key reconcile H1034):
подлинные корни словаря Монье-Уильямса, обогащённые корпусной частотой и
межсловарным согласием.

Consumes:
  * csl-orig v02/mw/mw_roots.tsv           — MW `verb_type` (genuineroot / root)
  * WhitneyRoots/crosswalk/roots.csv       — DCS частота/ранг/периоды (dcs_freq, dcs_rank, period_tags)
  * csl-orig v02/etymology_stats/root_oracle.tsv — межсловарное согласие (# словарей)

Emits:
  * mw_genuine_roots.tsv       — все 2113 MW-корней + флаг genuine + dcs_freq/dcs_rank/n_dicts/dcs_periods
  * mw_genuine_roots_list.md   — печатный список 750 подлинных (★), с частотой, согласием и периодом
  * mw_genuine_roots_enrich_provenance.json — покрытие · распределение по периодам · топ-20 по частоте
  * prints the split + core/tail cross-tab + period distribution

Join key = SLP1 (MW `k1_slp1` ↔ DCS `root_slp1` ↔ oracle `root_slp1`) — устойчив к
диакритике/нумерации омонимов, где IAST-поверхностный ключ недосчитывает (SLP1 покрывает
на ~100 корней больше DCS, ~40 больше оракула). Частота DCS — лучшая по омонимам, делящим
одну SLP1-форму. Разметка подлинный/вторичный — MW, не наше суждение. Run from the repo root.
"""
import csv, io, sys, os, json
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

MW = os.environ.get('MW_ROOTS_TSV', '../csl-orig/v02/mw/mw_roots.tsv')
ROOTS_CSV = os.environ.get('WHITNEY_ROOTS_CSV', '../WhitneyRoots/crosswalk/roots.csv')
ORACLE = os.environ.get('ROOT_ORACLE_TSV', '../csl-orig/v02/etymology_stats/root_oracle.tsv')
OUT_DIR = os.path.dirname(os.path.abspath(__file__))
TSV_OUT = os.path.join(OUT_DIR, 'mw_genuine_roots.tsv')
LIST_OUT = os.path.join(OUT_DIR, 'mw_genuine_roots_list.md')
PROV_OUT = os.path.join(OUT_DIR, 'mw_genuine_roots_enrich_provenance.json')

# DCS attestation periods, chronological (union rendered in this order).
PERIOD_ORDER = ['RV', 'AV', 'V', 'B', 'S', 'E', 'C']

def as_int(v, default=1 << 30):
    try: return int(float(v))
    except: return default

# ---- MW roots + genuine flag ----
with io.open(MW, encoding='utf-8') as f:
    mw = list(csv.DictReader(f, delimiter='\t'))
for r in mw:
    r['genuine'] = 1 if (r.get('verb_type') or '').strip() == 'genuineroot' else 0

# ---- DCS freq/rank/periods by root_slp1 (freq: best over homonyms; periods: union) ----
freq, rank, periods = defaultdict(int), {}, defaultdict(set)
with io.open(ROOTS_CSV, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        k = (r.get('root_slp1') or '').strip()
        if not k:
            continue
        fv = as_int(r.get('dcs_freq'), 0)
        if fv >= freq[k]:
            freq[k] = fv
            rank[k] = as_int(r.get('dcs_rank'), 0)
        for t in (r.get('period_tags') or '').split('|'):
            t = t.strip()
            if t:
                periods[k].add(t)

# ---- root_oracle: distinct dictionaries per root_slp1 ----
ndict = defaultdict(set)
with io.open(ORACLE, encoding='utf-8') as f:
    h = f.readline().rstrip('\n').split('\t')
    ki, si = h.index('root_slp1'), h.index('sources')
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) > max(ki, si):
            for s in p[si].split(','):
                if s.strip():
                    ndict[p[ki].strip()].add(s.strip())

def order_periods(pset):
    return [p for p in PERIOD_ORDER if p in pset] + sorted(pset - set(PERIOD_ORDER))

def enrich(r):
    k = (r.get('k1_slp1') or '').strip()
    r['dcs_freq'] = freq.get(k, 0)
    r['dcs_rank'] = rank.get(k, '') if freq.get(k, 0) else ''
    r['n_dicts'] = len(ndict.get(k, ()))
    r['dcs_periods'] = '|'.join(order_periods(periods[k])) if k in periods else ''

for r in mw:
    enrich(r)

# ---- full flagged + enriched dataset (MW entry order) ----
cols = ['mw_L', 'root_iast', 'k1_slp1', 'verb_type', 'genuine', 'classes',
        'dcs_freq', 'dcs_rank', 'n_dicts', 'dcs_periods', 'whitney_anchor', 'westergaard']
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
            '(частота/периоды DCS) + `root_oracle.tsv` (число словарей); join по SLP1. '
            'Всего %d подлинных из %d статей MW. '
            'Формат: ★ √корень — кл. классы · DCS частота (ранг) · N словарей · периоды._\n\n' % (len(genuine), len(mw)))
    for r in gen_sorted:
        cl = (r.get('classes') or '').strip()
        fparts = []
        if cl: fparts.append('кл. %s' % cl)
        if r['dcs_freq']: fparts.append('DCS %s%s' % (r['dcs_freq'], (' #%s' % r['dcs_rank']) if r['dcs_rank'] else ''))
        else: fparts.append('DCS —')
        fparts.append('%d слов.' % r['n_dicts'])
        if r['dcs_periods']: fparts.append(r['dcs_periods'])
        f.write('- ★ √*%s* — %s\n' % (r.get('root_iast', ''), ' · '.join(fparts)))

# ---- summary + core/tail cross-tab (by distinct genuine SLP1 form) ----
gi = sorted(set((r.get('k1_slp1') or '').strip() for r in genuine if (r.get('k1_slp1') or '').strip()))
att = [k for k in gi if freq.get(k, 0) > 0]
hi = [k for k in gi if len(ndict.get(k, ())) >= 4]
core = [k for k in gi if freq.get(k, 0) > 0 and len(ndict.get(k, ())) >= 4]
tail = [k for k in gi if freq.get(k, 0) == 0 and len(ndict.get(k, ())) <= 1]
period_counts = defaultdict(int)
for r in genuine:
    for p in (r['dcs_periods'].split('|') if r['dcs_periods'] else []):
        period_counts[p] += 1
top = sorted((r for r in genuine if r['dcs_freq']), key=lambda r: -int(r['dcs_freq']))[:20]

prov = {
    'script': 'mw_genuine_roots.py',
    'handoff': 'H1006 + enrichment H1006b + join-key reconcile H1034',
    'join_key': 'SLP1 (k1_slp1 / root_slp1)',
    'inputs': {'mw': 'csl-orig v02/mw/mw_roots.tsv',
               'dcs': 'WhitneyRoots/crosswalk/roots.csv',
               'oracle': 'csl-orig v02/etymology_stats/root_oracle.tsv'},
    'genuine_roots': len(genuine),
    'distinct_genuine_slp1': len(gi),
    'dcs_attested': len(att),
    'consensus_ge4_dicts': len(hi),
    'core_attested_and_ge4': len(core),
    'tail_unattested_le1': len(tail),
    'period_distribution': {p: period_counts.get(p, 0) for p in PERIOD_ORDER},
    'top20_by_dcs_freq': [{'root_iast': r.get('root_iast', ''), 'dcs_freq': int(r['dcs_freq'])} for r in top],
}
with io.open(PROV_OUT, 'w', encoding='utf-8', newline='') as f:
    json.dump(prov, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('MW root entries:', len(mw), '| genuine:', len(genuine), '| secondary:', len(mw) - len(genuine))
print('distinct genuine SLP1:', len(gi))
print('  DCS-attested:', len(att), '(%.0f%%)' % (100 * len(att) / len(gi)))
print('  cross-consensus >=4 dicts:', len(hi))
print('  CORE (attested & >=4 dicts):', len(core))
print('  TAIL (unattested & <=1 dict):', len(tail))
print('period distribution:', {p: period_counts.get(p, 0) for p in PERIOD_ORDER})
print('wrote:', os.path.basename(TSV_OUT), '(%d rows)' % len(mw))
print('wrote:', os.path.basename(LIST_OUT), '(%d genuine)' % len(genuine))
print('wrote:', os.path.basename(PROV_OUT))
