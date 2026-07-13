# -*- coding: utf-8 -*-
"""H385 — RWS findings triage.

Splits the 1127 RWS_FINDINGS.tsv rows into APPLY / SOFTEN / SKIP with a
Д1-Д5 cluster and a reason, following handoff H385 DO #1:
  - self-contained fixes (transliteration, native-term intro, register,
    logic/clarity rewordings that need no new citation) -> APPLY
  - fixes that require a fact not on hand (a page, a sutra number, a verse
    reference, a secondary-lit citation) -> SKIP
  - "unsupported claim" style findings -> SOFTEN (hedge) where a hedge needs
    no external fact, else SKIP.

zaliznyak-method is the priority optic (author decision 08-07-2026 #2): its
rows sort first within a paragraph.

Outputs revision-2026/rws_triage.json and prints a summary.
Stdlib only.
"""
import csv, json, os, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
BASE = os.path.dirname(os.path.abspath(__file__))  # revision-2026
TSV = BASE + r'\RWS_FINDINGS.tsv'

# --- cluster + disposition rules by finding `type` ---------------------------
# Д1 transliteration / native terms        -> APPLY
# Д2 logic / clarity / register / style    -> APPLY (self-contained rewording)
# Д3 evidentiary base / unsupported claims -> SOFTEN (hedge, no new fact)
# Д4 sources / sutra / citations           -> SKIP (needs a fact not on hand)
# Д5 tradition / commentary / apparatus    -> SKIP (needs added scholarship)
D1 = {'missing_iast_on_first_mention', 'mistranslated_native_term',
      'terminology_inconsistency', 'terminology', 'terminology_misuse',
      'terminological_ambiguity', 'anachronistic_sanskrit_period'}
D2 = {'logical_inconsistency', 'logical_consistency', 'logical_gap',
      'logical_lacuna', 'poor_logic', 'clarity_of_explanation', 'clarity',
      'clarity_issue', 'imprecise_formulation', 'stylistic_inconsistency',
      'stylistic_issue', 'redundancy', 'repetition', 'formatting',
      'spelling_error', 'incomplete_example', 'missing_reasoning',
      'inconsistency', 'historical_inconsistency'}
D3 = {'unsupported_semantization', 'unsupported_reading',
      'unsupported_sanskrit_etymology', 'unsupported_claim',
      'unsubstantiated_claim', 'insufficient_evidence', 'missing_evidence',
      'evidentiary_base', 'evidentiary_gap', 'lack_of_evidence',
      'weak_genre_framing', 'weak_parallel', 'questionable_claim',
      'anti_amateur_linguistics'}
D4 = {'missing_source', 'vague_source', 'inappropriate_source',
      'inaccurate_source', 'incomplete_reference', 'missing_reference',
      'unattributed_commentary', 'misattribution', 'missing_sutra_reference',
      'unclear_reference'}
D5 = {'missing_apparatus', 'missing_commentary_layer',
      'missing_tradition_context', 'commentary_function_gap',
      'missing_authority_chain', 'missing_context_of_hymn', 'missing_context',
      'missing_alternative_interpretation', 'factual_error',
      'arbitrary_sound_change', 'historical_continuity',
      'methodological_error'}

def classify(t):
    if t in D1: return 'Д1', 'APPLY',  'self-contained: transliteration / native-term intro'
    if t in D2: return 'Д2', 'APPLY',  'self-contained rewording: logic / clarity / register'
    if t in D3: return 'Д3', 'SOFTEN', 'unsupported claim -> hedge (no new fact); skip if hedge insufficient'
    if t in D4: return 'Д4', 'SKIP',   'needs a source/sutra/page/verse not on hand (DO #1)'
    if t in D5: return 'Д5', 'SKIP',   'needs added scholarship (tradition/commentary/apparatus)'
    return 'Д5', 'SKIP', 'unmapped type -> conservative skip'

STYLE_PRIO = {'zaliznyak-method': 0}  # everything else 1

def main():
    rows = list(csv.DictReader(open(TSV, encoding='utf-8'), delimiter='\t'))
    for i, r in enumerate(rows):
        r['_idx'] = i
        cl, disp, reason = classify(r['type'])
        r['cluster'], r['disposition'], r['disp_reason'] = cl, disp, reason
        r['style_prio'] = STYLE_PRIO.get(r['style'], 1)

    # per-paragraph grouping (file,line), zaliznyak first
    paras = defaultdict(list)
    for r in rows:
        paras[(r['file'], r['line'])].append(r)
    for k in paras:
        paras[k].sort(key=lambda r: (r['style_prio'], r['severity'] != 'major', r['_idx']))

    summary = {
        'total': len(rows),
        'by_disposition': dict(Counter(r['disposition'] for r in rows)),
        'by_cluster': dict(Counter(r['cluster'] for r in rows)),
        'apply_by_cluster': dict(Counter(r['cluster'] for r in rows if r['disposition'] == 'APPLY')),
        'unique_paragraphs': len(paras),
        'paragraphs_with_apply': sum(1 for k in paras if any(r['disposition'] == 'APPLY' for r in paras[k])),
        'paragraphs_apply_only_zaliznyak': sum(
            1 for k in paras
            if any(r['disposition'] == 'APPLY' and r['style'] == 'zaliznyak-method' for r in paras[k])),
    }

    def li(x):
        try: return int(x[1])
        except (ValueError, TypeError): return 10**9
    # build paragraphs list (sorted)
    plist = []
    for k in sorted(paras.keys(), key=lambda x: (x[0], li(x))):
        v = paras[k]
        plist.append({'file': k[0], 'line': (int(k[1]) if str(k[1]).isdigit() else None),
                      'has_apply': any(r['disposition'] == 'APPLY' for r in v),
                      'findings': [{'idx': r['_idx'], 'style': r['style'], 'severity': r['severity'],
                                    'type': r['type'], 'cluster': r['cluster'],
                                    'disposition': r['disposition'],
                                    'finding': r['finding'], 'suggestion': r['suggestion']} for r in v]})
    out = {'summary': summary, 'paragraphs': plist}
    json.dump(out, open(BASE + r'\rws_triage.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    print('=== TRIAGE SUMMARY ===')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    # per-file apply paragraph counts
    ff = defaultdict(lambda: [0, 0])
    for p in plist:
        ff[p['file']][0] += 1
        if p['has_apply']:
            ff[p['file']][1] += 1
    print('\n=== per file: [unique paras, paras-with-APPLY] ===')
    for f, (a, b) in ff.items():
        print(f'  {b:4d}/{a:4d}  {f}')

if __name__ == '__main__':
    main()
