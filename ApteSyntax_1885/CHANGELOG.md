# Changelog — ApteSyntax_1885

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-07-16
### Added
- **Treebank drain of the claim backlog (H1059, Opus 4.8 `claude-opus-4-8[1m]`).** New
  [`apte_treebank_stats.py`](apte_treebank_stats.py) (self-tested) measures the syntax backlog
  against DCS's own head/deprel/feat_case dependency slice (223,751 tokens / 29,433 fully-parsed
  sentences). Register **8 → 24 verified** (APT-9..APT-24): **16 TRUE · 6 OVERSTATED · 2
  UNTESTABLE**. Honest split: particle-position and agreement claims drain robustly (subject–verb
  number agreement 98.21% over n=10,672; ca/tu/ced/iva/eva/kila all confirmed never/rarely
  sentence-initial), with **uta the first corpus flag** (23.66% sentence-initial → OVERSTATED,
  vs <1% for the true postpositives; `hi` control 0.77%). Case-government claims split three ways
  — fear/disgust → ablative **confirmed** (APT-16/17), throw → locative and rule/remember →
  genitive **OVERSTATED** (a competing case leads in the corpus), anger/love → dative/locative
  **UNTESTABLE** (<10 case-tagged arguments in the Vedic-skewed slice). Motion-goal measurement
  quantifies the APT-5 flag: accusative goal 85.91% vs non-accusative 14.09% (n=873). Output in
  [`apte_treebank_stats.json`](apte_treebank_stats.json).

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
