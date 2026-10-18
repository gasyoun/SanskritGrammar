# H5687 — spot-check протокол урока XXXVI (08-10-2026)

_Executor: OxAlpha (`opencode/z-ai/glm-5.3-flash`) · прецедент серии: H5667/H5670/H5677/H5678/H5682/H5684/H5685/H5686_

## D12 спот-чек — DeepSeek-лейн

- DeepSeek-ключа на боксе нет (auth-store пуст) — **15-й прецедент серии** (H5685: «DeepSeek-лейн 401», H5686: «auth-store пуст»).
- Замена: **независимая свежепроцессная проверка** (одноразовый python-скрипт, не разделяет состояние с кураторским проходом).

## Результат: 22/22 PASS (21 PASS + 1 FAIL = дефект чекера, перепроверен)

| # | Проба | Вердикт |
|---|---|---|
| 1 | Сегмент урока XXXVI (mdx 5095–5240) содержит правило tan (tanomi, tanuvaḥ), kṛ (karo/kuru), cvi (pitrībhū) | PASS |
| 2 | Сегмент ограничен (без содержания XXXVII) | PASS |
| 3–10 | HB-287/288/289/290 в claims.yml + цитаты клеймов ∈ сегмент урока (fold-проверка реестра против текста) | PASS ×8 |
| 11 | Кочергина XVI tanādi-фраза байт-в-байт | PASS |
| 12 | Кочергина XVII karó-/kuru-фраза байт-в-байт | PASS |
| 13 | Кнауэр Nr.12 āviṣkurvantu байт-в-байт | PASS |
| 14 | Очерк §135 kar-аномалия байт-в-байт | PASS |
| 15 | crosswalk CSV покрывает tan/kṛ/kṣan/duṣ/man (csv-парсер) | PASS |
| 16 | Негативный проб: незаявленных корней в лемма-таблице нет | PASS |
| 17 | 16 новых TSV-строк × 10 колонок | PASS |
| 18 | Все новые строки dated 08-10-2026 | PASS |
| 19 | catalog.mdx: «Урок XXXVI» + 5 тем + лемма-таблица + reuse | PASS |
| 20 | ПЕРВИЧНО FAIL — **дефект чекера**: срез по `cat.index("## Урок XXXVI")+5` ловил следующую секцию по кривому оффсету; перепроверка awk-срезом `/^## Урок XXXVI /,/^<small/` — все 5 тем, спот-фразы в URL-фрагментах, лемма-таблица на месте | PASS (после фикса чекера) |
| 21 | backlinks JSON: knauer содержит XXXVI-записи | PASS |
| 22 | matches.json: ровно 1 reuse-кластер (XXXVI.833 ↔ knauer 12.274) | PASS |

## Build/lint (отдельные ворота)

- `python3 scripts/build_lesson_concordance.py` — **SPOT-FAIL контур жив**: `spots validated: 371 local OK, 21 external` (9 новых локальных фраз урока — все байт-в-байт).
- `python3 kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — **all clean, 0 ошибок**.

## Дефекты данных

- 0 дефектов данных урока XXXVI.
- Попутно найден артефакт **предыдущего прохода H5686**: topics.yml обрывается на заголовке темы `XXXV.lesson-roots` (title + buhler_locus, без spots/lemmas/exceptions) — лемма-таблица урока XXXV не попала в каталог. Вне скоупа H5687 → GTD @DO 08-10-2026.
