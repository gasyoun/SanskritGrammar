_Created: 01-08-2026 · Last updated: 26-08-2026_

# Natural-method story — «Старт чтения» long-term spine (v0 scaffold)

> ⚠️ **Draft status — NOT cleared for a live cohort.** Chapter prose is agent-drafted
> (Fable 5 `claude-fable-5`) and **requires a human editorial visa** before any paid
> student sees it (PLAN D7). Until that visa, the pilot's weeks 3–5 run on the interim
> spine (Hitopadeśa-0 + subhāṣita-beginner) — see «Interim vs final spine» below.

Parent plan: [PLAN_AKRO_START_CHTENIYA_2026.md](https://github.com/gasyoun/Uprava/blob/main/docs/PLAN_AKRO_START_CHTENIYA_2026.md)
· architecture: [ARCHITECTURE_AKRO_START_CHTENIYA_2026.md](https://github.com/gasyoun/Uprava/blob/main/docs/ARCHITECTURE_AKRO_START_CHTENIYA_2026.md)
· handoff: [H2113](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2113-Fable_SanskritGrammar_start-chteniya-natural-method-story_01.08.26.md)
· classroom map: [CURRICULUM_START_CHTENIYA_W1_W5.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/CURRICULUM_START_CHTENIYA_W1_W5.md).

## What this is

A **custom natural-method story** in graded continuous Sanskrit with Russian gloss —
the strategic differentiator of the «Старт чтения» product (PLAN D2). Method model:
continuous original prose whose every sentence is comprehensible from context plus a
strict per-chapter vocabulary budget (the *Lingua Latina per se illustrata* shape,
applied to Sanskrit with kosha's frequency curriculum as the budget source). All prose
here is **original composition** — no Kochergina or any textbook reprint (rights fence
in the handoff); the single embedded verse is a traditional subhāṣita already owned in
the [kosha beginner pack](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_beginner_pack.json).

## Files

| File | Content |
|---|---|
| [CHAPTER_1_AYAM_GRAMAH.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/CHAPTER_1_AYAM_GRAMAH.md) | Ch. 1 «अयं ग्रामः» — v0 draft (SA + RU) |
| [CHAPTER_2_GURUS_CA_SISYAS_CA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/CHAPTER_2_GURUS_CA_SISYAS_CA.md) | Ch. 2 «गुरुश्च शिष्यश्च» — v0 draft (SA + RU) |
| [CHAPTER_3_RAJA_GRAMAM_AGACCHATI.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/CHAPTER_3_RAJA_GRAMAM_AGACCHATI.md) | Ch. 3 «राजा ग्रामम् आगच्छति» — v0 draft (SA + RU) |
| [CHAPTER_4_SLOKAH.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/CHAPTER_4_SLOKAH.md) | Ch. 4 «श्लोकाः» — v0 draft (SA + RU; W4 metre verses `subh_6087` · `bhg_2_47` · `bhg_2_48`) |
| [CHAPTER_5_SUBHASITANI.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/CHAPTER_5_SUBHASITANI.md) | Ch. 5 «सुभाषितानि» — v0 draft (SA + RU; pack verses `subh_2366` · `subh_3371` · `subh_7583`, ladder ending) |
| [VOCAB_BUDGET_DIFFICULTY_TARGETS.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/VOCAB_BUDGET_DIFFICULTY_TARGETS.md) | Per-chapter vocab budget + difficulty targets (the control table) |
| [EXPORT_PACK_JSON_SCHEMA_NOTE.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/EXPORT_PACK_JSON_SCHEMA_NOTE.md) | How chapters export to the kosha reading-pack JSON so the Systema reader stays story-agnostic |

## Syllabus (5 chapters, all drafted v0)

| Ch. | Title | Swap target (classroom week) | Status |
|---:|---|---|---|
| 1 | अयं ग्रामः — village, family, first sentences | W3 first half | ✅ v0 draft |
| 2 | गुरुश्च शिष्यश्च — teacher and pupil in the forest | W3 second half | ✅ v0 draft |
| 3 | राजा ग्रामम् आगच्छति — the king's visit; the verse | W4–5 bridge | ✅ v0 draft |
| 4 | श्लोकाः — metre chapter: anuṣṭubh counted in-story, gerund *-tvā*, three W4 Karaoke verses | W4 | ✅ v0 draft (H3493) |
| 5 | सुभाषितानि — yad–tad correlative, three beginner-pack verses, ladder ending on *paṭha putra* | W5 | ✅ v0 draft (H3493) |

Difficulty targets and the lemma budget per chapter are locked in
[VOCAB_BUDGET_DIFFICULTY_TARGETS.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/VOCAB_BUDGET_DIFFICULTY_TARGETS.md) —
edit the budget first, prose second.

## Interim vs final spine

| Slot | Interim pilot (default, live now-path) | Final spine (this tree, after visa) |
|---|---|---|
| W3 continuous prose | [kosha `reading/data/hitopadesa-0.json`](https://github.com/gasyoun/kosha/blob/main/reading/data/hitopadesa-0.json) | Chapters 1–2 |
| W4 carry text + metre | Hitopadeśa review subset + Karaoke metre IDs | Chapter 3 (quotes the same `subh_1249` verse the W4 metre quiz drills) |
| W5 literature band | [kosha `subhashita_beginner_pack.json`](https://github.com/gasyoun/kosha/blob/main/data/subhashita/subhashita_beginner_pack.json) | Chapters 4–5 (v0 drafted; ch. 4 quotes the W4 metre set, ch. 5 the pack) |

**The pilot does not wait on this story** (PLAN D3, IMPLEMENTATION dependency graph:
H2113 «does not block pilot wire»). The swap happens per-slot, only after the human
visa, and only by replacing pack slugs — the Systema reader is story-agnostic by the
export contract in
[EXPORT_PACK_JSON_SCHEMA_NOTE.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/EXPORT_PACK_JSON_SCHEMA_NOTE.md).

## Conventions (v0)

- Every sentence carries four layers: Devanāgarī (sandhied) · IAST (sandhied) ·
  padapāṭha (word-split, unsandhied) · Russian translation. New lemmas are glossed at
  first occurrence and recycled thereafter — RU gloss register follows the school's
  existing pack glosses (`gloss_ru` in kosha packs), not academic apparatus style.
- **Sandhi exposure is graded against the classroom sandhi curriculum L1–3**
  ([kosha `data/sandhi/sandhi_curriculum.tsv`](https://github.com/gasyoun/kosha/blob/main/data/sandhi/sandhi_curriculum.tsv),
  ranks 1–10). Each chapter lists its sandhi events; events beyond L1–3 (chiefly
  visarga changes before voiced sounds) are marked **†** and resolved in the padapāṭha
  line, so the text stays honest Sanskrit while the drill burden stays inside what
  weeks 2–3 teach.
- **Quotation boundaries are pausa:** no sandhi is applied across the «…» marks or
  into the following *iti* (so «…kaḥ» iti, not *ka iti*; «…vasāmi» iti, not
  *vasāmīti*). Standard learner-edition convention; strict-sandhi forms arrive with
  the week-4 metre material.
- v0 is Markdown tables (IMPLEMENTATION step 1.6 explicitly allows this); the pack-JSON
  export is a later mechanical pass per the schema note.

## Register passes (handoff stop condition: 2)

| Pass | Scope | Result |
|---:|---|---|
| 1 | Grammar + sandhi audit of all three chapters (forms re-derived, sandhi events re-tagged against the L1–3 rank list) | Fixed: ch.1 `gaur apy asti` simplified to `gaur asti` (one † event instead of two); quote-boundary pausa convention made explicit (no *vasāmīti*-type coalescence — see Conventions); ch.2 s.11 `vanāt punar` kept `t p` unchanged (in-band); verse text re-checked against the kosha pack reading; budget-table counts re-derived from the vocab tables (33/18/16 — consistent) |
| 2 | RU gloss register (school-facing, non-academic) + natural-method pacing (recycle-before-new check) | Fixed: RU glosses de-formalized («совершает тапас» over «практикует аскезу»; «дхарма» kept as loanword per school usage); ch.1 s.9 RU rephrased («Плод она не ест»); ch.2 new-lemma count reduced by recycling ch.1 vocabulary in sentences 10–15 |

| 3 (ch. 4–5) | Grammar + sandhi audit of chapters 4–5 (verse texts re-checked against the Karaoke `s1`/`s2` fields and the pack `deva`/`iast`; every † event re-derived against ranks 1–10; word order chosen to avoid n → ñ/ṃs and d → t events) | Fixed: ch. 5 s. 1 `ślokān bahūn` order; ch. 5 s. 8 `yad dharmo nāsti` over `yat karma`; ch. 4 `aṣṭākṣarāṇi` kept as the metre's own technical compound |
| 4 (ch. 4–5) | RU gloss register + pacing (recycle-before-new; budget 15/13 vs cap 15/15; glue 25 %/27 % vs cap 30 %) | Fixed: BhG RU rewritten as original school gloss (the Karaoke RU layer is the licensed Sementsov text — not reused); «стопа» for *pāda*; «субхашита» kept as course-name loanword with «изречение» beside it |

Per the handoff, drafting **stops after these two passes per chapter** — further polish belongs to
the human editorial visa, not to more agent passes. Chapters 4–5 were drafted under
[H3493](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3493-Fable_SanskritGrammar_natural-method-story-chapters-4-5_25.08.26.md)
(Fable 5 `claude-fable-5`, 26-08-2026); mechanical budget/ID check:
[tools/story_chapter_budget_check.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tools/story_chapter_budget_check.py).

## Non-goals

- Replacing Hitopadeśa in the running pilot before the human visa
- Audio, TTS, or Karaoke alignment for story chapters (PLAN D4/D8 fence)
- A second reader schema (ARCHITECTURE mandates the kosha pack JSON)
- Full-textbook reproduction of any source (Kochergina fence)

## Provenance

Drafted by Fable 5 (`claude-fable-5`) executing
[H2113](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2113-Fable_SanskritGrammar_start-chteniya-natural-method-story_01.08.26.md)
on 01-08-2026, from IMPLEMENTATION step 1.6; vocabulary bands from
[kosha `data/frequency/vocab_curriculum.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/vocab_curriculum.tsv)
(lessons 1–3 = top-150 corpus lemmas).

_Dr. Mārcis Gasūns_
