# Future OxAlpha status gate design (NOT ENABLED)

_Created: 29-08-2026 · Last updated: 29-08-2026_

Handoff: [H3550](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3550-OxAlpha_SanskritGrammar_oxalpha-30d-risk-review-gate_26.08.26.md) · Companion report: [OXALPHA_RETROSPECTIVE_CODE_REVIEW_26-08-2026](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/reviews/OXALPHA_RETROSPECTIVE_CODE_REVIEW_26-08-2026.md)

**Status: design only. No workflow, no branch-protection rule, no required check was created or enabled by this document or its PR** — plan decision 12 and the autonomy contract («Never enable a workflow or protection rule») hold. Proof of non-enablement is at the end.

## Purpose

A repeatable independent review gate so future OxAlpha (or any second-opinion) passes over SanskritGrammar diffs are bounded, evidence-backed, and risk-scoped instead of ad-hoc — and so the in-window #870→#873 class (a broken import holding required CI red for four days) surfaces on the first offending PR, not days later.

## 1. Executable-code matching

A diff counts as **reviewable executable code** when any changed path matches:

```
scripts/**                      python pipeline, validators, guards
tools/**                        build/test tooling
pipelines/**                    pipeline contracts + schemas
packages/sg_tooling/src/**      workspace package code
src/**                          site JS (discovery.mjs, plugins)
apps/site/**                    site config, remark plugins
patches/**                      vendored-behavior patches (behavior-bearing by definition)
.github/workflows/**            CI/deploy (production config)
docusaurus.config.mjs · sidebars.mjs
tests/**                        reviewed as spec evidence, not as churn
```

Excluded by default (decision 5): generated book `.mdx` extractions, `sangram/editorial/data/consolidation_ledger.json` and other derived stores, `data/**` generated datasets, `content/**`, `*.min.js`, lockfiles, `CHANGELOG*`, `.ai_state.md`. A slice consisting only of excluded paths is **not reviewed as executable code**; it is listed in the report with an explicit exclusion note. Derived-file drift is handled by its committed generator gate (e.g. `consolidation_ledger_refresh.py --check`), not by re-reviewing the artifact.

## 2. Independent required status check (design)

When enabled later, the gate would be a **separate workflow job** `oxalpha-review-gate` that runs on a pull_request event and posts exactly one of three conclusions as a check run:

| Conclusion | Condition |
|---|---|
| `pass` | Every retained slice has separate Standards and Spec verdicts with evidence links |
| `fail` | Any finding lacks severity/location/failure-mode/repro, or a P0/P1 lacks a regression test — posted on the first offending PR (the #870 lesson) |
| `skip` | Diff matches no executable-code pattern (exclusion note posted as the run summary) |

Independence rule: the gate's verdicts must cite hunks and spec quotes produced **without access to the author session's reasoning** — inputs are the diff, the linked spec surfaces (PR body → issue → handoff/plan → matching doc), and committed tests only. The job would be added to `.github/workflows/ci.yml` as a new job id, marked non-required initially, and flipped to required in branch protection **by a human**, as its own audited step.

## 3. Added human approval for integrity/production/data-truth paths

This repo has no money contour; its human-approval analogue covers the surfaces where a wrong merge damages trust in published data or repo integrity:

```
.github/workflows/**                       deploy + CI mutation
scripts/pre_push_stale_base_check.py       repo-integrity guards
scripts/eol_census.py · .githooks/**
scripts/check_claims_consistency.py        published-figure truth gates
*/claims.yml (gate logic changes, not content edits)
scripts/refresh_published_figures.py       cross-repo figure ingestion
scripts/build_lessonpack.py                student-facing generation
```

Those slices require, on top of a green gate: (a) regression tests proving fail-before/pass-after, and (b) explicit human approval recorded in the PR body before merge. Claim VALUES remain governed by the existing claims/ledger gates and human editorial visas — this gate never adjudicates scholarship, only engineering evidence.

## 4. Rollout plan (future, human-triggered)

1. Land this design doc (no code).
2. A separate PR adds the workflow job with `required: false`; one dogfood run against a docs-only PR must conclude `skip`.
3. Two-week soak with weekly verdict audits (compare gate verdicts against human review of the same PRs).
4. Human flips the protection-rule requirement; rollback = untick the required check (no history rewrite, no force events).

## Rollback

Deleting the job from `ci.yml` fully disables the gate; because nothing here touches branch protection, default-branch merges never depended on it at design time.

## Proof of non-enablement

This PR contains only `docs/OXALPHA_STATUS_GATE_DESIGN_2026.md` (+ changelog/ledger). `git diff --name-only` against base shows no `.github/workflows/**` path, no `.githooks/**` mutation, and no protected-branch change.

_Dr. Mārcis Gasūns_
