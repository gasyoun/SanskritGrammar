# Changelog — GasunsDhatu_2014

All notable changes to this book's digital edition are documented here.
Cross-book/infra changes (errata system, site tooling, docs) live in the
[root CHANGELOG](../CHANGELOG.md).

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this book adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.1] - 2026-07-13
### Changed
- **Издательство M03 решено: «Нестор-История»** (MG, 13-07-2026). Закрывает открытый
  `@DECIDE` §6 плана 2-го издания
  ([`revision-2026/BOOK_PLAN.md`](revision-2026/BOOK_PLAN.md)): ЯСК и «Наука» сняты с
  рассмотрения, гриф ИЯз РАН уже был закрыт 10-07-2026. Р6/§6/§7 Фаза 3/§9 обновлены;
  к Фазе 3 остается только операционное (заявка + договор + рецензенты).
  ([H847](https://github.com/gasyoun/Uprava/blob/main/handoffs/H847-Opus_SanskritGrammar_m03-publisher-nestor-istoria-decided_13.07.26.md), Opus 4.8 `claude-opus-4-8`.)

## [0.2.0] - 2026-07-08
### Added
- **2026 print-edition execution (H328).** Executed the
  [`revision-2026/IMPROVEMENT_ROADMAP.md`](revision-2026/IMPROVEMENT_ROADMAP.md)
  per the four author decisions of 07-07-2026: положения re-composed
  (П1/П4 redrafted, П7/П9/П10 demoted to illustrative paragraphs with
  editorial footnotes, П8→П7); Заключение gained a per-положение
  «Верификация положений» draft block (C2); new «Цифровое послесловие 2026»
  section (A39 continuation + «будущая работа → готовый ресурс» map);
  new «Приложения издания 2026» page (6-appendix composition map + Прил. 3
  concordance excerpt over WhitneyRoots/kosha data-v0.1.0); Прил. 2 homonym
  table manually reconstructed from the source `.docx` (rows = group sizes,
  columns = Palsule/EWA); print-layer number fixes (root_oracle 10→8
  dictionaries; 180 176 lemmas re-attributed to VisualDCS; Табл. 2/3 caption;
  §2.6 dataset-change footnote; §3.3.3 L9 gap closed — 933/25,3 %/EWA 50);
  phone replaced with email+ORCID in both article headers (Р4); superseded
  duplicate «Распространение рядов согласных» page removed; 14 new
  `errata.yml` entries (`found_by: H328-review`). PALSULE_AUDIT gained the
  measured step-3 negative result (naive it-stripped join 454/930 — unusable
  as a candidates list without ablaut normalization).

## [0.1.0] - 2026-07-07
### Added
- **2026 print-edition prep (H246).** Conversion cleanup across the
  dissertation + 4 article appendices (~1200 unescapes, typos
  Emeneau/Morgenroth/«Lihusina»→Edgren, Latin-C fixes, `image1.wmf`→PNG, 8
  empty Pandoc headings removed); §2.5/2.6 renumbered (L8); number
  unification with editorial footnotes (Palsule 933/3690, EWA 50, АВ
  coefficient 1.33 — recomputed from the tables' own frequencies, L9); Гл. 2
  title fixed per Волошина (C6); корнеслов/морфемарий defined at first use
  (C5) + морфонология⊃морфонемика note (L10); bibliography split into
  RU/foreign blocks (C13, mechanical part); Гумбольдт ref restored, Потебня
  flagged (C4). **Табл. 5 replaced**: χ² p-values → varga shares by epoch +
  Cramér's V = 0.037 (DCS 2026-03-05, reproducible via
  `revision-2026/varga_shares.py`) per MG Q3; the «Распределение рядов
  согласных» article brought to standalone-appendix form per MG Q2
  (аннотация/method/shares/вывод; 2014 p-table kept as historical record);
  «Список файлов» reduced to an annotated supplementary note with dead-link
  markers. New «Состояние вопроса на 2026 год» section (590/935 Whitney
  roots attested in DCS; digital crosswalks; vidyut dhātupāṭha; kosha
  data-v0.1.0). `errata.yml` seeded with 51 entries
  (`found_by: H246-review`); `revision-2026/` working notes: П1/П4/П7/П9/П10
  draft rewrites (await author sign-off) + Palsule-vs-vidyut audit (`4añc`
  confirmed recoverable — 5 añc-family dhātus in the Paninian dhātupāṭha;
  `ast` present too, refining Крылов's 2014 remark).
- RWS style report (`feat(gasuns-dhatu): add RWS style report`).
- Initial mint: dissertation + article appendices, converted to `.mdx` via
  the `/docx-to-md` skill.
