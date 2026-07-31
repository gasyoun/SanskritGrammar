# Metadoc — RU_SANSKRIT_GRAM_ABBREV_TERMINOLOGY_CROSSWALK_2026-07

_Created: 31-07-2026 · Last updated: 31-07-2026_

## Purpose

Durable crosswalk of high-frequency PWG grammatical abbreviation families against the fixed SanskritGrammar corpus (11 books) + LES-1990 + Kochergina dictionary article text, so pwg_ru does not invent Russian calques where Russian Indology already tags Latin.

## Audience

- H2047 sheet remake / H1303 `RU_MAP` maintainers
- Future Fable dual-run comparison against this Grok pass
- Anyone voting non-case grammar abbreviations for pwg_ru

## Provenance

| Field | Value |
|---|---|
| Handoff | [H2048](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2048-Fable_SanskritGrammar_ru-sanskrit-gram-abbrev-crosswalk_31.07.26.md) |
| Intended executor | Fable 5 (`claude-fable-5`) |
| Actual executor this file | Grok 4.5 (`grok-4.5`) — override dual-run |
| Prior art | ABBREV_UNIFIED_LIST_PROPOSAL · ABBREV_LES1990_SRAVNENIE · ABBREVIATIONS_RU |
| MG locks used | Cases Latin-stay 31-07-2026 |

## Ranked improvement backlog

1. Full re-sample of remaining named СЯР dictionaries on samskrtam.ru (Kossovich, Frish, Knauer dict, Kudriavsky) with per-token counts.
2. If Elizarenkova full book is added as MDX, re-check for any compact legend (PDF layer had none).
3. Align H1303 sheet defaults programmatically to this matrix (code change in SanskritLexicography — out of this handoff’s non-goals).
4. Human ratification pass for LES-owned shorts (`прич.`, `инф.`, number +«ч.») vs Latin-stay for density.

## Limitations

- Wide multi-source table cells are citation pointers, not exhaustive frequency counts.
- Elizarenkova local tree is PDF-only; Morphology 1975 is English-only; Talmud uses different metalanguage (МП).
- Apte “abbreviations” list is source-sigla only.
- Dual-run: Fable may disagree on non-case recommendations — keep both artifacts until a human decides.

## Related docs

- Subject: [RU_SANSKRIT_GRAM_ABBREV_TERMINOLOGY_CROSSWALK_2026-07.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RU_SANSKRIT_GRAM_ABBREV_TERMINOLOGY_CROSSWALK_2026-07.md)
- LES comparison: [ABBREV_LES1990_SRAVNENIE_2026-07.md](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/pwg_ru/ABBREV_LES1990_SRAVNENIE_2026-07.md)
- H1303 proposal: [ABBREV_UNIFIED_LIST_PROPOSAL_2026-07.md](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/pwg_ru/ABBREV_UNIFIED_LIST_PROPOSAL_2026-07.md)

## Revision history

| Date | Change | By |
|---|---|---|
| 31-07-2026 | Initial dual-run crosswalk (Grok) | Grok 4.5 (`grok-4.5`) |

_Dr. Mārcis Gasūns_
