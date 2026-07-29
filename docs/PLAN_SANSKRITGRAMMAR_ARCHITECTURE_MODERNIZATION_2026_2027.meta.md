# Metadoc — PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md

_Created: 29-07-2026 · Last updated: 29-07-2026_

This is the companion record for
[PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md).
It records why the plan exists, how it was produced, its limitations, and the owned improvement
backlog; it does not duplicate the plan.

## Subject

- **Purpose:** coordinate a 12–18-month modular-monorepo modernization beneath the existing
  portfolio order and release an unattended Wave-1 package.
- **Audience:** repository owner, architecture executors, and maintainers of known sibling
  consumers.
- **Contract:** authored Markdown, five cross-linked layers, no unresolved blocking Wave-1
  decisions, and every executable improvement owned by a handoff.
- **Status:** active.

## Provenance

- Repository and cross-repo audit performed 29-07-2026 against current `origin/main`, GitHub
  issues/PRs/CI, state, roadmaps, reuse hubs, and shared-code registries.
- 23 author rulings collected through four `/ask` interview rounds.
- The configured Fable Planner returned no draft. Dr. Mārcis Gasūns explicitly authorized the
  root Codex agent to proceed best-effort.
- Root author and validator: Codex.
- No Planner or Advisor approval is claimed.

## Improvement backlog

| Rank | Improvement | Why | Status |
|---:|---|---|---|
| 1 | Delivery/publication safety foundation | Prevent ignored archive leakage, toolchain drift, and test-red deployment | queued — [H1911](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1911-Codex_SanskritGrammar_architecture-delivery-publication-safety_29.07.26.md) |
| 2 | Knauer book-pipeline pilot | Prove source authority, generation, discovery, hard cutover, and rollback on a bounded work | queued after H1911 — [H1912](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1912-Codex_SanskritGrammar_architecture-knauer-vertical-pilot_29.07.26.md) |
| 3 | SG-MO-021 Sangram pilot | Prove declared corpus pipeline and stable scholarly/data semantics | queued after H1911 — [H1913](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1913-Codex_SanskritGrammar_architecture-sg-mo-021-vertical-pilot_29.07.26.md) |
| 4 | Wave-2 factory migration ranking | Pilot cost must determine batch size and order | parked until H1912/H1913 publish measured effort |
| 5 | Separate-package/repository extraction | Extraction is justified only by stable external consumers | parked until W4 evidence |

## Known limitations

1. The implementation layer is root-authored best-effort because the configured Planner failed.
2. Later-wave effort is directional; only Wave 1 is file-level and execution-ready.
3. Auto-discovery was retained by author ruling. The plan can bound it, but cannot make it as
   explicit as a publication allowlist.
4. Hard cutover deliberately rejects a compatibility release; consumer census quality is
   therefore load-bearing.
5. Publication-rights uncertainty is not a stop condition by author ruling. The plan prevents
   invented claims and requires neutral provenance language, but it does not perform a rights
   audit.
6. The local planning checkout was stale and dirty; all authored work was isolated on a fresh
   `origin/main` worktree.

## Intended use and known misuse

- Use the PLAN as the single entry point and execute only the named handoff slice.
- Do not treat later roadmap waves as permission to bypass pilot gates.
- Do not read “modular monorepo” as permission to reimplement canonical Sanskrit/corpus assets.
- Do not treat `work.yml` or a pipeline manifest as a publication allowlist; the author retained
  safe auto-discovery.
- Do not use the architecture plan to change scholarly content or consume issue 563 output.

## Maintenance and sunset

- Update this metadoc when a handoff lands: keep the backlog row, mark it complete, and add the PR.
- Re-estimate W2 from measured H1912/H1913 cost and defects.
- Sunset when W4 closes and a measured successor roadmap is accepted, or mark superseded if the
  modular-monorepo decision is explicitly reversed.

## Related documents

- [Portfolio umbrella](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md)
- [Architecture roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_ARCHITECTURE_2026_2027.md)
- [Architecture specification](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANSKRITGRAMMAR_MODULAR_MONOREPO.md)
- [Wave-1 implementation](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md)
- [Verification and autonomy gate](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION.md)

## Revision history

| Date | Change | By |
|---|---|---|
| 29-07-2026 | Created with five-layer plan, 23 rulings, PASS autonomy gate, and H1911–H1913 ownership | Codex |

_Dr. Mārcis Gasūns_
