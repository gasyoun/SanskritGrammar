# Roadmap — SanskritGrammar Grammar Lab (2026–2027)

_Created: 09-08-2026 · Last updated: 09-08-2026_

This roadmap is the delivery layer of the
[Grammar Lab plan](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_GRAMMAR_LAB_2026H2.md).
It extends the completed pedagogy export/Systema hop into a paid learning product without
changing the portfolio's M03 and Sangram scholarly priorities.

## 1. Product outcome

A Russian-speaking Systema student can search a grammar concept in Russian, Devanagari, IAST,
or SLP1; compare Whitney and Zalizniak; inspect curated dictionary and corpus evidence; practise
the concept through validated drills and FSRS; receive a simple mastery-based next-topic
recommendation; and retain access through either an included course entitlement or a standalone
Grammar Lab subscription.

## 2. Waves and gates

| Wave | Deliverables | Opens when | Closes when |
|---|---|---|---|
| **W0 · Contract freeze** | Neutral topic schema, Type-D mapping, source/evidence policy, rights-safe excerpt rules, ID registry | This plan merges | Schema fixtures validate and 5 representative topics round-trip |
| **W1 · Root alternation vertical slice** | 25–40 publishable topics, Whitney + Zalizniak anchors, dictionary/corpus evidence, versioned bundle, local topic vectors | W0 green | Every published topic meets the evidence contract; bundle regenerates byte-stably except declared timestamps |
| **W2 · Paid Systema explorer** | Importer, topic/comparison/evidence UI, multilingual BM25 + local-vector search, bookmarks/history | W1 bundle available | Frozen search set Recall@5 ≥0.85; entitled users pass; unauthorized users receive no protected payload |
| **W3 · Learning loop** | Risk-tiered generated drills, 20% review sample, rollback, Grammar Lab SRS deck, mastery and recommendations | W2 topic IDs stable | Deterministic answers validate; interpretive items remain queued; attempt→mastery→recommendation round-trip passes |
| **W4 · Commercial and learner pilot** | Provider-independent entitlement, course inclusion, standalone sandbox subscription, expiry/revocation, 5–10-student pilot packet and readout | W2 + W3 green | Entitlement matrix passes; pilot reports task completion, accuracy, return use and confusion without overstating n |
| **W5 · Expansion** | Additional morphology/syntax domains, teacher authoring, richer corpus views | W4 evidence reviewed | A separate `/ask` rules the next domain and commercial activation |

## 3. Wave-1 topic envelope

The first 25–40 topics are drawn from root alternation and verbal morphology where existing
WhitneyRoots, Zalizniak 1975/1978/2004, MWS/Whitney crosswalks, and DCS measurements make a true
multi-source slice possible. Candidate clusters include:

- alternation series and grades;
- root types and morphological positions;
- guṇa/vṛddhi/zero-grade distribution;
- samprasāraṇa and nasal alternations;
- root designation and homonymy;
- attested versus predicted forms;
- selected tense/stem contrasts only where both spines and corpus evidence exist.

Selection is evidence-driven. A topic that lacks both Whitney and Zalizniak anchors stays draft.

## 4. Indexes delivered by the same graph

The graph generates distinct views instead of separate hand-maintained indexes:

| Index | Primary key/view | Learner use |
|---|---|---|
| Concept index | `subject:grammar-lab:<slug>` | Browse the neutral topic hierarchy |
| Whitney index | `whitney-sec:*` / `whitney-root:*` | Jump from Whitney to aligned topics |
| Zalizniak index | stable work + section locus | Jump from any Zalizniak work to aligned topics |
| Root index | shared SLP1/root identifiers | Gather alternations, forms, sources and exercises by root |
| Form index | normalized SLP1 plus display forms | Find the topic explaining an encountered form |
| Dictionary index | dictionary entry identifier | Show which topics use or qualify an entry |
| Corpus-evidence index | DCS locus / aggregate identifier | Trace examples and non-attestation claims |
| Curriculum index | prerequisite, difficulty and mastery fields | Recommend what to study next |

## 5. Commercial sequence

1. Build and test a provider-independent `grammar_lab` entitlement.
2. Grant it through selected course ownership and admin grants.
3. Exercise a standalone subscription in sandbox using existing billing primitives.
4. Run the 5–10-student pilot behind a non-production/limited cohort gate.
5. Production activation and pricing remain human decisions after the pilot readout.

## 6. Explicit non-goals

- No Sandhi domain before M.G. supplies Emeneau.
- No comprehensive grammar ontology in Wave 1.
- No live dependency on dictionary or corpus services for core page rendering.
- No new Sanskrit normalizer, concordance matcher, FSRS implementation, or payment ledger.
- No full dictionary-entry or source-text republication.
- No production subscription activation or charge from an autonomous handoff.
- No claim that a 5–10-student pilot proves population-level learning gain.

## 7. Expansion criteria

The next domain is opened only when W4 produces: search Recall@5 ≥0.85; zero protected-payload
leaks in the entitlement matrix; ≥80% pilot task completion; an exercise rejection/rollback
ledger; and a ranked record of student confusion. Sandhi additionally requires Emeneau as an
available, citable source and a fresh scope ruling.

---

_Dr. Mārcis Gasūns_
