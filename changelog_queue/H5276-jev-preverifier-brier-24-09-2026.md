### Added
- **H5276 (OxAlpha `opencode/z-ai/glm-5.3-flash`): Jev Noul pre-verifier gate + Brier measured on the frozen claim registers (24-09-2026).**
  [`scripts/jev_claims_preverifier.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/jev_claims_preverifier.py)
  — dry-run-default runner asking TypeSafe Jev Noul (jev-1.13.0, shared client Uprava
  `tools/jev_probe.py` H5275) "is the claim as stated supported by the cited evidence passage?"
  per settled claim across WhitneyGrammar_1889 + ZalizniakOcherk_1978 + ZalizniakKonspekt_2004
  (128 claims, one call each, retry ×3 backoff, cost from usage). Measurement only — **no registry
  edits**. Results
  ([report](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_JEV_PREVERIFIER_BRIER_24-09-2026.md) +
  [raw JSON](https://github.com/gasyoun/SanskritGrammar/blob/main/jev_preverifier_results_2026-09-24.json)):
  keep-all-true recall **0.991 at t=0.3 (PASS the ≥0.99 gate-wiring bar**, sole miss WH-15 noul 0.25 =
  conservative escalation), t=0.5 0.938 / t=0.7 0.768 FAIL; precision 1.000 at all three (0 FP);
  Brier 0.071; per-class separation TRUE 0.756 vs OVERSTATED 0.080 / FALSE 0.040 / UNTESTABLE 0.172 —
  all 5 non-TRUE verdicts ≤0.11, all flagged for paid verification at t=0.3. Cost: Jev **$0.03/1000**
  (measured) vs Sonnet paired-verifier est. $4.93/1000; gate scenario t=0.3 → $0.68/1000.
  Independently verified (DeepSeek councillor, paired-verifier family): all headline figures
  recomputed from raw JSON — PASS; two cosmetic defects fixed post-review. [PR #950](https://github.com/gasyoun/SanskritGrammar/pull/950) — open, not yet merged.
