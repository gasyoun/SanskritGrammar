"""H4486 — Emeneo sandhi-exercises → sandhi-drills gold enrich (offline)."""
import csv
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BUILDER = REPO / "scripts" / "build_emeneo_sandhi_drills.py"
TSV = REPO / "data" / "emeneo_sandhi" / "emeneo_sandhi_drills.tsv"
COLS = ["id", "type", "rule", "category", "lesson", "difficulty",
        "question", "answer", "choices", "context"]


def _rows():
    with TSV.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def test_parity_gate_passes():
    """The engine reproduces every pamphlet worked example (rules 41-71)."""
    out = subprocess.run([sys.executable, str(BUILDER), "--check"],
                         capture_output=True, text=True)
    assert "PARITY FAIL" not in out.stdout + out.stderr, out.stdout + out.stderr


def test_at_least_50_drills():
    assert TSV.exists()
    rows = _rows()
    assert len(rows) >= 50, f"only {len(rows)} drills"


def test_gold_format_columns_and_unique_ids():
    header = TSV.read_text(encoding="utf-8").split("\n")[0].split("\t")
    assert header == COLS
    rows = _rows()
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate drill ids"
    assert ids == sorted(ids), "ids not ordered"


def test_types_and_categories_valid():
    rows = _rows()
    assert {r["type"] for r in rows} <= {"join", "identify"}
    assert {r["category"] for r in rows} <= {
        "vowel coalescence", "visarga", "anusvāra / nasal", "consonant",
        "unchanged junction",
    }


def test_choices_are_4way_mcq():
    for r in _rows():
        choices = r["choices"].split(" | ")
        assert len(choices) == 4, r["id"]
        assert choices[0] == r["answer"], r["id"]


def test_no_duplicate_question_answer():
    """Gold must not carry literal duplicate drills (pamphlet repeats junctions)."""
    seen, dups = set(), []
    for r in _rows():
        key = (r["question"], r["answer"])
        if key in seen:
            dups.append(r["id"])
        seen.add(key)
    assert not dups, f"duplicate drills: {dups}"


def test_context_carries_provenance():
    for r in _rows():
        assert "Emeneau&vanNooten 2nd ed." in r["context"], r["id"]
