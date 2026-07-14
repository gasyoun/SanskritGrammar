# A63 — Pedagogical difficulty & optimal learning-order for Sanskrit (outline)

_Created: 14-07-2026 · Last updated: 14-07-2026_

**ID:** A63 · **Readiness:** 2/5 (outline + first measured result) · **Home:** SanskritGrammar ·
**Venue candidates:** ISCLS / WSC-computational / eLex / CALICO / ReCALL (a human `@DECIDE`s).
RQ1 method paper of the [digital-Sanskrit-pedagogy field](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md);
seeded by handoff [H913](https://github.com/gasyoun/Uprava/blob/main/handoffs/H913-Opus_SanskritGrammar_pedagogy-w1a-difficulty-ordering_14.07.26.md).
Aggregate numbers only (in-copyright textbook sources). Model: Opus 4.8 (`claude-opus-4-8[1m]`).

## Thesis

Corpus frequency is widely assumed to be the natural learning order for a language's vocabulary. For
Sanskrit we show it is a strong *ordering* signal for content words (τ=0.89 against an expert
learn-first curation) but **not a drop-in curriculum**: the decisive pedagogical act is **excluding**
the highest-frequency function words (≈46 % of the top-50 lemmas), and raw corpus frequency carries a
**genre bias** (epic/kāvya-weighted) that misranks the beginner register. Textbooks, meanwhile,
order vocabulary **frequency-agnostically** (τ≈0.05) yet agree strongly with one another (τ up to
0.83) — evidence that the real scaffold is the grammar-topic spine, not frequency.

## Central results (all reproduced by the committed pipeline)

1. Curated learn-first vs raw frequency: **Kendall-τ = 0.887, Spearman-ρ = 0.923** (n=7,120).
2. Exclusion: **top-50 46 % / top-100 30 % / top-200 22 %** of highest-frequency lemmas absent from the learn-first list — **100 % of them indeclinables or pronouns**.
3. Genre bias: epic-register content words (`vīra`, `vara`, `rakta`) rank top-few-hundred by corpus frequency, ~7,300th by learn-first priority.
4. Textbook introduction order vs frequency: **τ ≈ 0.05** across Bühler / Knauer / Kochergina.
5. Textbook-vs-textbook agreement (S1 context): **τ up to 0.835** — an order of magnitude above (4).

## Data inventory (claim → backing asset)

| Result | Backing asset (committed) |
|---|---|
| (1) τ / ρ curated-vs-frequency | [`data/difficulty_ordering/stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/stats.json) + [`core_vs_frequency.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/core_vs_frequency.tsv) (from kosha [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv)) |
| (2) exclusion bands + POS | `stats.json` → `exclusion_by_frequency_band` |
| (3) genre-biased demotions | `core_vs_frequency.tsv` (delta-sorted) |
| (4) textbook τ + coverage | [`textbook_frequency_join.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/textbook_frequency_join.tsv) (from [`sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json)) |
| (5) textbook-vs-textbook | [`sequence_tau_summary.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sequence_tau_summary.csv) (S1) |
| generator | [`scripts/build_difficulty_ordering.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_difficulty_ordering.py) |
| full result writeup | [`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md) |

## Section outline

1. **Introduction** — the "learn the frequent words first" assumption; why Sanskrit tests it sharply (function-word-heavy, genre-skewed corpus, strong grammar-first pedagogical tradition).
2. **Related work** — frequency-graded readers / vocabulary lists (general L2 + the ACL frequency-pedagogy line); Sanskrit CALL & computational resources (DCS, kosha, Leonchenko core-vocabulary); the gap: no study has tested corpus frequency against Sanskrit learning order. *(to verify + cite live — 3/5 gate.)*
3. **Data & method** — the three analyses (A/B/C), the SLP1 surface-join and its coverage, the metric choices (Kendall-τ, symmetric rank-delta).
4. **Results** — the five results above with the tables from `stats.json`.
5. **Discussion** — the two corrections frequency needs (exclusion, genre-weighting) and the primacy of the grammar-topic spine; implications for a frequency-ordered SRS and a difficulty scorer.
6. **Limitations** — surface-join coverage (→ lemmatised replication, W2); single curated list; single corpus; ordering-not-outcome (→ RQ4/A32 user study).

## To 3/5 → 5/5

- **3/5:** live-verified related-work section (§2) + a lemmatised-join robustness check on the content-word subset (segmenter) to confirm result (4) beyond function words.
- **5/5:** a register-balanced frequency comparison quantifying the genre-bias claim; venue `@DECIDE` + byline/ORCID; author pass.

---

_Dr. Mārcis Gasūns_
