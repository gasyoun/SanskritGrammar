_Created: 01-08-2026 · Last updated: 01-08-2026_

# Export schema note — story chapters → kosha reading-pack JSON

**Contract:** the story must eventually ship in the **same pack JSON schema** as every
other reading pack, so the Systema reader stays story-agnostic
([ARCHITECTURE_AKRO_START_CHTENIYA_2026.md](https://github.com/gasyoun/Uprava/blob/main/docs/ARCHITECTURE_AKRO_START_CHTENIYA_2026.md)
§ Data contracts: «Systema must not invent a second schema»). Canonical shape:
[kosha `reading/data/hitopadesa-0.json`](https://github.com/gasyoun/kosha/blob/main/reading/data/hitopadesa-0.json)
= Systema vendored
[`resources/data/kosha_reading_pack_nala_1.json`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/resources/data/kosha_reading_pack_nala_1.json).

## Field mapping (v0 Markdown → pack JSON)

| Pack JSON field | Source in the chapter MD | Note |
|---|---|---|
| `slug` | file name | proposed: `story-start-chteniya-1` … `-5` (one pack per chapter) |
| `title` | chapter title | Devanāgarī + transliteration, e.g. «अयं ग्रामः» |
| `ref` / `locus` | chapter + sentence number | `ch1.s7` style; `sentences[].n` = running index |
| `text_name` | fixed | «Natural-method story „Старт чтения"» |
| `source` | fixed | original composition, SanskritGrammar H2113 tree; license: project-owned (no external text; verse sentence cites `subh_1249` provenance from the kosha pack) |
| `built` | export date | stamp at export time |
| `stats` | computed | sentence + token counts |
| `sentences[].text` | Devanāgarī column | sandhied surface text |
| `sentences[].tokens[].form` | padapāṭha column | unsandhied word forms — **already the token layer**; the sandhied↔padapāṭha diff in the MD is exactly the `form`-vs-surface information the tap-token UI needs |
| `tokens[].lemma` | vocab tables | first-occurrence tables list lemma per form |
| `tokens[].upos` / `morph` | **not yet in MD** | to add at export: run the same tagging pass used for Hitopadeśa-0, then hand-verify (small text) |
| `tokens[].gloss` | — | EN gloss to add at export (RU is primary here — reverse of the DCS packs) |
| `tokens[].gloss_ru` | vocab tables | present for 100 % of lemmas by construction (vs ~94.6 % on Hitopadeśa-0) |
| `tokens[].slp1` | derivable | mechanical from IAST |
| `tokens[].href` / `tier` | derivable | kosha `w/` card links where a card exists |

## Story-specific extension (additive only)

Two optional per-pack fields, ignored by existing readers: `chapter` (1–5) and
`week_target` (`w3a`, `w3b`, `w4`, `w5`) — additive keys, **not** a schema fork.

## Export pipeline (later handoff, not this one)

1. Parse the chapter MD tables (sentence table + vocab tables) → sentence/token skeleton.
2. Morph-tag tokens (reuse the Hitopadeśa-0 tagging path; hand-verify — texts are ≤ 20 sentences).
3. Emit `story-start-chteniya-N.json`; register in
   [kosha `data/manifest/datasets.json`](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json)
   same pass; vendor into Systema under `resources/data/cohort_start_chteniya/` via the
   H2109/H2106 freeze-manifest path.
4. Gate: export only chapters that passed the human editorial visa.

The v0 MD format was designed so this export is mechanical: the padapāṭha line **is**
the token stream, and the sandhi-events table documents every surface↔form divergence.

## Provenance

Fable 5 (`claude-fable-5`), 01-08-2026, executing
[H2113](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2113-Fable_SanskritGrammar_start-chteniya-natural-method-story_01.08.26.md).

_Dr. Mārcis Gasūns_
