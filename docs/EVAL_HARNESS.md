# Eval harness note (H6846)

_Created: 26-10-2026_

`evals/` now carries the repo's first eval scaffold, a deterministic canary
over the pre-registered UD claims probes:

- suite manifest: [`evals/manifest.json`](../evals/manifest.json)
- runner: [`evals/run_eval.py`](../evals/run_eval.py) (`--canary` proves the
  grader goes red on a flipped verdict)
- gold: [`data/ud_sanskrit/claims.yml`](../data/ud_sanskrit/claims.yml) —
  existing H6842 register over the UD_Sanskrit-UFAL mirror, not new annotation.

The suite replays the live probe engine and expects the register's own verdicts,
including UDA-4's deliberate OVERSTATED. Scope is deliberately narrow: it
guards register/engine drift, not the philological reading of each claim. Any
new capability suite over the other `claims.yml` registers needs a separately
pre-registered reference solution and negative class (H6714).

CI: [`.github/workflows/eval-canary.yml`](../.github/workflows/eval-canary.yml)
runs the canary on PRs and pushes that touch `evals/`, `data/ud_sanskrit/` or
`tools/verify_claims_ud.py`.

_Dr. Mārcis Gasūns_
