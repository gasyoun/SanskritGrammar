# PWG gaṇa-membership layer

_Created: 19-07-2026 · Last updated: 19-07-2026_

The Pāṇinian word-class (gaṇa) of each PWG headword — sourced from the external
nominal Gaṇapāṭha and cross-validated against PWG's own Pāṇini citations.

## Why external

PWG itself carries almost no gaṇapāṭha markup (only ~5 explicit `gaṇa {#Xādi#}` references),
so gaṇa membership cannot be extracted from PWG. It is instead **joined in** from the
digitised Gaṇapāṭha and confirmed against the [Pāṇini crosswalk](../pwg_panini_crosswalk/README.md).

## Files

| File | |
|---|---|
| [`vidyut_ganapatha.rs`](vidyut_ganapatha.rs) | vendored source (see licence below) |
| [`vidyut_ganapatha.tsv`](vidyut_ganapatha.tsv) | the parsed Gaṇapāṭha: `const · name · number · sutra · kind · n_members · members_slp1` — **227 gaṇas** (193 basic · 34 ākṛti) |
| [`pwg_gana_membership.tsv`](pwg_gana_membership.tsv) | `member_slp1 · ganas · gana_sutras · crosswalk_sutra_match · corroborated · attested_in_pwg` |

## How it's built

1. Parse the Gaṇapāṭha (`vidyut_ganapatha.rs`) → `gaṇa → [members]` (SLP1).
2. Invert → `member → gaṇa(s)`.
3. Join members onto PWG headwords (the `pwg_lid_hom_map` `k1` set) — homonym-agnostic, since
   gaṇa membership is lexical, not per-sense.
4. Cross-validate with the Pāṇini crosswalk: mark `corroborated` when PWG independently cites the
   gaṇa's governing sūtra for that word.

**Result: 4,514 distinct Gaṇapāṭha member words; 3,035 attested as PWG headwords; 1,666 of those
independently corroborated** by PWG's own Pāṇini citation of the governing sūtra (e.g. ādyaśvi ∈
gahādiḥ / P.4.2.138, and PWG cites P.4.2.138 for it). A small but high-precision, genuinely
Pāṇinian layer — versus PWG's own 5 gaṇa references.

## Regenerate

```sh
python scripts/pwg_gana_membership.py
```

Deterministic; reads the vendored `.rs` + the sibling `pwg_lid_hom_map` and
`pwg_panini_crosswalk` datasets.

## Licence / provenance

`vidyut_ganapatha.rs` is vendored from
[ambuda-org/vidyut `vidyut-prakriya/src/ganapatha.rs`](https://github.com/ambuda-org/vidyut/blob/main/vidyut-prakriya/src/ganapatha.rs),
**MIT-licensed**, itself auto-generated from the Gaṇapāṭha on
[ashtadhyayi.com/ganapath](https://ashtadhyayi.com/ganapath). Members are in SLP1 — the same
convention as PWG, so no transliteration bridge is needed.

## Consumers

- A gaṇa field for pwg_ru portraits (which Pāṇinian class a word belongs to), with the governing
  sūtra and a corroboration flag.
- The parsed `vidyut_ganapatha.tsv` is a reusable Gaṇapāṭha asset for any consumer.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1282 follow-up._

_Dr. Mārcis Gasūns_
