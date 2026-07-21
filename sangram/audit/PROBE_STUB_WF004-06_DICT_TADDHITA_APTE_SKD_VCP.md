# Зонд-стуб — WF004-06: таддхита-объём из словарей Апте / SKD / VCP

_Created: 21-07-2026 · Last updated: 21-07-2026_

**Заметка автора** (лист `sanskritgrammar-sg-wf-004-taddhita_visa`, карточка `WF004-06`, дословно):

> «Одобрить отказ от количественной оценки - нет, есть словарь Апте санскритско-хниди,
> мы оттуда уже извлекали нужные нам данные, а также SKD и VCP»

**Статус: DEFERRED** — остаток заметки после H1274. Существо заметки — «не отказываться
от количественной оценки, словари её дают» — уже закрыто статьёй
[taddhita-overview](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/taddhita-overview/index.mdx)
§§ 3-bis / 3-ter / 3-quater: словарная количественная оценка дана по MW (36 290 токенов)
и PWG (117 243 токена). Открытым остаётся именно **проход по трём названным автором
словарям** — Апте (санскритско-хинди разметка аффиксов), SKD и VCP.

## Что уже существует (prior art — не перестраивать)

Автор прав: извлечение уже делалось. В
[csl-orig/v02/etymology_stats](https://github.com/sanskrit-lexicon/csl-orig/tree/master/v02/etymology_stats)
живёт кросс-словарный этимологический конвейер
([stats_etymology.py](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/etymology_stats/stats_etymology.py)),
а его входы — готовые TSV с разбором kāraka + pratyaya в стиле санскритской традиции:

| Словарь | Файл | Строк данных | Ключевые колонки |
|---|---|---:|---|
| SKD | [skd/skd_etymology.tsv](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/skd/skd_etymology.tsv) | 2 213 | `headword_slp1`, `root_slp1`, `affix`/`affix_slp1` (имя пратьяи), `group`, `context` |
| VCP | [vcp/vcp_etymology.tsv](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/vcp/vcp_etymology.tsv) | 3 664 | те же |
| Апте (AP90) | [ap90/ap90_etymology.tsv](https://github.com/sanskrit-lexicon/csl-orig/blob/master/v02/ap90/ap90_etymology.tsv) | 332 | те же; `affix_source=Apte-SH(affix_map.tsv)` — карта аффиксов санскритско-хинди Апте уже задействована |

## Что решит зонд

1. **Разделить пратьяи на kṛt и taddhita** по их панинийским именам (`ghañ`, `ac`,
   `lyuṭ` — kṛt; `matup`, `ini`, `ṭhak`, `aṇ`, `yat`, `tal`, `tva` — taddhita):
   курируемая карта имён, ~50 строк, не эвристика по финали.
2. **Сосчитать таддхита-типы** по каждому словарю и классу суффиксов — кураторская
   мера, параллельная § 3-bis (MW `wsfx`) и § 3-quater (PWG `von`).
3. **Приджойнить к пину DCS** (`04e0778`, тег `c3-pin-04e0778-content`) — токенные
   частоты, сопоставимые с колонками «Токенов DCS» существующих таблиц статьи.
4. **Сверить** с MW/PWG-срезами: пересечение и добор (ожидание: санскритская
   традиция SKD/VCP покрывает патронимы и относительные -ya/-ika лучше, чем MW `wsfx`).

## Почему отложено, а не сделано в H1274

Шаг 1 — курируемая карта пратьяя→kṛt/taddhita — содержательная санскритологическая
работа (омонимия имён, анубандхи), не механический фильтр; делать её мимоходом —
значит получить ту же ловушку, что поверхностный отбор по финали (§ 4 статьи).
Объём — отдельная сессия с собственной проверкой. Числа статьи этот остаток не
блокирует: § 6 п. 5 статьи уже фиксирует его как открытый.

_Dr. Mārcis Gasūns_
