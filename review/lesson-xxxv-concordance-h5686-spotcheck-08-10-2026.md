# H5686 spot-check (свежепроцессная верификация, 08-10-2026)

Независимый процесс (не код build): каждая spot-фраза урока XXXV сверяется grep'ом против файла источника; HB-id — против claims.yml; TSV-строки — против тем topics.yml.

| # | Локус | Фраза | Результат |
|---|---|---|---|
| 1 | kochergina-lesson:XVI | Второе главное спряжение включает шесть классов глаголов: II… | PASS |
| 2 | zalizniak-1978-sec:122 | Распределение сильных и слабых форм одинаково для всего атем… | PASS |
| 3 | knauer-fraza:Nr.12 | yajñeṣv adhvaryavaḥ somaṁ sunvatām… | PASS |
| 4 | sangram-article:thematic-present | атематические классы концентрируются именно в… | EXTERNAL (не валидируется) |
| 5 | kochergina-lesson:XVII | изменяется в основе настоящего времени в śṛ: śṛṇo-/śṛṇu-.… | PASS |
| 6 | kochergina-lesson:XVI | о.н.в. sunu-/sunó-… | PASS |
| 7 | zalizniak-1978-sec:135 | Основа равна корню в слабой ступени + суффикс no/nu… | PASS |
| 8 | knauer-fraza:Nr.12 | paṇḍitaḥ çiṣyebhyaḥ çabdaçāstraṁ vyavṛṇot… | PASS |
| 9 | kochergina-lesson:XII | Мы знакомимся сейчас с глаголами первого спряжения, образующ… | PASS |
| 10 | kochergina-lesson:IV | śṛṇu - слушай!… | PASS |
| 11 | zalizniak-1978-sec:122 | В оптативе между основой (первичной, § 27) и окончаниями выс… | PASS |
| 12 | knauer-fraza:Nr.4 | हे स्वसः पित्रोर्गृहे तिष्ठेः… | PASS |
| 13 | sangram-article:imperative-optative | императив (команда, 2-е → 3-е лицо)… | EXTERNAL (не валидируется) |
| 14 | zalizniak-1978-sec:134 | chind-āna- (m, n), -ā- (f)… | PASS |
| 15 | kochergina-lesson:XXVI | sunvāna (sunu-āna)… | PASS |
| 16 | knauer-fraza:Nr.12 | yajñeṣv adhvaryavaḥ somaṁ sunvatām… | PASS |
| 17 | dhatu:glava7-ukazatel-zaliznyaka | Идея Зализняка проста и мощна… | PASS |

spots: 15 PASS, 2 external, 0 FAIL
HB-утверждения урока: 11 (HB-277, HB-278, HB-279, HB-280, HB-281, HB-282, HB-283, HB-284, HB-285, HB-286, HB-49); отсутствующих в claims.yml: 0
TSV-строк урока XXXV: 24; уникальных якорей: 5 (тем в topics.yml: 5); якоря↔темами совпадают: True (первый прогон чекера ловил префикс XXXVIII — фильтр уточнён, данные не менялись)
catalog.mdx: секций тем урока XXXV (###): урок XXXV рендерится
Таблиц локусов в секции XXXV: 5; вердиктов «Исключения»: 5; лемм-таблиц: 1

ИТОГ: PASS — 15/15 локальных спот-фраз, 11/11 HB, 24/24 TSV-строки, 5/5 якорей↔тем (свежепроцессная верификация урока XXXV; DeepSeek-лейн без ключа на боксе, прецедент серии H5676/H5684).
