#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H1310 — audit PWG's lexicon-only headwords against other digitised dictionaries.

The register/genre layer flags headwords PWG attests ONLY from koṣas, never a dated text
(`lexicon_only=1`). PWG is one dictionary, so such a word may still be attested — in a text
via another dictionary (MW/Apte…) or just present in another koṣa. This resolves that by a
deterministic set-membership join against the Cologne digitisations (csl-orig, read-only).

Comparison sets (each dict's distinct `<k1>`, SLP1 — same convention as PWG):
  - INDEPENDENT text-based: ap90 · ap (Apte) · bhs (Edgerton BHS corpus) · gra (Grassmann RV corpus)
  - MW (Monier-Williams): text-based BUT compiled substantially FROM Böhtlingk-Roth (PW/PWG)
    itself — a well-known lexicographic fact — so an MW-only hit is WEAK independence evidence
    (MW may have copied the word from PW), reported as its own tier, not lumped with independent.
  - KOSA (same lexical tradition): skd
  - SAME-SOURCE (Böhtlingk's own PWK/abridgment — NOT independent evidence): pw
    → a `pw`-only or `mw`-only hit does NOT rescue a word from the ghost-word shortlist.

Verdict per lexicon-only headword (most-independent wins):
  - **text-independent** present in ≥1 INDEPENDENT text dict (Apte/BHS/Grassmann) → really attested
  - **mw-only**          present in MW but in no independent text dict (weak — MW ⊃ PW overlap)
  - **kosa-only**        present only in KOSA
  - **pwg-unique**       in NO other dict at all (the genuine ghost-word shortlist)

Read-only. Emits data/pwg_lexicon_only_audit/pwg_lexicon_only_audit.tsv (per word · verdict ·
per-dict hits) + a PWG-unique shortlist + a summary. Deterministic.

    python scripts/pwg_lexicon_only_audit.py
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

INDEP = ['ap90', 'ap', 'bhs', 'gra']   # independent text-based dictionaries
MW = ['mw']                            # text-based but derived largely from PW/PWG (weak)
STRONG = MW + INDEP                     # all text-based, for per-dict reporting
KOSA = ['skd']
SAME_SOURCE = ['pw']
ALL_DICTS = STRONG + KOSA + SAME_SOURCE
K1 = re.compile(r'<k1>([^<]+)')


def load_headwords(csl, code):
    p = Path(csl) / 'v02' / code / (code + '.txt')
    hw = set()
    if not p.exists():
        return hw
    with p.open(encoding='utf-8', errors='replace') as f:
        for line in f:
            if '<k1>' in line:
                for m in K1.finditer(line):
                    hw.add(m.group(1).strip())
    return hw


def load_lexicon_only(reg_tsv):
    words = []
    with open(reg_tsv, encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r.get('lexicon_only') == '1':
                words.append((r['k1'], r.get('hom', '')))
    return words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csl', default=None, help='csl-orig repo root')
    ap.add_argument('--reg', default=None, help='pwg_register_genre.tsv path')
    args = ap.parse_args()
    here = Path(__file__).resolve()
    repo, github = here.parents[1], here.parents[2]
    csl = Path(args.csl) if args.csl else github / 'csl-orig'
    reg = Path(args.reg) if args.reg else repo / 'data' / 'pwg_register_genre' / 'pwg_register_genre.tsv'
    for p, lbl in ((csl, 'csl-orig'), (reg, 'register/genre tsv')):
        if not p.exists():
            print('ERROR: %s not found: %s' % (lbl, p), file=sys.stderr)
            return 1
    out = repo / 'data' / 'pwg_lexicon_only_audit'
    out.mkdir(parents=True, exist_ok=True)

    dict_hw = {}
    for code in ALL_DICTS:
        dict_hw[code] = load_headwords(csl, code)
        print('  %-5s %d headwords' % (code, len(dict_hw[code])), file=sys.stderr)

    lex_only = load_lexicon_only(reg)
    # dedupe by k1 (audit is lexical, homonym-agnostic)
    lex_k1 = sorted({k for k, _ in lex_only})

    rows = []
    verdict_ctr = Counter()
    for k in lex_k1:
        hits = {code: (k in dict_hw[code]) for code in ALL_DICTS}
        indep = [c for c in INDEP if hits[c]]
        kosa = [c for c in KOSA if hits[c]]
        if indep:
            verdict = 'text-independent'
        elif hits['mw']:
            verdict = 'mw-only'
        elif kosa:
            verdict = 'kosa-only'
        else:
            verdict = 'pwg-unique'
        verdict_ctr[verdict] += 1
        rows.append((k, verdict,
                     '|'.join(indep), '1' if hits['mw'] else '', '|'.join(kosa),
                     '1' if hits.get('pw') else ''))

    tsv = out / 'pwg_lexicon_only_audit.tsv'
    with tsv.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['k1', 'verdict', 'independent_hits', 'in_mw', 'kosa_hits', 'in_pw_same_source'])
        for r in rows:
            w.writerow(r)

    shortlist = out / 'pwg_unique_shortlist.tsv'
    with shortlist.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['k1', 'also_in_pw_same_source'])
        for k, v, ind, mw, ko, pw in rows:
            if v == 'pwg-unique':
                w.writerow([k, pw])

    per_dict = {code: sum(1 for k in lex_k1 if k in dict_hw[code]) for code in ALL_DICTS}
    summary = {
        'study': 'H1310 — PWG lexicon-only headwords vs other digitised dictionaries',
        'as_of': '2026-07-19',
        'lexicon_only_k1': len(lex_k1),
        'comparison_independent_textbased': INDEP,
        'comparison_mw_weak_derived_from_pw': MW,
        'comparison_kosa': KOSA,
        'comparison_same_source_excluded': SAME_SOURCE,
        'by_verdict': dict(verdict_ctr.most_common()),
        'per_dict_hits': per_dict,
    }
    (out / 'pwg_lexicon_only_audit_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('lexicon-only k1: %d | verdicts %s' % (len(lex_k1), dict(verdict_ctr.most_common())),
          file=sys.stderr)
    print('per-dict hits: %s' % per_dict, file=sys.stderr)
    print('wrote audit.tsv + pwg_unique_shortlist.tsv + summary', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
