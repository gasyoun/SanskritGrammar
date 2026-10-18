_Created: 13-10-2026 · Last updated: 13-10-2026_

# A72 mini-census: indigenous Sanskrit metalanguage sigla (the 2006 §3 dimension)

_Гасунс_

Commissioned by [H6460](https://github.com/gasyoun/Uprava/blob/main/handoffs/H6460-OxAlpha_SanskritGrammar_a72-sanskrit-sigla-mini-census_11.10.26.md) (MG verdict 11-10 grill R1.4 "Mini-census now") as the Sanskrit-sigla leg of [A72](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md) — *Latin terms in Sanskrit dictionaries, twenty years on* (evolution of [Gasūns 2006, EURALEX Torino](https://github.com/gasyoun/Uprava/blob/main/research/notes/latin-terms-2006-fulltext.md), pp. 773–778). Mission source line: "Sources are NOT in CSDL: SanskritGrammar Panini corpus, csl-standards A70 apparatus line — read A70 docs first, do not rebuild."

## 1. Scope, method, and the census-vs-illustrative statement

**Explicit statement (acceptance bullet 3):** the 2006 §3 list — Pāṇini's "LAT, LAN", "°ādi", Jinendra's "kha/up/aup/ma", Vopadeva's "ma" — is **a list of examples, not a corpus**. This census therefore reports two evidence classes and never blurs them:

- **CENSUS** — a class is measured over an estate corpus or carries the A70 note's corpus counts (marker counts, lower bounds by the A70 method, §2 "Counts").
- **ILLUSTRATIVE** — the class is attested in the estate only by a citable printed/digitized text or by the 2006 paper itself; no estate corpus measurement exists. Where no estate citation at all exists, the class goes to §5 Limitations instead of being paraphrased from memory.

Method: A70 read first ([A70 note](https://github.com/sanskrit-lexicon/csl-standards/blob/main/docs/A70_TEI_LEX0_INDIGENOUS_APPARATUS_NOTE.md) + machine twin `data/pilot/skd-lex0-gaps.json`), csl-atlas M4 key consumed as-is, `data/shiva_sutras/` consumed as the vendored kosha snapshot — nothing rebuilt, no csl-orig writes.

## 2. Inventory of indigenous metalanguage sigla classes

| # | Sigla class | Token(s) | Meaning | Status | Estate source (per-row citation) |
|---|---|---|---|---|---|
| I1 | Pratyāhāra sigla machinery | `aK, aC, yaṆ, haL, …` (42 named) | one sigil = a closed class of phonemes, via it-marker deletion over the 14 Śiva sūtras (57-token master sequence) | CENSUS | `data/shiva_sutras/` (vendored from kosha `shiva-sutras-machine`, H4471, kosha commit `11a243eb`); `scripts/verify_shiva_pratyahara.py` PASS C1–C5; `REPORT_SHIVA_SUTRAS_PRATYAHARA_REFERENCE_2026.md` |
| I2 | lakāra tense/mood sigla | `LAṬ, LIṬ, LUṬ, LṚṬ, LOṬ, LAÑ, LIÑ, LṚÑ, LEÑ, LOÑ` (10; 9 named in source) | affix sigla carrying anubandha on L: present, perfect, periphrastic future, subjunctive, imperative, imperfect, optative/precative, aorist, conditional | CENSUS-side (digitized estate text) | `BibliothecaSanscritica/KnauerUchebnik_2021/KnauerUchebnik_2021.mdx` line 922: "लकार lakāra … введенная Панини saṃjñā: 10 времен и наклонений глагола, имеющие анубандху на L" — Knauer 1908 is [Kn] of the 2006 reference list |
| I3 | "°ādi" etc.-sigil | `…ādi` ("and so on") | Pāṇinian-style open-list closer, "could compete with their Latin equivalents" | ILLUSTRATIVE | [2006 paper](https://github.com/gasyoun/Uprava/blob/main/research/notes/latin-terms-2006-fulltext.md) §3, p. 777. No attestation in the 47-entry SKD Lex-0 pilot (`csl-standards/data/pilot/tei-lex0/`) — see §5 |
| I4 | Jinendra's Kośa it-sigla | `kha` = lopa = "0"; `up` = guṇa; `aup` = vṛddhi | technical letters of the root list; `kha` is a written zero-sigil | ILLUSTRATIVE | [2006 paper](https://github.com/gasyoun/Uprava/blob/main/research/notes/latin-terms-2006-fulltext.md) §3, p. 777. Estate census cousin for the *zero* concept: I6 |
| I5 | Vopadeva/SKD anubandha slot | root-final it-letters: gaṇa letters (`ka/ki…na…`), pada letters (`ṅ`=ātmane, `ñ`=ubhaya), operation letters (`i`=idit, `u/ū`=veṭ, `ṛ`=caṅ, `ma`=mit …), 46-letter key | operation codes on roots, decoded by the Dhātudīpikā key printed in the SKD front matter | CENSUS | csl-atlas [`MICROSTRUCTURE_SKD_ANUBANDHA_KEY.md`](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/MICROSTRUCTURE_SKD_ANUBANDHA_KEY.md) (Dhātudīpikā over SKD's 1,754 roots); [A70 note](https://github.com/sanskrit-lexicon/csl-standards/blob/main/docs/A70_TEI_LEX0_INDIGENOUS_APPARATUS_NOTE.md) §G2 (corpus count **1,925**; example *ghiṇa* L11792 `i ṅa` → ātmanepada + seṭ) |
| I6 | Zero-meaning sigil | dot `.` / zero (empty anubandha slot) | "roots that have no anubandha get a dot or a zero" — absence is a statement, not missing data; unmarked pada = parasmaipada default | CENSUS | SKD front matter, quoted in the [M4 key doc](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/MICROSTRUCTURE_SKD_ANUBANDHA_KEY.md) ("प्रत्येक-धातोरनुबन्धञ्च निर्णीतवान्…"); [A70 note](https://github.com/sanskrit-lexicon/csl-standards/blob/main/docs/A70_TEI_LEX0_INDIGENOUS_APPARATUS_NOTE.md) §G3 (corpus count **445**, example *bharbha* L24806) |
| I7 | Technical word-class letters | `tri` (triliṅga), `vya` (avyaya) | word class by gender behaviour — a morphological criterion, not a part of speech | CENSUS | [A70 note](https://github.com/sanskrit-lexicon/csl-standards/blob/main/docs/A70_TEI_LEX0_INDIGENOUS_APPARATUS_NOTE.md) §G10 (corpus count **4,440**; example *apa* L1368 `vya`) |
| I8 | Attributed restatement of it-letters | Durgādāsa's `i, ghiṇṇyate . ṅa, ghiṇṇate …` | commentary layer that restates each sigil before the form it licenses | CENSUS | [A70 note](https://github.com/sanskrit-lexicon/csl-standards/blob/main/docs/A70_TEI_LEX0_INDIGENOUS_APPARATUS_NOTE.md) §G4 (corpus count **2,287**; example *ghiṇa* L11792) |

Supporting counts from the same A70 machine twin (`data/pilot/skd-lex0-gaps.json`), relevant as the corpus scale of the indigenous apparatus: 30,029 *iti*-units (G1), 4,887 *paryāya* runs (G5), 20,452 positional quotations (G9), 667 *nibandha* prose (G8), 3,470 *bhāṣā* glosses (G6), 354 scoped cross-references (G7), 114 CDSL corrections (G12).

## 3. Spot-check rows (acceptance evidence)

- **kha = lopa = "0"** — Jinendra's written zero-sigil: [2006 paper](https://github.com/gasyoun/Uprava/blob/main/research/notes/latin-terms-2006-fulltext.md) §3, p. 777 ("There is, e.g., 'kha' (=lopa) for 'null', that is '0'"). Estate zero concept measured: SKD dot/zero zero-meaning, **445** rows (A70 §G3) with the front-matter Devanagari rule quoted in the M4 key doc.
- **up = guṇa, aup = vṛddhi** — [2006 paper](https://github.com/gasyoun/Uprava/blob/main/research/notes/latin-terms-2006-fulltext.md) §3, p. 777 ("'up' (=guna), 'aup' (=vṛddhi) in Jinendra's Kosha"). No estate corpus carries the Jinendra root list (see §5).
- **Jinendra-vs-Vopadeva ma divergence** — [2006 paper](https://github.com/gasyoun/Uprava/blob/main/research/notes/latin-terms-2006-fulltext.md) §3, p. 777: "Or 'ma' which Jinendra uses as 'parasmaipadam' yet Vopadeva has 'ātmanepadam' instead." **Estate refinement (census finding):** the decoded Dhātudīpikā key ([M4 key doc](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/docs/MICROSTRUCTURE_SKD_ANUBANDHA_KEY.md) § "`ma` — resolved (Palsule's KKD)", citing G.B. Palsule's *Kavikalpadruma* edition, Appendix III, pp. 95–100) gives Vopadeva `ma` = **mit / nici-hrasva** (an operation it, "penultimate shortens before ṇic", Pāṇ 6.4.92 *mitāṃ hrasvaḥ*), and in the Vopadeva/SKD convention **pada is carried only by `ṅ` (ātmane) and `ñ` (ubhaya)**, parasmai being the unmarked default. The estate decode therefore corrects the 2006 print claim on Vopadeva's `ma`; the Jinendra side has no estate corpus to check against (§5).

## 4. vs-Latin comparison table

Latin-side numbers are the computed A72 census v1 (csl-atlas, 45 dictionaries, 1,506,391 entries, 34,765 distinct raw labels): [ABBREV_CENSUS_V1_2026.md](https://github.com/sanskrit-lexicon/csl-atlas/blob/main/reports/ABBREV_CENSUS_V1_2026.md), [PR #545](https://github.com/sanskrit-lexicon/csl-atlas/pull/545); the 2006 homograph classes there compute (M. 11 senses, P. 11, N. 10, V. 7).

| Dimension | Latin grammatical sigla (2006 §2 + census v1) | Indigenous Sanskrit sigla (this census) |
|---|---|---|
| Polysemy analogue | **within one canon**: 448 of 4,752 legend-carrying strings polysemous (9.4%); single letters diverge by dictionary (V. = vocativus/Vedic/Vopadeva/vide/Vikram; P. = parasmaipada/Pāṇini's Aṣṭādhyāyī/person/…) | **within one tradition** the sigil is nearly monosemous (a pratyāhāra or a gaṇa letter denotes one closed class); polysemy appears **across traditions** — `ma`: Jinendra parasmaipada vs Vopadeva mit (I5/I8); cross-tradition divergence, not intra-dictionary homography, is the Sanskrit analogue of Latin's "M. = Manu or Murti" |
| Zero/absence | no zero-sigil; absence means nothing (a letter not used is simply absent) | absence is asserted: dot/zero anubandha slot (**445** rows) and the unmarked-pada parasmai default are *statements by silence* (I6) — a dimension Latin sigla do not have |
| Mechanism | linear word-abbreviations standing beside a form (cases, voices `Ä/A/P/p`, moods `Ipv., Ipf., Ppf.`, classes) | positional code letters with a decoding key: Śiva-sūtra it-markers → 42 pratyāhāra sigla (I1); L-series lakāra (I2); per-root anubandha slot decoded by the front-matter Dhātudīpikā table (I5) |
| Self-documentation | key is external (the dictionary's abbreviations page; 2006 §1 documents the resulting "twelve transliterations of ç"-style drift) | key is internal: the Dhātudīpikā key is printed in the dictionary's own front matter, and the commentary layer restates each letter in situ (**2,287** rows, I8) |
| Territorial scope (2006's own claim) | universal in Western lexicography, "anchors of associations for a Western scholar" | "used only in India and therefore are territorially restricted" (2006 §3) — but corpus-scale inside that restriction: 30,029 *iti*-units, 20,452 positional quotations in SKD alone |
| Composability | small-class proposal (2006 §2.3): 1–4 letter abbreviations by concept class | native composition: one sigil = one class (aK, haL), gaṇa letter + pada letter + operation it stacked in one anubandha slot (I5) |

## 5. Limitations

- **Jinendra's Kośa has no estate corpus.** The `kha/up/aup/ma(parasmai)` rows are ILLUSTRATIVE, sourced solely from the published 2006 paper (estate-held verbatim extraction + [evolution dossier](https://github.com/gasyoun/Uprava/blob/main/research/gasuns-2006-latin-terms-evolution-dossier.md)). Per H6460's fail rule these are recorded here rather than reconstructed from memory; the Cologne Vācaspatya (`vcp`) would be the acquisition route for a later census run.
- **"°ādi" is not attested in the 47-entry SKD Lex-0 pilot** (`data/pilot/tei-lex0/`); the 2006 citation stands alone for this row.
- **The 2006 §3 list is examples, not a corpus** — no class count on the Sanskrit side of this census derives from it; counts come from A70 §4 marker counts, which are lower bounds by the A70 method (§2 "Counts") and witness one dictionary (SKD), itself flagged as "a floor" in A70 §7.
- **`ma` divergence is asymmetrically evidenced**: the estate decode corrects the Vopadeva side (M4 key, Palsule's KKD); the Jinendra side is untestable until a Jinendra root list enters the estate.
- **Two root-row scopes as printed**: A70 §2 cites "the csl-atlas M4 table (2,544 SKD root rows)" while the M4 key doc says the key applies "over SKD's 1,754 roots"; both figures are quoted as printed and left to the owning repo to reconcile.

## 6. Reuse and provenance

- A70 ([csl-standards note](https://github.com/sanskrit-lexicon/csl-standards/blob/main/docs/A70_TEI_LEX0_INDIGENOUS_APPARATUS_NOTE.md) + `skd-lex0-gaps.json`) read first and consumed; **not rebuilt**.
- csl-atlas M4 anubandha key consumed as the authoritative Dhātudīpikā decode; **not rebuilt**.
- `data/shiva_sutras/` consumed as the vendored kosha snapshot (H4471); verify run green this pass.
- csl-atlas A72 census v1 consumed for the Latin-side column; **not rebuilt**.
- No csl-orig writes (hard guard); no TeX/PDF; markdown only.

## Delivery (five fields)

- **Changed:** new [`REPORT_A72_SANSKRIT_SIGLA_MINI_CENSUS_13-10-2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/REPORT_A72_SANSKRIT_SIGLA_MINI_CENSUS_13-10-2026.md) (8-class inventory + 6-dimension vs-Latin comparison, per-row citations); one `changelog_queue/` entry.
- **Unchanged:** all data layers (`data/shiva_sutras/`, sangram, BibliothecaSanscritica texts), scripts, site build.
- **Checks:** `python scripts/verify_shiva_pratyahara.py` → PASS C1–C5; `npm run test:site` + `npm run typecheck` → PASS (PR CI will run the full `npm run verify`).
- **Risks:** Jinendra rows are print-sourced only (declared); A70 counts are lower bounds; the 2,544-vs-1,754 scope mismatch is quoted, not reconciled.
- **Inspect:** open §2 (inventory), §3 (spot-checks: kha=lopa=0, up/aup, ma divergence), §4 (vs-Latin table).
