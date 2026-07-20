# Government (Rektion) lexicon + verb-class/voice census — Scherzl × Bühler × Apte × Whitney × Talmud

_Created: 17-07-2026 · Last updated: 17-07-2026_

Machine-readable extraction of
[index_Shertsl_Byuler_dopoln_180721.xlsx](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/index_Shertsl_Byuler_dopoln_180721.xlsx) —
Olga's collated catalogue of Sanskrit **case government** (управление / Rektion) built from
В. И. Шерцль's *Index of Old-Indic words and roots* (Scherzl), reconciled against Bühler 1923,
Apte (AP) and MW. This folder turns that spreadsheet into four queryable datasets and joins its
verb-class assignments to **Whitney 1889** (present-class) and **Толчельников-Талмуд 2026**
(morphoclass), the same triangulation spine used by the book's claim registry
([claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml)).

Built by Opus 4.8 (`claude-opus-4-8`), handoff
[H1195](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1195-Sonnet_SanskritGrammar_buhler-scherzl-government-and-verbclass-index_17.07.26.md).

## Files

| File | Rows | What |
|---|---|---|
| [government_structure.json](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/government_structure.json) | 197 | The analytic **case-government catalogue**: every case → sub-use → government status (direct/indirect/none) → page → governing verbs/prefixes → glossed examples |
| [government_lexicon.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/government_lexicon.jsonl) | 763 | The **inverse valency lexicon**: each root/stem → its class-readings + which cases it governs, page-anchored to Scherzl |
| [verb_class_voice_census.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/verb_class_voice_census.jsonl) | 763 | Per-root **5-source class + voice comparison** + Talmud morphoclass (ryad/tip/seṭ) |
| [verb_class_disagreements.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/verb_class_disagreements.csv) | 399 | Screening subset: every row where a class or voice source conflicts |
| [build_government_class_index.py](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/build_government_class_index.py) | — | Regenerates all four from the .xlsx + sibling sources |
| [SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md) | — | **Corpus adjudication report** — all 1 168 relations scored against the DCS treebank, incl. hand-adjudication of the contradicted set (§3 below) |
| [government_corpus_verdicts.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/government_corpus_verdicts.tsv) | 1 168 | Per-relation verdict (CONFIRMED / CONTRADICTED / UNATTESTED-INSUFFICIENT / NOT-ADJUDICABLE) + evidence, spreadsheet-friendly |
| [government_vs_dcs_adjudication.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/government_vs_dcs_adjudication.jsonl) | 1 168 | Same, richer — adds class/voice/subtype/replaceable_by + co-occurrence expected/ratio |
| [dcs_verb_government_profiles.json](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/dcs_verb_government_profiles.json) | 491 | DCS treebank-attested governed-case frame + deprel distribution for each matched verb — the corpus valency frame to set beside Scherzl's |
| [adjudicate_government_vs_dcs.py](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/adjudicate_government_vs_dcs.py) + [aggregate_dcs_gov.py](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/aggregate_dcs_gov.py) | — | Rebuild the adjudication from the [dcs-conllu](https://github.com/gasyoun/dcs-conllu) treebank |

## 1. Government (управление / Rektion)

`government_structure.json` classifies **197 sub-uses across 7 cases**, each tagged for verbal
government (`**` direct = 45, `*` indirect = 33, none = 119):

| Case | sub-uses | direct | indirect | none |
|---|---|---|---|---|
| Nominative | 15 | 6 | 2 | 7 |
| Accusative | 23 | 14 | 0 | 9 |
| Instrumental | 38 | 0 | 0 | 38 |
| Dative | 24 | 0 | 10 | 14 |
| Ablative | 31 | 6 | 10 | 15 |
| Genitive | 35 | 11 | 7 | 17 |
| Locative | 31 | 8 | 4 | 19 |

Every sub-use carries the *specific verbs/prefixes that trigger it* and *attested, glossed
examples*. `government_lexicon.jsonl` inverts this to a **root-keyed valency lexicon** — 763
root/stem rows carrying **1 168 governed-case relations** plus **246 case-alternation relations**
(places where Scherzl notes one case may be swapped for another — e.g. `.../abl.`, valuable for a
parser's valence frames). Governed-case profile:

| case | relations | | case | relations |
|---|---|---|---|---|
| instr | 285 | | dat | 150 |
| acc | 278 | | gen | 133 |
| abl | 179 | | loc | 118 |
| | | | nom | 25 |

Sub-type granularity is preserved: 12 instrumental/dative sub-functions are labelled — e.g.
`instr_orud` (instrument, 99×), `dat_ogr` (limitative dative, 83×), `dat_dop` (complementary, 66×),
`instr_soz` (sociative, 53×), `instr_pros` (prosecutive, 29×), `instr_sep` (separative, 27×).

## 2. Verb class vs Whitney and Talmud

Each root row carries up to **four independent present-class opinions** (`Класс` field, Apte,
Bühler as printed, Olga's collated `[class, voice]`), joined here to a fifth and sixth: Whitney's
Western present-class and Talmud's (which copies Whitney's class but adds a separate morphoclass).
**697/763 rows join to Whitney and Talmud**; 47 unique base roots do not — these are denominatives
and secondary roots (`daṇḍ`, `dhanāy`, `garv`, `taḍ`-type) that Whitney's root inventory excludes,
itself a reportable category.

Collapsed to **382 unique base roots**, class conflicts fall into three honest kinds:

**(a) Western-vs-Indian class differences — 10 roots — the real "not equal to Whitney and Talmud".**
The index/Apte/Bühler follow the Indian *dhātupāṭha gaṇa* system; Whitney (and therefore Talmud,
which copies him) uses his own Western present-class analysis, and they diverge systematically:

| root | Indian (index/Apte) | Whitney = Talmud |
|---|---|---|
| taḍ "strike" | 10 | 2 |
| sarj/sṛj | 4, 6 | 1 |
| vīj | 3, 6, 7 | 1 |
| marc | 10 | 4 |
| sparh | 10 | 6 |
| darś/dṛś "see" | 1 | 4 |
| majj | 6 | 1 |

**(b) Bühler-idiosyncratic — 8 roots — Bühler's printed class alone differs** while index+Apte agree
with Whitney: `cud` (B 10 vs 1), `īś` (B 6 vs 1–2), `īṣ` (B 6 vs 1), `jñā` (B 4 vs 9), `krī`
(B 4 vs 9), `mud` (B 4 vs 1), `pūj` (B 10 vs 1), `tul` (B 10 vs 1). Candidate 1923-edition typos of
the same family as the claim registry's HB-60.

**(c) Join-ambiguous — 4 roots — flagged low-confidence** (`whitney_homonyms > 1`): `aś`, `dar`,
`gar`, `i`. `i` "go" is instructive: gaṇa **2** (adādi, *eti*) in the Indian tradition the index
follows, but Whitney reanalyses it as I/IV/V — a genuine systematic difference that the homonym-union
join cannot cleanly resolve.

### Gold standard: the workbook's own human flags

The workbook marks **8 roots blue** on the Бühler column = Olga's expert "class differs from the
dictionaries" (`workbook_class_flag: true`): `aś, cakṣ, grah, idh, jñā, kar, krī, sthā`. This
human screen and the automated screen are **complementary** — they agree on `grah/jñā/krī/sthā`
as Bühler-idiosyncratic, while the human flags additionally catch `cakṣ` (where Whitney's union
`[1,2]` silently absorbs both the index's `2` and Bühler's `1`). Notable confirmed case: Whitney
lists the Vedic lemma **`grabh` (I|IX)**, which matches the index's `1,9,10` and contradicts
Bühler's printed `IV U`.

### Talmud enrichment — a dimension Scherzl/Bühler lack entirely

For all 697 joined roots the census attaches Talmud's morphoclass — `ryad` (ablaut series, e.g.
`A₁`), `tip` (alternation type I–IV), `seṭ`/`aniṭ`/`veṭ`, and `pada` (P/U/Ā) — none of which the
19th-century index records. This is the cleanest "what Talmud adds beyond class." Whitney records no
voice at all, so the voice axis (index vs Bühler vs Talmud `pada`) is a Talmud-only contribution.

## 3. Corpus adjudication — Scherzl's government vs the DCS treebank

All **1 168 governed-case relations** are checked, root by root, against the
[dcs-conllu](https://github.com/gasyoun/dcs-conllu) dependency treebank (15 900 CoNLL-U files,
5.69 M tokens, 754 726 sentences) — full report, with the hand-adjudication, in
[SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md).
Each relation resolves to its most specific DCS verb lemma (reading-stem first — with anusvāra
`ṁ→ṃ` normalisation — then bare root) and is scored on two strictly-separated evidence layers: a
**direct government arc** (a case-marked nominal that is a dependency child of the verb; strong)
and **co-occurrence measured against chance** (expected = verb_freq · corpus base-rate of the
case).

| Verdict | Relations | % | |
|---|---:|---:|---|
| CONFIRMED | 693 | 59.3 % | direct government arc found in the treebank |
| CONTRADICTED | 1 | 0.1 % | verb well-observed, case absent from every arc **and** co-occurs below half chance |
| UNATTESTED-INSUFFICIENT | 288 | 24.7 % | no arc; verb too thinly parsed, or case co-occurs but unparsed — can't judge |
| NOT-ADJUDICABLE | 186 | 15.9 % | root/stem not a DCS verb lemma |

**The headline is the adjudicability ceiling, not the confirmation rate: only ~3.9 % of DCS
sentences carry dependency arcs**, so a zero dep-count can never disconfirm a relation on its own.
Of the **982 adjudicable** relations, **70.6 % are confirmed by a direct government arc and only
one is contradicted** — and that one (√arc + ablative, an `example_only` reading Scherzl himself
marks `replaceable_by: instr`) hand-adjudicates to system-vs-usage divergence, not a defect, so
**zero errata are routed**. Scherzl's 19th-century catalogue holds up against the modern corpus to
the extent the corpus can test it. The double gate on CONTRADICTED (well-observed verb **and**
below-chance co-occurrence) is deliberately conservative so a sparse parse cannot manufacture a
contradiction — a case that co-occurs heavily (jñā + genitive) is never called contradicted just
because the parser missed the arc. NOT-ADJUDICABLE is dominated by lemma-form mismatches (Scherzl's
guṇa stem `sarj` vs DCS `sṛj`), not missing verbs, so the confirmation rate is a *lower* bound.
The sibling [dcs_verb_government_profiles.json](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/dcs_verb_government_profiles.json)
gives each verb's corpus-attested valency frame for direct comparison.

## Limitations (read before citing a conflict as fact)

- The automated class join is a **screening layer, not a verdict**. Residual false positives come
  from (i) wrong-homonym matches where the index lemma collides with a different real Whitney root
  (`har` = hṛ "take" cl.1, mis-matched to Whitney `har` "be gratified" cl.4), (ii) spelling-variant
  joins (`idh` vs Whitney `indh`), (iii) a-grade/vṛddhi spelling (`kar`/`kṛ`, `ar`/`ṛ`, bridged only
  where the index supplies the alt spelling). **Every conflict candidate needs per-root
  verification** before it enters `errata.yml` or a paper. Only the 8 workbook-flagged roots are
  human-curated ground truth.
- Government page numbers are parsed heuristically; arrow-annotations (`↓`/`↑` = line, not page) are
  excluded, but the raw collated string is retained in `government_lexicon.jsonl` so nothing is lost.
- `government_structure.json` covers 7 cases (Vocative has no government sub-uses in Scherzl).

## Reproduce

```bash
python BuhlerLeitfaden_1923/government_class_index/build_government_class_index.py
```

Requires sibling clones: [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots)
(`crosswalk/roots.csv`) adjacent to `SanskritGrammar/`, and the in-repo
[TolchelnikovTalmud_2026/data/whitney_talmud.json](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/whitney_talmud.json).

## Feeds

- The **Bühler-idiosyncratic** class candidates and the workbook's 8 blue flags feed the same
  errata/claim machinery as HB-60 →
  [errata.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/errata.yml).
- The **Western-vs-Indian** class split is a native example for paper A60 ("what grammars claim that
  the corpus / cross-grammar record does not confirm").
- The **government lexicon** is a valence resource for the Sanskrit parser / treebank stack — no
  equivalent machine-readable Rektion lexicon exists in the org crosswalk — and it is **no longer
  untested**: §3's DCS-treebank adjudication corpus-confirms 693/982 adjudicable relations by a
  direct government arc with a single (non-defect) contradiction, so a consumer can now filter
  frames by `verdict` in
  [government_corpus_verdicts.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/government_corpus_verdicts.tsv).
  The verdicts are registered as a **public** kosha dataset (id `scherzl-government-dcs-adjudication`
  in [kosha datasets.json](https://github.com/gasyoun/kosha/blob/main/data/manifest/datasets.json)) —
  cleared through `/publish-safety-check`, which ruled GO because DCS is CC BY 4.0 (attribution only)
  and the verdicts are aggregate counts, not DCS text.

_Dr. Mārcis Gasūns_
