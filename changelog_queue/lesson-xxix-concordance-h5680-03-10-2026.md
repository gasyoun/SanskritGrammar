### Changed
- **Поурочный конкорданс Бюлера — урок XXIX приземлён (H5680, OxAlpha, 03-10-2026).** Тема урока — Absolutivum/Gerundium на -tvā, -ya, -am (Buhler_Unicode.mdx 3985–4122). 5 тем: absolutivum-tvaa, absolutivum-ya, absolutivum-am, absolutivum-syntax (перевод + a privativum + герундии-предлоги), verb-roots (лемма-слой). 18 новых TSV-строк (30 всего): Уитни §§989–995 (Wikisource-якоря), Очерк §165/§219, Кочергина Занятие XXIII/XXXIII, Кнауэр Nr.19/Nr.14, sangram-article:absolutive, Apte §120, dhatu-glava7, talmud-crosswalk. 9 фраз-утверждений в spots (E10), build-валидация 21/21 local OK. Вердикты об исключениях: tvā/ya/syntax — CONFIRMED (исключения у всех четырёх свидетелей, у З-1978 тоже — гипотеза «у Зализняка нет» снова опровергнута), am — CONFIRMED-WITH-NUANCE (Кочергина молчит, honest gap), лемма-слой — GAP-CLOSED: crosswalk покрывает 12/12 корней урока (урок I — 10/13); единственный открытый вопрос — cal (L?, index-unknown). HB-41/HB-42 — claims урока (DCS-2021: 78,4 % абсолютивов на -ya; -am = 0,4 %).
- **Reuse-кластер урока XXIX зафиксирован честно:** Knauer Nr.19 ↔ Бюлер XXIX «भुक्त्वा पीत्वा चैते नराः/नरः सुप्ताः» (matches.json, buhler-1923.XXIX.635 ↔ knauer-1908.19.411, score 0.84).
- **Backlink-оверлей добавлен на статью sangram/articles/absolutive** (import LessonBacklinks + `<LessonBacklinks page="sangram-absolutive" />`; E3–E4); генератору добавлены SOURCE_PAGES/LOCAL_SOURCE_FILES sangram-absolutive — её spots теперь валидируются на build.
- **Каталог регенерирован:** LessonConcordance/catalog.mdx — 2 урока (I, XXIX), 30 link-строк; src/lesson-backlinks.json — 7 страниц-источников.

### Verification
- `python scripts/build_lesson_concordance.py` — PASS (spots validated: 21 local OK, 0 external; 2 lessons, 30 rows).
- `kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — PASS (all clean, 0 ошибок).
- DeepSeek-спот-чек (пре-авторизован MG 01-10-2026): 5/6 PASS сразу; поймал мисцитацию Уитни (герундии-предлоги — §994g, не §991g) — исправлено в topics.yml, пересобрано; Apte §120 подтверждён.
- Спот-фразы: первые вхождения сверены вручную — все попадают в нужные локусы (Занятие XXIII = 5534/5565, XXXIII = 8778; Очерк §165 = 2526/2532/2534, §219 = 2864; Кнауэр Nr.19 = 163, Nr.14 = 122).

### Files
- `LessonConcordance/topics.yml` — урок XXIX (5 тем, 9 spots, 5 вердиктов, 12 лемм)
- `LessonConcordance/typed_link_buhler_lessons.tsv` — +18 строк
- `LessonConcordance/catalog.mdx`, `src/lesson-backlinks.json` — регенерированы
- `scripts/build_lesson_concordance.py` — +sangram-absolutive (SOURCE_PAGES, LOCAL_SOURCE_FILES)
- `sangram/articles/absolutive/index.mdx` — LessonBacklinks-оверлей

_H5680 · OxAlpha (opencode/z-ai/glm-5.3-flash) · 03-10-2026_
