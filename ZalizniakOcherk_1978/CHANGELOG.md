# Changelog — ZalizniakOcherk_1978

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.9.0] - 2026-07-16
### Added
- **Залоговая картина Очерка как отдельная DCS-гипотеза (H1051, Fable 5 `claude-fable-5`;
  директива MG из адъюдикации A65, заметка к HB-100).** Реестр 74 → 96: OCH-75..OCH-96
  добирают все 22 нереестрованных залоговых утверждения (§§ 109-162, 206, 214 + примеч.
  § 115). **Секционный итог по 29 залоговым утверждениям (7 были в реестре): 23 TRUE ·
  1 OVERSTATED · 0 FALSE · 5 UNTESTABLE — залоговая МОРФОЛОГИЯ Зализняка безфлаговая;
  единственный флаг — синтаксический § 214** («в пассивных предложениях на первом месте
  обычно имя в I.»: даже среди пассивных предложений С выраженным творительным начальную
  позицию он занимает лишь в 18,6 % — 1 547 из 8 332; четвертый флаг кластера §§ 212-217).
  Новый инструмент [`och_voice_stats.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och_voice_stats.py)
  → [`och_voice_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och_voice_stats.json):
  ключевой факт снимка — `feat_voice` несет ТОЛЬКО `Pass` (36 701), Act/Mid в разметке НЕТ
  (реконфирмация KZ-2); P/Ā восстановлены по однозначным окончаниям (покрытие 49,1 %:
  **parasmaipada 77,8 % · ātmanepada 22,2 %** классифицируемой массы). Жемчужины: krāma-/krama-
  расщепление √kram подтверждено 84:4 и 94:7 (OCH-80); śī — media tantum 487:5 (OCH-84);
  «варианты» -ayāna- идут почти вровень с -ayamāna- (180:196, OCH-94); пассив непереходных
  аттестован (gam 289, sthā 62, OCH-95). **Сравнение с Бюлером (предрегистрированная
  гипотеза): подтверждена** — единственный залоговый флаг Зализняка синтаксический, тогда как
  флагманское залоговое утверждение Бюлера (HB-2, симметрия залогов) OVERSTATED ровно на тех
  ограничениях (§§ 140/146/149/159), которые Зализняк выписывает явно; OCH-85 против HK-38 —
  та же пара «скоуп есть/скоупа нет».

## [0.8.0] - 2026-07-16
### Added
- **Treebank instrument — §§212-217 syntax cluster MEASURED, OCH-65/66/67/68 flipped; first fact-axis flags in the register (H1022)** — new instrument [`treebank_syntax_stats.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/treebank_syntax_stats.py): discovered `dcs_full.sqlite`'s own `head`/`deprel` columns carry a genuine, fully-tagged UD-style treebank slice (223,751 tokens, 3.9% of the corpus, 29,433 complete sentences) that prior UNTESTABLE verdicts assumed didn't exist. **OCH-65** (prati adposition minority) confirmed TRUE: 20.3% of tagged `prati` tokens are unambiguously adpositional. **OCH-66** (word order) flipped OVERSTATED: modifier-precedes-head confirmed robustly (86.0%), but verb-final (46.4%) and subject-group-first (42.6%) do not clear a majority in any split tested. **OCH-67** (coordinate > subordinate) flipped FALSE: finite-subordinate clauses outnumber coordinate ones 6.5:1 (2,739 vs 419), the opposite of the claimed direction. **OCH-68** (the book's one absolute — antecedent noun always in the first clause) flipped OVERSTATED: 75.2% (n=335), not "always." **Genre-skew checked before verdicting, not assumed**: a classical-vs-Vedic/Śrauta-sūtra split and an Arthaśāstra-only isolation both rule out corpus skew as the explanation for OCH-66; OCH-67's classical subset shows a real but insufficient shift toward more coordination (33.3% vs 12.7% share). Two operationalization robustness checks (excluding trailing discourse-particles; restricting to single-clause sentences) each moved the root-final number under 5 points — not a metric artifact. Register: 74 verified = **65 TRUE · 2 OVERSTATED · 1 FALSE · 6 UNTESTABLE** — Zaliznyak held zero fact-axis flags through 70/74 claims, ending only when the syntax domain (previously untestable) became measurable; still the best-calibrated of the three cross-grammar books (3/74 = 4.1% flagged vs Bühler 5/64, Kochergina 12+24/234). Results: [`och65_68_treebank_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och65_68_treebank_stats.json).

## [0.7.0] - 2026-07-16
### Added
- **Root-shape parser — §59 six-slot template MEASURED, OCH-16 flipped to TRUE (H1012)** — new instrument [`root_shape_parser.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/root_shape_parser.py): over the 745-root Talmud Приложение-1 catalog, the alternating element (position 4) is located per each root's own `ryad` tag using §50's weak/guṇa/vṛddhi table (plus §54's before-vowel allomorphs); flanking consonants are tokenized (kṣ and aspirate digraphs count as one unit each, per §59's own exception) and classified sonant vs obstruent against the six positions `(s)-(obstruent)-(sonant)-NUCLEUS-(sonant)-(obstruent)`. **727/745 = 97.6% fit the template** (98.4% of the 739 roots where a nucleus could be identified at all) — confirming «подавляющее большинство» with a number. Named exceptions attested at real, minority scale: irregular v/m in slot 2 (21 roots), slot-1 s+obstruent (22), slot-6 obstruent clusters (126). The 15-case self-test replicates every one of §59's own worked examples (√i, √nī, √çru, √sthā, √styā, √iṣ, √pad, √krudh, √jīv, √cumb, √kṣṇu, √takṣ, √vyath, √mlā, √katth) before running over the full catalog. 18 residual non-fits individually documented, not a silent cap. Register: 74 verified = **64 TRUE · 0 OVERSTATED · 0 FALSE · 10 UNTESTABLE**. Results: [`och16_root_shape_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och16_root_shape_stats.json). (Sonnet 5 `claude-sonnet-5`, [H1012](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1012-Sonnet_SanskritGrammar_root-shape-parser-och16_16.07.26.md))

## [0.6.0] - 2026-07-16
### Added
- **Structural compound-type tagging — §193 dvigu MEASURED, OCH-58 flipped to TRUE; OCH-60's blocker probed and sharpened (H1004)** — new instrument [`compound_type_tagger.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/compound_type_tagger.py): first-member classification of all 623,119 nominal DCS mwt clusters (upos-classed, single-pass join). **Dvigu candidates (NUM-first, eka- excluded per §193's own parenthesis) = 16,406 = 15.3% of the determinative-shaped pool (1:5.4 vs adjective-first) and 2.6% of all nominal clusters — «сравнительно редко» confirmed**; top numerals tri/dvi/saptan/pañcan/catur. The tagger is function-blind BY DESIGN, and the reason is now a probe, not a presumption: DCS tags compound members lexically (mahābāhu's last member = NOUN in 192/193 clusters), so tatpuruṣa/bahuvrīhi FUNCTION is unrecoverable from this snapshot — OCH-60 stays honestly UNTESTABLE with the sharpened blocker recorded. Bühler's parallel Урок-XXXIII dvigu candidates unblocked for a future drain. Register: 74 verified = **63 TRUE · 0 OVERSTATED · 0 FALSE · 11 UNTESTABLE**. Results: [`och58_compound_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och58_compound_stats.json). (Fable 5 `claude-fable-5`, [H1004](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1004-Fable_SanskritGrammar_compound-type-tagging-och58_16.07.26.md))

## [0.5.0] - 2026-07-16
### Added
- **The causative detector — §167 diachronic half MEASURED, OCH-47 flipped to TRUE (H1001)** — new instrument [`causative_grade_detector.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/causative_grade_detector.py): DCS lemmatizes causatives as their own `-ay` lemmas, so guṇa~vṛddhi grade pairs (gamay~gāmay, smaray~smāray) are detected at lemma level, anchored on the root lemma existing in the same DB (screens denominatives), and sliced by the H1000 period map (one canonical map, imported). **150 anchored pairs, 57 fluctuating; the guṇa share falls exactly as §167 predicts** — all pairs 45.8% → 20.9% → 15.4% (веды → эпос → классика), fluctuating pairs **81.3% → 25.9% → 20.8%** (fourfold collapse; in the Vedic slice the «отступление» was the MAJORITY option). Purāṇa control at epic level (26.3%), consistent with H1000. Synchronic layer confirmed en passant (gam/jan/tvar guṇa-fixed per Whitney §1042; kṛ/mṛ/dhṛ vṛddhi-fixed). Register: 74 verified = **62 TRUE · 0 OVERSTATED · 0 FALSE · 12 UNTESTABLE**. Results: [`och47_causative_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och47_causative_stats.json) (per-root × period inventory + validation). (Fable 5 `claude-fable-5`, [H1001](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1001-Fable_SanskritGrammar_causative-grade-detector-och47_16.07.26.md))

## [0.4.0] - 2026-07-16
### Added
- **The period-tagging instrument — §207 flagship MEASURED, OCH-63 flipped to TRUE (H1000)** — new instrument [`period_style_gradient.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/period_style_gradient.py): a curated 41-text period map over the pinned DCS SQLite (dcs-conllu 04e0778; веды / эпос / классика + пураны as an epic-imitative CONTROL column; Buddhist-hybrid texts and lexica excluded as register-confounded), 4.07M tokens = 71.6% of the corpus. **All five style metrics rise monotonically vedic → epic → classical exactly as §207 predicts**: compound membership 12.2% → 40.5% → 57.3% of nominal tokens (near-5×), mean compound length 2.06 → 2.32 → 2.58, nominal share 43.3% → 52.7% → 56.4%, noun/verb ratio 2.13 → 2.89 → 3.28, finite-passive 2.7% → 5.8% → 7.5% (conditional). The purāṇas land BETWEEN epic and classical on the compound axis (48.1%) — the map measures language, not genre labels. **Design honesty baked in:** DCS verbal-feature annotation collapses for later texts (tagged ta-participles RV 1,874 → Daśakumāracarita 0, measured), so feats-based metrics are excluded from the verdict — only annotation-robust upos/mwt-segmentation axes decide. Register: 74 verified = **61 TRUE · 0 OVERSTATED · 0 FALSE · 13 UNTESTABLE**; OCH-47's blocker narrowed to a causative detector. Results: [`och63_period_style_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och63_period_style_stats.json) (per-text table + validation). (Fable 5 `claude-fable-5`, [H1000](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1000-Fable_SanskritGrammar_period-style-gradient-och63_16.07.26.md))

## [0.3.3] - 2026-07-15
### Added
- **Two H978 print-corruption finds folded into the errata register (H993)** — «√mam наклоняться» (§ 66 п. 3; должно быть √nam) and §67's rule-1 header «на a(ā), u(ū)» (contradicted by its own examples ji/nī/çru/bhū; должно быть «на i(ī), u(ū)») moved from the crosswalk instrument's header comment into [`errata.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/errata.yml) proper (`page: 0` + §/mdx-line locator per the Bühler precedent — the aligned mdx has no systematic print pagination); `ERRATA.md` regenerated (2 open) and the first print-ready [`ERRATA_PRINT_SHEET.html`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/ERRATA_PRINT_SHEET.html) generated. README residual «печатный лист опечаток» retired. (Fable 5 `claude-fable-5`, [H993](https://github.com/gasyoun/Uprava/blob/main/handoffs/H993-Fable_SanskritGrammar_errata-print-sheets_15.07.26.md))

## [0.3.2] - 2026-07-15
### Added
- **Strict token-weighted OCH-22 replication — the last H978 residual closed** — new instrument [`och22_token_weighted.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och22_token_weighted.py) performs the deferred lemma-frequency join keyed to citation forms (DCS-2026 SQLite × the crosswalk's 1978 columns; divergent keys resolved by identity-certain aliases ṛc→arc, bṛh→bṛṃh, jambh→jabh, tark→tarkay, carc→carcay; preverbed compounds attributed by preverb-strip; 14 rare Vedic roots reported unattested, never zero-faked) → [`och22_token_weighted.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och22_token_weighted.json) (8/8 validation). §67's «большинство употребительных корней — полноизменяемые» holds **stronger by tokens than by types**: 96.8% of 151,195 simplex R/M/N verbal tokens (96.6% of 220,228 incl. preverbed) on полноизменяемые roots vs 87% by type; top-20 frequent roots 19/20 full (only vṛdh defective); the §'s own examples rank #2 (gam), #3 (dṛś), #13 (bandh). OCH-22 register entry upgraded from a-fortiori to measured. (Fable 5 `claude-fable-5`, [H978](https://github.com/gasyoun/Uprava/blob/main/handoffs/H978-Fable_SanskritGrammar_1978-crosswalk-column-unblock-och21-23_15.07.26.md))

## [0.3.1] - 2026-07-15
### Changed
- **1978 columns merged upstream; companion CSV retired** — `build_1978_crosswalk.py` now maintains the five 1978 columns in place inside the Talmud crosswalk ([`morphoclass_crosswalk_1975_2014_2026.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv), 876 rows preserved incl. duplicates; idempotent re-runs). `crosswalk_1978.csv` deleted (its content lives upstream; the v0.3.0 release tag preserves the standalone artifact). Register refs (OCH-21..OCH-23) and both READMEs repointed. (Fable 5 `claude-fable-5`)

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
