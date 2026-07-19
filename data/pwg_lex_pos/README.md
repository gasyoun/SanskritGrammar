# PWG `<lex>` POS/gender layer

_Created: 19-07-2026 · Last updated: 19-07-2026_

The grammatical category (part of speech / gender) PWG assigns each entry, homonym-precise.

## What it is

PWG tags each entry's category with `<lex>m.</lex>` / `<lex>adj.</lex>` etc. — only **17
distinct raw values** across 130,864 tags. [`pwg_lex_pos.tsv`](pwg_lex_pos.tsv) records per
entry: `L_id · k1 · hom · primary_pos · lex_raw`.

**98,639 entries** carry a `<lex>` — one per headword, i.e. essentially complete. Primary POS
(first tag, normalised): m 35,184 · adj 31,666 · n 15,112 · f 14,192 · adv 1,808 · m.n 459 ·
indecl 110 · interj 85 · m.f.n 12 · m.f 7 · f.n 4.

Normalisation folds the raw variants: `m.`/`mm.`→`m`, `f.`/`ff.`/`fem.`/`femin.`→`f`,
`n.`/`neutr.`→`n`, `ind.`/`indecl.`→`indecl`. `lex_raw` keeps every tag in the entry (a headword
can carry more than one, e.g. `f.|m.n.|f.`).

## Cross-check use

The pwg_ru [`headword_index.tsv`](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/src/headword_index.tsv)
carries its own `lex` column (98,639 rows). This layer is the **same count**, keyed by the same
`k1`+`hom`, so it is a direct cross-check on that column — divergences flag either an index
build bug or a PWG multi-`<lex>` entry.

## Regenerate

```sh
python scripts/pwg_lex_pos.py
```

Deterministic; reads only `../csl-orig/v02/pwg/pwg.txt`.

## Consumers

- A homonym-precise POS/gender field for pwg_ru; a cross-check on the headword index's `lex`.

Sibling cheap PWG layers: the derivation graph, the Pāṇini crosswalk, compound splits, the
German glosses, the register/genre layer, and the L_id↔hom map.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1282 follow-up._

_Dr. Mārcis Gasūns_
