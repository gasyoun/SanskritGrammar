# H5685 — spot-check протокол: урок XXXIV (08-10-2026)

_Verifier: OxAlpha (`opencode/z-ai/glm-5.3-flash`), независимая свежепроцессная проверка._

## Lane

- **DeepSeek-лейн недоступен**: проба `api.deepseek.com/models` → **HTTP 401** (конечная точка жива; в env и `~/.zshrc` только `OMS_DEEPSEEK_MODEL`-алиас OpenRouter, ключа нет — тот же исход, что H5659…H5684, 14-й урок серии). Одна честная попытка; пере-аутентификация невозможна без человека.
- QA выполнена независимым код-путём (`/tmp/opencode/h5685_verify.py`, свежий процесс), отличным от build-генератора реализацией тех же проверок (build-валидация E12 — первый независимый барьер: **348 local OK / 18 external**; этот чекер — второй).

## Ledger — 87 checks

- **Урок-сегмент mdx**: `# УРОК XXXIV` = строка 4757 (**без точки** — кривой делимитер, записан в topics.yml риск-строкой), следующий `# УРОК XXXV` = 4885; 49 форм-проб в сегменте 4757–4884 — CONFIRMED (samāsānta-ряд: rājan, sakhi, pathin, dvigu, ahan, ahna, rātri; bahuvrīhi-ряд: dīrghabāhuḥ, yasya, caturmukhaḥ, kṛṣṇanāmā, kṛtakṛtyaḥ, uddhṛtaudanaḥ, vīrapuruṣaḥ, śivādayaḥ, devarūpaḥ, asipāṇiḥ, nirbalaḥ, unmukhaḥ, aputraḥ, saputraḥ, rūpavadbhāryaḥ, bahunadīka, unnasa, dvipād, prajas, medhas, gandhi, sudat; сноска особых слов: dvitra, tridaśa, dakṣiṇapūrvā, daṇḍādaṇḍi, keśākeśa; avyayībhāva-ряд: yathākāmam, yatheccham, yathāśakti, yāvajjīvam, anugaṅgam, upagaṅgam, prativarṣam, upanadi; глаголы: niś-ci, vi-dar, paṭ, abhi-bhū, ā-rabh, var I.Ā. (varaya), ā-sad, has IV; фрагмент अतितृष्णा).
- **HB-привязки 8/8** (все loc «Урок XXXIV»): HB-269 **OVERSTATED**/JUSTIFIED (su/kiṃ/a-блокировка patha не абсолютна — apatha при apathin), HB-270 TRUE (go→gava, dvigu-исключение), HB-271 TRUE (aha/ahna), HB-272 TRUE (ratra→rātra errata-кандидат в source), HB-273 TRUE (puṃvadbhāva), HB-274 TRUE (ā→a + kap), HB-275 TRUE (десяток замен), HB-276 TRUE (avyayībhāva) — вердикты прямо из claims.yml, тела клеймов проверены по ключевым словам (rājan/gava/ahna/ratra/мужским/суффикс ka/dhanvan/преимущественно).
- **Crosswalk-леммы 7/8**: ci 225+226 (I₁ high ×2); paṭ 437 (A₁ / A1 seṭ); bhū 528 (U₂ / U2 veṭ); rabh 628 (**вилка**: ряд A₁ / z-серия 1975 N1 / 1978 A₁ — третий внутризализняковский раскол после arh-XXX и raj-XXXIII, подтверждён csv-парсером); vṛ 741 «choose» (R₁ / R1 veṭ); sad 830 (две z-строки A1 aniṭ / I2 seṭ при одном 1978-ряде); has 910 (A₁; Бюлер IV — номер класса ≠ ряд); **dṝ/dar в реестре НЕТ** (отрицательный проб; dṛ 372 «heed» — другой корень, не покрышка) — GAP-PARTIAL честно.
- **matches.json: ровно 1 reuse-кластер Бюлер-стороны урока** (buhler-1923.XXXIV.804 «ā-rabh I. Ā» ↔ kochergina-1998.XIV.301 «ārabh - Ā», score 0.92) — табличная строка списка глаголов, записано честно.
- **corpus_layer.tsv: 5 строк XXXIV** (rājan топ-100 ранг 23; yuvarāja редкое 7964; sakhi топ-1000 875; pathin топ-1000 698; **apatha редкое 15149** — OVERSTATED-свидетель HB-269) — все заведены в topics.yml.
- **Уитни §§ (глава XVIII)**: якоря 1292/1296/1298/1304/1307/1313/1315 — 7/7 в файле главы; фактура: §1315 (rāja/rātra/sakha/ahna/gava-списки a/b/c — двойник §3 Бюлера), §1307a (ka), §1313 (термин avyayībhāva + yāvajjīvám + upanadam), §1292 (possessive definition) — CONFIRMED.
- **Очерк**: якоря s194/s195/s200 — 3/3; 3 спот-фразы байт-в-байт (§194 «обладающий тем, что обозначено соответствующим» с \*-разметкой, §195 ā→a, §200 «прямое соединение преверба с именной основой») — CONFIRMED.
- **Кочергина**: Занятие XXXII @8403, XXXIII @8654, XXXIV @8930, XXXX @10602; 4 спот-фразы найдены ЛИНЕВО и внутри своих диапазонов (XXXIII — «Входя в состав сложного слова…»; XXXII — определение bahuvrīhi + ā→a; XXXX — «класс слов, называемых avyayībhava»); anugan̄gam в XXXX — дословный двойник булеровского anugaṅgam — CONFIRMED.
- **Кнауэр**: Nr.15 → Nr.16 диапазон найден; prajākāmas-фраза внутри Nr.15 — CONFIRMED.
- **topics.yml**: 6 тем (tatpurusha-samasanta, bahuvrihi-definition, bahuvrihi-adjfirst, bahuvrihi-finals, avyayibhava, lesson-roots), 6 exceptions-вердиктов, 8 HB-привязок, 8 лемм, mdx-локус 4757–4884 + риск-строка «БЕЗ точки» — CONFIRMED.
- **catalog.mdx (регенерирован)**: `## Урок XXXIV — Composita (продолжение)` присутствует, 30 уроков в landed-списке, XXXIV последний; 904 глубоких ссылки `:~:text=` — CONFIRMED.
- **TSV**: ровно 19 строк XXXIV, все 10-колоночные, датированы 08-10-2026, 6 уникальных якорей, curated; `typed_link_lint` — **0 ошибок** (subprocess, свежий процесс).
- **src/lesson-backlinks.json**: XXXIV-строки в buhler/kochergina/knauer/ocherk/sangram-bahuvrihi/sangram-compounds-overview/dhatu-glava7 — CONFIRMED.
- **Спот-фразы урока: все 12 локальных проверены байт-в-байт** независимым чтением (5×Кочергина XXXII/XXXIII/XXXX, 3×Очерк 194/195/200, 2×sangram bahuvrihi/compounds-overview, 1×Кнауэр Nr.15, 1×dhatu).

## Дефекты первичного прогона чекера (не данных)

3 ложных FAIL — все баги чекера, исправлены и перегнаны: (1) TSV-фильтр `".XXXIV."` — разделитель в anchor_id — двоеточие (`buhler-topic:XXXIV.…`), а не точка → 0 строк при 535 валидных; (2) crosswalk-проб `len==1` — в CSV реестра ДУБЛЬ-строки (см. ниже); (3) reuse-фильтр ловил b-стороны kochergina-1998.XXXIV (занятие 34 Кочергиной) — сужен до Bühler-стороны. **0 дефектов данных H5685.**

## Честные пробелы (зафиксированы, не скрыты)

- crosswalk: корня dṝ «burst/split» (vi-dar) в реестре нет — 7/8, GAP-PARTIAL (второй пробел после hvā в XXXVIII); dṛ 372 «heed» — другой корень.
- **Артефакт реестра (до H5685, вне скоупа — GTD 08-10-2026)**: crosswalk CSV содержит байт-идентичный дубль строки `372,dṛ,2,heed,…` (файл, строки 606 и 657) — пассивный (не влияет на 1:1-джойны по whitney_no+homonym для лемм урока), но чистке подлежит.
- rabh-вилка двух Зализняков (1975 N1 / 1978 A₁) — третий случай серии, зафиксирован, не сглажен.
- Зализняк-1978: samāsānta-блок §3 не описан вовсе (Z− целой темы) и термина avyayībhāva нет (формальное покрытие §200 при номинативном, не наречном значении).
- Kochergina: бахуврихи-финали — только ā→a-половина (K±); puṃvadbhāva-термин не назван (феномен без имени).
- Whitney: puṃvadbhāva-термина нет — §1298 (accent-слой) + §334c (ā-укорочение) — W± на adjfirst-теме.

## VERDICT: PASS (87/87; 0 дефектов данных; 3 бага чекера исправлены)
