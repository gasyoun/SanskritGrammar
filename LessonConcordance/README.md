# LessonConcordance — поурочный конкорданс Бюлера (урок × все источники)

_Created: 01-10-2026 · Last updated: 01-10-2026_

Для каждого урока [Бюлера-1923](https://gasyoun.github.io/SanskritGrammar/grammars/BuhlerLeitfaden_1923/Buhler_Unicode/)
(48 уроков) и каждой темы внутри него — связи с локусами всех остальных
оцифрованных источников сайта. Зерно связи «урок+тема» (голос MG D2),
лемма-слой для проверки полноты грамматик, per-topic вердикты по гипотезе
об исключениях. План и решения D1–D16:
[BUHLER_LESSON_CONCORDANCE_PLAN_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BUHLER_LESSON_CONCORDANCE_PLAN_2026.md);
пилот — хендофф
[H5595](https://github.com/gasyoun/Uprava/blob/main/handoffs/H5595-OxAlpha_SanskritGrammar_buhler-lesson-concordance-pilot_01.10.26.md).

## Слои

- [typed_link_buhler_lessons.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/LessonConcordance/typed_link_buhler_lessons.tsv) —
  Type-D датасет (10 колонок по
  [TYPED_LINK_ID_GRAMMAR.md](https://github.com/gasyoun/Uprava/blob/main/TYPED_LINK_ID_GRAMMAR.md) §1;
  anchor `buhler-topic:<урок>.<тема>`, target — локус источника: `whitney-sec`, `kochergina-lesson`,
  `knauer-fraza`, `zalizniak-1978-sec`, `sangram-article`, `dhatu`, `talmud`, …).
  Линт: [kosha typed_link_lint.py](https://github.com/gasyoun/kosha/blob/main/scripts/typed_link_lint.py) — 0 ошибок обязательно.
- [topics.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/LessonConcordance/topics.yml) —
  контролируемый словарь тем (версионируется, D13), вердикты об исключениях с цитатами локусов,
  лемма-таблица урока (корень × З-1975 × З-1978 × crosswalk-покрытие).
- [catalog.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/LessonConcordance/catalog.mdx) —
  сгенерированная студенческая страница (генератор, не руки).

## Указатели на существующие регистры (D3 — индекс, не дубль)

Посев и обратные ссылки: [claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml)
(HB-утверждения урока), [Concordance/catalog.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx)
(общие предложения), [corpus_layer.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/corpus_layer/corpus_layer.tsv)
(леммы с DCS-частотами), [WHITNEY_CONCORDANCE_SANGRAM_KOCHERGINA_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/WHITNEY_CONCORDANCE_SANGRAM_KOCHERGINA_2026.md)
(свидетельские вердикты). В kosha-манифест датасет не регистрируется до Q2.1 unified release (прецедент D2b).

## Транспорт

Один урок = один дренажный проход (хендофф); DoD — план-док § «Definition of Done».
Автопроверка гипотезы об исключениях: вердикт по каждой теме копится в topics.yml.

_Гасунс_
