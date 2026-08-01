_Created: 01-08-2026 · Last updated: 01-08-2026_

# CURRICULUM — «Старт чтения» classroom weeks W1–W5

**One-page map** for the paid 5-week pilot. Parent plan:
[PLAN_AKRO_START_CHTENIYA_2026.md](https://github.com/gasyoun/Uprava/blob/main/docs/PLAN_AKRO_START_CHTENIYA_2026.md)
· implementation step 1.1 ([H2112](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2112-Fable_SanskritGrammar_start-chteniya-w1w5-curriculum_01.08.26.md)).

> **Name fence.** These are **classroom product weeks** for the Akro-style pilot.
> They are **not** research-pedagogy waves W1–W5 in
> [DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md)
> / SanGram freezes / kosha pedagogy Wave-1 builds. Do not renumber or merge those axes.

## Purpose

Map each live week → **drills** → **reading pack** → **homework**, with **concrete repo paths**
so ORS copy (H2108), Systema deep links (H2106), kosha freeze (H2109), and Karaoke metre
(H2114) share one spine.

## Interim pilot spine

| Role | Choice | Path |
|---|---|---|
| Weeks 3 continuous prose (default) | Hitopadeśa-0 + RU gloss | [kosha `reading/data/hitopadesa-0.json`](https://github.com/gasyoun/kosha/blob/main/reading/data/hitopadesa-0.json) |
| Week 5 literature band (default) | subhāṣita-beginner (106 sayings) | [kosha `data/subhashita/subhashita_beginner_pack.json`](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_beginner_pack.json) |
| Long-term story swap | Natural-method continuous SA+RU | *Not yet* — H2113 scaffold; **does not block** this map |

Textbook ladder context only (not the weekly drill list):
[LEARNER_MATERIALS.md](https://github.com/gasyoun/SanskritGrammar/blob/main/LEARNER_MATERIALS.md)
(Kochergina + Zalizniak *Конспект* as school background).

---

## Master table (week → live → digital → homework)

| Week | Live focus | Digital drills (owned) | Reading pack | Homework (cabinet / between sessions) |
|---:|---|---|---|---|
| **1** | Pronunciation; cabinet onboarding | Devanāgarī recognition + top-50 freq lemmas | *None yet* (script + lemma prep) | Letter quiz + 50-lemma recognition; name-in-Devanāgarī optional |
| **2** | Forms in context | Morphology band-1 (a-stems L1) + sandhi curriculum **L1–3** (ranks 1–10; stretch note → top-23 / ~51% corpus) | *None* (morph/sandhi only) | Morph L1 drills + sandhi L1–3 join recognition |
| **3** | Continuous prose, read aloud | Sandhi join/split drills on live text | **Hitopadeśa-0** (interim) | Read assigned Hitop. opening sentences; hover/tap gloss; sandhi split homework |
| **4** | Oral paraphrase + metre ID | Karaoke **metre quiz only** (3–5 ślokas, no audio) | Carry Hitop. review subset + metre verses | Metre quiz on pinned ślokas; oral Q prep (live-only) |
| **5** | First literature band; next-course ladder | subhāṣita band review / optional story ch. if visa’d | **subhāṣita-beginner** *or* story ch. (if ready) | 5–10 beginner sayings; ladder CTA to next samskrte course |

Every cell below either names a path or is marked **live-only**.

---

## Week 1 — Script + first lemmas

| Cell | Asset | Path / note |
|---|---|---|
| Live | Pronunciation, cabinet tour | **live-only** (teacher Zoom / group) |
| Drill — Devanāgarī quiz | csl-guides letter quiz | [csl-guides `docs/users/devanagari-quiz.mdx`](https://github.com/sanskrit-lexicon/csl-guides/blob/main/docs/users/devanagari-quiz.mdx) · live [devanagari-quiz](https://sanskrit-lexicon.github.io/csl-guides/users/devanagari-quiz) |
| Drill — name → Devanāgarī | csl-guides tool (marathon Day-1 pattern) | [csl-guides `docs/tools/name-in-devanagari.mdx`](https://github.com/sanskrit-lexicon/csl-guides/blob/main/docs/tools/name-in-devanagari.mdx) · Systema wire: [Systema `config/marathon.php`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/config/marathon.php) day1 message + [views `marathon/day1.blade.php`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/resources/views/marathon/day1.blade.php) (pattern reuse only — **not** R20 marathon enrollment) |
| Drill — top-50 lemmas | Vocab curriculum **lesson 1** = exactly 50 lemmas | Data: [kosha `data/frequency/vocab_curriculum.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/vocab_curriculum.tsv) (`lesson=1`) · Page: [kosha `reading/vocabulary/curriculum/`](https://github.com/gasyoun/kosha/blob/main/reading/vocabulary/curriculum/index.html) · Drills: [kosha `reading/vocabulary/drills/`](https://github.com/gasyoun/kosha/blob/main/reading/vocabulary/drills/index.html) · Bank: [kosha `data/frequency/vocab_drills.json`](https://github.com/gasyoun/kosha/blob/main/data/frequency/vocab_drills.json) |
| Pack | — | *none this week* |
| Homework | Cabinet onboarding + 50-lemma pass | Systema `/dvaram` deep links (wired by H2106 against this map) · cohort flag only (no global SRS) |
| Optional SRS seed | Frequency-ordered demo pattern | Systema [resources/data/kosha_srs_deck_b1_demo.json](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/resources/data/kosha_srs_deck_b1_demo.json) pattern; cohort import from pack lemmas later (H2106) |

**Top-50 IAST (vocab L1 head, for teacher glance):** kṛ, vac, mahat, as, rājan, gam, ādi, artha, dharma, ātman, putra, loka, agni, tva, śru, rasa, karman, indra, brū, sthā, jan, rūpa, bala, tri, ratha, pitṛ, ah, phala, guṇa, manas, prāp, tā, puruṣa, kāma, nara, śata, ṛṣi, bahu, doṣa, jñā, yoga, bhagavant, muni, tapas, go, grah, bhūta, sahasra, parama, man.

---

## Week 2 — Morphology + sandhi top rules

| Cell | Asset | Path / note |
|---|---|---|
| Live | Forms in sentential context | **live-only** |
| Drill — morph band-1 | Morphology curriculum **lesson 1** (107 a-stem lemmas) | Data: [kosha `data/morphology/morphology_curriculum.tsv`](https://github.com/gasyoun/kosha/blob/main/data/morphology/morphology_curriculum.tsv) (`lesson=1`, bucket `a-stems`) · Weights: [kosha `data/morphology/drill_weights.json`](https://github.com/gasyoun/kosha/blob/main/data/morphology/drill_weights.json) · Page: [kosha `reading/morphology/curriculum/`](https://github.com/gasyoun/kosha/blob/main/reading/morphology/curriculum/index.html) · Drills: [kosha `reading/morphology/drills/`](https://github.com/gasyoun/kosha/blob/main/reading/morphology/drills/index.html) |
| Drill — sandhi L1–3 (freeze pin) | Graded sandhi curriculum lessons 1–3 = ranks 1–10, cum. **~31.9%** corpus mass | Data: [kosha `data/sandhi/sandhi_curriculum.tsv`](https://github.com/gasyoun/kosha/blob/main/data/sandhi/sandhi_curriculum.tsv) · Page: [kosha `reading/sandhi/curriculum/`](https://github.com/gasyoun/kosha/blob/main/reading/sandhi/curriculum/index.html) · Drills JSON: [kosha `data/sandhi/sandhi_drills.json`](https://github.com/gasyoun/kosha/blob/main/data/sandhi/sandhi_drills.json) · Page: [kosha `reading/sandhi/drills/`](https://github.com/gasyoun/kosha/blob/main/reading/sandhi/drills/index.html) |
| Stretch (live, optional) | Top-23 rules ≈ **51.15%** cumulative (roadmap Akro analogue) | Same TSV ranks 1–23 (crosses into curriculum lesson 5) — **do not** expand H2109 freeze past L1–3 without a new pin |
| Pack | — | *none this week* |
| Homework | Morph L1 MCQ + sandhi L1–3 recognition | Cabinet links to morph/sandhi drill pages; cohort entitlement (H2105/H2106) |

**Sandhi L1–3 rule list (teacher cheat-sheet):**

| L | Rank | Rule (surface) | Category | Cum. % |
|---:|---:|---|---|---:|
| 1 | 1 | a a → ā | vowel coalescence | 6.22 |
| 1 | 2 | m p → ṃ p | anusvāra / nasal | 10.05 |
| 2 | 3–6 | m s/t/v/c → ṃ … | anusvāra / nasal | 22.36 |
| 3 | 7–9 | m k/m/n → ṃ … | anusvāra / nasal | 28.66 |
| 3 | 10 | ḥ t → s t | visarga | 31.87 |

---

## Week 3 — Continuous prose (Hitopadeśa-0 interim)

| Cell | Asset | Path / note |
|---|---|---|
| Live | Read-aloud continuous prose; comprehension Q | **live-only** |
| Pack (canonical freeze) | Hitopadeśa Prastāvikā opening | JSON: [kosha `reading/data/hitopadesa-0.json`](https://github.com/gasyoun/kosha/blob/main/reading/data/hitopadesa-0.json) · JS sibling: [hitopadesa-0.js](https://github.com/gasyoun/kosha/blob/main/reading/data/hitopadesa-0.js) · Reader: [kosha `reading/index.html#hitopadesa-0`](https://github.com/gasyoun/kosha/blob/main/reading/index.html) · Stats: 125 sentences / 900 tokens; `gloss_ru` present (~94.6% per [RU_GLOSS_COVERAGE.md](https://github.com/gasyoun/kosha/blob/main/reading/RU_GLOSS_COVERAGE.md)) · License note: DCS CC BY 4.0 (source field in JSON) |
| Systema embed (post H2106/H2110) | Vendored freeze under cohort dir | Target: `Systema-Sanscriticum/resources/data/cohort_start_chteniya/` (created by H2109→H2106; Nala pattern: [kosha_reading_pack_nala_1.json](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/resources/data/kosha_reading_pack_nala_1.json)) |
| Drill — sandhi join/split | Sandhi drills over continuous text | [kosha `reading/sandhi/drills/`](https://github.com/gasyoun/kosha/blob/main/reading/sandhi/drills/index.html) · corpus Hitop. sandhi events: [kosha `data/sandhi/hitopadesa_sandhi.tsv`](https://github.com/gasyoun/kosha/blob/main/data/sandhi/hitopadesa_sandhi.tsv) |
| Homework | Assigned Hitop. loci + split practice | Deep link to pack slug `hitopadesa-0` in cabinet; SRS lemmas from pack (cohort flag) |
| Story swap (later) | Natural-method chapters | H2113 tree under `docs/NATURAL_METHOD_STORY_START_CHTENIYA/` — **pilot default stays Hitopadeśa** until human visa |

---

## Week 4 — Oral + metre-only residual

| Cell | Asset | Path / note |
|---|---|---|
| Live | Oral paraphrase / questions on week-3 text | **live-only** (teacher voice = audio v1 per PLAN D4) |
| Metre pack (H2114 residual) | 3–5 existing verses, `has_audio: false`, **metre quiz only** | Karaoke index: [SanskritKaraoke `verses/index.json`](https://github.com/gasyoun/SanskritKaraoke/blob/main/verses/index.json) · Data dir: [verses/data/](https://github.com/gasyoun/SanskritKaraoke/tree/main/verses/data) |
| **Pinned W4 set (default)** | BhG 2.47–49 + 2 beginner subhāṣita already in Karaoke | `bhg_2_47` · `bhg_2_48` · `bhg_2_49` · `subh_1249` (*udyamena…*, also #2 in beginner band) · `subh_6087` (*vidyā dadāti vinayaṃ…*) — all five files under [verses/data/](https://github.com/gasyoun/SanskritKaraoke/tree/main/verses/data); `has_audio: false` |
| Student path | Wave diagram + **meter quiz only** | Fence: **no** `align_chapter` / render / audio-drop pipeline this pilot (PLAN D8 / H2114) |
| Carry pack | Hitop. review subset | Same week-3 pack path |
| Homework | Metre ID quiz on the five IDs + oral prep notes | Karaoke learner path (post H2114 wire); live oral is **live-only** |

---

## Week 5 — First literature band + ladder

| Cell | Asset | Path / note |
|---|---|---|
| Live | Joint reading; next-course ladder talk | **live-only** |
| Pack (default) | subhāṣita-beginner band | Pack: [kosha `data/subhashita/subhashita_beginner_pack.json`](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_beginner_pack.json) (106 sayings; `gloss_ru` ~85.3%) · Band TSV: [beginner_band.tsv](https://github.com/gasyoun/kosha/blob/main/data/subhashita/beginner_band.tsv) · Curation: [CURATION_NOTES.md](https://github.com/gasyoun/kosha/blob/main/data/subhashita/CURATION_NOTES.md) · Reader page: [kosha `reading/subhashita/`](https://github.com/gasyoun/kosha/blob/main/reading/subhashita/index.html) · Optional Anki: [subhashita_beginner_anki.apkg](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_beginner_anki.apkg) |
| Alt pack (if story ready) | Natural-method chapter export | H2113 → pack JSON schema per [ARCHITECTURE_AKRO…](https://github.com/gasyoun/Uprava/blob/main/docs/ARCHITECTURE_AKRO_START_CHTENIYA_2026.md); human visa before live cohort |
| Alt stretch (not required) | Nala-1 start | [kosha `reading/data/nala-1.json`](https://github.com/gasyoun/kosha/blob/main/reading/data/nala-1.json) — optional ladder demo only |
| Homework | 5–10 beginner sayings + ladder CTA | ORS/Systema next-course UTM (`utm_campaign=start-chteniya`); no invented RUB/dates |

---

## Freeze set for H2109 (derived from this map)

Pin these sources into `kosha/data/cohort_start_chteniya/` (or equivalent):

1. [reading/data/hitopadesa-0.json](https://github.com/gasyoun/kosha/blob/main/reading/data/hitopadesa-0.json)
2. [data/subhashita/subhashita_beginner_pack.json](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_beginner_pack.json)
3. Sandhi curriculum **L1–3** subset of [data/sandhi/sandhi_curriculum.tsv](https://github.com/gasyoun/kosha/blob/main/data/sandhi/sandhi_curriculum.tsv) + matching drills from [data/sandhi/sandhi_drills.json](https://github.com/gasyoun/kosha/blob/main/data/sandhi/sandhi_drills.json)
4. Optional lemma TSV: vocab L1 50 rows from [data/frequency/vocab_curriculum.tsv](https://github.com/gasyoun/kosha/blob/main/data/frequency/vocab_curriculum.tsv) + Hitop. pack lemmas for SRS

Karaoke W4 IDs are **not** kosha freeze — they stay in SanskritKaraoke (H2114).

---

## Systema deep-link skeleton (for H2106)

| Week | Suggested lesson slug key | Primary digital target |
|---:|---|---|
| 1 | `start_chteniya_w1_script_vocab` | csl-guides Devanāgarī quiz + kosha vocab L1 drills |
| 2 | `start_chteniya_w2_morph_sandhi` | morph L1 drills + sandhi L1–3 curriculum/drills |
| 3 | `start_chteniya_w3_hitopadesa_0` | pack `hitopadesa-0` + sandhi join/split |
| 4 | `start_chteniya_w4_metre` | Karaoke IDs `bhg_2_47`…`subh_6087` metre quiz |
| 5 | `start_chteniya_w5_subhashita` | pack `subhashita-beginner` + ladder CTA |

Gate all five behind cohort entitlement `start_chteniya_cohort` (name final in H2105) — **never** `SRS_ENABLED=true` global.

---

## Non-goals (this sheet)

- Second LMS / second sandhi engine / second dictionary stack
- Professional audio library or TTS (audio v1 = live teacher)
- CommentaryStrategies apparatus in the 5-week funnel
- Global `SRS_ENABLED` flip
- Waiting on Gītā-from-DCS isolation or natural-method story before pilot
- Confusing **research** pedagogy W1–W5 with these **classroom** weeks
- Inventing public RUB prices or cohort dates (human ops)
- Executing sibling handoffs from this map alone

---

## Downstream consumers

| Handoff | Uses this map for |
|---|---|
| [H2108](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2108-Fable_ORS-FAQ_start-chteniya-landing_01.08.26.md) | Landing arc copy (week promises) |
| [H2105](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2105-Sonnet_Systema-Sanscriticum_start-chteniya-cohort-funnel_01.08.26.md) | Lesson skeleton / entitlement scope |
| [H2109](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2109-Sonnet_kosha_start-chteniya-pack-freeze_01.08.26.md) | Freeze file list |
| [H2106](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2106-Sonnet_Systema-Sanscriticum_start-chteniya-pack-wire-srs_01.08.26.md) | `/dvaram` deep links per week |
| [H2114](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2114-Sonnet_SanskritKaraoke_start-chteniya-week4-metre_01.08.26.md) | W4 pinned verse IDs |
| [H2113](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2113-Fable_SanskritGrammar_start-chteniya-natural-method-story_01.08.26.md) | Story swap target for W3–W5 |

## Acceptance (H2112)

| Criterion | Status |
|---|---|
| One committed sheet `docs/CURRICULUM_START_CHTENIYA_W1_W5.md` | this file |
| Every week cell has repo path or **live-only** | ✅ W1–W5 sections |
| Own-data prior-art only (no rebuilt packs) | ✅ kosha / Karaoke / csl-guides / Systema paths cited |
| Research W fence | ✅ opening callout |

## Provenance

Authored Grok 4.5 (`grok-4.5`) executing H2112 (filename tier Fable 5) on 01-08-2026 from IMPLEMENTATION step 1.1 + live path census. Dual-run residual for intended Fable compare: see Uprava handoffs residual if minted.

_Dr. Mārcis Gasūns_
