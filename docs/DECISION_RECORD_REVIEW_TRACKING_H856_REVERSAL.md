# Decision record — reversing H856 (`/review/` tracking)

_Created: 19-07-2026 · Last updated: 19-07-2026_

Executed by [H1273](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1273-Sonnet_SanskritGrammar_sangram-review-votes-track-h856-reversal_18.07.26.md),
content per [`docs/ARCHITECTURE_SANGRAM_EDITORIAL_NOTE_PIPELINE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ARCHITECTURE_SANGRAM_EDITORIAL_NOTE_PIPELINE.md) §5.

## Context

[`.gitignore`](https://github.com/gasyoun/SanskritGrammar/blob/main/.gitignore) line 23
excluded `/review/`, with the rationale **H856**: "interactive review-sheet artifacts
(personal working artifacts, not repo deliverables)".

## Why H856 was reasonable then

When sheets were generated, voted, and applied within a single session, they genuinely
were scratch — the durable output was the article revision, not the voting UI.

## Why it is wrong now — measured

The votes became the record of the author's scholarly sign-off, and they are **not**
consumed in-session:

| Evidence | Measurement |
|---|---|
| Adjudicated items at risk | 120 across 13 sheets, all untracked, on one machine |
| Author sign-off represented | Every visa cast since 15-07-2026 |
| Loss already realised | **4 of 13** sheet HTMLs are gone before this reversal (`sangram-prose-style-guide-visa_16.07.26`, `sangram-sg-mo-017-perfect-visa_15.07.26`, `sangram-sg-mo-002-a-stems-visa_15.07.26`, `sanskritgrammar-a65-verdict-validation-disagreements_16.07.26`) |
| Cost of tracking | 13 `*_decisions.json` (measured 52 KB) + 9 surviving `*_review.html` (measured 240 KB) = **~292 KB total, accepted** |
| Failure modes that erase everything | an untracked-file wipe (force-clean including ignored paths), drive failure, machine change |

## Ruling (18-07-2026)

Track the **whole** `review/` directory — sheets *and* votes. `/review/` is removed from
`.gitignore`. This **reverses H856**.

## Consequences

- Generated HTML enters version control (accepted, quantified above).
- Sheets become citable by blob URL, so a revision row can link the exact sheet that
  motivated an edit.
- Future sessions can answer "was this note applied?" without local state — this is
  exactly what [`review/EDITORIAL_NOTE_INDEX.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv)
  (this same handoff) now provides.
- 4 of the 13 sheets have *already* lost their `_review.html` before this reversal took
  effect — those losses are permanent. The reversal stops further loss, it does not
  undo what already happened. See the NOTE INDEX's `RECONSTRUCTED`/`ORPHAN_MOOT`
  provenance rows for how those four orphan sheets were handled.

## Recorded, not silent

This decision record exists per ruling 2 of
[`docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANGRAM_EDITORIAL_NOTES_AND_CHARTER_2026H2.md) §2 --
a bare `.gitignore` edit would leave no trace of *why* a documented prior ruling (H856)
was reversed, which is precisely how H856's own rationale would have had to be
re-derived from scratch a year from now.

_Dr. Mārcis Gasūns_
