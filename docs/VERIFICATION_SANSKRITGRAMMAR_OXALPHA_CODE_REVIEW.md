# SanskritGrammar OxAlpha code-review verification and risks

_Created: 26-08-2026 · Last updated: 26-08-2026_

## Acceptance

| Deliverable | Proof | Failure |
|---|---|---|
| Adapter | Three docs, one Agent skills block, five labels, PR intake OFF | Missing or duplicate config |
| Selection | Zero to ten fixed-window rows with risk evidence | Churn substituted for risk |
| Standards | Rule or named smell plus exact hunk | Generic advice |
| Spec | Quoted requirement or no spec available | Inference presented as fact |
| Finding | Severity, location, failure mode, repro/test | No reproducible evidence |
| Fix | Regression fails before and passes after; CI green | Untested or fenced mutation |
| Gate design | Rollout and rollback; no activation | Workflow/protection enabled |

## Commands

Run uv sync --frozen, uv run python -m pytest, uv run sg pipeline list, the validators in CI, npm ci, npm run test:site, npm run typecheck, and npm run build. Run git diff --check and verify all full links.

## Risks and fence

source/generated confusion; SG-MO-021 hard cutover; DCS adapter assumptions; self-confirming golden fixtures; Pages artifact identity. Do not edit generated MDX or exercise JSON unless executable behavior depends on it.

## Stop policy and autonomy gate

Stop only the affected fix for the ruled hazards and continue safe slices. PASS: every wave-1 item has architecture, ordered steps, command-level acceptance, and named risks; no blocking decision remains.

_Dr. Mārcis Gasūns_
