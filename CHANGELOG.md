# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- **GasunsDhatu_2014 → 2026 print-edition prep (H246).** Conversion cleanup across the
  dissertation + 4 article appendices (~1200 unescapes, typos Emeneau/Morgenroth/«Lihusina»→Edgren,
  Latin-C fixes, `image1.wmf`→PNG, 8 empty Pandoc headings removed); §2.5/2.6 renumbered (L8);
  number unification with editorial footnotes (Palsule 933/3690, EWA 50, АВ coefficient 1.33 —
  recomputed from the tables' own frequencies, L9); Гл. 2 title fixed per Волошина (C6);
  корнеслов/морфемарий defined at first use (C5) + морфонология⊃морфонемика note (L10);
  bibliography split into RU/foreign blocks (C13, mechanical part); Гумбольдт ref restored,
  Потебня flagged (C4). **Табл. 5 replaced**: χ² p-values → varga shares by epoch + Cramér's V
  = 0.037 (DCS 2026-03-05, reproducible via `revision-2026/varga_shares.py`) per MG Q3; the
  «Распределение рядов согласных» article brought to standalone-appendix form per MG Q2
  (аннотация/method/shares/вывод; 2014 p-table kept as historical record); «Список файлов»
  reduced to an annotated supplementary note with dead-link markers. New «Состояние вопроса
  на 2026 год» section (590/935 Whitney roots attested in DCS; digital crosswalks; vidyut
  dhātupāṭha; kosha data-v0.1.0). `errata.yml` seeded with 51 entries (`found_by: H246-review`);
  `revision-2026/` working notes: П1/П4/П7/П9/П10 draft rewrites (await author sign-off) +
  Palsule-vs-vidyut audit (`4añc` confirmed recoverable — 5 añc-family dhātus in the Paninian
  dhātupāṭha; `ast` present too, refining Крылов's 2014 remark).
- **Errata system** (`/errata` skill): every book folder carries an `errata.yml`
  structured source → generated `<Book>/ERRATA.md` + root `ERRATA.md` index via
  `scripts/build_errata.py` (`npm run errata`). Each erratum records who found it
  and when; the generator de-duplicates across errata sheets and cross-references
  this CHANGELOG (`fixed_in` marks typos corrected in the digital edition).
- Errata enter two ways: transcribing a printed errata sheet, **or** an edition
  diff (`build_errata.py diff <Book> <old-ref> [<new-ref>]`) that turns changes
  between two versions of a book's text file into reviewable errata candidates —
  so books with no printed sheet (Kochergina, etc.) still accrue errata over time.
- `KnauerFrazy_1908` errata: 25 corrections transcribed from the 1908 printed book
  and the Knauer 2011/2015/2023 errata sheets. The other five books seeded with an
  empty `errata.yml`.
- Initial mint: reprint source scans/editions for `ApteSyntax_1885`, `BuhlerLeitfaden_1923`,
  `KnauerFrazy_1908`, `KocherginaUchebnik_1998`, `ZalizniakKonspekt_2004`, and
  `ZalizniakOcherk_1978`.
- `BuhlerLeitfaden_1923`: extracted Markdown via Word97 piece-table parsing, then a
  formatting-faithful LibreOffice+pandoc reconversion (italics, rowspan/colspan paradigm
  tables preserved).
- Buhler + Kochergina `.docx` converted to `.md` via the `/docx-to-md` skill (Pandoc GFM
  with grid tables, images extracted to `*_media/`, UTF-8 Devanagari intact).
- `README.md` documenting the repo's source editions and scope.
