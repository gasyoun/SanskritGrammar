# Урок XXXV конкорданса Бюлера приземлён (H5686)

_Repo: gasyoun/SanskritGrammar · Source: LessonConcordance_ · Date: 2026-10-08_

## Что

Поурочный конкорданс Бюлера дополнен уроком XXXV — первым атематическим уроком серии: сильная/слабая основы шести атематических классов (II, III, V, VII, VIII, IX) и распределение сильных форм, V класс no/nu (nav/nv, факультативное n, hi-отпадание/удержание, śru→śṛ) с парадигмами su и āp в 4 наклонениях, 2 sg. imper. dhi/hi/нуль + Pot. par. yā (3 pl. uḥ) + tāt-благословение, среднее причастие -āna- (āsīna). 24 TSV-строки, 5 тем, 11 HB-утверждений (HB-49, HB-277–286 — все TRUE/JUSTIFIED), лемма-слой 10/12 (star и niś-строк в crosswalk нет — честно; nis- у Бюлера без корня и класса; 7 из 10 классовых расхождений гана-традиции V-класса против морфонологических рядов A/I/U/R записаны как уровни классификаций, не ошибки; двойные z-серии śak A₁/I₁, śru U₁/R₁, hū U₂/I0). Уитни-якоря верифицированы по живому Wikisource: §599–604 (инвентарь non-a классов + strong/weak, nu-класс прямо с sunu/āpnu), §566 (оптатив yús), §§570–571 (tāt). Вердикты гипотезы об исключениях: CONFIRMED-WITH-NUANCE ×3 (классификационная вилка śṛṇo-: V класс у Бюлера vs VII-формула у З-1978 §135; tāt/dhi-дыры З-1978 и Кочергиной), CONFIRMED ×1 (причастие -āna-: āsīna выписан самим Бюлером). reuse: 1×0.956 (buhler XXXV.812 ↔ knauer Nr.12.272 — somaṁ sunvatām), corpus_layer пуст (честно).

## Проверки

- `python3 scripts/build_lesson_concordance.py` — PASS: spots 362 local OK / 19 external (после merge origin/main), catalog.mdx 31 урок (с XXXIV параллельного H5685), 559 строк.
- `typed_link_lint.py` — PASS: all clean.
- Свежепроцессная верификация 15/15 спот-фраз PASS + 11/11 HB + 24/24 TSV-строк (review/lesson-xxxv-concordance-h5686-spotcheck-08-10-2026.md); DeepSeek-лейн — auth-store без ключа на боксе (прецедент серии H5676/H5684) → фолбэк по прецеденту.

## Ссылки

- План: BUHLER_LESSON_CONCORDANCE_PLAN_2026.md (виза D1–D16, адденды E1–E13)
