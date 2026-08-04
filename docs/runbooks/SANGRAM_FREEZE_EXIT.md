# Runbook — Sangram freeze-exit operator ladder

_Created: 27-07-2026 · Last updated: 27-07-2026_

Operator contract for future Sangram consolidation-freeze dispositions. Authored by
[H1676](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1676-Sonnet_SanskritGrammar_runbook-sangram-freeze-exit_26.07.26.md).
Does **not** re-run or re-derive freeze-15 wave-1 (H1611–H1614, all DONE) — this is the durable
how-to for the *next* freeze wave, and the branch decision procedure for any single
`toc_ref` still sitting at `disposition=unknown`.

## 0. What "freeze" means here

Sangram's consolidation freeze (ruled 18-07-2026, machine-gated by H1260) locks
`baseline_ids[]` to a fixed candidate set while `freeze.active=true` in the consolidation
ledger. No new Sangram topic manifest may be authored outside that set until every row
carries a disposition in `{published, revised, rejected, kill_gated}`. Plan of record:
[`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md).

## 1. The pipeline (freeze-N matrix → probe → kill_gate/survivor → visa-or-no-sheet)

This ladder is owned by the [`/sangram-freeze-killgate`](https://github.com/gasyoun/claude-config/blob/main/commands/sangram-freeze-killgate.md)
skill — this runbook cites its rung order, it does not re-implement it:

| Order | Rung | What it produces | Precedent |
|---:|---|---|---|
| 1 | **matrix** | freeze-N killgate matrix: rows = unknown `toc_ref`s, cols = C5/C6 gates, one script path + acceptance criterion per row | H1611 |
| 2 | **probe-se** | per-article C5/C6 probes on the SE cluster; each `toc_ref` lands in `kill_gated` / `blocking_note` / clear-gate **survivor** | H1612 |
| 3 | **probe-stragglers** | same probe discipline for MO/WF stragglers | H1613 |
| 4 | **survivor-visa** | branch on the survivor count (§2 below) | H1614 |

One rung per session unless a handoff explicitly names a pair and the prior rung is green.
Stop on the first red cell (§3) rather than widening the freeze.

## 2. The branch after probing — visa sheet **or** no-sheet

Rung 4 is not "always emit a visa sheet." Branch on what the probe rung actually found:

- **Survivors > 0** → one multi-article visa sheet per cluster (SE survivors together;
  a second small sheet or individual cards for non-SE survivors) via
  [`/review-sheet`](https://github.com/gasyoun/claude-config/blob/main/commands/review-sheet.md),
  then [`/decisions-apply --visa`](https://github.com/gasyoun/claude-config/blob/main/commands/decisions-apply.md)
  once votes exist. Never apply unvoted edits inline.
- **Survivors == 0 (H1614 pattern)** → **no review sheet, no GTD vote noise.** Write a short
  disposition memo under `sangram/audit/` instead — see §2.1 for the template — and close the
  handoff. `kill_gated` rows are excluded from any future survivor sheet by the handoff fence;
  `blocking_note` parks stay freeze-stuck until a later rung defines a fireable gate for them.

This zero-survivors branch is first-class, not a fallback: a handoff whose probe rung finds
zero survivors is **done**, not blocked, the moment the disposition memo lands.

### 2.1 Disposition-memo template (zero-survivors case)

Worked example: [`sangram/audit/H1614_se_freeze_survivors_visa_disposition.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/H1614_se_freeze_survivors_visa_disposition.md).
A disposition memo states:

1. **Verdict** — survivor count, one line.
2. **Bucket table** — `toc_ref` → `{kill_gated, blocking_note, survivor}` with the citing
   C5/C6 criterion, sourced from the upstream probe rung's merged artifact (do not re-run
   the probe to write the memo).
3. **What was not produced** — no `review/specs/*.json`, no HTML via
   `scripts/build_visa_sheet.py`, no `Uprava/REVIEW_SHEETS_INDEX.md` row, no invented votes.
4. **Fence** — did not flip `freeze.active`; did not cast votes; did not include
   `kill_gated` rows on a future sheet; did not re-run the upstream probe.
5. **Residual** — which rows remain freeze-stuck and why, explicitly marked as separate,
   future work rather than something this memo owes a fix for.

## 3. When to call `/sangram-freeze-killgate` vs. mint a new probe handoff

- **Call the skill directly** (no new handoff needed) when the next rung in the ladder is
  unambiguous — e.g. rung 2 (SE probe) is green and rung 3 (MO/WF stragglers) is simply next
  in order with an already-defined instrument.
- **Handoff-mint a new probe** when: the matrix (rung 1) does not yet cover a `toc_ref`; a
  `blocking_note` park needs a newly fireable C5/C6 gate that does not exist yet; or a
  *different* grammar's freeze wants this ladder for the first time (the skill is reusable
  across grammars if the matrix shape holds, but the first run for a new corpus still needs
  its own matrix handoff).
- **Never** re-derive rung order or re-invent a kill-gate threshold ad hoc — an ambiguous
  criterion is a park-and-skip (`blocking_note` / `@DECIDE`), not an invented number.

## 4. What an agent may still touch while "freeze is frozen"

`freeze.active=true` blocks new Sangram topic manifests outside `baseline_ids[]`. It does
**not** block:

- Shared consolidation-ledger and validator maintenance (`scripts/consolidation_ledger_refresh.py`,
  `scripts/article_validate.py`).
- Errata (`errata.yml` → `npm run errata`) and claims-layer upkeep (`npm run claims` /
  `npm run check-claims`) on already-published books.
- CI, docs, and this runbook's own kind of operator documentation.
- Probe scripts and disposition memos under `sangram/audit/` for rows already inside the
  frozen candidate set — probing an existing candidate is disposition work, not a new
  manifest.

It **does** block: any new topic manifest outside `baseline_ids[]`, any `freeze.active=false`
flip before every row has a disposition, and any invented kill-gate threshold or scholarly
judgment not already sourced from the freeze-exit plan or a programme document
(`sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx`, `sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx`).
Full fence: [`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md)
§ Autonomy contract.

## 5. Pointer to disposition-artifact examples

- Zero-survivors memo: [`sangram/audit/H1614_se_freeze_survivors_visa_disposition.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/H1614_se_freeze_survivors_visa_disposition.md)
- Upstream probe roll-up it cites: [`sangram/audit/probe_freeze_se_H1612_survivors.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/probe_freeze_se_H1612_survivors.md)

_Dr. Mārcis Gasūns_
