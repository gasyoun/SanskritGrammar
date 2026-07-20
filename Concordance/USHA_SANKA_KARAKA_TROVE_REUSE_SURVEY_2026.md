# Usha Sanka kāraka PhD trove — reuse survey

_Created: 20-07-2026 · Last updated: 20-07-2026_

An asset→consumer survey of the material under `Concordance/UshaSanka_Ph.D_2014/` — the working
corpus behind Usha Sanka's 2014–15 PhD *"A Study Of Kāraka-Demand Of Some Dhātus, Based On
Meaning, Following Śābdabodha For Machine Translation."* The bound thesis PDF
`Concordance/Usha-PhD-Sampurna.pdf` has a broken text layer (Sanskrit2003 font, no ToUnicode) —
but the **source files below are clean, editable, machine-readable**, so no OCR is needed.

Model: Opus 4.8 (`claude-opus-4-8[1m]`), MG lead 20-07-2026.

## Read first — location, bulk, and rights

- **Untracked local bulk:** the whole `UshaSanka_Ph.D_2014/` tree is **361 MB and NOT git-tracked**
  (also not gitignored — only `Concordance/Gita.xlsm` + `Concordance/catalog.mdx` are committed).
  Do **not** commit the tree wholesale; extract only the structured derivations named below.
  Register the tree in [Uprava/DATA_LAYERS_CENSUS.md](https://github.com/gasyoun/Uprava/blob/main/DATA_LAYERS_CENSUS.md).
- **Usha Sanka's own work** (Ch-0…Ch-5a, `dhatu_chart.csv`, her `.xlsx` derivations, the
  `DhatuVistara/` HTML, the `DhatuKaraka-Akanksha-*` files): reuse needs her **permission +
  attribution** — it is an unpublished doctoral corpus, not a released open dataset.
- **Third-party copyrighted works — reference only, NEVER republish** (the repo has a public Pages
  site): Abhyankar *Dictionary of Sanskrit Grammar* (1961, + djvu), Krishnacharya *Bṛhad-Rūpāvalī /
  DhātuKośa* (1924), *Bhāratīya Upasargārtha-Candrikā* (1976), Palsule *Dhātu Concordance* (1955/1961),
  `dhatukarika.pdf`, and any published Dhātupāṭha/Aṣṭādhyāyī edition scans. Run
  [/publish-safety-check](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md) before anything here goes near a public surface.

## Tier A — directly reusable structured data (machine-readable, no OCR)

| Asset (local, untracked) | Shape | Reuse → consumer |
|---|---|---|
| `dhatu_chart.csv` | Dhātupāṭha, `;`-delimited, 9 cols: num · dhātu+num · dhātu · gaṇa · pada · iṭ/aniṭ · transitivity · sub-gaṇa · artha | Dhātupāṭha spine → [GasunsDhatu_2014](https://github.com/gasyoun/SanskritGrammar/tree/main/GasunsDhatu_2014); the pwg_ru 749 DCS-attested roots ([RussianTranslation](https://github.com/gasyoun/SanskritLexicography/tree/master/RussianTranslation)) |
| `Dhatu Patha- With Karakas.xlsx` | dhātu → kāraka mapping | **SG-SE-013 `karaka-case` gold** — the structured form of the kāraka-demand model |
| `Dhatu Patha- Sakarmaka-Akarmaka.xlsx`, `Dhatu Patha- All Sakarmakas.xlsx` | per-root transitivity | valency/kāraka; cross-check DCS transitivity |
| `mAdhavIya-dhAtupATha.xlsx` | 2 265 × 9: full root · root · marker · sense · class · class-name · sūtra · page · variant | Mādhavīya Dhātupāṭha, structured |
| `dhatu-index.xlsx` | 2 253 × 15: dhātu · gaṇa · iṭ · pada · upadeśa · anubandhas · artha · saṅkhyā | complete dhātu index with it-markers |
| `Ashtadyaayi SuutrapaaThaH - Alphabetical & Numerical arrangement.xlsx` | 3 983 sūtras, 2 sheets (by index-no / by akṣara) | Aṣṭādhyāyī sūtrapāṭha → [panini-sutra-lookup](https://github.com/gasyoun/github-spine/blob/main/SKILLS_INDEX.md), panini-commentary-corpus |
| `Ashtadhayi With Anuvritti.xlsx`, `Ashtadhyayi-...ManyVrittis.docx` | sūtras + anuvṛtti / vṛttis | Pāṇini commentary layer |
| `Upasarga-Arthas.xlsx` | 239 rows, upasarga → artha + examples | preverb semantics → SG-WF-011 `preverbs` article |
| `DhatuVistara/*.html` (587 files) | one per prefixed verb (e.g. `abhibhū (1. P.)`), each with **corpus attestations + citations** (Aṣṭāṅgahṛdaya, etc.) | per-verb concordance/evidence layer; complements the Bühler/Knauer/Kochergina [catalog.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/Concordance/catalog.mdx) |
| `PWG-Dhatu-Upasarga-entries.htm` (8.8 MB) | Petersburg-Dictionary verb+upasarga entries | **pwg_ru pipeline** (PWG→RU/EN verb roots) |
| `Oliver_Dev-IAST.htm`, `Dhatu_oliver.docx`, `For Ph.D-Examples-Oliver Doc..html` | DCS (O. Hellwig) dhātu examples, Dev+IAST | DCS-linked example data |

## Tier B — the kāraka model itself (clean Unicode `.docx`, no OCR)

- `धातुकारकाकांक्षा.docx` / `Ch-5-PhD-धातुकारकाकांक्षा.docx` — the **dhātu × kāraka × citation** model:
  verbs grouped by meaning-class (e.g. *utpannānukūlaḥ vyāpāraḥ*), each with `kārakākāṅkṣā` split
  into kartā / karma / karaṇa / sampradāna / apādāna / adhikaraṇa, every role backed by classical
  citations. **Verified clean Unicode** (292 671 Devanagari codepoints) → parse directly into
  SG-SE-013 as native, citation-backed kāraka gold (replaces the ~3.93 % `deprel` proxy).
- `kAraka Tagging scheme- Skt.pdf` — the kāraka annotation/tagging methodology.
- `DhatuKaraka-Akanksha-Work-file-Original*.docx`, `Backup-Dhatu-Karaka28-12-13.docx` — working
  drafts of the same dataset (provenance / earlier states).
- `Ch-0…Ch-4`, `Ch-5a-Conclusion`, `Ch-End-Parishishtam` `.docx` — full thesis text (Śābdabodha
  method, dhātu-vistāra, kāraka-vistāra, NLP method).

## Tier C — third-party reference (rights-restricted, do not republish)

Abhyankar 1961 (`KVAbhyankar-GramDic-1961.pdf`, `.djvu`), Krishnacharya 1924, Palsule 1955/1961
(`Palsule-DhatuConcordance-1961-WithMyComm.pdf`, `Palsule-ConcordDhatu1955-02 (OCR).pdf`),
Bhāratīya Upasargārtha-Candrikā 1976, `dhatukarika.pdf`, `itviveka.pdf`. Consult only.

## Highest-leverage next steps

1. **Register** the 361 MB tree in [DATA_LAYERS_CENSUS.md](https://github.com/gasyoun/Uprava/blob/main/DATA_LAYERS_CENSUS.md) (large unregistered data on disk).
2. **kāraka gold for SG-SE-013** — parse `Dhatu Patha- With Karakas.xlsx` + `धातुकारकाकांक्षा.docx`
   into a structured `dhātu → kāraka → citations` dataset; use as the native reference layer against
   which the DCS `deprel` proxy is measured (H-scale, no OCR).
3. **Dhātupāṭha reconciliation** — `dhatu_chart.csv` / `mAdhavIya-dhAtupATha.xlsx` cross-checked
   against GasunsDhatu_2014 and the pwg_ru 749-root list.
4. **Aṣṭādhyāyī** — load the sūtrapāṭha XLSX behind the Pāṇini skills.
5. **pwg_ru** — mine `PWG-Dhatu-Upasarga-entries.htm` for the verb-root translation queue.
6. **Rights** — confirm reuse permission + attribution terms from Usha Sanka before any derived
   dataset is published; keep Tier C off every public surface.

_Dr. Mārcis Gasūns_
