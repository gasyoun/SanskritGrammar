# Verification — freeze exit + methodichka residual

_Created: 24-07-2026 · Last updated: 24-07-2026_

Cover:
[`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md).

## 1. Acceptance per deliverable

| ID | Acceptance criterion | Prove with |
|---|---|---|
| A0 matrix | 15/15 unknown toc_refs; criterion quoted from C5/C6; script path or `MISSING` | file exists; row count; no invented thresholds |
| A1 SE probes | Each SE unknown has probe artifact; ledger updated; survivors listed | `sangram/audit/probe_freeze_*`; ledger diff; validate/pytest green |
| A2 MO/WF probes | Same for 6 stragglers | same |
| A3 SE visa sheet | Cards = SE survivors only; HTML generated from spec; index registered | spec card count == survivor count; `build_visa_sheet` exit 0 |
| B1 Apte residual | No bare OPEN on Apte target without disposition | `EDITORIAL_NOTE_INDEX.tsv` filter |
| B0 H1454 | Per H1454 stop condition | H1454 body |
| C0 hygiene | No merged-but-🟡 SG rows left without archive | registry grep |

## 2. Global green bar (every PR)

```text
python scripts/article_validate.py --all
python -m pytest
npm run build
```

If build is environment-blocked (Windows ENOTEMPTY), re-run in a clean worktree or rely on CI — do not claim green without a log.

## 3. Risks and spikes

| Risk | Severity | Mitigation |
|---|---|---|
| C6 kill-gate text underspecified for an SE slot | high | A0 marks `MISSING` criterion detail; A1 parks with `blocking_note`; no invented threshold |
| Concurrent session flips a candidate mid-probe (H214) | medium | worktree off fresh origin/main; re-read ledger before write |
| Probe changes a published DCS figure without re-run | high | fence: numbers change only with probe JSON + changelog |
| H1454 and B1 both edit methodichka index | low | disjoint targets (Kochergina vs Apte) |
| Visa sheet cut before probes finish | high | A3 blocked on A1 survivor list on origin/main |
| Agent flips `freeze.active` early | critical | fence in autonomy contract; W3 only mechanical exit check |
| zan-19 blocked on missing scan | low | escalate; do not fabricate Elizarenkova content |

## 4. What is deliberately unverified this wave

- Full freeze exit (`freeze.active=false`) — needs W2 human votes + apply.
- M03 manuscript freeze — human.
- RQ4 live recruitment — human feature flag.
- A65 OPEN research notes (6) — not in wave-1 methodichka elevation unless a later sitting adds them.

_Dr. Mārcis Gasūns_
