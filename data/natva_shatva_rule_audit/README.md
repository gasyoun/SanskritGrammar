# natva_shatva_rule_audit — ṇatva/śaṭva rule-vs-fact coverage audit (H6054)

_Created: 06-10-2026 · Author: Gasūns (GLM 5.3 (opencode/zai-coding-plan/glm-5.3))_

Compares the H185-draft ṇatva/śaṭva rules (89 stems / 326 cells, E1 top-10k
sample, vidyut-side) against the MWinflect + csl-inflect shipped facts.
Full analysis: [`coverage_matrix.md`](coverage_matrix.md).

| File | Content |
|---|---|
| `natva_cells_matrix.tsv` | 326-row per-cell matrix (rule form, fact form, rule class, key2 stem, 818-list membership, śaṭva evidence, DCS attestation) |
| `shatva_coverage_check.tsv` | 89-row per-paradigm śaṭva (s→ṣ) check — 89/89 applied |
| `summary.json` | machine rollup incl. verification counters |
| `inputs/diff_nopada_m_a.txt` | MWinflect#6 818-stem with/without-pada diff list — recovered from MWinflect git `2c512cc` (deleted upstream in `9bc0ed3`, 18-11-2019). **License: CC BY-SA 4.0 (MWinflect), inherited by this copy** |
| `DRAFT_csl_inflect_issue10_post.md` | draft give-back comment — **not posted; MG posts (diplomacy gate, kosha RELATIONS.md §2/§7)** |

Reproduce: `python3 scripts/build_natva_shatva_audit.py` (read-only; needs
kosha.db and the MWinflect clone at default paths; verifies the
calc_tables.txt sha256 against kosha's `build_source_lock` pin).

Sources (read-only, sha-pinned where noted): kosha `data/db/kosha.db`
(`hybrid-natva-fix` + `cologne_mwinflect` rows, `lemmas.rank_all`,
`entries`, `forms` = DCS form→lemma); MWinflect
`nominals/pysanskritv2/tables/calc_tables.txt` (sha256 `98185b17…`);
MWinflect git history `2c512cc` (818 list); MWinflect#6 thread.
