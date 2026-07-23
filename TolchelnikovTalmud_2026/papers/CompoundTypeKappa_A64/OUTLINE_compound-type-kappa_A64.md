# A64 — Can Pāṇinian compound type be recovered from an unannotated corpus? A two-pass κ study (outline)

_Created: 22-07-2026 · Last updated: 22-07-2026_

**ID:** A64 · **Readiness:** 2/5 → 3/5 (this handoff) · **Home:** SanskritGrammar ·
**Venue candidates:** ISCLS / WSC-2027-computational / NLP4DH / LREC-COLING (a human `@DECIDE`s;
see § "Venue" below — not chosen here).
Paper layer of the [Sangram morphology programme](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md),
English venue-paper draft of the published RU pilot [SG-WF-008](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/index.mdx)
(handoff [H989](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H989-Opus_SanskritGrammar_sangram-p4-tatpurusa_15.07.26.md), [v0.25.0](https://github.com/gasyoun/SanskritGrammar/releases/tag/v0.25.0)).
Model: Sonnet 5 (`claude-sonnet-5`), handoff [H1466](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1466-Sonnet_SanskritGrammar_a64-tatpurusa-english-venue-prose_22.07.26.md).

## Thesis

The Pāṇinian coarse compound-type distinction (tatpuruṣa / bahuvrīhi / dvandva / avyayībhāva)
is recoverable from an unannotated Sanskrit corpus by manual classification with high
inter-pass reliability (**coarse κ = 0.93**), but the finer case-relation (vibhakti)
subtype of tatpuruṣa is recoverable only at the margin (**fine κ = 0.72, lower 95% CI 0.60 —
below the 0.70 pre-registered threshold**). Both figures are measured between two passes
from **the same LLM family** (Opus 4.8 and Sonnet 5), so they bound *within-family
reproducibility*, not independent inter-annotator reliability — a caveat this paper carries
in its abstract, not buried in a limitations footnote.

## Central results (all reproduced by the committed pipeline)

1. Coarse Pāṇinian-class agreement: **Cohen's κ = 0.9295, 95% CI [0.8356, 1.0], n = 120, 117/120 agree**.
2. Fine tatpuruṣa case-relation (vibhakti) agreement, on the n = 93 items both passes called tatpuruṣa: **Cohen's κ = 0.7201, 95% CI [0.6017, 0.8171], 73/93 agree**.
3. All 3 coarse disagreements sit on one boundary: karmadhāraya ↔ bahuvrīhi/dvandva (endocentric/exocentric).
4. Fine disagreements concentrate on 2 boundaries: ṣaṣṭhī↔karmadhāraya (5) and saptamī↔upapada (4), of 20 total.
5. Sample frame: 2-member compounds only, seed 20260715, drawn from 442,649 two-member compounds (841,052 total `Case=Cpd` tokens, 396,305 sentences) in the pinned DCS snapshot (commit `04e0778`, SHA-256 `8f3b06bd...`).

## Data inventory (claim → backing asset)

| Result | Backing asset (committed, frozen) |
|---|---|
| (1) coarse κ, CI, confusion | [`kappa_result.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/data/kappa_result.json) → `coarse` |
| (2) fine κ, CI, confusion | `kappa_result.json` → `fine` |
| (3)–(4) confusion matrices | `kappa_result.json` → `coarse_confusion` |
| (5) corpus denominators + snapshot pin | [`coverage_summary.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/data/coverage_summary.json) |
| per-item audit trail (240 decisions) | [`annotations_full.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/data/annotations_full.tsv) |
| item-level verdicts | [`validation_verdicts.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/data/validation_verdicts.tsv) |
| codebook | [`codebook_leitan.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/data/codebook_leitan.md) |
| generator scripts | [`sg_wf_008_compound_sample.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_008_compound_sample.py), [`sg_wf_008_kappa.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_008_kappa.py) |
| published RU pilot (source study) | [`sangram/articles/tatpurusha/index.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/tatpurusha/index.mdx), [v0.25.0](https://github.com/gasyoun/SanskritGrammar/releases/tag/v0.25.0) |
| method-design rationale (Path A/B/C) | [`SANGRAM_P4_TATPURUSA_PILOT_DESIGN_PATHS_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANGRAM_P4_TATPURUSA_PILOT_DESIGN_PATHS_2026.md) |
| same-model-family contamination caveat | [`GOLD_PROVENANCE_AUDIT_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/GOLD_PROVENANCE_AUDIT_2026H2.md) (H1272) |

## Section outline

1. **Introduction** — DCS marks compound *membership* and *segmentation* (`Case=Cpd`) but not Pāṇinian *type* (evidence-limit EM4); the only type-ish UD signal (`compound:coord`) covers 0.26% of compound tokens and cannot separate tatpuruṣa from karmadhāraya or identify bahuvrīhi. RQ: is the coarse/fine Pāṇinian type recoverable by manual classification, and how reliably?
2. **Related work** — agreement-metric framing (Artstein & Poesio 2008); prior Sanskrit compound-type-identification work (Krishna et al. 2016; Sandhan et al. 2023 DepNeCTI) — neither measures *inter-pass/inter-annotator* reliability of the classification itself; DCS/Hellwig as the corpus; LLM-as-annotator agreement literature, flagging that same-family agreement can be inflated relative to true inter-annotator reliability. States the verified gap explicitly (§ below).
3. **Data & method** — pinned DCS snapshot (commit, SHA-256, denominators); two-tier Path-B κ design (why coarse+fine, not a single fine κ); Leitan/Pāṇinian codebook; seeded sampling (seed 20260715, n=120, 2-member frame only); two blind LLM passes (Opus 4.8, Sonnet 5).
4. **Results** — coarse κ=0.9295 [0.8356–1.0] n=120; fine κ=0.7201 [0.6017–0.8171] n=93; confusion matrices; class distributions.
5. **Discussion / Limitations** — same-model-family contamination (not independent inter-annotator reliability); fine κ borderline (lower CI below threshold); 2-member-only frame; 0 avyayībhāva/kevala is a sampling-frame artifact, not a corpus fact, per the frozen RU pilot's §6.7.
6. **Conclusion** — coarse type is corpus-recoverable with high within-family reproducibility; fine vibhakti subtype is not reliably recoverable at this sample size/frame; next step is a true cross-vendor or human second annotator, not a bigger same-family sample.

## Venue candidates (ranked, human `@DECIDE`s — not chosen by this handoff)

1. **ISCLS** (International Sanskrit Computational Linguistics Symposium) — closest topical fit (Sanskrit NLP + Pāṇinian grammar).
2. **WSC-2027 computational track** (World Sanskrit Conference) — broader Indological audience, computational track exists.
3. **NLP4DH** — digital-humanities NLP audience, agreement-methodology framing fits well.
4. **LREC-COLING** — resource/evaluation framing (treebank-adjacent), higher bar, larger audience.

**Open fork (surfaced, not resolved):** [`ARTICLES.md`](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md) also flags a **⚖️ →GUIDE?** option — whether A64 becomes a methodology GUIDE (how to run a two-tier κ study for a Pāṇinian type layer) rather than a results paper. This handoff proceeds with the paper default; the GUIDE fork stays open for a human ruling.

## To 3/5 → 5/5

- **3/5 (this handoff):** English DRAFT with live-verified related work (≥6 citations fetched this session), numbers audited against the frozen JSONs, same-model-family caveat in abstract + limitations, venue proposed not chosen.
- **5/5:** a true cross-vendor or human second annotator (replacing/supplementing the Sonnet-5 pass) to measure genuine inter-annotator reliability rather than within-family reproducibility; venue `@DECIDE` + submission; author pass; ORCID/byline finalized.

---

_Dr. Mārcis Gasūns_
