# Metadoc — LAST_MILE_PIPELINE_SPEC.md

_Created: 14-07-2026 · Last updated: 14-07-2026_

Companion record for [`LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md).

## Purpose

The integration contract for the digital-Sanskrit-pedagogy field's **last mile** — the one `queued`
hop (kosha open layer → Systema learner surface) that both proven value chains stop at (MEGABOOK
§14.2). It exists so a Wave-2 agent can wire kosha → Systema without re-discovering which real files,
endpoints, formats, and import commands already exist on each side.

## Audience

A Wave-2 implementation agent (kosha exporter / Systema importer), and MG as the human reviewer who
gates the wave-1 spec before any code is written.

## Provenance

- **Handoff:** [H916](https://github.com/gasyoun/Uprava/blob/main/handoffs/H916-Opus_SanskritGrammar_pedagogy-w1d-last-mile-pipeline_14.07.26.md) (wave-1d), field parent [H912](https://github.com/gasyoun/Uprava/blob/main/handoffs/H912-Opus_SanskritGrammar_digital-pedagogy-field-established_14.07.26.md).
- **Model:** Opus 4.8 (`claude-opus-4-8[1m]`), 14-07-2026.
- **Method:** governing docs (plan / architecture / implementation / verification + MEGABOOK §14.2 + W1a difficulty result) read first; then two read-only Explore passes over kosha and Systema-Sanscriticum to capture the real producer/consumer artifacts (endpoint paths, `lemma_frequency.tsv` 8-column schema, `export.js` card shape, `SanskritGlossary.php` vendored-feed pattern, `srs:import-memrise` manifest+CSV contract, Saraswati FSRS model).
- **Prior art checked:** the three transport patterns (V/D/S) are all pre-existing and live; the spec invents no new transport. The only genuinely new build it names is the kosha difficulty scorer.

## Ranked improvement backlog

1. **Quantify the genre bias** (ties to RQ1) — the spec asserts DCS epic/kāvya weighting but W1a has not yet measured it against a register-balanced count; until then the difficulty scorer ships with the bias documented, not corrected.
2. **Pin the difficulty-score home** — column-in-kosha vs SanskritGrammar-side TSV is left as a logged default; Wave-2's first decision.
3. **Worked demo artifact** — §4 is a data walkthrough, not a committed `manifest.json`+CSV fixture; a real fixture (even for one subhāṣita) would make the Pattern-D contract testable before Wave-2.
4. **`cyrillic` field** — kosha emits none; the A0 Cyrillic-only track's population path is unspecified.
5. **Second import target** — only the vocabulary/SRS path is spec'd; the corpus→Sangram→lesson chain's final hop (verb-form frequency I9 → conjugation drills) is a parallel last mile not covered here.

## Limitations

- **Spec, not build** — no code exists yet; every hop's wiring is Wave-2. The spec's correctness is
  "names real artifacts + a viable contract", verified against live files, not by a running pipeline.
- **One chain only** — covers dictionary→kosha→Systema (vocab/reading). The corpus→grammar→lesson
  chain's last mile is out of scope.
- **Difficulty scorer unbuilt** — Hop B depends on an artifact that does not exist; the spec fixes its
  contract (from W1a) but a null/weak RQ1 result would reshape it.

## Related docs

- Plan / Architecture / Implementation / Verification: `*_DIGITAL_SANSKRIT_PEDAGOGY*.md` (this `docs/` dir).
- [W1a difficulty result](https://github.com/gasyoun/SanskritGrammar/blob/main/DIFFICULTY_ORDERING_RESULT.md) — the Hop B scoring contract.
- [Systema pedagogy index](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/docs/SANSKRIT_HUB_ASSET_PEDAGOGY_INDEX.md) — G3 / E26 consumer rows.
- MEGABOOK [§14.2](https://github.com/gasyoun/Uprava/blob/main/MEGABOOK.md) — the three proven paths / the dashed hop.

## Revision history

| Date | Model | Change |
|---|---|---|
| 14-07-2026 | Opus 4.8 (`claude-opus-4-8[1m]`) | Created with the spec (wave-1d, H916). |

---

_Dr. Mārcis Gasūns_
