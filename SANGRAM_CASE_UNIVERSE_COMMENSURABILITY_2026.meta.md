# Metadoc — SANGRAM_CASE_UNIVERSE_COMMENSURABILITY_2026.md

_Created: 20-07-2026 · Last updated: 20-07-2026_

**Subject:** [SANGRAM_CASE_UNIVERSE_COMMENSURABILITY_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/SANGRAM_CASE_UNIVERSE_COMMENSURABILITY_2026.md)

## Purpose

The commensurability-of-record for the SANGRAM case cluster: which cross-article
case-share comparisons a reader may actually make, and which are category errors
over silently different universes. Answers the class of defect the number-level
ledger (H1229) is structurally blind to — nothing wrong inside an article, only
the cross-article comparison. Sits one layer above
[DCS_DERIVED_NUMBERS_LEDGER_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/DCS_DERIVED_NUMBERS_LEDGER_2026.md).

## Audience

Future sessions editing any SG-SE/SG-MO case article (check the universe before
comparing a share to a sibling's); referees of the case-cluster papers; the author
when citing a case-distribution figure externally.

## Provenance

- Handoff: [H1371](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1371-Opus_SanskritGrammar_se-cluster-case-count-commensurability-denominator-contract_20.07.26.md)
- Model: Opus 4.8 (`claude-opus-4-8[1m]`), 20-07-2026
- Corpus: `dcs_full.sqlite` pin `04e0778d3dc971030229179e25eea043d06ff397`
- Regenerator: [sangram/audit/universe_commensurability.py](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/universe_commensurability.py) → [universe_commensurability_verdicts.json](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/universe_commensurability_verdicts.json)
- Method rule: [П8](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx)

## Limitations

- Covers **case-category** shares in the case cluster; other cross-article category
  comparisons (tense, mood, compound type) are not yet enumerated.
- The register of published claims in `universe_commensurability.py` is hand-maintained;
  a new case article that reports a per-case share must be added to `CLAIMS` (else its
  pairs are silently absent — the opposite risk to a false verdict).
- The DB-backed regenerator is local-only (920 MB master gitignored); CI validates the
  committed verdicts JSON, not a fresh re-derivation.

## Ranked improvement backlog

1. Auto-extract the `CLAIMS` register from each `coverage_summary.json` (`pct_of_*` keys)
   instead of hand-listing it, so a new article can't be silently omitted.
2. Generalise beyond case: enumerate tense/mood/compound-type cross-article pairs on the
   same universe machinery.
3. Fold the two seed-article cross-links into a reusable MDX snippet so every future
   sub-article inherits the П8 cross-reference automatically.

## Revision history

| Date | Change | Actor |
|---|---|---|
| 20-07-2026 | Created: universe lattice + 28-pair verdicts (25 declared, 3 commensurable) + П8 ruling + two seed-article repairs | Opus 4.8 (`claude-opus-4-8[1m]`), H1371 |

_Dr. Mārcis Gasūns_
