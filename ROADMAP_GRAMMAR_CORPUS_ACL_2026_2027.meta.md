# Metadoc — ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md

_Created: 10-07-2026 · Last updated: 19-07-2026_

A document about [`ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md).

---

## Purpose

The one-year plan (Q3 2026 → Q2 2027) for promoting SanskritGrammar from a digitized-reprint
archive to a measured comparative corpus with two submittable papers, one citable dataset, and an
ACL-Anthology-shaped publishing layer.

## Audience

The repo owner (quarterly re-read), and any future session asked "what should this repo do next".
Not a public-facing document.

## Provenance

Authored 10-07-2026 by Opus 4.8 (`claude-opus-4-8`) in a single session, from four human decisions
taken that day (four spines in scope · ACL crosswalk covers method + product + benchmark · repo
promoted from Tier 2 to priority research · agenda delegated to Fable 5 `claude-fable-5` as
[H450](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H450-Fable_SanskritGrammar_dh_memo_research_agenda_10.07.26.md)).

The ACL-Anthology citations were **live-fetched and verified** in that session by three read-only
research agents — none is recalled from model memory. The verified non-findings (no ACL precedent
for rival-classification adjudication, for Western-grammar↔sūtra alignment, for seṭ/aniṭ as a
corpus-adjudicated target, and no confirmable SIGMORPHON Sanskrit track) are load-bearing: two of
the roadmap's papers claim novelty on exactly those gaps. **Re-verify before submission** — a gap
that closes between now and Q1 2027 changes the contribution claim.

## Relationship to sibling documents

- [`MORPHOCLASS_COMPARISON_ROADMAP.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_COMPARISON_ROADMAP.md)
  — the *narrow* roadmap for spine S2 alone; predates this file and remains valid inside its scope.
  This roadmap subsumes it as one of four spines and adds the corpus-adjudication framing.
- [`MORPHOCLASS_3WAY_MEMO.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.md)
  + [`MORPHOCLASS_3WAY_MEMO.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.meta.md)
  — the executed S2 comparison (H357). Its findings are inputs, not open questions.
- [`ZALIZNIAK_1975_1978_2004_COMPARISON.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md)
  — the intra-Zalizniak axis; treated as settled fact.
- [`docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md)
  — the H450 agenda (landed 10-07-2026): hypotheses SG-H1…SG-H9, visualisations SG-V1…SG-V6, the
  14-citation ACL crosswalk, sections N1–N4, and the ranked 11-item build backlog. **This roadmap
  is the plan; that memo is the agenda; neither is the analysis.**

## Known limitations / caveats

1. **The Bühler edition risk is understated by the plan's structure.** The 1923-reprint-as-proxy-for-1878
   problem (risk 1, gate `@DO D4`) sits underneath the *most attractive* early result (S1 borrowing
   direction). A reader skimming Q3 may not notice that Q4.5 is blocked. If D4 resolves negatively —
   i.e. the 1878 exercises differ — S1 loses its directionality claim and keeps only the order
   comparison. The roadmap does not currently spell out that fallback in Q4.
2. **Q3.3 has no second annotator** and standing guidance parks recruitment for 2026. The single-annotator
   fallback is stated, but it means the coverage-matrix evaluation ships without a κ — weaker than the
   plan's own methodology section implies.
3. **The tier promotion (D3) is asserted, not yet reconciled.** Nothing in
   [`Uprava/GTD_NEXT_ACTIONS.md`](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md)
   has been re-ranked; the roadmap names the cost but does not pay it.
4. **Effort estimates are absent** for Q4 and later. Only the ACL site-feature table (Angle B) carries
   S/M/L. Quarterly items have no sizing at all.
5. **S4 is deliberately starved.** If phonostatistics turns out to matter to the Dhātu monograph's
   2027 print deadline, this roadmap gives it no lane.

## Intended use / known misuse

- **Intended use.** A quarterly re-read planning document for the repo owner, and the resume
  point for any future session asked "what should SanskritGrammar do next" — read alongside
  [`docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md)
  (the agenda) and [`MORPHOCLASS_3WAY_MEMO.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.md)
  (the executed S2 finding it subsumes).
- **Known misuse.** (1) Treating the four ACL non-findings (§ Provenance) as still true without
  re-verification — they are explicitly time-bound novelty claims for two papers and the roadmap
  itself flags "re-verify before submission." (2) Reading the plan as already executed — it is a
  plan; only rows in the Revision history table below (D2 closed, H450 landed) reflect actual
  completed work, everything else in the quarterly body is still open. (3) Treating the D3 tier
  promotion (Tier 2 → priority research) as already reconciled in
  [`Uprava/GTD_NEXT_ACTIONS.md`](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md) —
  known-limitations item 3 states it is asserted, not yet paid for by re-ranking other tiered work.
  (4) Using the missing S/M/L effort estimates (known-limitations item 4) as evidence that Q4+ work
  is small — absence of sizing is a gap, not a zero.

## Maintenance & sunset plan

- **Who maintains.** The repo owner, on a quarterly re-read cadence (Q3 2026, Q4 2026, Q1 2027,
  Q2 2027), plus any session that closes a `@DO`/`@DECIDE` gate named in the roadmap (D1–D6) —
  each such closure gets its own Revision history row, as D2 and the H450 landing already do below.
- **Update trigger.** A quarterly boundary is reached; a gated decision (D1, D3, D4, D5, D6) is
  resolved; the H450 agenda's hypothesis/backlog set changes; or a listed ACL non-finding (§
  Provenance) closes in the literature and a novelty claim needs re-scoping.
- **Sunset condition.** Superseded once Q2 2027 concludes and a follow-on
  planning document is written for the next cycle, or earlier if all four spines (S1–S4) either
  ship or are formally closed such that the quarterly structure no longer matches remaining work.
  Until then this roadmap remains the single active plan for the repo — it is not sunset merely
  because individual quarters complete.

## Deprecation status

`active`

## Improvement backlog (ranked)

| # | Item | Status |
|---|---|---|
| 1 | Spell out the **S1 fallback** if `@DO D4` resolves negatively (keep order comparison, drop directionality) | open |
| 2 | Reconcile the **D3 tier promotion** into GTD's standing tier order — name what it displaces | open |
| 3 | Add **S/M/L effort estimates** to every Q3–Q2 item, not just Angle B | open |
| 4 | Fold H450's numbered hypotheses back in as the roadmap's **hypothesis IDs** once the memo lands | ✅ closed 10-07-2026 — memo landed with IDs **SG-H1…SG-H9** (S1: H1/H2/H3/H4/H9 · S2: H5/H6 · S3: H7 · S4: H8) + viz **SG-V1…SG-V6**; see [`docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md) |
| 5 | Re-verify the four **ACL non-findings** before any submission (they are the novelty claims) | open — due Q1 2027 |
| 6 | Decide whether **S4** gets a lane or is formally closed | open |
| 7 | Add a **budget line** — token/time cost per quarter — H450's backlog now carries S/M/L per item, quarterly roll-up still missing | open |

## Revision history

| Date | Change | By |
|---|---|---|
| 10-07-2026 | Created. Four spines, three ACL angles, four quarters, five open decisions (D1–D5). | Opus 4.8 (`claude-opus-4-8`) |
| 10-07-2026 | H450 agenda landed: backlog #4 closed (SG-H1…H9, SG-V1…V6); metadoc's stale `ROADMAP_2026_2027.md` self-references repointed to the renamed `ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md` (rename `77868c5` had missed them). | Fable 5 (`claude-fable-5`) |
| 10-07-2026 | **D2 closed.** [H449](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H449-Sonnet_SanskritGrammar_zaliznyak-zalizniak-rename-sweep_10.07.26.md) checked the premise behind cancelling the Zaliznyak→Zalizniak rename (that "Zaliznyak" was the historically-printed citation spelling) against real evidence — Tolchelnikov's own published paper already cites "Andrei Zalizniak. 1975." (i-spelling) — and found it false. Rename proceeded ([SanskritGrammar PR #78](https://github.com/gasyoun/SanskritGrammar/pull/78) + [RuWritingStyles PR #70](https://github.com/gasyoun/RuWritingStyles/pull/70), both merged); B6 (`people.yaml` name-variant map) demoted from "dissolves D2" to an independent, optional backlog item. Also fixed this metadoc's stale `ZALIZNYAK_1975_1978_2004_COMPARISON.md` self-reference to the renamed filename. | Sonnet 5 (`claude-sonnet-5`) |
| 11-07-2026 | template v2 backfill (H663) | Sonnet 5 (`claude-sonnet-5`) |
| 14-07-2026 | **S1 cross-grammar milestone recorded (H797 Phase 2).** S1 sub-thread updated: D-A/D-B rulings noted, second register live — [`BuhlerLeitfaden_1923/claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml) 64 verified + 339-candidate backlog ([PR #186](https://github.com/gasyoun/SanskritGrammar/pull/186)); two-register calibration finding added; remaining Knauer/Zaliznyak stated. | Fable 5 (`claude-fable-5`) |
| 18-07-2026 | **Portfolio rewrite (backfilled row — the authoring session did not update this metadoc).** [PR #417](https://github.com/gasyoun/SanskritGrammar/pull/417) rebuilt the file from an ACL-track roadmap into the repo's five-track **portfolio umbrella** (M03 · Sangram · pedagogy/RQ4 · comparative · archive) per the 18-07-2026 roadmap interview: 8 rulings, waves W1–W4, H1259/H1260/H1261 pointers, Sangram consolidation freeze. | recorded 19-07-2026 by Fable 5 (`claude-fable-5`) |
| 19-07-2026 | **Sangram-primary re-base ([H1277](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1277-Fable_SanskritGrammar_sangram-acl-roadmap-rebase-primary_18.07.26.md)).** Keep-both ruling executed: §2 "four spines" → "four instruments" feeding Sangram (labels kept), Track C re-titled the **publication arm of Sangram** with a §0 relation paragraph, per-instrument "Feeds Sangram" leads (honest τ/κ citation split: τ cited by three programme docs, not articles; tatpurusha's Cohen κ ≠ the never-run S2/Q3.4 κ), Q3.1/Q3.2 marked done and Q4.1–Q4.5 plainly unstarted, measured 34.2 % sangram/ share since 14-07. Freeze respected: no new topics/manifests, charter untouched. | Fable 5 (`claude-fable-5`) |

_Dr. Mārcis Gasūns_
