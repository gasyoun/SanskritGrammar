# Talmud санскрита — Improvement Plan (interactive companion to Zaliznyak)

_Created: 06-07-2026 · Last updated: 06-07-2026_

Turning I.E. Tolchelnikov's *Talmud санскрита* (a generative, Meaning-Text-Theory
formal grammar of Sanskrit morphonology, Whitney-root-based) into a scaffolded,
interactive Docusaurus **companion** to A.A. Zaliznyak's *Грамматический очерк
санскрита* (1978), for **post-beginner self-study** readers.

**Decisions locked with MG (06-07-2026):** audience = post-beginner self-study ·
role = companion *on top of* Zaliznyak (cross-referenced, not replacing) · format
= interactive Docusaurus site · scope = **Whitney-only, deepened** (no reading/vocab
strand, no broadened reference-grammar coverage).

**Standing instruction (MG, 06-07-2026):** *reuse the rich data already sitting in
sibling Sanskrit repos, and surface every data-derived enrichment as a **footnote
proposal for Ivan (I.E. Tolchelnikov) to approve** — never silently merge analysis
into the author's text.*

---

## What these two books are, and why they sit together

- [Zaliznyak *Очерк* (1978)](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/Zaliznyak-Ocherk_29-11-20-aligned.mdx)
  is the founding Russian **formal-structural** description of Sanskrit inflection:
  the морфонология layer, the positional strong/middle/weak system, ablaut grades as
  a calculus. It is a terse reference (~250 §§).
- [Tolchelnikov *Talmud* (2026)](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/talmud-refactoring.md)
  runs that machinery as a **generative engine**: every ending imposes a
  *морфологическая позиция 1/2/3*; every root carries a *Ряд* (ablaut series A–N),
  a *Тип* (s/a/v), and a *seṭ/aniṭ* flag; from those coordinates the surface form is
  *computed*. Framed explicitly in Mel'čuk's Meaning-Text Theory, deliberately
  **Whitney-root-only** (Monier-Williams excluded).

**One line:** the Talmud is Zaliznyak's formal grammar turned into a generative
engine and a drill course. That lineage is the spine of this plan.

---

## Rich data to reuse (do NOT rebuild)

Canonical, already-structured, **read-only** sources — consume, never edit:

| Asset | Path | Gives the Talmud |
|---|---|---|
| Whitney roots table | [`WhitneyRoots/crosswalk/roots.csv`](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/roots.csv) (+ `roots.sqlite`, `roots.ttl`) | `whitney_no`, gaṇa `class`, `ppp`, **`dcs_freq`/`dcs_rank`**, `section_refs`, `warnemyr_url`, `mw_id`, `apte_id` — the backbone of Appendix 1 |
| Primary lexicon | [`WhitneyRoots/src/app_data.json`](https://github.com/gasyoun/WhitneyRoots/blob/main/src/app_data.json) | root · meaning · class · ppp · grammar_ref |
| Paradigms / affixes | [`WhitneyRoots/src/paradigms.json`](https://github.com/gasyoun/WhitneyRoots/blob/main/src/paradigms.json), [`affix_data.json`](https://github.com/gasyoun/WhitneyRoots/blob/main/src/affix_data.json), [`participle_index.json`](https://github.com/gasyoun/WhitneyRoots/blob/main/src/participle_index.json) | answer-key generation, widget validation |
| PPP validation | [`WhitneyRoots/crosswalk/ppp_validation.json`](https://github.com/gasyoun/WhitneyRoots/blob/main/crosswalk/ppp_validation.json) | seṭ/aniṭ evidence (advisory) |
| Root index + glosses | [`WhitneyRoots/Whitney-linked-2026.md`](https://github.com/gasyoun/WhitneyRoots/blob/main/Whitney-linked-2026.md) | linked headword list |

**Guardrails (from [WhitneyRoots/CLAUDE.md](https://github.com/gasyoun/WhitneyRoots/blob/main/CLAUDE.md)):**
root-class fields are **revert-prone** (Phase 8 reverted 120/139 empirical class
adds) — never hand-edit `app_data.json`/`roots.csv` class fields; `scripts/sanskrit_util.py`
is a **canonical donor** for the org — don't touch it. This plan only *reads*
WhitneyRoots and builds a **new derived asset inside the Talmud repo**.

**Gap the Talmud adds on top:** the *Ряд* (A–N) and *Тип* (s/a/v) labels are
Zaliznyak/Tolchelnikov **analytical overlays** absent from WhitneyRoots. So Phase 3
is an **enrichment crosswalk**, not a digitization.

---

## Phases (run order: 0 → 3 → 2 → 1 → 4 → 5; the Whitney crosswalk is the bottleneck)

### Phase 0 — Spine & scaffold
1. Docusaurus book scaffold (reuse the books-7&8 `site_tools.py` / `/docx-to-md`
   pattern already in this repo), one MDX per Раздел I–X + Appendices 1–2, authored
   from [talmud-refactoring.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/talmud-refactoring.md)
   (keep `Talmud-2.1.6.mdx` as raw archive).
2. **Zaliznyak cross-reference spine** — a concordance mapping each Talmud section →
   the Zaliznyak §§ it formalizes, rendered both as a standalone page and as inline
   `<ZRef>` callouts. Highest-leverage deliverable for "companion on top of Zaliznyak".

### Phase 3 — Enrichment crosswalk (critical path; the "deepen" work)
Build **`whitney_talmud.json`** in the Talmud repo: join `roots.csv` (whitney_no,
class, ppp, dcs_freq, section_refs) with the Talmud's Ряд/Тип/seṭ overlay. This one
asset simultaneously becomes Appendix 1, the widget data source, and the answer-key
generator. Complete Appendix 1 (currently a stub ending *"(таблица корней от AKṢ до
HṚ)"*) and Appendix 2's fragment from it. Use `dcs_freq`/`dcs_rank` to mark the
high-frequency roots students should meet first.

### Phase 2 — Interactive components (build order = reuse order)
Spec'd in [visual-grammar.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/visual-grammar.md):
**Ablaut machine** (§II, build first — every later chapter calls it) → **seṭ/aniṭ
decision tree** (§III) → **Reduplication sandbox** (§IV) → **Sandhi collider** (§VII)
→ **Heteroclisis stem-map** (§X, needs Phase-3 data, build last). All driven by
`whitney_talmud.json` so text and widgets never diverge.

### Phase 1 — Re-scaffold for self-study
Impose a fixed micro-pattern per section: *motivating Whitney root → rule → flowchart
→ 2 worked traces → drill → answer key*. Promote the [student-roadmap.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/student-roadmap.md)
Master Pipeline (Раздел VIII) to the front as the map-before-territory, each step
hyperlinked. Add a **§0 notation onboarding** ({√}, [P][E][F], positions, rows, types)
taught on one running root before any real content.

### Phase 4 — Drill bank + answer keys
[Talmud-uroky.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/Talmud-uroky.mdx)
has **empty answer brackets** (Упр. 4 №2/№3/№5 `= []`) — a self-study reader is
stranded. Fill every `[]` with a **step trace** (not just the result), generated and
checked against `paradigms.json`/`participle_index.json`; add `<details>` self-check
reveals; tag each drill to its section + widget.

### Phase 5 — Hygiene & integration
Wire both books into the Docusaurus include (as books 7 & 8 were); seed a Talmud
`errata.yml` via the `/errata` skill (Zaliznyak already has one; Talmud has none);
add a guṇa/vṛddhi ↔ position/grade ↔ Zaliznyak-term glossary.

---

## Footnote-proposal workflow (human-gated, for Ivan's approval)

Every data-derived enrichment is a **proposal Ivan approves**, never a silent edit —
mirroring the repo's existing `errata.yml` pattern. Maintain
**`footnote-proposals/proposals.yml`** in the Talmud repo:

```yaml
- id: FN-0001
  target: { section: "II", root: "√kṛ" }        # or appendix row
  type: freq-note | whitney-ref | set-correction | missing-root | paradigm-check
  proposal: "√kṛ is DCS-rank 3 (very high frequency) — teach in the first cohort."
  evidence: "WhitneyRoots/crosswalk/roots.csv row whitney_no=… ; dcs_rank=3"
  status: pending            # pending → approved (Ivan) → applied
  approved_by: null
```

Approved proposals become MDX footnotes with source attribution; rejected ones stay
logged. Surface the pending queue to Ivan as a `/review-sheet` HTML voting sheet.
**No enrichment enters the author's running text without an `approved_by: Ivan` line.**

---

## Honest pedagogical caveat (kept in view, not "fixed")

The Talmud is formalism-first — a generative engine, not a language-acquisition path;
notation is a barrier taller than the Sanskrit it describes. For the chosen
post-beginner self-study audience that density is acceptable **only** with the
scaffolding of Phases 1–4. This plan keeps the Whitney-only purity MG chose and buys
learnability through scaffolds, cross-references, and widgets — not by diluting the
formalism.

_Dr. Mārcis Gasūns_
