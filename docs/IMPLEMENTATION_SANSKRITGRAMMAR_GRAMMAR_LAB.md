# Implementation — SanskritGrammar Grammar Lab Wave 1

_Created: 09-08-2026 · Last updated: 13-08-2026_

Ordered build sequence for the
[Grammar Lab plan](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_GRAMMAR_LAB_2026H2.md).
Each lane is one Grok 4.5 execution handoff and may merge only after its dependency is available.

## G1 — concordance and evidence bundle

1. Audit the exact source identifiers in WhitneyRoots and all three Zalizniak folders; create a
   deterministic Zalizniak section-locus registry only where stable loci are absent.
2. Add `data/grammar_lab/schemas/` for topic, Type-D edge, evidence, exercise and manifest
   contracts, with valid/invalid fixtures under `tests/fixtures/grammar_lab/`.
3. Add 5 representative topics spanning alternation, root type, grade, attestation and
   homonymy; make them pass the full evidence contract before scaling.
4. Build the remaining 20–35 topic records, reusing existing root crosswalks and DCS-derived
   files. Record `not_attested` honestly; never convert absence in a sample into linguistic
   impossibility.
5. Add deterministic low-risk exercise candidates plus interpretive placeholders; assign
   `risk_class` and publication status.
6. Implement `scripts/build_grammar_lab.py` with build and `--check`, emitting bundle, Type-D
   TSV, manifest and hashes.
7. Implement `scripts/grammar_lab_embed.py` using the pinned reusable multilingual model; record
   model name, revision, dimensionality and source-text hash in the vector artifact.
8. Add pytest coverage and wire `python scripts/build_grammar_lab.py --check` into CI.
9. Update README, CHANGELOG, `.ai_state.md`, and relevant cross-repo feed registry.

**Exit:** 25–40 publishable topics; zero schema/Type-D/hash errors; 5-topic fixture and full
bundle reproduce; every published topic satisfies the evidence contract.

**Status 13-08-2026 (H2492):** shipped — 32 published topics, 1 `needs_review` omit, 182 Type-D
edges, 192 frozen queries, `--check` and `tests/test_grammar_lab.py` green.

## G2 — Systema import, explorer and semantic search

1. Pin a G1 release/commit and vendor the manifest/bundle through an idempotent Artisan sync
   command, following the shipped pedagogy-export pattern.
2. Add migrations/models for topics, source edges, bookmarks, views and content versions. Preserve
   learner rows across content re-imports and represent retired topics explicitly.
3. Add one provider-independent `grammar_lab` authorization check and apply it to every protected
   route and response serializer before building UI.
4. Build the Russian learner explorer: browse/index, topic detail, Whitney↔Zalizniak comparison,
   dictionary/corpus evidence cards, provenance and deep links.
5. Add normalized lexical/BM25 search using shared Sanskrit normalization.
6. Add the pinned local embedding sidecar, query/topic parity check, cosine scorer and deterministic
   BM25/vector fusion. Keep it behind `features.grammar_lab_semantic` until verification passes.
7. Add bookmark/history behavior and accessibility/keyboard/error states.
8. Add unit, feature and authorization tests, including response-payload denial tests.

**Exit:** idempotent import; entitled explorer works; unauthorized requests reveal no protected
payload; frozen query set Recall@5 ≥0.85; lexical fallback remains usable with semantic OFF.

## G3 — generated drills, FSRS and recommendation

1. Map published Grammar Lab exercises into the existing SRS note/deck/card model using stable
   topic and exercise version IDs.
2. Implement validators for deterministic answer equivalence, normalization, distractor
   uniqueness, source presence and topic-version compatibility.
3. Implement deterministic 20% sampling, reviewer decision storage, a kill switch and rollback to
   the previous published exercise version.
4. Prevent all `interpretive` exercises from publication without an explicit approval record.
5. Add attempt/mastery projection without duplicating FSRS scheduling state.
6. Add an explainable prerequisite/weakness/overdue-card recommendation service and surface the
   reason to the learner.
7. Test generation rejection, rollback, SRS scheduling compatibility, mastery transitions,
   recommendation determinism and authorization.

**Exit:** low-risk items can safely auto-publish under the ruled policy; interpretive items cannot;
attempt → mastery → SRS/recommendation works end-to-end with reversible content versions.

## G4 — entitlement, sandbox subscription and pilot

1. Finalize the `grammar_lab` capability resolver for selected course ownership, standalone active
   subscription and time-bounded admin/pilot grants.
2. Exercise provider-independent grant/revoke lifecycle against existing billing/subscription
   services in sandbox; do not activate or charge production.
3. Build the entitlement matrix: guest, authenticated-unentitled, course-entitled,
   subscription-entitled, expired, revoked and admin-granted.
4. Add pilot consent/assignment/instrumentation for 5–10 current Russian-speaking intermediate
   students, reusing Systema privacy and study patterns.
5. Measure task completion, quiz accuracy, return use and confusion; report exact denominators and
   abstain from population-level claims.
6. Produce a human activation packet: pricing/SKU fields to fill, course inclusion list, feature
   flags, rollback, support copy and production smoke steps.

**Exit:** sandbox entitlement matrix green; pilot can run without a production charge; pilot
readout and human activation packet exist; all production switches remain OFF.

**Status 14-08-2026 (H2495):** shipped in Systema
[PR #1665](https://github.com/gasyoun/Systema-Sanscriticum/pull/1665) — `canUse()` resolves
course / subscription / admin / pilot grants identically; expiry and revocation deny;
`grammar-lab:rehearse-entitlement` sandbox matrix; consent + instrumentation dark behind
`GRAMMAR_LAB_PILOT`; activation packet and “pilot not human-authorized” readout committed.
No production charge or flag flip.

## Required sequencing and merge discipline

```text
G1 data contract → G2 import/search → G3 learning loop → G4 entitlement/pilot
```

G3 may begin after G2's schema/import contract merges even if UI polish continues. G4 may build
the resolver tests after G2 but must not run the pilot until G3 acceptance is green. Each handoff
uses an isolated worktree, targeted commits, green required checks, and the autonomy contract in
the plan index.

---

_Dr. Mārcis Gasūns_
