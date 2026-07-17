# Changelog — WhitneyGrammar_1889

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes live in the [root CHANGELOG](../CHANGELOG.md). The raw `.mdx` edition
and the subject concordance predate this changelog (H325/H427).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.4.0] - 2026-07-17
### Changed
- **WH-2 aorist number refreshed to the feat_formation count (H1137, Opus 4.8
  `claude-opus-4-8[1m]`).** WH-2 reused Kochergina HK-1's old figure (2,452 / 0.31%), which was
  refreshed in H1136 — so WH-2 was left stale and internally inconsistent with this register's own
  WH-15 (which already cites 12,054). Refreshed to **12,054 tokens = 2.30% of finite verbal forms**
  (DCS `feat_formation`, via `whitney_aorist_tagger.py`), matching HK-1, APT-31, and WH-15. Verdict
  unchanged (TRUE — the aorist is marginal either way); completes the aorist-number refresh across
  every register that cites it.

## [0.3.0] - 2026-07-17
### Added
- **Aorist-per-text tagger — closes WH-15 (H1134, Opus 4.8 `claude-opus-4-8[1m]`).** New
  self-tested [`whitney_aorist_tagger.py`](whitney_aorist_tagger.py) resolves the one UNTESTABLE
  claim. The sqlite has no aorist TENSE value, but it tags the aorist FORMATION: within
  `feat_tense='Past'`, `feat_formation` cleanly separates the seven aorist classes
  (root/them/s/is/red/sa/sis) from the perfect (peri / None). With that, Whitney's §826 aorist
  hand-count of **Manu (7) reproduces as DCS 6** — the same near-exact small-text match as the
  conditional (WH-13) and precative (WH-14); Hitopadeśa 4 vs his 8; MBh/Rāmāyaṇa dwarf his figures
  because he counted only sub-portions (the Nala episode; Rāmāyaṇa book 1).
### Changed
- **WH-15 UNTESTABLE → TRUE.** Register stays 15 verified; tally moves to **14 TRUE · 1
  OVERSTATED · 0 UNTESTABLE** — every drainable Whitney claim now confirmed.
- **Side finding:** the true aorist count is **12,054 tokens (1.2% of verbal)**, not the 2,452 /
  0.31% the earlier form-set / DCS-2021 tense-code method gave (it had missed the numerous root
  and thematic aorists). The "classically infrequent" verdict (WH-2) holds under either figure.

## [0.2.0] - 2026-07-17
### Added
- **Frequency-register drain with two instruments (H1107, Opus 4.8 `claude-opus-4-8[1m]`).**
  Register **10 → 15 verified** (WH-11..15). Two new self-contained instruments:
  [`whitney_root_count.py`](whitney_root_count.py) joins Whitney's per-present-class ROOT counts
  to his own 930-root [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots) catalog (his
  class-size claims count roots, not tokens), and [`whitney_per_text_counts.py`](whitney_per_text_counts.py)
  reproduces his per-text HAND-COUNTS (conditional/precative directly via `feat_mood`; aorist
  bridged via a 690-form set from `15.csv`). Tally **13 TRUE · 1 OVERSTATED · 1 UNTESTABLE**.
### Notes
- **Two showcase results.** (1) Whitney's 1889 running-text root counts per present-class match
  his own enumerated catalog almost exactly — the **tan-class (8) and nu-class (50) to the
  number**, nasal 29≈30, div 137≈130 — and class I is the largest at 56% of roots (WH-11/12).
  (2) His hand-counts of the rarest forms reproduce **to the token**: he counted **zero
  conditionals in the Hitopadeśa and exactly one in Manu** in 1889, and DCS-2021 gives 0 and 1
  (WH-13); the precative in Manu is likewise exactly 1 (WH-14). Only the aorist §826 per-text
  hand-count (WH-15) stays UNTESTABLE — the sqlite has no aorist tag, so form-set matching
  undercounts. A 137-year-old philologist's hand-counting, validated against a 5.7M-token corpus.

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
