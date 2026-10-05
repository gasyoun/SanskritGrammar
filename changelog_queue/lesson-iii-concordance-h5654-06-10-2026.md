### Changed
- **Поурочный конкорданс Бюлера — урок III приземлён (H5654, OxAlpha, 06-10-2026).** Тема урока — Present VI класса (тематическая a без guṇa; ṝ→ir, u/ū→uv, i→iy), склонение основ на a (недостающие к урокам I–II падежи D./Abl./L., ср. р. строкой «точно также»), значения падежей (Instr/Dat commodi/Abl/Gen/Loc по одной строке) (Buhler_Unicode.mdx 415–531). 4 темы: present-class-vi, a-stem-declension, case-functions, lesson-roots (лемма-слой, 12 глаголов: 9 VI + 3 I). 11 новых TSV-строк (118 всего): Уитни §§751–752 (tud-класс: §751 правило + §752 парадигма viç; переносы §§746–750, sad→śīda §748) / §§327–330 (§327 ед. ч. окончания, §330 парадигма kā́ma/devá/āsyà) / §§278–301 (употребления падежей), Очерк §117–121 (класс VI, коллапс I/VI, двухэтапные основы) / §71, Кочергина Занятие XV / X, sangram-article:thematic-present, dhatu-glava7, talmud-crosswalk. 7 фраз-утверждений в spots (E10), build-валидация 79/79 local OK + 5 external.
- **Вердикты об исключениях (гипотеза MG):** present-class-vi — CONFIRMED-WITH-NUANCE (правило чисто у Бюлера; Уитни §§746–750 даёт переносы корней в класс; Очерк §117: классы I/VI неразличимы послеведийски); a-stem-declension — PARTIAL (свидетели фрагментарны; локус Очерка — открытый вопрос, не выдуман); case-functions — CONFIRMED-WITH-NUANCE (HB-8 OVERSTATED — единственный не-TRUE клейм урока: «всякого рода принадлежность» опровергается §§294–300 Уитни: gen. с глаголами, gen. absolute, gen. времени); лемма-слой — GAP-DOCUMENTED.
- **Reuse-кластеры урока III честно пустые:** matches.json не содержит buhler-1923.III.*; corpus_layer.tsv урок III строк не имеет (регистр с XVIII).

### Verification
- `python scripts/build_lesson_concordance.py` — PASS (spots validated: 79 local OK, 5 external; 8 lessons, 118 rows).
- `kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — PASS (all clean, 0 ошибок).
- DeepSeek-спот-чек (пре-авторизован MG 01-10-2026, councillor-deepseek 06-10-2026): **5/8 PASS, все 3 дефекта подтверждены по первоисточникам и исправлены**: (1) a-stems: окончания ед. ч. — §§327c–g (§329 — множественное, вкл. eṣu §329g), было ошибочно §329c–g; (2) «Универсальные падежные окончания» сидит в Занятии X (L1931, заголовок L1871), не IX — локус перенесён; (3) ложный NO в crosswalk: строка `833,sarj,,creak` (A₁) СУЩЕСТВУЕТ — это другой корень √sarj «скрипеть», не уроковый √sṛj «творить»; покрытие 10/12 переформулировано по корневой тождественности с документированной ловушкой написания (класс tṝ/tṛ урока II). Re-verify: 3/3 CONFIRMED (grep по CSV/MDX).

### Files
- `LessonConcordance/topics.yml` — урок III (4 темы, 7 spots, 4 вердикта, 12 лемм)
- `LessonConcordance/typed_link_buhler_lessons.tsv` — +11 строк
- `LessonConcordance/catalog.mdx`, `src/lesson-backlinks.json` — регенерированы

_H5654 · OxAlpha (opencode/z-ai/glm-5.3-flash) · 06-10-2026_
