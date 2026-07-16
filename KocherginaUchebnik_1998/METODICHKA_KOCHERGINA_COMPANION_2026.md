# Methodichka — a printed companion-commentary to Kochergina, *Учебник санскрита*

_Created: 12-07-2026 · Last updated: 16-07-2026_

The roadmap for a **thin printed companion booklet** (методичка) to V. A. Kochergina's
*Учебник санскрита* — grammatical-accuracy notes, clarity/frequency refinements, extra
reinforcement exercises, cross-references to other Russian works, and a per-edition typo
(errata) list. This plan is the durable spec; each execution slice is a separate `H###`
handoff. First slice: [H807](https://github.com/gasyoun/Uprava/blob/main/handoffs/H807-Fable_SanskritGrammar_kochergina-methodichka-v1_12.07.26.md).

Companion metadoc (how to improve this plan, backlog, revision history):
[`METODICHKA_KOCHERGINA_COMPANION_2026.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.meta.md).

---

## 0. What this is (and is not)

A **не­толстное печатное издание** — a slim, print-first companion the learner keeps
open beside Kochergina. It does **not** reprint Kochergina's text (in copyright); it
overlays *our* commentary, numbers, exercises and errata. The same structured data also
feeds the existing reading-site overlay, so print and web never diverge.

**Audience & register:** Russian self-study and taught learners already using Kochergina.
Prose in Russian, «е» not «ё» (except всё/все disambiguation), IAST default with
Devanāgarī where Kochergina uses it, corpus numbers from DCS.

**Author of record:** Dr. Mārcis Gasūns. Every grammatical verdict and exercise key is
human-visaed before print.

---

## 1. Decisions locked (12-07-2026, MG)

| # | Fork | Ruling |
|---|---|---|
| A | Source-of-truth model | **Hybrid.** Numbers, verdicts and errata rows live in the `*.yml` registries (single source of truth, shared with the site); connective commentary and pedagogy essays are authored prose, assembled into the print manuscript by a build step. |
| B | Coverage of v1 | **Thin curated now, comprehensive later.** v1 ships only the high-value commentary (where Kochergina is wrong / misleading / frequency-blind / unclear) + compact errata + a small exercise appendix. The full-textbook claim harvest (H768) is already done — 43 claims — so v2 widens coverage and re-runs against DCS-2026, it does not start from scratch. |
| C | Editions in errata scope | **Start from what we have.** Build the errata register from the digitized text now; fold 2024/2025 edition diffs in when MG supplies the scans. Errata never blocks v1. |
| D | Exercise sourcing | **Both.** Corpus-sourced reading (attested Sanskrit) + newly authored graded drills matched to each занятие. |

---

## 2. Prior art — what already exists (consume, do not rebuild)

The repo has treated Kochergina as a book-with-commentary since early July. Three of the
five pillars already have working infrastructure:

| Pillar | Asset (source → generated) | State |
|---|---|---|
| Grammatical accuracy | [`claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.yml) → [`CLAIMS_VERIFIED.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/CLAIMS_VERIFIED.md) | 🟢 **43 claims** graded on a **fact axis** vs. DCS-2021 + Whitney (H768 full-textbook sweep, 12-07-2026: 28 TRUE, 11 OVERSTATED, 1 FALSE, 3 UNTESTABLE); numbers reproduced by [`verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py) |
| Clarity / frequency | same registry, `verdict_pedagogy` field | 🟢 second **pedagogy axis** on the same 43 claims; 16 flagged for overreach / hidden frequency |
| Errata (per edition) | [`errata.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/errata.yml) → [`ERRATA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/ERRATA.md), `/errata` skill | 🔴 system built, list **empty** — awaiting a printed sheet or an edition diff |
| Extra exercises | 3 213 in-repo exercise sentences · [Knauer *Фразы*](https://github.com/gasyoun/SanskritGrammar/tree/main/KnauerFrazy_1908) workbook · DCS corpus · Apte "Готовые уроки" (metod/unit) template | ⚪ raw material only; no exercise appendix yet |
| Cross-references | [`LEARNER_MATERIALS.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/LEARNER_MATERIALS.md) learning ladder | 🟢 Zaliznyak *Конспект*/*Очерк*, Knauer, Толчельников Талмуд, Гасунс-2014 already mapped by stage |

**Headline finding already in hand** (the model for the whole booklet): Kochergina
teaches the future stem as one rule `-syá` with `-ṣya/-iṣya` as "варианты", but in DCS the
seṭ form **-iṣya is the majority (56.8 %)** of distinct future forms — every surface fact
is correct, yet the ordering hides the distribution the learner will actually meet
(claims HK-4a/HK-4b). Factually right, pedagogically misleading: exactly the commentary
this методичка exists to add. The H768 sweep already found **12 more such cases** (11
OVERSTATED + 1 FALSE) plus 16 presentation flags across all 40 Занятия — so the curated-v1
pool is already picked, not still to be discovered.

**Edition caveat to resolve.** The folder is named `_1998`, but
[`LEARNER_MATERIALS.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/LEARNER_MATERIALS.md)
records the digitized copy as the **6-е изд. 2017 (ред. Н. П. Лихушина)**. Which physical
edition the `.mdx` transcribes must be pinned before any errata claims a page/line
(§ P2, @DECIDE K-1).

---

## 3. Source-of-truth model (Decision A — hybrid)

```
  claims.yml ──┐
  errata.yml ──┤
  exercises.yml (new) ──┤──►  build step  ──►  print manuscript (RU)  ──►  PDF booklet
  crossrefs.yml (new) ──┘         ▲                    ▲
                                  │                    └── authored prose sections (.md/.mdx)
                          reading-site overlay (existing KocherginaClaims.jsx etc.)
```

- **Structured (registry-owned):** every falsifiable number, verdict, errata row, exercise
  item + key, and cross-reference target. One canonical copy; the site and the print build
  both read it. Never hand-copy a number into prose — cite the registry field.
- **Authored (prose-owned):** the connective commentary, the pedagogy essays, the
  per-занятие "почему это важно", the introduction and usage notes. Lives as `.md`/`.mdx`.
- **Assembly:** a build step interleaves prose + registry rows into a single print
  manuscript. v1 may assemble by hand; v2 formalizes the assembler
  (`scripts/build_methodichka.py`).

New registries to add (mirroring the `claims.yml`/`errata.yml` shape):
`KocherginaUchebnik_1998/exercises.yml` and `KocherginaUchebnik_1998/crossrefs.yml`, each
with a `scripts/build_*.py` generator wired into `npm run` — **but only if v1 actually
needs them**; a curated v1 may start with a single hand-authored appendix and promote to a
registry once the shape stabilizes (@DECIDE K-2).

---

## 4. The five pillars — v1 scope vs v2 scope

### 4.1 Grammatical accuracy (точность)
- **v1:** the harvest is already done — *select* from the 12 non-TRUE claims (11 OVERSTATED
  + 1 FALSE) + the 16 presentation-flagged ones and promote them into print-ready commentary
  notes. Curation, not discovery. Drop UNTESTABLE claims from print unless the DCS-2026
  import resolves them.
- **v2:** widen to the TRUE-but-worth-noting claims and re-run the harvest against the
  DCS-2026 CoNLL-U import when it lands (may resolve the 3 UNTESTABLE aorist-subtype cases).

### 4.2 Clarity & frequency (ясность, частотность)
- **v1:** for each v1 claim, a one-paragraph "что учащийся встретит на практике" note with
  the DCS number (e.g. the -iṣya 56.8 % badge). This is the booklet's signature.
- **v2:** frequency badges for every form-class Kochergina teaches.
- **Queued material — MG ruling, виза P3/SG-MO-017, карточка A4 (15-07-2026):** для
  **Занятия 22 (перифрастический перфект, стр. 153)** — корпусная дистрибуция
  вспомогательных из 4 046 перифрастических перфектов DCS: **as (`āsa`/`āsuḥ`) 91,4 % ·
  kṛ (`cakāra`) 7,4 % · bhū (`babhūva`) 0,8 %**; лицо × число — почти исключительно
  нарративное 3 sg (86,6 %); основы — каузативы/деноминативы на `-ay` (`tāḍayām āsa`,
  `darśayām āsa`). Числа воспроизводимы из
  [periphrastic_perfect.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/perfect/data/periphrastic_perfect.csv)
  (статья [SG-MO-017](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/perfect/index.mdx) § 3.4);
  в печать — частотным бейджем «что учащийся встретит», как -iṣya 56,8 %.

### 4.3 Errata (опечатки, per edition — Decision C)
- **v1:** populate `errata.yml` from whatever is available now (the digitized text;
  MG-supplied loose corrections). Schema already carries `fixed_in`; extend the entry shape
  with an **`edition`** field so 2024 vs 2025 typos are distinguishable.
- **v2:** when MG supplies 2024 + 2025 scans → `build_errata.py diff` edition-to-edition
  pass → per-edition typo column ("2024 has more, 2025 fewer").
- **Hard dependency:** this is the only pillar gated on external input (the scans). It must
  never block the other four.

### 4.4 Extra exercises (упражнения — Decision D, both)
- **v1:** a small appendix — (a) 1–2 **corpus-sourced** reading passages per covered
  занятие, drawn from the 3 213 in-repo sentences / Knauer *Фразы* / DCS, each attested and
  cited; plus (b) a handful of **authored graded drills** (decline-this, fill-in,
  translate) matched to the занятие's grammar, **with an answer key**, human-visaed.
- **v2:** full per-занятие exercise sets; promote to `exercises.yml` if the appendix proves
  the shape.
- **Reuse note:** the Apte "Готовые уроки" `Урок N-metod.mdx` / `Урок N-unit.mdx` split is
  the existing in-repo template for a lesson-with-exercises unit — follow it, don't invent.

### 4.5 Cross-references (отсылки к рус. работам)
- **v1:** turn the [`LEARNER_MATERIALS.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/LEARNER_MATERIALS.md)
  ladder into per-topic "см. также" pointers — for each v1 занятие, where the same material
  is treated in Зализняк *Конспект*/*Очерк*, Кнауэр *Фразы*, the Талмуд, Гасунс-2014. The
  [shared-sentence concordance](https://github.com/gasyoun/SanskritGrammar/tree/main/Concordance)
  already links Kochergina ↔ Knauer ↔ Bühler sentences — reuse it.
- **v2:** a full topic-crosswalk table across all Russian companions.

---

## 5. Roadmap phases

| Phase | Deliverable | Home | Handoff |
|---|---|---|---|
| **P0** | This spec + metadoc; confirm the hybrid model; pin the digitized edition (K-1) | `KocherginaUchebnik_1998/` | H807 (this) |
| **P1** | v1 accuracy + clarity/frequency commentary (curated) | `claims.yml` + authored prose | H807 |
| **P2** | v1 errata seed + `edition` field | `errata.yml` | H807 |
| **P3** | v1 exercise appendix (corpus reading + authored drills + key) | appendix `.md` (→ `exercises.yml` if needed) | H807 |
| **P4** | v1 cross-reference "см. также" pointers | authored prose, reusing the concordance | H807 |
| **P5** | Print assembly (RU manuscript → PDF) + MG viza | `book-press-prep` / manual | follow-on H### |
| **v2** | Comprehensive commentary over all 43 claims / ~40 занятия; formal assembler; edition-diff errata; DCS-2026 re-run | registries | follow-on H### (built on the H768 harvest) |

**v1 = P0–P4** in the H807 handoff. **P5 (print) and v2 (comprehensive)** are follow-on
handoffs minted when v1 content is visaed.

---

## 6. Rights (do not skip)

Kochergina 1998 is in copyright. The reading-site publish override (06-07-2026) covers the
text on the Pages site **only**; it does **not** authorize a DOI/Zenodo release of the
sentence text, nor printing Kochergina's own text in the booklet. The методичка prints
*our* commentary/exercises/errata and quotes Kochergina only to the minimal extent a
commentary requires. Run [`/publish-safety-check`](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md)
before anything from this becomes public or goes to a printer.

---

## 7. Open questions (@DECIDE)

- **K-1 — which physical edition does the `.mdx` transcribe?** Folder says 1998;
  LEARNER_MATERIALS says 2017 6th ed. (Лихушина). Pin it before any errata cites a
  page/line. *Blocks precise errata, not v1 commentary.*
- **K-2 — registries now or later for exercises/cross-refs?** Start hand-authored and
  promote to `exercises.yml`/`crossrefs.yml` once the shape stabilizes, or build the
  registries up front? Recommendation: hand-author v1, promote in v2.
- **K-3 — booklet's own front matter:** title, target editions named on the cover,
  ISBN/print channel. MG call at P5.

---

## 8. Cross-references

- Reading-site overlay this shares data with: [`CLAIMS_OVERLAY.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/CLAIMS_OVERLAY.mdx)
- The learning ladder the cross-refs draw on: [`LEARNER_MATERIALS.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/LEARNER_MATERIALS.md)
- Repo research agenda (sibling planning doc): [`docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md)
- Print-prep precedent (GasunsDhatu 2026 edition): [`GasunsDhatu_2014/revision-2026/`](https://github.com/gasyoun/SanskritGrammar/tree/main/GasunsDhatu_2014/revision-2026)

_Dr. Mārcis Gasūns_
