# Roadmap — Digital Sanskrit Pedagogy (2026–2028)

_Created: 14-07-2026 · Last updated: 19-07-2026_

Waves for the [digital Sanskrit pedagogy field](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md).
Cover + decisions: [`docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md).
Each deliverable states what unblocks it.

## Wave 0 — Establish the field ✅ (14-07-2026)

Field metadoc + layered plan + registration (MEGABOOK §2.10/§2.9, ARTICLES A62, GTD straddle tier,
ROADMAP_INDEX) + wave-1 handoffs minted. *Unblocked by:* the three-audit prior-art sweep. **Done.**

## Wave 1 — First results + the on-ramp (2026 H2)

| Deliverable | Unblocked by |
|---|---|
| **W1a** Difficulty/ordering dataset + analysis + method paper skeleton (RQ1) | kosha `core_rank` + SanskritGrammar textbook-τ (both exist) |
| **W1b** A62 agenda paper draft (survey + hypotheses + evaluation design) | the field metadoc (exists) |
| **W1c** Zaliznyak-made-learnable on-ramp (graded, minimal-notation; Талмуд as deep tier) | *Очерк*/*Конспект* + Talmud widgets + Zaliznyak index (all exist) |
| **W1d** Consolidated last-mile pipeline spec (kosha → learner hop) | kosha reader/segmenter/frequency + Systema SRS (exist); W1a difficulty signal |

## Wave 2 — Evaluation + generation (2027 H1)

| Deliverable | Unblocked by |
|---|---|
| First **user study** proving learning gain (RQ4, paper A32) | W1a/W1c shipped (something to evaluate) |
| **Difficulty scorer** productionised (score any text → target-level reading set) | W1a result |
| **Auto-drill generation** with verified answer keys (RQ2) | drill schema + segmenter/paradigm engines (exist) |
| Reading-pack generator (Gītā 1, Nala 1) live | kosha reading-pack data un-gated |

## Wave 2 additions — attested-drills + RU corpus layer 🟡 (staged 19-07-2026 via `/ask-batch`)

Three queued builds sharpening Wave 2's generic "auto-drill generation" into specific,
attestation-first surfaces (rulings in
[`ASK_BATCH_STAGING_PEDAGOGY_2026-07.md`](https://github.com/gasyoun/Uprava/blob/main/ASK_BATCH_STAGING_PEDAGOGY_2026-07.md);
file-level steps:
[`docs/IMPLEMENTATION_DIGITAL_SANSKRIT_PEDAGOGY_ATTESTED_RU_ADDITIONS.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_DIGITAL_SANSKRIT_PEDAGOGY_ATTESTED_RU_ADDITIONS.md)):

| Deliverable | Delta vs prior art | Handoff |
|---|---|---|
| **W2-add-a — Attested-cell declension drills.** G2 cell coverage (10.44 % of lemma×24-cell space attested) × kosha frequency × Zaliznyak stem classes → drill only what the corpus shows | kosha H946 drills engine-generated forms; G2's only consumers are SG-MO articles | [H1296](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1296-Opus_SanskritGrammar_sangram-attested-cell-declension-drills_19.07.26.md) (Opus, queued) |
| **W2-add-b — Corpus-linked methodichka.** Kochergina/Apte companions gain a per-lemma corpus layer: DCS frequency band + one attested example with RU rendering | H1258/H1275 apply author *review notes*; this adds a new data layer (`--allow-dup` ruled at mint) | [H1297](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1297-Fable_SanskritGrammar_metodichka-corpus-linked-kochergina-apte_19.07.26.md) (Fable, queued) |
| **W2-add-c — Samāsa bracket-method trainer.** Right-to-left vigraha ladder (klammeruebersetzung method) over attested DCS compounds with RU constituent glosses | kosha H948 drills identify/split; this teaches the *resolution method* | [H1298](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1298-Opus_SanskritGrammar_sangram-samasa-bracket-method-trainer_19.07.26.md) (Opus, queued) |

## Wave 3 — Depth + the machine index (2027 H2)

| Deliverable | Unblocked by |
|---|---|
| **Pāṇini sūtra ↔ corpus** pedagogy surface (kosha Concordance Q4) | kosha concordance roadmap Q4 |
| `pedagogy_assets.tsv` — the machine index driving the metadoc §3 rows + §4 derived views | metadoc stable (exists) |
| Commentary-reading interface (C1/C2) | CommentaryStrategies apparatus maturing |

## Wave 4 — Audio + adaptivity (2028)

| Deliverable | Unblocked by |
|---|---|
| **Audio / śikṣā** — TTS or recorded recitation → unblock A0–A2 (RQ agenda §3.7) | a human GO on the audio-source @DECIDE (TTS vs reciter) + external content |
| Adaptive learning contour with provable provenance (MEGABOOK §2.9 future) | evaluation harness (Wave 2) + learner corpus |
| Learner corpus + error analysis | a live learner surface producing data |

## Non-goals (explicit)

- **Not** building/owning the LMS — [Systema-Sanscriticum](https://github.com/gasyoun/Systema-Sanscriticum) owns it; the field feeds it.
- **Not** rebuilding dictionaries, corpus, or morphology engines — consume CDSL/DCS/vidyut/Heritage/Zaliznyak-index.
- **Not** producing audio content in-house — audio is external content (Wave 4), the field builds the *pedagogy* around it.
- **Not** a new SRS engine — Systema "Saraswati" (FSRS) + kosha Anki export already exist.
- **Not** touching csl-orig (fence); **not** making anything public or publishing rights-gated corpora unattended.

---

_Dr. Mārcis Gasūns_
