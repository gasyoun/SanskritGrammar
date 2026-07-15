# Зализняк 1975 — «Morphophonological Classification of Sanskrit Verbal Roots»: цифровое издание и аудит классификации корней

_Created: 15-07-2026 · Last updated: 15-07-2026_

Папка работы: А. А. Зализняк, «Морфонологическая классификация санскритских глагольных
корней» (1975; в репозитории — английская версия статьи) — **научная исследовательская
статья, не учебник**: только глагольные корни (~750, без склонения), исчисление типов
чередования I–IV × ряды чередования (A/I/U/R/L/M/N) × aniṭ/seṭ/veṭ. По жанровой
калибровке трёх моделей Зализняка
([ZALIZNIAK_1975_1978_2004_COMPARISON.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md))
именно **модель 1975 года — предок машинерии Талмуда**: нумерованные морфологические
позиции — инновация 1975-го, которой нет ни в очерке 1978, ни в конспекте 2004; родословная
*Уитни (описывает) → Зализняк (абстрагирует) → Толчельников (порождает)* проходит через эту
статью. Исходники —
[A. Zalizniak Morphophonological Classification (English).mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/A.%20Zalizniak%20Morphophonological%20Classification%20(English).mdx)
(читательская страница сайта, ~497 строк) и `.docx`; журнал изменений —
[CHANGELOG.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/CHANGELOG.md).

## Что уже исследовано (существующие слои)

### Слой 1 — профиль квантификаторов метаязыка (H800)

[quantifiers.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/quantifiers.yml)
→ [QUANTIFIER_PROFILE.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/QUANTIFIER_PROFILE.md)
(`npm run quantifiers`): **254 квантификатора** в прозе статьи. Отличительный итог H800 —
**тип якоря**: у статьи 1975 года ~90 % квантификаторов висят на собственном формальном
исчислении (тип 48 % + позиция 16 % + ряд 15 % + ступень 11 %) и лишь 2 % — на §-ссылках;
это квантификаторный отпечаток линии «описать → абстрагировать → породить» на её среднем
звене: не параграфы грамматики, а клетки исчисления.

### Слой 2 — три модели Зализняка (1975 / 1978 / 2004)

По [сравнению трёх моделей](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md):
1975 — **verb-only исследовательская статья** с исчислением типов корней I–IV — центральной
примитивой, которую 1978 заменяет перекрёстными осями, а 2004 не имеет вовсе; инвентарь
~750 корней (2004 несёт ≈218 куррированных, 1978 — ни одного). Кроссволк морфоклассов
1975↔2014↔2026 — [morphoclass_crosswalk_1975_2014_2026.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv)
(колонки 1978 в нём НЕТ — это открытый инструмент, блокирующий OCH-21..OCH-23 очерка).

### Слой 3 — аудит классификации корней (H797, четвёртый жанр верификации)

Жанровая проверка перед стартом (правило программы после кнауэровской развилки) показала:
фальсифицируемая единица статьи — не корпусно-частотная проза (жанр Кочергиной / Бюлера /
очерка / конспекта) и не разбор сноски (жанр Кнауэра), а **СЧЁТ корней по клеткам
классификации** против перечислимого инвентаря Уитни (~750–847 корней). Постановление
автора: строить классификатор (не пропускать и не сводить к пилоту). Итог (PR
[#202](https://github.com/gasyoun/SanskritGrammar/pull/202), Sonnet 5 `claude-sonnet-5`):

- [build_root_classifier.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/build_root_classifier.py)
  → [root_classifier.json](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/root_classifier.json) —
  **~180 корней, явно названных в самой статье, оцифрованы** в структурную форму (namеренно
  НЕ независимая фонологическая ре-деривация: научные суждения Зализняка не переигрываются);
- сводка — [ROOT_CLASSIFICATION_AUDIT.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/ROOT_CLASSIFICATION_AUDIT.md);
- **сверка существования корней: 93 % (208 из 224 цитирований) найдены** в независимом
  структурном инвентаре [WhitneyRoots/crosswalk/roots.csv](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/roots.csv)
  (930 записей) — после нормализации транслитерационной конвенции ç/ṁ ↔ ś/ṃ (до
  нормализации — лишь 82 %: конвенция, а не данные);
- **объяснённые несовпадения** — квази-корни (chay, hvay, çvay, vay — по определению
  отсутствуют в списке первичных корней Уитни), различия цитатной ступени (spardh у
  Зализняка ↔ spṛdh у Уитни; krap ↔ kṛp — сам Зализняк оговаривает это в сноске),
  слияние вариантов (manth/math);
- **три пункта оставлены открытыми честно, не дозакрыты силой:** 9 подлинно ненайденных
  корней (med, kṣaṇ, randh, sañj, granth, aṁç, añc, hvā, bhraç — возможно, подстатьи других
  заглавных корней Уитни), арифметика Табл. 5 (aniṭ/seṭ ≈ 590 — непроверяема без размера
  несчитанного класса корней на -ā) и разрыв 847-vs-930 в размере инвентаря Уитни. Нужен
  санскритолог и/или оригинальное приложение Уитни 1885 года.

**Статус в программе:** инфраструктурный проход, НЕ вердикт-реестр — планка «≥ N
проверенных» к этому жанру не применяется (постановление зафиксировано в
[H797](https://github.com/gasyoun/Uprava/blob/main/handoffs/H797-Fable_SanskritGrammar_claim-verification-backlog-verify-and-cross-grammar-generalise_12.07.26.md)).
С этим проходом закрыт пятый — последний — источник программы: итог по всем пяти книгам —
**942 проверенных утверждения + 214 аудированных разборов + классификатор корней**;
у Зализняка по трём его текстам — ни одного фактического флага.

### Как воспроизвести

```bash
python ZalizniakMorphology_1975/build_root_classifier.py   # реестр корней + сверка с WhitneyRoots
npm run quantifiers                                         # перегенерация QUANTIFIER_PROFILE.md
```

Требуется соседний клон [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots)
(`crosswalk/roots.csv`).

### Что дальше

Три открытых пункта аудита (санскритолог / приложение Уитни 1885); ~~колонка 1978 в
кроссволке~~ — ПОСТРОЕНА 15-07-2026 (H978, [crosswalk_1978.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/crosswalk_1978.csv), OCH-21..23 подтверждены); сверка ~180 оцифрованных
корней с каталогом Приложения 1 Талмуда (ряд/тип/seṭ) — прямой тест преемственности
1975 → 2026 на уровне данных.

_Dr. Mārcis Gasūns_
