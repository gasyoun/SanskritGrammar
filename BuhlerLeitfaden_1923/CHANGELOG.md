# Changelog — BuhlerLeitfaden_1923

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- **8 FALSE claim-verification misprints transcribed into [`errata.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/errata.yml)** — the 0.3.0 entry below queued these as "candidates" but never actually wrote them; closed the gap (HB-60/133/186/199/200/211/219/372, `page: 0` + Урок/mdx-line locator, no printed pagination available for this book). `ERRATA.md` regenerated (8 open, 0 fixed). (Sonnet 5 `claude-sonnet-5`)

## [0.3.0] - 2026-07-15
### Added
- **Backlog FULLY DRAINED — 403 verified claims (H797)** — all 339 pending candidates verdicted by 6 parallel agents under a shared drain style guide (loc-alignment validation + manual spot-check of every FALSE at merge) and promoted as HB-65..HB-403: register tally **381 TRUE · 7 OVERSTATED · 8 FALSE · 7 UNTESTABLE · 23 M.G. footnotes**; [`claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims_harvest.yml) is `candidates: []`. Bühler's own grammar survives nearly untouched (3 new OVERSTATED, each on a concrete counterexample: pṝ→pūrayati, ūrṇoti, apatha); **all 8 FALSE are misprint-class** — sentences self-contradicted by the paradigm/example printed next to them («окончание āḥ» vs brahmahā; kroṣṭṛ for kroṣṭu; «a» for «aṅ»; krudh in a t/p/s list; «гласный» for «согласный»; «sam давать» for san; the viśvapā exception list; plus the core's «impf. VII кл.») — so the claims register doubles as an errata sweep of the 1923/2008 text, 8 localized candidates queued for errata.yml. (Fable 5 `claude-fable-5`)

## [0.2.1] - 2026-07-15
### Added
- **Russian-language folder README documenting the register findings** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/README.md): по-русски, для читателя без английского — метод двух осей и триангуляция DCS/Уитни/Талмуд, итог 64 проверенных (58 TRUE · 4 OVERSTATED · 1 FALSE · 1 UNTESTABLE · 13 сносок М.Г.), шесть главных выводов (калибровка хеджей Бюлера vs Кочергина на одном числе -iṣya 56,8 %; редкое-прежде-частого; перевёрнутый перфект/имперфект; FALSE-опечатка «VII вм. VI»; корпусные сноски; двойная верификация PR #184), инструкция воспроизведения чисел и остаток фазы 2. Closes the gap that the register's synthesis/notes are English-only while the Kochergina register has its Russian reading-site overlay. (Fable 5 `claude-fable-5`)

## [0.2.0] - 2026-07-14
### Added
- **Claim-verification register (H797 Phase 2, first cross-grammar port)** — [`claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml): 64 falsifiable grammatical assertions verified on the two axes (fact vs DCS-2021/Whitney 1889/Tolchelnikov-Talmud · pedagogy) — 58 TRUE, 4 OVERSTATED (the Урок-I "все времена имеют обе формы" absolute; ā+Acc government; genitive "всякого рода"; perfect claimed rarer than imperfect vs DCS 61,986 > 47,554), 1 FALSE (a-aorist "как impf. VII кл." beside its own thematic paradigm — likely a 1923 misprint for VI), 1 UNTESTABLE, 13 M.G. frequency footnotes (PPP = 29.8% of all verbal tokens; optative 9.3%; periphrastic future 14× rarer than simple; absolutive -ya 78.4%). Backlog: [`claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims_harvest.yml) — 339 candidates from the 6-reader full-book sweep (404 harvested, 65 promoted/merged). Rendered table: [`CLAIMS_VERIFIED.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/CLAIMS_VERIFIED.md). (Fable 5 `claude-fable-5`)
- **Seed slice (same day, concurrent session — absorbed into the register above)** — [PR #184](https://github.com/gasyoun/SanskritGrammar/pull/184) landed BU-1..BU-5 + a 40-candidate harvest + the book-local battery [`verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/verify_claims_dcs.py) (kept — it independently reproduces the tense/mood shares, imperative person distribution and PPP suffix split via `tense_case_data.json`). Reconciliation: BU-1→HB-57, BU-4→HB-38, BU-5→HB-56 (double-verified), BU-3 promoted as HB-64 (imperative 2nd person 62.7%, cross-confirms Kochergina HK-17 to 0.3pp); BU-2's FALSE grading of the aorist «равноправно» claim re-graded TRUE in HB-61 — the same clause says «редких форм», so «равноправно» is semantic interchangeability, not frequency parity (reconciliation recorded in HB-61's note). (Sonnet 5 `claude-sonnet-5`)

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
