# S1 — Textbook sequencing: Kendall's τ over shared exercise clusters

_Created: 10-07-2026 · Last updated: 10-07-2026_

First shippable result of **Track C / spine S1** in
[ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md).
Computed by Opus 4.8 (`claude-opus-4-8`), 10-07-2026, on data already committed to
this repo — no new derivation.

## Question

Bühler (1878, German), Knauer (1908, German) and Kochergina (1998, Russian) are
three independent *orderings* of Sanskrit teaching material. When two books share
an exercise sentence, do they introduce it at a comparable point in their
sequence? Kendall's τ-b turns that into a number.

## Data

[`scripts/data/catalog.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/catalog.csv)
— 124 shared-sentence clusters, each carrying the lesson the sentence occupies in
every book that contains it. Bühler and Kochergina number lessons in Roman
numerals, Knauer in Arabic.

## Method

* For each book pair, keep only clusters present in **both** books.
* A sentence appearing in several lessons uses the **earliest** (min) lesson — its
  point of first introduction. Only 2 cells carry multi-lesson values.
* τ-b (ties-corrected) via `scipy.stats.kendalltau`, with its two-sided p-value.
* Reproducible generator:
  [`scripts/sequence_tau.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sequence_tau.py).

## Result

| Book pair | n shared clusters | Kendall's τ-b | p-value | Reading |
|---|---:|---:|---:|---|
| Bühler ↔ Knauer | 86 | **0.236** | 2.1 × 10⁻³ | weak but significant |
| Bühler ↔ Kochergina | 40 | **0.446** | 1.2 × 10⁻⁴ | moderate, significant |
| Knauer ↔ Kochergina | 12 | **0.835** | 2.4 × 10⁻⁴ | very strong, significant |

Per-cluster pairs used:
[`scripts/data/sequence_tau_pairs.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sequence_tau_pairs.csv);
summary:
[`scripts/data/sequence_tau_summary.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sequence_tau_summary.csv).

## Reading

The headline is that **the two German textbooks agree with each other the *least*
(τ = 0.24)** on where shared material lands, while each agrees more with the
Russian Kochergina. The strongest agreement, Knauer ↔ Kochergina (τ = 0.84), rests
on only 12 shared clusters, so treat it as suggestive, not established. All three
coefficients are positive and statistically significant: shared exercises are not
placed at random — there is a common underlying progression — but the three
traditions realise it differently, and *not* along the obvious German/Russian
language line.

## Caveats

1. **The 1878/1923 Bühler proxy.** This repo holds the 1923 Stockholm reprint as a
   text proxy for the 1878 first edition, unverified against the 1878 print (see
   the S1 caveat in the roadmap, gated on decision D4). τ measures *co-placement*,
   which is symmetric and makes **no** borrowing-direction claim — so this result
   is sound as stated; only a directional reading would need D4 cleared.
2. **Small n for Knauer ↔ Kochergina.** n = 12; the point estimate is high but its
   confidence interval is wide. Do not headline it.
3. **Earliest-lesson policy** is a modelling choice; a "latest" or "mean" policy
   would move the 2 multi-lesson clusters only, so the coefficients are robust to it.

## Reproduce

```
cd C:\Users\user\Documents\GitHub\SanskritGrammar
python scripts/sequence_tau.py
```

Requires `scipy` (present in the environment; add to
[`scripts/requirements.txt`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/requirements.txt)
if provisioning fresh).

_Dr. Mārcis Gasūns_
