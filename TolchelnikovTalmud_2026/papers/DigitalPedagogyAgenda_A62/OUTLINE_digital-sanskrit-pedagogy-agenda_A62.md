# A62 — Digital Sanskrit pedagogy: a research agenda (outline)

_Created: 14-07-2026 · Last updated: 22-07-2026_

**ID:** A62 · **Readiness:** 3/5 (live-verified related work + abstract) · **Home:** SanskritGrammar ·
**Venue candidates:** eLex / Lexikos / ISCLS / CALICO / ReCALL / an NLP4DH venue (a human `@DECIDE`s).
The field-defining paper of the [digital-Sanskrit-pedagogy field](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md);
handoff [H914](https://github.com/gasyoun/Uprava/blob/main/handoffs/H914-Fable_SanskritGrammar_pedagogy-w1b-agenda-paper-a62_14.07.26.md);
3/5 pass = [H1464](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1464-Sonnet_SanskritGrammar_a62-agenda-related-work-abstract_22.07.26.md).
Aggregate numbers only (in-copyright textbook sources).

> **Provenance note.** H914 is tier-locked to Fable 5; this readiness-2 scaffold was authored on
> **Opus 4.8 (`claude-opus-4-8[1m]`)** by author decision (the "go" override). The 3/5 pass (abstract,
> survey table, related work) was authored on **Sonnet 5 (`claude-sonnet-5`)**. The Fable author-voice
> pass still belongs at readiness 4→5, on the prose, not this skeleton.

## Abstract

Sanskrit computing has produced dictionaries, morphological engines, annotated corpora, and dozens
of learner-facing tools, but no field that studies *how those assets teach*, and no falsifiable
account of what actually works pedagogically. We name **digital Sanskrit pedagogy** as a
research-and-integration field, give it a twelve-aspect taxonomy that unifies the ecosystem's
scattered assets across CEFR rung, NLP capability, and traditional Sanskrit discipline (śikṣā,
vyākaraṇa, nirukta, chandas, kośa, kāvya, bhāṣya), and state a falsifiable agenda of four research
questions: (RQ1) does corpus frequency predict optimal vocabulary-learning order; (RQ2) can valid,
answer-keyed drills be auto-generated from attested corpus; (RQ3) which corpus-unconfirmed textbook
grammar rules are pedagogically load-bearing; (RQ4) how is a digital tool's teaching effect measured
at all. Unlike a purely aspirational research programme, this agenda is demonstrably productive: RQ1
is **already answered** — corpus frequency tracks the expert "learn-these-first" order for content
vocabulary (Kendall-τ = 0.887, n = 7,120), but only after excluding function words, which make up 46%
of the raw top-50 by frequency, and after correcting for the corpus's epic-genre skew; textbook
introduction order, by contrast, is nearly frequency-agnostic (τ ≈ 0.05). RQ3 is partially answered
by a two-axis textbook-vs-corpus divergence method already applied to five Sanskrit grammars. Three
of the four RQs already have integration deliverables built or building — a frequency-ordered SRS
spec, a Zaliznyak on-ramp A/B testbed, and a two-axis claim-verification pipeline — showing the
research and integration layers of the field compose into one programme rather than two. We close
with the evaluation methodology (RQ4) that makes every "this tool teaches better" claim in the field
falsifiable for the first time, and a gap register — most saliently, the complete absence of audio
anywhere in the ecosystem, which blocks every beginner (A0–A2) rung.

## Thesis

Sanskrit computing has produced dictionaries, corpora, morphological engines, and dozens of
learner-facing tools — but no *field* that studies how those assets teach, and no falsifiable
account of what works. This paper names **digital Sanskrit pedagogy** as a research-and-integration
field, gives it a taxonomy that unifies the ecosystem's scattered assets, and states a falsifiable
agenda (four research questions) — one of which is **already answered** with a corpus result, and
three of whose integration deliverables are **already built**, so the agenda is demonstrably
productive rather than aspirational.

## §1 Introduction

- The gap: the substance of Sanskrit pedagogy exists but scattered across ~10 repos and three
  partial maps; "this tool teaches better" is asserted, never tested; MEGABOOK flags "the last mile
  to the student" as the chain's main unclosed link.
- The contribution: (a) a field definition + aspect taxonomy; (b) four falsifiable research
  questions; (c) a first result; (d) an integration architecture that closes the last mile.

## §2 The landscape (survey)

Reuses the field metadoc's aspect-primary taxonomy (12 aspects × CEFR rung × NLP capability ×
traditional discipline × owning repo). Consolidates the three pre-existing maps — Systema's
asset-index + A0–C2 ladder, SanskritGrammar's `LEARNER_MATERIALS`, kosha's `POSITIONING` — by
reference. Headline: the **B1–B2 middle is asset-rich but unintegrated**; the **A0–A1 column is
thin** (audio, native beginner grammar); **C1–C2 is planned depth**.

Survey table — the field metadoc's [§4a matrix](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md#4a-matrix--aspect--cefr-rung--where-the-assets-and-gaps-are),
aspect × CEFR rung (✅ built · 🟡 partial · 📋 planned · ⬜ gap · — not applicable at that rung):

| Aspect ↓ / Rung → | A0–A1 | A2 | B1 | B2 | C1–C2 |
|---|---|---|---|---|---|
| Sandhi | — | ✅ split drills | 🟡 sandhied reading | 🟡 | — |
| Morphology | — | ✅ a-stems/present | ✅ paradigms | 🟡 all classes | 🟡 |
| Vocabulary/SRS | 🟡 | ✅ freq decks | ✅ | ✅ | ✅ |
| Reading | — | — | ✅ subhāṣitas | 🟡 epic | 📋 Vedic/comm. |
| Pāṇini | — | — | — | 📋 | 📋 sūtra↔corpus |
| Zaliznyak on-ramp | — | ⬜ **build** | ⬜ **build** | 🟡 Талмуд | 🟡 |
| Audio/śikṣā | ⬜ **gap** | ⬜ **gap** | — | — | 📋 accent (VedaWeb) |

The pattern the table makes visible: **A0–A1 is the thinnest column** (audio and native beginner
grammar are the two holes), the **B1–B2 middle is asset-rich but unintegrated** (§5's integration
architecture is the fix), and **C1–C2 is planned depth**, not yet built (Pāṇini, Vedic, commentary).

## §3 The research agenda (four falsifiable questions)

| RQ | Hypothesis (falsifiable) | Status | Extends |
|---|---|---|---|
| **RQ1** difficulty/ordering | Corpus frequency predicts learning order **for content vocabulary**, but only after **function-word exclusion + genre correction**. | **CONFIRMED** — Kendall-τ 0.887 (core_rank vs rank_all); 46 % of top-50 lemmas excluded (all indeclinables/pronouns); DCS epic-genre bias; textbook order frequency-agnostic (τ≈0.05). [`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md) (A63). | kosha `core_rank`, textbook-τ (S1), [SG-H9](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md) (difficulty proxies), SG-H2 (positional drift) |
| **RQ2** drill generation | Valid, answer-keyed drills (sandhi-split, cloze, paradigm-fill) can be auto-generated from attested corpus with verified answers. | open | Talmud drill bank, Systema sort/match/cloze engines |
| **RQ3** textbook vs corpus | A subset of textbook grammar rules is not corpus-confirmed, and **those failures are pedagogically load-bearing** (they mislead learners). | partial — [A60](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60) (4/5), [FINDINGS §72](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md) two-axis method | Kochergina claim register, SG-H* fact-check axis |
| **RQ4** evaluation | A tool's teaching effect is measurable via learning-gain + retention user studies; the Zaliznyak on-ramp is the first testbed (**on-ramp-first vs Талмуд-first**). | open — [A32](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md); testbed [built](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp) | learner-modelling, MEGABOOK §2.9 |

**Meta-claim (research + integration composes):** RQ1's result already *constrains* the integration
— the frequency-ordered SRS deck spec ([last-mile spec](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md)
Hop B) consumes `core_rank` and strips function words *because* RQ1 showed raw frequency fails. The
agenda's questions and its plumbing are the same programme.

## §4 Evaluation methodology (RQ4 — the backbone)

Without a learning-gain metric, every "teaches better" claim is unfalsifiable. Design: pre/post
diagnostic, matched cohorts, retention at N weeks; the first concrete arm is **A/B on the Zaliznyak
on-ramp** (W1c) — on-ramp-first vs Талмуд-first — measuring time-to-first-correct-derivation and
retention. This is the section that makes the field a *science*, not a toolbox.

## §5 Integration architecture (closing the last mile)

The [last-mile spec](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md)
(W1d) is the field's delivery vehicle: kosha (open data/lookup) → Systema (product), via a
vendored-data-file contract, three hops (reader / SRS deck / difficulty→sequencing). The research
layer produces the signals; the integration layer delivers them to a learner. This is the
"research → education → value" chain made concrete.

## §6 Gaps & risks

Audio (the biggest, blocks A0–A2); DCS genre bias (RQ1); the still-open last mile; no learner corpus
(the raw material for RQ4 + adaptive modelling); reading-pack + difficulty datasets planned-not-built.
(Field metadoc §6.)

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
is this org's own curated-order asset, not an external citation, and is the "expert ground truth"
RQ1's τ-correlation is measured against.

**Gap this paper fills.** None of the above tests corpus statistics against Sanskrit learning order,
nor defines digital Sanskrit pedagogy as a field with a taxonomy and a falsifiable agenda: the L2
frequency literature (Nation; Waring & Takaki) is language-general and never applied to Sanskrit; the
ICALL literature (Heift & Schulze) predates the current Sanskrit-corpus tooling and was never
extended to it; the ACL readability line has no Sanskrit-language instantiation; and the Sanskrit
computational-resource line (DCS, Heritage, vidyut) is infrastructure, not pedagogy research — none
of it asks whether the infrastructure teaches. RQ1's already-confirmed result (§3, A63) is, to this
paper's knowledge, the first test of corpus-frequency-predicts-learning-order for Sanskrit or any
classical Indo-Aryan language.

## Data inventory (claim → committed asset)

| Claim | Backing asset |
|---|---|
| the field + taxonomy | [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md) |
| RQ1 result | [`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md) + [`data/difficulty_ordering/`](https://github.com/gasyoun/SanskritGrammar/tree/main/data/difficulty_ordering) (A63) |
| RQ3 method + result | [A60 draft](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60) + FINDINGS §72 |
| RQ4 testbed | [`TolchelnikovTalmud_2026/onramp/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp) (W1c) |
| integration architecture | [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md) (W1d) |
| frequency spine | kosha [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv) |
| textbook sequencing | [S1 τ result](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md) |

## To 3/5 → 5/5

- ~~**3/5:** live-verified §7 related work (real citations); the survey table filled from the metadoc; abstract written.~~ **DONE 22-07-2026** (H1464) — 8 live-verified external citations across four related-work threads (L2 frequency/extensive-reading, ICALL, ACL readability, Sanskrit computational resources) + the metadoc §4a matrix reproduced in §2 + a full abstract.
- **4/5:** RQ4 evaluation protocol specified in full.
- **5/5:** venue `@DECIDE` + byline/ORCID; a Fable author-voice pass over the prose.

---

_Dr. Mārcis Gasūns_
