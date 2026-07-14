# Digital Sanskrit Pedagogy — the field (org-wide metadocument)

_Created: 14-07-2026 · Last updated: 14-07-2026_

**What this is.** The single org-wide definition of **digital Sanskrit pedagogy** as a
*priority research field* across the ~85-repo Sanskrit-lexicon ecosystem. It sits **above** the
three partial pedagogy maps that already exist (see §1), consolidating them by reference — it
does **not** duplicate their content. Its job is to (a) name the field, (b) give a single
aspect-primary taxonomy with layered tags from which the learner-journey and capability views
derive, (c) inventory what already exists against what is missing, and (d) carry the research
agenda that turns a pile of learner-facing assets into a falsifiable field.

Registered as a field in [`MEGABOOK.md` §2.10](https://github.com/gasyoun/Uprava/blob/main/MEGABOOK.md)
(with §2.9 strengthened); the execution plan is
[`docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md).

---

## 0. What the field is

**Definition.** Digital Sanskrit pedagogy is the **research-and-integration** field that (1)
studies *how digital methods teach and assess Sanskrit* — difficulty estimation, exercise
generation, learner modelling, evaluation — and (2) consolidates the ecosystem's scattered
learner-facing assets into one coherent path from **A0 to C2**. It is both a research programme
(measurable findings, papers) *and* the integration that closes what
[`MEGABOOK.md`](https://github.com/gasyoun/Uprava/blob/main/MEGABOOK.md) §14.2 calls **«последняя
миля» до ученика** — the last mile to the student, the chain's main unclosed link.

**It is a field, not just a product, because** the substance already exists but scattered: three
separate maps, a dozen repos, dozens of assets, no shared definition and — critically — no
falsifiable research spine. Naming it consolidates the assets, states the hypotheses, and lets
"this tool teaches better" become a claim you can test rather than assert.

**Scope — org-wide, research-anchored.** This doc maps **all** pedagogy assets, including the
Tier-0 revenue product ([Systema-Sanscriticum](https://github.com/gasyoun/Systema-Sanscriticum),
the LMS), as the landscape. But the *field's own deliverables* are the **research + data + tool**
layer that feeds the product. The LMS is a **consumer** of the field, not part of it.

**Priority tier — straddle.** The research/data/tool layer is **Tier 1** (priority research,
alongside [kosha](https://github.com/gasyoun/kosha) and RussianTranslation); product integration
into Systema stays **Tier 0**. This matches the research/product split MEGABOOK keeps deliberately
separate (research creates knowledge; education and business turn it into value).

**What it is NOT.** Not the LMS itself. Not a new dictionary, corpus, or morphology engine — it
*consumes* those (CDSL, DCS, vidyut, Heritage, the Zaliznyak index) and never rebuilds them.

---

## 1. Relation to the three existing maps (consolidate by reference)

Three partial pedagogy maps already exist. This metadoc does not replace them; it is the layer
above that harmonizes their vocabulary (it adopts the A0–C2 rungs and the L0–L7 capability layers)
and adds the research/gap layer none of them carry.

| Existing map | Owner repo | What it covers | Relation to this doc |
|---|---|---|---|
| [`SANSKRIT_HUB_ASSET_PEDAGOGY_INDEX.md`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/docs/SANSKRIT_HUB_ASSET_PEDAGOGY_INDEX.md) + [`SANSKRIT_HUB_LEARNER_PROGRESSION_A0_C2.md`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/docs/SANSKRIT_HUB_LEARNER_PROGRESSION_A0_C2.md) | Systema-Sanscriticum | Asset → learner-rung → NLP-capability → **product** use-case, on one platform (8 layers L0–L7); the A0–C2 ladder the courses sell | The **product-facing** view. This doc reuses its rungs + layers and adds the org-wide research spine it lacks. |
| [`LEARNER_MATERIALS.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/LEARNER_MATERIALS.md) | SanskritGrammar (this repo) | The **textbook ladder** — Кочергина + Зализняк *Конспект* → Кнауэр → *Очерк* + Талмуд → Bühler → Apte | The **curriculum-source** view. This doc pins each aspect to its textbook rung and consumes this ladder. |
| [`POSITIONING.md`](https://github.com/gasyoun/kosha/blob/main/POSITIONING.md) + `USE_CASES.md` UC6–UC9 | kosha | The **dictionary-as-reading-companion** — the look-up-to-learned loop for a second-year student | The **lexical-tool** view. This doc treats kosha's loop as the reading + vocabulary engine. |
| **This doc** | SanskritGrammar (root) | The org-wide **field definition + aspect taxonomy + research agenda + gap register** | The layer **above** all three; no content duplicated. |

---

## 2. How to read an aspect entry — the layer schema

The spine below is **aspect-primary** (one section per pedagogy aspect). Every asset/gap in an
aspect is tagged on six layers, so that the **matrix**, **learner-journey**, **capability**, and
**traditional-discipline** views in §4 all *derive* from the same data instead of being separate
documents to maintain.

| Layer | Values |
|---|---|
| **Rung** | CEFR `A0 A1 A2 B1 B2 C1 C2` (as in the Systema ladder) |
| **Status** | ✅ built · 🟡 partial · 📋 planned · ⬜ gap (nothing yet) |
| **NLP capability** | `L0` script/translit · `L1` lexical · `L2` morphology/roots · `L3` corpus/frequency · `L4` alignment/translation · `L5` API/hub · `L6` learn-track · `L7` portal (+ specific: `cheda`=segmentation, `paradigm-gen`, `form2lemma`, `difficulty`, `TTS`, `ASR`) |
| **Research-Q** | `RQ1` difficulty/ordering · `RQ2` drill-generation · `RQ3` textbook-vs-corpus · `RQ4` evaluation-methodology (the wave-1 spine, §5) |
| **Discipline** | traditional Indian frame: `śikṣā` (phonetics) · `vyākaraṇa` (grammar) · `nirukta` (etymology) · `chandas` (metre) · `kośa` (lexicon) · `kāvya` (composition/reading) · `bhāṣya` (commentary) |
| **Owning repo** | the repo that owns the asset |

---

## 3. The aspects (the spine)

Six aspects carry the field. **Sandhi is already in active development** (kosha handoff H902,
Phase 4 pedagogy surfaces); the other five are the priority set the interview locked. Six further
aspects (§3.7–§3.12) are mapped for org-wide completeness with lighter treatment.

### 3.1 Sandhi — external + internal ✅🟡 (active)

Splitting joined surface text back into padas and joining split forms — the gateway skill that
stands between a learner and any real text.

- **Rungs** A2 (split a short line) → B1/B2 (read sandhied text) · **Disc.** śikṣā + vyākaraṇa · **NLP** `L2 cheda`, `L0`
- **Assets:** [SandhiCollider](https://github.com/gasyoun/SanskritGrammar/blob/main/src/components/talmud/SandhiCollider.jsx) (SanskritGrammar ✅ — vowel-sandhi rule visualiser) · kosha `sandhi:` operator + [`segmenter.py`](https://github.com/gasyoun/kosha/blob/main/app/segmenter.py) (✅) · corpus-sandhi extraction + [H902 pedagogy surfaces](https://github.com/gasyoun/Uprava/blob/main/handoffs/H902-Opus_kosha_sandhi-phase4-pedagogy-surfaces_14.07.26.md) (kosha 🟡 active) · [ScharfSandhi](https://github.com/gasyoun/ScharfSandhi) engine (✅) · shared-exercise [Concordance](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx) (✅) · Heritage / vidyut `cheda` (external)
- **Research-Q** RQ1 (which sandhi types are hardest — graded difficulty), RQ2 (auto-generate sandhi-split drills from attested corpus), [SG-H7](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md) (sandhi ↔ Pāṇini alignment)
- **Gap:** verified answer-keying of auto-split drills at scale; a *graded* difficulty ordering of sandhi phenomena.

### 3.2 Morphology drills — declension & conjugation

Practising the noun/verb paradigm system — the largest rote surface in the language.

- **Rungs** A2 (a-stems, present) → B1/B2 (all classes, all tenses) · **Disc.** vyākaraṇa · **NLP** `L2 paradigm-gen`, `form2lemma`
- **Assets:** kosha paradigm engine + [`ParadigmTable.svelte`](https://github.com/gasyoun/kosha/blob/main/ui/src/components/ParadigmTable.svelte) (✅) · SanskritGrammar widgets [AblautMachine / SetTree / ReduplicationSandbox / HeteroclisisMap](https://github.com/gasyoun/SanskritGrammar/tree/main/src/components/talmud) (✅) · [csl-inflect](https://github.com/sanskrit-lexicon/csl-inflect) (✅) · [VisualDCS](https://github.com/gasyoun/VisualDCS) paradigm browser + flashcard mode (✅) · Zaliznyak grammar-token [`cardToken.js`](https://github.com/gasyoun/kosha/blob/main/ui/src/lib/cardToken.js) + `zaliznyak-grammar-index` (98,639 headwords, ✅) · Systema sort/match/cloze [exercise engines](https://github.com/gasyoun/Systema-Sanscriticum/tree/main/public/exercises) (✅) · vidyut-prakriya (external)
- **Research-Q** RQ1 (**which forms actually occur** — VisualDCS verb-form frequency: stop drilling forms that never appear; Pareto-prioritised practice), RQ2 (auto paradigm-fill drills)
- **Gap:** accent-dependent class ambiguity (class I vs VI, IV vs passive) is *not* recoverable from unaccented DCS — surface it, never fabricate; answer keys for the SanskritGrammar drill bank (Talmud Phase 4).

### 3.3 Graded vocabulary / SRS

Learning the right words in the right order — the highest-leverage single lever a learner has.

- **Rungs** A1+ (all) · **Disc.** kośa · **NLP** `L3 frequency`
- **Assets:** kosha frequency layer [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv) — `core_rank` = Leonchenko **"learn-these-first"** order + `coverage_pct` (83,277 lemmas, ✅) · kosha CSV/**Anki** [`export.js`](https://github.com/gasyoun/kosha/blob/main/ui/src/lib/export.js) (✅) · Systema **"Saraswati"** FSRS SRS (✅, pilot Aug 2026) · [SanskritKaraoke](https://github.com/gasyoun/SanskritKaraoke) SM-2 SRS (✅) · [CourseDump2022](https://github.com/gasyoun/CourseDump2022) Memrise→Anki (✅) · Amarakośa (traditional semantic-field thesaurus — digitisation candidate)
- **Research-Q** RQ1 (**is corpus-frequency order the optimal learning order?** the `core_rank` hypothesis), RQ4 (does frequency-ordered SRS beat textbook-order — user study)
- **Gap:** no field-tested proof that frequency-order beats textbook-order; semantic-field decks (Amarakośa-style) not built.

### 3.4 Graded reading / readers

Reading real text with scaffolding — where all the sub-skills compose into comprehension.

- **Rungs** B1 (subhāṣitas) → B2 (epic) → C1 (Vedic/commentary) · **Disc.** kāvya · **NLP** `L4 alignment`, `L3`, `L2`, `difficulty`
- **Assets:** kosha reading packs Gītā 1 / Nala 1 (📋 data-gated) · kosha dict↔corpus **KWIC** [concordance](https://github.com/gasyoun/kosha/blob/main/concordance/dict/index.html) (✅) · [RussianRamayana](https://github.com/gasyoun/RussianRamayana) parallel reader (✅, the flagship B2 graded text) · `corpus_lexicon` interlinear (1.09M aligned Sa↔Ru pairs, ✅) · Indische Sprüche (7,537 subhāṣitas, ✅) · [SamudraManthanam](https://github.com/gasyoun/SamudraManthanam) parallel corpus (✅) · [buhler-sanskrit-book](https://github.com/alexander-myltsev/buhler-sanskrit-book) exercises (🟡 20/48 lessons) · [Nalopakhyanam](https://github.com/gasyoun/Nalopakhyanam) beginner reader (⬜ stub)
- **Research-Q** RQ1 (**difficulty-score any text** → auto-assemble a graded reader at a target level), RQ2 (reading-pack generation from DCS lemmatisation)
- **Gap:** the difficulty scorer itself; kosha reading packs (data-gated); the Nala beginner reader is an empty stub.

### 3.5 Pāṇinian derivation / grammar-rule pedagogy

Teaching the rule system itself — deriving a form from the Aṣṭādhyāyī (prakriyā). The most
scholarly aspect, highest ceiling, least built.

- **Rungs** B2 → C1/C2 · **Disc.** vyākaraṇa (Pāṇini is the core) · **NLP** `L2 Pāṇinian-parse/generate`
- **Assets:** [`/panini-sutra-lookup`](https://github.com/gasyoun/github-spine/blob/main/SKILLS_INDEX.md) + `/panini-commentary-corpus` skills · kosha **Pāṇini-sūtra ↔ corpus concordance** ([`CONCORDANCE_ROADMAP.md`](https://github.com/gasyoun/kosha/blob/main/CONCORDANCE_ROADMAP.md) Q4, 📋 planned) · Samsaadhanii / SCL Pāṇinian parse (external) · vidyut-prakriya — generates forms from Pāṇinian rules (external) · [csl-kale](https://github.com/sanskrit-lexicon/csl-kale) *Higher Sanskrit Grammar* (✅ display)
- **Research-Q** RQ3 (**where do sūtra-derivable forms not occur in the corpus?** — the Pāṇini-vs-attestation axis), RQ2 (sūtra → derivation drills)
- **Gap:** the sūtra↔corpus concordance (kosha Q4); a prakriyā (step-by-step derivation) teaching surface.

### 3.6 Zaliznyak-made-learnable — the formal-grammar on-ramp

A **gentler** path into Zaliznyak's formal declension/conjugation calculus (Ряд / Тип / seṭ) than
[Толчельников's *Талмуд*](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026),
which is a full generative Meaning-Text *руководство* — **often overkill** for a learner who needs
the intuition first. The Талмуд stays as the deep-dive tier *behind* the on-ramp
(progressive disclosure, à la kosha's "one tap deeper").

- **Rungs** A2 → B1 (a gentler entry, below the Талмуд's post-beginner peak) · **Disc.** vyākaraṇa · **NLP** `L2 stem-class tagging`
- **Assets:** [Зализняк *Очерк* 1978](https://github.com/gasyoun/SanskritGrammar/tree/main/ZalizniakOcherk_1978) (§-addressable ✅) · [*Конспект* 2004](https://github.com/gasyoun/SanskritGrammar/tree/main/ZalizniakKonspekt_2004) (✅) · the Талмуд (🟡 deep tier) · [samskrtam.ru/z/](https://samskrtam.ru/z/) Shirobokov verbal-morphology DB (external) · kosha Zaliznyak grammar-token `m·8n*` (✅) · `zaliznyak-grammar-index` (✅) · [Gasuns 2014 dissertation](https://github.com/gasyoun/SanskritGrammar/tree/main/GasunsDhatu_2014) (the middle term 1975→2014→2026) · [`MORPHOCLASS_3WAY_MEMO.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.md)
- **Research-Q** RQ4 (**does a gentler on-ramp improve retention vs Талмуд-first?**), pedagogical simplification of a formal calculus (minimal-notation, visual, graded)
- **Gap:** the on-ramp itself — a graded, visual, minimal-notation introduction to Ряд/Тип/seṭ that a Kochergina-stage learner can use, with the full Талмуд one tap deeper. **This is a wave-1 build.**

### 3.7 Audio / recitation / phonetics — śikṣā ⬜ (named gap, not wave-1)

- **Rungs** A0/A1/A2 (blocks beginners) · **Disc.** śikṣā · **NLP** `TTS`, `ASR` (both ⬜)
- **Assets:** [SanskritKaraoke](https://github.com/gasyoun/SanskritKaraoke) metre/akṣara trainer (✅ **but no audio**) · VedaWeb accent (external, C1) · spoken-sanskrit-corpus ~2,861 recorded lessons + ASR transcripts (🟡 private scaffold)
- **Research-Q** (agenda, not wave-1): śikṣā pedagogy; ASR-assisted recitation feedback; TTS authenticity vs cost
- **Gap:** **NO AUDIO ANYWHERE — the single biggest ecosystem gap**, flagged by both the Systema pedagogy index (§8) and the SanskritKaraoke roadmap. Needs external content (recorded reciter or TTS). On the agenda, not the first build.

### 3.8–3.12 Secondary aspects (org-wide completeness)

| # | Aspect | Rungs · Disc. | Key assets | Gap |
|---|---|---|---|---|
| 3.8 | **Script / Devanāgarī acquisition** | A0/A1 · lipi/śikṣā | SanskritKaraoke akṣara trainer; transliteration playground (`sanskrit-util`); Systema A0 Cyrillic-only track; "Devanāgarī teaching order — most-frequent conjuncts first" ([PROJECT_INTERLINKS](https://github.com/gasyoun/Uprava/blob/main/PROJECT_INTERLINKS.md)) | stroke-order module; handwriting UGC (Jan 2027 cohort) |
| 3.9 | **Metre / chandas** | B2/C1 · chandas | SanskritKaraoke wave-notation metre trainer + quizzes (✅); vidyut-chandas (external); paper A47 (anuprāsa + chandas) | metre-ID as a graded drill wired into reading |
| 3.10 | **Composition / active production** | B2+ · kāvya | Systema homework + curator review (✅); Eng→Skt composition helper; buhler translate-into-Sanskrit exercises (🟡); [SamasaChakram](https://github.com/gasyoun/SamasaChakram) compound trainer (⬜ empty stub) | auto-feedback on learner-produced Sanskrit (→ learner-error research); SamasaChakram is empty |
| 3.11 | **Commentary reading** | C1/C2 · bhāṣya | [CommentaryStrategies](https://github.com/gasyoun/CommentaryStrategies) (✅); Sundara apparatus (🟡); Skt→Skt "pandit mode" (SKD/VCP) | guided commentary-reading interface |
| 3.12 | **Spell / error feedback** (cross-cutting) | A2+ · vyākaraṇa | [SanskritSpellCheck](https://github.com/gasyoun/SanskritSpellCheck) faultfinder + detectors (✅ but scholar-facing); `union_headwords` "is this a word?" | a *learner-facing* forgiving spell-assist; a learner-error corpus |

---

## 4. Derived views (pivots on the §3 tags)

### 4a. Matrix — aspect × CEFR rung → where the assets and gaps are

| Aspect ↓ / Rung → | A0–A1 | A2 | B1 | B2 | C1–C2 |
|---|---|---|---|---|---|
| Sandhi | — | ✅ split drills | 🟡 sandhied reading | 🟡 | — |
| Morphology | — | ✅ a-stems/present | ✅ paradigms | 🟡 all classes | 🟡 |
| Vocabulary/SRS | 🟡 | ✅ freq decks | ✅ | ✅ | ✅ |
| Reading | — | — | ✅ subhāṣitas | 🟡 epic | 📋 Vedic/comm. |
| Pāṇini | — | — | — | 📋 | 📋 sūtra↔corpus |
| Zaliznyak on-ramp | — | ⬜ **build** | ⬜ **build** | 🟡 Талмуд | 🟡 |
| Audio/śikṣā | ⬜ **gap** | ⬜ **gap** | — | — | 📋 accent (VedaWeb) |

The visible pattern: **A0–A1 is the thinnest column** (audio + native beginner grammar are the
holes), the **B1–B2 middle is asset-rich but unintegrated**, and **C1–C2 is planned depth**
(Pāṇini, Vedic, commentary).

### 4b. Learner-journey view (A0 → C2)

Derives by re-sorting §3 assets by rung. The authoritative rung-by-rung ladder — with each rung's
gate and powering asset — is Systema's
[`SANSKRIT_HUB_LEARNER_PROGRESSION_A0_C2.md`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/docs/SANSKRIT_HUB_LEARNER_PROGRESSION_A0_C2.md);
this field consumes it rather than restating it. The three cross-rung mechanics it names —
**reader-as-a-service**, **frequency-ordered SRS**, **difficulty scorer** — are exactly the
integration deliverables the research agenda (§5) produces.

### 4c. NLP-capability view (L0 → L7)

Derives by grouping §3 assets by capability tag. The authoritative capability→asset map is
Systema's
[`SANSKRIT_HUB_ASSET_PEDAGOGY_INDEX.md`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/docs/SANSKRIT_HUB_ASSET_PEDAGOGY_INDEX.md)
(layers L0–L7). Pedagogically the load-bearing capabilities are **L2** (morphology: the drill
engines), **L3** (frequency: the difficulty + SRS spine), and **L4** (alignment: the interlinear
reader). Where an aspect's gap is really a *missing NLP capability* (audio = missing TTS/ASR; the
last mile = missing L6 wiring), this view is what surfaces it.

### 4d. Traditional-discipline view (the emic frame)

Sanskrit's own pedagogy is organised by discipline, and the field should read in that frame too:
**śikṣā** (§3.1 sandhi-phonology, §3.7 recitation, §3.8 script) · **vyākaraṇa** (§3.2 morphology,
§3.5 Pāṇini, §3.6 Zaliznyak) · **kośa** (§3.3 vocabulary) · **kāvya** (§3.4 reading, §3.10
composition) · **chandas** (§3.9 metre) · **bhāṣya** (§3.11 commentary). The etic CEFR ladder and
the emic Vedāṅga frame are two projections of the same asset set.

---

## 5. The research agenda — the wave-1 spine

Four research questions make the field falsifiable. Each names what it extends, its falsifiable
form, and its paper.

| RQ | Question | Extends | Falsifiable form | Paper |
|---|---|---|---|---|
| **RQ1** | Do corpus statistics predict/optimise **learning order** better than textbook intuition? | kosha `core_rank` + SanskritGrammar textbook-sequencing Kendall-τ ([S1 result](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md)) | Does frequency-order correlate with textbook-order (τ)? Where they diverge, which predicts learning gain? | new **difficulty/ordering** method paper |
| **RQ2** | Can we **auto-generate** valid, answer-keyed drills (sandhi-split, cloze, paradigm-fill) from attested corpus? | SanskritGrammar Talmud drill bank + Systema exercise engines | Gold-answer agreement rate; do auto-drills teach as well as authored ones? | (feeds A62 + the on-ramp) |
| **RQ3** | Which **textbook grammar rules the corpus does not confirm** are *pedagogically* load-bearing? | [A60](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60) + [FINDINGS §72](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md) two-axis method | Per-claim TRUE/OVERSTATED/FALSE vs DCS (e.g. future-stem `-iṣya` seṭ = 56.8% majority ⇒ "single rule -syá" OVERSTATED) | **A60** (flagship, 4/5) |
| **RQ4** | How do we **prove** a digital Sanskrit tool teaches? | [A32](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md) learner-reading-layer paper | User-study design; learning-gain + retention metrics; without it the field's claims are unfalsifiable | **A32** (elevate) |

The field-defining survey + hypotheses go in the new agenda paper **A62** ("Digital Sanskrit
pedagogy: a research agenda"). These four RQs align with, and extend, the SanskritGrammar
hypotheses [SG-H1…SG-H9](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md)
(each of which already carries an explicit "Learner read").

---

## 6. Gap register (honest — so nobody re-derives these)

1. **No audio anywhere** — the single biggest gap; blocks A0–A2 fully (§3.7). Needs external content.
2. **The "last mile" to the learner is unclosed** — the two proven chains (dictionary → kosha → Systema; corpus → Sangram → lesson) both have a *queued* final hop (MEGABOOK §14.2). This is the **integration** half of the field.
3. **A0–A2 native beginner grammar** is pedagogy to *build*, not an asset to fold in (Systema index §8).
4. **Difficulty scorer** — assumed by reading, SRS, and RQ1, but not yet built.
5. **Answer keys / auto-verification** for the drill banks (SanskritGrammar Talmud Phase 4; RQ2).
6. **Accent-dependent ambiguity** — class I/VI, IV/passive not recoverable from unaccented DCS; surface, never fabricate.
7. **Empty stubs** — [SamasaChakram](https://github.com/gasyoun/SamasaChakram) (compound trainer), [Nalopakhyanam](https://github.com/gasyoun/Nalopakhyanam) (beginner reader).
8. **No learner corpus / error analysis** — the raw material for RQ4 and adaptive modelling.

---

## 7. Priority, positioning, registration

- **Tier:** straddle — research/data/tool **T1**, product integration **T0** (§0).
- **MEGABOOK:** new thesis [§2.10](https://github.com/gasyoun/Uprava/blob/main/MEGABOOK.md) declares the field; [§2.9](https://github.com/gasyoun/Uprava/blob/main/MEGABOOK.md) (education inherits a verified source, rated 🔴 "усилить") is strengthened as its foundation.
- **Papers:** A62 (agenda) · A32 (evaluation, elevate) · A60 (textbook-vs-corpus, flagship) · new difficulty/ordering method paper (RQ1). See [`ARTICLES.md`](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md).
- **Execution plan:** [`docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md) (roadmap · architecture · implementation · verification).
- **Value-chain place:** research → **education** → public value; this field is the education contour, and closing its last mile is what turns the decade of lexical/corpus plumbing into something a learner touches.

---

## 8. How to extend this doc

- **Add an aspect** as a new §3.x with the full six-layer tag line + a gap; then reflect it in the §4a matrix. Do not spawn a parallel pedagogy doc — this is the single org-wide one.
- **Keep the derived views (§4) pointing at the source maps**, not copying them — when Systema's ladder or index changes, this doc references the change, it does not restate it.
- **Every new learner-facing asset in any repo** earns a row in its aspect here (and a line in the owning repo's own map). Companion metadoc: [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.meta.md).

---

_Dr. Mārcis Gasūns_
