# pwg_lexicon_only_audit — metadoc

_Created: 19-07-2026 · Last updated: 19-07-2026_

Companion record for the PWG lexicon-only cross-dictionary audit
([`README.md`](README.md) + its data files). The document *about* the dataset: why it
exists, how it was built, where it is weak, and how it changed.

## Purpose & audience

Isolate and characterise PWG's **lexicon-only vocabulary** (32,690 headwords attested only
in koṣas, never in a dated text) — the "lexicographers' words" / potential ghost-words — by
joining against every other digitised dictionary. Audience: lexicographers assessing PWG
coverage, and anyone building on the [PWG register/genre layer](../pwg_register_genre/).

## Provenance

- **Handoff:** [H1310](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1310-Opus_SanskritLexicography_pwg-lexicon-only-ghostword-cross-dictionary-audit_19.07.26.md).
- **Input:** `data/pwg_register_genre/pwg_register_genre.tsv` (PR #438, `lexicon_only=1`).
- **Comparison corpus:** `csl-orig/v02` headword sets (read-only), SLP1 `k1` keys.
- **v2 built by:** Opus 4.8 (`claude-opus-4-8`), 19-07-2026, deterministic
  ([`build_census.py`](build_census.py)).
- **v1 built by:** a prior same-day session (PR #447, commit `3c57f29`; model tier not
  recorded in the commit).

## Ranked improvement backlog

1. **Digitise the missing koṣas/nighaṇṭus** — Amara (AK), Rājanighaṇṭu, Trikāṇḍaśeṣa,
   Nighaṇṭu, Ratnamālā, Hārāvalī. 678 of the 2,298 pwg-uniques are sourced from these; adding
   them would reclassify most from "unique" to "corroborated". Highest-value next step.
2. **Homonym-precise join** — current join is spelling-level because dict hom-numbering does
   not align. A sense/gloss-based aligner would sharpen the 2,757 sibling-ambiguous
   text-attested rows.
3. **`L.`-split PW and Apte** too (only MW is split now) — would lift the `text-attested`
   floor and reclassify part of `dict-lexical`.
4. **Reconcile MW non-`L.` sources that are themselves named lexica** — a residue of
   `text-attested` is koṣa-corroboration mislabelled as text.
5. **Feed the 9,347 "MW-real-cite, no PWG text-sibling" rows back to PWG** as candidate
   text citations PWG's lexical entries lack (enrichment, not correction).

## Limitations

See README "Honest limitations". Headline: the join is spelling-level (homonym-collapsed);
`text-attested` is MW-only and a floor; Amara is absent from the comparison side (though
PWG's own `sources` column records its AK citations).

## Revision history

| Date | Version | Change |
|---|---|---|
| 19-07-2026 | v1 (PR #447) | First pass: koṣa corpus = `skd` only; MW treated as weak/PW-derived (no `L.`-split); already had the independence axis (corpus dicts `gra`/`bhs`, PW as same-source). pwg-unique = 2,619 (974 truly-absent). |
| 19-07-2026 | v2 (this pass) | Full 7-koṣa corpus (armh/abch/acph/acsj/nmmb/vcp/skd) added per review; MW `L.`-split; independence axis preserved; homonym-sibling flag; ghost-word adjudication (≈0.05 % artifact rate). pwg-unique = 2,298 (788 truly-absent). **Supersedes v1.** |

_Dr. Mārcis Gasūns_
