# Methodichka — a printed companion-commentary to Apte, *The Student's Guide to Sanskrit Composition*

_Created: 31-08-2026 · Last updated: 31-08-2026_

The roadmap for a **thin printed companion booklet** (методичка) to V. S. Apte's *The
Student's Guide to Sanskrit Composition* (1885; рус. пер. Н. П. Лихушиной, 2021) —
calibration commentary on the syntax rules, corpus frequency bands, cross-references
outward, and exercises drawn from the book itself. This plan is the durable spec; each
execution slice is a separate `H###` handoff. The line follows the
[five-artifact convention](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/CONVENTION_METODICHKA_ARTIFACT_SHAPE_2026.md),
with the Kochergina line
([METODICHKA_KOCHERGINA_COMPANION_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md))
as the reference implementation. Unlike Kochergina's, this companion is written
*after* two of its sections shipped — it records the shape those slices established
and plans what remains.

Companion metadoc (how to improve this plan, backlog, revision history):
[`METODICHKA_APTE_COMPANION_2026.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_COMPANION_2026.meta.md).

---

## 0. What this is (and is not)

A **нетолстое печатное издание** — a slim, print-first companion the learner keeps open
beside Apte/Лихушина. It does **not** reprint Likhushina's translation wholesale (in
copyright); it overlays *our* commentary, corpus numbers, cross-references and exercise
apparatus. The same structured data (claims registry, corpus layer TSV) also feeds the
site, so print and web never diverge.

**Audience & register:** Russian-speaking learners of Sanskrit *syntax* — the book is the
first syntactic manual in the verification pipeline (the other four lines are
morphological). Prose in Russian, «е» not «ё», IAST alongside Devanāgarī, corpus numbers
from DCS.

**Author of record:** Dr. Mārcis Gasūns. Every grammatical verdict and exercise key is
human-visaed before print.

## 1. Decisions locked

| # | Fork | Ruling |
|---|---|---|
| A | Source-of-truth model | **Hybrid, inherited from the Kochergina line** (its Decision A): numbers and verdicts live in [claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/claims.yml) (APT-1..40) and [corpus_layer/](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885/corpus_layer); connective commentary is authored prose. |
| B | Quoting the Likhushina translation | **Maximal, not minimal** — MG visa 17-07-2026 (карточка razdel-1-frame): «нужно использовать максимально, есть разрешение». Rule formulations are quoted verbatim in раздел I; the legal frame at the foot of each manuscript stays. |
| C | Exercise sourcing | **Drawn, never invented** (convention rule 1): every reading and translation task comes from Apte's own §§ and exercise blocks, cited by §. Contrast Kochergina Decision D, which allowed authored drills — a syntax manual supplies its own sentences. |
| D | Раздел numbering | I комментарий · II корпусный слой · III отсылки · IV упражнения. Diverges from Kochergina (her II = упражнения) because the corpus layer shipped second here (H1297) and its files already say «раздел II»; renumbering shipped, visaed manuscripts was not worth the symmetry. |

## 2. Prior art — what already exists (consume, do not rebuild)

| Pillar | Asset (source → generated) | State |
|---|---|---|
| Grammatical accuracy / calibration | [claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/claims.yml) → [CLAIMS_VERIFIED.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/CLAIMS_VERIFIED.md) | 🟢 **40 claims** (29 TRUE · 8 OVERSTATED · 1 FALSE · APT-30 narrowed · APT-40 pada layer), reproduced by three instruments ([apte_treebank_stats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_treebank_stats.py) · [apte_classical_government_stats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_classical_government_stats.py) · [apte_pada_stats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_pada_stats.py) + [apte_pada_preverb_stats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/apte_pada_preverb_stats.py)) |
| Раздел I — комментарий | [METODICHKA_APTE_KOMMENTARII_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_KOMMENTARII_2026.md) | 🟢 authored (H1090), MG-visaed 17-07-2026, visa edits applied (H1275/H1373/H1615/H3113); zan-29 closed by data 18-08-2026 |
| Раздел II — корпусный слой | [METODICHKA_APTE_CORPUS_LAYER_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_CORPUS_LAYER_2026.md) ← [corpus_layer/corpus_layer.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/corpus_layer/corpus_layer.tsv) | 🟢 authored (H1297): 34 lemmas over 7 sections, bands from kosha `lemma_frequency.tsv`, pinned by [tests/test_corpus_layer.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_corpus_layer.py); RU renderings await viza |
| Раздел III — отсылки | [METODICHKA_APTE_V1_OTSYLKI_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_V1_OTSYLKI_2026.md) | 🟢 authored (H3739): AP90 s.v. links (SLP1, all keys verified live), Шерцль pages, Whitney §§, Елизаренкова-2004, Kochergina parallels |
| Раздел IV — упражнения | [METODICHKA_APTE_V1_UPRAZHNENIIA_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_V1_UPRAZHNENIIA_2026.md) | 🟢 authored (H3739): readings, разборы and translation tasks for 7 занятий, every item drawn from Apte's own lessons with §; keys ⟦MG-viza⟧ |
| Errata (per edition) | [errata.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/errata.yml) → [ERRATA.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/ERRATA.mdx) | 🟡 system built, list deliberately empty — awaits a printed corrections sheet or an edition diff; never blocks the other pillars |

**Headline finding already in hand** (the model for the whole booklet): Apte's asymmetry —
> where the book says what a word MEANS it is reliable (all eight particle glosses TRUE);
> it errs in DISTRIBUTION, GOVERNMENT and ASPECT (APT-18/19/21 overstated, APT-31 false).

The verified-claims registry means the curated pool for print is already picked, not still
to be discovered — the same position the Kochergina plan reached after its H797 drain.

## 3. Source-of-truth model (Decision A — hybrid)

```
  claims.yml (APT-1..40) ──┐
  corpus_layer.tsv ────────┤──► build/assembly ──► print manuscript (RU) ──► PDF booklet
  errata.yml (empty) ──────┘        ▲                    ▲
                                    │                    └── authored prose: разделы I, III, IV
                            site overlay (CLAIMS_OVERLAY.mdx, dashboards)
```

- **Structured (registry-owned):** every verdict, corpus number, frequency band, errata
  row. One canonical copy; site and print both read it. Prose cites registry ids (APT-…),
  never hand-copies numbers.
- **Authored (prose-owned):** разделы I, III, IV — commentary, cross-references, exercise
  apparatus. Live as `.md` beside the registries.
- **Assembly:** v1 assembles by hand; a formal `build_methodichka.py` is deferred until
  the Kochergina line builds one (shared infra, one implementation for both lines).

## 4. The pillars — v1 scope vs v2 scope

### 4.1 Calibration commentary (раздел I)
- **v1:** done — the 12 flagged places (8 OVERSTATED + 1 FALSE + uta + krīḍ + the pada
  rules) with corpus numbers, visaed.
- **v2:** widen to TRUE-but-worth-noting claims; re-run against DCS-2026 when the corpus
  imports land; the cross-book calibration list (виза, prilozhenie) — separate handoff.

### 4.2 Corpus layer (раздел II)
- **v1:** done — 34 lemmas, bands + attested examples with fresh RU renderings.
- **v2:** extend to every lemma the print manuscript ends up naming.

### 4.3 Cross-references (раздел III)
- **v1:** done — dictionary (AP90 s.v., live getword links), Шерцль government lexicon,
  Whitney §§, Елизаренкова-2004, Kochergina-line parallels.
- **v2:** per-topic crosswalk into the Russian manuals ladder (Очерк/Конспект/Талмуд)
  once their syntax coverage is registered the way morphology already is.

### 4.4 Exercises (раздел IV)
- **v1:** done — readings, разборы and translation tasks for the 7 commented занятия,
  all drawn from Apte's own lessons (Decision C), keys ⟦MG-viza⟧.
- **v2:** widen to uncommented lessons if the booklet's scope grows; keys visaed at P5.

### 4.5 Errata
- **v1:** system in place, honestly empty.
- **v2:** populate when MG supplies a corrections source; per-edition diff if a second
  printing is digitized. The only externally-gated pillar; never blocks the rest.

## 5. Roadmap phases

| Phase | Deliverable | Home | Handoff |
|---|---|---|---|
| **P0** | Claims registry + instruments (39 → 40 claims) | `claims.yml` + `apte_*_stats.py` | H1055/H1059/H1062/H1081/H1084/H1087, H3113 |
| **P1** | Раздел I — комментарий, visa applied | authored prose | H1090, H1275/H1373/H1615 |
| **P2** | Раздел II — корпусный слой | `corpus_layer/` + prose | H1297 |
| **P3** | Разделы III–IV + this companion + metadoc (five-artifact parity) | authored prose | [H3739](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3739-Fable_SanskritGrammar_metodichka-apte-five-artifact-parity_30.08.26.md) |
| **P4** | Viza of раздел III/IV keys and renderings | review sheet | follow-on H### |
| **P5** | Print assembly (RU manuscript → PDF) + MG viza | shared with Kochergina P5 | follow-on H### |

**P0–P3 EXECUTED as of 31-08-2026.** P4 (viza) gates print, not further authoring.

## 6. Rights (do not skip)

Apte's English text (1885) is in the public domain; the Russian translation by
N. P. Likhushina (2021) is in copyright. The MG visa of 17-07-2026 (razdel-1-frame)
grants permission to quote the translation maximally **in this commentary apparatus**;
the manuscripts still bind quotation to the rule being commented (see the legal frame in
[раздел I](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/METODICHKA_APTE_KOMMENTARII_2026.md)).
The Шерцль/Елизаренкова scans stay outside git (порядок H552). Run
[/publish-safety-check](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md)
before anything from this goes to a printer or a public page.

## 7. Open questions (@DECIDE)

- **A-1 — viza scope for разделы III–IV:** one review sheet over the ⟦MG-viza⟧ items
  (translations + keys), or fold into the P5 print viza? Recommendation: one sheet at P4,
  so print assembly starts from visaed text.
- **A-2 — booklet front matter:** does the Apte методичка print as its own booklet or as
  a section of a combined syntax companion? MG call at P5.
- **A-3 — Кнауэр/Бюлер syntax parallels in раздел III:** the Russian-ladder anchors for
  *syntax* topics (government, particles) are not yet registered the way morphology is;
  v2 item, needs the ladder docs' coverage first.

## 8. Cross-references

- The five-artifact convention + live coverage matrix:
  [docs/CONVENTION_METODICHKA_ARTIFACT_SHAPE_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/CONVENTION_METODICHKA_ARTIFACT_SHAPE_2026.md)
- Reference implementation (Kochergina line):
  [METODICHKA_KOCHERGINA_COMPANION_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md)
- Book folder index: [ApteSyntax_1885/README.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/README.md)
- Site overlay sharing the same data:
  [CLAIMS_OVERLAY.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/CLAIMS_OVERLAY.mdx) ·
  [CLAIMS_STATS_DASHBOARD.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/CLAIMS_STATS_DASHBOARD.md)
- The voted review the apparatus honours:
  [review/sanskritgrammar-metodichka-apte-v1_17.07.26_decisions.json](https://github.com/gasyoun/SanskritGrammar/blob/main/review/sanskritgrammar-metodichka-apte-v1_17.07.26_decisions.json)
  (8 approvals, 1 null — nothing rejected; the null zan-29 card was closed by data, H3113)

_Dr. Mārcis Gasūns_
