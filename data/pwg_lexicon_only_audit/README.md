# PWG lexicon-only headwords — cross-dictionary audit (v3)

_Created: 19-07-2026 · Last updated: 19-07-2026_

Audit of the **32,690 PWG headwords flagged `lexicon_only=1`** by the
[PWG register/genre layer](../pwg_register_genre/) — words the *Petersburger Wörterbuch*
(gross) attests **only** from Sanskrit koṣas, never from a dated text — against the other
digitised dictionaries, to answer: is each lexicon-only word attested elsewhere, and which
of them are genuine "ghost-words" unique to PWG? Handoff
[H1310](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1310-Opus_SanskritLexicography_pwg-lexicon-only-ghostword-cross-dictionary-audit_19.07.26.md)
(v2), [H1326](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1326-Sonnet_SanskritGrammar_kosa-corpus-fill-amara-rajanighantu-lexicon-audit_19.07.26.md)
(v3 — this pass, adds Amara). This **v3 supersedes** v2 — see
[Version history](#version-history).

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
| **Koṣa** (Sanskrit–Sanskrit thesauri) | `armh` Abhidhānaratnamālā · `abch` Abhidhānacintāmaṇi · `acph` Abhidhānacintāmaṇipariśiṣṭa · `acsj` Abhidhānacintāmaṇiśiloñcha · `nmmb` Nāmamālikā · `vcp` Vācaspatya · `skd` Śabdakalpadruma · `amar` **Amarakośa (H1326)** |
| **Independent text corpus** | `gra` Grassmann (Ṛgveda) · `bhs` Edgerton (Buddhist Hybrid Sanskrit) |
| **Text-dictionary** | `mw` (with `L.`-split) · `ap90` · `ap` (Apte) |
| **Same source (not corroboration)** | `pw` (Böhtlingk, kürzere Fassung) |

**Coverage gap (v3 — narrowed):** **H1326 sourced Amara (`amar`, GNU GPL v3.0, from
[`sanskrit-kosha/kosha`](https://github.com/sanskrit-kosha/kosha) — see
[`kosa_extra/README.md`](kosa_extra/README.md))**, closing that gap. **Rājanighaṇṭu,
Trikāṇḍaśeṣa, generic Nighaṇṭu, Ratnamālā, Hārāvalī remain undigitised** as bulk
lemma-tagged headword sets — every source checked (`csl-orig`, `sanskrit-kosha/kosha`'s own
raw texts, the `cltk/sanskrit_text_dcs` DCS mirror, web search) is unsegmented sandhi-joined
verse with no per-word tagging; see `kosa_extra/README.md` for the full source audit. PWG's
own `sources` column already records its `AK`/`RĀJAN`/`TRIK`/`NIGH` etc. citations directly,
so PWG-side provenance is not lost; the residual gap is on the *comparison* side only.

## Result — 32,690 lexicon-only headwords (v3)

| Verdict | Count | % | Meaning |
|---|---:|---:|---|
| **text-attested** | 12,606 | 38.6 % | MW non-`L.` citation, or present in a text corpus (`gra`/`bhs`) — genuine text attestation, independent of PW-copying |
| **koṣa-corroborated** | 10,812 | 33.1 % | in ≥1 of the 8 koṣas (no text attestation) |
| **dict-lexical** | 6,978 | 21.3 % | only in MW-`L.` / Apte headword lists — lexical, no koṣa / real cite |
| **pwg-unique** | 2,294 | 7.0 % | in **no independent** dictionary → ghost-word shortlist |

- **v3 delta (Amara joined):** koṣa-corroborated **10,724 → 10,812** (+88), dict-lexical
  **7,062 → 6,978** (−84), pwg-unique **2,298 → 2,294** (−4), text-attested unchanged
  (12,606). Of the 4 newly-resolved pwg-uniques, all 4 came from the "present only in
  same-source PW" fringe (1,510 → 1,506) — the **hardest 788 "absent from every dictionary"
  core is unchanged** (none of those 788 happen to be Amara-cited words). This is a real but
  modest gain: Amara alone does not meaningfully shrink the hardest residue, though it is now
  methodologically joined rather than recorded as a gap.
- The **2,294 pwg-unique** split into **1,506 present only in same-source PW** (Böhtlingk's
  own *kürzere Fassung* — not independent corroboration) and **788 absent from every digitised
  dictionary** (the hardest ghost-word core, unchanged from v2). Of those 788, **73 collapse**
  onto an existing headword under a light normalisation (drop final visarga/anusvara) →
  **≈715 truly-absent**.
- **10,032** lexicon-only words are corroborated by a koṣa PWG did **not** itself cite
  (novel corroboration; was 10,010 in v2).

### The ghost-word shortlist is real vocabulary, not OCR noise

Hand-adjudication of a stratified sample and a source-token breakdown of all **2,294**
(v3; was 2,298) pwg-unique words:

| Dominant source | Count | Character |
|---|---:|---|
| **scholarly / journal / technical** (Colebrooke, Indische Studien, Burnouf) | 834 | maths, metrics, grammar terms & proper nouns |
| **MS catalogue / proper noun** (`Verz. d. B. H.` = Weber's Berlin catalogue) | 768 | names of works, authors, physicians — real but onomastic |
| **koṣa / nighaṇṭu not digitised** (Rājanighaṇṭu, Trikāṇḍaśeṣa, Nighaṇṭu, Ratnamālā — Amara now digitised, v3) | 674 | genuine plant/medical/synonym vocabulary — *corpus gap*, not ghosts (was 678; −4 resolved by Amara) |
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
- **Rājanighaṇṭu, Trikāṇḍaśeṣa, generic Nighaṇṭu are absent** from the comparison side
  (v3: Amara resolved, these three remain the biggest coverage gap — see
  `kosa_extra/README.md` for the full source audit of why they could not be sourced in bulk).

## Feedback to the register layer

The audit **confirms** the register layer's `lexicon_only` flag is sound: adjudication found
real words, and the layer correctly separates homonyms (e.g. `aMhati` hom1 vedic/RV vs hom2
lexical). No re-derivation is warranted. **v3 update:** digitising Amara (done, H1326) only
shrank the pwg-unique shortlist by 4 and left the hardest 788-word "absent from every
dictionary" core untouched — the corpus-coverage lever is real but smaller than v2 projected.
Rājanighaṇṭu/Trikāṇḍaśeṣa/Nighaṇṭu (674 of the 2,294 pwg-uniques cite one of these) remain the
productive next step, but require a real Sanskrit segmenter/annotation pass, not just a
bulk-download — see `kosa_extra/README.md`.

## Version history

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

**v3 (H1326, this pass)** joined Amara (`amar`, `kosa_extra/amar.txt`, GNU GPL v3.0) as an 8th
koṣa. Effect: koṣa-corroborated 10,724→10,812 (+88), dict-lexical 7,062→6,978 (−84),
pwg-unique 2,298→2,294 (−4); the hardest 788 truly-absent core is **unchanged**. Rājanighaṇṭu,
Trikāṇḍaśeṣa and generic Nighaṇṭu were exhaustively searched (`csl-orig`, `sanskrit-kosha/kosha`
raw texts, the `cltk/sanskrit_text_dcs` DCS mirror, web search) but **no bulk lemma-tagged
headword set exists for any of the three** — every digitisation found is unsegmented
sandhi-joined verse; full audit in [`kosa_extra/README.md`](kosa_extra/README.md). **v3 does
not meet the "≥2 new koṣas" target set by H1326** — only Amara was cleanly sourceable; this is
reported as a scoped partial result rather than forcing a low-quality parse of the raw verse
texts.

| Axis | v2 | v3 (this pass) |
|---|---|---|
| Koṣa comparison set | 7 koṣas | **8 koṣas** — adds `amar` (Amarakośa) |
| pwg-unique | 2,298 (788 truly-absent) | **2,294** (788 truly-absent, unchanged) |
| koṣa-corroborated | 10,724 | **10,812** |
| Remaining gap | Amara + Rājanighaṇṭu + Trikāṇḍaśeṣa + Nighaṇṭu + Ratnamālā + Hārāvalī | **Rājanighaṇṭu + Trikāṇḍaśeṣa + Nighaṇṭu only** (Ratnamālā/Hārāvalī: Ratnamālā already covered as `armh`; Hārāvalī checked, raw verse only, not sourceable) |

## Files

| File | |
|---|---|
| [`pwg_lexicon_only_cross_dictionary_census.tsv`](pwg_lexicon_only_cross_dictionary_census.tsv) | 32,690 rows — `verdict`, `mw_realcite`, `corpus_hit`, `also_in_pw_same_source`, `pwg_text_sibling`, `present_in`, `novel_kosa`, `pwg_cited_sources` |
| [`pwg_ghostword_shortlist.tsv`](pwg_ghostword_shortlist.tsv) | the 2,294 pwg-unique rows + `src_category` |
| [`census_summary.json`](census_summary.json) | all counts (machine-readable) |
| [`build_census.py`](build_census.py) | reproducible pipeline (reads `csl-orig/v02` + `kosa_extra/` + the register TSV) |
| [`kosa_extra/`](kosa_extra/) | koṣa data sourced by H1326 outside `csl-orig` (`amar.txt` + provenance `README.md`) |
| [`pwg_lexicon_only_audit.meta.md`](pwg_lexicon_only_audit.meta.md) | metadoc — provenance, backlog, v1→v2→v3 history |

## Regenerate

```sh
# needs csl-orig checked out as a sibling of the repo root, kosa_extra/ present, and the register TSV present
python build_census.py
```

_Dr. Mārcis Gasūns_
