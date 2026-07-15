# Metadoc — RQ4_EVALUATION_PROTOCOL_2026.md

_Created: 15-07-2026 · Last updated: 15-07-2026_

Companion for [`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md).

## Purpose
The full study design for RQ4 (learning-gain + retention on-ramp-first vs Талмуд-first), the digital-pedagogy field's falsifiability backbone. Closes A62's own "5/5: RQ4 evaluation protocol specified in full" checklist item. **Protocol-only**: no study has run, no harness has been built, no participants recruited.

## Audience
Whoever runs the actual pilot/study, and whoever writes A32 (the RQ4 evaluation-methodology paper).

## Provenance
- **Model:** Sonnet 5 (`claude-sonnet-5`), 15-07-2026.
- **Grounding:** the existing on-ramp testbed (`TolchelnikovTalmud_2026/onramp/`, H915), Talmud Appendix 1's 65 tagged roots (item-bank source), a direct check of `docusaurus.config.mjs` confirming the site has zero analytics/instrumentation today.

## Ranked backlog
1. **Resolve the 4 `@DECIDE` items in §6** (recruitment population/channel, retention window N, hosting/instrumentation home, consent framing) — nothing below can start honestly without these.
2. **Build the item bank** — derivable now from Appendix 1, independent of the `@DECIDE`s.
3. **Build the harness** — depends entirely on §6.3's hosting decision (Systema-hosted flow vs external form tool vs other).
4. **Run the pilot** (§7) before any confirmatory-sized run.
5. **Write A32** once pilot data exists.

## Limitations
- No sample-size-justified confirmatory design exists yet — §5's power estimate is a placeholder pending a real recruitment-population size.
- This is a between-subjects design; a learner can't experience "first contact" with the on-ramp twice, so no within-subject crossover arm was designed.
- Retention-window choice (N weeks) is unresolved — the field's own docs give no default.

## Related
- Field: [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md) · [A62 outline](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/papers/DigitalPedagogyAgenda_A62/OUTLINE_digital-sanskrit-pedagogy-agenda_A62.md) §4.
- Testbed: [`TolchelnikovTalmud_2026/onramp/`](https://github.com/gasyoun/SanskritGrammar/tree/main/TolchelnikovTalmud_2026/onramp) (H915) + [design doc](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/ZALIZNYAK_ONRAMP_DESIGN.md).
- Sibling last-mile spec (same kosha↔Systema division-of-labour pattern referenced in §6.3): [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md).

## Revision history
| Date | Change | Model |
|---|---|---|
| 15-07-2026 | Created — full protocol (hypothesis, design, metrics, instrument, analysis plan, 4 open `@DECIDE`s, pilot recommendation) | Sonnet 5 (`claude-sonnet-5`) |

---

_Dr. Mārcis Gasūns_
