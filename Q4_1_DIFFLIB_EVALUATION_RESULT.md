# Q4.1 difflib evaluation — precision against the 128-pair gold set

_Created: 24-09-2026 · Last updated: 24-09-2026_

[ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) §4 Q4.1: "Evaluate `difflib` against the 128 labeled pairs" — [`scripts/data/matches_review.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/matches_review.tsv) is already a gold set, use it before replacing anything. Generator: [`scripts/q41_difflib_gold_evaluation.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/q41_difflib_gold_evaluation.py).

## What is being scored

`extract_sentences.py match(threshold=0.82)` flags a pair as a candidate reuse whenever `difflib.SequenceMatcher(None, a, b).ratio() >= 0.82`. The 128 non-exact pairs it has flagged so far each carry an H327 verdict (`spelling_variant` / `length_mismatch` / `low_similarity`) from [`scripts/review_near_matches.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/review_near_matches.py), whose own docstring calls `low_similarity` "a candidate false positive". That is the ground truth this script scores difflib's `ratio()` against.

## Verdict counts (n=128)

| Verdict | n | score min | median | mean | max |
|---|---|---|---|---|---|
| `spelling_variant` | 58 | 0.851 | 0.921 | 0.9123 | 0.99 |
| `length_mismatch` | 20 | 0.833 | 0.923 | 0.8956 | 0.947 |
| `low_similarity` | 50 | 0.833 | 0.833 | 0.8337 | 0.857 |

## Precision at the shipped operating point (score ≥ 0.82)

Two readings over the same 128-pair pool, both reported (neither is hidden behind the other):

- **Strict** (TP = `spelling_variant` only; FP = `length_mismatch` + `low_similarity`): 58/128 = **0.4531**.
- **Lenient** (TP = `spelling_variant` + `length_mismatch`, both are genuine textual echoes even if the boundary slipped; FP = `low_similarity` only, per the pipeline's own documented false-positive class): 78/128 = **0.6094**.

## Precision sweep across score cutoffs

Same strict/lenient definitions as above, applied to the sub-pool with score ≥ cutoff. This is precision *within the flagged pool*, not corpus recall — see Scope, below.

| cutoff | n retained | spelling_variant | length_mismatch | low_similarity | precision (strict) | precision (lenient) |
|---|---|---|---|---|---|---|
| 0.82 | 128 | 58 | 20 | 50 | 0.4531 | 0.6094 |
| 0.85 | 75 | 58 | 16 | 1 | 0.7733 | 0.9867 |
| 0.9 | 44 | 33 | 11 | 0 | 0.7500 | 1.0000 |
| 0.95 | 15 | 15 | 0 | 0 | 1.0000 | 1.0000 |
| 0.98 | 3 | 3 | 0 | 0 | 1.0000 | 1.0000 |
| 0.99 | 1 | 1 | 0 | 0 | 1.0000 | 1.0000 |

## Scope — what this evaluation cannot say

This gold set is 128 pairs difflib already surfaced at score >= 0.82. It scores difflib's PRECISION at that operating point (of what it flagged, how much is genuine reuse) and how score separates the verdict classes. It cannot measure RECALL (reused sentences difflib never surfaced at all) — that needs an independent detector, which is the Q4.2 TRACER/Passim swap this evaluation gates.

This is the evidence check [ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) §4's Q4.2 gate names ("gate: Q4.1's evidence check accepted first"): a TRACER/Passim swap (Q4.2) should report Δ recall against this precision baseline, not re-derive it.

## Raw numbers

[`scripts/data/q41_difflib_gold_evaluation.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/q41_difflib_gold_evaluation.json).

_Гасунс_
