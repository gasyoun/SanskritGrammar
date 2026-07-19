# SanskritGrammar portfolio roadmap — 2026–2027

_Created: 10-07-2026 · Last updated: 19-07-2026_

> _Revision 19-07-2026 ([H1277](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1277-Fable_SanskritGrammar_sangram-acl-roadmap-rebase-primary_18.07.26.md), Fable 5 `claude-fable-5`): executed the 18-07-2026 **keep-both ruling** — Sangram is the product of record for the corpus-grammar line; Track C's two ACL papers are its **publication arm**, and the former "four spines" S1–S4 are demoted to **instruments** that feed Sangram (labels kept for link stability). Measured basis, 19-07-2026 against `origin/main`: `sangram/` accounts for 204 of 596 files touched since 14-07-2026 — **34.2 %, the single largest stream of work in the repo, 3.2× the next bucket** (`scripts/`, 64). The S1 τ result is already consumed as evidence by three Sangram programme docs; the agreement-metric method of the S2 paper is already practised inside `sangram/articles/tatpurusha/` — the papers productionise analyses that exist as one-offs. The portfolio order below (M03 first) is untouched: "Sangram primary" ranks Sangram over its instruments, not over the monograph._

This is the repository's **authoritative portfolio-ordering document**. It says which result
comes first and how the five active tracks share capacity. It does not duplicate their detailed
methods: the monograph, Sangram, digital pedagogy, archive/site, and comparative research retain
their own sources of truth, linked below.

The portfolio outcome for 2026–2027 is: finish the **M03 GasunsDhatu monograph** for publisher
preparation; turn Sangram's high-velocity candidate corpus into a verified publication set;
launch the already-built RQ4 learner evaluation; keep the comparative research programme moving
as **Sangram's publication arm**; and maintain the public grammar archive without opening a new
rights programme this cycle.

---

## 0. Portfolio order and authority

| Order | Track | Current state | Authoritative detail | Cadence ruling |
|---:|---|---|---|---|
| **1** | **M — M03 GasunsDhatu monograph** | Complete author-visaed draft; the remaining bottleneck is the 1,127-finding RWS line edit, then two mechanical pre-submission passes | [`GasunsDhatu_2014/revision-2026/BOOK_PLAN.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/BOOK_PLAN.md) and the [press-readiness checklist](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/NESTOR_ISTORIA_M03_PRESS_READINESS_CHECKLIST.md) | Highest-labelled priority; hybrid agent/human line edit; manuscript freeze **31-10-2026**; contact «Нестор-История» in **November 2026** |
| **2** | **S — Sangram corpus grammar** | 35 article manifests: 9 published, 26 candidates; the 18-07 adversarial re-derivation found 3 refuted numerical claims, 2 fixed and 1 routed to a draft fix | [`sangram/SANGRAM_CHARTER_2026_2031.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CHARTER_2026_2031.mdx) and the [DCS-derived-number ledger](https://github.com/gasyoun/SanskritGrammar/blob/main/DCS_DERIVED_NUMBERS_LEDGER_2026.md) | **Consolidation freeze:** no new topic/article manifests until all 26 baseline candidates reach a documented published, revised, rejected, or kill-gated disposition |
| **3** | **P — Digital Sanskrit pedagogy / RQ4** | Protocol, consent, item bank, and Systema harness complete | [`docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md) and [`docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md) | **GO now:** activate the existing RQ4 feature and recruit exactly under the approved protocol |
| **4** | **C — Comparative corpus / papers, the publication arm of Sangram** | S1–S4 are **instruments feeding Sangram** (§2), no longer independent workstreams; the two ACL papers productionise analyses Sangram already consumes or practises; A60/A61 and other already-open paper work continue | This document §§1–4 and [`docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md) | Full cadence continues alongside M03; M03 is the highest-labelled priority, not an exclusivity rule |
| **5** | **A — Archive and reading site** | Public Docusaurus archive and source/concordance pipelines are operational | [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/README.md) | Maintenance and correctness work only; the existing third-party-rights caveat remains, with no new rights audit this cycle |

The specific Sangram freeze overrides the general full-cadence ruling: **full cadence for Sangram
means verification, visa, repair, and disposition of the 26-candidate baseline—not new-topic
production**. Comparative papers, archive maintenance, and other research may continue at full
cadence without waiting for M03.

**How tracks S and C relate (ruling of 18-07-2026, keep both).** Sangram is the product;
Track C is its publication arm. The corpus-grammar line has one factory — 35 article manifests,
the single largest stream of work in the repo (34.2 % of all files touched since 14-07-2026,
measured 19-07-2026) — and the S1–S4 instruments of §2 exist to feed it: their datasets ground
Sangram's numbers, and the two ACL papers of §4 turn analyses Sangram already consumes or
practises into peer-reviewed method statements. Neither track is cancelled in favour of the
other, but where they compete for capacity, the instrument serves the product, not the reverse.

### Portfolio waves

| Wave | Window | Deliverables | What unblocks it |
|---|---|---|---|
| **W1 — establish the gates** | 18-07 → 31-08-2026 | Start M03 hybrid line edit; enforce Sangram's machine-readable freeze ledger; activate and smoke-test RQ4; finish already-open review/QA work | The eight author rulings recorded in §5 |
| **W2 — finish the manuscript** | 01-09 → 31-10-2026 | Complete tracked RWS edit and human sign-off; freeze M03; run final number consistency and ГОСТ bibliography/citation passes; continue Sangram candidate dispositions and comparative research | W1 line-edit packet; no unresolved argument-changing edit at freeze |
| **W3 — publisher and live study** | 01-11 → 31-12-2026 | Contact «Нестор-История»; obtain house requirements and Devanāgarī/IAST confirmation; recruit the approved RQ4 cohort; continue research tracks | Frozen manuscript; verified RQ4 production route |
| **W4 — publication year** | 2027 H1 | Publisher review/typesetting, two reviewers, RQ4 retention results, comparative papers/benchmark, and Sangram reopening only if the 26-candidate baseline is fully dispositioned | Publisher response; completed study window; Sangram consolidation exit criterion |

### Wave-1 execution pointers

- **H1259 — M03 hybrid line edit and freeze**

  Folder: `C:\Users\user\Documents\GitHub\SanskritGrammar` · model: Fable 5 (`claude-fable-5`)

  `Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H1259-Fable_SanskritGrammar_m03-final-hybrid-line-edit-freeze_18.07.26.md and execute it.`

- **H1260 — Sangram consolidation policy and ledger**

  Folder: `C:\Users\user\Documents\GitHub\SanskritGrammar` · model: Sonnet 5 (`claude-sonnet-5`)

  `Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H1260-Sonnet_SanskritGrammar_sangram-consolidation-policy-ledger_18.07.26.md and execute it.`

- **H1261 — RQ4 go-live**

  Folder: `C:\Users\user\Documents\GitHub\Systema-Sanscriticum` · model: Sonnet 5 (`claude-sonnet-5`)

  `Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H1261-Sonnet_Systema-Sanscriticum_rq4-study-go-live_18.07.26.md and execute it.`

The already-minted **H1257** applies the first 11-candidate Sangram visa batch. H1260 must consume
that work as evidence and must not duplicate or overwrite it.

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

## 2. The four instruments

Formerly "the four spines" — four independent comparative workstreams. Demoted by the
18-07-2026 keep-both ruling: S1–S4 are now **instruments that feed Sangram**, the corpus
grammar of record, and each is described below by what it delivers to Sangram. The S1–S4
labels survive unchanged for link stability. None of this adds a Sangram topic or article
manifest — the consolidation freeze (§0, ruling 2) binds this section too.

### S1 — Textbook sequencing corpus (highest leverage, lowest cost)

**Feeds Sangram:** the sequencing evidence base behind Sangram's pedagogical ordering claims.
Its τ result ([`S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md))
is already consumed as evidence by three Sangram programme docs —
[`sangram/SANGRAM_CHARTER_2026_2031.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CHARTER_2026_2031.mdx),
[`sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx),
[`sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx) —
though no Sangram *article* cites it yet. Paper 1 (§4) productionises this instrument.

Bühler, Knauer, Kochergina, Apte are **four independent orderings of the same grammar**, and
Whitney's 1,316 § is a ready-made spine to align them against. Nobody has measured which topics
each defers, which they never reach, or how the Russian and German traditions diverge.

- **Have:** 3,213 sentences with lesson numbers; 124 shared clusters; 128 labeled near-matches.
- **Missing:** a better-than-`difflib` detector; Apte + Whitney sentences; direction of borrowing;
  any difficulty measure.
- **Testable today, no new data:** Kendall's τ over the 79 Bühler↔Knauer and 33 Bühler↔Kochergina
  shared clusters, comparing lesson order. n=79 is enough for a real coefficient.

**S1 sub-thread — corpus fact-check + methodology critique of a textbook (H768, 12-07-2026).**
Beyond *ordering*, each textbook makes *falsifiable assertions* that can be graded against the DCS
corpus + Whitney on two axes — factual truth and pedagogical justification. Piloted on Kochergina
1998: a machine-readable register [`KocherginaUchebnik_1998/claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.yml)
→ generated [`CLAIMS_VERIFIED.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/CLAIMS_VERIFIED.md)
(numbers reproduced by [`verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py))
+ a reading-site overlay. Headline finding: Kochergina's *facts* are accurate (5/7 TRUE) but the
Petersburg-school "single base rule" ordering hides corpus frequency — the future stem is taught
as "-syá по единому правилу" while the seṭ form **-iṣya is the majority outcome (56.8%)**; the real
conditioning is the seṭ/aniṭ lexical class of **S2**. Both `@DECIDE` RULED 12-07-2026 (D-A
generalise; D-B tie-break DCS/Whitney/Talmud). **Cross-grammar since 14-07-2026 (H797 Phase 2,
Fable 5 `claude-fable-5`, [PR #186](https://github.com/gasyoun/SanskritGrammar/pull/186)):** second
register live — [`BuhlerLeitfaden_1923/claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml),
**64 verified** (58 TRUE · 4 OVERSTATED · 1 FALSE · 1 UNTESTABLE · 13 M.G. footnotes) + a
339-candidate backlog from a 404-candidate 6-reader sweep. Two-register finding: the SAME corpus
number (-iṣya 56.8%) grades Kochergina OVERSTATED and Bühler TRUE — **presentation calibration,
not factual accuracy, is the measurable axis on which grammars differ**; Bühler's own failure
modes are rare-before-common ordering (periphrastic future taught before a 14×-more-frequent
simple future) and one corpus-flipped frequency direction (perfect vs imperfect). Remaining:
Knauer, then Zaliznyak (≥50 verified each) + the Bühler backlog drain.

**S1 metalanguage extension — quantifier register + Zaliznyak comparison (H800, 13-07-2026, done).**
A second register grades not the *assertions* but the *quantifiers* — the metalanguage words that
scope a rule (редко / обычно / только / некоторые / могут / всегда): [`quantifiers.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/quantifiers.yml)
per source, auto-proxy anchored/unanchored tagged (`npm run quantifiers`) → [`QUANTIFIER_PROFILE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/QUANTIFIER_PROFILE.md),
over Kochergina 1998 + all three Zaliznyak works ([`GRADATION_METALANGUAGE_KOCHERGINA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/GRADATION_METALANGUAGE_KOCHERGINA.md)
§2а/§4, [PR #151](https://github.com/gasyoun/SanskritGrammar/pull/151)). **Honest negative worth
recording:** the intuitive "Zaliznyak's quantifiers are anchored to a class, Kochergina's hang on
nothing" is **refuted** at the per-quantifier level — hand-verified anchoredness is high and similar
across the three descriptive grammars (~83–88%). The real discriminators are density (a denominator
artifact once the glossary+reader are excluded: ~1.5–2× per grammar-prose line, not 9×) and anchor
**type** (Kochergina anchors on affixes/named forms with **0% §**; the 1975 classification on its
numbered formal calculus, **90%**) — the quantifier-level fingerprint of the Whitney→Zaliznyak→Talmud
describe→abstract→generate line. Apparatus, not a paper (**@DECIDE** anchor window N=8).

**S1 analysis output — "grammar claims the corpus does not confirm" (paper A60, H773, 12-07-2026).**
The `OVERSTATED`/`FALSE` subset of the claim register is itself a corpus-adjudicated finding with no
strong ACL precedent (it fills the documented "no paper treats seṭ/aniṭ as a corpus-adjudicated
target" non-finding). Seeded 12-07-2026 (Opus 4.8 `claude-opus-4-8`, H773 Q0 + HK-4): method,
framing, related-work, and the one verified worked example (future stem) in
[`TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/OUTLINE_grammar-claims-corpus-denies_A60.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/OUTLINE_grammar-claims-corpus-denies_A60.md).
Central table completion is gated on the H768 full harvest + the cross-grammar extension.

> ⚠ **The load-bearing caveat.** This repo carries the **1923 Stockholm reprint** of Bühler as a
> text proxy for the **1878 first edition** — and the [Concordance page itself flags](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx)
> that this has *not* been verified against the 1878 print. Knauer is **1908**, i.e. *earlier than
> the reprint we hold*. Any claim of the form "Knauer borrowed from Bühler" is therefore
> **unsound until the 1878 text is checked**: if the exercises were revised between editions, the
> arrow may point the other way. Directionality is gated on `@DO D4` below. Nothing publishable
> about borrowing direction ships before that gate clears.

### S2 — Morphoclass disagreement study

**Feeds Sangram:** the agreement-metric method this instrument's paper proposes to formalise is
**already practised inside Sangram** —
[`sangram/articles/tatpurusha/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/index.mdx)
reports Cohen κ = 0,929 (n = 120) and κ = 0,720 (n = 93) over two LLM annotator passes on
compound classification, echoed in
[`sangram/articles/compounds-overview/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/compounds-overview/index.mdx).
That is a *different* κ from this instrument's own three-scheme agreement over the 876-root
morphoclass crosswalk (Q3.4), **which has never been run** — Paper 2 (§4) formalises the method
Sangram already uses in practice and delivers the missing S2 number.

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

**Feeds Sangram:** sūtra-provenanced derivations for the apparatus of *existing* Sangram
articles — the pilot's sūtra-lookup harness is already the natural citation backend wherever an
article invokes a Pāṇinian rule. No new article is implied; the freeze binds.

Map Whitney's descriptive statements to Aṣṭādhyāyī sūtras; measure what each tradition says that
the other cannot.

- **Have:** a working sūtra-lookup harness + cache; Whitney's § structure.
- **Missing:** everything else. Whitney has 1,316 §; the Aṣṭādhyāyī ~4,000 sūtras.
- **Verified gap:** no ACL paper aligns Western descriptive grammar statements to Pāṇinian sūtra
  IDs. Net-new — and correspondingly risky. Scoped as a **two-chapter pilot** (ch. III sandhi
  §§98–260; ch. XI aorist §§824–930) with a hard kill-gate, not a year-long commitment.

### S4 — Phonostatistics / style forensics (fold in, do not paper)

**Feeds Sangram:** nothing directly — this instrument's answer already sits in the M03 monograph
(Track M), and that is where it stays.

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

## 4. Track C — the publication arm of Sangram

Full-throttle sizing, per the human decision to promote this repo. Each quarter ends in a
shippable artifact, and each depends only on the one before it. Re-based 19-07-2026 (H1277):
each item below is stated as **what it delivers to Sangram** — the instruments of §2 mature
here, and the two papers of Q1 2027 are how Sangram's methods reach peer review. Nothing in
this section proposes a new Sangram topic or article manifest (freeze, §0 ruling 2): where a
deliverable touches Sangram, it grounds, cites, or hardens **existing** articles.

**Plainly, as of 19-07-2026:** Q3.1 is done (the agenda memo exists) and Q3.2 is done
([`S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md),
computed 10-07-2026); Q4.1–Q4.5 are **unclaimed and unstarted** — no TRACER/Passim/RefD
implementation exists in the repo, and the Q4.4 Whitney↔DCS↔Vidyut crosswalk file does not
exist. Presenting them otherwise would be false.

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
  reuse in the Sanskrit teaching tradition.* Productionises the S1 instrument whose τ result three
  Sangram programme docs already cite as evidence. Venue candidates: [NLP4DH](https://aclanthology.org/venues/nlp4dh/)
  (published the Sanskrit TRACER paper), LaTeCH-CLfL, or CHR. → `@DECIDE D1`.
- **Paper 2 (method).** *Does the corpus prefer a classification? Adjudicating three
  morphophonological schemes for Sanskrit verbal roots.* Formalises the agreement-metric method
  Sangram already practises in its compound-classification articles (§2 S2) and delivers the
  never-run three-scheme κ. Venue: WSC / ISCLS or SIGMORPHON.
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

## 5. Portfolio decisions, risks, and non-goals

### Decisions taken

The following rulings were made by Dr. Mārcis Gasūns in the 18-07-2026 roadmap interview. Later
sessions must not re-open them without new evidence or an explicit author request.

| # | Ruling | Operational consequence |
|---:|---|---|
| 1 | **Finish M03 first.** | M03 is the portfolio's highest-labelled deliverable; its manuscript enters publisher preparation before Sangram reopens expansion. |
| 2 | **Sangram consolidation freeze.** | No new Sangram topic/article manifests until all 26 current candidates have independent numerical re-derivation, scholarly visa, validators/build, and a final disposition. |
| 3 | **RQ4 GO now.** | Activate the existing Systema feature and recruit only under the already-approved protocol. |
| 4 | **Keep the current textbook-rights caveat; defer rights work.** | No per-work rights programme or emergency unpublish pass is added to this roadmap. Existing caveats and ordinary takedown/compliance handling remain. |
| 5 | **Hybrid tracked M03 edit.** | Agents apply mechanically safe RWS corrections with every change highlighted and the original preserved in comments; a human editor decides voice, argument, and disputed cases. |
| 6 | **Freeze M03 by 31-10-2026; contact «Нестор-История» in November.** | The former mid-2027 freeze is superseded; final number and ГОСТ passes occur at the October freeze. |
| 7 | **Keep all research tracks at full cadence.** | Comparative papers and other research continue; this does not override the specific Sangram no-new-topic freeze. |
| 8 | **Make this file the portfolio umbrella.** | Track documents remain detailed sources of truth, but priority conflicts are resolved here. |

### Risks and gates

1. **M03 editorial throughput.** The 31-10 freeze fails if the hybrid pass becomes untracked bulk
   rewriting. Every safe agent edit must remain reviewable; argument-changing edits stop for human
   judgment.
2. **Sangram evidence debt.** Rapid candidate growth already produced three refuted numerical
   claims in a 129-row re-derivation. The freeze is a quality gate, not a scheduling preference.
3. **RQ4 operational validity.** A technical launch is not permission to change recruitment,
   consent, assignment, diagnostics, or the four-week retention design.
4. **The 1878/1923 Bühler proxy.** Any borrowing-direction claim remains blocked until the 1878
   first-edition exercises are obtained and checked.
5. **Zipfian sparsity and S3 failure.** Comparative results require confidence intervals and the
   existing Pāṇini precision kill-gate; a bounded negative result is acceptable.
6. **Public-text rights.** Rights uncertainty remains real even though the author deferred a rights
   programme. Do not expand the caveat into a claim of permission.

### Remaining human actions and later decisions

| ID | Type | Action |
|---|---|---|
| M-H1 | `@DO` | Review and sign off the hybrid RWS edit packet; reject argument/voice changes that should not enter the frozen manuscript. |
| M-H2 | `@DO` | In November 2026, contact «Нестор-История», request the current house template, confirm Devanāgarī/IAST support, nominate two reviewers, and preserve the right to the free digital edition in the contract. |
| P-H1 | `@DO` | Begin recruitment from Systema's approved Kochergina-stage cohort after H1261 reports the production route green. |
| C-D1 | `@DECIDE` | Choose Paper 1 venue when the submission-ready abstract exists: NLP4DH, LaTeCH-CLfL, or CHR. |
| C-D4 | `@DO` | Obtain and verify the 1878 Bühler first edition; no borrowing-direction claim ships before this. |
| C-D5 | `@DECIDE` | Before the coverage-matrix paper reports agreement, decide whether to recruit a second annotator or publish a single-annotator adjudicated re-pass without κ. |

### Explicit non-goals

- No new Sangram topics during the consolidation freeze; repairs, re-derivations, visas, and
  candidate dispositions are in scope.
- No rewrite of argument-sensitive M03 prose without human review; “hybrid” is not blanket
  delegation of authorship.
- No change to the approved RQ4 protocol during launch.
- No new rights audit, rights matrix, or proactive unpublishing programme in this roadmap cycle.
- No pause on comparative research merely because M03 is priority one.
- No full 18-chapter Pāṇini alignment unless the two-chapter pilot clears its precision kill-gate.
- No new umbrella roadmap alongside this one; subordinate plans provide detail, not competing
  priority orders.

---

## 6. Immediate execution order

1. **H1259 — required next action:** execute the M03 hybrid edit/freeze mission.
2. **H1260 — parallel quality gate:** establish the Sangram consolidation ledger and enforce the
   no-new-topic baseline; consume H1257 rather than duplicating it.
3. **H1261 — parallel launch:** activate and verify RQ4 without changing its protocol.
4. Keep already-open comparative-paper and archive correctness work moving at full cadence.

The H1259/H1260/H1261 folder, model, and literal start lines are in §0. The October manuscript
freeze triggers the two final agent passes named in the press-readiness checklist; the November
publisher contact remains a human `@DO`, not an autonomous handoff.

_Dr. Mārcis Gasūns_
