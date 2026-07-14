# Last-mile pipeline spec — kosha → learner (wave-1d)

_Created: 14-07-2026 · Last updated: 14-07-2026_

The **integration** deliverable of the [digital-Sanskrit-pedagogy field](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md):
a spec for the one **unclosed hop** in the value chain — kosha's open data/lookup layer → the
learner surface (Systema-Sanscriticum). Wave-1 item **W1d**
([H916](https://github.com/gasyoun/Uprava/blob/main/handoffs/H916-Opus_SanskritGrammar_pedagogy-w1d-last-mile-pipeline_14.07.26.md)).
Plan cover [here](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md);
component boundaries [here](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_DIGITAL_SANSKRIT_PEDAGOGY.md).

> **This is a spec, not a build.** Per the wave-1 fence it names inputs/outputs of each hop and a
> demo path; it changes **no Systema and no kosha production code**. The wiring it specifies is
> Wave-2 work, gated on human review. See [§7](#7-fence--gates).

## 1. What "the last mile" is

The ecosystem has two *proven* end-to-end chains (MEGABOOK
[§14.2](https://github.com/gasyoun/Uprava/blob/main/MEGABOOK.md)): dictionary → kosha → Systema, and
corpus → Sangram → lesson. Both are `live` **up to their final hop**, and both stop at the same place —
the hop **into the learner surface** is `queued`, a dashed edge on the value map. Everything upstream
(44 dictionaries collapsed, a 83k-lemma frequency layer, a segmenter, an FSRS engine) already exists;
what is missing is the **connection** that turns a decade of lexical/corpus plumbing into something a
student touches. This spec defines that connection for the vocabulary/reading path.

The last mile is **wire, not build** — with exactly one genuinely new piece (the difficulty scorer,
[§3, Hop B](#hop-b--difficulty-scorer--graded-vocabulary-the-one-new-build)). That ratio is the point:
the field is integration, and naming the contract precisely is most of the work.

## 2. The pipeline — three hops, open layer → product

```
 kosha (open data / lookup)                          Systema-Sanscriticum (product, T0)
 ─────────────────────────                           ─────────────────────────────────
  Hop A  reader-as-a-service   ──segment+gloss──▶     click-gloss surface (reading)
         /api/v1/.../analyze                          "one clean answer" (G3)

  Hop B  difficulty scorer     ──graded order──▶      graded vocabulary sequence
         (NEW · over freq layer)                      (which lemmas, in what order)

  Hop C  frequency-ordered     ──deck feed──────▶     Saraswati FSRS system deck
         SRS deck export                              bound to a course unit
```

Each hop carries a **typed relation** (per the source ontology: *generates* · *populates*), a
**producer artifact**, a **transport**, and a **consumer surface**. The contract is [§3](#3-the-koshasystema-contract-the-deliverable);
a single rung walked end-to-end is [§4](#4-one-rung-demo-path-b1-subhāṣita).

### Hop A — reader-as-a-service (reuse)

Take running Sanskrit text and return segmented tokens, each with a lemma and a collapsed gloss, so a
reader can tap any word.

- **Producer (kosha, live):** `GET /api/v1/forms/{form}/analyze` — [`app/main.py`](https://github.com/gasyoun/kosha/blob/main/app/main.py) → [`app/reverse_lookup.py`](https://github.com/gasyoun/kosha/blob/main/app/reverse_lookup.py) `analyze()`; sandhi/compound splitting in [`app/segmenter.py`](https://github.com/gasyoun/kosha/blob/main/app/segmenter.py) `segment()` (wraps vidyut-cheda). Static per-lemma cards for offline use: [`scripts/build_static_cache.py`](https://github.com/gasyoun/kosha/blob/main/scripts/build_static_cache.py) → `docs/cards/<token>.json`.
- **Output shape:** JSON with `segments[]` (`{text, text_iast, vidyut_lemma, lemmas[]}`) and a unified `lemmas[]` (`{lemma_slp1, lemma_iast, has_entry, resolved_by[], sources[]}`), where `has_entry` marks a real dictionary headword.
- **Consumer (Systema):** the reading/click-gloss surface. The **"one clean answer" collapse (G3)** in the [pedagogy index](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/docs/SANSKRIT_HUB_ASSET_PEDAGOGY_INDEX.md) — MW+PWG+AP90 merged into a single graded gloss for a B1–B2 learner who does not want 44 raw entries.

### Hop B — difficulty scorer → graded vocabulary (the one new build)

Turn "which lemmas, in what order" from an intuition into a committed, graded list.

- **Producer input (kosha, live):** the frequency layer [`data/frequency/lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv) — 83,277 rows, 8 columns; the load-bearing ones are `core_rank` (Leonchenko **"learn-these-first"** order, 7,120 lemmas), `rank_all` (DCS token frequency, full corpus), and `coverage_pct` (per-lemma coverage weight). Manifest id `kosha-lemma-frequency`, release `data-v0.1.0`. **LEFT-JOIN this; never re-derive frequency ordering.**
- **The new artifact (BUILD):** a **difficulty score** per lemma. It does **not** exist in kosha today (the frequency layer has no `difficulty`/`grade` column, and no scorer script exists) — the [W1a result](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md) *measured the method*, it did not ship a reusable scorer. Per the [architecture](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_DIGITAL_SANSKRIT_PEDAGOGY.md) component boundary, the scorer **lands in kosha** as a new column/sidecar on the frequency layer.
- **The scoring contract (fixed by W1a, non-negotiable):** a graded learning order is **not** raw `rank_all`. W1a proved that the curated `core_rank` tracks frequency closely (τ=0.89) *but* the pedagogical work is two corrections raw frequency cannot supply:
  1. **Function-word exclusion** — the top ~46 % of high-frequency lemmas (`ca`, `tu`, `api`, `iti`, `na`, `eva`; `tad`, `idam`, `sa`, `yad`…) are particles/pronouns acquired **structurally through grammar**, not drilled as vocabulary. Strip them from the deck.
  2. **Genre correction** — DCS frequency is epic/kāvya-weighted, so it over-ranks that register's content words (`vara`, `vīra`, `rakta`). Genre-weight, or accept the bias explicitly.
  Sequence **within** the grammar-topic spine, not against it (textbooks agree with each other τ≈0.83 on a non-frequency order). Output: an ordered, function-word-stripped, graded lemma list keyed on `lemma_slp1`.
- **Consumer (Systema):** the **frequency layer E26** row of the pedagogy index — "frequency-ordered SRS decks: learn the 2,000 most frequent lemmas in corpus order — the single highest-leverage vocabulary path. Also the input to difficulty scoring." This spec makes that row executable.

### Hop C — frequency-ordered SRS deck → course unit (wire)

Ship the graded list as a deck the FSRS engine can schedule, bound to a course unit.

- **Producer (kosha, live primitive):** the deck serialiser [`ui/src/lib/export.js`](https://github.com/gasyoun/kosha/blob/main/ui/src/lib/export.js) — `toCsv(rows)` (header `slp1,iast,devanagari,gloss,dicts`) and `toAnki(rows)` (2-field TSV: front `<deva> · <iast>`, back `gloss`), over rows `{slp1, iast, deva, gloss, dicts}`. Today it is **session-scoped** (a reader's own lookups); the wire promotes it to a **corpus-wide, difficulty-ordered** batch export.
- **Consumer (Systema, live engine):** the **"Saraswati" FSRS** trainer — [`app/Services/Srs/`](https://github.com/gasyoun/Systema-Sanscriticum/tree/main/app/Services/Srs) (`Fsrs.php`, `ReviewService.php`) over the `srs_note_types` / `srs_decks` / `srs_cards` model, gated by `config('srs.enabled')` (default on since H447; pilot Aug 2026). A `system` deck (`srs_decks.user_id = NULL`) is exactly the target.
- **Transport:** the import contract in [§3](#3-the-koshasystema-contract-the-deliverable) — the existing `srs:import-memrise` manifest+CSV surface, which is not Memrise-specific.

## 3. The kosha↔Systema contract (the deliverable)

Three transport patterns already ship in production; **the last mile reuses them verbatim and invents
nothing.** The rule (from the proven `sa_ru_glossary` precedent): **upstream builds a derived file →
the file is committed under Systema `resources/data/` (or handed to an import command) → a flag-gated
consumer reads it, with the cache keyed on file mtime so re-vendoring auto-refreshes.** No runtime
cross-repo dependency, ever.

| # | Pattern | Producer artifact (kosha) | Format | Transport | Consumer surface (Systema) | Status |
|---|---|---|---|---|---|---|
| **V** | Vendored static JSON feed | collapsed gloss / frequency slice | one `*.json` file `{_meta, entries:{key:{…}}}`, key = normalised IAST | commit under [`resources/data/`](https://github.com/gasyoun/Systema-Sanscriticum/tree/main/resources/data); flag-gated `App\Services` reader; `Cache::rememberForever` keyed on `md5(path)+filemtime` | reading/gloss enrichment (G3) — the proven [`SanskritGlossary.php`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Services/SanskritGlossary.php) path | **proven, live** |
| **D** | Deck import command | difficulty-ordered lemma deck | a **directory**: `manifest.json` (`course_id, course_name, source_url, language, columns{field→CSV header}, levels[]`) + one CSV per level | `php artisan srs:import-memrise <dir>` ([`ImportMemriseSrsDeck.php`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Console/Commands/ImportMemriseSrsDeck.php)); idempotent, `--dry-run` | builds `SrsNoteType` → system `SrsDeck` → `SrsCard`; card fields `devanagari/iast/cyrillic/translation` (+ `alt_answers`) | **proven, live** |
| **S** | System-deck seeder | (queries the vendored slice) | PHP seeder cloning [`SrsSanskritDeckSeeder.php`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/database/seeders/SrsSanskritDeckSeeder.php) | `db:seed --class=...` | a `system` `SrsDeck` built from filtered/ordered `DictionaryWord` rows | **proven, live** |

**Contract choice per hop:**
- **Hop A gloss (G3)** → **Pattern V.** kosha emits a collapsed-gloss JSON keyed on normalised IAST (mirroring `SanskritGlossary::normalizeKey()` / the upstream `norm_key()`), Systema vendors it exactly as `sa_ru_glossary.json` is vendored.
- **Hop B → Hop C deck** → **Pattern D** is the primary contract (its `columns` map makes it robust to kosha's own headers — nothing in it is Memrise-specific). **Pattern S** is the alternative when the deck should be derived in-DB from `DictionaryWord` rather than shipped as CSV.
- **Field mapping (kosha `export.js` row → Systema card fields):**

  | kosha row field | Systema card field | note |
  |---|---|---|
  | `deva` | `devanagari` | |
  | `iast` | `iast` | also the join/dedup key (priority `iast > devanagari > cyrillic`) |
  | — | `cyrillic` | optional; Systema's A0 Cyrillic-only track — blank if kosha does not supply |
  | `gloss` | `translation` | the G3 collapsed gloss |
  | (difficulty rank) | manifest `levels[]` ordering | Hop B's graded order becomes the level/sequence, **not** a card field |

The **inputs/outputs of every hop are named** (the acceptance bar): Hop A in = text, out = `segments[]`+`lemmas[]`; Hop B in = `lemma_frequency.tsv` (`core_rank`/`rank_all`/`coverage_pct`), out = ordered function-word-stripped lemma list; Hop C in = that list + glosses, out = `manifest.json`+CSVs (Pattern D) or a vendored JSON (Pattern S) → an FSRS system deck.

## 4. One-rung demo path (B1 subhāṣita)

The minimal integration that demonstrates a single rung end-to-end — **B1 subhāṣita reading → deck** —
chosen because every input already exists (Indische Sprüche, 7,537 subhāṣitas; the matrix marks B1
subhāṣita reading and B1 vocabulary/SRS both asset-rich). Walked as data:

1. **Pick a rung + text.** B1, one subhāṣita line (e.g. *vidyā dadāti vinayaṃ…*). Source: Indische Sprüche.
2. **Segment (Hop A).** `GET /api/v1/forms/vidyA/analyze?in=slp1` → `segments[]` + `lemmas[]`; each content lemma carries `lemma_slp1`, `lemma_iast`, `has_entry=true`.
3. **Click-gloss (Hop A, G3).** For each `lemma_slp1`, look up the collapsed one-clean-answer gloss (Pattern V feed) → `vidyā` → "knowledge", `vinaya` → "discipline, humility". Function words (`ca`, if present) are glossed for reading but **flagged non-drillable**.
4. **Grade + order (Hop B).** Join the rung's content lemmas to `lemma_frequency.tsv`; drop function words; order by the difficulty score (from `core_rank`, genre-aware). The subhāṣita's ~6–8 content lemmas become an ordered mini-set.
5. **Export (Hop C).** Emit a `manifest.json` (`course_id: subhashita-b1`, `language: sa`, `columns:{devanagari, iast, translation}`, `levels:[{index:1, name:"Subhāṣita 1", file:"level1.csv"}]`) + `level1.csv` — one row per content lemma, fields from the `export.js` mapping in [§3](#3-the-koshasystema-contract-the-deliverable).
6. **Import (Systema).** `php artisan srs:import-memrise <dir> --dry-run` then live → a `system` `SrsDeck` "Subhāṣita 1 (B1)" of `SrsCard`s the Saraswati FSRS engine schedules.
7. **(Wave-2) bind to a unit.** Set `srs_decks.lesson_id` to the B1 reading lesson — the `nullable` link the migrations already flagged "во Wave 2". **Spec stops here; the binding is not built in wave-1.**

Result: one subhāṣita, read with tap-gloss, becomes a graded, frequency-ordered, spaced-repetition
deck inside the product — every hop exercised, nothing new built except the Hop B ordering.

## 5. Build-vs-reuse ledger

| Hop | Verdict | What exists | What the wire adds |
|---|---|---|---|
| A reader/gloss | **REUSE** | `/analyze` + segmenter + static cards; G3 collapse spec'd | a vendored collapsed-gloss feed (Pattern V) |
| B difficulty scorer | **BUILD** (the only new build) | `lemma_frequency.tsv` (`core_rank`/`rank_all`); W1a *method* | a difficulty score column/sidecar in kosha, per the W1a contract |
| C SRS deck | **WIRE** | `export.js` (session), Saraswati FSRS, `srs:import-memrise`, seeder | a corpus-wide difficulty-ordered batch export → Pattern D/S |

## 6. What Wave-2 builds (seeds for the next handoffs)

Spec-only now; each is a candidate Wave-2 handoff, gated on human review of this spec:

1. **kosha difficulty scorer** — new column/sidecar on `lemma_frequency.tsv` implementing the [§2 Hop B](#hop-b--difficulty-scorer--graded-vocabulary-the-one-new-build) contract; the field's one genuinely new engine.
2. **kosha batch deck exporter** — promote `export.js` from session-scoped to a corpus-wide, difficulty-ordered emitter producing a Pattern-D directory (or Pattern-V JSON).
3. **kosha collapsed-gloss feed (G3)** — emit the one-clean-answer JSON keyed on normalised IAST for Pattern V.
4. **Systema deck↔lesson binding** — populate `srs_decks.course_id`/`lesson_id` (the "Wave 2" columns) so a deck attaches to a course unit.
5. **(later) typing/cloze exercise modes** — only `alt_answers` plumbing is pre-staged today; the matching/cloze/typing engines are absent.

## 7. Fence & gates

- **Spec-only.** This wave changes **no Systema and no kosha production code** — the deliverable is this doc (+ its metadoc). `git diff` for the SanskritGrammar PR touches only the spec and its metadoc; zero code in any repo. (Verification W1d: "git diff touches only the spec doc; contract section names inputs/outputs of each hop.")
- **Systema straddle-tier fence.** Systema is a T0 **consumer**; wave-1 does not modify it. The wiring in [§6](#6-what-wave-2-builds-seeds-for-the-next-handoffs) is Wave-2, after a human reviews this contract.
- **No new public surface, no rights-gated bulk.** Nothing here enables Pages/visibility or publishes grey corpus; any such step later goes through [`/publish-safety-check`](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md). The DCS-derived frequency layer is already released (`data-v0.1.0`); a vendored gloss feed inherits its rights and must be re-checked at build time.
- **Provenance.** Every vendored file carries a `_meta` block (builder, source repo/path, date, freq floor) exactly as `sa_ru_glossary.json` does — the contract is auditable, not just functional.

## 8. Open questions (marked defaults logged, per the autonomy contract)

- **Where the difficulty score lives** — default: a **new column/sidecar in kosha** on `lemma_frequency.tsv` (architecture puts the scorer in kosha). Alternative: a SanskritGrammar-side derived TSV. *Logged; Wave-2 decides at build.*
- **Primary deck transport** — default: **Pattern D** (`srs:import-memrise` manifest+CSV) for its data-driven `columns` map. Pattern S (seeder) if the deck is better derived in-DB. *Logged.*
- **`cyrillic` field source** — kosha `export.js` emits no Cyrillic; default: leave blank (Systema's A0 track can populate later). *Logged.*
- **Genre-weighting concretisation** — W1a argues the genre bias but does not yet quantify it against a register-balanced count; the scorer may ship with the bias documented rather than corrected. *Logged; ties to RQ1.*

---

_Dr. Mārcis Gasūns_
