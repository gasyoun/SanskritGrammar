# Metadoc — ZALIZNYAK_ONRAMP_DESIGN.md

_Created: 14-07-2026 · Last updated: 14-07-2026_

Companion record for
[`ZALIZNYAK_ONRAMP_DESIGN.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/ZALIZNYAK_ONRAMP_DESIGN.md).

## Purpose
The design-of-record for the Zaliznyak-made-learnable on-ramp — the graded, minimal-notation front
door that sits before the Толчельников *Талмуд* (progressive disclosure). Explains what the on-ramp
keeps vs. defers and why, so a future editor extending it does not re-derive the simplification policy.

## Audience
Editors of the SanskritGrammar pedagogy tree; anyone extending the on-ramp (more steps, widget props,
CEFR-rung alignment) or auditing why a concept is/ isn't in the first pass.

## Provenance
- Wave-1 item **W1c** of the digital-Sanskrit-pedagogy field (handoff
  [H915](https://github.com/gasyoun/Uprava/blob/main/handoffs/H915-Opus_SanskritGrammar_pedagogy-w1c-zaliznyak-onramp_14.07.26.md)).
- Built on the pre-existing spec
  [`student-roadmap.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/student-roadmap.md)
  (5 cheat sheets + 7-step self-check) — the on-ramp is the "three questions" distillation of its
  Master Pipeline.
- Author: Opus 4.8 (`claude-opus-4-8[1m]`).

## Ranked improvement backlog
1. **Widget "minimal mode" props** — `AblautMachine` / `SetTree` are zero-prop and always render the
   full example set; add an optional prop to restrict to the 4 on-ramp series (A₁ I₁ U₁ R₁) so the
   on-ramp widget matches its pocket table. *(Requires editing the widget source — deferred from W1c
   as out of the reuse-only scope.)*
2. **CEFR-rung tags** — align the four on-ramp pages to explicit A1/A2 rungs once the field taxonomy
   (metadoc §таксономия) is applied to the Талмуд tree.
3. **A worked "собери форму" exercise** — one end-to-end example (root → grade → seṭ → surface form)
   as an interactive check, reusing `Talmud-uroky.mdx` exercise style.
4. **Reduplication teaser** — a single "what comes next" pointer to chapter IV, so the on-ramp's edge
   toward the perfect/desiderative is visible without pulling reduplication into wave-1.

## Limitations
- **Notation coverage is intentionally partial** — the on-ramp does not teach the MST generative
  record; a learner who only reads the on-ramp cannot yet parse a full Талмуд derivation. That is by
  design (the "one tap deeper" links bridge the gap), not a defect.
- **No learning-gain measurement yet** — per the field's RQ4 (A32), "this on-ramp teaches better"
  stays a hypothesis until an evaluation metric exists.
- **Widgets show the full data set**, not the 4-series subset (see backlog #1) — the pocket table and
  the widget can therefore diverge in breadth on the same page.

## Related docs
- [`student-roadmap.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/student-roadmap.md) — the cheat-sheet spec the on-ramp distils.
- [`zalizniak-concordance.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/zalizniak-concordance.mdx) — Талмуд↔Zaliznyak § crosswalk; source of the `ZRef` ranges.
- [IMPLEMENTATION §W1c](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_DIGITAL_SANSKRIT_PEDAGOGY_WAVE1.md) · [VERIFICATION](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md).

## Revision history
| Date | Change | By |
|---|---|---|
| 14-07-2026 | Created with the on-ramp (design + 4 `.mdx` pages + `_category_.json`), W1c. | Opus 4.8 (`claude-opus-4-8[1m]`) |

---

_Dr. Mārcis Gasūns_
