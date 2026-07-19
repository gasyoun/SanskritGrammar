# PWG lexicon-only audit (H1310)

_Created: 19-07-2026 · Last updated: 19-07-2026_

Do PWG's **lexicon-only** headwords — the 32,690 words PWG attests *only* from koṣas, never
a dated text (`lexicon_only=1` in the [register/genre layer](../pwg_register_genre/README.md)) —
appear in any *other* digitised dictionary? A word "lexical" in PWG may still be attested via
another dictionary that cites a text, or corroborated by another koṣa. This resolves each one
by a deterministic set-membership join against the Cologne digitisations (`csl-orig`, read-only).

## What it is

[`pwg_lexicon_only_audit.tsv`](pwg_lexicon_only_audit.tsv) — one row per lexicon-only headword
(deduped to **31,925 distinct `<k1>`**), with a verdict and per-tier hits:

| Column | |
|---|---|
| `k1` | the headword (SLP1) |
| `verdict` | `text-independent` · `mw-only` · `kosa-only` · `pwg-unique` |
| `independent_hits` | which independent text dicts have it (`ap90`/`ap`/`bhs`/`gra`) |
| `in_mw` | `1` if in Monier-Williams |
| `kosa_hits` | which koṣas have it (`skd`) |
| `in_pw_same_source` | `1` if in Böhtlingk's own PWK (same source — not independent) |

[`pwg_unique_shortlist.tsv`](pwg_unique_shortlist.tsv) — the ghost-word shortlist (verdict
`pwg-unique`). [`pwg_lexicon_only_audit_summary.json`](pwg_lexicon_only_audit_summary.json) —
the counts.

## The verdict tiers — and why MW is separated

The naïve join says **91.5 %** of lexicon-only words appear in some text-based dictionary. That
is misleading: **28,935 of those hits are Monier-Williams, and MW was compiled substantially
*from* Böhtlingk-Roth (PW/PWG)** — a word in both PWG and MW may be MW copying PW, not
independent text-attestation. So MW gets its own tier, and the independent evidence is
Apte (`ap`, `ap90`), Grassmann (`gra`, RV corpus) and Edgerton (`bhs`, Buddhist Hybrid corpus):

| Verdict | Count | % | Reading |
|---|---:|---:|---|
| **text-independent** | 7,331 | 23.0 % | in Apte/BHS/Grassmann → genuinely text-attested elsewhere |
| **mw-only** | 21,874 | 68.5 % | in MW but no independent text dict → *weak* (MW ⊃ PW overlap) |
| **kosa-only** | 101 | 0.3 % | only in Śabdakalpadruma → same lexical tradition |
| **pwg-unique** | 2,619 | 8.2 % | in **no** other digitised dictionary → the ghost-word shortlist |

Of the 2,619 pwg-unique, **1,645 also appear in `pw`** (Böhtlingk's own kürzere Fassung — the
same source, so not independent corroboration); only **974 are truly absent from every other
dictionary in Cologne**, the hardest core of PWG-only vocabulary.

Per-dict raw hits among the 31,925: mw 28,935 · pw 29,550 · ap 5,969 · skd 3,359 · ap90 2,268 ·
bhs 1,537 · gra 502.

## Spot-check

The pwg-unique shortlist is clean (no digits, no spaces, no length outliers that flag OCR junk).
Manual inspection shows the expected make-up of a lexicon's residue: **text/work titles**
(`AcAracintAmaRi`, `AgamasAra`, `AdivAtulatantra` = *Ācāracintāmaṇi*, *Āgamasāra*,
*Ādivātulatantra*), **agent nouns in -tar** (`ADAtar`, `ASitar`, `Adezwar`), and **rare
compounds** — not corrupt entries. These are legitimate PWG headwords that no other digitised
dictionary carries, which is exactly what "ghost-word" should mean here.

## Honest scope

- The join is **exact SLP1 `<k1>` set membership**; a genuine word present under a variant
  spelling or with different accent marking in another dictionary would be missed and counted
  as more-unique than it is. The verdicts are therefore a **lower bound on attestation** (upper
  bound on uniqueness) — treat pwg-unique as "candidates", to be confirmed by hand.
- `mw-only` is the honest caveat, not a defect: it isolates the large slice whose only
  corroboration is a dictionary known to derive from PW, so it is neither confirmed
  independent-attestation nor confirmed ghost-word.
- Comparison is limited to the dictionaries digitised in `csl-orig`. Amba Kulkarni's
  digitisations (Vācaspatyam, Śabdārthakaustubha, others) are a natural next widening of the
  koṣa comparison set; not yet joined.

## Regenerate

```sh
python scripts/pwg_lexicon_only_audit.py
```

Deterministic; reads only `data/pwg_register_genre/pwg_register_genre.tsv` and the
`../csl-orig/v02/<dict>/<dict>.txt` headword lists (read-only). No network.

## Consumers

- A **research surface**: the 974 truly-unique + 2,619 pwg-unique candidates are the shortlist
  for "words that exist only in the Great Petersburg Dictionary".
- A **provenance qualifier** for pwg_ru portraits: a lexicon-only word can be annotated
  *also attested in Apte/BHS* vs *PWG-unique*.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1310._

_Dr. Mārcis Gasūns_
