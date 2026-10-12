# Pilot: Process-Sanskrit (DCS-word2vec) vs induced sandhi rules — H6456/WHEEL6

_Created: 2026-10-12 · Last updated: 2026-10-12_

**Handoff:** [H6456](https://github.com/gasyoun/Uprava/blob/main/handoffs/H6456-OxAlpha_SanskritGrammar_process-sanskrit-sandhi-pilot_11.10.26.md) · WHEEL6-виза MG 11-10 · исполнитель OxAlpha (opencode/zai-coding-plan/glm-5.3-flash).
**Dossier:** [wheel-watch-sandhi-nlp-2026-10.md](https://github.com/gasyoun/Uprava/blob/main/reports/wheel-watch-sandhi-nlp-2026-10.md), строка Process-Sanskrit (ADOPT, WHEEL6).

## Что сравнивалось

| Система | Реализация | Скоринг |
|---|---|---|
| upstream | [Process-Sanskrit 1.5.2](https://github.com/Giacomo-De-Luca/Process-Sanskrit) (pip; вендор MIT-копии sanskrit_parser-сплиттера, Rust/натив-бэкенд) | DCS word2vec-модель, **бандлится в пакете** (`splitter/data/w2v.npz` + sentencepiece.model — докачка не нужна); top-ranked split из limit=5 |
| ours | чистый rule-lookup по индукционным/hand-таблицам `X Y → Z` (kosha [gita_sandhi.tsv](https://github.com/gasyoun/kosha/blob/main/data/gita/gita_sandhi.tsv) + astavakragita_sandhi.tsv, 266 правил): каждое вхождение surface-формы Z даёт кандидата-сплит, ранжирование по частотной массе | частотность правила; лексикона/морфологии нет |

**Gold (актуальный sandhi-бенч):** DCS CoNLL-U (`dcs-conllu/files`), тексты Aṣṭāvakragīta + Gītagovinda — токен несёт sandhied FORM и pre-sandhi `Unsandhied=`; это машино-верифицируемый gold-набор программы sandhi-scaffold (тот же источник, что [dcs_sandhi_induce.py](https://github.com/gasyoun/kosha/blob/main/scripts/dcs_sandhi_induce.py), режимы 1/2). Рука-таблица gita_gold_master.tsv на этой машине смешивает layout rule-id/rule-строка в колонках — для бенча выбран CoNLL-U-путь (handoff разрешает другое имя файла gold-набора). Два семейства айтемов: edge (соседние токены с изменившейся кромкой) и MWT (слипшийся multi-word-token ровно из 2 компонент). Фильтры: только IAST-буквы, ≥2 символа на слово, joined ≤28, дедуп по joined, seed 42.

## Метрики (N=250, exact-2 junction accuracy)

| Система | exact-2 | first-token | мс/айтем | ошибки |
|---|---|---|---|---|
| upstream (w2v-scored) | **42.8%** (107/250) | 58.4% | 0.3 | 0 (16 «no split found») |
| ours (rule-lookup) | 2.0% (5/250) | 8.0% | <0.1 | 0 |

Разбивка (upstream exact): edge 37.7% (N=146) · MWT 50.0% (N=104); по текстам Aṣṭāvakragīta 36.8% (N=182) · Gītagovinda 58.8% (N=68).

**Диагностика «ours» (честность вердикта):** gold-сплит выразим кандидатами rule-lookup только в **5.6%** (14/250) айтемов. Причина структурная: таблицы `X Y → Z` кодируют только *меняющиеся* стыки, а bench из DCS-смежности доминирован нулевыми стыками (visarga-элизия видима, но «a+d»-типа границы и компаундные MWT-стыки surface не меняют) — без лексикона/морфологии чистый rule-lookup сегментировать такой текст не может в принципе. Это не «наши правила плохи», а граница применимости: наши правила — слой индукции/аудита (sandhi-check/gold-audit/DCS-alignment), а не standalone-сплиттер.

## Вердикт

**ADOPT подтверждён измерением** (строка карты 7 в досье остаётся ADOPT, теперь с числами): сплит-рантайм со скорингом брать у upstream — 42.8% exact на DCS-gold стыках из коробки (pip + бандл w2v, ноль докачек для сплит-задачи), против 2.0% у чисто-правилового рантайма без лексикона. Наши индукционные правила остаются нишевым активом, который upstream не закрывает: корпусная индукция правил с частотностью, аудит hand-разметки (gold-audit), линт over-applied sandhi (sandhi-check) — формулировки «где мы впереди» досье подтверждены (upstream их не делает).

Типовые промахи upstream (16 null + примеры): unknown pada («advayaṃkaścij»), over-split компаундов ([vi, galita, lajjā] при gold [vigalita, lajjā]) — то есть ровно стыки неоднозначности, куда в нашем стеке встаёт sandhi-council.

## Верификация (карта 9 — чужой семьёй)

**Вердикт: PASS** (DeepSeek-councillor, 12-10-2026; числа A–D пересчитаны независимо: 107/250, 5/250, 104/146/68 — сходятся; bench 250 айтемов воспроизведён). Раскрытые оговорки: (1) **конструктная валидность MWT-семейства** — gold MWT-айтемов берётся из pre-sandhi `Unsandhied`, поэтому concat компонент ≠ joined для части айтемов (напр. `mahāhrada→[mahā,hradaḥ]`); edge-семейство свободно от этого; измерение остаётся симметричным (обе системы получают одинаковые айтемы), но точные цифры трактуются как относительное сравнение, не абсолютная метрика качества; (2) coverage 5,6% (14/250) получен отдельным анализом, скриптом не эмитится; (3) `OK_CHARS` без ṇ/ṅ — такие айтемы молча отфильтрованы (влияет на состав bench, не на честность сравнения).

## Артефакты

- Пилот-скрипт: [scripts/pilot_process_sanskrit_vs_rules.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/pilot_process_sanskrit_vs_rules.py) (venv: `pip install process-sanskrit`; прогон `--n 250 --seed 42`)
- Машиночитаемые метрики + per-item: [reports/h6456_pilot_metrics.json](https://github.com/gasyoun/SanskritGrammar/blob/main/reports/h6456_pilot_metrics.json)
- Секция-вердикт в досье: [wheel-watch-sandhi-nlp-2026-10.md](https://github.com/gasyoun/Uprava/blob/main/reports/wheel-watch-sandhi-nlp-2026-10.md) (WHEEL6-результат)

Вне скоупа (по handoff): SanskritShala-UI, scl-joiner. Стоп-бюджет: 1 день / 5 попыток — израсходовано <1 часа.

## Provenance

2026-10-12 · GLM 5.3 (opencode/zai-coding-plan/glm-5.3-flash), drain-лейн H6456. Данные read-only (kosha + dcs-conllu); единственный сетевой шаг — `pip install process-sanskrit` 1.5.2.

_к.ф.н. М.Ю. Гасунс_
