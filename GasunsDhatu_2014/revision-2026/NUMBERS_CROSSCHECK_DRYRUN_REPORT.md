# Сверка чисел рукописи M03 — сухой прогон

_Created: 17-08-2026 · Last updated: 17-08-2026_

Отчет генератора [numbers_crosscheck.py](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/numbers_crosscheck.py) ([H2871](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2871-Opus_SanskritGrammar_m03-freeze-harness-gost-numbers-prebuild_16.08.26.md)), Opus 5 (`claude-opus-5`). **Сухой прогон: рукопись не изменялась.** Находки — инвентарь к предподачному проходу, а не правки.

**Охват:** 9 файлов рукописи; 77 числовых фактов в провенанс-джейсонах, из них 60 закреплено за локусами рукописи; базовая ревизия для N6 — `origin/main`.

## Классы и умолчания (политика default-and-log)

| Класс | Что считается сходящимся | Умолчание |
|---|---|---|
| `N1` | связь «колонка = колонка / колонка» держится на всех строках | связь признается за таблицей, если ей отвечают >= 3 строк и не менее двух третей строк |
| `N2` | напечатанный процент = пересчету по тем же X и Y | принимается и округление, и усечение последнего знака (усечение — засвидетельствованная практика издания, DCS-леджер H1229) |
| `N3` | «A + B = C» сходится точно | — |
| `N4` | номер ссылки есть среди заголовков/подписей | «§N» без дробной части адресует главу целиком |
| `N5` | значение провенанса встречается в рукописи | карта [numbers_anchor_map.json](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/numbers_anchor_map.json) — перегенерируется флагом `--update-map`, руками не правится |
| `N6` | мультимножество чисел файла совпадает с базовой ревизией | база — `origin/main`; на заморозке база меняется на ревизию «до правок» |

## Сводка находок

| Код | Класс | Находок |
|---|---|---:|
| `N4` | Внутренняя перекрестная ссылка | 1 |
| **Итого** | | **1** |

**Зелено (0 находок):** `N2` Процент, пересчитанный по своим же слагаемым · `N1` Производная колонка таблицы · `N3` Арифметика, выписанная в тексте · `N5` Привязка к провенансу данных 2026 г. · `N6` Дрейф чисел против базовой ревизии.

## `N4` — Внутренняя перекрестная ссылка (1)

- `02_gasuns-dhatu-PhD-text2.mdx:3231` — «Рисунок 1. Соотношение количества корней к словарным статьям» стоит в списке иллюстративного материала, но подписи «Рисунок 1» в тексте рукописи нет

## Подтверждено пересчетом (72)

Проверки, которые сошлись. Это половина ценности прохода: на заморозке они должны сойтись снова.

- 02_gasuns-dhatu-PhD-text2.mdx:1370 колонка 4 = колонка 3 / колонка 2 — все 5 строк сходятся
- `02_gasuns-dhatu-PhD-text2.mdx:688` «X из Y (Z %)»: 590 из 935 корней «рассудочного» списка Уитни (63,1 %
- `02_gasuns-dhatu-PhD-text2.mdx:3096` «X из Y (Z %)»: 590 из 935 корней Уитни (63,1 %
- `02_gasuns-dhatu-PhD-text2.mdx:3136` «X из Y (Z %)»: 590 из 935 корней Уитни (63,1 %
- `02_gasuns-dhatu-PhD-text2.mdx:4689` «X/Y (Z %)»: 749/930 корней кросс-уока (80,5 %
- `04_glava4_kross-uok-omonimiya.mdx:32` «X из Y (Z %)»: 550 из 935, то есть 58,8 %
- `07_glava7_ukazatel-zaliznyaka.mdx:41` «X из Y (Z %)»: 749 из 930 корней (80,5 %
- `07_glava7_ukazatel-zaliznyaka.mdx:65` «X из Y (Z %)»: 749 из 930 корней кросс-уока (80,5 %
- `07_glava7_ukazatel-zaliznyaka.mdx:77` «X/Y (Z %)»: 749/930 (80,5 %
- `Приложения издания 2026.mdx:81` сумма: 750 + 1 363 = 2 113
- `02_gasuns-dhatu-PhD-text2.mdx:1370` колонка 2: сумма 3 861 721 повторена в тексте (`02_gasuns-dhatu-PhD-text2.mdx:1361`)
- `02_gasuns-dhatu-PhD-text2.mdx:1370` колонка 3: сумма 5 289 873 повторена в тексте (`02_gasuns-dhatu-PhD-text2.mdx:1361`)
- `dcs_phonostats_provenance.json::per_text.Rāmāyaṇa.V` = 620385 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1378`
- `dcs_phonostats_provenance.json::per_text.Rāmāyaṇa.C` = 853340 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1378`
- `dcs_phonostats_provenance.json::per_text.Rāmāyaṇa.words` = 204959 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:4590`
- `dcs_phonostats_provenance.json::per_text.Mahābhārata.V` = 2689255 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1380`
- `dcs_phonostats_provenance.json::per_text.Mahābhārata.C` = 3711486 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1380`
- `dcs_phonostats_provenance.json::per_text.Meghadūta.V` = 8296 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1376`
- `dcs_phonostats_provenance.json::per_text.Meghadūta.C` = 11510 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1376`
- `dcs_phonostats_provenance.json::per_text.Atharvaveda (Śaunaka).V` = 159779 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1374`
- `dcs_phonostats_provenance.json::per_text.Atharvaveda (Śaunaka).C` = 212812 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1374`
- `dcs_phonostats_provenance.json::per_text.Ṛgveda.V` = 384006 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1382`
- `dcs_phonostats_provenance.json::per_text.Ṛgveda.C` = 500725 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1382`
- `dcs_phonostats_provenance.json::per_text.Ṛgveda.words` = 160783 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:4590`
- `dhatupatha_gana_stats_provenance.json::total_entries` = 2259 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:171` (+13)
- `dhatupatha_gana_stats_provenance.json::distinct_raw_forms` = 1966 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:289` (+21)
- `dhatupatha_gana_stats_provenance.json::forms_repeated` = 224 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:99` (+6)
- `dhatupatha_gana_stats_provenance.json::entries_in_repeated_forms` = 517 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1146` (+2)
- `dhatupatha_gana_stats_provenance.json::forms_in_multiple_ganas` = 183 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:87` (+4)
- `dhatupatha_gana_stats_provenance.json::per_gana.01 bhvādi` = 1166 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1158` (+1)
- `dhatupatha_gana_stats_provenance.json::per_gana.02 adādi` = 77 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1056` (+3)
- `dhatupatha_gana_stats_provenance.json::per_gana.03 juhotyādi` = 26 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:321` (+19)
- `dhatupatha_gana_stats_provenance.json::per_gana.04 divādi` = 163 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:610` (+5)
- `dhatupatha_gana_stats_provenance.json::per_gana.05 svādi` = 38 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:441` (+21)
- `dhatupatha_gana_stats_provenance.json::per_gana.06 tudādi` = 174 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:836` (+2)
- `dhatupatha_gana_stats_provenance.json::per_gana.07 rudhādi` = 25 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:351` (+33)
- `dhatupatha_gana_stats_provenance.json::per_gana.08 tanādi` = 10 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:18` (+67)
- `dhatupatha_gana_stats_provenance.json::per_gana.09 kryādi` = 71 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:910` (+6)
- `dhatupatha_gana_stats_provenance.json::per_gana.10 curādi` = 509 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:251` (+3)
- `mw_genuine_roots_enrich_provenance.json::genuine_roots` = 750 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:171` (+15)
- `mw_genuine_roots_enrich_provenance.json::distinct_genuine_slp1` = 704 — цитируется в `Приложения издания 2026.mdx:66`
- `mw_genuine_roots_enrich_provenance.json::dcs_attested` = 482 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:4235` (+1)
- `mw_genuine_roots_enrich_provenance.json::consensus_ge4_dicts` = 345 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:3543` (+1)
- `mw_genuine_roots_enrich_provenance.json::core_attested_and_ge4` = 294 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:2721` (+12)
- `mw_genuine_roots_enrich_provenance.json::tail_unattested_le1` = 101 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:429` (+8)
- `mw_genuine_roots_enrich_provenance.json::period_distribution.RV` = 361 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:4163` (+2)
- `mw_genuine_roots_enrich_provenance.json::period_distribution.AV` = 325 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:3911` (+3)
- `mw_genuine_roots_enrich_provenance.json::period_distribution.V` = 409 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:644` (+2)
- `mw_genuine_roots_enrich_provenance.json::period_distribution.B` = 424 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:746` (+6)
- `mw_genuine_roots_enrich_provenance.json::period_distribution.S` = 336 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1730` (+2)
- `mw_genuine_roots_enrich_provenance.json::period_distribution.E` = 424 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:746` (+6)
- `mw_genuine_roots_enrich_provenance.json::period_distribution.C` = 437 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:3683` (+1)
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.0.dcs_freq` = 40799 — цитируется в `Приложения издания 2026.mdx:28` (+2)
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.1.dcs_freq` = 40799 — цитируется в `Приложения издания 2026.mdx:28` (+2)
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.2.dcs_freq` = 40393 — цитируется в `Приложения издания 2026.mdx:29` (+1)
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.3.dcs_freq` = 35753 — цитируется в `Приложения издания 2026.mdx:30` (+1)
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.4.dcs_freq` = 35753 — цитируется в `Приложения издания 2026.mdx:30` (+1)
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.5.dcs_freq` = 33948 — цитируется в `Приложения издания 2026.mdx:32`
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.6.dcs_freq` = 18341 — цитируется в `Приложения издания 2026.mdx:33` (+1)
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.7.dcs_freq` = 14866 — цитируется в `Приложения издания 2026.mdx:34`
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.8.dcs_freq` = 12008 — цитируется в `Приложения издания 2026.mdx:35`
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.9.dcs_freq` = 12008 — цитируется в `Приложения издания 2026.mdx:35`
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.10.dcs_freq` = 11314 — цитируется в `Приложения издания 2026.mdx:36`
- `mw_genuine_roots_enrich_provenance.json::top20_by_dcs_freq.11.dcs_freq` = 11314 — цитируется в `Приложения издания 2026.mdx:36`
- `wordlist_clusters_provenance.json::headwords` = 323425 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1550` (+2)
- `wordlist_clusters_provenance.json::counts_types.any.2` = 375 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:798` (+4)
- `wordlist_clusters_provenance.json::counts_types.any.3` = 384 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:1554` (+4)
- `wordlist_clusters_provenance.json::counts_types.any.4+` = 52 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:952` (+7)
- `wordlist_clusters_provenance.json::counts_types.initial.2` = 108 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:726` (+7)
- `wordlist_clusters_provenance.json::counts_types.initial.3` = 21 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:41` (+17)
- `wordlist_clusters_provenance.json::counts_types.final.2` = 132 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:662` (+5)
- `wordlist_clusters_provenance.json::counts_types.final.3` = 30 — цитируется в `02_gasuns-dhatu-PhD-text2.mdx:319` (+12)

## Воспроизведение

```
cd GasunsDhatu_2014/revision-2026 && python numbers_crosscheck.py
```

_Dr. Mārcis Gasūns_
