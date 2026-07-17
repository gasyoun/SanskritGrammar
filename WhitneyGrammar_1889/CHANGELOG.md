# Changelog — WhitneyGrammar_1889

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes live in the [root CHANGELOG](../CHANGELOG.md). The raw `.mdx` edition
and the subject concordance predate this changelog (H325/H427).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-07-17
### Added
- **Frequency-claim register seed (H1101, Opus 4.8 `claude-opus-4-8[1m]`).** The two-axis claim
  pipeline's **sixth book and reference-grade endpoint**, with a methodological inversion: where
  every other book (Kochergina, Bühler, Zaliznyak ×2, Apte) is judged *against* Whitney, here
  **Whitney is the target** — his own falsifiable quantitative claims (frequencies, rarity, class
  sizes, hand-counts) verified against DCS-2021 + internal consistency, never against a higher
  authority. New [`claims.yml`](claims.yml) (WH-1..WH-10: **9 TRUE · 1 OVERSTATED**) → generated
  [`CLAIMS_VERIFIED.md`](CLAIMS_VERIFIED.md) + `claims.json`; [`claims_harvest.yml`](claims_harvest.yml)
  — a 74-candidate backlog (4-reader harvest over aorist/future, present-system, conjugation/
  perfect, declension); numbers reproduced by [`verify_whitney_freq.py`](verify_whitney_freq.py).
  Three seed claims reuse ground truth from sibling books (aorist %, class-I share, perfect-vs-
  imperfect). Finding: the gold-standard grammar's frequency architecture reproduces in the modern
  corpus almost perfectly — present > all other verb-systems (2.07:1), a-stems the majority of
  nominal stems (61.1%), the "extremely common" roots (kṛ/dā/brū) topping the frequency list — the
  best calibration in the programme. The single flag is Whitney's own hedged "perfect on the whole
  less common than the imperfect" (WH-4), which the DCS aggregate flips (perfect 61,986 > imperfect
  47,554) — OVERSTATED-in-aggregate, half-anticipated by his "varies by author" hedge.
