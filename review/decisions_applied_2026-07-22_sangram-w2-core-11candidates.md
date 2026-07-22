# Decisions applied — sangram-w2-core-11candidates-visa_17.07.26 (12 approve / 0 reject / 0 defer)

_Created: 22-07-2026 · Last updated: 22-07-2026_

Audit record closing the human vote on the W2-core 11-candidate visa, applied via
[`/decisions-apply`](https://github.com/gasyoun/claude-config/blob/main/commands/decisions-apply.md)
across three sessions.

- **Decisions file:** `review/sangram-w2-core-11candidates-visa_17.07.26_decisions.json`
  (voted 17-07-2026, reviewer `gasyoun`, 12/12 approve).
- **Handoff:** [H1257](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1257-Sonnet_sangram_apply-sangram-w2-core-11candidates-visa_17.07.26-decisions_18.07.26.md)
  (this session — closes the sheet); publication and the 9 substantive notes were
  already done by [H1316](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1316-Opus_SanskritGrammar_apply-voted-precative-w2core-visas_19.07.26.md)
  and [H1346](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1346-Sonnet_SanskritGrammar_w2-core-visa-editorial-notes_19.07.26.md).

## Counts

| Verdict | Count |
|---|---:|
| approve → publication only (no note: MO12, V) | 2 |
| approve → substantive note applied (H1346, 21-07-2026) | 7 |
| approve → substantive note applied (this session, H1257) | 1 (MO28) |
| approve → substantive note answered as a measured question, no trend found (H1346) | 1 (MO27) |
| reject | 0 |
| defer | 0 |
| **total** | **12** |

All 12 items carried a vote; no unvoted, no unknown IDs, 1:1 against the sheet.

## Publication (H1316, PR #472)

All 10 non-causative candidate articles got a `published` manifest revision; the causative
article (MO28) had already been published on 17-07-2026 by its own dedicated visa
(`sanskritgrammar-sg-mo-028-causative_visa`, 10/10 approve).

## Substantive notes (H1346, PR #498/#499, released v0.105.0)

WF06 (compounds-overview), WF01 (word-structure-overview), MO06 (consonant-stems), MO10
(pronouns), MO23 (ta-na-participles), MO26 (absolutive), MO16 (imperfect), MO18 (aorist)
all dispositioned directly. MO27 (passive) — "does the passive share grow over time?" —
was measured (2.7%→9.2%→7.0%, not monotonic) rather than answered with a `[Q]` row.

## MO28 — the residual card (this session, H1257)

MO28's note («слита с первичным curādi — кто из грамматик сливает? кто держит по
отдельности, но с оговоркой как Кнауэр?») was **not** covered by the causative
article's own dedicated visa (`MO028-05/07/08/09`, none of which address grammar
historiography) — H1346 incorrectly summarized it as "already handled there," which is
why `EDITORIAL_NOTE_INDEX.tsv`'s own row stayed `OPEN` despite that summary. Resolved
this session: a new § 4 paragraph in
[causative/index.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/articles/causative/index.mdx)
compares Whitney (formally merges the exposition, §607/§1041b, and explicitly quantifies
≈1/3 non-causative -áya-stems in the RV), Kochergina (keeps curādi — Заn. XV — and
causative — Заn. XXXV — structurally and silently separate, with no homonymy caveat),
and TolchelnikovTalmud_2026 (its `CAUS.` allomorph-selection formalism doesn't address
the traditional ten-class scheme at all). The specific Knauer caveat the visa recalls
could **not** be located in the org archive — only
[KnauerFrazy_1908](https://github.com/gasyoun/SanskritGrammar/tree/main/KnauerFrazy_1908)
(an exercise companion citing paragraph numbers into Knauer's fuller grammar, e.g.
"*impf. caus. (§ 183)*") is on disk, not the grammar text itself — so it is parked as a
source-not-found, per the same convention WF06 hit before Leitan's notes were located
(H1346). `EDITORIAL_NOTE_INDEX.tsv`'s `w2-core#MO28` row flipped `OPEN` → `APPLIED`.

## Leftovers

None outstanding for this sheet. MO12 and V carried no note (empty `note` field in the
decisions JSON) — publication alone (H1316) fully dispositions them; no
`EDITORIAL_NOTE_INDEX.tsv` row is owed, matching the convention already used for the
causative visa's own empty-note items (MO028-01/02/03/04/06/10). The one open thread is
the Knauer source-location gap above — future work only if the grammar text surfaces
elsewhere in the org (same search path as Leitan's: IndologyScholars, external catalogues).

_Dr. Mārcis Gasūns_
