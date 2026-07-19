# PWG German sense-gloss layer

_Created: 19-07-2026 · Last updated: 19-07-2026_

The German meaning spans of the großes Petersburger Wörterbuch, one per sense,
extracted per entry and **homonym-precise**.

## What it is

PWG marks every German meaning/translation with `{%…%}`
(`{#akarman#}¦ … <lex>n.</lex> {%das Nichthandeln%}`). [`pwg_german_glosses.tsv`](pwg_german_glosses.tsv)
pulls them out per entry:

| Column | |
|---|---|
| `L_id` · `k1` · `hom` | PWG entry id, headword (SLP1), homonym (`<h>`; '' for singletons) |
| `n_glosses` | number of German glosses in the entry |
| `glosses` | the glosses, `‖`-joined (U+2016; absent from the German prose) |

**192,763 glosses across 81,439 entries** (avg 2.37/entry). Because each row is a single
PWG entry, the layer is homonym-precise from the start — no L_id↔hom join needed (unlike
the headword-aggregated [Pāṇini crosswalk](../pwg_panini_crosswalk/README.md)).

Glosses mix headword meanings (`Theil`, `Antheil`) with example-sentence translations
(`den 6ten Theil gebe er vom väterlichen Vermögen`); PWG page-break markers (`[Page…]`) that
split a gloss are stripped.

## Regenerate

```sh
python scripts/pwg_german_glosses.py
```

Deterministic; reads only `../csl-orig/v02/pwg/pwg.txt`.

## Consumers

- **Bilingual gloss / translation-memory seed** for the pwg_ru RU translation — a compact
  DE-meaning inventory (complements, does not duplicate, the full-prose translation).
- **Per-sense German inventory** for a DE↔RU/EN compact dictionary export.

Sibling cheap PWG layers from the same source: derivation (`von {#base#}`), the Pāṇini sūtra
crosswalk, compound splits, and the L_id↔hom map.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1282 follow-up._

_Dr. Mārcis Gasūns_
