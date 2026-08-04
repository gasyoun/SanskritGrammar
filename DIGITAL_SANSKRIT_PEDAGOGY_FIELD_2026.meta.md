# Metadoc — DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md

_Created: 14-07-2026 · Last updated: 27-07-2026_

Companion record for [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md)
— the "document about the document" a fresh session should read before editing the field metadoc.

## Purpose

The single org-wide definition of **digital Sanskrit pedagogy** as a priority research field. It
sits *above* the three pre-existing pedagogy maps (Systema asset-index + A0–C2 ladder;
SanskritGrammar `LEARNER_MATERIALS.md`; kosha `POSITIONING.md`) and consolidates them by
reference — an aspect-primary taxonomy with layered tags, plus the research agenda and gap
register those maps lack.

## Audience

Researchers and maintainers deciding *what to build/measure next* across the pedagogy-facing
repos; paper authors (A62/A32/A60 + the RQ1 method paper); any session onboarding to the field.
Not a learner-facing document.

## Provenance

- **Method:** authored via [`/ask`](https://github.com/gasyoun/claude-config/blob/main/commands/ask.md)
  — a 4-round up-front interview (17 rulings, zero blocking forks) then the layered plan.
- **Model:** Opus 4.8 (`claude-opus-4-8`, 1M-context) — interview + authoring, 14-07-2026.
- **Audit basis:** three parallel repo/hub sweeps (KOSHA + SanskritGrammar; sibling pedagogy repos; Uprava hubs) grounding every asset row.
- **Registration:** MEGABOOK §2.10 (+ §2.9 strengthened); ARTICLES A62/A32/A60; GTD straddle tier; ROADMAP_INDEX; wave-1 handoffs (parent + 4 children).

## Ranked improvement backlog

1. **Fill the §4a matrix cells with counts, not just status glyphs** — once the asset inventory has per-cell tallies, the matrix becomes a coverage dashboard.
2. **Auto-generate the §3 asset rows from a machine index** — today they are hand-curated; a `pedagogy_assets.tsv` (tagged on the six layers) driving both this doc and the derived views would keep them in sync and let the matrix/journey/capability pivots be generated, not maintained.
3. ✅ **DONE 27-07-2026** ([H1476](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1476-Opus_SanskritGrammar_pedagogy-aspect-measurable-result-metrics_22.07.26.md)) — **per-aspect "first measurable result"**: §4e now carries the PM1–PM12 register (metric + denominator · data source · today · bar · refutation condition), a per-aspect line in §3.1–3.12, a metric column in the §4a matrix, and the RQ-composition table that reserves learning gain and retention to RQ4 alone.
4. **Wire the traditional-discipline (§4d) frame into the Sangram corpus-grammar** — the emic Vedāṅga axis is currently prose; it could anchor a real cross-tab.
5. **Reconcile with kosha's `CONCORDANCE_ROADMAP.md` Q4** (Pāṇini-sūtra↔corpus) as it lands — §3.5's central gap.
6. **Decide audio** (§3.7): TTS vs recorded reciter — the gating decision for the A0–A2 rungs (currently a GTD @DECIDE in the Systema ladder).
7. **Keep §4e's "today" column from rotting** — 10 of the 12 PMs read "unmeasured", and the two that carry numbers (PM2, PM6) were computed from committed artifacts. Both are derivable, so the column is a generation target, not a maintenance chore — the natural extension of item 2.

## Limitations

- **Aspect rows are hand-curated** from a point-in-time audit (14-07-2026); statuses drift as sibling repos ship. Re-audit before trusting a ✅/🟡.
- **External-project claims** (vidyut, Heritage, Samsaadhanii, DCS, VedaWeb capabilities) are as of the audit's knowledge; re-verify before citing in print.
- **Not a learner document** — no lesson content lives here; it is a map, not a course.
- **The derived views (§4) are illustrative**, not generated — until backlog item 2 lands, the matrix can lag the aspect rows.
- **§4e's bars are proposed, not ratified, and they carry an expiry.** Only **4 of 12** rest on a measurement (PM2, PM3, PM4, PM7); one is a disclosure rule (PM6); **7 are reasoned but unanchored**. §4e′ records each bar's anchor, its strength, and what evidence would move it, and sets a **27-09-2026** review point (mirrored as a `@DECIDE` in [`Uprava/GTD_NEXT_ACTIONS.md`](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md)) for a human to ratify, revise or extend them. Cheapest pre-review improvement: **PM8 and PM12 are computable from existing data** — replacing those two guesses with numbers needs no new build.
- **Ten of the twelve PMs read "unmeasured"** (27-07-2026). That is the honest state of the field, not an omission: only PM2 and PM6 have committed artifacts to compute from today. Do not read a missing number as a failing one.

## Related docs

- Plan cover: [`docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md) (+ roadmap/architecture/implementation/verification).
- Consolidated maps: Systema [asset-index](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/docs/SANSKRIT_HUB_ASSET_PEDAGOGY_INDEX.md) + [ladder](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/docs/SANSKRIT_HUB_LEARNER_PROGRESSION_A0_C2.md); [`LEARNER_MATERIALS.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/LEARNER_MATERIALS.md); kosha [`POSITIONING.md`](https://github.com/gasyoun/kosha/blob/main/POSITIONING.md).
- Field thesis: [`MEGABOOK.md`](https://github.com/gasyoun/Uprava/blob/main/MEGABOOK.md) §2.10/§2.9.

## Revision history

| Date | Change | Model |
|---|---|---|
| 14-07-2026 | Created — field defined, 12 aspects mapped, 4-RQ agenda, gap register; registered org-wide | Opus 4.8 (`claude-opus-4-8`) |
| 27-07-2026 | §4e′ recalibration clause — a **27-09-2026** review point plus the per-bar anchor/strength/what-would-move-it table, so a human recalibrating in two months does not have to re-derive where each threshold came from. Records the honest split: 4 bars measured, 1 disclosure rule, 7 reasoned-but-unanchored (PM8 and PM12 computable today). Revision protocol fixed: a bar changes in the open with a history row, and **never in the same pass as the measurement that failed it** | Opus 5 (`claude-opus-5[1m]`) |
| 27-07-2026 | Backlog item 3 — §4e metric register (PM1–PM12): one falsifiable capability metric per aspect with data source, today's value, bar and refutation condition; metric column added to the §4a matrix and to the §3.8–3.12 table; §5 + §8 state the RQ4 exclusivity rule (no PM may measure learning gain or retention). Two baselines measured, not asserted: PM2 = 90.7% answer-keyed items, PM6 = 56.5% type / 56.2% DCS-token on-ramp scope transfer (new [`measure_onramp_scope.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/measure_onramp_scope.py)). [H1476](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1476-Opus_SanskritGrammar_pedagogy-aspect-measurable-result-metrics_22.07.26.md) | Opus 5 (`claude-opus-5[1m]`) |

---

_Dr. Mārcis Gasūns_
