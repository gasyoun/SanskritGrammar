# Changelog — ZalizniakMorphology_1975

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- **Root classification audit (H797 Phase 2, infrastructure pass)** — [`build_root_classifier.py`](build_root_classifier.py)
  + [`root_classifier.json`](root_classifier.json) + [`ROOT_CLASSIFICATION_AUDIT.md`](ROOT_CLASSIFICATION_AUDIT.md).
  Genre-checked before starting: this paper's falsifiable claims are root-classification COUNTS
  against Whitney's fixed root inventory, not corpus-frequency prose (Kochergina/Bühler/Ocherk/
  Konspekt's genre) or individual footnote parses (Knauer's genre) — a fourth distinct
  verification methodology. Digitized ~180 of the paper's own explicitly-named roots into
  structured form (not an independent phonological re-derivation), cross-checked against
  [`WhitneyRoots/crosswalk/roots.csv`](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/roots.csv)
  (930 entries): 93% match after normalizing the ç/ṁ vs ś/ṃ transliteration convention, remainder
  explained by quasi-roots (not in Whitney by definition), citation-grade differences, and
  blend-variant naming, with 9 genuine unmatched roots and two arithmetic questions (Table 5's
  aniṭ/seṭ summary, the 847-vs-930 Whitney corpus-size gap) left explicitly unresolved rather than
  force-closed.

## [0.1.0] - 2026-07-06
### Added
- Initial mint: English translation (I. Tolchelnikov, ed. M. Ishimbaev) of Zaliznyak's 1975
  morphophonological root-classification paper, `.docx` + `.mdx`.
