# Changelog

All notable changes to this repo's shared infrastructure (errata system, site
tooling, docs) are documented here. **Book-specific changes now live in each
book's own `<Book>/CHANGELOG.md`** (per-book release scheme, H318):
[ApteSyntax_1885](ApteSyntax_1885/CHANGELOG.md) ·
[BuhlerLeitfaden_1923](BuhlerLeitfaden_1923/CHANGELOG.md) ·
[GasunsDhatu_2014](GasunsDhatu_2014/CHANGELOG.md) ·
[KnauerFrazy_1908](KnauerFrazy_1908/CHANGELOG.md) ·
[KocherginaUchebnik_1998](KocherginaUchebnik_1998/CHANGELOG.md) ·
[ZalizniakKonspekt_2004](ZalizniakKonspekt_2004/CHANGELOG.md) ·
[ZalizniakOcherk_1978](ZalizniakOcherk_1978/CHANGELOG.md) ·
[TolchelnikovTalmud_2026](TolchelnikovTalmud_2026/CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Each book tags/releases independently as `<book-slug>-vX.Y.Z`; this root
changelog tags as `vX.Y.Z`.

## [Unreleased]

## [0.12.0] - 2026-07-14
### Added
- **Cross-grammar claim-verification layer: Bühler register live (H797 Phase 2)** — the two-axis pipeline (fact × pedagogy, FINDINGS §72) is now grammar-agnostic and running on its second book: [`BuhlerLeitfaden_1923/claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml) opens with **63 verified claims** (57 TRUE · 4 OVERSTATED · 1 FALSE · 1 UNTESTABLE · 12 M.G. frequency footnotes) drawn from a **404-candidate 6-reader full-book harvest** ([`claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims_harvest.yml), 340 in backlog). Headline findings: Bühler's hedges are systematically well-calibrated (the same seṭ -iṣya 56.8% number that flagged Kochergina HK-4 confirms Bühler TRUE); his failure modes are the Урок-I voice absolute contradicted by his own later lessons, rare-before-common ordering (periphrastic future taught before a 14×-more-frequent simple future; -tavat billed "также часто" beside a 100×-more-frequent PPP), and one flipped frequency direction (perfect "реже" than imperfect vs DCS 61,986 > 47,554). [`scripts/build_claims.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_claims.py) de-Kochergina-ised (per-book `*gives_number`, shared-battery link, generic headings); [`verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py) gained the HB metrics (-tāt imperative 0.95%, optative 9.3% of verbal, periphrastic vs simple future 1,290 vs 18,004, absolutive split -ya 78.4% / -tvā 19.6% / -am 0.4%). ([H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md)) (Fable 5 `claude-fable-5`)
- **Sandhi reader-hover surface (pedagogy Phase-4, 3/4)** — [`SandhiCollider.jsx`](https://github.com/gasyoun/SanskritGrammar/blob/main/src/components/talmud/SandhiCollider.jsx) is now data-driven from kosha's [`corpus_sandhi.tsv`](https://github.com/gasyoun/kosha/blob/main/data/sandhi/corpus_sandhi.tsv): hovering (or focusing) the collided result shows the induced rule + its corpus frequency + a "#N most common sandhi" badge (top-10 highlighted), with an honest `нет в корпусе` state for the 29 rare junctions with no corpus attestation. New generator [`scripts/build_sandhi_frequency.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_sandhi_frequency.py) vendors the vowel-coalescence subset (74 junctions) into a committed data module `src/components/talmud/sandhiFrequency.js` (build never needs kosha checked out). The third of the sandhi-programme's four Phase-4 reader surfaces. ([H917](https://github.com/gasyoun/Uprava/blob/main/handoffs/H917-Opus_SanskritGrammar_sandhi-reader-hover-collider_14.07.26.md), [PR #183](https://github.com/gasyoun/SanskritGrammar/pull/183)) (Opus 4.8 `claude-opus-4-8`)
- **Difficulty & ordering result (pedagogy RQ1) + paper A63 skeleton** — [`scripts/build_difficulty_ordering.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_difficulty_ordering.py) + [`data/difficulty_ordering/`](https://github.com/gasyoun/SanskritGrammar/tree/main/data/difficulty_ordering) + writeup [`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md). Corpus frequency tracks the expert learn-first order for content vocabulary (Kendall-τ 0.887) but the decisive act is excluding the top function words (46 % of top-50 lemmas, all indeclinables/pronouns) and correcting DCS's epic-genre bias; textbook introduction order is frequency-agnostic (τ≈0.05). Paper [A63](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/DifficultyOrdering_A63/OUTLINE_difficulty-ordering_A63.md) seeded (2/5). Wave-1a of the digital-pedagogy field (H913). (Opus 4.8 `claude-opus-4-8[1m]`)
- **Zaliznyak-made-learnable on-ramp (pedagogy §3.6)** — a beginner-graded entry to the Ряд/Тип/seṭ system below Tolchelnikov's *Талмуд*: new [`TolchelnikovTalmud_2026/onramp/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp) (index + 3 steps — grades / position+type / seṭ) with "one tap deeper" links into the full chapters, design doc [`ZALIZNYAK_ONRAMP_DESIGN.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/ZALIZNYAK_ONRAMP_DESIGN.md). `AblautMachine` gained optional `rows`/`initialSeries` props (the on-ramp shows the 4 high-frequency rows; talmud-02 unchanged). Wave-1c of the digital-pedagogy field (H915). (Opus 4.8 `claude-opus-4-8[1m]`)
- **Last-mile pipeline spec (pedagogy §14.2)** — [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md) (+ meta): the kosha→Systema contract that closes the "last mile" — 3 hops (reader-as-a-service, frequency-ordered SRS deck, difficulty→sequencing), a **vendored-data-file** contract matching the `SanskritGlossary.php` precedent, a one-rung B1-subhāṣita demo path, folding in W1a's strip-function-words + genre-correct ranking rule. Spec-only (no Systema code touched; straddle-tier fence). Wave-1d of the digital-pedagogy field (H916). (Opus 4.8 `claude-opus-4-8[1m]`)
- **A62 agenda paper — the field's defining paper (readiness 2/5)** — [`papers/DigitalPedagogyAgenda_A62/`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/DigitalPedagogyAgenda_A62/OUTLINE_digital-sanskrit-pedagogy-agenda_A62.md): survey + 4 falsifiable research questions (RQ1 already confirmed by the difficulty result, RQ3 partial via A60), an RQ4 evaluation design using the Zaliznyak on-ramp as an A/B testbed, a data-inventory table, venue candidates. **Completes wave-1** of the digital-pedagogy field (H914; tier-locked Fable, drafted on Opus by author override — a Fable voice-pass is the 4→5 step). (Opus 4.8 `claude-opus-4-8[1m]`)

## [0.11.0] - 2026-07-14
### Added
- **Digital Sanskrit pedagogy established as a priority research field** — org-wide field metadoc [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md) (+ [`.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.meta.md)) consolidating the three pre-existing pedagogy maps by reference, plus a layered plan in [`docs/`](https://github.com/gasyoun/SanskritGrammar/tree/main/docs) ([PLAN](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md) · [ROADMAP](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md) · [ARCHITECTURE](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_DIGITAL_SANSKRIT_PEDAGOGY.md) · [IMPLEMENTATION](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_DIGITAL_SANSKRIT_PEDAGOGY_WAVE1.md) · [VERIFICATION](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md)). Aspect-primary taxonomy with layered tags (CEFR rung · NLP capability · research-Q · traditional discipline · owning repo) from which the matrix & learner-journey views derive. Registered org-wide: MEGABOOK §2.10 (+ §2.9 strengthened), ARTICLES A62, GTD straddle tier (research T1 / product T0); wave-1 handoffs H912–H916 minted. Authored via `/ask` (17 rulings, zero blocking forks). (Opus 4.8 `claude-opus-4-8`)

## [0.10.0] - 2026-07-14
### Fixed
- **In-page ToC anchors on the Word-converted book pages** ([`src/remark/fixHeadingAnchors.mjs`](https://github.com/gasyoun/SanskritGrammar/blob/main/src/remark/fixHeadingAnchors.mjs)) —
  a new build-time remark plugin. These pages use `#` (h1) for every section heading, but
  Docusaurus only assigns anchor ids to h2–h6, so the baked-in `Оглавление` links (`#урок-1.` etc.)
  all pointed at id-less headings. The plugin demotes content `h1 → h2` (page title comes from
  frontmatter) and re-slugs each in-page anchor with the same github-slugger — only when it lands on
  a real heading, so unmatched links are left as-is. Broken anchors **93 → 25** (Apte 34→0,
  Talmud 33→8, Gasūns 26→17); the 25 residual are genuine missing targets / `_Toc…` Word bookmarks.
  Scoped to pages that actually carry an in-page ToC. (Opus 4.8 `claude-opus-4-8`.)

### Changed
- Section headings on the ToC book pages now render as **h2** (was h1), which also surfaces
  Docusaurus's right-side table-of-contents navigation on those pages.

## [0.9.2] - 2026-07-14
### Changed
- **`onBrokenLinks: 'throw'`** (was `'warn'`) in [`docusaurus.config.mjs`](https://github.com/gasyoun/SanskritGrammar/blob/main/docusaurus.config.mjs) —
  now that every in-site broken link is cleared (catalog, Fortunatovskiye landing page, papers
  de-link), a dead cross-link fails the build + CI instead of shipping silently. `onBrokenAnchors`
  stays `'warn'` — the OCR'd book pages still carry the separate `#-N` self-anchor cleanup. (Opus 4.8 `claude-opus-4-8`.)

## [0.9.1] - 2026-07-14
### Fixed
- **Broken in-site link on the Subject-concordance catalog page.** `build_subject_concordance.py`
  emitted `[Whitney book pages](../WhitneyGrammar_1889/00_index)`, but Docusaurus strips the `00_`
  numeric prefix so the page's real route is `.../WhitneyGrammar_1889/index` — the link 404'd. Fixed
  the link in the generator and regenerated
  [`SubjectConcordance/catalog.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/SubjectConcordance/catalog.mdx);
  `npm run build` confirms the broken-link warning for that page is gone. (Opus 4.8 `claude-opus-4-8`.)

## [0.9.0] - 2026-07-13
### Added
- **First automated test suite + CI** — a `tests/` pytest suite (59 characterization tests) pinning
  the pure helpers of the core build scripts (`build_whitney`, `mdx_postprocess`, `build_errata`,
  `build_claims`, `build_quantifiers`, and the two divergent `slugify` functions), plus a
  [`.github/workflows/ci.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/.github/workflows/ci.yml)
  that runs the suite **and a full Docusaurus build on every PR** — the pre-merge safety net that
  would have caught the `@docusaurus` version-skew build break before it reached `main`. Scripts had
  zero test coverage before this. (Opus 4.8 `claude-opus-4-8`.)
- **A54 author-voice pass + sign-off doc** ([`SIGNOFF_A54_author_pass.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/SIGNOFF_A54_author_pass.md)) —
  `/paper-author-pass` over the Kulikov-answer article
  ([`IIL_ZALIZNIAK_ALTERNATIONS_ARTICLE_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/IIL_ZALIZNIAK_ALTERNATIONS_ARTICLE_2027.md)).
  Register confirmed as the author's own; no body-prose or substance edits (the 3-lens register
  pass + hostile referee had already settled voice). Four voice observations and the full ⟦MG⟧
  submission gate collected into the sign-off doc for a 30-minute read-and-sign; A54 held at 4/5
  until author sign-off. (Opus 4.8 `claude-opus-4-8`, umbrella
  [H552](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H552-Fable_SanskritGrammar_iil-zalizniak-polemic-article_10.07.26.md).)

### Fixed
- **Broken production build — `@docusaurus/*` version skew.** A partial Dependabot bump
  ([#156](https://github.com/gasyoun/SanskritGrammar/pull/156)) left `@docusaurus/preset-classic`
  at `3.10.2` while `core`, `theme-mermaid`, `module-type-aliases` and `types` stayed `3.10.1`, so
  `docusaurus build` aborted with `Invalid name=docusaurus-plugin-content-docs version number=3.10.2`.
  Aligned all five `@docusaurus/*` packages to `3.10.2`; the regenerated
  [`package-lock.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/package-lock.json) also
  dedupes 198 now-redundant nested `@docusaurus/*` subtrees (−4.5k lines). Supersedes the three open
  single-package Dependabot PRs (core / theme-mermaid / module-type-aliases → 3.10.2). Build verified
  green. (Opus 4.8 `claude-opus-4-8`.)
- **Deprecated `onBrokenMarkdownLinks` config warning** (removed in Docusaurus v4) — moved from the
  top level into [`docusaurus.config.mjs`](https://github.com/gasyoun/SanskritGrammar/blob/main/docusaurus.config.mjs)
  `markdown.hooks.onBrokenMarkdownLinks`, silencing the per-build warning.
- **Revived 5 dead `rws_*.py` revision scripts.** `rws_apply.py`, `rws_assemble.py`,
  `rws_extract_worklist.py`, `rws_gen_skipped.py` and `rws_triage.py` hardcoded
  `BASE = C:\…\SanskritGrammar-h385\…`, an H385 worktree that no longer exists — every one of
  them crashed on a missing path. Replaced the dead literals with `__file__`-derived paths
  (matching the already-correct `rws_to_docx.py`), so the H385 revision pipeline runs again from
  any checkout. (Opus 4.8 `claude-opus-4-8`.)
- **Dead cross-link** in [`TolchelnikovTalmud_2026/CHANGELOG.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/CHANGELOG.md) —
  `ZALIZNYAK…` → `ZALIZNIAK…` (misspelt target; file is `ZALIZNIAK_1975_1978_2004_COMPARISON.md`).

### Changed
- **`scripts/requirements.txt`** — declared the two already-imported but unlisted runtime deps
  `pyyaml` (used by `build_claims`/`build_errata`/`build_quantifiers`/`harvest_quantifiers`) and
  `python-docx` (`rws_to_docx.py`), so a fresh `pip install -r` no longer fails at import time.
- **UTF-8 output rule swept across 12 tracked scripts.** Added the missing
  `sys.stderr.reconfigure(encoding='utf-8')` to 6 scripts that only reconfigured stdout, and
  replaced the older `sys.stdout = io.TextIOWrapper(…)` idiom with the standard
  `sys.stdout/stderr.reconfigure(…)` pair in the 6 `rws_*.py` scripts, so Devanagari/IAST output
  can't raise `UnicodeEncodeError` on a non-UTF-8 Windows console. (Opus 4.8 `claude-opus-4-8`.)

## [0.8.0] - 2026-07-12
### Added
- **`verify_claims_dcs.py` (Kochergina) extended with reproducible backlog-verification metrics
  (H797)** — a vowel census over the full DCS-2021 running text ([`0.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py)),
  verb-class share, past-tense competition and case-slot token distribution, so every M.G.
  frequency footnote in the claim register is re-runnable from the committed corpus. Feeds the
  book-level v0.3.0 drain of the Kochergina claim register (43 → 234 verified claims).
  ([H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.7.0] - 2026-07-12
### Added
- **A60 hostile referee pass + fixes (H773 → toward Q4)**
  ([`A60_review_opus48.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/A60_review_opus48.md)):
  reject-by-default review of the single-book draft. An independent agent re-derived every number from
  the committed sources — register composition, divergence distributions, future-stem allomorphs,
  conditional/precative rates all reproduce exactly (figures-vs-data clean).
### Changed
- **A60 draft strengthened** per the review — **2 Major + 6 Minor findings applied**:
  §2 related work now cites the corpus-based materials-evaluation subfield (Nation 2001) and the
  descriptive/*rules-as-regularities* corpus-grammar tradition (Biber et al. 1999) and re-scopes the
  novelty to the Sanskrit *seṭ/aniṭ* target (M1); a single-annotator / no-IAA validity threat added to
  Limitations (M2); the 43-vs-42 register count reconciled in prose and the stale `claims.yml` header
  comment corrected; abstract "predicts" → "aligns closely with"; HK-16 citation, tool-version note,
  ground-truth provenance, and the DCS citation tidied. One **venue @DECIDE** left open (ISCLS / WSC
  computational / lexicography-DH journal) → GTD. Readiness held at 4/5.
  ([H773](https://github.com/gasyoun/Uprava/blob/main/handoffs/H773-Opus_SanskritGrammar_grammar-asserts-corpus-denies-study_12.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.6.0] - 2026-07-12
### Added
- **A60 full single-book draft — "grammar claims the corpus does not confirm" (H773 phase Q3)**
  ([`DRAFT_grammar-claims-corpus-denies_A60.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/DRAFT_grammar-claims-corpus-denies_A60.md)):
  the complete paper in prose — abstract, introduction, related work (ACL-anthology-anchored, the
  four reference titles web-verified), data & method (two-axis register, triangulation, the four-way
  divergence typology, reproducibility), results (register composition, the 12-row central table, the
  future-stem flagship at 56.8% *seṭ*, the one FALSE claim, aggregation), discussion, limitations, and
  future work. Single-book by design (Kochergina 1998); the cross-grammar comparison (Q2) is framed as
  an enhancement, not a gap. The central class⇄pedagogy finding is stated with an explicit
  anti-circularity caveat. A60 readiness 3/5 → 4/5. Remaining to submission: `/paper-referee` +
  `/paper-author-pass` (Fable 5) + `/venue-scout`.
  ([H773](https://github.com/gasyoun/Uprava/blob/main/handoffs/H773-Opus_SanskritGrammar_grammar-asserts-corpus-denies-study_12.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.5.0] - 2026-07-12
### Added
- **A60 central table — "grammar claims the corpus does not confirm" (H773 phase Q1)**
  ([`TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60)):
  the paper's core table, built from H768's now-complete 43-claim Kochergina register. All **12**
  `verdict_fact ∈ {OVERSTATED, FALSE}` divergences (of 43 verified — 28 TRUE / 11 OVERSTATED /
  1 FALSE / 3 UNTESTABLE) are classified by the H773 four-way divergence typology
  (**over-generalisation 8 · rule-real-but-marginal 3 · flat-contradiction 1 · system-vs-usage 0**)
  and quantified. New reproducible layer, kept out of H768's file per the consume-don't-re-derive
  boundary: [`divergence_classes.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/divergence_classes.yml)
  (class + rationale per claim) + [`build_divergence_table.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/build_divergence_table.py)
  (joins it to `claims.yml` → the generated [`TABLE_grammar-claims-corpus-denies_A60.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/TABLE_grammar-claims-corpus-denies_A60.md);
  `--check` guards any unclassified divergence). Finding: the divergence class **predicts** the H768
  pedagogy verdict (class 1 ⇔ `MISLEADING`, classes 2+4 ⇔ `FREQUENCY-HIDDEN`); the empty
  system-vs-usage class is itself a result. A60 readiness 2/5 → 3/5. Central table complete for
  Kochergina; per-grammar comparison (Q2) still gated on a second grammar's harvest.
  ([H773](https://github.com/gasyoun/Uprava/blob/main/handoffs/H773-Opus_SanskritGrammar_grammar-asserts-corpus-denies-study_12.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.4.0] - 2026-07-12
### Added
- **Sangram contract C5 — morphology programme (W2)** ([`sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx),
  route `/grammars/sangram/morphology-program`): thematic programme for wave **W2** over
  the C2 registry's WF (11) + MO (32) morphology slots — 9 macroclusters; the
  **attested / generated / traditional** three-source method (the programme's methodological
  core: attested-in-DCS carries the quantitative claim, generated fills paradigm cells as
  hypotheses, traditional witnesses existence, never silently merged); evidence limits
  EM1–EM8 tied to C3 defects Д1–Д8; morphology query-design (form-class not UD-Tense,
  WhitneyRoots class join, paradigm-cell-coverage query, dictionary-derivation join);
  per-cluster W2 quotas (**19 ① core across all 9 macroclusters**, within the charter 15–25
  range, ≥1 per macrocluster); 5 pilots each stressing a distinct limit with launch + kill
  gates; annotation gaps; witnesses (grammars-предшественники + machine paradigm assets —
  WhitneyRoots, mw_roots.tsv, MWinflect, csl-inflect, vidyut, VisualDCS); five-year placement
  in W2 between the W1 foundation and W3 semantics. References the canonical `SG-WF-*`/`SG-MO-*`
  IDs, mints none (C2 stays canonical). Build green, page generated, zero broken links
  ([H634](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H634-Fable_SanskritGrammar_sangram-morphology-program_11.07.26.md), Opus 4.8 `claude-opus-4-8` — slot was minted for Fable 5, run on Opus 4.8 by explicit author decision).

## [0.3.0] - 2026-07-12
### Added
- **WSC-2027 CDSL report — deep remake** (H795, Fable 5 `claude-fable-5`):
  [`TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/`](TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/) —
  13 `.mdx` chapters remaking the WSC-2025-rejected "Report on Cologne Digital
  Sanskrit Lexicon Project" for the 20th World Sanskrit Conference (Mumbai,
  December 2027): formal register per the four Kathmandu reviews, every
  quantitative claim tied to a committed dataset, Peter Scharf's review
  incorporated (Sanskrit Library co-history, TEI, morphid coordination,
  licence status), team history updated through Jim Funderburk's June-2026
  retirement (cited to the recorded volunteer call), full bibliography +
  abbreviations appendix. Provenance and residual pre-submission items in the
  folder's [`README.mdx`](TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/README.mdx).

## [0.2.0] - 2026-07-12
### Added
- **Атлас B5 — зависимости репозиториев** (`/sangram/atlas/dependencies`, H620,
  Fable 5 `claude-fable-5`): пять видов ребер публичного interlinks-экспорта
  (feeds · consumes · vendors · produces · cites) различимы цветом **и** текстовым
  бейджем, направление и канон/копия по каждому виду, таблица всех вендоренных
  копий организации, поиск по репозиториям/активам/контрагентам, программные
  группы census через новое опциональное поле `programme_ru` на `repo`-узлах
  (контракт данных 1.0.0 → **1.1.0**, append-only), полное покрытие census
  (75 репозиториев / 67 с ребрами / 8 изолятов пунктиром), controlled-mode на
  едином маршруте (`sangram/atlas/dependencies.mdx` +
  `src/components/AtlasDependencies/`). В источнике interlinks исправлены два
  инвертированных `vendors`-ребра (vidyut); bundle пересобран, leakage = 0.
- **Атлас B3 — переиспользование готовых активов** (`/sangram/atlas/reuse`, H630,
  Fable 5 `claude-fable-5`): владелец → актив → потребитель по 18 каноническим
  семействам с ярусами прав и запретами пересоздания
  (`sangram/atlas/reuse.mdx` + `src/components/AtlasReuseView/`).
- **Все пять представлений атласа живые на едином маршруте**
  (`/sangram/atlas/unified`): wave B серии MEGABOOK × Sangram (B1–B6) закрыта —
  attention · reuse · value-chain · dependencies · provenance подключены в
  `VIEW_REGISTRY`, выбранный узел сохраняется при переключении представлений.

## [0.1.0] - 2026-07-12
### Added
- **GrammarRelations — карта связей грамматик** ([GrammarRelations/grammar-relations-map.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GrammarRelations/grammar-relations-map.mdx),
  route `/grammars/GrammarRelations/grammar-relations-map`): читательская страница о том,
  как связаны 10 оцифрованных грамматик — генеалогия учебной линии (τ из S1), проверенная
  по тексту зависимость Очерк-1978↔Кочергина-1998, линия Зализняка 1975/1978/2004 и ветви
  Гасунс/Толчельников, карта тем, трудность подачи и совместимость для студента. Новый
  скрипт [`scripts/grammar_relations_stats.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/grammar_relations_stats.py)
  (SG-H2 подтверждена: медианный сдвиг +0.142, p≈2×10⁻⁵; SG-H9 опровергнута на
  символьном прокси) + результаты в
  [`scripts/data/grammar_relations_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/grammar_relations_stats.json)
  (H786, Fable 5 `claude-fable-5`).
- **Атлас B4 — интерактивная цепочка ценности** (`/sangram/atlas/value-chain`,
  H627, Fable 5 `claude-fable-5`): три селектируемых типизированных контура
  (исследовательский · образовательный · агентный) над 7 value-ступенями и
  10 ребрами bundle, роли источник/данные/продукт/отдача/мультипликатор без
  смешения, доказуемость каждого звена ребром bundle + свидетельством,
  Mermaid-объяснение с accTitle/accDescr и табличный эквивалент
  (`sangram/atlas/value-chain.mdx` + `src/components/AtlasValueChain/`).
- **Sangram contract C2 — article TOC network** ([`sangram/toc/SANGRAM_TOC_NETWORK.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/toc/SANGRAM_TOC_NETWORK.mdx),
  route `/grammars/sangram/toc-network-c2`): append-only registry
  [`articles.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/toc/data/articles.json)
  of 93 core articles across the 7 charter domains (PH 10 · WF 11 · MO 32 · SE 15 ·
  SY 14 · DI 6 · VA 5) — stable `SG-<domain>-<NNN>` IDs, 117-edge acyclic prerequisite
  graph, DCS query sketches (6-prefix grammar), curated witnesses from the repo's 10
  grammars plus a derived Whitney-chapter coverage layer; all 33 C6 programme slots
  mapped via `c6_slots`. Generator `scripts/toc_build_pages.py` (overview + 7 domain
  pages with Mermaid prerequisite graphs) and validator `scripts/toc_validate.py`
  (17 check classes incl. H540 form-class cross-check and `--check` page sync)
  (H631, Fable 5 `claude-fable-5`).
- **Sangram editorial + i18n contract (C4, H633)**: article manifest schema
  ([sangram/editorial/data/article.schema.json](sangram/editorial/data/article.schema.json)),
  fixture, validator (`python scripts/article_validate.py --self-test`) and the
  prose contract page ([sangram/editorial/SANGRAM_EDITORIAL_I18N_CONTRACT.mdx](sangram/editorial/SANGRAM_EDITORIAL_I18N_CONTRACT.mdx)):
  RU-default/EN-translation locales, one canonical SLP1 copy per example
  (IAST/Devanagari derived via sanskrit-util), scientific/pedagogical layers,
  stable `ex:<slug>:<n>` example IDs with locus/translation/provenance,
  public⇒https / internal⇒no-URL evidence rule, leakage = 0.
- **Sangram contract C3 — corpus evidence method** ([`sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx),
  route `/grammars/sangram/corpus-evidence-method`): corpus registry (DCS primary via the
  pinned [`gasyoun/dcs-conllu`](https://github.com/gasyoun/dcs-conllu) snapshot + 5
  supplementary witnesses), rights/liveness/quality gates, the reproducible
  query→sample→validate→claim→examples cycle, quantitative-claim rules П1–П7, and the
  append-only source-defect list Д1–Д8 (H632, Fable 5 `claude-fable-5`).
- **Errata system** (`/errata` skill): every book folder carries an `errata.yml`
  structured source → generated `<Book>/ERRATA.md` + root `ERRATA.md` index via
  `scripts/build_errata.py` (`npm run errata`). Each erratum records who found it
  and when; the generator de-duplicates across errata sheets and cross-references
  the book's own CHANGELOG (`fixed_in` marks typos corrected in the digital edition).
- Errata enter two ways: transcribing a printed errata sheet, **or** an edition
  diff (`build_errata.py diff <Book> <old-ref> [<new-ref>]`) that turns changes
  between two versions of a book's text file into reviewable errata candidates —
  so books with no printed sheet (Kochergina, etc.) still accrue errata over time.
- `README.md` documenting the repo's source editions and scope.
