# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- **Errata system** (`/errata` skill): per-book `errata.yml` structured source →
  generated `<Book>/ERRATA.md` + root `ERRATA.md` index via
  `scripts/build_errata.py` (`npm run errata`). Each erratum records who found it
  and when; the generator de-duplicates across errata sheets and cross-references
  this CHANGELOG (`fixed_in` marks typos corrected in the digital edition).
- `KnauerFrazy_1908` errata: 25 corrections transcribed from the 1908 printed book
  and the Knauer 2011/2015/2023 errata sheets.
- Initial mint: reprint source scans/editions for `ApteSyntax_1885`, `BuhlerLeitfaden_1923`,
  `KnauerFrazy_1908`, `KocherginaUchebnik_1998`, `ZalizniakKonspekt_2004`, and
  `ZalizniakOcherk_1978`.
- `BuhlerLeitfaden_1923`: extracted Markdown via Word97 piece-table parsing, then a
  formatting-faithful LibreOffice+pandoc reconversion (italics, rowspan/colspan paradigm
  tables preserved).
- Buhler + Kochergina `.docx` converted to `.md` via the `/docx-to-md` skill (Pandoc GFM
  with grid tables, images extracted to `*_media/`, UTF-8 Devanagari intact).
- `README.md` documenting the repo's source editions and scope.
