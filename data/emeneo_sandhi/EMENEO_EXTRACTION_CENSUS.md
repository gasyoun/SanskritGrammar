# Emeneo sandhi-exercises → sandhi-drills gold enrich — extraction census

_Created: 13-09-2026 · H4486 (OxAlpha drain, class: data)_

Source: yadisk `Санскрит/18_Эмено/` — Emeneau & van Nooten, *Sanskrit Sandhi
and Exercises* (2nd revised edition), three .doc vintages (2016/2017/2019) +
one OCR pdf. `.doc` files stay local (handoff constraint); text extractions
are committed under `extracted/` (doc→html via macOS `textutil`, html→txt via
stdlib HTMLParser — no poppler, no LibreOffice/pandoc on this box).

## Census (regenerable: `python3 scripts/build_emeneo_sandhi_drills.py`)

| file | paragraphs | exercise headings | numbered item marks |
|---|---|---|---|
| emeneo-sandhi-exercises-2016.txt | 362 | ~24 (heading-glued) | ~260 |
| emeneo-sandhi-exercises-2017.txt | 387 | 26 | ~280 |
| emeneo-sandhi-exercises-2019.txt | 462 | 26 (all detected) | ~330 |

Machine-readable: `emeneo_items_census.tsv`, `emeneo_build_summary.json`.

## Verdict per source

- **2019 = primary** — cleanest extraction, all 26 exercise headings intact,
  bilingual EN+RU item glosses, MG course-lesson anchors («После X занятия»).
- **2016/2017 = duplicate vintages** of the same pamphlet (older conversion
  artifacts: glued headings, PAGE-field garbage at tail). Census only; no
  drills derived from them. The enrichment value is in the 2019 vintage.
- **sandhi-exercises_OCR.pdf — not used.** Same content as the .doc set;
  Devanagari/IAST OCR text layers on Sanskrit2003-class fonts are unreliable
  (DANGER_FACTS trap). The .doc text extractions supersede it.

## Drill harvest (from the 2019 vintage)

- External-sandhi exercises 11, 12, 13, 14 → 37 sentence items → split into
  **80 junction drills** (73 join + 22 identify… see summary JSON for final
  counts) + **15 verified compound drills** (Ex 11b + 14a) → **95 drills**.
- Format: kosha `sandhi-drills` gold columns (see EMENEO_FORMAT_MAPPING.md).
- Every answer is derived by the committed junction engine (rules 41–71) and
  parity-gated against **37 worked examples printed in the pamphlet itself**
  (`parity: 37/37` in the build output; also enforced by
  `tests/test_emeneo_sandhi_drills.py`).
- Documented exclusions (5 junctions/compounds + 1 phrase-context rule):
  ambiguous or morphology-dependent junctions are excluded, never guessed —
  full list in `emeneo_build_summary.json` (`excluded`) and in
  EMENEO_FORMAT_MAPPING.md.

_Dr. Mārcis Gasūns_
