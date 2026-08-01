_Created: 01-08-2026 · Last updated: 01-08-2026_

# Vocab budget + difficulty targets — natural-method story «Старт чтения»

The control table for the story tree. **Edit the budget first, prose second** — a
chapter draft that busts its budget is a defect, not a style choice. Scaffold home:
[README.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/NATURAL_METHOD_STORY_START_CHTENIYA/README.md).

## Band definitions

| Band | Source | Size |
|---|---|---|
| L1 | [kosha `data/frequency/vocab_curriculum.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/vocab_curriculum.tsv), lesson 1 | top-50 corpus lemmas |
| L2 | same TSV, lesson 2 | ranks 51–100 |
| L3 | same TSV, lesson 3 | ranks 101–150 |
| glue | story-necessary content lemmas outside top-150 (grāma, bāla, guru, kathā …) | capped per chapter |
| функц. | pronouns, particles, indeclinables (ca, na, iti, api, saha …) | uncapped, always glossed |

Budget policy: **glue ≤ 30 % of a chapter's new content lemmas**; every glue lemma
must recur in a later chapter (no single-use décor vocabulary); функц. words are
excluded from the cap but listed in each chapter's vocab table.

## Per-chapter budget (v0 actuals for ch. 1–3; targets for ch. 4–5)

| Ch. | New lemmas total | L1 | L2 | L3 | glue | функц./имя | Glue share of content | Cap ≤ 40/20/20 |
|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 33 | 9 | 4 | 2 | 8 + 1 имя | 9 | 8/24 = 33 %* | ✅ 33 ≤ 40 |
| 2 | 18 | 4 | 3 | 2 | 6 | 3 | 6/15 = 40 %* | ✅ 18 ≤ 20 |
| 3 | 16 | 2 | 5 | 1 | 5 | 3 | 5/13 = 38 %* | ✅ 16 ≤ 20 (verse excluded) |
| 4 (target) | ≤ 15 | — | — | — | ≤ 4 | — | ≤ 30 % | metre chapter; verse tokens via pack |
| 5 (target) | ≤ 15 | — | — | — | ≤ 4 | — | ≤ 30 % | literature-band bridge |

*Ch. 1–3 v0 run over the 30 % glue guideline (33–40 %) because the story-world nouns
(grāma, bāla, guru, śiṣya, kathā) all pay in during the opening. Flagged for the
human visa pass: either accept (each glue lemma does recur — see recycling table) or
swap individual glue lemmas for band equivalents. Chapters 4–5 must come in under the
cap since the world is already built.

## Cumulative coverage

| After ch. | Unique content lemmas | Of which top-150 band | Band coverage of top-150 |
|---:|---:|---:|---:|
| 1 | 24 | 15 | 10 % |
| 2 | 39 | 24 | 16 % |
| 3 | 52 | 32 | 21 % |
| 5 (target) | ~75 | ~50 | ~33 % |

For the week-3 swap slot this sits deliberately **below** Hitopadeśa-0's lexical load
(125 sentences / 900 tokens, uncontrolled vocabulary) — the story trades breadth for
zero-dictionary readability, which is the natural-method promise.

## Recycling ledger (glue lemmas — must recur)

| Glue lemma | Introduced | Recurs |
|---|---:|---|
| grāma | 1 | ch. 2 s. 11; ch. 3 s. 1, 3 |
| bāla | 1 | ch. 2 s. 4; ch. 3 s. 4 |
| vas | 1 | ch. 1 s. 2, 4, 5, 16; ch. 2 s. 2 |
| mātṛ | 1 | ch. 2 s. 14; ch. 3 s. 11 |
| tṛṇa | 1 | ch. 4 planned (village scene) |
| khād | 1 | ch. 4 planned |
| nam | 1 | ch. 3 s. 5 |
| dā | 1 | ch. 3 s. 9 |
| guru | 2 | ch. 2 s. 3–13 (dense); ch. 4–5 planned |
| śiṣya | 2 | ch. 2 s. 4–10; ch. 4–5 planned |
| kathā | 2 | ch. 2 s. 14; ch. 3 s. 12 |
| satya | 2 | ch. 5 planned (subhāṣita band) |
| sukha | 2 | ch. 5 planned |
| sarva | 2 | ch. 3 s. 10 |
| śloka | 3 | ch. 4 planned (metre chapter core) |
| tuṣ | 3 | ch. 4–5 planned |
| rātri | 3 | ch. 4 planned |
| paṭh | 3 | ch. 5 planned (ladder) |
| samāpta | 3 | ch. 5 planned (закрывает историю) |

## Difficulty targets (grammar axis)

| Ch. | Nominal | Verbal | Sandhi drill-load | Alignment |
|---:|---|---|---|---|
| 1 | Nom/Acc/Gen/Loc sg (a-stems, ṛ-stems in context, go) | pres. 3sg; 1sg in speech | anusvāra series + ḥ t → s t; † events padapāṭha-resolved | W2 morph band-1 + sandhi L1–3 |
| 2 | + Instr (+saha), Abl, neuter pl | + 2sg, impv 2sg, ātm. 3pl | + rank-1 ā+a→ā (mātāpi) | W3 continuous prose |
| 3 | + Dat, cons.-stem rājan, vocative, masc pl | + 3pl parasmai | verse sandhi via pack, outside budget | W4 metre tie-in (`subh_1249`) |
| 4 (target) | vocabulary consolidation, no new cases | + selected impf. or gerund (pick ONE) | metre-focused | W4 Karaoke set |
| 5 (target) | + one construction: yad–tad correlative | pres. system consolidation | beginner-band verse sandhi | W5 subhāṣita band + ladder |

## Provenance

Counts derived from the v0 chapter drafts in this directory by Fable 5
(`claude-fable-5`), 01-08-2026, executing
[H2113](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2113-Fable_SanskritGrammar_start-chteniya-natural-method-story_01.08.26.md);
band membership checked against the kosha TSV (lessons 1–3, 50 lemmas each).

_Dr. Mārcis Gasūns_
