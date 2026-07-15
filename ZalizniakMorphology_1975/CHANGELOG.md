# Changelog — ZalizniakMorphology_1975

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-07-15
### Added
- **Russian-language folder README** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/README.md): по-русски, замыкает серию README всех источников программы — паспорт статьи (verb-only исследовательская работа, предок машинерии Талмуда по калибровке трёх моделей), слой квантификаторов H800 (254 квантификатора, ~90 % якорей на собственном исчислении тип/позиция/ряд/ступень и лишь 2 % на §§), аудит классификации корней (четвёртый жанр верификации: 93 % сверки с WhitneyRoots после нормализации ç/ṁ↔ś/ṃ, объяснённые несовпадения, три честно открытых пункта), статус инфраструктурного прохода и итог программы (942 утверждения + 214 разборов + классификатор; у Зализняка по трём текстам — ни одного фактического флага). (Fable 5 `claude-fable-5`)
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
- **Independent corroboration at scale via Tolchelnikov's Talmud data** (same-day follow-up, MG's
  tip) — [`TolchelnikovTalmud_2026/data/z_root_map.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/z_root_map.json)
  (905 roots from samskrtam.ru/z/, built on the same 1975 model) corroborates 4 of 5
  alternation-series group counts within ±6% (A1, A2, L, I+U+R; M+N is a −27% outlier, unresolved)
  and 2 of 3 Table 5 aniṭ/seṭ columns within a few percent (aniṭ 178 vs ~170, seṭ 325 vs ~320).
  Per-root series cross-validation (122 agree/67 disagree/28 not found) surfaced a genuine,
  unresolved `0`-vs-`1`/`2` subseries-tagging ambiguity in Talmud's data — tried and reverted a
  heuristic fix rather than force a wrong answer; documented as an open question for a trained
  Sanskritist, not glossed over.

## [0.1.0] - 2026-07-06
### Added
- Initial mint: English translation (I. Tolchelnikov, ed. M. Ishimbaev) of Zaliznyak's 1975
  morphophonological root-classification paper, `.docx` + `.mdx`.
