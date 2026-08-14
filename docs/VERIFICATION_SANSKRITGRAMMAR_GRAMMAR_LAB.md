# Verification — SanskritGrammar Grammar Lab

_Created: 09-08-2026 · Last updated: 14-08-2026_

Acceptance and risk register for the
[Grammar Lab plan](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_GRAMMAR_LAB_2026H2.md).

## 1. Acceptance matrix

| ID | Criterion | Proof | Failure means |
|---|---|---|---|
| A1 | 25–40 published root-alternation/verbal-morphology topics | Builder summary + committed manifest | G1 incomplete |
| A2 | Every published topic has Whitney and Zalizniak anchors | Schema validator and missing-anchor report = 0 | Topic becomes `needs_review` |
| A3 | Dictionary and corpus evidence present, or structured non-attestation | Evidence validator + provenance spot check | Topic not publishable |
| A4 | Type-D edges lint clean and stable IDs survive rebuild | Shared lint + fixture snapshot | Contract failure; stop G1 merge |
| A5 | Export is reproducible and hashes match | `python scripts/build_grammar_lab.py --check` | CI failure |
| A6 | All four scripts searchable | Frozen RU/Deva/IAST/SLP1 query file | Coverage failure |
| A7 | Hybrid search Recall@5 ≥0.85 | Versioned evaluation report with exact numerator/denominator | Semantic flag remains OFF |
| A8 | Lexical fallback works with sidecar unavailable | Feature test with semantic disabled | G2 failure |
| A9 | Unauthorized users receive no protected topic/vector/exercise payload | Route, API and serialization tests | Security stop |
| A10 | Import is idempotent and preserves learner history | Two imports + content-update fixture | G2 failure |
| A11 | Low-risk auto-publication obeys validators and reproducible 20% sample | Generation test + sample manifest | Auto-publication disabled |
| A12 | Interpretive item cannot publish without approval | Negative authorization/domain test | G3 failure |
| A13 | Exercise rollback restores prior version without deleting attempts | Version/attempt integration test | G3 failure |
| A14 | FSRS is reused and topic mastery/recommendation is deterministic | Existing FSRS vectors + new integration tests | G3 failure |
| A15 | Course, subscription, expiry, revocation and admin grants resolve correctly | Sandbox entitlement matrix | G4 failure |
| A16 | 5–10-student pilot reports four ruled outcomes with exact denominators | Pilot report and anonymized aggregate export | No production recommendation |
| A17 | No production charge or feature activation occurred | Config/deploy diff and operator checklist | Fence violation |

## 2. Commands and flows

Expected G1 commands:

```powershell
python scripts/build_grammar_lab.py
python scripts/build_grammar_lab.py --check
python -m pytest tests/test_grammar_lab*.py
npm run build
```

Expected Systema proof commands are added by G2–G4 to this document and must include focused
PHP tests plus the repository's required quality gates. The semantic benchmark command must
accept a frozen query file and emit machine-readable per-query ranks and aggregate Recall@5.

G4 (Systema, H2495, 14-08-2026):

```powershell
php artisan test --filter=GrammarLab
php artisan grammar-lab:rehearse-entitlement --json
php artisan grammar-lab:pilot-eligibility --json
php artisan grammar-lab:pilot-report
```

A15–A17: sandbox matrix is the rehearse command + `GrammarLabEntitlementLifecycleTest`;
pilot readout is “not human-authorized” until a roster is named;
production switches remain OFF (`GRAMMAR_LAB`, `GRAMMAR_LAB_PILOT`).

Manual staging flow:

1. Sign in as an entitled pilot user.
2. Search the same concept in Russian, Devanagari, IAST and SLP1.
3. Open one result; compare Whitney and Zalizniak; inspect dictionary and corpus evidence.
4. Complete a drill; add its topic to SRS; verify mastery and the next-topic reason.
5. Sign out or use an unentitled account; verify protected routes and payloads are denied.

## 3. Frozen semantic-search set

G1 supplies at least 100 judged queries distributed across the four scripts and these intent
classes: exact term, transliteration variant, Russian paraphrase, form-to-concept, root-to-topic,
and common learner misconception. Each query has one or more acceptable topic IDs. G2 may tune
fusion weights only on a designated development subset; the final test subset remains frozen.

Report Recall@1, Recall@5, mean reciprocal rank, lexical-only comparison, vector-only comparison,
hybrid score, latency and failures. The release gate is Recall@5 ≥0.85 on the frozen test subset.

## 4. Pilot measures

For 5–10 consented current Systema students:

- task completion: find and explain a ruled concept using both sources;
- quiz accuracy before/after the guided topic path;
- return use within the agreed pilot window;
- confusion: coded free-text and task-observation categories.

The report always shows `n`, missing observations and raw counts. It may recommend iteration; it
must not claim general learning efficacy from this sample.

## 5. Risks and spikes

| Risk | Default mitigation | Stop/continue rule |
|---|---|---|
| Zalizniak works lack uniform stable section IDs | Deterministic per-work section-locus registry, checked against source order | Stop only affected edge/topic |
| Offline embedding sidecar is operationally unavailable | Pinned deployment spike; lexical fallback remains live; semantic flag OFF | Continue G2, fail A7 visibly |
| Multilingual model confuses transliterations | Shared normalization + aliases + hybrid fusion; frozen four-script evaluation | Tune only on development set |
| Corpus absence is mistaken for linguistic impossibility | Structured `not_attested` includes corpus snapshot/query/limits | Topic withheld if wording overclaims |
| Generated distractor is plausible/ambiguous | Deterministic uniqueness/domain validators; `needs_review` or interpretive class | Withhold item, continue batch |
| Auto-published low-risk item is later rejected | Versioned content, kill switch, stored rejection and rollback | Roll back item, preserve attempts |
| Entitlement leaks protected data through search/API/cache | One resolver at controller, serializer and cache-key boundaries | Security stop; no merge |
| Existing billing providers encode access differently | Capability resolver consumes normalized lifecycle, never raw provider state | Sandbox adapter failure blocks G4 |
| Emeneau unavailable | Sandhi stays outside schemas, topic set and handoffs | Continue all non-Sandhi work |
| Rights/source-text concern | Concise evidence, citation and deep link; no bulk source text | Omit affected payload, continue |

## 6. Autonomy gate checklist

- [x] Every Wave-1 lane has an architecture contract.
- [x] Every lane has ordered file-level implementation steps.
- [x] Every deliverable has an acceptance criterion.
- [x] Every identified risk has a default and stop/continue rule.
- [x] Semantic-search failure has a safe, visible fallback rather than a paid substitution.
- [x] Sandhi is explicitly fenced until Emeneau is supplied.
- [x] Production billing and activation remain human actions.

---

_Dr. Mārcis Gasūns_
