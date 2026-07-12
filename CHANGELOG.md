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

## [0.3.0] - 2026-07-12
### Added
- **WSC-2027 CDSL report — deep remake** (H795, Fable 5 `claude-fable-5`):
  [`TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/`](TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/) —
  13 `.mdx` chapters remaking the WSC-2025-rejected "Report on Cologne Digital
  Sanskrit Lexicon Project" for the 20th World Sanskrit Conference (Mumbai,
  December 2027): formal register per the four Kathmandu reviews, every
  quantitative claim tied to a committed dataset, Peter Scharf's review
  incorporated (Sanskrit Library co-history, TEI, morphid coordination,
  licence status), team history updated through Jim Funderburk's June-2026
  retirement (cited to the recorded volunteer call), full bibliography +
  abbreviations appendix. Provenance and residual pre-submission items in the
  folder's [`README.mdx`](TolchelnikovTalmud_2026/papers/MumbaiWSC_2027/README.mdx).

## [0.2.0] - 2026-07-12
### Added
- **Атлас B5 — зависимости репозиториев** (`/sangram/atlas/dependencies`, H620,
  Fable 5 `claude-fable-5`): пять видов ребер публичного interlinks-экспорта
  (feeds · consumes · vendors · produces · cites) различимы цветом **и** текстовым
  бейджем, направление и канон/копия по каждому виду, таблица всех вендоренных
  копий организации, поиск по репозиториям/активам/контрагентам, программные
  группы census через новое опциональное поле `programme_ru` на `repo`-узлах
  (контракт данных 1.0.0 → **1.1.0**, append-only), полное покрытие census
  (75 репозиториев / 67 с ребрами / 8 изолятов пунктиром), controlled-mode на
  едином маршруте (`sangram/atlas/dependencies.mdx` +
  `src/components/AtlasDependencies/`). В источнике interlinks исправлены два
  инвертированных `vendors`-ребра (vidyut); bundle пересобран, leakage = 0.
- **Атлас B3 — переиспользование готовых активов** (`/sangram/atlas/reuse`, H630,
  Fable 5 `claude-fable-5`): владелец → актив → потребитель по 18 каноническим
  семействам с ярусами прав и запретами пересоздания
  (`sangram/atlas/reuse.mdx` + `src/components/AtlasReuseView/`).
- **Все пять представлений атласа живые на едином маршруте**
  (`/sangram/atlas/unified`): wave B серии MEGABOOK × Sangram (B1–B6) закрыта —
  attention · reuse · value-chain · dependencies · provenance подключены в
  `VIEW_REGISTRY`, выбранный узел сохраняется при переключении представлений.

## [0.1.0] - 2026-07-12
### Added
- **GrammarRelations — карта связей грамматик** ([GrammarRelations/grammar-relations-map.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GrammarRelations/grammar-relations-map.mdx),
  route `/grammars/GrammarRelations/grammar-relations-map`): читательская страница о том,
  как связаны 10 оцифрованных грамматик — генеалогия учебной линии (τ из S1), проверенная
  по тексту зависимость Очерк-1978↔Кочергина-1998, линия Зализняка 1975/1978/2004 и ветви
  Гасунс/Толчельников, карта тем, трудность подачи и совместимость для студента. Новый
  скрипт [`scripts/grammar_relations_stats.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/grammar_relations_stats.py)
  (SG-H2 подтверждена: медианный сдвиг +0.142, p≈2×10⁻⁵; SG-H9 опровергнута на
  символьном прокси) + результаты в
  [`scripts/data/grammar_relations_stats.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/grammar_relations_stats.json)
  (H786, Fable 5 `claude-fable-5`).
- **Атлас B4 — интерактивная цепочка ценности** (`/sangram/atlas/value-chain`,
  H627, Fable 5 `claude-fable-5`): три селектируемых типизированных контура
  (исследовательский · образовательный · агентный) над 7 value-ступенями и
  10 ребрами bundle, роли источник/данные/продукт/отдача/мультипликатор без
  смешения, доказуемость каждого звена ребром bundle + свидетельством,
  Mermaid-объяснение с accTitle/accDescr и табличный эквивалент
  (`sangram/atlas/value-chain.mdx` + `src/components/AtlasValueChain/`).
- **Sangram contract C2 — article TOC network** ([`sangram/toc/SANGRAM_TOC_NETWORK.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/toc/SANGRAM_TOC_NETWORK.mdx),
  route `/grammars/sangram/toc-network-c2`): append-only registry
  [`articles.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/toc/data/articles.json)
  of 93 core articles across the 7 charter domains (PH 10 · WF 11 · MO 32 · SE 15 ·
  SY 14 · DI 6 · VA 5) — stable `SG-<domain>-<NNN>` IDs, 117-edge acyclic prerequisite
  graph, DCS query sketches (6-prefix grammar), curated witnesses from the repo's 10
  grammars plus a derived Whitney-chapter coverage layer; all 33 C6 programme slots
  mapped via `c6_slots`. Generator `scripts/toc_build_pages.py` (overview + 7 domain
  pages with Mermaid prerequisite graphs) and validator `scripts/toc_validate.py`
  (17 check classes incl. H540 form-class cross-check and `--check` page sync)
  (H631, Fable 5 `claude-fable-5`).
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
