# H2355 CI acceptance — 3 consecutive green `origin/main` Python unit tests

_Created: 07-08-2026 · Last updated: 07-08-2026_

**Executor:** Grok 4.5 (`grok-4.5`) · optional residual after midway resume of the H2355 cut-release session.

**Handoff:** [H2355](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H2355-Sonnet_SanskritGrammar_csl-pyutil-pin-bump-visa-sheet-screening_07.08.26.md) (**Sonnet 5**) — Bump `csl-pyutil` pin past v0.3.0 to restore `render_review_sheet(screening=)` CI.

**Goal line under test:** `python -m pytest tests/test_visa_sheet_generator.py` green in CI **and** green on **3 consecutive** `origin/main` runs (no `TypeError: ... screening`).

## Verdict

**PASS.** More than three consecutive post-pin `origin/main` CI runs show **Python unit tests = success**, suite **`213 passed, 5 skipped, 1 warning`**, with `tests/test_visa_sheet_generator.py` executing. The only residual signal is the known **`PreflightWarning`** for missing `manifest=` (csl-pyutil V9 / H1889 migration ramp → hard error only in csl-pyutil 1.0.0) — not a regression of the H2355 `screening=` pin fix.

`origin/main` tip at measurement: `432df05` ([#608](https://github.com/gasyoun/SanskritGrammar/pull/608)).

## Evidence table (newest first)

| # | Commit | PR / subject | Python unit tests | Suite line (log) | Job URL |
|---|---|---|---|---|---|
| 1 | `432df05` | [#608](https://github.com/gasyoun/SanskritGrammar/pull/608) changelog Unreleased dedupe | **success** | `213 passed, 5 skipped, 1 warning` · `test_visa_sheet_generator.py::test_sheet_identity_survives` ran (PreflightWarning only) | [job 92923866857](https://github.com/gasyoun/SanskritGrammar/actions/runs/31195888426/job/92923866857) |
| 2 | `c5bba0e` | [#607](https://github.com/gasyoun/SanskritGrammar/pull/607) same Unreleased clear (concurrent) | **success** | same shape | [job 92922804255](https://github.com/gasyoun/SanskritGrammar/actions/runs/31195565567/job/92922804255) |
| 3 | `bece03b` | [#606](https://github.com/gasyoun/SanskritGrammar/pull/606) release v0.121.3 | **success** | same shape | [job 92857517914](https://github.com/gasyoun/SanskritGrammar/actions/runs/31175832164/job/92857517914) |
| 4 | `1a80230` | [#605](https://github.com/gasyoun/SanskritGrammar/pull/605) H2355 docs prop | **success** | same shape | [job 92856543503](https://github.com/gasyoun/SanskritGrammar/actions/runs/31175515328/job/92856543503) |

Pin merge: [#604](https://github.com/gasyoun/SanskritGrammar/pull/604) `csl-pyutil@v0.3.0` → `v0.9.0`. Release: [v0.121.3](https://github.com/gasyoun/SanskritGrammar/releases/tag/v0.121.3).

## What was ruled out

- **`TypeError: unexpected keyword argument 'screening'`** — the pre-pin main breakage — does **not** appear in any of the four post-pin job logs above.
- Changelog lint was red on the release tip alone (`bece03b`, duplicate Unreleased bullet); that is orthogonal to the visa-sheet suite and was fixed by #607/#608. Current tip: Changelog lint **success**.

## Reproduce

```text
# tip checks
gh api repos/gasyoun/SanskritGrammar/commits/432df05/check-runs
gh run view 31195888426 --repo gasyoun/SanskritGrammar
# log grep (job id from view):
gh api repos/gasyoun/SanskritGrammar/actions/jobs/92923866857/logs | findstr /i "visa_sheet TypeError passed"
```

_Dr. Mārcis Gasūns_
