### Changed
- **Поурочный конкорданс Бюлера — урок VI приземлён (H5657, OxAlpha, 05-10-2026).** Тема урока — морфонология основ IV класса (īv-удлинение dīv→dīvya; корневые i/u перед группой на r/v; a-удлинение kram/tam/dam/mad/śam/śram/bhram), ср. р. на u (madhu) и сандхи конечного n (Buhler_Unicode.mdx 789–923). 4 темы: present-class-iv, u-stems, n-sandhi, lesson-roots (лемма-слой). 15 новых TSV-строк (75 всего): Уитни §§761–765 (ya-класс: §763 am-корни + §765 īv-корни), §§335–344 (i/u-основы, §344 = разрешение Бюлера §2б), §§202–208 (n-сандхи), Очерк §118/§84/§43, Кочергина Занятие XV/XIII/X, Кнауэр Nr.10/Nr.2, sangram-article:thematic-present, dhatu-glava7, talmud-crosswalk. 11 фраз-утверждений в spots (E10), build-валидация 51/51 local OK.
- **Вердикты об исключениях:** present-class-iv — CONFIRMED (у всех четырёх свидетелей: Уитни §763/765 оговорки kṣam/çam, З-1978 §118 «неполноизменяемые» rādhya/vāya/dhyāya — гипотеза «у Зализняка нет» снова опровергнута); u-stems — CONFIRMED; n-sandhi — CONFIRMED-WITH-NUANCE (Уитни понижает статус n→ṇ «rarely if ever» и носового l «manuscripts disregard», Бюлер и З-1978 дают без оговорок); лемма-слой — GAP-CLOSED: crosswalk покрывает 12/12, но только под орфографией Зализняка — dīv (3 физ. строки: #363 play/#364 lament + дубль U₂-блока-2026) и hṛ (#923 take/#924 be angry), поиск по «div»/«har» пуст — обе ловушки задокументированы. Ключевая заметка лемма-слоя: шесть корней урока (kram/tam/śam/śram/bhram/cam) в crosswalk M-ряда (M₁→M₂) — ряд корня ≠ стратегия презенса урока.
- **Reuse-кластеры урока VI:** 3 точных совпадения упражнений с Kochergina XIII (VI.109/.115/.122 ↔ XIII.267/.266/.265) и 3 с Knauer (VI.113/.118 ↔ Nr.10; VI.122 ↔ Nr.2) — все exact 1.0 (matches.json). HB-регистр урока: HB-11, HB-86, HB-87, HB-88, HB-89, HB-90, HB-91 (все TRUE; HB-84/85 — урок V, не VI).
- **Каталог регенерирован:** LessonConcordance/catalog.mdx — 5 уроков (I, XXII, XXIX, XXXVIII, VI), 75 link-строк; src/lesson-backlinks.json — 10 страниц-источников.

### Verification
- `python scripts/build_lesson_concordance.py` — PASS (spots validated: 51 local OK, 3 external; 5 lessons, 75 rows).
- `kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — PASS (all clean, 0 ошибок).
- DeepSeek-спот-чек (пре-авторизован MG 01-10-2026): 5/6 PASS сразу; поймал 2 неточности лемма-слоя — dīv = 3 физ. строки (не 2; дубль #363 с рядом U₂ в блоке 2026) и mad = строки #545 совпадают только в колонках З-1975 (z-ряды A1/N1/N2) — обе исправлены в topics.yml, пересобрано.
- Первые вхождения спот-фраз сверены: все попадают в нужные локусы (Кочергина XV = 3285, XIII = 2646, X = 2034; Очерк §118 = 1970, §84 = 1192, §43 = 620; Кнауэр Nr.10 = 90, Nr.2 = 26; sangram = 16). Строка n-sandhi переведена с Nr.10 на Nr.2 (aśvāṁl laghvā впервые встречается в Nr.2).

### Files
- `LessonConcordance/topics.yml` — урок VI (4 темы, 11 spots, 4 вердикта, 12 лемм)
- `LessonConcordance/typed_link_buhler_lessons.tsv` — +15 строк
- `LessonConcordance/catalog.mdx`, `src/lesson-backlinks.json` — регенерированы

_H5657 · OxAlpha (opencode/z-ai/glm-5.3-flash) · 05-10-2026_
