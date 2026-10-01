# Grammar Lab G1 — source-identifier audit

_Created: 13-08-2026 · Last updated: 13-08-2026_

Audit of stable identifiers consumed by
[H2492 (Grok 4.6) — Grammar Lab G1: Whitney + Zalizniak evidence graph and export](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2492-Grok_SanskritGrammar_grammar-lab-g1-evidence-graph_09.08.26.md).
New loci are minted only where a work has no host-stable section id.

## Whitney

| Kind | Existing id | Source of the tail | Status |
|---|---|---|---|
| Grammar section | `whitney-sec:<n>` or `whitney-sec:<lo>-<hi>` | Whitney 1889 §§1–1316; range form already used by [typed_link_thematic.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/SubjectConcordance/typed_link_thematic.tsv) | Reuse |
| Root roster | `whitney-root:<whitney_no>` | [WhitneyRoots/crosswalk/roots.csv](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/roots.csv) primary key | Reuse |
| Bare root | `root:<SLP1>` | Type-D grammar fallback when no roster number applies | Reuse; not needed for Wave-1 cited roots |

Guna/vṛddhi increment is Whitney §§235–243 (ch. III). That chapter is also the sandhi chapter; Wave 1 cites those paragraphs only as the increment description, and does not implement Sandhi (fenced until Emeneau).

## Zalizniak 1978 (*Очерк*)

Native apparatus: `<span id="sN"></span>**§ N**` in
[Zalizniak-Ocherk_29-11-20-aligned.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/Zalizniak-Ocherk_29-11-20-aligned.mdx).
Canonical id: `zalizniak-1978-sec:<N>`. No registry row is required beyond verifying that `sN` exists.

Verbal-morphology anchors used in Wave 1 include §§50, 60–63, 109–136, 139–147, 150–157, 160–165, 167.

## Zalizniak 1975 (classification article)

No paragraph numbers. The English MDX is continuous prose plus Tables 1–5.
G1 therefore adds a deterministic locus registry keyed on the article's own titled blocks, in source order:
`zalizniak-1975:<slug>`. Tails are slugs of the titled blocks, not line numbers (the
`loc` field in [root_classifier.json](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakMorphology_1975/root_classifier.json)
is a source-line hint and is **not** a stable id).

## Zalizniak 2004 (*Конспект*)

No paragraph apparatus (confirmed by the book README and the H800 quantifier profile).
G1 adds `zalizniak-2004:<slug>` from the conspectus's own `###` headings, in source order.
Sandhi headings exist in the source and are registered so the validator can refuse them;
Wave 1 topics never publish a Sandhi locus.

## Alignment rule (do not invent equivalence)

- 1975 types I–IV are **not** Whitney present-classes I–X.
- 1975 morphological positions 1/2/3 are **not** Whitney strong/middle/weakest as a
  one-to-one map. Topics that join them must say what each spine actually describes.
- 1978/2004 drop numbered positions and the lettered type calculus. A topic that needs
  those primitives anchors Zalizniak on **1975**, and may add 1978/2004 only for the
  descriptive phenomenon both texts share (grade, series, seṭ, a present class).
- Corpus `dcs_freq == 0` is `not_attested` for the pinned snapshot, never "this form
  is impossible".

## Pinned consumer assets

- WhitneyRoots `roots.csv` slice: `data/grammar_lab/pins/whitneyroots_roots_slice.csv`
  (revision `b453ce0e739c761aa0e32a1df6200d9875b148a5`).
- Type-D fields: [TYPED_LINK_ID_GRAMMAR.md](https://github.com/gasyoun/Uprava/blob/main/TYPED_LINK_ID_GRAMMAR.md)
  via `kosha/scripts/concordance_core.py` `TYPE_D_RECORD_FIELDS`.

_Dr. Mārcis Gasūns_
