# Changelog — ApteSyntax_1885

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2026-07-16
### Added
- **Claim-verification register seed (H1055, Opus 4.8 `claude-opus-4-8[1m]`).** Ported the
  two-axis (fact × pedagogy) claim pipeline to Apte — the fifth book after Kochergina, Bühler
  and Zaliznyak ×2, and the **first syntax manual** in the register. New
  [`claims.yml`](claims.yml) (APT-1..APT-8: **7 TRUE · 1 OVERSTATED**) → generated
  [`CLAIMS_VERIFIED.md`](CLAIMS_VERIFIED.md) + `claims.json` via `npm run claims`; new
  [`claims_harvest.yml`](claims_harvest.yml) — a 79-candidate backlog (lessons 1–25 from a
  5-reader parallel harvest; lessons 26–30 logged as a coverage gap). Genre-checked first: Apte
  is syntax-weighted, so most claims are case-government/agreement rules testable against the
  DCS treebank layer, not surface frequency — flagged honestly, not forced. Three seed claims
  REUSE ground truth from sibling books (APT-6 = Bühler's 14:1 periphrastic/simple-future ratio;
  APT-3/APT-8 = the enclitic-position fact behind Kochergina HK-10), yielding two direct
  cross-book calibration contrasts (Apte's honest quantifiers where Kochergina/Bühler overreach).

## [0.1.0] - 2026-07-07
### Added
- Initial mint: reprint source scan/edition (`.doc`, `.docx`) plus faithful `.mdx`
  extraction (8 grid tables preserved) via the `/docx-to-md` skill.
