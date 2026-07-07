# `whitney_talmud.json` — schema & provenance

_Created: 07-07-2026 · Last updated: 07-07-2026_

The Phase-3 enrichment crosswalk for the *Talmud санскрита* interactive companion
(see [`IMPROVEMENT_PLAN.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/IMPROVEMENT_PLAN.md)).
It joins the canonical, **read-only** [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots)
data with the Talmud's analytical overlay (Ряд / Тип / seṭ), and is the single source
behind Приложение 1, the widget data (Phase 2), and the answer-key generator (Phase 4).

Regenerate with
[`tools/build_whitney_talmud.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/build_whitney_talmud.py)
(reads WhitneyRoots; writes only this file).

## Provenance — the honest boundary

| Marker | Meaning |
| :--- | :--- |
| `source=whitney` | Copied **verbatim** from WhitneyRoots (`crosswalk/roots.csv`). Trustworthy. |
| `ryad_source=derived` | Ряд **computed** from the root's nucleus vowel — a **proposal**, never asserted as Tolchelnikov's own. Every value is gated through `footnote-proposals/` for the author's approval. |
| `set_source=derived-ppp` | seṭ/aniṭ **inferred** from the p.p.p. connecting vowel. Advisory. |
| `tip=null` | Тип is a lexical property Whitney records but which is **absent** from the WhitneyRoots JSON — left null; unmarked default is `s` (Table 3, §II). Not invented. |
| `source=tolchelnikov` | The nominal roots the author himself tabulated in Приложение 2 — carried verbatim. |

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
| `ryad` | **derived** | Ablaut series (`A₁`…`N₂`) — see rules below. |
| `ryad_source` | — | `"derived"` or null. |
| `ryad_confidence` | — | `high` (i/ī/u/ū/ṛ/ṝ/ḷ roots) · `medium` (a/ā, incl. nasal M/N) · `low` (already-graded e/o/ai/au citation). |
| `ryad_note` | — | Caveat where the series is not phonologically forced (e.g. A vs M/N for nasal-final a-roots). |
| `tip` | — | Always null (see above). |
| `tip_default` | — | `"s"` — the unmarked behaviour. |
| `set` | **derived** | `seṭ` / `aniṭ` / null. |
| `set_source`, `set_confidence` | — | `"derived-ppp"`; `medium` where a p.p.p. was available. |
| `cohort` | derived | Teaching order from `dcs_rank`: `first` (≤50) · `second` (≤200) · `later` · `unranked`. |

## Ряд derivation (Table 2, §II)

The series letter is fixed by the root's **nucleus vowel** (last ablauting vowel of
the citation form); the subscript by its length:

```
a → A₁    ā → A₂        i → I₁    ī → I₂
u → U₁    ū → U₂        ṛ → R₁    ṝ → R₂       ḷ → L
```

- **Nasal-final a-roots** whose weak grade vocalises the sonant (`gam`→`gm̥`, `han`/`jan`→`n̥`)
  are placed in **M₁ / N₁** rather than A₁, with a `ryad_note` flag to verify against A₁.
- **Already-graded citation vowels** (`e`/`o`/`ai`/`au`) recover the underlying series
  but are marked `low` confidence.

Spot-checked against known roots: `kṛ`→R₁, `bhū`→U₂, `gam`→M₁, `han`/`jan`→N₁,
`dā`/`sthā`/`jñā`→A₂, `iṣ`→I₁, `nī`→I₂, `dṛś`/`hṛ`/`smṛ`→R₁ — all correct.

## seṭ derivation

`seṭ` if the p.p.p. inserts a connecting `i`/`ī` before `-ta` (`pat`→`patitá`,
`grah`→`gṛhītá`); `aniṭ` if it attaches directly (`kṛ`→`kṛtá`, `bhū`→`bhūtá`,
`gam`→`gatá`). A vowel-final root's own `-ī-`/`-ū-` before `-ta` (`nī`→`nītá`) is **not**
a connecting vowel, so the signal is read only on consonant-final roots. `veṭ`
(optional) and suppletive p.p.p.s are not distinguished — hence "advisory".

## Current counts

Regenerated 07-07-2026 (Opus 4.8 `claude-opus-4-8`): 930 verbal roots —
Ряд confidence `{high: 445, medium: 457, low: 28}`; seṭ `{seṭ: 172, aniṭ: 287, null: 471}`;
15 nominal roots (Приложение 2, verbatim).

_Dr. Mārcis Gasūns_
