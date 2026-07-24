# Freeze probe — SG-WF-002 (`art:krt-overview`)

_Created: 24-07-2026 · Last updated: 24-07-2026_

**Handoff:** [H1613](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1613-Opus_SanskritGrammar_freeze-probe-mo-wf-stragglers_24.07.26.md) (W1-A2).
**Executor:** Grok 4.5 (grok-4.5) (user-launched override of intended Opus 4.8).
**Matrix:** [`sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md).

## Criterion (quoted from H1611 matrix)

> MISSING — overview, not pilot. Related C5 § 7 P5 (SG-WF-003) is a different published article.

**Programme slot:** C5 · cluster «Деривация» (overview; script self-labels no kill-gate)

**Existing instrument (not used as a kill-gate):** [`scripts/sg_wf_002_krt_overview.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_002_krt_overview.py)

## Verdict

| Field | Value |
|---|---|
| Criterion status | **MISSING** |
| Probe action | **park-and-skip** (no corpus kill-gate run; no invented threshold) |
| Ledger disposition | leave `unknown` |
| Terminal class for H1613 | **escalated** (blocking_note + source_links) |
| `kill_gated` | no |
| Visa-list candidate (non-SE) | **yes** — pending human visa sheet (not H1614) |

## Do not

Do NOT re-fire P5 surface-suffix dictionary-validation gate against the WF-002 overview spine (native VerbForm in {Part,Conv,Gdv,Inf}).

## Escalate path

Visa-only or @DECIDE for an overview-specific freeze rule. Context: C5 EM5.

## Artifacts

- [`probe_freeze_krt-overview.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/probe_freeze_krt-overview.py) — regenerates JSON
- [`probe_freeze_krt-overview.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/probe_freeze_krt-overview.json) — machine record

_Dr. Mārcis Gasūns_
