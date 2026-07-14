# Difficulty & ordering: does corpus frequency predict Sanskrit learning order?

_Created: 14-07-2026 · Last updated: 14-07-2026_

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

## Limitations

- **B is a surface-form join** (no segmenter): type coverage 14–19 %, token coverage 32–43 %, biased toward indeclinables/pronouns (lemma == surface). The near-zero τ is consistent across three books, but a lemmatised join (W2) is needed to confirm it for inflected content words.
- **A rests on one curated list** (Leonchenko) as the "expert" ground truth; a second curated order would strengthen it.
- **Frequency = one corpus** (DCS); the genre-bias point is argued, not yet quantified against a register-balanced count.
- No learning-gain evidence — this is an *ordering* study, not an *outcome* study (that is RQ4/A32).

## Reproduce

```
python scripts/build_difficulty_ordering.py            # reads ../kosha frequency + scripts/data
python scripts/build_difficulty_ordering.py --freq <path-to-lemma_frequency.tsv>
```

Outputs → [`data/difficulty_ordering/`](https://github.com/gasyoun/SanskritGrammar/tree/main/data/difficulty_ordering):
`core_vs_frequency.tsv` (7,120 lemmas, both ranks + delta) · `pos_divergence.tsv` · `textbook_frequency_join.tsv` · `stats.json` (all headline numbers + provenance).

---

_Dr. Mārcis Gasūns_
