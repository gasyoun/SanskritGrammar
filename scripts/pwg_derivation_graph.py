#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PWG full derivation graph — every derivation note, classified, homonym-precise.

PWG states derivation as `von {#base#}` / `Von {#base#}` / `Wurzel {#root#}` /
`Stamm {#stem#}`. This one-pass extraction records EVERY such note per entry and
classifies it:

  - **kṛt**            — base is a verbal root (Whitney's 855) or the cue is `Wurzel`/`Stamm`
                         → deverbal (agent/gerundive/etc.).
  - **taddhita**       — base is a nominal AND the headword reconstructs as
                         base(+vṛddhi/+final-vowel-elision) + a known secondary suffix.
  - **denominal-other** — base is a nominal but no recognised secondary suffix (denominative
                         verbs -ay/-ya, rarer suffixes -la/-ana…, compound-final members).
  - **prefixed**       — base is an upasarga.

It SUPERSETS the taddhita-only slice (sg_wf_004_taddhita_pwg.py, ~5.7k): here the kṛt half
and the denominal residue are included, and each row carries L_id + homonym (`<h>`) so the
graph is homonym-precise. The root list is Whitney's clean inventory, NOT the contaminated
etymology_stats/dhatu_roots.txt (FINDINGS §130). Fixes the ultimate-root contamination of
the Cologne pwg_etymology extractor by keeping the IMMEDIATE base.

Read-only over the committed pwg.txt. Emits data/pwg_derivation_graph/pwg_derivation_graph.tsv
(L_id · k1 · hom · headword_iast · base_slp1 · base_iast · cue · base_type · deriv_kind ·
suffix · citation) + a summary. Deterministic.

    python scripts/pwg_derivation_graph.py
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

SLP1 = {'A': 'ā', 'I': 'ī', 'U': 'ū', 'f': 'ṛ', 'F': 'ṝ', 'x': 'ḷ', 'X': 'ḹ',
        'E': 'ai', 'O': 'au', 'M': 'ṃ', 'H': 'ḥ', 'K': 'kh', 'G': 'gh', 'N': 'ṅ',
        'C': 'ch', 'J': 'jh', 'Y': 'ñ', 'w': 'ṭ', 'W': 'ṭh', 'q': 'ḍ', 'Q': 'ḍh',
        'R': 'ṇ', 'T': 'th', 'D': 'dh', 'P': 'ph', 'B': 'bh', 'S': 'ś', 'z': 'ṣ',
        '~': 'm̐', '|': '', '@': ''}


def to_iast(s):
    return ''.join(SLP1.get(c, c) for c in s)


SUF_CLASS = {'tva', 'tA', 'in', 'vin', 'vat', 'mat', 'ika', 'ya', 'Iya', 'eya', 'maya',
             'ka', 'tara', 'tama', 'tas', 'Sas', 'anIya', 'tavya', 'tvana', 'tana', 'vala', 'min'}
SUFFIXES = sorted(SUF_CLASS, key=len, reverse=True)
VR = {'a': 'A', 'A': 'A', 'i': 'E', 'I': 'E', 'u': 'O', 'U': 'O',
      'f': 'Ar', 'e': 'E', 'o': 'O', 'E': 'E', 'O': 'O'}
UPASARGA = {'pra', 'parA', 'apa', 'sam', 'anu', 'ava', 'nis', 'nir', 'dus', 'dur', 'vi', 'A',
            'AN', 'ni', 'aDi', 'api', 'ati', 'su', 'ud', 'ut', 'aBi', 'prati', 'pari', 'upa', 'a', 'an'}


def vrddhi(stem):
    for i, ch in enumerate(stem):
        if ch in 'aAiIuUfeoEO':
            return stem[:i] + VR[ch] + stem[i + 1:]
    return stem


def base_variants(base):
    vs = {base}
    if base and base[-1] in 'aAiIuUf':
        vs.add(base[:-1])
    vs.add(vrddhi(base))
    if base and base[-1] in 'aAiIuUf':
        vs.add(vrddhi(base[:-1]))
    return vs


def match_suffix(hw, base):
    bv = base_variants(base)
    for suf in SUFFIXES:
        if hw.endswith(suf):
            st = hw[:-len(suf)]
            if len(st) >= 2 and st in bv:
                return suf
    return None


DERIV = re.compile(r'(Von|von|Wurzel|Stamm)\s+(?:<hom>[^<]*</hom>\s*)?\{#([^#]+)#\}')
LS = re.compile(r'<ls>([^<]+)</ls>')
RE_L = re.compile(r'<L>(\d+)')
RE_K1 = re.compile(r'<k1>([^<]*)')
RE_H = re.compile(r'<h>(\d+)')


def entries(path):
    lid = k1 = hom = None
    buf, on = [], False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('<L>'):
            ml, mk = RE_L.search(ln), RE_K1.search(ln)
            if ml and mk:
                if on and lid:
                    yield lid, k1, hom, buf
                mh = RE_H.search(ln)
                lid, k1, hom = ml.group(1), mk.group(1), (mh.group(1) if mh else '')
                buf, on = [], True
                continue
        if on:
            if ln.startswith('<LEND>'):
                yield lid, k1, hom, buf
                on = False
            else:
                buf.append(ln)


def load_roots(path):
    roots = set()
    for r in csv.DictReader(open(path, encoding='utf-8')):
        v = (r.get('root_slp1') or '').strip()
        if v:
            roots.add(v)
    return roots


def classify(hw, base, cue, roots):
    if cue in ('Wurzel', 'Stamm') or base in roots:
        return 'root', 'krt', ''
    if base in UPASARGA:
        return 'prefix', 'prefixed', ''
    suf = match_suffix(hw, base)
    return 'nominal', ('taddhita' if suf else 'denominal-other'), (suf or '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pwg', default=None)
    ap.add_argument('--roots', default=None)
    ap.add_argument('--out', default=None)
    args = ap.parse_args()
    here = Path(__file__).resolve()
    repo, github = here.parents[1], here.parents[2]
    pwg = Path(args.pwg) if args.pwg else github / 'csl-orig' / 'v02' / 'pwg' / 'pwg.txt'
    roots_p = Path(args.roots) if args.roots else github / 'WhitneyRoots' / 'crosswalk' / 'roots.csv'
    for p, lbl in ((pwg, 'pwg.txt'), (roots_p, 'Whitney roots')):
        if not p.exists():
            print('ERROR: %s not found: %s' % (lbl, p), file=sys.stderr)
            return 1
    out = Path(args.out) if args.out else repo / 'data' / 'pwg_derivation_graph'
    out.mkdir(parents=True, exist_ok=True)
    roots = load_roots(roots_p)

    rows = []
    by_kind = Counter()
    by_base = Counter()
    for lid, k1, hom, buf in entries(pwg):
        body = '\n'.join(buf)
        flat = ' '.join(body.split())
        cites = LS.findall(body)
        seen = set()
        for m in DERIV.finditer(flat):
            cue, base = m.group(1), m.group(2).strip()
            if ' ' in base or len(base) > 18:
                continue
            if (base, cue) in seen:
                continue
            seen.add((base, cue))
            base_type, deriv_kind, suf = classify(k1, base, cue, roots)
            by_kind[deriv_kind] += 1
            by_base[base_type] += 1
            rows.append((lid, k1, hom, to_iast(k1), base, to_iast(base), cue,
                         base_type, deriv_kind, suf, cites[0].strip() if cites else ''))

    rows.sort(key=lambda r: (int(r[0]), r[4]))
    cols = ['L_id', 'k1', 'hom', 'headword_iast', 'base_slp1', 'base_iast', 'cue',
            'base_type', 'deriv_kind', 'suffix', 'citation']
    tsv = out / 'pwg_derivation_graph.tsv'
    with tsv.open('w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t')
        w.writerow(cols)
        for r in rows:
            w.writerow(r)

    summary = {
        'study': 'PWG full derivation graph (von/Wurzel notes, classified, homonym-precise)',
        'as_of': '2026-07-19',
        'source': 'csl-orig/v02/pwg/pwg.txt (read-only)',
        'root_inventory': 'WhitneyRoots/crosswalk/roots.csv (855 dhātus) — not the contaminated dhatu_roots.txt',
        'total_derivations': len(rows),
        'by_deriv_kind': dict(by_kind.most_common()),
        'by_base_type': dict(by_base.most_common()),
    }
    (out / 'pwg_derivation_graph_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('derivations %d | kind %s' % (len(rows), dict(by_kind.most_common())), file=sys.stderr)
    print('wrote %s + summary' % tsv.name, file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
