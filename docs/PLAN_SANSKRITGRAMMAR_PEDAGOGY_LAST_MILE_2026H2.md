# Plan — SanskritGrammar pedagogy last-mile + RQ4 residual (2026 H2 wave-1)

_Created: 25-07-2026 · Last updated: 25-07-2026_

**This is the cover/index** of a layered `/ask` plan for [SanskritGrammar](https://github.com/gasyoun/SanskritGrammar).
It is **not** a re-foundation of the digital-pedagogy field (that remains
[`docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md))
and **not** a re-ordering of the portfolio umbrella
([`ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md)).
It is the **next executable wave** the author selected on 25-07-2026: close the
learner last-mile residual, clear methodichka human-gate debt, ship a versioned
research→product export from this repo, and smoke one real hop in Systema
**without** flipping production flags.

**Goal in one paragraph.** SanskritGrammar already has the difficulty/ordering
result, the RQ4 item bank, methodichka companions (including corpus layers), and
a last-mile *spec*; Systema already has Hop A/B/C demos and the RQ4 harness
behind `features.rq4_study` (OFF). Wave-1 of *this* plan turns residual
methodichka visas into terminal notes, packages public-safe pedagogy feeds as a
semver’d JSON/TSV export with a CI `--check` validator, updates the last-mile
spec to measured 2026 reality, and proves **one** end-to-end path
(export → Systema loads → item renders) on local/staging only.

## Layer docs

| Layer | Document |
|---|---|
| Roadmap (waves, non-goals) | [`docs/ROADMAP_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md) |
| Architecture (boundaries, adapter contract) | [`docs/ARCHITECTURE_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE.md) |
| Implementation (three handoffs, ordered steps) | [`docs/IMPLEMENTATION_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE.md) |
| Verification (acceptance + risks) | [`docs/VERIFICATION_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE.md) |
| This doc’s companion record | [`docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.meta.md) |

Related (do not rewrite; cite):

- Field metadoc: [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md)
- Prior last-mile spec: [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md)
- RQ4 protocol: [`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md)
- Portfolio order: [`ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md)

## Decisions taken (25-07-2026 `/ask` interview — 30 rulings)

Execution agents trust these without re-deriving.

| # | Decision | Ruling | Rationale |
|---|---|---|---|
| 1 | Primary “done” outcome | **Pedagogy last-mile + RQ4 residual** | Spec and most harnesses exist; residual is gate-debt + one proven hop |
| 2 | Portfolio capacity model | **Parallel capacity, not strict M03-first for this plan** | This plan’s budget is pedagogy-primary; M03/Sangram keep their own tracks |
| 3 | Time horizon | **Wave-1 only (~2–4 weeks / one 5–8h agent run family)** | Classic `/ask` autonomy window |
| 4 | Non-goals | **No new A## papers; no new Sangram topics; no rights audit** | Park scaffolds; freeze and rights stay outside |
| 5 | Agent-hour emphasis | **Human-gate debt reduction** | Visas/apply unblock everything else |
| 6 | Merge authority | **Commit → PR → merge green** on SG and Systema | Handoff-scoped; no force-push |
| 7 | Product surface | **Systema consumer; SG ships data/specs only** | Research vs product boundary |
| 8 | Last-mile deliverable | **Close LAST_MILE gaps + smoke one real hop** | Not full production RQ4 flip |
| 9 | Human-gate class in-scope | **Methodichka visas + re-votes** (incl. `zan-29`, WF004-07 class) | Pedagogy companions only |
| 10 | M03 / freeze under parallel capacity | **≤20% thin budget: shared gates only** | No M03 RWS prose; no freeze disposition unless a shared CI/claims gate breaks |
| 11 | Build-vs-reuse | **Reuse + one thin adapter in SG** | No second study harness |
| 12 | Primary boundary | **Research (SG) vs product/study (Systema)** | Prevents a second app in this repo |
| 13 | Work split | **Three handoffs: visas · adapter · smoke** | Serial-safe gates |
| 14 | Adapter shape | **Versioned JSON/TSV + schema + `--check` validator** | semver in manifest; CI-gated |
| 15 | File layout | **`docs/` + `data/` + `scripts/` only** | No new top-level programme folder |
| 16 | Tests | **pytest adapter + SG suite green; Systema smoke command documented** | No full dual-CI rewrite required |
| 17 | Hop smoke acceptance | **export → Systema loads → ≥1 item renders** | No cohort recruitment |
| 18 | Visa/apply acceptance | **Zero OPEN methodichka notes in scope** (APPLIED / DEFERRED / re-sheeted) | Cite sheet_id+item_id |
| 19 | Russian prose bar | **Author register; no invented corpus numbers** | RESEARCH → probe stub |
| 20 | Schema policy | **semver + `--check` fails on drift** | Systema pins min version |
| 21 | HOLD vs soft-fail | **Almost never HOLD** — absolute fences only | Default + log for technical ambiguity |
| 22 | Success reporting | **VERIFICATION checklist + GTD/RESULTS + issue comment if tracking** | Durable trail |
| 23 | Ambiguity | **Pick plan default, log, continue** | Unattended run |
| 24 | Stop conditions | **Absolute fences only** | csl-orig, secrets, publish-safety NO-GO, destructive wipe, missing credentials that make the whole handoff impossible |
| 25 | Fence (must NOT touch) | **csl-orig · rights-gated bulk publish · M03 RWS prose · new Sangram topics · money contour** | Plus no new papers |
| 26 | Production feature flags | **Local/staging smoke only — never flip prod `features.rq4_study` unattended** | Prod flip remains human @DO (H1261 residual) |
| 27 | Model tiers | **Visas/apply: Fable 5 · Adapter: Sonnet 5 · Smoke: Sonnet 5** | Register vs mechanical |
| 28 | Prior-art rule | **Do not re-implement Hops A/B/C or RQ4 harness** | Systema H955/H959/H965/H987 already shipped |
| 29 | Adapter payload (default) | **Public-safe feeds only:** RQ4 item bank pointer+checksum, difficulty_ordering stats/TSVs, methodichka corpus-layer manifest paths, last-mile hop status | No in-copyright bulk gloss dump |
| 30 | Thin parallel 20% | **Shared claims/errata/CI gates if pedagogy needs them; else unused** | Bank the 20% rather than invent freeze work |

## Autonomy contract (verbatim for wave-1 agents)

1. **On unplanned ambiguity:** pick the marked default in this plan (or the nearest recommended option in IMPLEMENTATION), **log** path + choice in the PR body and `.ai_state.md`, continue. Do not wait for a human.
2. **Stop conditions (HOLD):** only absolute fences — (a) any csl-orig direct edit, (b) secret/credential leak, (c) `/publish-safety-check` NO-GO for a publish action, (d) destructive data wipe, (e) missing credentials that make the **entire** handoff impossible. Soft-fail: individual RESEARCH notes → probe stub; single flaky network call → retry once then log.
3. **Commit authority:** commit → open PR → **merge green PRs autonomously** in SanskritGrammar and Systema-Sanscriticum for these three handoffs. No force-push, no history rewrite, no main-tree commits if hooks forbid (use worktree).
4. **Fence — must NOT touch:** csl-orig; rights-gated bulk corpus publish; M03 RWS prose / yellow-review docx application; new Sangram topic/article manifests; Systema money/payment contour; production `features.rq4_study` flip; new ARTICLES A## scaffolds.
5. **Provenance:** every deliverable records model tier **and** exact version (e.g. Fable 5 `claude-fable-5`, Sonnet 5 `claude-sonnet-5`).
6. **Worktree discipline:** prefer an isolated worktree on shared-contention clones; pathspec commits.

## Wave-1 handoffs

**Prior-art collision (25-07-2026 mint):** methodichka residual is **already staged** by the freeze-exit plan
([`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md))
as **H1454** (Kochergina) + **H1615** (Apte). This plan **does not re-mint** H-A; it **consumes** those handoffs as the methodichka front. The **new** work is H-B (export) + H-C (smoke).

| # | Role | Model | Repo | ID / path |
|---|---|---|---|---|
| H-A | Methodichka residual (reuse — do not re-mint) | Fable 5 | SanskritGrammar | [H1454](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1454-Fable_SanskritGrammar_kochergina-metodichka-v1-open-items_22.07.26.md) · [H1615](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1615-Fable_SanskritGrammar_metodichka-apte-open-residual_24.07.26.md) |
| H-B | Thin pedagogy export adapter + LAST_MILE gap close | Sonnet 5 | SanskritGrammar | [H1643](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1643-Sonnet_SanskritGrammar_pedagogy-export-adapter-last-mile_25.07.26.md) |
| H-C | Systema local/staging hop smoke against H-B export | Sonnet 5 | Systema-Sanscriticum | [H1644](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1644-Sonnet_Systema-Sanscriticum_pedagogy-export-hop-smoke_25.07.26.md) |

Execution order: **H-A ∥ H-B** (disjoint files), then **H-C** (depends on H-B artifact on a merged main or a reachable commit). Re-vote cards (`zan-29`, WF004-03/04/07) stay on H1615 / a follow-up sheet from that handoff — not a third parallel mint.

## Autonomy-readiness gate — verdict

| Check | Result |
|---|---|
| Every wave-1 deliverable has arch + steps + acceptance + risks | **PASS** (layer docs) |
| Zero blocking forks remain | **PASS** (30 rulings; residual choices have logged defaults) |
| No rebuild-what-exists | **PASS** (prior-art: Hops A/B/C, RQ4 harness, item bank, difficulty data cited) |
| Autonomy contract covers plausible ambiguities | **PASS** (default+log; fences; no prod flag) |

**Gate: PASS.** Safe to mint and launch wave-1.

## How to execute (one-line starters)

After mint, each handoff body carries a fenced starter. The plan index for any of them:

```text
Read C:\Users\user\Documents\GitHub\SanskritGrammar\docs\PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md and execute the wave-1 handoff named in that chat (H-A, H-B, or H-C per IMPLEMENTATION).
```

Folder: `C:\Users\user\Documents\GitHub\SanskritGrammar` (H-A/H-B) or `C:\Users\user\Documents\GitHub\Systema-Sanscriticum` (H-C). Model tier per table above.

---

_Dr. Mārcis Gasūns_
