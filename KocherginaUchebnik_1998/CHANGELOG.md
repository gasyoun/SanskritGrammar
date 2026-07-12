# Changelog — KocherginaUchebnik_1998

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Roadmap for a thin printed companion-methodichka (`METODICHKA_KOCHERGINA_COMPANION_2026.md`
  + its metadoc): five commentary pillars (accuracy, clarity/frequency, errata per edition,
  extra exercises, cross-references), hybrid source-of-truth model (registry data + authored
  prose), and a thin-v1 / comprehensive-v2 split. Consumes the existing 43-claim register
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
