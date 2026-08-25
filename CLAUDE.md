# CLAUDE.md

_Created: 20-07-2026 · Last updated: 25-08-2026_

This file provides guidance to Claude Code (claude.ai/code) when working with code in
this repository.

> Org-level conventions (hubs, `.ai_state.md` protocol, Windows encoding rules, the
> csl-orig fence) live in [`../CLAUDE.md`](../CLAUDE.md) and load automatically. Before
> touching encodings, transliteration, or corpus data, read the
> [Sanskrit context primer](https://github.com/gasyoun/github-spine/blob/main/SANSKRIT_CONTEXT_PRIMER.md).
> This file covers only what is specific to **this** repository.

## What this repository is

Three layers in one repo (full orientation:
[README.md](https://github.com/gasyoun/SanskritGrammar/blob/main/README.md)):

1. **A raw-source archive** of classic Sanskrit-grammar textbooks — one directory per
   work, named `<Author><ShortTitle>_<year>` (ApteSyntax_1885, BuhlerLeitfaden_1923,
   GasunsDhatu_2014, KnauerFrazy_1908, KocherginaUchebnik_1998,
   TolchelnikovTalmud_2026, WhitneyGrammar_1889, ZalizniakKonspekt_2004/
   Morphology_1975/Ocherk_1978) — kept as legacy `.doc`/`.docx` beside their faithful
   `.mdx` extraction.
2. **A Docusaurus site** to read them rendered
   ([docusaurus.config.mjs](https://github.com/gasyoun/SanskritGrammar/blob/main/docusaurus.config.mjs)
   auto-registers any top-level directory containing an `.mdx` — adding a work needs no
   config edit).
3. **A research layer**: the Sangram consolidation ([sangram/](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram)),
   the Bühler/Knauer/Kochergina [Concordance](https://github.com/gasyoun/SanskritGrammar/tree/main/Concordance)
   and [SubjectConcordance](https://github.com/gasyoun/SanskritGrammar/tree/main/SubjectConcordance),
   the [digital-pedagogy field doc](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md),
   the [DCS-derived numbers ledger](https://github.com/gasyoun/SanskritGrammar/blob/main/DCS_DERIVED_NUMBERS_LEDGER_2026.md),
   and the [ACL 2026–2027 roadmap](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md).
   Live queue: [.ai_state.md](https://github.com/gasyoun/SanskritGrammar/blob/main/.ai_state.md).

## The conversion pipeline — sources vs generated files

- **`npm run convert`** regenerates the `.mdx`: `scripts/docx_to_mdx.py` (Pandoc) then
  `scripts/mdx_postprocess.py` (MDX-safety). Pandoc runs with
  `markdown-simple_tables-multiline_tables`, so every table becomes a GFM pipe table or
  a grid table; **each grid table is wrapped in a plain ```` ```rst-table ```` fenced
  block**, rendered by the pure-JS remark plugin in
  [src/remark/](https://github.com/gasyoun/SanskritGrammar/tree/main/src/remark)
  (`rstTable.mjs` + `rstTableAst.mjs` + `rstTableParser.mjs`).
- **A hand-corrected `.docx` is authoritative** — conversion skips a `.doc` when a
  `.docx` sits beside it, and fixes belong in the `.docx` (or the postprocessor), never
  in the generated `.mdx`.
- **Generated files are never hand-edited**: every book's `ERRATA.md` (regenerate with
  `npm run errata`; the hand-edited source is `<Book>/errata.yml`),
  `Concordance/catalog.mdx`, and `review/<sheet_id>_review.html` (source:
  `review/specs/<sheet_id>.json`).
- ⚠️ The three-file `rstTable*` remark plugin exists as **three hand-synced copies**
  (canonical TypeScript in [buhler-sanskrit-book](https://github.com/gasyoun/buhler-sanskrit-book/tree/main/src/remark),
  `.mjs` ports here and in csl-guides) — keep all three in sync by hand; a drift-guard
  is wave-1 lane-3 work ([H1394](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1394-Sonnet_sanskrit-util_reuse-context-w1-consolidation-finish_20.07.26.md)).
- **SG-MO-021 is a hard-cutover content pipeline.** Its source and generated
  artifacts live under
  [`content/sangram/articles/future/`](https://github.com/gasyoun/SanskritGrammar/tree/main/content/sangram/articles/future),
  and [`pipelines/sg-mo-021-future.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/pipelines/sg-mo-021-future.yml)
  pins the DCS SQLite input and dispatches
  [`packages/sg_tooling/src/sg_tooling/generators/sg_mo_021_future.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/packages/sg_tooling/src/sg_tooling/generators/sg_mo_021_future.py).
  Run `uv run sg pipeline check sg-mo-021-future`
  before generation; the runtime SHA refusal is intentional. The independent
  and override implementations were reconciled in
  [`docs/architecture/H1913_DUAL_RUN_RECONCILIATION.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/architecture/H1913_DUAL_RUN_RECONCILIATION.md).

## Common commands

| Command | What it does |
|---|---|
| `npm run convert` | regenerate `.mdx` from the Word sources (Pandoc + postprocess) |
| `npm run build` / `npm run start` | build / serve the Docusaurus site |
| `npm run errata` | regenerate every book's `ERRATA.md` + the index from `errata.yml` |
| `npm run claims` / `npm run check-claims` | rebuild / consistency-check the grammar-claims layer (+ claims schema validate) |
| `uv run sg pipeline check sg-mo-021-future` | validate the pinned SG-MO-021 Slice C pipeline before generation |
| `python -m pytest` | run the script test suite ([tests/](https://github.com/gasyoun/SanskritGrammar/tree/main/tests)) |

**CI enforcement (H1840):** `.github/workflows/ci.yml` job `validators` is a **blocking** gate on every PR/push to `main`. It runs, each with nonzero-exit failure:

1. `python scripts/refresh_published_figures.py --check` (H2298 — shape guard on the vendored cross-repo asset)
2. `python scripts/check_claims_consistency.py`
3. `python scripts/claims_schema_validate.py --all` (H1842)
4. `python scripts/check_denominator_commensurability.py`
5. `python scripts/toc_validate.py`
6. `python scripts/article_validate.py --all`
7. `python scripts/consolidation_ledger_refresh.py --check`

If `--check` fails with "stale", refresh and commit: `python scripts/consolidation_ledger_refresh.py` (no `--check`). A planted stale aorist figure in any `*/claims.yml` is caught by step 2 (see `tests/test_claims_consistency.py::test_scan_flags_a_planted_stale`).

**⚠️ We consume a VisualDCS asset (H2298).** `check_claims_consistency.py` check 3 compares our DCS-2021 figures against
[`data/dcs_published_figures.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/dcs_published_figures.json),
a vendored copy of what [VisualDCS publishes](https://github.com/gasyoun/VisualDCS/blob/main/dcs_published_figures.json)
(CI checks out one repo, so a sibling-clone read is impossible). Refresh with `python scripts/refresh_published_figures.py`
after upstream regenerates via `regen_widgets.py --figures-only`. **Before adding a pair, read
[docs/CROSSREPO_FIGURE_COMMENSURABILITY_DCS_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/CROSSREPO_FIGURE_COMMENSURABILITY_DCS_2026.md)** —
our `imperfect_tokens` (47,554, five codes) is **not** the pair for a published `Imperfect Active`
(40,363, codes 4+8); `imperfect_active_tokens` is. An `incommensurable` report means re-adjudicate the pair, never edit a number to match.

Operator runbooks (RQ4 go-live, pedagogy-export hop, etc.): [docs/runbooks/](https://github.com/gasyoun/SanskritGrammar/tree/main/docs/runbooks).

## Traps

- ⚠️ **`Concordance/Usha-PhD-Sampurna.pdf` has a broken text layer** (Sanskrit2003
  font, no ToUnicode map) — text extraction yields garbage; use page rendering +
  vision OCR instead.
- The `.doc` files are legacy Word 97 binary (Composite Document File V2) — convert via
  LibreOffice headless to `.docx` first; never edit them in place.
- Whitney chapters under `WhitneyGrammar_1889/` are **generated** from
  [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots) by `scripts/build_whitney.py`
  — fix the generator or the source repo, not the output.

## Operational hazard notes

Destructive-risk facts for this repo (do-not-rerun scripts, decoys, traps) are
registered centrally in an org-private hub
([Uprava DANGER_FACTS.md](https://github.com/gasyoun/Uprava/blob/main/DANGER_FACTS.md),
org members only); the public-safe subset is mirrored in the generated block of
[AGENTS.md](https://github.com/gasyoun/SanskritGrammar/blob/main/AGENTS.md). Check them
before running anything that writes.
