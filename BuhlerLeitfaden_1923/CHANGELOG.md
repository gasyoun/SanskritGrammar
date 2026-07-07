# Changelog — BuhlerLeitfaden_1923

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
