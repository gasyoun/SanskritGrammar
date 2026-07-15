# `whitney_talmud.json` — schema & provenance

_Created: 07-07-2026 · Last updated: 08-07-2026_

The Phase-3 enrichment crosswalk for the *Talmud санскрита* interactive companion
(see [`IMPROVEMENT_PLAN.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/IMPROVEMENT_PLAN.md)).
It joins the canonical, **read-only** [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots)
inventory with the Talmud's analytical overlay (Ряд / Тип / seṭ), and is the single
source behind Приложение 1, the widget data (Phase 2), and the answer-key generator (Phase 4).

Regenerate (manual catalog first, then the join):

```sh
python tools/parse_appendix1.py       # -> data/talmud_appendix1.json (author's catalog)
python tools/build_whitney_talmud.py  # -> data/whitney_talmud.json  (this file)
```

## Provenance — the author's ruling (issue #50)

The overlay (Ряд/Тип/seṭ) was **reframed** by the author's ruling on
[issue #50](https://github.com/gasyoun/SanskritGrammar/issues/50) (I.E. Tolchelnikov,
08-07-2026): the **latest manual is the sole authority** for these values. The earlier
vowel-derived Ряд and p.p.p.-inferred seṭ were untrustworthy proposals and are **no
longer emitted**; the older [samskrtam.ru/z/](https://samskrtam.ru/z/) snapshot is kept
only as the Phase-4 paradigm deep-link, not as a data source.

| Marker | Meaning |
| :--- | :--- |
| `source=whitney` | Copied **verbatim** from WhitneyRoots (`crosswalk/roots.csv`). |
| `ryad_source=manual` | Ряд taken **verbatim** from the author's Приложение 1 catalog ([`talmud_appendix1.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/talmud_appendix1.json)). Un-indexed stays un-indexed (ruling #3). |
| `ryad=null`, `ryad_source=null` | The root is **not in the author's catalog** — no series is asserted. |
| `tip_source=manual` | Тип (`I`/`II`/`III`/`IV`, Table 5) taken verbatim from Приложение 1 where the author gives it. |
| `set_source=manual` | seṭ/aniṭ/veṭ taken verbatim from Приложение 1 (Table 8). `set_code` keeps the finer `s`/`a`/`v1`…`v4`. |
| `source=tolchelnikov` | The nominal roots the author tabulated in Приложение 2 — carried verbatim. |

## Top-level shape

```jsonc
{
  "_meta": { "what": "...", "source_data": {...}, "provenance": {...}, "counts": {...} },
  "verbal_roots":      [ { …one per Whitney root, 930 total… } ],
  "nominal_appendix2": [ { …the author's 15 nominal roots, verbatim… } ]
}
```

## `verbal_roots[]` fields

| Field | Source | Notes |
| :--- | :--- | :--- |
| `whitney_no` | whitney | Whitney's root number (int). |
| `root_iast`, `root_slp1` | whitney | Citation form (IAST / SLP1). |
| `homonym` | whitney | Homonym index, or null. |
| `gloss` | whitney | Short English gloss. |
| `class` | whitney | Present-class list, e.g. `["I","VI"]`. |
| `ppp` | whitney | Past passive participle (kta), or null. |
| `dcs_freq`, `dcs_rank` | whitney | Digital Corpus of Sanskrit frequency / rank (null if unattested). |
| `period_tags` | whitney | Attestation strata (RV/AV/B/S/E…). |
| `mw_id`, `apte_id` | whitney | Monier-Williams / Apte cross-ids. |
| `warnemyr_url`, `section_refs` | whitney | Warnemyr page; Whitney §-refs for form-sections. |
| `ryad` | **manual** | Ablaut series (`A₁`…`N₂`, or bare `A`/`I`/`U`/`R`/`L`/`M`/`N` un-indexed), or null. |
| `ryad_source` | — | `"manual"` or null. |
| `tip` | **manual** | Тип чередования `I`/`II`/`III`/`IV` (Table 5), or null. |
| `tip_source` | — | `"manual"` or null. |
| `tip_default` | — | `"I"` — the unmarked runtime behaviour (Table 5, полноизменяемый/full-range type), kept as a fallback for the form generator. |
| `set` | **manual** | `seṭ` / `aniṭ` / `veṭ` / null. |
| `set_code` | manual | Raw Table-8 code: `s` / `a` / `v` / `v1`…`v4` (veṭ sub-class), or null. |
| `set_source` | — | `"manual"` or null. |
| `pada` | manual | `P` / `U` / `Ā` where the author gives it, or null. |
| `cohort` | derived | Teaching order from `dcs_rank`: `first` (≤50) · `second` (≤200) · `later` · `unranked`. |

## Ряд / Тип / seṭ — read verbatim from the manual

`tools/parse_appendix1.py` extracts the Pandoc grid table of Приложение 1 from
`Talmud-2.1.6.mdx`. Column semantics come from the manual's own tables:

- **Тип** — Table 5 (Типы чередований): `I` полноизменяемые · `II`/`III` неполноизменяемые · `IV` неизменяемые.
- **Ряд** — Table 4: the series letter (`A`/`I`/`U`/`R`/`L`/`M`/`N`) with a length subscript ₁/₂; **bare where the author prints it bare** (ruling #3).
- **seṭ** — Table 8: `s`=seṭ · `a`=aniṭ · `v`/`v1`…`v4`=veṭ (the numbered sub-classes differ in which forms take the connecting `i/ī`).

The join key from the catalog into the Whitney spine is col 4 «Список Уитни» (the
author's own Whitney-nomenclature reference). A root marked `NA` there — or one whose
citation form is not in WhitneyRoots — carries no overlay.

## Current counts

Regenerated 08-07-2026 (Opus 4.8 `claude-opus-4-8`): 930 verbal roots —
**730 carry the author's Ряд** (200 null, i.e. not in the catalog), **721 carry a manual seṭ**;
catalog match 730/745 rows (6 unmatched non-NA spellings). Manual vs the retired derived
values: Ряд agreement **75.6 %** (552/730), seṭ **59.4 %** — see
[`manual_reconciliation_report.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/manual_reconciliation_report.md).
15 nominal roots (Приложение 2, verbatim).

_Dr. Mārcis Gasūns_
