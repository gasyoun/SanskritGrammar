# Roadmap — SanskritGrammar freeze exit + methodichka residual (2026 H2)

_Created: 24-07-2026 · Last updated: 24-07-2026_

Wave structure for the plan whose cover is
[`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md).

Waves are **contract-gated**, not calendar-gated (same principle as the 18-07 charter ruling).

## 1. Wave shape

| Wave | Opens when | Closes when | Fronts |
|---|---|---|---|
| **W1 · Probe + methodichka + hygiene** | This plan is committed | Every one of the 15 unknowns has a probe artifact + ledger update (`kill_gated` / survivor / `blocking_note`); Apte residual terminal or escalated; hygiene handoff merged; H1454 may still be in flight | A + B + C parallel |
| **W2 · Visas for survivors** | W1 probe report lists survivors | SE multi-article sheet cut + voted; non-SE survivors dispositioned or sheeted; apply handoffs minted for approve cards | A3 then apply |
| **W3 · Freeze exit check** | Zero `disposition=unknown` on baseline | `freeze.active` may flip false via a dedicated mechanical handoff that only checks the exit criterion | ledger-only |
| **W4 · Post-exit (out of scope here)** | Freeze flipped | New Sangram topics may resume under the charter | not staged |

Human track (parallel, not agent-gated): M03 freeze **31-10-2026** (review
[`GasunsDhatu_2026_RWS_review.docx`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/GasunsDhatu_2026_RWS_review.docx));
RQ4 feature flip; A61 CfP when published.

## 2. Non-goals

- New Sangram topic manifests while `freeze.active` is true.
- Re-running the drained 18-07 editorial-note apply wave (H1273–H1277).
- Minting new paper handoffs (A62–A64 already queued).
- Agent rewrite of M03 body prose or RQ4 protocol.
- Rights programme / new third-party corpus ingest.

## 3. Handoff specs (wave 1)

### W1-A0 · `freeze-15-killgate-matrix` — Sonnet

| Field | Value |
|---|---|
| Deliverable | [`sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md) — one row per unknown toc_ref: programme slot, kill-gate criterion (quoted), existing script path or `MISSING`, acceptance predicate |
| Acceptance | 15/15 rows; every `MISSING` has a named escalate path; no probe code required in this handoff |
| Human gate | none |

### W1-A1 · `freeze-probe-se-cluster` — Opus

| Field | Value |
|---|---|
| Scope | SG-SE-001, SG-SE-002, SG-SE-003, SG-SE-004, SG-SE-005, SG-SE-006, SG-SE-008, SG-SE-013, SG-SE-009 is **already published** — skip; remaining SE unknowns only |
| Deliverable | Per-article probe under `sangram/audit/probe_freeze_<art_id>.{py,json,md}` + ledger `disposition` or `blocking_note` |
| Acceptance | 9 SE unknowns terminal as `kill_gated` / survivor (`blocking_note` empty, disposition still unknown until visa) / escalated; validators green |
| Human gate | freeze-criterion dispute → hard stop |

### W1-A2 · `freeze-probe-mo-wf-stragglers` — Opus

| Field | Value |
|---|---|
| Scope | SG-MO-019, SG-MO-022, SG-MO-024, SG-MO-025, SG-WF-002, SG-WF-009, SG-WF-011 |
| Deliverable | Same pattern as A1 |
| Acceptance | 6/6 terminal as above; validators green |

### W1-A3 · `freeze-se-survivor-visa-sheet` — Sonnet

| Field | Value |
|---|---|
| Depends on | A1 survivor list |
| Deliverable | `review/specs/sangram-se-freeze-survivors-visa_<date>.json` + generated HTML via `scripts/build_visa_sheet.py`; registered in Uprava `REVIEW_SHEETS_INDEX.md` |
| Acceptance | Sheet covers **only** SE survivors; zero kill_gated articles on the sheet; save-path banner correct |
| Human gate | **vote** — apply is a follow-on handoff after decisions.json lands |

### W1-B0 · H1454 (existing) — Fable

Do not re-mint. See
[H1454](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1454-Fable_SanskritGrammar_kochergina-metodichka-v1-open-items_22.07.26.md).

### W1-B1 · `metodichka-apte-open-residual` — Fable

| Field | Value |
|---|---|
| Scope | Index rows on `ApteSyntax_1885/METODICHKA_APTE_KOMMENTARII_2026.md` with OPEN/PARTIAL: zan-19, zan-22, prilozhenie |
| Deliverable | Notes terminal (APPLIED / DEFERRED / ESCALATED) with revision-history rows; zan-19 stays escalated if Elizarenkova scan still missing |
| Acceptance | Zero OPEN on Apte target in `EDITORIAL_NOTE_INDEX.tsv` without a disposition reason |

### W1-C0 · `sg-handoff-hygiene-archive-triage` — Sonnet

| Field | Value |
|---|---|
| Deliverable | Registry rows flipped for executed/superseded SanskritGrammar handoffs; archive moves; short report of still-live 🟡 |
| Acceptance | No 🟡 row whose PR is merged without archive; H967-class SUPERSEDED banners respected (do not execute) |

## 4. Ordering

```text
A0 (matrix) ──┬──► A1 (SE probes) ──► A3 (SE visa sheet) ──► [human vote] ──► apply (later mint)
              └──► A2 (MO/WF probes) ──► non-SE survivor sheet or individual (later mint)
B0 (H1454) and B1 (Apte) and C0 (hygiene) run in parallel with A0–A2.
```

_Dr. Mārcis Gasūns_
