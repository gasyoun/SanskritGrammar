"""Path setup for the SG-MO-021 golden tests: the fixture builder lives next
to the tests, and the pre-cutover generator lives in scripts/ (same pattern as
the root tests/conftest.py)."""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = HERE.parents[2] / "scripts"

for entry in (str(HERE), str(SCRIPTS)):
    if entry not in sys.path:
        sys.path.insert(0, entry)
