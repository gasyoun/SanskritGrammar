# H2528 Slice A dual-run reconciliation

_Adjudicated 09-08-2026 by Codex Sol (`gpt-5.6-sol`)._

## Frozen lanes

| Lane | Provenance | Frozen result |
|---|---|---|
| Intended-tier independent lane | Codex Sol (`gpt-5.6-sol`) · branch `codex/h2528-independent-21976` · `e4f9ca5` · parent `83fe9be` | Pushed before PR #848's diff was inspected; no PR |
| Override lane | Fable 5 (`claude-fable-5`) · PR #848 · `c6c006b` · parent `83fe9be` | Merged to `main` as `0e0204b` |

The lanes were independently implemented from the same pre-#848 parent. The
Codex lane's `uv sync --frozen` was inconclusive after three PyPI wheel transport
timeouts; its focused 7 Python + 3 Node tests and TypeScript check passed. The
override lane's recorded full gate was 258 Python and 68 Node tests plus build.

## Inventory and adjudication

| Area | Class | Adjudication |
|---|---|---|
| Immutable `csl-pyutil` commit `d6cbe911…` | identical | Double-verification recorded: both lanes independently resolved the annotated `v0.9.0` tag to the same commit rather than pinning its tag object. |
| Workspace, package layers, and `sg` entry point | equivalent | Override lane retained: it implements the same five-layer boundary with fuller package metadata and integration tests. |
| Strict pipeline/work schemas; `rights: unknown` representable | equivalent | Override lane retained: both preserve unknown without treating it as permission; its schema vocabulary and fixtures are more complete. |
| Graph invariants | equivalent | Override lane retained: both reject duplicate IDs, cycles, self/unknown dependencies, multiple producers, and input/output overlap; its validator reports accumulated errors rather than the Codex lane's first error. |
| Validator dependency path | conflicting | Override lane wins: optional real `jsonschema` plus a bounded fallback keeps the installed CLI usable in minimal environments while CI still exercises Draft 2020-12; the Codex single-path pin was simpler but less portable. |
| CLI exit-code meaning | conflicting | Override lane wins: `0` success, `1` validation/execution failure, `3` missing pipeline, `4` unreadable contract is the locked public contract; Codex used `4` for execution failure, which would break CI consumers. |
| `pipeline run` command resolution | conflicting | Override lane wins: registry-based generator resolution preserves the architecture's extension boundary and resolves every step before side effects; arbitrary executable lookup was broader than the declared trust boundary. |
| Discovery deny breadth and reporting | conflicting | Override lane wins: both report path-segment reasons, while override additionally denies suffix and bounded front-matter flags, fails closed on unreadable candidates, and has substantially broader fixtures. |
| Discovery/plugin tests | equivalent | Override lane retained as the larger set; both independently reproduce root/archive denials plus rstTable and heading-anchor behavior. |
| TypeScript opt-in seam | conflicting | Combined: override's explicit `.d.ts` checked-file seam remains canonical; Codex's `apps/site/` wrappers survive as the requested transition boundary without mass-converting JSX. |
| `scripts/site_tools.py` stale embedded scaffold | net-new Codex | Codex lane survives: PR #848 left the stale scaffold intact, contrary to A4; the reconciled tree removes it and delegates only to the canonical root build. |
| `repo-site.yml`, package README, layering/integration tests | net-new override | Kept unchanged from PR #848; no Codex counterpart. |
| A5 neutral rights footer/README | net-new reconciliation | Repository MIT licensing is separated from per-work text/source status; unknown is explicitly not permission and the footer links to provenance notes. |
| A6 same-SHA Pages workflow | net-new reconciliation | One required job installs both locks, runs all gates, builds and uploads the exact-SHA artifact; deploy needs that job/output and performs no checkout or rebuild. |
| Deliberately-red deployment control | net-new reconciliation | `workflow_dispatch.fail_required_gate=true` fails before upload; deploy therefore cannot run, and a structural test locks that order. |

Class totals: **1 identical · 4 equivalent · 5 conflicting · 5 net-new**.
Every conflicting item above has an explicit winner and rationale; no lane was
silently preferred.

## Reconciled-tree local evidence

- `uv sync --frozen` — pass from a fresh worktree.
- `uv run sg pipeline list` — `pipeline:repo-site` discovered.
- `uv run python -m pytest` — **261 passed**.
- full validator chain from `.github/workflows/ci.yml` — pass.
- `npm run test:site` — **68 passed**; `npm run typecheck` — pass.
- `npm run build` — `[SUCCESS] Generated static files in "build"`; rendered
  HTML contains the neutral MIT/per-work provenance footer.
- `tests/test_same_sha_workflow.py` — 3 passed, including the planted-red
  control ordering and the no-rebuild deploy assertion.

## Remote same-SHA evidence

- Delivery: [PR #849](https://github.com/gasyoun/SanskritGrammar/pull/849),
  repaired by [PR #850](https://github.com/gasyoun/SanskritGrammar/pull/850).
- Green main run [#928](https://github.com/gasyoun/SanskritGrammar/actions/runs/31334518093)
  on `132a620d368dae88b2c9db08161f1ecedd646aec`: required quality job passed,
  the downloaded artifact's `deployment-sha.txt` matched `github.sha`, the
  Pages artifact uploaded, and deploy consumed it without checkout or rebuild.
- Deliberately-red control [#930](https://github.com/gasyoun/SanskritGrammar/actions/runs/31334671187)
  on the same SHA: all substantive gates and build passed; the planted step
  failed; identity/staging, Pages artifact, and deploy were skipped.

Verdict: **PASS** for the same-SHA gate and its negative control.

First merged main run [#924](https://github.com/gasyoun/SanskritGrammar/actions/runs/31334163383)
failed before checkout because `setup-uv` v9 uses immutable release tags and has
no floating `v9` ref. Both downstream jobs were skipped, proving fail-closed
ordering. Repair pins the official v9.0.0 action commit
`c771a70e6277c0a99b617c7a806ffedaca235ff9`; this failed run is diagnostic, not
the deliberately-red acceptance control.
