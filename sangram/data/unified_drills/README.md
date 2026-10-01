# Wave 2 — unified auto-drill bank with verified answer keys (RQ2)

_Created: 25-09-2026 · Last updated: 25-09-2026_

Closes the open "Wave 2 — auto-drill generation with verified answer keys (RQ2)"
row in [`docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/ROADMAP_DIGITAL_SANSKRIT_PEDAGOGY_2026_2028.md).

Three drill-generation engines already existed with no shared schema and no
combined verification pass:

| Engine | Source | Verification signal already computed |
|---|---|---|
| declension (W2-add-a, H1296) | [`sangram/data/attested_drills/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/data/attested_drills) | `agreement` column — corpus-attested form matches/variants the generated form |
| samasa (W2-add-c, H1298) | [`sangram/data/samasa_ladder/`](https://github.com/gasyoun/SanskritGrammar/tree/main/sangram/data/samasa_ladder) | `rungs_json` step count vs `depth`/`members` |
| sandhi (H4486) | [`data/emeneo_sandhi/`](https://github.com/gasyoun/SanskritGrammar/tree/main/data/emeneo_sandhi) | pamphlet worked-example MCQ parity |

[`build_unified_drill_bank.py`](build_unified_drill_bank.py) reads all three
committed TSVs, re-derives a `verified` flag for every row from its own
already-computed signal (no network, no DCS database, no engine re-run) and
never fabricates or upgrades a key: a declension row with `agreement in
{mismatch, no_generation}`, or a samasa ladder whose `rungs_json` step count
disagrees with its own `depth`, is emitted as `verified=false` with the
reason in `verification_method`, not silently dropped.

## Files

| File | What |
|---|---|
| [`unified_drill_bank.tsv`](unified_drill_bank.tsv) | one row per drill item across all three engines, one schema |
| [`verification_summary.json`](verification_summary.json) | machine-readable per-type verified counts — `--check` fails if a re-run drifts from this |
| [`VERIFICATION_REPORT.md`](VERIFICATION_REPORT.md) | the same numbers, human-readable — **computed, never hand-edited** |

## `unified_drill_bank.tsv` schema

| Column | Meaning |
|---|---|
| `drill_id` | `<TYPE>-<source-key>`, unique |
| `drill_type` | `declension` \| `samasa` \| `sandhi` |
| `prompt` | the drill's question surface, engine-native |
| `answer_key` | the gold answer this drill's engine already computed |
| `verified` | `true`/`false` — see the engine's own signal above |
| `verification_method` | which check produced `verified`, and its raw value |
| `difficulty_band` | engine-native frequency/difficulty band |
| `source_dataset` | the upstream TSV this row was derived from |
| `source_row_id` | the upstream row's own key, for round-tripping to the source |

## RQ2 falsifiable claim

**91.7% (46,400 / 50,582) of drill items across all three engines carry a
verified answer key.** Refuted if this share drops on a re-run over
unchanged source data — that would mean a verification check regressed, not
that the underlying drills changed (they didn't; `--check` compares against
the committed `verification_summary.json`).

## Re-running

```sh
python sangram/data/unified_drills/build_unified_drill_bank.py          # rebuild
python sangram/data/unified_drills/build_unified_drill_bank.py --check  # verify only, exit 1 on drift
```

## Non-goals

This does **not** re-implement or replace any of the three engines — it is a
read-only aggregation + verification pass over their committed output. A
change to an engine's own logic still lands in that engine's own directory;
re-run this builder afterward to refresh the unified view.

---

_Dr. Mārcis Gasūns_
