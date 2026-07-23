# Can Pāṇinian Compound Type Be Recovered from an Unannotated Sanskrit Corpus? A Two-Tier Inter-Pass Agreement Study

_Created: 22-07-2026 · Last updated: 22-07-2026_

**ID:** A64 · **Readiness:** 3/5 (draft, gate proposed — see [OUTLINE](OUTLINE_compound-type-kappa_A64.md)) ·
**Venue:** proposed, not chosen — see OUTLINE § Venue candidates · **Home:** SanskritGrammar

## Abstract

The Digital Corpus of Sanskrit (DCS) marks that a token is a member of a compound and gives
its segmentation, but does not annotate the compound's Pāṇinian semantic type — tatpuruṣa
(determinative), bahuvrīhi (possessive/exocentric), dvandva (coordinate), or avyayībhāva
(adverbial). We test whether that type can be recovered by manual classification, and how
reliably, using two independent, blind classification passes over a seeded sample of 120
two-member compounds drawn from 442,649 candidates in a pinned DCS snapshot. Agreement on
the coarse four-way-plus-residual Pāṇinian class is high (Cohen's κ = 0.9295, 95% CI
[0.8356, 1.0], n = 120). Agreement on the finer case-relation (vibhakti) subtype of
tatpuruṣa, measured on the subset both passes labeled tatpuruṣa (n = 93), is markedly lower
and sits at the boundary of our pre-registered 0.70 reliability threshold (κ = 0.7201, 95%
CI [0.6017, 0.8171] — the lower bound falls under the threshold). **Both passes were
produced by two models of the same LLM family (Opus 4.8 and Sonnet 5); consequently, these
figures bound within-family reproducibility of the classification task, not independent
inter-annotator reliability, and should not be read as evidence that a human or cross-vendor
annotator pair would agree at the same rate.** We report the result as a positive but
qualified answer at the coarse grain and an open question at the fine grain.

## 1. Introduction

Pāṇinian grammar (via the Mahābhāṣya tradition) divides Sanskrit nominal compounds
(samāsa) into four coordinate semantic classes by which member dominates the compound's
reference: **tatpuruṣa** (uttarapadārthapradhāna — the right member dominates),
**bahuvrīhi** (anyapadārthapradhāna — an external referent dominates, i.e. the compound is
exocentric), **dvandva** (ubhayapadārthapradhāna — both members are coordinate), and
**avyayībhāva** (pūrvapadārthapradhāna — the left member dominates); a residual
**kevala-samāsa** class covers compounds outside the four pradhāna types. The Digital
Corpus of Sanskrit (DCS) marks that a token is a non-final compound member
(`feat_case = 'Cpd'`) and gives the compound's segmentation, but does not annotate which of
these types applies — evidence-limit **EM4** in the Sangram morphology programme's
evidence-limit registry. The only type-adjacent signal available in DCS is the Universal
Dependencies edge `compound:coord` (an approximation of dvandva coordination), which covers
just 2,214 of 841,052 compound-member tokens (0.26%), exists only in the 3.9% of the corpus
that is syntactically parsed, and cannot distinguish tatpuruṣa from karmadhāraya or identify
bahuvrīhi at all. Closing the gap between "attested" (segmentation) and "traditional"
(Pāṇinian type) therefore requires manual classification — and the question this paper
answers is not "what is the type distribution" but **"is that classification reliable
enough to publish a type distribution at all, and at what grain?"** — measured as
inter-pass agreement (Cohen's κ), per a pre-registered kill-gate (κ < 0.70 → the type
taxonomy is revised before any distribution is published).

## 2. Related work

**Agreement metrics.** We follow the standard computational-linguistics framing of
inter-coder reliability: Cohen's κ = (p_o − p_e)/(1 − p_e), reported with a bootstrap 95%
confidence interval, per the methodological survey of Artstein and Poesio (2008), who argue
that agreement coefficients — not raw accuracy against a single gold standard — are the
correct instrument for validating a classification scheme before it is used to generate
corpus-wide claims.

**Sanskrit compound-type identification.** Two prior lines of work address the same
classification target from a different angle. Krishna et al. (2016) built a machine-learning
classifier for the four-way Pāṇinian compound-type distinction, combining rule features from
the Aṣṭādhyāyī, semantic relations from the Amarakoṣa lexical database, and corpus-derived
patterns via Adaptor Grammars; they report 77% accuracy with a random-forest classifier
against a single gold-labeled set, and find that grammar rules alone are insufficient without
lexical and corpus evidence. Sandhan et al. (2023, DepNeCTI) address the harder,
multi-component case — identifying nested compound spans and the semantic relations between
components — with a dependency-based framework that improves 13.1 F1 points (Labeled Span
Score) over prior baselines and releases two new annotated datasets. **Neither paper
measures inter-annotator or inter-pass agreement for the classification task itself**: both
evaluate a trained classifier's accuracy or span-F1 against a single annotated reference,
not the reliability of two independent classification passes against each other. This is the
gap our study targets — not "can a classifier be built" (both prior works answer yes) but
"if two independent passes classify the same items by the same codebook, how often do they
agree, and does that agreement survive a finer-grained taxonomy?"

**Corpus.** The Digital Corpus of Sanskrit, including its Vedic treebank component with
Universal Dependencies syntactic annotation (Hellwig et al., 2020), is the source corpus for
this study's snapshot; its syntactic layer is what supplies the (insufficient) UD
`compound:coord` signal discussed in § 1.

**LLM annotators and agreement.** Both classification passes in this study are large
language models. Two lines of recent work bear directly on how such agreement figures should
be read. First, LLM annotators have been shown to carry systematic biases inherited from
training data into their labeling decisions (Vallejo Vera and Driggers, 2024, on political
party-cue bias) — a finding that generalizes to any domain where the training corpus itself
encodes a bias, and motivates treating high agreement between models sharing a training
lineage as evidence of *correlated* judgment, not necessarily *correct* judgment. Second,
work evaluating LLMs as automatic annotators and adjudicators for fine-grained tasks (Negi et
al., 2026) finds LLMs reliable at coarser structural sub-tasks (e.g. span identification)
but less faithful at reproducing finer relational structure — a pattern that anticipates
this paper's own coarse-passes/fine-struggles result, though in a different domain (opinion
analysis rather than Pāṇinian compound typology). **The verified gap**: we found no prior
work measuring inter-pass or inter-annotator agreement specifically for LLM-based Pāṇinian
compound-type classification in Sanskrit; this paper is, to our knowledge, the first to do
so.

## 3. Data & method

**Snapshot.** The corpus snapshot is the pinned DCS master mirrored from
`gasyoun/dcs-conllu` (upstream: OliverHellwig/sanskrit), source commit
`04e0778d3dc971030229179e25eea043d06ff397`, imported 2026-06-06, SHA-256
`8f3b06bd6ef0e47a9ccf81d147e73d5d240d64e0c12f6d789262eb422ebb23bc`. The upstream mirror's
history was later rewritten, orphaning the commit reference in git terms; the binding
provenance is the snapshot's own provenance table and checksum, not a resolvable upstream
commit.

**Universe.** Tokens with `feat_case = 'Cpd'` (non-final compound members) total 841,052,
across 396,305 sentences. A compound is reconstructed as a maximal run of `Cpd`-tagged
tokens plus the following inflected head. This yields 595,021 total compounds, of which
442,649 are two-member (exactly one `Cpd` member + one inflected head) and 152,372 are
multi-member (three or more members). **This study's universe is two-member compounds
only** (442,649), deferring multi-member compounds as a limitation (§ 5) to avoid
conflating type-classification disagreement with bracketing disagreement (see the
method-design rationale below).

**Codebook.** Type labels follow Edgar Leitan's Pāṇinian/Mahābhāṣya-arrangement codebook:
four coarse classes (tatpuruṣa, bahuvrīhi, dvandva, avyayībhāva) plus dvigu and an
`unclear` residual at the coarse tier; and, for items both passes call tatpuruṣa, a fine
case-relation (vibhakti) tier — the six case-tatpuruṣas (dvitīyā/accusative through
saptamī/locative), karmadhāraya, nañ-tatpuruṣa, prādi, gati, and upapada. karmadhāraya is
folded inside the tatpuruṣa slot per repository convention (dvigu ⊂ karmadhāraya ⊂
tatpuruṣa), a departure this study's disagreement pattern (§ 4) partially stress-tests.

**Design.** We adopt the "two-tier" design (Path B of three candidate designs weighed before
the pilot ran): compute κ separately at the coarse tier (all sampled items) and the fine
tier (only the tatpuruṣa-labeled subset), rather than a single κ over either a coarse-only
or fine-only label space. This design was chosen because a single fine-only κ over
multi-member compounds would conflate two distinct sources of disagreement — genuine type
ambiguity versus bracketing ambiguity in recursive right-to-left compound structure — while
a coarse-only κ would under-test the taxonomy at the grain a working grammar description
actually needs. The two-tier, two-member-only design isolates type classification from
both confounds.

**Sampling.** A sample of n = 120 two-member compounds was drawn with `random.Random(20260715)`
over the full 442,649-item universe (seeded, not "first N").

**Annotation.** Two independent passes classified the full sample blind to each other,
using the same codebook and sampling frame: Pass A (Opus 4.8, `claude-opus-4-8`) and Pass B
(Sonnet 5, `claude-sonnet-5`). Both passes are LLM-generated and are flagged as
model-provisional pending scholarly sign-off, consistent with how earlier pilots in this
programme (P2, P3) framed single-annotator adjudication.

**Statistic.** Cohen's κ = (p_o − p_e)/(1 − p_e) with a bootstrap 95% confidence interval,
computed separately for the coarse tier (all n = 120) and the fine tier (n = 93, the
both-passes-tatpuruṣa subset). Pre-registered kill-gate: κ < 0.70 at either tier requires
the type taxonomy to be revised before any type distribution based on it is published; the
negative result would itself be publishable rather than suppressed.

## 4. Results

**Coarse tier.** Cohen's κ = 0.9295, 95% CI [0.8356, 1.0], n = 120, 117/120 items agree.
Of the 117 agreed items: tatpuruṣa 93 (79.5%), bahuvrīhi 17 (14.5%), dvandva 6 (5.1%),
unclear 1 (0.9%). All 3 disagreements sit on a single boundary — karmadhāraya read as
bahuvrīhi or dvandva by the other pass (e.g. a compound glossable either as "distinguished
qualities" [karmadhāraya] or "one whose qualities are distinguished" [bahuvrīhi]) — the
endocentric/exocentric boundary, which is not resolvable from segmentation alone and
arguably belongs to external syntax rather than word-formation.

**Fine tier.** On the n = 93 items both passes agreed were tatpuruṣa, Cohen's κ = 0.7201,
95% CI [0.6017, 0.8171], 73/93 items agree. The point estimate clears the 0.70 threshold,
but the lower confidence bound (0.60) does not — the case-relation subtype is recoverable
only at the margin, not reliably. Of 20 disagreements: 5 sit on the ṣaṣṭhī (genitive) ↔
karmadhāraya boundary (is the left member a genitive complement or an appositive
attributive?), 4 on saptamī (locative) ↔ upapada (with a kṛt-derived head, is the left
member locative or a direct-object-like argument?), 2 on ṣaṣṭhī ↔ caturthī (dative), and 9
scatter across other subtype boundaries (largely pulled toward a residual `tat-other` label,
or tṛtīyā/ṣaṣṭhī and caturthī/karmadhāraya confusions). Full confusion matrices are in the
committed `kappa_result.json`.

## 5. Discussion and limitations

**Same-model-family caveat (primary).** Both classification passes are large language
models from the same model family (Opus 4.8 and Sonnet 5). κ measured this way bounds
**within-family reproducibility of the classification decision**, not independent
inter-annotator reliability: correlated training data can correlate the two passes' errors,
which inflates agreement relative to what a genuinely independent — cross-vendor or human —
annotator pair would produce (cf. § 2's discussion of LLM annotator bias). The headline
figures (κ=0.93 coarse, κ=0.72 fine) should therefore be read as an upper-bound estimate of
recoverability, pending a true second annotator.

**Fine κ is borderline, not passed.** The fine-tier point estimate (0.7201) clears the
pre-registered 0.70 gate, but its 95% CI lower bound (0.6017) does not. We report this as
"recoverable at the boundary," not "recovered" — over-stating this as a clean pass would be
a defect.

**Two-member-only frame.** The sampling universe excludes multi-member compounds (152,372
of 595,021 total), by design (§ 3), to avoid conflating type ambiguity with bracketing
ambiguity. Multi-member compound type classification is a distinct, harder task this study
does not address.

**Sampling-frame artifact, not a corpus fact.** No avyayībhāva or kevala-samāsa items
appeared in the sample (0 of each), nor the fine subtypes nañ, prādi, or gati. This is a
consequence of the reconstruction rule (a `Cpd`-run followed by an *inflected nominal* head),
which structurally excludes indeclinable, left-headed avyayībhāva compounds — not evidence
that avyayībhāva is rare in the corpus. A full-taxonomy replication requires a different
sampling frame, including multi-member compounds.

**karmadhāraya/dvigu registry boundary.** This study follows the Leitan/Pāṇinian
arrangement (dvigu ⊂ karmadhāraya ⊂ tatpuruṣa) for the codebook, while the repository's own
slot registry (C2) parks dvigu with avyayībhāva in a separate slot (SG-WF-010) — a
documented divergence, not resolved by this pilot.

## 6. Conclusion

The coarse Pāṇinian compound-type distinction is recoverable from an unannotated Sanskrit
corpus by manual classification with high agreement between two same-family LLM passes
(κ=0.93), closing evidence-limit EM4 at the coarse grain with real, if bounded, confidence.
The finer case-relation subtype of tatpuruṣa is recoverable only at the margin (κ=0.72,
lower CI 0.60) — a genuine open question, not a settled result. Because both passes share a
model family, neither figure should be read as inter-annotator reliability in the classical
sense; the load-bearing next step toward a fully validated type distribution is a true
cross-vendor or human second annotator, not a larger same-family sample.

## References

- Artstein, R. and Poesio, M. (2008). Survey Article: Inter-Coder Agreement for
  Computational Linguistics. *Computational Linguistics*, 34(4):555–596.
  [https://aclanthology.org/J08-4004/](https://aclanthology.org/J08-4004/)
- Krishna, A., Satuluri, P., Sharma, S., Kumar, A., and Goyal, P. (2016). Compound Type
  Identification in Sanskrit: What Roles do the Corpus and Grammar Play? In *Proceedings of
  the 6th Workshop on South and Southeast Asian Natural Language Processing (WSSANLP2016)*.
  [https://aclanthology.org/W16-3701/](https://aclanthology.org/W16-3701/)
- Sandhan, J., Narsupalli, Y., Muppirala, S., Krishnan, S., Satuluri, P., Kulkarni, A., and
  Goyal, P. (2023). DepNeCTI: Dependency-based Nested Compound Type Identification for
  Sanskrit. In *Findings of the Association for Computational Linguistics: EMNLP 2023*.
  [https://arxiv.org/abs/2310.09501](https://arxiv.org/abs/2310.09501)
- Hellwig, O., Scarlata, S., Ackermann, E., and Widmer, P. (2020). The Treebank of Vedic
  Sanskrit. In *Proceedings of the 12th Language Resources and Evaluation Conference (LREC
  2020)*. [https://aclanthology.org/2020.lrec-1.632/](https://aclanthology.org/2020.lrec-1.632/)
- Vallejo Vera, S. and Driggers, H. (2024). Bias in LLMs as Annotators: The Effect of Party
  Cues on Labelling Decision by Large Language Models.
  [https://arxiv.org/abs/2408.15895](https://arxiv.org/abs/2408.15895)
- Negi, G., Waskow, M. A., McCrae, J., Zayed, O., and Buitelaar, P. (2026). Large Language
  Models as Automatic Annotators and Annotation Adjudicators for Fine-Grained Opinion
  Analysis. [https://arxiv.org/abs/2601.16800](https://arxiv.org/abs/2601.16800)

## Data availability

All figures reported here are reproducible from the frozen assets of the published RU pilot
study — [`sangram/articles/tatpurusha/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/index.mdx),
[v0.25.0](https://github.com/gasyoun/SanskritGrammar/releases/tag/v0.25.0), handoff
[H989](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H989-Opus_SanskritGrammar_sangram-p4-tatpurusa_15.07.26.md)
— including the generator scripts, sample, per-item annotations, and confusion matrices (see
[OUTLINE](OUTLINE_compound-type-kappa_A64.md) § Data inventory).

---

_Dr. Mārcis Gasūns_
