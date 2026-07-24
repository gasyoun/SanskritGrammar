# Freeze probe — SG-MO-025 (`art:infinitive`)

_Created: 24-07-2026 · Last updated: 24-07-2026_

**Handoff:** [H1613](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1613-Opus_SanskritGrammar_freeze-probe-mo-wf-stragglers_24.07.26.md) (W1-A2).
**Executor:** Grok 4.5 (grok-4.5) (user-launched override of intended Opus 4.8).
**Matrix:** [`sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md).

## Criterion (quoted from H1611 matrix)

> MISSING — not a C5 § 7 pilot.

**Programme slot:** C5 · cluster «Именные формы глагола»

**Existing instrument (not used as a kill-gate):** [`scripts/sg_mo_025_infinitive.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_025_infinitive.py)

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

Do not invent an infinitive-specific kill threshold.

## Escalate path

Human @DECIDE or visa-only path.

## Artifacts

- [`probe_freeze_infinitive.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/probe_freeze_infinitive.py) — regenerates JSON
- [`probe_freeze_infinitive.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/probe_freeze_infinitive.json) — machine record

_Dr. Mārcis Gasūns_
