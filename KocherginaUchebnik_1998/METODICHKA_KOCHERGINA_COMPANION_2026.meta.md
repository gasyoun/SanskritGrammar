# Metadoc — METODICHKA_KOCHERGINA_COMPANION_2026.md

_Created: 12-07-2026 · Last updated: 12-07-2026_

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
1. **Resolve @DECIDE K-1** — pin which physical edition the `.mdx` transcribes (1998 vs 2017
   6th ed. / Лихушина). Everything errata-precise depends on it.
2. **Formalize the print assembler** (`scripts/build_methodichka.py`) once v1 proves the
   hybrid prose+registry interleave by hand (currently deferred to v2 / P5).
3. **Decide K-2** — whether `exercises.yml` / `crossrefs.yml` registries are worth building
   up front or promoted from a hand-authored v1 appendix.
4. **Wire the errata `edition` field** into `build_errata.py` so a 2024/2025 diff produces a
   real per-edition column, not free-text notes.

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

_Dr. Mārcis Gasūns_
