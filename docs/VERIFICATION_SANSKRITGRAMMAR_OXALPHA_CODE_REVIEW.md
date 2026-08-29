# SanskritGrammar OxAlpha code-review verification and risks

_Created: 29-08-2026 · Last updated: 29-08-2026_

| Deliverable | Proof | Failure |
|---|---|---|
| Adapter | Three docs, one Agent skills block, five labels, intake OFF | Missing/duplicate config |
| Selection | Zero to ten fixed-window rows with risk evidence | Churn substituted for risk |
| Standards | Rule or named smell plus exact hunk | Generic advice |
| Spec | Quoted requirement or no spec available | Inference as fact |
| Finding | Severity, location, failure mode, repro/test | No reproducible evidence |
| Fix | Regression fails before and passes after; CI green | Untested/fenced mutation |
| Design | Rollout and rollback; no activation | Workflow/protection enabled |

Verification: run the slice selftests (`pwg_compound_split.py --selftest`, `build_lessonpack.py --check`), the focused pytest set, then the full `uv run python -m pytest`; run `git diff --check`; verify full links.

Risks: generated `.mdx`/bundle churn mistaken for executable change; csl-orig read-only fence; the stale-base guard blocking its own fix landing (escape hatch `ALLOW_STALE_BASE_PUSH=1`); duplicate merges (#577/#578) counted twice; pre-existing red CI at slice SHAs read as a slice defect. Exclude generated/data mega-PRs and never mutate generated surfaces.

Autonomy gate: PASS when every wave deliverable has architecture, ordered steps, command-level acceptance, and named risks; no blocking decision remains.

_Dr. Mārcis Gasūns_
