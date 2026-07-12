# Changelog

All notable changes to this repo's shared infrastructure (errata system, site
tooling, docs) are documented here. **Book-specific changes now live in each
book's own `<Book>/CHANGELOG.md`** (per-book release scheme, H318):
[ApteSyntax_1885](ApteSyntax_1885/CHANGELOG.md) ·
[BuhlerLeitfaden_1923](BuhlerLeitfaden_1923/CHANGELOG.md) ·
[GasunsDhatu_2014](GasunsDhatu_2014/CHANGELOG.md) ·
[KnauerFrazy_1908](KnauerFrazy_1908/CHANGELOG.md) ·
[KocherginaUchebnik_1998](KocherginaUchebnik_1998/CHANGELOG.md) ·
[ZalizniakKonspekt_2004](ZalizniakKonspekt_2004/CHANGELOG.md) ·
[ZalizniakOcherk_1978](ZalizniakOcherk_1978/CHANGELOG.md) ·
[TolchelnikovTalmud_2026](TolchelnikovTalmud_2026/CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Each book tags/releases independently as `<book-slug>-vX.Y.Z`; this root
changelog tags as `vX.Y.Z`.

## [Unreleased]
### Added
- **Sangram editorial + i18n contract (C4, H633)**: article manifest schema
  ([sangram/editorial/data/article.schema.json](sangram/editorial/data/article.schema.json)),
  fixture, validator (`python scripts/article_validate.py --self-test`) and the
  prose contract page ([sangram/editorial/SANGRAM_EDITORIAL_I18N_CONTRACT.mdx](sangram/editorial/SANGRAM_EDITORIAL_I18N_CONTRACT.mdx)):
  RU-default/EN-translation locales, one canonical SLP1 copy per example
  (IAST/Devanagari derived via sanskrit-util), scientific/pedagogical layers,
  stable `ex:<slug>:<n>` example IDs with locus/translation/provenance,
  public⇒https / internal⇒no-URL evidence rule, leakage = 0.
- **Sangram contract C3 — corpus evidence method** ([`sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CORPUS_EVIDENCE_METHOD.mdx),
  route `/grammars/sangram/corpus-evidence-method`): corpus registry (DCS primary via the
  pinned [`gasyoun/dcs-conllu`](https://github.com/gasyoun/dcs-conllu) snapshot + 5
  supplementary witnesses), rights/liveness/quality gates, the reproducible
  query→sample→validate→claim→examples cycle, quantitative-claim rules П1–П7, and the
  append-only source-defect list Д1–Д8 (H632, Fable 5 `claude-fable-5`).
- **Errata system** (`/errata` skill): every book folder carries an `errata.yml`
  structured source → generated `<Book>/ERRATA.md` + root `ERRATA.md` index via
  `scripts/build_errata.py` (`npm run errata`). Each erratum records who found it
  and when; the generator de-duplicates across errata sheets and cross-references
  the book's own CHANGELOG (`fixed_in` marks typos corrected in the digital edition).
- Errata enter two ways: transcribing a printed errata sheet, **or** an edition
  diff (`build_errata.py diff <Book> <old-ref> [<new-ref>]`) that turns changes
  between two versions of a book's text file into reviewable errata candidates —
  so books with no printed sheet (Kochergina, etc.) still accrue errata over time.
- `README.md` documenting the repo's source editions and scope.
