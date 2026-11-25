# Metadoc — DHATU_DERIVATIONAL_FAMILIES_2026-11-25.md

_Created: 25-11-2026 · Last updated: 25-11-2026_

_к.ф.н. М.Ю. Гасунс_

**Subject:** [DHATU_DERIVATIONAL_FAMILIES_2026-11-25.md](https://github.com/gasyoun/SanskritGrammar/blob/main/reports/DHATU_DERIVATIONAL_FAMILIES_2026-11-25.md)

## Purpose

The record of H6256: a 5,745-root dhātu → substantives dataset with family-size
distribution against DCS lemma frequency, plus a 10-root manually checked canary.
Answers "how large are MW derivational families and do they track corpus
frequency" once, without re-deriving the join.

## Audience

Future sessions extending the dataset; referees of the derivational-productivity
work; anyone about to cite a family-size number.

## Provenance

- Handoff: [H6256](https://github.com/gasyoun/Uprava/blob/main/handoffs/H6256-OxAlpha_SanskritGrammar_dhatu-derivational-families_08.10.26.md) (OxAlpha lane, MiMo v2.6 Flash `ollama-cloud/mimo-v2.6-flash`, 25-11-2026).
- Builder: [build_dhatu_families.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_dhatu_families.py) + [dhatu_families_lib.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/dhatu_families_lib.py).
- Data: Cologne `csl-orig/v02/mw` + `MWderivations/step4`, `kosha/data/frequency/lemma_frequency.tsv` (DCS-conllu, read-only).
- Machine check: `python scripts/build_dhatu_families.py --verify` (exit 0 = 5,745 roots / 24,353 edges / 10 canary verdicts / report tables consistent).
