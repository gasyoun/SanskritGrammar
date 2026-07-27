# Methodichka visa-apply runbook

_Created: 27-07-2026 · Last updated: 27-07-2026_

Procedure for terminalising residual OPEN/PARTIAL editorial notes on a methodichka
(`*_KOMMENTARII_2026.md`) companion after a `/review-sheet` voting round has produced a
`decisions.json`. This document is **process only** — it does not itself apply any visa. The
current residual backlogs live on
[H1454](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1454-Fable_SanskritGrammar_kochergina-metodichka-v1-open-items_22.07.26.md)
(Kochergina) and
[H1615](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1615-Fable_SanskritGrammar_metodichka-apte-open-residual_24.07.26.md)
(Apte) — this runbook does **not** re-mint or re-execute that work; it is the reusable
procedure future waves point at instead of re-deriving it from scratch.

## Scope fence

- **In scope:** pedagogy companion methodichkas (`ApteSyntax_1885/METODICHKA_APTE_KOMMENTARII_2026.md`,
  `KocherginaUchebnik_1998`'s methodichka, and any future `*_KOMMENTARII_2026.md`) and their
  entries in [`review/EDITORIAL_NOTE_INDEX.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv).
- **Out of scope:** pure Sangram-article register/prose work — that stays on the editorial
  track (`SANGRAM_STYLE_GUIDE_PROSE_RU.mdx` lifecycle) unless the specific note is explicitly
  listed as a re-vote class item (see zan-29 example below).
- Applying visas, writing methodichka prose, or ruling on Sangram-freeze disposition are
  **not** done by this runbook — it only documents how a worker does that work when a handoff
  assigns it.

## Pipeline

```
decisions.json (from a completed /review-sheet round)
        │
        ▼
Step 0 — RE-AUDIT: re-read review/EDITORIAL_NOTE_INDEX.tsv for the target methodichka
        │           (prior apply PRs may already have closed some notes — do not
        │            re-open or re-apply a note whose applied_status is already
        │            terminal: APPLIED / DEFERRED / ESCALATED / ANSWERED)
        ▼
Step 1 — For each still-OPEN/PARTIAL note_uid (= sheet_id#item_id), classify the
        │  decision:
        │
        ├─ decision = "approve" AND evidence exists in-repo
        │       → APPLY: edit the target file, add a dated revision-history row
        │         citing the sheet_id#item_id, set applied_status = APPLIED (or
        │         PARTIAL if only half-realised) in EDITORIAL_NOTE_INDEX.tsv with an
        │         `evidence` cell pointing at the exact rev-row
        │
        ├─ decision = "approve" BUT evidence/data is missing (a scan, a corpus figure,
        │  a source not yet in-repo)
        │       → DEFER: leave applied_status = OPEN (or set DEFERRED if the blocker
        │         is now named), write a probe stub — a one-line note of exactly what
        │         evidence is missing and where it would come from — do NOT invent the
        │         number/citation to close the item
        │
        └─ note proposes a genuine re-vote / research question rather than an edit
           (the zan-29 class: DCS cannot mark P/Ā or a semantic condition, so the note
           is asking for a corpus study, not a text change)
                → RE-SHEET: move the note to
                  review/EDITORIAL_NOTE_INDEX_EXCLUDED.tsv with a reason citing the
                  handoff that ruled it non-applicable, and queue it as a fresh
                  `@DECIDE` in Uprava/GTD_NEXT_ACTIONS.md or a follow-up /review-sheet
                  round — never silently drop it
        ▼
Step 2 — Update the methodichka's own revision-history section for every APPLIED/PARTIAL
        │  change, citing sheet_id#item_id
        ▼
Step 3 — Commit; CHANGELOG entry; PR
```

### Mandatory first step: re-audit the OPEN count

Before touching anything, re-read `review/EDITORIAL_NOTE_INDEX.tsv` for the target
methodichka's rows. A prior apply PR (a different wave, a different executor) may already
have closed notes that a stale plan/handoff still lists as OPEN — the count in a handoff body
is a snapshot at mint time, not live state. Only work the notes that are *actually* still
OPEN/PARTIAL in the current `origin/main` index.

## The three terminal states

| State | Meaning | Example (from `review/EDITORIAL_NOTE_INDEX.tsv`) |
|---|---|---|
| **APPLIED** | The note's request was realised in the target file; a dated revision-history row cites the note_uid as evidence | [`sangram-prose-style-guide-visa_16.07.26#A1`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv): "§1 RWS-council cross-check promoted from backlog item to standing lifecycle rule" |
| **DEFERRED** | The note is valid but blocked on evidence/data/a live-reading session that doesn't exist yet — the blocker is named, not papered over | [`sangram-prose-style-guide-visa_16.07.26#A2`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv): "rusgram-expansion half DEFERRED — blocker: dedicated live-reading session; site reachable over plain http only, https cert broken per SERVER_OUTAGES" |
| **re-sheet / ESCALATED** | The note is actually a research question or a disputed classification needing a fresh human vote, not a text edit — moved to `EDITORIAL_NOTE_INDEX_EXCLUDED.tsv` and queued as `@DECIDE` | [`sanskritgrammar-metodichka-apte-v1_17.07.26#zan-29`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX_EXCLUDED.tsv): "Re-vote. Note proposes deriving P/Ā from observable forms — a research question, not an edit. (H1275 confirmed: 'применению не подлежит; повторная виза = @DECIDE в GTD'.)" |

`PARTIAL` and `ANSWERED` are intermediate/adjacent states used when only half a note was
realised, or when a note was a question rather than a change request (see
`taddhita-revisa_visa#TAD2-08`, "ANSWERED... Not marked APPLIED per gate C4").

## Citation rule

Every APPLIED (or PARTIAL) change's revision-history row in the target `.mdx`/`.md` file
**must cite `sheet_id#item_id`** (the same `note_uid` used in `EDITORIAL_NOTE_INDEX.tsv`) —
never a bare date or a vague "per reviewer feedback". This is what lets a future audit trace
any prose sentence back to the exact vote that authorized it.

## "Do not invent numbers" + the probe-stub path

Russian prose in these methodichkas is author-register, evidence-anchored prose — **never**
close an OPEN note by inventing a corpus count, a percentage, or a bibliographic citation that
isn't already verifiable in-repo. If a note asks for a number/scan/citation that doesn't exist
yet (e.g. "what does Elizarenkova's «Аорист в Ригведе» say?" when the scan may be missing —
see `zan-19`), the correct move is:

1. Check whether the source is actually available in-repo or on a known shared drive first.
2. If not available: leave the note OPEN/ESCALATED and write a **probe stub** — a short,
   explicit note of what's missing and where it would come from (e.g. "scan not found under
   `Concordance/`; last known location: Общество ревнителей санскрита upload") — so the next
   pass knows exactly what to go get, instead of re-deriving the same dead end.
3. Never substitute a plausible-sounding number to make the item look closed.

## When to call `/decisions-apply` vs hand-apply

- **Call [`/decisions-apply`](https://github.com/gasyoun/claude-config/blob/main/commands/decisions-apply.md)**
  when the work is a straightforward batch of approve/reject/defer verdicts from a completed
  `/review-sheet` round with a clean 1:1 item-ID match against the sheet manifest — it handles
  validation, partitioning, the audit-record write (`decisions_applied_<date>.md`), and the
  GTD/`REVIEW_SHEETS_INDEX.md` bookkeeping in one pass.
- **Hand-apply** (the pattern this runbook documents, as used by H1454/H1615) when the notes
  need per-item editorial judgment beyond a bare verdict — deciding APPLIED vs PARTIAL vs
  DEFERRED, writing the actual prose/footnote, or classifying a note as a re-vote candidate
  rather than an edit. There is currently no dedicated apply *script* for the methodichka
  targets (no `scripts/apply_metodichka*.py` exists in this repo as of 27-07-2026) — hand-apply
  means: edit the target `.mdx`/`.md` directly, then update
  `review/EDITORIAL_NOTE_INDEX.tsv` by hand with the citation and evidence columns described
  above.

## Re-sheet generation

When Step 1 identifies a re-vote/research-question class note, generate the follow-up round
via [`/review-sheet`](https://github.com/gasyoun/claude-config/blob/main/commands/review-sheet.md)
— **markdown checkbox sheets are banned**. Follow that skill's naming convention
(`<repo-slug>-<topic>_<scope>_review.html` / `..._decisions.json`, never a generic filename)
and its Phase 0 gate (a 1-question decision goes in chat, not a sheet; ≥5 items or a repeated
homogeneous judgment gets the sheet). Every option on the sheet must state its consequence,
not just its label — see the `/review-sheet` skill's worked-example requirement.

## Related

- Pointed at by [`docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md)
  Wave-1 table (H-A row) and
  [`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md)
  for the source residual backlog this procedure operates on.
- [`review/EDITORIAL_NOTE_INDEX.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv) /
  [`review/EDITORIAL_NOTE_INDEX_EXCLUDED.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX_EXCLUDED.tsv)
  — the live tracking tables this runbook's Step 0/Step 1 read and write.

_Dr. Mārcis Gasūns_
