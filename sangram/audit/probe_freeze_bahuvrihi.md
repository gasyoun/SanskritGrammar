# Freeze probe — SG-WF-009 (`art:bahuvrihi`)

_Created: 24-07-2026 · Last updated: 24-07-2026_

**Handoff:** [H1613](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1613-Opus_SanskritGrammar_freeze-probe-mo-wf-stragglers_24.07.26.md) (W1-A2).
**Executor:** Grok 4.5 (grok-4.5) (user-launched override of intended Opus 4.8).
**Matrix:** [`sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md).

## Criterion (quoted from H1611 matrix)

> MISSING as a numeric pilot gate for this slot. Related C5 § 7 P4 (SG-WF-008 tatpurusa) is a different article.

**Programme slot:** C5 · cluster «Композиты»; C6-blocked exocentricity (article publishes the limit, not a census)

**Existing instrument (not used as a kill-gate):** [`scripts/sg_wf_009_bahuvrihi.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_009_bahuvrihi.py)

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

Do not transfer P4 Cohen-k threshold onto bahuvrihi. Honest-limit articles that already refuse a census are NOT automatic kill_gated.

## Escalate path

@DECIDE: keep as limit-candidate → visa sheet, or rule kill_gated only if a human adopts a written freeze criterion.

## Artifacts

- [`probe_freeze_bahuvrihi.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/probe_freeze_bahuvrihi.py) — regenerates JSON
- [`probe_freeze_bahuvrihi.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/probe_freeze_bahuvrihi.json) — machine record

_Dr. Mārcis Gasūns_
