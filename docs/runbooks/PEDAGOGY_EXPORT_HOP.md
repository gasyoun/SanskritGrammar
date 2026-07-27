# Runbook — pedagogy export → Systema hop

_Created: 26-07-2026 · Last updated: 26-07-2026_

Operator contract for every future SanskritGrammar (SG) pedagogy-export → Systema-Sanscriticum
vendor → smoke cycle. Consumed by the org `/export-consumer-smoke` skill for this repo pair.
Authored by [H1673](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1673-Sonnet_SanskritGrammar_runbook-pedagogy-export-hop_26.07.26.md);
does **not** re-implement the export builder ([H1643](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1643-Sonnet_SanskritGrammar_pedagogy-export-adapter-last-mile_25.07.26.md))
or the Systema smoke ([H1644](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H1644-Sonnet_Systema-Sanscriticum_pedagogy-export-hop-smoke_25.07.26.md)) — both are DONE; this is the durable how-to for repeating the cycle.

## 0. Soft-dependency state

| Handoff | Status | What it shipped |
|---|---|---|
| H1643 (SG export adapter) | ✅ EXECUTED 26-07-2026 ([PR #523](https://github.com/gasyoun/SanskritGrammar/pull/523)) | `scripts/build_pedagogy_export.py`, `data/pedagogy_export/`, schema 1.0.0 |
| H1644 (Systema smoke) | ✅ EXECUTED 26-07-2026 ([PR #699](https://github.com/gasyoun/Systema-Sanscriticum/pull/699)) | `pedagogy:sync-sg-export` artisan command, `Rq4`/`SyncPedagogyExportFromSg` test suites, flag OFF |

Both are done, so the commands below are the **actual commands that passed**, not a skeleton —
see §2.

## 1. Ordered steps

```powershell
# 1. Build the export (SanskritGrammar repo)
cd C:\Users\user\Documents\GitHub\SanskritGrammar
python scripts/build_pedagogy_export.py

# 2. Validate it (schema_version + per-feed sha256)
python scripts/build_pedagogy_export.py --check
# expect: OK: 6 feeds, schema_version=1.0.0

# 3. Vendor/copy into Systema (Systema-Sanscriticum repo)
cd C:\Users\user\Documents\GitHub\Systema-Sanscriticum
php artisan pedagogy:sync-sg-export --path=C:\Users\user\Documents\GitHub\SanskritGrammar\data\pedagogy_export
# reads export_manifest.json (schema major >= 1), verifies sha256, copies
# rq4_item_bank into resources/data/rq4_item_bank.json

# 4. Smoke the consumer
php artisan test --filter=SyncPedagogyExportFromSg
php artisan test --filter=Rq4

# 5. Record schema_version + item id (see §2 for the last recorded values)
```

## 2. Last recorded smoke (H1644, 25-07-2026)

| Field | Value |
|---|---|
| `schema_version` | 1.0.0 |
| item count | 24 |
| first item id | `yat` |
| `SyncPedagogyExportFromSg` tests | 2 passed |
| `Rq4` tests | 11 passed |
| prod `features.rq4_study` | OFF (unchanged) |

Source: [Systema PR #699](https://github.com/gasyoun/Systema-Sanscriticum/pull/699) test-plan section.
Update this table (date, counts, item id) every time the hop is re-run for a new export cut.

## 3. Flag-OFF fence

Production `features.rq4_study` is **never** flipped by this path. Every step above runs
against local/staging Systema only. Flipping the flag for a real study cohort is a **human
@DO** (tracked as the H1261 residual) — it requires ops/deploy sign-off outside this runbook's
scope. If a future agent run of this hop touches `config/features.php` or any prod env file to
set that flag `true`, that is a fence violation and must be reverted, not merged.

## 4. Rights fence

Only feeds marked `rights: aggregate-public-safe` or `rights: pointer-only-no-bulk-gloss` in
`export_manifest.json` are vendored. `methodichka_corpus_layer_pointers` is pointer-only — it
carries paths to methodichka corpus layers, never bulk textbook gloss text. Any feed whose
rights status is unclear at build time is **omitted** by the builder (see `omissions: []` in
the manifest) and logged, not silently included.

## 5. Failure table

| Symptom | Likely cause | Fix |
|---|---|---|
| `build_pedagogy_export.py --check` reports `FAIL: feed <id>: path/sha256 missing` | Manifest references a feed file that was deleted/renamed, or `build` was never run before `--check` | Re-run `python scripts/build_pedagogy_export.py` (no `--check`) to regenerate, then re-check |
| `--check` reports `FAIL: feed <id>: sha256 drift` | The feed file's bytes changed after the manifest was written — **or** a Windows checkout with `core.autocrlf=true` silently rewrote the committed JSON's line endings on clone (LF→CRLF), so the working-tree sha256 no longer matches the pinned hash even though content is unchanged. Reproduced live during H1673 authoring on `methodichka_corpus_layer_pointers.json` | Confirm with `git diff <file>` — if git only warns about CRLF and shows no content diff, this is the autocrlf case: re-run `build` to regenerate the manifest against the current working-tree bytes (do **not** hand-edit the hash). If `git diff` shows a real content change, investigate before regenerating — an unexplained content drift is a data-integrity signal, not a formatting one |
| `php artisan pedagogy:sync-sg-export` errors on schema major | SG bumped `schema_version` to a new major and Systema's loader still pins the old major | This is the intended breaking-change gate (semver major = R8 in VERIFICATION §3) — update Systema's loader to accept the new major, do not force the version down |
| `php artisan test --filter=Rq4` fails or the whole PHP suite is unreachable | Local PHP/Composer/Systema env not bootstrapped in this session (no `vendor/`, no `.env`, DB not migrated) | Document the blocked step explicitly (env, missing binary, error text) and stop — do not skip the smoke silently. This is the same class of soft-failure VERIFICATION §3 R3 already anticipates: log it, don't force it green |

## 6. Pointers

- Measured hop status (Hops A/B/C, RQ4 harness — **already shipped in Systema, do not
  re-implement**): [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md) §0.
- Manifest hop-status block: `last_mile_hop_status` in
  [`data/pedagogy_export/export_manifest.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/data/pedagogy_export/export_manifest.json).
- Verification acceptance criteria + risk register:
  [`docs/VERIFICATION_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/VERIFICATION_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE.md) §2 (reproduce commands), §3 (risks).
- Org skill this runbook is the SG-side contract for: `/export-consumer-smoke`.

---

_Dr. Mārcis Gasūns_
