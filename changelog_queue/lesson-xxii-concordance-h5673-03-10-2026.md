### Changed
- **Поурочный конкорданс Бюлера — урок XXII приземлён (H5673, OxAlpha, 03-10-2026).** Тема урока — именное склонение (Buhler_Unicode.mdx 2863–3025): имена на r (gir, pur, vār — висарга в N., удлинение ir/ur), на in/min/vin (dhanin → dhanī, отбрасывание n, ж. р. на -ī), ср. р. на as/is/us (manas, havis, dhanus — o/ir/ur перед bh, āṅsi/īṅṣi/ūṅṣi; м./ж. sumanāḥ/sumanaḥ). 4 темы: r-stems, in-stems, as-is-us-stems (D13-расширения словаря), lesson-roots (лемма-слой, 1 глагол sañj). 17 новых TSV-строк (60 всего): Уитни §§383–392 / §§438–441 / §§412–419 (Wikisource-якоря), Очерк §100/§90/§92, Кочергина Занятие XXIX/XXX, Кнауэр Nr.5/Nr.6, sangram-article:consonant-stems, dhatu-glava7, talmud-crosswalk. 11 фраз-утверждений в spots (E10), build-валидация 41/41 local OK. Вердикты об исключениях: r-stems — CONFIRMED-WITH-NUANCE (ṛṣ-перед-su Бюлер применяет молча, Зализняк оговаривает явно: §§31.2а/44.2), in-stems и as-is-us — CONFIRMED (у всех четырёх свидетелей правила/варианты есть; у Кочергиной не упомянут variant manassu — honest gap), лемма-слой — GAP-CLOSED: crosswalk покрывает 1/1 (строка 829,saj).
- **Reuse-кластеры урока XXII зафиксированы честно:** Knauer Nr.5 ↔ Бюлер XXII «पुरि वास्तडागान्नाल्या पार्थिवोऽनाययत्» (matches.json, buhler-1923.XXII.497 ↔ knauer-1908.5.97, 0.928) и Knauer Nr.6 ↔ «मन्त्रिणः स्वामिने कदापि न द्रुह्येयुः» (buhler-1923.XXII.498 ↔ knauer-1908.6.124, exact 1.0).
- **Backlink-оверлей добавлен на статью sangram/articles/consonant-stems** (import LessonBacklinks + `<LessonBacklinks page="sangram-consonant-stems" />`; E3–E4); генератору добавлены SOURCE_PAGES/LOCAL_SOURCE_FILES sangram-consonant-stems — её spots теперь валидируются на build.
- **Каталог регенерирован:** LessonConcordance/catalog.mdx — 4 урока (I, XXII, XXIX, XXXVIII), 60 link-строк; src/lesson-backlinks.json — 10 страниц-источников.

### Verification
- `python scripts/build_lesson_concordance.py` — PASS (spots validated: 41 local OK, 2 external; 4 lessons, 60 rows).
- `kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — PASS (all clean, 0 ошибок).
- DeepSeek-спот-чек (пре-авторизован MG 01-10-2026): 13/14 PASS; пойман ложный GAP — sañj ЕСТЬ в crosswalk под кратким написанием saj (строка 829, talmud_ref «saj, sañj»), первичный grep по «sañj» строку не нашёл — лемма-таблица и вердикт исправлены на GAP-CLOSED 1/1, ловушка поиска задокументирована; Уитни §§412–419 подтверждены (§419 ещё несёт as-основу anehás, an-раздел начинается с §420); все 4 HB-клейма урока (HB-164/165/166/168) локализованы «Урок XXII», verdict TRUE/JUSTIFIED.
- Спот-фразы: все 11 локальных первых вхождений сверены — попадают в нужные локусы (Очерк §100 = 1620, §90 = 1392, §92 = 1492; Занятие XXIX = 7332, XXX = 7646/7746/7691; Кнауэр Nr.5 = 50, Nr.6 = 56/58).

### Files
- `LessonConcordance/topics.yml` — урок XXII (4 темы, 11 spots, 4 вердикта, 1 лемма)
- `LessonConcordance/typed_link_buhler_lessons.tsv` — +17 строк
- `LessonConcordance/catalog.mdx`, `src/lesson-backlinks.json` — регенерированы
- `scripts/build_lesson_concordance.py` — +sangram-consonant-stems (SOURCE_PAGES, LOCAL_SOURCE_FILES)
- `sangram/articles/consonant-stems/index.mdx` — LessonBacklinks-оверлей

_H5673 · OxAlpha (opencode/z-ai/glm-5.3-flash) · 03-10-2026_
