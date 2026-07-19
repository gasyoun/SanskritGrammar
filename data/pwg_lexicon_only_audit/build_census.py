# -*- coding: utf-8 -*-
"""H1310 - Audit PWG's 32,690 lexicon-only headwords against digitised kosas.

Input : pwg_register_genre.tsv  (col8 lexicon_only==1)  -- SLP1 k1
Corpus: csl-orig/v02 dictionaries, headword sets in SLP1
  kosas (Sanskrit-Sanskrit thesauri): armh vcp skd (<k1> fmt) + abch acph acsj nmmb (kosha <syns> fmt)
  text-dicts (weaker evidence -- MW's L. hides kosa provenance): mw ap90 ap pw
  (Amara AK not digitised in csl-orig -- recorded as a gap; PWG's own `sources` col names its AK citations)
Output: pwg_lexicon_only_cross_dictionary_census.tsv + summary json
"""
import re, sys, os, json, collections
sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))

def _first_existing(cands, what):
    for p in cands:
        if os.path.exists(p):
            return p
    sys.exit(f'ERROR: could not locate {what}; tried:\n  ' + '\n  '.join(cands))

# csl-orig checked out as a sibling of the repo root (GitHub/csl-orig); env override wins.
CSL = os.environ.get('CSL_ORIG_V02') or _first_existing([
    os.path.normpath(os.path.join(HERE, '..', '..', '..', 'csl-orig', 'v02')),
    'C:/Users/user/Documents/GitHub/csl-orig/v02',
], 'csl-orig/v02')
# register TSV: sibling data folder in-repo, else alongside this script (scratch runs).
PWG = os.environ.get('PWG_REGISTER_TSV') or _first_existing([
    os.path.normpath(os.path.join(HERE, '..', 'pwg_register_genre', 'pwg_register_genre.tsv')),
    os.path.join(HERE, 'pwg_register_genre.tsv'),
], 'pwg_register_genre.tsv')
SCRATCH = HERE   # outputs land next to this script

KOSA_K1   = ['armh', 'vcp', 'skd']            # kosa, <k1> Cologne format
KOSA_SYNS = ['abch', 'acph', 'acsj', 'nmmb']  # kosa, sanskrit-kosha <syns> format
KOSA      = KOSA_K1 + KOSA_SYNS
# independence axis (folded in from the v1 audit, PR #447):
CORPUS    = ['bhs', 'gra']  # text-CORPUS dicts (Edgerton BHS, Grassmann RV) -- every headword is
                            # text-sourced, and NOT of the Bohtlingk/PW tradition -> real independence
APTE      = ['ap90', 'ap']  # Apte: text-based but mixed with lexical entries (no L.-split here)
SAME_SRC  = ['pw']          # PW = Bohtlingk's kuerzere Fassung, SAME author as PWG -> presence is
                            # NOT independent corroboration (MW likewise partly derives from PW)
TEXTDICTS = ['mw'] + CORPUS + APTE + SAME_SRC
K1_DICTS  = KOSA_K1 + TEXTDICTS

# PWG `sources` tokens that correspond to a kosa we compare against (for novelty test)
PWG_TOKEN_TO_DICT = {'H': 'abch', 'HALAY': 'armh', 'ŚKDR': 'skd', 'SKDR': 'skd'}

ALPHA = re.compile(r'^[a-zA-Z]+$')

def load_k1(code):
    hw = set()
    for fn in (f'{code}.txt', f'{code}_hwextra.txt'):
        p = f'{CSL}/{code}/{fn}'
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8') as f:
            for line in f:
                if '<k1>' in line:
                    for m in re.findall(r'<k1>([^<]+)', line):
                        w = m.strip()
                        if w:
                            hw.add(w)
    return hw

def load_syns(code):
    """kosha format: `<eid>N<syns>[<s>]lemma-GEN,lemma-GEN,...[</s>]` on the <syns> line."""
    hw = set()
    with open(f'{CSL}/{code}/{code}.txt', encoding='utf-8') as f:
        for line in f:
            if '<syns>' not in line:
                continue
            content = line.split('<syns>', 1)[1]
            content = re.sub(r'<[^>]+>', '', content)   # strip <s></s> and any tag
            for tok in content.split(','):
                lemma = tok.strip().split('-')[0].strip()
                if lemma and ALPHA.match(lemma):
                    hw.add(lemma)
    return hw

def load_mw_citations():
    """Split MW into <L>..<LEND> entries; per k1 record whether ANY entry carries a
    genuine (non-'L.') <ls> citation. MW marks purely-lexicographer senses <ls>L.</ls>,
    so a k1 whose every citation is 'L.' is itself koSa-sourced -- membership in MW then
    does NOT establish text attestation (the exact opacity this audit routes around)."""
    realcite, present = set(), set()
    txt = open(f'{CSL}/mw/mw.txt', encoding='utf-8').read()
    for chunk in re.split(r'(?=<L>)', txt):
        m = re.search(r'<k1>([^<]+)', chunk)
        if not m:
            continue
        k1 = m.group(1).strip()
        present.add(k1)
        ls = re.findall(r'<ls>([^<]*)</ls>', chunk)
        # a real citation = any <ls> whose leading source token is not exactly 'L.'
        if any(tok.strip() and tok.strip().split()[0] != 'L.' for tok in ls):
            realcite.add(k1)
    return realcite, present

def norm(w):
    """Conservative normalisation for a sensitivity pass: drop final visarga/anusvara."""
    return re.sub(r'[HM]$', '', w)

# ---- build headword sets ------------------------------------------------
sets = {}
for c in K1_DICTS:
    sets[c] = load_k1(c)
for c in KOSA_SYNS:
    sets[c] = load_syns(c)
for c in sorted(sets):
    tag = 'kosa' if c in KOSA else 'text'
    print(f'  {c:6s} [{tag}] {len(sets[c]):>7,} headwords', file=sys.stderr)

norm_sets = {c: {norm(w) for w in s} for c, s in sets.items()}

mw_realcite, mw_present = load_mw_citations()
print(f'  mw: {len(mw_present):,} headwords, {len(mw_realcite):,} with a non-L. citation '
      f'({len(mw_present)-len(mw_realcite):,} L.-only / lexical)', file=sys.stderr)

# ---- load PWG register rows ---------------------------------------------
# The cross-dictionary join is spelling-level (homonym-collapsed): MW/koSa headword
# sets carry their OWN hom numbering, which does not align with PWG's, so a k1 hit
# cannot be pinned to the specific PWG homonym. To quantify that, flag each
# lexicon_only row for whether PWG ITSELF text-attests the SAME spelling under a
# DIFFERENT homonym (register != lexical/uncategorised) -- if so, a MW/koSa spelling
# hit is plausibly that sibling sense, not this lexical one.
rows = []
text_sibling_k1 = set()      # k1 with >=1 dated-period (non-lexical) homonym in PWG
all_lexonly_k1 = collections.Counter()
with open(PWG, encoding='utf-8') as f:
    header = f.readline().rstrip('\n').split('\t')
    idx = {name: i for i, name in enumerate(header)}
    allrows = [line.rstrip('\n').split('\t') for line in f]
for c in allrows:
    if len(c) <= idx['sources']:
        continue
    k1 = c[idx['k1']]
    reg = c[idx['register']]
    if reg not in ('lexical', 'uncategorised', ''):
        text_sibling_k1.add(k1)          # this k1 has a dated-text homonym somewhere in PWG
for c in allrows:
    if len(c) <= idx['lexicon_only'] or c[idx['lexicon_only']] != '1':
        continue
    rows.append({
        'L_id': c[idx['L_id']],
        'k1': c[idx['k1']],
        'hom': c[idx['hom']] if idx['hom'] < len(c) else '',
        'sources': c[idx['sources']] if idx['sources'] < len(c) else '',
    })
print(f'  PWG lexicon_only rows: {len(rows):,}; k1 with a text-sibling homonym: '
      f'{len(text_sibling_k1):,}', file=sys.stderr)

# ---- join & classify ----------------------------------------------------
out = []
counts = collections.Counter()
counts_by_sibling = collections.Counter()
per_dict_hits = collections.Counter()
novel_kosa_words = []
for r in rows:
    k1 = r['k1']
    present = [c for c in K1_DICTS + KOSA_SYNS if k1 in sets[c]]
    kosa_hit = [c for c in KOSA if c in present]
    corpus_hit = [c for c in CORPUS if c in present]      # independent text-corpus attestation
    also_in_pw = 'pw' in present                          # same-source Bohtlingk (not independent)
    independent_present = [c for c in present if c not in SAME_SRC]  # anything but PW
    for c in present:
        per_dict_hits[c] += 1
    # PWG's own cited kosa tokens (from sources col) mapped to our dicts
    cited = {PWG_TOKEN_TO_DICT[t] for t in re.split(r'[|]', r['sources']) if t in PWG_TOKEN_TO_DICT}
    novel_kosa = sorted(set(kosa_hit) - cited)   # kosa attestation PWG did NOT itself cite
    mw_real = k1 in mw_realcite                  # MW attests it with a genuine (non-L.) source
    # Layered verdict. Genuine TEXT attestation = MW non-L. citation OR presence in a text-corpus
    # dict (BHS/GRA, every entry text-sourced). Bare membership in MW/PW/Apte is NOT text
    # attestation (they absorb the koSa vocabulary as L. entries; PW is the same author as PWG).
    if mw_real or corpus_hit:
        verdict = 'text-attested'                # real text attestation, independent of PW-copying
    elif kosa_hit:
        verdict = 'kosa-corroborated'            # in >=1 of our 7 koSas -> corroborated lexical word
    elif independent_present:
        verdict = 'dict-lexical'                 # in MW-L./Apte (not PW-only) -> lexical, no koSa/real-cite
    else:
        verdict = 'pwg-unique'                   # in NO independent dict (nowhere, or only same-source PW)
    counts[verdict] += 1
    has_sibling = k1 in text_sibling_k1
    counts_by_sibling[(verdict, has_sibling)] += 1
    if novel_kosa and not mw_real:
        novel_kosa_words.append(r['k1'])
    out.append({
        'L_id': r['L_id'], 'k1': k1, 'hom': r['hom'],
        'present_in': '|'.join(present),
        'mw_realcite': int(mw_real),
        'corpus_hit': '|'.join(corpus_hit),
        'also_in_pw_same_source': int(also_in_pw),
        'pwg_text_sibling': int(has_sibling),
        'n_kosa': len(kosa_hit),
        'novel_kosa': '|'.join(novel_kosa),
        'pwg_cited_sources': r['sources'],
        'verdict': verdict,
    })

# sensitivity: of the words absent from EVERY dict, how many collapse onto an existing
# headword under light normalisation (drop final visarga/anusvara) -> variant-spelling artifacts
absent = [o for o in out if o['verdict'] == 'pwg-unique' and not o['also_in_pw_same_source']]
allnorm = set().union(*norm_sets.values())
uniq_rescued = sum(1 for o in absent if norm(o['k1']) in allnorm)

# ---- write census -------------------------------------------------------
cols = ['L_id', 'k1', 'hom', 'verdict', 'mw_realcite', 'corpus_hit',
        'also_in_pw_same_source', 'pwg_text_sibling', 'n_kosa', 'present_in',
        'novel_kosa', 'pwg_cited_sources']
census = os.path.join(SCRATCH, 'pwg_lexicon_only_cross_dictionary_census.tsv')
with open(census, 'w', encoding='utf-8', newline='') as f:
    f.write('\t'.join(cols) + '\n')
    for o in out:
        f.write('\t'.join(str(o[c]) for c in cols) + '\n')

# cross-tab: verdict x whether PWG itself has a text-attested sibling homonym of the spelling
sibling_xtab = {}
for (v, s), n in sorted(counts_by_sibling.items()):
    sibling_xtab.setdefault(v, {})['with_text_sibling' if s else 'no_text_sibling'] = n

# ---- ghost-word shortlist (verdict==pwg-unique) + source-category tally ----
KOSA_TOK = re.compile(r'AK|TRIK|MED|ŚKDR|SKDR|RĀJAN|HALĀY|HĀR|ŚABDAC|WILS|WILSON|VYUTP|'
                      r'AMAR|NIGH|RATNAM|\bH\b')
CAT_TOK  = re.compile(r'Verz')
SCHOL_TOK = re.compile(r'Ind|COLEBR|HALL|BURN|Spr|ebend|WEBER|LIA|LASSEN|Journ|\bZ\b')
def src_category(src):
    if KOSA_TOK.search(src):  return 'kosa_nighantu_not_digitised'
    if CAT_TOK.search(src):   return 'ms_catalogue_propernoun'
    if SCHOL_TOK.search(src): return 'scholarly_journal_technical'
    return 'other_or_none'
shortlist = [o for o in out if o['verdict'] == 'pwg-unique']
ghost_cat = collections.Counter(src_category(o['pwg_cited_sources']) for o in shortlist)
# of the ghost-words, how many appear ONLY in same-source PW (Bohtlingk) vs nowhere at all
uniq_also_pw = sum(1 for o in shortlist if o['also_in_pw_same_source'])
uniq_nowhere = len(shortlist) - uniq_also_pw
sl_path = os.path.join(SCRATCH, 'pwg_ghostword_shortlist.tsv')
with open(sl_path, 'w', encoding='utf-8', newline='') as f:
    f.write('\t'.join(cols + ['src_category']) + '\n')
    for o in shortlist:
        f.write('\t'.join(str(o[c]) for c in cols) + '\t' + src_category(o['pwg_cited_sources']) + '\n')

summary = {
    'pwg_lexicon_only_total': len(rows),
    'ghostword_shortlist_total': len(shortlist),
    'ghostword_also_in_pw_same_source': uniq_also_pw,
    'ghostword_absent_from_every_dict': uniq_nowhere,
    'ghostword_by_source_category': dict(ghost_cat.most_common()),
    'verdict_counts': dict(counts),
    'verdict_by_pwg_text_sibling': sibling_xtab,
    'k1_with_text_sibling_homonym': len(text_sibling_k1),
    'per_dictionary_hits': dict(per_dict_hits.most_common()),
    'dict_headword_sizes': {c: len(sets[c]) for c in sorted(sets)},
    'novel_kosa_corroboration_words': len(novel_kosa_words),
    'pwg_unique_rescued_by_normalisation': uniq_rescued,
    'kosa_dicts': KOSA, 'text_dicts': TEXTDICTS,
    'amara_gap': 'AK not digitised in csl-orig; PWG sources col records AK citations directly',
}
with open(os.path.join(SCRATCH, 'census_summary.json'), 'w', encoding='utf-8') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(json.dumps(summary, ensure_ascii=False, indent=2))
