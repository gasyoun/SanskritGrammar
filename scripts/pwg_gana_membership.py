#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PWG gaṇa-membership layer — the Pāṇinian word-class of each headword.

PWG itself carries almost no gaṇapāṭha markup (only ~5 explicit `gaṇa {#Xādi#}` refs), so
gaṇa membership is sourced EXTERNALLY from the nominal Gaṇapāṭha and joined to PWG:

  1. Parse the vendored [vidyut] Gaṇapāṭha (data/pwg_gana_membership/vidyut_ganapatha.rs,
     MIT-licensed, SLP1, auto-generated from ashtadhyayi.com/ganapath) → gaṇa → [members].
  2. Invert to member(SLP1) → gaṇa(s).
  3. Join the members onto PWG headwords (from the pwg_lid_hom_map k1 set) → each attested
     headword's gaṇa(s). Homonym-agnostic — gaṇa membership is lexical, not per-sense.
  4. Cross-validate with the Pāṇini crosswalk (pwg_panini_word2sutra): mark whether PWG also
     cites the gaṇa's governing sūtra for that headword (independent corroboration).

Emits data/pwg_gana_membership/vidyut_ganapatha.tsv (the parsed gaṇapāṭha) and
pwg_gana_membership.tsv (headword → gaṇa · governing sūtra · corroborated · in_pwg) + a
summary. Deterministic; the .rs is read-only.

    python scripts/pwg_gana_membership.py
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# one entry: `pub(crate)? const NAME: GanapathaEntry = GanapathaEntry::basic|akrti( ... );`
ENTRY = re.compile(
    r'const\s+(\w+):\s*GanapathaEntry\s*=\s*GanapathaEntry::(basic|akrti)\((.*?)\n\);',
    re.S)
STR = re.compile(r'"([^"]*)"')
ARR = re.compile(r'&\[(.*)\]', re.S)


def parse_ganapatha(rs_text):
    """Return list of dicts: {const, name, number, code(sutra), kind, members[]}."""
    out = []
    for m in ENTRY.finditer(rs_text):
        const, kind, body = m.group(1), m.group(2), m.group(3)
        arr = ARR.search(body)
        members = STR.findall(arr.group(1)) if arr else []
        head = body[:arr.start()] if arr else body      # name, number, code live before &[
        head_strs = STR.findall(head)
        name = head_strs[0] if head_strs else const.lower()
        code = next((s for s in head_strs if re.match(r'^\d+\.\d+', s)), '')
        num_m = re.search(r',\s*(\d+)\s*,', head)
        out.append({'const': const, 'name': name, 'number': int(num_m.group(1)) if num_m else 0,
                    'code': code, 'kind': kind, 'members': members})
    return out


def load_pwg_headwords(sg):
    """set of PWG headwords (SLP1) from the L_id↔hom map."""
    p = Path(sg) / 'data' / 'pwg_lid_hom_map' / 'pwg_lid_hom_map.tsv'
    hw = set()
    with p.open(encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            hw.add(r['k1'])
    return hw


def load_word_sutras(sg):
    """PWG headword_slp1 → set of sūtra codes (from the Pāṇini crosswalk word2sutra)."""
    p = Path(sg) / 'data' / 'pwg_panini_crosswalk' / 'pwg_panini_word2sutra.tsv'
    out = {}
    with p.open(encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            out[r['headword_slp1']] = set(s.replace('P.', '').strip()
                                          for s in r['sutras'].split('|') if s.strip())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sg-root', default=None, help='SanskritGrammar repo root (for the joined datasets)')
    ap.add_argument('--rs', default=None, help='path to the vendored ganapatha.rs')
    args = ap.parse_args()
    here = Path(__file__).resolve()
    repo = here.parents[1]
    sg = Path(args.sg_root) if args.sg_root else repo
    out_dir = repo / 'data' / 'pwg_gana_membership'
    rs = Path(args.rs) if args.rs else out_dir / 'vidyut_ganapatha.rs'
    for p, lbl in ((rs, 'ganapatha.rs'),):
        if not p.exists():
            print('ERROR: %s not found: %s' % (lbl, p), file=sys.stderr)
            return 1
    out_dir.mkdir(parents=True, exist_ok=True)

    ganas = parse_ganapatha(rs.read_text(encoding='utf-8'))

    # 1. committed parsed gaṇapāṭha
    gp = out_dir / 'vidyut_ganapatha.tsv'
    with gp.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['const', 'name', 'number', 'sutra', 'kind', 'n_members', 'members_slp1'])
        for g in ganas:
            w.writerow([g['const'], g['name'], g['number'], g['code'], g['kind'],
                        len(g['members']), '|'.join(g['members'])])

    # 2. invert: member → list of (gana_name, sutra, kind)
    member_gana = defaultdict(list)
    for g in ganas:
        for mem in g['members']:
            member_gana[mem].append((g['name'], g['code'], g['kind']))

    # 3+4. join to PWG headwords + crosswalk corroboration
    pwg_hw = load_pwg_headwords(sg)
    word_sutras = load_word_sutras(sg)
    rows = []
    corrob = 0
    for mem in sorted(member_gana):
        entries = member_gana[mem]
        in_pwg = mem in pwg_hw
        # governing sūtras of this member's gaṇa(s)
        gana_sutras = {c for _, c, _ in entries if c}
        cross = word_sutras.get(mem, set()) & gana_sutras
        if cross:
            corrob += 1
        rows.append((
            mem,
            '|'.join(sorted({n for n, _, _ in entries})),
            '|'.join(sorted(gana_sutras)),
            '|'.join(sorted('P.' + s for s in cross)),
            '1' if cross else '',
            '1' if in_pwg else '',
        ))

    mem_tsv = out_dir / 'pwg_gana_membership.tsv'
    with mem_tsv.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(['member_slp1', 'ganas', 'gana_sutras', 'crosswalk_sutra_match',
                    'corroborated', 'attested_in_pwg'])
        for r in rows:
            w.writerow(r)

    n_members = len(member_gana)
    in_pwg_n = sum(1 for r in rows if r[5])
    summary = {
        'study': 'PWG gaṇa-membership layer (external vidyut Gaṇapāṭha × Pāṇini crosswalk)',
        'as_of': '2026-07-19',
        'ganapatha_source': 'ambuda-org/vidyut vidyut-prakriya/src/ganapatha.rs (MIT; from ashtadhyayi.com/ganapath)',
        'ganas': len(ganas),
        'basic_ganas': sum(1 for g in ganas if g['kind'] == 'basic'),
        'akrti_ganas': sum(1 for g in ganas if g['kind'] == 'akrti'),
        'distinct_member_words': n_members,
        'members_attested_in_pwg': in_pwg_n,
        'members_corroborated_by_crosswalk': corrob,
    }
    (out_dir / 'pwg_gana_membership_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('ganas %d (basic %d / akrti %d) | member words %d | in PWG %d | crosswalk-corroborated %d'
          % (len(ganas), summary['basic_ganas'], summary['akrti_ganas'], n_members, in_pwg_n, corrob),
          file=sys.stderr)
    print('wrote vidyut_ganapatha.tsv + pwg_gana_membership.tsv + summary', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
