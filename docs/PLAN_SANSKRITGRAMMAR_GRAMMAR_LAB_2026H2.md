# Plan — SanskritGrammar Grammar Lab concordance and paid learner service (2026 H2)

_Created: 09-08-2026 · Last updated: 14-08-2026_

This is the cover/index for the execution-ready `/ask` plan that turns the existing
SanskritGrammar concordances, indexes, dictionary links, and corpus evidence into a paid
**Grammar Lab** inside
[Systema-Sanscriticum](https://github.com/gasyoun/Systema-Sanscriticum). The first vertical
slice covers root alternation and verbal morphology for current Russian-speaking intermediate
students. It uses Whitney and Zalizniak as equal source spines behind neutral topic IDs, while
preserving SanskritGrammar as the research/data owner and Systema as the learner/product owner.

## Layer documents

| Layer | Document |
|---|---|
| Roadmap | [ROADMAP_SANSKRITGRAMMAR_GRAMMAR_LAB_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_GRAMMAR_LAB_2026_2027.md) |
| Architecture | [ARCHITECTURE_SANSKRITGRAMMAR_GRAMMAR_LAB.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANSKRITGRAMMAR_GRAMMAR_LAB.md) |
| Implementation | [IMPLEMENTATION_SANSKRITGRAMMAR_GRAMMAR_LAB.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANSKRITGRAMMAR_GRAMMAR_LAB.md) |
| Verification | [VERIFICATION_SANSKRITGRAMMAR_GRAMMAR_LAB.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANSKRITGRAMMAR_GRAMMAR_LAB.md) |
| Plan metadata | [PLAN_SANSKRITGRAMMAR_GRAMMAR_LAB_2026H2.meta.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_GRAMMAR_LAB_2026H2.meta.md) |

## Audit verdict

**Prior art: PARTIAL — build only the product gap.** Reuse the existing
[shared-sentence concordance](https://github.com/gasyoun/SanskritGrammar/tree/main/Concordance),
[Whitney subject concordance](https://github.com/gasyoun/SanskritGrammar/tree/main/SubjectConcordance),
[Type-D ID grammar](https://github.com/gasyoun/Uprava/blob/main/TYPED_LINK_ID_GRAMMAR.md),
[pedagogy export](https://github.com/gasyoun/SanskritGrammar/tree/main/data/pedagogy_export),
[DCS-derived assets](https://github.com/gasyoun/SanskritGrammar/tree/main/data), and Systema's
existing SRS/FSRS, drill, payment, tariff, and access machinery. The missing product gap is:

1. a neutral, source-provenanced grammar-topic graph joining Whitney and Zalizniak;
2. curated dictionary and corpus evidence cards for those topics;
3. multilingual hybrid semantic retrieval over the graph;
4. an entitlement-gated Systema explorer, comparison view, exercises, SRS, and recommendations;
5. a measured learner pilot and a provider-independent subscription entitlement.

This plan does **not** rebuild a Sanskrit normalizer, corpus index, dictionary endpoint,
concordance matcher, SRS scheduler, payment ledger, or course-access system.

## Decisions taken — 29 rulings from the 09-08-2026 interview

| # | Decision | Ruling and rationale |
|---:|---|---|
| 1 | Product | **Grammar Lab:** concordance, indexes, dictionary/corpus evidence, and interactive study tools. |
| 2 | Wave-1 shape | **One complete vertical slice**, not a broad unfinished inventory. |
| 3 | First audience | **Current Russian-speaking Systema students at Kochergina/intermediate level.** |
| 4 | Content spine | **Whitney and Zalizniak together**; neither is reduced to a decorative enrichment. |
| 5 | Commercial package | **Hybrid:** included with selected paid courses and sold as a standalone subscription. |
| 6 | Spine relationship | A **neutral concept layer** maps independently to Whitney, Zalizniak, textbooks, dictionaries, and corpora. |
| 7 | Record depth | Each topic is an **evidence graph record**, not merely a section crosswalk. |
| 8 | Delivery contract | SanskritGrammar emits a **versioned static bundle** imported by Systema. |
| 9 | Learner state | Bookmarks, mastery, attempts, recommendations, and entitlements live **only in Systema**. |
| 10 | Dictionary/corpus depth | Wave 1 uses **curated evidence cards** plus deep links, not bulk embedded dictionaries. |
| 11 | Paid boundary | A provider-independent **Grammar Lab entitlement** is granted by course ownership or active subscription. |
| 12 | First domain | **Root alternation and verbal morphology.** Sandhi waits for Emeneau. |
| 13 | Slice size | **25–40 curated topics.** |
| 14 | Learner tools | Ship explorer, comparison, evidence cards, generated drills, SRS, and personalized recommendations. |
| 15 | Authoring source | Curated **YAML/JSON in SanskritGrammar**, schema-validated and compiled to JSON/TSV. |
| 16 | Search | Russian, Devanagari, IAST, and SLP1 **semantic search from Wave 1**. |
| 17 | Exercise generation | Generated candidates are permitted; publication policy is refined by ruling 24. |
| 18 | Topic evidence | Every published topic has Whitney + Zalizniak anchors, dictionary evidence, corpus evidence or explicit non-attestation, provenance, and an exercise. |
| 19 | Editorial gate | Validators may publish **low-risk records** without universal expert review. |
| 20 | Search acceptance | Frozen multilingual set, **Recall@5 ≥ 0.85**, lexical fallback, attribution, and no entitlement leakage. |
| 21 | Learner validation | Staging acceptance, then a consented **5–10-student Systema pilot**. |
| 22 | Exercise review | Automatic publication is allowed subject to the risk-tier policy in ruling 24. |
| 23 | Paid acceptance | Automated entitlement matrix plus sandbox flows; no production charge required. |
| 24 | Final exercise policy | **Risk-tiered automation:** deterministic low-risk items may auto-publish after strict validation, 20% expert sampling, and instant rollback; interpretive items require prior approval. |
| 25 | Semantic implementation | **Offline hybrid retrieval:** BM25 plus a reusable multilingual embedding model; no paid runtime API or hosted vector database. |
| 26 | Ambiguity | Technical ambiguity → default + log; scholarly ambiguity → `needs_review`, omit from publication, continue. |
| 27 | Stop conditions | Halt only on an absolute fence, data-loss/security risk, irreconcilable schema conflict, or whole-handoff impossibility. Missing Emeneau parks Sandhi only. |
| 28 | Execution authority | Four Grok 4.5 handoffs may branch, implement, test, commit, PR, and merge green; no production activation. |
| 29 | Fence | No csl-orig edits, production charges/activation/flag flip, secrets, generated-MDX hand edits, Sandhi before Emeneau, or bulk source-text publication. |

## Autonomy contract

1. **On ambiguity:** apply the documented technical default and record it in the PR and
   `.ai_state.md`. If the ambiguity is scholarly, mark only the affected record
   `needs_review`, exclude it from the publishable bundle, and continue.
2. **Stop only for:** an absolute fence; credible data-loss or security risk; an
   irreconcilable schema conflict; or a failure that makes the whole handoff impossible.
   A missing source or a failed record is a scoped omission, not a wave-wide stop.
3. **Authority:** each scoped Grok 4.5 handoff may create a branch/worktree, implement, test,
   commit, open a PR, and merge once required checks are green. It may not activate production
   billing, subscriptions, cohorts, or feature flags.
4. **Fence:** no direct `csl-orig` edits; no secrets; no production charge or subscription
   activation; no production feature-flag flip; no manual edits to generated MDX; no Sandhi
   implementation before M.G. supplies Emeneau; no bulk publication of source text.
5. **Search fallback:** if the pinned local embedding runtime cannot deploy safely, keep the
   semantic flag OFF, ship lexical BM25 fallback, record the failed spike, and continue with
   the remaining handoff. Do not substitute a paid API without a new ruling.
6. **Generated content:** low-risk deterministic items may auto-publish only if validators
   pass, the 20% review sample is drawn reproducibly, and rollback is available. Interpretive
   items remain approval-gated.

## Wave-1 execution handoffs

The four handoffs are serial-safe at their boundaries:

| Lane | Handoff | Dependency |
|---|---|---|
| G1 | [H2492 (Grok 4.6) — Grammar Lab G1: Whitney + Zalizniak evidence graph and export](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2492-Grok_SanskritGrammar_grammar-lab-g1-evidence-graph_09.08.26.md) | This plan — **shipped 13-08-2026** (32 topics) |
| G2 | [H2493 (Grok 4.5) — Grammar Lab G2: Systema import, explorer, and offline hybrid search](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2493-Grok_Systema-Sanscriticum_grammar-lab-g2-systema-search-ui_09.08.26.md) | G1 merged |
| G3 | [H2494 (Grok 4.5) — Grammar Lab G3: risk-tiered drills, FSRS, mastery, and recommendations](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2494-Grok_Systema-Sanscriticum_grammar-lab-g3-learning-loop_09.08.26.md) | G2 stable topic/import contract merged |
| G4 | [H2495 (Grok 4.6) — Grammar Lab G4: hybrid entitlement, sandbox matrix, and learner pilot](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2495-Grok_Systema-Sanscriticum_grammar-lab-g4-entitlement-pilot_09.08.26.md) | G2 + G3 merged — **shipped 14-08-2026** (flags OFF; [Systema PR #1665](https://github.com/gasyoun/Systema-Sanscriticum/pull/1665)) |

Ordered implementation details are in the
[implementation document](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANSKRITGRAMMAR_GRAMMAR_LAB.md).

Literal plan starter carried by every handoff:

```text
Read C:\Users\user\Documents\GitHub\SanskritGrammar\docs\PLAN_SANSKRITGRAMMAR_GRAMMAR_LAB_2026H2.md and execute it.
```

## Autonomy-readiness gate

| Check | Verdict |
|---|---|
| Architecture for every Wave-1 deliverable | **PASS** — boundaries, schemas and owners are fixed. |
| Ordered implementation steps | **PASS** — G1 → G2 → G3 → G4 with file-level sequences. |
| Acceptance criteria | **PASS** — data, retrieval, access and pilot criteria are executable. |
| Risks and spikes | **PASS** — local embeddings, source coverage, automation and entitlement risks have defaults. |
| Blocking forks | **PASS** — all 29 interview decisions are resolved. |
| Rebuild prevention | **PASS** — prior-art inventory names every reused system. |

**Gate verdict: PASS.** The plan can be executed unattended within the stated fences.

---

_Dr. Mārcis Gasūns_
