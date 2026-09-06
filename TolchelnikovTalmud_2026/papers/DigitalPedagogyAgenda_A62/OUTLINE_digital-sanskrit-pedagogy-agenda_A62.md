# A62 — Digital Sanskrit pedagogy: a research agenda (outline)

_Created: 14-07-2026 · Last updated: 06-09-2026_

Mārcis Gasūns, independent scholar ([ORCID 0000-0003-4513-884X](https://orcid.org/0000-0003-4513-884X)), gasyoun@ya.ru

**ID:** A62 · **Readiness:** 4/5 (evaluation methodology + metric register specified in full) · **Home:** SanskritGrammar ·
**Venue candidates:** eLex / Lexikos / ISCLS / CALICO / ReCALL / an NLP4DH venue (a human `@DECIDE`s).
The field-defining paper of the [digital-Sanskrit-pedagogy field](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md);
handoff [H914](https://github.com/gasyoun/Uprava/blob/main/handoffs/H914-Fable_SanskritGrammar_pedagogy-w1b-agenda-paper-a62_14.07.26.md);
3/5 pass = [H1464](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1464-Sonnet_SanskritGrammar_a62-agenda-related-work-abstract_22.07.26.md);
4/5 pass = [H1731](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1731-Opus_SanskritGrammar_a62-metric-register-into-evaluation-section_27.07.26.md);
author-voice pass 06-09-2026 ([SIGNOFF_A62_author_pass.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/DigitalPedagogyAgenda_A62/SIGNOFF_A62_author_pass.md)).
Aggregate numbers only (in-copyright textbook sources).

> **Provenance note.** H914 is tier-locked to Fable 5; this readiness-2 scaffold was authored on
> **Opus 4.8 (`claude-opus-4-8[1m]`)** by author decision (the "go" override). The 3/5 pass (abstract,
> survey table, related work) was authored on **Sonnet 5 (`claude-sonnet-5`)**. The 4/5 pass (§2 metric
> re-sync, §4 capability-vs-outcome methodology and the PM1–PM12 register) was authored on
> **Opus 5 (`claude-opus-5`)** under H1731. The author-voice pass over the prose ran 04-08-2026 —
> the 4→5 slot it was reserved for — on **Fable 5 (`claude-fable-5`)**
> ([H1874](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1874-Fable_SanskritGrammar_a62-pedagogy-agenda-author-voice-pass_29.07.26.md)):
> the prose was aligned to the
> [Sangram prose guide](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/SANGRAM_STYLE_GUIDE_PROSE_RU.mdx)
> — telegraphic bullets expanded into full sentences, internal labels given plain-language readings
> at first use — with no claim, figure or citation changed.

## Abstract

Sanskrit computing has produced dictionaries, morphological engines, annotated corpora, and dozens
of learner-facing tools, but no field that studies *how those assets teach*, and no falsifiable
account of what actually works pedagogically. I name **digital Sanskrit pedagogy** as a
research-and-integration field, give it a twelve-aspect taxonomy that unifies the ecosystem's
scattered assets across CEFR rung, NLP capability, and traditional Sanskrit discipline (śikṣā,
vyākaraṇa, nirukta, chandas, kośa, kāvya, bhāṣya), and state a falsifiable agenda of four research
questions: (RQ1) does corpus frequency predict optimal vocabulary-learning order; (RQ2) can valid,
answer-keyed drills be auto-generated from attested corpus; (RQ3) which corpus-unconfirmed textbook
grammar rules are pedagogically load-bearing; (RQ4) how is a digital tool's teaching effect measured
at all. Unlike a purely aspirational research programme, this agenda is demonstrably productive: RQ1
is **already answered** — for content vocabulary, the two frequency-counting channels of one archive
agree at Kendall-τ = 0.887 (n = 7,120; `core_rank` is an argsort of per-lemma corpus coverage, 0
inversions), while the genuinely expert signal of the curated "learn-these-first" list is *membership*,
not internal order: function words, which make up 46% of the raw top-50 by frequency, are excluded by
the curator (with the corpus's epic-genre skew corrected); textbook
introduction order, by contrast, correlates only weakly with frequency — |τ| ≈ 0.05–0.10, in places
statistically significant (Kochergina surface p = 0.0158; Bühler lemmatised τ = +0.1006, p = 0.0011) —
and always far below the 0.45–0.84 between-textbook agreement. RQ3 is partially answered
by a two-axis textbook-vs-corpus divergence method already applied to five Sanskrit grammars. Three
of the four RQs already have integration deliverables built or building — a frequency-ordered SRS
spec, a Zaliznyak on-ramp A/B testbed, and a two-axis claim-verification pipeline — showing the
research and integration layers of the field compose into one programme rather than two. I close
with a two-layer evaluation methodology that makes every "this tool teaches better" claim in the
field falsifiable for the first time: a register of twelve **capability** metrics, one per aspect,
each with a denominator, a data source and a refutation condition and each computable from committed
artifacts today — of which **only two currently carry a measured value** (90.7% answer-keyed
morphology drill items; 56.5% by type and 56.2% by corpus token mass for the derivation on-ramp's
taught scope) — held strictly apart from learner **outcome** (learning gain, retention), which
remains the exclusive province of RQ4's single protocol. That separation is what lets eleven aspects
be tested before any user study runs, while keeping one ruler for teaching effect across all of them.
I close with a gap register — most saliently, the complete absence of audio anywhere in the
ecosystem, which blocks every beginner (A0–A2) rung.

## Thesis

Sanskrit computing has produced dictionaries, corpora, morphological engines, and dozens of
learner-facing tools — but no *field* that studies how those assets teach, and no falsifiable
account of what works. This paper names **digital Sanskrit pedagogy** as a research-and-integration
field, gives it a taxonomy that unifies the ecosystem's scattered assets, and states a falsifiable
agenda (four research questions) — one of which is **already answered** with a corpus result, and
three of whose integration deliverables are **already built**, so the agenda is demonstrably
productive rather than aspirational.

## §1 Introduction

The gap is this: the substance of Sanskrit pedagogy already exists, but it sits scattered across
roughly ten repositories and three partial maps, and the claim "this tool teaches better" is
asserted, never tested. The project's master planning document (MEGABOOK) names the last mile to
the student as the chain's main unclosed link.

The contribution is fivefold: (a) a field definition with an aspect taxonomy; (b) four falsifiable
research questions; (c) a first confirmed result; (d) an integration architecture that closes the
last mile; (e) a two-layer evaluation methodology — one falsifiable capability metric per aspect,
measurable from committed artifacts today, held apart from learner outcome, which stays with a
single study protocol.

## §2 The landscape (survey)

The survey reuses the field metadoc's aspect-primary taxonomy (12 aspects × CEFR rung × NLP
capability × traditional discipline × owning repo) and consolidates the three pre-existing maps by
reference: Systema's asset index with its A0–C2 ladder, the learner-materials inventory in
SanskritGrammar (`LEARNER_MATERIALS`), and kosha's positioning survey (`POSITIONING`). The headline
reading is that the **B1–B2 middle is asset-rich but unintegrated**, the **A0–A1 column is thin**
(audio and a native beginner grammar are the missing pieces), and **C1–C2 is planned depth**.

Survey table — the field metadoc's [§4a matrix](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md#4a-matrix--aspect--cefr-rung--where-the-assets-and-gaps-are),
aspect × CEFR rung (✅ built · 🟡 partial · 📋 planned · ⬜ gap · — not applicable at that rung),
with each aspect's pedagogy metric (PM) from the same document's
[§4e register](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md#4e-metric-view--the-first-measurable-result-per-aspect)
in the last column — the metric's value **today**, and the bar that would count as progress. The
full register, with denominators, data sources and refutation conditions, is §4:

| Aspect ↓ / Rung → | A0–A1 | A2 | B1 | B2 | C1–C2 | Metric — today → bar |
|---|---|---|---|---|---|---|
| Sandhi | — | ✅ split drills | 🟡 sandhied reading | 🟡 | — | **PM1** — unmeasured → ≥90% |
| Morphology | — | ✅ a-stems/present | ✅ paradigms | 🟡 all classes | 🟡 | **PM2** — 90.7% → ≥95% |
| Vocabulary/SRS | 🟡 | ✅ freq decks | ✅ | ✅ | ✅ | **PM3** — no corrected order → 0 function words in top 100 |
| Reading | — | — | ✅ subhāṣitas | 🟡 epic | 📋 Vedic/comm. | **PM4** — no scorer → τ ≥ 0.40 |
| Pāṇini | — | — | — | 📋 | 📋 sūtra↔corpus | **PM5** — unmeasured → ≥80% resolved |
| Zaliznyak on-ramp | — | ⬜ **build** | ⬜ **build** | 🟡 Талмуд | 🟡 | **PM6** — 56.5% type / 56.2% token (measured) |
| Audio/śikṣā | ⬜ **gap** | ⬜ **gap** | — | — | 📋 accent (VedaWeb) | **PM7** — **0** → ≥1 licensed unit |

Read by column, the table shows the same three things: **A0–A1 is the thinnest column** (audio and
native beginner grammar are the two holes), the **B1–B2 middle is asset-rich but unintegrated**
(§5's integration architecture is the fix), and **C1–C2 is planned depth**, not yet built (Pāṇini,
Vedic, commentary).

The metric column adds a second and less comfortable reading of the same rows. **Only two of the
seven wave-1 aspects carry a number at all** — PM2 and PM6 — and across the full twelve-aspect
taxonomy the count is two of twelve. The ✅ glyphs record that an asset was *built*, not that
anything about it was *measured*; the distance between those two claims is the distance this
paper's agenda is proposing to close. A survey that stopped at the glyphs would reproduce exactly
the condition §1 describes as the field's central defect — assets asserted to teach, never tested.

## §3 The research agenda (four falsifiable questions)

| RQ | Hypothesis (falsifiable) | Status | Extends |
|---|---|---|---|
| **RQ1** difficulty/ordering | Corpus frequency predicts learning order **for content vocabulary**, but only after **function-word exclusion + genre correction**. | **CONFIRMED** — τ = 0.887 measures agreement of two frequency-counting channels of one archive (`core_rank` = argsort of `coverage_pct`, 0 inversions), not expert-vs-corpus; the expert signal is *membership*: 46 % of top-50 lemmas excluded (all indeclinables/pronouns); DCS epic-genre bias; textbook order weak: \|τ\| ≈ 0.05–0.10, in places statistically significant (Kochergina surface p = 0.0158; Bühler lemmatised τ = +0.1006, p = 0.0011), always far below the 0.45–0.84 between-textbook agreement. [`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md) (A63). | kosha `core_rank`, textbook-τ (S1), [SG-H9](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md) (difficulty proxies), SG-H2 (positional drift) |
| **RQ2** drill generation | Valid, answer-keyed drills (sandhi-split, cloze, paradigm-fill) can be auto-generated from attested corpus with verified answers. | open | Talmud drill bank, Systema sort/match/cloze engines |
| **RQ3** textbook vs corpus | A subset of textbook grammar rules is not corpus-confirmed, and **those failures are pedagogically load-bearing** (they mislead learners). | partial — [A60](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60) (4/5), [FINDINGS §72](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md) two-axis method | Kochergina claim register, SG-H* fact-check axis |
| **RQ4** evaluation | A tool's teaching effect is measurable via learning-gain + retention user studies; the Zaliznyak on-ramp is the first testbed (**on-ramp-first vs Талмуд-first**). | open on the outcome layer — protocol [specified in full](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md), gated on a launch decision; testbed [built](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp); the capability layer (§4.2, PM1–PM12) is measurable now — 2 of 12 measured | learner-modelling, MEGABOOK §2.9 |

**Meta-claim (research + integration composes):** RQ1's result already *constrains* the integration
— the frequency-ordered SRS deck spec ([last-mile spec](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md)
Hop B) consumes kosha's `core_rank` "learn-these-first" ordering and strips function words *because*
RQ1 showed raw frequency fails. The agenda's questions and its plumbing are the same programme.

## §4 Evaluation methodology (RQ4 — the backbone)

Without a learning-gain metric, every "teaches better" claim is unfalsifiable. But a single
learning-gain study cannot be the field's only instrument either, because it gates every aspect's
progress on one recruitment. This section therefore states a **two-layer** methodology and defends
the line between the layers, which is the load-bearing methodological commitment of the paper.

### 4.1 Capability and outcome are different claims, and only one of them is measurable today

A **capability metric** is computed from committed artifacts — a coverage share, a rank
correlation, an agreement rate against a gold set — with no human subjects and no launch decision.
An **outcome metric** — learning gain, retention — requires learners, and is measured by the
protocol in §4.3.

The field's register admits **one capability metric per aspect** (§4.2) and reserves outcome
measurement **exclusively** to RQ4. Three consequences follow, and each is a claim this paper is
making rather than a bookkeeping convention:

1. **Aspects become falsifiable now.** If every aspect's metric were an outcome metric, nothing in
   the field would be measurable until recruitment runs — twelve aspects would sit unfalsifiable
   behind one study's launch flag.
2. **The field keeps one ruler for teaching effect.** Twelve aspects each free to define "teaches
   better" would produce twelve incompatible learning-gain instruments and no comparability
   between them. Exactly one instrument (§4.3) measures outcome; the capability metrics feed
   evidence into it and never restate it.
3. **A capability result may not be reported as a teaching result.** "PM2 reached 95%" means the
   drill bank is answer-keyable at that rate — it does not mean learners learn more from it. This
   paper treats the substitution of the first claim for the second as the field's characteristic
   error, and the two-layer split as the fix.

The split has a real cost: capability metrics can all move while teaching effect stays flat, and the
register cannot detect that. That is why RQ4 is not optional and why the twelve metrics are framed
as *evidence into* an evaluation, not as a substitute for one.

### 4.2 The metric register — one falsifiable capability metric per aspect

The register is maintained in the field metadoc
([§4e](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md#4e-metric-view--the-first-measurable-result-per-aspect)),
which is its source of truth; this paper reproduces it and does not re-define any metric. One
metric per aspect, deliberately: a basket of indicators always lets a stalled aspect show something
green. A metric is admitted only with a denominator, a data source, a current value and a
**refutation condition** — a metric that cannot be refuted is an indicator, not a claim.

| ID | Aspect | Metric (denominator) | Today | Bar → refuted if |
|---|---|---|---|---|
| **PM1** | Sandhi | auto-split items confirmed by an independent second segmenter / ≥200 hand-checked attested lines | unmeasured — no gold set | ≥90% → refuted if <90%: auto-split drills are not answer-keyable at scale |
| **PM2** | Morphology | drill items with an authoritative answer key / all drill items | **90.7%** — 40 863 / 45 045 attested cells | ≥95% across the union with the Talmud bank → refuted if the keyed share rises while the flagged share falls (coverage bought by fabricated keys) |
| **PM3** | Vocabulary/SRS | Kendall-τ of the published learn-order vs raw frequency rank; function words left in its top 100 | no corrected order published (curated vs raw τ = 0.887) | 0 function words in the top 100 → refuted if τ ≥ 0.99: the corrections are cosmetic |
| **PM4** | Reading | τ between predicted difficulty and first-full-coverage textbook lesson / ≥100 held-out passages | unmeasured — no scorer | τ ≥ 0.40 → refuted if τ < 0.20: the scorer reproduces frequency or length, not difficulty |
| **PM5** | Pāṇini | form-deriving sūtras with ≥1 attested corpus form / a fixed sūtra sample | unmeasured — concordance planned | ≥80% resolved → refuted if <50%: too sparse to teach from |
| **PM6** | Zaliznyak on-ramp | Приложение-1 roots in the 4 taught ablaut rows / the catalogue, by type **and** DCS token mass | **56.5% type** (421/745) · **56.2% token** (483 532/860 159; 82.7% join) | reporting rule, no threshold → refuted if added rows raise type coverage without raising token coverage |
| **PM7** | Audio | learner-facing units with a playable, licence-stamped track (absolute count) | **0** — the field's only zero baseline | ≥1 complete A0 unit with a provenance row → refuted if audio ships without one: it cannot be published, so it counts as 0 |
| **PM8** | Script | DCS conjunct-token mass covered by the first 50 conjuncts of the taught order | unmeasured — order named, coverage never computed | ≥90% → refuted if <70%: frequency-first is too weak an ordering |
| **PM9** | Metre | correct automatic metre IDs / ≥200 hand-labelled verses, reported per metre | unmeasured — trainer built, no gold set | ≥95% on the three commonest metres → refuted if <90% on śloka/anuṣṭubh |
| **PM10** | Composition | precision (and recall) of auto-feedback flags / ≥100 hand-labelled learner sentences | unmeasured — review is human-only | precision ≥0.90 at recall ≥0.50 → refuted if precision <0.80: false error-flags cost more trust than misses |
| **PM11** | Commentary | pratīka anchors resolving automatically to the exact mūla locus / ≥500 references | unmeasured | ≥85%, 0 guessed anchors → refuted if <60%: a manual-anchoring project, a different cost class |
| **PM12** | Spell/error | *correct* forms the faultfinder flags as errors / ≥5 000 correct learner-level forms | unmeasured — tuned scholar-facing | ≤2% → refuted if >5%: scholar-grade strictness is unusable for learners |

**Two of the twelve metrics have a value; ten do not.** PM2 (90.7% answer-keyed drill items) and
PM6 (56.5% by type, 56.2% by DCS token mass) are measured; PM7's zero is a real baseline rather
than a measurement; the remaining nine are unmeasured. I state this plainly because it *is* the
research programme this paper proposes — the register's function is to name what has never been
counted, and a field-defining paper that presented ten empty cells as an embarrassment would be
concealing its own agenda. The two cheapest to fill require no new build: PM8's conjunct
distribution and PM12's false-positive rate are both computable against data already committed.

Two further honesty conditions travel with the register. **The bars are proposed, not empirically
ratified** — four of the twelve rest on a measurement (PM2, PM3, PM4, PM7), one is a disclosure
rule with no threshold (PM6), and seven are reasoned from consequence or cost but unanchored (PM1,
PM5, PM8, PM9, PM10, PM11, PM12); they carry a scheduled recalibration point and may be revised in
the open against what gets measured, never in the same pass as a measurement that failed them.
And **a bar may never be relaxed to accommodate a result** — the register's revision protocol
records the old value, the new one and the reason, so a moved goalpost stays visible.

PM6 also reads as a result rather than a status line: the on-ramp's four taught ablaut rows reach
**56.5% of Приложение-1 by type and 56.2% by DCS token mass**, and the near-identity of the two
figures says the taught rows are frequency-neutral — they are neither the common roots nor the rare
ones, so type coverage can be read as reading-relevant coverage for this catalogue. That is a small
finding, but it is the kind the field currently has none of: a scope claim about a teaching artifact
with a denominator attached.

### 4.3 The outcome layer — one instrument for the whole field

The design rests on a pre/post diagnostic with matched cohorts and retention measured at N weeks.
The first concrete arm is an **A/B study on the Zaliznyak on-ramp** (work package W1c), comparing
an on-ramp-first cohort with a Талмуд-first cohort and measuring time to first correct derivation
alongside retention, with a pre-registered analysis plan (ANCOVA on the retention score with the
immediate post-test as covariate, so retention decay is separated from initial gain) and
differential attrition reported per arm rather than dropped. The protocol is
specified in full in
[`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md);
its design decisions are ruled and its remaining gate is a launch decision, not a methodological
one. The recommended first step is a pilot, not the full study.

This is the section that makes the field a *science* rather than a toolbox — but only in
combination with §4.2. The register without the study measures capability and calls it teaching;
the study without the register measures one arm of one aspect and leaves the other eleven
unfalsifiable.

## §5 Integration architecture (closing the last mile)

The [last-mile spec](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md)
(work package W1d) is the field's delivery vehicle: data flows from kosha (open data and lookup)
into Systema (the student-facing product) over a vendored-data-file contract, in three hops — a
reader, an SRS deck, and difficulty-driven sequencing. The research layer produces the signals; the
integration layer delivers them to a learner. This is the "research → education → value" chain made
concrete.

## §6 Gaps & risks

Five gaps carry the risk register (field metadoc §6). Audio is the largest: its absence blocks
every beginner rung (A0–A2). The epic-genre bias of the underlying corpus (the Digital Corpus of
Sanskrit, DCS) qualifies RQ1's result. The last mile to the student stays open until §5's
architecture ships. No learner corpus exists yet — the raw material for RQ4 and for adaptive
modelling. And the reading-pack and difficulty datasets are planned, not built.

**The measurement gap is itself a gap, and the largest one.** Ten of the twelve capability metrics
in §4.2 have never been computed, seven of the twelve bars are reasoned rather than anchored in a
measurement, and the outcome layer has produced no data at all because it is gated on a launch
decision. The risk this creates is specific: a proposed bar that goes unmeasured long enough stops
being read as a proposal and starts being cited as a standard. §4.2's recalibration point and
revision protocol exist to bound that risk, not to eliminate it.

## §7 Related work (live-verified 22-07-2026)

**Frequency-graded vocabulary & extensive reading (general L2 acquisition).** Nation's
frequency/coverage framework for vocabulary selection — a small high-frequency core covers most
running text, so learning order should track frequency, not intuition — is the standard reference
this paper's RQ1 tests against a specific (non-Indo-European-adjacent, classical, morphologically
rich) language for the first time (Nation 2001, *Learning Vocabulary in Another Language*, Cambridge
University Press). Waring & Takaki's graded-reader uptake study shows incidental vocabulary
acquisition from reading is real but slow and retention-fragile even at high exposure counts (Waring,
R., & Takaki, M. (2003). "At what rate do learners learn and retain new vocabulary from reading a
graded reader?" *Reading in a Foreign Language*, 15, 130–163) — the empirical floor RQ2's
auto-generated drills and §3.4's graded readers are trying to raise.

**Intelligent CALL / ITS & learner modelling.** Heift & Schulze's synthesis of parser-based error
diagnosis and student modelling in computer-assisted language learning (Heift, T., & Schulze, M.
(2007). *Errors and Intelligence in Computer-Assisted Language Learning: Parsers and Pedagogues*.
Routledge) is the ICALL line RQ2 (auto-drill generation with verified answer keys) and RQ4
(measuring teaching effect) extend into a language with no prior ICALL tradition of comparable
depth.

**Automated readability / frequency-difficulty NLP.** The ACL/NAACL readability-for-learners line —
word-frequency-based text difficulty (Xia, M., Kochmar, E., & Briscoe, T. (2016). "Text Readability
Assessment for Second Language Learners." *Proceedings of the 11th BEA Workshop*, ACL Anthology
[W16-0502](https://aclanthology.org/W16-0502/); and the frequency-vs-difficulty characterisation in
*Proceedings of the 11th BEA Workshop* [W16-0509](https://aclanthology.org/W16-0509.pdf)) — is the
NLP methodology §3.4's difficulty scorer (a named gap) will need to adapt; no such scorer has been
built for Sanskrit.

**Sanskrit computational resources.** The corpus and morphological infrastructure this paper's
research questions are computed against: the Digital Corpus of Sanskrit, ~3M lemmatised words
(Hellwig, O. *Digital Corpus of Sanskrit (DCS)*, 2010–2021,
[sanskrit-linguistics.org/dcs](http://www.sanskrit-linguistics.org/dcs/index.php)); the Sanskrit
Heritage Platform's segmentation/tagging engine (Goyal, P., & Huet, G. (2012). "A Distributed
Platform for Sanskrit Processing." *Proceedings of COLING 2012*, ACL Anthology
[C12-1062](https://aclanthology.org/C12-1062.pdf)); and vidyut, the Ambuda project's Rust
Pāṇinian-derivation and transliteration engine
([github.com/ambuda-org/vidyut](https://github.com/ambuda-org/vidyut)). kosha's `core_rank`
"learn-these-first" ordering (Leonchenko core-vocabulary list, consumed via kosha's
[`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv))
is this org's own curated-order asset, not an external citation — and its `core_rank` ordering is an
argsort of per-lemma corpus coverage, so RQ1's τ = 0.887 measures agreement between the archive's two
frequency-counting channels; the expert content of the list is the membership/exclusion decision (§3 RQ1).

**Gap this paper fills.** None of the above tests corpus statistics against Sanskrit learning order,
nor defines digital Sanskrit pedagogy as a field with a taxonomy and a falsifiable agenda: the L2
frequency literature (Nation; Waring & Takaki) is language-general and never applied to Sanskrit; the
ICALL literature (Heift & Schulze) predates the current Sanskrit-corpus tooling and was never
extended to it; the ACL readability line has no Sanskrit-language instantiation; and the Sanskrit
computational-resource line (DCS, Heritage, vidyut) is infrastructure, not pedagogy research — none
of it asks whether the infrastructure teaches. RQ1's already-confirmed result (§3, A63) is, to my
knowledge, the first test of corpus-frequency-predicts-learning-order for Sanskrit or any
classical Indo-Aryan language.

## Data inventory (claim → committed asset)

| Claim | Backing asset |
|---|---|
| the field + taxonomy | [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md) |
| the PM1–PM12 metric register (§4.2) | same doc, [§4e](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md#4e-metric-view--the-first-measurable-result-per-aspect) + §4e′ (bar anchors) — **source of truth; this paper reproduces, never re-defines** |
| PM2 = 90.7% | [`attested_drill_items.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/attested_drills/attested_drill_items.tsv) + [`COVERAGE_REPORT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/attested_drills/COVERAGE_REPORT.md) |
| PM6 = 56.5% type / 56.2% token | [`measure_onramp_scope.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/measure_onramp_scope.py) over [`talmud_appendix1.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/talmud_appendix1.json) × kosha `lemma_frequency.tsv` — re-run 04-08-2026, unchanged |
| RQ4 protocol (§4.3) | [`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md) |
| RQ1 result | [`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md) + [`data/difficulty_ordering/`](https://github.com/gasyoun/SanskritGrammar/tree/main/data/difficulty_ordering) (A63) |
| RQ3 method + result | [A60 draft](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60) + FINDINGS §72 |
| RQ4 testbed | [`TolchelnikovTalmud_2026/onramp/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp) (W1c) |
| integration architecture | [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md) (W1d) |
| frequency spine | kosha [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv) |
| textbook sequencing | [S1 τ result](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md) |

## To 3/5 → 5/5

- ~~**3/5:** live-verified §7 related work (real citations); the survey table filled from the metadoc; abstract written.~~ **DONE 22-07-2026** (H1464) — 8 live-verified external citations across four related-work threads (L2 frequency/extensive-reading, ICALL, ACL readability, Sanskrit computational resources) + the metadoc §4a matrix reproduced in §2 + a full abstract.
- ~~**4/5:** RQ4 evaluation protocol specified in full.~~ **DONE 04-08-2026** ([H1731](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1731-Opus_SanskritGrammar_a62-metric-register-into-evaluation-section_27.07.26.md)) — §4 rebuilt as a two-layer methodology: §4.1 states and defends the capability-vs-outcome split, §4.2 reproduces the PM1–PM12 register with denominators, refutation conditions, the bar-anchor honesty (4 measured / 1 disclosure rule / 7 unanchored) and the plain statement that 10 of 12 are unmeasured, §4.3 summarises the full RQ4 protocol. §2's survey matrix re-synced with the field doc's `Metric (§4e)` column; §6 gains the measurement gap.
- **5/5:** venue `@DECIDE` + byline/ORCID; ~~a Fable author-voice pass over the prose~~ — voice
  pass **done 04-08-2026** ([H1874](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1874-Fable_SanskritGrammar_a62-pedagogy-agenda-author-voice-pass_29.07.26.md),
  Fable 5 `claude-fable-5`), over the post-H1731 text; venue + byline/ORCID remain.

---

_Dr. Mārcis Gasūns_
