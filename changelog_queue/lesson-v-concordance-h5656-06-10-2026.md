### Changed
- **Поурочный конкорданс Бюлера — урок V приземлён (H5656, OxAlpha, 06-10-2026).** Тема урока — глаголы IV класса (ya к корню: lubh→lubhya-), сущ. м. р. на u (bhānu), висарга перед c/ch, ṭ/ṭh, t/th и предлог-преверб ā (Buhler_Unicode.mdx 652–788; жирный делимитер «**Урок V.**» — единственный урок без заголовочного «# УРОК N.», парсер ведёт нормализованный реестр). 5 тем: present-class-iv, u-stems, visarga-sandhi, preposition-a, lesson-roots (лемма-слой). 19 новых TSV-строк (137 всего): Уитни §§759–762 (ya-класс), §§341–344 (u-основы, §341 çátru), §§170–172 (висарга), §1128 (ā + Abl.), Очерк §118/§84/§44/§212, Кочергина Занятие XV/XIII/VI/XXXIX, Кнауэр Nr.2/Nr.17, sangram-article:thematic-present/preverbs, dhatu-glava7, talmud-crosswalk. 10 фраз-утверждений в spots (E10), build-валидация 91/91 local OK.
- **Вердикты об исключениях:** present-class-iv — CONFIRMED-WITH-NUANCE (Уитни §759 «accented but unstrengthened root» + §760 медийная парадигма, З-1978 §118 «неполноизменяемые» rādhya/vāya/dhyāya — гипотеза «у Зализняка нет» снова опровергнута); u-stems — CONFIRMED (Уитни §343: «There are no irregular u-stems» — ноль нерегулярных u-основ); visarga-sandhi — CONFIRMED (урок I + урок V = полный набор Бюлера; Очерк §44 п. 2 и Кочергина VI п. 2 а–г изоморфны с исключениями gīrṣu/niṣputra, которых Бюлер V не имеет); preposition-a — PARTIAL-REFUTED, единственный OVERSTATED-вердикт урока: HB-10 — печатное «Acc. или Abl.» не подтверждается (Уитни §1128 — только аблатив, Шерцль нулевая аккузативная аттестация); лемма-слой — GAP-DOCUMENTED: crosswalk 9/10 (śuṣ — строки нет), likh — ряд I₁ при VI-классе (повтор оси «ряд ≠ класс» урока IV), оба омонима урока разведены рядами (as, naś).
- **Reuse-кластеры урока V:** matches.json строк урока V не содержит — честно пусто; дословные перекрытия зафиксированы курируемо в notes тем (Кнауэр Nr.2: «viṣṇum ṛṣir yajati nṛpāya» = строка упражнения урока V; gurū çiṣyayoḥ krudhyataḥ и ṛkṣā madhu lubhyanti — § 124 ya-основы).
- **Каталог регенерирован:** LessonConcordance/catalog.mdx — 9 уроков (I, II, III, IV, V, VI, XXII, XXIX, XXXVIII), 137 link-строк; src/lesson-backlinks.json — 10 страниц-источников (+ sangram-preverbs).

### Verification
- `python scripts/build_lesson_concordance.py` — PASS (spots validated: 91 local OK, 7 external; 9 lessons, 137 rows).
- `kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — PASS (all clean, 0 ошибок; ключ темы preposition-ā → preposition-a: ASCII-требование lint к anchor_id).
- DeepSeek-спот-чек (пре-авторизован MG 01-10-2026): 9/10 OK сразу; поймал 3 неточности диапазонов — §3 = 675–687 (не 683–693), §2 = 656–673 (не 656–681), §4 = 689 (не 695–699) — все исправлены в topics.yml, пересобрано; PLUS метка bhānu-bhyaḥ I.pl.→D.pl. Все байт-вхождения спот-фраз подтверждены 1:1.
- `scripts/check_generated_outputs.py` — 0 file(s) with real changes (каталог в синхроне).

### Files
- `LessonConcordance/topics.yml` — урок V (5 тем, 10 spots, 5 вердиктов, 10 лемм)
- `LessonConcordance/typed_link_buhler_lessons.tsv` — +19 строк
- `LessonConcordance/catalog.mdx`, `src/lesson-backlinks.json` — регенерированы

_H5656 · OxAlpha (opencode/z-ai/glm-5.3-flash) · 06-10-2026_
