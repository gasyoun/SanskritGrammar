# Metadoc — METODICHKA_KOCHERGINA_COMPANION_2026.md

_Created: 12-07-2026 · Last updated: 21-07-2026_

Companion record for the Kochergina methodichka roadmap
([`METODICHKA_KOCHERGINA_COMPANION_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_COMPANION_2026.md)).

## Purpose
Plan a **thin printed companion booklet** to Kochergina's *Учебник санскрита* — accuracy
notes, clarity/frequency refinements, extra exercises, cross-references, and a per-edition
errata list — by *consuming* the repo's existing claims/errata infrastructure rather than
rebuilding it.

## Audience
MG (author of record) + any future session executing a methodichka slice (currently
[H807](https://github.com/gasyoun/Uprava/blob/main/handoffs/H807-Fable_SanskritGrammar_kochergina-methodichka-v1_12.07.26.md),
Fable 5).

## Provenance
- Authored 12-07-2026 by Opus 4.8 (`claude-opus-4-8`) from a prior-art sweep of the
  KocherginaUchebnik_1998 folder + repo `.ai_state.md` + memory.
- Four forks ruled by MG in-session (Decisions A–D, § 1 of the roadmap).
- Execution delegated to Fable 5 (`claude-fable-5`) via H807.

## Ranked improvement backlog
1. ~~**Resolve @DECIDE K-1**~~ — RESOLVED by MG 12-07-2026: reference edition = **1998
   original**. Residual caveat carried in `errata.yml`: LEARNER_MATERIALS.md records the
   digitized copy as the 2017 6th ed. — re-open K-1 if the `.mdx` is shown to transcribe it.
2. **Formalize the print assembler** (`scripts/build_methodichka.py`) once v1 proves the
   hybrid prose+registry interleave by hand (currently deferred to v2 / P5).
3. ~~**Decide K-2**~~ — RESOLVED 16-07-2026 (H807, per the roadmap's own recommendation):
   v1 sections hand-authored; `exercises.yml`/`crossrefs.yml` promotion deferred to v2.
4. **Wire the errata `edition` field** into `build_errata.py` so a 2024/2025 diff produces a
   real per-edition column, not free-text notes. (The field itself is documented in the
   `errata.yml` entry shape since H807; the renderer ignores it harmlessly until wired.)
5. **v2 widening** — comprehensive commentary over the full 234-claim register (the drained
   H797 register supersedes the 43-claim basis this plan was written against); DCS-2026
   re-run may resolve the 12 UNTESTABLE rows.
6. ~~**Corpus layer (раздел IV)** — per-lemma DCS frequency band + one attested example
   with a Russian rendering for every lemma the раздел-I commentary turns on.~~
   ✅ **DONE (H1297, 21-07-2026):**
   [`METODICHKA_KOCHERGINA_CORPUS_LAYER_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_CORPUS_LAYER_2026.md)
   (31 lemmas over 9 занятий) backed by
   [`corpus_layer/corpus_layer.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/corpus_layer/corpus_layer.tsv)
   and pinned by [`tests/test_corpus_layer.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/test_corpus_layer.py).
   Residual: the freshly authored Russian renderings await the MG viza, like the rest of
   the manuscript.

## Limitations
- The roadmap plans; it does not itself contain any commentary content (that is the
  handoff's output).
- Edition provenance (K-1) is unresolved, so no page/line errata claim is trustworthy yet.
- Rights: covers *our* overlay only — printing Kochergina's own text is out of scope
  (§ 6 of the roadmap).

## Related docs
- [`LEARNER_MATERIALS.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/LEARNER_MATERIALS.md)
  — the learning ladder the cross-references draw on.
- [`claims.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/claims.yml)
  / [`errata.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/errata.yml)
  — the registries the print build consumes.
- Registered in [`Uprava/ROADMAP_INDEX.md`](https://github.com/gasyoun/Uprava/blob/main/ROADMAP_INDEX.md).

## Revision history
| Date | Model | Change |
|---|---|---|
| 12-07-2026 | Opus 4.8 (`claude-opus-4-8`) | Created roadmap + metadoc; Decisions A–D locked; H807 minted for v1. |
| 16-07-2026 | Fable 5 (`claude-fable-5`) | § 4.2: queued material for Занятие 22 (стр. 153) per MG's P3-visa card A4 — periphrastic-perfect auxiliary distribution (as 91,4 % / kṛ 7,4 % / bhū 0,8 %, 3 sg 86,6 %) from the SG-MO-017 corpus package. |
| 16-07-2026 | Fable 5 (`claude-fable-5`) | **v1 (P0–P4) executed — H807.** Three manuscript sections authored (разделы I–III: комментарий / упражнения / отсылки); §2 pillar table refreshed to the drained 234-claim register; §5 marked v1 EXECUTED; `errata.yml` `edition` field added (seed empty); K-2 resolved (hand-authored v1); backlog items 1/3 closed, item 5 (v2 widening) added. |
| 21-07-2026 | Fable 5 (`claude-fable-5`) | **Corpus layer (раздел IV) authored — H1297.** 31 lemmas per занятие with DCS frequency bands (kosha `lemma_frequency.tsv` rank_all: топ-100/топ-1000/редкое) + one attested DCS-2026 example each, RU renderings freshly authored (no restricted layer opened). Working TSVs under `corpus_layer/`, banding regression + locus/rights checks in `tests/test_corpus_layer.py`. Backlog item 6 added and closed. |

_Dr. Mārcis Gasūns_
