# Gold-standard provenance and LLM-contamination audit (2026 H2)

_Created: 19-07-2026 · Last updated: 21-07-2026_

Cross-repo audit of every dataset the Sanskrit Lexicon org trades as "gold", "adjudicated",
or evaluation ground truth — asking, per dataset, what its annotation provenance actually is
and whether it supports the label it trades under. Executed under
[H1272](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1272-Fable_SanskritGrammar_gold-provenance-contamination-audit_18.07.26.md).
Gold files themselves were never modified: this audit is strictly read-only.

## Headline

**Not one of the 15 canonical gold datasets in this org meets the GOLD bar.** Zero have
independent human annotation with an adjudication trail. Exactly one — the hand-curated
Bhagavadgītā analysis — has any human annotator at all, and it is a single annotator with no
second pass, so it rules SILVER. The other fourteen are annotated end-to-end by language
models; ten of those carry a specific contamination mechanism beyond mere LLM authorship, and
each of those ten was put through an adversarial refutation pass that tried and failed to find
the human provenance a first pass might have missed.

The word "gold" in this org currently means *frozen*, not *human-adjudicated*. Several
datasets are documented with real integrity — models, versions, seeds, blind protocols and
"not a human" disclaimers are recorded in-repo — but the label they travel under does not
carry those caveats into the papers that cite them.

| Verdict | Count | Meaning |
|---|---|---|
| GOLD | 0 | Independent human annotation with adjudication trail |
| SILVER | 1 | Single human annotator, or human-reviewed LLM output |
| LLM-ASSISTED | 4 | LLM in the loop, human gate documented |
| CONTAMINATED | 10 | Eval data plausibly derived from, or seen by, a system it evaluates |
| UNDOCUMENTED | 0 | No recoverable provenance |

The zero in the UNDOCUMENTED row is the audit's one genuinely good news: provenance was
recoverable for every dataset. The org's record-keeping is strong. What it records is the
problem.

## Method

The census was built to be exhaustive by construction, then narrowed:

1. **Seven parallel finders** swept the org — one each for SanskritGrammar, RuWritingStyles,
   SamudraManthanam, SanskritLexicography, csl-atlas + WhitneyRoots, the Uprava hub read from
   the *consumer* side (which datasets do papers and review sheets treat as ground truth), and
   a sweep of the thirteen remaining active repos. Search terms covered `gold`, `adjudicat`,
   `kappa`/`κ`, `inter-annotator`, `benchmark`, `ground truth`, and the Russian `эталон`,
   `золотой стандарт`, `адъюдикац`. That produced 61 raw candidates.
2. **A merge pass** deduplicated candidates reported under different names by different
   finders and dropped entries that were not evaluation ground truth (engine-generated parity
   fixtures, CI regression snapshots, source dictionaries). 61 raw → **15 canonical datasets**.
3. **One provenance agent per dataset** reconstructed annotation history from the data files'
   own headers, sibling documentation and data statements, `git log --follow` over each path,
   and the minting handoff in the Uprava hub — read from the fetched `origin/main`, since the
   local Uprava clone is diverged. Each returned a verdict plus concrete evidence.
4. **An adversarial refutation pass** ran against every CONTAMINATED verdict, prompted to
   *overturn* it by finding documented human provenance the first pass missed.

**Verdict vocabulary.** GOLD = independent human annotation with an adjudication trail.
SILVER = single human annotator, or human-reviewed LLM output. LLM-ASSISTED = LLM in the loop
with a documented human gate. CONTAMINATED = eval data plausibly derived from or seen by a
system it evaluates. UNDOCUMENTED = no recoverable provenance. Where two labels fit, the
worse one wins, and CONTAMINATED outranks the rest. An LLM annotator is not a human annotator:
two blind LLM passes with an LLM adjudicator is not GOLD, whatever the κ.

## The census and its verdicts

| Dataset | Repo | Verdict | Refutation | Annotators |
|---|---|---|---|---|
| [Gītā gold master + morphology gold](https://github.com/gasyoun/kosha/blob/main/data/gita/gita_gold_master.tsv) | kosha | SILVER | n/a | 1 human (MG), no second pass |
| [SG-WF-008 tatpuruṣa two-pass κ set](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/data/kappa_result.json) | SanskritGrammar | LLM-ASSISTED | n/a | Opus 4.8 + Sonnet 5, blind |
| [sangram per-article adjudication sets](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/a-stems/data/validation_verdicts.tsv) | SanskritGrammar | LLM-ASSISTED | n/a | 1 LLM each (Fable 5 / Opus 4.8) |
| [RuWritingStyles gold eval suite](https://github.com/gasyoun/RuWritingStyles/blob/main/evals/GOLD_PROTOCOL.md) | RuWritingStyles | LLM-ASSISTED | n/a | Pipeline scorer + Fable 5 |
| [MWS G5 microstructure gold sample](https://github.com/sanskrit-lexicon/MWS/blob/master/review_packets/g5/G5_gold_adjudicated.csv) | MWS | LLM-ASSISTED | n/a | Sonnet 5 ×2, Fable 5 adjudicator |
| [A65 grammar-claims verdict registers](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/validation_sample_gold.json) | SanskritGrammar | CONTAMINATED | CONFIRMED | Claude family both passes |
| [semdom ↔ Amarakośa 200-synset gold](https://github.com/gasyoun/SanskritLexicography/blob/master/data/semdom_ak_gold.tsv) | SanskritLexicography | CONTAMINATED | CONFIRMED | Fable 5 + Opus 4.8, Fable 5 adjudicates |
| [corpus_lexicon A42 precision + recall sets](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/gold/gold_set.jsonl) | SanskritLexicography | CONTAMINATED | CONFIRMED | 38-agent Claude panel; 0 human labels |
| [pwg_ru judge A/B defect battery](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/research/JUDGE_AB.md) | SanskritLexicography | CONTAMINATED | CONFIRMED | Battery built by the judges' own family |
| [A44 verified correction queue + IRR](https://github.com/drdhaval2785/SanskritSpellCheck/blob/master/corrections_draft/irr/agreement_stats.md) | SanskritSpellCheck | CONTAMINATED | CONFIRMED | Sonnet 5 + Fable 5 vs Opus 4.8 |
| [Which-dictionary routing gold panel](https://github.com/sanskrit-lexicon/csl-guides/blob/main/src/data/which-dictionary-gold.json) | csl-guides | CONTAMINATED | CONFIRMED | Fable 5, single pass |
| [csl-atlas human-review overlay queues](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/src/data/review/h5-anomaly-review.json) | csl-atlas | CONTAMINATED | CONFIRMED | 93% LLM agents labelled "human review" |
| [OBS-T correction-typology gold sample](https://github.com/sanskrit-lexicon/csl-observatory/blob/main/validation/gold_sample.csv) | csl-observatory | CONTAMINATED | CONFIRMED | Sonnet 4.6 rule classifier, 0 humans |
| [MW defgen frozen 500-headword sample](https://github.com/gasyoun/kosha/blob/main/data/eval/defgen/frozen_sample.tsv) | kosha | CONTAMINATED | CONFIRMED | DeepSeek judges its own output |
| [IndologyScholars thematic classification + IRR](https://github.com/gasyoun/IndologyScholars/blob/main/analytics_output/interrater_sample_blind.csv) | IndologyScholars | CONTAMINATED | CONFIRMED | DeepSeek, second pass same model |

## The four contamination mechanisms

The ten CONTAMINATED verdicts are not ten instances of "an LLM did it". They fall into four
distinct structural failures, and the distinction matters because the repairs differ.

**1. The evaluated system authored its own gold.** The MW defgen sample is the sharpest case:
`deepseek-chat` is simultaneously a generation arm and the sole blinded adequacy judge for all
arms including its own output, and the underlying MW 1899 text is, by the protocol's own
admission, certainly in the model's pretraining. In the semdom ↔ Amarakośa set, both
annotators saw the bridge system's top-6 candidates and kept one for roughly half the rows, so
about half the "gold" labels are the output of the very bridge the gold is used to score. The
csl-guides routing panel was annotated by Fable 5 against a quiz answer key authored by
Opus 4.8 — same family on both sides of a 100% accuracy claim.

**2. Same-family agreement reported as inter-annotator agreement.** Every κ in the org that
travels as a reliability number is model-vs-model. A65's κ = 0.877 is Claude-vs-Claude.
A44's 0.336/0.663 is Sonnet 5 + Fable 5 versus Opus 4.8. A26's L1 0.670 is DeepSeek versus
Claude — the one genuinely cross-family number, and also the lowest. The pattern is that
agreement rises as the annotators become more similar, which is exactly what a reliability
statistic must not measure.

**3. LLM output labelled as human review.** Two datasets make a claim in prose that the data
contradicts. The csl-observatory report states "390 human-annotated events"; commit
`5b5b280` shows all 390 labels were filled in one pass by an uncommitted ad hoc rule-based
classifier co-authored by Sonnet 4.6, with no human annotation at any point. The csl-atlas
benchmark reports precision 1.000 against a "human-reviewed gold subset" of 147 rows, of which
130 carry reviewer `codex` (an OpenAI agent) and 7 `Antigravity` (a Gemini-family agent) —
93% machine, with notes that openly say "Automated resolution based on nasalization
normalization", i.e. re-derived from the same normalization logic the evaluated pipeline uses.
Ten of 147 rows are human.

**4. Circular controls.** The pwg_ru judge battery's BAD half is sound by construction — a
mutation provably exists — but its 76 OK controls were declared clean by the same Opus and
Sonnet judges the battery exists to compare, under evaluation conditions. The κ = 1.00 that
travels with this dataset does not even belong to it: it is run 3's 191/191 agreement on a
different set of cards.

## What this costs the papers

Every affected paper is listed in [Uprava/ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md).
The exposure is uneven, and honesty about it is already uneven too — several papers disclose
the machine-annotator status in a methods section while the headline number travels without
the caveat.

| Paper | Readiness | Exposure |
|---|---|---|
| A16 MW microstructure | 5/5, submission-ready | Calls the G5 sample "double-annotated, adjudicated"; all three roles were LLMs |
| A65 Что корпус сказал грамматикам | 5/5, author-signed | κ-validation gate declared CLOSED on a Claude-vs-Claude κ |
| A29 Совет филологов | 5/5 | Cites 0.96 / 0.97 as two-rater agreement; rater A is software, rater B is Fable 5 |
| A12 OBS-T error typology | 4/5 | §4.3 validation rests on "390 human-annotated events", which is false as written |
| A44 dictionary body as ground truth | 4/5 | κ figures are single-family LLM agreement; repo concedes no human anchor exists |
| A26 Russian Indological Archive | deposit-ready | Frozen snapshot ships a cross-model κ that reads as human IRR |
| A58 semdom ↔ Amarakośa | 3/5 | Discloses model-only annotation in §7; headline κ still reads as reliability |
| A42 corpus_lexicon | 3/5 | Carries the LLM-estimated caveat first-class — the best-behaved of the set |
| A64 / A66 sangram compounds | 2/5 | Explicitly says "two independent blind LLM passes" — no misrepresentation |
| A59 MW defgen | 2/5 | Lists the human-scored subsample as an open blocker rather than claiming gold |

A12 and A16 are the urgent pair: both are at or near submission, and both make a claim about
human annotation that the underlying data does not support. A64, A66, A59 and A42 are the
model of what the rest should look like — the machine nature is stated where the number is
stated.

## Limitations

**This audit is an LLM judging LLM contamination.** The census, the verdicts and the
refutations were all produced by Claude subagents (Fable 5, `claude-fable-5`), with the report
synthesized by Opus 4.8 (`claude-opus-4-8`). The same reflexivity problem it diagnoses in the
datasets applies to it: a model assessing whether model annotation is trustworthy is not an
independent instrument. The human vote on the repair actions is the real gate, and nothing
here should be treated as adjudicated until that vote happens.

**The acceptance criterion is now met (closed 21-07-2026).** H1272 requires that no
CONTAMINATED verdict ship without a refutation pass. The csl-atlas overlay-queue verdict
initially shipped without one (the 19-07 run was cut short by a session limit); the missing
refutation ran 21-07-2026 (Fable 5, `claude-fable-5`) and returned **CONFIRMED**: an
independent recount of all 14 review-queue files on `origin/main` reproduced the reviewer
distribution exactly (130 `codex` / 7 `Antigravity` / 10 `gasyoun`, `reviewed-corrected` = 0
everywhere); "codex"/"Antigravity" are agent identities, not human aliases (the human
reviewer has his own token, `gasyoun`, in the same schema); no subsequent human gate over
the agent verdicts exists anywhere in the repo — an archived session journal even treats the
codex verdicts *as* the human review, which is the contamination, not a refutation;
[`build-benchmark-report.mjs`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/scripts/build-benchmark-report.mjs)
counts gold by `reviewStatus` alone and never reads the reviewer field (`annotatorType`
appears nowhere in the repo); and nothing in the review layer changed after 19-07. One
wording refinement: the codex notes are boilerplate keyed to sampleClass × reviewed value —
codex did differentiate rows — but that remains LLM adjudication with zero documented human
verification. All ten CONTAMINATED verdicts have now survived adversarial refutation.

**The census is exhaustive by construction, not by proof.** It was built from a term sweep
plus the consumer-side hub read plus per-repo document sweeps. Any gold dataset found later
that is missing from the table is a defect of this audit, per the handoff's own standard.

**Two datasets in the census sit partly outside git.** The SanskritGrammar `review/` vote
files that constitute the human gate for the sangram sets are local-only (gitignored under
H856), so the only human-authored artifacts in that lane are the ones most at risk of being
lost. RuWritingStyles `dict-*` gold cases exist on `origin/main` but not in the local working
tree, which is behind.

## Repairs, for a human to decide

None of these were executed — the audit's fence is that gold data is read-only, and every
proposed change routes through a review sheet and a human vote.

1. **Fix the two false claims in place.** csl-observatory's "390 human-annotated events" and
   csl-atlas's "human-reviewed gold subset" describe machine work as human work. These are
   documentation corrections, not data changes, and they gate A12.
2. **Add an `annotatorType` field** (`human` / `llm-agent` / `automated`) to the csl-atlas
   review-overlay schema and split the benchmark's precision into human-gold and machine-gold
   tracks. Today a 0.76%-coverage, 93%-machine subset produces a headline precision of 1.000.
3. **Buy one genuine human anchor per lane, not per dataset.** The cheapest defensible move
   across the whole estate is a stratified human-labelled seed — roughly 30 rows for A44 (the
   repo already specifies this in its own `HUMAN_ANCHOR_NEEDED.md`), ~50 for semdom
   oversampling the self-adjudicated rows, the pending adjudication sheets for A29. Each
   upgrades its dataset from CONTAMINATED to LLM-ASSISTED and gives every downstream κ a human
   reference point.
4. **Re-run same-family κ across families.** Where a second pass is affordable but a human is
   not, running it on a genuinely different model family (Codex GPT-5 and DeepSeek are already
   in the org's toolchain) removes the shared-prior confound. A26's low cross-family κ is
   evidence this matters, not evidence the method failed.
5. **Stop using "gold" as the default word.** The estate needs a vocabulary where frozen,
   machine-adjudicated and human-adjudicated are distinguishable at a glance — in dataset
   names, manifest entries and paper prose alike.

## Provenance of this audit

Census, per-dataset verdicts and adversarial refutations: Fable 5 (`claude-fable-5`) subagents
under a workflow harness, 18–19-07-2026. Report synthesis: Opus 4.8 (`claude-opus-4-8`).
The final csl-atlas refutation (closing the 10/10 acceptance criterion) and this revision:
Fable 5 (`claude-fable-5`), 21-07-2026.
Raw per-dataset verdict records, including full evidence lists, are committed alongside this
report as [GOLD_PROVENANCE_AUDIT_2026H2_verdicts.json](https://github.com/gasyoun/SanskritGrammar/blob/main/GOLD_PROVENANCE_AUDIT_2026H2_verdicts.json).
Gold files' git status was verified unchanged against a pre-audit baseline snapshot.

_Dr. Mārcis Gasūns_
