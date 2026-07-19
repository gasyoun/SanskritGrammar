# Metadoc — PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2

_Created: 18-07-2026 · Last updated: 18-07-2026_

Companion record for
[`docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md)
and its four layer docs.

## Purpose

Convert the author-visa editorial backlog in
[`review/`](https://github.com/gasyoun/SanskritGrammar/blob/main/review) into executable, tracked
work, and correct three governing documents (charter calendar, ACL roadmap framing, review-artifact
tracking) that production has outgrown.

## Audience

| Reader | Uses it for |
|---|---|
| A wave-1 executing agent | The per-handoff spec, tier, and acceptance gate |
| A future session asking "was this note applied?" | The ledger design and the `note_uid` convention |
| A human resolving the escalations | The `@DECIDE` list, the A61 contradiction, the 3 undecided items |

## Provenance

| Field | Value |
|---|---|
| Authoring model | Opus 4.8 (`claude-opus-4-8`) |
| Date | 18-07-2026 |
| Method | Phase-1 audit brief + 7 human rulings (18-07-2026), with every load-bearing number re-derived this session by parsing the 13 `decisions.json` files directly |
| Register | English — matched to the existing `docs/` siblings (`PLAN_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`, `ARCHITECTURE_DIGITAL_SANSKRIT_PEDAGOGY.md`), while `sangram/` article content stays Russian. Quoted notes are verbatim Russian |
| Written in | Worktree `SanskritGrammar-askbatch`, branch `askbatch-slice2-plan`. No commit, no push |

### Premises that did not survive verification

The brief was largely accurate; three claims were not, and all three were load-bearing. They are
recorded here because a future reader may encounter the original framing elsewhere.

| Briefed | Measured | Where corrected |
|---|---|---|
| "Every decision is approve" | 114 approve · 3 reject · 3 null | Plan §1, table row 1 |
| "The 87 notes are real unapplied forward work" | 81 applicable; 21 already applied (18 at visa time + 3 by PR #416); **60** genuinely open | Plan §1.1–1.2 |
| "14 articles carry the candidate banner" | The string occurs in all 35 — historical rows in published articles | Plan §1, row 3; Verification §5 |

Two further corrections carried in from the brief's own instructions and confirmed:
the Next-free-ID marker is **not** a collision risk (`mint_handoff.py` takes `max()` over disk +
marker), and the RQ4 study's four `@DECIDE`s were already ruled with consent wording approved
verbatim on 16-07-2026 — so W3-A is operationalisation, not design.

## Limitations

| # | Limitation |
|---|---|
| L1 | The applied/open split (21 / 60) is evidence-based but **not** exhaustively hand-verified across all 81 notes. Only the `precative` 3 are conclusively evidenced (a merge commit). It is deliberately the gated output of W1-B, not an input |
| L2 | `note_class` assignments in the docs are illustrative examples, not a complete classification of all 81 |
| L3 | Four sheets have lost their HTML; **three** of the four use positional ids, and for two of those the referent of 8 open notes must be reconstructed by text matching (the third, `a-stems`, is moot — its 3 notes are applied) |
| L4 | `target_file` for the `precative` and `w2-core` sheets is per-note, not per-sheet; the mapping table is partial by design |
| L5 | No estimate of how many `RESEARCH` notes will actually close in wave 1 — several need corpus probes that may not resolve |
| L6 | Every number here is a snapshot against `origin/main` at `3b4f9e4` (18-07-2026). The `precative` row moved from 3 open to 0 open **during** authoring; the registry figures moved while the drafting clone sat 74 commits behind. Re-derive, never re-cite |

## Improvement backlog

| Rank | Item | Why |
|---|---|---|
| 1 | Complete the `note_class` assignment for all 81 notes | Turns the illustrative taxonomy into the actual dispatch table |
| 2 | Make the revision-row provenance convention mandatory in the style guide | It is the only reason applied/open was reconstructible; `perfect` and `a-stems` show what its absence costs |
| 3 | Reconstruct the 4 lost sheet HTMLs from `decisions.json` + article text | Restores provenance for the 8 `RECONSTRUCTED` notes |
| 4 | Add a ledger-status check to CI | Prevents a note silently regressing to `UNKNOWN` |
| 5 | Fold the "≥5 examples" and "no invented jargon" policies into an authoring checklist | **Five notes each** — the "≥5 examples" five span four sheets (`future` contributes two), the "no invented jargon" five span five different sheets. The two most-repeated author complaints |
| 6 | Decide whether `/decisions-apply` should learn about the ledger | Currently the ledger is an external manifest; the skill may deserve the concept natively |

## Related docs

| Doc | Relation |
|---|---|
| [`docs/ROADMAP_SANSKRITGRAMMAR_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_SANSKRITGRAMMAR_2026H2.md) | Wave structure + handoff specs |
| [`docs/ARCHITECTURE_SANGRAM_EDITORIAL_NOTE_PIPELINE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANGRAM_EDITORIAL_NOTE_PIPELINE.md) | Pipeline, `note_uid`, H856 decision record |
| [`docs/IMPLEMENTATION_SANGRAM_EDITORIAL_NOTES.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/IMPLEMENTATION_SANGRAM_EDITORIAL_NOTES.md) | Step-by-step |
| [`docs/VERIFICATION_SANGRAM_EDITORIAL_NOTES.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANGRAM_EDITORIAL_NOTES.md) | Gates |
| [`docs/RQ4_EVALUATION_PROTOCOL_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/RQ4_EVALUATION_PROTOCOL_2026.md) | W3-A consumes it; supersedes any re-design |
| [`sangram/SANGRAM_CHARTER_2026_2031.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_CHARTER_2026_2031.mdx) | Rewrite target, W2-A |
| [`ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) | Rewrite target, W2-B |

## Revision history

| Date | Change | By |
|---|---|---|
| 18-07-2026 | Created with the four layer docs; three briefed premises corrected against a direct parse of the 13 vote files | Opus 4.8 (`claude-opus-4-8`) |
| 18-07-2026 | Adversarial verification pass. Nine defects patched: `precative` re-derived 3 open → 0 applied (PR #416), so the backlog closes at 21 applied / **60** open; wave-1 coverage made exhaustive (W1-C 32 + W1-D 19 + W1-E 9 = 60, both taddhita sheets owned); A61 dominance restated as patch-identity, **not** ancestry (`merge-base --is-ancestor` exits 1); the underivable "13 🟡 rows / PRs #382–#413" replaced with a measured **51 of 67** plus its method; orphan-sheet split corrected to 3 positional + 1 dual-family; the "five unarchived ✅" list cut to four terminal rows, only one ✅ (H1065 struck — WhitneyRoots, already archived); `generated` documented as two formats; closed worktree list replaced by an enumeration rule; policy-note counts reconciled to five/five; bare `[A8]` qualified to `sangram-prose-style-guide-visa#A8`. Two findings **refuted** against `origin/main` and left unchanged: H1252 is filled and rowed (the "unfilled stub" reading came from a clone 74 commits behind), and the ledger's items/notes/applicable columns re-parsed clean at 120/87/81 | Opus 4.8 (`claude-opus-4-8`) |

_Dr. Mārcis Gasūns_
