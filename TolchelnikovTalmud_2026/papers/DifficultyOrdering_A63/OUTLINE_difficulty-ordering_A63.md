# A63 — Pedagogical difficulty & optimal learning-order for Sanskrit (outline)

_Created: 14-07-2026 · Last updated: 22-07-2026_

**ID:** A63 · **Readiness:** 3/5 (outline + first result + live-verified related work + W2 lemmatised-join robustness) · **Home:** SanskritGrammar ·
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
6. **W2 robustness (new, 22-07-2026):** (4) was a surface-form join (coverage skewed toward
   indeclinables/pronouns). A heuristic a-/aa-stem suffix-stripping lemmatiser raises
   nominal-content-word type coverage **2.1–2.7×** (Bühler 6.7%→18.0%, Knauer 9.8%→22.7%,
   Kochergina 8.7%→19.3%) and the near-zero τ **holds** (Bühler −0.05→+0.10, Knauer
   +0.07→−0.01, Kochergina +0.01→+0.02) — textbook sequencing is frequency-agnostic for
   inflected content words too, not an artefact of the surface-join's function-word bias.

## Data inventory (claim → backing asset)

| Result | Backing asset (committed) |
|---|---|
| (1) τ / ρ curated-vs-frequency | [`data/difficulty_ordering/stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/stats.json) + [`core_vs_frequency.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/core_vs_frequency.tsv) (from kosha [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv)) |
| (2) exclusion bands + POS | `stats.json` → `exclusion_by_frequency_band` |
| (3) genre-biased demotions | `core_vs_frequency.tsv` (delta-sorted) |
| (4) textbook τ + coverage | [`textbook_frequency_join.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/textbook_frequency_join.tsv) (from [`sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json)) |
| (5) textbook-vs-textbook | [`sequence_tau_summary.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sequence_tau_summary.csv) (S1) |
| (6) W2 lemmatised-join robustness | [`data/difficulty_ordering/lemmatised_join_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/lemmatised_join_stats.json) + [`lemmatised_join.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/difficulty_ordering/lemmatised_join.tsv) |
| generator | [`scripts/build_difficulty_ordering.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_difficulty_ordering.py) + [`scripts/build_lemmatised_join_robustness.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_lemmatised_join_robustness.py) (W2) |
| full result writeup | [`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md) |

## Section outline

1. **Introduction** — the "learn the frequent words first" assumption; why Sanskrit tests it sharply (function-word-heavy, genre-skewed corpus, strong grammar-first pedagogical tradition).
2. **Related work** — see §2 below (live-verified, 22-07-2026).
3. **Data & method** — the three analyses (A/B/C), the SLP1 surface-join and its coverage, the metric choices (Kendall-τ, symmetric rank-delta); W2 adds the a-/aa-stem suffix-stripping lemmatised join.
4. **Results** — the six results above with the tables from `stats.json` + `lemmatised_join_stats.json`.
5. **Discussion** — the two corrections frequency needs (exclusion, genre-weighting) and the primacy of the grammar-topic spine; implications for a frequency-ordered SRS and a difficulty scorer.
6. **Limitations** — W2 lemmatised join covers only a-/aa-stem nominal declension (not i-/u-/consonant stems or verb conjugation — root recovery needs ablaut reversal, out of scope for suffix-stripping); single curated list; single corpus; ordering-not-outcome (→ RQ4/A32 user study).

## §2 Related work (live-verified 22-07-2026)

**Frequency-graded vocabulary lists and readers (general L2).** The idea that a language's
highest-frequency words are the right thing to teach first is decades old in L2 pedagogy:
West's *General Service List* (1953, ~2,000 words from a written-English corpus, chosen for
~90–95% coverage of colloquial speech) is the founding case, and Nation's
*Learning Vocabulary in Another Language* (2001) is the standard synthesis of the
frequency-first vocabulary-acquisition literature it spawned. The *New General Service List*
(Browne, Culligan & Phillips, 2013, ~2,800 words, explicitly combining corpus-frequency
statistics with pedagogic judgment) is the direct modern descendant, and remains the basis
for graded-reader series built on frequency bands. The **CEFR-graded lexical-resource line**
(the CEFRLex family, e.g. EFLLex, Université catholique de Louvain) formalises the same idea
per proficiency level from L2-learner corpora rather than native-speaker corpora, and a recent
ACL BEA-workshop line (e.g. the CEFR-based contextual lexical-complexity classifier, BEA 2023;
Nature *Humanities & Social Sciences Communications* 2025 on supplementing CEFR lists with
corpus-frequency + dictionary-view + polysemy signals) treats frequency as one predictor among
several, not a sufficient one — the same qualified role result (1)+(2) find for Sanskrit.
None of this literature, to our knowledge, tests frequency order against an *expert curated
learn-first* order the way analysis A does, or against *actual textbook sequencing* the way
analysis B/W2 does — most of it validates frequency lists against corpus coverage or learner
judgments, not against a second independent pedagogical ordering.

**Sanskrit computational linguistics & CALL resources.** The Digital Corpus of Sanskrit (DCS;
Hellwig 2010–2026), the manually-validated lexical/morphosyntactic corpus this paper's
frequency counts are drawn from (via kosha's `lemma_frequency.tsv` sidecar), is the
field's central resource; Hellwig & collaborators' Treebank of Vedic Sanskrit (LREC 2020)
extends it with Universal-Dependencies syntax. Huet's Sanskrit Heritage Engine/Reader
(Huet, "Sanskrit Corpus Manager"; "A Distributed Platform for Sanskrit Processing", COLING
2014) is the best-known computer-assisted Sanskrit reading tool — a segmenter/analyser, not a
pedagogical sequencer. The 2024/2025 survey *Sandarśana: A Survey on Sanskrit Computational
Linguistics and Digital Infrastructure for Sanskrit* (ACM Computing Surveys) catalogues this
resource landscape (corpora, segmenters, morphological analysers, treebanks) and — consistent
with our gap claim — contains no pedagogical-sequencing or vocabulary-ordering study. kosha's
`lemma_frequency.tsv` (this paper's frequency source) and its `core_rank` column (an internal
"Leonchenko" learn-these-first compilation extracted from the VisualDCS archive, not itself a
peer-reviewed publication) are infrastructure, not prior *studies* of the RQ1 question.

**The gap.** No prior work — general-L2 or Sanskrit-specific — has tested raw corpus-frequency
order against (a) an expert-curated Sanskrit learn-first order or (b) actual Sanskrit-textbook
vocabulary-introduction order. This paper is, to our knowledge, the first to do either.

## To 3/5 → 5/5

- **3/5 — DONE 22-07-2026 (H1465, wave W2):** live-verified related-work §2 above + the
  a-/aa-stem lemmatised-join robustness check (result 6) confirming (4) for inflected
  nominal content words, not just the surface-join's function-word-heavy subset.
- **5/5:** a register-balanced frequency comparison quantifying the genre-bias claim
  (result 3); i-/u-/consonant-stem + verb-conjugation lemmatisation (a real morphological
  analyser, beyond W2's suffix-stripping scope) for full-coverage confirmation of (4);
  venue `@DECIDE` + byline/ORCID; author pass.

---

_Dr. Mārcis Gasūns_
