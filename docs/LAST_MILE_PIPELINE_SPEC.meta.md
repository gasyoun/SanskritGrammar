# Metadoc — LAST_MILE_PIPELINE_SPEC.md

_Created: 14-07-2026 · Last updated: 14-07-2026_

Companion for [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md).

## Purpose
The contract a Wave-2 executor implements to close MEGABOOK §14.2's "last mile" — kosha → Systema.
Wave-1d of the digital-pedagogy field, H916. **Spec-only**: no Systema code was touched this wave.

## Audience
Whoever builds Wave 2 (the kosha deck/reading-pack/difficulty datasets + the Systema flag-gated importer/reader).

## Provenance
- **Model:** Opus 4.8 (`claude-opus-4-8[1m]`), 14-07-2026.
- **Grounding:** a concrete map of both repos' real integration surfaces — kosha FastAPI + segmenter + frequency layer + Anki export + manifest, and Systema's Saraswati SRS schema, `Lesson`, exercise engines, and the live `SanskritGlossary.php` vendoring precedent.
- **Design input:** wave-1a ([`DIFFICULTY_ORDERING_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md)) supplies Hop B's ranking rule (strip function words, genre-correct).

## Ranked backlog (for Wave 2)
1. **Locate/commit `build_sa_ru_glossary.py`** — the vendoring build script the contract leans on is referenced but not in the tree (only its output). Resolve before freezing.
2. **Decide the SRS order mechanism** — insert-in-rank-order (demo) vs a `srs_cards.sort_rank` migration (production).
3. **Build the demo rung** (B1 subhāṣita) end-to-end as the acceptance proof.
4. **API phase** — only if arbitrary paste-reading becomes a requirement (Hop A); needs CORS allow-list.

## Limitations
- Spec, not build — every hop is a contract, nothing is wired.
- Vendored-file path chosen as the default; the live-API path is described but deferred.
- kosha reading-packs + a difficulty dataset don't exist yet (planned) — the spec defines their shape, Wave 2 builds them.

## Related
- Field: [`DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md) · plan [`docs/PLAN_...`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md).
- Systema-side planned wiring: `Systema-Sanscriticum/docs/ROADMAP_SANSKRIT_HUB_NLP_2026_2028.md` (phase B: `/nlp` API + auto-built frequency-ordered SRS decks).

## Revision history
| Date | Change | Model |
|---|---|---|
| 14-07-2026 | Created — 3-hop contract (reader / SRS deck / difficulty), vendored-file default, one-rung demo | Opus 4.8 (`claude-opus-4-8`) |

---

_Dr. Mārcis Gasūns_
