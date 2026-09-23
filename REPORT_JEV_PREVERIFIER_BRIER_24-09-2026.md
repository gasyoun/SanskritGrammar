# REPORT — H5276 Jev Noul pre-verifier gate + Brier (measurement only)

_Created: 24-09-2026 · Last updated: 24-09-2026_

Handoff: H5276 · Shared client: Uprava tools/jev_probe.py (H5275) · Model: jev-1.13.0
Question (per settled claim): "Is the claim as stated supported by the cited evidence passage? Give the probability that the evidence passage supports the claim as stated."
Registries (frozen, read-only): WhitneyGrammar_1889 + ZalizniakOcherk_1978 + ZalizniakKonspekt_2004

## Verdict (measurement only — gate wiring itself stays a human decision)

- **Keep-all-true recall ≥99%:** t=0.3: PASS | t=0.5: FAIL | t=0.7: FAIL → **GO**; wiring candidate = t=0.3 (highest passing threshold).
- TRUE-verdict claims falling below each threshold (the gate's known losses): t=0.3: WH-15; t=0.5: OCH-39, OCH-6, OCH-62, OCH-82, WH-10, WH-14, WH-15; t=0.7: KZ-16, KZ-17, KZ-2, KZ-5, KZ-7, OCH-11, OCH-18, OCH-32, OCH-36, OCH-39, OCH-4, OCH-42, OCH-54, OCH-59, OCH-6, OCH-62, OCH-71, OCH-79, OCH-82, OCH-84, OCH-86, OCH-95, WH-10, WH-13, WH-14, WH-15. At t=0.3 the margin is one claim (WH-15, noul 0.25) — 0.991 vs the 0.99 bar is razor-thin.
- Brier (TRUE=1 vs rest=0): **0.071** · TRUE-vs-FALSE only: **0.077** (1 FALSE claim only — indicative, not decisive).
- Cost: Jev **$0.03/1000** (measured from usage) vs Sonnet paired-verifier est. **$4.93/1000** ($3.0/M in + $15.0/M out, +250 tok prompt, 150 tok out — ESTIMATE, not a bill).
- At t=0.3 the gate flags ALL OVERSTATED (4) + the single FALSE (OCH-67, noul 0.04) + 9/11 UNTESTABLE for paid verification — the pre-verifier would have caught every non-TRUE verdict in this set while clearing 111/112 TRUE claims.

## Precision/recall sweep (positive = noul ≥ t vs verdict_fact TRUE)

| t | TP | FP | FN | TN | precision | recall (keep-all-true) | share sent to paid verifier | gate $/1000 (Jev+Sonnet) | savings vs Sonnet-only /1000 |
|---|----|----|----|----|-----------|------------------------|------------------------------|--------------------------|------------------------------|
| 0.3 | 111 | 0 | 1 | 16 | 1.000 | **0.991** | 13.3% | $0.68 | $4.25 |
| 0.5 | 105 | 0 | 7 | 16 | 1.000 | **0.938** | 18.0% | $0.91 | $4.01 |
| 0.7 | 86 | 0 | 26 | 16 | 1.000 | **0.768** | 32.8% | $1.64 | $3.28 |

## Per-verdict-class Noul calibration

| verdict_fact | n | mean | min | max |
|---|---|---|---|---|
| TRUE | 112 | 0.756 | 0.250 | 0.940 |
| OVERSTATED | 4 | 0.080 | 0.050 | 0.110 |
| FALSE | 1 | 0.040 | 0.040 | 0.040 |
| UNTESTABLE | 11 | 0.172 | 0.100 | 0.250 |

## Reliability bins

| bin | n | share TRUE | mean noul |
|---|---|---|---|
| 0.0-0.1 | 3 | 0.00 | 0.047 |
| 0.1-0.2 | 9 | 0.00 | 0.136 |
| 0.2-0.3 | 6 | 0.33 | 0.240 |
| 0.3-0.4 | 4 | 1.00 | 0.335 |
| 0.4-0.5 | 2 | 1.00 | 0.440 |
| 0.5-0.6 | 3 | 1.00 | 0.553 |
| 0.6-0.7 | 16 | 1.00 | 0.649 |
| 0.7-0.8 | 32 | 1.00 | 0.757 |
| 0.8-0.9 | 47 | 1.00 | 0.842 |
| 0.9-1.0 | 7 | 1.00 | 0.914 |

## Contract compliance

- Registry edits: **none** — measurement only (claims.yml files untouched).
- Key: TYPESAFE_API_KEY from ~/.secrets/typesafe.env, never echoed.
- Raw per-claim results: jev_preverifier_results_2026-09-24.json (same dir).
- NO-GO = no threshold keeps ≥99% of TRUE-verdict claims above the gate; gate wiring stays unwired either way until a human rules.

_Гасунс_
