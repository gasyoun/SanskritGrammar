# Зализняк 2004 — «Конспект грамматических сведений о санскрите»: цифровое издание и исследовательские слои

_Created: 15-07-2026 · Last updated: 15-07-2026_

Папка книги: А. А. Зализняк, конспект грамматических сведений о санскрите (2004) —
**конспект**, а не полная грамматика: весь язык в сжатом изложении (~657 строк) с
заметным диахроническим/индоевропейским планом и куррированным инвентарём ≈218 корней
с и.-е. когнатами (жанровая калибровка по Уитни 1889 — в
[ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md)).
Исходники — [zalizniak-konspekt-2015-11-X_bd_t.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/zalizniak-konspekt-2015-11-X_bd_t.mdx)
(читательская страница сайта; грамматической прозы ~65 строк) и `.doc`/`.docx`; система
опечаток — [errata.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/errata.yml)
(пока пуст — ждёт печатного листа) →
[ERRATA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/ERRATA.md);
журнал изменений — [CHANGELOG.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/CHANGELOG.md).
Написание фамилии в латинице — **Zalizniak** (i-написание; решение D2, 10-07-2026).

## Что уже исследовано (существующие слои)

### Слой 1 — профиль квантификаторов метаязыка (H800)

Реестр градационных слов конспекта:
[quantifiers.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/quantifiers.yml)
→ генерируемый [QUANTIFIER_PROFILE.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/QUANTIFIER_PROFILE.md)
(`npm run quantifiers`), с ручной калибровочной выборкой
[quantifiers.sample.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/quantifiers.sample.yml).
Числа конспекта: **92 квантификатора** в грамматической прозе, плотность **1,42 на
строку**; заякоренность по авто-прокси 50,0 % в окне ±8 токенов (79,3 % при ±40); тип
якоря — **аффикс 63 %** (§-ссылок нет вовсе: конспект, в отличие от очерка 1978, не несёт
собственного параграфного аппарата). Межкнижный вывод H800: заякоренность у трёх
описательных грамматик близка (~83–88 % при ручной проверке); различают их плотность и
*тип* якоря.

### Слой 2 — три модели Зализняка (1975 / 1978 / 2004)

[ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md):
конспект 2004 — **одноуровневый** (без двухуровневой записи I/II очерка 1978 и без
нумерованных морфологических позиций статьи 1975), без буквенного исчисления типов
корней, зато с выдвинутой вперёд диахронией, цифрой презентного класса как тегом корня и
куррированными ≈218 корнями. Родословная: Уитни *(описывает)* → Зализняк
*(абстрагирует)* → Толчельников-Талмуд 2026 *(порождает)*; учебная лестница в систему
Ряд/Тип/seṭ для начинающих — в
[TolchelnikovTalmud_2026/onramp/](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp).

## Проверка утверждений (реестр `claims.yml`) — В ОЧЕРЕДИ, с оговоркой о масштабе

Реестра у конспекта **ещё нет** — он в остатке фазы 2
[H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md).
**Предварительная проверка жанра — урок кнауэровской развилки — здесь выполнена, итог
двоякий:** текст дискурсивен (92 квантификатора — есть что жать, конвейер факт × подача
применим), **но масштаб мал**: ~65 строк грамматической прозы против ~420 у очерка 1978
и тысяч у Кочергиной/Бюлера. Планка «≥ 50 проверенных», заданная для полноразмерных
дискурсивных грамматик, конспекту может не подойти — как и у Кнауэра, меру «сделано»
для него должен определить человек (реалистичнее ожидать десятки кандидатов, не сотни).
Методику см. в README соседей:
[Кочергина](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/README.md) ·
[Бюлер](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/README.md) ·
[Кнауэр](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/README.md) ·
[очерк 1978](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/README.md).

### Как воспроизвести числа

```bash
npm run quantifiers        # перегенерация QUANTIFIER_PROFILE.md + quantifiers.json
```

### Что дальше

Реестр `claims.yml` по конвейеру H797 с планкой, откалиброванной под объём конспекта
(решение человека); печатный лист опечаток для `errata.yml`; закрытие открытого
`@DECIDE` по окну якоря N=8 квантификаторного слоя.

_Dr. Mārcis Gasūns_
