# Changelog — BuhlerLeitfaden_1923

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- **Claim-verification register (H797 Phase 2 seed)** — [`claims.yml`](claims.yml) (BU-1..BU-5,
  two-axis fact/pedagogy grading) + [`claims_harvest.yml`](claims_harvest.yml) (40-candidate
  backlog from a full 48-lesson parallel harvest) + [`verify_claims_dcs.py`](verify_claims_dcs.py)
  (DCS-2021 ground truth: tense/mood token shares, imperative person distribution, PPP suffix
  split). Ports the two-axis verification pipeline from `KocherginaUchebnik_1998` (H768/H797) to
  a second grammar. Headline: two frequency claims about the perfect/imperfect/aorist trio both
  fail — Bühler calls the perfect rarer than the imperfect (it's actually more common, 7.93% vs
  5.48% of verbal tokens: OVERSTATED) and the aorist "on equal footing" with both (it's ~0.31%,
  18-25× rarer: FALSE) — while systemic/paradigmatic claims (imperative person split, PPP -ta/-na
  ratio, periphrastic-perfect root-class conditions) hold up, one cross-confirming Kochergina's
  HK-17 to within 0.3pp via an independently re-run query. First slice, not a full drain — 40
  candidates remain in the backlog for a future pass.

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
