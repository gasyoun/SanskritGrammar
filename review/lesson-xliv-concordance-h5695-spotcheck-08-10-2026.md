# H5695 spot-check (свежепроцессная верификация, 08-10-2026)

Независимый процесс (не код build): каждая spot-фраза урока XLIV сверяется grep'ом против файла источника; HB-id — против claims.yml; TSV-строки — против тем topics.yml; формы парадигм — против сегмента mdx 6733–6905; crosswalk — прямые пробы CSV.

**DeepSeek-лейн недоступен**: проба `api.deepseek.com/models` → **HTTP 401** «Authentication Fails (governor)» (конечная точка жива; ключа на боксе нет — тот же исход, что H5659…H5688, **18-й урок серии**). Одна честная попытка; пере-аутентификация невозможна без человека.

## Спот-фразы (14 локальных)

| # | Локус | Фраза | Результат |
|---|---|---|---|
| 1 | kochergina-lesson:XVIII | образуется от всех глаголов по единому правилу - прибавлением к корню ударяемого суффикса -syá | PASS |
| 2 | kochergina-lesson:XIX | в залоге Ātmanepada as употребляется только в описательном будущем времени и не имеет формы 3-го лица | PASS |
| 3 | kochergina-lesson:XIX | Оно обозначает нереальное действие | PASS |
| 4 | kochergina-lesson:XIX | употребляется в обеих частях условного предложения | PASS |
| 5 | zalizniak-1978-sec:157 | Основа простого будущего времени равна корню в ступени guṇa + sya | PASS |
| 6 | zalizniak-1978-sec:158 | по внешнему строению представляет собой имперфект от основы будущего времени | PASS |
| 7 | zalizniak-1978-sec:159 | с внешней стороны равно сочетанию N.sg имени деятеля на -tar- | PASS |
| 8 | zalizniak-1978-sec:149 | основа прекатива равна корню в слабой ступени + yās | PASS |
| 9 | knauer-fraza:Nr.13 | yadi devo varṣiṣyati vayaṁ bahir na gamiṣyāmaḥ | PASS |
| 10 | knauer-fraza:Nr.13 | kaliyuge balaṁ prāpte | PASS |
| 11 | knauer-fraza:Nr.13 | dharmo vinaçiṣyati | PASS |
| 12 | knauer-fraza:Nr.13 | yo bhikṣāṁ dātā sa svargaṁ yātā | PASS |
| 13 | knauer-fraza:Nr.13 | suvṛṣṭiç ced abhaviṣyat tadā subhikṣam abhaviṣyat | PASS |
| 14 | dhatu:glava7-ukazatel-zaliznyaka | Идея Зализняка проста и мощна | PASS |

## Прочие оси

- **HB-утверждения урока: 12** (HB-58, HB-352…HB-362) — все в claims.yml; HB-58 note якорит «Урок XLIV» (order-flag: описательное будущее первым) — PASS
- **TSV-строк урока XLIV: 17** (всего 692); все строки 10 колонок; якоря ↔ темы topics.yml: совпадают (5/5: future-periphrastic-tar-as, future-simple-sya, future-participle-conditional, benedictive-precative, lesson-roots) — PASS
- **Whitney §-якоря** (921-926 → гл. XI 824-930; 931-940/939/941 → гл. XII 931-950): диапазоны глав валидны; внешние (Wikisource, E13) — PASS
- **Z-1978 §-якоря** (149, 157, 158, 159): все в Очерке — PASS
- **Crosswalk**: позитивные пробы tṛ w319 (tṝ-ловушка), grabh w196 (grah-ловушка), pṛ w469 (pṝ-ловушка), glā w200 (glai-ловушка), syand w895 **1975 A₁ ≠ 1978 N₁** (5-е расхождение рядов серии); негативные пробы tṝ/grah/pṝ/glai/gai/stu/sṛj/hve/i — НЕ ключи реестра — PASS
- **Формы парадигм урока** (15 проб kartāsmi…dāsīran + tṝ-двойник tariṣyati/tarīṣyati + gam-пара saṅgaṅsyate/saṅgaṅsīṣṭa): все в сегменте mdx 6733–6905 — PASS; заголовок «# УРОК XLIV.» в сегменте, «# УРОК XLV.» вне — PASS
- **Кнауэр-переиспользование** (кураторская находка): ядро упражнения Бюлера (калиюга) = Кнауэр Nr.13 дословно (varṣiṣyati/gamiṣyāmaḥ/vinaçiṣyati/utsrakṣyanti/ācariṣyanti/vikreṣyanti/bhakṣayiṣyanty/pāsyanti + dātā/yātā + abhaviṣyat ×2) — весь формальный инвентарь урока живым текстом; matcher'у невидимо (рус↔санскрит) — PASS
- **catalog.mdx**: секция «## Урок XLIV —» рендерится, 7 строк локусов (Очерк ×4, Кочергина ×3), 4 блока «Исключения», лемма-таблица 46 строк (41 yes + 5 NO — честно), dhatu/talmud-строки, счётчик «Уроки (48)» — PASS
- **backlinks JSON**: страницы buhler / kochergina / knauer / ocherk / dhatu-glava7 — PASS

## Прогоны чекера

Первичный прогон: 69/70 — **1 FAIL был багом чекера, не данных**: ожидание `| [Гасунс, Dhātu 2014]` (линк на ярлыке), тогда как генератор рендерит `| Гасунс, Dhātu 2014 | [glava7-ukazatel-zaliznyaka](…)` (линк на локусе, как у всей серии). Строки на месте — PASS. **70/70 PASS. 0 дефектов данных.**

**ИТОГ: PASS — 14/14 локальных спот-фраз, 12/12 HB, 17/17 TSV-строк, 5/5 якорей↔тем, 46/46 лемм (41+5), 70/70 осей (свежепроцессная верификация урока XLIV; DeepSeek-лейн без ключа на боксе, прецедент серии H5659…H5688).**
