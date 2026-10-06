# ṇatva/śaṭva rule-vs-fact coverage audit (H6054)

_Created: 06-10-2026 · Author: Gasūns (GLM 5.3 (opencode/zai-coding-plan/glm-5.3)) · Handoff: [H6054](https://github.com/gasyoun/Uprava/blob/main/handoffs/H6054-GLM_SanskritGrammar_natva-shatva-rule-audit_04.10.26.md) (Epic E024)_

Compares the Paninian **ṇatva/śaṭva** rules as materialised by kosha's H185
"hybrid-natva-fix" layer (vidyut-prakriya derivations; MG-ruled HYBRIDIZE
05-07-2026) against the **facts** shipped by MWinflect + csl-inflect
(`cologne_mwinflect` rows in kosha.db, ingested verbatim from
`MWinflect/nominals/pysanskritv2/tables/calc_tables.txt` — the exact file
csl-inflect's own `sqlite/lgtab1`/`lgtab2` builders consume).

**Audit universe = the H185 characterization draft: the E1 top-10k frequency
sample — 326 cells / 89 stem-paradigms / 55 lemmas.** Reproduced exactly
(`natva_cells: 326`, `natva_stems_paradigms: 89`), see `summary.json`.

## The rule × engine coverage matrix

| Rule (retroflexion) | Pāṇini | vidyut (rule side, H185 fix) | MWinflect + csl-inflect (facts) | Verdict |
|---|---|---|---|---|
| **śaṭva** — s→ṣ after i/u/ṛ/k etc. | 8.3.59 ff. | applies | **applies** — verified: the loc.pl cell of **89/89** affected paradigms in the shipped tables carries ṣ (`-eṣu`/`-iṣu`/`-uṣu`, e.g. `nfpezu`, `praBuzu`, `SatruGnezu`) | 🟰 **both engines cover** — no divergence |
| **ṇatva, intra-pada** — n→ṇ after r/ṛ/ṝ within one pada | 8.4.1–2 (+ ṛ-vārttika `ṛvarṇāc ca`) | applies | applies wherever the trigger sits in the key2 **final member** (e.g. `jYAti-praBuka` → `jYAtipraBukeRa` has the ṇ) | 🟰 covered — divergence only where the trigger sits outside the final member |
| **ṇatva across compound, monosyllabic final member** | 8.4.12 antaraṅga (per [MWinflect#6](https://github.com/sanskrit-lexicon/MWinflect/issues/6), drdhaval2785) | applies | **misses** — emits `-ena`/`-ānām`/`-āni` without ṇ | 🔴 **divergence class A** — 121/326 cells |
| **ṇatva across key2 hyphen, polysyllabic final member** (upasarga splits `pra-Bu`, `nir-Baya`; kṛt-suffixed finals `cakravAka`, `-in`/`-an` compounds `antaryAmin`) | scholarly fork: single-pada analysis of kṛt/upasarga formations vs strict final-pada | applies (single-pada reading) | **misses** — the with-pada algorithm suppresses ṇ | ⚖️ **divergence class B** — 205/326 cells |

## The 326 divergent cells (rule side vs shipped facts)

- Per-cell matrix: [`natva_cells_matrix.tsv`](natva_cells_matrix.tsv) — one row
  per cell: rule form (vidyut), fact form (MWinflect/csl-inflect), rule class,
  hyphenated key2 stem, features, 818-list membership, śaṭva evidence, DCS
  attestation counts.
- Per-paradigm śaṭva check: [`shatva_coverage_check.tsv`](shatva_coverage_check.tsv) — **89/89 `yes`**.

### Independent verification (re-done in this audit, not copied)

| Check | Result |
|---|---|
| E1 sample reproduction (entries-joined, rank_all-ordered top-10k) | 9,994 paradigms (whole-lemma batch boundary; ≤1-lemma wobble) → natva intersection **89 paradigms / 326 cells = exact H185 draft count** |
| `is_natva_diff` property re-verified per cell (mapping ṇ→n makes form sets equal) | **326/326 ok** — every divergent cell differs *only* at n↔ṇ; śaṭva (ṣ) and all other characters identical |
| Shipped-table spot-proof: every fact form present in the raw `calc_tables.txt` line (sha256 `98185b17…` = kosha DB `build_source_lock` pin) | **326/326 ok** |
| DCS-corpus attestation (kosha `forms` table, `dcs_form2lemma.tsv`): ṇ-form rows vs n-form rows per cell | **ṇ-only 166 · both 51 · n-only 23 · neither 86** — corpus weight 217:74 favours the retroflexed forms, with honest unattested residue |

### Divergence taxonomy

**Class A — compound with monosyllabic final member (121 cells / 27 of the 89
paradigms, 15 distinct key2 stems).** `nf-pa`→`nfpeRa/nfpARAm`, `tura-ga`,
`ura-ga`, `Satru-Gna`, `pra-Bu`… The documented [MWinflect#6](https://github.com/sanskrit-lexicon/MWinflect/issues/6)
class: drdhaval2785's regex over the 818-stem `diff_nopada_m_a.txt` diff list
yielded 69 such m_a stems; **57 of the 89 paradigms (36 distinct key2 stems)
appear in that 818 list** — 13 of them in this class A, 44 also in class B.
MWinflect's with-pada algorithm (decline the key2 final pada, then re-attach
the head) suppresses the retroflexion that Pāṇini 8.4.12 mandates for laghu
final members. Corpus backs the ṇ-forms here (e.g. `nfpeRa` attested,
`nfpena` not).

**Class B — key2 hyphen splits where the final member is polysyllabic
(205 cells / 62 of the 89 paradigms).** Three sub-motivations surface in the data:
1. *upasarga splits on single-pada stems* — `pra-Bu` (m_u/f_u/n_u), `nir-Baya`:
   the key2 hyphen treats the preverb as a compound member, but the nominal is
   one pada for 8.4.1–2 purposes;
2. *kṛt-suffixed finals* — `cakravAka` (`cakravAkeRa` attested in DCS,
   `cakravAkena` not), `cakravARTi`-type;
3. *secondary-suffix compounds* — `-in`/`-an` stems (`antaryAmin`,
   `cakriNavant`-type): the n belongs to the suffix that extends the pada over
   the whole compound.

Whether class B *should* retroflex is a genuine scholarly fork (Whitney's
formulation vs the strict final-pada reading); vidyut applies the single-pada
analysis, MWinflect the final-pada one. The corpus column in the TSV lets a
reader adjudicate per cell.

### Why śaṭva never diverges here

The ṣ-retroflexion triggers (i/u/ṛ/k…) sit in the **endings** or the final
member itself (`-eṣu`, `-uṣu`), so MWinflect's final-pada scope applies them
correctly; the ṇ-triggers of classes A/B sit **before** the key2 hyphen, where
the final-pada scope cannot see them. Same paradigms, opposite outcomes —
`nfpezu` (śaṭva ✓) beside `nfpena` (ṇatva ✗) in one line of the shipped table.

## Files

| File | Content |
|---|---|
| [`natva_cells_matrix.tsv`](natva_cells_matrix.tsv) | 326-row per-cell matrix |
| [`shatva_coverage_check.tsv`](shatva_coverage_check.tsv) | 89-row per-paradigm śaṭva check |
| [`summary.json`](summary.json) | machine rollup |
| [`inputs/diff_nopada_m_a.txt`](inputs/diff_nopada_m_a.txt) | the MWinflect#6 818-stem diff list, recovered from MWinflect git `2c512cc` (removed upstream in `9bc0ed3`, 18-11-2019) |
| [`DRAFT_csl_inflect_issue10_post.md`](DRAFT_csl_inflect_issue10_post.md) | draft give-back comment for [csl-inflect#10](https://github.com/sanskrit-lexicon/csl-inflect/issues/10) — **MG posts it; diplomacy-gated (kosha RELATIONS.md §2/§7)** |

Reproduce: `python3 scripts/build_natva_shatva_audit.py` (~40 s; read-only;
needs kosha.db + MWinflect clone at the default paths). Full-universe context:
the shipped kosha DB carries 14,199 `hybrid-natva-fix` rows / 2,157 lemmas
(full entry-bearing pass) — this audit deliberately stays at the H185 draft's
top-10k characterization scope.
