# Зализняк 1978 — «Грамматический очерк санскрита»: цифровое издание и исследовательские слои

_Created: 15-07-2026 · Last updated: 15-07-2026_

Папка книги: А. А. Зализняк, «Грамматический очерк санскрита» (приложение к
«Санскритско-русскому словарю» В. А. Кочергиной, М., 1978) — **очерк**, а не полная
грамматика: сжатый обзор всего языка на ~242 §§ (жанровая калибровка по Уитни 1889 — в
[ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md)).
Исходники — [Zalizniak-Ocherk_29-11-20-aligned.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx)
(читательская страница сайта, 3 128 строк, из них ~420 — грамматическая проза) и
`.doc`/`.docx`; система опечаток —
[errata.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/errata.yml)
(пока пуст — ждёт печатного листа) →
[ERRATA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/ERRATA.md);
журнал изменений — [CHANGELOG.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/CHANGELOG.md).
Написание фамилии в латинице — **Zalizniak** (i-написание: так автор процитирован в
опубликованной статье Толчельникова; решение D2, 10-07-2026).

## Что уже исследовано (существующие слои)

### Слой 1 — профиль квантификаторов метаязыка (H800)

Реестр всех градационных слов очерка («редко», «обычно», «только», «некоторые»,
«всегда»…): [quantifiers.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/quantifiers.yml)
→ генерируемый [QUANTIFIER_PROFILE.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/QUANTIFIER_PROFILE.md)
(`npm run quantifiers`), с ручной калибровочной выборкой
[quantifiers.sample.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/quantifiers.sample.yml).
Числа очерка: **832 квантификатора** в грамматической прозе, плотность **1,98 на строку**;
заякоренность по авто-прокси 51,8 % в окне ±8 токенов (83,7 % при ±25 — уровень,
подтверждённый ручной проверкой в H800); тип якоря — **§ 46 % + аффикс 34 %**:
квантификаторы очерка висят на формальном аппарате параграфов, а не «ни на чём».
Межкнижный вывод H800: интуиция «у Зализняка заякорено, у Кочергиной висит в воздухе»
**опровергнута** — заякоренность у всех трёх описательных грамматик близка (~83–88 %);
различают их плотность и *тип* якоря.

### Слой 2 — три модели Зализняка (1975 / 1978 / 2004)

[ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md):
Зализняк описал санскрит трижды — каждый раз **другой парадигмой**. Хребет очерка 1978 —
двухуровневая запись I/II (глубинное/поверхностное), которой нет ни в статье 1975, ни в
конспекте 2004; нумерованных морфологических позиций 1975 года очерк не имеет, корневого
инвентаря — тоже. Родословная: Уитни *(описывает)* → Зализняк *(абстрагирует)* →
Толчельников-Талмуд 2026 *(порождает)* — причём машинерия Талмуда наследует модели
**1975** года, а не очерку 1978, на который указывает наш §-конкорданс.

### Слой 3 — связи с другими грамматиками (H786)

По [карте связей десяти грамматик](https://github.com/gasyoun/SanskritGrammar/blob/main/GrammarRelations/grammar-relations-map.mdx):
зависимость пары Очерк-1978 ↔ Кочергина-1998 **односторонняя** — Кочергина рекомендует
очерк (отсылка к § 34 в «Заключении» учебника), Зализняк же цитирует только «Начальный
курс» 1956 года; при этом конвенции двух книг систематически расходятся по 7 признакам.

## Проверка утверждений (реестр `claims.yml`) — В ОЧЕРЕДИ

Реестра у очерка **ещё нет**: это оставшаяся книга фазы 2
[H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md)
(после Кочергиной — 234 проверенных, Бюлера — 64, и развилки Кнауэра). **Предварительная
проверка жанра — урок кнауэровской развилки — здесь выполнена:** очерк дискурсивен
(832 квантификатора на ~420 строк прозы, ~242 §§), стандартный двухосевой конвейер
(факт × подача против DCS-2021 / Уитни / Талмуда) применим как есть, планка «≥ 50
проверенных» реалистична. Методику см. в README соседей:
[Кочергина](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/README.md) ·
[Бюлер](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/README.md) ·
[Кнауэр](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/README.md).

### Как воспроизвести числа

```bash
npm run quantifiers        # перегенерация QUANTIFIER_PROFILE.md + quantifiers.json
python scripts/grammar_relations_stats.py   # статистика карты связей (SG-H2/SG-H9)
```

### Что дальше

Реестр `claims.yml` + `claims_harvest.yml` по конвейеру H797 (жатва параллельными
читателями → вердикты → ≥ 50 проверенных → синтез); печатный лист опечаток для
`errata.yml`; закрытие открытого `@DECIDE` по окну якоря N=8 квантификаторного слоя.

_Dr. Mārcis Gasūns_
