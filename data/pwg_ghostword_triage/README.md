# PWG ghost-word triage cascade (H1323)

_Created: 19-07-2026 · Last updated: 19-07-2026_

The lexicon-only audit **v2** (H1310) leaves **2,270 distinct pwg-unique** headwords — present
in no other digitised Cologne dictionary — of which **777 are absent even from Böhtlingk's own
PWK** (`pw`), the hardest ghost-word core. Hand-adjudicating them is too much. This cascade
auto-classifies each into a bucket using layers we already own plus one **reused** normalizer,
so a human only ever reviews the small true residue — and it cross-checks every verdict against
v2's independent citation-source category.

Result: **777 → 16 residue** (97.9 % triaged away). Every non-residue word carries its evidence
(the matched attested word, the xref target, or the marker tags) so its verdict is checkable at
a glance. The reduction chain across the whole programme: **974 (v1 core) → 788 (v2) → 141
(triage stages 1–4) → 16 (greedy decomposition + expanded markers + v2-source fallback)**.

> Consumes the v2 [`pwg_ghostword_shortlist.tsv`](../pwg_lexicon_only_audit/pwg_ghostword_shortlist.tsv).
> v2 already classifies each ghost-word by its **citation source** (`src_category`:
> ms-catalogue-propername / scholarly-journal-technical / koṣa-not-digitised); this cascade adds
> the orthogonal **morphological + PWG-body-marker + normalization** signal v2 does not carry, and
> reports where the two agree.

## The cascade

Each word is tagged by **all** signals that fire; a single `verdict` is picked by precedence
(misreading › spelling-variant › xref-attested › propername › compositional ›
descriptive-compound › catalogue-propername › kosa-corpus-gap › residue).

| Stage | Signal → what it proves | Source |
|---|---|---|
| **1. Compositional** | word ∈ `pwg_compound_splits` / `pwg_derivation_graph`, or its PWG body carries a `({#X#} + {#Y#})` compound formula / `von {#base#}` note, **or it splits (greedy longest-prefix) into ≥2 attested headwords** → not a novel simplex | own layers + body backstop + 302k-headword decomposition |
| **2. Body markers** | `<ab>N. pr.</ab>`/`<ab>N.</ab>`/`Titel eines …`/`Name eines …` → proper name or work title · `falsche/richtige Lesart`/`zu lesen für`/`fehlerhaft`/`…kritisch für` → PWG-declared misreading/emendation/dialect variant · `= {#X#}` → PWG's own cross-reference | one regex pass over committed `pwg.txt` |
| **3. Descriptive gloss** | German gloss is a `dessen…/deren…` bahuvrīhi paraphrase → a compound the splitter missed | own `pwg_german_glosses` |
| **4. Normalization re-join** | the word's confusion-collapsed skeleton key matches an attested headword in another dictionary **within edit distance ≤ 2** → a spelling/OCR/sandhi variant of an attested word; the same key resolves each `= {#X#}` xref target | reused `slp1util.confusion_key` + `edit_distance` |
| **5. v2 source fallback** | when 1–4 are silent: v2 `src_category = ms_catalogue_propernoun` → a catalogue name/title (`catalogue-propername`); `= kosa_nighantu_not_digitised` → attested in a koṣa PWG names but not digitised (`kosa-corpus-gap`) | v2 `src_category` |

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
| **spelling-variant** | 293 | 37.7 % | variant of an attested word (`variant_of` names it) |
| **propername** | 199 | 25.6 % | PWG `N. pr.` / `Titel …` / `Name eines …` — a name or work title |
| **compositional** | 171 | 22.0 % | compound (incl. greedy-decomposed) / regular derivative |
| **misreading** | 38 | 4.9 % | PWG flags a wrong reading / emendation / dialect variant |
| **xref-attested** | 24 | 3.1 % | PWG `= X` where X is an attested synonym |
| **catalogue-propername** | 23 | 3.0 % | (stage 5) cited only from a manuscript catalogue |
| **residue** | 16 | 2.1 % | no signal fired → genuine ghost-word candidate (the human list) |
| **kosa-corpus-gap** | 13 | 1.7 % | (stage 5) attested in a non-digitised koṣa |

The 16 residue: mostly transliterated **foreign toponyms** from Weber's Berlin-MS catalogue
(`isaPahARa` = Isfahan, `pArAsapuli` = Persepolis, `oqISadeSa` = Odisha, `KamBAyatabindara` =
Cambay, `hUNgarAI`, `mugasTAna`), plus a few genuine rare terms (`BAgApahArajAti` a maths term,
`namiTuna` "Gemini", `cuwikA` "foot-washing vessel", `bfhatsUryasidDAnt`) and one internal variant
(`viviwwyE` = `vivizwyE`, both PWG-only). This is the irreducible interesting core — words that
genuinely warrant a human's eyes.

## Cross-validation against v2's citation-source category

The `v2_src_category` column lets each verdict be checked against v2's independent, citation-based
classification — the two methods corroborate where it matters: the body-marker **propername** set
agrees heavily with v2's `ms_catalogue_propernoun`, and what remains in the residue is dominated
by v2's `scholarly_journal_technical` (the toponyms/technical terms), exactly the make-up observed.
The full verdict × `src_category` cross-tab is in the summary JSON.

## Outputs

- [`pwg_ghostword_triage.tsv`](pwg_ghostword_triage.tsv) — every pwg-unique word: `k1 · core ·
  verdict · tags · variant_of · variant_dicts · xref_target · compound_parts · v2_src_category ·
  accented · gloss`.
- [`pwg_ghostword_residue.tsv`](pwg_ghostword_residue.tsv) — the **16-word review list**: `k1 ·
  accented (<k2>) · gloss`, ready to drop into a `/review-sheet` (see the toponym/technical make-up
  above).
- [`pwg_ghostword_triage_summary.json`](pwg_ghostword_triage_summary.json) — the counts + the full
  verdict × v2-src_category cross-tab.

## Honest scope

- The skeleton key is deliberately **aggressive** (built for scribal/OCR correction); the `ED ≤ 2`
  filter is what keeps precision. A spot-check of the spelling-variant bucket found every sampled
  match a genuine variant, but the verdict is a **machine judgement** — the `variant_of` /
  `compound_parts` columns exist so a human can confirm, not so the word is deleted.
- Greedy decomposition is **string-level** — it does not undo sandhi at the compound join, so a
  handful of sandhi-boundary compounds (`caturTa+AraRyaka`) stay in the residue; the deferred
  **stage 6** (vidyut sandhi-aware split) + DCS corpus attestation would clear those.
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
