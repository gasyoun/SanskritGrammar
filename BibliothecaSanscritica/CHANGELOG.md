# Changelog — Bibliotheca Sanscritica (series)

_Created: 10-09-2026 · Last updated: 13-09-2026_

## [Unreleased]

- H4628 (OxAlpha, opencode/z-ai/glm-5.3-flash): e-publish волна 1, тома II–V —
  4 mdx живого текста вёрстки + coverage-check GREEN на всех
  ([E_PUBLISH_MANIFEST.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/E_PUBLISH_MANIFEST.md));
  II Фриш — аппарат вёрстки 24.12.2022 (корпус = плашки); III Кнауэр — ПОЛНЫЙ
  текст (idml 17.12.2020, 201 946 зн.); IV Лихушина — H4484 pilot ре-проверен
  GREEN; V Миллер — живой текст блока 2021 (PyMuPDF; корпус = плашки).
  Новые инструменты: пер-томное происхождение в
  [tools/idml_to_mdx.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tools/idml_to_mdx.py),
  [tools/pdf_to_mdx.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tools/pdf_to_mdx.py),
  гейт [tools/idml_coverage_check.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tools/idml_coverage_check.py)
  (независимая переэкстракция, пол 90%). Derived-only: бинарники не коммитятся.
- H4642 (OxAlpha, opencode/z-ai/glm-5.3-flash): e-publish wave 1 — digital
  editions of toms II, III, IV, V (idml route, pilot-proven extractor) and
  tom XVIII (never-print ruling D3, MG 13-09-2026: e-published from the final
  block PDF via PyMuPDF, standing
  [never-print directive](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/STANDING_DIRECTIVE_neverprint_toms_epub_2026-09-13.md)
  registered) — per-tom stats, spot-checks and honest facsimile/OCR residue in
  [BIBLIOTHECA_EPUB_WAVE1_REPORT_2026-09-13.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/BIBLIOTHECA_EPUB_WAVE1_REPORT_2026-09-13.md);
  [tools/idml_to_mdx.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tools/idml_to_mdx.py)
  generalized with front-matter overrides (pilot output re-verified
  byte-identical), new
  [tools/pdf_to_mdx.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tools/pdf_to_mdx.py).
  Derived-only: no InDesign binaries or print PDFs committed.
- H4484 (OxAlpha, glm-5.3-flash): series onboarded — 27-tom state census
  (14 издан / 2 в правке / 11 не начат, evidence per tom, @DECIDE memo D1–D5
  reprint/e-publish/new-tom) in
  [BIBLIOTHECA_SANSCRITICA_CENSUS_2026-09-10.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/BIBLIOTHECA_SANSCRITICA_CENSUS_2026-09-10.md);
  pilot digital edition of the Lihushina chrestomathy from the newest
  .indd-derived source (`lihusina-15.12.14.idml`, verbatim, 36 stories, 2 628
  paragraphs, 75 918 Devanagari chars; 92.9% lexical coverage vs the 09.2014
  control versta) in
  [LihushinaChrestomathy_2015/](https://github.com/gasyoun/SanskritGrammar/tree/main/BibliothecaSanscritica/LihushinaChrestomathy_2015)
  via [tools/idml_to_mdx.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tools/idml_to_mdx.py).
  Derived-only: no InDesign binaries committed.
