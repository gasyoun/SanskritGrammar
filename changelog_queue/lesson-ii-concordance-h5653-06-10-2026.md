### Changed
- **Поурочный конкорданс Бюлера — урок II приземлён (H5653, OxAlpha, 06-10-2026).** Тема урока — ступени гласных guṇa/vṛddhi и их применение в I классе, a-основы (м./ср. р.), значения N./Acc., внешние сандхи гласных, s→ṣ (Buhler_Unicode.mdx 255–414). 5 тем: guna-ladder, a-stems, vowel-sandhi, s-retroflex, verb-roots (лемма-слой). 17 новых TSV-строк (107 всего): Уитни §§234–242 (guṇa/vṛddhi: §236 таблица + §240 правило допустимости) / §§326–331 (§330 deva) / §§126–127 / §§180–183 (Wikisource-якоря), Очерк §50 / §82 / §41 / §35, Кочергина Занятие XIII / IX / VII / X, Кнауэр Nr.3, sangram-article:conjugation-overview, dhatu-glava7, talmud-crosswalk. 14 фраз-утверждений в spots (E10), build-валидация 73/73 local OK + 4 external.
- **Вердикты об исключениях (гипотеза MG):** guna-ladder — CONFIRMED-WITH-NUANCE (лестница + правило допустимости HB-5 §§235/240 — редкое для школьной линии настоящее обобщение; но не-гуна основы (piba-, tiṣṭha-, paśya-, gaccha-, yaccha-) даны лексически в скобках, mdx 345–353 — проверено); a-stems — CONFIRMED; vowel-sandhi — CONFIRMED (HB-6: exceptionless, корпусная аргументация a/ā = junction rank #1); s-retroflex — CONFIRMED-WITH-NUANCE (прозрачность висарги/анусвары mdx 327 — уточнение, которого нет у школьных грамматик); лемма-слой — GAP-DOCUMENTED: crosswalk покрывает 10/11, отсутствует только yam.
- **Reuse-кластеры урока II честно пустые:** matches.json не содержит buhler-1923.II.* ; corpus_layer.tsv урок II строк не имеет (регистр с XVIII).

### Verification
- `python scripts/build_lesson_concordance.py` — PASS (spots validated: 73 local OK, 4 external; 7 lessons, 107 rows).
- `kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — PASS (all clean, 0 ошибок).
- DeepSeek-спот-чек (пре-авторизован MG 01-10-2026, councillor-deepseek 06-10-2026): **5/5 PASS после правок**. Верификатор поймал 3 дефекта, все подтверждены по первоисточникам и исправлены: (1) a-stems ссылался на §§347–351 — это основы на долгие гласные; парадигма deva — §330, верно §§326–331; (2) диапазон guṇa/vṛddhi был §§221–240 — верно §§234–242 (§236 таблица, §240 допустимость); (3) ложный GAP: tṝ ЕСТЬ в crosswalk — строка 669 под написанием tṛ «pass» (whitney_no 319, R₁) — ловушка поиска по написанию+глоссе, покрытие 9/11→10/11; плюс advisory: pā — drink ×2 / protect (не «protect ×2»).

### Files
- `LessonConcordance/topics.yml` — урок II (5 тем, 14 spots, 5 вердиктов, 11 лемм)
- `LessonConcordance/typed_link_buhler_lessons.tsv` — +17 строк
- `LessonConcordance/catalog.mdx`, `src/lesson-backlinks.json` — регенерированы

_H5653 · OxAlpha (opencode/z-ai/glm-5.3-flash) · 06-10-2026_
