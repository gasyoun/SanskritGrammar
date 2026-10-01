# Bibliotheca Sanscritica — e-publish wave 1 report (H4642)

_Created: 13-09-2026 · Last updated: 13-09-2026_

**Handoff:** [H4642](https://github.com/gasyoun/Uprava/blob/main/handoffs/H4642-OxAlpha_SanskritGrammar_bibliotheca-epub-wave1_13.09.26.md) · **Executor:** OxAlpha (opencode/z-ai/glm-5.3-flash) · **Rulings:** MG 13-09-2026, D1 (idml wave = toms II–V via the pilot-proven extractor) + D3 (tom XVIII never prints → e-publish from final block PDF).

## Deliverables

| Том | Digital edition | Source of record | Stats (extractor-reported) |
|---|---|---|---|
| II | [FrishChrestomathyII_2022/](https://github.com/gasyoun/SanskritGrammar/tree/main/BibliothecaSanscritica/FrishChrestomathyII_2022) | `yadisk:Bibliotheca/02 том II/В печать/Frish_II_24.12.22.idml` (2022-12-24) | 500 stories, 544 paras, 26 863 chars, 82 Devanagari |
| III | [KnauerUchebnik_2021/](https://github.com/gasyoun/SanskritGrammar/tree/main/BibliothecaSanscritica/KnauerUchebnik_2021) | `…/03 том III/Кнауэр 2021/старый кнауэр Folder/knauer-17.12.2020 Folder/knauer-17.12.2020.idml` (2020-12-17) | 57 stories, 376 paras, 201 946 chars, 2 166 Devanagari |
| IV | [LihushinaChrestomathy_2015/LihushinaChrestomathy_2015.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/LihushinaChrestomathy_2015/LihushinaChrestomathy_2015.mdx) | `yadisk:Sanskrityatina/33_Lihusina/lihusina-15.12.14.idml` (2014-12-16) | 36 stories, 2 628 paras, 404 926 chars, 75 918 Devanagari |
| V | [MillerRukovodstvo_2021/](https://github.com/gasyoun/SanskritGrammar/tree/main/BibliothecaSanscritica/MillerRukovodstvo_2021) | `…/05 том V/сканы для сверки/miller-29.07.idml` (2020-10-20; the `Miller Folder/Miller.idml` is cover/front-matter only, 989 chars — body idml used instead) | 24 stories, 229 paras, 22 154 chars, 222 Devanagari |
| XVIII | [KanunDrevneindiyskoyFilosofii_2022/](https://github.com/gasyoun/SanskritGrammar/tree/main/BibliothecaSanscritica/KanunDrevneindiyskoyFilosofii_2022) | `…/18 том XVIII/В печать/Канун древнеиндийской философии.pdf` (2022-12-02, 272 pp) | 270 pp with text (+2 empty), 454 101 chars, 0 Devanagari (Russian prose — expected) |

Extractors: [tools/idml_to_mdx.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tools/idml_to_mdx.py) (generalized: `--key=value` front-matter overrides; no-flag output re-verified **byte-identical** to the committed H4484 pilot) and new [tools/pdf_to_mdx.py](https://github.com/gasyoun/SanskritGrammar/blob/main/tools/pdf_to_mdx.py) (PyMuPDF; poppler banned on Cyrillic). Standing never-print directive: [STANDING_DIRECTIVE_neverprint_toms_epub_2026-09-13.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BibliothecaSanscritica/STANDING_DIRECTIVE_neverprint_toms_epub_2026-09-13.md).

## Spot-checks (evidence)

- **Extractor fidelity:** re-extraction of the pilot idml reproduced the committed pilot mdx **byte-identical** (36/2 628/75 918 — matches the H4484 numbers).
- **Tom II:** zip-internal typesetter copy `Frish_II_24.12.idml` re-extracted → identical story/para/char/Devanagari counts (content-equal; kept the `В печать` copy as source of record).
- **Tom IV:** final mdx body == pilot body (same source idml, same tool path).
- **Tom XVIII:** Cyrillic text layer dense from page 1 (title page reads correctly); 270/272 pages carry text.
- **Tom III (Knauer):** sampled 20 mdx paragraphs vs the newer companion export `knauer_24.12.2020.pdf` (59 pp, 133 369 chars): 9/20 literal hits; all misses are glyph-encoding variance (pre-1918 ѣ/Ѳ/‡/U+2010, soft hyphens) plus one-week revision drift (export 24.12 vs idml 17.12). The extraction tool itself is pilot-proven byte-identical.

## Limitations / honest residue

- **Tom II:** the 2022 re-set carries only the newly typeset Russian companion (front matter, alphabet guide, bibliography) as text; the Sanskrit chrestomathy plates are placed images/vectors in the print PDF (370 pp, 47.7 K extractable chars, ~0 Devanagari). Full-text e-publish of the Sanskrit part needs vision OCR — out of wave-1 scope.
- **Tom III & V:** the 2021 print blocks (`blok_2021.pdf` 306 pp / `04 miller-blok-24.02.2021.pdf` 304 pp) are **facsimiles with no text layer** (3 and 23 K chars respectively). The wave-1 mdx files cover the typeset companion matter; the facsimile bodies need OCR — out of wave-1 scope.
- Tom III's separate companion «Сводный указатель суффиксов санскрита» (own idml) not extracted in wave 1.

Derived-only respected: no `.indd`/`.idml`/print-production PDF committed.

_Гасунс_
