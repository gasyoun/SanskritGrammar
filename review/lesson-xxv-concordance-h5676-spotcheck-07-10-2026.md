# H5676 — spot-check протокол: урок XXV (07-10-2026)

_Verifier: OxAlpha (`opencode/z-ai/glm-5.3-flash`), независимая свежепроцессная проверка._

## Lane

- **DeepSeek-лейн: endpoint доступен, ключа нет** — `curl api.deepseek.com` → HTTP 401 (впервые за серию: H5659–H5672 давали HTTP 000); retry-политика не потребовалась (первая проба не сетевая). Ключ на боксе отсутствует; из устаревших бэкапов конфигов (`DO-NOT-RESTORE-*.bak`) ключи не добываются по credential-контракту.
- Фолбэк по прецеденту H5671/H5672/H5670: QA **в процессе**, независимым код-путём от build-генератора (build-валидация E12 остаётся первым, независимым барьером). Чекер: 130 атомарных проверок, отдельный парсинг TSV/YAML/CSV/matches.json/mdx, свежий python-процесс.

## Ledger — 130 checks, 130 PASS

- **HB-привязки (7):** HB-34 (loc «mdx 3275»), HB-183 (3277), HB-35 (3303), HB-184 (3315), HB-185 (3333), HB-186 (3355, verdict_fact FALSE + methodichka-errata «читать на aṅ»), HB-187 (3357) — loc-строки + verdict_fact присутствуют — **14/14 CONFIRMED** (прямо из claims.yml). Дрейф: loc-строки реестра указывают на строки более ранней ревизии mdx (±2–4 строки: фактические 3277/3279/3305/3317/3357/3359); содержимое всех семи локусов подтверждено в секции XXV по цитатам — реестр не тронут (владелец H797), дрейф задокументирован здесь.
- **Таблицы урока XXV (mdx 3275–3416):** заголовок `# УРОК XXV` без точки (3275); vas-таблицы vidvan/vidvāṃsam/viduṣi/vidvatsu + jagmivan/jagmuṣi/jagmuṣoḥ/jagmivatsu; §1б: ninīvas/ninyuṣ, śuśruvuṣ, cakruṣ, jagmuṣ; §2 троица (śvān/śvan(śva)/śun; yuvān/yuvan(yuva)/yūn; maghavān/maghavan(maghava)/maghon); ahan: ahaḥ/ahāni/ahnā/ahobhiḥ/ahaḥsu/ahassu; ac-таблица: prāñc/avāñc/udañc/pratyañc/nyac/anūc/tiraśc/udīc; §4: rājñī/śunī/viduṣī/udicī/yuvati/yuvatī; глаголы astam gam/ud-gam/sparh X. P. — **39/39 CONFIRMED**.
- **Crosswalk-леммы:** gam — wno 170 «go», aniṭ, ryad_1978 M₁ (§66-список, open/full); spṛh — wno 884 «be eager», ryad_1978 R₁ (§66-правило, closed/full) — **2/2 CONFIRMED, полный ряд** (контраст XXI 6/7 с sṛj-пробоиной).
- **matches.json reuse-квинтет:** XXV.548↔kochergina XXVIII.694 (1.0), XXV.543↔knauer 6.127 (1.0), XXV.545↔knauer 7.146 (1.0), XXV.547↔knauer 5.102 (1.0), XXV.550↔knauer 5.103 (0.956) — ровно 5 XXV-пар, ни одна не потеряна и не выдумана — **CONFIRMED**.
- **Уитни §§ (локальный mdx):** §458 (vāṅs→vān N.sg., van V.sg., uṣ слабейшие, vat средние + §458a выпадение соед. i), §427 (çún/yū́n), §428 (maghón), §430 (áhan n. day), §407 (Compounds with añc or ac + §407b fem ī), §436 (sómarājñī к weakest), §459 (úṣī) — **9/9 CONFIRMED**.
- **Зализняк-1978 §§:** §94 (vāṁs/vaṁs/vat/uṣ «аномально»), §155 (замена -ma на -vaṁs-, fem -uṣī-), §89 (çun-/yūn-/maghon-), §101 (ahan-/ahar-/ahas-), §95 (añc/ac/c-с-удлинением), §180 (ar/an/in/ant/at/yaṁs/vaṁs/añc → -ī-); §89 НЕ покрывает yuvati-исключение (утверждение topics.yml об отсутствии) — **12/12 CONFIRMED**.
- **Кочергина:** XXVI (суффикс -(i)vaṃs-), XXVIII (cakṛvaṃs-парадигма; śvan/yuvan «основы śun- и yūn-»; pratyañc; tiryañc tiraśc-), XXXI (fem ī к слабой ступени: rājan→rajñī, cakṛvaṃs→cakruṣī; ahan списком основ: ahas/ahnā/ahobhis/ahaḥsu/ahassu/ahnī/ahanī/ahāni); **maghavan — 0 вхождений по всему файлу** (дыра свидетеля подтверждена); yuvati-исключения нет — **9/9 CONFIRMED**.
- **Кнауэр:** Nr.6 «एव क्षत्रियावयुध्येताम्», Nr.7 «काश्या आजग्मुषो», Nr.5 «तिर्यक्षु जायन्त» + «प्राचां देशे… नगरं» (вариант matches 0.956) + «यूना वीरेण यशो लब्धम्» (yūn-рядом, вне реестра — зафиксировано в topics.yml notes) — **5/5 CONFIRMED**.
- **topics.yml самосогласованность:** 5 тем (vas-stems, an-stems-trio, ac-stems, feminine-i, lesson-roots); topic_claims ⊆ lesson claims (7 = {34,183,35,184,185,186,187}); spots ⊆ TSV-локусы по каждому якорю; у всех тем exceptions.verdict + 4 свидетеля; lemmas = {gam, spṛh}; сangram-present-perfect-participles добавлен в LOCAL_SOURCE_FILES — **18/18 CONFIRMED**.
- **TSV XXV (25 строк):** 10 колонок, дата 07-10-2026, match_method curated, confidence ∈ [0.7, 1.0]; спот-фразы 17 локальных байт-точно в источниках (build: 262 local OK / 17 external) — **CONFIRMED**.
- **catalog.mdx (перегенерирован):** `## Урок XXV —`, 5 topic-заголовков, 25 табличных строк, все 7 HB-ссылок, шапка «Уроки (48): …XXV…» = 23 урока — **CONFIRMED**.

## Дефекты первичного прогона чекера (не данных) — 6, все исправлены

1. Игла «ninīyuṣ» — Бюлер печатает **ninyuṣ** (по его же правилу §1б: n + ī, один согласный → y); HB-183-«number» согласен. Чекер, не данные.
2. Пять проверок «claims loc = строка mdx N» — реестр loc от ревизии mdx ±2–4 строки; заменены на проверку содержимого в секции + задокументированный дрейф (см. Ledger).
3. Счётчик matches-пар: префикс `buhler-1923.XXV.` матчит также XXVII/XXVIII — заменён на точный сплит по `.`[1]==`XXV`.
4. **Ложный вывод «kochergina ahan отсутствует»** — первый grep был обрезан `head -5`; на самом деле Занятие XXXI покрывает ahan списком основ. **Исправлены данные topics.yml** (вердикт K− → K±, witness-gap только maghavan) + добавлена честная строка kochergina-lesson:XXXI со спотом «N.sg. ahas, I.sg. ahnā, I.pl. ahobhis» (теперь 25 TSV-строк, не 24).
5. Игла «п. день» против печатного «ahan \*п\*. день» — учтён курсивный маркер.
6. Порядок объявления `sec` в скрипте чекера — переставлен.

## Drive-by repair (попутный, вне DoD урока)

Дубликат YAML-ключа `notes:` (строка 1957) в XXI.lesson-roots — паста dual-run-адъюдикации H5671, затенявшая (last-wins) собственную заметку XXI о пробоине sṛj: вычищено — заметка XX «2 глагола… crosswalk 2/2» с хвостом provenance (auto-H2628, origin/h5671-drain) возвращена в XX.lesson-roots, заметка XXI «crosswalk 6/7, sṛj — пробоина урока III» снова единственная в своей теме. Контент не изобретался — пара «ключ/владелец» восстановлена; виден в catalog.mdx секций XX/XXI.

## VERDICT: PASS (130/130 после исправлений; 1 дефект данных пойман и исправлен в же проходе)
