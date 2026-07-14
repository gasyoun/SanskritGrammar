# Architecture — Digital Sanskrit Pedagogy

_Created: 14-07-2026 · Last updated: 14-07-2026_

Component boundaries, the data model behind the aspect taxonomy, and the build-vs-reuse verdict per
piece. For the [field definition](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md);
plan cover [here](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md).

## 1. What the field owns vs consumes

The field is an **integration / consumption layer**. It owns **no primary data** (dictionaries,
corpus, morphology engines) — a hard boundary inherited from the ecosystem's reuse-first mandate.

- **Owns:** the tagged pedagogy asset index (drives the metadoc + views); the difficulty/ordering derivation; drill-generation + answer-verification; the evaluation harness; the "last-mile" wiring spec; the Zaliznyak on-ramp; the field's papers.
- **Consumes (never rebuilds):** CDSL dictionaries · DCS corpus/frequency · vidyut/Heritage morphology + `cheda` · the Zaliznyak grammar index · `corpus_lexicon` alignment · Systema SRS/exercise/LMS engines.

## 2. Data model — one tagged index drives everything

The metadoc's aspect-primary spine (§3) and its derived views (§4 matrix/journey/capability/
discipline) are two projections of a **single tagged dataset**. Target artifact (Wave 3):

`data/pedagogy_assets.tsv` — one row per asset/gap:

| column | meaning |
|---|---|
| `aspect` | sandhi · morphology · vocab · reading · panini · zaliznyak · audio · script · metre · composition · commentary · spell |
| `rung` | CEFR rung(s) A0…C2 |
| `status` | built · partial · planned · gap |
| `nlp_capability` | L0…L7 (+ cheda / paradigm-gen / form2lemma / difficulty / TTS / ASR) |
| `research_q` | RQ1…RQ4 (or blank) |
| `discipline` | śikṣā · vyākaraṇa · nirukta · chandas · kośa · kāvya · bhāṣya |
| `owning_repo` | the repo that owns it |
| `asset_path` | file/URL |
| `note` | one line |

The four derived views are `GROUP BY` pivots on this table:
- **Matrix** = pivot `aspect × rung → status`.
- **Learner-journey** = filter/sort by `rung` (aligns to Systema's ladder).
- **Capability** = group by `nlp_capability` (aligns to Systema's L0–L7).
- **Discipline** = group by `discipline` (the emic Vedāṅga frame).

Until this TSV lands, the metadoc rows are hand-curated (a known limitation — see the metadoc's
`.meta.md` backlog). Building it is Wave 3; the metadoc's §3/§4 are the human-readable spec it must
reproduce.

## 3. Component boundaries (which repo hosts what)

| Component | Repo | Boundary |
|---|---|---|
| Field spec (metadoc, plan, papers) | **SanskritGrammar** | the definition + agenda live here (this repo) |
| Difficulty/ordering, textbook-τ, Zaliznyak on-ramp | **SanskritGrammar** | inputs (textbooks, τ, Zaliznyak texts) live here |
| Frequency, reader-as-a-service, difficulty scorer, reading packs, sandhi, Pāṇini concordance | **kosha** | the data/lookup engines live here |
| SRS, exercise engines, homework, certificates, the learner surface | **Systema-Sanscriticum** (T0) | the **consumer**; receives the last-mile pipeline; **spec-only** in wave-1 (fenced) |
| Metre/audio trainer | **SanskritKaraoke** | recitation surface (audio gap) |
| Paradigm/flashcard browser | **VisualDCS** | fold in, don't rebuild |

Rule: the field spec is centralised in SanskritGrammar; each data/tool lands where its inputs
already live; product integration lands in Systema (T0) and is spec-only until a human reviews it.

## 4. Build-vs-reuse verdict (prior-art checked)

| Piece | Verdict | Why |
|---|---|---|
| Reader-as-a-service | **REUSE** | kosha segmenter + KWIC concordance + reverse-lookup already build it |
| SRS | **REUSE** | Systema "Saraswati" (FSRS) + kosha Anki export exist |
| Paradigm drills | **REUSE + wire** | kosha paradigm engine, SG widgets, csl-inflect, VisualDCS flashcards all exist |
| Frequency/graded vocabulary | **REUSE** | kosha `core_rank` "learn-these-first" is the spine |
| **Difficulty scorer** | **BUILD** | new; feeds RQ1 + reading + SRS; nobody owns it yet |
| **Auto-drill generation + answer verification** | **BUILD** | on top of the Talmud drill bank + Systema engines |
| **Evaluation harness (user study)** | **BUILD** | RQ4; the field's falsifiability backbone |
| **Zaliznyak on-ramp** | **BUILD** (new UI over existing data) | reuses *Очерк*/index/token + Talmud widgets; the *presentation* is new |
| **Last-mile pipeline** | **WIRE** | the pieces exist (kosha ↔ Systema); the connection is the deliverable |

The pattern: almost everything is **reuse or wire**; the genuinely new builds are the **difficulty
scorer**, **drill generation + verification**, the **evaluation harness**, and the **on-ramp
presentation**. That ratio is the point — the field is integration, and its research lives in the
few new pieces plus the measurement.

---

_Dr. Mārcis Gasūns_
