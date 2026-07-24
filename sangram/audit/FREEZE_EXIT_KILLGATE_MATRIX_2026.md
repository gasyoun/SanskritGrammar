# Freeze-exit kill-gate matrix — 15 `disposition=unknown` baseline candidates

_Created: 24-07-2026 · Last updated: 24-07-2026_

**Handoff:** [H1611](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1611-Sonnet_SanskritGrammar_freeze-15-killgate-matrix_24.07.26.md) (W1-A0).
**Plan:** [`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md).
**Ledger source:** [`sangram/editorial/data/consolidation_ledger.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/data/consolidation_ledger.json) — filter `disposition == "unknown"` (15/15 rows below; ledger refresh date 2026-07-22).
**Provenance:** assembled 24-07-2026 by Grok 4.5 (`grok-4.5`) executing H1611 under user-launched override of the intended Sonnet 5 (`claude-sonnet-5`) executor. **No probe code was run in this handoff; zero probe JSON written.**

## How to read this matrix

| Column | Meaning |
|---|---|
| `toc_ref` / `art_id` | C2 baseline id + article id from the ledger |
| Programme · slot | C5 morphology or C6 semantics/syntax programme + registered C6 slot id(s) from [`sangram/toc/data/articles.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/toc/data/articles.json) where present |
| Kill-gate criterion (quoted) | **Only** pilot kill-gates named in C5 § 7 or C6 § 7. If the C2 slot is not one of the five pilots, this cell is **`MISSING`** — do not invent a numeric threshold |
| Script path | Existing `scripts/sg_*` (or `sangram/audit/probe_*`) instrument; **`MISSING`** if none |
| Acceptance predicate | What H1612 (SE) / H1613 (MO·WF) must treat as pass/fail/park |
| Escalate path | Required whenever criterion is `MISSING` (roadmap acceptance for A0) |

**Programme text sources (do not invent thresholds):**

- C5 pilots § 7: [`sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx)
- C6 pilots § 7: [`sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx)

**Census of this matrix**

| Bucket | Count | toc_refs |
|---|---|---|
| Named pilot kill-gate quoted | **1** | SG-SE-006 (= C6 § 7 P2 `sem-b-past-competition`) |
| Criterion `MISSING` (no pilot gate for this C2 slot) | **14** | the rest |
| Script present | **15** | all fifteen have a committed `scripts/sg_*` instrument |
| Script `MISSING` | **0** | — |

**Identity caution (do not conflate slots):** C6 pilot P1 kill-gate is registered on C2 **`SG-SY-005`** (`syn-c-locative-absolute`), **not** on `SG-SE-005` (`sem-a-locative`). SE-005’s article covers the locative absolute as a headline, but the pilot kill-gate text is not owned by that C2 id. None of the C5 pilots (SG-MO-002 / MO-013 / MO-017 / WF-008 / WF-003) appear in this unknown set — they are already off the freeze baseline as published or otherwise terminal.

---

## SE cluster (H1612 scope) — 9 rows

### SG-SE-001 · `art:case-system-overview`

| Field | Value |
|---|---|
| Programme · slot | C6 · `sem-a-case-overview` (SEM-A) |
| Kill-gate criterion (quoted) | **MISSING** — C6 § 7 names no pilot for `sem-a-case-overview` (case overview is a non-pilot ① slot) |
| Script path | [`scripts/sg_se_001_case_overview.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_se_001_case_overview.py) |
| Acceptance predicate | Cannot fire a programme kill-gate. H1612 must **park-and-skip**: leave `disposition=unknown`, set `blocking_note` pointing at this row |
| Escalate path | Human `@DECIDE`: mint a per-slot freeze gate, or route to SE multi-article visa without kill-gate (survivors path). Nearest method rule only (not a kill-gate): C6 E5 (no CI → no quantitative claim) |

### SG-SE-002 · `art:nominative-accusative`

| Field | Value |
|---|---|
| Programme · slot | C6 · case sub-article under SEM-A (no dedicated `c6_slots` row in registry; sibling of SE-001) |
| Kill-gate criterion (quoted) | **MISSING** — not a C6 § 7 pilot |
| Script path | [`scripts/sg_se_002_nom_acc.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_se_002_nom_acc.py) |
| Acceptance predicate | Park-and-skip as above; script is a re-derive instrument, not a kill-gate |
| Escalate path | Same as SE-001. Context only: adversarial verify already tightened double-accusative (article-local honesty; not a programme threshold) |

### SG-SE-003 · `art:instrumental-dative`

| Field | Value |
|---|---|
| Programme · slot | C6 · `sem-a-instrumental` + `sem-a-dative-experiencer` |
| Kill-gate criterion (quoted) | **MISSING** — neither slot is a C6 § 7 pilot |
| Script path | [`scripts/sg_se_003_instrumental_dative.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_se_003_instrumental_dative.py) |
| Acceptance predicate | Park-and-skip |
| Escalate path | Same as SE-001 |

### SG-SE-004 · `art:ablative-genitive`

| Field | Value |
|---|---|
| Programme · slot | C6 · `sem-a-genitive` (article also covers ablative + genitive absolute) |
| Kill-gate criterion (quoted) | **MISSING** — `sem-a-genitive` is not a C6 § 7 pilot. Do **not** apply C6 P1 (`syn-c-locative-absolute`) to genitive absolute: that pilot is owned by **SG-SY-005** |
| Script path | [`scripts/sg_se_004_abl_gen.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_se_004_abl_gen.py) |
| Acceptance predicate | Park-and-skip |
| Escalate path | Same as SE-001; optional later mint of a gen-absolute construction gate under SYN-C if SY-005 is ever produced |

### SG-SE-005 · `art:locative`

| Field | Value |
|---|---|
| Programme · slot | C6 · `sem-a-locative` (headline: locative absolute) |
| Kill-gate criterion (quoted) | **MISSING** for this C2 id. Nearest **named** pilot text lives on a **different** slot — C6 § 7 P1 `syn-c-locative-absolute` (= C2 **SG-SY-005**), quoted here for reference only and **not** claimed as SE-005’s gate: «Точность retrieval <80% на ручной выборке 100 кандидатов → пилот останавливается, разрыв A1 эскалируется» |
| Script path | [`scripts/sg_se_005_locative.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_se_005_locative.py) |
| Acceptance predicate | Park-and-skip for SE-005 freeze disposition. Do not silently re-host the P1 threshold onto `sem-a-locative` |
| Escalate path | `@DECIDE`: (a) mint a sem-a-locative freeze gate, or (b) treat SE-005 as visa-only survivor, or (c) defer absolute-construction kill-gate to SG-SY-005 production |

### SG-SE-006 · `art:past-tenses`

| Field | Value |
|---|---|
| Programme · slot | C6 · `sem-b-past-competition` — **this is C6 pilot P2** |
| Kill-gate criterion (quoted) | C6 § 7 P2 (W3): «Родные теги различают три претерита в <95% выборки → количественная часть снимается, статья публикует честный отрицательный результат» |
| Script path | [`scripts/sg_se_006_past_tenses.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_se_006_past_tenses.py) |
| Acceptance predicate | **Runnable kill-gate.** H1612 must implement/re-run against a 100-or-documented sample and the native-tag distinction of imperfect / aorist / perfect. Fail criterion → `disposition=kill_gated` + `source_links` to probe artifact. Survive → leave `unknown`, clear `blocking_note`, list as SE survivor for H1614. Ambiguity on whether the sample meets 95% → hard-stop `@DECIDE` (do not flip disposition) |
| Escalate path | None for criterion (named). Probe instrument reuse: `sg_se_006_past_tenses.py` + new `sangram/audit/probe_freeze_past-tenses.{py,json,md}` per Implementation A1 |

### SG-SE-008 · `art:imperative-optative`

| Field | Value |
|---|---|
| Programme · slot | C6 · `sem-b-optative` + `sem-b-imperative` |
| Kill-gate criterion (quoted) | **MISSING** — neither mood slot is a C6 § 7 pilot |
| Script path | [`scripts/sg_se_008_imperative_optative.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_se_008_imperative_optative.py) |
| Acceptance predicate | Park-and-skip |
| Escalate path | Same as SE-001 |

### SG-SE-013 · `art:karaka-case`

| Field | Value |
|---|---|
| Programme · slot | C6 · `sem-a-karaka-vs-case` |
| Kill-gate criterion (quoted) | **MISSING** — not a C6 § 7 pilot |
| Script path | [`scripts/sg_se_013_karaka_case.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_se_013_karaka_case.py) |
| Acceptance predicate | Park-and-skip. Context only (not a threshold): article honesty already states deprel overlay coverage ≈3.93% and no native kāraka layer |
| Escalate path | Same as SE-001 |

---

## MO / WF stragglers (H1613 scope) — 6 rows

### SG-MO-019 · `art:aorist-types`

| Field | Value |
|---|---|
| Programme · slot | C5 · cluster «Перфект, аорист, будущее» (beyond-quota partition of SG-MO-018) |
| Kill-gate criterion (quoted) | **MISSING** — C5 § 7 pilots are only MO-002 / MO-013 / MO-017 / WF-008 / WF-003. Nearest related pilot text is C5 P3 (SG-MO-017 perfect), which does **not** transfer: «Форма-класс отделяет перфект от аориста/имперфекта в <95% выборки → количественная часть снимается…» — that gate is owned by the perfect pilot, not by aorist-types |
| Script path | [`scripts/sg_mo_019_aorist_types.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_019_aorist_types.py) |
| Acceptance predicate | Park-and-skip |
| Escalate path | Human `@DECIDE` for a per-slot MO-019 gate, or visa-only path. Context only: C5 EM2 (preterites by form-class, never sole UD `Tense=Past`) |

### SG-MO-022 · `art:present-perfect-participles`

| Field | Value |
|---|---|
| Programme · slot | C5 · cluster «Именные формы глагола» |
| Kill-gate criterion (quoted) | **MISSING** — not a C5 § 7 pilot |
| Script path | [`scripts/sg_mo_022_participles.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_022_participles.py) |
| Acceptance predicate | Park-and-skip |
| Escalate path | Same as MO-019. Context only: C5 EM2-adjacent perfect-participle bucketing |

### SG-MO-024 · `art:gerundive`

| Field | Value |
|---|---|
| Programme · slot | C5 · cluster «Именные формы глагола»; C6 also lists construction slot `syn-c-gerundive` (not mapped on this C2 id) |
| Kill-gate criterion (quoted) | **MISSING** — not a C5/C6 pilot |
| Script path | [`scripts/sg_mo_024_gerundive.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_024_gerundive.py) |
| Acceptance predicate | Park-and-skip |
| Escalate path | Same as MO-019 |

### SG-MO-025 · `art:infinitive`

| Field | Value |
|---|---|
| Programme · slot | C5 · cluster «Именные формы глагола» |
| Kill-gate criterion (quoted) | **MISSING** — not a C5 § 7 pilot |
| Script path | [`scripts/sg_mo_025_infinitive.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_mo_025_infinitive.py) |
| Acceptance predicate | Park-and-skip |
| Escalate path | Same as MO-019 |

### SG-WF-002 · `art:krt-overview`

| Field | Value |
|---|---|
| Programme · slot | C5 · cluster «Деривация» (overview; script self-labels «no kill-gate») |
| Kill-gate criterion (quoted) | **MISSING** — overview, not pilot. Related pilot C5 § 7 P5 (SG-WF-003 kṛt-suffixes) already fired on the surface-suffix instrument and is a **different** published article: «Словарная валидация отбрасывает >20% поверхностно-совпавших кандидатов → запрос переработан до утверждения». Do **not** re-fire P5 against the WF-002 overview spine (native VerbForm ∈ {Part,Conv,Gdv,Inf}) |
| Script path | [`scripts/sg_wf_002_krt_overview.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_002_krt_overview.py) |
| Acceptance predicate | Park-and-skip |
| Escalate path | Visa-only or `@DECIDE` for an overview-specific freeze rule. Context only: C5 EM5 |

### SG-WF-009 · `art:bahuvrihi`

| Field | Value |
|---|---|
| Programme · slot | C5 · cluster «Композиты»; C6-blocked exocentricity (article publishes the **limit**, not a census) |
| Kill-gate criterion (quoted) | **MISSING** as a numeric pilot gate for this slot. Related C5 § 7 P4 (SG-WF-008 tatpuruṣa) is a different article: «Межразметочное согласие двух независимых проходов классификации <0.7 (Cohen κ) → таксономия типов пересматривается до публикации». Related method rule (not a fireable threshold) C5 EM4: «Тип классифицируется вручную на выборке по циклу C3; … автоматический подсчёт по типам не публикуется без ручной валидации» |
| Script path | [`scripts/sg_wf_009_bahuvrihi.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_009_bahuvrihi.py) |
| Acceptance predicate | Park-and-skip for inventing a κ threshold on bahuvrīhi. Honest-limit articles that already refuse a census are **not** automatic `kill_gated` — that disposition needs an explicit cited criterion or a human ruling |
| Escalate path | `@DECIDE`: keep as limit-candidate → visa sheet, or rule `kill_gated` only if a human adopts a written freeze criterion |

### SG-WF-011 · `art:preverbs`

| Field | Value |
|---|---|
| Programme · slot | C5 · cluster «Композиты» / preverb system (beyond-quota native positive) |
| Kill-gate criterion (quoted) | **MISSING** — not a C5 § 7 pilot |
| Script path | [`scripts/sg_wf_011_preverbs.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/sg_wf_011_preverbs.py) |
| Acceptance predicate | Park-and-skip |
| Escalate path | Same as MO-019 |

---

## Compact table (15/15)

| # | toc_ref | art_id | Programme slot | Kill-gate criterion | Script | Accept / escalate |
|---|---|---|---|---|---|---|
| 1 | SG-SE-001 | art:case-system-overview | C6 `sem-a-case-overview` | **MISSING** | `scripts/sg_se_001_case_overview.py` | park → `@DECIDE` / visa path |
| 2 | SG-SE-002 | art:nominative-accusative | C6 SEM-A sub | **MISSING** | `scripts/sg_se_002_nom_acc.py` | park → `@DECIDE` / visa path |
| 3 | SG-SE-003 | art:instrumental-dative | C6 `sem-a-instrumental` + `sem-a-dative-experiencer` | **MISSING** | `scripts/sg_se_003_instrumental_dative.py` | park → `@DECIDE` / visa path |
| 4 | SG-SE-004 | art:ablative-genitive | C6 `sem-a-genitive` | **MISSING** (do not use SY-005 P1) | `scripts/sg_se_004_abl_gen.py` | park → `@DECIDE` / visa path |
| 5 | SG-SE-005 | art:locative | C6 `sem-a-locative` | **MISSING** (P1 owns SG-SY-005) | `scripts/sg_se_005_locative.py` | park → `@DECIDE` / visa path |
| 6 | SG-SE-006 | art:past-tenses | C6 `sem-b-past-competition` **P2** | Quoted C6 § 7 P2: native tags distinguish 3 preterites in **<95%** of sample → strip quantitative part / publish honest negative | `scripts/sg_se_006_past_tenses.py` | **run** probe; fail→`kill_gated`; survive→SE visa list |
| 7 | SG-SE-008 | art:imperative-optative | C6 `sem-b-optative` + `sem-b-imperative` | **MISSING** | `scripts/sg_se_008_imperative_optative.py` | park → `@DECIDE` / visa path |
| 8 | SG-SE-013 | art:karaka-case | C6 `sem-a-karaka-vs-case` | **MISSING** | `scripts/sg_se_013_karaka_case.py` | park → `@DECIDE` / visa path |
| 9 | SG-MO-019 | art:aorist-types | C5 preterite cluster | **MISSING** (do not transfer P3) | `scripts/sg_mo_019_aorist_types.py` | park → `@DECIDE` / visa path |
| 10 | SG-MO-022 | art:present-perfect-participles | C5 nominal verb forms | **MISSING** | `scripts/sg_mo_022_participles.py` | park → `@DECIDE` / visa path |
| 11 | SG-MO-024 | art:gerundive | C5 nominal verb forms | **MISSING** | `scripts/sg_mo_024_gerundive.py` | park → `@DECIDE` / visa path |
| 12 | SG-MO-025 | art:infinitive | C5 nominal verb forms | **MISSING** | `scripts/sg_mo_025_infinitive.py` | park → `@DECIDE` / visa path |
| 13 | SG-WF-002 | art:krt-overview | C5 derivation overview | **MISSING** (do not re-fire P5) | `scripts/sg_wf_002_krt_overview.py` | park → `@DECIDE` / visa path |
| 14 | SG-WF-009 | art:bahuvrihi | C5 compounds (limit article) | **MISSING** (do not transfer P4 κ) | `scripts/sg_wf_009_bahuvrihi.py` | park → `@DECIDE` / visa path |
| 15 | SG-WF-011 | art:preverbs | C5 preverb system | **MISSING** | `scripts/sg_wf_011_preverbs.py` | park → `@DECIDE` / visa path |

---

## Implications for H1612 / H1613 / H1614

1. **H1612 (SE cluster):** Only **SG-SE-006** has a fireable C6 pilot kill-gate. The other **8** SE unknowns must be parked with `blocking_note` → this matrix, **or** a human must rule a non-invented path (visa-only survivors, or newly written gates). Do not treat re-derive success of `sg_se_*` as a kill-gate pass — the plan forbids a uniform re-derive substitute for programme gates.
2. **H1613 (MO/WF):** All **6** stragglers are criterion-`MISSING`. Prefer park-and-skip over inventing FP-rate / κ / form-class thresholds borrowed from sibling pilots.
3. **H1614 (SE survivor visa sheet):** Survivors can only be listed after H1612. With the current programme text, the only mechanical kill/survive outcome is SE-006; other SE cards enter a visa sheet only after human gate-minting or an explicit “no kill-gate → visa” ruling.
4. **Fence retained:** no `freeze.active` flip; no M03 prose; no RQ4 protocol change; no invented thresholds.

## Non-goals (this file)

- Did not run any probe or write `sangram/audit/probe_freeze_*`.
- Did not edit the consolidation ledger.
- Did not invent kill-gate numbers for the 14 non-pilot slots.

_Dr. Mārcis Gasūns_
