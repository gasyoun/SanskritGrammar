# RWS-правки: что внедрено, что отложено (H385)

_Created: 10-07-2026 · Last updated: 10-07-2026_

Памятка по внедрению стилистических RWS-находок
([RWS_FINDINGS.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/RWS_FINDINGS.tsv),
1127 находок) в прозу книги GasunsDhatu 2026 по задаче
[H385](https://github.com/gasyoun/Uprava/blob/main/handoffs/H385-Opus_SanskritGrammar_gasuns-dhatu-rws-apply-highlight_08.07.26.md)
(исполнитель Opus 4.8 `claude-opus-4-8`).

## Что внедрено

**85 абзацев переработано, 94 находки внедрены** в 4 файлах. Каждый правленый абзац —
жёлтая заливка + Word-комментарий «Было: …» в
[GasunsDhatu_2026_RWS_review.docx](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/GasunsDhatu_2026_RWS_review.docx)
(85 комментариев, 91 highlight-фрагмент). Машинный лог —
[rws_edits.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/rws_edits.jsonl).

| Файл | Внедрено |
|---|---|
| [02_gasuns-dhatu-PhD-text2.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx) | 73 |
| [Морфонологическая запись глагольных корней санскрита.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/Морфонологическая%20запись%20глагольных%20корней%20санскрита.mdx) | 5 |
| [О записи омонимии корней в словарях древнеиндийского языка.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/О%20записи%20омонимии%20корней%20в%20словарях%20древнеиндийского%20языка.mdx) | 1 |
| [Распределение рядов согласных.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/Распределение%20рядов%20согласных.mdx) | 6 |

**Характер правок** (по приоритетной оптике `zaliznyak-method` в первую очередь):

- **Д1 — транслитерация и туземные термины:** IAST при первом упоминании (дхату →
  дхату (*dhātu*); пять варг → кантхья (*kaṇṭhya*) и т.д.), уточнение туземных терминов
  (анубандха, дхатупатха).
- **Д2 — логика, ясность, регистр:** снятие риторики («вне всяких сомнений», «трудно не
  заметить», «разумеется»), приведение прозы в соответствие с собственными таблицами
  статьи «Распределение рядов согласных» (где текст утверждал рост ряда, а таблица
  показывала p > 0,05 — правка убирает противоречие, **не меняя цифр**).

## Что НЕ внедрено и почему

**756 находок отложено** по кластерам (см.
[RWS_SKIPPED.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/RWS_SKIPPED.md)):
Д4 (нет источника/сутры/страницы/стиха) и Д5 (требуется дописать научный слой) —
внедрять ссылку «на память» нельзя; Д3 (недоказанные утверждения) — смягчение отложено,
чтобы не менять регистр всей книги одним махом.

## ⚠️ Критично: якоря RWS_FINDINGS.tsv смещены относительно текущего .mdx

Из **282 абзацев-кандидатов** на внедрение правку получили только **85**. Остальные
**197 не тронуты не потому, что находки неприменимы, а потому что номера строк (`line`) в
[RWS_FINDINGS.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/RWS_FINDINGS.tsv)
не соответствуют текущей сегментации файла** — файл уже правился (пилот Гл. 2
[H358](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H358-Fable_SanskritGrammar_gasuns-dhatu-ch2-monograph-pilot_08.07.26.md)
и др.) после того, как находки были посчитаны, и строки «съехали».

Признаки, подтверждённые двумя независимыми проходами и диагностикой:

- В хвосте документа (строки 3000+) абзац по `line` — это **библиография, оглавление,
  списки сокращений**, а находка при нём говорит о прозе (корни, сутры). Пример: находка
  просит IAST для корня √sac, а абзац при её `line` — `- № 349 *2dā* divide, share`.
- В таблицах (лакары ЛАṬ/ЛОṬ, `rst-table`) сидят находки о процентах согласных.
- В нумерованных строках-цитатах (`34. sr 761 dasrā, usrā`) — находки о глаголах,
  которых там нет.

**Защита от порчи:** внедрение шло через детерминированный конвейер с двумя предохранителями —
(1) правка внедряется только если её «было» присутствует в файле **дословно и ровно один
раз**; (2) правки, чьё «было» — библиографическая / табличная / индексная строка,
**отклоняются** ([rws_assemble.py](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/rws_assemble.py)
`unsafe_edit`). Поэтому ни одна смещённая находка не попала в текст.

**Как добрать оставшиеся ~197 + основную массу Д1/Д2:** пере-привязать находки к текущим
абзацам **по содержанию** (`para_hash`/дословный фрагмент), а не по номеру строки, затем
повторить проход. Это **подтверждает зависимость H385 из хендоффа** — задачу следует
доводить **после**
[H378](https://github.com/gasyoun/Uprava/blob/main/handoffs/H378-Opus_SanskritGrammar_gasuns-dhatu-ch3-monograph-rework_08.07.26.md)
(Гл. 3 сейчас в активной переработке) и
[H386](https://github.com/gasyoun/Uprava/blob/main/handoffs/H386-Opus_SanskritGrammar_gasuns-dhatu-monograph-skeleton_08.07.26.md)
(перестройка скелета), иначе якоря продолжат смещаться.

## Метод и трудозатраты

Конвейер (все скрипты в
[revision-2026/](https://github.com/gasyoun/SanskritGrammar/tree/main/GasunsDhatu_2014/revision-2026)):
`rws_triage.py` (1127 → 371 APPLY / 185 SOFTEN / 571 SKIP по Д1–Д5) →
`rws_extract_worklist.py` (точный текст абзаца) → параллельная переработка (8 сессий
Opus 4.8, read-only, по батчам) → `rws_assemble.py` (сборка + предохранители) →
`rws_apply.py` (детерминированное внедрение) → `rws_to_docx.py` (docx с заливкой и
комментариями). Первый заход fan-out по основному тексту вернул пусто (недоработка
агентов); повторный заход с уточнённым брифом дал корректный «выровненный» поднабор и
независимо выявил смещение якорей.

Трудозатраты: ≈52 мин по
[EFFORT_LOG.md](https://github.com/gasyoun/Uprava/blob/main/EFFORT_LOG.md) (счётчик не
инкрементировался пофайлово — учтено время сессии, не поштучные чтения).

Инструкция автору по просмотру — 
[RWS_REVIEW_INSTRUCTION.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/RWS_REVIEW_INSTRUCTION.md).

_Dr. Mārcis Gasūns_
