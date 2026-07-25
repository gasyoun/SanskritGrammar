# Verification — SanskritGrammar pedagogy last-mile residual

_Created: 25-07-2026 · Last updated: 25-07-2026_

Acceptance criteria, commands, and risks for
[`docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md).

## 1. Acceptance criteria

### A1 — H-A methodichka residual

| # | Criterion | Proof |
|---|---|---|
| A1.1 | Zero OPEN in-scope methodichka notes | Residual table in PR: every id → APPLIED / DEFERRED / re-sheeted |
| A1.2 | Every APPLIED note cites `sheet_id#item_id` | Revision-history grep |
| A1.3 | No invented corpus numbers | Diff review: numbers only from committed JSON/TSV or prior published claims |
| A1.4 | Re-vote sheets exist for remaining null/blocked cards | Sheet HTML + decisions.json path listed (or “already voted” evidence) |
| A1.5 | Suite green if code/site touched | `python -m pytest` and/or `npm run build` as applicable |

### A2 — H-B pedagogy export

| # | Criterion | Proof |
|---|---|---|
| A2.1 | `data/pedagogy_export/export_manifest.json` exists with `schema_version` | File present |
| A2.2 | `python scripts/build_pedagogy_export.py --check` exit 0 | Command log |
| A2.3 | `tests/test_pedagogy_export.py` passes | pytest |
| A2.4 | LAST_MILE spec records measured Systema hop status | Section dated ≥ 25-07-2026 |
| A2.5 | No rights-grey bulk in export | Manifest `rights` fields + omit log |

### A3 — H-C Systema smoke

| # | Criterion | Proof |
|---|---|---|
| A3.1 | One path: export → Systema load → ≥1 item renders without error | Command log + item id |
| A3.2 | Production `features.rq4_study` **not** flipped by the agent | Config/PR diff shows no prod enable |
| A3.3 | `schema_version` major accepted | Smoke log records version |
| A3.4 | Results persisted | VERIFICATION checklist ticks + RESULTS_LOG or GTD row + issue comment if tracking |

### Wave-1 plan close

All of A1–A3 green (or A3 soft-failed only under absolute env impossibility with explicit log — then plan is “partial close” and a follow-up handoff is minted, not silently dropped).

## 2. Reproduce commands

### SanskritGrammar

```powershell
cd C:\Users\user\Documents\GitHub\SanskritGrammar
python scripts/build_pedagogy_export.py
python scripts/build_pedagogy_export.py --check
python -m pytest tests/test_pedagogy_export.py -q
# if site MDX changed:
npm run build
```

### Systema (H-C — exact filter may match repo’s current test names)

```powershell
cd C:\Users\user\Documents\GitHub\Systema-Sanscriticum
# after copying/updating vendored item bank from SG export:
php artisan test --filter=Rq4
```

Record the **actual** commands that passed in the smoke PR; if filters renamed, update this section in the same PR.

## 3. Risks & spikes register

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | Methodichka “OPEN” count wrong (already applied) | Med | Wasted re-edit | Audit step 1 mandatory; evidence pointers |
| R2 | Rights-grey feed almost included | Med | Publish incident | Omit-by-default; publish-safety on any public action |
| R3 | Systema env cannot run PHP smoke here | Med | A3 blocked | Document; use test filter; partial close + follow-up |
| R4 | LAST_MILE spec still says “planned” after hops shipped | High (pre-plan) | Agent rebuilds hops | H-B measured-status section |
| R5 | Parallel freeze work creeps in | Med | Budget steal | ≤20% shared-gate rule; bank unused |
| R6 | Prod flag flipped by mistake | Low | Live study without ops | Fence + PR review of config |
| R7 | WF004 re-votes expand into full Sangram rewrite | Med | Scope blow | Re-sheet only; no silent article rewrite |
| R8 | Export schema churn breaks Systema | Med | Smoke red | semver major; pin min version |

## 4. Checklist (tick on close)

- [ ] A1 residual table committed / in merged PR
- [ ] A2 export + `--check` green
- [ ] A2 LAST_MILE measured-status section live
- [ ] A3 smoke log with item id + schema_version
- [ ] A3 prod flag untouched
- [ ] CHANGELOG `[Unreleased]` bullets in touched repos
- [ ] `.ai_state.md` Next Steps point at any residual human @DO (prod RQ4 flip)
- [ ] GTD / RESULTS row + tracking issue comment if applicable

## 5. Post-wave human @DO (not agent wave-1)

| Item | Why human |
|---|---|
| Flip production `features.rq4_study` + deploy ops | H1261 residual; ruling 26 |
| Vote re-opened methodichka/WF004 sheets | Human scholarly judgment |
| M03 RWS yellow-docx review | Outside fence |
| Publisher «Нестор-История» contact | Outside this plan |

---

_Dr. Mārcis Gasūns_
