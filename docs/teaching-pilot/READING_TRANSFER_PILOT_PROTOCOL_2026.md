# Reading-transfer pilot protocol after the compound lesson — PROPOSAL, NOT APPROVED

_Created: 11-11-2026 · Last updated: 11-11-2026 · H8030 (epic E033)_

> **STATUS: PROPOSAL. No study has been approved, recruited or run. Every numerical
> parameter below is a labelled proposal that requires study approval before use**
> (roadmap [DECISIONS.md](https://github.com/gasyoun/Uprava/blob/main/docs/linguistic-visualization-2026/DECISIONS.md) Q10:
> "Sample size, scoring rubric, retention interval and expansion threshold must be specified before the pilot;
> this interview does not invent them"). This document specifies them *for approval*, it does not approve them.
> **Missing evidence is INCONCLUSIVE, never PASS.**

## 0. What this document is / is not

| It is | It is not |
|---|---|
| A reviewable protocol + kit for testing **unseen unaided reading** after the compound lesson | Evidence that the teaching works |
| Proposed parameters with rationale, ready for a human approval pass | Approved parameters |
| A pre-study approval checklist (§8) | A recruitment plan — nobody is contacted by this handoff |
| An honest **pending** results record (§9) | A running study, a dataset, or a PASS/FAIL verdict |

A software smoke test (widget grades, build green, lint green) **cannot satisfy the transfer gate**:
it measures the tool, not the learner. The transfer gate is satisfied only by recorded learner evidence
on held-out items with the visual aids removed.

## 1. Transfer question (falsifiable shape)

**H₀:** after the compound lesson (explanation → practice), learners perform at chance-level-like or
clearly incomplete accuracy on **unseen, never-displayed** compounds with the Klammer/ladder aids removed.
**H₁ (direction to test):** learners correctly analyse and defensibly translate a majority of unseen
compounds without aids.

A pilot of this size **cannot establish general educational effectiveness** (same limitation as
[`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md) §5/§7).
It validates the instrument (no floor/ceiling, no ambiguous items), yields completion/time-on-task
estimates, and produces **initial** transfer evidence at wide uncertainty. Report uncertainty
appropriate to a small exploratory pilot: counts, medians, IQRs and a Wilson interval — never a bare
percentage and never an effectiveness claim.

## 2. Sequence and gates (fixed order)

```
(1) grammatical-accuracy review gate  →  (2) learner pilot on held-out items  →  (3) expansion decision
        [§3, PENDING]                        [never run by this handoff]           [§5 threshold, PROPOSED]
```

1. **Grammatical-accuracy review gate (before any learner testing):** every item in
   `transfer_pilot_items.tsv` passes a documented review of constituent grouping, compound category,
   analytical expansion (vigraha) and source/translation alignment — the four annotations the roadmap
   keeps distinct. Machine checks (§10) verify structure and provenance; **they do not replace
   linguistic review**. Current state: items are the H1298 agent-ratified gold set (PR #464) —
   **human philological sign-off is PENDING**, so the gate is PENDING and learner testing is not authorized.
2. **Learner pilot:** worked/practice material is shown; held-out items are attempted *before* any
   analysis is revealed. Success on a previously displayed answer is not the transfer measure
   (CONTEXT.md glossary, "Unaided reading").
3. **Expansion:** flipping the H8031 gate (`external:compound-transfer-pass`) requires the §5 threshold
   plus a recorded results row. A merged UI, a green build or roadmap confirmation does not open it.

## 3. Grammatical-accuracy review gate

- **Scope:** all 30 manifest items + their answer-key rows; any accepted alternative readings.
- **Evidence required per item:** grouping agrees, category agrees, vigraha agrees, RU translation aligned
  to source words (Klammerübersetzung convention, not a free paraphrase); constructed examples labelled.
- **Reviewer:** a philological reviewer independent of the agent that ratified the gold set.
  A separate execution session performs the protocol/logic review (§10); that is not by itself a
  linguistic sign-off.
- **State now:** PENDING — no human sign-off exists. Until it exists, the kit is **materials for review**,
  not test-ready material.
- **Upstream approved-pack dependency (final item selection):** [H8028](https://github.com/gasyoun/Uprava/blob/main/handoffs/H8028-OxAlpha_SamasaChakram_reviewed-reading-example-pack_11.11.26.md)
  — the SamasaChakram reviewed-reading-example pack, whose
  [correction crosswalk](https://github.com/gasyoun/SamasaChakram/blob/main/KLAMMERDIAGRAMM_LEITAN_SAMASA_COMPARISON.md)
  must inform reviewed teaching examples. **Final held-out item selection is re-validated against that pack
  when it lands**; this manifest is the provisional selection drawn from the already-reviewed H1298 gold set.

## 4. Item kit: worked / practice / held-out

Files (all under `docs/teaching-pilot/`):

| File | Contents |
|---|---|
| [`transfer_pilot_items.tsv`](transfer_pilot_items.tsv) | Manifest: 30 items, 10 `worked` · 10 `practice` · 10 `heldout` — no answers in this file |
| [`transfer_pilot_answer_key.tsv`](transfer_pilot_answer_key.tsv) | Main analysis per item; `visibility` = learner-visible (worked/practice) vs **examiner-only (held-out)** |
| [`scoring_sheets.md`](scoring_sheets.md) | Scoring rubric + blank scoring sheet |
| [`RESULTS_PENDING.md`](RESULTS_PENDING.md) | Blank results record — status **INCONCLUSIVE** |

- **Disjointness rule:** the three sets are disjoint by `item_id`, by `surface` and by `members` pair;
  assignment rule = round-robin over gold-file order (`idx mod 3`), so each set carries the same
  frequency/type spread. Enforced mechanically by `scripts/check_transfer_pilot_kit.py`.
- **Leakage rule:** no held-out `surface` (or its full member pair) may appear in worked/practice
  material or in any learner-visible key row. Held-out key rows are `examiner-only`.
- **Provenance:** every item cites its source row in
  [`sangram/data/samasa_ladder/gold_ladder_30.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/samasa_ladder/gold_ladder_30.tsv)
  (H1298 / PR #464, agent-ratified, 20 tests green). Original text stays recoverable; the source file is untouched.
- **Accepted alternatives:** the key records `alternative_status = PENDING_NO_SECOND_REVIEWED_READING` for
  every item — the gold set carries one ratified reading per surface, and the roadmap's "reveal reviewed
  alternatives on demand" needs a second *reviewed* reading to exist. None does yet. The alternative key
  fills in from the H8028 pack; **unreviewed machine candidates are never accepted answers.**
- **Uncertainty label:** `review_status` on every row = agent-ratified gold, human sign-off PENDING.

## 5. Proposed study parameters — EVERY ROW REQUIRES STUDY APPROVAL

Nothing in this table is agreed. The roadmap interview explicitly declined to invent these numbers.

| Parameter | PROPOSAL | Rationale | Status |
|---|---|---|---|
| **Sample size** | Single cohort, **N = 10 learners** (acceptable band 8–12); below 5, do not run as a pilot — run a 2–3 person expert dry-run of the instrument instead | Purpose is instrument validation + feasibility, not effect detection. RQ4 §5's own power placeholder needs ~64/arm for d≈0.5 — an order of magnitude beyond any first cohort, and this design has **no control arm** at all. N≈10 surfaces ambiguous items and floor/ceiling effects; it cannot support significance claims and none will be made | **PROPOSED — approval required** |
| **Scoring rubric** | Per held-out item: 3 criteria × 0–2 (C1 grouping/head, C2 category-or-relation defence, C3 defensible RU translation with alignment) = 0–6; **item pass = ≥4 with C1 ≥ 1**; primary measure = count of held-out items passed (0–10) | Mirrors the roadmap's three-part unaided check ("analyse, explain the grouping and relation, give a defensible translation"). 0–2 allows partial credit without pseudo-precision; primary measure kept as a count so a small-n median is interpretable. Full definitions in `scoring_sheets.md` | **PROPOSED — approval required** |
| **Retention interval** | **4 weeks**, same instrument shape, fresh-equivalent item set, no material sent in between | Consistency with RQ4 §6.2 (ruled 4 weeks for the estate's other learner study) — one house default instead of two; 2–4 weeks is the common L2 range. Retention is secondary in a pilot: report descriptively, attrition counts included | **PROPOSED — approval required** |
| **Expansion threshold** | Expand only if **all four** hold: (a) §3 accuracy gate passes with zero unresolved substantive objections; (b) ≥ 70% of completing learners pass ≥ 6 of 10 held-out items; (c) no rubric criterion has median < 1; (d) results recorded with completion + attrition counts | Compound→sandhi expansion (H8031 gate) should need converging evidence, not one number. 70%/6-of-10 sits above "half the items" so a lucky guess-heavy instrument cannot pass; (c) catches a systematically failing dimension that an aggregate hides. Wilson 95% CI reported alongside (b) because n≈10 makes any point estimate wide | **PROPOSED — approval required** |
| **Control arm** | **None** in wave 1 | A waitlist/control doubles recruitment for an instrument-validation pilot; RQ4 already owns the comparative question for a different content area. Wave 1 asks "can we measure transfer at all", not "is teaching A better than B" | **PROPOSED — approval required** |

**Pre-approval stance:** until §8 is signed off, these numbers may appear only as proposals.
No downstream handoff may treat this table as an approved design; H8031's gate explicitly reads
"a merged implementation or a prepared protocol is not transfer evidence".

## 6. Scoring mechanics

See [`scoring_sheets.md`](scoring_sheets.md) for criterion definitions, the accepted-answer rule
(main reading + key-marked reviewed alternatives only), the blind-scoring order (attempt recorded
**before** the analysis is revealed) and a blank per-learner sheet. Scores are entered by a human
scorer against the key; inter-scorer agreement on a 3-item subsample is itself a pilot output.

## 7. Consent and privacy procedures (152-FZ posture)

- **This handoff contacts nobody.** Recruitment, if approved, runs through an existing course channel
  by a human — the RQ4 precedent (Systema's own Kochergina-stage students, ruled by MG) is the standing
  estate pattern, and reusing it is a proposal, not a decision of this document.
- **Draft consent text (DRAFT — requires approval in the Society's voice; RQ4's MG-approved paragraph is
  the wording precedent):**

  > Это исследование — часть работы Общества ревнителей санскрита над тем, как лучше учить санскриту.
  > Вам будет показан урок составов, затем короткий тест на новых примерах без подсказок, и такой же
  > тест ещё раз через 4 недели, без дополнительных материалов между тестами. Участие добровольное,
  > результаты используются обезличенно (для анализа, не для оценки успеваемости). В любой момент
  > можно выйти без объяснения причин.

- **Data minimisation:** results files carry a pseudonymous learner ID only — no names, no handles, no
  emails, no contact data in the repository. Contact data, if any exists for follow-up, stays on the
  platform that already holds it and is never copied into this repo.
- No special-category data, no biometrics, no automated profiling of learners; no transfer of learner
  data to third parties; scores used for analysis, never for grading.
- Participants may withdraw and request deletion of their rows; the blank results template is designed
  so that withdrawing a row leaves the record coherent (counts recomputed, never fabricated).

## 8. Pre-study approval checklist — ALL PENDING

| # | Approval item | Depends on | Status |
|---|---|---|---|
| 1 | Sample size (N band) | §5 row 1 | PENDING |
| 2 | Scoring rubric incl. pass rule | §5 row 2, `scoring_sheets.md` | PENDING |
| 3 | Retention interval | §5 row 3 | PENDING |
| 4 | Expansion threshold | §5 row 4 | PENDING |
| 5 | Consent wording (§7 draft) | MG / Society voice | PENDING |
| 6 | Recruitment channel + contact procedure | human; RQ4 §6.1 precedent | PENDING |
| 7 | Instrument/hosting home (print sheets vs Systema harness reuse) | §8/§6.3-analogue @DECIDE | PENDING |
| 8 | Grammatical-accuracy review gate sign-off (§3) | philological reviewer | PENDING |
| 9 | Final item selection | **H8028 approved pack** | PENDING (upstream) |
| 10 | Independent protocol/logic review | separate execution session | PENDING |

## 9. Pending results record

[`RESULTS_PENDING.md`](RESULTS_PENDING.md) is committed **blank**, standing `INCONCLUSIVE`.
Rules: it is filled only by an approved run; a run that did not happen never produces rows;
synthetic, illustrative or "expected" learner numbers are forbidden anywhere in this kit;
attrition is a recorded datum, never silently dropped.

## 10. Verification performed and outstanding

- **Automated (this handoff):** `python scripts/check_transfer_pilot_kit.py` — set disjointness,
  held-out leakage, key coverage/visibility, source provenance vs `gold_ladder_30.tsv`, blank results
  record, PROPOSED labels present. Wired as `tests/test_transfer_pilot_kit.py`.
- **Independent review (outstanding, required by the handoff verifier clause):** a separate session
  reviews logic + evidence; **its absence keeps this protocol PENDING, not PASS.**
- **Linguistic review (outstanding, required by §3):** human philological sign-off on items.
- Machine green + these two reviews outstanding = **status PENDING / INCONCLUSIVE**, never PASS.

## 11. Traceability

| Claim | Backing |
|---|---|
| Direction, sequence, expansion policy | [ROADMAP.md](https://github.com/gasyoun/Uprava/blob/main/docs/linguistic-visualization-2026/ROADMAP.md), [DECISIONS.md](https://github.com/gasyoun/Uprava/blob/main/docs/linguistic-visualization-2026/DECISIONS.md) (finalized 11-11-2026) |
| Glossary: unaided reading, transfer pilot, main/alternative reading | [CONTEXT.md](https://github.com/gasyoun/Uprava/blob/main/docs/linguistic-visualization-2026/CONTEXT.md) |
| Item source: 30 hand-checked analyses, head-first ladder | PR [#464](https://github.com/gasyoun/SanskritGrammar/pull/464) (H1298), `sangram/data/samasa_ladder/gold_ladder_30.tsv` |
| Prior protocol shape, 4-week precedent, consent precedent | `docs/RQ4_EVALUATION_PROTOCOL_2026.md` §5–§7 (rulings 15–16-07-2026) |
| Upstream pack dependency | [H8028](https://github.com/gasyoun/Uprava/blob/main/handoffs/H8028-OxAlpha_SamasaChakram_reviewed-reading-example-pack_11.11.26.md) + SamasaChakram correction crosswalk |
| Gate semantics for downstream handoffs | ROADMAP.md "Minted delivery plan" (H8031 `external:compound-transfer-pass`) |

---

_Gasūns · Spec executed under H8030 (OxAlpha), 11 November 2026. Parameters above are proposals awaiting
study approval; no participant, run, or sign-off is represented as existing._
