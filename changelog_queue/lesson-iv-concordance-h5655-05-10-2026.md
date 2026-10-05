### Changed
- **Поурочный конкорданс Бюлера — урок IV приземлён (H5655, OxAlpha, 05-10-2026).** Тема урока — имена на i (agni м. / vāri ср.), правила saṃdhi aḥ→o/a, āḥ→ā, ar/ār→r, глаголы VI класса (Buhler_Unicode.mdx 532–651). 4 темы: i-stems, as-sandhi, present-class-vi, lesson-roots (лемма-слой). 15 новых TSV-строк (75 всего): Уитни §§335–343 / §§174–179 / §§751–758 (Wikisource-якоря), Очерк §84 / §44 / §117, Кочергина Занятие XIII / VI / XV, Кнауэр Nr.2 / Nr.10, sangram-article:thematic-present, dhatu-glava7, talmud-crosswalk. 10 фраз-утверждений в spots (E10), build-валидация 51/51 local OK + 3 external; первые вхождения сверены по строкам (все в нужных локусах).
- **Вердикты об исключениях (гипотеза MG):** i-stems — CONFIRMED (§3 Бюлера «могут употребляться формы муж. р.» = дословно заметка Очерка §84 о прилагательных на i/u; Уитни §336d — ведийская спорадичность ṇ-инфикса); as-sandhi — CONFIRMED (Очерк §44 пп. 3–6 изоморфен §4а–г Бюлера, общий пример agnī rocate; у Уитни исключение §176a sás/eṣás, которого у Бюлера нет); present-class-vi — CONFIRMED-WITH-NUANCE (Бюлер даёт только stems-список с n-инфиксом; Уитни §758 перечисляет все четыре глагола урока поимённо — muñcá/kṛntá/lumpá/limpá; З-1978 §117: «классы I и VI в послеведийском неразличимы» — системный ответ, почему Бюлер смешивает I и VI молча); лемма-слой — GAP-CLOSED: crosswalk покрывает 6/6 корней урока (карта полноты: I 10/13, XXII 1/1, XXIX 12/12, XXXVIII 5/7); ловушка поиска kṛt/kart задокументирована.
- **Reuse-кластеры урока IV зафиксированы честно:** 3 точных совпадения упражнений с Кочергиной XIII (matches.json 0.95–1.0), 3 с Кнауэром (Nr.10 × 2, Nr.2 × 1), 2 sandhi-примера с Кочергиной VI («agnī rocate» exact). corpus_layer.tsv урока IV: 0 строк (честно).

### Verification
- `python scripts/build_lesson_concordance.py` — PASS (spots validated: 51 local OK, 3 external; 5 lessons, 75 rows).
- `kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — PASS (all clean, 0 ошибок).
- DeepSeek-спот-чек (пре-авторизован MG 01-10-2026, councillor-deepseek 05-10-2026): **6/6 PASS**. Самопойманные до верификатора: (1) «nudātu/muñcātu occur in Sūtras» — это §752, а не §753a (исправлено в topics.yml до спот-чека); (2) «закрывающая заметка §84» — правило прилагательных стоит перед «Особыми случаями» sakhi/pati, формулировка ослаблена после вердикта. Advisories верификатора: оба приняты.
- Ресидюал (вне скоупа урока, занесён в GTD): claims.yml loc-строки урока IV (HB-79…83 «mdx line 566/570/572/574/576») систематически отстают на 2 строки от текущего Buhler_Unicode.mdx (фактически 568/572/574/576/578) — дрейф нумерации mdx от момента H797; перенавести все 403 HB-лока отдельной бухгалтерской задачей.

### Files
- `LessonConcordance/topics.yml` — урок IV (4 темы, 10 spots, 4 вердикта, 6 лемм)
- `LessonConcordance/typed_link_buhler_lessons.tsv` — +15 строк
- `LessonConcordance/catalog.mdx`, `src/lesson-backlinks.json` — регенерированы

_H5655 · OxAlpha (opencode/z-ai/glm-5.3-flash) · 05-10-2026_
