# Architecture — freeze exit + methodichka residual

_Created: 24-07-2026 · Last updated: 24-07-2026_

Cover:
[`docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md).

## 1. Components

| Component | Role | Canonical home |
|---|---|---|
| Consolidation ledger | Machine freeze gate + per-baseline disposition | [`sangram/editorial/data/consolidation_ledger.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/editorial/data/consolidation_ledger.json) |
| Ledger refresh | Recompute evidence fields from review/ + DCS ledger | [`scripts/consolidation_ledger_refresh.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/consolidation_ledger_refresh.py) |
| Article validator | Freeze-aware validation | [`scripts/article_validate.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/article_validate.py) |
| Morphology programme (C5) | Kill-gates for MO/WF slots | [`sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_MORPHOLOGY_PROGRAM_W2.mdx) |
| Syntax/semantics programme (C6) | Kill-gates for SE slots | [`sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx`](https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx) |
| Probe artifacts | Durable evidence per toc_ref | `sangram/audit/probe_freeze_*` |
| Kill-gate matrix | toc_ref → criterion map | `sangram/audit/FREEZE_EXIT_KILLGATE_MATRIX_2026.md` |
| Visa sheet builder | Spec → HTML | [`scripts/build_visa_sheet.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/build_visa_sheet.py) |
| Editorial note index | Note OPEN/APPLIED tracking | [`review/EDITORIAL_NOTE_INDEX.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/review/EDITORIAL_NOTE_INDEX.tsv) |
| Methodichka manuscripts | Russian pedagogy companions | `KocherginaUchebnik_1998/`, `ApteSyntax_1885/` |

## 2. Data flow (freeze front)

```text
baseline_ids[disposition=unknown]
        │
        ▼
  FREEZE_EXIT_KILLGATE_MATRIX (A0)
        │
        ├─ SE cluster ──► per-article C6 probe ──► artifact + ledger
        │                      │
        │                      ├─ fail criterion ──► disposition=kill_gated
        │                      └─ survive ──► SE multi-visa sheet (A3) ──► human vote ──► apply
        │
        └─ MO/WF ──────► per-article C5 probe ──► same fork
```

**Invariant:** `freeze.active` flips false **only** when zero baseline rows remain `unknown`
(ledger `exit_criterion`). Agents never flip the flag as a convenience.

## 3. Disposition vocabulary (closed)

`published` · `revised` · `rejected` · `kill_gated` · `unknown`

Probe-first maps:

| Probe outcome | Ledger write |
|---|---|
| Clear kill-gate fail with cited criterion | `kill_gated` + `source_links` to probe |
| Clear survive | leave `unknown`; set `blocking_note` empty; list on survivor sheet |
| Instrument missing / criterion ambiguous | leave `unknown`; `blocking_note` = escalate text; park-and-skip |

## 4. Build-vs-reuse

| Need | Verdict |
|---|---|
| Ledger / freeze gate | **Reuse** H1260 |
| Visa HTML | **Reuse** `build_visa_sheet.py` + csl-pyutil |
| Kill-gate criteria | **Reuse** C5/C6 programme text; do not invent thresholds |
| Probe scripts | **Reuse** article-local + `sangram/audit/probe_*`; write new only when matrix marks `MISSING` |
| Note index | **Reuse** H1273 TSV; update rows, do not redesign schema |
| Methodichka apply | **Reuse** H1258/H1275 patterns + H1454 list |

## 5. Methodichka front

Parallel, disjoint files from Sangram articles:

- Kochergina: owned by H1454 (appendix «Открытые вопросы визы»).
- Apte: residual OPEN/PARTIAL on `METODICHKA_APTE_KOMMENTARII_2026.md` (B1).
- A65 OPEN research notes (HB-*/HK-*) are **not** methodichka; optional later wave — park unless a probe is already specified in claims.yml.

_Dr. Mārcis Gasūns_
