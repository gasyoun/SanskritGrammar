# Changelog — BuhlerLeitfaden_1923

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.5] - 2026-07-17
### Changed
- **Aorist figure refreshed in HB-1/HB-20/HB-61 (H1140).** 2,452 / 0.31% -> 12,054 / 2.30%
  (feat_formation), which the old tense-code method undercounted by omitting root+thematic aorists.
  Verdicts unchanged (aorist stays rarest of the three past tenses; HB-61 ratio 1:25 -> ~1:4/~1:5).
  Found by the new cross-register consistency check.

## [0.3.4] - 2026-07-16
### Added
- **HB-21 (Урок XII.3б u-stem feminine -vī frequency) — MEASURED TRUE (H1044)** — new instrument [`u_stem_feminine_freq.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/u_stem_feminine_freq.py): the prior blocker ("needs lemma+gender+agreement joins the relational dump does not carry") didn't hold up — DCS lemmatizes guru/bahu to one lemma across genders, so a surface-form split of the already `feat_gender=Fem`-tagged tokens (gurv-/bahv- glide-inflected vs plain u-stem shape) needs no join at all. Testing Bühler's own two named examples: **guru — 95 -vī tokens vs 77 plain-u = 55.2%** (a real but narrow majority); **bahu — 150 -vī tokens vs 20 plain-u = 88.2%** (a strong majority). Both confirm "более употребительны" in the claimed direction, though not by an identical margin. Results: [`hb21_u_stem_feminine_freq.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/hb21_u_stem_feminine_freq.json). (Sonnet 5 `claude-sonnet-5`, [H1044](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1044-Sonnet_SanskritGrammar_u-stem-feminine-freq-hb21_16.07.26.md))

## [0.3.3] - 2026-07-16
### Added
- **HB-256 (Урок XXXII.3 suppletive comparative/superlative frequency) — MEASURED TRUE (H1042)** — new instrument [`suppletive_comparative_freq.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/suppletive_comparative_freq.py): ranked all 9 pairs Bühler names (antika/alpa/guru/dīrgha/praśasya/priya/bahu/yuvan/vṛddha → nedīyas·kanīyas·garīyas·drāghīyas·śreyas(jyāyas)·preyas·bhūyas·yavīyas·varṣīyas(jyāyas)) against every ADJ lemma ending in the same suffixes (103 comparative + 141 superlative types after excluding confirmed non-superlative homographs — ṣaṣṭha "sixth", vāsiṣṭha patronymic, etc.). **7/10 of the comparative top-10 and 6/10 of the superlative top-10 are named-set members** — bhūyas #1 (654 tok), śreyas #2, kanīyas #3, śreṣṭha #1 (2,952), bhūyiṣṭha #3 — confirming "наиболее часто" as an absolute-frequency claim. Results: [`hb256_suppletive_comparative_freq.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/hb256_suppletive_comparative_freq.json). (Sonnet 5 `claude-sonnet-5`, [H1042](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1042-Sonnet_SanskritGrammar_suppletive-comparative-freq-hb256_16.07.26.md))

## [0.3.2] - 2026-07-16
### Changed
- **HB-158 (Урок XX gender resolution across mixed-gender conjuncts) — SIZED, not "no instrument" (H1035)** — new probe [`gender_resolution_probe.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/gender_resolution_probe.py), reusing the same DCS head/deprel treebank slice ZalizniakOcherk_1978's [H1022](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/treebank_syntax_stats.py) opened: 1,847 mixed-gender NOUN `conj` groups exist, but restricting to genuine PREDICATE adjectives whose resolved gender covers the whole coordination (not an ordinary attributive adjective trivially agreeing with one conjunct) leaves **n = 4** in the entire annotated slice. 2/4 match the stated rule exactly; 2/4 show agreement with the nearest/first-listed conjunct instead — the RIVAL proximity/attraction strategy this entry's own note already anticipated from Whitney/Speijer. n=4 (2-for/2-against) is a genuine data desert, not a missing instrument — recorded with numbers so it is never re-derived. Results: [`hb158_gender_resolution_probe.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/hb158_gender_resolution_probe.json). (Sonnet 5 `claude-sonnet-5`, [H1035](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1035-Sonnet_SanskritGrammar_gender-resolution-probe-hb158_16.07.26.md))

## [0.3.1] - 2026-07-16
### Changed
- **HB-268 (Урок XXXIII dvigu proportions) — blocker MEASURED, not presumed (H1008 negative pilot)** — the H1004 structural compound tagger finds the NUM-first class, but its final-member gender census (5,763 clusters probed, 99.9% gender coverage) shows **56% masculine finals**: the surface class is dominated by numeral BAHUVRĪHIS (caturbhuja-type), which are precisely not dvigus. With compound-FUNCTION tagging absent from DCS (OCH-60 probe), the «большей частью / реже» proportions stay uncountable — dead end recorded with numbers so it is never re-derived. (Fable 5 `claude-fable-5`, [H1008](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1008-Fable_SanskritGrammar_root-shape-parser-och16_16.07.26.md))
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
