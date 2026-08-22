"""C2 characterization: pin the CURRENT SG-MO-021 generator behavior before
any code movement (H1913 Slice C2, "characterization/golden tests pin current
behavior before movement").

The goldens in expected/ were captured by driving the pre-cutover
``scripts/sg_mo_021_future.py`` against the deterministic fixture DB
(capture_goldens.py); every number in them is hand-derived and asserted
explicitly below, so a mechanical capture error cannot silently become the
contract. After the extraction these SAME goldens must be reproduced through
the registered ``sg_mo_021_future.generate`` command — byte for byte.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

import build_fixture

HERE = Path(__file__).resolve().parent
EXPECTED_DIR = HERE / "expected"

# Hand-derived fixture numbers (see build_fixture.py docstring).
FIN_TOTAL = 80
FIN_FUT = 74
SIMPLE = 59
PERI = 15
COND = 5
POT = 2
FUT_PART = 4


@pytest.fixture(scope="module")
def fixture_db(tmp_path_factory):
    return build_fixture.build_dcs_fixture(
        tmp_path_factory.mktemp("h1913-golden") / "dcs_fixture.sqlite"
    )


def run_legacy_generator(db, out_dir):
    """Drive the pre-cutover script exactly as production did."""
    import sg_mo_021_future as legacy

    legacy.OUT_DIR = Path(out_dir)
    old_argv = sys.argv
    sys.argv = ["sg_mo_021_future", "--db", str(db)]
    try:
        rc = legacy.main()
    finally:
        sys.argv = old_argv
    assert rc == 0
    return rc


def _load_summary(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_golden_outputs_reproduced_by_legacy_script(fixture_db, tmp_path):
    """Byte-identical regeneration of both committed-shape outputs."""
    run_legacy_generator(fixture_db, tmp_path)
    for name in ("coverage_summary.json", "validation_sample.tsv"):
        produced = (tmp_path / name).read_bytes()
        golden = (EXPECTED_DIR / name).read_bytes()
        assert produced == golden, f"{name} drifted from the captured golden"


def test_determinism_two_runs_byte_identical(fixture_db, tmp_path):
    run_legacy_generator(fixture_db, tmp_path / "a")
    run_legacy_generator(fixture_db, tmp_path / "b")
    for name in ("coverage_summary.json", "validation_sample.tsv"):
        assert (tmp_path / "a" / name).read_bytes() == (
            tmp_path / "b" / name
        ).read_bytes()


def test_hand_derived_numbers_hold(tmp_path):
    """The goldens are not just self-consistent: every headline number equals
    the hand-derived value for this row set (build_fixture docstring)."""
    summary = _load_summary(EXPECTED_DIR / "coverage_summary.json")
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
    source = (HERE.parents[2] / "scripts" / "sg_mo_021_future.py").read_text(encoding="utf-8")
    for token in ("crosswalk", "whitneyroots", "WhitneyRoots"):
        assert token not in source
