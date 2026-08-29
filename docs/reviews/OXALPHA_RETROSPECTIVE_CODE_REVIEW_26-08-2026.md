# SanskritGrammar OxAlpha 30-day retrospective code review (26-07-2026 .. 25-08-2026)

_Created: 29-08-2026 · Last updated: 29-08-2026_

Handoff: [H3550](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3550-OxAlpha_SanskritGrammar_oxalpha-30d-risk-review-gate_26.08.26.md) · Plan: [PLAN_SANSKRITGRAMMAR_OXALPHA_CODE_REVIEW_HARDENING_2026Q3](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_OXALPHA_CODE_REVIEW_HARDENING_2026Q3.md) · Window: **26-07-2026 .. 25-08-2026** (merged-at UTC) · Executor: OxAlpha `x-preview-f-free` (opencode, glm-5.3-flash).

## Method

Independent passes per slice: **Standards** (named rule/smell + exact hunk, executable code only) and **Spec** (requirement quoted from the ruled source order: PR body → linked issue → handoff/plan → matching doc; `no spec available` otherwise). Generated/vendor/data-only churn excluded unless behavior changed (plan decision 5). Findings require severity, location, failure mode, and repro/test; only proven P0/P1 fixed, always with regression tests (decisions 9–10). Live checks run on the review worktree: `pwg_compound_split.py --selftest` (17/17), `build_lessonpack.py --check` (9/9 profiles), focused pytest (30 passed), full `python -m pytest tests/ --ignore=tests/site` (green), consolidation-ledger `--check` (PASS).

## Risk-ranked slices (10 retained, cap respected)

~130 PRs merged in the window; docs/release/churn PRs excluded. Retained, highest executable/critical-path risk first:

| # | PR | Merged | Base → head | Focus | Spec source (quoted requirement) | Spec | Standards |
|---|---|---|---|---|---|---|---|
| 1 | [#600](https://github.com/gasyoun/SanskritGrammar/pull/600) pre-push silent-revert guard + CRLF gate (re-merges [#865](https://github.com/gasyoun/SanskritGrammar/pull/865) `c44ab87b→7c804d30`, [#866](https://github.com/gasyoun/SanskritGrammar/pull/866) `c6297caf→716a69fa`, [#868](https://github.com/gasyoun/SanskritGrammar/pull/868) `001dea2d→feddea98`) | 08-06, 08-17 | `c913e4f6` → `50deae70` | repo-integrity infra, blocking hook | Body: «Warns when a push deletes lines the remote gained in the last 3 days and the pushed commits never reference them»; H2301 half «BLOCKS a push that would newly land a CRLF blob»; blocking-by-default re-promoted 16-08 per MG ruling (docstring history) | PASS | **FAIL → fixed** ([#888](https://github.com/gasyoun/SanskritGrammar/pull/888)) |
| 2 | [#578](https://github.com/gasyoun/SanskritGrammar/pull/578) validators: claims schema, CI gates, offline search (duplicate merge [#577](https://github.com/gasyoun/SanskritGrammar/pull/577) `97887245→518d76de`) | 08-02 | `7d8d8ef6` → `024b7c1b` | CI blocking gates | Body table: H1842 claims schema+validator wired into CI, H1839 pipeline tests, H1840 blocking validators, H1841 offline search | PASS | PASS |
| 3 | [#599](https://github.com/gasyoun/SanskritGrammar/pull/599) lunr `sa` patch — Devanagari offline search | 08-07 | `d2acfca0` → `9c3b3be0` | public site search | Body: «add 'sa' to the plugin's language list… patch-package around lunr-languages' lunr.sa hard dependency on the wordcut segmenter»; fixes the `\u11B00-\u11B09` unreachable-escape bug «which stopped the trimmer stripping ASCII punctuation… for every language the instant 'sa' is loaded» | PASS | PASS |
| 4 | [#589](https://github.com/gasyoun/SanskritGrammar/pull/589) whitney 15.csv headerless reader | 08-05 | `33101c96` → `f2d837cf` | data correctness → published claims | Body: «Its line 1 (`21865,158442,'likhyante',24,9,`) is a real finite-form row, silently discarded on every run… No published number changes — 690 before and after» | PASS | PASS |
| 5 | [#529](https://github.com/gasyoun/SanskritGrammar/pull/529) pwg_compound_split headword-anchored extraction (#527) | 07-26 | `3210d193` → `b01195ff` | parser feeding «high-precision splitter gold» | Body: «Anchor on the entry's own `{#headword#}¦`, blank every balanced `[...]`, split the balanced paren at depth 0… 344/16,738 rows (2.06 %)» shipped wrong members pre-fix; drop-never-guess policy | PASS | PASS |
| 6 | [#848](https://github.com/gasyoun/SanskritGrammar/pull/848) H2309 Slice A: uv workspace + sg_tooling + contracts | 08-09 | `83fe9be1` → `c6c006b6` | build-system restructure | Body: «Steps A1, A2 and A4 of Slice A… `uv sync --frozen` installs one exact graph… csl-pyutil pinned by immutable commit d6cbe911… A5/A6 deliberately not here» | PASS | PASS |
| 7 | [#849](https://github.com/gasyoun/SanskritGrammar/pull/849) H2528 same-SHA Pages gating | 08-09 | `0e0204b1` → `52b00d4e` | production deploy surface | Body: «A6 one-run exact-SHA Pages gating with a deliberately-red control»; artifact SHA must equal `github.sha` before deploy | PASS | PASS |
| 8 | [#592](https://github.com/gasyoun/SanskritGrammar/pull/592) claims consistency across the VisualDCS boundary (H2298) | 08-06 | `335b21b5` → `4aef47ac` | blocking data-truth gate | Body: «check 2 already asserts… a figure reused across registers must be cited with ONE value everywhere… Its blind spot is reach, not logic»; pairs must be commensurable, «never edit a number to match» | PASS | PASS |
| 9 | [#882](https://github.com/gasyoun/SanskritGrammar/pull/882) LYW wave-1 lessonpack generator + 9 packs | 08-25 | `3a13f93a` → `2af73047` | student-facing generator (flag OFF) | Body: «deterministic assembler/validator (`--check` / `--build` / `--emit-checklist`)… 9 committed pack profiles… MG sign-off required before flipping `LYW_ENABLED=ON`… the agent never flips the flag» | PASS | PASS |
| 10 | [#590](https://github.com/gasyoun/SanskritGrammar/pull/590) visa-sheet screening wire (H2039) | 08-05 | `61c3f3d9` → `af5d89e6` | editorial review-sheet pipeline | Body: «`render_review_sheet` now requires `screening=` when `extras=True` (H1649)… `build_screening(spec)` reports the honest state… `human=len(items)`» | PASS | PASS |

## Findings

### F1 — P1 — stale-base guard miscounts removals after a removed `--`-prefixed line — **FIXED** [PR #888](https://github.com/gasyoun/SanskritGrammar/pull/888) (merged `05aa969`)

- **Where:** [scripts/pre_push_stale_base_check.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/pre_push_stale_base_check.py) `removed_line_numbers()` (~line 139 at slice SHA `feddea98`); live on main at review time.
- **Failure mode:** the `---`/`+++` **file-header** test ran on every diff line. Inside a hunk, a removed line whose *content* starts with `--` (a Markdown `---` rule, a `-- comment`) is emitted as a `---…` line, so it was (a) dropped from the removal set and (b) never advanced `old_line` — every later removal in the same hunk was reported at a shifted number. The blocking guard then blamed and survivor-checked the wrong lines: real silent reverts slip through (false negative on the exact Uprava#1516 class the hook exists to catch) and unrelated lines can be misattributed (false positive).
- **Repro/test:** parser-level, deterministic. Hunk `@@ -10,3 +10,2 @@` with removed lines `row A`, `----` (content `---`), `row C` → scanner returned `[10, 11]`, correct answer `[10, 11, 12]`. Regression tests `tests/test_pre_push_stale_base_check.py` — 3 of 5 fail on the pre-fix scanner, 5/5 pass after; full local suite green; CI green on the PR.
- **Fix:** headers recognized only before the first hunk (`seen_hunk` state). One branch + comment; no change for any existing diff shape.
- **Residual (tracked, not a stop):** the canonical copy is `Uprava/scripts/pre_push_stale_base_check.py` (PR #600: «edit there and re-run the deploy, do not fork per repo»). The same fix + org re-deploy is owed in Uprava — GTD row minted 29-08-2026.

**No other proven P0/P1** in the retained set. The stop-condition ledger (plan autonomy contract: secrets/PII, production state, irreversible migration, unclear money, generated bulk) has no entries — no fix was stopped.

## Observations (below fix bar, recorded only)

| ID | Sev | Slice | Observation |
|---|---|---|---|
| O1 | LOW (process) | #577/#578 | The validator bundle was merged twice five minutes apart (08-02 17:24Z and 17:29Z); #578 is a superset of #577 (adds one `GasunsDhatu_2014` mdx fix). No live defect — both trees on main are content-consistent — but the double merge defeated the one-PR-one-merge shape and doubled CI cost |
| O2 | MED-LOW (interface invariant) | #882 | `quizzes.json` ships `answer_keys` in the same artifact as student-facing items; safety depends on the Systema consumer stripping keys server-side before serving (its LYW spec: «Quiz answer keys never leave the server»). Keep as a stated cross-repo invariant whenever the pack schema evolves; `LYW_ENABLED` remains default-OFF with MG sign-off owed before flip |
| O3 | MED (in-window, already repaired) | #870/#873 | #870 (18-08) imported a non-existent `RU_UI_STRINGS` from pinned csl-pyutil → required CI red from `57dadc4` until #873 (22-08) defined the chrome locally. Fixed inside the window with a regression-tolerant local definition; no live defect on main. Recorded because four days of unmergeable PRs is the cost class the future gate's `fail` verdict is designed to surface early |

## Exclusions (no executable-impact review)

- Book `.mdx`/curriculum/methodichka prose mega-PRs (#525, #549, #553, #565, #572, #574, #862, #863, #869, #881): content-only, no behavior change.
- Generated/data churn: `pwg_compound_splits.tsv` (+1018/−651, derived by reviewed #529 code), atlas bundle regeneration (#878/#879 — reviewed as its generator's output), consolidation_ledger.json refreshes (derived, CI-gated), Grammar Lab export bundle inside #857.
- Release/version chores (#531, #535, #550–#562, #571, #583, #587, #594, #596, #598, #602, #606–#611, #847, #851, #859, #872, #880) and CI-clip PRs (#564 changelog-dup guard — reviewed as part of #578's CI-gate family, #569 pre-commit config, #580/#850 action pins — supply-chain clips with no repo code change).
- #864 (GOST bibliography checker, +3750): new standalone checker harness; excluded from the retained ten by the risk cap — its failure surface is bounded to the M03 freeze artifact and it carries its own test suite.

## No-spec outcomes

None — all ten retained slices carried PR-body specs resolving the ruled order at its first step.

## Adapter bootstrap

[PR #887](https://github.com/gasyoun/SanskritGrammar/pull/887) merged as [`981d66e`](https://github.com/gasyoun/SanskritGrammar/commit/981d66e): canonical Matt Pocock GitHub-issue-tracker adapter under `docs/agents/` (intake OFF), `## Agent skills` block in CLAUDE.md, five triage labels live (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), plus this repo's previously-missing five-document plan family.

## Verdict sanity

The retained set is unusually hardened (the guard family alone absorbed four fix rounds inside the window, and every generator ships with a selftest/validator). One live P1 was still found and fixed with a fail-before/pass-after regression test; three lower-severity observations are recorded with evidence and none were silently promoted or dropped.

_Dr. Mārcis Gasūns_
