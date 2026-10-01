# gasuns-dissertation — derived corpus (H4479)

_Created: 13-09-2026 · Last updated: 13-09-2026_

Derived-only corpus land of M. Gasūns' PhD dissertation «Состав и строй
древнеиндийских корней: история изучения» (2014, ИЯз РАН) for the
GasunsDhatu_2014 → revision-2026 lane.

- **Source (not committed):** `yadisk:Sanskrityatina/34_Диссертация/Итоговый текст/`
  — 7 PDFs mirrored into `src/` (gitignored). Defence transcripts
  (`стенограмма*`) are **out of scope** (personal data).
- **Method:** PyMuPDF text-layer extraction; poppler `pdftotext` is forbidden on
  Cyrillic PDFs (plausible-blank trap). Extraction verdicts:
  [EXTRACTION_REPORT.json](EXTRACTION_REPORT.json) — 7/7 PASS, 508 pages,
  ~974k chars.

## Artifacts

| File | What |
|---|---|
| [text/*.jsonl](text/) | per-page text records: `{file, page, verdict, stats, text}` — 7 volumes |
| [toc_index.json](toc_index.json) | volume map + 31-entry Оглавление of the main text (printed pages) |
| [claim_census.json](claim_census.json) / [claim_census.md](claim_census.md) | dhātu-claim census + mapping to revision-2026 (PALSULE_AUDIT lane) |
| [extract_text_layer.py](extract_text_layer.py) | extraction + fail-loud quality gate |
| [build_toc_index.py](build_toc_index.py) | TOC builder |
| [build_claim_census.py](build_claim_census.py) | census builder |

**Sibling land (same handoff, earlier session):**
[GasunsDhatu_2014/revision-2026/phd_corpus/](https://github.com/gasyoun/SanskritGrammar/tree/main/GasunsDhatu_2014/revision-2026/phd_corpus)
— supplements JSONL + root-level concordance census (3 687 entries, 35.9 %
Palsule-only) from the .xlsm. Dual-run parity: independent PyMuPDF extractions
agree byte-for-byte on sampled concordance pages (verifier evidence).

## Regenerate

```bash
rclone copy "yadisk:Sanskrityatina/34_Диссертация/Итоговый текст" src \
  --include "0*_*.pdf"
python3 extract_text_layer.py && python3 build_toc_index.py && python3 build_claim_census.py
```

_Dr. Mārcis Gasūns_
