# Audit — SANGRAM SE case-count denominator commensurability

_Created: 20-07-2026 · Last updated: 20-07-2026_

The SANGRAM case-semantics cluster (`SG-SE-*`) publishes case counts across several
articles, all off the **same pinned DCS-2026 snapshot** (source commit `04e0778`,
sha256 `8f3b06…`). For those counts to be comparable, every article must denominate
them against the same, self-consistent case-marked totals. This audit establishes that
common denominator family, reconciles it to the token, and records the gaps that the
machine-checked contract now forbids.

Model: Opus 4.8 (`claude-opus-4-8[1m]`), H1371.

## The canonical case-marked family

All values are exact counts on the pinned snapshot (`token` table, `feat_case`):

| Quantity | Definition | Value |
|---|---|---|
| `all_tokens` | every token | 5,688,416 |
| `case_bearing` | `feat_case IS NOT NULL` — **includes** the `Cpd` pseudo-case | 4,014,688 |
| `real_vibhakti` | the eight true vibhakti (Nom…Voc) — **excludes** `Cpd` | 3,173,636 |
| `Cpd` | compound-internal members (no overt case ending) | 841,052 |

**Invariant:** `case_bearing == real_vibhakti + Cpd` (4,014,688 = 3,173,636 + 841,052). ✓

Two legitimate denominator **bases** are in play and they are not interchangeable — a share
is only meaningful once its basis is named:

- **`case_bearing`** (incl `Cpd`) — the basis of SG-SE-002/SG-SE-004's `pct_of_case_bearing`.
- **`real_vibhakti`** (excl `Cpd`) — the natural per-case basis; this is where "Dat = 2.1 %"
  comes from (65,423 / 3,173,636 = 2.06 %, not 65,423 / 4,014,688 = 1.63 %).

## Reconciliation to the token

`case_bearing` partitions **exactly** by part of speech (`upos`), and the two already-published
sub-denominators are precisely the NOUN and PRON cells of the `real_vibhakti` (excl `Cpd`) partition:

| `upos` | case-bearing (incl `Cpd`) | real-vibhakti (excl `Cpd`) |
|---|---:|---:|
| NOUN | 2,388,507 | **1,790,270** ← `declension-overview` `inflected_noun_tokens` |
| ADJ | 599,361 | 472,922 |
| PRON | 585,607 | **544,999** ← `pronouns` `case_number_tokens` |
| VERB (participial case) | 369,326 | 320,784 |
| NUM | 71,782 | 44,574 |
| ADP / PART / INTJ | 105 | 87 |
| **Total** | **4,014,688** | **3,173,636** |

So the sub-denominators are commensurable with the master by construction (each is a POS-restricted
subset of `real_vibhakti`, itself a subset of `case_bearing`); the contract enforces the bound
`0 < sub ≤ case_bearing` rather than a false "they sum to the master" (they do not — they are
scoped subsets, not a full partition of the master).

## Gaps found and closed

Before this audit, three case-cluster articles reported case counts but cited **no** case-marked
master denominator, so their shares were not reconcilable:

| Article | Was | Now |
|---|---|---|
| `instrumental-dative` (SG-SE-003) | only `all_tokens` | + `case_bearing_tokens`, `real_vibhakti_tokens`; Ins/Dat shares on **both** bases |
| `locative` (SG-SE-005) | only `all_tokens`, `locative_total` | + `case_bearing_tokens`, `real_vibhakti_tokens`, locative share on both bases |
| `karaka-case` (SG-SE-013) | no `snapshot`, no `denominators` block | + `snapshot` (sha256), `denominators` (family) — brought to the sibling schema |

A second, subtler incommensurability is now made explicit rather than left implicit: SG-SE-002/004
compute per-case shares on the `case_bearing` basis (incl `Cpd`) while SG-SE-003's "2.1 %" prose used
the `real_vibhakti` basis (excl `Cpd`). The regenerated data files now carry **both** labelled shares
so no reader has to guess the basis.

## The contract

[`scripts/check_denominator_commensurability.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/check_denominator_commensurability.py)
scans every `sangram/articles/*/data/coverage_summary.json` and enforces five checks: master values
(any family-key alias must carry the one canonical value), family arithmetic, snapshot pin, the
case-cluster **gap** check (every `SG-SE` case article must cite the `case_bearing` master), and the
sub-denominator bound. It is wired into CI via
[`tests/test_denominator_commensurability.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_denominator_commensurability.py)
(bare `python -m pytest` auto-discovers it) and available as `npm run check-denominators`. A regeneration
that silently ships an incommensurable denominator can no longer merge green.

_Dr. Mārcis Gasūns_
