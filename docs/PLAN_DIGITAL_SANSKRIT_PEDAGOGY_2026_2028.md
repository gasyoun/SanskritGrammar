# Plan — Digital Sanskrit Pedagogy as a priority research field (2026–2028)

_Created: 14-07-2026 · Last updated: 14-07-2026_

**This is the cover/index** of the layered plan that establishes and builds out
[digital Sanskrit pedagogy](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md)
as a field. Authored via [`/ask`](https://github.com/gasyoun/claude-config/blob/main/commands/ask.md):
a 4-round up-front interview (**17 rulings, zero blocking forks**) then this layered plan, complete
enough for a fresh agent to execute wave-1 unattended. A wave-1 execution handoff points its
starter line here.

**Goal in one paragraph.** Name and consolidate the ecosystem's scattered pedagogy work into one
research-and-integration field; produce measurable findings (papers) *and* close the "last mile"
to the learner; register it as a straddle-tier priority (research T1 / product T0). The field
metadoc is the definition; this plan is how it gets built.

## Layer docs

- **Field definition (the metadoc):** [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md)
- **Roadmap (waves):** [`docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md)
- **Architecture (data model + how views derive):** [`docs/ARCHITECTURE_DIGITAL_SANSKRIT_PEDAGOGY.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_DIGITAL_SANSKRIT_PEDAGOGY.md)
- **Implementation (wave-1 file-level steps):** [`docs/IMPLEMENTATION_DIGITAL_SANSKRIT_PEDAGOGY_WAVE1.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_DIGITAL_SANSKRIT_PEDAGOGY_WAVE1.md)
- **Verification (acceptance + risks):** [`docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md)

## Decisions taken (the 17 rulings — the execution agent trusts these without re-deriving)

| # | Decision | Ruling | Rationale |
|---|---|---|---|
| 1 | Field identity | **Research + integration** | Produces both papers and the last-mile pipeline; matches the real research→education flow |
| 2 | Metadoc home | **SanskritGrammar** (root), org-wide scope | The pedagogy-first repo; registration routes through Uprava hubs |
| 3 | Scope | **Org-wide, research-anchored** | Map all assets incl. Systema; field's deliverables = research/data/tool layer; Systema stays a T0 consumer |
| 4 | Existing maps | **Sit above, consolidate by reference** | No duplication; harmonize the 3 maps, add the research/gap layer |
| 5 | Research spine (wave-1) | **RQ1 difficulty/ordering · RQ2 drill-gen · RQ3 textbook-vs-corpus · RQ4 evaluation** | Four falsifiable questions; data already exists for RQ1/RQ3 |
| 6 | Taxonomy | **Aspect-primary + layered tags** | Matrix & learner-journey views derive from one tagged dataset |
| 7 | Layers per entry | CEFR rung + status (default) + **NLP capability + research-Q + traditional discipline + owning repo** | Enables the capability, discipline, journey, and matrix pivots |
| 8 | Aspects prioritized | morphology · vocab/SRS · reading · Pāṇini · **Zaliznyak-made-learnable** · (sandhi already active) | The interview's priority set; +6 secondary aspects for completeness |
| 9 | Audio | **Named gap + research-Q, not wave-1** | Biggest gap but needs external content; on the agenda, not the first build |
| 10 | MEGABOOK | **New §2.10 + strengthen §2.9** | Append-only: new thesis names the field; §2.9 (rated "усилить") is its foundation |
| 11 | Priority tier | **Straddle** — research/data/tool T1, product T0 | Matches MEGABOOK's research/product split |
| 12 | Papers | **A62 agenda · elevate A32 · new difficulty/ordering method paper · A60 flagship** | A62 defines the field; A60 (4/5) is the first result; A32 is evaluation |
| 13 | Ambition | Metadoc + layered plan + registration + **wave-1 handoffs** | Plan now, build unattended later |
| 14 | Wave-1 builds | **All four** (W1a difficulty result · W1b A62 draft · W1c Zaliznyak on-ramp · W1d last-mile pipeline) | The interview selected all four for wave-1 |
| 15 | Ambiguity policy | **Pick marked default + log** | Keeps the unattended run moving; human reviews logged calls |
| 16 | Merge authority | **Commit → PR → merge autonomously** | The user explicitly overrode the standing "don't merge unless asked" for these handoffs |
| 17 | Fence | **csl-orig only** (+ standing publish/rights gates apply globally) | Only added build-scope fence; public-deploy & rights-gated publish stay behind publish-safety-check |

## Wave-1 builds

- **W1a — Difficulty/ordering result + method paper (RQ1).** Build the pedagogical-difficulty / optimal-order dataset + analysis from kosha `core_rank` + SanskritGrammar textbook-τ; draft the method paper. Data exists — fastest to a measurable finding.
- **W1b — A62 agenda paper draft.** Draft "Digital Sanskrit pedagogy: a research agenda" — asset survey + falsifiable hypotheses + evaluation design. The print companion to the metadoc.
- **W1c — Zaliznyak-made-learnable on-ramp.** Prototype the gentler on-ramp into Ряд/Тип/seṭ — simpler than the Талмуд, which stays as the deep-dive tier behind it (progressive disclosure).
- **W1d — Consolidated last-mile pipeline.** Spec/wire the kosha→learner hop MEGABOOK flags as unclosed. Highest integration value; touches the most parts — sequence it last in wave-1.

**Execution handoffs** (minted 14-07-2026; [registry](https://github.com/gasyoun/Uprava/blob/main/handoffs/README.md)):

| Handoff | Build | Executor |
|---|---|---|
| [H912](https://github.com/gasyoun/Uprava/blob/main/handoffs/H912-Opus_SanskritGrammar_digital-pedagogy-field-established_14.07.26.md) | Parent — field established (this session, done) | Opus 4.8 |
| [H913](https://github.com/gasyoun/Uprava/blob/main/handoffs/H913-Opus_SanskritGrammar_pedagogy-w1a-difficulty-ordering_14.07.26.md) | **W1a** difficulty/ordering result + method paper | Opus 4.8 |
| [H914](https://github.com/gasyoun/Uprava/blob/main/handoffs/H914-Fable_SanskritGrammar_pedagogy-w1b-agenda-paper-a62_14.07.26.md) | **W1b** A62 agenda paper draft | Fable 5 |
| [H915](https://github.com/gasyoun/Uprava/blob/main/handoffs/H915-Opus_SanskritGrammar_pedagogy-w1c-zaliznyak-onramp_14.07.26.md) | **W1c** Zaliznyak-made-learnable on-ramp | Opus 4.8 |
| [H916](https://github.com/gasyoun/Uprava/blob/main/handoffs/H916-Opus_SanskritGrammar_pedagogy-w1d-last-mile-pipeline_14.07.26.md) | **W1d** last-mile pipeline spec | Opus 4.8 |

## The autonomy contract (what the unattended wave-1 agent runs under)

- **On unplanned ambiguity:** pick the plan's marked default and **log** the decision; press on. Do not halt.
- **Merge authority:** commit → open PR → **merge the green PR autonomously**, same pass (the user overrode the standing "don't merge unless asked" specifically for these wave-1 handoffs).
- **Stop conditions:** stop only on a hard blocker (missing data access, a failing build that a marked default can't resolve, or an action the fence forbids). Otherwise continue.
- **The fence (must NOT touch):** **csl-orig** source — never commit directly; any dictionary correction goes via the monthly queue. Standing **global** guardrails still bind independent of the fence: no making anything newly public (Pages/visibility) and no publishing rights-gated ("grey") corpus bulk without a human GO/NO-GO via [`/publish-safety-check`](https://github.com/gasyoun/claude-config/blob/main/commands/publish-safety-check.md) — an unattended agent does not trip those.
- **Provenance:** every deliverable records model tier+version; papers stay `.md` (not built as site pages) where source rights (e.g. Kochergina in-copyright) restrict to aggregate numbers only.

## Autonomy-readiness gate — verdict

Each wave-1 build has an architecture spec (ARCHITECTURE §), ordered steps (IMPLEMENTATION §), an
acceptance criterion (VERIFICATION §), and identified risks. Zero blocking forks remain (all 17
ruled). No scheduled build duplicates an existing asset (prior-art checked in the metadoc's asset
inventory). The autonomy contract covers the plausible ambiguities. **Gate: PASS** — wave-1 is
launchable unattended.

---

_Dr. Mārcis Gasūns_
