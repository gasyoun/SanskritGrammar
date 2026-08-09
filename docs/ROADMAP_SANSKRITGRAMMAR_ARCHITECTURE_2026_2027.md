# Roadmap — SanskritGrammar architecture, 2026–2027

_Created: 29-07-2026 · Last updated: 09-08-2026_

_Provenance: root best-effort after the configured Fable Planner returned no draft. No Planner or Advisor approval is claimed._

This is the subordinate technical roadmap for the
[SanskritGrammar portfolio roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md).
It coordinates two lanes over 12–18 months: close the portfolio's real delivery gates, and
replace the repository's flat script-and-content layout with the modular architecture defined
in the [architecture specification](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANSKRITGRAMMAR_MODULAR_MONOREPO.md).
Product throughput wins any scheduling conflict.

The package index is
[PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md);
Wave-1 steps and gates live in the
[implementation](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md)
and
[verification](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md)
documents.

## 1. Starting point

### Product lane

| Track | Current truth on 29-07-2026 | Next gate | Owner |
|---|---|---|---|
| M03 monograph | H1259 line edit complete; 290 highlighted paragraphs await review | Human accepts/reverts changes; freeze 31-10-2026; publisher contact in November | Human |
| Sangram | Freeze baseline: 11 published, 1 kill-gated, 14 unknown | Supply legitimate C5/C6 gates or use visa/another documented terminal path | Scholarly/human gate, agent evidence |
| RQ4 | Protocol, item bank, export, Systema harness, smoke test, and runbook complete | Human production authorization after the non-collision window | Human |
| Grammar Lab | Five-layer plan and 29 rulings complete; concordance/index/product gap scoped | Build the evidence graph, then Systema import/search, learning loop and entitlement/pilot | Four Grok 4.5 handoffs |
| Comparative/publication | A61 submission-ready; A64 draft with venue/form unresolved | CfP-triggered submission work and later author rulings | Mixed |
| Archive/site | CI and Pages green; local populated archive can fail discovery | Delivery/publication safety slice | Agent |
| Integrity | Issue 563 shows 74.5% impossible PWG–Pāṇini “sūtra” keys | Suppress until contextual extraction and regeneration | Agent research, scholarly acceptance |

### Technical lane

Strengths to preserve:

- explicit authoritative-source and generated-output rules;
- stable IDs, schemas, validation, and Sangram's consolidation ledger;
- reproducible compact data committed with provenance;
- current green pytest and clean-clone Docusaurus build;
- canonical ownership in `sanskrit-util`, VisualDCS, `csl-pyutil`, and WhitneyRoots.

Debt to retire:

- flat, duplicated Python scripts and machine-specific paths;
- auto-discovery that can traverse ignored archival MDX;
- independently deploying Pages workflow;
- floating Python dependencies and an inaccurate Node engine floor;
- stale scaffold/configuration copies;
- mixed source/generated/content/data boundaries;
- roadmap and session-state drift.

## 2. Wave gates

Waves open by evidence, not calendar. Dates are planning windows, not permission to bypass a
contract.

| Wave | Indicative window | Opens when | Closes when |
|---|---|---|---|
| **W0 — truth rebase** | July–August 2026 | Current `origin/main` and hubs are audited | Portfolio roadmap/state/issues describe shipped vs active work accurately; architecture package and handoffs exist |
| **W1 — safety and two pilots** | August–October 2026 | W0 package passes autonomy readiness | Delivery safety, Knauer, and SG-MO-021 slices pass every gate, including rollback and known-consumer smoke |
| **W2 — core factories** | Q4 2026–Q1 2027 | Both pilots demonstrate stable contracts and measured migration cost | Remaining active book and Sangram factories use declared pipelines and shared tooling |
| **W3 — hard cutover** | Q1–Q2 2027 | Consumer census is complete and W2 output is reproducible | Legacy active paths are removed; known consumers migrate in the same wave; no compatibility release remains |
| **W4 — consolidate and measure** | Q2–Q4 2027 | Hard cutover is stable for one release interval | Duplicates are retired, ownership is reconciled, build/research throughput is measured, next roadmap is based on evidence |

## 3. W0 — truth rebase

### Product deliverables

1. Replace the umbrella roadmap's stale H1259 execution pointer with the human review gate.
2. Replace stale Sangram counts with the 26-row ledger disposition.
3. Record pedagogy last-mile, H1514, freeze-probe, and A61 completion accurately.
4. Keep issue 563 output suppressed and visible as an integrity blocker.
5. Move completed material out of active `.ai_state.md` signals during the next journal
   maintenance pass; retain audit history in Completed or changelog records.

### Technical deliverables

1. Ratify this five-document package and its metadoc.
2. Register the subordinate roadmap in
   [Uprava/ROADMAP_INDEX.md](https://github.com/gasyoun/Uprava/blob/main/ROADMAP_INDEX.md).
3. Mint three non-overlapping Wave-1 handoffs.
4. Capture baseline commands and current failures before implementation.

### Acceptance

- no Wave-1 path contains an unresolved blocking decision;
- every open architecture backlog item has a handoff owner;
- the authoritative roadmap remains the priority arbiter;
- no current-state statement relies on the stale planning checkout.

## 4. W1 — safety and vertical pilots

### W1-A · delivery and publication safety

Deliver:

- auto-discovery constrained to tracked allowed content roots with explicit exclusions for
  ignored/private/raw/draft/review/archive/scratch MDX;
- regression fixtures for a clean clone and a populated archival clone;
- one current Docusaurus configuration source; retire the stale `site_tools.py` scaffold;
- neutral code/site and per-work rights messaging without making new rights determinations;
- correct Node engine floor, `pyproject.toml`, locked `uv` baseline, and documented `npm ci`;
- a same-SHA CI-to-Pages artifact flow;
- focused remark/plugin and discovery tests.

Product unblock: archive correctness can continue without local archival assets poisoning builds,
and a Python-red commit cannot deploy merely because Docusaurus is green.

### W1-B · Knauer book pilot

Migrate `KnauerFrazy_1908` through the per-work bounded context and declared-pipeline model.
Preserve the authoritative source, MDX content, errata/claim semantics, media, routes, and stable
IDs until the single hard cutover. Prove byte or normalized-semantic equivalence, deterministic
regeneration, rollback, and site discovery.

Product unblock: proves that print/source maintenance can move into the new factory without
changing scholarship.

### W1-C · SG-MO-021 future pilot

Migrate the generator, article manifest/data, provenance, and verification contract behind
`sg pipeline check/run sg-mo-021-future`. Preserve every published number, claim, stable ID,
sample seed, and article byte except path/metadata changes explicitly required by cutover.
Coordinate any demonstrated Systema consumer in the same wave; an unknown consumer stops this
lane.

Product unblock: proves that Sangram can consolidate and repair existing articles faster without
opening new topics or rebuilding corpus engines.

### W1 dependency order

```text
W0 truth rebase
  -> W1-A delivery/package foundation
       -> W1-B Knauer pilot
       -> W1-C SG-MO-021 pilot
  -> joint rollback + consumer smoke
  -> W1 exit review
```

W1-B and W1-C may run in parallel after W1-A publishes the package, manifest, path, and test
contracts. They must use disjoint files and may not independently redefine those contracts.

### Parallel product lane · Grammar Lab

The [Grammar Lab roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_GRAMMAR_LAB_2026_2027.md)
is a product lane, not a fourth architecture-migration pilot. Its SanskritGrammar bundle must
adopt the declared-pipeline and deterministic-check conventions as they land, but it need not
wait for the full W2 monorepo migration. Its dependency chain is data graph → Systema import and
hybrid search → exercises/SRS/recommendations → entitlement and learner pilot.

## 5. W2 — migrate the core factories

Order is evidence-driven:

1. Migrate the remaining source-to-MDX book pipelines by increasing complexity.
2. Migrate claims, errata, quantifier, concordance, and review-spec generators.
3. Migrate Sangram's MO/SE/WF families in bounded batches.
4. Promote shared DCS access, provenance, deterministic writers, statistics, and path policy
   into `sg_tooling`.
5. Replace duplicated helpers only after behavior is characterized by golden tests.
6. Add TypeScript when a component or plugin is materially changed; do not churn untouched JSX.

W2 closes only when every active production pipeline has an owner, manifest, lock/provenance
record, deterministic check, and rollback path.

## 6. W3 — hard cutover

1. Freeze a complete consumer census for each path/schema scheduled to move.
2. Prepare SanskritGrammar and known sibling-consumer commits against the same cutover contract.
3. Rehearse cutover and rollback in isolated worktrees.
4. Merge producer first only when consumer PRs are ready and their smoke tests pass.
5. Merge known consumers immediately; do not maintain compatibility wrappers for a release.
6. Remove legacy active scripts/paths and update documentation, CI, hubs, and provenance.
7. Stop the affected lane if an unknown consumer appears.

Hard cutover never authorizes semantic content changes or private-source publication.

## 7. W4 — consolidate, measure, and sunset

Measure:

- clean and populated build success;
- median time to reproduce a declared artifact;
- nondeterministic-output incidents;
- duplicated-helper count;
- pipelines with immutable provenance;
- migration/rollback defects;
- known-consumer breakages;
- time from scholarly gate closure to published verified artifact.

Then:

- remove dead adapters and superseded docs;
- decide whether any package has earned extraction into a separate repository through a stable
  external-consumer record;
- archive this roadmap when its contracts are complete or superseded;
- write the next roadmap from measured throughput, not directory aesthetics.

## 8. Stop, park, and continuation policy

For reversible infrastructure ambiguity, apply the documented default and log it. Park
scholarly, rights, destructive, or data-semantic ambiguity. Stop only the affected lane on
possible data loss, changed scholarly meaning, an unknown external consumer, irreproducible
output, or a failing protected-branch baseline; continue independent lanes.

Uncertain publication rights alone is not a stop condition. It forbids invented rights claims,
not neutral infrastructure work or accurate provenance messaging.

## 9. Non-goals

- No Docusaurus replacement.
- No publication allowlist; auto-discovery remains within an explicit safety boundary.
- No semantic rewrite of books, articles, claims, or generated data.
- No generic Sanskrit/corpus utility reimplementation.
- No use of issue 563 output.
- No broad migration before both pilots pass.
- No compatibility release after hard cutover.
- No architecture task that displaces a time-bound M03, RQ4, or Sangram gate.

_Dr. Mārcis Gasūns_
