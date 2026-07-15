# Metadoc — RQ4_EVALUATION_PROTOCOL_2026.md

_Created: 15-07-2026 · Last updated: 15-07-2026_

Companion for [`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md).

## Purpose
The full study design for RQ4 (learning-gain + retention on-ramp-first vs Талмуд-first), the digital-pedagogy field's falsifiability backbone. Closes A62's own "5/5: RQ4 evaluation protocol specified in full" checklist item. **§6.1–6.3 ruled 15-07-2026 (MG): Systema-hosted, Systema's own students, 4-week retention.** §6.4 (consent wording) still open.

## Audience
Whoever runs the actual pilot/study, and whoever writes A32 (the RQ4 evaluation-methodology paper).

## Provenance
- **Model:** Sonnet 5 (`claude-sonnet-5`), 15-07-2026.
- **Grounding:** the existing on-ramp testbed (`TolchelnikovTalmud_2026/onramp/`, H915), the full 745-root Приложение 1 catalogue (item-bank source, restricted to the on-ramp's 4 taught rows), a direct check of `docusaurus.config.mjs` confirming the site has zero analytics/instrumentation today.

## Ranked backlog
1. ~~Resolve the 4 `@DECIDE` items in §6~~ — §6.1–6.3 ruled 15-07-2026; §6.4 (consent wording) still open, drafted pending MG review (H988 harness handoff).
2. ~~Build the item bank~~ — **DONE** (H984): [`data/rq4_item_bank.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/rq4_item_bank.json), 24 items, 0 shortfall.
3. **Build the Systema-hosted harness** (H988) — consent/intake, arm assignment, diagnostic flow, +4-week retention reminder.
4. **Run the pilot** (§7) before any confirmatory-sized run.
5. **Write A32** once pilot data exists.

## Limitations
- No sample-size-justified confirmatory design exists yet — §5's power estimate is a placeholder pending a real recruitment-population size (now knowable: Systema's Kochergina-stage student count).
- This is a between-subjects design; a learner can't experience "first contact" with the on-ramp twice, so no within-subject crossover arm was designed.
- The diagnostic instrument is scoped to the on-ramp's own 4 taught rows (A₁/I₁/U₁/R₁) — a deliberate fairness restriction, not a full-matrix generalisation test.

## Related
- Field: [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md) · [A62 outline](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/DigitalPedagogyAgenda_A62/OUTLINE_digital-sanskrit-pedagogy-agenda_A62.md) §4.
- Testbed: [`TolchelnikovTalmud_2026/onramp/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp) (H915) + [design doc](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/ZALIZNYAK_ONRAMP_DESIGN.md).
- Sibling last-mile spec (same kosha↔Systema division-of-labour pattern referenced in §6.3): [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md).

## Revision history
| Date | Change | Model |
|---|---|---|
| 15-07-2026 | Created — full protocol (hypothesis, design, metrics, instrument, analysis plan, 4 open `@DECIDE`s, pilot recommendation) | Sonnet 5 (`claude-sonnet-5`) |
| 15-07-2026 | §6.1–6.3 ruled by MG (Systema-hosted, own students, 4-week retention); item bank built (H984), instrument scoped to the on-ramp's 4 rows (documented restriction) | Sonnet 5 (`claude-sonnet-5`) |

---

_Dr. Mārcis Gasūns_
