# Roadmap — Digital Sanskrit Pedagogy (2026–2028)

_Created: 14-07-2026 · Last updated: 25-09-2026_

> **Truth-pass 27-08-2026** (Grok 4.6 `grok-4.6`). Closed references checked against the combined registry. Kept in place ([FINDINGS §475](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md) clause 3). Not archived.

> **Verdict pass 24-09-2026** (OxAlpha `opencode/z-ai/glm-5.3-flash`, [H5364](https://github.com/gasyoun/Uprava/blob/main/handoffs/H5364-OxAlpha_SanskritGrammar_rm-verdict-digital-sanskrit-pedagogy-2026-202_24.09.26.md)). Verdict = **REFRESH** (not archive): Wave 0, Wave 1 (all four deliverables) and the Wave 2 additions are shipped with cited evidence below; Wave 2's remaining two deliverables and all of Wave 3/Wave 4 are genuine unminted prose work with no merged PR or live H### against them (checked via `hub_grep.py` — zero hits on every remaining deliverable's own wording). Rewritten as gated checkboxes under "What is left"; each human gate has a dated GTD row in [Uprava/GTD_NEXT_ACTIONS.md](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md).

Waves for the [digital Sanskrit pedagogy field](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md).
Cover + decisions: [`docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md).
Each deliverable states what unblocks it.

## Wave 0 — Establish the field ✅ (14-07-2026)

Field metadoc + layered plan + registration (MEGABOOK §2.10/§2.9, ARTICLES A62, GTD straddle tier,
ROADMAP_INDEX) + wave-1 handoffs minted. *Unblocked by:* the three-audit prior-art sweep. **Done.**

## Wave 1 — First results + the on-ramp (2026 H2) ✅ (all four shipped, verified 24-09-2026)

| Deliverable | Unblocked by | Evidence |
|---|---|---|
| **W1a** Difficulty/ordering dataset + analysis + method paper skeleton (RQ1) | kosha `core_rank` + SanskritGrammar textbook-τ (both exist) | ✅ [H913](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H913-Opus_SanskritGrammar_pedagogy-w1a-difficulty-ordering_14.07.26.md) archived (RQ1 confirmed, cited from A62 §survey) |
| **W1b** A62 agenda paper draft (survey + hypotheses + evaluation design) | the field metadoc (exists) | ✅ [H914](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H914-Fable_SanskritGrammar_pedagogy-w1b-agenda-paper-a62_14.07.26.md) archived; A62 now 4/5 in [ARTICLES.md](https://github.com/gasyoun/Uprava/blob/main/ARTICLES.md), awaiting MG sign-off ([SIGNOFF_A62_author_pass.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/DigitalPedagogyAgenda_A62/SIGNOFF_A62_author_pass.md)) for 5/5 — that residual is A62's own, not this roadmap's |
| **W1c** Zaliznyak-made-learnable on-ramp (graded, minimal-notation; Талмуд as deep tier) | *Очерк*/*Конспект* + Talmud widgets + Zaliznyak index (all exist) | ✅ [H915](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H915-Opus_SanskritGrammar_pedagogy-w1c-zaliznyak-onramp_14.07.26.md) archived |
| **W1d** Consolidated last-mile pipeline spec (kosha → learner hop) | kosha reader/segmenter/frequency + Systema SRS (exist); W1a difficulty signal | ✅ [H916](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H916-Opus_SanskritGrammar_pedagogy-w1d-last-mile-pipeline_14.07.26.md) archived |

## Wave 2 — Evaluation + generation (2027 H1)

| Deliverable | Unblocked by |
|---|---|
| First **user study** proving learning gain (RQ4, paper A32) | W1a/W1c shipped (something to evaluate) |
| ~~**Difficulty scorer** productionised (score any text → target-level reading set)~~ ✅ **DONE** — kosha H949 shipped `data/difficulty/reading_pack_difficulty.json` (4-axis scoring), consumed by Systema's `/reading/kosha-demo` (H965) | W1a result |
| **Auto-drill generation** with verified answer keys (RQ2) | drill schema + segmenter/paradigm engines (exist) |
| ~~Reading-pack generator (Gītā 1, Nala 1) live~~ ✅ **DONE** — the Nala-1/Gītā reading packs already existed from H848/H871 (found stale when H959 built the Systema-side reader route) | kosha reading-pack data un-gated |

## Wave 2 additions — attested-drills + RU corpus layer 🟡 (staged 19-07-2026 via `/ask-batch`)

Three queued builds sharpening Wave 2's generic "auto-drill generation" into specific,
attestation-first surfaces (rulings in
[`ASK_BATCH_STAGING_PEDAGOGY_2026-07.md`](https://github.com/gasyoun/Uprava/blob/main/ASK_BATCH_STAGING_PEDAGOGY_2026-07.md);
file-level steps:
[`docs/IMPLEMENTATION_DIGITAL_SANSKRIT_PEDAGOGY_ATTESTED_RU_ADDITIONS.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_DIGITAL_SANSKRIT_PEDAGOGY_ATTESTED_RU_ADDITIONS.md)):

| Deliverable | Delta vs prior art | Handoff |
|---|---|---|
| **W2-add-a — Attested-cell declension drills.** G2 cell coverage (10.44 % of lemma×24-cell space attested) × kosha frequency × Zaliznyak stem classes → drill only what the corpus shows | kosha H946 drills engine-generated forms; G2's only consumers are SG-MO articles | [H1296](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1296-Opus_SanskritGrammar_sangram-attested-cell-declension-drills_19.07.26.md) (Opus, queued) |
| **W2-add-b — Corpus-linked methodichka.** Kochergina/Apte companions gain a per-lemma corpus layer: DCS frequency band + one attested example with RU rendering | H1258/H1275 apply author *review notes*; this adds a new data layer (`--allow-dup` ruled at mint) | [H1297](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1297-Fable_SanskritGrammar_metodichka-corpus-linked-kochergina-apte_19.07.26.md) (Fable, queued) |
| **W2-add-c — Samāsa bracket-method trainer.** Right-to-left vigraha ladder (klammeruebersetzung method) over attested DCS compounds with RU constituent glosses | kosha H948 drills identify/split; this teaches the *resolution method* | [H1298](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1298-Opus_SanskritGrammar_sangram-samasa-bracket-method-trainer_19.07.26.md) (Opus, queued) |

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

## What is left (verdict pass 24-09-2026 — gated checkboxes, replaces the loose Wave 2/3/4 prose above where a deliverable has no live handoff)

Zero of the six rows below have a merged PR or a live H### against their own wording
(checked via `hub_grep.py`, [H5364](https://github.com/gasyoun/Uprava/blob/main/handoffs/H5364-OxAlpha_SanskritGrammar_rm-verdict-digital-sanskrit-pedagogy-2026-202_24.09.26.md)) — this is the unminted-prose table the verdict pass found, kept as the acceptance record.

- [x] **Wave 2 — auto-drill generation with verified answer keys (RQ2).** ✅ 25-09-2026 (Sonnet 5, A07 drain unit) — [`sangram/data/unified_drills/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/data/unified_drills) unifies the three existing engines (declension/samasa/sandhi) into one schema with a re-derived `verified` answer-key flag per row: 46,400/50,582 (91.7%) verified, non-fabrication guaranteed by test. PR: (opened same pass, see commit history).
- [ ] **Wave 2 — first user study proving learning gain (RQ4, paper A32).** Human-gated: needs a live learner cohort/consent design, not something an agent can run unattended. GTD row: [Uprava/GTD_NEXT_ACTIONS.md](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md) `@WAITING H5364-W2-RQ4`.
- [ ] **Wave 3 — Pāṇini sūtra ↔ corpus pedagogy surface.** Blocked on an external prerequisite (kosha Concordance Q4) that has not itself shipped — re-check when kosha's Concordance roadmap reports Q4 done.
- [ ] **Wave 3 — `pedagogy_assets.tsv` machine index.** Not human-gated — the metadoc is stable per the row above; open only because no handoff has been minted for it yet.
- [ ] **Wave 3 — Commentary-reading interface (C1/C2).** Blocked on an external prerequisite (CommentaryStrategies apparatus maturing) that has not itself shipped.
- [ ] **Wave 4 — Audio/śikṣā, adaptive learning contour, learner corpus (all three).** Human-gated / prerequisite-gated: audio needs an explicit MG @DECIDE (TTS vs reciter) plus external content; adaptivity needs the Wave-2 evaluation harness (RQ2/RQ4 above) plus a learner corpus; the learner corpus itself needs a live learner surface producing data — none exists yet. GTD row: [Uprava/GTD_NEXT_ACTIONS.md](https://github.com/gasyoun/Uprava/blob/main/GTD_NEXT_ACTIONS.md) `@WAITING H5364-W4-audio` (audio-source decide) and `@WAITING H5364-W4-adaptive` (blocked on RQ2/RQ4 + learner corpus, no date — re-check when Wave 2 ships).

No real calendar-dated trigger is named anywhere in the source roadmap for any of the six rows above (only prerequisite conditions), so none qualifies for a silent-until-\<date\> verdict per ruling 3 — they stay open gated checkboxes instead.

## Non-goals (explicit)

- **Not** building/owning the LMS — [Systema-Sanscriticum](https://github.com/gasyoun/Systema-Sanscriticum) owns it; the field feeds it.
- **Not** rebuilding dictionaries, corpus, or morphology engines — consume CDSL/DCS/vidyut/Heritage/Zaliznyak-index.
- **Not** producing audio content in-house — audio is external content (Wave 4), the field builds the *pedagogy* around it.
- **Not** a new SRS engine — Systema "Saraswati" (FSRS) + kosha Anki export already exist.
- **Not** touching csl-orig (fence); **not** making anything public or publishing rights-gated corpora unattended.

---

_Dr. Mārcis Gasūns_
