"""H8030 acceptance tests for the reading-transfer pilot kit (docs/teaching-pilot/).

Positive layer: `scripts/check_transfer_pilot_kit.py` must be green on the committed kit.
Negative layer (red-gate discipline): the gate must REFUSE — held-out leakage into a
learner-visible row, a non-blank results record, and a missing PROPOSED label each fail.
Canary layer: pinned golden rows of the split rule (gold idx % 3) so a silent re-split
of the manifest trips CI.

Linguistic/philological review is deliberately NOT asserted here — it stays PENDING
(protocol §3/§10); machine green never equals PASS.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_transfer_pilot_kit.py"


def _load():
    spec = importlib.util.spec_from_file_location("check_transfer_pilot_kit", SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def kit():
    return _load()


def test_committed_kit_is_green(kit):
    assert kit.check() == []


def test_canary_split_rule(kit):
    items = kit._rows(kit.ITEMS)
    assert len(items) == 30
    worked = [r for r in items if r["set"] == "worked"]
    heldout = [r for r in items if r["set"] == "heldout"]
    assert (worked[0]["item_id"], worked[0]["surface"]) == ("W01", "rājendra")
    assert len(worked) == len(heldout) == 10
    # split rule: gold file order, idx % 3 (0-based) -> worked/practice/heldout
    gold = kit._rows(kit.GOLD)
    for row in items:
        gi = int(row["gold_row_index"].replace("gold_r", "")) - 1
        assert row["surface"] == gold[gi]["surface"]
        assert row["set"] == ("worked", "practice", "heldout")[gi % 3]


def test_negative_heldout_leakage_refused(kit, tmp_path, monkeypatch):
    rows = kit._rows(kit.ITEMS)
    held = next(r for r in rows if r["set"] == "heldout")
    for r in rows:
        if r["set"] == "worked":
            r["surface"] = held["surface"]  # leak a held-out surface into worked
            break
    fake = tmp_path / "items.tsv"
    with fake.open("w", encoding="utf-8", newline="") as fh:
        import csv

        w = csv.DictWriter(fh, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    monkeypatch.setattr(kit, "ITEMS", fake)
    errs = kit.check()
    assert any("LEAKAGE" in e for e in errs), errs


def test_negative_nonblank_results_refused(kit, tmp_path, monkeypatch):
    fake = tmp_path / "RESULTS_PENDING.md"
    fake.write_text(
        "Status: INCONCLUSIVE\n\n## Runs\n\n| run_id | date |\n|---|---|\n"
        "| R-001 | 2026-11-11 | 8 | 8 | 0 | 7 | 2 | 2 | 2 | [0.4,0.9] | met | - |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(kit, "RESULTS", fake)
    errs = kit.check()
    assert any("not blank" in e for e in errs), errs


def test_negative_missing_proposed_label_refused(kit, tmp_path, monkeypatch):
    fake = tmp_path / "PROTOCOL.md"
    fake.write_text(
        "Sample size\nScoring rubric\nRetention interval\nExpansion threshold\n"
        "approval checklist\nH8028\nconsent 152-FZ\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(kit, "PROTOCOL", fake)
    errs = kit.check()
    assert any("PROPOSED" in e for e in errs), errs
