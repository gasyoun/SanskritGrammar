# Metadoc — SANGRAM_GRAMMAR_CLAIM_ENCODING_METHOD.mdx

_Created: 25-07-2026 · Last updated: 25-07-2026_

**Purpose.** Normative methodology manual for encoding and corpus-verifying grammatical claims in Sangram: the falsifiable-claim criterion and `claims.yml` register format, the two-axis fact × presentation verdict system with its judgment rules (D-B source priority), the four-way divergence typology as a classifier, the adversarial probe → verify workflow, the kāraka↔UD-deprel proxy rules with the three systematic non-mappings, the gold/etalon layer rules (extraction, crosswalk, per-lemma agreement with saturation guard), and the recorded reproducibility pitfalls (denominator universes, kappa rederivation, pin-by-tag, local-only scripts vs CI). Method only — results live in the source reports and articles. Companion of contract C3 ([SANGRAM_CORPUS_EVIDENCE_METHOD.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx)): C3 owns the corpus registry and the evidence cycle, this manual owns claim encoding and verdicts; on corpus questions C3 wins, on encoding questions this manual wins.

**Audience.** Sessions encoding claims for the five queued grammars; authors of papers A54/A65 (the verdict rules here are their methodology canon); any session applying the kāraka proxy table to a new measurement; reviewers checking that a published number names its universe and pin.

**Provenance.** Fable 5 (`claude-fable-5`), 25-07-2026, handoff [H1406](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1406-Fable_SanskritGrammar_deep-manual-karaka-claims-methodology-wave3_20.07.26.md) — Wave 3 of the org deep-manuals programme ([PLAN](https://github.com/gasyoun/Uprava/blob/main/docs/PLAN_ORG_DEEP_MANUALS_FABLE_WAVES_2026H2.md), Uprava-private). Distilled from: [REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md) (two-axis system, typology, κ=0.877 dual-pass design), [karaka-case/index.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/karaka-case/index.mdx) (proxy table, non-mappings, gold layer, probe→verify precedent), [AUDIT_SANGRAM_CASE_DENOMINATOR_COMMENSURABILITY_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/AUDIT_SANGRAM_CASE_DENOMINATOR_COMMENSURABILITY_2026.md) (universe rule), [RQ4_EVALUATION_PROTOCOL_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md) (falsifiability exemplar). Language ruling: Russian body + English abstract per charter §2.1/§3 and the C4 i18n contract (the contract override that programme ruling D4 explicitly allows).

LAST_VERIFIED: 25-07-2026
VERIFIED_BY: Fable 5 (claude-fable-5), H1406
COMMANDS_SPOT_RUN: 6

**Verification block (25-07-2026, authoring pass, Fable 5 `claude-fable-5`).**

| Claim in the manual | How verified | Result |
|---|---|---|
| κ 0.929 (117/120 coarse) / 0.720 (73/93 fine) rederivable from committed TSV | ran `python sangram/audit/rederive_kappa.py` in the worktree | exact match, exit 0 |
| Denominator family invariant `case_bearing = real_vibhakti + Cpd` enforced in CI | ran `python scripts/check_denominator_commensurability.py` | OK: 34 coverage summaries commensurable; all 6 case-cluster articles cite `case_bearing` 4,014,688 |
| Repo test gate green with the new files | ran `python -m pytest -q` at origin/main + after adding the manual | all tests passed both times |
| Site builds with the new .mdx, no dead links | ran `npm run build` (`onBrokenLinks: 'throw'`) | build green |
| 0 live stale "unpublished" Usha surfaces on origin/main | `git grep -i "unpublished\|неопубликован"` over the worktree at origin/main; every hit classified | 10 hits: 4 corrected-historical records of the fix itself, 2 "unpublished article candidates" (unrelated sense), 1 generic private-data note, 1 pipeline-state description in `sangram/editorial/data/article.schema.json` (unrelated), 2 in A61/MumbaiWSC about archival correspondence and venue policy (not Usha). Zero live stale claims; manual introduces none and states the corrected wording (published 2014, reuse with scholarly attribution); tally independently re-derived by the adversarial pass |
| H1399 (§7.2 per-lemma agreement) already merged | `git log origin/main` shows [PR #496](https://github.com/gasyoun/SanskritGrammar/pull/496) merged | recorded as done in manual §7, not re-executed |
| Independent adversarial refutation pass (programme ruling D11) | separate agent (no authoring context) re-ran the commands and checked 34 load-bearing claims against sources, default-REFUTED on uncertainty | 31 CONFIRMED / 3 REFUTED; all 3 fixed pre-PR: H1399 handoff link corrected to the real archive filename, unsourced "защищена в 2014" dropped (only "published 2014" is sourced), Usha grep tally corrected 9 → 10 hits (the 10th — a generic pipeline-state line in `article.schema.json`, unrelated; the 0-live-stale-surfaces conclusion unchanged) |

**Improvement backlog (ranked).**
1. Apply the encoding method to the next queued grammar register end-to-end and record what the manual under-specified (the first real consumer will surface gaps the calibration programme cannot).
2. Wire a claims-register lint for §3 rule 1 (every verdict row names its number's artifact) — currently prose-enforced only; `check_claims_consistency.py` covers counts, not artifact links.
3. Add a worked negative example to §4 (a flagged record walked through the decision tree, including one deliberate misclassification and why it fails) — the classifier is stated but not demonstrated in-page.
4. When a second etalon (beyond Usha Sanka) is adopted, generalize §7's crosswalk rules from Devanāgarī→IAST to a source-agnostic checklist.

**Limitations.** The judgment rules (§3) are distilled from one completed programme (five Russian-language grammars, 776 claims) — thresholds like "FALSE requires hard contradiction" are calibrated on that corpus of claims and may need adjustment for genres outside textbook/reference grammar. The two typology consequences (§4) are diagnostics observed on one programme, not laws. The kāraka proxy table inherits DCS treebank coverage (3.93%) and its Vedic skew; the manual states this but cannot repair it. The manual does not restate per-book results — a reader wanting the numbers must follow the links to the synthesis report and SG-SE-013. Inherited source tension, surfaced by the adversarial pass and left unresolved here: the extraction stats give **581** distinct dhātus while SG-SE-013 §7.2's crosswalk universe says **576** distinct roots (212/576 = 36.8%) — the manual cites each number in its own scope; reconciling the pair belongs to the source articles, not this method doc.

**Revision history.**
| Date | Change |
|---|---|
| 25-07-2026 | Created (v1) — Wave 3, H1406, Fable 5 (`claude-fable-5`): method distilled from the verification programme + SG-SE-013 + denominator audit; first SanskritGrammar metadoc carrying the LAST_VERIFIED staleness block. |
| 25-07-2026 | Adversarial refutation pass (D11, independent agent): 31/34 CONFIRMED; 3 peripheral refutations fixed same pass (H1399 link slug, "защищена" dropped, grep tally 9→10). |

_Dr. Mārcis Gasūns_
