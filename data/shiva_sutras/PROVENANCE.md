# data/shiva_sutras/ — vendored pratyāhāra reference table

_Vendored: 15-09-2026 (H4716) · Source: [kosha `shiva-sutras-machine`](https://github.com/gasyoun/kosha/tree/main/data/shiva_sutras)_

## What this is

Machine-readable Māheśvara (Śiva) Sūtras + the pratyāhāra span table, consumed as the
pratyāhāra reference table for the sangram morphology programme and VisualDCS-style
sandhi/derivation lookup notes (kosha registry `consumer_candidates`, H4471).

## Files (byte-identical vendor snapshot, `cmp`-verified)

| File | Rows | Content |
|---|---|---|
| `sutras.tsv` | 14 | one row per sūtra: `sutra_number`, `devanagari` (incl. anubandha/IT marker), `letters_only`, `it_marker` |
| `pratyaharas.tsv` | 42 | one row per named pratyāhāra (aK, aC, yaṆ, haL, …): `name`, `devanagari_span`, `letters_only` (markers stripped), `it_marker`, `length` |
| `shiva_sutras.json` | — | bundles both plus the 57-token master sequence |

## Provenance

- **Upstream of truth:** kosha `data/shiva_sutras/` (built by `kosha/scripts/build_shiva_sutras.py`,
  H4471, 09-09-2026) from `Panini/ShivaSutras.xlsx` (yadisk, gitignored local-only).
  Pinned source state: kosha commit `11a243eb` (data last touched 2026-09-10).
- **License:** MIT (Pāṇini's grammar itself is public domain).
- **This copy is a consumer snapshot, NOT canonical.** If kosha's table changes, re-vendor and
  re-run `python scripts/verify_shiva_pratyahara.py`.

## Verification

`python scripts/verify_shiva_pratyahara.py` — deterministic offline checker:
all 14 sūtras rebuild the 57-token master sequence; all 42 named pratyāhāra spans round-trip
(expansion-from-table == recomputation-from-sūtra-sequence == marker-stripped raw span);
classic semantics canaries (aC = vowels only, haL = consonants, aC ⊎ haL = master sequence).

_Гасунс_
