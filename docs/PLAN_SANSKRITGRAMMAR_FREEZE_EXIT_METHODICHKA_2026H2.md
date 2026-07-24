# Plan — SanskritGrammar freeze exit + methodichka residual (2026 H2, Pass 4)

_Created: 24-07-2026 · Last updated: 24-07-2026_

**This is the cover/index** for the next unattended agent wave in
[SanskritGrammar](https://github.com/gasyoun/SanskritGrammar), staged by
[`/ask-batch`](https://github.com/gasyoun/claude-config/blob/main/commands/ask-batch.md)
Pass 4 (`--repos SanskritGrammar`, 24-07-2026). It **succeeds** the drained editorial-notes plan
[`docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md)
(H1273–H1277 executed). That plan remains the historical record of the visa-note apply wave; do not
re-execute it.

**Goal in one paragraph.** Sangram's consolidation freeze is still **active**: of 26 baseline
candidates, **11 are published and 15 sit at `disposition=unknown` with `visa=not_submitted`**. In
parallel, **19 OPEN / 3 PARTIAL** editorial notes remain (mostly Kochergina + Apte methodichkas and
six A65 research notes). Wave 1 runs **two equal fronts**: (A) per-article C5/C6 kill-gate probes on
the 15 unknowns, then visas only for survivors (one SE multi-article sheet for SE survivors); (B)
methodichka residual — keep [H1454](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1454-Fable_SanskritGrammar_kochergina-metodichka-v1-open-items_22.07.26.md)
and mint Apte residual. Human M03 RWS review and RQ4 feature flip stay GTD `@DO`, not agent work.

## Layer docs

| Layer | Document |
|---|---|
| Roadmap (waves, gates) | [`docs/ROADMAP_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md) |
| Architecture | [`docs/ARCHITECTURE_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA.md) |
| Implementation | [`docs/IMPLEMENTATION_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA.md) |
| Verification | [`docs/VERIFICATION_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA.md) |
| This doc's companion | [`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.meta.md) |

Portfolio order of record (unchanged):
[`ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md).

## Decisions taken (Pass 4 interview, 24-07-2026)

| Fork | Ruling | Rationale / consequence |
|---|---|---|
| `capacity-aug-oct` | **Freeze exit + methodichka residual in parallel** | Two equal agent fronts through Oct; human M03/RQ4 remain `@DO`. |
| `freeze-exit-mechanism` | **Probe-first C5/C6 kill-gates; visas only for survivors** | Clear failures → `kill_gated` without human visa; survivors get sheets. |
| `se-cluster-batching` | **One SE multi-article visa sheet for SE survivors** | Non-SE survivors: second small sheet or individual cards. |
| `methodichka-vs-freeze` | **Methodichka elevated to wave-1 equal with freeze** | H1454 kept; Apte residual minted; Fable capacity shared. |
| `probe-instrument` | **Per-article C5/C6 kill-gate named in the programme** | No uniform re-derive substitute for programme gates. |
| `papers-arm` | **Execute existing handoffs only; mint nothing new** | H1464–H1466 / H1476 optional parallel; A54/A61 human-gated. |
| `stale-handoff-hygiene` | **One Sonnet archive/triage handoff** | Improves `/next-task` signal. |
| `autonomy-on-ambiguity` | **Park-and-skip + ledger `blocking_note`; never invent scholarly judgment** | No invented kill thresholds; no published-number edits without evidence. |
| `verification-bar` | **Committed probe artifact + ledger row + green validators** | Kill/reject only with explicit C5/C6 criterion citation. |
| `fence` | **No M03 body prose rewrite; no RQ4 protocol change; no `freeze.active` flip without exit criterion** | May edit candidates, methodichkas, probes, ledger, review sheets. |
| `stop-conditions` | **Hard-stop on build red after 2 repair tries, rights/PII, or freeze-criterion dispute** | Else park-and-skip. |
| `plan-docs-home` | **New five-doc set; leave 18-07 editorial plan as historical** | Successor pointer only on the old cover. |

## Autonomy contract (verbatim)

1. **On ambiguity** — park-and-skip: set ledger `blocking_note` or note-index `ESCALATED`/`OPEN` with evidence; do **not** invent kill-gate thresholds, do **not** change published DCS figures without a re-run artifact, do **not** invent methodichka bibliographic claims. Continue the next in-scope item.
2. **Hard stop** — `npm run build` or `pytest` still red after two repair attempts; any rights-gated corpus publish; disagreement about whether a kill-gate criterion is met (surface as `@DECIDE`, do not flip disposition).
3. **Commit authority** — handoff-scoped commit → PR → merge is allowed for wave-1 handoffs of this plan. Work only in a fresh worktree off `origin/main` (repo has `.githooks` shared-tree guard).
4. **Fence** — must not rewrite GasunsDhatu chapter body prose; must not alter RQ4 protocol/item bank design; must not set `freeze.active=false` until every `baseline_ids[]` row has disposition in `{published, revised, rejected, kill_gated}`.
5. **Prior art** — reuse `scripts/consolidation_ledger_refresh.py`, `scripts/article_validate.py`, article-local probe scripts under `sangram/articles/*/`, `sangram/audit/probe_*`, and programme kill-gates in
   [`sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx) /
   [`sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx). Do not rebuild the ledger or visa-sheet emitter.

## Measured ground truth (24-07-2026)

| Surface | Count |
|---|---|
| Freeze baseline candidates | 26 (11 published · **15 unknown**) |
| Unknown toc_refs | SG-SE-004, SG-MO-019, SG-WF-009, SG-SE-001, SG-MO-024, SG-SE-008, SG-MO-025, SG-SE-003, SG-SE-013, SG-WF-002, SG-SE-005, SG-SE-002, SG-SE-006, SG-MO-022, SG-WF-011 |
| Editorial notes (index) | 81 total · 54 APPLIED · **19 OPEN** · 3 PARTIAL · 3 ANSWERED · 1 ESCALATED · 1 DEFERRED |
| OPEN by target | Kochergina ~11 · A65 6 · Apte 3 · style-guide 1 · future 1 |
| Already-owned | H1454 (Kochergina open-9) · H1259 PARTIAL (M03 human residual) · H1464–H1466 / H1476 (papers, optional) |

## Wave-1 handoff map

| Front | ID | Tier | Deliverable |
|---|---|---|---|
| A0 | [H1611](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1611-Sonnet_SanskritGrammar_freeze-15-killgate-matrix_24.07.26.md) | Sonnet | Matrix: toc_ref → C5/C6 kill-gate + script path + acceptance criterion |
| A1 | [H1612](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1612-Opus_SanskritGrammar_freeze-probe-se-cluster_24.07.26.md) | Opus | Probes for SE unknowns; artifacts + ledger updates |
| A2 | [H1613](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1613-Opus_SanskritGrammar_freeze-probe-mo-wf-stragglers_24.07.26.md) | Opus | Probes for MO/WF stragglers |
| A3 | [H1614](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1614-Sonnet_SanskritGrammar_freeze-se-survivor-visa-sheet_24.07.26.md) | Sonnet | One multi-article SE visa sheet for **survivors only** (blocked on H1612) |
| B0 | [H1454](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1454-Fable_SanskritGrammar_kochergina-metodichka-v1-open-items_22.07.26.md) | Fable | **Existing** — do not re-mint |
| B1 | [H1615](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1615-Fable_SanskritGrammar_metodichka-apte-open-residual_24.07.26.md) | Fable | Terminalise Apte OPEN/PARTIAL residual notes |
| C0 | [H1616](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1616-Sonnet_SanskritGrammar_sg-handoff-hygiene-archive-triage_24.07.26.md) | Sonnet | Archive/triage stale SanskritGrammar handoffs |

Optional parallel (existing, not re-minted): H1464, H1465, H1466, H1476, H1514.

## Autonomy-readiness gate

| Wave-1 deliverable | Arch | Steps | Acceptance | Risks | Gate |
|---|---|---|---|---|---|
| Kill-gate matrix | ✅ | ✅ | ✅ | programme ambiguity → park | PASS |
| SE / MO-WF probes | ✅ | ✅ | ✅ | missing instrument → escalate | PASS |
| SE survivor visa sheet | ✅ | ✅ | ✅ | blocked until A1 reports | PASS (serial) |
| Methodichka Apte residual | ✅ | ✅ | ✅ | scan-gated zan-19 stays human | PASS |
| H1454 Kochergina | ✅ (existing) | ✅ | ✅ | 9 research items | PASS (owned) |
| Hygiene | ✅ | ✅ | ✅ | none blocking | PASS |

**Gate verdict: PASS** for agent wave-1. Blocking human residue (not in wave-1 path): M03 RWS docx review, RQ4 `features.rq4_study` flip, A61 CfP formatting, Apte zan-19 Elizarenkova scan.

_Dr. Mārcis Gasūns_
