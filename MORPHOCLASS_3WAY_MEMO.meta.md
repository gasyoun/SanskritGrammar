# Метадок — MORPHOCLASS_3WAY_MEMO.md

_Created: 08-07-2026 · Last updated: 08-07-2026_

Документ *о* записке
[`MORPHOCLASS_3WAY_MEMO.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.md).

## Назначение и аудитория

- **Что это.** Внутренняя сопроводительная записка (companion), отвечающая на вопрос МГ:
  как «Талмуд санскрита» Толчельникова (2026) развивает морфонологическую классификацию
  Зализняка (1975), с диссертацией Гасунса (2014) как средним звеном.
- **Аудитория.** МГ (внутренне) + база для сносок-предложений автору (И. Е. Толчельников).
  **Не статья** — публикация пока не планируется (решение МГ, 08-07-2026).

## Провенанс

- Проход **H357** ([handoff](https://github.com/gasyoun/Uprava/blob/main/handoffs/H357-Opus_SanskritGrammar_morphoclass_3way_comparison_08.07.26.md)),
  модель **Opus 4.8 (`claude-opus-4-8`)**. Спека —
  [`MORPHOCLASS_COMPARISON_ROADMAP.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_COMPARISON_ROADMAP.md).
- Первоисточники (полные тексты в репозитории): 1975 англ. перевод, Гасунс 2014
  морфонологическая запись, Талмуд гл. I–III + `zalizniak-concordance` + база `/z/` (H329).
- Парная ось (внутризализняковская, 1975/1978/2004) — не переоткрывается, берется из
  [`ZALIZNYAK_1975_1978_2004_COMPARISON.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNYAK_1975_1978_2004_COMPARISON.md).

## Ключевые находки (ранжировано)

1. **Аппарат Талмуда наследуется целиком из статьи 1975 г.**, а не из «Очерка» 1978 г.:
   позиции 1/2/3, типы, порождение по рядам — это 1975.
2. **Инвертированная нумерация позиций** (1975: 1=нуль…3=вриддхи; Талмуд: 1=вриддхи…3=слабая).
3. **`0`-ряды `/z/` — баг реализации Широбокова** (issue #50), не категория; исправлена
   ошибочная атрибуция в парном документе.
4. **Типы `s/a/v` ≠ типы `I–IV` поклеточно** — переименованы и переопределены операционально.
5. **Линия развития veṭ**: Зализняк «словами» → Гасунс схематизирует → Толчельников
   встраивает в алгоритм.
6. Единственное содержательное авторское расхождение с 1975 в выборке — `kṣar` (R₁ vs R₂).

## Backlog улучшений записки

| # | Пункт | Статус |
|---|---|---|
| 1 | Расширить покорневую выборку § 5 за пределы ~10 переякоренных корней (нужен полный проход по типам I–IV Таблицы 4 1975 г.) | open |
| 2 | Свести тип-мэппинг `s/a/v/v1..v4` ↔ `I/II/III/IV` в отдельную формальную таблицу соответствий по клеткам позиций | open |
| 3 | Дождаться ответов автора по FN-0015…FN-0017 и внести решения в § 6 | @WAITING (Иван) |
| 4 | При решении публиковать — конвертировать в `.mdx` для сайта (правило mdx-only) | deferred (пока не статья) |

## Связанные документы

- [`MORPHOCLASS_COMPARISON_ROADMAP.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_COMPARISON_ROADMAP.md) — спека.
- [`ZALIZNYAK_1975_1978_2004_COMPARISON.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNYAK_1975_1978_2004_COMPARISON.md) — парная (внутризализняковская) ось.
- [`TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv) — машинный джойн 876 корней.
- [`TolchelnikovTalmud_2026/footnote-proposals/proposals.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/footnote-proposals/proposals.yml) — FN-0015…FN-0017.
- [`TolchelnikovTalmud_2026/data/z_reconciliation_report.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/z_reconciliation_report.md) — сверка `/z/` (H329).

## История правок subject-документа

| Дата | Изменение | Автор |
|---|---|---|
| 08-07-2026 | Создан (проход H357): записка + категориальный и покорневой кросс-уок + CSV + FN-0015…0017 | Opus 4.8 (`claude-opus-4-8`) |

_Dr. Mārcis Gasūns_
