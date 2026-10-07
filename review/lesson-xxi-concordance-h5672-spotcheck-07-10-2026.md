# H5672 — spot-check протокол: урок XXI (07-10-2026)

_Verifier: OxAlpha (`opencode/z-ai/glm-5.3-flash`), независимая свежепроцессная проверка._

## Lane

- **DeepSeek-лейн недоступен** (curl-проба `api.deepseek.com` → HTTP 000, сетевой уровень; 07-10-2026) — повтор прецедентов H5659/H5670 (где 3 попытки + curl 000).
- Fresh-context subagent-делегация отклонена на правах сессии (permission-reject, task никогда не стартовал) — QA выполнена **в процессе**, независимым код-путём от build-генератора (build-валидация E12 остаётся первым, независимым барьером).

## Ledger — 33 checks

- HB-привязки: HB-32 (loc 2715), HB-159 (2743), HB-160 (2745), HB-161 (2747), HB-162 (2763), HB-163 (2771) — loc + verdict_fact TRUE — **12/12 CONFIRMED** (прямо из claims.yml).
- Таблицы урока XXI (mdx): L.pl vākṣu/rukṣu/dikṣu (строка 2741) и dviṭsu/viṭsu/liṭsu + I.pl dviḍbhiḥ/viḍbhiḥ/liḍbhiḥ (2759/2761); заголовок `# УРОК XXI` без точки (2715) — **CONFIRMED**.
- Crosswalk-леммы: dam 343/control/M₁→M₂; druh 385/U₁→U₁; dhṛ 402/R₁→R₁; bhṛ 530/R₁→R₁; svaj 900/A₁→A₁; hṛ 923+924/R₁; **GAP sṛj подтверждён** (0 строк) — **7/7 CONFIRMED**.
- matches.json reuse-квадруплет: XXI.464↔kochergina XIV.299 (1.0), XXI.465↔XIV.300 (0.958), XXI.475↔knauer 5.96 (1.0), XXI.484↔kochergina XXX.758 (0.947) — **CONFIRMED**.
- Уитни §§: 217 (c→k reversion), 218 («reversions of final ç to k… diç, dṛç, spṛç, and optionally naç»), 219 (j split yuj/rāj), 222–223 (h-классы; §223b lih в ruh-классе — ось классификации отлична от деклинационной liṭsu), 165 («even before su») — **6/6 CONFIRMED**.
- Зализняк §35 п. 1: триггеры «после k, r и любой гласной, кроме a/ā» — **l НЕ назван** (утверждение topics.yml о расхождении с Бюлеровым «k, r и l») — **CONFIRMED**.
- catalog.mdx (перегенерирован): заголовок `## Урок XXI —`, 5 topic-заголовков, 6 HB-ссылок, лемма-таблица 7 строк, таблицы сбалансированы — **CONFIRMED**.
- Spot-фразы: 11 локальных (3×Z-§34/§45, 3×Kochergina XXX, 1×Kochergina X, 2×Knauer Nr.5, 1×sangram, 1×dhatu) — байт-точно в источниках (build-валидация E12: 232 local OK / 12 external).

## Дефекты первичного прогона чекера (не данных)

2 ложных FAIL: (1) проверка таблиц по неверным индексам строк (liṭsu искался в таблице §1 вместо §2а), (2) срез секции XXI упирался в `## Урок XXII` (префикс-коллизия `c.index('## Урок XXI')`). Исправлены и перегнаны — все проверки зелёные. Один аналог ловушки у H5670.

## VERDICT: PASS (33/33 после перегонки)
