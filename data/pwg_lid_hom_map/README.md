# PWG L_id ↔ (headword, homonym) map

_Created: 19-07-2026 · Last updated: 19-07-2026_

The homonym-alignment key that lets the other PWG data layers target the **exact**
homonym instead of attaching to all homonyms of a headword.

## What it is

Every PWG entry header states its homonym number explicitly:

```
<L>2<pc>1-0001<k1>a<k2>a<h>2      → L_id 2 = headword `a`, homonym 2
<L>5<pc>1-0003<k1>a<k2>a<h>5      → L_id 5 = headword `a`, homonym 5
<L>1000<pc>1-0074<k1>ajIta<k2>a/jIta   → singleton (no <h>, homonym '')
```

[`pwg_lid_hom_map.tsv`](pwg_lid_hom_map.tsv) turns that into `L_id · k1 · hom · k2` for
all **123,366 entries** (6,494 carry an explicit `<h>`; 116,872 are singletons;
106,082 distinct headwords, of which **2,345 have >1 homonym**).

## Why it matters

The derivation / Pāṇini / compound layers are each keyed by PWG `L_id`. Before this map,
joining them onto the pwg_ru headword index (keyed by `k1` + `hom`) could only match on
`k1` and had to attach a value to *every* homonym of a headword, flagged
`homonym_ambiguous` (the guardrail in `enrich_portrait_grammar.py` /
`pwg_derivation_layer.py`). With `L_id → (k1, hom)` the value pins to the one homonym PWG
actually wrote it against — removing the ambiguity for the 2,345 multi-homonym headwords.

**Validated:** 100.00 % of the pwg_ru headword index's 96,166 distinct `(k1, hom)` pairs
resolve in this map.

## Regenerate

```sh
python scripts/pwg_lid_hom_map.py
```

Deterministic; reads only `../csl-orig/v02/pwg/pwg.txt`.

## Consumers

- **pwg_ru** `src/pwg_derivation_layer.py` — homonym-precise join of the derivation/Pāṇini/
  compound layers onto `headword_index`.
- Any layer keyed by PWG `L_id` that needs the pwg_ru homonym numbering.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1282 follow-up._

_Dr. Mārcis Gasūns_
