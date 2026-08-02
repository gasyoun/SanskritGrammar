"""Tests for scripts/atlas_validate_bundle.py (H1839).

Wires the validator's --self-test and the committed public bundle (when present).
"""
from pathlib import Path

import atlas_validate_bundle as avb

ROOT = Path(__file__).resolve().parent.parent
BUNDLE = ROOT / "sangram" / "atlas" / "data" / "atlas.bundle.json"


def test_self_test():
    assert avb.self_test() == 0


def test_fixture_path_exists():
    assert avb.FIXTURE_PATH.is_file()


def test_committed_bundle_valid_if_present():
    if not BUNDLE.is_file():
        return  # bundle is optional until a rebuild lands
    assert avb.run_file(BUNDLE) == 0
