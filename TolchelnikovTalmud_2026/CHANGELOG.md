# Changelog — TolchelnikovTalmud_2026

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Standing rule (MG, 08-07-2026): every change to the Talmud — text, data, widgets,
> apparatus — gets an `[Unreleased]` entry here in the same pass.** No silent edits.

## [Unreleased]

## [0.2.3] - 2026-07-15
### Added
- **Russian folder README** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/README.md): по-русски — паспорт живой книги (порождающая морфонология Ряд/Тип/seṭ, наследование модели Зализняка 1975, публикация Ауровиль-2024), состав папки (Talmud-2.1.6 + 14 поглавных страниц с AblautMachine/SandhiCollider, onramp H915, издательский хаб papers/ c A60/A62/A63/WSC-2027, аппарат со standing rule автора), и роль в программе проверки утверждений — **опора, не мишень**: авторитет морфокласса корня в D-B, несущая ось seṭ/aniṭ за флагманским числом -iṣya 56,8 %, приёмник подмножества OVERSTATED/FALSE в A60. Ряд README: [Кочергина](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/README.md) · [Бюлер](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/README.md) · [Кнауэр](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/README.md) · Зализняк×2 · [Уитни](https://github.com/gasyoun/SanskritGrammar/blob/main/WhitneyGrammar_1889/README.md). (Fable 5 `claude-fable-5`)

## [0.2.2] - 2026-07-14
### Fixed
- **`papers/` index: de-linked the un-published source binaries.** The links to the Auroville /
  Fortunatovskiye / Dubyanskiye `.pptx`/`.pdf` slide sources were broken *by design* — those source
  files are deliberately gitignored (`.gitignore` H411 "derived-edition-only" policy), so they aren't
  in the repo and can't resolve. Converted the 6 dead links to plain filenames (kept a source-only
  note). `npm run build` now reports **zero broken links** site-wide (the separate broken-*anchor*
  items on the OCR'd book pages are unaffected). (Opus 4.8 `claude-opus-4-8`.)

## [0.2.1] - 2026-07-14
### Fixed
- **`papers/Fortunatovskiye_2023/` landing page** — added a hand-authored `index.mdx` (matching the
  Desnickaya_2020 / Kulikov_2025 pattern), so the folder route resolves. The two `../Fortunatovskiye_2023/`
  cross-links from those sibling pages were broken (the folder had only a `.docx`-generated paper page,
  no index); `npm run build` confirms both now resolve, with no new broken links. (Opus 4.8 `claude-opus-4-8`.)

## [0.2.0] - 2026-07-14
### Added
- **`papers/`** — Tolchelnikov's 2023–2025 companion conference papers/talks (Auroville,
  Fortunatovskiye, Dubyanskiye, plus Desnickaya/Kulikov's independent commentary) published
  as `.mdx` in the Docusaurus site, with a `Papers & talks (Tolchelnikov)` sidebar category
  (`_category_.json` per folder) kept separate from the main chapter list, and a
  [`papers/index.mdx`](papers/index.mdx) cross-linked with
  [`ZALIZNIAK_1975_1978_2004_COMPARISON.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md) (H411).
- **`data/talmud_appendix1.json`** — the author's own Приложение 1 verb-root catalog (745 roots),
  parsed **verbatim** from the authoritative manual `Talmud-2.1.6.mdx` by new
  `tools/parse_appendix1.py`. Carries per root the author's Ряд, Тип (`I`–`IV`), seṭ
  (`s`/`a`/`v1`…`v4`), pada and Whitney-nomenclature reference — the **source of truth** for these
  values per the issue-#50 ruling (H329 Phase 3).
- `data/manual_reconciliation_report.md` — audit trail: how the author's catalog covers the
  Whitney spine (730/745 rows → 730 Whitney roots) and how far the retired derived Ряд/seṭ
  disagreed with him (Ряд 75.6 %, i.e. **178 roots the derivation got wrong**).
- `data/z_root_map.json` — Whitney-no ↔ [samskrtam.ru/z/](https://samskrtam.ru/z/) verb-id
  join map (876/905 roots matched) + reproducible `tools/build_z_root_map.py` (H329 Phase 1).
- `data/z_reconciliation_report.md` — reconciliation of `/z/`'s Ряд/seṭ vs our derived values
  (H329 Phase 2).
- `/z/` deep-links: «/z/» column in Appendix 1 + `z_url` on the AblautMachine/SetTree widget
  captions, linking each root to its full generated paradigm (H329 Phase 4).

### Notes
- **`/z/` is built from an EARLIER version of the Talmud** (MG, 08-07-2026) — so a share of the
  Ряд/seṭ discrepancies is **authorial version drift** (values Ivan revised between the version
  `/z/` was generated from and the current v2.1.6), not an error on either side. The 70.7 % Ряд
  agreement therefore partly measures version difference, not fidelity.
- Author correction (issue #50): `/z/`'s `0`-variant (`I0/N0/…`) + `L` rows and ṛ→`A1` values are
  `/z/` bugs; the printed manual (руководство) is ground truth for Ряд.
- **Author ruling (I. E. Tolchelnikov, issue #50, 08-07-2026):** Ряд, seṭ and Whitney refs are taken
  from the **latest manual = `Talmud-2.1.6.mdx`** (the current authoritative edition), not `/z/` and
  not our derivation; un-indexed rows stay un-indexed; **no methodology footnote** (FN-0001/0002
  marked `rejected`). `/z/` is kept only as the paradigm deep-link (outdated snapshot, still useful).

### Changed
- **`data/whitney_talmud.json`: Ряд/Тип/seṭ now sourced from the manual, not derived** (H329 Phase 3).
  `tools/build_whitney_talmud.py` overlays the author's Приложение 1 catalog onto the Whitney spine
  (`ryad_source`/`tip_source`/`set_source` = `"manual"`); the vowel-derived Ряд and p.p.p.-inferred
  seṭ are **no longer emitted** (derivation code retained only for the reconciliation audit). New
  fields `tip`, `tip_source`, `set_code`, `pada`; **dropped** `ryad_confidence`, `ryad_note`,
  `set_confidence`. 730 roots carry the author's Ряд, 200 are `null` (not in his catalog); 721 carry
  a manual seṭ. Тип is now populated (previously always `null`).
- Приложение 1 render (`talmud-appendix-1.mdx`, `tools/render_appendix1.py`): columns `Ряд*`/`seṭ*` →
  `Ряд`/`Тип`/`seṭ` (no `*`); provenance note rewritten to cite the manual; the «Структура словарной
  статьи» legend corrected — Тип is `I`–`IV` (Table 5), the `s`/`a`/`v` codes are the seṭ-parameter
  (Table 8), which the prior draft had conflated.
- Widget feed (`data/widget_roots.json`, `tools/build_widget_data.py`): Ряд/seṭ relabelled as the
  author's manual values; `ryad_confidence`/`set_confidence` projections dropped, `tip`/`set_code`
  added; ablaut examples now restricted to roots the author gives a series for.
- `footnote-proposals/proposals.yml`: FN-0001/0002 (derived Ряд/seṭ methodology notes) → `status: rejected`
  per the author's issue-#50 ruling ("примечание не нужно").

## [0.1.0] - 2026-07-07
### Added
- Docusaurus scaffold + §-concordance skeleton (H242 Phase 0).
- `whitney_talmud.json` enrichment crosswalk (H241 Phase 3).
- 5 interactive widgets (H241 Phase 2).
- `IMPROVEMENT_PLAN.md` — interactive-companion planning note.
- Initial mint: `.mdx` for the dissertation text plus a separate `-uroky`
  (lessons) edition, converted via the `/docx-to-md` skill.
