"""Shared pytest setup for the SanskritGrammar build-script tests.

The build scripts live in ``scripts/`` and are run as standalone programs
(``python scripts/build_errata.py``), not as an installed package, so tests
import them by putting ``scripts/`` on ``sys.path``. Each script guards its
entry point with ``if __name__ == "__main__":``, so importing only defines the
functions — nothing runs. ``sys.argv`` is neutralised in case a module ever
inspects it at import time.
"""
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

sys.argv = ["pytest"]
