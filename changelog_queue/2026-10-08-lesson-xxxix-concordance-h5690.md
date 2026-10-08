# Урок XXXIX конкорданса Бюлера приземлён (H5690)

_Repo: gasyoun/SanskritGrammar · Source: LessonConcordance_ · Date: 2026-10-08_

## Что

Поурочный конкорданс Бюлера дополнен уроком XXXIX — продолжение морфонологии корней II класса (урок открывается жирным делимитером «**Урок XXXIX**», mdx 5647 — косой случай плана, парсер и здесь не подавился): ṛ-корни (jāgṛ — отбрасывание окончаний 2/3 sg, n-less 3 pl ati/atu/uḥ + guṇa), c/j→k/g (vac) с дефектностью 3 pl ind. (клетка-тире, statistic-клейм HB-301), d→t (vid) с висарга-опцией avet/aveḥ и перфект-презенсом veda + vidāṃ karavāṇi, han (jahi, ghn-алломорф), ś/ṣ/kṣ/mṛj (dviṣ трёхрядный, cakṣ, mṛj) + īś/vaś. 20 TSV-строк, 5 тем, 9 HB-утверждений (HB-299–307 — все TRUE/JUSTIFIED). Лемма-слой 9/10: jāgṛ — «одинокий корень» (NO ROW в crosswalk, отсутствует у Кнауэра/Кочергиной/dhatu-гл.7 — интенсив-стем по Уитни §1020a, лакуна всех реестров, честно); vid — две строки-омонима know/find, обе I₁; расхождение рядов ceṣṭ 1975-I₁(low)↔1978-A₂ — продолжение серии. КУРАТОРСКАЯ НАХОДКА: упражнение Бюлера mdx 5853 «yo 'smān dveṣṭi yaṁ ca vayaṁ dviṣmas tam ebhir mantrair hanāma» дословно = Кнауэр Nr.11 п.5 — dviṣmas + hanāma урока в живой фразе; в matches.json пары нет (снэпшот) — зафиксирована в topics.yml reuse_clusters честно. Вердикты гипотезы об исключениях: CONFIRMED ×2 (han/dviṣ-узел §§9–10; c/j-ряд §7), CONFIRMED-WITH-NUANCE ×2 (jāgṛ: «корень» вне словаря З-1978 и Кочергиной; vid: перфект-презенс не подан у Кочергиной), GAP-DOCUMENTED ×1 (лемма-слой). Найден дрейф реестра: loc-строки HB-299…307 систематически −2 от фактических строк mdx (контент всех девяти верифицирован PASS; сдвиг реестра — @DO в GTD). corpus_layer пуст (честно).

## Проверки

- `python3 scripts/build_lesson_concordance.py` — PASS: spots 489 local OK / 34 external, catalog.mdx 42 урока, 785 строк.
- `typed_link_lint.py` — PASS: all clean, 0 ошибок.
- Свежепроцессная верификация 13/13 PASS (review/lesson-xxxix-concordance-h5690-spotcheck-08-10-2026.md); DeepSeek-лейн — auth-store без ключа на боксе (20-й прецедент серии H5676→H5699) → фолбэк по прецеденту.

## Ссылки

- План: BUHLER_LESSON_CONCORDANCE_PLAN_2026.md (виза D1–D16, адденды E1–E13)
- Хендофф: gasyoun/Uprava handoffs/H5690-OxAlpha_SanskritGrammar_buhler-concordance-XXXIX_02.10.26.md
- Спот-чек: review/lesson-xxxix-concordance-h5690-spotcheck-08-10-2026.md
