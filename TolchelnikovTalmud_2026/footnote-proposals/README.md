# Footnote proposals — правило согласования с автором

_Created: 06-07-2026 · Last updated: 06-07-2026_

Every **data-derived enrichment** to the *Talmud санскрита* (frequency notes,
Whitney references, seṭ/aniṭ corrections, missing roots, paradigm checks derived
from [WhitneyRoots](https://github.com/gasyoun/WhitneyRoots) or any other dataset)
is a **proposal that Ivan (I.E. Tolchelnikov, the author) must approve** — never a
silent edit to the author's running text. This mirrors the repo's `errata.yml`
"source + generate" pattern.

Workflow:

1. Add a row to [`proposals.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/footnote-proposals/proposals.yml)
   with the schema documented in the file header (`id` is append-only), `status: pending`.
2. Surface the pending queue to Ivan as a `/review-sheet` interactive HTML voting
   sheet (markdown checkboxes are banned).
3. Only after a row carries `approved_by: Ivan` may the proposal become an MDX
   footnote **with source attribution** in the book text (`status: applied`).
   Rejected proposals stay logged with `status: rejected`.

Rule of record: **no enrichment enters the author's running text without an
`approved_by: Ivan` line** — see
[`IMPROVEMENT_PLAN.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/IMPROVEMENT_PLAN.md).

_Dr. Mārcis Gasūns_
