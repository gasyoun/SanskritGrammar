# Grammar Claims the Corpus Does Not Confirm — corpus-adjudicated divergences in Sanskrit reference and textbook grammars (A60, working outline)

_Created: 12-07-2026 · Last updated: 12-07-2026_

> **Status: readiness 2/5 skeleton.** This outline seeds paper **A60** with (a) the method,
> framing, and related-work spine (H773 phase Q0) and (b) the single fully-verified worked
> example (HK-4, the future stem). The central table below is deliberately **one row + schema**:
> the remaining rows are gated on [H768](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H768-Opus_SanskritGrammar_kochergina-claim-verification-roadmap_12.07.26.md)
> completing its P1 harvest (only the verb-system core of `claims.yml` is verified so far) and
> on the cross-grammar extension ([H773](https://github.com/gasyoun/Uprava/blob/main/handoffs/H773-Opus_SanskritGrammar_grammar-asserts-corpus-denies-study_12.07.26.md)).
> _Seeded by Opus 4.8 (`claude-opus-4-8`), H773 Q0 + HK-4, 12-07-2026._

---

## Abstract (thesis)

Pedagogical and reference grammars of Sanskrit state categorical rules — _"образуется от всех…",
"лишь от части…", "по единому правилу…"._ Measured against the attested corpus (DCS-2021), some of
these rules describe a system the texts **under-populate or contradict**: the rule is either
over-generalised, true-but-marginal, licensed-but-unused, or flatly at odds with the corpus
distribution. The set of such divergences — _what the grammars assert that the corpus denies_ — is
itself a finding. It has, per an [ACL Anthology](https://aclanthology.org/) crosswalk, **no strong
precedent** as a corpus-adjudicated target (see §3). We build a two-axis claim register across the
Sanskrit grammars digitised in this repository, isolate the `verdict_fact ∈ {OVERSTATED, FALSE}`
subset, and give each divergence a *class* and a corpus number. The paper's contribution is the
**typology of divergence** plus the adjudicated table, not merely a list of errors.

## 1. Introduction

Reference grammars are prescriptive-descriptive hybrids written before machine-readable corpora
existed. Their categorical phrasing was the only economical way to teach a paradigm. The question
this paper asks is narrow and falsifiable: **for each categorical assertion, does the DCS corpus
confirm it, and if not, why not?** We are not auditing scholarship for "errors" — most surface facts
in these grammars are correct. We are measuring the gap between a rule *as stated for teaching* and
the *distribution a reader actually meets in the texts*, and classifying that gap.

## 2. Method

**2.1 Claim register (consumed from H768).** Each falsifiable assertion in a grammar is an entry in
that book's `claims.yml` with a two-axis verdict — `verdict_fact` (TRUE / OVERSTATED / FALSE /
UNTESTABLE, with the number) and `verdict_pedagogy` (JUSTIFIED / MISLEADING / RARE-AS-CENTRAL /
FREQUENCY-HIDDEN / ORDER-QUESTIONABLE). This paper reads only the `OVERSTATED`/`FALSE` fact-axis
subset. The register is generated to `CLAIMS_VERIFIED.md` via
[`scripts/build_claims.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_claims.py);
corpus numbers are reproduced by
[`KocherginaUchebnik_1998/verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py).

**2.2 Ground truth (triangulation, source-priority rule).** Per the confirmed H768 tie-break: **DCS**
is authority for frequency/attestation, **Whitney 1889** for systemic grammatical fact,
**Tolchelnikov-Talmud 2026** for root-morphoclass. When the three disagree the disagreement is
**flagged, never silently resolved**. The corpus is DCS-2021 (Oliver Hellwig, CC BY), via
[VisualDCS](https://github.com/gasyoun/VisualDCS).

**2.3 Divergence typology (the contribution).** Every qualifying claim is assigned one class:

| # | Class | Definition | Seed instance |
|---|---|---|---|
| 1 | **Over-generalisation** | "от всех / по единому правилу" where the corpus shows a sizeable class the rule does not fit | HK-4 (§4) |
| 2 | **Rule-real-but-marginal** | the form exists but at a frequency the textbook's prominence misrepresents | — (pending) |
| 3 | **System-vs-usage** | Whitney/Pāṇinian system licenses a form the corpus does not use (licensed ≠ attested) | — (pending) |
| 4 | **Flat contradiction** | the grammar's stated conditioning does not match the corpus distribution | — (pending) |

## 3. Related work — where this sits, and the gap it fills

Real ACL anchors (do not over-claim beyond these):

- **Segmentation / DCS spine:** Hellwig & Nehrdich 2018, EMNLP — [D18-1295](https://aclanthology.org/D18-1295/); ByT5-Sanskrit 2024 — [2024.findings-emnlp.805](https://aclanthology.org/2024.findings-emnlp.805/). These supply the corpus and its counts, not the adjudication.
- **Difficulty progression (methodology only, English-trained):** Arase et al. 2022, EMNLP — [2022.emnlp-main.416](https://aclanthology.org/2022.emnlp-main.416/).
- **Textual directionality (weak precedent):** Hoenen 2015, NAACL — [N15-1127](https://aclanthology.org/N15-1127/).

**Honest non-findings (the niche).** An ACL-Anthology crosswalk confirms there is **no** paper that
treats **seṭ/aniṭ or ablaut as a corpus-adjudicated classification target**, and **none** that
adjudicates a grammar's *categorical rule* against corpus frequency. A60's worked example (§4) is
exactly a seṭ/aniṭ corpus adjudication — it lands in a documented, unoccupied gap. _(Crosswalk
inherited from [`ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) §"Honest non-findings"; re-verify at submission.)_

## 4. Worked example (verified seed): the future stem

**The claim.** Kochergina (Учебник санскрита, 1998) presents the future stem as formed _от ВСЕХ
глаголов по единому правилу_ **-syá**, with consonant-stem **-ṣya / -iṣya** given as *variants*
(_согл. корни: -ṣya/-iṣya_). The unifying "single rule -syá" is the foregrounded fact; the split is
a footnote.

**The corpus (DCS-2021).** Across 2,618 distinct attested future stems (18,004 tokens, 2.3 % of
781,618 verbal tokens):

| Allomorph | Distinct forms | Share |
|---|---|---|
| **-iṣya** (seṭ) | 1,487 | **56.8 %** |
| -sya | 652 | 24.9 % |
| -ṣya | 479 | 18.3 % |

**The divergence.** The surface facts are all correct — every allomorph Kochergina names exists — so
this is not a factual error in the narrow sense. But the *presentation* inverts the distribution: the
form taught as the base rule (**-sya**) is a **minority** realisation (24.9 %), while the form
demoted to a consonant-stem "variant" (**-iṣya**, the seṭ outcome) is the **majority** (56.8 %). The
categorical framing "по единому правилу -syá" **overstates** — it hides the seṭ/aniṭ lexical
conditioning that actually governs which allomorph appears. A learner optimised on "the rule is
-sya" will mis-predict the single most common case.

- `verdict_fact`: **OVERSTATED** · `verdict_pedagogy`: **FREQUENCY-HIDDEN**
- Divergence class: **1 — Over-generalisation** (a uniform rule where the corpus shows a conditioned split with the demoted "variant" dominant)
- Ties to roadmap spine **S2** (seṭ/aniṭ as a classification axis).

## 5. Central table (the paper's core — schema + seed)

Columns: grammar · claim (short) · source(s) · `verdict_fact` · corpus number · divergence class · note.

| Grammar | Claim | Source | verdict_fact | Number | Class | Note |
|---|---|---|---|---|---|---|
| Kochergina 1998 | future stem "по единому правилу -syá"; -ṣya/-iṣya as variants | DCS, Whitney | **OVERSTATED** | -iṣya **56.8 %** majority (1,487 / 2,618) vs -sya 24.9 % | 1 | seṭ conditioning unnamed |
| _pending H768 harvest_ | … | … | … | … | … | … |
| _pending cross-grammar (Bühler / Knauer / Zaliznyak / Apte)_ | … | … | … | … | … | … |

## 6. Data inventory (assets backing each claim)

| Asset | Path | Backs |
|---|---|---|
| Claim register | [`KocherginaUchebnik_1998/claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.yml) | every row's claim text + two-axis verdict |
| Corpus numbers | [`KocherginaUchebnik_1998/claims_dcs_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims_dcs_stats.json) | §4 allomorph counts (HK4_future) |
| Reproducer | [`KocherginaUchebnik_1998/verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py) | re-derives the DCS numbers |
| Corpus | DCS-2021 (Hellwig, CC BY) via [VisualDCS](https://github.com/gasyoun/VisualDCS) | attestation / frequency ground truth |
| Systemic reference | [`WhitneyGrammar_1889/`](https://github.com/gasyoun/SanskritGrammar/tree/main/WhitneyGrammar_1889) | systemic grammatical fact (by §) |
| Root morphoclass | [`TolchelnikovTalmud_2026/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026) | which roots form X |

## 7. Limitations & next steps (maps to H773 Q1–Q4)

- **Central table incomplete (Q1).** One verified row. Fills as H768's P1 harvest verifies more
  Kochergina claims and the cross-grammar registers (Bühler / Knauer / Zaliznyak / Apte) come online.
- **Per-grammar comparison (Q2)** — which grammar over-generalises most — needs ≥2 grammars verified;
  not yet computable.
- **Cross-grammar generalisation is unverified.** §4 attributes the future-stem framing to Kochergina
  only. Whether Bühler/Knauer/Zaliznyak present it identically is the H773 harvest, not yet done —
  do **not** cite a shared framing until measured.
- **Rights.** Kochergina 1998 (and Zaliznyak) source text is in-copyright. The paper may cite claims
  and report **aggregate** corpus numbers; a `/data-release` of the underlying text is **not** covered
  by the 06-07-2026 reading-site override — re-run `/publish-safety-check` before any DOI.
- **Draft → submission (Q3–Q4):** `/paper-referee` then `/paper-author-pass`; `/venue-scout`
  (ACL/CL or a lexicography journal); readiness bump on a complete central table.

---

_Dr. Mārcis Gasūns_
