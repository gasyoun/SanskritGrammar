# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Initial mint: reprint source scans/editions for `ApteSyntax_1885`, `BuhlerLeitfaden_1923`,
  `KnauerFrazy_1908`, `KocherginaUchebnik_1998`, `ZalizniakKonspekt_2004`, and
  `ZalizniakOcherk_1978`.
- `BuhlerLeitfaden_1923`: extracted Markdown via Word97 piece-table parsing, then a
  formatting-faithful LibreOffice+pandoc reconversion (italics, rowspan/colspan paradigm
  tables preserved).
- Buhler + Kochergina `.docx` converted to `.md` via the `/docx-to-md` skill (Pandoc GFM
  with grid tables, images extracted to `*_media/`, UTF-8 Devanagari intact).
- `README.md` documenting the repo's source editions and scope.
