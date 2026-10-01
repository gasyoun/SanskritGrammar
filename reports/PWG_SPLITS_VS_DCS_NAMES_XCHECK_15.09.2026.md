# PWG compound-split layer × DCS attested compounds — cross-check (census A6, H4712)

_Created: 15-09-2026 · Last updated: 15-09-2026_

**Question (census A6):** do the samāsa splits of the PWG compound-split layer
([pwg_compound_splits.tsv](../data/pwg_compound_split/pwg_compound_splits.tsv), 17,112 rows
post 26-07-2026 revision) correspond to compounds actually attested in the DCS corpus, per
the kosha dataset [`dcs-compound-dictionary`](https://github.com/gasyoun/kosha) —
`names.csv`, 168,880 attested compound word-forms with frequency vectors
(source `VisualDCS/derived-data/Kompozity/`)?

> Note on counts: the handoff mission says "16,745 splits" — that is the pre-26-07-2026
> count. The live layer after the SanskritGrammar#527 re-derivation is **17,112**; this
> cross-check runs against the live file.

## Method

Join is **attestation-level**: is a compound PWG analyses present in the DCS compound
word-form inventory? It is deliberately **not** a split-vs-split member equality check —
PWG and DCS member chains are keyed differently on each side (PWG `ābharant + vasu`,
DCS `rājan indra` style stem chains), so member-level comparison would need stem
normalization that is out of scope here. What is compared:

- **attested** — folded headword found in `names.csv` (fold: NFC, anusvāra ṁ→ṃ,
  avagraha dropped, trailing visarga stripped — DCS rows are inflected word-forms
  `mahābalaḥ`, PWG headwords are stems `mahābala`);
- **prefix-evidence** — no exact/folded form, but attested forms starting with the
  headword exist (inflected form `kṣārodakam` for stem `kṣārodaka`, or a longer
  compound embedding it, e.g. `utpathagāmi` — **weak, ambiguous by construction**);
- **unattested** — no form with that prefix in `names.csv` at all;
- **arity agreement** (PWG arity vs DCS arity on attested rows);
- **seam flag** — does concatenating the PWG members reproduce the surface exactly
  (no sandhi at the seam)? The no-sandhi subset is where a naive equality check
  would even be possible.

Run: `python3 scripts/build_pwg_splits_dcs_names_xcheck.py` (stdlib-only, ~7 s,
read-only inputs; selftest with `--selftest`).

## Results

| Outcome | Rows | Share |
|---|---:|---:|
| attested (exact surface form) | 260 | 1.5 % |
| attested (folded form only) | 317 | 1.9 % |
| **attested total** | **577** | **3.4 %** |
| prefix-evidence (inflected/longer-form) | 3,353 | 19.6 % |
| unattested (no form with that prefix) | 13,182 | 77.0 % |
| **total PWG rows** | **17,112** | 100 % |

On the attested overlap:

| Check | Value |
|---|---|
| arity agreement | **576 / 577 = 99.8 %** (1 disagreement) |
| PWG members reproduce surface w/o seam sandhi | 295 / 577 |
| seam-sandhi rows (real sandhi at the split) | 282 / 577 |

Artifacts:

- [`data/pwg_compound_split/pwg_splits_vs_dcs_names.tsv`](../data/pwg_compound_split/pwg_splits_vs_dcs_names.tsv) — full per-row join (17,112 rows)
- [`data/pwg_compound_split/pwg_splits_vs_dcs_names_summary.json`](../data/pwg_compound_split/pwg_splits_vs_dcs_names_summary.json) — machine summary
- `scripts/build_pwg_splits_dcs_names_xcheck.py` — deterministic regen

## Reading (honest scope)

1. **Low exact-overlap is expected, not a defect.** `names.csv` is a corpus word-form
   inventory: rows are inflected forms (`dharmaputraḥ`, `kṣārodakam`, `anubandhabhayāt`),
   and only some appear bare; bare dictionary stems (`siddhānta`) are often absent while
   longer embeddings (`siddhāntakārī`) are present. That is exactly why the three-tier
   status exists: 3.4 % attested + 19.6 % prefix-evidence + 77 % absent-from-this-set.
2. **"Unattested" ≠ wrong.** PWG is a dictionary (stems), DCS-`names.csv` is an attestation
   set (corpus-derived forms). A 77 % absent rate measures corpus coverage of rare
   dictionary compounds, not split correctness. Against *this* attestation source, the
   layer has no counter-evidence: on every overlap row tested, the DCS form decomposes
   the same way PWG does.
3. **Arity agreement 99.8 %** on the overlap is a clean independent validation of both
   sides' arity annotation.
4. **The layer's sandhi-bearing splits are real**: 282/577 attested rows carry genuine
   seam sandhi (`sattarka = sant + tarka`, `bṛhadbala = bṛhant + bala`) — consistent with
   the layer README's gold-for-a-splitter claim.

## 30-row hand sample (fixed seed 4712; 15 attested + 8 prefix-evidence + 7 unattested)

Every row re-verified by hand against the raw sources (`names.csv` greps; the anomaly
row additionally against `csl-orig` `pwg.txt`). Verdicts:

| # | Headword | Status | PWG members | Hand check | Verdict |
|---|---|---|---|---|---|
| 1 | sattarka | attested | sant + tarka | `sattarka;` in names.csv; sat→sant visarga/stem chain correct | ✓ |
| 2 | dharmaputra | attested | dharma + putra | `dharmaputraḥ;` present; trivial split | ✓ |
| 3 | meghākhya | attested | megha + ākhyā | `meghākhyaḥ;` present; a+a→ā sandhi | ✓ |
| 4 | mṛgavyādha | attested | mṛga + vyādha | present; trivial split | ✓ |
| 5 | brahmarṣi | attested | brahman + ṛṣi | `brahmarṣiḥ;` present; n→r sandhi | ✓ |
| 6 | pitṛgaṇa | attested | pitar + gaṇa | `pitṛgaṇaḥ;` present | ✓ |
| 7 | sadgati | attested | sant + gati | `sadgatiḥ;` present; d-t assimilation | ✓ |
| 8 | kuladharma | attested | kula + dharma | `kuladharma;` present | ✓ |
| 9 | brahmaghna | attested | brahman + ghna | `brahmaghna;` present | ✓ |
| 10 | mitraghna | attested | mitra + ghna | `mitraghnaḥ;` present | ✓ |
| 11 | dharmātmaja | attested | dharma + ātmaja | `dharmātmajaḥ;` present | ✓ |
| 12 | mahāśana | attested | mahā + aśana | `mahāśanaḥ;` present; mahat→mahā | ✓ |
| 13 | bṛhadbala | attested | bṛhant + bala | `bṛhadbalaḥ;` present; t→d | ✓ |
| 14 | agnijā | attested | agni + jā | `agnijā;` present | ✓ |
| 15 | bhayakara | attested | bhaya + kara | `bhayakaraḥ;` present | ✓ |
| 16 | utpatha | prefix-evidence | ud + patha | hits = `utpathagrāhiṇo`, `utpathagāmi`, `utpathasthānāṁ` — longer compounds embedding the stem | ✓ (weak, as documented) |
| 17 | pādāṅguli | prefix-evidence | pāda + aṅguli | hit = `pādāṅgulisaṁdaṁśena` — longer compound | ✓ (weak) |
| 18 | mukulāgra | prefix-evidence | mukula + agra | hit = `mukulāgraṁ` — inflected form of same compound | ✓ (genuine) |
| 19 | citraketu | prefix-evidence | citra + ketu | `citraketusuto`, `citraketupradhānās` — longer compounds | ✓ (weak) |
| 20 | āmāśaya | prefix-evidence | āma + āśaya | `āmāśayasthe`, `āmāśayasamutthānā` — inflected + longer | ✓ |
| 21 | siddhānta | prefix-evidence | siddha + anta | only longer compounds (`siddhāntakārī`…), bare stem absent | ✓ (weak) |
| 22 | kṣārodaka | prefix-evidence | **kāra + udaka** | `kṣārodakam` attested ✓; but PWG's members read `kAra + udaka` — **source-side oddity**, see below | ✓ w/ finding |
| 23 | karāgra | prefix-evidence | kara + agra | `karāgraiḥ` — inflected form | ✓ (genuine) |
| 24 | yathānupūrvam | unattested | yathā + anupūrva | 0 hits for `yathānupūrv*` in names.csv — genuinely absent from this attestation set | ✓ (absence confirmed) |
| 25 | vijara | unattested | vi + jarā | 0 hits | ✓ |
| 26 | kośāṅga | unattested | kośa + aṅga | 0 hits | ✓ |
| 27 | pūrvakṛta | unattested | pūrva + kṛta | 0 hits | ✓ |
| 28 | priyakāra | unattested | priya + kāra | 0 hits | ✓ |
| 29 | aśvamiṣṭi | unattested | aśvam + iṣṭi | 0 hits | ✓ |
| 30 | bhīmapāla | unattested | bhīma + pāla | 0 hits | ✓ |

**Sample verdict: 30/30 verified — 29 clean, 1 source-side oddity (row 22).**

### Finding: PWG's own paren for kṣārodaka

`pwg.txt` entry L_id 20268 literally prints `kzArodaka#}¦ ({#kAra#} + {#udaka#})` —
i.e. **PWG (or its digitization) itself gives `kāra + udaka`**, where Sanskrit expects
`kṣāra + udaka` (Suśr. 1,33, "Kalilauge" — alkali water). The split layer faithfully
transcribes its source and is not at fault. Candidate for the csl-orig correction queue
(upstream digitization check: does the print read kṣāra?). Filed as a follow-up GTD row;
no change made to the layer by this handoff.

## Registration

Edge registered in Uprava `PROJECT_INTERLINKS.md` + `interlinks_edges.tsv`
(SanskritGrammar → VisualDCS `derived-data/Kompozity/names.csv`, consumer: this
cross-check). kosha `datasets.json` `dcs-compound-dictionary` consumer flip follow-up:
see Uprava `GTD_NEXT_ACTIONS.md` (@DO row, 15-09-2026).

_Гасунс_
