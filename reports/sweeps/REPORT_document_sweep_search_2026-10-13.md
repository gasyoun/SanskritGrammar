_Created: 13-10-2026 · Last updated: 13-10-2026_

# /document свип поисковой волны SanskritGrammar (H6552/H6567/H6593/H6672)

_к.ф.н. М.Ю. Гасунс_

Артефакты: [patches/@easyops-cn+docusaurus-search-local+0.55.3.patch](https://github.com/gasyoun/SanskritGrammar/blob/main/patches/@easyops-cn+docusaurus-search-local+0.55.3.patch),
[scripts/search_contexts.mjs](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/search_contexts.mjs),
[src/theme/SearchPage/index.jsx](https://github.com/gasyoun/SanskritGrammar/blob/main/src/theme/SearchPage/index.jsx)
(`document_check.py`, kind=interface, --handoff H6672).

Числа: до — 20 missing на артефакт (60 батчем); после — **14 present / 0 missing / 12 n-a с причинами** (батч 26 поверхностей). Receipt-пруфы:
[batch-H6672](https://github.com/gasyoun/SanskritGrammar/blob/main/reports/sweeps/document_sweep_2026-10-13_search-counter-h6672.json) и
[патч, параллельная свипа](https://github.com/gasyoun/SanskritGrammar/blob/main/reports/sweeps/document_sweep_2026-10-13__easyops-cn_docusaurus-search-local_0.55.3.json).

| Поверхность | Вердикт |
|---|---|
| CLAUDE.md (SG) | ✏️ раздел «Site search»: единый источник scripts/search_contexts.mjs (порядок = тиры, SG_TIER_BOUNDARY=10), ручная пересборка патча, страница /search/ (PR #1096) |
| .ai_state.md (SG) | ✏️ ✅ search-wave запись: H6552/H6567/H6593/H6672, PR #1083/#1086/#1088/#1094/#1095, остатки-кандидаты (PR #1096) |
| Uprava FINDINGS | ✅ §1590 — RECIPES: mint/close под многосессионной очередью из свежего shallow-клона (e463a1a) |
| Vault 20-Areas/Ops-index | ✅ [[uprava-push-contention-fresh-clone]] + атомная заметка (db74a07) |
| changelog | ✅ записи в changelog_queue/ (h6552/h6593/h6672-файлы); /cut-release — на следующем срезе |
| handoffs_registry | ✅ написан пайплайном mint/close: 4 хендоффа 🟡→✅ archived |
| README / AGENTS.md / metadoc / sibling docs | ⛔ n/a — поиск самоочевидный UI сайта; правило живёт в CLAUDE.md; артефакты — код/патч |
| FEATURES_INDEX / REUSE_INDEX / INTERLINKS / kosha / DATA_LAYERS / SKILLS_INDEX / ARTICLES / DANGER_FACTS / QUESTIONS_LOG / MEGABOOK / SKILLS_MANUAL_RU / HOOKS_INDEX / REPO_STATUS / hub_manifest / GTD / issues / auto-views | ⛔ n/a — причины в receipt JSON (чужой продукт/каталоги/без изменений; auto-views самозалечиваются) |

Верификации волны: DeepSeek keep (H6593), Explore-субагент 11/11 PASS (H6672); живой прод — порядок «1–21 книги, Санграм с 22-й», счётчик «Найдено документов: 254», прогрев ~1 мин против холодных 2,5–3,5 мин.
