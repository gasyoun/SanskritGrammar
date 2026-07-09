# revision-2026 — рабочие материалы подготовки печатного издания 2026 г.

_Created: 07-07-2026 · Last updated: 08-07-2026_

Working notes for the 2026 print edition of Gasūns, «Состав и строй древнеиндийских корней»
([H246](https://github.com/gasyoun/Uprava/blob/main/handoffs/H246-Fable_GasunsDhatu_2026_printed_book_prep_06.07.26.md), private hub).
These `.md` files are deliberately **not** `.mdx` — the Docusaurus site only includes
`GasunsDhatu_2014/**.mdx`, so nothing here is published on the public reading site.

| File | What it is |
|---|---|
| [PROPOSALS.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/PROPOSALS.md) | Draft rewrites of положения П1/П4/П7/П9/П10 + parked content questions — **every item needs the author's sign-off** |
| [PALSULE_AUDIT.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/PALSULE_AUDIT.md) | C10/L1 audit: concordance's Palsule-driven exclusions checked against the digital (vidyut) dhātupāṭha, starting with `4añc` |
| [CH2_PILOT_MEMO.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/CH2_PILOT_MEMO.md) | H358 pilot report: Гл. 2 reworked monograph-style (2026 data merged into §2.3–§2.4 prose, Выводы rewritten, «было 2014/стало 2026» provenance footnotes); method verdict for Гл. 1/3/Обзор — **continuation is the author's call** ([PR #55](https://github.com/gasyoun/SanskritGrammar/pull/55), no auto-merge) |
| [LITREVIEW_DATA_MAP.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/LITREVIEW_DATA_MAP.md) | H384 pre-assembly: which 2026 resources touch the Обзор литературы (thin, mostly indirect — count numbers → §2.4, Whitney→Zaliznyak→Tolchelnikov line → §3.2); the "Корректировка 1" data-map, like PALSULE_AUDIT for Гл. 2 |
| [LITREVIEW_MEMO.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/LITREVIEW_MEMO.md) | H384 rework report: Обзор restructured chronological→problem-oriented around the book's 3 questions (what is a root / how many / how to record); −353 lines net, facts/citations moved-not-invented, 2 provenance footnotes `[^edlr1]`/`[^edlr2]`, ~35 Д2 (logic/composition) RWS findings closed, rest to H385 ([PR](https://github.com/gasyoun/SanskritGrammar/pulls), no auto-merge) |
| [panini_sutra.py](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/panini_sutra.py) | H413 Aṣṭādhyāyī sūtra resolver over the public [ashtadhyayi-com/data](https://github.com/ashtadhyayi-com/data) dataset — backs the `/panini-sutra-lookup` skill (reference `a.p.n` or keyword → Devanagari + IAST + Vasu + sūtrārtha + `--commentary` Kāśikā/Mahābhāṣya/vārttika + paste-ready `ср. Aṣṭādhyāyī a.p.n`). For RWS `panini-traditional` sūtra-reference edits (RWS_REPORT.md §6.6) |
| [varga_shares.py](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/varga_shares.py) | Reproducible aggregation: 25 sparśa varṇas → 5 vargas × 5 DCS time slots, shares + Cramér's V (replaces the χ² p-value Табл. 5, defect L7) |
| [varga_shares.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/varga_shares.csv) | Its output (source: VisualDCS `derived-data/Fonetika/regen-2026/varna_freq.csv`, DCS pin 2026-03-05) |
| — | **Canonical sibling:** the same aggregation was built independently the same night as a VisualDCS dataset — [derived-data/Fonetika/varga-series-diachrony/](https://github.com/gasyoun/VisualDCS/tree/main/derived-data/Fonetika/varga-series-diachrony) (counts byte-identical, Cramér's V = 0.037 agrees; registered in PROJECT_INTERLINKS as "consume — don't re-aggregate"). For anything beyond this book, consume that; its [slot_era_map.csv](https://github.com/gasyoun/VisualDCS/blob/main/derived-data/Fonetika/varga-series-diachrony/slot_era_map.csv) also gives an empirical slot→era mapping (slot 5 ≈ medieval ~1000–1700 CE) that refines the dissertation-era labels used in the book's Табл. 5 — a candidate footnote for the author. |

## H382 — пересчёт Таблиц 1-4 и «слогов на слово» (§2.5)

Пересчёт ВСЕХ вычислительных данных §2.5 издания 2014 г. на открытых воспроизводимых корпусах 2026 г. (решение автора от 08-07-2026; H382). Итог: коэффициент C/V (Табл. 1) и топ-кластеры (Табл. 2-3) **подтверждают** 2014 г.; Табл. 4 и качественные тезисы положений 5-6 **пересмотрены** (иной словник, прозрачный метод).

| File | What it is |
|---|---|
| [DATA_RECOMPUTE_MEMO.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/DATA_RECOMPUTE_MEMO.md) | Памятка: старое число → новое, метод, дельта, что изменилось в выводах и положениях 5/6/7 |
| [dcs_text_phonostats.py](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/dcs_text_phonostats.py) | Воспроизводимый скрипт Табл. 1-3 + слогов/слово по DCS (пин 2026-03-05), фильтр по `<textName>` |
| [table1_consonant_coefficient.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/table1_consonant_coefficient.csv) | Табл. 1: V, C, коэффициент C/V, слогов/слово по 4 текстам 2014 г. + Ригведа |
| [table2_rigveda_clusters.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/table2_rigveda_clusters.csv) · [table3_ramayana_clusters.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/table3_ramayana_clusters.csv) | Полные списки кластеров Ригведы (360 типов) и Рамаяны (376 типов) с частотами + 2 примера-слова |
| [syllables_per_word.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/syllables_per_word.csv) | Слогов/слово по 5 текстам + итог |
| [wordlist_clusters.py](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/wordlist_clusters.py) | Воспроизводимый скрипт Табл. 4 по союзному словнику `union_headwords.tsv` (323 425 заголовков) |
| [table4_word_clusters.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/table4_word_clusters.csv) · [table4_word_clusters_full.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/table4_word_clusters_full.csv) | Табл. 4: сводка (разновидности по позиции, старое-2014 рядом) + полный список типов |

_Dr. Mārcis Gasūns_
