"""One-off: capture SG-MO-021 goldens from the CURRENT legacy script behavior.

Run from the repo root:
    uv run python tests/golden/sg_mo_021_future/capture_goldens.py

Writes expected/coverage_summary.json + expected/validation_sample.tsv by
driving scripts/sg_mo_021_future.py (pre-cutover generator) against the
deterministic fixture DB. Characterization-before-movement, C2 of H1913.
"""
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))

import build_fixture  # noqa: E402
import sg_mo_021_future as legacy  # noqa: E402

out_dir = Path(tempfile.mkdtemp(prefix="h1913-golden-"))
legacy.OUT_DIR = out_dir
db = build_fixture.build_dcs_fixture(out_dir / "dcs_fixture.sqlite")
sys.argv = ["sg_mo_021_future", "--db", str(db)]
rc = legacy.main()
assert rc == 0, rc

expected = HERE / "expected"
expected.mkdir(exist_ok=True)
shutil.copyfile(out_dir / "coverage_summary.json", expected / "coverage_summary.json")
shutil.copyfile(out_dir / "validation_sample.tsv", expected / "validation_sample.tsv")
print("captured:", sorted(p.name for p in expected.iterdir()))
