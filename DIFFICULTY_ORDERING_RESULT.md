# Difficulty & ordering: does corpus frequency predict Sanskrit learning order?

_Created: 14-07-2026 · Last updated: 22-07-2026_

The first measured result of [RQ1](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md)
of the digital-Sanskrit-pedagogy field (wave-1a, handoff
[H913](https://github.com/gasyoun/Uprava/blob/main/handoffs/H913-Opus_SanskritGrammar_pedagogy-w1a-difficulty-ordering_14.07.26.md)).
Sibling of the textbook-sequencing result
[`S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md).
Produced by [`scripts/build_difficulty_ordering.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_difficulty_ordering.py)
on **Opus 4.8 (`claude-opus-4-8[1m]`)**, 14-07-2026. Aggregate numbers only (no in-copyright textbook text is reproduced).

## The question

Corpus frequency is the obvious candidate for "what to teach first" — learn the commonest words
first. RQ1 tests it three ways: does a corpus-frequency ordering match (A) an **expert** curated
learn-first ordering, and (B) the order **textbooks** actually introduce vocabulary; and (C) how do
the textbooks compare with each other?

## Method & data

| Analysis | Compares | Data | Metric |
|---|---|---|---|
| **A** | curated learn-first order vs raw corpus frequency | kosha [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv): `core_rank` (Leonchenko "learn-these-first") vs `rank_all` (DCS token frequency), 7,120 lemmas with both | Kendall-τ, Spearman-ρ + centred rank-delta |
| **B** | textbook introduction order vs corpus frequency | `core_rank`/`rank_all` × per-book word→first-lesson derived from [`scripts/data/sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json) (3,213 exercise sentences, Devanāgarī→SLP1) | Kendall-τ (lesson, freq-rank) on the exact-match subset |
| **C** | textbooks vs each other | existing [`sequence_tau_summary.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sequence_tau_summary.csv) (S1) | Kendall-τ-b |

A **surface-form** join (no lemmatiser) is used for B — see Limitations.

## Results

### A. The expert order follows frequency — but the decisive move is *exclusion*

Over the 7,120 lemmas that carry both signals, the curated learn-first order tracks raw frequency
**very closely**: **Kendall-τ = 0.887, Spearman-ρ = 0.923** (both p ≪ 10⁻³). *Inside the content
vocabulary, frequency is a strong ordering signal.*

The real pedagogical work is at the boundary — **what the curated list leaves out**:

| Frequency band | Top-N lemmas absent from the learn-first list | Composition |
|---|---|---|
| top 50 | **23 (46 %)** | 15 indeclinable · 8 pronoun |
| top 100 | 30 (30 %) | 19 indeclinable · 11 pronoun |
| top 200 | 44 (22 %) | 31 indeclinable · 13 pronoun |

Every excluded high-frequency lemma is a **function word** — `ca`, `tu`, `api`, `iti`, `na`, `eva`
(particles/conjunctions), `tad`, `idam`, `etad`, `sa`, `ka`, `yad` (pronouns). A raw-frequency
flashcard deck would open with these; the expert curation removes them, because they are acquired
**structurally through grammar**, not memorised as vocabulary.

### A′. Corpus frequency carries a genre bias

The lemmas most **demoted** by the curation (frequent in the corpus, ranked near the bottom of the
learn-first list) are epic/kāvya-register content words:

| lemma | gloss | corpus rank | learn-first rank |
|---|---|--:|--:|
| `vara` | boon / suitor | 82 | ~7443 |
| `vīra` | hero | 138 | ~7361 |
| `rakta` | red, blood | 226 | ~7374 |
| `varṣa` | rain, year | 186 | ~7252 |

The DCS corpus is epic-, Purāṇa- and kāvya-heavy, so its frequency counts over-weight the vocabulary
of *that* register. Frequency reflects the **corpus**, not the learner's target register — a
beginner-register frequency would rank these differently. (Per-POS, derived/causative verb classes
`10.Ā`/`Denom` are mildly promoted, adjectives mildly demoted; effects are small — see
[`pos_divergence.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/pos_divergence.tsv).)

### B. Textbook introduction order is frequency-agnostic

On the exact-match subset, the lesson at which a word is first introduced is **essentially
uncorrelated** with its corpus frequency, in all three textbooks:

| Textbook | τ(lesson, freq-rank) | type coverage | token coverage |
|---|--:|--:|--:|
| Bühler | 0.050 | 13.7 % | 32.3 % |
| Knauer | 0.056 | 19.4 % | 42.5 % |
| Kochergina | 0.072 | 15.9 % | 43.0 % |

Textbooks sequence by **grammar topic**, not vocabulary frequency: Bühler lesson I already contains
`tatra`, `tadā`, `atra`, `adya` (moderate-frequency adverbs), not the corpus's top words.

### C. …yet the textbooks agree with each other far more than with frequency (context, S1)

Bühler↔Kochergina τ = 0.446, Knauer↔Kochergina τ = 0.835 — an order of magnitude above the ≈0.05
textbook-vs-frequency agreement. There **is** a shared pedagogical sequence; it just isn't the
frequency sequence.

## Pedagogical reading (the bottom line)

Corpus frequency is a useful **ordering** signal for content vocabulary (τ=0.89 against expert
curation) but **not a drop-in learning order**. To become one it needs two corrections the raw
number can't supply: **(1) function-word exclusion** — the top ~46 % of high-frequency lemmas are
grammar words to teach structurally, not to drill; and **(2) genre correction** — DCS frequency is
epic/kāvya-weighted, so it over-ranks that register's content words. And the textbooks' own strong
mutual agreement (τ up to 0.83) on a *non-frequency* order says the grammar-topic spine is the real
scaffold. This directly shapes the field's **frequency-ordered SRS** deliverable: strip the function
words, genre-weight the counts, and sequence *within* the grammar spine — do not SRS raw `rank_all`.

## W2 robustness: lemmatised join (added 22-07-2026, handoff H1465)

B's near-zero τ was measured on a **surface-form** join, whose 14–19% type coverage is
skewed toward indeclinables and pronouns (lemma == surface). W2 adds a heuristic
**a-stem / ā-stem suffix-stripping lemmatiser** — [`scripts/build_lemmatised_join_robustness.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_lemmatised_join_robustness.py) —
that recovers the citation-form stem from inflected nominal surface forms (case-ending
tables for the two declension classes covering the large majority of Sanskrit nominal
content words), then re-runs the textbook-vs-frequency join **restricted to nominal
content-word POS** (m/f/n/mf/mn/fn/mfn/adj) so the comparison is apples-to-apples with
the surface-only content-word subset, not with the (4) figure's indeclinable/pronoun-heavy
sample.

| Book | Surface-only (nominal subset) n / cov / τ | Lemmatised join n / cov / τ | Coverage gain |
|---|---|---|---|
| Bühler | 182 / 6.7% / τ=−0.051 | 487 / 18.0% / τ=+0.101 | +11.3 pp |
| Knauer | 135 / 9.8% / τ=+0.066 | 311 / 22.7% / τ=−0.006 | +12.9 pp |
| Kochergina | 292 / 8.7% / τ=+0.015 | 651 / 19.3% / τ=+0.023 | +10.6 pp |

Coverage on the nominal content-word subset roughly **doubles-to-triples** and τ stays in
the same near-zero band (all |τ| ≤ 0.10, all far below (5)'s textbook-vs-textbook 0.45–0.84).
**Result (4) is robust**: textbook introduction order is frequency-agnostic for inflected
content-word nominals, not merely an artefact of the surface-join's bias toward
easily-matched, high-frequency function words. Full numbers:
[`data/difficulty_ordering/lemmatised_join_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/lemmatised_join_stats.json) ·
per-token join: [`lemmatised_join.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/lemmatised_join.tsv).

**Scope of the W2 lemmatiser** — a-stem and ā-stem thematic declension only (the two
classes covering most Sanskrit nouns/adjectives): i-stem, u-stem, and consonant-stem
nominals, and all verb conjugation, are **out of scope**. Recovering a verb root from a
conjugated surface form needs guṇa/vṛddhi ablaut reversal, not suffix stripping, and
consonant stems are irregular enough that a hand suffix table would be unreliable —
stated as a limitation, not hidden.

## Limitations

- **W2 lemmatised join covers only a-/aa-stem nominal declension** (see above) — i-/u-/consonant-stem nominals and all verb-conjugation forms still rely on the surface-only join; a real morphological analyser (segmenter) would be needed for full-coverage confirmation (→ 5/5 gate).
- **A rests on one curated list** ("Leonchenko" core-vocabulary compilation, extracted from the VisualDCS archive — an internal learn-these-first ranking, not itself a peer-reviewed publication) as the "expert" ground truth; a second curated order would strengthen it.
- **Frequency = one corpus** (DCS); the genre-bias point is argued, not yet quantified against a register-balanced count.
- No learning-gain evidence — this is an *ordering* study, not an *outcome* study (that is RQ4/A32).

## Reproduce

```
python scripts/build_difficulty_ordering.py            # reads ../kosha frequency + scripts/data
python scripts/build_difficulty_ordering.py --freq <path-to-lemma_frequency.tsv>
python scripts/build_lemmatised_join_robustness.py      # W2: a-/aa-stem lemmatised join
```

Outputs → [`data/difficulty_ordering/`](https://github.com/gasyoun/SanskritGrammar/tree/main/data/difficulty_ordering):
`core_vs_frequency.tsv` (7,120 lemmas, both ranks + delta) · `pos_divergence.tsv` · `textbook_frequency_join.tsv` · `stats.json` (all headline numbers + provenance) · `lemmatised_join.tsv` + `lemmatised_join_stats.json` (W2).

---

_Dr. Mārcis Gasūns_
