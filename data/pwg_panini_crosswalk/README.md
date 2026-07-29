# PWG → Aṣṭādhyāyī (Pāṇini sūtra) crosswalk

_Created: 18-07-2026 · Last updated: 30-07-2026_

A corpus↔grammar index mined from the großes Petersburger Wörterbuch (PWG): the
Pāṇinian sūtra that PWG cites as the authority for each headword. Normally an
expensive dataset to assemble; here it falls out of one pass over the committed
`pwg.txt` (read-only), so it is cheap to regenerate and to keep fresh.

## What it is

PWG cites the grammar as `P. a,b` (adhyāya, pāda) or `P. a,b,c` (adhyāya, pāda,
sūtra). Extraction is anchored on the `<ls>`-resolved citation abbreviation (not a
bare `a,b,c`-shaped number run in the prose), so a Vedic/epic citation that merely
*contains* "P." after another abbreviation (`BHĀG. P.` = Bhāgavata Purāṇa) is never
mistaken for Pāṇini — see [H1888](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1888-Sonnet_SanskritGrammar_panini-crosswalk-nonpanini-citation-purge_29.07.26.md),
which found 74.5% of the previous 14,417 "sūtra" keys were impossible (adhyāya > 8
or pāda > 4). A structural assertion (adhyāya ∈ 1–8, pāda ∈ 1–4) now guards the
builder itself. This extraction reads every reference and builds **both directions**:

| File | Rows | Direction |
|---|---|---|
| [`pwg_panini_word2sutra.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/pwg_panini_crosswalk/pwg_panini_word2sutra.tsv) | 12,974 words | headword → the sūtra(s) that license it |
| [`pwg_panini_sutra2word.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/pwg_panini_crosswalk/pwg_panini_sutra2word.tsv) | 3,792 sūtras | sūtra → the words attested under it (capped at 50/row) |
| [`pwg_panini_summary.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/pwg_panini_crosswalk/pwg_panini_summary.json) | — | counts + the 25 most-cited sūtras |

Totals: **22,825 references** (22,821 full `a.b.c` · 4 pāda-only; 102 candidate
`P.`-prefixed citations rejected by the structural assertion). The most-cited
sūtras are the Adhyāya-4 taddhita rules (`P.4.2.80`, `P.4.1.105`, `P.2.4.31`…) —
PWG cites Pāṇini densest for secondary derivation, which is what makes this a good
companion to the taddhita derivation layer
([`sangram/articles/taddhita-overview/`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/taddhita-overview/index.mdx)).

## Regenerate

```sh
python scripts/pwg_panini_crosswalk.py
```

Deterministic; reads only `../csl-orig/v02/pwg/pwg.txt`. Columns are SLP1 headword +
IAST + `L_id` (PWG entry id) + the pipe-separated sūtra list.

## Consumers (cheap reuse)

- **pwg_ru translation** — attach the licensing sūtra to each Russian entry as a
  structured field (language-independent, no extra annotation).
- **An Aṣṭādhyāyī interface** — `sutra2word` gives the attested word-set per rule.
- **Derivation pedagogy** — link a taddhita form to the rule that forms it.

Sibling cheap PWG layers from the same source: derivation (`von {#base#}`, the
taddhita dataset), compound splits (`({#X#}+{#Y#})`), and German sense glosses.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1254 follow-up._

_Dr. Mārcis Gasūns_
