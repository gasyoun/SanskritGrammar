# Changelog — KocherginaUchebnik_1998

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- **Виза автора применена к v1 методички — H1258 (Sonnet 5 `claude-sonnet-5`), 12 approve /
  1 reject / 0 defer из 13.** `METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md`,
  `_OTSYLKI_2026.md`, `_UPRAZHNENIIA_2026.md`: свернуты 12 одобренных заметок визы (рамка
  раздела I — scope-оговорка про опечатки/errata; занятие VI — открытый методологический
  вопрос; занятие XII — открытый вопрос про три частотных среза; занятие XXI —
  «полный список» aniṭ-корней/долгих-гласных исключений по требованию визы; занятие XXX —
  словоупотребление «пользуйтесь» → «употребляйте»; занятие XXXII — ссылка на критику
  Э. З. Лейтана, не найдена в репозитории, открытый пункт; занятие XXXVII — оговорка про
  редкость корневого аориста вне Ригведы; занятие XXXIX — библиография (диссертация +
  монография 1990 г. Кочергиной), открытый пункт; раздел III — номера страниц Конспекта
  и добавление Миллера, оба открытые пункты). Занятие X (2 заметки: -ā женского рода;
  имперфект-повествование) — **REJECT**: помечено `⟦MG-viza: REJECT⟧`, не готово к
  печати, ждет переписи автором. Все открытые пункты, требующие корпусного/
  библиографического разбора, сведены в приложение «Открытые вопросы визы (H1258)» в
  конце `_KOMMENTARII_2026.md` — ничего не изобретено без основания.
- **Фикс: две пропущенные заметки визы H1258 (zan-18, zan-22) — Sonnet 5 `claude-sonnet-5`.**
  Первый проход по [PR #508](https://github.com/gasyoun/SanskritGrammar/pull/508) сверял
  заметки против рендера review-sheet и упустил, что zan-18 и zan-22 несут собственные
  вопросы автора в исходном `decisions.json`/handoff-стабе (а не только уже вшитый в
  рукопись текст карточки A4). Занятие XVIII (HK-21) — открытый вопрос про сверку с
  «Талмудом»; занятие XXII — открытый вопрос про долю каузативов vs. прочих производных
  основ в перифрастическом перфекте. Оба добавлены как открытые пункты (9 вместо 7),
  ничего не изобретено.

## [0.13.0] - 2026-07-21
### Added
- **Корпусный слой методички (раздел IV) — H1297 (Fable 5 `claude-fable-5`).**
  [`METODICHKA_KOCHERGINA_CORPUS_LAYER_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_CORPUS_LAYER_2026.md):
  31 лемма по 9 занятиям раздела I, каждая с частотной полосой
  (топ-100/топ-1000/редкое по `rank_all` таблицы kosha `lemma_frequency.tsv`,
  DCS-производной) и одним живым примером из DCS-2026 с локусом; будущее — реальными
  формами -iṣya/-kṣya, корневой аорист — формами asthāt/adāt/dhīmahi/akramuḥ,
  перифрастический перфект — °ayām āsa. Русские переводы примеров авторские
  (закрытые слои выравнивания не открывались), ждут визы. Данные:
  [`corpus_layer/`](https://github.com/gasyoun/SanskritGrammar/tree/main/KocherginaUchebnik_1998/corpus_layer)
  (curated inventory + generated candidates + итоговый `corpus_layer.tsv`); сборка —
  [`scripts/build_corpus_layer.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_corpus_layer.py);
  регресс полос на 20 леммах + проверка локусов/прав —
  [`tests/test_corpus_layer.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_corpus_layer.py).
### Changed
- **A65 claim-level write-backs: HK-4a, HK-4b, HK-5, HK-15, HK-34 (H1276, Fable 5
  `claude-fable-5`).** Same write-back gap as the Bühler register: the notes were discharged
  by the H1049 fan-out, leaving no trace on the claim entries. HK-15 records that the
  narrative-switching effect is microscopic in the epic and **inverted in classical** texts
  (T2607-26, partially confirmed); HK-34 records that "весь раздел неверный" was **refuted for
  the factual layer** and upheld only for the framing (7 flags, H1050); HK-5 gains the Talmud
  root-count census, which independently declines to make the thematic aorist the largest type
  (is-aorist leads with 511 roots of 745). HK-4b is cross-referenced to H1228, which owns the
  Whitney policy sweep — no sweep duplicated here. HK-4a is **ESCALATED**: whether -ṣya/-iṣya
  are invariants of -syá is a morphonological position the corpus cannot settle.
- **HK-39 `mg_footnote` re-labeled from Ātmanepada-specific to whole-mood (H1253, Sonnet 5
  `claude-sonnet-5`; review sheet `sanskritgrammar-precative-label-dcs2026-visa_17.07.26`,
  policy B).** DCS-2026 doesn't tag pada, so the 577-token precative-mood figure cannot
  isolate the medium/Ātmanepada subset (DCS-2021's separate medium-only code was 221). The
  footnote now labels 577 as the whole mood and states it upper-bounds the Ātmanepada
  subset; the book's own medium-specific thesis (`claim_ru`) is untouched. Verdict unchanged.

## [0.12.0] - 2026-07-17
### Changed
- **HK-1 aorist number refreshed to the feat_formation count (H1136, Opus 4.8
  `claude-opus-4-8[1m]`).** The aorist figure moves from the DCS-2021 tense-code count (2,452 /
  0.31% of verbal) to DCS's own aorist-formation tag: **12,054 tokens = 2.30% of finite verbal
  forms** (root 5,690 · thematic 2,781 · s 1,508 · iṣ 1,077 · reduplicated 833 · sa 124 · siṣ 41).
  The old method undercounted by omitting the root and thematic aorists (the two largest classes).
  Verdict unchanged (TRUE — marginal beside the present system either way); this also resolves an
  internal inconsistency, since the register's own `aorist_type_ranking.py` (H1045) already summed
  to 12,054. Discovered via the Whitney register's `whitney_aorist_tagger.py` (H1134).

## [0.11.0] - 2026-07-16
### Added
- **Полный аудит раздела самас по кодбуку Лейтана (H1050, Fable 5 `claude-fable-5`; директива
  MG из адъюдикации A65: «весь раздел по самасам неверный — проверить все по Лейтану»).**
  Реестр вырос 234 → 260: HK-234..HK-259 добирают все 26 нереестрованных утверждений
  занятий XXX-XXXIII, XXXVIII, XXXX. **Секционный итог (46 утверждений): 36 TRUE · 7
  OVERSTATED · 0 FALSE · 3 UNTESTABLE — гипотеза опровергнута для фактов и подтверждена
  для каркаса:** все семь флагов сидят на классификационном скелете — определение
  композита (HK-234, исключает upapada-класс её же уроков), все четыре определения типов
  (HK-236 tatpuruṣa и HK-237 karmadhāraya — по частям речи вместо падежного отношения,
  оба ломаются её же аппозитивным расширением; HK-238 — аппозиции навязана семантика
  сравнения; HK-239 — dvigu без собирательного критерия, перехватывает числительные
  бахуврихи) и правило рода (HK-34); 36 механических правил раздела (изменения основ,
  порядок членов, сандхи стыков, двойств./множ. в dvandva) — верны. Синтез реестра
  дополнен третьим паттерном («система, не факты»); 3 UNTESTABLE — инструментные
  спецификации (ономастический ценз типов; акцентный ценз su-/dus-; анимационная
  разметка — ср. H1056).

## [0.10.0] - 2026-07-16
### Changed
- **HK-42 (a-/an- privative nouns, ~80% abstract) — part 2 sized, a third confound found (H1060)** — new instrument [`privative_noun_abstractness.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/privative_noun_abstractness.py) reuses `animacy_lookup.py`'s Sanskrit-WordNet sembank technique, rooted at abstraction/psychological_feature/knowledge/state/attribute/relation/event/act/phenomenon (all WordNet Tops nodes traditional grammar calls "abstract" — the narrow "abstraction" node alone gave a misleadingly low 30.6%). Measured **52.8% abstract** (171/324 classified privative noun lemmas) — short of ~80%, but NOT a refutation: candidate identification itself is contaminated by LEXICALIZED words that structurally pattern-match a-/an-+lemma without being felt as productive negations — asura ("demon") = a-+sura ("god", a real lemma), agni ("fire")+gni, aja ("goat")+ja, ahi ("snake")+hi, amṛta ("nectar")+mṛta. A minimum base-length filter doesn't fix this (checked). Same fundamental semantic-transparency wall as HK-226/227, discovered via a different structural pattern. Part 1 (≥1/3 of all prefixed nouns) stays untouched, same wall as HK-225/229. Results: [`hk42_privative_noun_abstractness_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/hk42_privative_noun_abstractness_stats.json). (Sonnet 5 `claude-sonnet-5`, [H1060](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1060-Sonnet_SanskritGrammar_privative-noun-abstractness-hk42_16.07.26.md))

## [0.9.0] - 2026-07-16
### Added
- **DCS animacy tagging built — HK-221 MEASURED TRUE; HK-86 sized with a major confound found (H1056)** — new reusable instrument [`animacy_lookup.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/animacy_lookup.py): DCS's own `m_wordsem` column carries Sanskrit-WordNet sense ids (per VisualDCS's A38 packaging paper), and the mapping table that turns those ids into a usable category (`word-senses.csv` + `sembank-relations.csv`) already existed in the upstream `dcs-conllu` mirror's `lookup/` folder — never built into a corpus-side animacy tagger before. Animate = descends from "person" (574) or "animal" (575) via the WordNet subclass hierarchy; two more roots were added after spot-checks caught real gaps — "spiritual being" (42842, WordNet doesn't treat deities as "person") and "imaginary being" (42775, mythical monsters like rākṣasa sit under a "concept/idea" branch, not "entity" at all). Validated against 24 known animate/inanimate nouns: 22/24 correct.
  - **HK-221** (dus-+S: few person-nouns, mostly inanimate) → **TRUE**: 6/56 classified dus-/dur-/duṣ-/duś-prefixed noun lemmas are animate (10.7%), confirming the claim clearly. Results: [`hk221_dus_prefix_animacy_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/hk221_dus_prefix_animacy_stats.json).
  - **HK-86** (most animate masc a-stems form feminine in -ī) → stays `UNTESTABLE`, but SIZED not "no instrument": a naive surface-form check showed -ā dominating overwhelmingly, but this turned out to be almost entirely BAHUVRĪHI COMPOUND-FINAL AGREEMENT contamination (e.g. "putrā" mostly the tail of compounds like diti-vinaṣṭa-putrā, not the substantive noun putrā "daughter"). Filtered via the `mwt` compound-span table — even after filtering, -ā still dominates on a thin n=22 residual. Recorded as INCONCLUSIVE with the confound documented, not forced to a verdict. Results: [`hk86_masc_animate_feminine_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/hk86_masc_animate_feminine_stats.json).
  - HK-42 (a-/an- privative nouns, ~80% abstract) still needs the same difficult prefixed-noun identification that hit a wall for HK-225/229 (H1047) — not re-attempted.

## [0.8.0] - 2026-07-16
### Added
- **HK-88 (Занятие XIII two-grade root vowel) — MEASURED TRUE; prior UNTESTABLE premise was wrong (H1047)** — new instrument [`two_grade_root_vowel_check.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/two_grade_root_vowel_check.py) reuses the H978 morphoclass crosswalk, no new corpus query. Re-checked the mdx source directly: the claim is NOT internally confused as the prior verdict thought — it precisely names Ocherk §62's own subtype-1 неполноизменяемость (weak grade = guṇa, vṛddhi distinct; tyaj is the identical example in both books). Among 429 roots classified "defective" in the crosswalk, **261 = 60.8% are A-series (vowel -a-)** vs only **34/424 = 8.0%** among "full"-alternating roots — a ~7.6× overrepresentation, confirming "обычно это корни с гласной -a-" clearly. Results: [`hk88_two_grade_root_vowel_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/hk88_two_grade_root_vowel_stats.json).
### Changed
- **HK-225/HK-229 (prefixed-verb share; prati- noun productivity) — independently re-attempted, same wall confirmed (H1047)** — a second, root-validated verb-lemma classification (930-root WhitneyRoots crosswalk) leaves 72% of DCS-2026's 11,096 verb lemmas unclassifiable (neither a known bare root nor a known preverb+root compound) — genuine morphological segmentation this pipeline doesn't have, not a smarter-query problem. HK-229's unvalidated noun-prefix count corroborates the prior finding (prati- ranks 10th, not top). Both stay `UNTESTABLE`, with the second attempt documented so neither is re-derived without new segmentation infrastructure. (Sonnet 5 `claude-sonnet-5`, [H1047](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1047-Sonnet_SanskritGrammar_two-grade-root-vowel-hk88_16.07.26.md))

## [0.7.0] - 2026-07-16
### Changed
- **HK-5 (Занятие XXXVII thematic aorist as the most widespread type) — MEASURED, flipped to OVERSTATED (H1045)** — new instrument [`aorist_type_ranking.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/aorist_type_ranking.py), reusing HK-207's (H1040) aorist-formation identification. Genuinely mixed result, dug into with a genre split + lexical-outlier check before verdicting (same diligence as OCH-66/67): **whole corpus, raw tokens — Type I root aorist leads (5,690) over Type II thematic (2,781); excluding bhū (≈38% of Type I's tokens) — Type I still leads (3,346 vs 2,781); by distinct-lemma count — Type IV s-aorist leads (216), Type II is 3rd (175).** Type II only tops the ranking in the classical (non-Vedic) text subset with bhū excluded — there it leads both by tokens (850 vs 724) and lemma-types (58 vs 52). 2/6 checks confirm Type II as top; 4 do not. Whitney's account may hold for Classical Sanskrit narrative specifically, but not as the flat unqualified "самый распространенный в санскрите" claim. Results: [`hk5_aorist_type_ranking.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/hk5_aorist_type_ranking.json). (Sonnet 5 `claude-sonnet-5`, [H1045](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1045-Sonnet_SanskritGrammar_aorist-type-ranking-hk5_16.07.26.md))

## [0.6.0] - 2026-07-16
### Changed
- **HK-207 (aorist register: narrative vs dialogue/drama) — SIZED, not "no instrument" (H1040)** — new probe [`aorist_register_probe.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/aorist_register_probe.py): checked the full 270-text DCS inventory first — DCS carries **zero drama/nāṭaka texts** (no Śakuntalā, no Mṛcchakaṭikā; Nāṭyaśāstra is a treatise about dramaturgy, not a play), so the literal comparison the claim names cannot be tested at all. Built a structural genre proxy instead — catechism-dialogue Upaniṣads (Bṛhadāraṇyaka, Chāndogya, Kaṭha, Kauṣītaki, Śvetāśvatara, Muṇḍaka, Taittirīya, Aitareya) vs Brāhmaṇa+Śrautasūtra ritual-prescriptive prose — using DCS-2026's aorist-specific `feat_formation` tags. Result: dialogue proxy 1.14% aorist share (91/8,010 verbal) vs narrative proxy 1.33% (1,530/114,924) — the opposite direction from the claim, though both are close to the whole-corpus baseline (1.20%). This null result does NOT refute Whitney's actual observation about dramatic dialogue specifically — Upaniṣadic catechism is formulaic ritual prose, not the colloquial register Whitney means, so the proxy itself is a stretch, not just its direction. Recorded as a sized negative pilot. Results: [`hk207_aorist_register_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/hk207_aorist_register_stats.json). (Sonnet 5 `claude-sonnet-5`, [H1040](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1040-Sonnet_SanskritGrammar_aorist-register-frequency-hk207_16.07.26.md))

## [0.5.0] - 2026-07-16
### Added
- **Методичка v1 (P0–P4) — три печатные рукописи-раздела (H807, Fable 5 `claude-fable-5`).**
  Первый исполненный слайс плана [`METODICHKA_KOCHERGINA_COMPANION_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md):
  - **Раздел I — комментарий точности и частотности**
    ([`METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md)):
    15 печатных заметок по 11 занятиям — все 12 не-TRUE утверждений реестра (11 OVERSTATED
    + единственный FALSE HK-16 «-ī/-ū всегда женского рода»), два помеченных TRUE
    (HK-21/HK-26) и карточка Занятия XXII (дистрибуция вспомогательных перифрастического
    перфекта по визе P3/A4); приложение — 11 частотных бейджей М. Г. таблицей. Каждое
    число цитируется по идентификатору `claims.yml`, UNTESTABLE в печать не включены.
  - **Раздел II — упражнения**
    ([`METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md)):
    по тем же 11 занятиям — засвидетельствованные чтения только из общественного достояния
    (Кнауэр 1908 / Bühler 1878, по банку `scripts/data/sentences.json` и конкордансу;
    аористный блок — из Кнауэра Nr. 14 напрямую, банк его не покрывает) + авторские дриллы
    с ключами и переводами, все помечены ⟦MG-viza⟧.
  - **Раздел III — отсылки «см. также»**
    ([`METODICHKA_KOCHERGINA_V1_OTSYLKI_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_OTSYLKI_2026.md)):
    попозанятийные привязки к Очерку-1978 (по §§), Конспекту-2004 (по разделам),
    Талмуду-2026 (по главам), Кнауэру (по Nr.) и Гасунсу-2014 (seṭ/aniṭ), выверенные по
    цифровым текстам репозитория.
- **`errata.yml`: поле `edition` в схеме записи** — привязка страницы/строки к конкретному
  тиражу (K-1: эталон — оригинал 1998 г.); список намеренно пуст — печатного списка
  опечаток и второго издания для diff нет, выдумывать errata запрещено гардрейлом H807.
### Changed
- План методички: § 2 обновлен на осушенный реестр (234), § 5 помечен «v1 EXECUTED»,
  K-2 решен по рекомендации (ручные разделы v1, реестры `exercises.yml`/`crossrefs.yml` —
  v2); metadoc — строка ревизии + бэклог (пп. 1/3 закрыты, п. 5 «расширение v2» добавлен).
### Gate
- **Визовый пакет:** review-sheet `sanskritgrammar-metodichka-kochergina-v1_16.07.26_review.html`
  (13 карточек, локальный `review/`, реестр листов — Uprava). До визы автора разделы —
  черновик рукописи; следующая ревизия прозы — по стайл-гайду Sangram (H1003), когда тот
  получит визу.

## [0.4.1] - 2026-07-15
### Added
- **Russian-language folder README documenting the register findings** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/README.md): по-русски, зеркало бюлеровского README — метод двух осей и триангуляция DCS/Уитни/Талмуд, итог 234 проверенных (210 TRUE · 11 OVERSTATED · 1 FALSE · 12 UNTESTABLE · 11 сносок М.Г. · 24 с флагом), семь главных выводов (два типа сбоя: сверхобобщение универсалий с единственным FALSE HK-16 и слепота к частотности с шаблоном HK-4 -iṣya 56,8 %; честная зона UNTESTABLE; оправданные частотные хеджи; кросс-грамматический контроль с Бюлером; корпусные сноски М.Г.), инструкция воспроизведения чисел, связи с оверлеем/квантификаторами/методичкой. Синтез реестра был доступен только по-английски (CLAIMS_VERIFIED.md); русский оверлей показывает таблицу, но не выводы. (Fable 5 `claude-fable-5`)

## [0.4.0] - 2026-07-14
### Added
- **Quantifier metalanguage register (H800)** — `quantifiers.yml` per source → generated
  `QUANTIFIER_PROFILE.md` (via `scripts/harvest_quantifiers.py` + `scripts/build_quantifiers.py`,
  `npm run quantifiers`). Every metalanguage quantifier (редко / обычно / только / некоторые /
  могут / всегда …) harvested and tagged anchored/unanchored by an auto-proxy, calibrated
  against a hand-verified stratified sample (`quantifiers.sample.yml`, adjudicator Opus 4.8).
  Extends `GRADATION_METALANGUAGE_KOCHERGINA.md` with the three missing quantifier classes
  (modality/optionality, indefinite subset, hedged universals) and a measured four-way
  comparison against Zalizniak's Ocherk 1978 / Konspekt 2004 / Morphology 1975. Findings:
  per-quantifier anchoredness is high and *similar* across the three descriptive grammars
  (~83–88 % by hand count) — the crisp "hers hang on nothing" thesis is not supported; the
  real discriminators are density (~1.5–2× per grammar-prose line, not 9×) and anchor *type*
  (Kochergina anchors on affixes/forms with **0 % §**; the 1975 classification on its numbered
  formal calculus, **90 %**).

## [0.3.0] - 2026-07-12
### Added
- **Claim register drained to completion — 43 → 234 verified claims (H797).** The full
  223-candidate harvest backlog ([`claims_harvest.yml`](claims_harvest.yml)) was verdicted on
  both axes and promoted into [`claims.yml`](claims.yml) (HK-1..HK-233) in seven lesson-ordered
  batches: 210 TRUE · 11 OVERSTATED · 1 FALSE · 12 UNTESTABLE, with 11 M.G. frequency footnotes.
  The register now covers all 40 Занятия (phonology → sandhi → declension → conjugation → aorist →
  compounds → prefixation → adverbs). The harvest backlog is now empty (`candidates: []`).
- **`verify_claims_dcs.py` extended with reproducible backlog metrics** — a vowel census over the
  full DCS-2021 running text (0.csv: a+ā = 65.8% of vowels; ṛ 199,930 vs ṝ 1,588 / ḷ 0 / ḹ 0),
  verb-class share (thematic I/IV/VI/X = 70.2% of present-system tokens; class II frozen at
  154,301), a past-tense competition (imperfect 47,554 · perfect 61,986 · aorist 2,452) and the
  case-slot token distribution — so every M.G. footnote number is re-runnable. The seven new
  DCS-computed footnotes (N.sg visarga, Acc.sg anusvāra, ṛ dominance, vowel-length, class-II
  frozenness, injunctive rarity 0.30%) all reproduce from the committed corpus.
- Roadmap for a thin printed companion-methodichka (`METODICHKA_KOCHERGINA_COMPANION_2026.md`
  + its metadoc): five commentary pillars (accuracy, clarity/frequency, errata per edition,
  extra exercises, cross-references), hybrid source-of-truth model (registry data + authored
  prose), and a thin-v1 / comprehensive-v2 split. Consumes the now-234-claim register
  and errata system rather than rebuilding. Decisions A–D locked with MG; first execution
  slice minted as H807 (Fable).

## [0.2.0] - 2026-07-12
### Added
- **Claim-verification register (H768)** — `claims.yml` → generated `CLAIMS_VERIFIED.md`
  (via `scripts/build_claims.py`, `npm run claims`), a register *distinct* from `errata.yml`:
  it catalogues the textbook's *falsifiable grammatical assertions* and grades each on two
  axes — **fact** (true vs. the DCS-2021 corpus + Whitney 1889, with the actual number) and
  **pedagogy** (is the presentation defensible). Full-textbook sweep of all 40 Занятия:
  **43 claims** (verb-system seeds HK-1..HK-6 + harvest HK-7..HK-42) — 28 TRUE, 11 OVERSTATED,
  1 FALSE, 3 UNTESTABLE; 16 flagged for an overreach or presentation issue.
- **Reproducible corpus numbers** — `verify_claims_dcs.py` recomputes every DCS figure
  (imperative-by-person, conditional/precative rarity, PPP -ta/-na split, future allomorphy,
  aorist/gerundive share) into `claims_dcs_stats.json`.
- **Reading-site overlay** — `<KocherginaClaims/>` (`src/components/KocherginaClaims.jsx`) +
  `CLAIMS_OVERLAY.mdx` badge the two-axis verification over the reading site (Kochergina 1998
  stays in-copyright — verification metadata only, no text re-release).

## [0.1.0] - 2026-07-07
### Added
- Converted `.docx` → `.md`/`.mdx` via the `/docx-to-md` skill (Pandoc GFM with
  grid tables — 124 grid tables, the most of any book here — images extracted
  to `Kochergina_unicode_media/`, UTF-8 Devanagari intact).
- Initial mint: reprint source edition (*Учебник санскрита*, 1998).
