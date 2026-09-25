import csv
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

rows = list(csv.DictReader(open(
    r'TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv', encoding='utf-8')))
print('rows', len(rows))
print(rows[0])

kosha_cw = json.load(open(
    r'C:\Users\user\Documents\GitHub\kosha\data\e1\dhatu_crosswalk.json', encoding='utf-8'))['crosswalk']
kosha_roots_by_bare = {}
for k, v in kosha_cw.items():
    _, bare = k.split('|', 1)
    kosha_roots_by_bare.setdefault(bare, []).append(v)
print('kosha unique bare roots', len(kosha_roots_by_bare))

dcs = json.load(open(
    r'C:\Users\user\Documents\GitHub\VisualDCS\dcs_lemma_summary.json', encoding='utf-8'))['lemmas']
print('dcs lemma count', len(dcs))

matched_kosha = 0
matched_dcs = 0
ambiguous = 0
for r in rows[:20]:
    iast = r['root']
    slp1 = transliterate(iast, sanscript.IAST, sanscript.SLP1)
    kmatch = kosha_roots_by_bare.get(slp1)
    dmatch = slp1 in dcs
    print(r['whitney_no'], iast, '->', slp1, 'kosha:', kmatch, 'dcs:', dmatch)
