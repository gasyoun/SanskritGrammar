import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open(r'C:\Users\user\Documents\GitHub\VisualDCS\dcs_lemma_summary.json', encoding='utf-8'))
lemmas = d['lemmas']
print('lemmaCount', d.get('lemmaCount'), 'actual', len(lemmas))
print('sample keys', list(lemmas[0].keys()) if isinstance(lemmas, list) else list(lemmas.keys())[:5])
if isinstance(lemmas, list):
    for row in lemmas[:5]:
        print(row)
else:
    for k in list(lemmas.keys())[:5]:
        print(k, lemmas[k])
