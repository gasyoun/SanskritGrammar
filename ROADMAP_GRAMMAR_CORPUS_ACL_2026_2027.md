# Roadmap 2026–2027 — SanskritGrammar as a priority research thread

_Created: 10-07-2026 · Last updated: 10-07-2026_

A one-year plan (Q3 2026 → Q2 2027) turning this repo from a **digitized-reprint archive** into
a **measured comparative corpus of Sanskrit grammatical description**, with two submittable
papers, one citable dataset, and a site that follows [ACL Anthology](https://aclanthology.org/)
publishing practice.

Authored by Opus 4.8 (`claude-opus-4-8`), 10-07-2026, on four decisions taken by a human the
same day: (1) all four analysis spines are in scope; (2) the ACL crosswalk covers research
method, site product, and benchmark packaging, ranked; (3) the repo is **promoted from Tier 2
to a priority research thread** in the standing order of
[`Uprava/GTD_NEXT_ACTIONS.md`](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md);
(4) the research agenda proper is delegated to Fable 5 (`claude-fable-5`) as
[H450](https://github.com/gasyoun/Uprava/blob/main/handoffs/H450-Fable_SanskritGrammar_dh_memo_research_agenda_10.07.26.md).

This file is the **plan**. H450's memo is the **agenda**. Neither is the analysis.

---

## 1. What already exists (ground truth, not a wish list)

Every row below is a committed artifact in this repo. The roadmap builds only on these.

| Asset | Path | Size | What it already is |
|---|---|---:|---|
| Exercise-sentence pool | [`scripts/data/sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json) | 3,213 sentences | Bühler / Knauer / Kochergina, each tagged `book`, `lesson`, `script`, stable id (`buhler-XIV-364`) |
| Shared-sentence catalog | [`scripts/data/catalog.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/catalog.csv) | 124 clusters | 7 in all three books · 79 Bühler↔Knauer · 33 Bühler↔Kochergina · 5 Knauer↔Kochergina |
| **Hand-classified near-matches** | [`scripts/data/matches_review.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/matches_review.tsv) | 128 pairs | Each carries a human `verdict` (`spelling_variant`, …) — **this is already a gold set** |
| Subject-coverage matrix | [`SubjectConcordance/catalog.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/SubjectConcordance/catalog.mdx) | 9 works × 18 chapters + 41 fine categories | Keyword-lexicon first pass, self-described as *"a finding-aid, not an authority"* |
| Morphoclass crosswalk | [`TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv) | 876 roots | `whitney_no`, `root`, `gloss`, `ryad_derived` + `ryad_conf`, `z_series`, `z_set`, `set_derived`, `z_url` |
| Whitney spine | [`WhitneyGrammar_1889/`](https://github.com/gasyoun/SanskritGrammar/tree/main/WhitneyGrammar_1889) | 18 ch · 1,316 § | Generated from [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots), each § linked to Wikisource |
| Phonostatistics | [`GasunsDhatu_2014/revision-2026/`](https://github.com/gasyoun/SanskritGrammar/tree/main/GasunsDhatu_2014/revision-2026) | 6 CSVs | consonant coefficient, RV/Rāmāyaṇa clusters, varga shares, syllables-per-word, + provenance JSON |
| Pāṇini lookup harness | [`GasunsDhatu_2014/revision-2026/panini_sutra.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/panini_sutra.py) | script + `panini_cache/` | Already used to verify 2 sūtra citations in H415 |
| Errata pipeline | 8 × `errata.yml` → [`ERRATA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ERRATA.md) | 1 populated of 8 | [`scripts/build_errata.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_errata.py); Knauer only |
| Site | [gasyoun.github.io/SanskritGrammar](https://gasyoun.github.io/SanskritGrammar/) | 10 books | Docusaurus, auto-registering `bookDirs`, GitHub Pages |

**The headline:** three of the four spines are testable on data already committed. Nothing in
Q3 below requires a new derivation.

---

## 2. The four spines

### S1 — Textbook sequencing corpus (highest leverage, lowest cost)

Bühler, Knauer, Kochergina, Apte are **four independent orderings of the same grammar**, and
Whitney's 1,316 § is a ready-made spine to align them against. Nobody has measured which topics
each defers, which they never reach, or how the Russian and German traditions diverge.

- **Have:** 3,213 sentences with lesson numbers; 124 shared clusters; 128 labeled near-matches.
- **Missing:** a better-than-`difflib` detector; Apte + Whitney sentences; direction of borrowing;
  any difficulty measure.
- **Testable today, no new data:** Kendall's τ over the 79 Bühler↔Knauer and 33 Bühler↔Kochergina
  shared clusters, comparing lesson order. n=79 is enough for a real coefficient.

> ⚠ **The load-bearing caveat.** This repo carries the **1923 Stockholm reprint** of Bühler as a
> text proxy for the **1878 first edition** — and the [Concordance page itself flags](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx)
> that this has *not* been verified against the 1878 print. Knauer is **1908**, i.e. *earlier than
> the reprint we hold*. Any claim of the form "Knauer borrowed from Bühler" is therefore
> **unsound until the 1878 text is checked**: if the exercises were revised between editions, the
> arrow may point the other way. Directionality is gated on `@DO D4` below. Nothing publishable
> about borrowing direction ships before that gate clears.

### S2 — Morphoclass disagreement study

Three classifications of the same verbal roots — Zaliznyak 1975, Gasūns 2014, Tolchelnikov 2026 —
already crosswalked over 876 roots on Whitney root numbers, with the lineage argued in
[`MORPHOCLASS_3WAY_MEMO.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.md).

- **Have:** the crosswalk, per-row confidence (`ryad_conf`), the `/z/` root map.
- **Missing:** a join to corpus frequency (Whitney-no ↔ DCS lemma ↔ Vidyut dhātu), and a decision
  procedure for *which scheme the data prefers*.
- **The contribution is the framing.** Verified this session: **no ACL/CL paper adjudicates two or
  more pre-existing expert classifications of the same lemma set against corpus evidence.** Every
  precedent predicts or induces *one* classification. That gap is the paper.

### S3 — Pāṇini ↔ Western grammar alignment (moonshot, gated)

Map Whitney's descriptive statements to Aṣṭādhyāyī sūtras; measure what each tradition says that
the other cannot.

- **Have:** a working sūtra-lookup harness + cache; Whitney's § structure.
- **Missing:** everything else. Whitney has 1,316 §; the Aṣṭādhyāyī ~4,000 sūtras.
- **Verified gap:** no ACL paper aligns Western descriptive grammar statements to Pāṇinian sūtra
  IDs. Net-new — and correspondingly risky. Scoped as a **two-chapter pilot** (ch. III sandhi
  §§98–260; ch. XI aorist §§824–930) with a hard kill-gate, not a year-long commitment.

### S4 — Phonostatistics / style forensics (fold in, do not paper)

The existing varga-share work already produced its answer: **Cramér's V = 0.037** — essentially no
association. That is a legitimate negative result, and it belongs in the Dhātu monograph where it
already sits, not in a separate paper. Verified this session: **no ACL precedent** for varga-share
stylometry; the natural venue would be DSH/CHR, not ACL. **Lowest priority — no separate track.**

---

## 3. What aclanthology.org teaches — three angles, ranked

Every citation below was fetched and verified this session. Nothing is recalled from memory.
Where there is no precedent, this says so.

### Angle A — Research method (rank 1: this is where the value is)

| Method to adopt | Precedent (verified) | Applies to | Replaces / upgrades |
|---|---|---|---|
| **Kendall's τ for order comparison** | Lapata 2006, *Computational Linguistics* — [J06-4002](https://aclanthology.org/J06-4002/) | S1: lesson-order divergence across textbooks | nothing — net-new measurement |
| **Topological sort → consensus order** | Prabhumoye et al. 2020, ACL — [2020.acl-main.248](https://aclanthology.org/2020.acl-main.248/) | S1: reconstruct a canonical curriculum from pairwise evidence | nothing |
| **RefD, unsupervised asymmetric prerequisite metric** | Liang et al. 2015, EMNLP — [D15-1193](https://aclanthology.org/D15-1193/) | S1: directionality **without training labels** | the missing directionality signal |
| **TRACER text-reuse, validated *on Sanskrit*** | Miyagawa et al. 2024, NLP4DH — [2024.nlp4dh-1.12](https://aclanthology.org/2024.nlp4dh-1.12/) | S1: cluster detection; their finding that *smaller chunk sizes raise recall* is a directly reusable knob | `difflib.SequenceMatcher` |
| **Passim** (OCR-robust fuzzy alignment) | not an ACL paper — [Programming Historian lesson](https://programminghistorian.org/en/lessons/detecting-text-reuse-with-passim) | S1: same, at scale | same |
| **κ / α as agreement between *schemes*** | Artstein & Poesio 2008, *Computational Linguistics* — [J08-4004](https://aclanthology.org/J08-4004/) | S2: treat the three classifications as three "coders"; S1: gold-sample sizing | the unmeasured `ryad_conf` column |
| **Mutual information: does form/meaning predict class?** | Williams et al. 2020, ACL — [2020.acl-main.597](https://aclanthology.org/2020.acl-main.597/) | S2: run all three schemes through one estimator, compare predictiveness | the adjudication method |
| **Inflection-class complexity via entropy** | Cotterell et al. 2019, *TACL* — [tacl_a_00271](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00271/43492/) | S2: complexity of each rival scheme | — |
| **MDL induction of inflection classes** | Beniamine & Bonami — [Wiley chapter](https://onlinelibrary.wiley.com/doi/10.1002/9781119693604.morphcom038) (not ACL) | S2: score rival systems by description length | — |
| **vidyut-prakriya (MIT): sūtra-provenanced derivation** | Prasad 2024, ISCLS — [2024.iscls-1.7](https://aclanthology.org/2024.iscls-1.7/) · [github](https://github.com/ambuda-org/vidyut) | S2 surface forms; S3 sūtra IDs | hand-derivation |
| **Sanskrit segmentation / DCS spine** | Hellwig & Nehrdich 2018, EMNLP — [D18-1295](https://aclanthology.org/D18-1295/); ByT5-Sanskrit 2024 — [2024.findings-emnlp.805](https://aclanthology.org/2024.findings-emnlp.805/) | S2 corpus counts | — |
| **Difficulty progression (methodology only, English-trained)** | Arase et al. 2022, EMNLP — [2022.emnlp-main.416](https://aclanthology.org/2022.emnlp-main.416/) | S1: do exercises get harder? do books agree? | — |

**Honest non-findings** (do not cite what does not exist):
- **Directionality of borrowing between printed books has weak ACL precedent.** The single anchor
  is Hoenen 2015, NAACL — [N15-1127](https://aclanthology.org/N15-1127/) (archetype reconstruction).
  Mature stemmatic/CBGM machinery lives in DSH, not ACL. Say so in the paper.
- No ACL paper adjudicates **rival** classifications of the same lemmas (S2's framing is new).
- No ACL paper aligns Western grammar statements to **sūtra IDs** (S3 is new).
- No ACL paper treats **seṭ/aniṭ or ablaut** as a corpus-adjudicated classification target.
- A **SIGMORPHON Sanskrit track** could not be verified — do not assume one exists.

**Adopt first:** τ (Lapata) + κ (Artstein & Poesio). Both run on committed data, this quarter,
with no new derivation, and both convert an existing hand-wave into a number.

### Angle B — Site as product (rank 2: cheap, compounding)

The Anthology's [corrections policy](https://aclanthology.org/info/corrections/) is the single
best thing to copy, because this repo already has the raw material (8 `errata.yml`) and none of
the discipline. Its model is **append-only**: originals immutable; corrections are new *versioned*
artifacts; three tiers — **erratum** (note read alongside), **revision** (replacement, id gains
`v2`), **retraction** (watermark + notice, never deleted); each a structured element with `id`,
`date`, `checksum`, and a neutral change summary. Verified live on
[2023.acl-long.594](https://aclanthology.org/2023.acl-long.594/), which serves both `v1` and `v2`.

| # | Feature | Effort | Note |
|---|---|:--:|---|
| B1 | **Three-tier versioned errata schema** (erratum / revision / retraction + `date` + `checksum`) | M | Generalizes [`build_errata.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_errata.py). **Do this first.** |
| B2 | **Stable per-item ID grammar** — `buhler-1923.XIV.10`, mirroring `YEAR.VENUE-VOLUME.NUMBER` ([policy](https://aclanthology.org/info/ids/)) | S | `sentences.json` ids are already 90% there |
| B3 | **Per-page BibTeX + bulk `all.bib`** ([Anthology does both](https://aclanthology.org/faq/)) | S | Makes 10 books citable at once |
| B4 | **Multi-representation URLs** — `/{id}`, `/{id}.bib`, `/{id}.json` | S | One ID, many representations |
| B5 | **Site search via Google Programmable Search** — [what the Anthology actually uses](https://github.com/acl-org/acl-anthology/tree/master/google-cse) | S | No backend |
| B6 | **`people.yaml` with name-variant map** ([author-page policy](https://aclanthology.org/info/author-pages/)) | M | General-purpose author-identity feature, independent of D2 (below) |
| B7 | Checksums on every source `.doc`/`.docx` | M | Fixity for digitized editions |
| B8 | DOI per book/edition via Zenodo, embedding the local ID | L | Pairs with [`/cut-release`](https://github.com/gasyoun/claude-config/blob/main/commands/cut-release.md) |

> **B6 raised, then narrowed — the premise it rested on turned out false.** This section
> originally argued the rename sweep should be *cancelled* in favor of a `people.yaml`
> name-variant map, on the theory that "Zaliznyak" was the historically-printed citation
> spelling and the rename would overwrite it. [H449](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H449-Sonnet_SanskritGrammar_zaliznyak-zalizniak-rename-sweep_10.07.26.md)
> checked that premise against the actual evidence before proceeding: Tolchelnikov's own
> published paper ([`Auroville_Feb2024/A NonPaninian Approach...mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/Auroville_Feb2024/A%20NonPaninian%20Approach%20to%20Sanskrit%20Morphonology%20%28article%29.mdx))
> already cites "Andrei **Zalizniak**. 1975." (i-spelling) in its own References section — so
> `Zalizniak`, not `Zaliznyak`, is the real citation convention already in scholarly use here.
> The rename ([SanskritGrammar PR #78](https://github.com/gasyoun/SanskritGrammar/pull/78) +
> [RuWritingStyles PR #70](https://github.com/gasyoun/RuWritingStyles/pull/70), both merged
> 10-07-2026) proceeded on that basis. **D2 closed — see the decisions table below.** B6
> itself (a general author-identity feature for name variants across the whole corpus, not
> specific to this one spelling question) remains a legitimate, independent backlog item if
> wanted later — it just no longer blocks or reverses this rename.

### Angle C — Benchmark packaging (rank 3: the payoff of A + B)

ACL shared tasks package as: a GitHub repo per task-year, frozen splits sharing no items, a fixed
format, baseline + eval script, and an overview paper — e.g.
[sigmorphon/2023InflectionST](https://github.com/sigmorphon/2023InflectionST) and
[2021Task0](https://github.com/sigmorphon/2021Task0). Leaderboards are usually informal.

Applied here, the obvious release is a **Sanskrit grammar-description benchmark**: the shared-sentence
concordance + the subject-coverage matrix + the 876-root crosswalk, each with a **frozen gold sample**
and a published κ. Ships through [`/data-release`](https://github.com/gasyoun/claude-config/blob/main/commands/data-release.md),
registered in [`kosha/data/manifest/datasets.json`](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json).

---

## 4. The year

Full-throttle sizing, per the human decision to promote this repo. Each quarter ends in a
shippable artifact, and each depends only on the one before it.

### Q3 2026 (Jul–Sep) — Measure what is already committed

No new derivations. Convert three existing hand-waves into numbers.

| # | Item | Data | Method | Output |
|---|---|---|---|---|
| Q3.1 | **H450 research agenda** (Fable 5) | — | [`/dh-memo`](https://github.com/gasyoun/claude-config/blob/main/commands/dh-memo.md) | `docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md` |
| Q3.2 | **Lesson-order divergence** | 79 + 33 shared clusters | Kendall's τ ([J06-4002](https://aclanthology.org/J06-4002/)) | first real result; τ per book pair |
| Q3.3 | **Score the coverage matrix** | freeze 150 (chapter × work) cells | 2 annotators → Fleiss κ → P/R/F1 of the keyword lexicon ([J08-4004](https://aclanthology.org/J08-4004/)) | turns *"finding-aid, not an authority"* into a measured number |
| Q3.4 | **Three-scheme agreement** | 876-root crosswalk | Fleiss κ / Krippendorff α over Zal./Gas./Tol. as three coders | where the three actually disagree, quantified |
| Q3.5 | **Errata schema B1 + IDs B2** | 8 `errata.yml` | [ACL corrections model](https://aclanthology.org/info/corrections/) | site v1 |

**Gate:** Q3.3 needs a second annotator. Per [[feedback-second-annotator-deferred]] no candidate
exists and recruitment is parked for 2026 — so Q3.3 runs as **single-annotator + adjudicated
re-pass** (report as such, no κ claimed) unless `@DECIDE D5` says otherwise. Do not silently
report a κ computed by one person.

### Q4 2026 (Oct–Dec) — Replace naive detectors; build the joins

| # | Item | Note |
|---|---|---|
| Q4.1 | **Evaluate `difflib` against the 128 labeled pairs** | [`matches_review.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/matches_review.tsv) is already a gold set — use it before replacing anything |
| Q4.2 | **Swap in TRACER / Passim**, tune chunk size per [2024.nlp4dh-1.12](https://aclanthology.org/2024.nlp4dh-1.12/) | report Δ recall vs the 124-cluster baseline |
| Q4.3 | Extend extraction to **Apte + Whitney** examples | 5 books on the spine, not 3 |
| Q4.4 | **Whitney-no ↔ DCS lemma ↔ Vidyut dhātu crosswalk** | net-new derived asset; corpus counts belong to [VisualDCS](https://github.com/gasyoun/VisualDCS) — **boundary: consume, do not re-derive**. Register in [`PROJECT_INTERLINKS.md`](https://github.com/gasyoun/Uprava/blob/main/PROJECT_INTERLINKS.md) + the kosha manifest |
| Q4.5 | **RefD directionality** ([D15-1193](https://aclanthology.org/D15-1193/)) | ⚠ **blocked on `@DO D4`** (1878 Bühler). Run the metric, publish no arrow until the gate clears |

### Q1 2027 (Jan–Mar) — Two papers

- **Paper 1 (resource/DH).** *Four grammars, one spine: measuring textbook sequencing and exercise
  reuse in the Sanskrit teaching tradition.* Venue candidates: [NLP4DH](https://aclanthology.org/venues/nlp4dh/)
  (published the Sanskrit TRACER paper), LaTeCH-CLfL, or CHR. → `@DECIDE D1`.
- **Paper 2 (method).** *Does the corpus prefer a classification? Adjudicating three
  morphophonological schemes for Sanskrit verbal roots.* Venue: WSC / ISCLS or SIGMORPHON.
  Contribution = the adjudication framing, which has no precedent.
- Site: **B3 + B8** (bulk `all.bib`, DOIs).
- Register both in [`Uprava/ARTICLES.md`](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md)
  the moment a skeleton exists (readiness 2), via [`/articles-update`](https://github.com/gasyoun/claude-config/blob/main/commands/articles-update.md).
  They are **not** registered today — a roadmap line is not a draft, and ARTICLES is an inventory
  of papers that exist.

### Q2 2027 (Apr–Jun) — Pāṇini pilot + submission

- **S3 pilot, hard-gated.** Two Whitney chapters (III sandhi §§98–260; XI aorist §§824–930).
  Retrieve sūtra candidates via [vidyut-prakriya](https://github.com/ambuda-org/vidyut) (MIT,
  emits sūtra provenance) + a machine-readable Aṣṭādhyāyī; adjudicate against a **frozen gold
  sample** with reported agreement.
  **Kill-gate:** if retrieval precision@5 on the sandhi chapter is below 0.4 after tuning, stop and
  write the negative result. Do not extend to 18 chapters on hope.
- Submit Papers 1 and 2. Package the benchmark (Angle C) via `/data-release`.

---

## 5. Risks, gates, and what a human must decide

**Risks.**
1. **The 1878/1923 Bühler proxy** (§2, S1) invalidates any borrowing-direction claim until
   resolved. Highest-severity risk in the plan; it sits under the most attractive result.
2. **Zipfian sparsity.** 876 roots against DCS frequencies means many roots are too rare for
   stable per-root MI/entropy estimates. Requires explicit rare-root back-off and confidence
   intervals — report CIs, not point κ.
3. **Tier promotion is a real cost.** Priority research time is finite and currently owed to
   [`RussianTranslation`](https://github.com/gasyoun/SanskritLexicography) and
   [`kosha`](https://github.com/gasyoun/kosha). Promotion is a reallocation, not a free addition.
4. **S3 may simply fail.** Hence the kill-gate. A negative result is publishable; an unbounded
   alignment project is not.

**Open decisions** (mirrored to [`Uprava/GTD_NEXT_ACTIONS.md`](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md)):

| ID | Context | Question |
|---|---|---|
| D1 | `@DECIDE` | Venue for Paper 1 — NLP4DH, LaTeCH-CLfL, or CHR? |
| ~~D2~~ | ✅ **Closed 10-07-2026** | ~~Adopt the Anthology name-variant model (B6) and cancel the `Zaliznyak`→`Zalizniak` rename sweep?~~ Resolved by evidence, not preference: Tolchelnikov's own published paper already cites "Andrei Zalizniak. 1975." (i-spelling), so that IS the real citation convention in use — the premise behind cancelling the rename was false. Rename proceeded ([SanskritGrammar PR #78](https://github.com/gasyoun/SanskritGrammar/pull/78) + [RuWritingStyles PR #70](https://github.com/gasyoun/RuWritingStyles/pull/70), merged). See B6 note above for detail. |
| D3 | `@DECIDE` | Formalize the Tier-2 → priority-research promotion in the standing tier order, and name what it displaces. |
| D4 | `@DO` | Obtain / verify the **1878 Bühler first edition** exercises. Gates all directionality work (Q4.5). |
| D5 | `@DECIDE` | Q3.3 with one annotator (no κ) or wait for a second? Standing guidance says no candidate exists. |

---

## 6. Next action

The agenda that turns this plan into numbered hypotheses and viz specs:

```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H450-Fable_SanskritGrammar_dh_memo_research_agenda_10.07.26.md and execute it.
```

Executor: Fable 5 (`claude-fable-5`); `cd` into `GitHub/SanskritGrammar`. Memo-only — H450 builds nothing.

_Dr. Mārcis Gasūns_
