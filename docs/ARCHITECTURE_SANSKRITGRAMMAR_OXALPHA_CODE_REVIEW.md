# SanskritGrammar OxAlpha code-review architecture

_Created: 29-08-2026 · Last updated: 29-08-2026_

1. Canonical [issue tracker](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/agents/issue-tracker.md), [triage labels](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/agents/triage-labels.md), and [domain rules](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/agents/domain.md).
2. Bounded risk selector: executable and critical-path exposure outranks churn; generated/vendor/data-only PRs are excluded unless executable behavior changed.
3. Standards reviewer: repository rules plus smell baseline, verdict per exact hunk.
4. Spec reviewer: ruled evidence chain (PR body → issue → handoff/plan → matching doc); no evidence becomes `no spec available`.
5. [Evidence ledger](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/reviews/OXALPHA_RETROSPECTIVE_CODE_REVIEW_26-08-2026.md) preserving axes, exclusions, exact SHAs, and proof.
6. Fix lane: only proven P0/P1, one minimal regression-tested PR per defect.
7. Inactive [future-gate design](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/OXALPHA_STATUS_GATE_DESIGN_2026.md).

Each manifest row records PR, base/head SHA, executable paths, exclusions, reasons, spec source, and both review states. Findings require severity, exact location, failure mode, and repro/test. Future check states are pass, evidence-backed fail, or skip — never silent success.

Prior art: the sibling batch (Systema H3546, kosha H3549) ships the same adapter and two-axis review; this repo reuses that shape and builds only its own selection, evidence, fix, and gate-design layers.

_Dr. Mārcis Gasūns_
