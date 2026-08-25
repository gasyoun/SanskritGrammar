# H1913 dual-run reconciliation — SG-MO-021 Slice C

_Created: 25-08-2026 · Last updated: 25-08-2026_

## Scope and provenance

This memo reconciles the planned dual execution required by
[H3321 (Codex) — H1913 dual-run compare: independent Codex re-run of the SG-MO-021 Slice C pilot vs the override lane](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3321-Codex_SanskritGrammar_h1913-codex-dual-run-compare_22.08.26.md).

1. **Override lane:** OpenCode preview (`opencode/ox-alpha`, lane label
   `x-preview-f-free`), PR [#874](https://github.com/gasyoun/SanskritGrammar/pull/874),
   merge `d059f23`, based on `5019832`.
2. **Independent lane:** Codex (`GPT-5`), commit `2e2f60f`, independently built
   from the Slice C plan and the same base `5019832` before reading PR #874.
3. **Surviving lane:** this reconciliation branch, based on current
   `origin/main`, with one canonical registry, generator, pipeline, article
   path, and output pair.

## Classification and adjudication

| Area | Class | Override lane | Independent lane | Winner and argument |
|---|---|---|---|---|
| Frozen scholarly payload | Identical | Reproduces the pre-cutover summary and sample through fixture goldens. | Reproduces the real committed outputs by SHA-256 and proves the whole summary equals C0 `published_numbers`. | **Both retained as double verification.** Fixture expectations catch semantic mistakes without the 921 MB corpus; full C0 equality proves own-data parity. |
| DCS adapter | Equivalent by a different route | Generic `DcsMaster` exposes reusable read-only count/distribution/sample primitives and tests missing-file, missing-pin, hash, and join behavior. | One-purpose reader performs the complete future census and enforces the declared database hash. | **Override structure wins; independent integrity check is absorbed.** Genericity belongs in the adapter, while the generator now rejects any SHA-256 different from the manifest. |
| Generator | Equivalent by a different route | Pure summary/sample functions, declarative test seams, strong fixture tests, but writes the legacy article path and did not compare the runtime DB hash to the manifest. | Pure summary builder plus atomic LF writer, canonical `content/` output, and mandatory runtime hash comparison. | **Hybrid.** Keep the override decomposition and tests; take the independent canonical output path and hash refusal. |
| Pipeline manifest | Conflicting | Detailed inputs, five named consumers, verification notes, and rollback; outputs remain under `sangram/articles/future`. | Outputs under the architecture-owned `content/sangram/articles/future` boundary and declares the same immutable input more tersely. | **Hybrid with canonical-path ruling.** Keep the override evidence-rich contract, change outputs/consumer contracts to `content/`, and retain the stable public slug. |
| C3 hard cutover | Net-new to independent | Deletes the legacy script but leaves the article and generated data in the legacy active directory. | Moves all four article assets to `content/sangram/articles/future`, removes the legacy directory, and preserves `/sangram/articles/future` through front matter. | **Independent wins.** Slice C explicitly owns the target `content/` boundary and forbids a duplicate active path. |
| Internal consumers | Net-new to independent | Inventories consumers but leaves path-bearing links, the editorial ledger, validators, and discovery fixture unchanged. | Updates article links, visa source/index, ledger refresh, article validation, denominator validation, and discovery tests; sibling-repo search found no external path consumer. | **Independent wins.** These are required coordinated C3 consumer changes; historical C0 documentation remains intentionally frozen. |
| Registry discovery | Equivalent by a different route | Deterministic sorted path scan and a strong ownership-fence contract test, but contains a duplicate empty-registry assignment. | `pkgutil` discovery with one registry assignment and a weaker positive-only test. | **Override wins with repair.** Keep deterministic discovery and the ownership-fence test; remove the duplicate assignment found by the independent review. |
| Golden and integration tests | Net-new to override, with one independent addition | Builds a characterized SQLite fixture, stores full expected outputs, checks adapter behavior, deterministic double-run, frozen seed/sample refusal, and installed CLI execution. | Stores real-output hashes and asserts full C0 payload equality after the real pipeline run. | **Both retained.** The override suite is the stronger CI-sized harness; the independent C0 equality is the on-data acceptance gate. |
| Provenance lock | Equivalent | Detailed off-Git path, composite upstream owner, orphaned-pin explanation, immutable commit and SHA-256. | Same commit/SHA/right, shorter ID and note. | **Override wins.** It carries more operational information without changing identity. |

Class counts: **1 identical · 3 equivalent · 2 conflicting · 3 net-new**.
No area was silently selected; each conflict above records the governing plan
rule and the retained parts of both lanes.

## Frozen invariants and consumer census

1. The generated `coverage_summary.json` equals
   `docs/architecture/baseline/h1913_c0_invariants.json#published_numbers` as a
   complete JSON value. Published counts, stable IDs, sample metadata, limits,
   and scholarly meaning are unchanged.
2. The committed `coverage_summary.json` and `validation_sample.tsv` remain the
   same content artifacts; only their canonical directory changes.
3. `art:future`, `SG-MO-021`, 14 `ex:future:*` IDs, and the public
   `/sangram/articles/future` slug remain stable.
4. Exact sibling-repository search for `sangram/articles/future` found no
   external code/path consumer. The manifest therefore records only known
   same-repository consumers; historical C0/plan documents keep their original
   pre-cutover paths as evidence.

## Verification transcript

The surviving tree passed the H3321 V-C gate on 25-08-2026:

1. `uv run sg pipeline check sg-mo-021-future` — PASS.
2. `uv run sg pipeline run sg-mo-021-future` twice — PASS; second run produced
   no tracked output drift.
3. `uv run pytest tests/golden/sg_mo_021_future tests/integration/test_sg_mo_021_future_pipeline.py` — PASS.
4. `python scripts/article_validate.py --all` — PASS.
5. `python scripts/check_claims_consistency.py` — PASS.
6. `npm run build` — PASS; only the repository's pre-existing warn-only anchor
   inventory was reported.
7. Rollback rehearsal from pre-cutover commit `d00f9dca` — PASS: the legacy
   generator reproduced its committed outputs with no diff.

## Final disposition

The canonical tree keeps the override lane's reusable adapter, fixture suite,
and detailed contract; it keeps the independent lane's hard cutover, runtime
hash refusal, complete C0 parity assertion, and consumer migration. There is no
parallel registry, legacy active generator, or duplicate article output path.

_Dr. Mārcis Gasūns_
