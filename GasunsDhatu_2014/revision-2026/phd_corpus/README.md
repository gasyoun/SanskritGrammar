# phd_corpus — Gasūns PhD dhātu dissertation → derived corpus (H4479)

_Created: 10-09-2026 · Last updated: 10-09-2026_

Derived-only landing of the PhD dissertation supplements and bibliography from
`yadisk:Sanskrityatina/34_Диссертация/Итоговый текст/` — the main text and Глава 4-7
were already landed (see [toc_index.json](toc_index.json)); this pass digitizes the
five Приложения (supplements) and the standalone bibliography that were not yet
in the repo, and builds a structured claim-census from the dhātu concordance.

## What's here

| File | Content |
|---|---|
| [toc_index.json](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/toc_index.json) | Full TOC — every dissertation part, its yadisk source, landed/new status, repo path |
| [bibliography_ref.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/bibliography_ref.jsonl) | Per-page text of `01_gasuns-dhatu-PhD-ref.pdf` (23pp, standalone reference list) |
| [suppl1_whitney_bucknell_roots.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/suppl1_whitney_bucknell_roots.jsonl) | Приложение 1 — Whitney/Bucknell root list |
| [suppl2_whitney_roots_by_prefix.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/suppl2_whitney_roots_by_prefix.jsonl) | Приложение 2 — Whitney roots by prefix |
| [suppl3_concordance_text.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/suppl3_concordance_text.jsonl) | Приложение 3 — concordance, raw PDF text (236pp) |
| [suppl4_huet_roots.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/suppl4_huet_roots.jsonl) | Приложение 4 — Huet root list (580 roots, autumn-2014 snapshot) |
| [suppl5_binary_source_comparison.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/suppl5_binary_source_comparison.jsonl) | Приложение 5 — binary source-comparison matrix |
| [dhatu_concordance_claim_census.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/dhatu_concordance_claim_census.jsonl) / [.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/dhatu_concordance_claim_census.csv) | **Claim-census** — structured concordance parsed from `gasuns-dhatu-concordance.xlsm` (sheet `Final`): for each Palsule dhātu, presence/absence in Whitney/Mayrhofer-EWA/Werba-VIA-I/Böhtlingk-PWG |

PDFs and the source `.xlsm` are **not** committed — they stay in local/yadisk storage
per the derived-only landing rule ([reports/YADISK_INVENTORY_07-09-2026.md](https://github.com/gasyoun/Uprava/blob/main/reports/YADISK_INVENTORY_07-09-2026.md) §7).

## Extraction method

**`pdftotext`/poppler is forbidden on Cyrillic PDFs** — [FINDINGS.md §506](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md)
measured it returning *zero* Cyrillic on Russian text while looking shape-plausible
(right token count, right spacing). All extraction here used **PyMuPDF (`fitz`)**,
one of the four readers that scored 8/8 in that bake-off. Every file's Cyrillic-letter
ratio is recorded in [toc_index.json](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/phd_corpus/toc_index.json); three supplements score low
(0.05–0.23) — verified by reading the page-1 text sample, not the ratio alone, to be
genuine IAST/Latin-diacritic root tables (Приложения 1/2/3), not a blank-trap.

## Claim-census — feeds PALSULE_AUDIT.md

[PALSULE_AUDIT.md](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/revision-2026/PALSULE_AUDIT.md) names the exact blocker this unblocks:

> «Метод полной сверки… 1. Оцифровать колонку исключений Приложения 3 (в `.mdx` вошли
> только «Материалы для конкорданса» §3.4; полный конкорданс — в исходном `.docx`/PDF
> диссертации).»

The `.xlsm` concordance (sheet `Final`, 7 379 spreadsheet rows) is the machine-readable
source of Приложение 3, more reliable to parse than the 236-page PDF table. The census
script classifies each row as `root_entry` (non-empty Palsule page-№ ref — a genuine
dhātu headword) or `continuation_or_gloss` (empty ref — a wrapped gloss/translation line
glued into column 0 by the sheet's two-physical-rows-per-entry layout; **not** a new root
claim, and excluded from the census statistics below).

**Result (3 687 root entries):**

| Source | Attested | Share |
|---|--:|--:|
| Böhtlingk PWG (1855-75) | 2 143 | 58.1 % |
| Mayrhofer EWA (1986-2001) | 1 003 | 27.2 % |
| Whitney (1885) | 939 | 25.5 % |
| Werba VIA I (1997) | 737 | 20.0 % |
| **Palsule-only (0 other sources)** | **1 323** | **35.9 %** |

This is the corpus-wide baseline the PALSULE_AUDIT method needs for step 3 (join
Palsule-only roots against the digital vidyut dhātupāṭha + WhitneyRoots crosswalk to
recover "lost genuine roots" per the Krylov critique). **Known limitation:** the
`root_entry`/`continuation_or_gloss` split is a heuristic on one column, not a verified
row-merge; a small number of genuine multi-line root entries may be undercounted if a
root's own gloss also happens to carry non-empty col-0 text on its continuation row.
A tighter merge (group by physical row-pairs, not by ref-presence) is future work, not
done in this pass.

## @DECIDE — which supplement feeds revision-2026 first

The handoff's stop condition asks which supplement should be worked into
`revision-2026` first. Recommendation: **Приложение 3 (the claim-census above)** —
it is the only supplement PALSULE_AUDIT.md already names as a named blocker with a
defined next step (join against `WhitneyRoots/crosswalk/roots.csv` +
`WhitneyRoots/scratch/vidyut_data/prakriya/dhatupatha.tsv`, then a candidate list for
the author's visa, destination article A39). Приложения 1/2/4/5 are useful
cross-references but have no comparable open blocker naming them. **A human should
decide** whether to greenlight that join as the next PALSULE_AUDIT session.

_Dr. Mārcis Gasūns_
