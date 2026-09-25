# Q4.2 TRACER-style swap — chunk-size tuning, Δ recall vs the 124-cluster baseline

_Created: 25-09-2026 · Last updated: 25-09-2026_

[ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) §4 Q4.2: "Swap in TRACER / Passim, tune chunk size per [2024.nlp4dh-1.12](https://aclanthology.org/2024.nlp4dh-1.12/); report Δ recall vs the 124-cluster baseline." Gate (Q4.1's evidence check accepted first) is cleared — see [`Q4_1_DIFFLIB_EVALUATION_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/Q4_1_DIFFLIB_EVALUATION_RESULT.md). Generator: [`scripts/q42_tracer_style_recall_evaluation.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/q42_tracer_style_recall_evaluation.py).

## What "TRACER/Passim" means here

Neither tool (both JVM/Spark, unverified as installable in this repo's CI per [docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md) "Unverified externals") is vendored. Per that memo's SG-H4, this implements the one transferable finding Miyagawa et al. 2024 (NLP4DH) validated *on Sanskrit*: smaller matching chunks raise recall over whole-string comparison — shingle-seeded candidate generation (the shape both TRACER's anchor n-grams and Passim's MinHash/LSH reduce to), then local chunk-window alignment scoring. Not either tool's own codebase.

## Pool

3-book pool (buhler, knauer, kochergina) — the same scope the 124-cluster catalog was built from; Q4.3's Apte/Whitney extension left `matches.json`/`catalog.mdx` at this 3-book state on purpose, so this stays comparable. 3213 sentence candidates, 32216 pairs survive 4-gram shingle seeding (>= 1 shared shingles) — the blocking step that keeps this tractable in place of a full cross-product.

## Claim 1 — recall on the existing 128-pair gold (regression floor)

All 78 gold true pairs (`spelling_variant` + `length_mismatch`) already clear the shipped whole-sentence 0.82 gate by construction — this only checks the shingle-seeding step does not *lose* any of them before scoring. **76/78 recovered (recall=0.9744).** This is a floor, not the roadmap's recall gain.

2 pair(s) missed — both are the same transposition edit (`dhāiiiu` ↔ `dhāuiii`): a character swap shares no contiguous 4-gram shingle even though `SequenceMatcher.ratio()` scores the pair high, a known blind spot of contiguous-shingle seeding (not of the chunk scorer itself, which would find these if seeded).

## Claim 2 — new candidates beyond the 124-cluster baseline, per chunk size

Pairs with whole-sentence ratio < 0.82 (never surfaced by the shipped detector) whose best chunk ratio at window size W clears 0.9. Per Miyagawa et al.'s own finding, smaller W should surface more such pairs than the whole-string reference row:

| chunk size W | new candidates found |
|---|---|
| 8 | 168 |
| 12 | 35 |
| 16 | 6 |
| 20 | 7 |
| whole | 0 |

The trend holds at the ends (small W finds far more than whole-string, which finds none by definition) but is not perfectly monotonic in between (16 < 20) — at these small counts a handful of borderline pairs crossing the 0.90 cutoff in either direction is expected noise, not a claim that every smaller W strictly dominates.

## Scope — what this evaluation cannot say

New candidates (claim 2) are UNVERIFIED — no H327-style human review pass has scored them. This reports discovery counts and score distributions, not a verified recall percentage or precision figure, because no ground truth exists yet for pairs outside the 128-pair gold. A verified Δ recall number requires running the same review pass Q4.1's gold set went through on this new-candidate pool first.

## Raw numbers

[`scripts/data/q42_tracer_style_recall_evaluation.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/q42_tracer_style_recall_evaluation.json) (includes up to 5 top-scoring examples per chunk size).

_Гасунс_
