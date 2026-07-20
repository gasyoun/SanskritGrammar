# Metadoc — SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md

_Created: 20-07-2026 · Last updated: 20-07-2026_

Companion record for
[SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md).

## Purpose

The government lexicon's own Limitations section conceded it was **untested against usage** — "a
screening layer, not a verdict" — while the folder README already advertised it as a valence
resource "about to be consumed on trust" by the parser/treebank stack. This report is that
missing corpus test: every one of Scherzl's 1 168 case-government relations scored against the DCS
dependency treebank, so a downstream consumer knows which frames are corpus-confirmed and which are
merely catalogued.

## Audience

Sanskrit lexicographers/syntacticians citing a government claim; parser/valence-frame builders
choosing which Scherzl relations to trust; anyone auditing the government lexicon before it enters
`errata.yml` or a paper.

## Provenance

- **Handoff:** [H1372](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1372-Opus_SanskritGrammar_scherzl-government-relations-vs-dcs-treebank-adjudication_20.07.26.md) (20-task wave H1355–H1374).
- **Model:** Opus 4.8 (`claude-opus-4-8`).
- **Inputs:** [`government_lexicon.jsonl`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/government_lexicon.jsonl) (H1195) + the [dcs-conllu](https://github.com/gasyoun/dcs-conllu) treebank. The CoNLL-U export is the same DCS-2026 master as `VisualDCS/src/DCS-data-2026/dcs_full.sqlite`: token count **5 688 416** and **11 096** verb lemmas match the sqlite exactly, which is why the conllu serialisation (which carries HEAD/DEPREL directly) was used in place of the sqlite the handoff named.
- **Shipped:** [PR #476](https://github.com/gasyoun/SanskritGrammar/pull/476) (first cut, 3-tier) then the completing PR bringing it to the handoff's 4-tier spec + hand-adjudication.

## Key design decisions (the judgment a fresh session would otherwise re-derive)

1. **Two evidence layers kept strictly separate.** Dependency arc (strong, ~4 % of corpus) vs
   co-occurrence (full corpus, weak). They are never blended into one score.
2. **Co-occurrence is measured against chance, not raw.** A frequent verb co-occurs with every
   case, so raw co-occurrence is uninformative; the report uses observed ÷ (verb_freq · base-rate).
   This is the single most important guard — it is what shrinks the raw 25-candidate CONTRADICTED
   screen to 1 real survivor and stops jñā+genitive (coocC 1533) being mis-flagged.
3. **Most-specific lemma match, never stem+root summed.** A prefixed reading (`vidhā`, `saṃdhā`)
   must not inherit the bare root's frame. Anusvāra `ṁ→ṃ` normalisation recovers 11 such verbs.
4. **CONTRADICTED is a screen, then hand-adjudicated.** The report classifies each survivor as
   defect / homonym-preverb-misjoin / system-vs-usage. The hand notes live in a dict in the script
   so the report can never silently claim a review that did not happen (unreviewed survivors print
   as UNREVIEWED).

## Improvement backlog (ranked)

1. **Stem→root normaliser** (guṇa/vṛddhi/sandhi undo) + DCS `lemma` preverb column — would shrink
   the 186 NOT-ADJUDICABLE (mostly `sarj`↔`sṛj`-type form mismatches, not missing verbs) and raise
   the confirmation floor. Highest value.
2. **Per-(verb, case) deprel split** in the profiles (currently deprel is pooled across cases) —
   sharpens "which construction" reads a governed case.
3. **Rerun as DCS dependency coverage grows** beyond ~4 %; UNATTESTED-INSUFFICIENT is the bucket
   that will move.
4. Feed CONFIRMED frames + the 246 case-alternation relations into a parser valence table.

## Limitations

- The **~3.9 % parse ceiling** bounds everything: CONFIRMED is a floor, UNATTESTED-INSUFFICIENT is
  genuinely "unknown". Do not read NOT-ADJUDICABLE or UNATTESTED-INSUFFICIENT as "Scherzl is wrong".
- CONTRADICTED thresholds (MIN_PARSED 20, MIN_DEPTOT 15, MAX_CONTRA_RATIO 0.5) are pre-registered
  and conservative; loosening them re-introduces parser-sparsity false positives.

## Revision history

| Date | Change |
|---|---|
| 20-07-2026 | Created. First cut (3-tier CONFIRMED/COOCCURRENCE/UNATTESTED/ABSENT, PR #476), then completed to the handoff's 4-tier spec (CONFIRMED/CONTRADICTED/UNATTESTED-INSUFFICIENT/NOT-ADJUDICABLE) with chance-based co-occurrence gating, TSV deliverable, and hand-adjudication of the single contradiction (√arc + abl → no defect). |

_Dr. Mārcis Gasūns_
