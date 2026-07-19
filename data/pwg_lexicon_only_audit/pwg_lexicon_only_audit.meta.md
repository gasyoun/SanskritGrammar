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

- **Handoffs:** [H1310](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1310-Opus_SanskritLexicography_pwg-lexicon-only-ghostword-cross-dictionary-audit_19.07.26.md)
  (v2), [H1326](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1326-Sonnet_SanskritGrammar_kosa-corpus-fill-amara-rajanighantu-lexicon-audit_19.07.26.md)
  (v3, this pass).
- **Input:** `data/pwg_register_genre/pwg_register_genre.tsv` (PR #438, `lexicon_only=1`).
- **Comparison corpus:** `csl-orig/v02` headword sets (read-only), SLP1 `k1` keys, plus (v3)
  `kosa_extra/amar.txt` — Amarakośa sourced from
  [`sanskrit-kosha/kosha`](https://github.com/sanskrit-kosha/kosha) (GNU GPL v3.0; full
  provenance in [`kosa_extra/README.md`](kosa_extra/README.md)).
- **v3 built by:** Sonnet 5 (`claude-sonnet-5`), 19-07-2026, deterministic
  ([`build_census.py`](build_census.py)).
- **v2 built by:** Opus 4.8 (`claude-opus-4-8`), 19-07-2026, deterministic.
- **v1 built by:** a prior same-day session (PR #447, commit `3c57f29`; model tier not
  recorded in the commit).

## Ranked improvement backlog

1. **Digitise Rājanighaṇṭu / Trikāṇḍaśeṣa / generic Nighaṇṭu** (Amara done in v3). 674 of the
   2,294 pwg-uniques still cite one of these three. **No bulk lemma-tagged source exists for
   any of them** (exhausted `csl-orig`, `sanskrit-kosha/kosha` raw texts, the
   `cltk/sanskrit_text_dcs` DCS mirror, and web search — see `kosa_extra/README.md`); the
   real next step is running a Sanskrit sandhi-segmenter over the raw verse (e.g. the
   Sanskrit Heritage tools) and hand-verifying the output, or waiting for
   `sanskrit-kosha/kosha`'s own manual `<syns>` annotation to reach these three works.
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
`text-attested` is MW-only and a floor; Rājanighaṇṭu/Trikāṇḍaśeṣa/generic-Nighaṇṭu remain
absent from the comparison side (Amara resolved in v3) — PWG's own `sources` column still
records all these citations directly, so nothing is lost on the PWG side.

## Revision history

| Date | Version | Change |
|---|---|---|
| 19-07-2026 | v1 (PR #447) | First pass: koṣa corpus = `skd` only; MW treated as weak/PW-derived (no `L.`-split); already had the independence axis (corpus dicts `gra`/`bhs`, PW as same-source). pwg-unique = 2,619 (974 truly-absent). |
| 19-07-2026 | v2 | Full 7-koṣa corpus (armh/abch/acph/acsj/nmmb/vcp/skd) added per review; MW `L.`-split; independence axis preserved; homonym-sibling flag; ghost-word adjudication (≈0.05 % artifact rate). pwg-unique = 2,298 (788 truly-absent). **Supersedes v1.** |
| 19-07-2026 | v3 (this pass, H1326) | Joined Amara (`amar`, 9,788 headwords, GNU GPL v3.0, `kosa_extra/`) as an 8th koṣa. koṣa-corroborated 10,724→10,812; pwg-unique 2,298→2,294; truly-absent core (788) **unchanged**. Rājanighaṇṭu/Trikāṇḍaśeṣa/generic-Nighaṇṭu exhaustively searched but found **not sourceable** as bulk lemma-tagged data anywhere (only raw sandhi-joined verse exists) — reported as a scoped partial result (1 of the ≥2 new koṣas targeted), not forced. **Supersedes v2.** |

_Dr. Mārcis Gasūns_
