# Implementation — SanskritGrammar pedagogy last-mile residual (wave-1)

_Created: 25-07-2026 · Last updated: 25-07-2026_

File-level, step-ordered build sequence for the three wave-1 handoffs.
Cover: [`docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md).
Autonomy contract: that PLAN § “Autonomy contract”.

**Worktrees** preferred on shared-contention clones; **pathspec commits**;
**UTF-8** I/O; model tier per handoff.

## Ordering

```text
H-A (Fable, SG)  ──┐
                   ├── (disjoint files) ──▶ both green on main
H-B (Sonnet, SG) ──┘
                          │
                          ▼
                   H-C (Sonnet, Systema)  ── depends on H-B export
```

H-A and H-B may run in parallel. H-C starts only after H-B’s export is on a
reachable commit (merged main preferred).

---

## H-A — Methodichka residual (REUSE existing handoffs — do not re-mint)

| Field | Value |
|---|---|
| Tier | **Fable 5** (`claude-fable-5`) |
| Repo | SanskritGrammar |
| Status | **Already staged** by freeze-exit plan B0/B1 |
| Kochergina | [H1454](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1454-Fable_SanskritGrammar_kochergina-metodichka-v1-open-items_22.07.26.md) |
| Apte | [H1615](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1615-Fable_SanskritGrammar_metodichka-apte-open-residual_24.07.26.md) |
| Unblocks | Clean companions; D1/D2 for *this* plan’s close checklist |

### Steps

1. **Execute H1454 and/or H1615** as written (whichever is still OPEN). Do **not** mint a parallel “pedagogy-last-mile-methodichka” handoff — mint guard correctly blocked that collision.
2. **Align acceptance with this plan’s A1** where possible: residual table, `sheet_id#item_id` citations, no invented numbers, re-sheets for `zan-29` / WF004-03/04/07 if still open after those handoffs.
3. If H1454/H1615 are already ✅ when this plan runs, mark D1/D2 satisfied with evidence links and skip.

### Starters (existing)

```text
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H1454-Fable_SanskritGrammar_kochergina-metodichka-v1-open-items_22.07.26.md and execute it.
```

```text
Read C:\Users\user\Documents\GitHub\Uprava\handoffs\H1615-Fable_SanskritGrammar_metodichka-apte-open-residual_24.07.26.md and execute it.
```

Folder: `C:\Users\user\Documents\GitHub\SanskritGrammar` · model: Fable 5 (`claude-fable-5`).

### Acceptance (H-A)

See VERIFICATION **A1** (satisfied by H1454+H1615 outcomes or prior evidence).

---

## H-B — Thin pedagogy export adapter + LAST_MILE gap close

| Field | Value |
|---|---|
| Tier | **Sonnet 5** (`claude-sonnet-5`) |
| Repo | SanskritGrammar |
| Depends on | Existing difficulty + item bank assets |
| Unblocks | H-C; D3/D4 |

### Steps

1. **Prior-art pass (mandatory, short):** confirm Systema H955/H959/H965/H987 surfaces still present (paths in ARCHITECTURE §1). Do **not** re-implement hops.

2. **Implement** [`scripts/build_pedagogy_export.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_pedagogy_export.py):
   - `build` mode writes `data/pedagogy_export/` + `export_manifest.json` (`schema_version` **1.0.0**).
   - `--check` mode validates paths + sha256 + supported major.
   - UTF-8; no BOM; Windows stdout reconfigure if printing.

3. **Feeds (defaults, public-safe):**
   - RQ4 item bank from `TolchelnikovTalmud_2026/data/rq4_item_bank.json`
   - `data/difficulty_ordering/*`
   - Methodichka corpus-layer **pointers** (paths + titles + optional visa flag)
   - `last_mile_hop_status` block per ARCHITECTURE §3.2
   - Omit any rights-grey candidate; log omission.

4. **Tests:** `tests/test_pedagogy_export.py` — build smoke, `--check` pass, intentional hash break fails, schema major mismatch fails.

5. **Update** [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md):
   - Add a dated “Measured status 25-07-2026” section: Hops A/B/C + RQ4 harness **shipped in Systema**; remaining = export packaging + local smoke + human prod flag.
   - Keep vendored-file ruling.
   - Point consumers at `data/pedagogy_export/`.
   - Bump “Last updated”; keep creation date.

6. **Wire:** optional `package.json` script `pedagogy-export` if npm scripts are the house pattern; else document pure python invoke in README snippet inside VERIFICATION.

7. **Ship:** commit → PR → merge green; changelog; ensure `--check` is runnable in CI **or** documented as local gate if CI job addition is blocked (default: add to existing python test job if present, else pytest discovery alone).

### Acceptance (H-B)

See VERIFICATION **A2**.

### Defaults on ambiguity

- Large binary/media → pointer only, not copy.
- CI job edit contested → rely on pytest discovery; log.
- Feed rights unclear → omit + log.

---

## H-C — Systema local/staging hop smoke

| Field | Value |
|---|---|
| Tier | **Sonnet 5** (`claude-sonnet-5`) |
| Repo | Systema-Sanscriticum |
| Depends on | H-B merged (or pinned commit with `data/pedagogy_export/`) |
| Unblocks | D5; plan wave-1 close |

### Steps

1. **Locate** cheapest existing load path (default: RQ4 item bank vendor at `resources/data/rq4_item_bank.json` + feature tests under `tests/Feature/Rq4*`).

2. **Sync feed** from SanskritGrammar export (copy or build script). Preserve Systema’s flag-OFF defaults. **Never** flip production `features.rq4_study`.

3. **Smoke command** (document the exact command(s) that passed), preferred order:
   1. `php artisan test --filter=Rq4` (or current equivalent) after feed refresh
   2. If needed, a minimal local route hit that renders one item (dev server)
   3. Fallback: Hop B/C demo loader if RQ4 path is environment-blocked — log which path

4. **Record** results table: command · exit · item id rendered · schema_version consumed · env (local/staging).

5. **If importer glue is missing** for the new manifest: add the **thinnest** possible loader (read manifest, verify min schema, copy item bank) behind existing patterns; flag default OFF. No money contour; no prod deploy.

6. **Ship:** commit → PR → merge green on Systema; link PR in SanskritGrammar VERIFICATION / RESULTS; GTD note that **prod flag remains human @DO**.

### Acceptance (H-C)

See VERIFICATION **A3**.

### Defaults on ambiguity

- Cannot run PHP in environment → document blocked env, run whatever is available, soft-fail with explicit “smoke incomplete” log (absolute fence only if zero credentials for the whole handoff).
- Multiple loaders → RQ4 item bank first.

---

## Thin parallel (≤20%) — only if blocked

If H-A/H-B blocked by red claims/errata/pytest:

1. Fix the **shared gate only** (minimal diff).
2. Do not open freeze or M03 work.
3. Log hours spent under “parallel budget”.

---

## Out-of-scope reminders (do not implement)

- Production RQ4 cohort recruitment
- New A## papers
- Sangram freeze exit mass disposition
- M03 RWS yellow-docx human review (human @DO)
- Live kosha API CORS

---

_Dr. Mārcis Gasūns_
