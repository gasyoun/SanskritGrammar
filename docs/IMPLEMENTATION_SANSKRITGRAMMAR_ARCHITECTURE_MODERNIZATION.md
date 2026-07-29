# Implementation — SanskritGrammar architecture modernization

_Created: 29-07-2026 · Last updated: 29-07-2026_

_Provenance: root best-effort after the configured Fable Planner returned no draft. No Planner or Advisor approval is claimed._

This is the file-level Wave-1 build sequence for the
[plan](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md),
[roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_ARCHITECTURE_2026_2027.md),
and
[architecture](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANSKRITGRAMMAR_MODULAR_MONOREPO.md).
Acceptance belongs to the
[verification specification](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md).

Wave 1 is split into three non-overlapping handoffs. Slice A owns shared contracts and must land
before B or C. Slices B and C then run in parallel.

## 1. Shared rules

- Start from current `origin/main` in an isolated worktree.
- Record baseline hashes/status before moving anything.
- Preserve scholarly prose, numerical results, stable IDs, source authority, and generated-data
  semantics.
- Use canonical `sanskrit-util`, VisualDCS, `csl-pyutil`, and WhitneyRoots assets through
  adapters; do not copy their logic.
- Use UTF-8 and LF for authored text.
- Do not consume the PWG–Pāṇini crosswalk while issue 563 is unresolved.
- Ruling 17 is a hard cutover: known consumers migrate with the producer; no compatibility
  release is created.

## 2. Slice A — delivery and publication safety

### Ownership

Slice A exclusively owns:

- `pyproject.toml`, `uv.lock`, root Python packaging configuration;
- `package.json`, `package-lock.json`;
- `docusaurus.config.mjs`, `sidebars.mjs`;
- `.github/workflows/ci.yml`, `.github/workflows/deploy-pages.yml`;
- shared `apps/site/`, `packages/sg_tooling/`, `pipelines/`, and test scaffolds;
- shared discovery, manifest-schema, path, provenance, and CLI contracts;
- `scripts/site_tools.py`, `README.md`, and the site footer/rights messaging.

Slices B/C must not edit these shared contracts unless Slice A explicitly leaves a named extension
point.

### A0 · Baseline

Record:

```powershell
git status --short
python -m pytest
npm ci
npm run build
git ls-files
```

Also demonstrate the known populated-archive failure using a fixture or an isolated copy; never
commit private/ignored source material.

Stop this lane if the protected baseline fails for a reason unrelated to the known populated
archive discovery defect.

### A1 · Package and workspace foundation

Create:

```text
pyproject.toml
uv.lock
packages/sg_tooling/pyproject.toml
packages/sg_tooling/src/sg_tooling/__init__.py
packages/sg_tooling/src/sg_tooling/cli/__init__.py
packages/sg_tooling/src/sg_tooling/cli/main.py
packages/sg_tooling/src/sg_tooling/domain/__init__.py
packages/sg_tooling/src/sg_tooling/adapters/__init__.py
packages/sg_tooling/src/sg_tooling/generators/__init__.py
packages/sg_tooling/src/sg_tooling/contracts/__init__.py
pipelines/pipeline.schema.json
data/provenance.lock.json
```

Define the `sg` console entry point and the initially supported commands:

```text
sg pipeline check <id>
sg pipeline run <id>
sg pipeline list
```

Pin direct and transitive Python dependencies through `uv.lock`; pin Git dependencies by immutable
commit, not only a mutable tag. Correct the Node engine floor to the actual Docusaurus-supported
range. CI must install the lock rather than resolving lower bounds.

### A2 · Pipeline and work contracts

Implement schemas/models for:

- pipeline ID, owner, generator, explicit inputs, immutable versions/hashes, outputs, checks,
  external consumers, and rollback;
- work ID, authority, source pointers, generated roots, media roots, routes, rights/provenance
  statement, and pipeline IDs;
- provenance lock entries for repository URL/ref/commit/hash/schema.

Validation rejects unknown keys where silent acceptance would change execution. A missing optional
rights determination remains representable as `unknown`; it is not a pipeline failure.

### A3 · Safe auto-discovery

Move the Docusaurus application boundary toward `apps/site/`, but keep one runnable configuration
during the slice. Replace repository-root scanning with discovery rooted in approved content zones
and an explicit tracked exclusion policy covering:

- gitignored paths;
- raw/private/source directories;
- drafts, review output, archives, scratch, caches, worktrees, and generated build directories;
- arbitrary root MDX outside allowed content zones.

Do **not** create a publication allowlist. Valid MDX added under an allowed work/content zone must
still appear automatically.

Add fixture tests for:

1. a valid new work;
2. malformed MDX in an ignored archival directory;
3. draft/review/private MDX;
4. valid Sangram content;
5. arbitrary root MDX.

### A4 · Single site configuration and TypeScript test seam

- Move or wrap Docusaurus config, sidebar, pages, components, and remark plugins under
  `apps/site/` according to the architecture.
- Remove the stale embedded Docusaurus scaffold from `scripts/site_tools.py`; retain only a CLI
  that delegates to the canonical template/config if the command remains necessary.
- Introduce TypeScript configuration for new/refactored code without mass-converting untouched JSX.
- Add focused tests for discovery and the `rstTable`/heading-anchor plugins.
- Correct README statements that contradict the live configuration.

### A5 · Neutral rights/provenance presentation

Replace the blanket site-content licence claim with wording that distinguishes repository code
licensing from per-work text/source status and links to work provenance. Do not decide an unknown
right or describe uncertainty as permission.

Rights uncertainty alone does not stop this step. A discovered explicit restriction is recorded
and respected; scholarly content remains unchanged.

### A6 · Same-SHA delivery gate

Refactor workflows so one CI run for a commit:

1. installs the locked Python and Node environments;
2. runs Python, contract, frontend/plugin, and site-build gates;
3. uploads the built Pages artifact for that exact SHA;
4. deploys only after every required job succeeds;
5. records/verifies the deployed artifact SHA.

`deploy-pages.yml` must not independently rebuild and deploy a commit whose other required gates
failed.

### A7 · Slice-A merge

Run verification V-A. Commit in bounded milestones, open one targeted PR, and auto-merge only if
the entire diff is infrastructure-only and every gate is green.

## 3. Slice B — Knauer bounded-context pilot

### Ownership

Slice B owns only Knauer-specific content, manifests, adapters/generators, fixtures, and tests:

```text
KnauerFrazy_1908/
content/works/knauer-frazy-1908/
pipelines/knauer-frazy-1908.yml
packages/sg_tooling/src/sg_tooling/generators/knauer.py
tests/golden/knauer/
tests/integration/test_knauer_pipeline.py
```

### B0 · Inventory and invariants

Inventory tracked and off-Git pointers without adding private/raw files. Freeze:

- authoritative source identity/hash;
- generated MDX normalized hash;
- media inventory;
- route/anchor list;
- errata and claims IDs/counts/values;
- release/changelog provenance.

If authority is ambiguous, park the affected file and continue with independently classified
assets.

### B1 · Declare the work and pipeline

Create `content/works/knauer-frazy-1908/work.yml` and
`pipelines/knauer-frazy-1908.yml`. Register the authoritative source, generator chain, outputs,
verification, route contract, and rollback commit/artifact.

### B2 · Extract pure generation

Move Knauer-specific conversion/postprocessing behavior behind `sg_tooling` generator and adapter
interfaces. Reuse the shared converter/remark contracts from Slice A. Do not change output merely
to normalize style; every semantic or byte change must be explained by an accepted generator
contract.

### B3 · Hard cutover

Move tracked assets into the bounded context in one coherent cutover, update Docusaurus discovery,
README/work links, and every known internal/sibling consumer found by the census. No compatibility
wrapper or duplicate active path remains.

### B4 · Rollback rehearsal and merge

Prove `sg pipeline check/run knauer-frazy-1908`, deterministic output, route parity, known-consumer
smoke, and restoration to the pre-cutover release. Run V-B and merge only after every gate passes.

## 4. Slice C — SG-MO-021 future pilot

### Ownership

Slice C owns:

```text
scripts/sg_mo_021_future.py
sangram/articles/future/
content/sangram/articles/future/
pipelines/sg-mo-021-future.yml
packages/sg_tooling/src/sg_tooling/generators/sg_mo_021_future.py
packages/sg_tooling/src/sg_tooling/adapters/dcs.py
tests/golden/sg_mo_021_future/
tests/integration/test_sg_mo_021_future_pipeline.py
```

Shared DCS adapter changes must remain generic and characterized; corpus-engine logic stays in
VisualDCS.

### C0 · Freeze scholarly and data invariants

Record article manifest/schema, stable IDs, all published numbers, sample seed/universe, source DB
hash, generated datasets, article normalized hash, validation result, and external consumers.

Any changed scholarly number or meaning stops this lane.

### C1 · Declare the pipeline

Create `pipelines/sg-mo-021-future.yml` with immutable corpus/version inputs, generator,
outputs, determinism checks, Sangram schema/ledger validation, consumers, and rollback.

### C2 · Extract generator and adapters

Refactor the current script into pure domain/generator functions plus explicit adapters for
filesystem, SQLite/DCS, provenance, and output writing. The CLI invokes these functions through
the manifest. Characterization/golden tests pin current behavior before movement.

### C3 · Hard cutover and consumers

Move the active article/pipeline assets into the target boundary, update every demonstrated
internal and known sibling consumer in coordinated PRs, and remove the legacy active path.
If a consumer is detected but its contract/owner is unknown, stop C3 and preserve the prepared
producer/consumer commits without merging.

### C4 · Rollback rehearsal and merge

Run `sg pipeline check/run sg-mo-021-future` twice, Sangram validators, golden comparisons,
article/site build, consumer smoke, and rollback. Run V-C/V-D and merge only when infrastructure
changes preserve every frozen invariant.

## 5. Cross-repo consumer protocol

1. Search code, hubs, pipeline metadata, and release notes for path/schema consumers.
2. Classify each as internal, known sibling, unknown, or historical.
3. Record exact owner, current contract, target contract, PR order, smoke command, and rollback.
4. Prepare known sibling changes in isolated worktrees.
5. Do not merge the producer until all required consumer PRs are ready and verified.
6. Hard-cut producer and consumers in the declared order; do not ship a compatibility cycle.
7. Unknown consumer means stop the affected lane, not the other Wave-1 slices.

## 6. Commands introduced by implementation

These do not exist at plan time and must be added:

```powershell
uv sync --frozen
uv run sg pipeline list
uv run sg pipeline check knauer-frazy-1908
uv run sg pipeline run knauer-frazy-1908
uv run sg pipeline check sg-mo-021-future
uv run sg pipeline run sg-mo-021-future
npm run test:site
npm run test:discovery
npm run verify
```

Existing baseline commands remain:

```powershell
python -m pytest
npm ci
npm run build
python scripts/article_validate.py --all
python scripts/check_claims_consistency.py
```

_Dr. Mārcis Gasūns_
