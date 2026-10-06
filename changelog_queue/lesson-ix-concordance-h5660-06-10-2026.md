### Changed
- **Поурочный конкорданс Бюлера — урок IX приземлён (H5660, OxAlpha, 06-10-2026).** Темы урока — ж. р. на ā (jāyā) + прилагательные на a, сандхи конечных ai/au, внутренние правила согласных (ch → cch; n → ṇ после приставок), частые превербы (Buhler_Unicode.mdx 1166–1300, заголовок «# УРОК IX.»). 5 тем: f-stems, ai-au-sandhi, internal-sandhi, verb-prefixes (D13-расширение), lesson-roots (лемма-слой: 13 глаголов, 11 корней). 20 новых TSV-строк (157 всего): Уитни §§347–348 (f-основы), §§132–134 (ai/au), §227 + §§189–195 (cch; n→ṇ), §§1076–1087 (превербы), Очерк §83/§42/§38/§212, Кочергина Занятие X/XIII/XXXIX, Кнауэр Nr.16/Nr.1/Nr.6, sangram-article:preverbs, dhatu-glava7, talmud-crosswalk. 14 фраз-утверждений в spots (E10), build-валидация 104/104 local OK.
- **Вердикты об исключениях:** f-stems — CONFIRMED-WITH-NUANCE (Уитни §348: корневые ā-основы «with few exceptions» ж. р., §355a мужские panthā/mahā́/gopā́ — Бюлер IX универсалию «-ā = ж. р.» не заявляет, в отличие от квантора Кочергиной X, клейма HK-14 OVERSTATED); ai-au-sandhi — CONFIRMED-WITH-NUANCE (асимметрия «обычно ā вместо ai, но āv вместо au» совпадает у Бюлера и Уитни §§133–134 дословно; З-1978 §42 несёт явное «Исключение из §§ 41 и 42» — прагрия-дв. и междометия; Кочергина XIII даёт только внутреннюю половину ai→āy/au→āv — honest gap); internal-sandhi — CONFIRMED-WITH-NUANCE (Уитни §§189–195: блокировки intervening coronals, которые Бюлер только хеджирует «в большинстве корней»; З-1978 §38 — явный список непереходов; у Кочергиной правило в сноске 21; cch-удвоения в Очерке нет); verb-prefixes — NOT-APPLICABLE; лемма-слой — GAP-DOCUMENTED: crosswalk 9/11 (śubh, mṛg — строк нет), три ловушки поиска: dī/ḍī («fly» под двумя написаниями), tṛ/tar (повтор урока II), śubh→subh «smother» — ложное покрытие (второй случай после sarj/saj урока III).
- **Reuse-кластеры урока IX:** 3 совпадения словарных строк с Kochergina (matches.json: IX.236 saṃ-gam ↔ X.184 «saṃgam Ā» 0.93; IX.240 śubh ↔ XXXIV.1269; IX.241 vart ↔ XXXIV.1259) — совпадения словарных статей, не упражнений, помечены как таковые.
- **Каталог регенерирован:** LessonConcordance/catalog.mdx — 10 уроков (I, II, III, IV, V, XXII, XXIX, XXXVIII, VI, IX), 157 link-строк; src/lesson-backlinks.json — 10 страниц-источников.

### Verification
- `python scripts/build_lesson_concordance.py` — PASS (spots validated: 104 local OK, 8 external; 10 lessons, 157 rows).
- `kosha/scripts/typed_link_lint.py LessonConcordance/typed_link_buhler_lessons.tsv` — PASS (all clean, 0 ошибок).
- DeepSeek-спот-чек (пре-авторизован MG 01-10-2026): локусы Бюлера mdx-строк — OK; 14/14 спот-фраз — дословные вхождения в названных локусах — OK; лемма-таблица против crosswalk — OK (vṛt-дубль L639/643, subh L691, dī L382 подтверждены); консистентность TSV↔topics.yml↔catalog — OK (20 строк, 5 тем). Спот-чек не поймал ни одной ошибки в новых артефактах урока IX.
- `scripts/check_generated_outputs.py` — 0 file(s) with real changes (каталог в синхроне).

### Files
- `LessonConcordance/topics.yml` — урок IX (5 тем, 14 spots, 5 вердиктов, 11 лемм)
- `LessonConcordance/typed_link_buhler_lessons.tsv` — +20 строк
- `LessonConcordance/catalog.mdx`, `src/lesson-backlinks.json` — регенерированы

_H5660 · OxAlpha (opencode/z-ai/glm-5.3-flash) · 06-10-2026_
