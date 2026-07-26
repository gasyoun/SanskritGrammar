# Verification — SanskritGrammar pedagogy last-mile residual

_Created: 25-07-2026 · Last updated: 26-07-2026_

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

**A1 status (H1454 Kochergina, 26-07-2026, Grok 4.5 `grok-4.5`):** residual table in
[`KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md)
appendix «Открытые вопросы визы (H1258) — residual после H1454». Sheet
`sanskritgrammar-metodichka-kochergina-v1_16.07.26` items terminalized in
[`review/EDITORIAL_NOTE_INDEX.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv)
(APPLIED / DEFERRED / ESCALATED / re-sheeted — no OPEN left on this sheet).
Re-vote sheet: [`review/sanskritgrammar-metodichka-kochergina-zan10-rewrite_26.07.26_review.html`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/sanskritgrammar-metodichka-kochergina-zan10-rewrite_26.07.26_review.html)
(spec under `review/specs/`). Numbers from
`hk_peri_formation_share_h1454.json` / `hk16_feminine_ending_probe_h1454.json` / DCS
probes only. **Apte residual (H1615) is out of this PR’s scope.**

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

- [x] A1 residual table committed / in merged PR — H1454 Kochergina ([PR #525](https://github.com/gasyoun/SanskritGrammar/pull/525)); H1615 Apte ([PR #524](https://github.com/gasyoun/SanskritGrammar/pull/524))
- [x] A2 export + `--check` green — H1643 ([PR #523](https://github.com/gasyoun/SanskritGrammar/pull/523)); re-verified 26-07-2026: schema 1.0.0, 6 feeds, pytest green
- [x] A2 LAST_MILE measured-status section live — H1643 §0 Measured status (25-07-2026)
- [x] A3 smoke log with item id + schema_version — H1644 Systema ([PR #699](https://github.com/gasyoun/Systema-Sanscriticum/pull/699)): `pedagogy:sync-sg-export` + `SyncPedagogyExportFromSgTest` (local artisan re-run 26-07 blocked: no `vendor/` in this clone)
- [x] A3 prod flag untouched — H1644 fence; no prod `features.rq4_study` flip
- [x] CHANGELOG `[Unreleased]` bullets in touched repos — SG + Systema release notes for H1643/H1644/H1454/H1615
- [x] `.ai_state.md` Next Steps point at residual human @DO (prod RQ4 flip + zan-10 vote + errata/Miller/Konspekt)
- [x] Registry close H1454/H1615/H1643/H1644 → ✅ (Uprava handoff_close + reconcile flush 26-07-2026)

## 5. Post-wave human @DO (not agent wave-1)

| Item | Why human |
|---|---|
| Flip production `features.rq4_study` + deploy ops | H1261 residual; ruling 26 |
| Vote re-opened methodichka/WF004 sheets | Human scholarly judgment |
| M03 RWS yellow-docx review | Outside fence |
| Publisher «Нестор-История» contact | Outside this plan |

---

_Dr. Mārcis Gasūns_
