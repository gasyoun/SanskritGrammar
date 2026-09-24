"""Wave-2 RQ2 unified drill bank — schema, non-fabrication, parity gate.

Verifies build_unified_drill_bank.py never upgrades an unverified upstream
row to `verified=true`, that its schema is stable, and that `--check`
catches drift against the committed verification_summary.json.
"""
import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILDER_DIR = ROOT / "sangram" / "data" / "unified_drills"
BUILDER = BUILDER_DIR / "build_unified_drill_bank.py"
TSV = BUILDER_DIR / "unified_drill_bank.tsv"
SUMMARY = BUILDER_DIR / "verification_summary.json"

FIELDS = [
    "drill_id", "drill_type", "prompt", "answer_key", "verified",
    "verification_method", "difficulty_band", "source_dataset", "source_row_id",
]


def _rows():
    with TSV.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def test_check_mode_passes_against_committed_artifact():
    out = subprocess.run([sys.executable, str(BUILDER), "--check"],
                         capture_output=True, text=True)
    assert out.returncode == 0, out.stdout + out.stderr
    assert "OK:" in out.stdout


def test_schema_columns():
    header = TSV.read_text(encoding="utf-8").split("\n")[0].split("\t")
    assert header == FIELDS


def test_drill_ids_unique():
    ids = [r["drill_id"] for r in _rows()]
    assert len(ids) == len(set(ids)), "duplicate drill_id"


def test_drill_types_valid():
    rows = _rows()
    assert {r["drill_type"] for r in rows} == {"declension", "samasa", "sandhi"}


def test_verified_is_boolean_string():
    for r in _rows():
        assert r["verified"] in ("true", "false"), r["drill_id"]


def test_declension_mismatch_never_verified():
    """The non-fabrication guarantee: a source `agreement` of mismatch or
    no_generation must never surface as verified=true downstream."""
    for r in _rows():
        if r["drill_type"] == "declension" and (
            "mismatch" in r["verification_method"] or "no_generation" in r["verification_method"]
        ):
            assert r["verified"] == "false", r["drill_id"]


def test_declension_match_or_variant_always_verified():
    for r in _rows():
        if r["drill_type"] == "declension" and (
            "agreement:match" in r["verification_method"]
            or "agreement:variant" in r["verification_method"]
        ):
            assert r["verified"] == "true", r["drill_id"]


def test_summary_totals_match_tsv():
    rows = _rows()
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert summary["total"] == len(rows)
    assert summary["verified"] == sum(1 for r in rows if r["verified"] == "true")


def test_all_three_engines_fully_represented():
    rows = _rows()
    counts = {"declension": 0, "samasa": 0, "sandhi": 0}
    for r in rows:
        counts[r["drill_type"]] += 1
    # sanity floors -- catches a silently-skipped source file
    assert counts["declension"] > 40000
    assert counts["samasa"] > 5000
    assert counts["sandhi"] >= 90
