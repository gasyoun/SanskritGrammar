# Урок XX конкорданса Бюлера приземлён (H5671)

_Repo: gasyoun/SanskritGrammar · Source: LessonConcordance_ · Date: 2026-10-07_

## Что

Поурочный конкорданс Бюлера дополнен уроком XX (согласные основы): окончания nau и выпадение s, классификация одна/две/три основы (сильная/средняя/слабая), нейтрализация конечных t/d/dh/bh, перенос придыхания (budh→bhut), согласование прилагательного при существительных разных родов. 19 TSV-строк, 5 тем, 9 HB-утверждений (HB-31, 151–158: 8 TRUE + HB-158 UNTESTABLE→замерено 2/4), лемма-слой 2/2 (ruh U₁; labh A₁ с двумя z-сериями A1/N1) + каузативные cross-loci (whitney-sec:1042, kochergina:XXXV — из salvage-версии при dual-run адъюдикации), reuse: 4 exact Kochergina XXX + честный «0 Knauer-кластеров» (материал Кнауэра — Nr.6/Nr.7 без построчных совпадений), corpus_layer пуст (урок именной — зафиксировано).

## Проверки

- `python3 scripts/build_lesson_concordance.py` — PASS: spots 233 local OK / 17 external, catalog.mdx 21 урок, 346 строк.
- `typed_link_lint.py` — PASS: all clean.
- DeepSeek-лейн — 3 попытки (Errno 49 / curl 000, тот же отказ, что H5670/H5659) → фолбэк: свежепроцессная проверка 33/33 PASS (review/lesson-xx-concordance-h5671-spotcheck-07-10-2026.md).

## Ссылки

- PR: <заполнить при открытии>
- План: BUHLER_LESSON_CONCORDANCE_PLAN_2026.md (виза D1–D16, адденды E1–E13)
