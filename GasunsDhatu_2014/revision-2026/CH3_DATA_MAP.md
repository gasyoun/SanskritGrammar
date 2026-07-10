# CH3_DATA_MAP — какие 2026-данные есть для Главы 3

_Created: 11-07-2026 · Last updated: 11-07-2026_

Короткая карта готового 2026-слоя для Гл. 3 «Строй корня и способы
морфонологической записи» ([02_gasuns-dhatu-PhD-text2.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/02_gasuns-dhatu-PhD-text2.mdx),
Гл. 3 -- от `# Глава 3`). Составлена по корректировке 1 памятки
[CH2_PILOT_MEMO.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/CH2_PILOT_MEMO.md)
(«перед Гл. 1/3 завести список, какие 2026-данные вообще есть») перед
переработкой главы по [H378](https://github.com/gasyoun/Uprava/blob/main/handoffs/H378-Opus_SanskritGrammar_gasuns-dhatu-ch3-monograph-rework_08.07.26.md).
Исполнитель: Opus 4.8 (`claude-opus-4-8`).

## Готовые входы

| # | Источник | Что даёт Гл. 3 | Куда слито |
|---|---|---|---|
| 1 | [ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md) (12 осей, калибровка против грамматики Уитни 1889 г.; H357) | постатейная атрибуция трёх работ Зализняка; линия Уитни→Зализняк→Толчельников; полной грамматики среди трёх нет | §3.2 (осн. текст) + сноска `[^ed3b]` |
| 2 | [morphoclass_crosswalk_1975_2014_2026.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv) (876 корней: `ryad_derived` = ряд «Талмуда», `z_series` = ряд Зализняка) | покорневое совпадение инвентаря рядов «Талмуда» и Зализняка 1975 г. | §3.2 + решение по Таблице 9 (`[^ed3c]`) |
| 3 | [issue #50](https://github.com/gasyoun/SanskritGrammar/issues/50) -- виза автора И. Е. Толчельникова | рядов `I₀/M₀/N₀/R₀/U₀` не существует: артефакт обработки Таблицы 2 в базе `/z/` | §3.2: **отменяет** премиссу DO#3 хендоффа (см. ниже) |
| 4 | [whitney_talmud.json](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/whitney_talmud.json) (930 глагольных корней) + [zalizniak-concordance.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/zalizniak-concordance.mdx) | машинный корнеслов «Талмуда» = список Уитни целиком | контекст §3.2 (не пересчитывался) |
| 5 | [MORPHOCLASS_COMPARISON_ROADMAP.md](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_COMPARISON_ROADMAP.md) | terminology trap: аблаутный **Ряд A–N** ≠ **ряды согласных (варги)** | соблюдено (DO NOT) -- в §3.2 везде «ряды чередования» |
| 6 | [RWS_REPORT.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/RWS_REPORT.md) -- Гл. 3: **269 замечаний (129 major/critical)**, максимум по книге | стилистика §3.1/§3.3 (IAST при первом упоминании, authority chain, ссылки на сутры) | **вне объёма H378** -- отдельный стилевой проход (как §2.1–§2.2 для Гл. 2) |
| 7 | Существующие 2026-сноски в Гл. 3: `[^edt1]`, `[^edt4]`, `[^edt5]`, `[^edl9a]` (пересчёты H246/H328) | вычислительные результаты уже верифицированы | **НЕ трогать** (DO NOT) |

## Расхождение хендоффа с H357 (зафиксировано)

H378 (сминчен 08-07-2026) в DO#3 предписывал записать, что 0-подстрочные ряды
`I₀/M₀/N₀/R₀/U₀` -- «собственное расширение Толчельникова, ни в одной из трёх работ
Зализняка их нет». H357 (COMPARISON.md обновлён 09-07-2026, **после** минта хендоффа,
п. 3) это **опроверг**: ряды -- баг обработки Таблицы 2 в базе `/z/` (115 строк модели
А. П. Широбокова), подтверждено самим автором на [issue #50](https://github.com/gasyoun/SanskritGrammar/issues/50);
инвентарь рядов одинаков во всех трёх работах. Это ровно тот случай, который хендофф и
предусмотрел оговоркой «Depends on H357 -- его кросс-уок прямой источник DO#3/#4».
Исполнено **по H357**, а не по устаревшей букве DO#3; в текст книги баг не внесён.

## Оси, которых для Гл. 3 нет (заделы)

- **Цифрового Пальсуле нет** -- Таблицы 6/7 (структура слога, 3690 корней) цифровым путём
  не переверяемы (как и в Гл. 2, сноска `[^ed24a]`); не пересчитывались.
- **Полная сверка Таблицы 9 против оригиналов Зализняка/Моргенрота построчно** (все 15
  строк) не делалась -- проверялось совпадение *инвентаря* рядов, не каждая ячейка.
- Гигиена: сноска `[^ed24c]` в §2.4 ссылается на файл с написанием `ZALIZNYAK_…` (через
  `Y`), тогда как файл в репозитории -- `ZALIZNIAK_…` (через `I`): ссылка ведёт в 404.
  Правка -- вне объёма H378 (Гл. 2 не трогаем, DO NOT); новые сноски Гл. 3 используют
  верное написание. Заведено как follow-up.

_Dr. Mārcis Gasūns_
