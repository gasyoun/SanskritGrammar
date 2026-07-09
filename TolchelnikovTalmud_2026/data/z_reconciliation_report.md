# Reconciliation — samskrtam.ru/z/ (Tolchelnikov/Shirobokov DB) vs our derived Ряд/seṭ

_Created: 08-07-2026 · Last updated: 08-07-2026_

Handoff **H329**. Model: Opus 4.8 (`claude-opus-4-8`).

> **⚠ Author correction (08-07-2026, I. E. Tolchelnikov via [issue #50](https://github.com/gasyoun/SanskritGrammar/issues/50)).**
> `/z/` is **not** fully authoritative for Ряд — it has systematic bugs. Two classes of
> what this report first counted as "disagreements" are in fact **`/z/` errors, not ours**:
> (1) the **115 `0`-variant / `L` rows** (`I0/N0/R0/U0/M0`, `L`) — such rows **do not exist**;
> they are a Table-2 handling bug in `/z/`, to be **discarded** (NOT "`/z/` richer" as written
> below). (2) The **ṛ-nucleus cases** where our derivation gave `R₁` and `/z/` gave `A1` —
> the manual has `R₁`, which is correct; `/z/`'s `A1` is the error, so **our value stands**
> (NOT "our calculus wrong"). Ground truth for Ряд is the printed manual (руководство), not
> `/z/`. The 70.7 % Ряд figure below therefore **understates** our derivation's fidelity.
> seṭ coverage from `/z/` is still valuable (fills 246 nulls) but each adopted value needs
> author confirmation. Phase 3 applies the author's answers from issue #50.
>
> **Version drift (MG, 08-07-2026):** `/z/` was generated from an **earlier version of the
> Talmud** than the current v2.1.6. A further share of the Ряд/seṭ disagreements is therefore
> **neither side's error but authorial revision** between versions — expected, not a defect.
> The 70.7 % Ряд / 91.3 % seṭ agreement figures partly measure version difference; do not read
> the disagreement rate as an error rate. Phase 3 must weigh three causes per conflict —
> `/z/` bug · our-derivation error · authorial version drift — before changing anything.
>
> **AUTHOR RULING — supersedes the "adopt `/z/`" recommendation below (I. E. Tolchelnikov,
> [issue #50](https://github.com/gasyoun/SanskritGrammar/issues/50), 08-07-2026).**
> The single source of truth is the **latest version of the manual (руководство = `Talmud-2.1.6.mdx`,
> the current/authoritative edition)** — **not** `/z/` and **not** our algorithmic derivation:
> - **Ряд** and **seṭ** are taken **from the manual**. A row letter with **no digit stays
>   un-indexed** (do not force `1`/`2`); the `1`/`2` refinements are only where the manual gives
>   them. `0`-variants are not created.
> - **No methodology footnote** — the author declined it; FN-0001/0002 are marked `rejected`.
> - **Whitney references** come from the manual; roots absent from Whitney simply carry no ref.
> - `/z/` is retained **only as the paradigm deep-link** (Phase 4) — an older snapshot, outdated
>   in places but still useful for the generated paradigms.
> So Phase 3 is no longer "reconcile/adopt `/z/`" but **"transcribe the manual's own
> Ряд/seṭ/Whitney catalog (Приложение 1 of `Talmud-2.1.6.mdx`) as authoritative, replacing derived
> + `/z/` values."** This reconciliation stays as the audit trail of *why* the derived values were
> untrustworthy.

## What this is

[`samskrtam.ru/z/`](https://samskrtam.ru/z/) is Shirobokov A.P.'s interactive database of
Tolchelnikov's «Санскритская морфология» v1.1.0 — a verb-root DB carrying the author's
**authoritative Ряд** (series) and **seṭ/aniṭ** class per root. Our Phase-3
[`whitney_talmud.json`](https://github.com/gasyoun/SanskritGrammar/blob/chore/errata-kochergina-waiting/TolchelnikovTalmud_2026/data/whitney_talmud.json)
instead **derived** Ряд from the nucleus vowel (Table-2 calculus) and **inferred** seṭ from
the p.p.p. — all flagged advisory, pending the author (footnote-proposals FN-0001/0002).

This report joins the two and measures how far our derived values diverge from the
authoritative ones, to decide whether to adopt `/z/`'s values (H329 decision (a), locked
with MG 07-07-2026). Join map: [`data/z_root_map.json`](https://github.com/gasyoun/SanskritGrammar/blob/chore/errata-kochergina-waiting/TolchelnikovTalmud_2026/data/z_root_map.json).

## Method

- **Single polite fetch** of the `/z/` index (277 KB, one page, 905 rows) — cached locally,
  gitignored. **No detail-page scrape**: the index table alone carries per root the id
  (→ deep-link URL `verb.php?id=N`), Series (Ряд), «Verb by Whitney», seṭ-aniṭ code, present
  class, aorist type, and gloss. Detail pages add only computed paradigms, referenced by URL.
- **Join key** = the «Verb by Whitney» cell (`"<homonym> <rootform>"`, e.g. `1 as`) → matched
  against `whitney_talmud.json` on `(root_iast, homonym)`, with fallback to unique-root match.
- **seṭ code decode**: `s`=seṭ, `a`=aniṭ, `v`/`v1…v5`=veṭ (optional), `0`=unmarked, `s(ī?)`=seṭ (uncertain).
- **Ряд normalization**: our subscript form `A₁` ↔ `/z/`'s ASCII `A1`.
- Reproduce: `python tools/build_z_root_map.py` (needs the cached index in `data/raw_cache/`).

## Coverage

| `/z/` index rows | matched to `whitney_no` | ambiguous homonym | no Whitney row |
|---|---|---|---|
| 905 | **876** (96.8%) | 11 | 18 |

- **Ambiguous homonym** (11): `/z/` gives a homonym number, but the `(root, homonym)` pair does
  not resolve to a single Whitney row — `i, ran, rās, stu, tan, uṣ, śuṣ, ūh`. Resolve by hand in Phase 3.
- **No Whitney row** (18): variant spellings and later/non-Whitney roots (`chuḍ, hary, mikṣ,
  mlich, nū, riṅkh, yav, …`), plus **DB-noise rows** (`-`, `отсутствует` = "absent") — confirming
  MG's "`/z/` is not very clean" warning. These are logged, not force-matched.

## Ряд (series) reconciliation

Over the 876 matched roots (both sides present):

| | count | share |
|---|---|---|
| **agree** | 619 | **70.7%** |
| disagree | 257 | 29.3% |

The 257 disagreements split into two very different classes:

| disagreement class | count | meaning |
|---|---|---|
| **structural** (`/z/` `0`-variant `N0/I0/R0/U0/M0` or series `L`) | 115 | our Table-2 calculus **cannot express** these — `/z/` is richer, not "wrong vs right" |
| **genuine series conflict** | 142 | the two methods assign a different series letter/subscript |

Treating the structural cases as "`/z/`-richer" rather than errors, genuine agreement is
**619 / 761 = 81.3%**. Either way, adopting `/z/` strictly improves the data.

**Two findings inside the 142 genuine conflicts:**

1. **Systematic ṛ-nucleus divergence.** Our calculus routes ṛ-vowel roots to series R
   (`R₁`), but Tolchelnikov assigns many to `A1` — `ṛj, bhṛjj, mṛkṣ, mṛd, spṛś, …`. The
   dominant swap is **N→A (45)**, then R↔A/U. This is a methodology gap in FN-0001, not
   random noise.
2. **Over-confident derivation.** 57 of the 142 genuine conflicts are cases our derivation
   marked `ryad_confidence: high` yet `/z/` disagrees — our confidence flag was optimistic.
   (84 were `medium`, 1 `low`.)

## seṭ / aniṭ reconciliation

| | count |
|---|---|
| both assert seṭ/aniṭ — **agree** | 294 |
| both assert seṭ/aniṭ — disagree | 28 |
| **agreement** | **294 / 322 = 91.3%** |
| `/z/` **fills a value where we derived null** | **246** |
| `/z/` says `veṭ` where we derived seṭ/aniṭ | 203 |
| we assert, `/z/` unmarked | 11 |

- 27 of the 28 genuine conflicts are `/z/`=seṭ vs our=aniṭ (our p.p.p. inference missed a
  connecting vowel): `lag, sah, vyā, śī, hū, śri, śvit, kṣvid, ji, gṛ, vij, śak, dīv, …`;
  one is the reverse (`nind`). All were `medium` confidence on our side.
- The biggest win is coverage: `/z/` supplies a seṭ value for **246** roots our derivation
  left `null`, and flags **203** as `veṭ` (optional) — a distinction our binary derivation
  could not make at all.

## Recommendation (Phase 3)

Adopt `/z/`'s Ряд and seṭ as the authoritative source, replacing derived/advisory values,
with a `ryad_source` / `set_source` = `z` provenance field and `derived` kept only where
`/z/` is silent. **Author-gating still applies** (H329 guardrail): sourced values enter the
running text only as **Ivan-approved footnotes** via `/review-sheet` — but the proposal now
cites `/z/` (the author's own DB) instead of "derived from vowel", which is far stronger.
Rewrite FN-0001/0002's methodology notes to (a) cite `/z/`, (b) record the ṛ-nucleus series
divergence, and (c) drop the over-confident `high` flags shown false here.

## Deep-link coverage (Phase 4)

The widget feed ([`widget_roots.json`](https://github.com/gasyoun/SanskritGrammar/blob/chore/errata-kochergina-waiting/TolchelnikovTalmud_2026/data/widget_roots.json))
and the Appendix 1 catalog now carry a `z_url` deep-link to each root's full generated
paradigm on `/z/`. Coverage: **39/44** ablaut examples, **101/106** seṭ examples.

- **Collision rule.** ~107 Whitney roots have >1 `/z/` row (a primary alphabetical
  listing + a high-id `800–900s` s-mobile/variant cross-reference, e.g. `kṛ` id=594 vs
  `skṛ` id=895). The deep-link picks the **lowest `z_id`** = the primary listing.
- **Graceful gaps.** The 5 uncovered widget roots are present-stem-vs-lemma form
  differences (`gach`≈gam, `ich`≈iṣ, `har`≈hṛ), the ambiguous `i`, and `sṛj` — where
  `/z/` id=649's own row is internally inconsistent: root cell `sṛj` but «Verb by
  Whitney» cell `vṛṣ`. We join on the Whitney cross-ref column, so such rows degrade to
  **no link** rather than a wrong one. **col0 (root) ≠ col3 (Verb by Whitney)**
  disagreement is a `/z/` data-quality signal worth a Phase-3 pass.

## Provenance

- **Source data**: Толчельников И.Е., «Санскритская морфология: руководство» v1.1.0 (author);
  Широбоков А.П. (algorithmisation / DB) — [samskrtam.ru/z/](https://samskrtam.ru/z/), **ours** (MG).
- **Join target**: [`whitney_talmud.json`](https://github.com/gasyoun/SanskritGrammar/blob/chore/errata-kochergina-waiting/TolchelnikovTalmud_2026/data/whitney_talmud.json) (930 Whitney roots).
- **Generator**: [`tools/build_z_root_map.py`](https://github.com/gasyoun/SanskritGrammar/blob/chore/errata-kochergina-waiting/TolchelnikovTalmud_2026/tools/build_z_root_map.py) · Opus 4.8 (`claude-opus-4-8`), 08-07-2026.
- Raw `/z/` index cache is gitignored (`data/raw_cache/`); only the derived join map + this report are committed.

_Dr. Mārcis Gasūns_
