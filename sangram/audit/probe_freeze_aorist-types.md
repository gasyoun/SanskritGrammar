# Freeze probe — SG-MO-019 (`art:aorist-types`)

_Created: 24-07-2026 · Last updated: 24-07-2026_

**Handoff:** [H1613](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1613-Opus_SanskritGrammar_freeze-probe-mo-wf-stragglers_24.07.26.md) (W1-A2).
**Executor:** Grok 4.5 (grok-4.5) (user-launched override of intended Opus 4.8).
**Matrix:** [`sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md).

## Criterion (quoted from H1611 matrix)

> MISSING — C5 § 7 pilots are only MO-002 / MO-013 / MO-017 / WF-008 / WF-003. Nearest related pilot text is C5 P3 (SG-MO-017 perfect), which does NOT transfer.

**Programme slot:** C5 · cluster «Перфект, аорист, будущее» (beyond-quota partition of SG-MO-018)

**Existing instrument (not used as a kill-gate):** [`scripts/sg_mo_019_aorist_types.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_019_aorist_types.py)

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

Do not transfer C5 P3 form-class 95% gate from perfect to aorist-types.

## Escalate path

Human @DECIDE for a per-slot MO-019 gate, or visa-only path. Context: C5 EM2.

## Artifacts

- [`probe_freeze_aorist-types.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/probe_freeze_aorist-types.py) — regenerates JSON
- [`probe_freeze_aorist-types.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/probe_freeze_aorist-types.json) — machine record

_Dr. Mārcis Gasūns_
