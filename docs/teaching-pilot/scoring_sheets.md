# Transfer-pilot scoring sheets — rubric (PROPOSED) + blank templates

_Created: 11-11-2026 · Last updated: 11-11-2026 · H8030 · Part of [`READING_TRANSFER_PILOT_PROTOCOL_2026.md`](READING_TRANSFER_PILOT_PROTOCOL_2026.md)_

> **PROPOSED — requires study approval before use** (protocol §5, row 2). No learner has been scored.

## 1. Rubric — per held-out item (0–6)

| Criterion | 0 | 1 | 2 |
|---|---|---|---|
| **C1 — Grouping / head** | Wrong or no grouping; head misidentified | Right members, wrong nesting/head, or partial grouping | Head + constituent grouping correct (Klammerdiagramm-equivalent) |
| **C2 — Category / relation** | No defensible relation | Correct family (e.g. татпуруша) with hedged/incorrect qualifier | Compound category or relation correctly defended (whichever the item's task asks) |
| **C3 — Translation** | No translation or unrelated | Acceptable RU rendering with alignment defects or sense drift | Defensible RU translation, source-word alignment intact (Klammerübersetzung convention) |

- **Item pass = total ≥ 4 AND C1 ≥ 1** (grouping is the load-bearing skill; a lucky translation cannot pass alone).
- **Accepted answers:** the key's `main` analysis, plus any answer whose `alternative_status` is
  `REVIEWED-ACCEPTED`. Today **every row is `PENDING_NO_SECOND_REVIEWED_READING`** — so only the main
  reading scores. Machine-generated candidates are never accepted answers.
- **Primary measure:** count of held-out items passed (0–10). Secondary: per-criterion medians.
  Report counts/medians/IQR and Wilson 95% CI for proportions; never a lone percentage.

## 2. Blind-scoring order (anti-leakage)

1. Learner attempts the held-out item **with aids removed**; the attempt is recorded first.
2. Only then is the key consulted for scoring. A revealed analysis before the attempt voids that item.
3. Worked/practice items never reappear in the held-out measure — a displayed answer is not transfer.

## 3. Per-learner blank sheet (copy per participant; pseudonymous ID only — no names in the repo)

```
learner_id: ________        session: □ immediate   □ retention (+4 wk, PROPOSED)
                                                        C1  C2  C3   total  pass?
held-out item H01  surface: ____________                __  __  __    __    □
held-out item H02  surface: ____________                __  __  __    __    □
held-out item H03  surface: ____________                __  __  __    __    □
held-out item H04  surface: ____________                __  __  __    __    □
held-out item H05  surface: ____________                __  __  __    __    □
held-out item H06  surface: ____________                __  __  __    __    □
held-out item H07  surface: ____________                __  __  __    __    □
held-out item H08  surface: ____________                __  __  __    __    □
held-out item H09  surface: ____________                __  __  __    __    □
held-out item H10  surface: ____________                __  __  __    __    □
passes (of 10): ____   median total: ____   time-on-task: ____   □ completed  □ attrited
```

- Surfaces are printed on the sheet from `transfer_pilot_items.tsv` at run time; the sheet carries **no answers**.
- Inter-scorer check: two scorers independently score the same 3 items; disagreement rate is a pilot output.
- **Attrition is a datum**: non-completion is recorded, never dropped silently.

## 4. Aggregate roll-up (filled only by an approved run)

```
date: __________  scorer(s): __________  approvals 1–8 of protocol §8 signed: □ yes
n invited: ____   n completed: ____   n attrited: ____
passes of 10: median ____  IQR ____  Wilson95% CI for (≥6 passes) proportion: [____, ____]
criterion medians: C1 ____  C2 ____  C3 ____      expansion threshold (§5): □ met  □ not met
notes / instrument problems: __________________________________________
```
