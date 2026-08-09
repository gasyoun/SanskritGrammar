# Roadmap — SanskritGrammar pedagogy last-mile residual (2026 H2 wave-1)

_Created: 25-07-2026 · Last updated: 09-08-2026_

Wave structure for the plan whose cover is
[`docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md).
This roadmap is **wave-1 only** (ruling 3). Later portfolio tracks (M03 freeze,
Sangram consolidation exit, paper venues) keep their own roadmaps.

**Successor product layer (09-08-2026):** the export and local Systema smoke this roadmap
specified are shipped. The next learner/revenue wave is the
[Grammar Lab roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_GRAMMAR_LAB_2026_2027.md):
a Whitney + Zalizniak concordance and evidence graph feeding semantic search, exercises, SRS,
recommendations and a hybrid paid entitlement. This document remains the integration-contract
history; it is not expanded into the new product spec.

## 1. Relation to existing roadmaps

| Doc | Role after this plan |
|---|---|
| [`ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) | Portfolio umbrella — **unchanged order for the estate**; this plan’s *capacity* is parallel pedagogy, not a re-rank of M03 |
| [`docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md) | Field roadmap — wave-1/2 research builds largely **done**; this plan is the **integration residual** |
| [`docs/ROADMAP_SANSKRITGRAMMAR_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_2026H2.md) | Sangram editorial notes — **out of scope** except shared CI/claims gates (≤20%) |

## 2. Wave shape

Waves open on **contracts**, not calendar dates.

| Wave | Opens when | Closes when | Owner handoffs |
|---|---|---|---|
| **W1 · Residual last-mile** | This plan merges | H-A terminal + H-B export green + H-C smoke documented PASS | H-A, H-B, H-C |
| **W2 · (sketch only)** | W1 closed + human wants prod RQ4 | Production `features.rq4_study` flip + cohort ops | Human @DO / H1261 residual — **not minted here** |
| **W3 · (sketch only)** | W1 closed + rights GO | Optional public deck expansion beyond public-domain demo | Deferred rights programme |

## 3. Wave-1 deliverables

| ID | Deliverable | Unblocks |
|---|---|---|
| **D1** | Methodichka notes in scope terminal (APPLIED / DEFERRED / re-sheeted) | Clean companions for learners; removes visa backlog noise |
| **D2** | Re-vote sheets for `zan-29` + WF004-03/04/07-class items (if still open) | Unblocks blocked reject/null cards without inventing research |
| **D3** | `data/pedagogy_export/` versioned package + `scripts/build_pedagogy_export.py` + pytest `--check` | Machine contract for Systema (and future kosha) |
| **D4** | `docs/LAST_MILE_PIPELINE_SPEC.md` gap section updated to 2026 measured state (Hops A/B/C + RQ4 already in Systema) | Stops agents from re-spec’ing shipped work |
| **D5** | One E2E smoke: export → Systema local load → ≥1 item renders; command in VERIFICATION | Proves last mile is not only prose |

## 4. Explicit non-goals (ruling 4 + fence)

- No new ARTICLES IDs / paper scaffolds (A54–A65 polish only if a methodichka note *requires* a citation fix — default: skip paper files).
- No new Sangram topic or article manifests; no freeze-ledger mass disposition.
- No M03 RWS prose application or publisher contact.
- No third-party rights audit; no publishing rights-gated bulk.
- No production flip of `features.rq4_study`.
- No live kosha API dependency (vendored-file contract stands).
- No greenfield learner mini-app inside SanskritGrammar.

## 5. Capacity note (ruling 2 + 10)

Portfolio tracks M03 and Sangram freeze continue on **their own** handoffs outside this budget.
This plan may spend **≤20%** of agent hours only on **shared** claims/errata/CI gates if a pedagogy step is blocked by them. If unused, bank the 20% — do not invent freeze work.

## 6. Cadence

| Phase | Expected duration | Exit signal |
|---|---|---|
| W1 authoring (this plan) | 1 session | Plan PR merged |
| W1 H-A + H-B | 1–2 sessions each | Green merges |
| W1 H-C | 1 session after H-B | Smoke log in VERIFICATION / RESULTS |

---

_Dr. Mārcis Gasūns_
