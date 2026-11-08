# Metadoc — TOPIC_ORDER_FREQUENCY_KOCHERGINA_2026.md

_Created: 08-11-2026 · Last updated: 08-11-2026_

Companion record for
[`TOPIC_ORDER_FREQUENCY_KOCHERGINA_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/TOPIC_ORDER_FREQUENCY_KOCHERGINA_2026.md).

## Purpose & audience

Methodichka slice (i) (grill v2, Q5+Q8): measures whether Kochergina's topic order is
corpus-justified. Three layers — (A) 40-lesson topic inventory × DCS-2021 category share,
(B) overtake-distance table (rule demanded by an exercise before its theory, Δ + forms +
source exercise), (C) the four MG lexical questions. Audience: methodichka authors, the
exercise-parse playbook's step 4 (frequency probe), and anyone deciding reordering
proposals for the print companion. Russian, scholarly register.

## Provenance

- Created 08-11-2026 under **H7825** (GLM 5.3, `zcode/zai-individual-coding-plan/GLM-5.3`):
  script `topic_order_frequency_kochergina.py` (structure parse + three collection
  channels + lexical pass + Spearman) → `topic_order_frequency_data.json` → hand
  adjudication of every candidate into the six verified overtake rows.

## Data & tooling backing the claims

- Frequency slice: `VisualDCS/tense_case_data.json` + `src/DCS-data-2021/timws.csv`
  (DCS-2021, CC BY) — the SAME slice as `verify_claims_dcs.py` / `claims.yml` /
  `GRADATION_METALANGUAGE_KOCHERGINA.md`, so all shares are directly comparable
  (control points: aorist 0.31%, precative Ā 0.03%, conditional 0.03%, PPP 29.82%).
- Textbook source: `Kochergina_unicode.mdx`; exercise-block contract identical to
  `EXERCISE_BLOCK_COVERAGE_KOCHERGINA_2026.md` (5 exercise-less lessons: 11, 20, 27, 34, 40).
- Machine-verifiable anchors carried in the dossier: Spearman ρ = −0.4951, p = 0.037, n = 18
  (intro lesson vs DCS share); inventory rows count = 40; overtake rows = 6, Δ range 2–12;
  dict 1634/1582 headwords, never-used 367 (23.2%), glossary 484 entries in 27 lessons,
  out-of-glossary 1979 of 2671 text types (74.1%), cumulative reuse 47/484 (9.7% weighted).

## Key numbers (what a future session should not re-derive)

- ("spearman", "rho -0.4951, p 0.037, n 18 — moderately frequency-graded order"),
- ("inversions", "conditional 0.03% at XIX vs precative 0.03% at XXXIX (20 lessons apart at identical rarity); periphrastic future 0.17% at XIX; PPP 29.82% analysed only at XXV; absolutive 10.43% theory XXIII but read from XVI"),
- ("overtakes", "6 verified rows: absolutive XVI (Δ7, prāpya) and XXI (Δ2, jñātvā); passive-present XVI (Δ8, dṛśyáte); compounds XX mahākāya (Δ12), XXV mahāvidyālayaṃ (Δ7), XXVII gaṅgāsnānārthaṃ (Δ5)"),
- ("sandhi", "no overtakes; lesson VI §4 already carries the ENTIRE external -s/-r system incl. dadū-type compensatory lengthening — reading-driven order"),
- ("lexicon", "74.1% of lesson text types beyond the lesson glossary; 30 of 34 exercise blocks instruct dictionary lookup; 367 of 1582 dict headwords (23.2%) never used; «около 3 тысяч основ» claim ≈ 1.5× overstated vs 1634-entry dictionary"),
- ("not used", "23.2% of dictionary headwords never appear in any lesson (367 of 1582; manual sample 14/15 confirmed) — the dictionary is a quarter over-provisioned reference, not a lesson-fed wordlist"),
- ("cumulative", "47 of 484 glossary entries (9.7%) recur from earlier lessons; per-lesson reuse rises 0% → 33% through the book; lessons XXXV–XXXX carry no glossary at all"),

## Verdicts (one line each)

- order_vs_frequency: moderately frequency-graded; tail exemplary, two mid-book rarity
  anomalies are morphology-driven (conditionalis built on the XVIII future stem),
  not frequency-driven.
- overtake: mid-band only (XVI–XXVII), Δ ≤ 12; head and tail clean; pre-exposure class
  (PPP lexically from I–II, present stems as vocabulary from VIII) is the book's
  two-tempo architecture, not a defect.
- sandhi_axis: reading-driven, not frequency-driven — the surprise is early completeness
  in VI, not lateness anywhere.

## Related

- `GRADATION_METALANGUAGE_KOCHERGINA.md` — quantifier scale + same DCS anchors
- `claims.yml` / `CLAIMS_VERIFIED.md` — register this dossier stays numerically aligned with
- `PLAYBOOK_KOCHERGINA_V2_GRILL_2026-11-08.md` — Q5/Q8 verdicts that minted this slice
- `EXERCISE_BLOCK_COVERAGE_KOCHERGINA_2026.md` — exercise-block parsing contract reused here
- H7826 (unflagged exceptions), H7827 (migrating examples — explicitly waits on this
  dossier's frequency base), H7828 (etymologies), H7829 (anubandha key)

## Maintenance

- Data pass: `python3 topic_order_frequency_kochergina.py` (regenerates
  `topic_order_frequency_data.json`; needs `indic-transliteration`, optional `scipy`
  for Spearman).
- The dossier table (B) is hand-adjudicated from JSON candidates — re-run the
  adjudication, not just the script, if the mdx changes.
- 367 of 1582 dictionary keys never matched: UPPER bound on never-used (stem alternation
  bhrātṛ/bhrātā, gacch/gam hides some used words).

_Dr. Mārcis Gasūns_
