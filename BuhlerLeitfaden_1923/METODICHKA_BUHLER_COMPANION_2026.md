# Methodichka — a printed companion-commentary to Bühler, «Руководство к элементарному курсу санскритского языка» (1923)

_Created: 28-07-2026 · Last updated: 28-07-2026_

The roadmap for a **thin printed companion booklet** (методичка) to G. Bühler's
«Руководство к элементарному курсу санскритского языка» (Стокгольм, 1923 — the Russian
translation of the *Leitfaden für den Elementarcursus des Sanskrit*, 1883; electronic
edition v2.0 by N. P. Likhushina, 2008, 48 lessons). Grammatical-accuracy notes,
frequency refinements, a corpus-adjudicated case-government section, the misprint errata,
and cross-references to Knauer's *Фразы*. This plan is the durable spec; the executing
slice for v1 is [H1757](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1757-Fable_SanskritGrammar_buhler-metodichka-v1-companion-commentary_27.07.26.md).
The pattern followed is the Kochergina companion,
[METODICHKA_KOCHERGINA_COMPANION_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md)
(H807 precedent) — decisions already ruled there are inherited, not re-litigated.

Premise row: [review/EDITORIAL_NOTE_INDEX.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv)
`sanskritgrammar-sg-mo-021-future_visa#MO021-09` — «На основе SANGRAM потом будем писать
методички ко всем санскритским грамматикам на русском, начиная с Кочергиной и Бюлера».
Kochergina shipped (H807); this spec starts Bühler.

Companion metadoc (how to improve this plan, backlog, revision history):
[`METODICHKA_BUHLER_COMPANION_2026.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/METODICHKA_BUHLER_COMPANION_2026.meta.md).

---

## 0. What this is (and is not)

A **нетолстое печатное издание** — a slim, print-first companion the learner keeps open
beside Bühler. It does **not** reprint Bühler's text; it overlays *our* commentary,
numbers, government data and errata. The same structured data (the
[claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml)
registry with its `methodichka` field) also feeds the reading-site overlay, so print and
web never diverge.

**Audience & register:** Russian self-study and taught learners already using Bühler —
the same audience as the Kochergina companion, one shelf over. Prose in Russian, «е» not
«ё» (except всё/все disambiguation), IAST default with Devanāgarī where Bühler uses it,
corpus numbers from DCS.

**Author of record:** Dr. Mārcis Gasūns. Every grammatical verdict carries ⟦MG-виза⟧
before print — v1 authoring precedes the visa, exactly as H807 did for Kochergina.

**How Bühler differs from Kochergina (and why the booklet reads differently).** The
two-axis verification (403 claims) found Bühler's signature virtue to be *calibrated
hedging*: his «обыкновенно»/«иногда»/«очень редкая» land on the variable zones and his
absolutes on the categorical ones. Kochergina's companion corrects calibration errors;
Bühler's corrects mostly **misprints** — all 8 FALSE claims are misprint-class, each
self-contradicted by the paradigm or example the book prints beside it. The booklet's
centre of gravity therefore shifts from «правило сформулировано слишком сильно» to
«напечатано не то, что имелось в виду» + the frequency layer Bühler's era could not have.

---

## 1. Decisions locked

Inherited from the Kochergina companion rulings (12-07-2026, MG), applied to Bühler:

| # | Fork | Ruling |
|---|---|---|
| A | Source-of-truth model | **Hybrid**, unchanged. Numbers, verdicts and errata rows live in [claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml) / [errata.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/errata.yml) (generated outputs `claims.json`, `CLAIMS_VERIFIED.md`, `ERRATA.mdx` — never hand-edited); connective commentary is authored prose. The learner-facing distillate of each note is stored in the registry's `methodichka` field (the Apte precedent), so the site overlay and the print manuscript cite one source. |
| B | Coverage of v1 | **Thin curated now, comprehensive later.** v1 ships the 17 non-TRUE / pedagogy-flagged notes + the case-government section + the errata slice + Knauer cross-references. The full harvest is already done (403 claims, drained 15-07-2026) — v2 widens to TRUE-but-worth-noting claims and re-runs against DCS-2026. |
| C | Errata scope | **Better position than Kochergina:** 8 misprint rows already sit in [errata.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/errata.yml) (H797, self-contradiction evidence per row). v1 prints them; a scan-против-digitization check (1923 print vs Likhushina 2008) stays open as B-1. |
| D | Exercise sourcing | **Deferred to a follow-on slice** (unlike Kochergina v1). Bühler's own exercises are the org's shared-sentence hub — the [Concordance](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx) shows 119 of 124 shared clusters involve Bühler — so the exercise appendix should be designed together with the concordance, not before it. v1 carries cross-references only. |

New, Bühler-specific:

| # | Fork | Ruling |
|---|---|---|
| E | Government data | The [Scherzl↔DCS adjudication](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md) (1,168 relations, 693 CONFIRMED) becomes a learner-facing раздел of the booklet — its first downstream consumer. The 3.9 % dependency-arc ceiling is **always stated with the numbers**, never dropped. |

---

## 2. Prior art — what already exists (consume, do not rebuild)

| Pillar | Asset (source → generated) | State |
|---|---|---|
| Grammatical accuracy | [`claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml) → [`CLAIMS_VERIFIED.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/CLAIMS_VERIFIED.md) + [`claims.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.json) | 🟢 **403 claims** graded on two axes (H797 core 14-07-2026 + full drain 15-07-2026): fact — 383 TRUE · 7 OVERSTATED · 8 FALSE · 5 UNTESTABLE; pedagogy — 395 JUSTIFIED · 5 MISLEADING · 2 FREQUENCY-HIDDEN · 1 ORDER-QUESTIONABLE; 24 `mg_footnote` frequency badges. Numbers reproduced by [`verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/verify_claims_dcs.py) |
| Case government | [`government_class_index/`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/README.md): `government_lexicon.jsonl` (355 KB), `dcs_verb_government_profiles.json`, `government_corpus_verdicts.tsv`, from MG's 10.8 MB Scherzl index (`index_Shertsl_Byuler_dopoln_180721.xlsx`) | 🟢 **1,168 relations adjudicated against DCS** (H1372): 693 CONFIRMED · 1 CONTRADICTED (hand-cleared, no erratum) · 288 UNATTESTED-INSUFFICIENT · 186 NOT-ADJUDICABLE. Until v1, its only downstream artifact was its own report — this booklet is the first learner-facing consumer |
| Errata (misprints) | [`errata.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/errata.yml) → [`ERRATA.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/ERRATA.mdx) | 🟢 8 rows (H797), each localized to Урок/mdx-line with the self-contradiction evidence; ERRATA_PRINT_SHEET.html exists |
| Cross-references | [`Concordance/catalog.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx) — Bühler ↔ Knauer ↔ Kochergina shared exercise sentences | 🟢 124 clusters: 79 Bühler↔Knauer only, 33 Bühler↔Kochergina only, 7 in all three (H327) |
| Frequency probes | [`hb21_u_stem_feminine_freq.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/hb21_u_stem_feminine_freq.json), [`hb158_gender_resolution_probe.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/hb158_gender_resolution_probe.json), [`hb256_suppletive_comparative_freq.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/hb256_suppletive_comparative_freq.json) + their scripts | 🟢 committed with reproducible builders |

**Headline finding already in hand** (the model for the whole booklet): the one place
Bühler states a frequency direction — «перфект … только реже употребляется» (HB-57,
Урок XLIII) — the corpus flips it: perfect 90,001 tokens vs imperfect ~46,695, ~1.9×
*more* frequent (stratum-conditioned: DCS is epic-heavy). Everywhere else his hedging is
calibrated; the flip is the exception that proves the register was worth building.

---

## 3. v1 scope (H1757) vs follow-on

**v1 = one manuscript section**, [`METODICHKA_BUHLER_V1_KOMMENTARII_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/METODICHKA_BUHLER_V1_KOMMENTARII_2026.md):

1. Commentary notes on all 17 flagged claims (8 FALSE + 7 OVERSTATED + 2 pedagogy-only),
   in lesson order, each citing its HB-id;
2. The case-government раздел from the Scherzl↔DCS adjudication, ceiling stated;
3. The errata slice (8 misprints, compact print table);
4. Cross-references to Knauer's [*Фразы*](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/README.md)
   via the concordance;
5. Annex: the 24 M.G. frequency badges (`mg_footnote` registry fields);
6. `methodichka` fields filled in `claims.yml` for every claim that has a note.

**Follow-on (not v1):** exercise appendix (Decision D above), отсылки-раздел in the
Kochergina раздел-III shape, print assembly + PDF, the B-1 scan check, v2 comprehensive
coverage. Mint fresh handoffs when v1 is visaed.

---

## 4. Rights (do not skip)

Bühler died in 1898 — the German original is public domain. The **1923 Russian
translation and the 2008 Likhushina electronic edition are separate rights objects**:
the translator's identity/death date and the terms under which the electronic edition
was prepared have not been established in-repo. The Docusaurus reading page publishes
the text already, but **print is a new distribution act** — before the booklet (which
quotes Bühler only minimally, as commentary requires) or any PDF goes public, run
[/publish-safety-check](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md)
and resolve @DECIDE B-2 below. The companion's own commentary, numbers and data are ours.

---

## 5. Open questions (@DECIDE / @DO)

- **B-1 — scan check for the 8 misprints.** Each FALSE is self-contradicted in the
  digitized text, but whether the corruption is the 1923 print's or the 2008
  digitization's is unresolved per row (HB-372's note asks exactly this). Needs the 1923
  scan. *Blocks nothing in v1; changes the errata rows' `note` wording only.*
- **B-2 — translation rights.** Establish the 1923 translator and the Likhushina-edition
  terms before print (see § 4).
- **B-3 — government section depth.** v1 prints the summary + a learner-facing
  confirmed-frames selection. Whether the full 693-row confirmed table belongs in print
  (as an appendix) or stays web-only is a print-assembly call at the P5-analogue stage.

_Dr. Mārcis Gasūns_
