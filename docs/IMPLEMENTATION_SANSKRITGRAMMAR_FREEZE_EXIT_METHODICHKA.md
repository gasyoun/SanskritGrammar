# Implementation — freeze exit + methodichka residual (wave 1)

_Created: 24-07-2026 · Last updated: 24-07-2026_

Cover:
[`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md).

Work only in a **fresh worktree** off `origin/main` (`.githooks` refuses direct commits in the shared main tree).

## Step 0 — shared bootstrap (every handoff)

1. `git fetch origin` and compare `HEAD..origin/main`.
2. Claim handoff via `claim_handoff.py`; open tracking issue if the handoff requires it.
3. Read the PLAN cover decisions table + this step list for the handoff's ID only.
4. Run baseline green: `python -m pytest` (or the subset the handoff names) and note starting state.

## Step A0 — kill-gate matrix (Sonnet)

1. Load `sangram/editorial/data/consolidation_ledger.json` → filter `disposition == "unknown"` (expect 15).
2. For each `toc_ref`, open the matching article `article.manifest.json` + index.mdx + C5 or C6 programme section that owns that slot.
3. Quote the kill-gate criterion verbatim into the matrix row; locate any existing `scripts/sg_*` or `sangram/audit/probe_*` script; mark `MISSING` if none.
4. Write `sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md` (table + provenance date + model tier+version).
5. Do **not** run probes in A0.
6. PR: matrix only + CHANGELOG bullet.

## Step A1 — SE cluster probes (Opus)

Depends on A0 (may proceed with an inline matrix if A0 not merged, but must not invent criteria).

1. Restrict to SE unknowns: SE-001, SE-002, SE-003, SE-004, SE-005, SE-006, SE-008, SE-013 (and any other SE still `unknown` per ledger — **not** SE-009 if published).
2. Per article: implement or re-run the matrix kill-gate; write `sangram/audit/probe_freeze_<art_id>.py` + `.json` result + short `.md` note citing criterion pass/fail.
3. Update ledger row: `kill_gated` + links on clear fail; on survive leave disposition `unknown` and clear `blocking_note`; on ambiguity set `blocking_note` and skip.
4. `python scripts/consolidation_ledger_refresh.py` if the handoff expects refreshed evidence fields.
5. `python scripts/article_validate.py --all` + `python -m pytest` + `npm run build` (or document build skip if only JSON/md under audit and CI already covers validate).
6. PR with probe artifacts + ledger delta; list survivors explicitly in PR body for A3.

## Step A2 — MO/WF stragglers (Opus)

Same as A1 for: MO-019, MO-022, MO-024, MO-025, WF-002, WF-009, WF-011.

Prefer reusing morphology pilot scripts from published siblings (a-stems, perfect, taddhita) rather than new frameworks.

## Step A3 — SE survivor visa sheet (Sonnet)

Blocked until A1 survivor list is on `origin/main`.

1. Read A1 PR / matrix survivors.
2. Author `review/specs/sangram-se-freeze-survivors-visa_<DD.MM.YY>.json` with one card per survivor (title, path, kill-gate summary, approve/reject/defer).
3. `python scripts/build_visa_sheet.py …` → HTML under `review/`.
4. Register sheet in [Uprava/REVIEW_SHEETS_INDEX.md](https://github.com/gasyoun/Uprava/blob/main/REVIEW_SHEETS_INDEX.md).
5. Do **not** invent votes; stop when sheet is ready for human.

## Step B1 — Apte residual (Fable)

1. Read `review/EDITORIAL_NOTE_INDEX.tsv` rows for Apte target with OPEN/PARTIAL.
2. For each: apply if evidence is in-repo; else DEFER/ESCALATE with reason (zan-19: Elizarenkova scan `@DO`).
3. Update methodichka revision history; flip index `applied_status`.
4. Do not assert Likhushina rights beyond existing framing.
5. PR + changelog under Apte book or root as appropriate.

## Step B0 — H1454

Execute the existing handoff file; do not duplicate its scope here.

## Step C0 — hygiene (Sonnet)

1. List `Uprava/handoffs/*SanskritGrammar*` active files + registry 🟡 rows.
2. For each: if merged PR / 🔴 EXECUTED / SUPERSEDED banner → archive path + registry flip via house procedure.
3. Do not execute research handoffs during hygiene.
4. Emit a short `docs/` or handoff-body report of remaining live 🟡.

## Shared validation commands

```text
python scripts/article_validate.py --all
python scripts/consolidation_ledger_refresh.py
python -m pytest
npm run build
```

_Dr. Mārcis Gasūns_
