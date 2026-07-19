# PWG compound (samāsa) segmentation layer

_Created: 19-07-2026 · Last updated: 19-07-2026_

Surface compound → its ordered underlying members, mined from the großes
Petersburger Wörterbuch (PWG). PWG analyses a compound headword in its etymology
parenthesis as a `+`-joined chain of SLP1 members —
`{#aMSakaraRa#}¦ ({#aMSa#} + {#karaRa#})`. This is exactly the surface↔underlying
pairing a sandhi/segmentation splitter is trained and evaluated on, and it falls out
of one regex pass over the committed `pwg.txt` (read-only).

## What it is

| File | Rows | Content |
|---|---|---|
| [`pwg_compound_splits.tsv`](pwg_compound_splits.tsv) | 16,745 | `headword_slp1 · headword_iast · L_id · arity · members_slp1 · members_iast` |
| [`pwg_compound_summary.json`](pwg_compound_summary.json) | — | counts + arity distribution |

Arity: 16,729 binary · 15 ternary · 1 quaternary. The splits carry **real sandhi at
the seam** — e.g. `āśīrvāda = āśis + vāda` (visarga → r), `ādhārādheyabhāva = ādhāra +
ādheya + bhāva`, `aṃśāvataraṇa = aṃśa + avataraṇa` (a + a → ā) — which is what makes
them useful gold for a splitter, not just a dictionary of parts.

## Honest scope

Only **fully-spelled** member analyses are kept. PWG abbreviates a repeated stem with
`˚` (e.g. `A˚` = "the headword's ā-stem"), and **18,852** such analyses are **excluded**
because the member is truncated and not reconstructable without resolving the
abbreviation. Only the first `+`-chain in the entry head is taken, and only when its
first member is a lead-compatible prefix of the headword — this keeps citation-run
`{#..#}` noise out. So this is a high-precision **subset** of PWG's compound analyses,
not all of them.

## Regenerate

```sh
python scripts/pwg_compound_split.py
```

Deterministic; reads only `../csl-orig/v02/pwg/pwg.txt`.

## Consumers (cheap reuse)

- **kosha DCS-sandhi programme** / **SanskritSpellCheck** splitters — an independent,
  dictionary-sourced gold reference for surface↔member segmentation.
- **Compound-formation pedagogy** — worked samāsa resolutions.
- **pwg_ru translation** — attach the member analysis as a structured field.

Sibling cheap PWG layers from the same source: derivation (`von {#base#}`, the taddhita
dataset), the [Pāṇini sūtra crosswalk](../pwg_panini_crosswalk/README.md), and German
sense glosses.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1254 follow-up._

_Dr. Mārcis Gasūns_
