### Changed
- **Ночной consolidation-ledger refresh переведён на один rolling-branch + один PR (H7967, GLM lane / MiMo V2.6 Pro `mimo-v2.6-pro`, 10-11-2026).** [PR #1173](https://github.com/gasyoun/SanskritGrammar/pull/1173) (merged `324356c`): датированные `chore/ledger-refresh-YYYYMMDD` ветка+PR каждую изменившуюся ночь заменены одной bot-владеемой веткой `chore/ledger-refresh` и одним открытым PR — последующие изменившиеся прогоны заменяют единственный generator-owned коммит через `--force-with-lease` и обновляют ТОТ ЖЕ PR; ночь без изменений не открывает ничего. Оркестрация: [`scripts/consolidation_ledger_pr_orchestrate.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/consolidation_ledger_pr_orchestrate.py) (чистое ядро `plan()`); fail-closed: single-file scope guard (`sangram/editorial/data/consolidation_ledger.json`), чужая/не-owned ветка (tip без owner-маркера) никогда не обновляется, ни одна команда не называет другую ветку/PR; легаси датированные PR не закрываются и не удаляются (вне скоупа). Семантика ledger'а и рулсеты не тронуты.

### Verification
- `pytest tests/test_consolidation_ledger_pr_orchestrate.py` — 8/8 (reuse branch+PR между двумя прогонами · no-change без PR · fail-closed до любой мутации · foreign branch/PR не трогается).
- `python scripts/consolidation_ledger_refresh.py --check` exit 0; `--self-test` 4/4; соседние сьюты (`test_consolidation_ledger*`, `test_same_sha_workflow`) — 24 passed.
- CI required gate green ([run 42814986627](https://github.com/gasyoun/SanskritGrammar/actions/runs/42814986627/job/129825684081), 6m39s). Независимая сессия-ревьюер (lane-reviewer, fresh context) — PASS.

### Risks
- Live-run evidence pending до пост-merge авторизованного dispatch (`gh workflow run consolidation-ledger-nightly.yml --ref main`) — production-активация по брифу отдельно авторизуется.
- Однонедельный benefit-пересчёт ≤17-11-2026 против baseline 2026-11-10T12:20:55Z (3 открытых датированных refresh-PR: #1169/#1171/#1172); гипотеза — меньше ручной разборки конфликтов, не гарантированная экономия.

### Files
- `.github/workflows/consolidation-ledger-nightly.yml` — шаг датированной ветки/PR заменён вызовом оркестратора
- `scripts/consolidation_ledger_pr_orchestrate.py` — новый
- `tests/test_consolidation_ledger_pr_orchestrate.py` — новый

_H7967 · GLM lane (MiMo V2.6 Pro, `mimo-v2.6-pro`) · 10-11-2026_
