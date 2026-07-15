# Changelog — KnauerFrazy_1908

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-07-15
### Added
- **Parse-audit backlog FULLY DRAINED — 214 audited parses, zero errors (H797 fork)** — every auditable footnote parse of all 19 Nr. blocks extracted from `block_backlog` (surface forms recovered from the source mdx) and audited by 5 parallel agents: [`parse_audit.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/parse_audit.yml) KN-1..KN-214 — **210 CONFIRMED · 4 QUESTIONABLE (citation gaps, not doubts) · 0 ERRORS** (~82 bare §-references skipped by rule). Seed follow-ups resolved: KN-10 pinned to Whitney §1059b-c **and found to be a corpus hapax attested exactly in the verse Knauer excerpts**; KN-9 re-scoped after the Talmud catalog's pada=U dissolved the deponent over-reading (audit the footnote, not the auditor's gloss). New generator [`build_parse_audit.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/build_parse_audit.py) renders [`PARSE_AUDIT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/PARSE_AUDIT.md) from the YAML (hand-written no more). Data defects logged: garbled Nr. 7 backlog row (audited from source), KN-3 loc self-mislabel fixed. (Fable 5 `claude-fable-5`)

## [0.2.1] - 2026-07-15
### Added
- **Russian-language folder README documenting the parse-audit findings** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/README.md): по-русски, в ряду README Кочергиной и Бюлера — история развилки метода (фразовая хрестоматия vs дискурсивная грамматика, постановление автора «адаптировать»), адаптированная единица анализа (корректность разбора сноски по Уитни 1889, без оси подачи), итог посева KN-1..KN-10 (8 CONFIRMED · 2 QUESTIONABLE · 0 ошибок из ~280-330), четыре вывода (жанр задаёт профиль надёжности; содержательные подтверждения §608/§771/§639; QUESTIONABLE = недобитые цитаты; жанр источника проверять до запуска конвейера), block_backlog и остаток фазы 2. Also the folder's first README (files, the 31-entry printed errata — the only populated one in the repo). (Fable 5 `claude-fable-5`)

## [0.2.0] - 2026-07-15
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
