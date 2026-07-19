# PWG register / genre layer

_Created: 19-07-2026 · Last updated: 19-07-2026_

The diachronic profile of each PWG headword, derived from the texts that attest it
(its `<ls>` source citations), homonym-precise.

## What it is

PWG cites its attesting sources (`<ls>ṚV. 1,62,8</ls>`, `<ls>MBH. 12,10374</ls>`).
[`pwg_register_genre.tsv`](pwg_register_genre.tsv) reads every `<ls>` per entry, maps the
source to a `(period, genre)`, and records per headword:

| Column | |
|---|---|
| `L_id` · `k1` · `hom` | PWG entry, headword, homonym |
| `n_citations` | number of `<ls>` citations |
| `periods` | attesting periods (`vedic` < `brahmana` < `sutra` < `epic` < `classical`) |
| `earliest_period` | the diachronic anchor (first attestation) |
| `register` | `earliest_period`, or `lexical` (only lexica), or `uncategorised` |
| `lexicon_only` | `1` if attested **only** in lexica/commentary — no dated-text citation |
| `genres` | saṃhitā / brāhmaṇa-upaniṣad / sūtra / grammar / dharmaśāstra / epic / kāvya / purāṇa / śāstra / lexicon / commentary / modern-ref / other |
| `sources` | the curated source tokens matched |

**116,033 entries with citations**; **90.6 %** of citation tokens map to a curated source.
Register spread: classical 21,511 · sūtra 19,221 · vedic 17,636 · epic 14,500 · brāhmaṇa
5,144 · **lexical 32,690** · uncategorised 5,331.

**Notable: 32,690 lexicon-only headwords** — words PWG attests *only* from Sanskrit koṣas
(Amara, Hemacandra, Medinī…), never from a dated text. A ready census of the lexicographers'
vocabulary (potential ghost-words), which is hard to isolate any other way.

## Honest scope

The `(period, genre)` map is a **curated table of the top ~90 source tokens** (≈89 % of the
566,678 citations); rarer sources count as genre `other` and set no period. `register`/
`earliest_period` therefore read the mapped 90.6 % — a high-coverage estimate, not every
citation. Periods are the standard coarse strata, not fine dates.

## Regenerate

```sh
python scripts/pwg_register_genre.py
```

Deterministic; reads only `../csl-orig/v02/pwg/pwg.txt`.

## Consumers

- A **diachronic/register field** for pwg_ru portraits (Vedic vs Epic vs Classical vs
  lexicon-only), homonym-precise; complements the DCS-genre `renou_register.py`.
- The **lexicon-only census** as a research surface (which words live only in the koṣas).

Sibling cheap PWG layers: the derivation graph, the Pāṇini crosswalk, compound splits, the
German glosses, and the L_id↔hom map.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1282 follow-up._

_Dr. Mārcis Gasūns_
