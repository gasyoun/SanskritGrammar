# Changelog — TolchelnikovTalmud_2026

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Standing rule (MG, 08-07-2026): every change to the Talmud — text, data, widgets,
> apparatus — gets an `[Unreleased]` entry here in the same pass.** No silent edits.

## [Unreleased]
### Added
- `data/z_root_map.json` — Whitney-no ↔ [samskrtam.ru/z/](https://samskrtam.ru/z/) verb-id
  join map (876/905 roots matched) + reproducible `tools/build_z_root_map.py` (H329 Phase 1).
- `data/z_reconciliation_report.md` — reconciliation of `/z/`'s Ряд/seṭ vs our derived values
  (H329 Phase 2).
- `/z/` deep-links: «/z/» column in Appendix 1 + `z_url` on the AblautMachine/SetTree widget
  captions, linking each root to its full generated paradigm (H329 Phase 4).

### Notes
- **`/z/` is built from an EARLIER version of the Talmud** (MG, 08-07-2026) — so a share of the
  Ряд/seṭ discrepancies is **authorial version drift** (values Ivan revised between the version
  `/z/` was generated from and the current v2.1.6), not an error on either side. The 70.7 % Ряд
  agreement therefore partly measures version difference, not fidelity.
- Author correction (issue #50): `/z/`'s `0`-variant (`I0/N0/…`) + `L` rows and ṛ→`A1` values are
  `/z/` bugs; the printed manual (руководство) is ground truth for Ряд.

## [0.1.0] - 2026-07-07
### Added
- Docusaurus scaffold + §-concordance skeleton (H242 Phase 0).
- `whitney_talmud.json` enrichment crosswalk (H241 Phase 3).
- 5 interactive widgets (H241 Phase 2).
- `IMPROVEMENT_PLAN.md` — interactive-companion planning note.
- Initial mint: `.mdx` for the dissertation text plus a separate `-uroky`
  (lessons) edition, converted via the `/docx-to-md` skill.
