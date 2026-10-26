# SanskritGrammar eval harness

_Created: 26-10-2026 · H6846 (eval-harness scaffold rollout)_

Minimal, deterministic eval scaffold over gold this repo already commits. It
creates no new gold and adds no annotation.

## Suite `ud-claims-probe`

Replays the pre-registered UD_Sanskrit-UFAL claims register
([`data/ud_sanskrit/claims.yml`](../data/ud_sanskrit/claims.yml)) through
[`tools/verify_claims_ud.py`](../tools/verify_claims_ud.py) and grades the live
dual verdicts (`verdict_fact` / `verdict_ud`) against the frozen register:

| Claim | Expected |
|---|---|
| UDA-1 ca-position | TRUE / PASS |
| UDA-2 OV order | TRUE / PASS |
| UDA-3 verbless roots | TRUE / PASS |
| UDA-4 top lemma | OVERSTATED / OVERSTATED |

UDA-4 is deliberately OVERSTATED on both axes — a canary that asserted "all
PASS" would be lying about the register. Gold provenance: H6842 WHEEL9 item
(b), UD_Sanskrit-UFAL mirror commit `80f88c8`, CC BY-SA 4.0; thresholds were
fixed before the first probe run.

## Run

```sh
python evals/run_eval.py            # live probe replay
python evals/run_eval.py --canary   # replay matches AND a flipped verdict fails
```

`--canary` flips one replayed UD verdict and requires the grader to reject it.
Exit code 0 means the replay matched (and, with `--canary`, the mutation was
caught).

The same command runs on PRs and pushes touching `evals/`, `data/ud_sanskrit/`
or `tools/verify_claims_ud.py` via `.github/workflows/eval-canary.yml`.

_Dr. Mārcis Gasūns_
