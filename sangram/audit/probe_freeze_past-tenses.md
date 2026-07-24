# Freeze probe — SG-SE-006 (`art:past-tenses`)

_Created: 24-07-2026 · Last updated: 24-07-2026_

**Handoff:** H1612 · **Model:** Grok 4.5 (grok-4.5)

## Criterion

- **Status:** `QUOTED`
- **C6 slot:** sem-b-past-competition
- **Pilot:** P2
- **Quoted (C6 § 7):** Родные теги различают три претерита в <95% выборки → количественная часть снимается, статья публикует честный отрицательный результат
- **Source / note:** sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx § 7 row P2 (sem-b-past-competition)

## Integrity re-derive (pin 04e0778)

- **all_match:** `True`
- **kind:** SE-006 past-tense census

## Outcome

- **outcome:** `kill_gated`
- **ledger disposition:** `kill_gated`

## Kill-gate measurement (P2)

- universe (Impf+Past): **148750**
- natively assigned: **62795**
- unassigned Past+None: **85955**
- share: **42.22%** (threshold 95%)
- **gate_fires:** `True`
- rationale: Native tags do not distinguish the three classical preterites on ≥95% of the finite past universe (simple perfect lives in untagged Past+None). Clear P2 fail → disposition kill_gated without human visa (freeze-exit mechanism).

## Artifacts

- JSON: `sangram/audit/probe_freeze_past-tenses.json`
- runner: `sangram/audit/probe_freeze_past-tenses.py`
- article script: `scripts/sg_se_006_past_tenses.py`

_Dr. Mārcis Gasūns_
