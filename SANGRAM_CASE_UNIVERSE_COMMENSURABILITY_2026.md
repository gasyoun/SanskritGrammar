# SANGRAM case-cluster universe commensurability (H1371)

_Created: 20-07-2026 · Last updated: 20-07-2026_

The SANGRAM case-semantics articles publish case-distribution shares off the **same pinned
DCS-2026 snapshot** (`04e0778`, sha256 `8f3b06…`), but they denominate those shares against
**different universes**. The number-level audit ([DCS_DERIVED_NUMBERS_LEDGER_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/DCS_DERIVED_NUMBERS_LEDGER_2026.md),
H1229) verifies each figure against its own generating predicate and is **structurally blind**
to the cross-article defect: two articles can each be CONFIRMED yet be incomparable. This
document is the commensurability layer over that ledger.

Model: Opus 4.8 (`claude-opus-4-8[1m]`), H1371. Companion to the denominator-family reconciliation
in [docs/AUDIT_SANGRAM_CASE_DENOMINATOR_COMMENSURABILITY_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/AUDIT_SANGRAM_CASE_DENOMINATOR_COMMENSURABILITY_2026.md).

## The seed defect

| Article | Nom count | Universe (denominator) | Share |
|---|---:|---|---:|
| case-system-overview (SG-SE-001) | 1 419 146 | real vibhakti, all POS — 3 173 636 | **44,7 %** |
| declension-overview (SG-MO-001) | 692 647 | inflected NOUN only — 1 790 270 | **38,7 %** |

Both correct inside their own article; "44,7 % vs 38,7 %" is a category error — same category
(nominative), different universe. Neither article cross-referenced the other, so a reader saw two
figures for "the nominative" with no signal they measure different things.

## The universe lattice

Four universes, each re-derived to its expected value from the pinned master by
[`sangram/audit/universe_commensurability.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/universe_commensurability.py):

| Universe | Predicate | Denominator |
|---|---|---:|
| `case_bearing` | `feat_case IS NOT NULL` (incl `Cpd`) | 4 014 688 |
| `real_vibhakti` | the eight vibhakti (excl `Cpd`) | 3 173 636 |
| `noun_inflected` | `upos='NOUN'` ∧ eight vibhakti | 1 790 270 |
| `pron_inflected` | `upos='PRON'` ∧ eight vibhakti | 544 999 |

Containment: `noun_inflected` ⊂ `real_vibhakti` ⊂ `case_bearing`; `pron_inflected` ⊂
`real_vibhakti` ⊂ `case_bearing`. A share over `noun_inflected` and a share over `real_vibhakti`
measure **genuinely different quantities** (within-NOUN vs whole-corpus), so they are legitimately
different, not a bug — but they must be labelled as such.

## Verdicts — 28 cross-article pairs, zero unclassified

`universe_commensurability.py` enumerates every pair of articles reporting the same case category
and adjudicates each. The committed result is
[`sangram/audit/universe_commensurability_verdicts.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/universe_commensurability_verdicts.json)
(CI-gated by [`tests/test_universe_commensurability.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_universe_commensurability.py)):

| Verdict | Pairs | Meaning |
|---|---:|---|
| `COMMENSURABLE` | 3 | same universe — directly comparable |
| `INCOMMENSURABLE-DECLARED` | 25 | different universe, but each article states its denominator |
| `INCOMMENSURABLE-UNDECLARED` | 0 | different universe with an unstated denominator (forbidden) |

The **3 COMMENSURABLE** pairs (Ins/Dat: SG-SE-001 vs SG-SE-003; Loc: SG-SE-001 vs SG-SE-005, all
on `real_vibhakti`) exist **because** the H1371 denominator fix added the `real_vibhakti` share to
SG-SE-003/005 — before the fix those were incommensurable. Every other divergence is now DECLARED
rather than silent.

## The ruling (method П8)

For a corpus-wide "case distribution" claim the **canonical universe is `real_vibhakti`** (the
eight true vibhakti, 3 173 636) — not `case_bearing` (which folds in the `Cpd` pseudo-case) and
not a POS-restricted universe. A sub-article that counts the same category over a different
universe **must** name its universe and cross-link the sibling. Codified as
[П8](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx)
and applied in-place to the two seed articles' §2 universe blocks.

## Enforcement layers

1. [`scripts/check_denominator_commensurability.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/check_denominator_commensurability.py) — the denominator family (values, arithmetic, snapshot pin, gap, bound) over every `coverage_summary.json`; CI + `npm run check-denominators`.
2. [`tests/test_universe_commensurability.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_universe_commensurability.py) — the committed verdicts (zero unclassified, zero UNDECLARED, universes re-derived, seed pair typed); CI.
3. [`sangram/audit/universe_commensurability.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/universe_commensurability.py) — the local DB-backed regenerator (like `rederive_dcs_numbers.py`; the 920 MB master is gitignored, so this runs locally, not in CI).

_Dr. Mārcis Gasūns_
