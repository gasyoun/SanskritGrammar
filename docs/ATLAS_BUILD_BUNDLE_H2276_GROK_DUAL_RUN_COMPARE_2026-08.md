# H2276 dual-run compare — atlas_build_bundle e2e coverage (H2271 residual)

_Created: 06-08-2026 · Last updated: 06-08-2026_

**Provenance:** Grok 4.5 (`grok-4.5`) — dual-run residual of
[H2271](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H2271-Grok_SanskritGrammar_h1839-residual-validator-test-coverage-6-uncovered-scripts_04.08.26.md)
after Sonnet 5 (`claude-sonnet-5`) executed it under an explicit human
"run anyway" override (standing dual-run protocol, 01-08-2026). Source
override PR: [SanskritGrammar#585](https://github.com/gasyoun/SanskritGrammar/pull/585)
(squash-merged `918e54a`, release `v0.118.1`).

## Independent re-derivation (not rubber-stamp of #585)

### 1. What was the real residual of H1839?

Re-read [PR #578](https://github.com/gasyoun/SanskritGrammar/pull/578) body
and the live `tests/` tree without treating #585 as ground truth:

| Claimed "uncovered" script (H2271 mint slug) | Actual pre-H2271 coverage |
|---|---|
| `check_claims_consistency` | covered (`tests/test_claims_consistency.py`) |
| `check_denominator_commensurability` | covered |
| `article_validate` | covered |
| `build_corpus_layer` | covered |
| `build_visa_sheet` | covered |
| `consolidation_ledger_refresh` | covered |

PR #578 itself names the residual as **depth**, not missing files:
`atlas_build_bundle` full e2e rebuild needs the private Uprava hub — pure
helpers only in CI. **Verdict:** the H2271 mint premise ("6 uncovered
scripts") was already stale; Sonnet correctly re-scoped to the e2e gap.

### 2. Independent live rebuild (this session)

From worktree `SanskritGrammar-h2276-29140` against sibling
`../Uprava` (MEGABOOK.md + interlinks_edges.tsv present):

```text
python scripts/atlas_build_bundle.py --uprava ../Uprava --out <tmp>/atlas.bundle.json \
  --generated-by H2276-independent --date 2026-08-06
# build rc: 0 ; bundle size: 179725 bytes

python scripts/atlas_validate_bundle.py <tmp>/atlas.bundle.json
# VALID: 149 nodes, 285 edges, 5 views; leakage=0
```

`python -m pytest tests/test_atlas_build_bundle_e2e.py tests/test_atlas_build_bundle.py -q`
→ **12 passed** (4 e2e + 8 pure-helper) before the H2276 net-new tests below.

### 3. Independent checks of the two shipped drift fixes

**Fix A — `ext:sanskrit-lexicon-scans` in EXTERNAL_STACKS / EXT_NAME_MAP**

- Live `interlinks_edges.tsv` unique `ext:` names:
  `DharmaMitra, GRETIL, Heritage, Nagari, Samsaadhanii, VedaWeb,
  samskrtam.ru, sanskrit-lexicon-scans, vidyut` (9).
- `EXT_NAME_MAP` keys: **exact set match**, zero missing / zero extra.
- `sanskrit-lexicon-scans` edges present (H1706, 27-07-2026 + later
  ramayana-edition-alignment row). Without the map entry a real rebuild
  hard-`SystemExit`s — confirmed by reading the edge-resolution path at
  `EXT_NAME_MAP.get(name[4:])` in `scripts/atlas_build_bundle.py`.

**Fix B — `parse_anchors` markdown-linked § refs**

- Live MEGABOOK §9 table cells: **26 linked** (`§N.M`), **0 bare**,
  **0 other** forms.
- `parse_anchors` on live MEGABOOK: 83 triples, 16 unique section tokens, all
  matching `^[\d.]+$` (no `[`/`]`/`#` residue).
- The `_bare_section` helper correctly strips both `§N.M` and bare `§N.M`.

## Comparison class (dual-run-salvage scheme)

| Dimension | Class | Rationale |
|---|---|---|
| Scope re-derivation (stale "6 scripts" → e2e depth) | **identical** | Same conclusion as #585 from PR #578 + live tests tree |
| E2e test shape (real rebuild + validate; skipif no hub) | **equivalent** | Independently would write the same contract; no better skip message or extra e2e case found |
| Drift fix A (sanskrit-lexicon-scans) | **identical** | Required by live TSV; map now complete |
| Drift fix B (markdown § links) | **identical** | Required by live MEGABOOK (100% linked cells) |
| Pure-helper regression pins for A+B | **net-new** | #585 left both bugs guarded only by e2e (skipped in CI). H2276 adds three CI-runnable unit tests so a future map/parser regression fails without private Uprava |
| Third drift bug on live data | **none** | Independent rebuild VALID; TSV↔map parity complete; parse_anchors clean |

**Overall adjudication:** keep **all of PR #585** (equivalent / identical).
**Add** the pure-helper regression tests (net-new) so CI, not only a local
hub checkout, pins the two fixes. No conflicting cells; no revert of #585.

## Net-new landed this dual-run

In `tests/test_atlas_build_bundle.py`:

1. `test_parse_anchors_accepts_markdown_linked_section_refs` — synthetic §9
   fixture with linked + bare cells; asserts bare section tokens only.
2. `test_ext_name_map_covers_every_external_stack` — EXTERNAL_STACKS ↔
   EXT_NAME_MAP bidirectional parity.
3. `test_external_stacks_includes_sanskrit_lexicon_scans` — specific H1706
   host pin.

## Explicit non-findings

- No third live-data drift bug on 06-08-2026 Uprava.
- No change needed to e2e skip reason text (already states MEGABOOK +
  interlinks requirement).
- `consolidation_ledger.json` refresh in #585 was correctly out of scope for
  dual-run re-adjudication (pre-existing CI blocker, not atlas logic).

## Evidence checklist

- [x] Independent pytest e2e against live Uprava (12 passed pre-net-new; then
      pure-helper suite green with the three new tests)
- [x] Written classification above (identical / equivalent / net-new; zero
      conflicting)
- [x] Follow-up PR for net-new pure-helper pins (this dual-run's code delta)
- [ ] Handoff closed via `handoff_close.py H2276 --pr <url>`

_Dr. Mārcis Gasūns_
