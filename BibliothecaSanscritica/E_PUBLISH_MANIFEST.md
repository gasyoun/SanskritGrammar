# Bibliotheca Sanscritica — e-publish manifest (волна 1)

_Created: 13-09-2026 · Last updated: 13-09-2026_

**Handoff:** [H4628](https://github.com/gasyoun/Uprava/blob/main/handoffs/H4628-OxAlpha_SanskritGrammar_e-publish-wave1-toms-II-V_12.09.26.md) · **Executor:** OxAlpha (opencode/z-ai/glm-5.3-flash) · **Gate:** none · **Sources:** `yadisk:Bibliotheca/` + `yadisk:Sanskrityatina/33_Lihusina/` (mtime 10–13.09.2026)

Mechanics-only verbatim extraction (no prose rewriting). Derived-only: `.idml`/`.indd`/print-final PDFs never committed. Coverage gate: `python3 tools/idml_coverage_check.py <source> <mdx>` (independent re-extraction, token+char, floor 90%; `--source-kind pdf` for PDF sources via words-mode).

## Волна 1 (MG D1 12-09: тома II–V)

| Том | mdx | Источник (новейший доступный) | Coverage | Примечание |
|---|---|---|---|---|
| II — Фриш, хрестоматия ч. 2 | [Tom_II_Frish/FrishII_chrestomathy_2022.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/Tom_II_Frish/FrishII_chrestomathy_2022.mdx) | `yadisk:Bibliotheca/02 том II/В печать/Frish_II_24.12.22.idml` | **GREEN** 99.3% tok / 94.5% char | 500 stories, 544 абз., 26 863 зн., 82 деванагари. ⚠️ Хрестоматийный корпус — плашки-изображения (нет текстового слоя ни в idml, ни в `!Frish_II_20.02.2023.pdf`, 370 стр.): в mdx вошёл живой текст вёрстки 2022 (предисловие к 3-му изд., библиография оцифрованных словарей и др.). Полный текст корпуса = OCR-дорожка, вне волны 1 |
| III — Кнауэр, учебник | [Tom_III_Knauer/Knauer_uchebnik_2021.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/Tom_III_Knauer/Knauer_uchebnik_2021.mdx) | `yadisk:Bibliotheca/03 том III/Кнауэр 2021/старый кнауэр Folder/knauer-17.12.2020 Folder/knauer-17.12.2020.idml` | **GREEN** 99.9% tok / 99.8% char | 57 stories, 376 абз., 201 946 зн., 2 166 деванагари — ПОЛНЫЙ текст учебника (один сквозной story u114f ≈ 177 кЗн). Новейший .idml-производный источник (позже «старый кнауэр.idml» 17.12.2020) |
| IV — Лихушина, хрестоматия | [LihushinaChrestomathy_2015/LihushinaChrestomathy_2015_pilot.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/LihushinaChrestomathy_2015/LihushinaChrestomathy_2015_pilot.mdx) | `yadisk:Sanskrityatina/33_Lihusina/lihusina-15.12.14.idml` (H4484 pilot, не перегенерировался) | **GREEN** 99.7% tok / 99.7% char (H4628 ре-проверка) | 36 stories, 2 628 абз., 404 926 зн., 75 918 деванагари; 92.9% vs внешний контроль-верста 09.2014 (H4484) |
| V — Миллер, руководство | [Tom_V_Miller/Miller_blok_2021_live_text.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/Tom_V_Miller/Miller_blok_2021_live_text.mdx) | `yadisk:Bibliotheca/05 том V/Миллер 2021/В печать/04 miller-blok-24.02.2021.pdf` (PyMuPDF, `tools/pdf_to_mdx.py`) | **GREEN** 100% / 100% (words-mode независимая дорожка) | 298 стр. с текстом, 23 164 зн., 127 деванагари — живой текст блока 2021 (титул, «Списокъ лигатуръ письма деванагари», колофон). ⚠️ Корпус руководства — плашки (304 стр., 13 стр. с текстом>50 зн.). `.idml`-полных экспортов нет (`Miller.idml` = элемент-заглушка 982 зн.; `miller-29.07.idml` = частичный 20 610 зн.). Полный текст = OCR-дорожка, вне волны 1 |

**Итог волны 1:** 4/4 тома имеют цифровую редакцию живого текста, coverage-check зелёный по всем четырём; полные тексты корпусов II и V — на OCR-дорожке (плашки-переиздания, живой вёрстки нет).

## Пайплайн

- `tools/idml_to_mdx.py <in.idml> <out.mdx> --source-path yadisk:… [--title …] [--status …]` — H4484 экстрактор, H4628: пер-томное происхождение в шапке.
- `tools/pdf_to_mdx.py <in.pdf> <out.mdx> --source-path yadisk:…` — H4628: PyMuPDF текстовый слой (poppler на кириллице запрещён — не используется).
- `tools/idml_coverage_check.py <source> <mdx> [--source-kind pdf]` — H4628: независимая переэкстракция источника (все Content всех Story без сортировки / words-mode) → token+char покрытие, зелёный пол 90%.

_Др. Марцис Газунс_
