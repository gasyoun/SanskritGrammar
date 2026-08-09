"""Shared pytest setup for the SanskritGrammar build-script tests.

The build scripts live in ``scripts/`` and are run as standalone programs
(``python scripts/build_errata.py``), not as an installed package, so tests
import them by putting ``scripts/`` on ``sys.path``. Each script guards its
entry point with ``if __name__ == "__main__":``, so importing only defines the
functions — nothing runs. ``sys.argv`` is neutralised in case a module ever
inspects it at import time.

``packages/sg_tooling/src`` joins ``sys.path`` too (H2309, Slice A) so the
contract suites import ``sg_tooling`` whether or not the workspace has been
``uv sync``'d. Under ``uv run`` the installed distribution is already importable
and this entry is simply redundant; in a plain ``python -m pytest`` it is what
makes the package reachable.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "scripts"
SG_TOOLING_SRC = ROOT / "packages" / "sg_tooling" / "src"

for entry in (SCRIPTS, SG_TOOLING_SRC):
    if str(entry) not in sys.path:
        sys.path.insert(0, str(entry))

sys.argv = ["pytest"]
