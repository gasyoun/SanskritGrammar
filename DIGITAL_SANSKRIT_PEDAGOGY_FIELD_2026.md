# Digital Sanskrit Pedagogy — the field (org-wide metadocument)

_Created: 14-07-2026 · Last updated: 27-07-2026_

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
- **First measurable result — PM1, verified-split agreement rate** (§4e): share of auto-generated split items whose split a second, independent segmenter confirms, over a hand-checked gold sample of ≥200 attested lines. Today unmeasured (no gold set). Bar ≥90%, every disagreement shipped as evidence.

### 3.2 Morphology drills — declension & conjugation

Practising the noun/verb paradigm system — the largest rote surface in the language.

- **Rungs** A2 (a-stems, present) → B1/B2 (all classes, all tenses) · **Disc.** vyākaraṇa · **NLP** `L2 paradigm-gen`, `form2lemma`
- **Assets:** kosha paradigm engine + [`ParadigmTable.svelte`](https://github.com/gasyoun/kosha/blob/main/ui/src/components/ParadigmTable.svelte) (✅) · SanskritGrammar widgets [AblautMachine / SetTree / ReduplicationSandbox / HeteroclisisMap](https://github.com/gasyoun/SanskritGrammar/tree/main/src/components/talmud) (✅) · [csl-inflect](https://github.com/sanskrit-lexicon/csl-inflect) (✅) · [VisualDCS](https://github.com/gasyoun/VisualDCS) paradigm browser + flashcard mode (✅) · Zaliznyak grammar-token [`cardToken.js`](https://github.com/gasyoun/kosha/blob/main/ui/src/lib/cardToken.js) + `zaliznyak-grammar-index` (98,639 headwords, ✅) · Systema sort/match/cloze [exercise engines](https://github.com/gasyoun/Systema-Sanscriticum/tree/main/public/exercises) (✅) · vidyut-prakriya (external)
- **Research-Q** RQ1 (**which forms actually occur** — VisualDCS verb-form frequency: stop drilling forms that never appear; Pareto-prioritised practice), RQ2 (auto paradigm-fill drills)
- **Gap:** accent-dependent class ambiguity (class I vs VI, IV vs passive) is *not* recoverable from unaccented DCS — surface it, never fabricate; answer keys for the SanskritGrammar drill bank (Talmud Phase 4).
- **First measurable result — PM2, answer-keyed item share** (§4e): share of drill-bank items carrying an authoritative key, with ambiguity flagged rather than fabricated. Today **90.7%** (40 863 of 45 045 attested-cell items). Bar ≥95% across the union with the Talmud Phase-4 bank, 100% of accent-ambiguous cells flagged.

### 3.3 Graded vocabulary / SRS

Learning the right words in the right order — the highest-leverage single lever a learner has.

- **Rungs** A1+ (all) · **Disc.** kośa · **NLP** `L3 frequency`
- **Assets:** kosha frequency layer [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv) — `core_rank` = Leonchenko **"learn-these-first"** order + `coverage_pct` (83,277 lemmas, ✅) · kosha CSV/**Anki** [`export.js`](https://github.com/gasyoun/kosha/blob/main/ui/src/lib/export.js) (✅) · Systema **"Saraswati"** FSRS SRS (✅, pilot Aug 2026) · [SanskritKaraoke](https://github.com/gasyoun/SanskritKaraoke) SM-2 SRS (✅) · [CourseDump2022](https://github.com/gasyoun/CourseDump2022) Memrise→Anki (✅) · Amarakośa (traditional semantic-field thesaurus — digitisation candidate)
- **Research-Q** RQ1 (**is corpus-frequency order the optimal learning order?** the `core_rank` hypothesis), RQ4 (does frequency-ordered SRS beat textbook-order — user study)
- **Gap:** no field-tested proof that frequency-order beats textbook-order; semantic-field decks (Amarakośa-style) not built.
- **First measurable result — PM3, corrected-order divergence** (§4e): Kendall-τ between the published learn-order and raw `rank_all`, plus the count of function words left in its top 100. Today no corrected order exists (curated `core_rank` vs `rank_all` τ = **0.887**; **30 of the top-100** corpus lemmas are absent from the curated list). Bar: a committed order with 0 function words in the top 100 and a reproducible genre-weighting step.

### 3.4 Graded reading / readers

Reading real text with scaffolding — where all the sub-skills compose into comprehension.

- **Rungs** B1 (subhāṣitas) → B2 (epic) → C1 (Vedic/commentary) · **Disc.** kāvya · **NLP** `L4 alignment`, `L3`, `L2`, `difficulty`
- **Assets:** kosha reading packs Gītā 1 / Nala 1 (📋 data-gated) · kosha dict↔corpus **KWIC** [concordance](https://github.com/gasyoun/kosha/blob/main/concordance/dict/index.html) (✅) · [RussianRamayana](https://github.com/gasyoun/RussianRamayana) parallel reader (✅, the flagship B2 graded text) · `corpus_lexicon` interlinear (1.09M aligned Sa↔Ru pairs, ✅) · Indische Sprüche (7,537 subhāṣitas, ✅) · [SamudraManthanam](https://github.com/gasyoun/SamudraManthanam) parallel corpus (✅) · [buhler-sanskrit-book](https://github.com/alexander-myltsev/buhler-sanskrit-book) exercises (🟡 20/48 lessons) · [Nalopakhyanam](https://github.com/gasyoun/Nalopakhyanam) beginner reader (⬜ stub)
- **Research-Q** RQ1 (**difficulty-score any text** → auto-assemble a graded reader at a target level), RQ2 (reading-pack generation from DCS lemmatisation)
- **Gap:** the difficulty scorer itself; kosha reading packs (data-gated); the Nala beginner reader is an empty stub.
- **First measurable result — PM4, scorer agreement with an independent ordering** (§4e): Kendall-τ between predicted passage difficulty and the textbook lesson at which that passage's vocabulary is first fully covered, over ≥100 held-out passages. Today unmeasured (no scorer); the anchors are textbook-vs-frequency τ ≈ **0.05–0.07** and textbook-vs-textbook τ **0.446–0.835**. Bar τ ≥ 0.40 — above the frequency floor, inside the human-agreement band.

### 3.5 Pāṇinian derivation / grammar-rule pedagogy

Teaching the rule system itself — deriving a form from the Aṣṭādhyāyī (prakriyā). The most
scholarly aspect, highest ceiling, least built.

- **Rungs** B2 → C1/C2 · **Disc.** vyākaraṇa (Pāṇini is the core) · **NLP** `L2 Pāṇinian-parse/generate`
- **Assets:** [`/panini-sutra-lookup`](https://github.com/gasyoun/github-spine/blob/main/SKILLS_INDEX.md) + `/panini-commentary-corpus` skills · kosha **Pāṇini-sūtra ↔ corpus concordance** ([`CONCORDANCE_ROADMAP.md`](https://github.com/gasyoun/kosha/blob/main/CONCORDANCE_ROADMAP.md) Q4, 📋 planned) · Samsaadhanii / SCL Pāṇinian parse (external) · vidyut-prakriya — generates forms from Pāṇinian rules (external) · [csl-kale](https://github.com/sanskrit-lexicon/csl-kale) *Higher Sanskrit Grammar* (✅ display)
- **Research-Q** RQ3 (**where do sūtra-derivable forms not occur in the corpus?** — the Pāṇini-vs-attestation axis), RQ2 (sūtra → derivation drills)
- **Gap:** the sūtra↔corpus concordance (kosha Q4); a prakriyā (step-by-step derivation) teaching surface.
- **First measurable result — PM5, sūtra→attestation resolution rate** (§4e): share of a fixed sample of form-deriving sūtras for which the concordance returns ≥1 attested corpus form, with the zero-attestation residue published as a count rather than dropped. Today unmeasured (concordance planned). Bar ≥80% resolved.

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
- **First measurable result — PM6, on-ramp scope transfer** (§4e): share of the Приложение-1 root catalogue the on-ramp's 4 taught ablaut rows cover, by type *and* by DCS token mass. Measured 27-07-2026: **56.5% by type** (421 of 745 roots) and **56.2% by token mass** (483 532 of 860 159 over the 616 roots that join kosha's frequency table). The two figures being near-identical is the finding: the 4 rows are **frequency-neutral**, so the on-ramp buys scope proportional to its size, not a high-frequency shortcut. Bar: quote that transfer figure beside every on-ramp completion claim. *Learning-gain and retention for this aspect belong exclusively to the RQ4 protocol — PM6 measures reach, never teaching effect.*

### 3.7 Audio / recitation / phonetics — śikṣā ⬜ (named gap, not wave-1)

- **Rungs** A0/A1/A2 (blocks beginners) · **Disc.** śikṣā · **NLP** `TTS`, `ASR` (both ⬜)
- **Assets:** [SanskritKaraoke](https://github.com/gasyoun/SanskritKaraoke) metre/akṣara trainer (✅ **but no audio**) · VedaWeb accent (external, C1) · spoken-sanskrit-corpus ~2,861 recorded lessons + ASR transcripts (🟡 private scaffold)
- **Research-Q** (agenda, not wave-1): śikṣā pedagogy; ASR-assisted recitation feedback; TTS authenticity vs cost
- **Gap:** **NO AUDIO ANYWHERE — the single biggest ecosystem gap**, flagged by both the Systema pedagogy index (§8) and the SanskritKaraoke roadmap. Needs external content (recorded reciter or TTS). On the agenda, not the first build.
- **First measurable result — PM7, rights-cleared audio units** (§4e): count of learner-facing units (akṣara, verse, lesson) with a playable, licence-stamped audio track. Today **0** — the field's only zero-baseline metric, and the only one whose bar is a single unit. Gated on the TTS-vs-reciter `@DECIDE`; audio without a licence row counts as 0, since it cannot be published.

### 3.8–3.12 Secondary aspects (org-wide completeness)

| # | Aspect | Rungs · Disc. | Key assets | Gap | First measurable result (§4e) |
|---|---|---|---|---|---|
| 3.8 | **Script / Devanāgarī acquisition** | A0/A1 · lipi/śikṣā | SanskritKaraoke akṣara trainer; transliteration playground (`sanskrit-util`); Systema A0 Cyrillic-only track; "Devanāgarī teaching order — most-frequent conjuncts first" ([PROJECT_INTERLINKS](https://github.com/gasyoun/Uprava/blob/main/PROJECT_INTERLINKS.md)) | stroke-order module; handwriting UGC (Jan 2027 cohort) | **PM8** — cumulative DCS conjunct-token coverage of the first 50 taught conjuncts; bar ≥90% |
| 3.9 | **Metre / chandas** | B2/C1 · chandas | SanskritKaraoke wave-notation metre trainer + quizzes (✅); vidyut-chandas (external); paper A47 (anuprāsa + chandas) | metre-ID as a graded drill wired into reading | **PM9** — per-metre metre-ID accuracy on ≥200 hand-labelled verses; bar ≥95% on the three commonest metres |
| 3.10 | **Composition / active production** | B2+ · kāvya | Systema homework + curator review (✅); Eng→Skt composition helper; buhler translate-into-Sanskrit exercises (🟡); [SamasaChakram](https://github.com/gasyoun/SamasaChakram) compound trainer (⬜ empty stub) | auto-feedback on learner-produced Sanskrit (→ learner-error research); SamasaChakram is empty | **PM10** — feedback **precision** on ≥100 labelled real learner sentences; bar ≥0.90 at recall ≥0.50 |
| 3.11 | **Commentary reading** | C1/C2 · bhāṣya | [CommentaryStrategies](https://github.com/gasyoun/CommentaryStrategies) (✅); Sundara apparatus (🟡); Skt→Skt "pandit mode" (SKD/VCP) | guided commentary-reading interface | **PM11** — pratīka→mūla auto-resolution rate over ≥500 references; bar ≥85%, 0 guessed anchors |
| 3.12 | **Spell / error feedback** (cross-cutting) | A2+ · vyākaraṇa | [SanskritSpellCheck](https://github.com/gasyoun/SanskritSpellCheck) faultfinder + detectors (✅ but scholar-facing); `union_headwords` "is this a word?" | a *learner-facing* forgiving spell-assist; a learner-error corpus | **PM12** — false-positive rate on ≥5 000 *correct* learner-level forms; bar ≤2% |

---

## 4. Derived views (pivots on the §3 tags)

### 4a. Matrix — aspect × CEFR rung → where the assets and gaps are

| Aspect ↓ / Rung → | A0–A1 | A2 | B1 | B2 | C1–C2 | Metric (§4e) — today → bar |
|---|---|---|---|---|---|---|
| Sandhi | — | ✅ split drills | 🟡 sandhied reading | 🟡 | — | **PM1** — unmeasured → ≥90% |
| Morphology | — | ✅ a-stems/present | ✅ paradigms | 🟡 all classes | 🟡 | **PM2** — 90.7% → ≥95% |
| Vocabulary/SRS | 🟡 | ✅ freq decks | ✅ | ✅ | ✅ | **PM3** — no corrected order → 0 function words in top 100 |
| Reading | — | — | ✅ subhāṣitas | 🟡 epic | 📋 Vedic/comm. | **PM4** — no scorer → τ ≥ 0.40 |
| Pāṇini | — | — | — | 📋 | 📋 sūtra↔corpus | **PM5** — unmeasured → ≥80% resolved |
| Zaliznyak on-ramp | — | ⬜ **build** | ⬜ **build** | 🟡 Талмуд | 🟡 | **PM6** — 56.5% type / 56.2% token (measured) |
| Audio/śikṣā | ⬜ **gap** | ⬜ **gap** | — | — | 📋 accent (VedaWeb) | **PM7** — **0** → ≥1 licensed unit |

The visible pattern: **A0–A1 is the thinnest column** (audio + native beginner grammar are the
holes), the **B1–B2 middle is asset-rich but unintegrated**, and **C1–C2 is planned depth**
(Pāṇini, Vedic, commentary). The metric column adds a second reading: **only two of the seven
aspects have a number at all today** (PM2, PM6) — the ✅ glyphs record that an asset was *built*,
not that anything was *measured*, and the register in §4e is what closes that distance.

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

### 4e. Metric view — the "first measurable result" per aspect

Every aspect in §3 carries exactly one **PM** (pedagogy metric): the single number whose movement
would count as evidence that this aspect progressed. One metric per aspect, deliberately — a
basket of indicators lets a stalled aspect always show *something* green, which is the failure
mode this register exists to prevent.

**Two layers, and the line between them is load-bearing.** A PM is a **capability** metric,
measurable from committed artifacts with no human subjects. Learner **outcomes** — learning gain
and retention — belong exclusively to
[RQ4's protocol](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md),
which is gated on a launch decision (the `features.rq4_study` flag) and has one instrument for the
whole field. Splitting it this way is what makes the register usable *now*: if every aspect's
metric were an outcome metric, nothing would be measurable until recruitment runs, and twelve
aspects would each be quietly inventing a second learning-gain instrument.

**Admission rule.** A PM is admitted only with all five fields below — a metric with no
refutation condition is an indicator, not a falsifiable claim, and does not belong here. Each
metric targets its aspect's own stated **Gap**, so "the metric moved" and "the gap closed" are
the same sentence.

| ID | Aspect | Metric — counted over what denominator | Data source | Today | Bar → refuted if |
|---|---|---|---|---|---|
| **PM1** | 3.1 Sandhi | Auto-split drill items whose split an independent second segmenter confirms / all items in a hand-checked gold sample of ≥200 attested lines | kosha [`segmenter.py`](https://github.com/gasyoun/kosha/blob/main/app/segmenter.py) + corpus-sandhi extraction (H902) vs Heritage / vidyut `cheda`; gold set to be committed beside the drills | **unmeasured** — no gold set exists | ≥90%, every disagreement shipped as evidence → **refuted if** <90%: auto-split drills are not answer-keyable at scale and §3.1's gap stands |
| **PM2** | 3.2 Morphology | Drill items carrying an authoritative answer key / all drill items, with accent-ambiguous cells flagged rather than fabricated | [`attested_drill_items.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/attested_drills/attested_drill_items.tsv) + [`COVERAGE_REPORT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/data/attested_drills/COVERAGE_REPORT.md) | **90.7%** — 40 863 of 45 045 (33 886 `match` + 6 977 `variant`; 4 152 `mismatch` excluded, 30 `no_generation`); mean 7.72 attested cells of 24 | ≥95% across the union with the Talmud Phase-4 bank, 100% of class I/VI and IV/passive cells flagged → **refuted if** the keyed share rises while the flagged share falls: coverage was bought by fabricating keys |
| **PM3** | 3.3 Vocabulary/SRS | Kendall-τ of the published learn-order against raw `rank_all`, plus function words remaining in its top 100 | kosha [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv) + [`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md) | **no corrected order published**; curated `core_rank` vs `rank_all` τ = 0.887; 30 of the top-100 corpus lemmas absent from the curated list (19 indeclinable, 11 pronoun) | a committed learn-order with **0** function words in the top 100 + a reproducible genre-weighting step, τ vs `rank_all` reported → **refuted if** τ ≥ 0.99: the corrections are cosmetic and the order is raw frequency renamed |
| **PM4** | 3.4 Reading | Kendall-τ between predicted passage difficulty and the textbook lesson at which that passage's vocabulary is first fully covered / ≥100 held-out passages | the (unbuilt) scorer over Indische Sprüche (7 537), [RussianRamayana](https://github.com/gasyoun/RussianRamayana), [SamudraManthanam](https://github.com/gasyoun/SamudraManthanam), [`sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json) (3 213 exercise sentences) | **unmeasured** — no scorer; anchors: textbook-vs-frequency τ ≈ 0.05–0.07, textbook-vs-textbook τ 0.446–0.835 | τ ≥ 0.40 **and** ≥50 passages placed at each of B1 and B2 → **refuted if** τ < 0.20: the scorer reproduces frequency or length, not difficulty |
| **PM5** | 3.5 Pāṇini | Form-deriving sūtras for which the concordance returns ≥1 attested corpus form / a fixed sūtra sample | kosha [`CONCORDANCE_ROADMAP.md`](https://github.com/gasyoun/kosha/blob/main/CONCORDANCE_ROADMAP.md) Q4 output × vidyut-prakriya generation × DCS | **unmeasured** — concordance planned, not built | ≥80% resolved, zero-attestation residue published as a count (the RQ3 axis) → **refuted if** <50%: too sparse to teach from, and prakriyā pedagogy must be authored rather than derived |
| **PM6** | 3.6 Zaliznyak on-ramp | Приложение-1 roots in the 4 taught ablaut rows / the whole catalogue — by type **and** by DCS token mass | [`measure_onramp_scope.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/measure_onramp_scope.py) over [`talmud_appendix1.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/talmud_appendix1.json) (745 roots) joined to kosha `lemma_frequency.tsv` via [`sanskrit_util.to_slp1`](https://github.com/sanskrit-lexicon/sanskrit-util/blob/main/py/sanskrit_util/__init__.py) | **56.5% by type** (421/745; 416 of 736 fully tagged) · **56.2% by token mass** (483 532 / 860 159 over the 616 roots that join, 82.7% join rate) — measured 27-07-2026 | quote the transfer figure with its join rate beside every on-ramp completion claim → **refuted if** added rows raise type coverage without raising token coverage: the additions are catalogue padding, not reading-relevant |
| **PM7** | 3.7 Audio | Learner-facing units (akṣara, verse, lesson) with a playable, licence-stamped audio track — an absolute count, not a ratio | none exists | **0** — the field's only zero baseline | ≥1 complete A0 unit (the akṣara set) with a provenance/licence row → **refuted if** audio ships without that row: it counts as 0, because it cannot be published |
| **PM8** | 3.8 Script | Cumulative DCS conjunct-token mass covered by the first 50 conjuncts of the taught order / all conjunct tokens | DCS text × the "most-frequent conjuncts first" order ([PROJECT_INTERLINKS](https://github.com/gasyoun/Uprava/blob/main/PROJECT_INTERLINKS.md)) | **unmeasured** — the order is named, its coverage never computed | ≥90%, published as an ordered list with running coverage → **refuted if** <70%: frequency-first is too weak an ordering to justify the module's sequence |
| **PM9** | 3.9 Metre | Correct automatic metre identifications / ≥200 hand-labelled verses spanning ≥5 metres, reported **per metre**, not macro-averaged | [SanskritKaraoke](https://github.com/gasyoun/SanskritKaraoke) metre trainer + vidyut-chandas, labelled over Indische Sprüche and RussianRamayana verses | **unmeasured** — trainer built, no gold set | ≥95% on the three commonest metres, every mis-ID shipped → **refuted if** <90% on śloka/anuṣṭubh: not auto-gradeable as a drill |
| **PM10** | 3.10 Composition | **Precision** (and recall) of auto-feedback flags / ≥100 hand-labelled real learner sentences | Systema homework + curator review as the label source | **unmeasured** — review is human-only today | precision ≥0.90 at recall ≥0.50, confusion set published → **refuted if** precision <0.80: a false error-flag on a correct form costs more learner trust than a miss, so recall cannot buy it back |
| **PM11** | 3.11 Commentary | Commentary pratīka/lemma anchors resolving automatically to the exact mūla locus / a fixed sample of ≥500 references | [CommentaryStrategies](https://github.com/gasyoun/CommentaryStrategies) + the Sundara apparatus | **unmeasured** | ≥85% auto-resolution, unresolved residue listed, **0** guessed anchors → **refuted if** <60%: the guided interface is a manual-anchoring project, a different cost class |
| **PM12** | 3.12 Spell/error | *Correct* forms the faultfinder flags as errors / ≥5 000 correct learner-level forms (drill-bank gold answers + attested corpus lines) | the §3.12 faultfinder + detectors and `union_headwords`, run over `attested_drill_items.tsv` | **unmeasured** — tuned scholar-facing, learner false-positive rate never measured | ≤2% → **refuted if** >5%: scholar-grade strictness is unusable for learners, confirming §3.12's gap |

**How the register composes with the four RQs (§5).** Each RQ keeps one thing exclusively; the PMs
supply evidence into it and never restate it.

| RQ | What the RQ owns exclusively | PMs that feed it | Why this is not duplication |
|---|---|---|---|
| **RQ1** ordering | the τ methodology and the reading of where orderings diverge | PM3, PM4, PM8 | the PMs *construct and score* candidate orderings; RQ1 evaluates them. No PM re-runs RQ1's own textbook-vs-frequency τ. |
| **RQ2** drill generation | the general falsifiable form — "gold-answer agreement rate" | PM1, PM2, PM5, PM9 | one shared definition, four aspect-specific gold sets and bars. Each PM *instantiates* RQ2 on its own material. |
| **RQ3** textbook-vs-corpus | the per-claim TRUE / OVERSTATED / FALSE verdict (A60) | PM5 (zero-attestation residue), PM2 (`mismatch` cells) | the PMs contribute attestation evidence; the verdict stays A60's and is never pronounced in this register. |
| **RQ4** evaluation | **learning gain and retention — one instrument for the whole field** | *none by design* | **No PM may define a learning-gain or retention metric.** Every aspect claim stays a capability claim until RQ4's protocol measures an outcome. This is the one rule that keeps twelve aspects from growing twelve incompatible rulers. |

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

**The RQs are the field's questions; the §4e metrics are its per-aspect answers-in-progress.**
Four questions cannot report progress on twelve aspects — an aspect can be visibly advancing with
none of the four moving, and RQ4 in particular cannot report anything at all until a study runs.
So §4e gives each aspect one falsifiable capability metric that resolves *today*, and the
composition table there fixes the division of labour: the metrics feed RQ1–RQ3 with evidence, and
they are barred from touching RQ4's learning-gain and retention instrument. Without that bar the
field would accumulate twelve incompatible definitions of "teaches better" — the exact
unfalsifiability RQ4 exists to prevent.

---

## 6. Gap register (honest — so nobody re-derives these)

Each gap below is the target of exactly one §4e metric — the register is this list restated as
numbers with refutation conditions, so "the gap closed" is a measurement, not an impression.

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
- **An aspect without a metric is not admitted.** A new §3.x needs its **PM** row in §4e with all five fields (metric + denominator · data source · today's value · bar · refutation condition), and the metric must target that aspect's own gap. If today's value is genuinely unmeasured, say "unmeasured" — that is a legitimate baseline; a missing refutation condition is not.
- **Never let a PM measure learning gain or retention** — that instrument is RQ4's alone (§4e). An aspect claims capability; only RQ4 claims teaching effect.
- **Update a PM's "today" value in the same pass as the measurement that changed it**, with its date, and keep the superseded number in the metadoc's revision history rather than overwriting it silently.
- **Keep the derived views (§4) pointing at the source maps**, not copying them — when Systema's ladder or index changes, this doc references the change, it does not restate it.
- **Every new learner-facing asset in any repo** earns a row in its aspect here (and a line in the owning repo's own map). Companion metadoc: [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.meta.md).

---

_Dr. Mārcis Gasūns_
