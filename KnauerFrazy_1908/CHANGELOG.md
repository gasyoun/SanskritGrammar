# Changelog — KnauerFrazy_1908

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- **Morphological-parse audit (H797 methodology fork, seed)** — [`parse_audit.yml`](parse_audit.yml)
  (KN-1..KN-10) + [`PARSE_AUDIT.md`](PARSE_AUDIT.md). H797 asks to port the Kochergina/Bühler
  two-axis discursive-claim pipeline to Knauer next, but this book's digitized text
  (`Frazy-Knauer-03.05.2023.mdx`) is a phrase reader, not a discursive grammar — no
  universality/frequency prose to harvest. Adapted the unit of analysis instead: each footnote's
  morphological parse (root + category, e.g. "к. rakṣ по § 120") audited for linguistic
  correctness against Whitney 1889. 10 of an estimated 280-330 total footnote parses verified (8
  CONFIRMED, 2 QUESTIONABLE pending a citation follow-up, 0 errors); full raw footnote text for
  all 19 exercise sets preserved verbatim as a backlog for future per-parse extraction.

## [0.1.0] - 2026-07-07
### Added
- 25 errata transcribed from the 1908 printed book and the Knauer
  2011/2015/2023 errata sheets — the first populated `errata.yml`/`ERRATA.md`
  in this repo.
- Initial mint: reprint source scan/edition (`.doc`, `.docx`) plus faithful
  `.mdx` extraction (prose, 0 grid tables) via the `/docx-to-md` skill.
