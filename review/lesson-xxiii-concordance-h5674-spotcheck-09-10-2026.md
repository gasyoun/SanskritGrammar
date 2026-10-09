# H5674 — спот-чек урока XXIII (свежепроцессная независимая верификация)

_Дата: 09-10-2026 · executor: OxAlpha (opencode/z-ai/glm-5.3-flash) · хендофф: [H5674](https://github.com/gasyoun/Uprava/blob/main/handoffs/H5674-OxAlpha_SanskritGrammar_buhler-concordance-XXIII_02.10.26.md)_

DeepSeek-лейн — без ключа на боксе (23-й прецедент серии H5659→H5697) → фолбэк по прецеденту: независимая свежепроцессная проверка (отдельный python-процесс, не переиспользует состояние build).

Скоуп: 15 локальных спот-фраз байт-в-байт + негативный проб, 21 TSV-строка × 10 колонок × дата, каталог (заголовок/темы/исключения), backlinks (knauer/kochergina), crosswalk csv-парсером (nind ×2, rāj homonym-2-only, sar-negative + ловушка tsar/sarj), claims.yml 8/8 HB + 8/8 loci, вердикты 5/5.

Первичный прогон: 51 PASS / 2 FAIL — дефект чекера (фильтр `.XXIII.` не матчит `:XXIII.`); 2-й прогон: 50 PASS / 3 FAIL — дефект чекера №2 (`XXIII.` — подстрока `XXXIII.`); 3-й прогон с `:XXIII.`: **53 PASS / 0 FAIL — данных дефектов нет** (прецедент H5687: FAIL первичного прогона = дефект чекера, не данных).

```
PASS  spot zalizniak-1978-sec:93 «Образец: kanīyaṁs- (m, n)…»
PASS  spot zalizniak-1978-sec:185 «Особую группу составляют производные, св…»
PASS  spot kochergina-lesson:XXIX «Прилагательные в сравнительной степени н…»
PASS  spot knauer-fraza:Nr.7 «गुरुषु पिताचार्यो माता च गरीयांसः…»
PASS  spot zalizniak-1978-sec:91 «Образцы: для причастий --- pacant-…»
PASS  spot kochergina-lesson:XXVI «Активные причастия настоящего времени об…»
PASS  spot knauer-fraza:Nr.7 «जीवतः पुत्रस्य मुखं पश्यन्तौ पितरौ तुष्य…»
PASS  spot sangram-article:present-perfect-participles «активное `-ant` + среднее `-māna`…»
PASS  spot zalizniak-1978-sec:91 «Вообще эта форма всегда совпадает с N.sg…»
PASS  spot kochergina-lesson:XXIX «у причастий от глаголов I, VI (иногда), …»
PASS  spot kochergina-lesson:XXXI «Как активное причастие настоящего времен…»
PASS  spot knauer-fraza:Nr.11 «भार्यां किं मां द्वेक्षीत्यब्रवीत्पतिः…»
PASS  spot zalizniak-1978-sec:91 «mahant- (m, n)…»
PASS  spot kochergina-lesson:XXIX «имеет сильную основу на -ānt…»
PASS  spot dhatu:glava7-ukazatel-zaliznyaka «Идея Зализняка проста и мощна…»
PASS  negative probe (kanīyaṁs-x absent)
PASS  TSV XXIII rows == 21 (got 21)
PASS  TSV XXIII all 10 columns
PASS  TSV XXIII 5 topic anchors
PASS  TSV XXIII date 09-10-2026
PASS  catalog has Урок XXIII header
PASS  catalog topic XXIII.yas-stems
PASS  catalog heading XXIII yas-stems
PASS  catalog topic XXIII.at-stems
PASS  catalog heading XXIII at-stems
PASS  catalog topic XXIII.n-insertion-neuter
PASS  catalog heading XXIII n-insertion-
PASS  catalog topic XXIII.mahat-sant
PASS  catalog heading XXIII mahat-sant
PASS  catalog topic XXIII.lesson-roots
PASS  catalog heading XXIII lesson-roots
PASS  catalog 44 lessons marker
PASS  catalog XXIII exceptions blocks (5)
PASS  backlinks knauer XXIII rows >= 3
PASS  backlinks kochergina XXIII rows >= 5
PASS  crosswalk nind == 2 rows
PASS  crosswalk raj == 1 row (homonym 2 «color»)
PASS  crosswalk sar absent
PASS  crosswalk trap: tsar/sarj present (other roots)
PASS  claims.yml has HB-169
PASS  claims.yml has HB-170
PASS  claims.yml has HB-171
PASS  claims.yml has HB-172
PASS  claims.yml has HB-173
PASS  claims.yml has HB-174
PASS  claims.yml has HB-175
PASS  claims.yml has HB-33
PASS  claims.yml Урок XXIII loci == 8 (got 8)
PASS  verdict XXIII.yas-stems non-empty
PASS  verdict XXIII.at-stems non-empty
PASS  verdict XXIII.n-insertion-neuter non-empty
PASS  verdict XXIII.mahat-sant non-empty
PASS  verdict XXIII.lesson-roots non-empty

TOTAL: 53 PASS / 0 FAIL (local spots 15)
```
