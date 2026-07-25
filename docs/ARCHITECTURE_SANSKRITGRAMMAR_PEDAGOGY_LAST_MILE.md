# Architecture — SanskritGrammar pedagogy last-mile residual

_Created: 25-07-2026 · Last updated: 25-07-2026_

Component boundaries and contracts for
[`docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE_2026H2.md).

## 1. System context (prior-art, not aspirational)

| Layer | What already exists | Owner |
|---|---|---|
| Difficulty / ordering result | [`data/difficulty_ordering/`](https://github.com/gasyoun/SanskritGrammar/tree/main/data/difficulty_ordering) + [`scripts/build_difficulty_ordering.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_difficulty_ordering.py) | SanskritGrammar (H913) |
| RQ4 item bank | [`TolchelnikovTalmud_2026/data/rq4_item_bank.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/rq4_item_bank.json) | SanskritGrammar (H984) |
| Last-mile **spec** | [`docs/LAST_MILE_PIPELINE_SPEC.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/LAST_MILE_PIPELINE_SPEC.md) | SanskritGrammar (H916) |
| Hop A reader demo | Systema Livewire reader path | Systema (H959) |
| Hop B SRS demo import | Systema seeder/import path | Systema (H955) |
| Hop C difficulty advisory | Systema lesson advisory consumption | Systema (H965) |
| RQ4 study harness | `/rq4-study`, item bank vendor, consent, tests | Systema (H987); preflight H1261 |
| Methodichkas | Apte + Kochergina companions + corpus layers | SanskritGrammar (H807/H1258/H1297…) |

**Build-vs-reuse verdict:** **reuse all of the above**. This plan adds only (1) residual editorial apply, (2) a **thin export adapter** that packages SG public-safe feeds, (3) a smoke that consumes that package in Systema **local/staging**.

## 2. Boundary: research repo vs product repo (ruling 7, 12)

```text
┌─────────────────────────────┐         vendored file          ┌──────────────────────────────┐
│ SanskritGrammar (research)  │  ──── pedagogy_export vN ───▶  │ Systema-Sanscriticum (T0)    │
│  · methodichkas             │         (JSON/TSV +           │  · RQ4 harness (flag OFF)    │
│  · difficulty_ordering      │          schema_version)       │  · Hop A/B/C demos           │
│  · rq4_item_bank            │                                │  · Saraswati SRS             │
│  · LAST_MILE spec           │                                │  · local/staging smoke only  │
└─────────────────────────────┘                                └──────────────────────────────┘
```

- **SanskritGrammar must not** grow a second learner app, consent UI, or payment surface.
- **Systema must not** become the source of truth for claim registers, methodichka prose, or difficulty derivation scripts.
- Contract pattern matches the shipped [`SanskritGlossary.php`](https://github.com/gasyoun/Systema-Sanscriticum/blob/main/app/Services/SanskritGlossary.php) **vendored static feed** rule (“НЕ живая зависимость от kosha”).

## 3. Pedagogy export adapter (ruling 14, 29)

### 3.1 Paths (ruling 15)

| Path | Role |
|---|---|
| `scripts/build_pedagogy_export.py` | Builder + `--check` mode |
| `data/pedagogy_export/export_manifest.json` | `schema_version`, content hashes, feed list |
| `data/pedagogy_export/*.tsv` / `*.json` | Snapshot copies or generated compact views of **public-safe** feeds |
| `tests/test_pedagogy_export.py` | Round-trip + schema drift gate |

### 3.2 Manifest schema (semver, ruling 20)

Minimum fields (implementation may add optional keys; removing/renaming is a **major** bump):

```json
{
  "schema_version": "1.0.0",
  "generated_at": "ISO-8601",
  "generator": "scripts/build_pedagogy_export.py",
  "feeds": [
    {
      "id": "rq4_item_bank",
      "path": "…",
      "sha256": "…",
      "rights": "aggregate-public-safe",
      "consumer_hint": "Systema resources/data/rq4_item_bank.json"
    }
  ],
  "last_mile_hop_status": {
    "A_reader": "shipped-in-Systema",
    "B_srs": "shipped-in-Systema",
    "C_difficulty": "shipped-in-Systema",
    "rq4_harness": "shipped-flag-off"
  }
}
```

**Default feeds to include (public-safe):**

1. RQ4 item bank (or checksum + relative source path if copy is large — default: include file if already in-repo and rights-clean aggregates).
2. `data/difficulty_ordering/stats.json` + the three TSVs (or a single compact join).
3. Methodichka corpus-layer **manifest pointers** (paths + titles + visa status), not full textbook OCR.
4. Hop status block (above) so consumers stop treating Hops A–C as “planned”.

**Must not include:** in-copyright Kochergina full text, rights-gated RU bulk gloss layers, private review HTML.

### 3.3 `--check` contract

- Exit 0 iff: manifest parses, `schema_version` matches the script’s supported major, every `feeds[].path` exists, every `sha256` matches.
- Exit non-zero on drift (CI-blocking).
- Systema smoke pins `min_schema_version` major (default `1`).

## 4. Methodichka residual pipeline (H-A)

```text
review/*metodichka*_decisions.json
        │
        ▼
 residual OPEN notes (audit against revision-history / prior apply PRs)
        │
        ├── APPLIED  → prose edit + revision row (sheet_id#item_id)
        ├── DEFERRED → reason + optional probe stub
        └── null/reject re-vote → new review-sheet (zan-29, WF004-03/04/07 class)
```

WF004 taddhita notes are **in scope only when they affect methodichka/pedagogy companions or are explicit re-vote cards** (ruling 9). Pure Sangram-article register work stays on the Sangram editorial track unless the note is the listed re-vote class.

## 5. Smoke architecture (H-C)

| Piece | Rule |
|---|---|
| Environment | Local or staging only |
| Feature flags | Do **not** set production `features.rq4_study=true` unattended |
| Input | H-B `data/pedagogy_export/` (from merged SG main or a pinned commit path) |
| Success | ≥1 study/demo item loads and renders without error |
| Output | Command log + checklist tick in VERIFICATION / RESULTS_LOG |

Prefer reusing existing Systema paths: vendored `rq4_item_bank.json` reload, or Hop B/C demo loaders — **whichever is the cheapest proven path**. Default if multiple: **RQ4 item bank reload** (already the study contract).

## 6. Shared-gate thin lane (≤20%)

Only if H-A or H-B is blocked by a red shared gate:

- `npm run claims` / claims consistency
- `npm run errata` / errata.yml hygiene
- pytest suite breakage introduced by the adapter

**Not** freeze-ledger disposition or M03 packaging.

## 7. Rights & publish-safety

- Adapter default = public-safe aggregates.
- Any candidate feed that is rights-grey is **omitted** and logged (soft-fail), not published.
- Site Pages / visibility changes require `/publish-safety-check` (absolute fence if NO-GO).

---

_Dr. Mārcis Gasūns_
