# Grammar Claims the Corpus Does Not Confirm — corpus-adjudicated divergences in Sanskrit reference and textbook grammars (A60, working outline)

_Created: 12-07-2026 · Last updated: 14-07-2026_

> **Status: readiness 4/5 — full single-book draft written.** This directory now carries the complete
> paper: (a) method, framing, related-work (H773 Q0); (b) the complete Kochergina central table — all
> **12** `verdict_fact ∈ {OVERSTATED, FALSE}` divergences from
> [H768](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H768-Opus_SanskritGrammar_kochergina-claim-verification-roadmap_12.07.26.md)'s
> finished 43-claim register, each classified + quantified (H773 Q1); and (c) the **full single-book
> draft** — [`DRAFT_grammar-claims-corpus-denies_A60.md`](DRAFT_grammar-claims-corpus-denies_A60.md),
> all sections in prose (H773 Q3). This outline is now the working scaffold behind the draft. **To 5/5:**
> `/paper-referee` + `/paper-author-pass` (Fable 5 register polish) + `/venue-scout`. The cross-grammar
> comparison (Q2 — Bühler / Knauer / Zaliznyak / Apte) is **future work / an enhancement, not a gate on
> the single-book paper**; a human decides whether to submit single-book or hold for cross-grammar.
> _Q0 + HK-4 by Opus 4.8 (`claude-opus-4-8`) 12-07-2026 (PR #146); Q1 central table 12-07-2026 (PR #147);
> Q3 draft by Opus 4.8 (`claude-opus-4-8`) 12-07-2026._

---

## Abstract (thesis)

Pedagogical and reference grammars of Sanskrit state categorical rules — _"образуется от всех…",
"лишь от части…", "по единому правилу…"._ Measured against the attested corpus (DCS-2021), some of
these rules describe a system the texts **under-populate or contradict**: the rule is either
over-generalised, true-but-marginal, licensed-but-unused, or flatly at odds with the corpus
distribution. The set of such divergences — _what the grammars assert that the corpus denies_ — is
itself a finding. It has, per an [ACL Anthology](https://aclanthology.org/) crosswalk, **no strong
precedent** as a corpus-adjudicated target (see §3). We build a two-axis claim register — designed to
span the Sanskrit grammars digitised in this repository and here fully applied to Kochergina's textbook
(1998, 43 verified assertions across all 40 lessons) — isolate the `verdict_fact ∈ {OVERSTATED, FALSE}`
subset (12 claims), and give each divergence a *class* and a corpus number. The paper's contribution is the
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

**2.3 Divergence typology (the contribution).** Every qualifying claim is assigned exactly one
class. The assignment lives in [`divergence_classes.yml`](divergence_classes.yml) (with a one-line
rationale per claim) and is joined to H768's verdicts by
[`build_divergence_table.py`](build_divergence_table.py) — the class is the only thing this paper
adds to the register; the fact-verdicts and numbers are H768's, consumed not re-derived.

| # | Class | Definition | Kochergina instances (n) |
|---|---|---|---|
| 1 | **Over-generalisation** | absolute quantifier ("всегда / от всех / по единому правилу / никогда") + a well-defined, non-marginal exception class | HK-4a, HK-10, HK-14, HK-16, HK-25, HK-34, HK-38, HK-40 (**8**) |
| 2 | **Rule-real-but-marginal** | a "большинство / обычно" majority claim the corpus does not bear out — the pattern is real but a minority, plurality, or register-conditioned | HK-15, HK-19, HK-32 (**3**) |
| 3 | **System-vs-usage** | the reference grammar licenses a form the corpus barely uses (licensed ≠ attested) | **0 — empty, and that is a finding** (see §5.1): in the OVERSTATED/FALSE subset no divergence is of this shape; the licensed-but-unused cases are all `verdict_fact=TRUE`/`FREQUENCY-HIDDEN` (HK-21, HK-26), out of this table's fact-axis scope. Slot reserved for the Whitney-sourced cross-grammar harvest. |
| 4 | **Flat contradiction** | the grammar's stated conditioning (which allomorph/form, and when) does not match the corpus distribution | HK-4b (**1**) |

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

## 5. Central table (the paper's core)

All rows are **Kochergina 1998**, from the complete 43-claim register. The canonical, regenerable
copy — with the full Russian claim text and every corpus number — is
[`TABLE_grammar-claims-corpus-denies_A60.md`](TABLE_grammar-claims-corpus-denies_A60.md), produced
by [`build_divergence_table.py`](build_divergence_table.py). What follows is the curated reading copy.

**Register composition (why this is a "minority report").** The corpus **confirms the large
majority** of Kochergina's assertions — the paper is about the minority it does not:

| verdict_fact | n | share |
|---|--:|--:|
| ✅ TRUE | 28 | 65.1 % |
| 🟠 OVERSTATED | 11 | 25.6 % |
| ❌ FALSE | 1 | 2.3 % |
| ⚪ UNTESTABLE | 3 | 7.0 % |

The **12** OVERSTATED/FALSE rows (27.9 %) are the divergence set. Grouped by class:

| Class | ID | Claim (gloss) | Fact | Corpus evidence / counter-class | Pedagogy |
|---|---|---|---|---|---|
| **1 Over-generalisation** | HK-4a | future "от ВСЕХ глаголов по единому правилу -syá" | OVERSTATED | 18,004 fut. tokens are productive, but **3 conditioned suffixes** -sya/-ṣya/-iṣya, not one rule | MISLEADING |
| **1** | HK-10 | finite verb "**никогда** не носит ударение" | OVERSTATED | verb **is** accented in a subordinate clause & sentence-initially (Whitney §168) | MISLEADING |
| **1** | HK-14 | "основы на -ā — женского рода" | OVERSTATED | root/monosyllabic ā-stems + masc. proper nouns exist (Whitney §347ff) | MISLEADING |
| **1** | HK-16 | "основы на -ī и -ū **всегда** женского рода" | **FALSE** | masc. **rathī, senānī, sudhī**, monosyll. **bhū-** attested (Whitney §343–352) | MISLEADING |
| **1** | HK-25 | "простой перфект от **всех** односложных корней" | OVERSTATED | periphrastic-perfect roots **vid, ās** & long-vowel monosyllables (Whitney §1070) | MISLEADING |
| **1** | HK-34 | "род сложного слова = род последней основы" | OVERSTATED | **bahuvrīhi** gender tracks the referent, not the final stem (Whitney §1293ff) | MISLEADING |
| **1** | HK-38 | root aorist "от **некоторых** корней на -ā и bhū" | OVERSTATED | source set wider: **gam, sthā, dā, jñā, kram, dhā** (Whitney §829ff) | MISLEADING |
| **1** | HK-40 | double preverb "**всегда**" contact/distant order | OVERSTATED | attested double-preverb verbs show ordering variation (Whitney §1076ff) | MISLEADING |
| **2 Rule-real-but-marginal** | HK-15 | imperfect "**обычно** ... повествования о прошлом" | OVERSTATED | stratum-dependent: in Vedic the perfect competes; "обычно" hides the period split | FREQUENCY-HIDDEN |
| **2** | HK-19 | "**большинство** IX класса — носовой+согласная" | OVERSTATED | many kryādi roots are **not** nasal+C: krī, jñā, grah, bandh, pū, lū, prī | FREQUENCY-HIDDEN |
| **2** | HK-32 | "-as/-is/-us **в большинстве** среднего рода" | OVERSTATED | masc. -as (candramas) + mixed -is/-us; lumping the three suffixes overstates | FREQUENCY-HIDDEN |
| **4 Flat contradiction** | HK-4b | -ṣya/-iṣya as "**варианты**" of a base -sya | OVERSTATED | **-iṣya 56.8 %** (1,487) > -sya 24.9 % (652) > -ṣya 18.3 % (479) of 2,618 forms — the "variant" is the majority; real predictor is seṭ/aniṭ, not root-final phonology | FREQUENCY-HIDDEN |

### 5.1 What the aggregation shows

- **Distribution across classes:** Over-generalisation **8**, Rule-real-but-marginal **3**, Flat
  contradiction **1**, System-vs-usage **0**. Kochergina's failures are overwhelmingly *quantifier
  overreach* (an absolute rule with an unstated exception class), not conditioning errors.
- **By claim kind:** universality **7**, statistic **3**, rule **1**, allomorphy **1** — the
  divergences cluster in the *universal* statements, exactly where an absolute quantifier is riskiest.
- **The typology explains the pedagogy verdict.** Class 1 coincides *exactly* with the H768
  `MISLEADING` pedagogy flag (8 = 8); classes 2 + 4 coincide *exactly* with `FREQUENCY-HIDDEN`
  (3 + 1 = 4). An absolute rule with a hidden escape hatch reads as misleading; a minority/variant
  reframed as the norm reads as frequency-hidden. The two H768 axes and the H773 typology are not
  independent — the divergence class predicts the pedagogy verdict.
- **The empty class 3 is itself a result.** No OVERSTATED/FALSE claim is "system licenses X but the
  corpus does not use it": those are all `verdict_fact = TRUE` with a `FREQUENCY-HIDDEN` flag (the
  aniṭ set understated in HK-26, the h/j future reflex in HK-21). *Licensed-but-unused* is a pedagogy
  problem in an otherwise-correct rule, not a factual divergence — a distinction the two-axis design
  surfaces and a one-axis "error list" would miss. The slot is reserved for Whitney-sourced claims in
  the cross-grammar harvest, where the system itself is the object.

**Not divergences — the UNTESTABLE bucket (3).** HK-5 (thematic aorist "самый распространённый" — the
DCS-2021 export does not tag aorists by formation type), HK-41 (prefixed-verb 60/30/<10 % semantic
split) and HK-42 (a-privative ≥⅓ of prefixed nouns, ~80 % abstract) assert numbers with no disclosed
count base. The corpus *cannot adjudicate* them; they are flagged, not scored, and kept out of the
divergence set.

## 6. Data inventory (assets backing each claim)

| Asset | Path | Backs |
|---|---|---|
| **Full draft (H773 Q3)** | [`DRAFT_grammar-claims-corpus-denies_A60.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/DRAFT_grammar-claims-corpus-denies_A60.md) | the paper itself — all sections in prose (abstract → references) |
| Claim register (H768) | [`KocherginaUchebnik_1998/claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.yml) | all 43 rows' claim text + two-axis verdict + corpus number |
| Divergence classes (H773) | [`divergence_classes.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/divergence_classes.yml) | the class + rationale for each OVERSTATED/FALSE row (§2.3, §5) |
| Table generator (H773) | [`build_divergence_table.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/build_divergence_table.py) | joins the two sources → the central table; `--check` guards unclassified rows |
| Central table (generated) | [`TABLE_grammar-claims-corpus-denies_A60.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/TABLE_grammar-claims-corpus-denies_A60.md) | §5 source of record (full Russian text + every number) |
| Corpus numbers | [`KocherginaUchebnik_1998/claims_dcs_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims_dcs_stats.json) | §4 allomorph counts (HK4_future) |
| Reproducer | [`KocherginaUchebnik_1998/verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py) | re-derives the DCS numbers |
| Corpus | DCS-2021 (Hellwig, CC BY) via [VisualDCS](https://github.com/gasyoun/VisualDCS) | attestation / frequency ground truth |
| Systemic reference | [`WhitneyGrammar_1889/`](https://github.com/gasyoun/SanskritGrammar/tree/main/WhitneyGrammar_1889) | systemic grammatical fact (by §) |
| Root morphoclass | [`TolchelnikovTalmud_2026/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026) | which roots form X |

## 7. Limitations & next steps (maps to H773 Q1–Q4)

- **Central table complete for Kochergina (Q1 ✅).** All 12 OVERSTATED/FALSE divergences from the
  finished 43-claim register are classified and quantified. What remains is breadth, not depth: the
  table is **single-book**.
- **Per-grammar comparison (Q2) — UNBLOCKED for Bühler 14-07-2026 (H797 Phase 2, Fable 5
  `claude-fable-5`).** The second verified register is live:
  [`BuhlerLeitfaden_1923/claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml)
  — 63 verified (57 TRUE · 4 OVERSTATED · 1 FALSE · 1 UNTESTABLE), flagged rows HB-2, HB-8, HB-10,
  HB-57 (perfect claimed rarer than imperfect vs DCS 61,986 > 47,554), HB-60 (FALSE, likely misprint).
  Knauer / Zaliznyak / Apte remain; re-running
  [`build_divergence_table.py`](build_divergence_table.py) over both registers is now possible —
  it groups by grammar automatically. A human decides single-book vs cross-grammar submission.
- **Cross-grammar generalisation now has its first data point.** §4 attributes the future-stem
  framing to Kochergina only — correctly so: Bühler's register shows the SAME corpus number
  (seṭ -iṣya 56.8%) confirming his hedged formulation TRUE (HB-59) where Kochergina's absolute was
  OVERSTATED (HK-4). The divergence is presentation calibration, not shared framing — cite it that
  way, not as a common error.
- **Class 3 unpopulated by design here.** System-vs-usage needs a *system-sourced* claim set (Whitney /
  Pāṇinian licensing); it will fill from the cross-grammar harvest, not from Kochergina's beginner text.
- **Numbers are consumed, not re-derived.** The corpus figures are H768's, reproduced by
  `verify_claims_dcs.py` against `../VisualDCS`; per the roadmap boundary this paper does not recompute
  them. A submission-time re-run of the reproducer is the audit step, not a rebuild.
- **Rights.** Kochergina 1998 (and Zaliznyak) source text is in-copyright. The paper may cite claims
  and report **aggregate** corpus numbers; a `/data-release` of the underlying text is **not** covered
  by the 06-07-2026 reading-site override — re-run `/publish-safety-check` before any DOI.
- **Draft → submission (Q3–Q4):** `/paper-referee` then `/paper-author-pass`; `/venue-scout`
  (ACL/CL or a lexicography journal); readiness bump to 4/5 once a second grammar lands the per-grammar
  comparison.

---

_Dr. Mārcis Gasūns_
