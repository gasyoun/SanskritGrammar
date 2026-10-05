_Created: 05-10-2026 · Last updated: 05-10-2026_

# BUGHUNT-FINDINGS-SanskritGrammar-05.10.2026

Nightly one-repo bug hunt (MG ruling 26-09-2026: nightly, one repo, auto-fix HIGH). Hunt scope:
hand-written code only — `src/ tools/ scripts/ packages/ apps/` (~162 py/mjs/jsx files), generated
data (`src/components/talmud/*Data.js`), `node_modules/`, `build/`, `archive/`, vendored textbook
corpora all skipped. Every finding below carries live evidence actually executed this pass.
Executor: OxAlpha (`opencode/z-ai/glm-5.3-flash`).

## Findings (ranked)

### F1 — HIGH — committed test suite red at HEAD: `article_validate --self-test` broke at the 05-10-2026 freeze lift (FIXED this pass)

- Location: [scripts/article_validate.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/article_validate.py#L313-L338) (`self_test()`, H1260 freeze cases) + [tests/test_article_validate.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_article_validate.py#L29).
- What breaks: `python3 -m pytest tests/test_article_validate.py::test_self_test` FAILS on a clean
  checkout at `origin/main` (391fb14): `SELF-TEST FAIL: mutation 'new toc_ref outside the frozen
  H1260 baseline, freeze active' should fail but passed` + `could not load the real freeze ledger
  for the positive self-test (active=False, warn=None) — freeze gate is untestable` → 14/16.
- Root cause (proven, not guessed): the negative/positive H1260 cases deliberately use the REAL
  [consolidation_ledger.json](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/data/consolidation_ledger.json)
  "so a stale/mis-generated ledger would surface here too" — but that design assumed the freeze was
  permanently active. This morning's C5/C6 freeze lift ([PR #1015](https://github.com/gasyoun/SanskritGrammar/pull/1015),
  commit 3173bd2, MG in-chat ruling) flipped `freeze.active` `True → False` (both states probed
  from git: pre-lift `active=True`, post-lift `active=False` with lift provenance). The post-lift
  validation was `article_validate --all` PASS — the self-test was never re-run.
- Impact: every fresh-clone CI/pytest run of the repo is red; the freeze gate's own regression
  harness is dead (its explicit self-description: "freeze gate is untestable").
- Fix (this pass): the gate cases now run against a SYNTHETIC frozen ledger injected over
  `load_freeze_baseline` (same `validate()` code path, independent of the on-disk freeze state —
  the real ledger's `active` flag is mutable operational state since the lift and can no longer be
  a fixture for an always-frozen expectation); a new state residual still watches the REAL ledger
  (`active=true` + empty allowed set ⇒ failure), preserving the original stale-ledger tripwire.
- Verification: `python3 scripts/article_validate.py --self-test` → `PASS 16/16 checks green`;
  full suite diff vs unmodified-HEAD baseline shows zero new failures.

### F2 — HIGH — `scripts/site_tools.py` npm build ran `shell=True` with a list: documented `site` command could never succeed on POSIX (FIXED this pass)

- Location: [scripts/site_tools.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/site_tools.py#L102-L103) (`site()`, the README-documented one-command book-site flow).
- What breaks: `subprocess.run(["npm", "run", "build"], shell=True)` — on POSIX, list-argv +
  `shell=True` executes only `argv[0]` as the shell command (`sh -c npm run build` → bare `npm`;
  "run build" become `$0`/`$1` of the shell, silently dropped). Live probe: `["echo","X"]` +
  `shell=True` → stdout `"\n"`, argument gone. So `npm` ran bare, no Docusaurus output, the
  `"[SUCCESS] Generated static files"` check always failed → `site()` always returned False:
  the gate was permanently red and dead weight. (Repo's own P1 heuristic table flags exactly this
  pattern — [scripts/oxalpha_gate_review.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/oxalpha_gate_review.py#L54).)
- Fix (this pass): `shell=True` dropped (comment left in place). Verification: `py_compile` green +
  end-to-end shim probe (fake `npm` on PATH echoing args + SUCCESS marker) → `[site] build: GREEN`,
  `site()` returned `True`. Full real Docusaurus build not re-run in-hunt (no `node_modules` in the
  hunt worktree); the argv-delivery mechanism is what was broken and is now proven fixed.

### F3 — LOW — broad `except` maps every validator crash to `"unknown"` (report only, no code edit)

- Location: [scripts/consolidation_ledger_refresh.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/consolidation_ledger_refresh.py#L318-L328) (`compute_validator_evidence`).
- Any exception (decode error, IO error, schema blow-up) collapses to
  `{"article_validate": "unknown"}` — a deliberate fail-open contract, but it masks a broken
  validator as "unknown" telemetry indefinitely. Suggestion only: narrow to
  `(json.JSONDecodeError, OSError, AttributeError)` so programming errors surface.

### F4 — LOW — atlas e2e tests are red in a lived-in tree, green on clean checkout (pre-existing, report only)

- 5 tests (`test_atlas_build_bundle*` e2e/sidecar) FAIL in the main working tree (local
  `node_modules`/`.docusaurus`/build artifacts present) and PASS in a fresh worktree of the same
  commit. Not a committed-code defect; noted so nobody chases them on a dirty tree. Baseline
  evidence: identical suite run on unmodified HEAD vs fresh worktree this pass.

## What verified green

- No committed secrets (pattern sweep over all four code dirs: none), no `os.system`, no
  unguarded `eval/exec`; the only `shell=True` in code was F2 (fixed).
- [scripts/git_ops.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/git_ops.py)
  (GIT_* env seam), `topological_order` in
  [packages/sg_tooling](https://github.com/gasyoun/SanskritGrammar/blob/main/packages/sg_tooling/src/sg_tooling/domain/__init__.py#L73-L94)
  (cycle + unknown-dep + determinism), all `[i+1]` indexing sites (bounds-guarded),
  `check_claims_consistency.blocks()` (capture-group re.split keeps odd length), `images()` glob
  (guarantees the `_media` ancestor) — audited, clean.
- Suite on clean checkout: `7 failed / 374 passed / 7 skipped / 23 errors` pre-existing at HEAD in
  the lived-in tree, `0` new failures from this pass's fixes; self-test 16/16; both fixed files
  `py_compile` green.

## Autonomy notes

- Both HIGH findings are CODE bugs → auto-fixed per MG ruling 26-09-2026, max-3-attempts budget
  unused (1 attempt each, both green first try). No credential/infra HIGH found ⇒ no GTD `@DO`
  mint this pass. F3/F4 report-only. CHANGELOG bullet landed via
  `changelog_queue/2026-10-05-bughunt-high-fixes.md` (the repo's documented CHANGELOG route).
- Fixes land in this report's PR (branch `bughunt-2026-10-05`, worktree off `origin/main` 391fb14).

Elapsed: hunt+report+fixes ≈ 48 min wall (start 07:25, end 08:13 +0300).

_Гасунс_
