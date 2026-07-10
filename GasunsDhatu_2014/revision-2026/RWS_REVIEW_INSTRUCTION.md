# Как просмотреть RWS-правки в Google Docs

_Created: 10-07-2026 · Last updated: 10-07-2026_

Одностраничная памятка к файлу
[`GasunsDhatu_2026_RWS_review.docx`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/GasunsDhatu_2026_RWS_review.docx)
— это вся книга 2026 г. с внедрёнными стилистическими правками (задача
[H385](https://github.com/gasyoun/Uprava/blob/main/handoffs/H385-Opus_SanskritGrammar_gasuns-dhatu-rws-apply-highlight_08.07.26.md)).

## Что открыть

1. Загрузите `GasunsDhatu_2026_RWS_review.docx` на Google Drive.
2. Откройте через **Google Docs** (правый клик → «Открыть с помощью» → Google Документы).
   Заливка и комментарии сохранятся при конвертации.

## Что вы видите

- **Жёлтая заливка** — этот абзац переработан. Всё, что не залито, осталось как было.
- **Комментарий к жёлтому абзацу** («Было: …») — исходный текст **до** правки, а также
  номера RWS-находок и стиль-рецензент, по которым правка сделана. Приоритетная оптика —
  `zaliznyak-method` (логическая доказательность, снятие риторики).

## Как принять или отклонить правку

- **Принять** — ничего не делать; правленый текст уже в основном тексте.
- **Отклонить** — скопируйте текст из комментария «Было: …» и вставьте на место жёлтого
  абзаца (либо просто напишите в комментарии «откатить», и правка будет снята при сведении).
- **Поправить** — отредактируйте прямо в жёлтом абзаце; заливку можно снять
  (Формат → Цвет выделения → Без выделения).

## Границы задачи (что НЕ трогалось)

- **Цифры и данные не менялись** — это отдельная задача
  ([H382](https://github.com/gasyoun/Uprava/blob/main/handoffs/H382-Opus_SanskritGrammar_gasuns-dhatu-data-recompute_08.07.26.md)).
- **Структура уровня книги** (порядок глав, скелет ВАК→монография) — задача
  [H386](https://github.com/gasyoun/Uprava/blob/main/handoffs/H386-Opus_SanskritGrammar_gasuns-dhatu-monograph-skeleton_08.07.26.md).
- **Ссылки, сноски, номера сутр и стихов НЕ добавлялись**: находки, требовавшие источника,
  точной страницы, номера сутры Панини или ведийского стиха, которых нет на руках, **не
  внедрялись** — они собраны в
  [`RWS_SKIPPED.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/RWS_SKIPPED.md)
  с указанием причины. Их можно закрыть отдельным проходом, когда источники будут под рукой.

## Куда вернуть решения

Отметки «откатить / поправить» можно оставить прямо в Google-комментариях; при следующем
проходе они сводятся в
[`rws_edits.jsonl`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/rws_edits.jsonl).
Сводка внедрённого и пропущенного — в
[`RWS_APPLY_MEMO.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/RWS_APPLY_MEMO.md).

_Dr. Mārcis Gasūns_
