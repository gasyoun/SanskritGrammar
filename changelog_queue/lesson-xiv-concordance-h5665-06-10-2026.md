# Поурочный конкорданс Бюлера — урок XIV (H5665)

_Created: 06-10-2026_

### Changed
- **Поурочный конкорданс Бюлера — урок XIV приземлён (H5665, OxAlpha, 06-10-2026).** Тема урока — Imperativus Parasmaipada (vad-āni; vad-a-tāt), сущ. ж. р. на ū (vadhū §2а, односложное bhū §2б), значения императива + mā (Buhler_Unicode.mdx 1801–1948). 5 тем: imperative-parasmaipada, u-stems-fem, u-stems-root-nouns, imperative-semantics, lesson-roots (лемма-слой). 18 новых TSV-строк (218 всего): Уитни §§739–740 (парадигма bhávāni + tāt «not rare»), §§362–364 (vadhū́ — модель §364), §§349–351 (bhū́ в §351), Очерк §§115/85/98/109, Кочергина Занятие XIV (повелительное) / XII (склонение ī/ū) / XXXVII (стих «धर्मं चरत»), Кнауэр Nr.3/Nr.10, sangram-article:imperative-optative, Apte §192 (благословение — точный параллель tāt-сноски), dhatu-glava7, talmud-crosswalk. 15 фраз-утверждений в spots (E10), build-валидация 147 local OK.
- **Reuse-кластеры урока:** 10 совпадений (matches.json) — 5 с Knauer Nr.3 (из них 4 точных; XIV.333↔3.58 0.974 — Кнауэр опускает висаргу в वध्वा), 2 с Knauer Nr.10 (पृच्छतु/पृछतу 0.968), 2 точных с Kochergina XXXVII (стих целиком), 1 частичное с Kochergina XIV (0.868).
- **Вердикты об исключениях:** imperative — CONFIRMED-WITH-NUANCE (tāt: у Уитни §740 ведийский список RV, у Бюлера «иногда» без списка); u-stems — CONFIRMED-WITH-NUANCE (три свидетеля ставят vadhū в модельную четвёрку); bhū — CONFIRMED-WITH-NUANCE (З-1978 §98 «в части форм» точнее немого списка Бюлера; Кочергина — honest gap); semantics — CONFIRMED-WITH-NUANCE (Apte §192 — единственный свидетель бенедиктивного 2–3 л.; Очерк §109 — только инвентарь наклонений); лемма-слой — GAP-DOCUMENTED: crosswalk 6/7 (śuc «grieve» — гомонимический провал, строка только «gleam»; as — омонимия be/throw, уроку отвечает «throw»).
- **Каталог регенерирован:** LessonConcordance/catalog.mdx — 14 уроков, 218 link-строк; src/lesson-backlinks.json — 11 страниц-источников (+sangram-imperative-optative).
- **Оверлей добавлен на статью sangram/articles/imperative-optative** (import LessonBacklinks + `<LessonBacklinks page="sangram-imperative-optative" />`; E3–E4); генератору добавлены SOURCE_PAGES/LOCAL_SOURCE_FILES sangram-imperative-optative — её spots теперь валидируются на build.

### Verification
- `python scripts/build_lesson_concordance.py` — PASS (spots validated: 147 local OK, 10 external; 14 lessons, 218 rows).
- `kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — PASS (all clean, 0 ошибок).
- DeepSeek-спот-чек (пре-авторизован MG 01-10-2026, councillor-deepseek): PASS 30/33 — поймал мисцитацию Кочергиной (таблица nadī↔vadhū с vadhū́ṣu — Занятие XII, раздел «Склонение основ на -ī и -ū», не XIII; замечено независимо повторной сверкой занятие-границ по строкам 2287/2585) — исправлено (TSV-строка + 2 текста topics.yml), пересобрано. Остальные 2 «FAIL» — дрейф loc-полей claims.yml на +2 строки (HB-22: указано 1815, текст на 1817; HB-64: 1859 vs 1861) — реестровый дрейф внесённой записи, не правился в этом проходе (вне скоупа урока; GitHub-якоря страницы конкорданса ссылаются на строки `- id:` и не затронуты).

### Files
- `LessonConcordance/topics.yml` — урок XIV (5 тем, 15 spots, 5 вердиктов, 7 лемм)
- `LessonConcordance/typed_link_buhler_lessons.tsv` — +18 строк
- `LessonConcordance/catalog.mdx`, `src/lesson-backlinks.json` — регенерированы
- `scripts/build_lesson_concordance.py` — +sangram-imperative-optative (SOURCE_PAGES, LOCAL_SOURCE_FILES)
- `sangram/articles/imperative-optative/index.mdx` — LessonBacklinks-оверлей

_H5665 · OxAlpha (opencode/z-ai/glm-5.3-flash) · 06-10-2026_
