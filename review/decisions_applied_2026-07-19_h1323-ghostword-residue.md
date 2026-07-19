# Decisions applied — H1323 PWG ghost-word residue (16 words)

_Created: 19-07-2026 · Last updated: 19-07-2026_

Audit record for the human vote on the H1323 ghost-word residue, applied via
[`/decisions-apply`](https://github.com/gasyoun/claude-config/blob/main/commands/decisions-apply.md).

- **Sheet:** [`review/sanskritgrammar-pwg-ghostword-residue_h1323_review.html`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/sanskritgrammar-pwg-ghostword-residue_h1323_review.html)
- **Decisions file:** [`review/sanskritgrammar-pwg-ghostword-residue_h1323_decisions.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/sanskritgrammar-pwg-ghostword-residue_h1323_decisions.json) (voted 19-07-2026, reviewer `gasyoun`)
- **Applied to:** [`data/pwg_ghostword_triage/pwg_ghostword_residue_adjudicated.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/pwg_ghostword_triage/pwg_ghostword_residue_adjudicated.tsv) (new) + [`README.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/pwg_ghostword_triage/README.md) § Human adjudication

## Counts

| Verdict | Count |
|---|---:|
| approve → `confirmed_ghost` | 11 |
| reject | 5 |
| defer | 0 |
| **total** | **16** |

All 16 items carried a vote; no unvoted, no unknown IDs, 1:1 against the residue manifest.

## Rejected (5) — with reason

| k1 | Voter reason |
|---|---|
| `BAgApahArajAti` | Decomposable — `BAga` + `apahAra…`; a saṃāsa split, not a clean unique ghost. |
| `bfhatsUryasidDAnt` | Technical / astronomical title (Bṛhat-Sūryasiddhānta). |
| `ISvare` | Untranslated German residue (`desgl.`) + gloss/translation gaps. |
| `KamBAyatabindara` | Untranslated German residue (`ebend.`). |
| `babakARa` | Untranslated German residue (`ebend.`). |

Per `/decisions-apply` Phase 2, rejected items are recorded here and are **not** re-surfaced in a
future sheet unless the underlying data changes.

## Confirmed ghost-words (11)

`cuwikA` · `hUNgarAI` · `isPIva` · `isaPahARa` (Isfahan) · `mugasTAna` · `namiTuna` ·
`oqISadeSa` (Odisha) · `pArAsapuli` (Persepolis) · `upayicArika` · `uterijA` · `viviwwyE` —
the final, human-signed floor of the H1310 → H1323 study.

## Voter feedback routed onward (not part of the ghost verdict)

Several notes are **pwg_ru data-quality observations**, not ghost-word judgements, and belong to
the existing pwg_ru cleanup track (German-residue sweep, H1301–H1308), not this study:

- Untranslated German left in the RU portrait: `ebend.`, `desgl.`, `<ls>` (words above + `hUNgarAI`
  "why 2 × `ebend.`? fix at Cologne data level?").
- Untranslated fragments / short words (`v. u.`, the `_in_` underscore markup, "короткие слова без перевода").
- Gloss truncation: `upayicArika` should read "Wächter eines *Vihāra*", not "Wächter eines".

These are captured here for the pwg_ru cleanup owner; no action taken in this pass.

## Leftovers

None — all 16 applied. No csl-orig correction pipeline involved (this is a study dataset, not a
text correction); nothing queued for `/cologne-correction-queue`.

_Dr. Mārcis Gasūns_
