# Changelog — ZalizniakOcherk_1978

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- **Claim-verification register (H797 Phase 2 seed)** — [`claims.yml`](claims.yml) (OCH-1..OCH-6,
  two-axis fact/pedagogy grading) + [`claims_harvest.yml`](claims_harvest.yml) (68-candidate
  backlog from a full-text 4-reader parallel harvest, 74 total) + [`verify_claims_dcs.py`](verify_claims_dcs.py).
  Genre-checked before harvesting: of Zaliznyak's three digitized sources, only this one (Очерк
  1978) is a full discursive grammar matching Kochergina's/Bühler's genre — Konspekt 2004 and
  Morphology 1975 are different genres, held for separate passes. Three of the six seed claims
  REUSE ground truth already computed for other books (Kochergina's vowel census and precative-
  middle stats, Bühler's absolutive split) rather than recomputing it — first demonstration that
  the cross-grammar program's corpus infrastructure compounds. One claim (çās as an exception to
  the closed-long-vowel-root pattern) cross-confirms KnauerFrazy_1908's independent KN-3 finding
  from a completely different genre of source. 6 TRUE (1 flagged MISLEADING for understating how
  thin the ya/aya frequency gap actually is), 0 errors — too small and reuse-biased a sample to
  characterize overall calibration. Two high-value backlog targets flagged for the next pass:
  §68's aniṭ/seṭ-by-alternation-series correlation, and §207's flagship Vedic-to-Classical
  syntactic-style diachronic claim (needs period-tagged corpus data, not yet confirmed to exist).

## [0.1.1] - 2026-07-15
### Added
- **Russian-language folder README** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/README.md): книга и жанр (по калибровке [ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md)), существующие исследовательские слои (профиль квантификаторов H800, три модели Зализняка, односторонняя зависимость Очерк↔Кочергина по карте связей H786), и статус реестра проверки утверждений: В ОЧЕРЕДИ фазы 2 H797 — с выполненной предварительной проверкой жанра (урок кнауэровской развилки). (Fable 5 `claude-fable-5`)
- **Changelog backfill (13-07-2026, H800):** the quantifier-metalanguage layer files landed in this folder without a book-level bullet — `quantifiers.yml` + `quantifiers.sample.yml` → generated [`QUANTIFIER_PROFILE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/QUANTIFIER_PROFILE.md) + `quantifiers.json` (`npm run quantifiers`; register + method in [GRADATION_METALANGUAGE_KOCHERGINA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/GRADATION_METALANGUAGE_KOCHERGINA.md)). (Opus 4.8 `claude-opus-4-8`)

## [0.1.0] - 2026-07-07
### Added
- Initial mint: reprint source scan/edition (`.doc`, `.docx`) plus faithful
  `.mdx` extraction (aligned edition, 55 grid tables) via the `/docx-to-md`
  skill.
