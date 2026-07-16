# Changelog — KocherginaUchebnik_1998

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
