# Поурочная навигация (h2 + нативный TOC) на остальных книгах (H6563)

_Created: 13-10-2026 · Last updated: 13-10-2026_

_Repo: gasyoun/SanskritGrammar · Source: ApteSyntax_1885, KnauerFrazy_1908, TolchelnikovTalmud_2026, GasunsDhatu_2014, ZalizniakOcherk_1978_ · Date: 2026-10-13_

## Что

Паттерн PR [#1082](https://github.com/gasyoun/SanskritGrammar/pull/1082) (Kochergina/Buhler h2 + нативный TOC) распространён на остальные маршрутизированные книги, где Word-конверсия держала секции h1, а нативный TOC их не показывал. Точный цензус перед правкой: из 265+ трекаемых `.mdx` ровно 5 маршрутизированных файлов несут больше одного h1 — Apte-unicode.mdx (35), Frazy-Knauer-03.05.2023.mdx (19), Talmud-2.1.6.mdx (16), 02_gasuns-dhatu-PhD-text2.mdx (11), Zalizniak-Ocherk_29-11-20-aligned.mdx (9). Во всех пяти **все** ин-боди h1 повышены до h2 — вербатим, 90 строк, у каждой меняется только счётчик `#`; заголовки из front matter не тронуты. Whitney — почётвертые файлы-главы без мульти-h1 (цензус: 0 кандидатов), Apte-Composition под `src/` и RWS-review — вне сборки (exclude), не тронуты. Apte-якоря: 31 ин-пейдж `#…`-ссылка оглавления не тронута; слаги заголовков выводятся тем же github-slugger из того же текста, так что `remarkFixHeadingAnchors` (демоция h1→h2 в AST) стал идемпотентным, ссылки резолвятся как раньше; владелец-гейт `#-N`-якорей (класс H889) не затронут — в файле `#-N`-литералов нет.

Потребители, требовавшие толерантности к уровню: `extract_sentences.py` — матчеры knauer (`^#\s*Nr\.` → `^#{1,2}\s*Nr\.`) и apte (`^#\s*\**Урок` → `#{1,2}`) расширены по образцу PR [#1084](https://github.com/gasyoun/SanskritGrammar/pull/1084); buhler/kochergina уже были толерантны. M03-чекеры диссертации: `gost_bibliography_check.py` (заголовок библиографии + секция «Принятые сокращения») и `numbers_crosscheck.py` (граница блока «Список иллюстративного материала») переведены с exact-h1-матча на level-agnostic (`lstrip('#')`, идиома `build_lessonpack.lesson_slice`), иначе чекер библиографии падал SystemExit, а сокращения парсились 21 → 0 с 8 ложными R1. Реген: `sangram/editorial/data/consolidation_ledger.json` — пре-существующая суточная сталь (воспроизведена `--check`-фейлом на чистом origin/main), освежена для зелёного CI end-to-end.

## Проверки

- Дельта-пруф матчеров: old-rx/old-text ≡ new-rx/new-text (knauer 19, apte 30 уроков, идентичные последовательности id; new-rx на старом тексте тоже идентичен — обратно-совместимо).
- Дельта-пруф M03-чекеров: отчёты `numbers_crosscheck --stdout` и `gost_bibliography_check --stdout` побайтно идентичны на чистом origin/main и на промотированном дереве.
- `pytest` — полный локальный прогон зелёный (включая `test_m03_freeze_harness`, `test_build_lessonpack`, `test_corpus_layer`).
- Все 8 CI-валидаторов exit 0, включая `build_grammar_lab --check` и `consolidation_ledger_refresh --check` (после регена).
- `npm run build` exit 0; собранный HTML каждой из 5 книг содержит `theme-doc-toc` и промотированные секции в TOC (Apte: 31 «Урок N», Knauer: «Nr. 19», Talmud: «Именная система», PhD: «Библиография», Ocherk: «Фонология»/«Морфология»).

## Ссылки

- Handoff: H6563 (Uprava registry), паттерн-родители [#1082](https://github.com/gasyoun/SanskritGrammar/pull/1082) + [#1084](https://github.com/gasyoun/SanskritGrammar/pull/1084).

_Dr. Mārcis Gasūns_
