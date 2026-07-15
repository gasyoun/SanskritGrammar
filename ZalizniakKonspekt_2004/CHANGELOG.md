# Changelog — ZalizniakKonspekt_2004

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-07-15
### Added
- **Backlog FULLY DRAINED — 17 verified, all TRUE — by BUILDING the missing instrument (H797)** — all 15 backlog candidates promoted ([`claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/claims.yml) KZ-3..KZ-17): **17 TRUE · 0 OVERSTATED · 0 FALSE · 0 UNTESTABLE**; [`claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/claims_harvest.yml) is `candidates: []`. The five Rigveda exact fractions were unblocked by a NEW period-isolation instrument — [`rigveda_kz_fractions.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/rigveda_kz_fractions.py) over the pinned VisualDCS SQLite master (dcs-conllu `04e0778`, the H953 pilot's snapshot) → [`rigveda_kz_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/rigveda_kz_stats.json) — and measured **astonishingly exact**: 1/3 claimed vs 33.2% measured (-āsas, to 0.1pp), 7/8 vs 84.9%, 3/5 vs 65.6%, 1/2 vs 42.3%, 5/6 vs 76.9% — hand-era Vedic-philology fractions reproduced by a 2026 treebank. The same instrument flipped KZ-11 (injunctive 7.3% of RV finite verbs vs 0.5% MBh, ≈15×; optative reversed) and KZ-12 (ta-participle predication 1.7% of RV verbal roots vs 11.8-18.4% epic samples — the first measured point on the Ocherk-§207 style-I/style-II arc) from UNTESTABLE to measured TRUE. Zaliznyak across both books: 91 verified, zero fact-axis flags. Cross-book verdict pairs KZ-5=OCH-43, KZ-2=OCH-42, KZ-6=OCH-64; the Whitney-adjudicated diachrony precedent (KZ-7, §§1246-1247). (Fable 5 `claude-fable-5`)
- **Claim-verification register (H797 Phase 2 seed)** — [`claims.yml`](claims.yml) (KZ-1..KZ-2,
  two-axis fact/pedagogy grading) + [`claims_harvest.yml`](claims_harvest.yml) (15-candidate
  backlog from a full 657-line read, 17 total) + [`verify_claims_dcs.py`](verify_claims_dcs.py).
  Deliberately small seed: this book turned out the hardest of the four Zaliznyak/Kochergina/
  Bühler/Knauer sources checked to verify — overwhelmingly tabular/mechanical content, and
  several of its richest claims are Rigveda-specific exact fractions (1/3, 7/8, 3/5, 1/2, 5/6 of
  cases) needing period-isolated corpus data confirmed NOT to exist in this pipeline's current
  DCS ground truth. Both seed claims TRUE, one via cross-reference to Kochergina's HK-4 (seṭ/aniṭ
  future-stem split), one from DCS-2021's codebook itself carrying no separate medium-voice
  periphrastic-future tag.

## [0.1.1] - 2026-07-15
### Added
- **Russian-language folder README** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/README.md): книга и жанр (по калибровке [ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md)), существующие исследовательские слои (профиль квантификаторов H800, три модели Зализняка, родословная Уитни→Зализняк→Талмуд и оговорка о масштабе для планки ≥50), и статус реестра проверки утверждений: В ОЧЕРЕДИ фазы 2 H797 — с выполненной предварительной проверкой жанра (урок кнауэровской развилки). (Fable 5 `claude-fable-5`)
- **Changelog backfill (13-07-2026, H800):** the quantifier-metalanguage layer files landed in this folder without a book-level bullet — `quantifiers.yml` + `quantifiers.sample.yml` → generated [`QUANTIFIER_PROFILE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/QUANTIFIER_PROFILE.md) + `quantifiers.json` (`npm run quantifiers`; register + method in [GRADATION_METALANGUAGE_KOCHERGINA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/GRADATION_METALANGUAGE_KOCHERGINA.md)). (Opus 4.8 `claude-opus-4-8`)

## [0.1.0] - 2026-07-07
### Added
- Initial mint: reprint source scan/edition (`.doc`, `.docx`) plus faithful
  `.mdx` extraction (6 grid tables) via the `/docx-to-md` skill.
