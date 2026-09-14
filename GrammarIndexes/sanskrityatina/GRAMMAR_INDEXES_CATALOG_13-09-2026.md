# Sanskrityatina «Указатели указателей» — grammar-index catalog + claims-audit mapping

_Created: 13-09-2026 · Last updated: 13-09-2026_

H4476 (class: data, tier: OxAlpha / opencode, model z-ai/glm-5.3-flash). Catalog of the
`yadisk:Sanskrityatina/Указатели указателей/` folder + the companion `yadisk:Sanskrityatina/Index/Data/`
texts, each mapped to a grammar-claims-audit target
(`/grammar-claims-audit` registries in this repo; kosha `paninian-sutra-coverage-map`).
Derived index-of-owners TSV: [index_of_owners.tsv](https://github.com/gasyoun/SanskritGrammar/blob/main/GrammarIndexes/sanskrityatina/index_of_owners.tsv).
Raw scans were fetched **read-only to session temp** (never committed); refetch command below.

## Census method (one line each)

Every PDF probed with pypdf: page count + text extraction on 5 spread sample pages
(≈10% of pages for the big register) → OCR verdict. docx/xlsx probed via `word/document.xml`
/`xl/sharedStrings.xml` char counts. Knauer.zip unzipped and listed. «Указатели» PDFs are
Latin/Devanagari-script — poppler-free pypdf probing is safe (the poppler-Cyrillic danger
fact does not apply; no Cyrillic PDF was text-probed).

## Catalog — yadisk:Sanskrityatina/Указатели указателей/

| # | File | Size | Pages | Granularity | OCR / text layer | Claims-audit target |
|---|------|------|-------|-------------|------------------|---------------------|
| 1 | `Grammaire-Sanscrite-Louis-Renou Index.pdf` | 2.35 MB | 11 | word-form → §-ref index to Renou GS (1930) | **SCANNED — no text layer** (vision OCR needed) | future Renou-GS registry (none yet) |
| 2 | `Grammaire-de-la-Langue-Vedique-de-Louis-Renou Index.pdf` | 3.82 MB | 24 | word-form → §-ref index to Renou TV (1952) | text OK (16.2K chars / 5-pg sample) | future Renou-Védique registry (none yet); Vedic corpus probes via DCS |
| 3 | `Index from Oberlies-EpicSkr2003.pdf` | 2.54 MB | 25 | word-form → page index to Oberlies EAS 2003 | text OK (10.8K chars / 5-pg) | future Epic-Sanskrit registry (none yet) |
| 4 | `Verbs Oberlies-EpicSkr2003.pdf` | 13.3 MB | 126 | verb-root → page index (same volume) | text OK (thin per-page, dense Sanskrit; 9.5K chars / 5-pg) | same as #3 |
| 5 | `Hauschild-RegisterzurWackernagel1964.pdf` | 67 MB | 263 | word-form → p.-col. register to Wackernagel AIG I (1896); the big one | text OK (9.9K chars / 5-pg sample; subset CFF font `ClarendonIndologique` — full-pass extraction unverified, fontTools warn) | future Wackernagel-AIG registry; Vedic claims pool |
| 6 | `Bucknell 359.pdf` | 26.5 KB | 6 | excerpt, 6 pp. (p.359 of Bucknell's Sanskrit manual?) | text OK (7.9K chars / 5-pg) | inspect before harvest; likely supplement |
| 7 | `Knauer.zip` | 37.4 MB | — | **HTML, not a scan**: `knauer_dict.htm` (829 KB) + Charis-SIL/Sahitya TTFs | text natively (HTML) | [KnauerFrazy_1908/](https://github.com/gasyoun/SanskritGrammar/blob/main/KnauerFrazy_1908/) — in-repo sibling |
| 8 | `MacDonell-Grammar1927 Index.pdf` | 1.52 MB | 11 | word-form → §-ref to MacDonell Sanskrit Grammar | **SCANNED — no text layer** | future MacDonell-SG registry |
| 9 | `MacDonell-Vedic1916 Index.pdf` | 1.52 MB | 20 | word-form → §-ref to MacDonell Vedic Grammar | **SCANNED — no text layer** | future MacDonell-Vedic registry |
| 10 | `Whitney-Grammatik1879 Sanskritregister.pdf` | 1.62 MB | 14 | Sanskrit word → §-ref register of the 1879 German Whitney | **SCANNED — no text layer** | [WhitneyGrammar_1889/claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/WhitneyGrammar_1889/claims.yml) (15 rows) — 1879≈1889 edition pair |
| 11 | `Wortregister from Thumb-Hand1904-ii.pdf` | 1.31 MB | 19 | word register to Thumb/Hand grammar (1904) | **SCANNED — no text layer** | future Thumb registry |
| 12 | `Pages from Edgren-SansGrammar-1885.pdf` | 199 KB | 8 | extracted pages from Edgren 1885 | text OK (9.0K chars / 5-pg) | future Edgren registry |
| 13 | `Ukazatel_Uch_KOChERGINA.docx` | 238 KB | — | Kochergina textbook index, native docx (909 words) | text natively | [KocherginaUchebnik_1998/claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.yml) (260 rows) |
| 14 | `Ukazatel_Uch_KOChERGINA_Byuler.docx` | 111 KB | — | Kochergina↔Bühler cross ukazatel (1,353 words) | text natively | KocherginaUchebnik_1998 + [BuhlerLeitfaden_1923/claims.yml](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/claims.yml) (403 rows) — **bridge file** |
| 15 | `Ukazatel_k_Kocherginoy_Olga.xlsx` | 18 KB | — | index table (415 shared-string cells) | text natively | KocherginaUchebnik_1998 |
| 16 | `Указатель к «Учебнику санскрита».docx` | 25 KB | — | index to «Учебник санскрита» (425 words) | text natively | textbook registry (identify edition on harvest) |
| 17 | `index.doc` / `index.pdf` | 619 KB / 794 KB | ? | unnamed generic pair — **not downloaded** (name gives nothing; fetch on demand) | unknown | triage before any use |
| 18 | `Kossovich_21.04.2020.zip` | 132.8 MB | — | Kossovich materials zip — **not downloaded** (dupes `30_Kossowich/` sibling folder) | unknown | out of scope; see `30_Kossowich/` |
| 19 | `Порядок слов/` subfolder | ~300 MB | — | word-order literature (Delbrück, Staal, Gillon, Wackernagel-Syntax 1950, Renou 1952) — **syntax papers, not indexes** | n/a | out of scope for claims-audit; separate syntax pool |

## Catalog — companion yadisk:Sanskrityatina/Index/Data/ (28 files)

The handoff named four; the folder holds **МхБхКомм01–10+.txt** (Махабхарата vols I–X, 1950–,
Russian translation/commentary, UTF-8, 85 KB–616 KB each), `fasmer-dr-ind.htm` (2.27 MB, Фасмер
HTML — not Sanskrit-claims material), `Mify_759_ind.html` (7.3 MB), plus dictionary texts
(Потапова, Смирнов, Топоров, Фриш, Эрман-Темкин) and `Index_pr.exe` (Windows index program).
These are **corpus-side companions, not grammar indexes**: no page/§ mapping to a grammarian's
prose → not claims-audit targets; they feed DCS-adjacent commentary work instead.

## Mapping — index → claims-audit surface (the mission's second deliverable)

- **Direct, in-repo targets (ready now):** #13–15 Kochergina → 260-row registry;
  #14 bridge also → 403-row Bühler registry; #10 Whitney-1879 → 15-row 1889 registry;
  #7 Knauer → `KnauerFrazy_1908/`. **Text-layer or native-text on every one** — zero OCR gate.
- **Future registries (index exists, book harvest does not):** Renou GS (#1), Renou Védique (#2),
  Oberlies EAS (#3–4), Wackernagel AIG (#5), MacDonell SG+VG (#8–9), Thumb (#11), Edgren (#12).
  These indexes are the cheap half of a future harvest: §/page anchors are already tabulated
  here; the books themselves would be the expensive half.
- **kosha `paninian-sutra-coverage-map`** (3,983-row Aṣṭādhyāyī derivation enumeration) —
  unchanged by this catalog; none of the 19 items is a sūtra-level index, so no mapping edge
  into that dataset. Cross-check done so future passes don't invent one.

## @DECIDE (MG) — which index becomes the first claims-harvest wave

Options, all with the index side already cataloged:

1. **Kochergina ukazateli (#13–15) — RECOMMENDED.** Native text, in-repo 260-row registry,
   bridge file to Bühler's 403 rows → one wave exercises two registries; ~zero OCR cost.
2. Whitney-1879 register (#10) → extends the existing 15-row 1889 registry; but scanned —
   vision OCR first (~1 h class).
3. Oberlies EAS (#3–4, 151 pp, text OK) → opens a NEW Epic registry; highest new-coverage
   value, medium cost (§-ref → DCS probes).
4. Hauschild Wackernagel register (#5, 263 pp) → biggest, Vedic pool; CFF-font extraction
   risk must be cleared first.

## Provenance / refetch (raws are NOT in the repo)

```
rclone copy "yadisk:Sanskrityatina/Указатели указателей/<file>" <tmp>/   # remote 'yadisk' in ~/.config/rclone/rclone.conf
rclone copy "yadisk:Sanskrityatina/Index/Data" <tmp>/Data --include "МхБхКомм0[1-4].txt" --include "fasmer-dr-ind.htm"
```

Byte sizes in the TSV were read off the remote listing at census time (13-09-2026).

_Dr. Mārcis Gasūns_
