# Zalizniak's three Sanskrit models compared — 1975 vs 1978 vs 2004 (calibrated against Whitney 1889)

_Created: 08-07-2026 · Last updated: 09-07-2026_

Zalizniak described Sanskrit **three times** and used a **different paradigm each time**;
none of the three is a *full grammar*. To keep the genre honest this pass calibrates them
against **Whitney's *Sanskrit Grammar* (1889)** — the one actual full reference grammar in
the repo ([`WhitneyGrammar_1889/`](https://github.com/gasyoun/SanskritGrammar/tree/main/WhitneyGrammar_1889),
18 chapters, §§1–1316). Second pass (Opus 4.8 `claude-opus-4-8`): four parallel structural
reads of the in-repo `.mdx`, correcting the first pass's genre errors. This is the
intra-Zalizniak axis of the [morphoclass comparison](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_COMPARISON_ROADMAP.md)
(H357); it matters because the Талмуд's core machinery descends from the **1975** model,
not the **1978** Очерк our §-concordance points at.

## The works, by genre (the "full grammar" was a mislabel)

| Work | Genre — accurately | Size | Coverage |
|---|---|---|---|
| **Whitney 1889** | **Full reference grammar** (the benchmark) | §§1–1316, 18 ch. | Everything: phonetics, complete sandhi, all declension + conjugation, accent, syntax, derivation, compounds, Vedic vs Classical |
| **Zalizniak 1975** — *Morphophonological Classification of Sanskrit Verbal Roots* (EN) | **Verb-only research article** | ~498 lines, 5 tables | Verbal roots only — no declension |
| **Zalizniak 1978** — *Грамматический **очерк** санскрита* (RU) | **Grammatical SKETCH** («очерк», not a grammar) | ~242 §§ | Broad but compressed sketch of the whole language |
| **Zalizniak 2004** — *Конспект* (RU) | **SYNOPSIS** («конспект грамматических сведений») | ~657 lines | Whole language in compressed synopsis + heavy diachrony; ≈218 curated roots |

**The key relation:** Whitney *describes* exhaustively with **no higher-order abstractions**
(no morphological positions, no ablaut series, no root-type calculus, no deep/surface
notation — just guṇa/vṛddhi increments, strong/middle/weakest stems, "union-vowel *i*", and
case-by-case description). The Zalizniak works do the opposite: they **replace** exhaustive
description with abstractions. The Талмуд (2026) then turns those abstractions into a
generative engine. So the lineage runs Whitney *(describe)* → Zalizniak *(abstract)* →
Толчельников *(generate)*.

## Detailed comparison (12 structural axes)

Whitney shown as the full-grammar baseline; the three Zalizniak columns are the object of study.

| Axis | Whitney 1889 (benchmark) | 1975 Classification | 1978 Очерк | 2004 Конспект |
|---|---|---|---|---|
| **1. Морфологическая позиция** (numbered) | ABSENT — strong/middle/weakest stems | **PRESENT — numbered 1/2/3**, THE grade-driver | **ABSENT** — grade keyed to grammatical form; strong/weak in declension only | **ABSENT** — strong/weak "+" + per-form `v/g` rules |
| **2. Grade system** | guṇa/vṛddhi "increment"; no zero-term | 3: zero/guṇa/vṛddhi | 3 ступени слабая/средняя/долгая (§50) | 3: ø/g/v symbols |
| **3. Ряд (ablaut series)** | **ABSENT** (no series abstraction) | A–N + subscript **1/2** | A–N indices **1/2** (§50,60) | A₁…N₂ subscript **1/2** |
| **4. Тип (root behaviour type)** | ABSENT as lettered type; present-class I–X + individual | **PRESENT — Roman I–IV** ("degree of alternation", central result) | No unified type; cross-axes (§61–63) | ABSENT as lettered type |
| **5. seṭ/aniṭ/veṭ** | terms ABSENT; = "union-vowel *i*" | PRESENT, 2nd axis, tied to Whitney | PRESENT (§63) | PRESENT (with "колебания" caveat) |
| **6. Notation (deep/surface)** | ABSENT — straight descriptive | no запись I/II; proposes H+uppercase | **запись I/II — the 1978 spine** (§28–30) | ABSENT two-level; single-level + subscripts |
| **7. Root inventory** | no catalogue *in the grammar* (separate 1885 Roots vol.); full index | **~750 Whitney roots enumerated + classified** | **ABSENT** (schema only, §59) | **≈218** curated «важнейшие корни» + IE cognates |
| **8. Declension** | **COMPLETE** (all stems/cases/numbers, gradation, accent) | **ABSENT — verb-only** | Full (stem-types, strong/middle/weak, heteroclita §78–101) | Full (ending-matrix + exceptions) |
| **9. Verbal paradigms** | **COMPLETE** (all classes, all tense-systems, secondary conj., non-finite) | scope-boundary lists, by position | Full "systems" (§109–165) | Full (classes 1–10, all tenses) |
| **10. Sandhi** | **COMPLETE** (largest chapter, internal+external) | light/background only | Extensive, ordered II→I→phonetic (§31–46) | Deep, ordered (7+7 blocks) |
| **11. Generativity** | descriptive only | generative *in intent* (rules unwritten) | generative rule-computing (§458) | rule-generative via formulae |
| **12. Genre / scope** | **full reference grammar** (max) | verb-only article | broad **sketch** (очерк) | broad **synopsis** (конспект); diachrony front-loaded |

## How many differences (among the three Zalizniak works), by severity

**MAJOR — 5** (a model-primitive or the object of description differs):

1. **Numbered морфологическая позиция** — grade-driving abstraction: **1975 only**; 1978 & 2004 drop it. *(MG's example. Whitney also lacks it — it is a 1975 innovation.)*
2. **Root-type calculus I–IV** — 1975's central primitive; 1978 replaces it with cross-axes, 2004 has no lettered type.
3. **Two-level запись I/II notation** — the **1978** spine; 1975 has no I/II system, 2004 is single-level. *(Whitney has no deep/surface notation at all.)*
4. **Genre / object of description** — 1975 **verb-only article** (no declension) vs 1978 **sketch** vs 2004 **synopsis**. **None is a full grammar** — that is Whitney 1889. *(Corrected: the first pass wrongly called 1978 & 2004 "full grammar".)*
5. **Root inventory** — 1975 enumerates ~750 roots, 2004 carries ≈218 curated roots with IE cognates, **1978 has none**.

**MEDIUM — 6:** grade-selection engine (position→type vs stipulated-per-form vs strong/weak+`v/g`) · root sub-classification axis-set · sandhi depth (marginal in 1975 vs extensive in 1978/2004) · deep↔surface made explicit (1978) vs informal (1975) vs single-level (2004) · diachrony/IE-comparison prominence (front-loaded in 2004) · samprasāraṇa placement.

**MINOR — 6:** grade terminology · **series subscripts** (all use 1/2; NONE uses the `0`-variants — see implications) · symbol inventories · strong/weak stance (1975 rejects it for verbs; 1978/2004 use it in declension) · present-class digit as a root tag (2004) · length/audience gradient.

**Totals: 5 major · 6 medium · 6 minor.**

## What it means for us

1. **The §-concordance points at the wrong Zalizniak layer for the Талмуд's core mechanism.**
   H241 links Talmud sections to the **1978 Очерк**, but the Талмуд's engine — numbered
   **positions 1/2/3**, the **root-type** calculus, position-driven generation — comes from
   the **1975 Classification**, which 1978 **absents**. Actionable: attribute per-mechanism —
   positions/type/Ряд-generation → **1975**; запись I/II + full paradigms/sandhi → **1978**;
   diachrony/cognates → **2004** — not a blanket "→ Очерк 1978".
2. **"The Талмуд develops Zalizniak" = it revives the 1975 line Zalizniak himself abandoned.**
   Positions, the type calculus, and full generativity are exactly what he dropped in the more
   traditional 1978/2004 works. That is the memo's headline.
3. **The `0`-subscript Ряд variants (I0/M0/N0/R0/U0) are a `/z/` DB bug, NOT a real category**
   — corrected 08-07-2026 (H357). The author (I. E. Tolchelnikov) stated on
   [issue #50](https://github.com/gasyoun/SanskritGrammar/issues/50): «Рядов `I0`, `N0`, `R0`,
   `U0`, `M0` не существует — это ошибка обработки Таблицы 2 в базе `/z/`». So they are neither
   Zalizniak's (all three works use only subscript 1/2), nor Gasuns's, nor Tolchelnikov's own
   extension — they are **115 buggy rows in А. П. Широбоков's `/z/` computer model** of the
   Talmud, to be **discarded**. The ryad inventory is therefore **identical** across all three
   works; the apparent "extension" was an implementation artefact. (This supersedes the earlier
   reading of these rows as an authoritative author extension.)
4. **Тип is relabeled, not inherited** — Talmud Тип (s/a/v) ≠ Zalizniak 1975 Тип (I–IV).
5. **"По Зализняку" is ambiguous** — three paradigms mean footnotes/companion text must cite
   **which** work (1975 / 1978 / 2004). And none of them is the "full grammar" — that role is
   Whitney's, the advanced-stage reference above the whole Russian ladder.

## Related — Tolchelnikov's own papers on the 1975 line

[`TolchelnikovTalmud_2026/papers/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/papers)
collects the author's 2023–2025 conference papers/talks developing this same 1975→generative-engine
line (Auroville Feb 2024, Fortunatovskiye 2023, Dubyanskiye 2024), plus Kulikov's independent
50th-anniversary commentary on the same Zalizniak-1975 article — published as MDX at
[`papers/index`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/index.mdx)
for side-by-side reading with the comparison above.

_Dr. Mārcis Gasūns_
