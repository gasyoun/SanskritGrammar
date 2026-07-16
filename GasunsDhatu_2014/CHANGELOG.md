# Changelog — GasunsDhatu_2014

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Приложение 7 — печатный лист свёрстан (третий проход)**: `APPENDIX7_PRINT_SHEET.html`
  ([`revision-2026/mw_genuine_roots_print_sheet.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/mw_genuine_roots_print_sheet.py)),
  A4 трёхколоночная вёрстка всех 750 подлинных корней MW, по образцу листов опечаток
  ([H993](https://github.com/gasyoun/Uprava/blob/main/handoffs/H993-Fable_SanskritGrammar_errata-print-sheets_15.07.26.md)).
  MG ruled **Route 2** on the H1018 scope question (the appendix page's own text argues against
  inlining the full list into the book body — the print sheet is a separate asset, book body
  unchanged) — page + footnote `[^ed2]` updated with the link.
  ([H1018](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1018-Sonnet_SanskritGrammar_m03-appendix7-typesetting_16.07.26.md), Sonnet 5 `claude-sonnet-5`)

## [0.11.0] - 2026-07-16
### Added
- **Часть II, Глава 6 «Корпусная аттестация корней» (черновик)** — третья новая глава; замыкает
  арку трёх свидетелей (Гл. 4). Новая страница [`06_glava6_korpusnaya-attestaciya.mdx`](06_glava6_korpusnaya-attestaciya.mdx)
  + план [`revision-2026/CH6_PLAN_corpus_attestation.md`](revision-2026/CH6_PLAN_corpus_attestation.md).
  Тезис: корпус — свидетель, который *подтверждает* ~2/3 словника **и** честно очерчивает свой
  потолок. Канонические числа (MWS/root_crosswalk): **590/935 (63,1 %)** аттестованы в DCS, **550
  (58,8 %)** «готовое ядро» (MW+DCS), **259** словарно-грамматических корней корпусно отсутствуют;
  продуктивность топ-50 ≈ 70 %. Пределы (ссылка на SANGRAM, не пересказ): класс gaṇa корпусно
  невосстановим (SG-MO-013, ≈ 38,9 %), претериты сливаются под `Tense=Past` (SG-MO-017), без
  акцентуации неразличимы классы I/VI и IV/пассив (A06/A32). Ждёт визы автора.
### Changed
- **Гл. 4 — числа покрытия приведены к каноническим** (при сверке для Гл. 6): было 497/930 (53,4 %)
  по `roots.csv`, стало **550/935 (58,8 %)** по MWS/root_crosswalk (809 MW, 590 DCS) — устранено
  расхождение с общекнижным 590/935; сноска `[^ed4a]` обновлена.
  ([H1027](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1027-Opus_SanskritGrammar_m03-ch6-corpus-attestation_16.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.10.0] - 2026-07-16
### Added
- **Часть II, Глава 5 «Дхатупатха и паниниевская традиция как данные» (черновик)** — вторая новая
  глава. Новая страница [`05_glava5_dhatupatha-panini.mdx`](05_glava5_dhatupatha-panini.mdx) + план
  [`revision-2026/CH5_PLAN_dhatupatha_panini.md`](revision-2026/CH5_PLAN_dhatupatha_panini.md).
  Тезис: туземная традиция впервые становится **машиночитаемыми данными**. Проверенные скриптом
  опоры: цифровая дхатупатха vidyut (**2 259 дхату**, адресация `gaṇa.sūtra`) + резолвер сутр
  Аштадхьяи. **Аудит пальсуле-центризма** конкорданса (отзыв С. А. Крылова): `añc` — 5 дхату
  семейства (4añc восстановим, упрёк подтверждён); `and` — только-Пальсуле (согласуется); `ast` —
  **есть** в паниниевской дхатупатхе (уточняет отзыв). Честный предел: наивный it-stripped джойн
  454/930, несовпавшие = √i/√ah/√an (аблаут, не потеря) → нужна нормализация ступеней; полный
  список «потерянных корней» — задел статьи-компаньона A39. Деривация (A35) и микроструктура (A04)
  — ссылка, не пересказ (антисаламная граница с M01). Ждёт визы автора.
  ([H1023](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1023-Opus_SanskritGrammar_m03-ch5-dhatupatha-panini_16.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.9.0] - 2026-07-16
### Added
- **Часть II начата — Глава 4 «Кросс-уок и омонимия корней» (черновик)** — первая новая глава
  «Корня в цифровую эпоху», написана из готовых данных 2026 г. (не rework). Новая страница
  [`04_glava4_kross-uok-omonimiya.mdx`](04_glava4_kross-uok-omonimiya.mdx) + план
  [`revision-2026/CH4_PLAN_crosswalk_homonymy.md`](revision-2026/CH4_PLAN_crosswalk_homonymy.md).
  Тезис: корень проверяют **три свидетеля** — грамматика, словарь, корпус. Проверенные скриптом
  числа: **497/930 (53,4 %)** корней Уитни имеют и MW-статью, и корпусную аттестацию; класс
  презенса согласуется **376 : 26** (конкорданс MW↔Уитни, актив MWS/SANGRAM — цитируется, не
  выводится); омонимия расходится по источникам (Пальсуле 933 · Уитни 67 · EWA 50 · Юэ 38 ·
  Эдгрен 18), 143 помечены, автоматическое токенное расщепление упирается в потолок (≈5/38).
  Пределы поданы как результат. Пишется в связке со статьёй-компаньоном A39; ждёт визы автора.
  ([H1019](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1019-Opus_SanskritGrammar_m03-ch4-crosswalk-homonymy_16.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.8.1] - 2026-07-16
### Changed
- **Приложение 7 — обогащение подлинных корней MW** (второй проход). К каждому корню
  присоединены **корпусная частота/ранг DCS** ([`roots.csv`](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/roots.csv))
  и **число словарей-источников** ([`root_oracle.tsv`](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/etymology_stats/root_oracle.tsv))
  через генератор `mw_genuine_roots.py` (join по `root_iast`). Кросс-таб по 704 различным
  подлинным корням: **482 (68 %)** засвидетельствованы в DCS, **345** согласованы ≥4 словарями;
  их пересечение -- **ядро из 294 корней** (подлинные + корпусно аттестованные + межсловарно
  согласованные), на другом полюсе -- **хвост из 101** (подлинные по MW, но корпусно
  неаттестованные и известные одному источнику). «Подлинность» градуируется тремя свидетелями.
  Выжимка на странице «Приложения издания 2026» переработана в обогащённую (частота · словари);
  TSV получил колонки `dcs_freq`/`dcs_rank`/`n_dicts`. `ERRATA.md` без изменения счёта.
  ([H1006](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1006-Opus_SanskritGrammar_m03-appendix-mw-genuine-roots_16.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.8.0] - 2026-07-16
### Added
- **Приложение 7 «Подлинные корни словаря Монье-Уильямса»** — начато по визе автора (заметка
  §1.5, 16-07-2026). Разделение подлинных/вторичных корней взято из **собственной разметки**
  кёльнской цифровой MW (колонка `verb_type` таблицы `mw_roots.tsv`): **750 подлинных**
  (`genuineroot`) против **1 363 вторичных** (`root`, — деноминативы, каузативные основы,
  класс-0) из 2 113 статей; сумма совпадает с §1.2/§2.3. На страницу «Приложения издания 2026»
  добавлена секция с выжимкой (★-помета) и ссылками; сгенерированы полный размеченный
  [`mw_genuine_roots.tsv`](revision-2026/mw_genuine_roots.tsv) (2 113 строк, флаг `genuine`),
  печатный компактный список 750 подлинных [`mw_genuine_roots_list.md`](revision-2026/mw_genuine_roots_list.md)
  и воспроизводимый генератор [`mw_genuine_roots.py`](revision-2026/mw_genuine_roots.py).
  ([H1006](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1006-Opus_SanskritGrammar_m03-appendix-mw-genuine-roots_16.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.7.0] - 2026-07-16
### Changed
- **Виза автора на четыре вставки данных Гл. 1 (5/5 approve) + уточнения по заметкам** (визовый
  лист `sanskritgrammar-m03-ch1-inserts-visa`, MG 16-07-2026). Все четыре вставки (Выводы,
  §1.2/§1.3/§1.5) и снятие дубля §1.4 одобрены; по авторским заметкам внесено:
  - **V1 (Выводы):** дефективность (429) сосуществует с полной парадигмой (424) почти на равных
    («не исключение, как подсказывало бы слово „дефект“»); уточнено, что 105 корней без пометы
    *seṭ/aniṭ* в зализняковской колонке всё же классифицированы в «Талмуде».
  - **§1.2:** «спросить» → «задать вопрос»; вплетена **продуктивность корней** — по частотам DCS
    первые ~50 корней дают около 70 % из 827 тыс. словоупотреблений, свыше 200 корней Уитни не
    засвидетельствованы (источник [`crosswalk/roots.csv`](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/roots.csv), проверено скриптом).
  - **§1.3:** добавлено, что «синхрония» системы Панини **пандиахронична** («над временем»).
  - **§1.5:** формулировка уточнена — индийская традиция и европейская компаративистика разделены
    более чем двумя тысячелетиями (не единое суждение); полный список ~750 подлинных корней MW с
    графической пометой — записан как задел для Приложения.
  Сноски `[^ed1d]/[^ed12a]/[^ed13a]/[^ed15a]` помечены «одобрено автором 16-07-2026». `ERRATA.md`
  перегенерирован (83 записи, 19 fixed).
  ([H1002](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1002-Opus_SanskritGrammar_m03-ch1-inserts-visa-apply_16.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.6.0] - 2026-07-15
### Changed
- **Гл. 1 rework, второй проход — слияния данных 2026 в §1.2/§1.3/§1.5** (метод пилота Гл. 2).
  По одному абзацу с провенансом добавлено в каждую секцию, все числа **проверены скриптом** по
  реальным файлам:
  - **§1.2 «Понятие *dhātu*»** (`[^ed12a]`): эмпирическая проверяемость понятия — MW 2 113
    корневых статей (~750 подлинных); 590/935 (63,1 %) корней Уитни засвидетельствованы в DCS;
    *dhātu* ≠ европейский «корень» уже по объёму.
  - **§1.3 «Роль корня в системе»** (`[^ed13a]`): количественная мера дефективности —
    полноизменяемость 429 дефективных / 424 полноизменяемых / 22 колеблющихся (876 корней,
    `polnoizm_1978`).
  - **§1.5 «Первичные и вторичные корни»** (`[^ed15a]`): эмпирическая градация первичности —
    сводный `root_oracle` (3 036 корней, 8 словарей): 436 корней с согласием ≥4 источников
    против 1 847 в единственном; первичность как степень межисточникового согласия.
  Абзацы-вставки ждут авторской визы пакетом. `ERRATA.md` перегенерирован (82 записи, 18 fixed);
  карта — [`revision-2026/CH1_DATA_MAP.md`](revision-2026/CH1_DATA_MAP.md). Осталось по Гл. 1:
  §1.1/§1.4 — человек-редактор (стиль).
  ([H992](https://github.com/gasyoun/Uprava/blob/main/handoffs/H992-Opus_SanskritGrammar_m03-ch1-prose-rework_15.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.5.0] - 2026-07-15
### Changed
- **Прозаический rework новой Гл. 1 «Понятие глагольного корня» — первый проход** (метод пилота
  Гл. 2). «Выводы по первой главе» переработаны: концептуальные положения сохранены, добавлен
  **измеримый слой** — покорневая сверка 876 глагольных корней даёт seṭ/aniṭ (308 *seṭ* : 287
  *veṭ* : 176 *aniṭ*) и полноизменяемость (429 дефективных / 424 полноизменяемых / 22
  колеблющихся); «дефективность» традиции стала исчисляемым параметром реестра (сноска `[^ed1d]`,
  источник — [`TolchelnikovTalmud_2026/…/morphoclass_crosswalk_1975_2014_2026.csv`](TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv), числа проверены скриптом).
  Карта данных для дальнейших проходов — [`revision-2026/CH1_DATA_MAP.md`](revision-2026/CH1_DATA_MAP.md).
### Fixed
- **Снят дубль-абзац в §1.4** (о синтетическом подходе Панини/Яске стоял дважды подряд —
  дефект конверсии 2014 г.). `ERRATA.md` перегенерирован (79 записей, 15 fixed).
  ([H992](https://github.com/gasyoun/Uprava/blob/main/handoffs/H992-Opus_SanskritGrammar_m03-ch1-prose-rework_15.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.4.0] - 2026-07-15
### Changed
- **Рекомпоновка границы Глав 1/2 по трём вопросам книги** (MG, Вариант A, 15-07-2026) —
  структурная перестройка Части I. Прежние Гл. 1 «Структура древнеиндийского перечня корней»
  и Гл. 2 «Понятие глагольного корня и количество корней» смешивали два вопроса; теперь:
  **Гл. 1 «Понятие глагольного корня»** (что такое корень — §1.1 зарождение анализа, §1.2
  понятие *dhātu*, §1.3 роль корня, §1.4 формальные показатели, §1.5 первичные/вторичные) и
  **Гл. 2 «Количество корней и структура перечня»** (сколько корней — §2.1 устройство
  dhātupāṭha, §2.2 цитирование, §2.3 количество, §2.4 фоностатистика, §2.5 распределение
  рядов; завизированный фоностат-пилот сохранён). Секции перенесены **без изменения
  содержания** (проверено: 0 потерянных абзацев), перенумерованы; §-кросс-ссылки (24 шт.) и
  оглавление обновлены; Выводы обеих глав перераспределены по вопросам; провенанс — сноски
  `[^edrecomp1]`/`[^edrecomp2]`/`[^ed1d]`. `errata.yml`: §-якоря обновлены + запись о
  рекомпоновке; `ERRATA.md` перегенерирован (77 записей, 13 fixed). План:
  [`revision-2026/CH1_CH2_RECOMPOSITION_SPEC.md`](revision-2026/CH1_CH2_RECOMPOSITION_SPEC.md).
  Прозаический rework новой Гл. 1 по методу пилота Гл. 2 — следующий шаг.
  ([H991](https://github.com/gasyoun/Uprava/blob/main/handoffs/H991-Opus_SanskritGrammar_m03-ch1-ch2-recompose-execute_15.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.3.0] - 2026-07-15
### Changed
- **Визовый пакет Фазы 0 пройден автором (14/14 approve) и сведён в текст/errata/PROPOSALS**
  (MG, 15-07-2026) — единственный оставшийся гейт книги (BOOK_PLAN §7/§9) закрыт. Положения
  П1/П4/П7/П9/П10 и блок «Верификация положений» переведены из «черновик; финал за автором»
  в «одобрено автором»; таксономия библиографии C13 подтверждена. **5 errata «Совет
  филологов / Зализняк-9» (E1–E5) внесены в печатный `.mdx`** (ранее только предложены):
  санскритские примеры вместо русских (E1), явная отсылка к Л. Рену с пояснением расхождения
  (E2, вариант автора), определения вместо риторических вопросов (E3), нейтрализация
  публицистического регистра (E4), полное имя «Хлодвиг Верба» при **истинном** первом
  упоминании L123 — исправлен якорь замечания (E5). Содержательная виза-добавление автора:
  сноска о типологической сопоставимости индо-арабского понятия корня (устное сообщение
  А. А. Зализняка, `[^edp10b]`). `ERRATA.md` перегенерирован (76 записей, 12 fixed).
### Added
- **Q4 закрыт запиской [`revision-2026/A39_SANGRAM_SCOPE_MEMO.md`](revision-2026/A39_SANGRAM_SCOPE_MEMO.md)**
  (+ `.meta.md`): решение автора — рефрейм статьи-компаньона A39 через SANGRAM (что уже
  сделано и цитируется: SG-MO-013, SG-MO-017, два crosswalk-CSV, метод C3, типология A60;
  vs. собственный вклад A39 — покорневой трёхсторонний синтез + книжная рамка).
- **Старт Фазы 1:** памятка [`revision-2026/CH1_REWORK_MEMO.md`](revision-2026/CH1_REWORK_MEMO.md)
  — карта переработки Гл. 1, узлы слияния 2026-данных, развилка заглавия (@DECIDE).
  ([H986](https://github.com/gasyoun/Uprava/blob/main/handoffs/H986-Opus_SanskritGrammar_m03-phase0-visa-apply_15.07.26.md), Opus 4.8 `claude-opus-4-8[1m]`.)

## [0.2.2] - 2026-07-13
### Changed
- **Титульная формула 2-го издания решена: «2-е изд., перераб. и доп.»** (MG, 13-07-2026).
  Закрывает развилку §9 п.3 плана ([`revision-2026/BOOK_PLAN.md`](revision-2026/BOOK_PLAN.md))
  против «изд. 2-е, существенно расширенное»; совпадает с Р9 и заглавием M03 в реестре;
  финальная сверка с серийными нормами «Нестор-Истории» — при вёрстке (Фаза 4). Заодно
  приоритет M03 поднят до «активно сейчас»: Фаза 0 (визовый пакет) — единственный
  оставшийся гейт книги, собирается в один review-sheet (H856); контакт с издательством
  отложен до Фазы 3. ([PR #162](https://github.com/gasyoun/SanskritGrammar/pull/162), Opus 4.8 `claude-opus-4-8`.)

## [0.2.1] - 2026-07-13
### Changed
- **Издательство M03 решено: «Нестор-История»** (MG, 13-07-2026). Закрывает открытый
  `@DECIDE` §6 плана 2-го издания
  ([`revision-2026/BOOK_PLAN.md`](revision-2026/BOOK_PLAN.md)): ЯСК и «Наука» сняты с
  рассмотрения, гриф ИЯз РАН уже был закрыт 10-07-2026. Р6/§6/§7 Фаза 3/§9 обновлены;
  к Фазе 3 остается только операционное (заявка + договор + рецензенты).
  ([H847](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H847-Opus_SanskritGrammar_m03-publisher-nestor-istoria-decided_13.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.2.0] - 2026-07-08
### Added
- **2026 print-edition execution (H328).** Executed the
  [`revision-2026/IMPROVEMENT_ROADMAP.md`](revision-2026/IMPROVEMENT_ROADMAP.md)
  per the four author decisions of 07-07-2026: положения re-composed
  (П1/П4 redrafted, П7/П9/П10 demoted to illustrative paragraphs with
  editorial footnotes, П8→П7); Заключение gained a per-положение
  «Верификация положений» draft block (C2); new «Цифровое послесловие 2026»
  section (A39 continuation + «будущая работа → готовый ресурс» map);
  new «Приложения издания 2026» page (6-appendix composition map + Прил. 3
  concordance excerpt over WhitneyRoots/kosha data-v0.1.0); Прил. 2 homonym
  table manually reconstructed from the source `.docx` (rows = group sizes,
  columns = Palsule/EWA); print-layer number fixes (root_oracle 10→8
  dictionaries; 180 176 lemmas re-attributed to VisualDCS; Табл. 2/3 caption;
  §2.6 dataset-change footnote; §3.3.3 L9 gap closed — 933/25,3 %/EWA 50);
  phone replaced with email+ORCID in both article headers (Р4); superseded
  duplicate «Распространение рядов согласных» page removed; 14 new
  `errata.yml` entries (`found_by: H328-review`). PALSULE_AUDIT gained the
  measured step-3 negative result (naive it-stripped join 454/930 — unusable
  as a candidates list without ablaut normalization).

## [0.1.0] - 2026-07-07
### Added
- **2026 print-edition prep (H246).** Conversion cleanup across the
  dissertation + 4 article appendices (~1200 unescapes, typos
  Emeneau/Morgenroth/«Lihusina»→Edgren, Latin-C fixes, `image1.wmf`→PNG, 8
  empty Pandoc headings removed); §2.5/2.6 renumbered (L8); number
  unification with editorial footnotes (Palsule 933/3690, EWA 50, АВ
  coefficient 1.33 — recomputed from the tables' own frequencies, L9); Гл. 2
  title fixed per Волошина (C6); корнеслов/морфемарий defined at first use
  (C5) + морфонология⊃морфонемика note (L10); bibliography split into
  RU/foreign blocks (C13, mechanical part); Гумбольдт ref restored, Потебня
  flagged (C4). **Табл. 5 replaced**: χ² p-values → varga shares by epoch +
  Cramér's V = 0.037 (DCS 2026-03-05, reproducible via
  `revision-2026/varga_shares.py`) per MG Q3; the «Распределение рядов
  согласных» article brought to standalone-appendix form per MG Q2
  (аннотация/method/shares/вывод; 2014 p-table kept as historical record);
  «Список файлов» reduced to an annotated supplementary note with dead-link
  markers. New «Состояние вопроса на 2026 год» section (590/935 Whitney
  roots attested in DCS; digital crosswalks; vidyut dhātupāṭha; kosha
  data-v0.1.0). `errata.yml` seeded with 51 entries
  (`found_by: H246-review`); `revision-2026/` working notes: П1/П4/П7/П9/П10
  draft rewrites (await author sign-off) + Palsule-vs-vidyut audit (`4añc`
  confirmed recoverable — 5 añc-family dhātus in the Paninian dhātupāṭha;
  `ast` present too, refining Крылов's 2014 remark).
- RWS style report (`feat(gasuns-dhatu): add RWS style report`).
- Initial mint: dissertation + article appendices, converted to `.mdx` via
  the `/docx-to-md` skill.
