# Changelog — ZalizniakOcherk_1978

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-07-15
### Added
- **The 1978 crosswalk column — §68 CONFIRMED, OCH-21..OCH-23 flipped to measured TRUE (H978)** — new instrument [`build_1978_crosswalk.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/build_1978_crosswalk.py) derives per-root ряд-1978/открытость/полноизменяемость for 749 roots from Ocherk's OWN §§66-67 rules + named lists (15/15 validation against the §§' own examples) → [`crosswalk_1978.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/crosswalk_1978.csv) + [`och_1978_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och_1978_stats.json). The faithful §68 join (A₂ excluded per §63, полноизменяемость filtered, §66's own open-M/N indices): group A = **92.6% aniṭ-or-veṭ** (plain seṭ 7.4%), group B = **93.0% seṭ-or-veṭ** (plain aniṭ 7.0%) — the structural prediction behind the programme's flagship -iṣya fact is real; the recorded naive-join inversion is fully explained (2026-vs-1978 open-M/N index disagreement, missing filter, ignored A₂ exclusion). OCH-21 (19/13/18 «примерно поровну») and OCH-22 (139/21 = 87%) confirmed by the same run. Register: 74 verified = **60 TRUE · 0 OVERSTATED · 0 FALSE · 14 UNTESTABLE**. Two new errata-class source finds («√mam» for nam in §66; §67's rule-1 header vs its own examples). (Fable 5 `claude-fable-5`, [H978](https://github.com/gasyoun/Uprava/blob/main/handoffs/H978-Fable_SanskritGrammar_1978-crosswalk-column-unblock-och21-23_15.07.26.md))

## [0.2.0] - 2026-07-15
### Added
- **Backlog FULLY DRAINED — 74 verified claims, zero fact-axis flags (H797 Phase 2)** — all 68 pending candidates verdicted and promoted ([`claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/claims.yml) OCH-7..OCH-74; [`claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/claims_harvest.yml) now `candidates: []`): **57 TRUE · 0 OVERSTATED · 0 FALSE · 17 UNTESTABLE · 7 M.G. footnotes** — the programme's first zero-flag drain; calibration ranking now Зализняк (0/74) > Бюлер (5/64) > Кочергина (12/234 fact-axis). New reproducible metrics in [`verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/verify_claims_dcs.py): final-consonant census (final l 838 = 0.025%; ṇ 118 vs ṅ/ñ 659/1,934; final-stop ranking t 99,262 >> k 4,100), saḥ/so/sa surface split (95.1% sandhi variants), i-rates by suffix, rare-mood tokens (0.37% of verbal), and the Talmud Приложение-1 set×series join. The 17 UNTESTABLE entries name their missing instruments (period tags, treebank, compound typing, 1978↔2026 series crosswalk, root-shape parser); two negative pilots recorded with numbers (OCH-23 naive series join inverts §68; OCH-24 aggregate i-rate proxy inverts §63) so the dead ends are never re-derived as refutations. Headline contrast: the verb-accent rule grades Кочергина OVERSTATED («никогда», HK-10) and Зализняк TRUE («как правило», OCH-72) — same fact, third data point that presentation calibration is the measurable axis. (Fable 5 `claude-fable-5`)
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
