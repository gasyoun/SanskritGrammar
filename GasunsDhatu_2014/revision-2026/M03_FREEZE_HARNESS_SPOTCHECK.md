# Ручная сверка сухих прогонов заморозочной оснастки M03 — H2871

_Created: 17-08-2026 · Last updated: 17-08-2026_

Приемочная улика к [H2871](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2871-Opus_SanskritGrammar_m03-freeze-harness-gost-numbers-prebuild_16.08.26.md):
по три позиции из каждого сухого прогона, проверенные глазами по печатному тексту
рукописи. Отчеты машинные и перегенерируются
([GOST_BIBLIOGRAPHY_DRYRUN_REPORT.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/GOST_BIBLIOGRAPHY_DRYRUN_REPORT.md),
[NUMBERS_CROSSCHECK_DRYRUN_REPORT.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/NUMBERS_CROSSCHECK_DRYRUN_REPORT.md));
эта страница — ручная, ее генератор не трогает.

Исполнитель: Opus 5 (`claude-opus-5`), 17-08-2026. **Рукопись не изменялась** —
находки суть инвентарь к предподачному проходу (авторская проза, H275; review-docx
[H1259](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1259-Fable_SanskritGrammar_m03-final-hybrid-line-edit-freeze_18.07.26.md)
под автором и не перегенерировался).

## ГОСТ-проход: 960 находок, проверено 3

| # | Код | Локус | Что печатает рукопись | Вердикт сверки |
|---|---|---|---|---|
| 1 | `G2` | [02_gasuns-dhatu-PhD-text2.mdx:3547](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx#L3547) | `369. **Mahabharata** 1919--1966 -- (= MBh) … -- Poona: Bhandarkar Oriental Research Institute, 1927--<2009>.` | **Подтверждено.** Сигла говорит 1919--1966, выходные данные — 1927--2009. Ссылка `MBh` из «Принятых сокращений» ведет на сиглу, поэтому расхождение не косметическое: год сиглы — ключ разрешения ссылки. |
| 2 | `G10` | та же строка 3547 | `1927--&lt;2009&gt;` | **Подтверждено.** HTML-сущности `&lt;`/`&gt;` — остаток конвертации Word→pandoc 2014 г.; наборщик воспроизведет их буквально. |
| 3 | `R1` | [02_gasuns-dhatu-PhD-text2.mdx:2046](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx#L2046), [:2048](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx#L2048) | «перечислены 996 корней [Whitney 1886, 25--29]» и «…[Whitney 1885 …], спустя же год [Whitney 1886]» | **Подтверждено.** В библиографии есть Whitney 1856, 1863, 1873, 1885, 1896 — записи 1886 нет. Текст противопоставляет 1885 и «спустя же год» 1886 осознанно, то есть источник реальный, а описания к нему в списке не существует. |

Дополнительно сверены (вне тройки, класс подтверждается одним взглядом):
`G5` — запись 14 «Бетлинг О.Н.» (инициалы без пробела);
`G7` — запись 21 «Сравнительно--историческое» (внутрисловное `--` вместо дефиса).

## Сверка чисел: 1 находка + 72 подтверждения, проверено 3

| # | Класс | Локус | Что проверялось | Вердикт сверки |
|---|---|---|---|---|
| 1 | `N4` (находка) | [02_gasuns-dhatu-PhD-text2.mdx:3231](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx#L3231) | «Рисунок 1 Соотношение количества корней к словарным статьям 25» в списке иллюстративного материала | **Подтверждено.** Поиск по всей рукописи дает единственное вхождение «Рисунок 1» — саму строку списка. Подписи в основном тексте нет (у «Рисунка 2» она есть, строка 1644, `*Рисунок 2.*`). Либо иллюстрация утрачена при рекомпоновке, либо строку списка надо снять. |
| 2 | `N1` (подтверждение) | [02_gasuns-dhatu-PhD-text2.mdx:1370](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx#L1370), Таблица 1 | колонка «Консонантный коэффициент» = C / V построчно | **Сходится вручную:** 212812/159779 = 1,332; 11510/8296 = 1,387; 853340/620385 = 1,376; 3711486/2689255 = 1,380; 500725/384006 = 1,304 — то есть напечатанные 1.33 · 1.39 · 1.38 · 1.38 · 1.30. |
| 3 | сумма колонки (подтверждение) | Таблица 1 против [строки 1361](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx#L1361) | «выборка из 3 861 721 гласного (V) и 5 289 873 согласных (C)» | **Сходится вручную:** 159779 + 8296 + 620385 + 2689255 + 384006 = 3 861 721; 212812 + 11510 + 853340 + 3711486 + 500725 = 5 289 873. Проза и таблица описывают одну и ту же выборку. |

Дополнительно сверено: `N2` — «590 из 935 корней Уитни (63,1 %)»,
590/935 = 63,10 %; `N5` — 60 из 77 числовых фактов провенанс-джейсонов
2026 г. найдены в рукописи и закреплены за локусами в
[numbers_anchor_map.json](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/numbers_anchor_map.json).

## Что эти прогоны НЕ означают

- Это **не** объявление заморозки. Рабочая дата 31-10-2026 объявляется чеклистом
  [NESTOR_ISTORIA_M03_PRESS_READINESS_CHECKLIST.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/NESTOR_ISTORIA_M03_PRESS_READINESS_CHECKLIST.md)
  только после авторской проверки docx и применения одобренных правок.
- Это **не** правки. Ни один `.mdx` рукописи не изменен; невмешательство
  закреплено тестом
  [tests/test_m03_freeze_harness.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_m03_freeze_harness.py)
  `test_a_full_run_of_both_checkers_leaves_the_manuscript_untouched`.
- 960 находок ГОСТ-прохода — это **классы**, а не 960 независимых решений:
  449 из них — одно правило пунктуации (`X: Y` → `X : Y`), 130 — один артефакт
  конвертации (`--` внутри слова). Реальная работа человека сосредоточена в
  `R1` (76) и `G2` (14).

_Dr. Mārcis Gasūns_
