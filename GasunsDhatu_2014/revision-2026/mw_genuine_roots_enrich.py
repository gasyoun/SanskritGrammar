#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""M03 Гл.1 Приложение 7 (H1006, второй проход): обогащение списка 750 подлинных
корней MW корпусной частотой DCS и межсловарным согласием (root_oracle).

Consumes (reproducible, no judgement added — every column is sourced, not invented):
  * mw_genuine_roots.tsv                     — база H1006 (2113 корней + флаг genuine)
  * ../../../WhitneyRoots/crosswalk/roots.csv — DCS: корпусная частота/ранг/периоды
  * ../../../csl-orig/v02/etymology_stats/root_oracle.tsv — межсловарное согласие

Join key: SLP1 (MW `k1_slp1` ↔ DCS `root_slp1` ↔ oracle `root_slp1`).
Омонимы, делящие одну SLP1-форму, агрегируются: частота DCS суммируется, ранг —
минимальный (лучший), периоды и словари-источники — объединение.

Emits:
  * mw_genuine_roots_enriched.tsv       — 750 подлинных корней + столбцы обогащения
  * mw_genuine_roots_enriched_list.md   — печатный список с частотой/периодом/согласием
  * mw_genuine_roots_enrich_provenance.json — покрытие и сводка (для сносок/аудита)
  * печатает сводку покрытия и распределения

Run from the repo root or the script dir (paths resolved relative to the script).
"""
import csv, io, sys, os, json
from collections import defaultdict
sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
# repo root = .../SanskritGrammar; org root = its parent (holds sibling repos)
ORG = os.path.abspath(os.path.join(HERE, '..', '..', '..'))

BASE_TSV = os.path.join(HERE, 'mw_genuine_roots.tsv')
DCS_CSV = os.environ.get('DCS_ROOTS_CSV', os.path.join(ORG, 'WhitneyRoots', 'crosswalk', 'roots.csv'))
ORACLE_TSV = os.environ.get('ROOT_ORACLE_TSV', os.path.join(ORG, 'csl-orig', 'v02', 'etymology_stats', 'root_oracle.tsv'))

TSV_OUT = os.path.join(HERE, 'mw_genuine_roots_enriched.tsv')
LIST_OUT = os.path.join(HERE, 'mw_genuine_roots_enriched_list.md')
PROV_OUT = os.path.join(HERE, 'mw_genuine_roots_enrich_provenance.json')

# DCS attestation periods, chronological (union rendered in this order).
PERIOD_ORDER = ['RV', 'AV', 'V', 'B', 'S', 'E', 'C']


def as_int(v, default=1 << 30):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


# ---- base: 750 genuine roots (genuine flag == 1) ----
with io.open(BASE_TSV, encoding='utf-8') as f:
    base = [r for r in csv.DictReader(f, delimiter='\t') if (r.get('genuine') or '').strip() == '1']

# ---- DCS: aggregate freq/rank/periods by root_slp1 ----
dcs = defaultdict(lambda: {'freq': 0, 'rank': None, 'periods': set()})
with io.open(DCS_CSV, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        slp = (r.get('root_slp1') or '').strip()
        if not slp:
            continue
        d = dcs[slp]
        d['freq'] += as_int(r.get('dcs_freq'), 0)
        rank = as_int(r.get('dcs_rank'), None) if (r.get('dcs_rank') or '').strip() else None
        if rank is not None:
            d['rank'] = rank if d['rank'] is None else min(d['rank'], rank)
        for t in (r.get('period_tags') or '').split('|'):
            t = t.strip()
            if t:
                d['periods'].add(t)

# ---- oracle: aggregate the set of source dictionaries by root_slp1 ----
oracle = defaultdict(set)
with io.open(ORACLE_TSV, encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        slp = (r.get('root_slp1') or '').strip()
        if not slp:
            continue
        for s in (r.get('sources') or '').split(','):
            s = s.strip()
            if s:
                oracle[slp].add(s)


def order_periods(pset):
    known = [p for p in PERIOD_ORDER if p in pset]
    rest = sorted(pset - set(PERIOD_ORDER))
    return known + rest


# ---- build enriched rows ----
cols = ['mw_L', 'root_iast', 'k1_slp1', 'classes',
        'dcs_freq', 'dcs_rank', 'dcs_periods', 'oracle_dicts', 'oracle_sources']
enriched = []
for r in base:
    slp = (r.get('k1_slp1') or '').strip()
    d = dcs.get(slp)
    src = sorted(oracle.get(slp, set()))
    enriched.append({
        'mw_L': r.get('mw_L', ''),
        'root_iast': r.get('root_iast', ''),
        'k1_slp1': slp,
        'classes': (r.get('classes') or '').strip(),
        'dcs_freq': d['freq'] if d else '',
        'dcs_rank': (d['rank'] if d and d['rank'] is not None else ''),
        'dcs_periods': '|'.join(order_periods(d['periods'])) if d else '',
        'oracle_dicts': len(src) if src else '',
        'oracle_sources': ','.join(src),
    })

# sort by MW entry order for the TSV
enriched_by_L = sorted(enriched, key=lambda r: as_int(r['mw_L']))
with io.open(TSV_OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(cols)
    for r in enriched_by_L:
        w.writerow([r[c] for c in cols])

# ---- print-ready enriched list, alpha by IAST ----
gen_sorted = sorted(enriched, key=lambda r: ((r['root_iast'] or '').lower(), as_int(r['mw_L'])))
with io.open(LIST_OUT, 'w', encoding='utf-8', newline='') as f:
    f.write('# Подлинные корни словаря Монье-Уильямса — обогащённый список\n\n')
    f.write('_Сгенерировано `mw_genuine_roots_enrich.py`: 750 подлинных корней MW '
            '(колонка `verb_type=genuineroot`), обогащённых корпусной частотой DCS '
            '(`WhitneyRoots/crosswalk/roots.csv`) и межсловарным согласием '
            '(`csl-orig/v02/etymology_stats/root_oracle.tsv`). '
            'Частота — сумма по омонимам DCS; словари — число независимых источников, '
            'подтверждающих формы корня. Прочерк = нет данных в источнике._\n\n')
    f.write('_Легенда: **freq** — вхождений в корпусе DCS; **per.** — периоды аттестации '
            '(RV·AV·V·B·S·E·C); **слов.** — независимых словарей (макс. 9)._\n\n')
    for r in gen_sorted:
        cl = (' — кл. %s' % r['classes']) if r['classes'] else ''
        bits = []
        if r['dcs_freq'] != '' and r['dcs_freq'] != 0:
            bits.append('freq %s' % r['dcs_freq'])
        if r['dcs_periods']:
            bits.append('per. %s' % r['dcs_periods'])
        if r['oracle_dicts'] != '':
            bits.append('слов. %s' % r['oracle_dicts'])
        tail = (' *(%s)*' % '; '.join(bits)) if bits else ''
        f.write('- ★ √*%s*%s%s\n' % (r['root_iast'], cl, tail))

# ---- provenance / coverage summary ----
n = len(enriched)
in_dcs = sum(1 for r in enriched if r['dcs_freq'] != '')
in_oracle = sum(1 for r in enriched if r['oracle_dicts'] != '')
in_neither = sum(1 for r in enriched if r['dcs_freq'] == '' and r['oracle_dicts'] == '')
attested_corpus = sum(1 for r in enriched if r['dcs_freq'] not in ('', 0))
period_counts = defaultdict(int)
for r in enriched:
    for p in (r['dcs_periods'].split('|') if r['dcs_periods'] else []):
        period_counts[p] += 1
# top-20 by DCS freq
top = sorted((r for r in enriched if r['dcs_freq'] not in ('', 0)),
             key=lambda r: -int(r['dcs_freq']))[:20]

prov = {
    'script': 'mw_genuine_roots_enrich.py',
    'handoff': 'H1006 (второй проход)',
    'inputs': {
        'base': 'mw_genuine_roots.tsv',
        'dcs': 'WhitneyRoots/crosswalk/roots.csv',
        'oracle': 'csl-orig/v02/etymology_stats/root_oracle.tsv',
    },
    'genuine_roots': n,
    'matched_dcs': in_dcs,
    'matched_oracle': in_oracle,
    'matched_neither': in_neither,
    'corpus_attested_dcs_freq_gt0': attested_corpus,
    'period_distribution': {p: period_counts.get(p, 0) for p in PERIOD_ORDER},
    'top20_by_dcs_freq': [{'root_iast': r['root_iast'], 'dcs_freq': int(r['dcs_freq'])} for r in top],
}
with io.open(PROV_OUT, 'w', encoding='utf-8', newline='') as f:
    json.dump(prov, f, ensure_ascii=False, indent=2)
    f.write('\n')

print('genuine roots:', n)
print('  matched in DCS (freq/rank/period):', in_dcs, '(%.0f%%)' % (100 * in_dcs / n))
print('  matched in root_oracle (cross-dict):', in_oracle, '(%.0f%%)' % (100 * in_oracle / n))
print('  matched in neither:', in_neither)
print('  corpus-attested (DCS freq > 0):', attested_corpus)
print('period distribution among genuine roots:',
      {p: period_counts.get(p, 0) for p in PERIOD_ORDER})
print('wrote:', os.path.basename(TSV_OUT), '(%d rows)' % n)
print('wrote:', os.path.basename(LIST_OUT))
print('wrote:', os.path.basename(PROV_OUT))
