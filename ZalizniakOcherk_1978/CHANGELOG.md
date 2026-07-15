# Changelog — ZalizniakOcherk_1978

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-07-15
### Added
- **Russian-language folder README** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/README.md): книга и жанр (по калибровке [ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md)), существующие исследовательские слои (профиль квантификаторов H800, три модели Зализняка, односторонняя зависимость Очерк↔Кочергина по карте связей H786), и статус реестра проверки утверждений: В ОЧЕРЕДИ фазы 2 H797 — с выполненной предварительной проверкой жанра (урок кнауэровской развилки). (Fable 5 `claude-fable-5`)
- **Changelog backfill (13-07-2026, H800):** the quantifier-metalanguage layer files landed in this folder without a book-level bullet — `quantifiers.yml` + `quantifiers.sample.yml` → generated [`QUANTIFIER_PROFILE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/QUANTIFIER_PROFILE.md) + `quantifiers.json` (`npm run quantifiers`; register + method in [GRADATION_METALANGUAGE_KOCHERGINA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/GRADATION_METALANGUAGE_KOCHERGINA.md)). (Opus 4.8 `claude-opus-4-8`)

## [0.1.0] - 2026-07-07
### Added
- Initial mint: reprint source scan/edition (`.doc`, `.docx`) plus faithful
  `.mdx` extraction (aligned edition, 55 grid tables) via the `/docx-to-md`
  skill.
