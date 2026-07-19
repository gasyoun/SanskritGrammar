# PWG ghost-word triage cascade (H1323)

_Created: 19-07-2026 · Last updated: 19-07-2026_

The lexicon-only audit **v2** (H1310) leaves **2,270 distinct pwg-unique** headwords — present
in no other digitised Cologne dictionary — of which **777 are absent even from Böhtlingk's own
PWK** (`pw`), the hardest ghost-word core. Hand-adjudicating them is too much. This cascade
auto-classifies each into a bucket using layers we already own plus one **reused** normalizer,
so a human only ever reviews the small true residue — and it cross-checks every verdict against
v2's independent citation-source category.

Result: **777 → 141 residue** (81.9 % triaged away). Every non-residue word carries its evidence
(the matched attested word, the xref target, or the marker tags) so its verdict is checkable at
a glance.

> Consumes the v2 [`pwg_ghostword_shortlist.tsv`](../pwg_lexicon_only_audit/pwg_ghostword_shortlist.tsv).
> v2 already classifies each ghost-word by its **citation source** (`src_category`:
> ms-catalogue-propername / scholarly-journal-technical / koṣa-not-digitised); this cascade adds
> the orthogonal **morphological + PWG-body-marker + normalization** signal v2 does not carry, and
> reports where the two agree.

## The cascade

Each word is tagged by **all** signals that fire; a single `verdict` is picked by precedence
(misreading › spelling-variant › xref-attested › propername › compositional ›
descriptive-compound › residue).

| Stage | Signal → what it proves | Source |
|---|---|---|
| **1. Compositional** | word ∈ `pwg_compound_splits` / `pwg_derivation_graph`, or its PWG body carries a `({#X#} + {#Y#})` compound formula or a `von {#base#}` note → not a novel simplex | own layers + body backstop |
| **2. Body markers** | `<ab>N. pr.</ab>`/`<ab>N.</ab>` → proper name · `falsche/richtige Lesart` → PWG-declared **misreading** · `= {#X#}` → PWG's own cross-reference to word X | one regex pass over committed `pwg.txt` |
| **3. Descriptive gloss** | German gloss is a `dessen…/deren…` bahuvrīhi paraphrase → a compound the splitter missed | own `pwg_german_glosses` |
| **4. Normalization re-join** | the word's confusion-collapsed skeleton key matches an attested headword in another dictionary **within edit distance ≤ 2** → a spelling/OCR/sandhi variant of an attested word; the same key resolves each `= {#X#}` xref target | reused `slp1util.confusion_key` + `edit_distance` |

**Stage 4 reuses, does not re-implement.** The confusion-collapsing SLP1 skeleton key is
[`SanskritSpellCheck/detectors/slp1util.py`](https://github.com/gasyoun/SanskritSpellCheck/blob/main/detectors/slp1util.py)
`confusion_key` — the org's documented canonical scribal/OCR key (SHARED_CODE.md §12) — with its
capped `edit_distance`. It collapses vowel-length, ś/ṣ/s, retroflex↔dental, nasals, aspiration
and v/b, so `AdyavIja` collides with the standard `AdyabIja` (bīja) and `Adityapatra` with
`Adityapattra`. The `edit_distance ≤ 2` filter rejects distant same-skeleton collisions and lets
us record the **actual matched headword** rather than a bare dict code.

## The 777 core, by verdict

| Verdict | Count | % | Meaning |
|---|---:|---:|---|
| **spelling-variant** | 294 | 37.8 % | variant of an attested word (`variant_of` names it) |
| **propername** | 170 | 21.9 % | PWG `N. pr.` — a name, not common lexis |
| **residue** | 141 | 18.1 % | no signal fired → genuine ghost-word candidate (the human list) |
| **compositional** | 117 | 15.1 % | transparent compound / regular derivative |
| **misreading** | 31 | 4.0 % | PWG itself flags a wrong reading |
| **xref-attested** | 24 | 3.1 % | PWG `= X` where X is an attested synonym |

## Cross-validation against v2's citation-source category

The `v2_src_category` column lets each verdict be checked against v2's independent, citation-based
classification. The two methods corroborate where it matters:

- **propername** (170): 115 are v2 `ms_catalogue_propernoun` — v2 reaches the same conclusion from
  the citation source that this cascade reaches from the `N. pr.` body marker.
- **residue** (141): the largest v2 category is `scholarly_journal_technical` (57) — matching the
  observed make-up of the residue (technical maths vocabulary from Colebrooke &c.). A further 49
  are v2 `ms_catalogue_propernoun`: proper-name-like words whose PWG body carried no `N. pr.`
  marker, so they escaped stage 2 — the honest gap this cascade does not close.
- **spelling-variant** (294): 160 are v2 `kosa_nighantu_not_digitised` — variants of words living
  only in koṣas PWG cites but Cologne has not digitised.

## Outputs

- [`pwg_ghostword_triage.tsv`](pwg_ghostword_triage.tsv) — every pwg-unique word: `k1 · core ·
  verdict · tags · variant_of · variant_dicts · xref_target · v2_src_category · accented · gloss`.
- [`pwg_ghostword_residue.tsv`](pwg_ghostword_residue.tsv) — the **141-word review list**: `k1 ·
  accented (<k2>) · gloss`, ready to drop into a `/review-sheet`. The genuine core: technical maths
  vocabulary (`BAgApahArajAti`, `aMSasavarRa` "reducing fractions"), transliterated foreign
  toponyms (`andulIsa` = Andalusia, `antAkzI` = Antioch), rare simplexes — plus some long
  compound-titles only a morphological splitter (deferred stage 5) would remove.
- [`pwg_ghostword_triage_summary.json`](pwg_ghostword_triage_summary.json) — the counts + the full
  verdict × v2-src_category cross-tab.

## Honest scope

- The skeleton key is deliberately **aggressive** (built for scribal/OCR correction); the `ED ≤ 2`
  filter is what keeps precision. A spot-check of the spelling-variant bucket found every sampled
  match a genuine variant, but the verdict is a **machine judgement** — the `variant_of` column
  exists so a human can confirm, not so the word is deleted.
- Stages 1–4 only. **Stage 5** (vidyut compound decomposition, to catch the long compound-titles
  and the 49 catalogue-propername words still in the residue) and **stage 6** (DCS corpus
  attestation) are deferred to the residue.
- A `propername`/`compositional` word may also be a variant; the `tags` column keeps every signal,
  the `verdict` keeps only the highest-precedence one.

## Regenerate

```sh
python scripts/pwg_ghostword_triage.py
```

Deterministic; read-only. Requires the H1310 v2 ghost-word shortlist + the PWG layers under
`data/`, the committed `../csl-orig`, and `SanskritSpellCheck` + `sanskrit-util` cloned as
siblings (stage 4 degrades with a loud warning if absent). No network.

_Auto-generated dataset; extractor authored by Opus 4.8 (`claude-opus-4-8[1m]`), H1323._

_Dr. Mārcis Gasūns_
