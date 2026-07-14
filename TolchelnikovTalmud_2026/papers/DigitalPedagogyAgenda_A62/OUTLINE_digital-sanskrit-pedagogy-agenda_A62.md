# A62 — Digital Sanskrit pedagogy: a research agenda (outline)

_Created: 14-07-2026 · Last updated: 14-07-2026_

**ID:** A62 · **Readiness:** 2/5 (outline + data-inventory) · **Home:** SanskritGrammar ·
**Venue candidates:** eLex / Lexikos / ISCLS / CALICO / ReCALL / an NLP4DH venue (a human `@DECIDE`s).
The field-defining paper of the [digital-Sanskrit-pedagogy field](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md);
handoff [H914](https://github.com/gasyoun/Uprava/blob/main/handoffs/H914-Fable_SanskritGrammar_pedagogy-w1b-agenda-paper-a62_14.07.26.md).
Aggregate numbers only (in-copyright textbook sources).

> **Provenance note.** H914 is tier-locked to Fable 5; this readiness-2 scaffold was authored on
> **Opus 4.8 (`claude-opus-4-8[1m]`)** by author decision (the "go" override). The Fable author-voice
> pass belongs at readiness 4→5, on the prose, not this skeleton.

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
thin** (audio, native beginner grammar); **C1–C2 is planned depth**. Survey table = the metadoc §3
rows, condensed.

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

## §7 Related work (stub — verify + cite live at 3/5)

Frequency-graded vocabulary & graded readers (L2 acquisition); intelligent CALL / ITS & learner
modelling; Sanskrit computational resources (DCS, Heritage, vidyut, kosha, Leonchenko core-vocab);
the ACL frequency-pedagogy / readability line. **Gap this paper fills:** no prior work tests corpus
statistics against Sanskrit learning order, nor defines the field.

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

- **3/5:** live-verified §7 related work (real citations); the survey table filled from the metadoc; abstract written.
- **5/5:** the RQ4 evaluation protocol specified in full; venue `@DECIDE` + byline/ORCID; a Fable author-voice pass over the prose.

---

_Dr. Mārcis Gasūns_
