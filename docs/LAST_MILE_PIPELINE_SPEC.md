# Last-mile pipeline — kosha → learner (Systema): the contract spec

_Created: 14-07-2026 · Last updated: 14-07-2026_

Specifies the **"last mile"** [MEGABOOK §14.2](https://github.com/gasyoun/Uprava/blob/main/MEGABOOK.md) flags
as the chain's main unclosed link: how the open kosha data/lookup layer feeds the Tier-0
[Systema-Sanscriticum](https://github.com/gasyoun/Systema-Sanscriticum) learning platform. Wave-1d of the
[digital-Sanskrit-pedagogy field](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md),
handoff [H916](https://github.com/gasyoun/Uprava/blob/main/handoffs/H916-Opus_SanskritGrammar_pedagogy-w1d-last-mile-pipeline_14.07.26.md).
Model: Opus 4.8 (`claude-opus-4-8[1m]`).

> **This is a spec, not a build.** Per the field's straddle-tier fence, wave-1 touches **no Systema
> production code** — the wiring is Wave 2, behind feature flags, after human review. This document is the
> contract the Wave-2 executor implements.

## 1. The integration decision — vendored data-file, not live API

kosha exposes **both** a callable HTTP API (FastAPI, [`app/main.py`](https://github.com/gasyoun/kosha/blob/main/app/main.py),
`127.0.0.1:8000`) **and** a static dataset registry ([`data/manifest/datasets.json`](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json)).
The one integration that **actually ships today** — [`SanskritGlossary.php`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Services/SanskritGlossary.php) —
deliberately chose the **vendored static feed**: it reads a build-time JSON file
([`resources/data/sa_ru_glossary.json`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/resources/data/sa_ru_glossary.json)),
memoizes it (`Cache::rememberForever` keyed by file mtime), and is gated by `config('features.slovar_enrichment')`
(OFF by default). Its feature doc states the rule plainly: **"НЕ живая зависимость от kosha."**

**Ruling for this pipeline (the marked default):** all three hops below use the **vendored-data-file contract**,
matching that proven pattern — kosha (or a sibling) derives a lemma-keyed dataset → a Systema build script rolls it
into a compact keyed JSON in `resources/data/` → Systema vendors it + flag-gates it. The live kosha API stays the
*future* option (needs a CORS allow-list + accepts a runtime dependency Systema currently avoids); it is **not** the
wave-2 path. Rationale: (a) it is the only pattern with a shipped precedent; (b) it survives kosha being offline;
(c) it inherits the OFF-by-default deploy discipline.

## 2. The three hops

Each hop names the **kosha source surface**, the **Systema sink surface**, the **contract artifact**, and the **gap to close**.

### Hop A — Reader-as-a-service (paste text → segmented → click-gloss)

| | |
|---|---|
| **kosha source** | segmenter [`app/segmenter.py`](https://github.com/gasyoun/kosha/blob/main/app/segmenter.py) `segment(slp1)`→`[{text, lemma}]`; the cascade [`reverse_lookup.py`](https://github.com/gasyoun/kosha/blob/main/app/reverse_lookup.py); the embeddable card [`app/word_page.py`](https://github.com/gasyoun/kosha/blob/main/app/word_page.py) `render_word_page(card, include_doc=False)` → a self-contained `word-page` fragment (host-independent, no-JS fallback). API twins: `GET /api/v1/forms/{form}/analyze`, `GET /w/{slp1}`. |
| **Systema sink** | **No paste-text reader exists.** Closest: [`StudentDictionary`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Livewire/StudentDictionary.php) (DB search) and the `slovar` entity pages. A reader is a new Livewire route. |
| **Contract (vendored)** | For a **fixed** text (a graded reading, not arbitrary paste), pre-segment offline and vendor a **reading-pack** artifact (see Hop B's deck format + per-token `lemma_slp1`). Arbitrary paste needs the live API — defer to the API phase. |
| **Gap** | kosha reading-packs are **planned, not built** (UC9, Gītā 1 / Nala 1); the new reader route; a vendored per-text token→lemma+gloss pack. |

### Hop B — Frequency-ordered SRS deck (kosha → Systema Saraswati)

| | |
|---|---|
| **kosha source** | [`data/frequency/lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv) (`rank_all`, `core_rank`, `coverage_pct`) joined to glosses; the Anki serialiser [`ui/src/lib/export.js`](https://github.com/gasyoun/kosha/blob/main/ui/src/lib/export.js) `toAnki` shows the field convention (`front = "देव · iast"`, `back = gloss`) — but only for *session* lookups. **No full-deck export artifact exists yet.** |
| **Systema sink** | Saraswati SRS — [`SrsDeck`/`SrsCard`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Models/SrsCard.php) (schema in `2026_07_07_1300*` migrations). Ingestion precedent: [`SrsSanskritDeckSeeder`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/database/seeders/SrsSanskritDeckSeeder.php) builds system decks from the internal `dictionary_words` table. `srs_decks.course_id`/`lesson_id` are nullable **"Wave 2" binding hooks** already in the schema. |
| **Contract (vendored)** | kosha publishes a manifest dataset `kosha-srs-deck-<level>` → rows `{rank, slp1, deva, iast, gloss}` in **learn-order**; a Systema importer (twin of the seeder) creates one `SrsDeck` (`visibility=system`) + `SrsCard`s whose `fields` JSON = the note-type fields (`devanagari,iast,cyrillic,translation`) **plus** `slp1` + `rank`. |
| **⚠ Gap — order** | `srs_cards` has **no `rank`/`order`/`difficulty` column** — new-card order is implicit (insertion/id). Either **insert in rank order** (cheapest, honours the deck order) or add a nullable `sort_rank` column (cleaner, needs a migration = Systema code → Wave 2, human-reviewed). Recommend insert-in-order for the demo, `sort_rank` column for production. |
| **⚠ Gap — what to rank** | **Do NOT ship raw `rank_all`.** The wave-1a result ([`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md)) is load-bearing here: (1) **strip the function words** — ~46 % of the top-50 frequency lemmas are indeclinables/pronouns learned as grammar, not vocab flashcards; use `core_rank` (which already excludes them) as the deck spine, not `rank_all`; (2) **genre-correct** — DCS frequency over-weights epic/kāvya vocabulary; a beginner deck should down-weight epic-register content words. The deck-builder consumes `core_rank` first, `rank_all` only as a tiebreak among core items. |

### Hop C — Difficulty score → lesson sequencing

| | |
|---|---|
| **kosha source** | **No dedicated difficulty asset.** Compose from `rank_all` + `core_rank` + `coverage_pct` + the query-time evidence band 1–5 ([`app/evidence.py`](https://github.com/gasyoun/kosha/blob/main/app/evidence.py)); the manifest already names a **"Nagari teaching order"** consumer — the existing teaching-order precedent. The *method* is wave-1a's (`build_difficulty_ordering.py`). |
| **Systema sink** | [`Lesson`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Models/Lesson.php) `sort_order` + `block_number`/`block_half` (sequencing); `SrsDeck.lesson_id`/`course_id` (deck↔lesson binding). **Nothing consumes a difficulty score today.** |
| **Contract (vendored)** | kosha publishes `kosha-text-difficulty` → per-text/per-chapter `{text_id, difficulty_score, rare_form_pct, band_profile}`; Systema reads it as advisory metadata to *order* graded readings, never to auto-reorder a human-authored course. |
| **Gap** | the difficulty scorer itself (compose per wave-1a, emit as a manifest dataset); Systema-side it is advisory-only (no schema change needed). |

## 3. Contract artifacts (the deliverable checklist for Wave 2)

**kosha must emit** (each a `datasets.json` row, `tier: public`, keyed by `lemma_slp1`/`text_id`, with a data-statement):
1. `kosha-srs-deck-<level>` — learn-ordered `{rank, slp1, deva, iast, gloss}`, `core_rank`-spined, function-words stripped.
2. `kosha-reading-pack-<text>` — per-token `{surface, lemma_slp1, gloss, freq_band}` for a fixed graded text (closes UC9).
3. `kosha-text-difficulty` — advisory per-text difficulty.

**Systema must add** (Wave 2, flag-gated, human-reviewed):
1. A deck importer (twin of `SrsSanskritDeckSeeder`) reading artifact 1 → `SrsDeck`+`SrsCard`, order preserved.
2. A `features.kosha_srs` / `features.kosha_reader` flag pair (mirror `slovar_enrichment`).
3. (optional, production) a `srs_cards.sort_rank` migration.
4. A reader route consuming artifact 2 (or the live API, later).

## 4. One-rung demo path (proves the pipeline end-to-end, minimal surface)

**Rung B1 — subhāṣita reading.** Public-domain [Indische Sprüche](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json) source (rights-clean), one short verse:

1. kosha: segment the verse (`segment`) → per-pada lemmas; join `lemma_frequency` + gloss → emit a `kosha-reading-pack-subhashita-demo` file (artifact 2).
2. kosha: cut a `kosha-srs-deck-b1-demo` from that pack's content words, `core_rank`-ordered, function-words stripped (artifact 1).
3. Systema: vendor both files to `resources/data/`; the importer builds one system `SrsDeck`; a minimal reader route renders the verse with click-gloss from the pack.
4. **Proof:** a learner opens the verse, taps a word → gloss + frequency band; the same verse's content words appear as a frequency-ordered SRS deck — one rung, end-to-end, **no live dependency, both flags default-OFF.**

## 5. Open questions / caveats (resolve before Wave 2 freezes)

- **`build_sa_ru_glossary.py` is uncommitted** — `SanskritGlossary.php` + the feed's `_meta` reference it, but it is not in the Systema tree (only its output is). The vendoring build-script convention this spec leans on must be located/committed first, or re-established.
- **Rights** — the SRS deck glosses and reading-pack text must be rights-clean (Indische Sprüche + DCS lemmatisation are; in-copyright dictionary glosses are not redistributable). The demo uses public-domain sources only. `/publish-safety-check` before any deck ships.
- **API vs file** — if arbitrary paste-a-verse reading becomes a requirement, the live API phase (CORS allow-list, origin pinning) supersedes the vendored-file path for Hop A only.

## 6. Verification (how Wave 2 proves it)

- Artifacts 1–3 exist as `datasets.json` rows with data-statements; each validates against its keying.
- The importer is idempotent (re-run → no dup decks), order preserved (card `id` order == `rank` order).
- The demo rung renders: verse click-gloss resolves every content token; the deck contains **zero** stripped function words.
- `git diff` of the Wave-2 Systema PR is flag-gated and OFF-by-default; the reader/importer are dead code until the flag flips (mirrors `slovar_enrichment`).

---

_Dr. Mārcis Gasūns_
