# Changelog

All notable changes to this repo's shared infrastructure (errata system, site
tooling, docs) are documented here. **Book-specific changes now live in each
book's own `<Book>/CHANGELOG.md`** (per-book release scheme, H318):
[ApteSyntax_1885](ApteSyntax_1885/CHANGELOG.md) ·
[BuhlerLeitfaden_1923](BuhlerLeitfaden_1923/CHANGELOG.md) ·
[GasunsDhatu_2014](GasunsDhatu_2014/CHANGELOG.md) ·
[KnauerFrazy_1908](KnauerFrazy_1908/CHANGELOG.md) ·
[KocherginaUchebnik_1998](KocherginaUchebnik_1998/CHANGELOG.md) ·
[ZalizniakKonspekt_2004](ZalizniakKonspekt_2004/CHANGELOG.md) ·
[ZalizniakOcherk_1978](ZalizniakOcherk_1978/CHANGELOG.md) ·
[TolchelnikovTalmud_2026](TolchelnikovTalmud_2026/CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Each book tags/releases independently as `<book-slug>-vX.Y.Z`; this root
changelog tags as `vX.Y.Z`.

## [Unreleased]

### Changed
- **Whole claim programme standardized on DCS-2026 corpus figures (H1172, Opus 4.8 `claude-opus-4-8[1m]`).** MG ruled 17-07-2026 to replace the DCS-2021 vintage numbers that had been the shared basis of the six claim registers with recomputed DCS-2026 values, so every register cites one corpus snapshot — resolving the version-pair the [H1164 consistency check](scripts/check_claims_consistency.py) had explicitly left open. New [`scripts/dcs2026_figures.py`](scripts/dcs2026_figures.py) computes the authoritative table from `dcs_full.sqlite` (denominator = **523,738** finite verbal forms): present **353,215** · imperfect **46,695** · perfect **90,001** · aorist 12,054 · simple future **21,556** · optative **91,912** · imperative **56,506** · injunctive **5,258** · conditional **340** · precative **577** · pluperfect 200. **44 figure/percentage refreshes** across [Apte](ApteSyntax_1885/claims.yml), [Bühler](BuhlerLeitfaden_1923/claims.yml), [Kochergina](KocherginaUchebnik_1998/claims.yml), [Whitney](WhitneyGrammar_1889/claims.yml), [Konspekt](ZalizniakKonspekt_2004/claims.yml), [Ocherk](ZalizniakOcherk_1978/claims.yml); registers regenerated. **NO verdict flips:** perfect > imperfect (WH-4/HB-20/HB-57/OCH-31) holds and strengthens (90,001 > 46,695); aorist rarest of the three pasts holds (aorist:perfect ~1:7, :imperfect ~1:4); HK-116 "comparable" reworded since the perfect now exceeds the imperfect (verdict TRUE kept); HB-39 (PPP vs present) checked — DCS-2026 present-indicative 203,363 < DCS-2021 PPP 233,080, so the like-scope direction holds (the flag was a present-finite-vs-indicative scope artifact). Version-specific figures with no DCS-2026 equivalent kept + tagged: **periphrastic future 1,290** (no distinct 2026 tense tag) and the **precative-medium** (DCS-2026 gives only the whole-mood total 577; `feat_voice` does not tag pada — verified all 577 `feat_voice=None`, so the "medium/Ātmanepada" label is bounded above by 577 and flagged for author viza). The consistency check + pytest gate were updated to the DCS-2026 allowed-value sets and are green.

## [0.59.0] - 2026-07-17

### Added
- **Sangram ядро W2 — статья SG-MO-021 «Будущее время и кондиционал» — статья-кандидат, ПЕРВАЯ сверх открывающей квоты 19 (H1180, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/future/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/future): будущее **замыкает финитную систему времён** (презенс/имперфект/аорист/перфект/будущее — все нативно размечены). Нативный тег `Tense=Fut` = **21 556 финитных токенов (4,1 % [4,06–4,17])**. Простое vs перифрастическое разделены **нативно** (`feat_formation`): простое (s-)будущее **20 216 (93,8 %)**, перифрастическое -tā **1340 (6,2 %)** (во главе bhavitā, kartā). Кондиционал (контрфактическое «сделал бы», `feat_mood=Cond`) **340 (1,6 %)**; причастие будущего **1575** — отдельно. Уникальный профиль: будущее — **самая перволичная финитная форма** (1 л. **36,4 %** [35,8–37,1] против 0,5 % у пассива, narrative-3-е у имперфекта) — язык заявленного намерения (bhaviṣyati, vakṣyāmi «скажу», kariṣyāmi «сделаю»). Скрипт [`sg_mo_021_future.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_021_future.py); toc_validate + article_validate (20 манифестов) + docusaurus build green. Первая статья, произведённая по решению автора продолжить производство ядра сверх открывающей квоты (opening set остаётся 18/19). Публикация гейтится авторской визой.
- **Fix: SG-WF-004 taddhita example IDs `ex:taddhita:N` → `ex:taddhita-overview:N`** (H1180). The manifest/MDX example IDs must match the article slug (`taddhita-overview`); the mismatch made `article_validate --all` FAIL on `main` (shipped in #368, not caught by the segmentation synthesis #369/#370). `--all` restored to green (21 PASS).

## [0.58.0] - 2026-07-17

### Changed
- **Sangram ядро W2 — обзор SG-WF-004 taddhita дополнен положительной половиной (слой сегментации); свод двух сессий ([PR #369](https://github.com/gasyoun/SanskritGrammar/pull/369); Opus 4.8 `claude-opus-4-8[1m]`).** Честный негатив [v0.57.0](https://github.com/gasyoun/SanskritGrammar/releases/tag/v0.57.0) (H1168) сохранён дословно (ручная адъюдикация 30/60, `adjudication.json`, `ex:taddhita:1-5`), но добавлено то, что первая версия упустила: **слой сегментации DCS** выделяет четыре самых продуктивных суффикса отдельными морфемо-токенами (`-tva` 163754, `-tā` 203679, `-maya` 109021, `-vat` 167498), а деривационная база восстановима на `idx-1` (**99,8 %**) → продуктивная абстрактная/материальная taddhita **нативно счётна: 24 108 токенов** (нижняя оценка; целиком-лемматизированные sattva/tattva/devatā не входят). Абстракты доминируют: `-tva` 10 850 / 2883 базы, `-tā` 5 919 / 1843, `-vat` 4 125 / 1418, `-maya` 3 214 / 650; база `-tva` по POS — ADJ 4876 / NOUN 4441 / VERB 1107. Целиком-лемматизированный посессив/относит./патроним (`-in/-mant/-vant/-ika/-ya`) остаётся **не счётным** (§ 4, EM5; поверхностный отбор ~50 % ложных). +4 сегментированных примера (amṛtatva/vṛddhatā/tejomaya/mṛgavat); скрипт [`sg_wf_004_taddhita_overview.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_004_taddhita_overview.py) + [`coverage_summary.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/taddhita-overview/data/coverage_summary.json)/`validation_sample.tsv`. Заслуга обеих сессий: H1168 (адъюдикация) + H1178 (сегментация). Ядро W2: **18/19** (без изменения счёта — SG-WF-004 уже засчитан v0.57.0). docusaurus build (smoke) + python tests green. Публикация гейтится авторской визой.

## [0.57.0] - 2026-07-17

### Added
- **Sangram ядро W2 — обзорная статья SG-WF-004 «Вторичная деривация (taddhita): обзор» — статья-кандидат, эндшпильный слот (H1168, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/taddhita-overview/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/taddhita-overview): **самый тяжёлый негатив эндшпиля**. taddhita размечена **0 признаков** деривации и — в отличие от kṛt (SG-WF-002), у которого была нативная формо-половина 483 623 токена — **не имеет размеченного подмножества** вовсе. Именной универсум `NOUN+ADJ` = **2 996 410 токенов (52,7 %)**, но taddhita в нём без пометы. Единственная зацепка — поверхностный отбор по финали леммы — **проваливается**: по ручной адъюдикации посеянной частотно-взвешенной выборки (60 лемм-типов, 10 канонических суффиксов) настоящей taddhita **лишь 30 — точность 50 %**; прочие 50 % — kṛt-герундивы/агенты (`-ya/-aka/-in` от корней, 27 %: kārya, śiṣya, vyāpaka), первичные имена (20 %: sūrya, haya, hiraṇya, priya), местоименные формы (`tā`, `tva`) и композиты. Крупнейший загрязнитель — `-ya` (224 191 токен). Путь реестра C2 «via MW etymology» тот же P5 измерил как малополный (точность 0,75, **полнота 0,09**). Сравнимо с kṛt-именами (P5 ~41 % точности), но жёстче по охвату. Скрипт [`sg_wf_004_taddhita.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_004_taddhita.py) + ручной разбор [`adjudication.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/taddhita-overview/data/adjudication.json); toc_validate + article_validate (19 манифестов) + docusaurus build green. Ядро W2: **18/19** (остаётся 1: SG-WF-009 бахуврихи — блокирован C6). Публикация гейтится авторской визой.

## [0.56.0] - 2026-07-17

### Changed
- **Sangram SG-MO-028 «Каузатив» — коллизия двух сессий сведена в пользу более полной версии ([PR #366](https://github.com/gasyoun/SanskritGrammar/pull/366); Opus 4.8 `claude-opus-4-8[1m]`).** Две сессии произвели SG-MO-028 параллельно (обе H1139); первой смёржилась моя версия ([v0.55.0](https://github.com/gasyoun/SanskritGrammar/releases/tag/v0.55.0), «не отделим»), но параллельная сессия сделала строго лучше — с **количественной оценкой** доли каузативов. Принята она (тот же выбор, что P4 H989↔H990): то же ядро (класс-X -aya- 55 376 токенов, слияние с curādi под кодом 10, EM5), но с ответом «сколько именно каузативов» двумя сходящимися методами — **ручная адъюдикация** посеянной выборки 60 типов (49 каузативов / 11 curādi = 18,3 % ложных) и **механическое де-усиление** (44 117/55 376 = **79,7 %** массы бакета имеет аттестованный первичный корень) → **≈80 % каузативов**, ~18–20 % curādi неотделимы (частично восстановим, как аорист SG-MO-018). Добавлены `adjudication.json` + `adjudication_sample.tsv`; заслуга параллельной сессии. Ядро W2: 17/19 (без изменения счёта). Публикация гейтится авторской визой.

## [0.56.0] - 2026-07-17
### Changed
- **Consistency check extended to five more shared figures (H1164, Opus 4.8 `claude-opus-4-8[1m]`).** [`scripts/check_claims_consistency.py`](scripts/check_claims_consistency.py) gains a second mode: alongside the aorist supersession guard, four cross-register figures (perfect 61,986 · imperfect 47,554 · present · verbal-denominator 781,618) are now pinned to an **allowed-value set** — any citation outside it (a typo, a stale value, an un-reconciled recompute) fails. The present allows a **version-distinguished pair** (157,003 DCS-2021 · 353,215 DCS-2026), which the check permits explicitly. Reconciliation outcome: **no value-level drift found** — every figure already uses only its known value(s); the two present counts are legitimately different corpus snapshots, not an inconsistency. A second pytest gate ([`tests/test_claims_consistency.py`](tests/test_claims_consistency.py)) enforces it in CI. NOTE: full standardization on DCS-2026 (which would collapse the present pair and recompute the DCS-2021 rarity family) is a corpus-version policy decision left open.

## [0.55.0] - 2026-07-17

### Added
- **Sangram ядро W2 — статья SG-MO-028 «Каузатив» — статья-кандидат (H1139, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/causative/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/causative): несущий границу слот, map-heavy с реальным измеримым ядром. Каузатив корпусом **не размечен** (меток Caus — 0): основа -aya- лежит под вестергоровским кодом X класса (`lemma.grammar 10.%`), который СЛИВАЕТ производный каузатив (kāray/janay/darśay) с первичным curādi (kathay/pūjay/cintay). Измеримо целое — **класс-X -aya- = 55 376 финитных токенов (10,6 %), 1998 лемм** — но каузатив как таковой из curādi не отделим (EM5). Контраст: прочие вторичные спряжения корпус РАЗЛИЧАЕТ (деноминатив 5482, дезидератив 1060, интенсив 921), т.е. caus↔curādi — единственное неразрешённое слияние; чистое разделение требует WhitneyRoots + разбора по стеблю. 5 примеров (4 каузатива + kathay curādi). Scoping — воркфлоу-скаут. Скрипт [`sg_mo_028_causative.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_028_causative.py); 3 валидатора + CI build green. Ядро W2: 17/19. Публикация гейтится авторской визой.

## [0.55.0] - 2026-07-17
### Added
- **Cross-register claim-figure consistency check (H1140, Opus 4.8 `claude-opus-4-8[1m]`).** A
  guardrail against superseded corpus figures drifting back into the claim registers, after the
  aorist count (2,452 / 0.31% -> 12,054 / 2.30%) drifted repeatedly across registers that reuse
  each other's numbers. New [`scripts/check_claims_consistency.py`](scripts/check_claims_consistency.py)
  holds a canonical-figures registry and FAILs if any `*/claims.yml` cites a superseded value as a
  live number without a correction marker; wired into CI via
  [`tests/test_claims_consistency.py`](tests/test_claims_consistency.py) and available as
  `npm run check-claims`. On its first run it caught **5 stale aorist citations** the manual
  refresh had missed (Bühler HB-1/20/61, Zalizniak Ocherk OCH-31, Konspekt KZ-3), now all fixed.

## [0.54.0] - 2026-07-17

### Added
- **Sangram ядро W2 — обзорная статья SG-WF-002 «Первичная деривация (kṛt): обзор» — статья-кандидат (H1135, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/krt-overview/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/krt-overview): обзор первичной деривации. Количественная опора — нативно размеченная половина kṛt: отглагольные формы `VerbForm∈{Part,Conv,Gdv,Inf}` = **483 623 токена (8,5 % корпуса)**, чистое замкнутое множество (0 утечки на не-VERB): причастие 341 556 (70,6 %), абсолютив 102 054 (21,1 %), герундив 28 260 (5,8 %), инфинитив 11 753 (2,4 %). kṛt-ИМЕНА (kartṛ, dāna) корпусом НЕ размечены (EM5): поверхностный отбор шумен (~59 % ложных, P5) — не считаются. Scoping — параллельный воркфлоу-скаут эндшпиля ядра (4 слота). Скрипт [`sg_wf_002_krt_overview.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_002_krt_overview.py); 3 валидатора + CI build green. Ядро W2: 16/19. Публикация гейтится авторской визой.

## [0.53.0] - 2026-07-17

### Added
- **Sangram ядро W2 — статья SG-MO-027 «Пассив» — статья-кандидат (H1108, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/passive/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/passive): несущий границу слот. Пассив (слабый корень + -ya- + медиальные окончания; ucyate/dṛśyate) нативно размечен (Voice=Pass) → измерим напрямую: **29 699 финитных токенов (5,7 %)** + 7 002 причастных. Профиль резче любого разреза глагола — голос безличной цитаты: **98,1 %** 3-е лицо, **92,6 %** презенс; во главе verba dicendi/восприятия (ucyate «говорится» — самый частотный пассив корпуса, dṛśyate, śrūyate, kathyate). Граница EM1: пассивная основа -ya- формально омонимична презенсу IV класса (divādi: paśyati vs dṛśyate), разделены тегом залога, не формой (P2). 5 примеров. Скрипт [`sg_mo_027_passive.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_027_passive.py); 3 валидатора + CI build green. Ядро W2: 15/19. Публикация гейтится авторской визой.

## [0.52.0] - 2026-07-17

### Added
- **Талмуд-сверка аористов — второй проход, консолидация (H1054).** Сверка доведена до полных **53 записей** четырех реестров (31 подтверждено · 4 противоречия книгам, все подтверждают стоящие вердикты HK-5/HK-38/HB-60/HB-372 · 18 «молчит»); файл сверки, на который ссылался v0.50.0, реально создан по обещанному адресу — [AORIST_REGISTRY_TALMUD_CROSSCHECK_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/AORIST_REGISTRY_TALMUD_CROSSCHECK_2026.md); новый инструмент — перепись аористных классов Приложения 1: [`aorist_class_census.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/aorist_class_census.py) → [`aorist_class_census.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/aorist_class_census.json) (745 корней: iṣ 511 · удв. 342 · s 196 · корневой 142 · тематический 116 — 5-й из 7, вторая независимая ось против HK-5 · siṣ 33 · sa 26; кросс-таблица seṭ×класс: класс 4 aniṭ-доминантен 102/21, класс 5 seṭ-доминантен 337/37, у 6–7 seṭ-корней ноль). Fable 5 (`claude-fable-5`).

### Fixed
- **Талмуд-заметки v0.50.0 переселены из сгенерированных `CLAIMS_VERIFIED.md` в `claims.yml` (18 записей) + регенерация** — первый проход правил генерируемые файлы напрямую, и следующая регенерация стерла бы все 12 его ссылок; теперь они regen-устойчивы. Fable 5 (`claude-fable-5`).

## [0.51.0] - 2026-07-17

### Added
- **Sangram ядро W2 — статья SG-MO-018 «Аорист» — статья-кандидат (H1098, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/aorist/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/aorist): несущий границу слот; заполняет **середину градиента восстановимости претеритов** имперфект→аорист→перфект. Аорист склеен с перфектом под Tense=Past (EM2, P3), но — в отличие от перфекта — feat_formation размечает типы аористной основы (корневой/s/iṣ/sa/siṣ/редупл./тематический) на **12 054 токенах (11,8 % Past)** по всем семи типам. Это **нижняя оценка**: P3 оценил перфект ≈76 % Past → аорист ≈24 %, размечена примерно половина; вторая половина неотделима от перфекта в неразмеченном массиве. Честная оговорка о смежности them/red (adadat — «ложный друг» P3). 4 примера по типам основы. Скрипт [`sg_mo_018_aorist.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_018_aorist.py); 3 валидатора + CI build green. Ядро W2: 14/19. Публикация гейтится авторской визой.

## [0.50.0] - 2026-07-17
### Added
- **Талмуд-сверка аористов пяти реестров (H1054, директива адъюдикации к HK-5).** [AORIST_REGISTRY_TALMUD_CROSSCHECK_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/AORIST_REGISTRY_TALMUD_CROSSCHECK_2026.md): 24 утверждения × система Талмуда 2.1.6 (Табл. 16, 7 классов) — ни одного противоречия вердиктам, Талмуд = третий свидетель FALSE по HB-60; системная находка: «только Parasmaipada» классов 1/6 — правда индикатива (класс 1 — универсальная база пассивного аориста и P-прекатива, класс 6 — редчайшая опция Ā-прекатива); OCH-92 системно закрыт (пассив аориста = только Ā.3.SG), частотные UNTESTABLE Талмуд не снимает по построению. 12 строк реестров получили Талмуд-ссылки. Fable 5 (`claude-fable-5`).

## [0.49.0] - 2026-07-17

### Added
- **Sangram ядро W2 — статья SG-MO-016 «Имперфект» — статья-кандидат (H1096, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/imperfect/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/imperfect): первый несущий границу слот ядра и **позитивный двойник пилота P3**. Где P3 показал склейку перфекта/аориста под Tense=Past (EM2, recall перфекта 3,3 %), имперфект — **единственный претерит, размеченный DCS отдельно** (Tense=Impf), потому измерим: **46 695 токенов** из 523 721 финитного. Нарративное прошедшее, скошенное к 3-му лицу сильнее целого: 3-е **94,1 %** [93,9–94,4], ед. 75,1 %, актив 96,9 %; частотнейшие корни — verba dicendi/бытия (brū abravīt #1, bhū, as āsīt, paś, kṛ). Несёт два предела: EM2 (сёстры-претериты склеены) + EM1 (презентный класс не в признаках, P2). 5 примеров с аугментом. Скрипт [`sg_mo_016_imperfect.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_016_imperfect.py); 3 валидатора + CI build green. Ядро W2: 13/19. Публикация гейтится авторской визой.

## [0.48.0] - 2026-07-17
### Added
- **Секвенционная проверка имперфекта — заметка адъюдикации к HK-15 (H1053).** Предрегистрированный инструмент [imperfect_switching_stats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/imperfect_switching_stats.py) (T2607-26 заморожена до замера) + отчет [IMPERFECT_SWITCHING_HK15_REPORT.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/IMPERFECT_SWITCHING_HK15_REPORT.md): кластеризация имперфекта повсеместна (runs-test p<0,001, все срезы; аорист кластеризуется сильнее всех — lift до 3,61), «переключение темы» в точке вкрапления значимо, но микроскопично в эпосе (+0,2 п.п., p=0,002) и содержательно лишь в ведийском (+1,5 п.п., p<0,001); классика — направление перевернуто. ЧАСТИЧНО ПОДТВЕРЖДЕНО; компаньон-формулировка к § 2 A65 в отчете. Fable 5 (`claude-fable-5`), по разрешению MG на Opus-ряд.

## [0.47.0] - 2026-07-17

### Added
- **Sangram ядро W2 — статья SG-MO-026 «Абсолютив (-tvā/-ya)» — статья-кандидат (H1091, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/absolutive/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/absolutive): четвёртый (последний) частотный флективный слот — **группа закрыта**. Абсолютив несклоняем, поэтому рамка — алломорфия -tvā/-ya. **Корпус подтверждает традиционное правило на ≈98 %:** по сопоставлению суффикса с `lemma.preverbs` над 102 054 токенами Conv, -tvā на 98,5 % при простом корне (34 293/34 816 без преверба), -ya/-tya на 97,8 % при глаголе с превербом (56 501/57 790). Распределение: -ya/-tya 56,6 %, -tvā 34,1 %, прочее 8,8 %, редкий -am 0,5 %. «Аттестовано подтверждает традиционно». Несклоняем → порождённой парадигмы нет. 5 примеров (kṛtvā/gatvā простые; praṇamya/āgatya/vihāya составные). Скрипт [`sg_mo_026_absolutive.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_026_absolutive.py); 3 валидатора + CI build green. Ядро W2: 12/19. Публикация гейтится авторской визой.

## [0.46.0] - 2026-07-17

### Added
- **Sangram ядро W2 — статья SG-MO-023 «Причастия на -ta/-na» (прош. страд.) — статья-кандидат (H1083, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/ta-na-participles/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/ta-na-participles): третий частотный флективный слот ядра (кластер именных форм глагола). Причастие -ta/-na (kṛta/gata/bhinna) — **самый частотный причастный тип**: **219 902 токена** (нижняя оценка) = 64,4 % всех 341 556 причастий, из 4742 корней, -ta к -na как 13,6:1; употребление преимущественно предикативное (57 % в Nom. — перифрастический пассив/перфект). Предел EM5 честно: DCS не тегирует класс -ta/-na (атрибут tense — для причастия настоящего), опознание по основе (снятие a-/ā-флексии, основа на -t/-n) — нижняя оценка, исключает ассимилированные labdha/rūḍha/baddha. Выборка 50 токенов: 0 ложных. Склоняется как a-основа (SG-MO-002). Скрипт [`sg_mo_023_ta_na_participles.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_023_ta_na_participles.py); 3 валидатора + CI build green (локальный build OOM под давлением памяти concurrent-сессий). Ядро W2: 11/19. Публикация гейтится авторской визой.

## [0.45.0] - 2026-07-16

### Added
- **Sangram ядро W2 — статья SG-MO-010 «Склонение: местоимения» — статья-кандидат; ИСКЛЮЧЕНИЕ из предела EM3 (H1064, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/pronouns/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/pronouns): второй частотный флективный слот ядра. Ключевой контраст: где открытый именной инвентарь (актив G2) даёт медиану **1** клетку на лемму, закрытый высокочастотный класс местоимений (**38 лемм / 544 999 токенов**) аттестует медиану **12,5** из 24 (среднее 12,13, макс 22, 39,5 % лемм ≥18 клеток) — 38 лемм несут ≈14 300 токенов каждая. Не потребитель G2 (G2 только по NOUN; местоимения — PRON, отдельный запрос). Супплетивный закрытый класс → порождение ≡ традиция: канонические парадигмы aham/tad из Уитни гл. VII, не машинно-порождённые. 5 аттестованных примеров с супплетивизмом (aham←mad, tasya←tad) + выборка 50 токенов. Скрипт [`sg_mo_010_pronouns.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_010_pronouns.py); 3 валидатора + build green. Ядро W2: 10/19. Публикация гейтится авторской визой.

## [0.44.0] - 2026-07-16

### Added
- **Sangram ядро W2 — статья SG-MO-006 «Склонение: согласные основы» — статья-кандидат; первый потребитель актива G2 (H1058, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/consonant-stems/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/consonant-stems): первый частотный флективный слот ядра после обзоров (порядок § 5 контрольной точки). Трёхслойная: АТТЕСТАЦИЯ **потребляет** актив G2 (H1048, не пересчитывает) — 4 212 согласных лемм / 232 935 токенов, медиана 1 клетка/лемма (EM3), покрытие растёт с частотой (rājan 20/24, karman 22/24); по подтипам -in 900 · -an 846 · -as 572 · -us/-is по 86 · корневые 1 722. ПОРОЖДЕНО (MWinflect) — парадигмы rājan/manas со ступенями основы (сильная rājā / слабая rājñā / средняя rājasu); ТРАДИЦИОННО — Уитни гл. V §§383–465. 5 аттестованных примеров по подтипам + посеянная выборка 50 токенов. Скрипт [`sg_mo_006_consonant_stems.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_006_consonant_stems.py); 3 валидатора + build green. Ядро W2: 9/19. Публикация гейтится авторской визой.

## [0.43.0] - 2026-07-16
### Changed
- **A65: авторская адъюдикация 9 расхождений валидации применена — 9/9 за реестр (H1049,
  Fable 5 `claude-fable-5`).** Ни один вердикт не правится: человеческий ярус подтвердил
  первый проход против более строгого слепого второго; цепочка валидации закрыта (числа →
  проход 1 → слепой проход 2 κ = 0,877 → человек 9/9). Машинная запись голосования —
  [`verdict_validation/validation_adjudication.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/validation_adjudication.json);
  валидационный отчет + § 5/§ 6/§ 11/аннотация статьи переведены в «выполнено». Заметки
  адъюдикации развернуты: сноски [^hb2] (дидактика «модель — потом исключения») и [^hb10]
  (управление ā, Уитни § 1128 + ожидаемые данные Шерцля) в § 2.2; пять исследовательских
  директив → handoffs **H1050–H1054** (аудит раздела самас Кочергиной по Лейтану ·
  залоговая гипотеза Зализняка-1978 на DCS · прошедшие времена в параллельном корпусе ·
  имперфект как маркер переключения нарратива · сверка аористов с Талмудом); Шерцль-сверка —
  GTD @WAITING; два открытых вопроса — в журнал вопросов. **До подачи A65 — только вычитка.**
  ([H1049](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1049-Fable_SanskritGrammar_a65-adjudication-apply-9-approve_16.07.26.md))

## [0.42.0] - 2026-07-16

### Changed
- **A65: авторская адъюдикация девяти расхождений κ-валидации применена — 9/9 за реестр (H1049, Fable 5 `claude-fable-5`).** Все девять спорных вердиктов (HB-2, HB-10, HB-57, HB-100, HK-4a, HK-4b, HK-5, HK-15, HK-34) оставлены как в первом проходе; машинная запись решений закоммичена ([validation_adjudication.json](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/validation_adjudication.json)), [валидационный отчет](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/VERDICT_VALIDATION_KAPPA_A65_2026.md) получил раздел «Адъюдикация автора — 9/9 за реестр». В статью внесены две заказанные адъюдикацией сноски (HB-10: Уитни § 1128 об управлении ā; HB-2: дидактический прием «модель — потом исключения»); § 6/§ 5/§ 11/аннотация переведены из «адъюдикация ожидается» в «выполнена». Заметки автора развернуты в программу продолжения: handoffs H1050–H1054 (самасы Кочергиной по Лейтану · залоги Зализняка-1978 на DCS · прошедшие времена в параллельном корпусе · имперфект как маркер переключения · аористы против Талмуда), @WAITING по данным Шерцля, два вопроса в QUESTIONS_LOG (HK-4a, HB-2).

## [0.41.0] - 2026-07-16

### Added
- **Sangram G2 производный дата-актив — «аттестованные клетки склонения на лемму» (H1048, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/data/declension_cell_coverage/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/data/declension_cell_coverage): для каждой из **57 144** именных лемм — какие из 24 клеток (8 падежей × 3 числа) аттестованы в пинованном снапшоте DCS (1 790 270 токенов, знаменатель совпадает с SG-MO-001). Общая (все типы основ, все роды) версия покрытия пилота P1; кросс-статейный слой для SG-MO-001/002/006/010, рекомендованный контрольной точкой ядра W2 (§ 5 G2). **EM3 в масштабе корпуса:** медиана **1** клетка/лемма, 58,9 % лемм с одной клеткой, 0,0 % с полными 24, лишь **10,44 %** пространства лемма×клетка аттестовано; покрытие — артефакт частоты (среднее 1,0 у hapax → 17,3 при 1000+); Nom.Sg (41 998 лемм) против Dat.Du (128) — разброс ×328. `lemma_cell_coverage.csv` (битовая строка `cells_bits24`) + `coverage_summary.json` (разбивки по роду/основе/частоте) + README. Скрипт [`sg_g2_declension_cell_coverage.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_g2_declension_cell_coverage.py); read-only, C3-пин; build green.

## [0.40.0] - 2026-07-16
### Changed
- **A65 подписана автором — 5/5.** [SIGNOFF_A65_author_pass.md](https://github.com/gasyoun/SanskritGrammar/blob/main/SIGNOFF_A65_author_pass.md): голосовые решения VC1–VC8 приняты без вето; статус в [Uprava/ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md) переведен 4/5 → **5/5**. Остаточные флаги (адъюдикация девяти расхождений κ-валидации, Zenodo/OSF, ГОСТ/Зализняк-1975, кольцо § 10, верстка § 2.2) живут как самостоятельные GTD-позиции. (H1015, Fable 5 `claude-fable-5`.)

## [0.39.0] - 2026-07-16
### Changed
- **A65: author-voice pass (/paper-author-pass) — proposed 5/5, awaiting the author's sign-off (H1015)** — [the manuscript](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md) now reads as the author's own: academic frontmatter (М. Ю. Гасунс, независимый исследователь, ORCID, ya.ru — per AUTHOR.md), working banner removed, title recast («корпусная верификация…», the H797 tag dropped), §8 de-coded (companion papers named descriptively, no Axx), the LLM-adjudication sentence in journal register with model attribution preserved, appendix provenance glyphs/H-IDs neutralized. **No number, claim, or citation touched.** 8 voice calls + 5 residual flags recorded in [SIGNOFF_A65_author_pass.md](https://github.com/gasyoun/SanskritGrammar/blob/main/SIGNOFF_A65_author_pass.md) — a ~30-minute read-and-sign; the 5/5 bump itself waits for the signature. (Fable 5 `claude-fable-5`, [H1015](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1015-Fable_SanskritGrammar_h797-programme-synthesis-report-ru_16.07.26.md))

## [0.38.0] - 2026-07-16

### Changed
- **Sangram: ретро-проход прозы по [style guide](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/SANGRAM_STYLE_GUIDE_PROSE_RU.mdx) — 4 оставшиеся опубликованные статьи (H1014, Fable 5 `claude-fable-5`).** Явный follow-up частичного исхода [H1003](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1003-Fable_SanskritGrammar_sangram-style-guide-rusgram-etalon_16.07.26.md) (perfect прошёл первым): проза [a-stems (P1)](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/a-stems/index.mdx), [thematic-present (P2)](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/thematic-present/index.mdx), [tatpurusha (P4)](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/index.mdx) и [krt-suffixes (P5)](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/krt-suffixes/index.mdx) выровнена по диагностике «птичьего языка» (гайд § 4): коммит-пины, зёрна выборок, дословные запросы и имена моделей-разметчиков уведены из аналитического текста в §§ данных/провенанса (в прозе — «разбирающий», «проход A/B»), падежные аббревиатуры и морфопризнаки получили русские чтения, вложенные скобки развёрнуты, техника восстановления пина у P1 свёрнута в примечание; попутно исправлены опечатки «Стярка» → «Сверка» (P2 § 3.2) и «деривациий» → «дериваций» (P5 § 5), шапка таблицы P1 § 3.3 уточнена («сколько лемм», не «доля»). **Все числа и выводы неприкосновенны** — ревизии `revision` внесены в манифесты всех четырёх статей (контракт C4); backlog гайда § 6 строки 3–6 → ✅. ([H1014](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1014-Fable_SanskritGrammar_sangram-prose-retro-pass-p1-p2-p4-p5_16.07.26.md))

## [0.37.0] - 2026-07-16

### Added
- **Sangram ядро W2 — обзорная статья SG-WF-001 «Строение слова: корень, основа, аффикс» — статья-кандидат; ЧЕТВЁРТЫЙ и последний обзор ядра W2 (H1032, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/word-structure-overview/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/word-structure-overview): структурная рамка слова по пинованному снапшоту, привязанная к трём нативно-измеримым слоям (не текстбучная схема): **A** — приоритетное разбиение всех **5 688 416** токенов (нарицательное 39,9 % — первичн./kṛt/taddhita НЕ разделены · закрытый класс 28,4 % · член композита 14,8 % · финитный глагол 9,2 % · отглагольное kṛt 7,6 %; прозрачно «корень+аффикс» 16,8 %); **B** — инвентарь корней: 8 053 аттестованные финитные леммы (топ-10 = 29,7 %, закон Ципфа) vs гана-инвентарь WhitneyRoots 1 133 корня (I класс 46,5 %); **C** — окно словообразования основы `feat_formation`, разрежено (1,7 %). Разбор нарицательных на первичные/kṛt/taddhita по поверхности НЕ делается (перенесённый предел P5/SG-WF-003: ~59 % ложных). Скрипт [`sg_wf_001_word_structure.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_001_word_structure.py); 3 валидатора + build green. **Завершает четвёрку обзоров ядра W2** (SG-MO-001 · SG-MO-012 · SG-WF-006 · SG-WF-001). Публикация гейтится авторской визой.

## [0.36.0] - 2026-07-16
### Added
- **A65: валидация вердиктов выполнена — слепой двухпроходный κ-дизайн по шаблону A64
  (H1041, Fable 5 `claude-fable-5`; аннотатор B — Sonnet 5 `claude-sonnet-5`).** Новая папка
  [`verdict_validation/`](https://github.com/gasyoun/SanskritGrammar/tree/main/verdict_validation):
  стратифицированная выборка n = 115 (ВСЕ 30 фактических флагов + ВСЕ 25 UNTESTABLE + 60
  случайных TRUE, зерно 20260716), слепой пакет без вердиктов/заметок первого прохода,
  **κ Коэна = 0,877** (95 %-ДИ бутстрэпа [0,796; 0,946], 2 000 ресэмплов), сырое согласие
  106/115 = 92,2 %; Очерк 19/19 и Конспект 5/5 — полное согласие. Конфузия чистая на
  TRUE и FALSE; все 9 расхождений — граница OVERSTATED/UNTESTABLE, в 7 случаях из 9 второй
  аннотатор СТРОЖЕ (флаги реестров консервативны). Попутно классифицированы 7 OVERSTATED
  Бюлера — **первое заполнение класса «система-против-узуса»** (HB-10, предлог ā + Acc.):
  ровно у самой систематической книги, как § 2.2 и предсказывал; итог типологии — 22
  классифицированных (14·4·1·3). Отчет
  [`VERDICT_VALIDATION_KAPPA_A65_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/verdict_validation/VERDICT_VALIDATION_KAPPA_A65_2026.md)
  + воспроизводимые скрипты/данные; § 6/§ 2.2/§ 5/§ 11/аннотация статьи обновлены.
  **Остаток до 5/5:** авторская адъюдикация 9 расхождений — review-sheet
  `sanskritgrammar-a65-verdict-validation-disagreements_16.07.26_review.html` (локальный
  `review/`) + вычитка.
  ([H1041](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1041-Fable_SanskritGrammar_a65-verdict-validation-kappa_16.07.26.md))

## [0.35.0] - 2026-07-16
### Changed
- **A65 (4/5): hostile referee pass applied to the canonical merged article (H1015; merit-merge after the H1033 collision)** — a fresh-context referee produced **10 Major + 16 Minor** findings ([disposition + collision note](https://github.com/gasyoun/SanskritGrammar/blob/main/REVIEW_A65_SYNTHESIS_REFEREE_2026.md)). The concurrent H1033 4/5 (PR #277, v0.34.0) was taken as base — it had performed the five-book typology classification (9/4/2/0 of 15) and fixed HK-10/HK-38 in the register — and the referee corrections absent from it were re-applied on top: first-substantive-FALSE attribution restored to HK-16; per-book two-axis counts; «пометка, не предрегистрация» instead of «ПРЕДСКАЗАЛ»; ACL-scoped novelty claim; per-genre word-order breakdowns inlined into the OCH-66 verdict; Fisher exact p = 0.42; systematic de-jargonization; bibliography upgrades (Кнауэр place, Бюлер translator, Зализняк-1975 title flagged for verification). PR #278 closed as superseded. Deferred to author-pass: banner, Zenodo deposit, GOST, RU-scholarship ring. (Fable 5 `claude-fable-5`, [H1015](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1015-Fable_SanskritGrammar_h797-programme-synthesis-report-ru_16.07.26.md))

## [0.34.0] - 2026-07-16

### Changed
- **A65 продвинута 3/5 → 4/5: слияние A60 ВЫПОЛНЕНО (H1033, Fable 5 `claude-fable-5`).**
  [Отчет-статья](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md)
  принял весь аналитический состав A60, перебазированный с 43-клеточного пилота на осушенный
  реестр 234 (доля расхождений Кочергиной 27,9 % → **5,1 %** — учебник точнее, чем показывал
  пилот): § 1 — метод (единица анализа, две оси, правило D-B, четырехчастная типология
  расхождений), § 2.2 — центральная таблица 12 расхождений с **точным** соответствием
  класс⇄подача (8 сверхобобщений = MISLEADING, 4 частотных = FREQUENCY-HIDDEN) и находкой
  пустого класса «система-против-узуса»; типология растянута на пять книг (15
  классифицированных: 9 · 4 · 2 · 0; восемь FALSE Бюлера — опечаточный класс вне типологии,
  его 7 OVERSTATED честно оставлены до валидации), § 2.3 — флагман -iṣya, § 2.4 —
  петербургская традиция как источник профиля, § 10 — положение в литературе
  (Hellwig/Nation/Biber/Arase/Hoenen + четыре пункта новизны), § 11 — заключение, § 12 —
  +6 внешних позиций литературы. Черновик A60 помечен архивным источником (не продвигать,
  не цитировать, не подавать отдельно). Адверсариальный верификационный проход перед
  коммитом исправил 10 дефектов, включая **неверный § Уитни у HK-10** — § 168 (сандхи)
  вместо §§ 592/595 (акцент глагола): ошибка сидела в самом реестре и исправлена в
  `claims.yml` (+ регенерация CLAIMS_VERIFIED/claims.json), в методичке v1 (разделы I–II)
  и в README книги. До 5/5 — человеческая валидация выборки вердиктов (κ-шаблон A64)
  + авторская вычитка.
  ([H1033](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1033-Fable_SanskritGrammar_a65-4of5-full-paper-a60-merge_16.07.26.md))

### Added
- **Sangram ядро W2 — обзорная статья SG-WF-006 «Композиты: обзор и классификация» — статья-кандидат (H1031, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/compounds-overview/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/compounds-overview): третья обзорная статья ядра W2. Рамка композитов по пинованному снапшоту: **841 052** члена `Case=Cpd` → **595 021** реконструированный композит в 396 305 предложениях (**52,5 %** корпуса несут композит); гистограмма числа членов — двучлен 74,4 %, трёхчлен 17,6 %, 4-член 4,8 %, 5+ 3,3 %. Тип корпусом НЕ размечен (предел EM4): нативный сигнал только `compound:coord` (≈двандва) в разобранном подмножестве; количественный ориентир по типу — двухпроходная κ пилота P4 по выборке 120 (татпуруша 79,5 % / бахуврихи 14,5 % / двандва 5,1 %, честно как выборка). Скрипт [`sg_wf_006_compound_overview.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_006_compound_overview.py); 3 валидатора + build green. Публикация гейтится авторской визой.

### Added
- **Sangram ядро W2 — обзорная статья SG-MO-012 «Спряжение: обзор» — статья-кандидат (H1028, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/conjugation-overview/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/conjugation-overview): вторая обзорная статья ядра W2. Частотная рамка финитного глагола по **523 721** токену — распределение по пяти **нативным** морфопризнакам DCS (лицо/число/время/наклонение/залог), реальная аттестованная рамка без приближения: 3-е лицо 80,3 %, презенс 67,4 %, индикатив 69,6 %, оптатив 17,5 %, двойственное 1,8 %, пассив 5,7 %. Несёт пределы EM1 (класс не в признаках) + EM2 (Tense=Past склейка). Скрипт [`sg_mo_012_conjugation_overview.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_012_conjugation_overview.py); 3 валидатора + build green. Публикация гейтится авторской визой.

## [0.33.0] - 2026-07-16
### Changed
- **A65 (3/5) synchronized with the H1022 treebank wave — the programme headline honestly recast (H1015)** — the same-day treebank instrument measured the §§212-217 syntax cluster and ended Zalizniak's zero-flag run at 70/74: register now **65 TRUE · 2 OVERSTATED · 1 FALSE · 6 UNTESTABLE**. [The draft](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md) replaces the flag-rate ranking (now statistically fragile: Бюлер 3.7% · Зализняк 4.1% · Кочергина 5.1%) with the two-tier picture — what separates the books is WHERE flags cluster (misprints vs quantifier absolutes vs one syntax §-cluster) — and records the register's pre-registered «hunting licence» on OCH-68 as a fulfilled prediction (75.2%, n=335); OCH-67 documented as the programme's first substantive FALSE (subordinate:coordinate 6.5:1, genre split checked); §7 inventory +row 13; the instrument's own lesson (the «no syntactic annotation» premise was never checked) added to §4. (Fable 5 `claude-fable-5`, [H1015](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1015-Fable_SanskritGrammar_h797-programme-synthesis-report-ru_16.07.26.md))

## [0.32.1] - 2026-07-16
### Changed
- **A65: both human gates RULED by MG 16-07-2026 (H1024)** — ① venue/language =
  **российская индология, RU as-is** (the eLex/GWC/ISCLS translation branch dropped);
  ② **A60 merged into A65** — one paper: A65 § 2 absorbs A60's central divergence table
  (4-way typology), the five-book count becomes its frame. Applied to the
  [report](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md)
  (banner, § 5, § 8, § 10 self-citation slot), its metadoc (backlog rebuilt — the 4/5
  merge pass is the new head item), and the
  [A60 draft](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/DRAFT_grammar-claims-corpus-denies_A60.md)
  header (🔀 MERGED INTO A65 — source material, do not advance separately; the A60 leg
  of H967 is superseded). Uprava side (ARTICLES A65/A60 rows, GTD Publication Gates,
  H967 banner) updated the same pass. (Fable 5 `claude-fable-5`,
  [H1024](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1024-Fable_SanskritGrammar_a65-venue-ru-a60-merge-rulings-apply_16.07.26.md))

## [0.32.0] - 2026-07-16

### Changed
- **P3 (SG-MO-017 перфект) — проза ВСЕЙ статьи переписана по [style guide прозы](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/SANGRAM_STYLE_GUIDE_PROSE_RU.mdx) (расширенный охват H1003 — «вся статья, не только § 6», решение MG 16-07-2026).**
  [`sangram/articles/perfect/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/perfect/index.mdx),
  §§ 1, 3.1–3.3, 3.5, 4: вложенные скобки-приписки развёрнуты в предложения, запросы и коммит-пин уведены
  из аналитического текста (живут в § 2 «Данные и воспроизводимость»), телеграфные пункты kill-gate § 4
  развёрнуты в связные абзацы с сырыми счётами при процентах (61 из 80, 8 из 80), административный регистр
  («виза») заменён словами читателя; **все числа и выводы сохранены** (гайд правит слог, не находки — те под
  авторской визой); попутно исправлена опечатка «Уитри» → «Уитни» (§ 3.4). Append-only ревизия `revision` в
  [манифесте](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/perfect/article.manifest.json) (C4);
  строка 1 очереди гайда (§ 6) обновлена. Проход подготовлен предыдущей сессией Fable 5 (`claude-fable-5`)
  и удержан до решения MG о расширенном охвате; отревьюирован и дошлифован этой сессией — Fable 5
  (`claude-fable-5`). ([H1003](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1003-Fable_SanskritGrammar_sangram-style-guide-rusgram-etalon_16.07.26.md))
- **Sangram SG-MO-001 «Склонение: обзор» — ОПУБЛИКОВАНА (виза MG 8/8 approve; H1013).**
  [`sangram/articles/declension-overview/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/declension-overview)
  ([PR #262](https://github.com/gasyoun/SanskritGrammar/pull/262)): виза применена → ревизия `published`,
  плашка кандидата снята; по карточке A4 § 3.2 переведён на реальную парадигматическую классификацию
  (окончание Ins.Sg, покрытие 75,1 %) — реальная доля основ на -a **52,6 %** против завышенных
  морфологических 62,9 %. Запись статьи-кандидата — в секции `[0.30.0]`, в чей тег она реально вошла
  (см. Fixed ниже). (Opus 4.8 `claude-opus-4-8[1m]`)

### Fixed
- **CHANGELOG: дубликат заголовка `[0.29.0]` устранён** — запись SG-MO-001 «Склонение: обзор» (merged
  [PR #255](https://github.com/gasyoun/SanskritGrammar/pull/255) ПОСЛЕ тега v0.29.0) при переносе H1015-записи
  в 0.30.0 ([PR #257](https://github.com/gasyoun/SanskritGrammar/pull/257)) оказалась под вторым, ложным
  заголовком `[0.29.0]`; запись-кандидат перенесена в секцию `[0.30.0]`, в чей тег она реально входит,
  а её издательский статус (виза 8/8, [PR #262](https://github.com/gasyoun/SanskritGrammar/pull/262)) —
  Changed-строкой этого релиза. (Fable 5 `claude-fable-5`)

## [0.31.0] - 2026-07-16
### Changed
- **A65 advanced 2/5 → 3/5 per the house playbook (H1015)** — [`REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md) is now a citable draft: abstract with first-class caveats (LLM-adjudicated verdicts vs deterministic corpus numbers, no second human annotator — stated up front), §6 reproducibility contract, §7 claim→artifact inventory (12 rows, 1 flagged gap), §8 anti-salami boundaries vs A60/A62/A63/A64, §10 references with ⬜ self-citation slots, @DECIDE banner (venue/language; A60 развязка). **Mandatory fact-check fan-out caught 2 real defects**: the headline «942 claims + 214 parses» double-counted (correct: 728 verdicted claims + 214 parses = 942 items; the source `.ai_state` line fixed in the same PR), and §59 cited the superseded H1008 figure 98.3% where the canonical H1012 parser reads 97.6%/98.4% (the two independent parsers agreeing within 1pp is now recorded as a robustness datum). (Fable 5 `claude-fable-5`, [H1015](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1015-Fable_SanskritGrammar_h797-programme-synthesis-report-ru_16.07.26.md))

## [0.30.0] - 2026-07-16
### Added
- **Programme synthesis report (RU) — the H797 claim-verification programme in one document (A64 draft, H1015)** — [`REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_GRAMMAR_CLAIM_VERIFICATION_SYNTHESIS_2026.md) (+ sibling metadoc): 942 verified claims + 214 audited parses across five books, three equal lines — presentation-calibration ranking (Зализняк 0/74 > Бюлер 15/403 > Кочергина 12+24/234, with the verb-accent control pair), the measured diachrony (§207 five monotonic axes, §167 causative collapse 81→21%, the twice-replicated purāṇa epic-imitative signature, §§59/68/193 structural confirmations), and the honesty methodology (UNTESTABLE-as-instrument-spec, negative pilots with numbers, measured blockers, FINDINGS §86-88). Registered as **A65** in [Uprava/ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md) (A64 was claimed concurrently by the Sangram P4 method paper). All numbers sourced from the generated registers and instrument JSONs — none hand-entered. (Fable 5 `claude-fable-5`, [H1015](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1015-Fable_SanskritGrammar_h797-programme-synthesis-report-ru_16.07.26.md))
- **Sangram ядро W2 — обзорная статья SG-MO-001 «Склонение: обзор» — статья-кандидат (H1013, Opus 4.8 `claude-opus-4-8[1m]`).** [`sangram/articles/declension-overview/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/declension-overview): первая обзорная статья ядра W2 — устанавливает тип «обзор» (скелет пилота минус §4 kill-gate плюс § «Карта подстатей»). Частотная рамка домена склонения по **1 790 270** словоизменённым именным токенам DCS: ед. 79,3 % / дв. **2,09 %** [2,07–2,12] / мн. 18,6 %; Nom 38,7 % + Acc 24,0 % доминируют, Dat реже всех 2,2 %; основы на **-a — 62,9 %** [62,86–63,0] (почему SG-MO-002 — флагман). Скрипт [`sg_mo_001_declension_overview.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_001_declension_overview.py); 3 валидатора + build green. Публикация гейтится авторской визой (виза 8/8 применена позднее — см. `[0.32.0]`).

## [0.29.0] - 2026-07-16

### Added
- **Sangram: style guide прозы по эталону rusgram.ru (H1003, виза P3 карточки B1+A7).**
  [`sangram/editorial/SANGRAM_STYLE_GUIDE_PROSE_RU.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/SANGRAM_STYLE_GUIDE_PROSE_RU.mdx)
  (+ metadoc): разбор двух статей эталона («Будущее время» Стойновой 2018, «Творительный падеж») с таблицей
  «у них — у нас», 6 правил слога (термин один раз и по-русски; процент + сырой счёт + словесное чтение;
  технический провенанс — в `<details>`/«Данные и воспроизводимость»; абзац тезис→пример→комментарий;
  безличный тон с лексическими хеджами; полное имя в прозе, аббревиатура в подписи), запрет «птичьего языка»
  с 6 диагностическими признаками, чек-лист самопроверки перед PR, очередь потребителей (следующая —
  методичка Кочергиной, по заказу MG 16-07-2026). Гайд держит СЛОГ, контракт C4 — структуру; при конфликте
  структура за C4. **Демо на P3:** § 6 «Ограничения» статьи [perfect](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/perfect/index.mdx)
  переписан по гайду — те же шесть оговорок и те же числа человекочитаемым слогом, техника пина свёрнута
  в примечание (append-only `revision` в манифесте, C4). Сам гайд — под авторской визой: review-sheet
  `sangram-prose-style-guide-visa_16.07.26` (локальный), @WAITING строка в GTD. (Fable 5 `claude-fable-5`,
  [H1003](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1003-Fable_SanskritGrammar_sangram-style-guide-rusgram-etalon_16.07.26.md))
- **Sangram: контрольная точка фундамента W1→W2 — ядро W2 (19 статей ①) ОТКРЫТО (H1007).**
  [`sangram/SANGRAM_W2_CORE_OPENING_CHECKPOINT_2026.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_W2_CORE_OPENING_CHECKPOINT_2026.mdx):
  ворота входа пройдены (C2–C6 приняты + все 5 пилотов опубликованы ≥3), синтез пяти пилотов (2 положительных /
  3 честных отрицательных, пределы EM1–EM5 подтверждены), решения по слоям аннотации § 9 (G1–G6 — ядро открывается
  на дешёвых заплатках; G2/G3 агент-исполнимы; смета слоя класса G1 — на checkpoint 2028), и открытие ядра из
  19 ① (4/19 произведено, 15 к производству + порядок). Отличается от годового checkpoint W2 (июль 2028). Релиз —
  с ближайшей статьёй ядра. (Opus 4.8 `claude-opus-4-8[1m]`)

### Changed
- **RQ4 evaluation protocol § 6 — all four `@DECIDE` gates closed.** § 6.1–6.3 (Systema-hosted,
  Systema's own Kochergina-stage students, 4-week retention) were already ruled 15-07-2026
  ([H984](https://github.com/gasyoun/Uprava/blob/main/handoffs/H984-Sonnet_SanskritGrammar_rq4-item-bank-build_15.07.26.md));
  a re-ask against "open call" reconfirmed the existing student-population ruling (the harness,
  [H987](https://github.com/gasyoun/Uprava/blob/main/handoffs/H987-Sonnet_Systema-Sanscriticum_rq4-study-harness_15.07.26.md)/[Systema PR #536](https://github.com/gasyoun/Systema-Sanscriticum/pull/536),
  already assumes real, retention-contactable Systema accounts). **§ 6.4 (consent wording)
  APPROVED 16-07-2026 (MG), no revisions** — the plain-language Russian consent text drafted in
  H987 is now finalised in [`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](docs/RQ4_EVALUATION_PROTOCOL_2026.md)
  § 6.4. Nothing blocks recruitment but flipping the `features.rq4_study` launch flag (a separate,
  not-yet-made decision). ([H1009](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1009-Sonnet_SanskritGrammar_rq4-consent-approved-gates-closed_16.07.26.md), Sonnet 5 `claude-sonnet-5`)

## [0.28.0] - 2026-07-16

### Fixed
- **Fresh `npm ci` was broken repo-wide**: dependabot [PR #155](https://github.com/gasyoun/SanskritGrammar/pull/155) bumped `react` to 19.2.7 but left `react-dom` at 18.3.1 — an unsatisfiable peer pair (`ERESOLVE`) for any clean install/worktree. Aligned `react-dom` to 19.2.7 (Docusaurus 3.10 supports React 19), lockfile regenerated, production build green. (Fable 5 `claude-fable-5`)

### Changed
- **P3 (SG-MO-017 перфект) — применены четыре заметки визового листа** (виза 8/8 approve была применена в [PR #241](https://github.com/gasyoun/SanskritGrammar/pull/241) как «no wording edits» — заметки MG оставались неисполненными): **(A1)** главный вывод § 4 получил существенную оговорку «**по данным DCS**» — измерена аннотация снапшота `04e0778`, а не язык и не корпусы вообще; **(A5)** вопрос автора «а если проверить по списку известных перфектов?» записан заделом следующей ревизии (§ 3.5): лексиконный зонд по заведомым перфектным формам (`cakāra`, `jagāma`, `dadau`, `veda`…) меряет полноту разметки без ложных кандидатов; **(A4)** дистрибуция вспомогательных перифрастики (as **91,4 %** / kṛ 7,4 % / bhū 0,8 %; 3 sg 86,6 %) маршрутизирована в [методичку Кочергиной § 4.2](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md) как queued material для **Занятия 22 (стр. 153)** (+ строка в метадоке); **(B1+A7)** требование style guide по эталону [rusgram.ru](http://rusgram.ru/main) («чтобы это мог читать человек, а не просто агент») — заминчен handoff [H1003](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1003-Fable_SanskritGrammar_sangram-style-guide-rusgram-etalon_16.07.26.md) (Fable), заметка A7 о «птичьем языке» раздела ограничений — его вход. Ревизия `revision` в [манифесте](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/perfect/article.manifest.json) (append-only, C4). (Fable 5 `claude-fable-5`)

## [0.27.0] - 2026-07-16

### Changed
- **P3 (SG-MO-017 перфект) — авторская виза применена → ОПУБЛИКОВАНО (честный отрицательный результат).**
  [`sangram/articles/perfect/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/perfect):
  ревизия `published` в манифесте, плашка кандидата снята, § 6 п. 6 обновлён на формулировку восстановленного
  провенанс-пина (тег [`c3-pin-04e0778-content`](https://github.com/gasyoun/dcs-conllu/tree/c3-pin-04e0778-content)
  зеркала dcs-conllu). Review-sheet `sangram-sg-mo-017-perfect-visa_15.07.26` — 8/8 approve, без правок к
  формулировкам. Главный результат: DCS-форма-класс (`feat_formation`) не содержит значения «перфект» —
  единственный форма-эвидентный перфект перифрастический (3,96 % бакета `Tense=Past`); главная редуплицированная
  формация (`uvāca`, `cakāra`, `jaghnuḥ`) не тегируется вовсе; тег `red` под `Past` — ложный друг (редуплицированный
  аорист). Kill-gate C5 § 7 P3 СРАБОТАЛ: recall перфекта по форма-классу 2/61 = 3,3 % ≪ 95 %. (Opus 4.8
  `claude-opus-4-8[1m]`, [H983](https://github.com/gasyoun/Uprava/blob/main/handoffs/H983-Opus_SanskritGrammar_sangram-w2-pilot-p3-perfect_15.07.26.md))

## [0.26.0] - 2026-07-16

### Changed
- **P5 (SG-WF-003 kṛt-суффиксы) — авторская виза применена → ОПУБЛИКОВАНО (честный отрицательный результат).**
  [`sangram/articles/krt-suffixes/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/krt-suffixes):
  ревизия `published` в манифесте, плашка кандидата снята. Единственная реализация P5 (коллизии нет, в отличие
  от P4 — supersede-review неприменим). Числа воспроизведены из закоммиченных данных: доля ложных срабатываний
  поверхностного отбора kṛt по исходу леммы **48/81 = 59,3 % ≫ 20 % → kill-gate C5 § 7 P5 СРАБОТАЛ** (шум:
  композиты 31/48, имена 6, посессивная таддхита 6); суффикс -tṛ (`tf`) не отбираем (0 лемм NOUN/ADJ); MW-валидация
  точность 0,75 / полнота 0,09. Оговорка о модельной адъюдикации сохранена. (Opus 4.8 `claude-opus-4-8[1m]`,
  [H996](https://github.com/gasyoun/Uprava/blob/main/handoffs/H996-Opus_SanskritGrammar_sangram-w2-pilot-p5-krt-suffixes_15.07.26.md))

## [0.25.0] - 2026-07-15

### Changed
- **P4 (SG-WF-008 tatpuruṣa) — H989 замещает H990 как каноническую статью и ОПУБЛИКОВАНА (виза MG).**
  Две сессии независимо реализовали P4 (H989 и H990); по итогам слепого сравнения по существу
  канонической выбрана **H989** — доверительные интервалы на κ, двухуровневая декомпозиция
  coarse/fine, детальный панинийский кодбук Лейтана. [`sangram/articles/tatpurusha/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/tatpurusha):
  высший класс κ = **0,93** [0,84–1,0] (117/120), падежный подтип κ = **0,72** [0,60–0,82] (73/93) —
  оба ≥ 0,7, kill-gate C5 § 7 P4 **НЕ сработал**. Обе разметки — Pass A Opus 4.8 (`claude-opus-4-8[1m]`)
  + Pass B Sonnet 5 (`claude-sonnet-5`), одна модельная семья → κ есть **верхняя** граница, помечены
  предварительными. Ревизия `published` в манифесте, плашка кандидата снята. Правки при замещении:
  исправлена воспроизводимость (фильтр метки `tatpurusa` vs слаг `tatpurusha`), добавлен полный аудит-след
  [`annotations_full.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/data/annotations_full.tsv)
  (240 разборов vigraha + обоснование), перенесена оговорка H990 об артефакте рамки выборки (§ 6.7).
  Предыдущая реализация ([0.22.0], H990) помечена superseded. (Opus 4.8 `claude-opus-4-8[1m]`, [H989](https://github.com/gasyoun/Uprava/blob/main/handoffs/H989-Opus_SanskritGrammar_sangram-p4-tatpurusa_15.07.26.md))

## [0.24.0] - 2026-07-15

### Added
- **H996 — Sangram Phase 1 pilot P5 (SG-WF-003, primary kṛt suffixes -ana/-ti/-in) —
  статья-кандидат (Opus 4.8 `claude-opus-4-8[1m]`)**: [`sangram/articles/krt-suffixes/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/krt-suffixes)
  — пятый пилот программы C5, тест предела **EM5** (нет деривационной разметки; сандхи
  стирает границы морфем). Отбор kṛt-производных идёт по поверхностному исходу леммы
  `dcs:lemma /(ana|ti|tf|in)$/`; пилот меряет надёжность. **Отрицательный результат:**
  суффикс **-tṛ (`tf`) вообще не отбираем** — 0 лемм NOUN/ADJ на `tf`. По
  -ana (3438 лемм) / -ti (1886) / -in (2926) ручная адъюдикация 81-лемменной выборки
  даёт **долю ложных срабатываний ≈ 59 % ≫ 20 % → kill-gate C5 § 7 P5 СРАБОТАЛ**.
  Главный шум — **композиты** (31 из 48 ложных: лемма-композит с kṛt-финалью), затем
  имена собственные (6) и посессивная таддхита -in/-vin (6, tapasvin). Словарная
  проверка по MW-этимологии тоже не спасает: точность 0,75, но **полнота лишь 0,09**
  (отбрасывает 96 %, теряя 30 из 33 настоящих производных) — «поверхностный отбор +
  MW-фильтр» плох в обе стороны. Запрос требует переработки (исключить композиты/имена,
  отделить посессив, заменить редкую MW-этимологию морфоанализатором). Скрипты
  [`sg_wf_003_krt_validation.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_003_krt_validation.py)
  + [`sg_wf_003_adjudicate_sample.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_003_adjudicate_sample.py);
  3 валидатора green; полная сборка docusaurus green (проверено на чистом `npm ci`).
  Публикация гейтится авторской визой. **Волна W2 пилотов (P1–P5) завершена.**

## [0.23.0] - 2026-07-15
### Added
- **Print-ready errata sheets — «Замеченные опечатки» из errata.yml (H993)** — new generator [`scripts/build_errata_print_sheet.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_errata_print_sheet.py) (`npm run errata:print`) renders each populated `<Book>/errata.yml` as a self-contained, A4-print-styled `<Book>/ERRATA_PRINT_SHEET.html` in the classic publisher's layout (№ · Место · Напечатано · Следует читать; sources + generation date in small print) — printable from any browser as a physical-book insert or a reprint-editor hand-off. Parsing/dedup/ordering imported from `build_errata.py` (one canonical errata.yml reader); empty registers get no sheet, stale sheets are removed on regen. First sheets: Bühler (8 позиций), GasunsDhatu (77), Knauer (25 after dedup), Ocherk (2). (Fable 5 `claude-fable-5`, [H993](https://github.com/gasyoun/Uprava/blob/main/handoffs/H993-Fable_SanskritGrammar_errata-print-sheets_15.07.26.md))

## [0.22.0] - 2026-07-15

### Added
- **⚠️ SUPERSEDED by H989 ([Unreleased]).** Эта реализация P4 заменена канонической H989 по итогам
  слепого сравнения по существу; запись сохранена как история выпуска. Далее — как было отгружено:
- **H990 — Sangram Phase 1 pilot P4 (SG-WF-008, determinative compounds / tatpuruṣa) —
  статья-кандидат (Opus 4.8 `claude-opus-4-8[1m]` + Sonnet 4.6 `claude-sonnet-4-6`)**:
  [`sangram/articles/tatpurusha/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/tatpurusha)
  — четвёртый пилот программы C5, тест предела **EM4**: DCS даёт членение композита
  (нечленные члены `feat_case=Cpd`, **841 052** токена), но НЕ тип — у **98,56 %**
  членов пусто даже UD-отношение (`deprel=NULL`). Тип классифицирован вручную двумя
  **независимыми** проходами (Opus + Sonnet, разные модели — против инфляции согласия)
  по кодбуку **Э. Лейтана** (пани́ниевская иерархия `dvigu ⊂ karmadhāraya ⊂ tatpuruṣa`).
  **Первый ПОЛОЖИТЕЛЬНЫЙ kill-gate серии** (после сработавших P2/P3): межразметочное
  согласие на 5 классах Лейтана **κ=0,818** (почти идеально), бинарно «татпуруша или
  нет» **κ=0,887**, полное 7-классное κ=0,710 → **kill-gate C5 § 7 P4 (κ<0,7) НЕ
  сработал**, частоты типов публикуемы. Из 18 расхождений 7-классного разбора 11 —
  подграница `tatpuruṣa↔karmadhāraya` (внутри одного класса Лейтана, исчезает на
  кодбучном уровне); остаются 7 межклассовых (4 `bahuvrīhi↔tatpuruṣa` — эндо/экзо, это
  C6). Татпуруша — доминирующий тип (~56 %; с подтипами ~76 %). Surface-побочно:
  расхождение с реестром C2 (SG-WF-010 паркует dvigu с avyayībhāva; Лейтан — под
  tatpuruṣa) зафиксировано. Скрипты
  [`sg_wf_008_compound_sample.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_008_compound_sample.py)
  + [`sg_wf_008_kappa.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_008_kappa.py);
  3 валидатора + docusaurus build green. Публикация гейтится авторской визой.

## [0.21.0] - 2026-07-15

### Changed
- **SG-MO-002 «Основы на -a» ОПУБЛИКОВАНА — авторская виза применена (пилот P1, H953)** — MG voted the 7-card review-sheet 7/7 approve; the `published` revision entered [`article.manifest.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/a-stems/article.manifest.json), the candidate banner left the [MDX](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/a-stems/index.mdx). Visa edits applied: (A2) terminology — the vocative is a **падежная форма**, not a падеж (matrix now reads «8 падежных форм × 3 числа»); (A2) the universe boundaries got their rationale + consequences spelled out in § 6 п. 1/3 (why `upos=NOUN` only, why suffix-lemma *tva* is in, what each choice does to the numbers); (A5) Vedic stratification recorded as feasible (270-text composition + `m_ismantra` 120,707 tokens + surface-recognizable variant endings) and queued as the article's next revision; (A6) **the orphaned C3 pin is restored**: GitHub had GC'd commit `04e0778` entirely (422 on the API), so the live mirror commit was verified count-identical to the ingest on all three dimensions (270 texts · 5,688,416 tokens · 754,726 sentences) and tagged [`c3-pin-04e0778-content`](https://github.com/gasyoun/dcs-conllu/tree/c3-pin-04e0778-content); [C3 § 2.1](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx) amended with the restoration + the "pin by tag, never by bare hash" rule (revision row added). ([H953](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H953-Fable_SanskritGrammar_sangram-w2-pilot-p1-a-stems_14.07.26.md)) (Fable 5 `claude-fable-5`)

### Added
- **H984: RQ4 diagnostic item bank + protocol decisions ruled.** [`TolchelnikovTalmud_2026/tools/build_rq4_item_bank.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/build_rq4_item_bank.py) emits [`data/rq4_item_bank.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/rq4_item_bank.json): 24 items (8 per pre/post/retention phase, 2 per row) drawn from the 745-root Приложение 1 catalogue, restricted to the on-ramp's 4 taught rows (A₁/I₁/U₁/R₁), excluding every root already used in the on-ramp's/talmud-02's worked material, frequency-sorted via kosha's `lemma_frequency.tsv`. 307 eligible candidates, 0 shortfall on any row. [`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md) updated: MG ruled §6.1–6.3 (Systema-hosted harness, Systema's own Kochergina-stage students, 4-week retention window); §6.4 (consent wording) still open. Harness build follows (H988).
## [0.20.0] - 2026-07-15

### Added
- **H983 — Sangram Phase 1 pilot P3 (SG-MO-017, the perfect) — статья-кандидат
  (Opus 4.8 `claude-opus-4-8[1m]`)**: [`sangram/articles/perfect/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/perfect)
  — третий пилот программы морфологии C5, прямой тест предела **EM2** (дефект C3 Д1):
  UD-разметка DCS склеивает все претериты под `Tense=Past` (**102 055** финитных
  токенов), поэтому слот предписывает отбор по **форма-классу**, не по времени. Итог —
  **честный отрицательный результат**: собственный форма-класс DCS (`feat_formation`)
  **не содержит значения «перфект»**. Единственный форма-эвидентный перфект —
  перифрастический (`peri`, **4 046 = 3,96 %** бакета; вспомогательный `as` 91,4 % /
  `kṛ` 7,4 % / `bhū` 0,8 %; 86,6 % — 3 sg). Главная, редуплицированная формация
  перфекта (`uvāca`, `cakāra`, `jaghnuḥ`) **не тегируется вовсе** — лежит в NULL-бакете
  (84,22 %), неотличимая от аориста. Тег `red` под `Past` — это редуплицированный
  **АОРИСТ** (`ajījanat`, аугмент + редупликация), ложный друг для наивного правила
  «редупликация = перфект». **Kill-gate (C5 § 7 P3, <95 %) сработал:** в выборке 80
  токенов 61 (76 %) — перфекты, но форма-класс опознаёт лишь 2 (**recall 3,3 %**);
  количественная часть снимается. Любопытство: редчайший плюсквамперфект (`Plp`/`Pqp`,
  200) тегирован отдельным временем, а частотный перфект — нет.
- Скрипты: [`scripts/sg_mo_017_perfect_coverage.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_017_perfect_coverage.py)
  + [`scripts/sg_mo_017_adjudicate_sample.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_017_adjudicate_sample.py);
  данные — [`sangram/articles/perfect/data/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/perfect/data)
  (`coverage_summary.json`, `formation_partition.csv`, `periphrastic_perfect.csv`,
  выборка + вердикты). Три валидатора + docusaurus build green. Публикация гейтится
  авторской визой.

## [0.19.0] - 2026-07-15

### Added
- **H980 — Sangram Phase 1 pilot P2 (SG-MO-013, thematic present classes) — статья-кандидат
  (Opus 4.8 `claude-opus-4-8[1m]`)**: [`sangram/articles/thematic-present/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/thematic-present)
  — второй пилот программы морфологии C5 (после P1 a-stems), проверяет предел EM1
  «класс презенса не в морфопризнаках DCS». Измерение по методу
  аттестовано/порождено/традиционно над **353 215 презентными финитными токенами**
  пинованного снапшота DCS: класс (гана I–X) отсутствует в `feat_*` **и** в собственном
  словарном коде леммы DCS (`lemma.grammar` — не гана: tud VI→7, viś VI→3, grah IX→4);
  восстановление требует join'а во внешний инвентарь [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots),
  который неоднозначен — **чисто-классифицируемо лишь 38,85 %** (одноклассный корень 25,16 %
  + форменный `-aya-` 13,68 %; много-класных корней 51,07 %, не-join'ящихся 10,08 %).
  **Kill-gate (C5 § 7 P2) сработал** → частоты гана публикуются как оценки по
  чисто-классифицируемому подмножеству, не как токен-уровневые факты; ручная адъюдикация
  80-токенной выборки: морфоанализ восстанавливает 78/80. Скрипты
  [`sg_mo_013_thematic_present_coverage.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_013_thematic_present_coverage.py),
  [`sg_mo_013_adjudicate_sample.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_013_adjudicate_sample.py),
  [`sg_mo_013_build_examples.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_013_build_examples.py);
  первый боевой манифест `art:thematic-present` (toc_ref SG-MO-013). Все три валидатора +
  `npm run build` green. **Виза MG получена 15-07-2026 → опубликовано** (ревизия `published`
  в манифесте, плашка кандидата снята — первая опубликованная статья серии Sangram).

## [0.18.0] - 2026-07-15

### Added
- **H976 — RQ4 evaluation protocol spec (built by Sonnet 5 `claude-sonnet-5`; verified,
  merged and closed out by Fable 5 `claude-fable-5`)**:
  [`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md)
  (+ meta) — full study design for the digital-pedagogy field's RQ4 (on-ramp-first vs
  Талмуд-first): falsifiable H0/H1, between-subjects two-arm design matched on prior
  exposure, two diagnostic-instrument metrics (time-to-first-correct-derivation,
  retention @ N weeks), item-bank plan from Talmud Appendix 1's 65 tagged roots,
  pre-registered analysis plan with an honest power reality-check (~64/arm for d≈0.5 —
  wave 1 is a pilot, not confirmatory), and 4 `@DECIDE` gates (recruitment channel,
  retention window, hosting/instrumentation home, consent wording) filed to the GTD hub.
  Protocol-only: no harness code, no simulated data, no recruitment.

## [0.17.0] - 2026-07-15
### Added
- **1978 morphoclass-crosswalk column: the §68 structural prediction is CONFIRMED (H978)** — [`ZalizniakOcherk_1978/build_1978_crosswalk.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/build_1978_crosswalk.py) closes the last named instrument of the Ocherk register: seṭ/aniṭ membership tracks alternation-series × полноизменяемость almost deterministically (group A 92.6% aniṭ-or-veṭ vs group B 93.0% seṭ-or-veṭ; plain-type leakage 7% both ways), with veṭ as exactly the fluctuation band Zaliznyak's hedge reserved. OCH-21/22/23 flip to measured TRUE (Ocherk register now 60 TRUE · 14 UNTESTABLE · 0 flags of 74); the earlier naive-join dead end is fully explained, not just superseded. Companion columns kept in ZalizniakOcherk_1978/ (merging into the Talmud crosswalk CSV = a human's call). ([H978](https://github.com/gasyoun/Uprava/blob/main/handoffs/H978-Fable_SanskritGrammar_1978-crosswalk-column-unblock-och21-23_15.07.26.md)) (Fable 5 `claude-fable-5`)

## [0.16.0] - 2026-07-15
### Added
- **H797 Phase 2 COMPLETE: every register backlog drained, one new corpus instrument built** — the cross-grammar claim-verification programme closes its harvest debt in one pass: **Bühler** 64 → 403 verified (381/7/8/7; all 8 FALSE misprint-class — the register doubles as an errata sweep), **Knauer** 10 → 214 audited parses (210/4/0 — the 1908 footnote apparatus is error-free at full coverage; PARSE_AUDIT.md now generated), **Konspekt** 2 → 17 verified (ALL TRUE — including the five Rigveda exact fractions, unblocked by the NEW period-isolation instrument [`rigveda_kz_fractions.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/rigveda_kz_fractions.py) over the pinned dcs_full.sqlite: claimed 1/3 → measured 33.2%, 7/8 → 84.9%, 3/5 → 65.6%, 1/2 → 42.3%, 5/6 → 76.9% — hand-era Vedic fractions reproduced by treebank; the same instrument measured injunctive RV 7.3% vs epic 0.5% and ta-participle predication RV 1.7% vs epic 11.8-18.4%, the first point on the Ocherk-§207 style arc). Programme totals: **942 verified claims + 214 audited parses across 5 books**; Zalizniak 91/91 unflagged; Russian READMEs updated for all drained registers. Remaining H797: only the Morphology-1975 genre ruling. ([H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md)) (Fable 5 `claude-fable-5`; seeds Sonnet 5 `claude-sonnet-5`)

## [0.15.0] - 2026-07-15
### Added
- **Third claim-verification register complete: Zalizniak Ocherk 1978 fully drained — the programme's first zero-flag book (H797 Phase 2)** — [`ZalizniakOcherk_1978/claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/claims.yml) goes 6 → **74 verified** (57 TRUE · 0 OVERSTATED · 0 FALSE · 17 UNTESTABLE · 7 M.G. footnotes; backlog `candidates: []`), past the ≥50 stop condition. With three discursive grammars graded, the calibration ranking is clean: **Зализняк 0 флагов/74 > Бюлер 5/64 > Кочергина 12/234** — presentation calibration, not factual accuracy, is where grammars measurably differ (the verb-accent rule is the sharpest pair: «никогда» = OVERSTATED HK-10 vs «как правило» = TRUE OCH-72). The 17 UNTESTABLE entries double as the pipeline's next-instruments list (period-tagged slices for §207's diachronic style shift; a treebank; compound typing; the 1978↔2026 morphoclass-series crosswalk; a root-shape parser), and two negative pilots are recorded with numbers (naive Talmud series join inverts §68; aggregate i-rate proxy inverts §63) per the PALSULE-audit lesson. The Talmud's Приложение-1 catalog debuts as machine-readable D-B morphoclass ground truth. ([H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md), seed [PR #196](https://github.com/gasyoun/SanskritGrammar/pull/196) Sonnet 5 `claude-sonnet-5`) (Fable 5 `claude-fable-5`)

## [0.14.1] - 2026-07-15
### Added
- **Russian folder README for WhitneyGrammar_1889** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/WhitneyGrammar_1889/README.md) (the folder has no book-level changelog — Whitney predates the per-book release scheme, so the bullet lives here): по-русски — паспорт издания (2-е изд. 1889/тираж 1950, public domain, Wikisource CC BY-SA 4.0; все 19 `.mdx` генерируются `scripts/build_whitney.py` из соседнего [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots), руками не правятся), история H427 (деванагари парадигм регенерирована из IAST самого Уитни: 1 840 ячеек + 186 inline-форм, PUA-глифы в 57 % битых строк), и роль эталона в программе проверки утверждений — авторитет системного факта D-B (все 308 записей трёх реестров цитируют по §§), жанровая точка отсчёта линии Уитни→Зализняк→Толчельников, конкордансный хребет (H540 + sangram), и будущий «подсудимый» класса система-vs-употребление в A60. Completes the Russian findings-README set: all 7 programme-relevant books covered. (Fable 5 `claude-fable-5`)

## [0.14.0] - 2026-07-15
### Added
- **SG-MO-002 «Основы на -a» — первая статья-кандидат корпусной грамматики Sangram (пилот P1, флагман метода C5)** — the attested/generated/traditional method (C5 § 3) gets its first end-to-end measurement: of the 8-case × 3-number paradigm matrix, **not a single a-stem noun attests all 24 cells** in the pinned DCS snapshot (`04e0778`, 270 texts / 5,688,416 tokens) — masc.: 21,837 lemmas / 716,864 tokens, median **1** cell per lemma, max *putra* 23/24; neut.: 13,857 / 359,194, max *netra* 22/24; *deva* (17,536 tokens) reaches 22/24 with its Ins.Du and Loc.Du each attested **once**; rarest cell Dat.Du (46 lemmas, 0.21 %). Kill-gate passed: 0/60 false positives in the seeded validation sample (95 % CI 0–6.0 %, threshold 10 %). New: article-candidate [`sangram/articles/a-stems/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/a-stems/index.mdx) + first real C4 manifest [`article.manifest.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/a-stems/article.manifest.json) (`art:a-stems`, `toc_ref` SG-MO-002, 3 SLP1-canonical examples incl. the unique *devābhyām* MS 2,8,11) + reproducible corpus package [`data/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/articles/a-stems/data) (verbatim SQL, seeded sample + 60 adjudicated verdicts, per-cell CSVs, MWinflect paradigms, snapshot SHA-256) + analysis script [`scripts/sg_mo_002_a_stems_coverage.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_002_a_stems_coverage.py) (re-run 15-07-2026 reproduced all numbers). Publication gated on the author's visa (review-sheet in local `review/`, registered in Uprava). Provenance gap recorded: the dcs-conllu mirror's history rewrite orphaned the C3 pin `04e0778` — the SQLite master's provenance table + file SHA-256 now carry the binding (article § 6.7). ([H953](https://github.com/gasyoun/Uprava/blob/main/handoffs/H953-Fable_SanskritGrammar_sangram-w2-pilot-p1-a-stems_14.07.26.md)) (Fable 5 `claude-fable-5`)

## [0.13.0] - 2026-07-14
### Added
- **Cross-grammar claim-verification layer: Bühler register live (H797 Phase 2)** — the two-axis pipeline (fact × pedagogy, FINDINGS §72) is now grammar-agnostic and running on its second book: [`BuhlerLeitfaden_1923/claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml) opens with **64 verified claims** (58 TRUE · 4 OVERSTATED · 1 FALSE · 1 UNTESTABLE · 13 M.G. frequency footnotes) drawn from a **404-candidate 6-reader full-book harvest** ([`claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims_harvest.yml), 339 in backlog). Headline findings: Bühler's hedges are systematically well-calibrated (the same seṭ -iṣya 56.8% number that flagged Kochergina HK-4 confirms Bühler TRUE); his failure modes are the Урок-I voice absolute contradicted by his own later lessons, rare-before-common ordering (periphrastic future taught before a 14×-more-frequent simple future; -tavat billed "также часто" beside a 100×-more-frequent PPP), and one flipped frequency direction (perfect "реже" than imperfect vs DCS 61,986 > 47,554). [`scripts/build_claims.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_claims.py) de-Kochergina-ised (per-book `*gives_number`, shared-battery link, generic headings); [`verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py) gained the HB metrics (-tāt imperative 0.95%, optative 9.3% of verbal, periphrastic vs simple future 1,290 vs 18,004, absolutive split -ya 78.4% / -tvā 19.6% / -am 0.4%). ([H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md)) Absorbs the same-day concurrent seed slice BU-1..BU-5 ([PR #184](https://github.com/gasyoun/SanskritGrammar/pull/184), Sonnet 5 `claude-sonnet-5`): BU-3 promoted as HB-64, overlapping entries double-verified, BU-2's frequency-parity reading of «равноправно» reconciled in HB-61's note; the seed's book-local [`verify_claims_dcs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/verify_claims_dcs.py) battery kept. (Fable 5 `claude-fable-5`)

## [0.12.0] - 2026-07-14
### Changed
- **`scripts/build_claims.py` generalized off Kochergina-only field names** — the harvest-backlog
  "gives a number?" column read the hardcoded key `kochergina_gives_number`; it now accepts any
  `<author>_gives_number` key, and the methodology-synthesis section header no longer hardcodes
  "Kochergina's presentation principles". Needed to onboard `BuhlerLeitfaden_1923/claims.yml`
  (H797 Phase 2) without a second per-book special case.
### Added
- **Sangram programme overview — public index of indexes (series S19 capstone)** — new category landing page [`sangram/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/index.mdx) (`/grammars/sangram`): the twelve public pillars of the 2026 series (charter, TOC network, corpus-evidence method, editorial/i18n contract, morphology W2 + syntax/semantics W3–W4 programmes, atlas data contract + five views + unified route) with their typed relations, an accessible Mermaid map, and the public/private boundary statement. The sangram category now opens on this authored page instead of a generated index. Production build green under `onBrokenLinks: 'throw'`. ([H636](https://github.com/gasyoun/Uprava/blob/main/handoffs/H636-Fable_Uprava_megabook-sangram-capstone_11.07.26.md), Fable 5 `claude-fable-5`)
- **Sandhi reader-hover surface (pedagogy Phase-4, 3/4)** — [`SandhiCollider.jsx`](https://github.com/gasyoun/SanskritGrammar/blob/main/src/components/talmud/SandhiCollider.jsx) is now data-driven from kosha's [`corpus_sandhi.tsv`](https://github.com/gasyoun/kosha/blob/main/data/sandhi/corpus_sandhi.tsv): hovering (or focusing) the collided result shows the induced rule + its corpus frequency + a "#N most common sandhi" badge (top-10 highlighted), with an honest `нет в корпусе` state for the 29 rare junctions with no corpus attestation. New generator [`scripts/build_sandhi_frequency.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_sandhi_frequency.py) vendors the vowel-coalescence subset (74 junctions) into a committed data module `src/components/talmud/sandhiFrequency.js` (build never needs kosha checked out). The third of the sandhi-programme's four Phase-4 reader surfaces. ([H917](https://github.com/gasyoun/Uprava/blob/main/handoffs/H917-Opus_SanskritGrammar_sandhi-reader-hover-collider_14.07.26.md), [PR #183](https://github.com/gasyoun/SanskritGrammar/pull/183)) (Opus 4.8 `claude-opus-4-8`)
- **Difficulty & ordering result (pedagogy RQ1) + paper A63 skeleton** — [`scripts/build_difficulty_ordering.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_difficulty_ordering.py) + [`data/difficulty_ordering/`](https://github.com/gasyoun/SanskritGrammar/tree/main/data/difficulty_ordering) + writeup [`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md). Corpus frequency tracks the expert learn-first order for content vocabulary (Kendall-τ 0.887) but the decisive act is excluding the top function words (46 % of top-50 lemmas, all indeclinables/pronouns) and correcting DCS's epic-genre bias; textbook introduction order is frequency-agnostic (τ≈0.05). Paper [A63](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/DifficultyOrdering_A63/OUTLINE_difficulty-ordering_A63.md) seeded (2/5). Wave-1a of the digital-pedagogy field (H913). (Opus 4.8 `claude-opus-4-8[1m]`)
- **Zaliznyak-made-learnable on-ramp (pedagogy §3.6)** — a beginner-graded entry to the Ряд/Тип/seṭ system below Tolchelnikov's *Талмуд*: new [`TolchelnikovTalmud_2026/onramp/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp) (index + 3 steps — grades / position+type / seṭ) with "one tap deeper" links into the full chapters, design doc [`ZALIZNYAK_ONRAMP_DESIGN.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/ZALIZNYAK_ONRAMP_DESIGN.md). `AblautMachine` gained optional `rows`/`initialSeries` props (the on-ramp shows the 4 high-frequency rows; talmud-02 unchanged). Wave-1c of the digital-pedagogy field (H915). (Opus 4.8 `claude-opus-4-8[1m]`)
- **Last-mile pipeline spec (pedagogy §14.2)** — [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md) (+ meta): the kosha→Systema contract that closes the "last mile" — 3 hops (reader-as-a-service, frequency-ordered SRS deck, difficulty→sequencing), a **vendored-data-file** contract matching the `SanskritGlossary.php` precedent, a one-rung B1-subhāṣita demo path, folding in W1a's strip-function-words + genre-correct ranking rule. Spec-only (no Systema code touched; straddle-tier fence). Wave-1d of the digital-pedagogy field (H916). (Opus 4.8 `claude-opus-4-8[1m]`)
- **A62 agenda paper — the field's defining paper (readiness 2/5)** — [`papers/DigitalPedagogyAgenda_A62/`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/DigitalPedagogyAgenda_A62/OUTLINE_digital-sanskrit-pedagogy-agenda_A62.md): survey + 4 falsifiable research questions (RQ1 already confirmed by the difficulty result, RQ3 partial via A60), an RQ4 evaluation design using the Zaliznyak on-ramp as an A/B testbed, a data-inventory table, venue candidates. **Completes wave-1** of the digital-pedagogy field (H914; tier-locked Fable, drafted on Opus by author override — a Fable voice-pass is the 4→5 step). (Opus 4.8 `claude-opus-4-8[1m]`)

### Fixed
- **Atlas overview omitted the B5 dependencies view** — [`sangram/atlas/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/atlas/index.mdx) listed only four of the five live views; the [dependencies view](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/atlas/dependencies.mdx) (slot B5, merged 12-07-2026) is now linked. Found by the S19 capstone hostile audit ([H636](https://github.com/gasyoun/Uprava/blob/main/handoffs/H636-Fable_Uprava_megabook-sangram-capstone_11.07.26.md), Fable 5 `claude-fable-5`).

## [0.11.0] - 2026-07-14
### Added
- **Digital Sanskrit pedagogy established as a priority research field** — org-wide field metadoc [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md) (+ [`.meta.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.meta.md)) consolidating the three pre-existing pedagogy maps by reference, plus a layered plan in [`docs/`](https://github.com/gasyoun/SanskritGrammar/tree/main/docs) ([PLAN](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md) · [ROADMAP](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md) · [ARCHITECTURE](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_DIGITAL_SANSKRIT_PEDAGOGY.md) · [IMPLEMENTATION](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_DIGITAL_SANSKRIT_PEDAGOGY_WAVE1.md) · [VERIFICATION](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md)). Aspect-primary taxonomy with layered tags (CEFR rung · NLP capability · research-Q · traditional discipline · owning repo) from which the matrix & learner-journey views derive. Registered org-wide: MEGABOOK §2.10 (+ §2.9 strengthened), ARTICLES A62, GTD straddle tier (research T1 / product T0); wave-1 handoffs H912–H916 minted. Authored via `/ask` (17 rulings, zero blocking forks). (Opus 4.8 `claude-opus-4-8`)

## [0.10.0] - 2026-07-14
### Fixed
- **In-page ToC anchors on the Word-converted book pages** ([`src/remark/fixHeadingAnchors.mjs`](https://github.com/gasyoun/SanskritGrammar/blob/main/src/remark/fixHeadingAnchors.mjs)) —
  a new build-time remark plugin. These pages use `#` (h1) for every section heading, but
  Docusaurus only assigns anchor ids to h2–h6, so the baked-in `Оглавление` links (`#урок-1.` etc.)
  all pointed at id-less headings. The plugin demotes content `h1 → h2` (page title comes from
  frontmatter) and re-slugs each in-page anchor with the same github-slugger — only when it lands on
  a real heading, so unmatched links are left as-is. Broken anchors **93 → 25** (Apte 34→0,
  Talmud 33→8, Gasūns 26→17); the 25 residual are genuine missing targets / `_Toc…` Word bookmarks.
  Scoped to pages that actually carry an in-page ToC. (Opus 4.8 `claude-opus-4-8`.)

### Changed
- Section headings on the ToC book pages now render as **h2** (was h1), which also surfaces
  Docusaurus's right-side table-of-contents navigation on those pages.

## [0.9.2] - 2026-07-14
### Changed
- **`onBrokenLinks: 'throw'`** (was `'warn'`) in [`docusaurus.config.mjs`](https://github.com/gasyoun/SanskritGrammar/blob/main/docusaurus.config.mjs) —
  now that every in-site broken link is cleared (catalog, Fortunatovskiye landing page, papers
  de-link), a dead cross-link fails the build + CI instead of shipping silently. `onBrokenAnchors`
  stays `'warn'` — the OCR'd book pages still carry the separate `#-N` self-anchor cleanup. (Opus 4.8 `claude-opus-4-8`.)

## [0.9.1] - 2026-07-14
### Fixed
- **Broken in-site link on the Subject-concordance catalog page.** `build_subject_concordance.py`
  emitted `[Whitney book pages](../WhitneyGrammar_1889/00_index)`, but Docusaurus strips the `00_`
  numeric prefix so the page's real route is `.../WhitneyGrammar_1889/index` — the link 404'd. Fixed
  the link in the generator and regenerated
  [`SubjectConcordance/catalog.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/SubjectConcordance/catalog.mdx);
  `npm run build` confirms the broken-link warning for that page is gone. (Opus 4.8 `claude-opus-4-8`.)

## [0.9.0] - 2026-07-13
### Added
- **First automated test suite + CI** — a `tests/` pytest suite (59 characterization tests) pinning
  the pure helpers of the core build scripts (`build_whitney`, `mdx_postprocess`, `build_errata`,
  `build_claims`, `build_quantifiers`, and the two divergent `slugify` functions), plus a
  [`.github/workflows/ci.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/.github/workflows/ci.yml)
  that runs the suite **and a full Docusaurus build on every PR** — the pre-merge safety net that
  would have caught the `@docusaurus` version-skew build break before it reached `main`. Scripts had
  zero test coverage before this. (Opus 4.8 `claude-opus-4-8`.)
- **A54 author-voice pass + sign-off doc** ([`SIGNOFF_A54_author_pass.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/SIGNOFF_A54_author_pass.md)) —
  `/paper-author-pass` over the Kulikov-answer article
  ([`IIL_ZALIZNIAK_ALTERNATIONS_ARTICLE_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/IIL_ZALIZNIAK_ALTERNATIONS_ARTICLE_2027.md)).
  Register confirmed as the author's own; no body-prose or substance edits (the 3-lens register
  pass + hostile referee had already settled voice). Four voice observations and the full ⟦MG⟧
  submission gate collected into the sign-off doc for a 30-minute read-and-sign; A54 held at 4/5
  until author sign-off. (Opus 4.8 `claude-opus-4-8`, umbrella
  [H552](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H552-Fable_SanskritGrammar_iil-zalizniak-polemic-article_10.07.26.md).)

### Fixed
- **Broken production build — `@docusaurus/*` version skew.** A partial Dependabot bump
  ([#156](https://github.com/gasyoun/SanskritGrammar/pull/156)) left `@docusaurus/preset-classic`
  at `3.10.2` while `core`, `theme-mermaid`, `module-type-aliases` and `types` stayed `3.10.1`, so
  `docusaurus build` aborted with `Invalid name=docusaurus-plugin-content-docs version number=3.10.2`.
  Aligned all five `@docusaurus/*` packages to `3.10.2`; the regenerated
  [`package-lock.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/package-lock.json) also
  dedupes 198 now-redundant nested `@docusaurus/*` subtrees (−4.5k lines). Supersedes the three open
  single-package Dependabot PRs (core / theme-mermaid / module-type-aliases → 3.10.2). Build verified
  green. (Opus 4.8 `claude-opus-4-8`.)
- **Deprecated `onBrokenMarkdownLinks` config warning** (removed in Docusaurus v4) — moved from the
  top level into [`docusaurus.config.mjs`](https://github.com/gasyoun/SanskritGrammar/blob/main/docusaurus.config.mjs)
  `markdown.hooks.onBrokenMarkdownLinks`, silencing the per-build warning.
- **Revived 5 dead `rws_*.py` revision scripts.** `rws_apply.py`, `rws_assemble.py`,
  `rws_extract_worklist.py`, `rws_gen_skipped.py` and `rws_triage.py` hardcoded
  `BASE = C:\…\SanskritGrammar-h385\…`, an H385 worktree that no longer exists — every one of
  them crashed on a missing path. Replaced the dead literals with `__file__`-derived paths
  (matching the already-correct `rws_to_docx.py`), so the H385 revision pipeline runs again from
  any checkout. (Opus 4.8 `claude-opus-4-8`.)
- **Dead cross-link** in [`TolchelnikovTalmud_2026/CHANGELOG.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/CHANGELOG.md) —
  `ZALIZNYAK…` → `ZALIZNIAK…` (misspelt target; file is `ZALIZNIAK_1975_1978_2004_COMPARISON.md`).

### Changed
- **`scripts/requirements.txt`** — declared the two already-imported but unlisted runtime deps
  `pyyaml` (used by `build_claims`/`build_errata`/`build_quantifiers`/`harvest_quantifiers`) and
  `python-docx` (`rws_to_docx.py`), so a fresh `pip install -r` no longer fails at import time.
- **UTF-8 output rule swept across 12 tracked scripts.** Added the missing
  `sys.stderr.reconfigure(encoding='utf-8')` to 6 scripts that only reconfigured stdout, and
  replaced the older `sys.stdout = io.TextIOWrapper(…)` idiom with the standard
  `sys.stdout/stderr.reconfigure(…)` pair in the 6 `rws_*.py` scripts, so Devanagari/IAST output
  can't raise `UnicodeEncodeError` on a non-UTF-8 Windows console. (Opus 4.8 `claude-opus-4-8`.)

## [0.8.0] - 2026-07-12
### Added
- **`verify_claims_dcs.py` (Kochergina) extended with reproducible backlog-verification metrics
  (H797)** — a vowel census over the full DCS-2021 running text ([`0.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py)),
  verb-class share, past-tense competition and case-slot token distribution, so every M.G.
  frequency footnote in the claim register is re-runnable from the committed corpus. Feeds the
  book-level v0.3.0 drain of the Kochergina claim register (43 → 234 verified claims).
  ([H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.7.0] - 2026-07-12
### Added
- **A60 hostile referee pass + fixes (H773 → toward Q4)**
  ([`A60_review_opus48.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/A60_review_opus48.md)):
  reject-by-default review of the single-book draft. An independent agent re-derived every number from
  the committed sources — register composition, divergence distributions, future-stem allomorphs,
  conditional/precative rates all reproduce exactly (figures-vs-data clean).
### Changed
- **A60 draft strengthened** per the review — **2 Major + 6 Minor findings applied**:
  §2 related work now cites the corpus-based materials-evaluation subfield (Nation 2001) and the
  descriptive/*rules-as-regularities* corpus-grammar tradition (Biber et al. 1999) and re-scopes the
  novelty to the Sanskrit *seṭ/aniṭ* target (M1); a single-annotator / no-IAA validity threat added to
  Limitations (M2); the 43-vs-42 register count reconciled in prose and the stale `claims.yml` header
  comment corrected; abstract "predicts" → "aligns closely with"; HK-16 citation, tool-version note,
  ground-truth provenance, and the DCS citation tidied. One **venue @DECIDE** left open (ISCLS / WSC
  computational / lexicography-DH journal) → GTD. Readiness held at 4/5.
  ([H773](https://github.com/gasyoun/Uprava/blob/main/handoffs/H773-Opus_SanskritGrammar_grammar-asserts-corpus-denies-study_12.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.6.0] - 2026-07-12
### Added
- **A60 full single-book draft — "grammar claims the corpus does not confirm" (H773 phase Q3)**
  ([`DRAFT_grammar-claims-corpus-denies_A60.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/DRAFT_grammar-claims-corpus-denies_A60.md)):
  the complete paper in prose — abstract, introduction, related work (ACL-anthology-anchored, the
  four reference titles web-verified), data & method (two-axis register, triangulation, the four-way
  divergence typology, reproducibility), results (register composition, the 12-row central table, the
  future-stem flagship at 56.8% *seṭ*, the one FALSE claim, aggregation), discussion, limitations, and
  future work. Single-book by design (Kochergina 1998); the cross-grammar comparison (Q2) is framed as
  an enhancement, not a gap. The central class⇄pedagogy finding is stated with an explicit
  anti-circularity caveat. A60 readiness 3/5 → 4/5. Remaining to submission: `/paper-referee` +
  `/paper-author-pass` (Fable 5) + `/venue-scout`.
  ([H773](https://github.com/gasyoun/Uprava/blob/main/handoffs/H773-Opus_SanskritGrammar_grammar-asserts-corpus-denies-study_12.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.5.0] - 2026-07-12
### Added
- **A60 central table — "grammar claims the corpus does not confirm" (H773 phase Q1)**
  ([`TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60)):
  the paper's core table, built from H768's now-complete 43-claim Kochergina register. All **12**
  `verdict_fact ∈ {OVERSTATED, FALSE}` divergences (of 43 verified — 28 TRUE / 11 OVERSTATED /
  1 FALSE / 3 UNTESTABLE) are classified by the H773 four-way divergence typology
  (**over-generalisation 8 · rule-real-but-marginal 3 · flat-contradiction 1 · system-vs-usage 0**)
  and quantified. New reproducible layer, kept out of H768's file per the consume-don't-re-derive
  boundary: [`divergence_classes.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/divergence_classes.yml)
  (class + rationale per claim) + [`build_divergence_table.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/build_divergence_table.py)
  (joins it to `claims.yml` → the generated [`TABLE_grammar-claims-corpus-denies_A60.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/TABLE_grammar-claims-corpus-denies_A60.md);
  `--check` guards any unclassified divergence). Finding: the divergence class **predicts** the H768
  pedagogy verdict (class 1 ⇔ `MISLEADING`, classes 2+4 ⇔ `FREQUENCY-HIDDEN`); the empty
  system-vs-usage class is itself a result. A60 readiness 2/5 → 3/5. Central table complete for
  Kochergina; per-grammar comparison (Q2) still gated on a second grammar's harvest.
  ([H773](https://github.com/gasyoun/Uprava/blob/main/handoffs/H773-Opus_SanskritGrammar_grammar-asserts-corpus-denies-study_12.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.4.0] - 2026-07-12
### Added
- **Sangram contract C5 — morphology programme (W2)** ([`sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx),
  route `/grammars/sangram/morphology-program`): thematic programme for wave **W2** over
  the C2 registry's WF (11) + MO (32) morphology slots — 9 macroclusters; the
  **attested / generated / traditional** three-source method (the programme's methodological
  core: attested-in-DCS carries the quantitative claim, generated fills paradigm cells as
  hypotheses, traditional witnesses existence, never silently merged); evidence limits
  EM1–EM8 tied to C3 defects Д1–Д8; morphology query-design (form-class not UD-Tense,
  WhitneyRoots class join, paradigm-cell-coverage query, dictionary-derivation join);
  per-cluster W2 quotas (**19 ① core across all 9 macroclusters**, within the charter 15–25
  range, ≥1 per macrocluster); 5 pilots each stressing a distinct limit with launch + kill
  gates; annotation gaps; witnesses (grammars-предшественники + machine paradigm assets —
  WhitneyRoots, mw_roots.tsv, MWinflect, csl-inflect, vidyut, VisualDCS); five-year placement
  in W2 between the W1 foundation and W3 semantics. References the canonical `SG-WF-*`/`SG-MO-*`
  IDs, mints none (C2 stays canonical). Build green, page generated, zero broken links
  ([H634](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H634-Fable_SanskritGrammar_sangram-morphology-program_11.07.26.md), Opus 4.8 `claude-opus-4-8` — slot was minted for Fable 5, run on Opus 4.8 by explicit author decision).

## [0.3.0] - 2026-07-12
### Added
- **WSC-2027 CDSL report — deep remake** (H795, Fable 5 `claude-fable-5`):
  [`TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/`](TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/) —
  13 `.mdx` chapters remaking the WSC-2025-rejected "Report on Cologne Digital
  Sanskrit Lexicon Project" for the 20th World Sanskrit Conference (Mumbai,
  December 2027): formal register per the four Kathmandu reviews, every
  quantitative claim tied to a committed dataset, Peter Scharf's review
  incorporated (Sanskrit Library co-history, TEI, morphid coordination,
  licence status), team history updated through Jim Funderburk's June-2026
  retirement (cited to the recorded volunteer call), full bibliography +
  abbreviations appendix. Provenance and residual pre-submission items in the
  folder's [`README.mdx`](TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/README.mdx).

## [0.2.0] - 2026-07-12
### Added
- **Атлас B5 — зависимости репозиториев** (`/sangram/atlas/dependencies`, H620,
  Fable 5 `claude-fable-5`): пять видов ребер публичного interlinks-экспорта
  (feeds · consumes · vendors · produces · cites) различимы цветом **и** текстовым
  бейджем, направление и канон/копия по каждому виду, таблица всех вендоренных
  копий организации, поиск по репозиториям/активам/контрагентам, программные
  группы census через новое опциональное поле `programme_ru` на `repo`-узлах
  (контракт данных 1.0.0 → **1.1.0**, append-only), полное покрытие census
  (75 репозиториев / 67 с ребрами / 8 изолятов пунктиром), controlled-mode на
  едином маршруте (`sangram/atlas/dependencies.mdx` +
  `src/components/AtlasDependencies/`). В источнике interlinks исправлены два
  инвертированных `vendors`-ребра (vidyut); bundle пересобран, leakage = 0.
- **Атлас B3 — переиспользование готовых активов** (`/sangram/atlas/reuse`, H630,
  Fable 5 `claude-fable-5`): владелец → актив → потребитель по 18 каноническим
  семействам с ярусами прав и запретами пересоздания
  (`sangram/atlas/reuse.mdx` + `src/components/AtlasReuseView/`).
- **Все пять представлений атласа живые на едином маршруте**
  (`/sangram/atlas/unified`): wave B серии MEGABOOK × Sangram (B1–B6) закрыта —
  attention · reuse · value-chain · dependencies · provenance подключены в
  `VIEW_REGISTRY`, выбранный узел сохраняется при переключении представлений.

## [0.1.0] - 2026-07-12
### Added
- **GrammarRelations — карта связей грамматик** ([GrammarRelations/grammar-relations-map.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GrammarRelations/grammar-relations-map.mdx),
  route `/grammars/GrammarRelations/grammar-relations-map`): читательская страница о том,
  как связаны 10 оцифрованных грамматик — генеалогия учебной линии (τ из S1), проверенная
  по тексту зависимость Очерк-1978↔Кочергина-1998, линия Зализняка 1975/1978/2004 и ветви
  Гасунс/Толчельников, карта тем, трудность подачи и совместимость для студента. Новый
  скрипт [`scripts/grammar_relations_stats.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/grammar_relations_stats.py)
  (SG-H2 подтверждена: медианный сдвиг +0.142, p≈2×10⁻⁵; SG-H9 опровергнута на
  символьном прокси) + результаты в
  [`scripts/data/grammar_relations_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/grammar_relations_stats.json)
  (H786, Fable 5 `claude-fable-5`).
- **Атлас B4 — интерактивная цепочка ценности** (`/sangram/atlas/value-chain`,
  H627, Fable 5 `claude-fable-5`): три селектируемых типизированных контура
  (исследовательский · образовательный · агентный) над 7 value-ступенями и
  10 ребрами bundle, роли источник/данные/продукт/отдача/мультипликатор без
  смешения, доказуемость каждого звена ребром bundle + свидетельством,
  Mermaid-объяснение с accTitle/accDescr и табличный эквивалент
  (`sangram/atlas/value-chain.mdx` + `src/components/AtlasValueChain/`).
- **Sangram contract C2 — article TOC network** ([`sangram/toc/SANGRAM_TOC_NETWORK.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/toc/SANGRAM_TOC_NETWORK.mdx),
  route `/grammars/sangram/toc-network-c2`): append-only registry
  [`articles.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/toc/data/articles.json)
  of 93 core articles across the 7 charter domains (PH 10 · WF 11 · MO 32 · SE 15 ·
  SY 14 · DI 6 · VA 5) — stable `SG-<domain>-<NNN>` IDs, 117-edge acyclic prerequisite
  graph, DCS query sketches (6-prefix grammar), curated witnesses from the repo's 10
  grammars plus a derived Whitney-chapter coverage layer; all 33 C6 programme slots
  mapped via `c6_slots`. Generator `scripts/toc_build_pages.py` (overview + 7 domain
  pages with Mermaid prerequisite graphs) and validator `scripts/toc_validate.py`
  (17 check classes incl. H540 form-class cross-check and `--check` page sync)
  (H631, Fable 5 `claude-fable-5`).
- **Sangram editorial + i18n contract (C4, H633)**: article manifest schema
  ([sangram/editorial/data/article.schema.json](sangram/editorial/data/article.schema.json)),
  fixture, validator (`python scripts/article_validate.py --self-test`) and the
  prose contract page ([sangram/editorial/SANGRAM_EDITORIAL_I18N_CONTRACT.mdx](sangram/editorial/SANGRAM_EDITORIAL_I18N_CONTRACT.mdx)):
  RU-default/EN-translation locales, one canonical SLP1 copy per example
  (IAST/Devanagari derived via sanskrit-util), scientific/pedagogical layers,
  stable `ex:<slug>:<n>` example IDs with locus/translation/provenance,
  public⇒https / internal⇒no-URL evidence rule, leakage = 0.
- **Sangram contract C3 — corpus evidence method** ([`sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx),
  route `/grammars/sangram/corpus-evidence-method`): corpus registry (DCS primary via the
  pinned [`gasyoun/dcs-conllu`](https://github.com/gasyoun/dcs-conllu) snapshot + 5
  supplementary witnesses), rights/liveness/quality gates, the reproducible
  query→sample→validate→claim→examples cycle, quantitative-claim rules П1–П7, and the
  append-only source-defect list Д1–Д8 (H632, Fable 5 `claude-fable-5`).
- **Errata system** (`/errata` skill): every book folder carries an `errata.yml`
  structured source → generated `<Book>/ERRATA.md` + root `ERRATA.md` index via
  `scripts/build_errata.py` (`npm run errata`). Each erratum records who found it
  and when; the generator de-duplicates across errata sheets and cross-references
  the book's own CHANGELOG (`fixed_in` marks typos corrected in the digital edition).
- Errata enter two ways: transcribing a printed errata sheet, **or** an edition
  diff (`build_errata.py diff <Book> <old-ref> [<new-ref>]`) that turns changes
  between two versions of a book's text file into reviewable errata candidates —
  so books with no printed sheet (Kochergina, etc.) still accrue errata over time.
- `README.md` documenting the repo's source editions and scope.
