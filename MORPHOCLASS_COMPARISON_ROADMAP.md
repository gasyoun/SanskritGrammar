# Roadmap — morphophonological classification of Sanskrit verbal roots: Zalizniak 1975 → Gasuns 2014 → Tolchelnikov 2026

_Created: 08-07-2026 · Last updated: 08-07-2026_

Plan for a **deep three-way comparison** answering MG's question: *how exactly does
Tolchelnikov's Талмуд develop Zalizniak's 1975 morphophonological classification, and
where do they diverge?* — treating it as a lineage with Gasuns 2014 as the middle term.

**Deliverable (decided with MG, 08-07-2026):** a **Russian-language memo + data
crosswalk**, as an **internal companion doc** (also the sourced basis for Talmud
footnote-proposals), **not** a paper for now. Executed via the handoff this roadmap
anchors — this file is the plan, not the analysis.

---

## The three works (the lineage)

| Step | Work | In-repo source | Role in the lineage |
|---|---|---|---|
| 1975 | А. А. Зализняк, *Morphophonological Classification of Sanskrit Verbal Roots* (English) | [`ZalizniakMorphology_1975/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ZalizniakMorphology_1975) (`.docx` + `.mdx`; now committed on `main` as of the 08-07 errata→main merge) | Origin: the deep-morpheme √-record with **Тип** + **seṭ/aniṭ**; the ablaut apparatus later called *Ряд*. Also underpins his [*Очерк* (1978)](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx). |
| 2014 | М. Гасунс, «Морфонологическая запись глагольных корней санскрита» (PhD, Russian) | [`GasunsDhatu_2014/Морфонологическая запись глагольных корней санскрита.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/%D0%9C%D0%BE%D1%80%D1%84%D0%BE%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F%20%D0%B7%D0%B0%D0%BF%D0%B8%D1%81%D1%8C%20%D0%B3%D0%BB%D0%B0%D0%B3%D0%BE%D0%BB%D1%8C%D0%BD%D1%8B%D1%85%20%D0%BA%D0%BE%D1%80%D0%BD%D0%B5%D0%B9%20%D1%81%D0%B0%D0%BD%D1%81%D0%BA%D1%80%D0%B8%D1%82%D0%B0.mdx) + [`02_gasuns-dhatu-PhD-text2.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx) + [`О записи омонимии корней…`](https://github.com/gasyoun/SanskritGrammar/tree/main/GasunsDhatu_2014) | Middle term. Its abstract **explicitly** says «Автор **развивает разработки акад. Зализняка**» (e.g. √vAsH → **√vás(i)** = «неполноизменяемый корень, группа seṭ»), and compares Zalizniak's deep-morpheme notation against Western root-lists (Morgenroth, Werba). A prior comparison the memo builds on. |
| 2026 | И. Е. Толчельников, «Санскритская морфология: руководство» / Талмуд | [`TolchelnikovTalmud_2026/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026) + the [`samskrtam.ru/z/`](https://samskrtam.ru/z/) root DB (Shirobokov) | Endpoint: develops the classification into a full **generative MTT engine** — Ряд A–N, morphological positions 1/2/3, seṭ from Whitney, surface-form computation. |

## Intra-Zalizniak axis — his three works use different paradigms (2nd pass DONE)

Zalizniak described Sanskrit **three times with a different model each time**, so "по
Зализняку" is ambiguous — and **none of the three is a full grammar**. Comparison done,
now **calibrated against Whitney 1889** (the one full reference grammar in the repo) —
[`ZALIZNIAK_1975_1978_2004_COMPARISON.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md):
**5 major · 6 medium · 6 minor** differences across 12 axes. Genre ladder (corrected):
Whitney 1889 *full grammar* » 1978 *очерк/sketch* » 2004 *конспект/synopsis* » 1975
*verb-only article*; Whitney *describes*, Zalizniak *abstracts*, the Талмуд *generates*. Headline for the memo: the
Талмуд's core engine (**numbered positions 1/2/3**, the **root-type calculus**,
position-driven generation) comes from **1975**, which the **1978 Очерк our §-concordance
points at ABSENTS** — so the Талмуд revives the 1975 line Zalizniak himself dropped, and the
concordance should attribute per-mechanism (1975 vs 1978 vs 2004), not blanket "→ Очерк 1978".
Also resolved: the `0`-subscript Ряд variants (I0/M0/N0/R0/U0) are in **none** of the three
Zalizniak works — **Tolchelnikov's own extension** (he is a student of М. Гасунс; Shirobokov
built only the `/z/` computer model, not the classification). The H357 pass deepens this
against the full texts.

## ⚠ Terminology trap (must not be conflated)

- **Ряд (ablaut series A–N)** — the vowel-grade series of the Talmud/Zalizniak
  morphophonological classification. **This is the object of the comparison.**
- **«ряды согласных» (варги)** — the five *consonant* classes (velar/palatal/retroflex/
  dental/labial) in Gasuns's separate corpus-statistics study
  [`Распределение рядов согласных.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/%D0%A0%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%B8%D0%B5%20%D1%80%D1%8F%D0%B4%D0%BE%D0%B2%20%D1%81%D0%BE%D0%B3%D0%BB%D0%B0%D1%81%D0%BD%D1%8B%D1%85.mdx). **Unrelated** to the ablaut Ряд — do not pull it into the comparison.

## Axes of comparison (the crosswalk columns)

For each of the three works, tabulate and then diff:

1. **Notation** — Zalizniak's записи I/II & √-form; Gasuns's √vás(i)-style deep-morpheme
   record; Talmud's `{√}` + `[P][E][F]` + positions 1/2/3.
2. **Ablaut-series (Ряд) taxonomy** — the A–N inventory; **provenance of the `0`-subscript
   variants** `I0/M0/N0/R0/U0` seen in `/z/` but absent from the Talmud's Table 2 — did they
   originate with Gasuns 2014, Shirobokov's DB, or elsewhere? (open question to resolve).
3. **Тип** (s / a / v / v1…) — behaviour under morphological position; how each defines it.
4. **seṭ / aniṭ / veṭ** — integration and source (Talmud draws it from Whitney §63; Gasuns
   encodes it in the √-form; does the 1975 paper?).
5. **Root inventory / source** — Whitney-only (Talmud) vs each predecessor's scope.
6. **Generativity** — the core "development": classify (1975) → refine the record (2014) →
   *generate* surface forms (2026, MTT). Name what each step added.

## Deliverable structure (Russian)

1. **Memo (Russian prose)** — the lineage narrative and, per axis, «что добавил каждый шаг
   / в чем разошлись», with a clear verdict on *как именно Талмуд развивает Зализняка 1975*.
2. **Crosswalk tables** — (a) category-level: the Ряд/Тип/seṭ taxonomy aligned across the
   three works; (b) per-root divergence: where the three disagree, seeded by the existing
   `/z/` reconciliation (see below) plus Gasuns's and (if root-listed) Zalizniak's tables.

## Findings already in hand (seed the analysis)

From the H329 `/z/` reconciliation
([`data/z_reconciliation_report.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/z_reconciliation_report.md),
876 roots):

- a **systematic ṛ-nucleus R→A divergence** between `/z/` (Tolchelnikov) and our derived Ряд;
- the extra **`0`-subscript Ряд variants** `/z/` carries beyond Table 2;
- **57 over-confident `high`** derived-Ряд cases shown false; seṭ agreement 91.3% with `/z/`
  filling 246 of our nulls and flagging 203 veṭ.

These are candidate *divergence rows*, but the `/z/` report compares Tolchelnikov vs **our
derived** values — the memo must re-anchor divergences against **Zalizniak 1975 / Gasuns
2014 directly**, not against our derivation.

## Suggested phases

1. **Prerequisite** — `ZalizniakMorphology_1975/` is now committed on `main` (done);
   `/prior-art` for any existing Zalizniak↔Gasuns↔Tolchelnikov comparison.
2. **Extract** — read each work's classification apparatus; tabulate categories per axis.
3. **Category crosswalk** — align Ряд/Тип/seṭ definitions across the three; flag renamings,
   additions (the `0`-variants), and drops.
4. **Per-root crosswalk** — join root assignments where available; produce the divergence
   table; re-anchor the `/z/` findings against 1975/2014.
5. **Memo** — write the Russian synthesis; route genuine per-root divergences into
   [`footnote-proposals/proposals.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/footnote-proposals/proposals.yml)
   (author-gating for Ivan — never a silent edit to the running text).

## Guardrails

- **Author-gating** — any divergence that would touch the Talmud's running text enters only
  as an Ivan-approved footnote.
- **Do not conflate the two «ряд» senses** (see the terminology trap above).
- **1975 source is committed on `main`** (08-07 errata→main merge) — build on `main`.
- **WhitneyRoots is read-only**; this work reads the three sources + `/z/` and writes only
  new derived assets inside the Talmud repo.

_Dr. Mārcis Gasūns_
