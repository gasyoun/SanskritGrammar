_Created: 10-09-2026 · Last updated: 10-09-2026_

# Dark_library syntax (Speyer/Apte/Tubb) — text-layer verdict + claims-harvest queue (H4483)

Source: yadisk folder "Санскритский синтаксис" (Speyer 1886, Apte *Composition* 1885,
Tubb–Boose 2007, Leitan 2022, plus the На иностранных/Общий синтаксис subdirs). The raw
PDFs and their machine-extracted `.md` text layers already live in
[SanskritLexicography](https://github.com/gasyoun/SanskritLexicography) under
`literature/` (root + `На иностранных/`) and `literature/md/` (guarded main-tree repo —
**read-only** from this pass; raw PDFs stay on that disk, nothing copied here). This repo
(SanskritGrammar) hosts the claims-harvest queue derived from that text.

## Text-layer verdict per book

| Book | Author · year | Source (SanskritLexicography, `master`) | Text-layer verdict |
|---|---|---|---|
| *Sanskrit Syntax* | J.S. Speyer · 1886 | [literature/Speyer-Syntax1886.pdf](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/Speyer-Syntax1886.pdf) → [literature/md/Speyer-Syntax1886.md](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/md/Speyer-Syntax1886.md) | **Usable.** 800 KB / 32 577 lines. Real, minable prose body from page 4 on; scattered pages (esp. the Delhi-reprint colophon, p.3) are OCR mush where running headers/page numbers interleave with body text. No `-OCR` suffix — this is the plain extraction, not the flagged-noisy variant. Public domain (1886, author d. 1934 — safely PD by any jurisdiction's term). **Picked first per mission** (public domain, no permission gate). |
| *The Student's Guide to Sanskrit Composition* (*Sanskrit Syntax*) | V.S. Apte · 1885 | [literature/Apte-Composition1885.pdf](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/Apte-Composition1885.pdf) → [literature/md/Apte-Composition1885.md](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/md/Apte-Composition1885.md) | **Usable — already harvested.** 623 KB / 20 648 lines, legible native/OCR text (period spacing artifacts: "th.at", "a.dditions"). This is the same book already worked in this repo as [`ApteSyntax_1885/`](https://github.com/gasyoun/SanskritGrammar/tree/main/ApteSyntax_1885) — full `.mdx`, `claims.yml` (39 promoted claims APT-1..APT-39) and `claims_harvest.yml` (115 candidates) already exist there. **No new harvest done this pass** — re-harvesting would duplicate existing APT-H-* work; see [`ApteSyntax_1885/claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/claims_harvest.yml). |
| *Scholastic Sanskrit: A Handbook for Students* | Gary Tubb & Emery Boose · 2007 | [literature/Tubb-ScholasticSans-2007.pdf](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/Tubb-ScholasticSans-2007.pdf) → [literature/md/Tubb-ScholasticSans-2007.md](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/md/Tubb-ScholasticSans-2007.md) | **Usable, text layer clean.** 560 KB / 11 678 lines, modern typeset PDF, minimal OCR noise. **Not public domain** (AIBS/Columbia, 2007, in-copyright) — no claims harvested from it this pass; a future harvest needs a permission/fair-use check first (cf. [H734 literature-copyright-triage](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H734-Fable_SanskritLexicography_literature-copyright-triage_11.07.26.md)). |
| Leitan, "Шастрический санскрит: стратегии традиционного комментария (1)" | Edgar Leitan · 2022 | [literature/Leitan_Sintaksis 20.2_11.09.2022.pdf](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/Leitan_Sintaksis%2020.2_11.09.2022.pdf) → [literature/md/Leitan_Sintaksis 20.2_11.09.2022.md](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/md/Leitan_Sintaksis%2020.2_11.09.2022.md) | **Usable, clean.** 10 KB / 83 lines — a short lecture/article on commentary strategy (pañcalakṣaṇam), not a syntax grammar in Speyer/Apte's sense (no case-government rules to harvest — it is metalanguage about *how commentaries* describe syntax, not a rule inventory itself). No claims harvested — out of scope by genre, not by OCR quality. |
| *Vedische und Sanskrit-Syntax* (1896 ed., 1974 photo-reprint) | J.S. Speyer · 1895/1896 | [literature/На иностранных/Speyer-Syntax1895.pdf](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/%D0%9D%D0%B0%20%D0%B8%D0%BD%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%BD%D1%8B%D1%85/Speyer-Syntax1895.pdf) → [literature/md/На иностранных/Speyer-Syntax1895.md](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/md/%D0%9D%D0%B0%20%D0%B8%D0%BD%D0%BE%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%BD%D1%8B%D1%85/Speyer-Syntax1895.md) | **Usable, but noisy — this is the `-OCR`-class file.** [`literature/md/INDEX.md`](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/md/INDEX.md) (generated 26-06-2026) still logs it "⚠ blocked — needs OCR (~215 chars, no body)" — **that verdict is stale**: the `.md` now carries a 352 KB / 6091-line body headed `**Machine OCR** (RapidOCR/ONNX, 200 dpi, 54 pp) of the previously un-OCR'd image PDF`, with the file's own caveat that macrons/diacritics are lost (ā ū ṛ ś ṣ ṇ → a u r s s n) and Devanagari is noisy. German-language edition; not harvested this pass (Speyer 1886 English edition covers the same author's syntax claims and is far cleaner to mine). **Flag for a SanskritLexicography-side INDEX.md refresh** — out of scope here (guarded main-tree repo, not touched this pass). |
| Meenakshi, *Sanskrit Syntax* · 1983 (adjacent "Вспомогательное" find, not in the mission list) | — | [literature/md/Вспомогательное/Meenakshi-Syntax1983.md](https://github.com/gasyoun/SanskritLexicography/blob/master/literature/md/%D0%92%D1%81%D0%BF%D0%BE%D0%BC%D0%BE%D0%B3%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B5/Meenakshi-Syntax1983.md) | **Blocked — no body** (~222 chars, title block only per INDEX.md). Noted here only because it turned up adjacent to the same OCR sweep; not part of this handoff's mission list and not harvested. |

## What was actually harvested this pass

Per mission ("pick Speyer first — public domain"): **Speyer 1886** is the only book newly
harvested. Apte is already covered by the existing `ApteSyntax_1886` harvest; Tubb is
in-copyright (no clearance to mine text this pass); Leitan is off-genre (no rule
inventory to harvest); Speyer 1895 duplicates the 1886 author's syntax and is far
noisier OCR.

**40 candidate claims** harvested into
[`../SpeyerSyntax_1886/claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/SpeyerSyntax_1886/claims_harvest.yml)
(candidates `SPE-H-1`..`SPE-H-40`), covering: passive/impersonal constructions, subject/
agent ellipsis, gender-number concord, case government (instrumental, ablative,
genitive, dative-of-purpose via infinitive), compounding rules (ṣaṣṭhī-tatpuruṣa
exceptions, bahuvrīhi-mātra, fossilized case-endings), pronouns and particles (ātman,
address titles, idam/etad, indefinite ka-, na, hi), tense/mood (imperfect scope,
conditional protasis/apodosis), participles/absolutive/infinitive, and sentence-level
word order (interrogatives, relative-correlative direction, negative asyndeton).

None are promoted to a verified `claims.yml` this pass — per the CLAIMS_MAINTENANCE
runbook ([docs/runbooks/CLAIMS_MAINTENANCE.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/runbooks/CLAIMS_MAINTENANCE.md))
promotion requires a verification pass (reference-grammar cross-check or a
`verify_claims_dcs.py`/treebank run), which is explicitly **out of scope this pass**
("corpus-probe design notes only — no probes"). No `claims.yml` was created for
`SpeyerSyntax_1886/`, so `scripts/check_claims_consistency.py` and
`scripts/claims_schema_validate.py` (which both glob only `*/claims.yml`) are
unaffected by this commit — CI stays green with zero new surface.

## Corpus-probe design notes (no probes run this pass)

Each harvested candidate carries a `testability` tag naming the instrument that would
verify it, reusing the taxonomy already established in
[`ApteSyntax_1885/claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/ApteSyntax_1885/claims_harvest.yml):

| Tag | What it names | Existing instrument to reuse (not run this pass) |
|---|---|---|
| `syntax-treebank` | Case-government, agreement, word-order and particle-position claims — needs head/deprel-annotated corpus counts | [`ZalizniakOcherk_1978/treebank_syntax_stats.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/treebank_syntax_stats.py) pattern (DCS treebank query by relation/case), or `ApteSyntax_1885/apte_treebank_stats.py` as a second worked example |
| `morphology-DCS` | Surface token frequency / case-form distribution claims (e.g. "ātman is always masc. sg.") | DCS SQLite frequency query, `verify_claims_dcs.py` pattern per [`docs/runbooks/CLAIMS_MAINTENANCE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/runbooks/CLAIMS_MAINTENANCE.md) |
| `reference-Whitney` | A systematic grammatical fact adjudicated against Whitney 1889 rather than corpus-counted (tense/mood semantics, address-register claims) | manual cross-check against [`WhitneyGrammar_1889/`](https://github.com/gasyoun/SanskritGrammar/tree/main/WhitneyGrammar_1889) |
| `untestable` | Style/translation-equivalence claims with no stated numeric base (none assigned in this harvest — every SPE-H candidate has a concrete corpus or reference check available) | — |

A **new** design note this harvest surfaces: several Speyer candidates (SPE-H-14..17,
genitive-compounding exceptions) are naturally checked as a **negative-evidence corpus
query** — count of attested `genitive+participle`/`genitive+gerund` compounds in DCS,
expected near-zero — rather than a positive-frequency count. `treebank_syntax_stats.py`
would need a `--forbidden-compound` mode to run this; that mode does not exist yet and
is not built this pass (design note only, per mission scope).

## Acceptance

- [x] Text-layer verdict per book (5 books in the mission's yadisk scope + 1 adjacent find, table above).
- [x] ≥30 harvested claims — 40 delivered in [`SpeyerSyntax_1886/claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/SpeyerSyntax_1886/claims_harvest.yml).
- [x] Backlog committed; raw PDFs untouched on the SanskritLexicography disk (read-only cross-repo reference, no copy).
- [x] Corpus-probe design notes only — no probe script run, no corpus number invented (fence in CLAIMS_MAINTENANCE.md honored).

## Inspect

- [`SpeyerSyntax_1886/claims_harvest.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/SpeyerSyntax_1886/claims_harvest.yml) — the 40 harvested candidates.
- [`SpeyerSyntax_1886/README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/SpeyerSyntax_1886/README.md) — scope note + source pointer.
- This file's verdict table, for the four other books' disposition and the stale-INDEX flag.

_Dr. Mārcis Gasūns_
