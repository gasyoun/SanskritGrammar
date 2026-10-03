_Created: 01-10-2026 · Last updated: 03-10-2026_

# План: поурочный конкорданс Бюлера — урок I–XLVIII × все источники сайта

**Задача (MG, 01-10-2026):** связать уроки [Бюлер-1923](https://gasyoun.github.io/SanskritGrammar/grammars/BuhlerLeitfaden_1923/Buhler_Unicode/) поурочно, 1 урок за раз, со всеми остальными источниками сайта; сделать конкорданс.

**Провенанс:** план собран OxAlpha (`opencode/z-ai/glm-5.3-flash`) 01-10-2026 по `/grillme` (Phase 0 homework по эзтейту; карточки раунда 1 D1–D4 проголосованы MG в сессии 01-10-2026, D5–D16 приняты командой «go» — окно вето до batch-минта, см. § «Лист решений»). Хендофф пилота: [H5595](https://github.com/gasyoun/Uprava/blob/main/handoffs/H5595-OxAlpha_SanskritGrammar_buhler-lesson-concordance-pilot_01.10.26.md).

## Prior art — что уже стоит (не дублируем, индексируем)

1. [Concordance/catalog.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx) — 124 кластера общих предложений Бюлер↔Кнауэр↔Кочергина, **уже с колонкой урока Бюлера** (римские I–XLVIII); генерируется из [scripts/data/matches.json](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/matches.json).
2. [SubjectConcordance/](https://github.com/gasyoun/SanskritGrammar/blob/main/SubjectConcordance/README.md) — 41 тематическая категория ↔ §-диапазоны Уитни (спайн из [WhitneyRoots form_section_concordance.json](https://github.com/gasyoun/WhitneyRoots/blob/main/src/form_section_concordance.json)); typed-link TSV в канонической форме `TYPE_D_RECORD_FIELDS` ([TYPED_LINK_ID_GRAMMAR.md](https://github.com/gasyoun/Uprava/blob/main/TYPED_LINK_ID_GRAMMAR.md) §4b), lint — [kosha typed_link_lint.py](https://github.com/gasyoun/kosha/blob/main/scripts/typed_link_lint.py); в kosha-манифесте отложен до Q2.1 (прецедент D2b, H540).
3. [BuhlerLeitfaden_1923/claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml) — HB-1…403, вердикты против DCS+Уитни (381 TRUE · 7 OVERSTATED · 8 FALSE · 7 UNTESTABLE · 24 M.G. footnotes; H797).
4. [corpus_layer.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/corpus_layer/corpus_layer.tsv) — леммы поурочно (колонка `lesson`, римские) с DCS-частотами и примерами.
5. [WHITNEY_CONCORDANCE_SANGRAM_KOCHERGINA_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/WHITNEY_CONCORDANCE_SANGRAM_KOCHERGINA_2026.md) — сетка 436 утверждений × 4 свидетеля (Б-1923, З-1975/1978/2004), AGREE/DISAGREE/SILENT.
6. [GrammarRelations/grammar-relations-map.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GrammarRelations/grammar-relations-map.mdx) — карта связей 10 книг + τ-секвенция ([S1](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md)) + SG-H2/H9.
7. [ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) — Q2.1 unified concordance (куда этот датасет встанет).

**Чего нет:** поурочного тематического сшивания «урок Бюлера ↔ каждый источник». Это ядро нового конкорданса.

## Архитектура — решения D1–D16

Рекомендации приняты **для пилота**; после пилота MG правит лист решений до batch-минта остальных 45 уроков.

| # | Решение | Рекомендация (для пилота) | Если MG скажет «нет» |
|---|---|---|---|
| D1 ✅ голос | Потребитель | Оба слоя: TSV + генерируемая страница (паттерн SubjectConcordance) | — |
| D2 ✅ голос, расширен | Зерно связи | Урок + тема (2–5 тем/урок) **плюс лемма-слой**: pointer-колонка покрытия лемм урока по источникам (из [corpus_layer.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/corpus_layer/corpus_layer.tsv) + [GasunsDhatu_2014](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/)) — чтобы мерить полноту каждой грамматики. Пилот отвечает гипотезу MG: «списки исключений — много у Бюлера, нет у Зализняка-1978, всегда у Уитни?» — per-topic exception-coverage заметки в topic sidecar (цитаты локусов) | Урок целиком — 48 строк, грубо; тема+claim+lemma — дублирует HB/corpus_layer |
| D3 ✅ голос | Типы связей | Тематические + указатели на существующие регистры (HB-*, C-кластеры, corpus_layer) | — |
| D4 ✅ голос | Источники | Матрица применимости (§ ниже) | — |
| D5 ✅ «go» | Anchor-типы | Один spec-PR в [TYPED_LINK_ID_GRAMMAR.md](https://github.com/gasyoun/Uprava/blob/main/TYPED_LINK_ID_GRAMMAR.md): `buhler-lesson:<римская N>` + конвенции target-локусов | Регистрировать по ходу — lint догоняет задним числом; свободные строки — вне спеки |
| D6 ✅ «go» | Формат | TSV `typed_link_buhler_lessons.tsv`, 10 колонок как в thematic; лемма/exception-заметки — в topic sidecar, TSV остаётся lint-чистым | YAML на урок (48 файлов) или SQLite — вне lint-контура |
| D7 ✅ «go» | Где живёт | Новый каталог `LessonConcordance/` рядом с `SubjectConcordance/` (README + generated catalog.mdx + TSV) | Внутри `Concordance/` — студенты вместе, но смешение жанров; внутри BuhlerLeitfaden — кросс-источниковый продукт заперт в источнике |
| D8 ✅ «go» | Локус урока | Заголовки `# УРОК N.` в [Buhler_Unicode.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/Buhler_Unicode.mdx); кривые делимитеры нормализует парсер | Вставка явных якорей трогает текст Лихушиной; только номер — нет цитируемого локуса |
| D9 ✅ «go» | Транспорт | Пилот-хендофф [H5595](https://github.com/gasyoun/Uprava/blob/main/handoffs/H5595-OxAlpha_SanskritGrammar_buhler-lesson-concordance-pilot_01.10.26.md) → ревью формата → `--batch`-минт 45 → дренаж | 48 хендоффов сразу — spec-чёрн × 45 при переделке; один ledger-хендофф — риск 30-мин потолка автономии |
| D10 ✅ «go» | Пилот | Урок I (глаголы I класса + sandhi: максимум связей, reuse-кластеры и corpus_layer уже под ним) | XVIII (плотный corpus_layer) или XX–XXIV (зона Уитни-DISAGREE) |
| D11 ✅ «go» | Курация | Посев кандидатов из регистров + агент-куратор за проход, `match_method=curated`, confidence градуированный 0.7–0.97 с evidence | Чисто computed — шум; чисто руками MG — не масштабируется на 48 |
| D12 ✅ «go» | QA урока | `typed_link_lint` 0-error + спот-чек DeepSeek-верификатором (пре-авторизован MG 01-10-2026) + deploy same pass | QA в конце — систематическая ошибка × 48 |
| D13 ✅ «go» | Словарь тем | 41 категория form_section_concordance + расширяемые ключи (синтаксис, pronouns и т.п.), versioned | Свободные строки — дрейф словаря; свой словарь с нуля — теряется механический mapping на Уитни |
| D14 ✅ «go» | Язык страницы | RU (язык сайта), ключи/IDs EN в TSV | Двуязычие — дороже; EN — разнобой с сайтом |
| D15 ✅ «go» | kosha-манифест | Не регистрировать до Q2.1 unified release (прецедент D2b) | Регистрация сразу — двойная правка манифеста |
| D16 ✅ «go» | DoD урока | Список из 7 пунктов (§ ниже) | Короче — риск недобора; длиннее — проход перестаёт влезать в дренажный слот |

## Формат данных

TSV `LessonConcordance/typed_link_buhler_lessons.tsv`, колонки как в [SubjectConcordance/typed_link_thematic.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/SubjectConcordance/typed_link_thematic.tsv): `anchor_type · anchor_id · anchor_key_slp1 · target_locus · link_type · source_dataset · match_method · confidence · evidence_count · date`. Иллюстративные строки (локусы финализирует пилот):

```
anchor_type	anchor_id	anchor_key_slp1	target_locus	link_type	source_dataset	match_method	confidence	evidence_count	date
buhler-lesson	buhler-lesson:I		subject:sanskritgrammar:present_a	thematic	SanskritGrammar/LessonConcordance/typed_link_buhler_lessons.tsv	curated	0.97	3	01-10-2026
buhler-lesson	buhler-lesson:I		whitney-sec:319-335	thematic	SanskritGrammar/LessonConcordance/typed_link_buhler_lessons.tsv	curated	0.9		01-10-2026
buhler-lesson	buhler-lesson:I		kochergina-lesson:5	thematic	SanskritGrammar/LessonConcordance/typed_link_buhler_lessons.tsv	curated	0.85	1	01-10-2026
buhler-lesson	buhler-lesson:I		knauer-fraza:Nr.4	thematic	SanskritGrammar/LessonConcordance/typed_link_buhler_lessons.tsv	curated	0.9	2	01-10-2026
```

Одна строка = одна связь; кластер reuse-предложений урока и его HB-утверждения попадают в колонку-указатель генерируемой страницы (`evidence_count` — число задетых регистровых строк), а не в отдельные TSV-строки.

## Матрица применимости источников

| Источник | target_locus-конвенция | Применимость |
|---|---|---|
| [WhitneyGrammar_1889](https://github.com/gasyoun/SanskritGrammar/blob/main/WhitneyGrammar_1889/00_index.mdx) | `whitney-sec:LO-HI` (якоря `[**§N**]`) | все 48 уроков |
| [KocherginaUchebnik_1998](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/Kochergina_unicode.mdx) | `kochergina-lesson:N` (делимитер `Занятие N` — отдельные строки, не заголовки: строка 229+) | все |
| [KnauerFrazy_1908](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/Frazy-Knauer-03.05.2023.mdx) | `knauer-fraza:Nr.N` (заголовки `# Nr. N (§§ …)`) | все |
| [ZalizniakOcherk_1978](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/) | `z-ocherk:§N` | все; witness-вердикты уже в WHITNEY_CONCORDANCE v2 |
| [ZalizniakMorphology_1975](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/) | `z-morpho:<класс/quantifier>` | глагольные уроки (I–III, VII–VIII, X–XI, XIV–XVIII, XXVIII+) |
| [ZalizniakKonspekt_2004](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/) | `z-konspekt:§N` | все |
| Sangram-статьи | `sangram-article:<slug>` | все, по теме урока |
| [ApteSyntax_1885](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/) / [SpeyerSyntax_1886](https://github.com/gasyoun/SanskritGrammar/blob/main/SpeyerSyntax_1886/) | `apte:§N` / `speyer:§N` | синтаксические темы: IX (префиксы), X (пассив), XVIII+ (каузатив), порядок слов |
| [GasunsDhatu_2014](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/) | `dhatu:<root-iast>` | уроки со списками корней (морфонологическая запись — прямое продолжение HB) |
| [TolchelnikovTalmud_2026](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/) | `talmud:<локус>` | root-morphoclass арбитр (роли арбитров по шапке claims.yml) |
| BibliothecaSanscritica (Фриш) | `frish:<локус>` | где упражнение Бюлера имеет хрестоматийный источник |

## Операционный план

1. **Пилот (минтирован, OxAlpha):** урок I — spec-PR anchor-типов в TYPED_LINK_ID_GRAMMAR.md, `LessonConcordance/` каркас (TSV + генератор `build_lesson_concordance.py` по образцу [build_subject_concordance.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_subject_concordance.py)), строки урока I, DoD целиком.
2. **Ревью MG:** лист решений D1–D16 (виза/вето по каждому), смотрим пилотную страницу.
3. **Batch:** 45 уроков `--batch`-минтом (правило: `--batch` при N≥2 известных минтах), дренаж ~4.6/ч (замер pass 1, 01-10-2026) ≈ 10 ч; косые уроки (V с жирным делимитером, 43–47 без рус-упражнений) — в spec.

## Definition of Done одного урока

1. TSV-строки по матрице применимости (урок+тема), посев из claims.yml / corpus_layer / catalog.mdx.
2. Регенерация `catalog.mdx` генератором (не руками).
3. `typed_link_lint.py` — 0 ошибок.
4. Спот-чек парным верификатором (DeepSeek, пре-авторизован 01-10-2026).
5. Deploy same pass (github-pages).
6. Строка в changelog_queue/.
7. В хендоффе: закрытие с elapsed и changed/unchanged/checks/risks.

QA-инструменты урока (wiring H5790, 03-10-2026): где урок опирается на рукописную таблицу sandhi-правил — аудиться через [`/sandhi-gold-audit`](https://github.com/gasyoun/claude-config/blob/main/commands/sandhi-gold-audit.md) (malformed-строки, corpus-unattested правила, пробелы покрытия), контраст регистров «урок vs corpus_layer» — через [`/sandhi-diff`](https://github.com/gasyoun/claude-config/blob/main/commands/sandhi-diff.md) (различающие junction-правила двух корпусов); иллюстративные блоки длинных компаундов на странице урока — [`/klammerdiagramm`](https://github.com/gasyoun/claude-config/blob/main/commands/klammerdiagramm.md) (SVG-скобочная схема) + [`/klammeruebersetzung`](https://github.com/gasyoun/claude-config/blob/main/commands/klammeruebersetzung.md) (вплетение перевода слово-в-слово).

## Лист решений MG — да/нет по D1–D16

**Статус 02-10-2026: ВИЗА ПОЛУЧЕНА** — D1–D16 утверждены МГ («виза D1–D16 - yes», чат 02-10-2026); вето-окно закрыто. **Batch-минт исполнен тем же проходом:** H5653–H5699 (уроки II–XLVIII, 47 хендоффов — в плане стояло «45», арифметика 48−1 даёт 47; минт исходит из фактического числа) + H5700 (остаток-минт BuhlerClaims, E9); acceptance/evidence заполнены тем же проходом. Дренаж: launchd-очередь / day boost `drain_night_launch.py run --bucket handoffs`. До batch: по каждому D — «нет» = правится spec, пилотная страница пересобирается (дёшево на 1 уроке, дорого на 45). Ключевые развилки, где «нет» дороже всего: **D2** (зерно — переверстка всей TSV), **D4** (матрица — ±40 % строк), **D7** (место — перенос каталога), **D9** (транспорт — форма 45 хендоффов). Остальные локально дешёвые.

## Риски

- **Делимитеры уроков неровные:** I–IV, VI+ — `# УРОК N.`, V — `**Урок V.**` (жирным, строка 650); 43–47 без русско-санскритских упражнений; парсер должен вести нормализованный реестр уроков, не доверять одному паттерну.
- **41 категория не покрывает синтаксис и фонетику** — расширение словаря D13 версионируется, а не молча растёт.
- **claims.yml не поурочный** (упоминания lesson единичны) — посеву нужен locus→урок маппинг; это же даст «урок × HB» указатели.
- **Kochergina `Занятие N` не заголовки** — парсинг по строкам, тест на делимитер.
- **Апте/Speyer §-якоря** в их MDX не проверены на устойчивость — пилот фиксирует конвенцию, batch переиспользует.

## Адденда 02-10-2026: перелинковка (решения E1–E9, /grillme × 2 раунда)

Ревью пилотной страницы МГ 02-10-2026 («в Chrome не увидел подсветку», «перелинковки недостаточно»).

| # | Решение | Принято |
|---|---|---|
| E1 | Подсветка глубоких ссылок | **JS-фолбэк + натив**: сайт — SPA, браузер не выполняет `#:~:text=` при клиентских переходах; `static/js/spotlight.js` (подключён через `scripts:`) сам находит фразу, рисует `<mark class="sg-spotlight">`, скроллит; нативный фрагмент остаётся для прямых открытий/новых вкладок |
| E2 | Цвет подсветки | Янтарный `#fff3ad` |
| E3 | Обратные ссылки в источниках | Да, **оба слоя**: SSR-оверлей `<LessonBacklinks/>` (паттерн CLAIMS_OVERLAY) в 6 книгах + клиент-скрипт как страховка |
| E4 | Положение бэклинка | Низ страницы источника, серым и мельче (правило тех-плашек) |
| E5 | Регистры с страницы конкорданса | Все кликабельны: HB-утверждения → claims.yml GitHub `#L`-якоря; witness-вердикты → WHITNEY_CONCORDANCE; лемма-слой → crosswalk CSV; reuse-кластеры → Concordance (0 на уроке I — указано честно) |
| E6 | Связка с GrammarRelations | Двусторонняя: §11 в карте ↔ ссылка из интро конкорданса |
| E7 | Навигация | Темы урока: строка «темы 1/N» с подсветкой текущей; уроки: строка «Уроки: I — остальные по мере batch» |
| E8 | Глубина | Каркас на 48 уроков (map/компоненты), данные — урок I; batch наполняет |
| E9 | Транскрипция | Эта адденда + changelog_queue; **остаток-минт: оверлей-страница BuhlerClaims (403 HB-утверждения по образцу KocherginaClaims) — отдельным хендоффом после batch** |


## Адденда 02-10-2026 (II): точность spot-фраз (решения E10–E13, /grillme)

Ревью МГ: «выделен номер параграфа, а не конкретное релевантное место».

| # | Решение | Принято |
|---|---|---|
| E10 | Стандарт «релевантного места» | **Фраза-утверждение**: точная непрерывная цитата из источника, несущая релевантную мысль (Очерк §31 → «Правила сандхи разбиты ниже на разделы», §114–121 → «Различаются тематическое и атематическое спряжения», Кнауэр Nr.1 → само упражнение «narān rakṣanti», а не примечание). Если локус — целый §, цитируется первое предложение сути |
| E11 | Хранение | `topics.yml`, поле `spots:` под темой (target_locus → фраза) — данные, не код; фраза = локус-цитата, проходит DeepSeek-спот-чек |
| E12 | Валидация | На build: генератор проверяет каждую локальную фразу против файла источника и валит сборку на дрейфе (уже поймал: «ṛṣir duḥkhāt» разорвана сноской ^1^ — заменена на «putraṁ rakṣati»); внешние (Wikisource, talmud-CSV) не валидируются |
| E13 | Объём | Все 12 строк пересмотрены: 9 локальных — фразы-утверждения; 3 whitney-строки — якоря заголовков § на Wikisource (§ — юнит гранулярности, внешняя валидация невозможна); talmud — CSV-файл (страницы нет) |


_Гасунс_
