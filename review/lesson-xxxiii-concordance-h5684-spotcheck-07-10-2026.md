# H5684 — spot-check протокол: урок XXXIII (07-10-2026)

_Verifier: OxAlpha (`opencode/z-ai/glm-5.3-flash`), независимая свежепроцессная проверка._

## Lane

- **DeepSeek-лейн недоступен**: проба `api.deepseek.com/models` → **HTTP 401** (конечная точка жива, `DEEPSEEK_API_KEY` не установлен ни в env, ни в `~/.zshrc` — ключа на боксе нет; тот же исход, что H5659/H5670/H5671/H5672/H5677/H5678/H5682). Одна честная попытка; пере-аутентификация невозможна без человека.
- QA выполнена независимым код-путём (`/tmp/opencode/h5684_verify.py`, свежий процесс), отличным от build-генератора реализацией тех же проверок (build-валидация E12 — первый независимый барьер: **327 local OK / 18 external**; этот чекер — второй).

## Ledger — 144 checks

- **Урок-сегмент mdx**: `# УРОК XXXIII.` = строка 4657 (с точкой), следующий `# УРОК XXXIV` = 4757 (без точки); 55 форм-проб в сегменте 4657–4756 — CONFIRMED (dvandva-ряд: rāmakṛṣṇau, brāhmaṇakṣatriyavaiśyāḥ, pāṇipādam, sarpanakulam, chatropānaham, ahorātra, mātāpitarau, dyāvābhūmī, dyāvāpṛthivyau, mitrāvaruṇau, agnīṣomau; tatpuruṣa-ряд: grāmagataḥ, śivarakṣitaḥ, caurabhayam, sthālīpakvaḥ, pūrvakāyaḥ, madhyāhnaḥ, ātmanotṛtīyaḥ, vācaspatiḥ, manasija, apaṇḍitaḥ, atidevaḥ; karmadhāraya-ряд: kṛṣṇāśvaḥ, snātānuliptaḥ, puruṣavyāghraḥ, pādapadmam; dvigu-ряд: caturyugam, tribhuvanam, trilokam/trilokī, dvigu, pañcagu; глаголы: sam-āp, ni-yuj, anu-rajj, pra-vas, ni-vart; вводный слой: asmad, yuṣmad, mahā; сносковый is/us→iṣ/uṣ + ретрофлексия; śakuntalā-фрагмент दुष्षन्तो नाम राजर्षिः).
- **HB-привязки 10/10** (все loc «Урок XXXIII»): HB-259 TRUE/JUSTIFIED (местоименные d-основы + mahā), HB-260 TRUE (rāmakṛṣṇau-дв./мн.), HB-261 TRUE (samāhāra -am + chatropānaham), HB-262 TRUE (iṣ/uṣ-сноска), HB-263 TRUE (ретрофлексия «язычными»), HB-264 TRUE (mitrāvaruṇau-долгота), HB-265 TRUE (косвенный падеж), HB-266 TRUE (ātmanotṛtīyaḥ-удержание), HB-267 TRUE (upapada: verbam finitam; -pāla/-stha/-ja), HB-268 UNTESTABLE/JUSTIFIED (dvigu-пропорции) — вердикты прямо из claims.yml свёрены fold-парсером.
- **Crosswalk-леммы 4/5 + 1 через омонимы**: āp wno 26 (A₂ medium / A₂ closed); yuj wno 608 (U₁ high / U₁ closed); raj h.2 wno 617 (derived A₁, z-серия N1, 1978 A₁ — внутризализняковская вилка подтверждена csv-парсером); vas h.1 715 + h.2 716 ×2 (shine/clothe; «dwell/go»-строки в реестре НЕТ — честная неполнота подтверждена отрицательным пробом); vṛt wno 744 ×2 z-строки (R₁ high / R₁ closed).
- **matches.json: 0 совпадений XXXIII** — честно (связный śakuntalā-фрагмент упражнения, не фразовый ряд); **corpus_layer.tsv: 0 строк XXXIII** — честно.
- **Уитни §§ (глава XVIII)**: якоря 1250/1251/1252/1253/1255/1263/1264/1269/1279/1280/1300/1312 — 12/12 в файле главы; фактура §1250 (case-form first member «no means rare») — CONFIRMED.
- **Очерк**: якоря s107/s191/s192/s193/s196 — 5/5; 7 спот-фраз байт-в-байт (§191 основа=последовательность, §192 «означает \*А и Б\*», §193 косвенный падеж + karmadhāraya-определение + dvigu «кроме eka-», §196 «Изредка… словоформа», §107 d-основы) — CONFIRMED.
- **Кочергина**: Занятие XXXII @8403, следующий Занятие XXXIII @8654; 5 спот-фраз найдены ЛИНЕВО и лежат внутри диапазона XXXII (род по последней основе + внешние saṃdhi; определения tatpuruṣa/karmadhāraya/dvigu; dvandva dual/samāhāra -am); порядок основ dvandva («Основы, начинающиеся с гласной…») — CONFIRMED.
- **Кнауэр Nr.11**: заголовок «# Nr. 11 (§§ 127—143)» @102; devatā-dvandva-фраза अग्नी\xadषोमावष्टाभिर्ऋग्भिर्ऋषिरस्तौदिन्द्रावरुणौ внутри Nr.11 (с soft-hyphen U+00AD источника — байт-в-байт); puruṣasiṅhaṁ внутри Nr.11; сноска §223 «человѣкъ подобный льву» — CONFIRMED.
- **topics.yml**: 6 тем (compound-general, dvandva, tatpurusha, karmadharaya, dvigu, lesson-roots), 6 exceptions-вердиктов, 10 HB-привязок урока, лемма-таблица 5 строк, locus 4657–4756 — CONFIRMED.
- **catalog.mdx (регенерирован)**: `## Урок XXXIII — Composita` присутствует, XXXIII — 28-й в списке landed (28 уроков), 6 topic-секций, все 10 HB-ссылок в блоке урока — CONFIRMED.
- **TSV**: ровно 26 строк XXXIII, все 10-колоночные, все датированы 07-10-2026, 6 уникальных якорей, link_type=thematic + match_method=curated — CONFIRMED; `typed_link_lint` — **0 ошибок** (subprocess, свежий процесс).
- **src/lesson-backlinks.json**: XXXIII-строки в buhler/kochergina/knauer/ocherk/sangram-compounds-overview/sangram-tatpurusha/dhatu-glava7 — CONFIRMED.

## Дефекты первичного прогона чекера (не данных)

7 ложных FAIL — все баги чекера, исправлены и перегнаны: (1) claim_ru в claims.yml — fold-блоки (`>-`), текст на следующих строках: needle-проверка по строке заголовка давала 6 ложных «не найдено» (кал HB-260/261/262/259/267/268); чекер переведён на fold-сборку; (2) needle HB-267 «प्रजापाल» — в клейме транслит (-pāla/-stha/-ja), деванагари только в тексте Бюлера; needle заменён на «verbam finitam» из claim_ru. **0 дефектов данных.**

## Честные пробелы (зафиксированы, не скрыты)

- matches.json: 0 reuse-кластеров урока XXXIII (связный текст упражнения) — в topics.yml записано честно.
- corpus_layer.tsv: 0 строк урока XXXIII — записано честно.
- crosswalk: vas «обитать/уезжать»-строки в реестре нет — 4/5 через омонимы, GAP-PARTIAL.
- raj: расхождение рядов двух Зализняков (1975 z-серия N1 против 1978 A₁) + класс Бюлера IV. — уровень лексемы против ряда, зафиксировано, не сглажено.
- Kochergina Занятие XXXII: pronoun-слой вводного § Бюлера и nañ-тип (2б) не оговорены; dvigu без ж.р.-на-ī и «реже прилагательные» — K±.
- Zaliznyak-1978: itaretara/samāhāra термины и devatā-долгота в §§192/193 отсутствуют — Z±.
- HB-268 UNTESTABLE (пропорции dvigu) — та же непроверяемая статистика типов композита, что OCH-60.

## VERDICT: PASS (144/144 после перегонки; 0 дефектов данных)
