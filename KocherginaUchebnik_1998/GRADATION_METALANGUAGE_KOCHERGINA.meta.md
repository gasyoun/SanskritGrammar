# Metadoc — GRADATION_METALANGUAGE_KOCHERGINA.md

_Created: 13-07-2026 · Last updated: 13-07-2026_

Companion record for
[`GRADATION_METALANGUAGE_KOCHERGINA.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/GRADATION_METALANGUAGE_KOCHERGINA.md).

## Purpose & audience

The metalanguage companion to the H768 claim register: it documents *how* Kochergina scopes
her rules (the quantifier metalanguage — редко / обычно / только / некоторые / могут / всегда)
and measures the same across Zalizniak's three Sanskrit works, asking of each quantifier
whether it is **anchored** to a decidable target. Audience: the reading-site / methodichka
authors and anyone weighing "Kochergina vs Zalizniak rigour". Russian, scholarly register.

## Provenance

- **§1–3** created 12-07-2026 by a concurrent session under **H768** (PR #136) — the
  «реже»≠«редко» logical-type analysis, the rarity/frequency/productivity gradation scales
  with DCS-2021 numbers, and the Zalizniak-rigour "5 operations / 3 defects" remediation.
- **§2а + §4** added 13-07-2026 under **H800** (Opus 4.8, `claude-opus-4-8`) — the three
  quantifier classes §1–3 missed (modality/optionality, indefinite subset, hedged universals)
  and the *measured* four-way comparison: the machine register
  ([`quantifiers.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/quantifiers.yml)
  × 4 sources), density, anchor-share + sensitivity, anchor-type mix, and a hand-verified
  precision/recall pass.

## Data & tooling backing the claims

- Harvest + auto-proxy:
  [`scripts/harvest_quantifiers.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/harvest_quantifiers.py);
  render:
  [`scripts/build_quantifiers.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_quantifiers.py)
  (`npm run quantifiers`). Generated:
  per-source `QUANTIFIER_PROFILE.md` + `quantifiers.json` + root
  [index](https://github.com/gasyoun/SanskritGrammar/blob/main/QUANTIFIER_PROFILE.md).
- Hand-verified samples: `<Book>/quantifiers.sample.yml` (133 rows total, adjudicated Opus 4.8).

## Limitations

- The anchor auto-proxy is **high-precision (~90 %), low-recall (~45 %)** at N=8 — the N=8
  anchored-share UNDER-reads true anchoredness; use the hand-verified figure. Axis assignment
  is lexicon-driven and not itself hand-verified.
- DCS numbers in §1–2 are from the H768 register (DCS-2021); not re-verified here.
- The §1–2 gradation *scales* (реже < редко < очень редко …) are curated illustrations, not an
  exhaustive census; the exhaustive census is `quantifiers.yml`.

## Improvement backlog (ranked)

1. **@DECIDE the anchor window N** (fixed at 8; sensitivity table provided). Confirm or set.
2. Hand-verify the **axis assignment** on a sample (currently only anchoredness is verified).
3. Reconcile the §1–2 curated gradation scales with the `quantifiers.yml` census counts (the
   scales predate the machine register; some example line-numbers are hand-picked).
4. If MG upgrades D1 → a methods paper, lift §4 + the anchor-type finding into an Axx draft
   (currently apparatus only; no Axx minted).
5. Optional: an anchoredness overlay on the reading site (mirror `KocherginaClaims.jsx`).

## Revision history

| Date | Who | Change |
|---|---|---|
| 12-07-2026 | H768 (concurrent session) | §1–3 created (реже/редко, gradation scales, Zalizniak-rigour remediation) |
| 13-07-2026 | H800 (Opus 4.8) | +§2а (3 missing classes) +§4 (machine register + measured 4-way comparison + D3 verification); Last-updated bumped |

_Auto-generated companion; maintained by hand._
