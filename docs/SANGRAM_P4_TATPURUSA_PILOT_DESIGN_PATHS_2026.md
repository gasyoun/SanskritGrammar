# Sangram Pilot P4 (SG-WF-008, tatpuruṣa) — three design paths for the compound-type κ study

_Created: 15-07-2026 · Last updated: 15-07-2026_

> **Provenance.** Drafted by Opus 4.8 (`claude-opus-4-8[1m]`) from a three-agent scout of the
> C5 program, the C3 evidence method, the P2/P3 pilot templates, and the DCS SQLite master.
> Author decision pending: pick one path (or amend). This is a pre-build decision doc — no
> pilot code has been written yet. Handoff: [H989](https://github.com/gasyoun/Uprava/blob/main/handoffs/H989-Opus_SanskritGrammar_sangram-p4-tatpurusa_15.07.26.md).

---

## 1. What P4 tests, and why the design is a real choice

Pilot **P4 = [SG-WF-008](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/toc/data/articles.json)** (детерминативные композиты, tatpuruṣa) is the word-formation pilot that stress-tests evidence-limit **EM4: the compound _type_ is not annotated in DCS**. The corpus marks _that_ a token is a compound member (`token.feat_case = 'Cpd'`) and gives its segmentation, but carries no tatpuruṣa / karmadhāraya / dvandva / bahuvrīhi / avyayībhāva label. So the type has to be classified by hand, and the pilot's job is to measure **whether that classification is reliable enough to publish** — not to assume it is.

The [C5 program](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx) § 7 fixes the kill-gate verbatim:

> Межразметочное согласие двух независимых проходов классификации < 0.7 (Cohen κ) → таксономия типов пересматривается до публикации.

That is the whole reason there is a design choice to make. **κ is not a fixed property of the data — it moves with how fine the codebook is.** A coarse codebook (six top-level classes) will agree more often; a fine one (tatpuruṣa split by case-relation) will agree less. Where we set that dial decides whether the gate passes, and — more importantly — _what the pilot actually proves about EM4_. The three paths below are three positions on that dial.

**Confirmed GO (corpus locator, 15-07-2026):** the data exists at scale — **841 052** `Case=Cpd` members across **396 571** sentences in the pinned master `VisualDCS/src/DCS-data-2026/dcs_full.sqlite` (provenance `source_commit 04e0778`, imported 2026-06-06). EM4 is confirmed hard: the only type-ish signal is UD `compound:coord` (≈ dvandva), which covers 2 214 tokens (0.26 %), lives only in the 3.9 % dependency-parsed subset, and cannot separate tatpuruṣa from karmadhāraya or identify bahuvrīhi at all.

---

## 2. What is identical across all three paths

These are fixed by the C3 contract and the P2/P3 template; only the **codebook** and **sample frame** differ between paths.

| Invariant | Value |
|---|---|
| Corpus | `dcs_full.sqlite` pinned master; opened read-only; refuse to run without the `provenance.source_commit` pin; record file SHA-256 (C3 § 2.1). |
| Compound reconstruction | Group `Case=Cpd` tokens by `sentence_id`, order by `idx`; a maximal `Cpd` run **+ the following inflected head** = one compound. Segmentation from `m_unsandhied`. |
| Sampling | Seeded `random.Random(20260715).sample(...)` over the full universe id-list — never "first N" (rule П3). Record the denominator. |
| Two independent passes | Two annotator agents on **different model tiers**, each blind to the other, same sample + same codebook + same rules → two label vectors. Both are **model-provisional**, flagged for your scholarly sign-off (exactly as P2/P3 framed their single-annotator adjudication). |
| Agreement statistic | Cohen's κ = (p_o − p_e)/(1 − p_e), reported with a bootstrap 95 % CI. Net-new code — no κ template exists in the repo (P1/P2/P3 all used a single-annotator coverage/recall gate). |
| Kill-gate | κ < 0.7 → taxonomy revised before any type distribution is published; the negative result is itself published under rule П7. κ ≥ 0.7 → adjudicate disagreements, publish the determinative distribution with denominator + CI (rules П1/П2). |
| Standing rulings baked into the codebook | Samāsa parsed **right-to-left** (tatpuruṣa head = right member; dvandva is the coordinate exception); compound structure counted in **lemmas, not letters**. |
| Article shape | `sangram/articles/tatpurusha/{index.mdx (7-section + candidate banner), article.manifest.json (revisions: [] until visa), data/}`; three validators + `npm run build` green; CHANGELOG `[0.21.0]`; candidate → author-visa → published lifecycle. |

**Repo taxonomy conventions to honour** (from the C2 registry, unless a path revises them): karmadhāraya is folded _inside_ the SG-WF-008 tatpuruṣa slot; **dvigu** is parked in SG-WF-010 with avyayībhāva, _not_ under tatpuruṣa (a departure from the Pāṇinian arrangement — and exactly the kind of boundary the kill-gate can flag for revision).

---

## 3. Path A — Coarse-robust

**Codebook (7 labels, one tier):** `tatpuruṣa` · `karmadhāraya` · `dvandva` · `bahuvrīhi` · `avyayībhāva` · `dvigu` · `unclear`. No sub-splitting of tatpuruṣa.

**Sample frame:** 2-member compounds only (exactly one `Cpd` member + one inflected head), seeded **n = 120**. Isolates type-classification from recursive bracketing.

**κ computed:** a single κ over the 7-way label.

**Kill-gate reading:** pass if κ ≥ 0.7 → publish the coarse type distribution, headlining the determinative (tatpuruṣa + karmadhāraya) share as the SG-WF-008 content.

**Expected outcome (honest estimate):** κ ≈ 0.70–0.85. Tatpuruṣa-vs-dvandva-vs-avyayībhāva is fairly agreeable from member lemmas; **bahuvrīhi is the weak spot** (exocentric — genuinely undecidable from segmentation without external agreement, which is C6 territory), so most disagreement concentrates there. Likely **passes**.

**What publishes:** a clean coarse distribution for the determinative slice — a positive result.

**Effort:** lowest (one small codebook, one κ). **Risk:** may pass "too easily" and thereby _under-test_ EM4 — a coarse pass doesn't prove the type is recoverable at the granularity a grammar actually needs, so the scientific contribution is thinnest.

---

## 4. Path B — Two-tier κ  ·  recommended

**Codebook (two tiers):**
- **Tier 1 (coarse):** the 7-label set from Path A.
- **Tier 2 (fine), applied only to items both passes called tatpuruṣa/karmadhāraya:** the case-relation split — `tat-acc (dvitīyā)` · `tat-ins (tṛtīyā)` · `tat-dat (caturthī)` · `tat-abl (pañcamī)` · `tat-gen (ṣaṣṭhī)` · `tat-loc (saptamī)` · `karmadhāraya (samānādhikaraṇa)` · `nañ-tatpuruṣa (a-/an-)` · `upapada` · `unclear`.

**Sample frame:** 2-member compounds only, seeded **n = 120** (same as A).

**κ computed:** **two** — κ_coarse (7-way) and κ_fine (case-relation, over the tatpuruṣa subset).

**Kill-gate reading:** the gate can **pass coarse and fail fine** — and that split _is the finding_. "Coarse κ = 0.81 (type recoverable at class level); fine κ = 0.58 (vibhakti relation not recoverable from surface segmentation) → the fine sub-taxonomy is revised before publication" directly discharges the kill-gate's mandate ("таксономия типов пересматривается до публикации") with evidence for exactly which boundary fails.

**Expected outcome:** κ_coarse ≈ 0.75–0.85 (pass); κ_fine ≈ 0.50–0.65 (fail). The genitive (ṣaṣṭhī) tatpuruṣa is a huge attractor and the case-relation is often ambiguous on the surface, so fine agreement should genuinely struggle.

**What publishes:** a two-layer result — a publishable coarse distribution _and_ an honest "the case-relation layer is not corpus-recoverable" negative, with the neighbor-class confusion matrix showing where the two annotators diverge. Richest EM4 picture of the three.

**Effort:** medium (same scripts, two κ, a slightly richer article). **Risk:** none material; it is the most defensible and the one that best serves the gate's stated purpose.

---

## 5. Path C — Fine-adversarial

**Codebook (one tier, fine):** the full case-relation split of tatpuruṣa (as Path B tier 2) plus the neighbor classes, with **no coarse fallback** — every item gets a fine label.

**Sample frame:** includes **multi-member** compounds, classifying the outermost (right-most) binary split per the samāsa right-to-left ruling, seeded **n = 120**. More representative of real Sanskrit compounding.

**κ computed:** a single κ over the full fine label space.

**Kill-gate reading:** most likely κ < 0.7 → honest negative + taxonomy revision, the P3-style result.

**Expected outcome:** κ ≈ 0.50–0.65 — **most likely fails**, giving the strongest EM4-confirming statement: "compound type is not reliably classifiable at fine granularity on DCS segmentation alone."

**What publishes:** a strong negative — but no usable type distribution for the SG-WF-008 slot content.

**Effort:** medium-high (adds multi-member bracketing logic). **Risk (important):** with multi-member items, a κ failure **conflates two different causes** — annotators may disagree because the _type_ is ambiguous _or_ because the _bracketing_ is ambiguous. That confound is exactly what Path B's 2-member restriction removes, so a Path C failure is scientifically muddier: it can't cleanly attribute the low κ to EM4.

---

## 6. Side-by-side

| Dimension | A — Coarse-robust | B — Two-tier ✅ | C — Fine-adversarial |
|---|---|---|---|
| Codebook | 7 top-level classes | 7 coarse + case-relation fine | fine only |
| Sample | 2-member, n=120 | 2-member, n=120 | multi-member, n=120 |
| κ reported | 1 (coarse) | 2 (coarse + fine) | 1 (fine) |
| Likely verdict | pass | coarse pass / fine fail | fail |
| Publishes | coarse distribution | distribution **+** where fine breaks | negative only |
| Serves the "revise taxonomy" mandate | weakly | **directly** | yes, but muddied |
| Confound risk | low | none | bracketing-vs-type |
| Effort | low | medium | medium-high |

---

## 7. Recommendation and what I need from you

**Recommended: Path B.** It is the only path whose _designed_ outcome is the thing the kill-gate exists to produce — a precise statement of which taxonomic boundary the corpus can and cannot support — and it avoids Path C's bracketing/type confound while still delivering a publishable determinative distribution if the coarse tier holds.

Two sub-decisions are yours regardless of path, because they are scholarly boundary calls, not engineering ones:

1. **karmadhāraya placement** — keep it folded _inside_ SG-WF-008 (repo convention, and what the slot title says), or treat it as a distinct coarse class the annotators must separate from case-tatpuruṣa? (Folding-in raises κ; separating tests a real boundary.)
2. **dvigu placement** — leave it in SG-WF-010 as the registry has it, or pull it under tatpuruṣa the Pāṇinian way for this pilot? (If annotators keep splitting dvigu vs numeral-karmadhāraya, that disagreement is itself a kill-gate signal.)

And one optional anchor: if you want the codebook's definitions pinned to a specific authority — **Whitney §1246–1316**, **Bühler's compound lessons**, or **Apte 1885** — name it and I will quote the type definitions from there into the annotator codebook rather than use a neutral synthesis.

Once you pick a path (and rule on 1–2), I build: `scripts/sg_wf_008_compound_sample.py` → the two-pass κ workflow → `scripts/sg_wf_008_kappa.py` → the candidate article, validators + build green, CHANGELOG, PR on `feat/sangram-p4-tatpurusa`.

_Dr. Mārcis Gasūns_
