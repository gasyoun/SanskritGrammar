# Урок XXV конкорданса Бюлера приземлён (H5676)

_Repo: gasyoun/SanskritGrammar · Source: LessonConcordance_ · Date: 2026-10-07_

## Что

Поурочный конкорданс Бюлера дополнен уроком XXV: vas-основы причастий перфекта (vāṃs/vat/uṣ + выпадение соед. i, i/ī→y/iy, u/ū→uv, ṛ→r), имена на an с тремя формами (śvan/yuvan/maghavan) и ср. р. ahan, прилагательные на ac (prāñc…tiryañc, N.sg.m. на -aṅ — в печати -a: HB-186 FALSE/errata), женский род на ī (rājñī, viduṣī; исключение yuvati/yuvatī). 25 TSV-строк, 5 тем, 7 HB-утверждений (HB-34, 183, 35, 184, 185, 186, 187: 6 TRUE + HB-186 FALSE как напечатано — опечатка набора, методичка «читать aṅ»), лемма-слой 2/2 ПОЛНЫЙ ряд (gam M₁ wno 170 aniṭ §66-список; spṛh R₁ wno 884 §66-правило), reuse: 5 совпадений — 4 exact (Kochergina XXVIII vidvāṃso… + Knauer Nr.5 tiryakṣu, Nr.6 ahanī, Nr.7 ājagmuṣoḥ) + 1×0.956 (Nr.5 prācāṃ deśe — орфографические варианты собственных имён), corpus_layer пуст (урок именной — зафиксировано). Вердикты гипотезы об исключениях: CONFIRMED ×3, CONFIRMED-WITH-WITNESS-GAP (Kochergina: maghavan 0 вхождений по всему файлу; ahan — списком основ в XXXI), CONFIRMED (с опечаткой HB-186).

## Проверки

- `python3 scripts/build_lesson_concordance.py` — PASS: spots 262 local OK / 17 external, catalog.mdx 23 урока, 387 строк; LOCAL_SOURCE_FILES дополнен sangram-present-perfect-participles (E12-валидация спот-фразы SG-MO-022).
- `typed_link_lint.py` — PASS: all clean.
- DeepSeek-лейн — endpoint доступен (HTTP 401, впервые за серию: H5659–H5672 давали curl 000), но ключа на боксе нет (не добываем из устаревших бэкапов по credential-контракту) → фолбэк по прецеденту: свежепроцессная проверка 130/130 PASS (review/lesson-xxv-concordance-h5676-spotcheck-07-10-2026.md).

## Ссылки

- PR: https://github.com/gasyoun/SanskritGrammar/pull/1047 (merged 07-10-2026)
- План: BUHLER_LESSON_CONCORDANCE_PLAN_2026.md (виза D1–D16, адденды E1–E13)
