# PWG compound (samāsa) segmentation layer

_Created: 19-07-2026 · Last updated: 26-07-2026_

Surface compound → its ordered underlying members, mined from the großes
Petersburger Wörterbuch (PWG). PWG analyses a compound headword in its etymology
parenthesis as a `+`-joined chain of SLP1 members —
`{#aMSakaraRa#}¦ ({#aMSa#} + {#karaRa#})`. This is exactly the surface↔underlying
pairing a sandhi/segmentation splitter is trained and evaluated on, and it falls out
of one regex pass over the committed `pwg.txt` (read-only).

## What it is

| File | Rows | Content |
|---|---|---|
| [`pwg_compound_splits.tsv`](pwg_compound_splits.tsv) | 17,112 | `headword_slp1 · headword_iast · L_id · arity · members_slp1 · members_iast` |
| [`pwg_compound_summary.json`](pwg_compound_summary.json) | — | counts + arity distribution + drop reasons |

Arity: 17,095 binary · 17 ternary. The splits carry **real sandhi at
the seam** — e.g. `āśīrvāda = āśis + vāda` (visarga → r), `ādhārādheyabhāva = ādhāra +
ādheya + bhāva`, `aṃśāvataraṇa = aṃśa + avataraṇa` (a + a → ā) — which is what makes
them useful gold for a splitter, not just a dictionary of parts.

## Honest scope

Only **fully-spelled** member analyses are kept. PWG abbreviates a repeated stem with
`˚` (e.g. `A˚` = "the headword's ā-stem"), and **18,852** such analyses are **excluded**
because the member is truncated and not reconstructable without resolving the
abbreviation. The chain is taken only from the balanced paren that belongs to the
entry's **own** headword, and only when its first member is a lead-compatible prefix of
the headword. Where PWG's paren is genuinely ambiguous — a disjunction or ladder of
derivation bases (`von {#BAnumant#} oder von {#BAnu#} + {#mati#}`), a sense divider run
into the paren — the entry is **dropped, never guessed at**, and the drop is counted by
reason in `pwg_compound_summary.json`. So this is a high-precision **subset** of PWG's
compound analyses, not all of them.

## Revision 26-07-2026 — the layer was 2 % wrong before this

The pre-26-07-2026 extractor took the first `+`-chain anywhere in the first 400 chars
of the entry, which is often **not** the headword's own analysis:
[SanskritGrammar#527](https://github.com/gasyoun/SanskritGrammar/issues/527) measured
344/16,738 rows carrying a bracketed *inner* sub-analysis (`akṛttaruc` shipped as
`a + kṛtta`, true `akṛtta + ruc`) or a *neighbouring* word's parenthesis (`adhikaṣāṣṭika`
shipped as `adhika + ṣaṣṭi`, which composes a different headword). It is now anchored on
the entry's `{#headword#}¦`, bracket-aware, and settles multi-candidate parts against the
headword's surface. Against the 19-07-2026 cut: **16,094 rows unchanged · 139 members
corrected · 512 dropped as unresolvable · 879 added** that the old head-scan had missed.
Consumers who pinned the 19-07-2026 file should re-pull.

## Regenerate

```sh
python scripts/pwg_compound_split.py
python scripts/pwg_compound_split.py --selftest   # 17 bracket/ambiguity fixtures
```

Deterministic; reads only `../csl-orig/v02/pwg/pwg.txt`.

The extractor's `pwg_toplevel()` is kept in sync with the same-named function in
SanskritLexicography's
[`adjudicate_compound_differs.py`](https://github.com/gasyoun/SanskritLexicography/blob/master/RussianTranslation/src/pilot/adjudicate_compound_differs.py),
which adjudicates this layer against Monier-Williams. If the two disagree about what
PWG says, that queue measures the extractors instead of the dictionaries — change both
or neither.

## Consumers (cheap reuse)

- **kosha DCS-sandhi programme** / **SanskritSpellCheck** splitters — an independent,
  dictionary-sourced gold reference for surface↔member segmentation.
- **Compound-formation pedagogy** — worked samāsa resolutions.
- **pwg_ru translation** — attach the member analysis as a structured field.

Sibling cheap PWG layers from the same source: derivation (`von {#base#}`, the taddhita
dataset), the [Pāṇini sūtra crosswalk](../pwg_panini_crosswalk/README.md), and German
sense glosses.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1254
follow-up; re-derived 26-07-2026 by Opus 5 1M (`claude-opus-5[1m]`) for
[#527](https://github.com/gasyoun/SanskritGrammar/issues/527) (H1703)._

_Dr. Mārcis Gasūns_
