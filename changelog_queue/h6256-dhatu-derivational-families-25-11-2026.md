[Reading 19 lines from start (total: 19 lines, 0 remaining)]

### Changed
- **Деривационные гнёзда dhātu против частотности DCS (H6256, OxAlpha / MiMo v2.6 Flash `ollama-cloud/mimo-v2.6-flash`, 25-11-2026).** Датасет [families.json](https://github.com/gasyoun/SanskritGrammar/blob/main/data/dhatu_families/families.json) — 5,745 корней (канонический dhātu-инвентарь), 24,353 ребра root→derivative, 23,545 уникальных substantives; атрибуция по MW `genuineroot` без upasarg из пяти каналов MW/MWderivations (`mw_etymology`, `root_oracle[mw]`, `mw_deriv`, `mw_pfxderiv`, `analysis2_decomp`), частоты — LEFT-JOIN канонического `lemma_frequency.tsv` kosha (DCS-conllu). Отчёт [DHATU_DERIVATIONAL_FAMILIES_2026-11-25.md](https://github.com/gasyoun/SanskritGrammar/blob/main/reports/DHATU_DERIVATIONAL_FAMILIES_2026-11-25.md): покрытие 608/5,745 корней с ≥1 производным, 49.9% производных с DCS-частотой, Spearman ρ=0.831 между размером гнезда и суммарной частотой, наклон rank–frequency −1.971. Canary: 10 корней сверены с сырыми записями `mw.txt` — 4 AGREE, 3 DISCREPANCY, 3 WEAK-EVIDENCE (все расхождения задокументированы в `canary_verdicts.tsv`, чистка не скрыта). Это НЕ dhatupatha-парность H4741/Q4.4: структура и статистика семей идут из MWderivations + MW.

### Verification
- `python scripts/build_dhatu_families.py --sources-root ~/Documents/GitHub` — exit 0 (5,745 корней / 24,353 рёбер), детерминированный offline-прогон.
- `python scripts/build_dhatu_families.py --verify` — VERIFY PASS (таблицы отчёта пересчитаны из `families.tsv`, canary 10/10).
- `python -m ruff check scripts/build_dhatu_families.py scripts/dhatu_families_lib.py --select E9,F63,F7,F8` — All checks passed.

### Risks
- Строгое множество атрибуции (750 MW `genuineroot` минус upasargi) даёт 89.4% корней с гнездом размера 0 — это измеренное покрытие, а не баг; расширение на m4/vidyut-корни потребует отдельной проверки против ложных гнёзд (`su-`, `pra-`, `vi-`).
- Canary показал 6/10 слабых или расходящихся атрибуций в канале `mw_etymology` (глагольные омонимы, кросс-ссылки `See √`, путаница омонимов homonym confusion); numbers надо цитировать как оценку с оговоркой.
- П-frequency source pin: kosha `lemma_frequency.tsv` — снимок DCS ~5.7M токенов; пересчёт при обновлении корпуса будет требовать `--sources-root` на новый снимок.

### Files
- `scripts/build_dhatu_families.py`, `scripts/dhatu_families_lib.py` — новые
- `data/dhatu_families/{families.json,families.tsv,root_stats.tsv,canary_10.tsv,canary_verdicts.tsv}` — новые
- `reports/DHATU_DERIVATIONAL_FAMILIES_2026-11-25.md` + `.meta.md` — новые

_H6256 · OxAlpha (MiMo v2.6 Flash, `ollama-cloud/mimo-v2.6-flash`) · 25-11-2026_