# Changelog — BuhlerLeitfaden_1923

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-07-14
### Added
- **Claim-verification register (H797 Phase 2, first cross-grammar port)** — [`claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml): 63 falsifiable grammatical assertions verified on the two axes (fact vs DCS-2021/Whitney 1889/Tolchelnikov-Talmud · pedagogy) — 57 TRUE, 4 OVERSTATED (the Урок-I "все времена имеют обе формы" absolute; ā+Acc government; genitive "всякого рода"; perfect claimed rarer than imperfect vs DCS 61,986 > 47,554), 1 FALSE (a-aorist "как impf. VII кл." beside its own thematic paradigm — likely a 1923 misprint for VI), 1 UNTESTABLE, 12 M.G. frequency footnotes (PPP = 29.8% of all verbal tokens; optative 9.3%; periphrastic future 14× rarer than simple; absolutive -ya 78.4%). Backlog: [`claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims_harvest.yml) — 340 candidates from the 6-reader full-book sweep (404 harvested, 64 promoted/merged). Rendered table: [`CLAIMS_VERIFIED.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/CLAIMS_VERIFIED.md). (Fable 5 `claude-fable-5`)

## [0.1.0] - 2026-07-07
### Added
- Extracted Markdown via Word97 piece-table parsing, then a formatting-faithful
  LibreOffice+pandoc reconversion (italics, rowspan/colspan paradigm tables
  preserved — 97 grid tables, the highest of any book here).
- Converted `.docx` → `.md`/`.mdx` via the `/docx-to-md` skill (Pandoc GFM with
  grid tables, images extracted to `Buhler_Unicode_media/`, UTF-8 Devanagari
  intact).
- Initial mint: reprint source (Stockholm, 1923; electronic edition v2.0 by
  N. P. Likhushina).
