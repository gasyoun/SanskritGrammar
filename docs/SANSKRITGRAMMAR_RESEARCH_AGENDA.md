# SanskritGrammar research agenda — hypotheses, visualisations, and the ACL crosswalk

_Created: 10-07-2026 · Last updated: 10-07-2026_

**Provenance:** authored by Fable 5 (`claude-fable-5`) executing
[H450](https://github.com/gasyoun/Uprava/blob/main/handoffs/H450-Fable_SanskritGrammar_dh_memo_research_agenda_10.07.26.md)
via [`/dh-memo`](https://github.com/gasyoun/claude-config/blob/main/commands/dh-memo.md), on the plan in
[`ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md)
(Opus 4.8 `claude-opus-4-8`, 10-07-2026). The roadmap is the **plan**; this memo is the **agenda**:
the numbered, falsifiable hypotheses and the visualisation specs the plan calls for but does not
contain. Memo-only — nothing here was built, run, or derived this session.

**ID scheme.** No hypothesis registry existed in this repo before this memo. Hypotheses are minted
here as `SG-H1…SG-H9` and visualisations as `SG-V1…SG-V6`; future sessions cite these IDs. "Nearest
existing" anchors point at the roadmap's quarter items (`Q3.2` etc.), the settled memos
([`MORPHOCLASS_3WAY_MEMO.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.md),
[`MORPHOCLASS_COMPARISON_ROADMAP.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_COMPARISON_ROADMAP.md),
[`ZALIZNYAK_1975_1978_2004_COMPARISON.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNYAK_1975_1978_2004_COMPARISON.md)),
and committed data caveats — the closest prior claims this repo actually holds.

---

## 1. Executive summary

The five highest-leverage moves, in order:

1. **Compute Kendall's τ over the shared-exercise clusters** (SG-H1/SG-H2, viz SG-V1) — the one
   analysis that converts the concordance from a curiosity into a result, runs on committed data
   this quarter, and seeds Paper 1. _[measure-now layer]_
2. **Evaluate the existing `difflib` detector against the 128 labeled pairs** (SG-H4) — the gold
   set already exists; scoring the current pipeline before replacing it is the cheapest publishable
   rigor upgrade in the repo. _[measure-now layer]_
3. **Krippendorff α over the three morphoclass schemes as three coders** (SG-H5) — quantifies where
   Zaliznyak 1975 / Gasūns 2014 / Tolchelnikov 2026 actually disagree, on data already joined over
   876 roots; the precondition for the Paper 2 adjudication framing (SG-H6). _[measure-now layer]_
4. **Difficulty-ramp curves from surface proxies** (SG-H9, viz SG-V5) — 3,213 sentences with lesson
   numbers make "do the textbooks agree on how fast to get harder?" testable today, with honest
   no-Sanskrit-readability-model caveats. _[measure-now layer]_
5. **Surface the two orphaned data layers** — the phonostatistics CSVs (SG-V6) and the
   subject-coverage matrix as a real heatmap (SG-V2) — committed since H246/H325, rendered nowhere.
   _[surface layer]_

Everything else (directionality SG-H3, corpus adjudication SG-H6, the Pāṇini pilot SG-H7) is
specified below with its gate named. Nothing in this memo requires a new derivation to start;
items that later need one say which repo owns it.

---

## 2. New testable hypotheses

Format per entry: claim · data (+ join key) · method (+ ACL precedent) · expected output ·
research read · learner read · nearest existing + delta · readiness.

### SG-H1 — The German-tradition pair agrees on order; the 1998 Russian textbook does not

**Claim.** Kendall's τ between lesson orders of shared exercises is substantially higher for
Bühler↔Knauer (n=79 clusters) than for Bühler↔Kochergina (n=33): τ(B↔K) − τ(B↔Ko) > 0.2, with
bootstrap 95% CIs excluding zero difference.
**Data.** [`scripts/data/catalog.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/catalog.csv)
(124 clusters, columns `buhler_lessons`/`knauer_lessons`/`kochergina_lessons`); no join needed.
**Method.** Kendall's τ with bootstrap CIs — Lapata 2006, *Computational Linguistics*
([J06-4002](https://aclanthology.org/J06-4002/)), the standard ACL treatment of τ for order
comparison. First occurrence per book where a cluster spans lessons.
**Expected output.** One table (τ per book pair + CI) and the slope graph SG-V1.
**Research read.** First quantified claim about curriculum inheritance across the
German → Russian Sanskrit-teaching tradition; the headline number of Paper 1.
**Learner read.** "If I switch textbooks mid-course, how far off will the order be?" — a
practical compatibility score between books.
**Nearest existing + delta.** Roadmap Q3.2 mandates *computing* τ; the delta is the directional,
falsifiable claim (which pair agrees more, by how much, with CIs) — Q3.2 states no expectation.
**Readiness.** ✅ Runs today on committed data.

### SG-H2 — Inherited exercises migrate deeper into the course

**Claim.** Within shared clusters, the *normalized* lesson position (lesson ÷ total lessons of that
book) is systematically later in Kochergina 1998 than in Bühler 1923: paired Wilcoxon signed-rank
over the 33 B↔Ko clusters rejects the null at p < .05, median shift ≥ +0.05.
**Data.** Same [`catalog.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/catalog.csv)
plus per-book lesson counts derivable from
[`scripts/data/sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json)
(3,213 sentences, `book` × `lesson`).
**Method.** Paired Wilcoxon on normalized positions. No direct ACL precedent for the *positional
drift* claim itself; the order-analysis frame is Lapata 2006 ([J06-4002](https://aclanthology.org/J06-4002/)).
This is a position claim, **not** a borrowing-direction claim — it stands regardless of who copied whom.
**Expected output.** Paired dot-plot (before/after normalized position per cluster) + test table.
**Research read.** Evidence that later textbooks accrete new introductory material in front of
inherited exercises — a measurable "curriculum sedimentation" effect.
**Learner read.** "The classics come later in the modern book" — explains why a 1998 course feels
slower to reach the same sentences.
**Nearest existing + delta.** The `earliest_book`/`earliest_year` columns of `catalog.csv` record
*that* clusters recur; the delta is a signed positional statistic over them.
**Readiness.** ✅ Runs today.

### SG-H3 — Borrowing direction is recoverable without labels ⚠ gated on D4

**Claim.** RefD — the unsupervised asymmetric reference-distance metric — applied over shared
clusters and their surrounding lesson vocabulary assigns Bühler→Knauer directionality consistent
with publication order for ≥70% of the 79 shared clusters.
**Data.** `catalog.csv` + `sentences.json` (lesson-context vocabulary); no external join.
**Method.** RefD, Liang et al. 2015, EMNLP ([D15-1193](https://aclanthology.org/D15-1193/)) —
prerequisite directionality without training labels; archetype-reconstruction as the only other
ACL-adjacent anchor: Hoenen 2015, NAACL ([N15-1127](https://aclanthology.org/N15-1127/)). Mature
directionality machinery lives in DSH/textual criticism, not ACL — Paper 1 must say so, not overclaim.
**Expected output.** Directed graph over the three books, edge confidence per cluster.
**Research read.** A rare NLP-side test of stemmatic intuition on printed pedagogy.
**Learner read.** None on its own — cut from learner-facing pages; feeds the timeline SG-V4 caption.
**Nearest existing + delta.** Roadmap Q4.5 schedules RefD; the delta is the ≥70%-consistency
threshold that makes it falsifiable.
**Readiness.** ⚠ **Gated on `@DO D4`** (the repo holds the 1923 Stockholm reprint as a proxy for
the 1878 Bühler first edition, unverified — [Concordance caveat](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx);
Knauer 1908 is *earlier* than the reprint we hold). **Fallback:** run the metric, publish the order
comparison (SG-H1/H2), draw **no arrow** until D4 clears.

### SG-H4 — The current detector leaves ≥15% recall on the table

**Claim.** Against the frozen 128-pair gold, a TRACER-style smaller-chunk fuzzy matcher raises
recall on true variant pairs (`spelling_variant`, n=58) by ≥15 points over the current
`difflib.SequenceMatcher` pipeline at equal or better precision.
**Data.** [`scripts/data/matches_review.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/matches_review.tsv)
(128 pairs, human `verdict`: 58 spelling_variant · 50 low_similarity · 20 length_mismatch) as the
frozen gold; candidates from `sentences.json`.
**Method.** Text-reuse detection with chunk-size tuning — TRACER validated *on Sanskrit* by
Miyagawa et al. 2024, NLP4DH ([2024.nlp4dh-1.12](https://aclanthology.org/2024.nlp4dh-1.12/)),
whose finding that smaller chunks raise recall is the directly reusable knob. Report P/R/F1
against the frozen gold.
**Gold-sample caveat.** The verdicts are **single-annotator** (H327 review pass). Per the standing
constraint no second annotator exists and recruitment is parked for 2026 — so this gold is used as
single-annotator + adjudicated re-pass, **no κ claimed**. The paper reports it as such.
**Expected output.** P/R/F1 table difflib vs TRACER-style, per chunk size; new clusters found.
**Research read.** A clean detector-evaluation result on a Sanskrit pedagogical corpus — exactly
the evaluation the 124-cluster catalog currently lacks.
**Learner read.** More shared sentences found ⇒ a richer "this exercise also appears in…" cross-link
layer on the concordance pages.
**Nearest existing + delta.** H327 *classified* the 128 near-matches; the delta is using them as an
evaluation benchmark to score detectors — no detector has ever been scored here.
**Readiness.** ✅ Gold and candidates committed; only the alternative detector run is new compute.

### SG-H5 — Morphoclass disagreement concentrates in the Zipfian tail

**Claim.** Pairwise and three-way chance-corrected agreement (Krippendorff α) between Zaliznyak
1975, Gasūns 2014, and Tolchelnikov 2026 — treated as three coders of the same 876 roots — is
high overall (α > 0.7) but drops by ≥0.15 in the lowest corpus-frequency band relative to the
highest: the schemes agree where the corpus gives evidence, and diverge where it doesn't.
**Data.** [`morphoclass_crosswalk_1975_2014_2026.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv)
(876 roots × `ryad_derived`/`z_series`/`z_set`); frequency stratification needs the
**whitney_no ↔ DCS lemma join** (roadmap Q4.4) — corpus counts are owned by
[VisualDCS](https://github.com/gasyoun/VisualDCS) (consume, never re-derive).
**Method.** α with bootstrap CIs — Artstein & Poesio 2008, *Computational Linguistics*
([J08-4004](https://aclanthology.org/J08-4004/)). **Sparsity guard:** 876 roots against Zipfian DCS
counts leaves many roots too rare for per-root estimates — pool into frequency *bands* (e.g.
quartiles of DCS lemma count) as the rare-root back-off and report per-band α with CIs, never
per-root point values.
**Expected output.** α per scheme pair (whole set) + α per frequency band (chart SG-V3 companion).
**Research read.** The first quantification of *where* three expert classifications of the same
root list disagree — the empirical base of Paper 2.
**Learner read.** "Which roots are settled and which are contested" — a per-root confidence badge
for the Talmud pages.
**Nearest existing + delta.** [`MORPHOCLASS_3WAY_MEMO.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.md)
argues the lineage and lists per-root divergences qualitatively; the delta is chance-corrected
agreement + the frequency-conditioning claim, neither of which the memo computes.
**Readiness.** ◐ Whole-set α runs today; the frequency bands wait on the Q4.4 join (VisualDCS boundary).

### SG-H6 — The corpus prefers a scheme, and it is measurable

**Claim.** On the disagreement subset from SG-H5, mutual information between scheme label and
corpus-attested inflectional behavior (present-system stem distribution; seṭ/aniṭ-relevant forms)
is highest for one scheme, and the ranking is stable under bootstrap (same winner in ≥80% of
resamples). Which scheme wins is deliberately *not* predicted — the decision procedure is the contribution.
**Data.** The 876-root crosswalk + DCS form counts (Q4.4 join, VisualDCS-owned) + surface forms
generated with sūtra provenance by [vidyut-prakriya](https://github.com/ambuda-org/vidyut) (MIT;
Prasad 2024, ISCLS — [2024.iscls-1.7](https://aclanthology.org/2024.iscls-1.7/)). DCS spine:
Hellwig & Nehrdich 2018 ([D18-1295](https://aclanthology.org/D18-1295/)) · ByT5-Sanskrit 2024
([2024.findings-emnlp.805](https://aclanthology.org/2024.findings-emnlp.805/)).
**Method.** MI between class label and form/meaning — Williams et al. 2020, ACL
([2020.acl-main.597](https://aclanthology.org/2020.acl-main.597/)); scheme-complexity companion
via inflection-class entropy — Cotterell et al. 2019, *TACL*
([tacl_a_00271](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00271/43492/)). Same
frequency-band back-off and CI discipline as SG-H5.
**Expected output.** MI-per-scheme table with CIs; the Paper 2 core figure.
**Research read.** The verified novelty: **no ACL/CL paper adjudicates two or more rival expert
classifications of the same lemma set against corpus evidence** (every precedent predicts or
induces *one* scheme). This hypothesis is that framing, made operational.
**Learner read.** "Which classification should a student learn?" gets an evidence-based answer —
or an honest "the corpus can't tell" if MI differences vanish under CIs (also publishable).
**Nearest existing + delta.** Roadmap S2 names the missing "decision procedure for which scheme
the data prefers"; the delta is naming the estimator (MI), the tie-breaker (bootstrap stability),
and the failure mode (CIs overlap ⇒ negative result).
**Readiness.** ⚠ Gated on the Q4.4 crosswalk (net-new derived asset; register in
[`PROJECT_INTERLINKS.md`](https://github.com/gasyoun/Uprava/blob/main/PROJECT_INTERLINKS.md) + the
[kosha manifest](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json) when built).

### SG-H7 — Sandhi aligns to Pāṇini more readily than the aorist ⚠ pilot-gated

**Claim.** In the two-chapter pilot, sūtra-retrieval precision@5 for Whitney's sandhi chapter
(ch. III, §§98–260) exceeds that for the aorist chapter (ch. XI, §§824–930) by ≥0.15 — descriptive
phonology maps onto Pāṇinian rule IDs more directly than tense-system morphology.
**Data.** [`WhitneyGrammar_1889/`](https://github.com/gasyoun/SanskritGrammar/tree/main/WhitneyGrammar_1889)
(1,316 §, chapter files committed); candidate sūtras via vidyut-prakriya's emitted provenance
([2024.iscls-1.7](https://aclanthology.org/2024.iscls-1.7/)) + the existing lookup harness
[`panini_sutra.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/panini_sutra.py)
with its `panini_cache/` (already used to verify 2 citations in H415).
**Method.** Retrieval evaluation over a **frozen gold sample of 30 §** (15 per chapter),
single-annotator + adjudicated re-pass, **no κ claimed** (no second annotator exists). Verified
gap: no ACL paper aligns Western descriptive grammar statements to Pāṇinian sūtra IDs — net-new,
and correspondingly risky.
**Kill-gate (inherited from the roadmap, restated as part of the hypothesis).** If precision@5 on
the *sandhi* chapter is < 0.4 after tuning, the hypothesis is dead and the pilot stops with a
written negative result. Do not extend to 18 chapters on hope.
**Expected output.** precision@5 per chapter; error taxonomy of misalignments.
**Research read.** Even the comparative claim (phonology > morphology alignability) is new; the
negative result is publishable as a scoping finding for grammar-alignment work.
**Learner read.** Aligned §↔sūtra pairs become "what Pāṇini says here" side-notes on Whitney pages.
**Nearest existing + delta.** Roadmap Q2-2027 pilot defines the task + kill-gate; the delta is the
*comparative* two-chapter claim, which turns a build item into a falsifiable hypothesis.
**Readiness.** ⚠ Q2 2027 by plan; harness committed, gold sample and retrieval loop are new work.

### SG-H8 — The varga-share negative result holds and is worth exhibiting (S4: viz, no paper)

**Claim.** The already-computed association between varga category and text type is negligible
(Cramér's V = 0.037) and will remain < 0.1 under any reasonable re-binning of the committed tables —
a stable negative result.
**Data.** [`varga_shares.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/varga_shares.csv)
and the 5 sibling CSVs in
[`revision-2026/`](https://github.com/gasyoun/SanskritGrammar/tree/main/GasunsDhatu_2014/revision-2026).
**Method.** Re-binning robustness check only (V under 2–3 alternative groupings). Verified: **no
ACL precedent** for varga-share stylometry; the natural venue would be DSH/CHR — per the roadmap,
S4 gets **no paper**, at most a viz (SG-V6).
**Expected output.** SG-V6, annotated with V = 0.037.
**Research read.** An honestly-surfaced negative result in the Dhātu monograph's digital afterlife.
**Learner read.** "Sound-class proportions don't distinguish these texts" — a myth-buster panel.
**Nearest existing + delta.** V = 0.037 is already in Табл. 5 of the monograph revision (H246);
the delta is only the robustness check + surfacing. Deliberately starved, per the handoff.
**Readiness.** ✅ Data committed; check is trivial.

### SG-H9 — The textbooks disagree on how fast to get harder

**Claim.** Surface-proxy difficulty (sentence length in aksharas; type/token novelty per lesson)
increases with lesson number in all three books (Spearman ρ > 0.5 each), but the *slopes* differ:
Kochergina's ramp is the shallowest of the three, i.e. its final-quartile exercises are closest to
its own median difficulty.
**Data.** [`sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json)
(3,213 sentences with `book`, `lesson`, `text`, `script`); syllable methodology precedent already
in-repo ([`syllables_per_word.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/syllables_per_word.csv)).
**Method.** Difficulty-progression methodology (English-trained, method only): Arase et al. 2022,
EMNLP ([2022.emnlp-main.416](https://aclanthology.org/2022.emnlp-main.416/)); framing from
competence-based curriculum learning — Platanios et al. 2019, NAACL
([N19-1119](https://aclanthology.org/N19-1119/)) — where the difficulty-vs-competence schedule is
exactly what a textbook's lesson sequence encodes. **Honesty constraint** from the readability
survey (Vajjala 2022, LREC — [2022.lrec-1.574](https://aclanthology.org/2022.lrec-1.574/)): no
Sanskrit-trained readability model exists, so only surface proxies are claimed, named as such.
**Expected output.** Difficulty-vs-lesson curves per book (SG-V5) + slope table with CIs.
**Research read.** First quantitative comparison of pacing across the Sanskrit teaching tradition;
a curriculum-learning reading of 19th–20th-century pedagogy.
**Learner read.** Directly answers "which textbook ramps gently?" — arguably the single most
useful number this repo can give a beginner.
**Nearest existing + delta.** Nothing in-repo measures difficulty at all; nearest is the
syllables-per-word phonostatistics (different corpus, different question). Delta: entire claim.
**Readiness.** ✅ Runs today on committed data.

**Spine coverage check:** S1 → SG-H1, H2, H3, H4, H9 · S2 → SG-H5, H6 · S3 → SG-H7 · S4 → SG-H8. ✅

---

## 3. Visualisation proposals

The repo's stack is Docusaurus MDX (auto-registered `bookDirs`,
[`docusaurus.config.mjs`](https://github.com/gasyoun/SanskritGrammar/blob/main/docusaurus.config.mjs))
with the `rst-table` remark plugin; charts land as React components or build-time-generated SVG
inside `.mdx` pages — no external chart service, per the site's zero-backend constraint.

### SG-V1 — Shared-exercise slope graph (upgrade: Concordance page) — effort M

**Page.** Upgrade [`Concordance/catalog.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx).
**Data.** [`catalog.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/catalog.csv);
loader: build-time script emitting JSON, imported by an MDX React component.
**Chart.** Slope graph: one line per shared cluster, x = book (Bühler 1923 · Knauer 1908 ·
Kochergina 1998), y = normalized lesson position. τ from SG-H1 annotated per pair.

```
norm.
lesson  Bühler        Knauer        Kochergina
 1.0 ┤    ●━━━━━━━━━━━━━●
     │      ●━━━━━━╲
 0.5 ┤   ●━━━━━━━━━━╲━━━●            ● (33 B↔Ko lines)
     │    ●━━━━━━━━━━╲━━━━━━━━━━━━━━━●
 0.0 ┤                ●━━━━━━━━━━━━━━●
     └── τ(B↔K)=0.xx ──── τ(B↔Ko)=0.xx ──
```

**Research read.** The Paper 1 figure — order agreement and its exceptions at a glance.
**Learner read.** Hover a line → the sentence text + "appears in lesson 12 (B) / 14 (K)".

### SG-V2 — Subject-coverage heatmap (upgrade: SubjectConcordance) — effort M

**Page.** Upgrade [`SubjectConcordance/catalog.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/SubjectConcordance/catalog.mdx),
whose 9 works × 18 Whitney chapters + 41 fine categories currently render as a wall of table rows —
**a committed-but-unsurfaced layer** in exactly the sense this memo must cover.
**Data.** The matrix already embedded in the page (regenerate via
[`scripts/build_subject_concordance.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_subject_concordance.py)).
**Chart.** Heatmap, works × chapters, cell shade = coverage strength; a toggle to the 41
fine categories.

```
              Ch: 01 02 03 04 05 06 07 08 09 10 11 …
Bühler 1923      ██ ██ ▓▓ ██ ▓▓ ░░ ▓▓ ██ ██ ░░ ░░
Knauer 1908      ██ ▓▓ ▓▓ ██ ██ ░░ ▓▓ ██ ▓▓ ░░ ░░
Kochergina 1998  ██ ██ ██ ██ ▓▓ ▓▓ ██ ██ ██ ▓▓ ░░
Whitney 1889     ██ ██ ██ ██ ██ ██ ██ ██ ██ ██ ██
```

**Caveat carried visibly:** the matrix is a keyword-lexicon first pass, self-described as *"a
finding-aid, not an authority"* — the heatmap legend must say so until roadmap Q3.3 scores it.
**Research read.** Coverage gaps per tradition (what the Russian textbooks never teach) become
visible; feeds the Q3.3 scoring design.
**Learner read.** "Which book covers the aorist at all?" answered in one glance.

### SG-V3 — Morphoclass three-scheme alluvial (new page) — effort L

**Page.** New `TolchelnikovTalmud_2026/morphoclass-flows.mdx` (spec only; not built this session).
**Data.** [`morphoclass_crosswalk_1975_2014_2026.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv).
**Chart.** Alluvial/Sankey: 876 roots flowing Zaliznyak-1975 series → Gasūns-2014 Ряд →
Tolchelnikov-2026 class; ribbons that split or cross = the disagreement mass SG-H5 quantifies.
Low-`ryad_conf` rows rendered hatched.

```
 Zal.1975        Gas.2014        Tol.2026
 series I ████━━━━█ Ряд 1 ███━━━━━█ I ███
 series II ███━━┓ ┌█ Ряд 2 ██━━┓ ┌━█ II ██
              ┗━╳━┛            ┗━╳━┛        ← crossings = disagreement
 series III ██━┛ ┗━█ Ряд 4 █━━━┛ ┗━━█ IV █
```

**Research read.** The Paper 2 motivation figure — where the α of SG-H5 lives, visibly.
**Learner read.** Click a ribbon → root list with glosses; a student sees which "hard" roots are
hard because the experts themselves disagree.

### SG-V4 — Edition timeline with proxy-status markers (new section on the site index) — effort S

**Page.** Add to [`src/pages/index.js`](https://github.com/gasyoun/SanskritGrammar/blob/main/src/pages/index.js)
(or a new `docs/` landing `.mdx`) — the memo's mandatory **diachronic view**.
**Data.** Edition metadata already in [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/README.md)
and folder names (1885 · 1889 · 1908 · 1923 (proxy for 1878!) · 1975 · 1978 · 1998 · 2004 · 2014 · 2026).
**Chart.** Horizontal timeline; each edition a node; **the Bühler node carries a visible ⚠
"1923 reprint held as unverified proxy for 1878 — D4 open"** so the repo's highest-severity data
caveat is surfaced on the site instead of buried in a catalog footnote.

```
1878?…1885───1889───1908──1923⚠────1975──1978────1998──2004───2014────2026
 Bühler Apte Whitney Knauer Bühler  Zal.  Zal.   Koch.  Zal.  Gasūns  Tol.
 (1st)               (repr., proxy)
```

**Research read.** The chronology every directionality claim depends on, stated once, correctly.
**Learner read.** Orientation: what these ten books are and when they're from.

### SG-V5 — Difficulty-ramp curves (new page under Concordance) — effort M

**Page.** New `Concordance/difficulty.mdx` (spec only).
**Data.** [`sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json);
loader shared with SG-V1.
**Chart.** Line chart per book: x = normalized lesson, y = surface-proxy difficulty (akshara
length; lesson type/token novelty), smoothed, with the SG-H9 slope table beneath. Legend states
the Vajjala-2022 caveat: surface proxies, no Sanskrit readability model exists.

```
diff.
  ▲        ╭─── Bühler
  │    ╭───╯╭── Knauer
  │ ╭──╯╭───╯
  │─╯╭──╯  ╭──────── Kochergina (shallowest?)
  │──╯─────╯
  └──────────────────▶ lesson (normalized)
```

**Research read.** SG-H9's figure.
**Learner read.** The gentlest-ramp answer, visually.

### SG-V6 — Phonostatistics negative-result exhibit (new section in the Dhātu revision pages) — effort S

**Page.** Add a section to the existing
[`GasunsDhatu_2014/revision-2026/`](https://github.com/gasyoun/SanskritGrammar/tree/main/GasunsDhatu_2014/revision-2026)
book pages — the second **orphaned/committed-but-unsurfaced dataset** view: 6 CSVs committed since
H246, rendered nowhere on the site.
**Data.** [`varga_shares.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/varga_shares.csv)
+ [`table2_rigveda_clusters.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/table2_rigveda_clusters.csv)
+ [`table3_ramayana_clusters.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/table3_ramayana_clusters.csv).
**Chart.** Small-multiple bars: varga shares side-by-side per text type, annotated
**"Cramér's V = 0.037 — no association"** (SG-H8).
**Research read.** A negative result, exhibited instead of hidden — DH best practice.
**Learner read.** Sound-class proportions are stable across texts; don't let anyone tell you otherwise.

---

## 4. ACL-Anthology method crosswalk

12 citations verified by live fetch on 10-07-2026 (roadmap session, Opus 4.8 `claude-opus-4-8`);
2 more (marked ★) live-fetched this session by Fable 5 (`claude-fable-5`). All 14 clickable and
confirmed to exist. "Now" = applies to committed data as-is; "derive" = needs the named derivation.

| Method | ACL paper(s) | Applies to (dataset) | Enables | Nearest the repo does today (gap delta) | Now/derive |
|---|---|---|---|---|---|
| Kendall's τ order comparison | Lapata 2006 — [J06-4002](https://aclanthology.org/J06-4002/) | [`catalog.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/catalog.csv) | SG-H1/H2, SG-V1 | Catalog lists shared clusters; **no order statistic ever computed** | now |
| Topological sort → consensus curriculum | Prabhumoye et al. 2020 — [2020.acl-main.248](https://aclanthology.org/2020.acl-main.248/) | `catalog.csv` pairwise orders | consensus-order layer for SG-V1 | nothing — net-new | now |
| RefD asymmetric prerequisite metric | Liang et al. 2015 — [D15-1193](https://aclanthology.org/D15-1193/) | `catalog.csv` + `sentences.json` | SG-H3 (directionality, D4-gated) | no directionality signal at all | now (claim gated) |
| Text reuse w/ chunk tuning, Sanskrit-validated | Miyagawa et al. 2024 — [2024.nlp4dh-1.12](https://aclanthology.org/2024.nlp4dh-1.12/) | [`matches_review.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/matches_review.tsv) gold + `sentences.json` | SG-H4 | `difflib.SequenceMatcher`, never evaluated | now |
| Stemma/archetype reconstruction | Hoenen 2015 — [N15-1127](https://aclanthology.org/N15-1127/) | shared clusters | SG-H3's honest precedent framing | — (weak precedent; DSH owns the machinery — say so) | now |
| κ/α agreement methodology | Artstein & Poesio 2008 — [J08-4004](https://aclanthology.org/J08-4004/) | [`morphoclass_crosswalk_1975_2014_2026.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv) | SG-H5 | unquantified `ryad_conf` column + prose divergence lists | now (bands: derive) |
| MI: does the label predict behavior | Williams et al. 2020 — [2020.acl-main.597](https://aclanthology.org/2020.acl-main.597/) | crosswalk + DCS counts | SG-H6 (Paper 2 core) | nothing — the adjudication framing is the verified ACL gap | derive (Q4.4 join) |
| Inflection-class entropy | Cotterell et al. 2019 — [tacl_a_00271](https://direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00271/43492/) | crosswalk | scheme-complexity companion to SG-H6 | — | derive |
| Sūtra-provenanced derivation (vidyut) | Prasad 2024 — [2024.iscls-1.7](https://aclanthology.org/2024.iscls-1.7/) | [`WhitneyGrammar_1889/`](https://github.com/gasyoun/SanskritGrammar/tree/main/WhitneyGrammar_1889) + [`panini_sutra.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/panini_sutra.py) | SG-H7 pilot; SG-H6 surface forms | harness verified 2 citations (H415) — no retrieval loop | derive (pilot) |
| Sanskrit segmentation / DCS corpus spine | Hellwig & Nehrdich 2018 — [D18-1295](https://aclanthology.org/D18-1295/) · ByT5 2024 — [2024.findings-emnlp.805](https://aclanthology.org/2024.findings-emnlp.805/) | DCS counts (VisualDCS-owned) | frequency bands for SG-H5/H6 | none in-repo — **boundary: consume from VisualDCS** | derive (Q4.4) |
| Difficulty-progression methodology | Arase et al. 2022 — [2022.emnlp-main.416](https://aclanthology.org/2022.emnlp-main.416/) | [`sentences.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/sentences.json) | SG-H9, SG-V5 | nothing measures difficulty | now |
| ★ Competence-based curriculum learning | Platanios et al. 2019 — [N19-1119](https://aclanthology.org/N19-1119/) | `sentences.json` lesson sequences | SG-H9's framing: a textbook *is* a difficulty schedule | — | now |
| ★ Readability-assessment limits (survey) | Vajjala 2022 — [2022.lrec-1.574](https://aclanthology.org/2022.lrec-1.574/) | SG-H9 methodology | the honesty constraint: surface proxies only, no Sanskrit model | — | now |
| Versioned corrections model | [Anthology corrections policy](https://aclanthology.org/info/corrections/) · live example [2023.acl-long.594](https://aclanthology.org/2023.acl-long.594/) | 8 × `errata.yml` → [`ERRATA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ERRATA.md) | §5-N2 errata analytics; roadmap B1/B2 | flat errata list, one book populated, no versioning tiers | now |

**What to adopt first, and why.** τ (Lapata) and α (Artstein & Poesio), exactly as the roadmap
already ruled — both run on committed data with zero derivation and each converts an existing
hand-wave (a cluster list; a confidence column) into a number a paper can lead with. The one
addition this memo makes to that ruling: run the **SG-H4 detector evaluation in the same first
batch**, because `matches_review.tsv` is a gold set the repo already paid for and every später
detector decision (TRACER chunk size, threshold) becomes evidence-based once it exists. The
MI/entropy pair waits for the Q4.4 join; vidyut waits for the pilot quarter. **Honest
non-findings stand as verified on 10-07-2026:** no ACL precedent for rival-classification
adjudication (SG-H6's novelty), none for Western-grammar→sūtra alignment (SG-H7's), none for
seṭ/aniṭ or ablaut as a corpus-adjudicated target, only weak precedent for printed-book borrowing
direction (Hoenen), and no verifiable SIGMORPHON Sanskrit track — none of these may be cited into
existence.

---

## 5. New sections mining committed-but-unsurfaced layers

### N1 — "Concordance metrics" block on the Concordance page

**Surfaces.** The SG-H1/H2 numbers (τ per pair, positional-drift test) as a permanent, dated
results block on [`Concordance/catalog.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx).
**Reuse.** In-repo only: `catalog.csv` + `sentences.json`; no join.
**Claim → Evidence → Source.** "Bühler and Knauer order shared material near-identically (τ=…)"
→ computed statistic table → `catalog.csv` at a pinned commit.
**Derivation + owner.** A ~100-line stats script in `scripts/` — this repo owns it.
**Research read.** Paper 1's numbers live on the site, citable.
**Learner read.** The book-compatibility score, where a learner will actually see it.

### N2 — Errata analytics + versioned-corrections section

**Surfaces.** The 8 committed `errata.yml` files as data: corrections per book, per-type counts,
open vs `fixed_in` status — presently only Knauer's 25 render at all, via
[`build_errata.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_errata.py).
**Reuse.** The [ACL corrections model](https://aclanthology.org/info/corrections/) (erratum /
revision / retraction, versioned, checksummed) — roadmap B1/B2 specify the schema; this section is
its visible face.
**Claim → Evidence → Source.** "KnauerFrazy 1908 carries 25 print corrections, 0 still open" →
generated table → the book's `errata.yml` at a pinned commit.
**Derivation + owner.** Extend `build_errata.py` with a stats emitter — this repo owns it.
**Research read.** A digitization-quality signal per edition; DH-standard fixity practice.
**Learner read.** "Is the text I'm reading corrected?" answered per book.

### N3 — Root-frequency layer on the morphoclass pages ⚠ boundary-routed

**Surfaces.** DCS corpus frequency per root next to each crosswalk row — the column that makes
SG-H5's bands and SG-H6's adjudication legible on the site.
**Reuse + join key.** **whitney_no ↔ DCS lemma** (the Q4.4 crosswalk, net-new) joining
[`morphoclass_crosswalk_1975_2014_2026.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv)
to DCS lemma counts. **Corpus counts are owned by [VisualDCS](https://github.com/gasyoun/VisualDCS)**
— this repo consumes an exported table, never re-derives; MW-root assets come via the
[kosha release](https://github.com/gasyoun/kosha/releases). Register the feed in
[`PROJECT_INTERLINKS.md`](https://github.com/gasyoun/Uprava/blob/main/PROJECT_INTERLINKS.md) and the
[kosha manifest](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json) when Q4.4 lands.
**Claim → Evidence → Source.** "√bhū: 12,4xx DCS attestations; all three schemes agree" → joined
table → VisualDCS export (versioned) + crosswalk CSV.
**Research read.** SG-H5/H6 become inspectable row-by-row.
**Learner read.** "Learn the frequent contested roots first" — frequency-guided study order.

### N4 — Provenance & fixity block per book

**Surfaces.** What each book folder actually *is* — edition, source file, checksum, known proxy
status — currently scattered between `README.md` and folder names. The Bühler 1878/1923 proxy
warning (D4) becomes a standing per-book banner rather than a footnote.
**Reuse.** Roadmap B7 (checksums) + the Anthology's ID grammar (B2) — in-repo.
**Claim → Evidence → Source.** "This text = 1923 Stockholm reprint, SHA-256 …, proxy for 1878
(unverified, D4 open)" → generated block → the committed source file itself.
**Research read.** Citation-grade provenance for every quoted passage.
**Learner read.** Trust signal: what am I actually reading?

---

## 6. Prioritised build backlog

Ranked by leverage ÷ effort. **No build handoffs were minted this session** — every row carries
the `H###` placeholder form to be minted by `/handoff-mint` when the work is actually picked up.

| # | Item | Delivers | Effort | Deps | Owner repo | Tier |
|---|---|---|:--:|---|---|---|
| 1 | τ + positional-drift stats + N1 metrics block | SG-H1, SG-H2, N1 | S | — | SanskritGrammar | Sonnet |
| 2 | Detector evaluation on the frozen 128-pair gold | SG-H4 (P/R/F1 baseline) | S | — | SanskritGrammar | Sonnet |
| 3 | Three-scheme α (whole-set) + memo-back into Paper 2 skeleton | SG-H5 (part A) | S | — | SanskritGrammar | Opus |
| 4 | Concordance slope graph + heatmap upgrade | SG-V1, SG-V2 | M | 1 | SanskritGrammar | Sonnet |
| 5 | Difficulty proxies + ramp curves | SG-H9, SG-V5 | M | — | SanskritGrammar | Sonnet |
| 6 | Whitney-no ↔ DCS lemma ↔ vidyut dhātu crosswalk (Q4.4) | unblocks SG-H5 bands, SG-H6, N3 | M | VisualDCS export | SanskritGrammar (join) / [VisualDCS](https://github.com/gasyoun/VisualDCS) (counts) | Opus |
| 7 | Timeline + provenance/fixity blocks | SG-V4, N4 | S | — | SanskritGrammar | Sonnet |
| 8 | Errata analytics + versioned schema (B1/B2) | N2 | M | — | SanskritGrammar | Sonnet |
| 9 | MI/entropy adjudication run | SG-H6 (Paper 2 core) | L | 3, 6 | SanskritGrammar | Fable |
| 10 | Varga exhibit + alluvial | SG-V6, SG-V3 | M | 3 | SanskritGrammar | Sonnet |
| 11 | Pāṇini two-chapter pilot (kill-gated) | SG-H7 | L | 9 preferred first | SanskritGrammar | Fable |

Starter lines (placeholder form — mint the real ID at pickup):

```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Sonnet_SanskritGrammar_tau_concordance_metrics_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Sonnet_SanskritGrammar_detector_gold_eval_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Opus_SanskritGrammar_morphoclass_alpha_agreement_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Sonnet_SanskritGrammar_concordance_viz_upgrade_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Sonnet_SanskritGrammar_difficulty_ramp_curves_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Opus_SanskritGrammar_whitney_dcs_vidyut_crosswalk_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Sonnet_SanskritGrammar_timeline_provenance_blocks_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Sonnet_SanskritGrammar_errata_analytics_schema_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Fable_SanskritGrammar_mi_scheme_adjudication_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Sonnet_SanskritGrammar_varga_exhibit_alluvial_DD.MM.YY.md and execute it.
```
```
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H###-Fable_SanskritGrammar_panini_pilot_two_chapters_DD.MM.YY.md and execute it.
```

---

## 7. Deferred / out-of-scope appendix

- **1878 Bühler first edition (`@DO D4`)** — human acquisition/verification task; gates SG-H3 and
  every borrowing arrow. Tracked in the roadmap's decision table and
  [GTD](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md). Not agent-doable.
- **Second annotator** — parked for 2026 by standing guidance; every gold-sample item above
  (SG-H4, SG-H7, roadmap Q3.3) runs single-annotator + adjudicated re-pass and **claims no κ**.
- **Apte + Whitney sentence extraction (roadmap Q4.3)** — extends `sentences.json` to 5 books;
  deferred to its own quarter, OCR-quality triage first.
- **Benchmark packaging (roadmap Angle C)** — ships via
  [`/data-release`](https://github.com/gasyoun/claude-config/blob/main/commands/data-release.md)
  into the [kosha manifest](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json)
  only after frozen golds exist; premature today.
- **Name-variant model vs rename sweep (`@DECIDE D2`)** — the Anthology `people.yaml` alternative
  to the in-flight `Zaliznyak`→`Zalizniak` sweep; a human decides, not this memo.
- **Unverified externals** — a SIGMORPHON Sanskrit track (could not be verified — do not assume);
  Passim at scale (tooling verified via [Programming Historian](https://programminghistorian.org/en/lessons/detecting-text-reuse-with-passim),
  not ACL — usable, but cite as DSH tooling); MDL inflection-class scoring
  ([Beniamine & Bonami](https://onlinelibrary.wiley.com/doi/10.1002/9781119693604.morphcom038),
  Wiley, not ACL) — candidate SG-H6 companion, kept out of the crosswalk table proper.
- **Boundary routings restated.** DCS corpus counts → [VisualDCS](https://github.com/gasyoun/VisualDCS);
  MW root assets → [kosha](https://github.com/gasyoun/kosha); TEI/OntoLex packaging of any released
  dataset → csl-standards. This repo builds joins and pages, never sibling-owned derivations.

_Dr. Mārcis Gasūns_
