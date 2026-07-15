# Кочергина 1998 — «Учебник санскрита»: цифровое издание и корпусная проверка утверждений

_Created: 15-07-2026 · Last updated: 15-07-2026_

Папка книги: В. А. Кочергина, «Учебник санскрита» (М., 1998), 40 занятий. Исходники —
[Kochergina_unicode.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/Kochergina_unicode.mdx)
(читательская страница сайта, 15 756 строк) и `.docx`; система опечаток —
[errata.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/errata.yml) →
[ERRATA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/ERRATA.md)
(пока пуст — ждёт печатного листа опечаток); журнал изменений —
[CHANGELOG.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/CHANGELOG.md).
Смежные слои папки: реестр квантификаторов метаязыка
[quantifiers.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/quantifiers.yml) →
[QUANTIFIER_PROFILE.md](https://github.com/gasyoun/SanskritGrammar/blob/main/QUANTIFIER_PROFILE.md)
(исследование градационного метаязыка —
[GRADATION_METALANGUAGE_KOCHERGINA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/GRADATION_METALANGUAGE_KOCHERGINA.md))
и план печатной методички-компаньона
[METODICHKA_KOCHERGINA_COMPANION_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md).

## Реестр проверенных утверждений (H768 → H797, фаза 1)

Пилотная книга двухосевого конвейера проверки утверждений — здесь метод был построен
(H768, 12-07-2026), доведён до полного дренажа (H797, фаза 1) и отсюда перенесён на
Бюлера ([BuhlerLeitfaden_1923/README.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/README.md),
фаза 2). Каждое фальсифицируемое грамматическое утверждение учебника оценивается по
**двум осям**:

- **verdict_fact** — истинно ли утверждение относительно корпуса и справочных грамматик,
  с конкретным числом: `TRUE · OVERSTATED · FALSE · UNTESTABLE`;
- **verdict_pedagogy** — оправданна ли *подача* (порядок изложения, выдвижение редкого как
  центрального, сокрытие частотности): `JUSTIFIED · MISLEADING · RARE-AS-CENTRAL ·
  FREQUENCY-HIDDEN · ORDER-QUESTIONABLE`.

Опорная триангуляция: **DCS-2021** (частотность/засвидетельствованность; Оливер Хельвиг,
CC BY, через соседний репозиторий VisualDCS), **Уитни 1889** (системный грамматический
факт, по §§), **Толчельников-Талмуд 2026** (морфокласс корня). При конфликте источников
действует правило D-B: DCS решает частотность, Уитни — системный факт, Талмуд —
морфокласс; расхождение флагуется, никогда не замалчивается.

Файлы реестра:

- [claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.yml) — верифицированный реестр (HK-1..HK-233; HK-4 расщеплён на 4a/4b), источник правды;
- [claims_harvest.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims_harvest.yml) — бэклог жатвы, **полностью выработан** (223 кандидата собраны 6 параллельными читателями по всем 40 занятиям, все продвинуты; `candidates: []`);
- [CLAIMS_VERIFIED.md](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/CLAIMS_VERIFIED.md) + [claims.json](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.json) — генерируются из `claims.yml` скриптом [scripts/build_claims.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_claims.py) (`npm run claims`), руками не править;
- [verify_claims_dcs.py](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/verify_claims_dcs.py) — воспроизводимая батарея корпусных запросов (она же общая батарея кросс-грамматического слоя);
- [CLAIMS_OVERLAY.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/CLAIMS_OVERLAY.mdx) — русская страница-оверлей читательского сайта (компонент [KocherginaClaims.jsx](https://github.com/gasyoun/SanskritGrammar/blob/main/src/components/KocherginaClaims.jsx)); текст 1998 года под охраной авторского права, оверлей несёт только нашу верификационную метадату.

## Итог проверки: 234 утверждения

**210 TRUE · 11 OVERSTATED · 1 FALSE · 12 UNTESTABLE · 11 частотных сносок М.Г. ·
24 записи с флагом (факт или подача).**

### Главные выводы

1. **Фактическая точность Кочергиной высока** — подавляющее большинство утверждений
   подтверждается корпусом DCS-2021 и Уитни. Её сбои — почти никогда не ошибки факта,
   а ошибки **калибровки**: петербургско-советская традиция полноты парадигмы даёт
   каждой форме правило и исключения в порядке системы — и это же порождает два
   систематических типа сбоя.
2. **Тип 1 — сверхобобщение универсалий.** Правило для начинающих формулируется с
   абсолютным квантификатором («всегда», «только», «никогда», «по единому правилу»)
   там, где существует известный класс исключений. Самый острый случай — единственный
   **FALSE**: «основы на -ī и -ū всегда женского рода» (HK-16) — мужские основы на ī/ū
   хорошо засвидетельствованы (rathī, senānī, sudhī, односложное bhū-); имелся в виду
   производный класс nadī/vadhū. Тот же тип: «личная форма глагола никогда не несёт
   ударения» (HK-10 — несёт в придаточном, Уитни §168), род бахуврихи «всегда» по
   последнему члену (HK-14/HK-34 — противоречит её же занятию), простой перфект «от
   всех односложных» (HK-25), корневой аорист «от некоторых корней на -ā и bhū» (HK-38 —
   класс много шире), порядок двойных превербов «всегда» (HK-40).
3. **Тип 2 — слепота к частотности.** Каноническое «базовое правило» выдвигается вперёд
   статистически господствующей реализации. Шаблонный случай — будущее время: «-syá по
   единому правилу», тогда как seṭ-форма **-iṣya — большинство: 56,8 %** из 2 618
   различных форм будущего (HK-4, FREQUENCY-HIDDEN). Рядом: имперфект «обычно»
   повествовательное прошедшее (HK-15 — зависит от жанрового пласта; в агрегате DCS
   перфект частотнее), IX класс «большинство — носовой + согласная» (HK-19), HK-26,
   HK-32.
4. **Честная зона UNTESTABLE.** Точные проценты, заявленные без указания базы счёта,
   не воспроизводимы и помечены, а не приняты на веру: семантическое членение
   приставочных глаголов 60/30/<10 % (HK-41), a-privativum «≥ 1/3 приставочных имён,
   ~80 % абстрактные» (HK-42).
5. **Где корпус может судить частотное утверждение — он чаще всего её оправдывает:**
   кондиционалис «сравнительно редко» = 0,03 % глагольных словоупотреблений (HK-23),
   средний прекатив «крайне редко» = 0,03 % (HK-39), императив «наиболее часто 2-е
   лицо» = 63 % различных форм (HK-17), аорист «лишь от части корней… редко» = 0,31 %
   (HK-1).
6. **Кросс-грамматический контроль (фаза 2).** То же корпусное число — -iṣya 56,8 % —
   оценивает формулировку Кочергиной как OVERSTATED, а хеджированную формулировку
   Бюлера как TRUE (HB-59): с двумя живыми реестрами измеримой осью различия грамматик
   оказывается **калибровка подачи, а не фактическая точность**. Разбор — в
   [BuhlerLeitfaden_1923/README.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/README.md).
7. **Сноски М.Г. добавляют корпусные числа, которых в 1998 году не было:** гласные a+ā —
   65,8 % всех монофтонгов корпуса, ṛ в 126 раз частотнее редких сонантов ṝ/ḷ/ḹ
   (HK-7/HK-8); тематические классы (I/IV/VI/X) — 70,2 % словоупотреблений системы
   настоящего времени, один II класс — 20,1 % (HK-18); причастие на -na — 8,0 %
   инвентаря причастий на -ta/-na (HK-29); и далее по реестру.

Рекомендация для читательского оверлея (из методологического синтеза
[claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.yml)):
текст Кочергиной сохранять как есть — он точен; бейджировать два типа сбоя — у
FALSE/OVERSTATED-универсалий показывать класс-контрпример, у частотно-скрытых
утверждений — корпусное число, чтобы учащийся видел, где у абсолютного правила есть
лазейка и где «вариант» на деле норма.

Подмножество OVERSTATED/FALSE питает статью A60 («что грамматики утверждают, а корпус
не подтверждает»); история — H768 ([PR #119](https://github.com/gasyoun/SanskritGrammar/pull/119),
[PR #134](https://github.com/gasyoun/SanskritGrammar/pull/134),
[PR #135](https://github.com/gasyoun/SanskritGrammar/pull/135)) и H797 фаза 1
([PR #150](https://github.com/gasyoun/SanskritGrammar/pull/150), релиз
[kochergina-uchebnik-v0.3.0](https://github.com/gasyoun/SanskritGrammar/releases/tag/kochergina-uchebnik-v0.3.0)).

### Как воспроизвести числа

```bash
python KocherginaUchebnik_1998/verify_claims_dcs.py --check   # батарея корпусных запросов (HK-* и HB-*)
npm run claims                                                 # перегенерация CLAIMS_VERIFIED.md + claims.json
npm run quantifiers                                            # слой квантификаторов метаязыка
```

Требуется соседний клон VisualDCS (`../VisualDCS`, экспорт DCS-2021).

### Что дальше

Бэклог книги выработан полностью; продолжение конвейера — кросс-грамматический слой
(Бюлер ✅, далее Кнауэр и Зализняк, см. H797, фаза 2) и печатная методичка-компаньон
(H807), потребляющая этот реестр вместе с системой опечаток.

_Dr. Mārcis Gasūns_
