# PWG lexicon-only headwords — cross-dictionary audit (v2)

_Created: 19-07-2026 · Last updated: 19-07-2026_

Audit of the **32,690 PWG headwords flagged `lexicon_only=1`** by the
[PWG register/genre layer](../pwg_register_genre/) — words the *Petersburger Wörterbuch*
(gross) attests **only** from Sanskrit koṣas, never from a dated text — against the other
digitised dictionaries, to answer: is each lexicon-only word attested elsewhere, and which
of them are genuine "ghost-words" unique to PWG? Handoff
[H1310](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1310-Opus_SanskritLexicography_pwg-lexicon-only-ghostword-cross-dictionary-audit_19.07.26.md).
This **v2 supersedes** the first pass (PR #447) — see [Version history](#version-history--v2-supersedes-v1-pr-447).

## Two ways bare dictionary membership lies — and how the join corrects each

1. **MW's `L.` opacity.** MW and PW absorbed the whole koṣa vocabulary as `L.`-marked
   entries (`L.` = "lexicographers", i.e. koṣa-sourced, no text attestation, and MW never
   names *which* koṣa). **59,697 of MW's 194,084 headwords (30.8 %) are `L.`-only.** So bare
   MW membership re-confirms "lexical word", nothing more. → The join reads MW's `<ls>`
   citations and counts only a **non-`L.`** source as text attestation.
2. **The Böhtlingk tradition is not independent of itself.** PW is Böhtlingk's own *kürzere
   Fassung* (same author as PWG); MW was compiled substantially *from* PW. A PWG-lexical word
   appearing in PW/MW may just be the same tradition copying itself. → **PW is scored as
   "same source" (never corroboration)**, and genuine independence is measured by the
   **text-corpus dictionaries** Grassmann-RV (`gra`) and Edgerton-BHS (`bhs`), whose every
   headword is by construction text-sourced.

## Comparison corpus (all SLP1 `k1` headword sets, from `csl-orig/v02`)

| Role | Dictionaries |
|---|---|
| **Koṣa** (Sanskrit–Sanskrit thesauri) | `armh` Abhidhānaratnamālā · `abch` Abhidhānacintāmaṇi · `acph` Abhidhānacintāmaṇipariśiṣṭa · `acsj` Abhidhānacintāmaṇiśiloñcha · `nmmb` Nāmamālikā · `vcp` Vācaspatya · `skd` Śabdakalpadruma |
| **Independent text corpus** | `gra` Grassmann (Ṛgveda) · `bhs` Edgerton (Buddhist Hybrid Sanskrit) |
| **Text-dictionary** | `mw` (with `L.`-split) · `ap90` · `ap` (Apte) |
| **Same source (not corroboration)** | `pw` (Böhtlingk, kürzere Fassung) |

**Coverage gap:** **Amara (AK), Rājanighaṇṭu, Trikāṇḍaśeṣa, Nighaṇṭu, Ratnamālā, Hārāvalī**
are koṣas/nighaṇṭus PWG *cites* but which are **not digitised in `csl-orig`** — the single
biggest limit on this audit (see the ghost-word breakdown). PWG's own `sources` column already
records its `AK` (Amara) etc. citations directly, so PWG-side provenance is not lost; the gap
is on the *comparison* side.

## Result — 32,690 lexicon-only headwords

| Verdict | Count | % | Meaning |
|---|---:|---:|---|
| **text-attested** | 12,606 | 38.6 % | MW non-`L.` citation, or present in a text corpus (`gra`/`bhs`) — genuine text attestation, independent of PW-copying |
| **koṣa-corroborated** | 10,724 | 32.8 % | in ≥1 of the 7 koṣas (no text attestation) |
| **dict-lexical** | 7,062 | 21.6 % | only in MW-`L.` / Apte headword lists — lexical, no koṣa / real cite |
| **pwg-unique** | 2,298 | 7.0 % | in **no independent** dictionary → ghost-word shortlist |

- The **2,298 pwg-unique** split into **1,510 present only in same-source PW** (Böhtlingk's
  own *kürzere Fassung* — not independent corroboration) and **788 absent from every digitised
  dictionary** (the hardest ghost-word core). Of those 788, **73 collapse** onto an existing
  headword under a light normalisation (drop final visarga/anusvara) → **≈715 truly-absent**.
- **10,010** lexicon-only words are corroborated by a koṣa PWG did **not** itself cite
  (novel corroboration).

### The ghost-word shortlist is real vocabulary, not OCR noise

Hand-adjudication of a stratified sample and a source-token breakdown of all **2,298**
pwg-unique words:

| Dominant source | Count | Character |
|---|---:|---|
| **scholarly / journal / technical** (Colebrooke, Indische Studien, Burnouf) | 834 | maths, metrics, grammar terms & proper nouns |
| **MS catalogue / proper noun** (`Verz. d. B. H.` = Weber's Berlin catalogue) | 768 | names of works, authors, physicians — real but onomastic |
| **koṣa / nighaṇṭu not digitised** (Rājanighaṇṭu, Trikāṇḍaśeṣa, Amara, Nighaṇṭu, Ratnamālā) | 678 | genuine plant/medical/synonym vocabulary — *corpus gap*, not ghosts |
| **other / unresolved** | 18 | the only genuine OCR/segmentation-artifact residue |

Sampled entries — `atyamlaparRa` (*Asclepias acida*, Rājanighaṇṭu), `ahiPeRa` (opium,
Rājanighaṇṭu), `ativizAdin` (a physician, *Verz.*), `aMSasavarRa` (reduction of fractions,
Colebrooke's Algebra), `atiliha` (a metre) — are all well-formed PWG entries. **The genuine
ghost-word (artifact) rate is ≈ 18 / 32,690 ≈ 0.05 %.** PWG's lexicon-only layer is
high-quality real material whose *sources* (koṣas, nighaṇṭus, catalogues) are simply not in
the digitised comparison set.

## Honest limitations

- **The join is spelling-level (homonym-collapsed).** Dictionary hom-numbering does not align
  across works, so a `k1` hit cannot be pinned to the specific PWG homonym. Flagged per row
  (`pwg_text_sibling`): of the 12,606 text-attested, **2,757 have a PWG text-attested sibling
  homonym** (ambiguous — the hit may belong to that sibling) and **9,849 do not** (MW/corpus
  and PWG genuinely disagree). The **pwg-unique shortlist is immune** — a spelling in no
  independent dictionary cannot be rescued by any homonym.
- **`text-attested` is a floor.** Only MW is `L.`-split; Apte is not, so a word attested only
  in Apte with a real source is scored `dict-lexical`. A few MW non-`L.` `<ls>` sources are
  themselves named lexica, so a small part of `text-attested` is koṣa-corroboration in disguise.
- **Amara is absent** from the comparison side (biggest coverage gap).

## Feedback to the register layer

The audit **confirms** the register layer's `lexicon_only` flag is sound: adjudication found
real words, and the layer correctly separates homonyms (e.g. `aMhati` hom1 vedic/RV vs hom2
lexical). No re-derivation is warranted. The productive next step is **corpus coverage**, not
a flag change: digitising Amara / Rājanighaṇṭu / Trikāṇḍaśeṣa / Nighaṇṭu would reclassify most
of the 678 koṣa/nighaṇṭu pwg-uniques from "unique" to "corroborated".

## Version history — v2 supersedes v1 (PR #447)

A first pass ([PR #447](https://github.com/gasyoun/SanskritGrammar/pull/447), commit
`3c57f29`, also Opus 4.8, same day) shipped `pwg_lexicon_only_audit.tsv` +
`pwg_unique_shortlist.tsv` + a summary json and `scripts/pwg_lexicon_only_audit.py`. **v2
replaces all of them.** Full provenance in
[`pwg_lexicon_only_audit.meta.md`](pwg_lexicon_only_audit.meta.md).

| Axis | v1 (PR #447) | v2 (this pass) |
|---|---|---|
| Koṣa comparison set | **`skd` only** | **7 koṣas** — armh, abch, acph, acsj, nmmb, vcp, skd |
| MW | "weak, derived from PW", undifferentiated | **`L.`-split** — non-`L.` citation = text attestation |
| Independence axis | ✔ corpus dicts `gra`/`bhs`, PW as same-source | **kept and carried forward** |
| Homonyms | collapsed silently | **flagged** (`pwg_text_sibling`), quantified |
| Ghost-word adjudication | spot note | full source-category breakdown, ≈0.05 % artifact rate |
| **pwg-unique** (no independent corroboration) | **2,619** (974 truly-absent) | **2,298** (788 truly-absent) |

v1 was not wrong — it already had the independence insight (MW ⊃ PW; corpus dicts as the real
signal), which v2 preserves. v1's limit was a **single-koṣa** comparison and treating MW as an
undifferentiated block. Adding the six other koṣas and splitting MW's `L.` reclassified
**321** formerly-unique words as corroborated and shrank the truly-absent core from 974 to 788,
while making the large middle buckets (`text-attested`, `koṣa-corroborated`) meaningful for the
first time. **The lesson v2 makes visible: most PWG "ghost-words" are corpus gaps, not ghosts.**

## Files

| File | |
|---|---|
| [`pwg_lexicon_only_cross_dictionary_census.tsv`](pwg_lexicon_only_cross_dictionary_census.tsv) | 32,690 rows — `verdict`, `mw_realcite`, `corpus_hit`, `also_in_pw_same_source`, `pwg_text_sibling`, `present_in`, `novel_kosa`, `pwg_cited_sources` |
| [`pwg_ghostword_shortlist.tsv`](pwg_ghostword_shortlist.tsv) | the 2,298 pwg-unique rows + `src_category` |
| [`census_summary.json`](census_summary.json) | all counts (machine-readable) |
| [`build_census.py`](build_census.py) | reproducible pipeline (reads `csl-orig/v02` + the register TSV) |
| [`pwg_lexicon_only_audit.meta.md`](pwg_lexicon_only_audit.meta.md) | metadoc — provenance, backlog, v1→v2 history |

## Regenerate

```sh
# needs csl-orig checked out as a sibling of the repo root, and the register TSV present
python build_census.py
```

_Dr. Mārcis Gasūns_
