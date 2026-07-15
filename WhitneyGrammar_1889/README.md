# Уитни 1889 — «A Sanskrit Grammar»: цифровое издание и роль эталона

_Created: 15-07-2026 · Last updated: 15-07-2026_

Папка книги: Уильям Дуайт Уитни, *A Sanskrit Grammar, including both the Classical
Language and the older Dialects, of Veda and Brahmana* (2-е изд., Лейпциг/Бостон 1889;
текст 7-го тиража 1950) — **единственная полная справочная грамматика** репозитория:
§§ 1–1316, 18 глав + приложение, от фонетики и полного сандхи до синтаксиса,
словообразования и ведийского слоя. Public domain; цифровой текст восходит к изданию
английского Wikisource (CC BY-SA 4.0).

**Все поглавные страницы генерируются** — 19 `.mdx` (обзор
[00_index.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/WhitneyGrammar_1889/00_index.mdx)
+ главы 01–18 с приложением) собирает
[scripts/build_whitney.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_whitney.py)
из источников соседнего репозитория
[WhitneyRoots](https://github.com/gasyoun/WhitneyRoots) (`src/wg_text.txt` +
`src/whitney_sections.json`) — **руками `.mdx` не править**, править источник и
перегенерировать. Книжного `CHANGELOG.md` у папки нет — изменения логируются в
[корневом CHANGELOG](https://github.com/gasyoun/SanskritGrammar/blob/main/CHANGELOG.md).

## Восстановление деванагари (H427)

OCR печатного PDF захватил клетки парадигматических таблиц в *визуальном* порядке
(и-знаки перед не той согласной, потерянные матры, глифы лигатур из Private Use Area —
напр. § 902 «апāивишам» вместо «апāвишам»); эвристика перестановки матр невозможна —
57 % битых строк несли PUA-глифы. Решение в
[build_whitney.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_whitney.py):
деванагари **регенерируется из собственной латинской транслитерации Уитни**, стоящей
рядом в тексте (`indic_transliteration`, с учётом нотации Уитни: снятие ведийских
акцентов, āi/āu → ai/au, ç → ś) — 1 840 табличных ячеек + 186 доказуемо битых
inline-форм (замена гейтится диакритикой, чтобы не тронуть английские глоссы вида
«√नी lead»).

## Роль в программе проверки утверждений — эталон и судья

1. **Авторитет системного факта (правило D-B).** В триангуляции конвейера
   ([Кочергина](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/README.md) ·
   [Бюлер](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/README.md) ·
   [Кнауэр](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/README.md))
   Уитни решает *системный грамматический факт* (DCS-2021 — частотность,
   Толчельников-Талмуд — морфокласс корня): все 308 проверенных записей трёх реестров
   (HK-1..233, HB-1..64, KN-1..10) цитируют его по §§.
2. **Жанровый эталон.** В сравнении трёх моделей Зализняка
   ([ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md))
   Уитни — точка отсчёта: описывает исчерпывающе, **без абстракций высшего порядка**
   (ни морфологических позиций, ни рядов аблаута, ни исчисления типов корней) —
   родословная *Уитни (описывает) → Зализняк (абстрагирует) → Толчельников (порождает)*.
3. **Конкордансный хребет.** Тематические типизированные связи
   [SubjectConcordance](https://github.com/gasyoun/SanskritGrammar/tree/main/SubjectConcordance)
   (H540: 41 категория с якорями вида `whitney-sec:611-641`) и покрытие глав Уитни
   статьями ядра Sangram
   ([whitney_chapter_coverage.json](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/toc/data/whitney_chapter_coverage.json)).
4. **Будущий подсудимый.** Статья A60 резервирует класс «система-vs-употребление»
   (лицензировано грамматикой — не употребляется корпусом) именно под реестр,
   **собранный из Уитни**: судья конвейера — следующий кандидат в его же подсудимые
   ([набросок A60](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60/OUTLINE_grammar-claims-corpus-denies_A60.md)).

### Как воспроизвести

```bash
python scripts/build_whitney.py     # перегенерация всех 19 .mdx из WhitneyRoots
```

Требуется соседний клон [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots).
⚠️ В этом репозитории действует протокол осторожности с несохранённой работой других
сессий — перед перегенерацией см. памятки о конкурентных сессиях в
[.ai_state.md](https://github.com/gasyoun/SanskritGrammar/blob/main/.ai_state.md).

### Что дальше

Реестр «система-vs-употребление» из §§ Уитни для A60 (жатва системных лицензий →
корпусная проверка употребления); объединение §-конкордансов (SubjectConcordance ×
sangram TOC × §-отсылки трёх реестров) в единый навигационный слой.

_Dr. Mārcis Gasūns_
