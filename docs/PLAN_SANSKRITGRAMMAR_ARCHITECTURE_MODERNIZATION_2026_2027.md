# SanskritGrammar architecture modernization plan — 2026–2027

_Created: 29-07-2026 · Last updated: 29-07-2026_

This is the execution index for modernizing SanskritGrammar as a modular, reproducible
research-publication monorepo while its product portfolio continues to ship. The
[portfolio roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md)
remains authoritative for priority conflicts: M03 first, Sangram consolidation second, RQ4
launch third, comparative/publication work fourth, and archive/site maintenance fifth. This
plan adds a subordinate technical lane; it does not create a competing portfolio umbrella.

The configured Fable Planner returned no draft. The author explicitly authorized the root
Codex agent to continue best-effort, so this package is root-authored and root-validated. No
Planner or Advisor approval is claimed.

## Open this package in this order

1. [Roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_ARCHITECTURE_2026_2027.md)
   — the coordinated product and architecture waves over 12–18 months.
2. [Architecture](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANSKRITGRAMMAR_MODULAR_MONOREPO.md)
   — boundaries, contracts, ownership, data flow, and the hard-cutover target.
3. [Implementation](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md)
   — file-level Wave-1 sequence and non-overlapping execution slices.
4. [Verification](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md)
   — acceptance commands, risks, stop rules, and the autonomy-readiness matrix.

The companion [metadoc](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.meta.md)
records provenance, limitations, improvement backlog, and revision history.

## Audit verdict

The repository is operationally healthy but architecturally overgrown:

- current `origin/main` passes 133 Python tests, and recent CI and GitHub Pages deployments
  are green;
- its strongest boundary is scholarly governance: authoritative-source rules, stable IDs,
  schemas, the Sangram consolidation ledger, and generated-artifact contracts already exist;
- 94 Python files under `scripts/` form a flat script monolith with repeated hashing,
  statistics, transliteration, path, DCS-access, and output-writing logic;
- Docusaurus auto-discovery can include ignored archival MDX, so a populated local archive
  fails where a clean CI clone succeeds;
- Pages can deploy a site-build-green commit even if the independent Python test job for that
  commit fails;
- the site footer makes a blanket licensing statement that the README itself qualifies;
- local and CI toolchains drift because Python dependencies float, the Node engine floor is
  stale, and local `node_modules` can differ from the lockfile;
- the portfolio roadmap and the 152 KB session journal contain completed work represented as
  active work.

Prior-art verdict: **PARTIAL**. Existing pipelines and canonical cross-repo assets must be
consumed, not rebuilt. The missing piece is a repo-wide technical architecture with executable
pipeline, provenance, publication-boundary, and delivery contracts.

## Decisions taken

These 23 rulings were made by Dr. Mārcis Gasūns during the 29-07-2026 `/ask` interview.
Execution must not reopen them without new evidence and an explicit author request.

| # | Ruling | Operational consequence |
|---:|---|---|
| 1 | Portfolio throughput first. | Immediate M03, Sangram, and RQ4 gates retain precedence over structural elegance. |
| 2 | Plan for 12–18 months. | Wave 1 is exact; later waves are contract-gated and may be re-estimated from measured pilot cost. |
| 3 | Keep the existing portfolio roadmap authoritative. | This package is subordinate; the umbrella is refreshed rather than replaced. |
| 4 | Coordinate product and technical lanes. | Every architecture deliverable states which portfolio bottleneck or risk it removes. |
| 5 | Permit clean-slate restructuring. | Internal paths may change and consumers may require migration. |
| 6 | Use a modular monorepo. | Target boundaries are `apps/`, `packages/`, `content/`, `data/`, `pipelines/`, and layered tests. |
| 7 | Retain automatic publication discovery. | No publication allowlist is introduced; discovery is constrained by explicit allowed roots and tested exclusions. |
| 8 | Use per-work bounded contexts. | Each work converges on sources, generated output, media, work metadata, and provenance. |
| 9 | Build one installable `sg_tooling` package. | Existing scripts become thin migration inputs or are removed at hard cutover. |
| 10 | Declare every production pipeline. | Manifests pin inputs, hashes/versions, generator, outputs, and verification. |
| 11 | Preserve canonical cross-repo ownership. | SanskritGrammar owns adapters and grammar-specific logic, not generic Sanskrit or corpus engines. |
| 12 | Migrate by vertical slices. | Knauer is the book pilot; SG-MO-021 future is the Sangram pilot. |
| 13 | Use `pyproject.toml` and a locked `uv` workspace. | CI and developers install the exact dependency graph. |
| 14 | Keep Docusaurus and introduce TypeScript progressively. | No site rewrite; new/refactored components and remark code receive focused tests. |
| 15 | Use a lightweight manifest-driven CLI. | `sg pipeline check/run <id>` is the orchestration contract behind convenience commands. |
| 16 | Keep compact reproducible data in Git. | Large artifacts use immutable external releases, checksums, and pointers; private/raw sources remain off Git. |
| 17 | Use a hard cutover. | Known consumers are updated in the same wave; there is no compatibility release cycle. |
| 18 | Require contract-oriented verification. | Tests include determinism, schemas, frontend/plugin behavior, both build environments, and same-SHA deployment. |
| 19 | Prove two pilots before broad migration. | One book and one Sangram pipeline must pass rollback and consumer smoke tests. |
| 20 | Use a hybrid ambiguity policy. | Reversible infrastructure defaults may be applied and logged; scholarly, rights, destructive, or data-semantic ambiguity is parked. |
| 21 | Stop only the affected lane on named hazards. | Possible data loss, changed scholarly meaning, unknown consumers, irreproducible output, or a failing protected baseline stop that lane; other lanes continue. Rights uncertainty alone does not stop work. |
| 22 | Commit and PR per verified slice. | Automatic merge is allowed only when all gates pass and the change is infrastructure-only. |
| 23 | Permit coordinated sibling-consumer changes. | Known consumers may be migrated in Wave 1; unknown consumers trigger the stop rule. |

## Architecture outcome

The target is a modular monorepo with these stable responsibilities:

```text
apps/site/
packages/sg_tooling/src/sg_tooling/
  cli/
  domain/
  adapters/
  generators/
  contracts/
content/works/<work>/
  sources/
  generated/
  media/
  work.yml
content/sangram/
data/
  provenance.lock.json
pipelines/
tests/
  unit/
  contract/
  golden/
  integration/
```

Automatic Docusaurus discovery remains, but it operates only inside tracked content roots and
applies an explicit deny policy for ignored, private, raw, draft, review, archive, and scratch
surfaces. This preserves the convenience ruling without treating “an MDX exists somewhere” as
publication authority.

## Prior-art and ownership rulings

| Concern | Canonical owner | SanskritGrammar action |
|---|---|---|
| Sanskrit transcoding and normalization | [`sanskrit-util`](https://github.com/sanskrit-lexicon/sanskrit-util) | Import the canonical API through an adapter; do not add another mapping table. |
| DCS ingest and phonostat engines | [`VisualDCS`](https://github.com/gasyoun/VisualDCS) | Pin and consume released engines/data; keep grammar-specific query adapters here. |
| Review-sheet rendering | [`csl-pyutil`](https://github.com/sanskrit-lexicon/csl-pyutil) | Retain the pinned dependency; own only sheet specifications and workflow. |
| Canonical root crosswalks | [`WhitneyRoots`](https://github.com/gasyoun/WhitneyRoots) | Consume versioned crosswalks; do not derive replacement root identity tables. |
| DCS period map and declension coverage | SanskritGrammar H1000/H1048 | Promote existing assets into declared pipelines; do not recalculate their scholarly rulings. |
| Pedagogy export | SanskritGrammar H1643, consumed by Systema | Preserve its schema and coordinate the known consumer during cutover. |
| PWG–Pāṇini crosswalk | Blocked by issue 563 | Do not consume or promote until the contaminated extraction is repaired and regenerated. |

## Autonomy contract

### On ambiguity

- For a reversible infrastructure choice, apply the default stated in this package and log the
  choice in the PR.
- Park scholarly, publication-rights, destructive, or data-semantic ambiguity; do not guess.
- Uncertainty about publication rights by itself does **not** stop execution. Continue all
  non-semantic infrastructure work and use neutral, provenance-based messaging without making
  a new rights determination.

### Stop conditions

Stop the **affected lane**, preserve evidence, and continue independent lanes when any of these
occurs:

1. possible data loss;
2. changed scholarly meaning or data semantics;
3. an external consumer exists but its contract or owner is unknown;
4. a generated output cannot be reproduced from its declared inputs;
5. the protected-branch baseline fails independently of the change.

Do not widen a handoff merely to fix another lane. Do not stop solely because publication rights
remain uncertain.

### Commit, PR, and merge authority

- Work in an isolated worktree.
- Commit each verified slice and open a targeted PR.
- Automatically merge only when every acceptance gate passes and the diff is
  infrastructure-only.
- Stop before merge when the diff contains a human-gated scholarly ruling, a new rights
  determination, destructive source migration, or an unresolved stop condition.

### Fence

- Byte-preserving moves, infrastructure changes, manifests, tests, neutral rights messaging,
  and coordinated updates to **known** sibling consumers are allowed.
- Do not change scholarly prose, claim values, stable IDs, source authority, or generated-data
  semantics.
- Do not publish private/raw sources.
- Do not simulate human editorial, production-launch, or scholarly-gate decisions.
- Do not consume the contaminated PWG–Pāṇini crosswalk.

## Wave-1 release gate

Wave 1 is executable only when every row below is satisfied:

| Deliverable | Architecture | Ordered implementation | Acceptance | Risks |
|---|---:|---:|---:|---:|
| Delivery and publication safety | Architecture doc | Implementation Slice A | Verification V-A | Verification risk register |
| Knauer bounded-context pilot | Architecture doc | Implementation Slice B | Verification V-B | Verification risk register |
| SG-MO-021 pipeline pilot | Architecture doc | Implementation Slice C | Verification V-C | Verification risk register |
| Known-consumer hard cutover | Architecture ownership contract | Implementation cross-repo protocol | Verification V-D | Unknown-consumer stop rule |

The detailed gate verdict is maintained in the verification document. Any unresolved blocking
decision in a Wave-1 path fails release.

## Wave-1 execution handoffs

### H1911 — delivery and publication safety

[Handoff](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1911-Codex_SanskritGrammar_architecture-delivery-publication-safety_29.07.26.md)

```text
Read C:\Users\user\Documents\GitHub\SanskritGrammar\docs\PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md and execute the Wave-1 handoff H1911 (Slice A: delivery and publication safety).
```

### H1912 — Knauer vertical pilot

[Handoff](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1912-Codex_SanskritGrammar_architecture-knauer-vertical-pilot_29.07.26.md)

```text
Read C:\Users\user\Documents\GitHub\SanskritGrammar\docs\PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md and execute the Wave-1 handoff H1912 (Slice B: Knauer book pilot).
```

H1912 depends on H1911.

### H1913 — SG-MO-021 vertical pilot

[Handoff](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1913-Codex_SanskritGrammar_architecture-sg-mo-021-vertical-pilot_29.07.26.md)

```text
Read C:\Users\user\Documents\GitHub\SanskritGrammar\docs\PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md and execute the Wave-1 handoff H1913 (Slice C: SG-MO-021 future pilot).
```

H1913 depends on H1911 and may run in parallel with H1912 after that dependency lands.

## Non-goals

- No rewrite of Docusaurus.
- No publication allowlist or manifest-driven page enumeration.
- No semantic edit to a grammar, Sangram article, claim register, or corpus result.
- No generic transcoder, DCS ingest engine, review renderer, or root crosswalk.
- No broad migration beyond the two pilots until both pass.
- No use of issue 563 output.
- No architecture work that delays a time-bound M03, RQ4, or Sangram human gate.

_Dr. Mārcis Gasūns_
