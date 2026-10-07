# H5681 — spot-check протокол: урок XXX (07-10-2026)

_Verifier: OxAlpha (`opencode/z-ai/glm-5.3-flash`), независимая свежепроцессная проверка._

## Lane

- **DeepSeek-лейн недоступен**: тот же исход, что H5659/H5667/H5670/H5671/H5672/H5677/H5678 — `DEEPSEEK_API_KEY` на боксе нет (прецедентная цепочка; одна попытка без ключа невозможна физически). QA выполнена независимым код-путём (`/tmp/h5681_verify.py`, свежий процесс), отличным от build-генератора реализацией тех же проверок (build-валидация E12 — первый независимый барьер: **297 local OK / 18 external**; этот чекер — второй).

## Ledger — 190 checks

- **Урок-сегмент mdx**: `# УРОК XXX` = строка 4123, следующий `# УРОК XXXI.` = 4331; ~85 форм-проб в сегменте 4123–4330 — глагольные ряды §1–5 (pātum, dātum, jetum, netum, śrotum, dhātum, gātum; mantum, hantum, āptum, kṣeptum, paktum, vaktum, draṣṭum, deṣṭum, praṣṭum, kroddhum, banddhum; attum, vettum, gantum; bhavitum, kathayitum, yojayitum, grahītum, taritum/tarītum; gāhitum/gāḍhum, sahitum/soḍhum, gūhitum/goḍhum, mārṣṭum/mārjitum), герундивы §6 (vaktavya, labdhavya; dānīya, gānīya, śravaṇīya, bodhanīya, coraṇīya, śrāvaṇīya, gūhanīya, mārjanīya; deya, geya, jeya, neya, kārya, tārya, śravya, śrāvya; vedyа, bodhya, tṛdya, vācya, labhya, śakya, sekya, aṅgya; itya, kṛtya, bhṛtya, stutya, vadhya), словарь (sam-āp, apā-kar, arh, ava-gāh, vi-dhā, nart, pra-bhū, yat, pra-vart, manas kar; nāṭaka, brahmacārin, vapus, samāja, sāman; taruṇa, priyavādin, puṣṭa, phalavant, samartha; alam, svairam; aniṭ), деванагари-проба упражнения (द्रष्टुमागच्छन्) — **CONFIRMED**.
- **HB-привязки**: HB-234–245 + HB-43/44/45 — все 15 loc «Урок XXX / mdx», все `verdict_fact: TRUE` (HB-246 — XXXI, не приписан; проверено) — **15/15 CONFIRMED** (прямо из claims.yml).
- **Crosswalk-леммы 10/10 корней**: āp wno 26 (A₂ closed); kṛ wno 106 (R₁ open, омоним 107); arh wno 18 (A₁ derived, **1978-ряд R₁ — расхождение свидетелей**); gāh wno 178 (A₂ closed); dhā wno 393 (A₂ open, омоним 394); nṛt wno 433 (R₁ closed); bhū wno 528 (U₂ open); yat wno 598 (A₁ closed); vac wno 699 (A₁ closed); vṛt wno 744 (R₁ closed) — **CONFIRMED**.
- **Ловушки написания**: `kar` отсутствует в реестре (только kṛ); `nart` отсутствует (только nṛt) — обе задокументированы в topics.yml — **CONFIRMED**.
- **matches.json секстет**: XXX.647↔knauer 19.415 (0.977), XXX.650↔19.418 (1.0), XXX.653↔19.416 (1.0), XXX.657↔19.417 (1.0), XXX.647↔kochergina XXIII.564 (1.0), XXX.658↔XXIII.572 (1.0) — **CONFIRMED**.
- **Уитни §§ (локальные главы)**: §968 «only a single infinitive»; §972 tu/itu-таблица с gāh/yat и mṛj-двойником mā̆rṣṭu/mārjitu (дословный параллель §4 Бюлера); §227 dṛç/sṛj ra-ряд; §627 mṛj vṛddhi; §962 «are three: ya, tavya, anīya»; §963 itya/kṛtya-ряд; §964b «the rules are the same as for the formation of the infinitive»; §965 anīya — **8/8 CONFIRMED**.
- **Очерк**: §164 («Инфинитив равен корню в ступени guṇa + tum», grahītum в примерах), §129 («практически не связаны с делением корней на aniṭ и seṭ»), §173 («иногда называются также пассивными причастиями будущего времени»; «ступень корня большей частью как в каузативе»; jeya/dṛçya/deya) — **CONFIRMED**.
- **Кочергина**: Занятие XXIII (заголовочно-якорный слайс: seṭ/aniṭ-правило инфинитива, триада seṭ/aniṭ/veṭ, «Ударение падает на корень», ī̆/ū̆→guṇa, упражнение с «सर्वे पौराः कालिदासेन» — exact-совпадение с уроком) / Занятие XXV (герундив: «-ya, -(i)tavya или -anīya»; грейды «сильной (kar → kārya)…слабой (darś → dṛśya)»; «Корни на ā меняют ā на e») — **CONFIRMED**.
- **Sangram**: infinitive (SG-MO-025 «отглагольное имя цели/намерения»), gerundive (SG-MO-024 «отглагольное прилагательное со значением необходимости»; числа 19 901/5740/1280) — **CONFIRMED**.
- **catalog.mdx (регенерирован)**: `## Урок XXX —` присутствует (26-й урок), блок 5/5 тем, все 15 HB-ссылок, Nr.19 с ev=4, sangram gerundive-локус — **CONFIRMED**.
- **TSV**: ровно 23 строки XXX, все 10-колоночные, все датированы 07-10-2026, 5 уникальных якорей — **CONFIRMED**; `typed_link_lint` — **0 ошибок**.
- **Спот-фразы**: 13 локальных (3×Кочергина XXIII, 3×Очерк §§164/129/173 ×2, 1×Кнауэр Nr.19, 2×sangram infinitive/gerundive, 1×dhatu, +2 дубля-локусов с другими фразами) — байт-точно (build E12 — первый барьер, чекер — второй); внешние (whitney-§§, talmud-CSV) — якоря, не фразы.

## Дефекты первичного прогона чекера (не данных)

16 ложных FAIL — все баги чекера, исправлены и перегнаны: (1) LOCAL-словарь ключился полным локусом («kochergina-lesson:XXIII») вместо префикса — 11 спотов; (2) слайс Занятия XXV бился о кросс-ссылку «см. Занятие XXV» раньше заголовка — 3 проверки; (3) арифметика TSV (23 строки: 5+7+5+4+2, а не 24); (4) деванагари-проба «वध्य» — глифовая форма Бюлера иная (латинская vadhya-проба PASS). **0 дефектов данных.**

## Честные пробелы (зафиксированы, не скрыты)

- corpus_layer.tsv не содержит строк урока XXX (контраст с XXXIV/XXXVIII) — corpus_layer: [] записан честно.
- arh — первое расхождение рядов derived/Z-1978 в серии (A₁ против R₁) — зафиксировано без сглаживания.
- alam (+dat./instr.) — синтаксическая тема урока не откурирована отдельной темой (бюджет 2–5 тем потрачен на 4 грамматические + лемма-слой); расширение D13 возможно при будущей синтаксической волне.
- HB-246 — утверждение урока XXXI (eka), к уроку XXX не относится; хвост неправильных §6в (itya…vadhya) стоит в topics.yml без отдельного клейма — фактура верифицирована чекером.

## VERDICT: PASS (190/190 после перегонки; 0 дефектов данных)
