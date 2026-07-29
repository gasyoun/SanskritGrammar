# Verification — SanskritGrammar architecture modernization

_Created: 29-07-2026 · Last updated: 29-07-2026_

_Provenance: root best-effort after the configured Fable Planner returned no draft. No Planner or Advisor approval is claimed._

This document owns acceptance, risk, and autonomy readiness for the
[plan](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md),
[roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_ARCHITECTURE_2026_2027.md),
[architecture](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANSKRITGRAMMAR_MODULAR_MONOREPO.md),
and
[implementation](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md).

## 1. Baseline evidence

Observed during the 29-07-2026 audit:

- `python -m pytest`: 133 passed; warnings came from upstream
  `indic_transliteration` deprecations;
- current `main` CI and Pages deployments: green;
- local populated-archive `npm run build`: failed because auto-discovery included ignored
  `Concordance/UshaSanka_Ph.D_2014` MDX with invalid frontmatter;
- clean CI did not contain that ignored archive and passed;
- local `node_modules` contained React 18 while the lock/manifest requested React 19;
- one open integrity issue, 563, invalidates consumption of the current PWG–Pāṇini crosswalk.

The populated-archive failure is required regression evidence, not permission to commit the
private/ignored fixture.

## 2. V-A — delivery and publication safety

### Dependency and packaging

Pass when:

```powershell
uv sync --frozen
uv run python -m pytest
uv run sg pipeline list
npm ci
```

also pass on Windows and Linux using the declared minimum/current supported Node versions.
`pyproject.toml` and `uv.lock` must have no unpinned mutable Git dependency.

### Discovery boundary

Automated tests must prove:

| Fixture | Expected |
|---|---|
| valid MDX inside an allowed work/content zone | discovered |
| valid Sangram MDX inside its allowed zone | discovered |
| malformed MDX inside an ignored archive | not read, build remains green |
| MDX under raw/private/source/review/draft/archive/scratch | not discovered |
| arbitrary root MDX | not discovered |
| cache, worktree, `node_modules`, build output | not discovered |

Run both:

```powershell
npm run test:discovery
npm run build
```

in a clean clone and a populated archival clone/worktree. The populated run may use local ignored
assets but must not add them to Git.

### Site, plugins, and messaging

Pass when:

```powershell
npm run test:site
npm run build
```

and tests cover the `rstTable` parser/AST, heading-anchor behavior, discovery policy, and any
refactored TypeScript component.

The deployed footer must distinguish code licensing from per-work text/source status. It must not
make a blanket content-rights claim or invent a determination for an unknown work.

### Same-SHA deployment

For a test PR and merged commit, evidence must show:

1. all required Python, contract, frontend/plugin, and site jobs ran for SHA `X`;
2. the Pages artifact was produced by that gated workflow for SHA `X`;
3. deploy consumed that artifact, not a rebuild of another SHA;
4. a deliberately failing required job prevents deploy.

## 3. V-B — Knauer pilot

Freeze before/after evidence:

- authoritative source identity and hash;
- normalized MDX hash and rendered route/anchor inventory;
- media file inventory/hashes;
- errata/claims stable IDs, counts, verdicts, and values;
- generated artifact list and pipeline provenance.

Pass when:

```powershell
uv run sg pipeline check knauer-frazy-1908
uv run sg pipeline run knauer-frazy-1908
uv run sg pipeline run knauer-frazy-1908
git diff --exit-code
uv run pytest tests/golden/knauer tests/integration/test_knauer_pipeline.py
npm run build
```

The twice-run sequence must produce identical bytes or an explicitly normalized deterministic
contract. Public routes and anchors must match the frozen inventory unless the hard-cutover plan
names and verifies every updated consumer.

Rollback passes only when the prior coherent Knauer release can be restored from the recorded
commit/artifacts without private-source loss.

## 4. V-C — SG-MO-021 pilot

Freeze before/after evidence:

- article ID, manifest schema, stable IDs, revision state, and ledger disposition;
- every published number and table value;
- corpus/database version and hash;
- universe, query, seed, sample IDs, and generated outputs;
- article normalized hash;
- all internal and external consumers.

Pass when:

```powershell
uv run sg pipeline check sg-mo-021-future
uv run sg pipeline run sg-mo-021-future
uv run sg pipeline run sg-mo-021-future
git diff --exit-code
uv run pytest tests/golden/sg_mo_021_future tests/integration/test_sg_mo_021_future_pipeline.py
python scripts/article_validate.py --all
python scripts/check_claims_consistency.py
npm run build
```

Any change to a frozen number, stable ID, sample, claim, or scholarly meaning fails the lane.
Issue 563 data must not appear in the pipeline's declared inputs.

## 5. V-D — hard-cutover consumer gate

The consumer census must contain:

| Field | Required |
|---|---|
| consumer repo/path | yes |
| owner | yes |
| old contract | yes |
| new contract | yes |
| producer/consumer merge order | yes |
| smoke command | yes |
| rollback | yes |
| status | prepared/verified/merged/retired |

Known sibling consumers may be changed in Wave 1. Producer merge is forbidden until required
consumer PRs are ready and their smoke commands pass. Detecting a consumer whose owner or contract
is unknown triggers the affected-lane stop condition.

No compatibility wrapper or duplicate active path remains after the coordinated cutover.

## 6. Determinism and provenance gate

Every Wave-1 manifest must:

- validate against the pipeline schema;
- name one owner and one generator;
- pin external repositories by immutable commit and inputs by hash;
- enumerate outputs and verification;
- record rights/provenance without treating `unknown` as permission;
- name known consumers and rollback;
- reproduce committed compact outputs;
- point large artifacts to immutable releases with checksums.

Generated output may not embed wall-clock timestamps, unordered traversal, host-specific paths, or
platform line endings unless the contract normalizes them before hashing.

## 7. Risk and spike register

| ID | Risk | Gate or spike | Stop behavior |
|---|---|---|---|
| R1 | Auto-discovery still traverses ignored/private content | Clean + populated fixture matrix | Stop Slice A |
| R2 | Hard cutover misses a consumer | Code/hub/release census plus sibling smoke | Stop affected B/C lane |
| R3 | Moving a source changes authority or loses an off-Git pointer | Hash/inventory and rollback rehearsal | Stop affected pilot |
| R4 | Refactor changes a published number or sample | Golden scholarly/data invariant comparison | Stop Slice C |
| R5 | Cross-platform output remains nondeterministic | Two-run Windows/Linux comparison | Stop affected pipeline |
| R6 | Same-SHA deploy assumption is false | Deliberately red required job | Stop Slice A |
| R7 | Rights messaging overclaims | Exact deployed-copy/provenance review | Park claim wording; continue neutral infrastructure |
| R8 | Generic logic is copied from a canonical owner | Import/ownership review | Stop affected adapter |
| R9 | Issue 563 data leaks into a pilot | Manifest/input scan | Stop Slice C |
| R10 | Protected `main` is red independently | Baseline control without branch changes | Stop affected lane; continue independent lanes |

## 8. Autonomy rules

### Ambiguity

- Apply and log the documented default only for reversible infrastructure.
- Park scholarly, rights, destructive, or data-semantic ambiguity.
- Rights uncertainty alone does **not** stop work; continue neutral infrastructure and
  provenance messaging without inventing a determination.

### Stop conditions

Stop the affected lane on:

1. possible data loss;
2. changed scholarly meaning;
3. an unknown external consumer;
4. irreproducible output;
5. a failing protected-branch baseline.

Preserve evidence and continue independent lanes.

### Merge

Commit per verified slice and open targeted PRs. Auto-merge only when every specified gate passes
and the change is infrastructure-only. Stop before merge for a human-gated scholarly ruling, new
rights determination, destructive migration, or unresolved stop condition.

## 9. Autonomy-readiness matrix

| Wave-1 deliverable | Architecture contract | Ordered steps | Acceptance | Risks |
|---|---|---|---|---|
| Delivery/publication safety | Architecture §§ publication, site, package, delivery | Implementation Slice A | V-A | R1, R5–R8, R10 |
| Knauer pilot | Per-work bounded context, authority, pipeline, cutover | Implementation Slice B | V-B | R2, R3, R5, R8, R10 |
| SG-MO-021 pilot | Sangram boundary, adapters, provenance, stable IDs | Implementation Slice C | V-C | R2, R4, R5, R8–R10 |
| Consumer hard cutover | Ownership and external-consumer contract | Cross-repo protocol | V-D | R2, R3, R10 |

**Gate verdict at authoring:** PASS for planning readiness. Every Wave-1 deliverable has an
architecture contract, ordered steps, acceptance evidence, and named risks. No blocking
decision remains. Execution still begins with each slice's live baseline control.

## 10. Planning-package checks

Before releasing handoffs:

```powershell
git diff --check
python -m pytest
```

Review must also confirm that no unresolved blocking decision remains. The planning docs do not
themselves implement the future `uv`, `sg`, TypeScript, discovery, or same-SHA gates.

_Dr. Mārcis Gasūns_
