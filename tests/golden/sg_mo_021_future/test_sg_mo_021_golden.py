"""C2/C3 golden contract for the SG-MO-021 pilot (H1913).

The goldens in expected/ were captured from the pre-cutover generator
(scripts/sg_mo_021_future.py, deleted in the hard cutover; the capture driver
is preserved in git history as tests/golden/sg_mo_021_future/capture_goldens.py
@ 1f56d3e). Since the cutover they are reproduced through the REGISTERED
command — the same resolution path the pipeline runner uses — and every
headline number is asserted against hand-derived fixture values, so a
mechanical capture error can never silently become the contract.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

import build_fixture

HERE = Path(__file__).resolve().parent
EXPECTED_DIR = HERE / "expected"
GENERATOR_SOURCE = (
    HERE.parents[2] / "packages" / "sg_tooling" / "src" / "sg_tooling" /
    "generators" / "sg_mo_021_future.py"
)

# Hand-derived fixture numbers (see build_fixture.py docstring).
FIN_TOTAL = 80
FIN_FUT = 74
SIMPLE = 59
PERI = 15
COND = 5
POT = 2
FUT_PART = 4


def norm(data: bytes) -> bytes:
    """The committed-artifact normalization contract (.gitattributes pins LF)."""
    return data.replace(b"\r\n", b"\n")


@pytest.fixture(scope="module")
def fixture_db(tmp_path_factory):
    return build_fixture.build_dcs_fixture(
        tmp_path_factory.mktemp("h1913-golden") / "dcs_fixture.sqlite"
    )


def run_registered_command(db, out_dir):
    """Drive sg_mo_021_future.generate the way the manifest step does."""
    from sg_tooling.generators import resolve

    step = {"options": {"db": str(db), "out_dir": str(out_dir)}}
    return resolve("sg_mo_021_future.generate")(step, {})


def test_golden_outputs_reproduced_by_registered_command(fixture_db, tmp_path):
    run_registered_command(fixture_db, tmp_path)
    for name in ("coverage_summary.json", "validation_sample.tsv"):
        produced = norm((tmp_path / name).read_bytes())
        golden = norm((EXPECTED_DIR / name).read_bytes())
        assert produced == golden, f"{name} drifted from the captured golden"


def test_determinism_two_runs_byte_identical(fixture_db, tmp_path):
    run_registered_command(fixture_db, tmp_path / "a")
    run_registered_command(fixture_db, tmp_path / "b")
    for name in ("coverage_summary.json", "validation_sample.tsv"):
        assert norm((tmp_path / "a" / name).read_bytes()) == norm(
            (tmp_path / "b" / name).read_bytes()
        )


def test_hand_derived_numbers_hold():
    """The goldens are not just self-consistent: every headline number equals
    the hand-derived value for this row set (build_fixture docstring)."""
    summary = json.loads((EXPECTED_DIR / "coverage_summary.json").read_text(encoding="utf-8"))
    den = summary["denominators"]
    assert den["finite_total"] == FIN_TOTAL
    assert den["finite_future"] == FIN_FUT
    assert den["simple_future"] == SIMPLE
    assert den["periphrastic_future"] == PERI
    assert den["conditional"] == COND
    assert den["future_participle"] == FUT_PART
    assert den["finite_future_share"] == round(FIN_FUT / FIN_TOTAL, 4)
    assert den["periphrastic_share_of_future"] == round(PERI / FIN_FUT, 4)

    assert {k: v["tokens"] for k, v in summary["person"].items()} == {
        "1": 27,
        "2": 8,
        "3": 39,
    }
    assert {k: v["tokens"] for k, v in summary["number"].items()} == {
        "Sing": 67,
        "Plur": 7,
    }
    mood = {k: v["tokens"] for k, v in summary["mood"].items()}
    assert mood == {"Ind": FIN_FUT - COND - POT, "Cond": COND, "Pot": POT}

    # strictly descending top-form counts: the fixture makes GROUP BY order tie-free
    counts = [row["tokens"] for row in summary["top_forms"]]
    assert counts == sorted(counts, reverse=True)
    assert len(set(counts)) == len(counts)
    assert [r["form"] for r in summary["top_forms"]] == [
        "kariṣyāmi",
        "bhaviṣyati",
        "bhavitā",
        "gamiṣyāmi",
        "vakṣyasi",
        "bhaviṣyanti",
        "akariṣyat",
        "kartāsmi",
        "syāt",
    ]
    assert [r["form"] for r in summary["top_periphrastic"]] == ["bhavitā", "kartāsmi"]

    sample_meta = summary["validation_sample"]
    rows = (EXPECTED_DIR / "validation_sample.tsv").read_text(encoding="utf-8").splitlines()
    assert sample_meta["seed"] == 20260717
    assert sample_meta["size"] == 50
    assert len(rows) == 51  # header + 50 sampled future tokens


def test_issue_563_tokens_absent_from_generator_source():
    """C0 gate: no crosswalk/Pāṇini token enters the declared input surface."""
    source = GENERATOR_SOURCE.read_text(encoding="utf-8")
    for token in ("crosswalk", "whitneyroots", "WhitneyRoots"):
        assert token not in source
