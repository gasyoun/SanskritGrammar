# Толчельников 2026 — «Талмуд»: порождающая морфонология глагола и издательский хаб

_Created: 15-07-2026 · Last updated: 17-10-2026_

Папка живой книги: Толчельников, «Талмуд» (2026) — современное **порождающее** описание
глагольной морфонологии санскрита (система Ряд / Тип / seṭ), наследующее модели
Зализняка **1975** года (не очерку 1978 — см.
[ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md)):
родословная *Уитни (описывает) → Зализняк (абстрагирует) → Толчельников (порождает)*.
Непанинианский подход опубликован: доклад «A Non-Paninian Approach to Sanskrit
Morphonology» (Ауровиль, февраль 2024) — в
[papers/Auroville_Feb2024](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/papers/Auroville_Feb2024).

## Состав папки

- **Текст книги:** полный
  [Talmud-2.1.6.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/Talmud-2.1.6.mdx)
  (+ уроки [Talmud-uroky.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/Talmud-uroky.mdx))
  и 14 поглавных читательских страниц `talmud-00…talmud-13` (введение · смысл-текст ·
  чередование · соединительная i · редупликация · saṃprasāraṇa · межрядовой переход ·
  сандхи · алгоритм · глагольная система …) с интерактивными виджетами: `AblautMachine`
  (ряды аблаута) и `SandhiCollider`, с 14-07-2026 показывающий **корпусные частоты
  сандхи** из kosha (наведение → правило + ранг «#N most common» из 9 840 стыков; H917).
- **Лестница для начинающих:**
  [onramp/](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp)
  (H915) — вход в систему Ряд/Тип/seṭ *ниже* уровня книги, 3 шага с переходами «на
  один тап глубже» в полные главы; дизайн —
  [ZALIZNYAK_ONRAMP_DESIGN.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/ZALIZNYAK_ONRAMP_DESIGN.md).
- **Издательский хаб:**
  [papers/](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/papers)
  — статьи и конференции вокруг линии Зализняк→Талмуд: A60 «что грамматики утверждают,
  а корпус не подтверждает», A62 «повестка цифровой санскритской педагогики», A63
  «сложность и порядок изучения», пакет WSC-2027 (Мумбаи, 13 глав), разбор доклада
  Куликова 2025, Ауровиль-2024 и др.
- **Аппарат:** [CHANGELOG.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/CHANGELOG.md)
  (постоянное правило автора 08-07-2026: **каждое** изменение Талмуда — текст, данные,
  виджеты — получает запись в тот же проход, молчаливых правок нет);
  [errata.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/errata.yml)
  (пуст); [IMPROVEMENT_PLAN.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/IMPROVEMENT_PLAN.md);
  [student-roadmap.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/student-roadmap.md);
  §-конкорданс с Зализняком —
  [zalizniak-concordance.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/zalizniak-concordance.mdx);
  `data/`, `chunks/`, `footnote-proposals/`.

## Данные: семантика строк crosswalk (H6352-r1, 17-10-2026)

[`data/morphoclass_crosswalk_1975_2014_2026.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv)
— **876 строк на 749 различных корней Уитни**: строка здесь = одна запись
Z-реестра (Толчельников v1.1.0), а не один корень. Это зафиксировано в
[GasunsDhatu_2014/CHANGELOG.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/CHANGELOG.md)
(охват 749/930, утверждён автором) и в отчёте Q3.4; потребители с этим живут
осознанно — [`och22_token_weighted.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/och22_token_weighted.py)
прямо разрешает дубли по индексу ряда и требует согласия `polnoizm_1978`.

Три класса повторов — **не** дефект и **не** подлежат удалению строк:

1. **24 пары, различающиеся только `z_url`** (пример — `372,dṛ,2,heed`, z_id
   613 и 939). Это две РАЗНЫЕ записи Z-реестра с общими `z_series`/`z_set`, но
   разными `z_pres_class`/`z_aorist` (613: 2,9 / 2,3,4,5,6; 939: 1 / 1,3,4) —
   crosswalk эти два поля не проецирует, поэтому строки выглядят байт-дублем.
   Спот-чек H5685 прочитал это как «дубль-строку»; проверка H6352-r1 показала,
   что удаление потеряло бы отдельную Z-запись и её ссылку.
2. **82 группы с расходящимся `z_series`** — конкурирующие разборы одного корня,
   сохранены намеренно (их считают `q34_three_scheme_agreement.py` и OCH-22).
3. **Омонимы Уитни** (`aś` attain/eat, `ci` gather/observe, `vṛ` cover/choose) —
   отдельные строки по построению.

Поэтому «дедуп» не выполняется: файл читается как 876 записей / 749 корней, а
не как 876 корней.

## Роль в программе проверки утверждений — опора, не мишень

В отличие от пяти исторических грамматик
([Кочергина](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/README.md) ·
[Бюлер](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/README.md) ·
[Кнауэр](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/README.md) ·
[очерк 1978](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/README.md) ·
[конспект 2004](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakKonspekt_2004/README.md)),
Талмуд стоит **по другую сторону конвейера** — он корпусно-осведомлён и служит опорой:

1. **Авторитет морфокласса корня (правило D-B).** В триангуляции DCS (частотность) ·
   Уитни (системный факт) · **Талмуд (морфокласс)** — Талмуд решает принадлежность
   корня классу, прежде всего оси **seṭ/aniṭ**.
2. **Ось seṭ/aniṭ — несущая для главного вывода реестров.** Флагманское число конвейера
   (seṭ-футурум **-iṣya = 56,8 %** различных форм — скрытое большинство у Кочергиной,
   корректно поданное Бюлером) обусловлено именно лексическим классом seṭ/aniṭ, который
   Талмуд систематизирует; aniṭ-список Бюлера (HB-43, ~75 корней) сверялся по этой оси.
3. **Питает статью A60** — подмножество OVERSTATED/FALSE обоих реестров собирается в
   [papers/GrammarClaimsCorpusDenies_A60](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/papers/GrammarClaimsCorpusDenies_A60)
   (центральная таблица: 12 расхождений Кочергиной; Q2 разблокирован вторым реестром).

### Что дальше

Дренаж бэклогов реестров и реестр Зализняка (остаток H797, фаза 2) продолжают питать
A60; педагогическая линия — оценка onramp по RQ4 повестки A62; наполнение errata.yml
по мере вычитки; сандхи-поверхности фазы 4 (осталась 1 из 4 — тренажёры).

_Dr. Mārcis Gasūns_
