# PWG full derivation graph

_Created: 19-07-2026 · Last updated: 19-07-2026_

Every derivation note PWG states — `von {#base#}` / `Wurzel {#root#}` / `Stamm {#stem#}`
— classified and homonym-precise. Supersets the taddhita-only slice by adding the kṛt
(deverbal) half and the denominal residue.

## What it is

[`pwg_derivation_graph.tsv`](pwg_derivation_graph.tsv): one row per derivation note in an
entry — `L_id · k1 · hom · headword_iast · base_slp1 · base_iast · cue · base_type ·
deriv_kind · suffix · citation`.

**28,588 derivations**, by kind:

| deriv_kind | n | what |
|---|---:|---|
| denominal-other | 13,509 | nominal base, no recognised secondary suffix — denominative verbs (-ay/-ya), rarer suffixes (-la/-ana…), compound-final members |
| **kṛt** | 8,834 | verbal-root base (Whitney's 855) or `Wurzel`/`Stamm` cue — deverbal |
| **taddhita** | 5,720 | nominal base + a recognised secondary suffix (matches the [taddhita layer](../../sangram/articles/taddhita-overview/index.mdx)) |
| prefixed | 525 | upasarga base |

Base types: nominal 19,187 · root 8,834 · prefix 525.

## Why it is trustworthy

- Root inventory is **Whitney's clean 855 dhātus** (`WhitneyRoots/crosswalk/roots.csv`), NOT
  the contaminated `etymology_stats/dhatu_roots.txt` (which lists nouns as roots — FINDINGS
  §130).
- Classification uses the **immediate** base PWG names, fixing the ultimate-root contamination
  of the Cologne `pwg_etymology` extractor (which folded aṃśaka←aṃśa up to the root aṃś).
- **Homonym-precise:** each row carries the entry's homonym (`<h>`), so aṃśaka's derivation is
  recorded once per homonym rather than merged.

## Regenerate

```sh
python scripts/pwg_derivation_graph.py
```

Deterministic; reads only `../csl-orig/v02/pwg/pwg.txt` + `../WhitneyRoots/crosswalk/roots.csv`.

## Consumers

- The full derivation typology for pwg_ru / a derivation interface (kṛt vs taddhita vs
  denominative), homonym-precise.
- The taddhita subset feeds SG-WF-004; the kṛt subset is a corpus-independent deverbal census.

Sibling cheap PWG layers: the taddhita dataset, the Pāṇini crosswalk, compound splits, the
German glosses, and the L_id↔hom map.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1282 follow-up._

_Dr. Mārcis Gasūns_
