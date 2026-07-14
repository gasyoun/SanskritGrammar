# Implementation — Digital Sanskrit Pedagogy, Wave 1

_Created: 14-07-2026 · Last updated: 14-07-2026_

File-level, step-ordered build sequence for wave-1 (W1a–W1d). Each step names the files it touches
and its dependency. Run under the [autonomy contract](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md)
(pick-default-and-log; commit → PR → merge; fence = csl-orig). **Work in a `git worktree`** (this
repo has a documented EmEditor watcher + concurrent-session contention); **commit with explicit
pathspec**; verify any site page with `npm run build` (only that proves MDX validity).

## W1a — Difficulty/ordering result + method paper (RQ1)

1. **Assemble inputs** (read-only): kosha [`lemma_frequency.tsv`](https://github.com/gasyoun/kosha/blob/main/data/frequency/lemma_frequency.tsv) (`core_rank`, `coverage_pct`); SanskritGrammar [`S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/S1_TEXTBOOK_SEQUENCING_TAU_RESULT.md) + `scripts/data/sequence_tau_*.csv`; VisualDCS verb-form frequency.
2. **`scripts/build_difficulty_ordering.py`** — compute a per-lemma/topic difficulty signal (frequency band × rare-form density × paradigm-class × sandhi-type); compute Kendall-τ between frequency-order and each textbook's lesson-order; extract the top divergences. Emit `data/difficulty_ordering/difficulty_ordering.tsv` + a stats JSON. *(UTF-8 stdout reconfigure; `encoding='utf-8'` on subprocess.)*
3. **`DIFFICULTY_ORDERING_RESULT.md`** (root, sibling of `S1_...`) — the result writeup: the τ table + ≥1 concrete divergence with its pedagogical reading (e.g. "textbook front-loads X but the corpus says learn Y first").
4. **`TolchelnikovTalmud_2026/papers/DifficultyOrdering_A63/OUTLINE_difficulty-ordering_A63.md`** — readiness-2 skeleton with a data-inventory table (each claimed result → the committed asset backing it) + venue line. *(`.md`, aggregate numbers only — rights.)*
- **Depends on:** kosha frequency layer + S1 (both exist). **Unblocks:** difficulty scorer (Wave 2), RQ4.

## W1b — A62 agenda paper draft

1. **`TolchelnikovTalmud_2026/papers/DigitalPedagogyAgenda_A62/OUTLINE_digital-sanskrit-pedagogy-agenda_A62.md`** — scaffold from the metadoc: §survey (asset inventory, metadoc §3), §hypotheses (RQ1–RQ4, metadoc §5, cross-linked to SG-H1…SG-H9), §evaluation design (RQ4), §gaps (metadoc §6).
2. **Data-inventory table** — each claimed survey fact → its committed source (the metadoc rows).
3. **Venue candidates** line (e.g. Lexikos / eLex / a Sanskrit-CL / DH venue) — a human picks.
- **Depends on:** the metadoc (exists). **Unblocks:** the field's print identity.

## W1c — Zaliznyak-made-learnable on-ramp

1. **`TolchelnikovTalmud_2026/ZALIZNYAK_ONRAMP_DESIGN.md`** (+ `.meta.md`) — the design: a graded, minimal-notation path into Ряд → Тип → seṭ; progressive disclosure with "one tap deeper" into the full [Талмуд](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026) chapters. State the simplification rules (what notation is deferred, what stays).
2. **On-ramp `.mdx` page(s)** — a short graded sequence reusing the existing widgets [AblautMachine / SetTree](https://github.com/gasyoun/SanskritGrammar/tree/main/src/components/talmud) at minimal settings; each step links deeper to its Талмуд section.
3. **Wire into Docusaurus** — add to the sidebar; the on-ramp sits *before* the Талмуд in the ladder.
4. **`npm run build`** green; "one tap deeper" links resolve; no new broken links.
- **Depends on:** *Очерк*/*Конспект* + Talmud widgets + Zaliznyak index (all exist). **Unblocks:** the A2→B1 formal-grammar rung.

## W1d — Consolidated last-mile pipeline (spec)

1. **`docs/LAST_MILE_PIPELINE_SPEC.md`** — spec the kosha→learner hop: reader-as-a-service + frequency-SRS deck export + difficulty scorer → a Systema course unit. Name the contract (data/API handoff) between kosha (open layer) and Systema (product).
2. **One-rung demo path** — specify the minimal integration to demonstrate a single rung end-to-end (e.g. B1 subhāṣita: text → segment → click-gloss → frequency-ordered SRS deck).
3. **Fence check** — **spec only**; do **not** modify Systema production code in wave-1. The spec is the deliverable; the wiring is Wave 2 after human review.
- **Depends on:** kosha reader/segmenter/frequency + Systema SRS (exist); W1a difficulty signal. **Unblocks:** Wave-2 integration.

## Ordering

W1b and W1a can run in parallel (independent inputs). W1c is independent. **W1d runs last** in wave-1
(it references W1a's difficulty signal and touches the most parts). Each ships as its own PR under
the merge-autonomously authority.

---

_Dr. Mārcis Gasūns_
