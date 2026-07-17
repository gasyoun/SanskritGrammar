# Changelog — TolchelnikovTalmud_2026

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

> **Standing rule (MG, 08-07-2026): every change to the Talmud — text, data, widgets,
> apparatus — gets an `[Unreleased]` entry here in the same pass.** No silent edits.

## [Unreleased]

## [0.3.0] - 2026-07-17
### Added
- **Join provenance on every `whitney_talmud.json` record — `talmud_root` · `talmud_ref` · `talmud_match` (H1065).** Consumers could see *that* a Ряд/Тип/seṭ was `manual` but not **which** Приложение-1 entry it came from or how it was bound, so a downstream feed that wanted the audit trail had to re-join the catalog itself. [WhitneyRoots `alternation_type.csv`](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/alternation_type.csv) did exactly that and its independent join **smeared 16 authorial values across homonyms the author never catalogued** — his «2 iṣ» bound onto BOTH `iṣ¹` and `iṣ²`, his single «1 śṛ» onto `śṛ¹`/`śṛ²`/`śṛ³` — each row still claiming `grade_confidence=authorial`. Emitting the binding makes the canonical join auditable in place, so downstream **reads** it instead of repeating it. Additive fields only; `widget_roots.json` regenerates with no diff; `npm run build` green. (Opus 4.8 `claude-opus-4-8`)
### Fixed
- **Multi-spelling catalog rows bound only ONE Whitney record — 57 roots, `gach` (DCS rank 5) among them, sat `tip`/`ryad`/`seṭ` = null although the author had classified them ([H1065](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1065-Opus_WhitneyRoots_alternation-type-induction-nonpaninian_16.07.26.md)).** `build_manual_index()` in [`tools/build_whitney_talmud.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/build_whitney_talmud.py) iterated a catalog row's «Список Уитни» spellings but `return`ed on the first hit, so an entry cross-referenced under two of Whitney's citation forms — `GM̥` «gam, gach», `YM̥` «yam, yach», `ŚĪØ̄` «śyā, śī» — bound the primary form and silently dropped the alternate. Col4 is the author's own concordance (ruling #5): one morpheme under two citation forms, so the alternate is **authorial data, not an inference**. Added a purely additive `spelling-alt` pass — manual overlay **730 → 787 records** (`tip` null 200 → 143), verified against the prior build as **57 filled / 0 changed / 0 lost** across `tip`/`ryad`/`set`/`pada`. Homonym-safe by construction, mirroring the pass-1 `root-uniq`/`root-none` discipline: where the author indexed the entry («1 paś», «1 stu»), the Whitney homonym must agree, so `paś²`/`stu²`/`pā³` stay null pending his ruling rather than inherit a neighbouring homonym's Тип ([issue #50](https://github.com/gasyoun/SanskritGrammar/issues/50) precedent); and where he did **not** index it, the alternate spelling must resolve to a single Whitney record — «vakṣ, ukṣ» is un-indexed while Whitney has `ukṣ¹` **and** `ukṣ²`, so binding both would assert he classified two morphemes where he catalogued one, and the pass abstains. Audited: **zero** authorial entries bound to several homonyms of one spelling. Visible in [Приложение 1](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/talmud-appendix-1.mdx): `gach` renders `M₁ | I | veṭ` instead of `— | — | —`, matching its `gam` twin. Regenerated [`whitney_talmud.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/whitney_talmud.json), [`widget_roots.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/widget_roots.json) (ablaut examples 45 → 46) and the appendix; [schema doc](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/whitney_talmud.schema.md) documents `spelling-alt` + the homonym abstention. Found while checking prior art for H1065, which had assumed this table did not exist. (Opus 4.8 `claude-opus-4-8`)

## [0.2.5] - 2026-07-16
### Fixed
- **Поз.1↔3 / grade-mapping inversion, plus a Тип↔seṭ code mix-up (H995 follow-up finding).** [`talmud-02-cheredovanie.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/talmud-02-cheredovanie.mdx), [`onramp/step-2-pozicia-i-tip.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/onramp/step-2-pozicia-i-tip.mdx), and the [`AblautMachine`](https://github.com/gasyoun/SanskritGrammar/blob/main/src/components/talmud/AblautMachine.jsx) free-exploration caption all stated Поз.1→Вриддхи/Поз.3→Слабая — the manual's own Table 5 says the opposite (Поз.1→Слабая, Поз.3→Вриддхи, consistently across all four types). Separately, the same pages labeled the ablaut-Тип rows `s`/`a`/`v`/`v1`–`v4` — those are actually the manual's Table 8 **seṭ/aniṭ/veṭ** codes, a different grammatical dimension entirely; the real Тип labels (Table 5) are `I`/`II`/`III`/`IV`. Rewrote both pages + the widget caption against Table 5 verbatim, added a clarifying note distinguishing Тип from seṭ. Also found and fixed the same confusion baked into the data pipeline: [`tools/build_whitney_talmud.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/tools/build_whitney_talmud.py)'s `tip_default` fallback was `"s"` (a seṭ code, outside the `tip` field's own `I`/`II`/`III`/`IV`/null value space) — changed to `"I"` (Table 5's full-range/default type) and regenerated [`data/whitney_talmud.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/whitney_talmud.json) (930 records). Confirmed **no functional impact** — `tip_default` has zero downstream consumers in the widget code, and `AblautMachine`'s interactive grade/series toggle was already independent of the buggy prose (only the "no root selected" caption text was wrong). `npm run build` green, `widget_roots.json` regenerated with no diff (as expected). (Sonnet 5 `claude-sonnet-5`)

## [0.2.4] - 2026-07-15
### Changed
- **Morphoclass crosswalk is now four-way (+1978)** — the 1978 columns (ряд+индекс, открытость, полноизменяемость per Ocherk's own §§66-67 rules and named lists) are merged INTO [`data/morphoclass_crosswalk_1975_2014_2026.csv`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv) itself (876 rows × 5 new columns; filename kept — the PhD text and several memos cite it). Maintainer script: [`ZalizniakOcherk_1978/build_1978_crosswalk.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/build_1978_crosswalk.py) (idempotent, 15/15 validation); the former companion `crosswalk_1978.csv` is retired. Cross-layer fact now IN the data: 1978 and 2026 disagree on open-M/N indices (jan = N₂ per §66 vs N₁ in ryad_derived). ([H978](https://github.com/gasyoun/Uprava/blob/main/handoffs/H978-Fable_SanskritGrammar_1978-crosswalk-column-unblock-och21-23_15.07.26.md)) (Fable 5 `claude-fable-5`)

## [0.2.3] - 2026-07-15
### Added
- **Russian folder README** — [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/README.md): по-русски — паспорт живой книги (порождающая морфонология Ряд/Тип/seṭ, наследование модели Зализняка 1975, публикация Ауровиль-2024), состав папки (Talmud-2.1.6 + 14 поглавных страниц с AblautMachine/SandhiCollider, onramp H915, издательский хаб papers/ c A60/A62/A63/WSC-2027, аппарат со standing rule автора), и роль в программе проверки утверждений — **опора, не мишень**: авторитет морфокласса корня в D-B, несущая ось seṭ/aniṭ за флагманским числом -iṣya 56,8 %, приёмник подмножества OVERSTATED/FALSE в A60. Ряд README: [Кочергина](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/README.md) · [Бюлер](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/README.md) · [Кнауэр](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/README.md) · Зализняк×2 · [Уитни](https://github.com/gasyoun/SanskritGrammar/blob/main/WhitneyGrammar_1889/README.md). (Fable 5 `claude-fable-5`)

## [0.2.2] - 2026-07-14
### Fixed
- **`papers/` index: de-linked the un-published source binaries.** The links to the Auroville /
  Fortunatovskiye / Dubyanskiye `.pptx`/`.pdf` slide sources were broken *by design* — those source
  files are deliberately gitignored (`.gitignore` H411 "derived-edition-only" policy), so they aren't
  in the repo and can't resolve. Converted the 6 dead links to plain filenames (kept a source-only
  note). `npm run build` now reports **zero broken links** site-wide (the separate broken-*anchor*
  items on the OCR'd book pages are unaffected). (Opus 4.8 `claude-opus-4-8`.)

## [0.2.1] - 2026-07-14
### Fixed
- **`papers/Fortunatovskiye_2023/` landing page** — added a hand-authored `index.mdx` (matching the
  Desnickaya_2020 / Kulikov_2025 pattern), so the folder route resolves. The two `../Fortunatovskiye_2023/`
  cross-links from those sibling pages were broken (the folder had only a `.docx`-generated paper page,
  no index); `npm run build` confirms both now resolve, with no new broken links. (Opus 4.8 `claude-opus-4-8`.)

## [0.2.0] - 2026-07-14
### Added
- **`papers/`** — Tolchelnikov's 2023–2025 companion conference papers/talks (Auroville,
  Fortunatovskiye, Dubyanskiye, plus Desnickaya/Kulikov's independent commentary) published
  as `.mdx` in the Docusaurus site, with a `Papers & talks (Tolchelnikov)` sidebar category
  (`_category_.json` per folder) kept separate from the main chapter list, and a
  [`papers/index.mdx`](papers/index.mdx) cross-linked with
  [`ZALIZNIAK_1975_1978_2004_COMPARISON.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZALIZNIAK_1975_1978_2004_COMPARISON.md) (H411).
- **`data/talmud_appendix1.json`** — the author's own Приложение 1 verb-root catalog (745 roots),
  parsed **verbatim** from the authoritative manual `Talmud-2.1.6.mdx` by new
  `tools/parse_appendix1.py`. Carries per root the author's Ряд, Тип (`I`–`IV`), seṭ
  (`s`/`a`/`v1`…`v4`), pada and Whitney-nomenclature reference — the **source of truth** for these
  values per the issue-#50 ruling (H329 Phase 3).
- `data/manual_reconciliation_report.md` — audit trail: how the author's catalog covers the
  Whitney spine (730/745 rows → 730 Whitney roots) and how far the retired derived Ряд/seṭ
  disagreed with him (Ряд 75.6 %, i.e. **178 roots the derivation got wrong**).
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
- **Author ruling (I. E. Tolchelnikov, issue #50, 08-07-2026):** Ряд, seṭ and Whitney refs are taken
  from the **latest manual = `Talmud-2.1.6.mdx`** (the current authoritative edition), not `/z/` and
  not our derivation; un-indexed rows stay un-indexed; **no methodology footnote** (FN-0001/0002
  marked `rejected`). `/z/` is kept only as the paradigm deep-link (outdated snapshot, still useful).

### Changed
- **`data/whitney_talmud.json`: Ряд/Тип/seṭ now sourced from the manual, not derived** (H329 Phase 3).
  `tools/build_whitney_talmud.py` overlays the author's Приложение 1 catalog onto the Whitney spine
  (`ryad_source`/`tip_source`/`set_source` = `"manual"`); the vowel-derived Ряд and p.p.p.-inferred
  seṭ are **no longer emitted** (derivation code retained only for the reconciliation audit). New
  fields `tip`, `tip_source`, `set_code`, `pada`; **dropped** `ryad_confidence`, `ryad_note`,
  `set_confidence`. 730 roots carry the author's Ряд, 200 are `null` (not in his catalog); 721 carry
  a manual seṭ. Тип is now populated (previously always `null`).
- Приложение 1 render (`talmud-appendix-1.mdx`, `tools/render_appendix1.py`): columns `Ряд*`/`seṭ*` →
  `Ряд`/`Тип`/`seṭ` (no `*`); provenance note rewritten to cite the manual; the «Структура словарной
  статьи» legend corrected — Тип is `I`–`IV` (Table 5), the `s`/`a`/`v` codes are the seṭ-parameter
  (Table 8), which the prior draft had conflated.
- Widget feed (`data/widget_roots.json`, `tools/build_widget_data.py`): Ряд/seṭ relabelled as the
  author's manual values; `ryad_confidence`/`set_confidence` projections dropped, `tip`/`set_code`
  added; ablaut examples now restricted to roots the author gives a series for.
- `footnote-proposals/proposals.yml`: FN-0001/0002 (derived Ряд/seṭ methodology notes) → `status: rejected`
  per the author's issue-#50 ruling ("примечание не нужно").

## [0.1.0] - 2026-07-07
### Added
- Docusaurus scaffold + §-concordance skeleton (H242 Phase 0).
- `whitney_talmud.json` enrichment crosswalk (H241 Phase 3).
- 5 interactive widgets (H241 Phase 2).
- `IMPROVEMENT_PLAN.md` — interactive-companion planning note.
- Initial mint: `.mdx` for the dissertation text plus a separate `-uroky`
  (lessons) edition, converted via the `/docx-to-md` skill.
