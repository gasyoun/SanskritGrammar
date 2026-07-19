#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H1323 — PWG ghost-word triage cascade (stages 1-4).

The lexicon-only audit v2 (H1310) leaves 2,298 pwg-unique headwords — in no other digitised
Cologne dictionary — of which 788 are absent even from Böhtlingk's own PWK (`pw`). Hand-
adjudicating them is too much. This cascade auto-classifies each into a bucket using layers we
already own plus one reused normalizer, so a human only ever reviews the small true residue,
and cross-checks each verdict against v2's citation-source category (`src_category`).

Every word is tagged by ALL signals that fire; a single `verdict` is chosen by precedence.

  Stage 1 — COMPOSITIONAL (own datasets + body backstop + greedy decomposition)
     word ∈ pwg_compound_splits / pwg_derivation_graph, or its PWG body carries a
     `({#X#} + {#Y#})` compound formula or a `von {#base#}` derivation note, or the word splits
     (greedy longest-prefix) into ≥2 attested headwords → not a novel simplex.
  Stage 2 — BODY MARKERS (one regex pass over the committed pwg.txt entry body)
     `<ab>N. pr.</ab>`/`<ab>N.</ab>`/`Titel eines …`/`Name eines …` → proper name or work title ·
     `falsche/richtige Lesart`/`zu lesen für`/`fehlerhaft`/`… kritisch für` → PWG-declared
     misreading, emendation or dialect variant · `= {#X#}` → PWG's cross-reference to word X.
  Stage 3 — DESCRIPTIVE GLOSS (own pwg_german_glosses)
     German gloss is a `dessen…/deren…` bahuvrīhi paraphrase → a compound the splitter missed.
  Stage 4 — NORMALIZATION RE-JOIN (reuses SanskritSpellCheck `slp1util.confusion_key`)
     the word's confusion-collapsed skeleton key matches an attested headword in another
     dictionary → a spelling/OCR variant of an attested word, not genuinely unique. The same
     key resolves each `= {#X#}` xref target (spelling-variant vs attested synonym).
  Stage 5 — V2 CITATION-SOURCE FALLBACK (only when stages 1-4 are silent)
     v2's `src_category` = `ms_catalogue_propernoun` → cited only from a manuscript catalogue,
     so a name/title (`catalogue-propername`); = `kosa_nighantu_not_digitised` → attested in a
     koṣa PWG names but Cologne has not digitised (`kosa-corpus-gap`), not a ghost.

  → RESIDUE — no signal fired: a genuine simplex ghost-word candidate. Emitted with its
     accented headword (`<k2>`) + German gloss for fast human review.

Read-only. Deterministic. Reuses the org normalizer rather than re-implementing one
(prior-art: SHARED_CODE.md §12 marks `confusion_key` the canonical scribal/OCR skeleton key).

Emits data/pwg_ghostword_triage/ : the full triage TSV, the residue review-list, a summary.

    python scripts/pwg_ghostword_triage.py
"""
import argparse
import csv
import functools
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# comparison dictionaries (same tiers as the H1310 audit)
INDEP = ['ap90', 'ap', 'bhs', 'gra']
MW = ['mw']
KOSA = ['skd']
SAME_SOURCE = ['pw']
ALL_DICTS = MW + INDEP + KOSA + SAME_SOURCE

RE_L = re.compile(r'<L>(\d+)')
RE_K1 = re.compile(r'<k1>([^<]*)')
RE_H = re.compile(r'<h>(\d+)')
K1_DICT = re.compile(r'<k1>([^<]+)')

# stage-2 body markers
NPR = re.compile(r'<ab>\s*N\.(?:\s*pr\.)?\s*</ab>')       # <ab>N. pr.</ab> / <ab>N.</ab>
TITLE_NAME = re.compile(r'\bTitel\b|\bName\s+ein')       # "Titel eines Werkes/Schrift" · "Name eines …"
MISREAD = re.compile(                                     # PWG-declared error / emendation / dialect variant
    r'(?:falsche|fehlerhafte?)\s+Lesart|richtige\s+Lesart\s+ist|fehlerhaft'
    r'|zu\s+lesen\s+f[uü]r|so,?\s+nicht\s+\{#|kritisch\s+f[uü]r')
XREF = re.compile(r'=\s*\{#([^#]+)#\}')                   # = {#X#}
COMPOUND_BODY = re.compile(r'\(\s*\{#[^#]+#\}\s*\+\s*\{#[^#]+#\}')   # ({#X#} + {#Y#})
VON = re.compile(r'\bvon\s+\{#([^#]+)#\}')               # von {#base#}
# stage-3 bahuvrīhi paraphrase cue (conservative)
BVR = re.compile(r'\bdessen\b|\bderen\b')


def load_normalizer(github):
    """Reuse the org's canonical confusion-collapsing SLP1 skeleton key + capped Levenshtein
    (do not re-implement). Returns (confusion_key, edit_distance) or (None, None)."""
    for p in (github / 'sanskrit-util' / 'py', github / 'SanskritSpellCheck' / 'detectors'):
        sys.path.insert(0, str(p))
    try:
        from slp1util import confusion_key, edit_distance
        return confusion_key, edit_distance
    except Exception as e:                                # pragma: no cover
        print('WARN: SanskritSpellCheck slp1util unavailable (%s) — stage 4 normalization '
              're-join SKIPPED; clone SanskritSpellCheck + sanskrit-util as siblings to enable '
              'it.' % e, file=sys.stderr)
        return None, None


def entries(path):
    """Yield (L_id, k1, hom, body) per <L>…<LEND> entry (same idiom as pwg_german_glosses.py)."""
    lid = k1 = hom = None
    buf, on = [], False
    for ln in open(path, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if ln.startswith('<L>'):
            ml, mk = RE_L.search(ln), RE_K1.search(ln)
            if ml and mk:
                if on and lid:
                    yield lid, k1, hom, '\n'.join(buf)
                mh = RE_H.search(ln)
                lid, k1, hom = ml.group(1), mk.group(1), (mh.group(1) if mh else '')
                buf, on = [], True
                continue
        if on:
            if ln.startswith('<LEND>'):
                yield lid, k1, hom, '\n'.join(buf)
                on = False
            else:
                buf.append(ln)


def load_dict_headwords(csl, code):
    p = Path(csl) / 'v02' / code / (code + '.txt')
    hw = set()
    if p.exists():
        with p.open(encoding='utf-8', errors='replace') as f:
            for line in f:
                if '<k1>' in line:
                    for m in K1_DICT.finditer(line):
                        hw.add(m.group(1).strip())
    return hw


def tsv_col(path, col):
    with open(path, encoding='utf-8') as f:
        return set(r[col] for r in csv.DictReader(f, delimiter='\t') if r.get(col))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--csl', default=None)
    ap.add_argument('--pwg', default=None)
    args = ap.parse_args()
    here = Path(__file__).resolve()
    repo, github = here.parents[1], here.parents[2]
    csl = Path(args.csl) if args.csl else github / 'csl-orig'
    pwg = Path(args.pwg) if args.pwg else csl / 'v02' / 'pwg' / 'pwg.txt'
    data = repo / 'data'
    short = data / 'pwg_lexicon_only_audit' / 'pwg_ghostword_shortlist.tsv'
    for p, lbl in ((csl, 'csl-orig'), (pwg, 'pwg.txt'), (short, 'H1310 v2 ghostword shortlist')):
        if not p.exists():
            print('ERROR: %s not found: %s' % (lbl, p), file=sys.stderr)
            return 1
    out = data / 'pwg_ghostword_triage'
    out.mkdir(parents=True, exist_ok=True)
    ckey, edist = load_normalizer(github)
    ED_MAX = 2          # a skeleton collision counts as a variant only within this edit distance

    # ---- inputs -----------------------------------------------------------------
    pu = {}          # k1 -> is_core (absent from every dict incl pw)
    v2cat = {}       # k1 -> v2 citation-source category (src_category), for cross-validation
    with short.open(encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            k = r['k1']
            if k not in pu:
                pu[k] = (r.get('also_in_pw_same_source') != '1')
                v2cat[k] = r.get('src_category', '')
    targets = set(pu)

    comp_set = tsv_col(data / 'pwg_compound_split' / 'pwg_compound_splits.tsv', 'headword_slp1')
    deriv_set = tsv_col(data / 'pwg_derivation_graph' / 'pwg_derivation_graph.tsv', 'k1')
    gloss = {}
    with (data / 'pwg_german_glosses' / 'pwg_german_glosses.tsv').open(encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['k1'] in targets and r.get('glosses'):
                gloss.setdefault(r['k1'], []).append(r['glosses'])
    gloss = {k: ' ‖ '.join(v) for k, v in gloss.items()}
    accent = {}
    with (data / 'pwg_lid_hom_map' / 'pwg_lid_hom_map.tsv').open(encoding='utf-8') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            if r['k1'] in targets and r['k1'] not in accent:
                accent[r['k1']] = r.get('k2', '')

    bodies = {}
    for lid, k1, hom, body in entries(pwg):
        if k1 in targets:
            bodies[k1] = (bodies.get(k1, '') + ' ' + re.sub(r'\s+', ' ', body)).strip()

    dict_exact = {c: load_dict_headwords(csl, c) for c in ALL_DICTS}
    # skeleton -> list of (dict_code, headword), for edit-distance-filtered variant lookup
    skel_index = {}
    if ckey:
        for c in ALL_DICTS:
            for w in dict_exact[c]:
                skel_index.setdefault(ckey(w), []).append((c, w))

    def find_variant(word):
        """Return (matched_headword, sorted_dict_codes) if `word` is within ED_MAX of a
        same-skeleton attested headword, else (None, [])."""
        if not ckey:
            return None, []
        cands = skel_index.get(ckey(word), [])
        best, best_ed, dicts = None, ED_MAX + 1, {}
        seen = {}
        for c, hw in cands:
            if hw == word:
                continue
            e = seen.get(hw)
            if e is None:
                e = edist(word, hw)
                seen[hw] = e
            if e <= ED_MAX:
                dicts.setdefault(hw, set()).add(c)
                if e < best_ed:
                    best, best_ed = hw, e
        if best is None:
            return None, []
        return best, sorted(dicts[best])

    # union of all attested headwords, for greedy string-level compound decomposition
    HW_ALL = set().union(*dict_exact.values()) if dict_exact else set()
    DECOMP_MIN = 3

    @functools.lru_cache(maxsize=None)
    def decompose(w):
        """Greedy longest-prefix split of `w` into attested headwords (≥ DECOMP_MIN chars each).
        Returns the tuple of parts if it splits into ≥2, else None. String-level only — it does
        not undo sandhi at the join, so sandhi-boundary compounds (caturTa+AraRyaka) are left for
        the deferred vidyut splitter (stage 5)."""
        if len(w) < DECOMP_MIN:
            return None
        if w in HW_ALL:
            return (w,)
        for i in range(len(w) - DECOMP_MIN, DECOMP_MIN - 1, -1):
            if w[:i] in HW_ALL:
                rest = decompose(w[i:])
                if rest:
                    return (w[:i],) + rest
        return None

    print('  loaded %d target words · %d comp · %d deriv · %d gloss · %d headword-union · normalizer=%s'
          % (len(targets), len(comp_set), len(deriv_set), len(gloss), len(HW_ALL), bool(ckey)),
          file=sys.stderr)

    # ---- classify ---------------------------------------------------------------
    def clean_xref(t):
        return t.strip()

    rows = []
    for k1 in sorted(targets):
        body = bodies.get(k1, '')
        gl = gloss.get(k1, '')
        tags = set()

        # stage 2 — body markers
        if MISREAD.search(body):
            tags.add('misreading')
        if NPR.search(body) or TITLE_NAME.search(body):
            tags.add('propername')
        xref_targets = [clean_xref(t) for t in XREF.findall(body)]
        xref_targets = [t for t in xref_targets if t and '˚' not in t and t != k1]

        # stage 1 — compositional (own datasets + body backstop + greedy decomposition)
        compound_parts = ''
        if k1 in comp_set or COMPOUND_BODY.search(body):
            tags.add('compound')
        if k1 in deriv_set or VON.search(body):
            tags.add('derivative')
        if 'compound' not in tags:
            d = decompose(k1)
            if d and len(d) >= 2:              # splits into ≥2 attested headwords → a compound
                tags.add('compound')
                compound_parts = '+'.join(d)

        # stage 3 — descriptive/bahuvrīhi gloss
        if BVR.search(gl):
            tags.add('descriptive-compound')

        # stage 4 — edit-distance-filtered normalization re-join + xref resolution
        variant_of, variant_dicts = find_variant(k1)
        if variant_of:
            tags.add('spelling-variant')
        xref_kind = ''
        xref_hit = ''
        for t in xref_targets:
            # PWG says "= X" and X is a near-spelling of the headword -> spelling variant
            if ckey and ckey(t) == ckey(k1) and edist(k1, t) <= ED_MAX:
                xref_kind = 'spelling-variant'
                xref_hit = t
                break
            # X is itself an attested headword (exact, or a near-variant) -> genuine cross-ref
            if any(t in dict_exact[c] for c in ALL_DICTS) or find_variant(t)[0]:
                xref_kind = xref_kind or 'xref-attested'
                xref_hit = xref_hit or t
        if xref_kind == 'spelling-variant':
            tags.add('spelling-variant')
            if not variant_of:
                variant_of, variant_dicts = xref_hit, []
        elif xref_kind == 'xref-attested':
            tags.add('xref-attested')

        # ---- primary verdict by precedence ----
        if 'misreading' in tags:
            verdict = 'misreading'
        elif 'spelling-variant' in tags:
            verdict = 'spelling-variant'
        elif 'xref-attested' in tags:
            verdict = 'xref-attested'
        elif 'propername' in tags:
            verdict = 'propername'
        elif 'compound' in tags or 'derivative' in tags:
            verdict = 'compositional'
        elif 'descriptive-compound' in tags:
            verdict = 'descriptive-compound'
        # stage 5 — v2 citation-source fallback (only when no direct signal fired)
        elif v2cat.get(k1) == 'ms_catalogue_propernoun':
            verdict = 'catalogue-propername'   # cited only from a manuscript catalogue → a name/title
        elif v2cat.get(k1) == 'kosa_nighantu_not_digitised':
            verdict = 'kosa-corpus-gap'        # attested in a koṣa PWG names but not digitised
        else:
            verdict = 'residue'

        rows.append({
            'k1': k1,
            'core': '1' if pu[k1] else '',
            'verdict': verdict,
            'tags': '|'.join(sorted(tags)),
            'variant_of': variant_of or '',
            'variant_dicts': '|'.join(variant_dicts),
            'xref_target': xref_hit,
            'compound_parts': compound_parts,
            'v2_src_category': v2cat.get(k1, ''),
            'accented': accent.get(k1, ''),
            'gloss': gl,
        })

    # ---- outputs ----------------------------------------------------------------
    cols = ['k1', 'core', 'verdict', 'tags', 'variant_of', 'variant_dicts', 'xref_target',
            'compound_parts', 'v2_src_category', 'accented', 'gloss']
    with (out / 'pwg_ghostword_triage.tsv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter='\t')
        w.writeheader()
        w.writerows(rows)

    core = [r for r in rows if r['core']]
    residue = [r for r in core if r['verdict'] == 'residue']
    with (out / 'pwg_ghostword_residue.tsv').open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['k1', 'accented', 'gloss'], delimiter='\t')
        w.writeheader()
        for r in residue:
            w.writerow({'k1': r['k1'], 'accented': r['accented'], 'gloss': r['gloss']})

    def dist(sub):
        return dict(Counter(r['verdict'] for r in sub).most_common())
    # cross-validate my verdict against v2's independent citation-source category
    xval = {}
    for r in core:
        xval.setdefault(r['verdict'], Counter())[r['v2_src_category'] or '(none)'] += 1
    xval = {v: dict(c.most_common()) for v, c in xval.items()}
    summary = {
        'study': 'H1323 — PWG ghost-word triage cascade (stages 1-4), on the H1310 v2 shortlist',
        'as_of': '2026-07-19',
        'confusion_key_reused': 'SanskritSpellCheck detectors/slp1util.confusion_key' if ckey else None,
        'pwg_unique_total': len(rows),
        'core_absent_from_every_dict': len(core),
        'core_by_verdict': dist(core),
        'core_residue': len(residue),
        'core_verdict_vs_v2_src_category': xval,
        'all_pwg_unique_by_verdict': dist(rows),
    }
    (out / 'pwg_ghostword_triage_summary.json').write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('core (absent from every dict) verdicts: %s' % dist(core), file=sys.stderr)
    print('core residue (genuine ghost candidates): %d' % len(residue), file=sys.stderr)
    print('wrote triage.tsv + residue.tsv + summary', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
