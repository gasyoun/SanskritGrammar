# Changelog — KocherginaUchebnik_1998

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-07-12
### Added
- **Claim register drained to completion — 43 → 234 verified claims (H797).** The full
  223-candidate harvest backlog ([`claims_harvest.yml`](claims_harvest.yml)) was verdicted on
  both axes and promoted into [`claims.yml`](claims.yml) (HK-1..HK-233) in seven lesson-ordered
  batches: 210 TRUE · 11 OVERSTATED · 1 FALSE · 12 UNTESTABLE, with 11 M.G. frequency footnotes.
  The register now covers all 40 Занятия (phonology → sandhi → declension → conjugation → aorist →
  compounds → prefixation → adverbs). The harvest backlog is now empty (`candidates: []`).
- **`verify_claims_dcs.py` extended with reproducible backlog metrics** — a vowel census over the
  full DCS-2021 running text (0.csv: a+ā = 65.8% of vowels; ṛ 199,930 vs ṝ 1,588 / ḷ 0 / ḹ 0),
  verb-class share (thematic I/IV/VI/X = 70.2% of present-system tokens; class II frozen at
  154,301), a past-tense competition (imperfect 47,554 · perfect 61,986 · aorist 2,452) and the
  case-slot token distribution — so every M.G. footnote number is re-runnable. The seven new
  DCS-computed footnotes (N.sg visarga, Acc.sg anusvāra, ṛ dominance, vowel-length, class-II
  frozenness, injunctive rarity 0.30%) all reproduce from the committed corpus.
- Roadmap for a thin printed companion-methodichka (`METODICHKA_KOCHERGINA_COMPANION_2026.md`
  + its metadoc): five commentary pillars (accuracy, clarity/frequency, errata per edition,
  extra exercises, cross-references), hybrid source-of-truth model (registry data + authored
  prose), and a thin-v1 / comprehensive-v2 split. Consumes the now-234-claim register
  and errata system rather than rebuilding. Decisions A–D locked with MG; first execution
  slice minted as H807 (Fable).

## [0.2.0] - 2026-07-12
### Added
- **Claim-verification register (H768)** — `claims.yml` → generated `CLAIMS_VERIFIED.md`
  (via `scripts/build_claims.py`, `npm run claims`), a register *distinct* from `errata.yml`:
  it catalogues the textbook's *falsifiable grammatical assertions* and grades each on two
  axes — **fact** (true vs. the DCS-2021 corpus + Whitney 1889, with the actual number) and
  **pedagogy** (is the presentation defensible). Full-textbook sweep of all 40 Занятия:
  **43 claims** (verb-system seeds HK-1..HK-6 + harvest HK-7..HK-42) — 28 TRUE, 11 OVERSTATED,
  1 FALSE, 3 UNTESTABLE; 16 flagged for an overreach or presentation issue.
- **Reproducible corpus numbers** — `verify_claims_dcs.py` recomputes every DCS figure
  (imperative-by-person, conditional/precative rarity, PPP -ta/-na split, future allomorphy,
  aorist/gerundive share) into `claims_dcs_stats.json`.
- **Reading-site overlay** — `<KocherginaClaims/>` (`src/components/KocherginaClaims.jsx`) +
  `CLAIMS_OVERLAY.mdx` badge the two-axis verification over the reading site (Kochergina 1998
  stays in-copyright — verification metadata only, no text re-release).

## [0.1.0] - 2026-07-07
### Added
- Converted `.docx` → `.md`/`.mdx` via the `/docx-to-md` skill (Pandoc GFM with
  grid tables — 124 grid tables, the most of any book here — images extracted
  to `Kochergina_unicode_media/`, UTF-8 Devanagari intact).
- Initial mint: reprint source edition (*Учебник санскрита*, 1998).
