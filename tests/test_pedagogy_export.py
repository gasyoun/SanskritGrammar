"""Tests for scripts/build_pedagogy_export.py (H1643).

Acceptance A2 from docs/VERIFICATION_SANSKRITGRAMMAR_PEDAGOGY_LAST_MILE.md:
- build produces export_manifest.json with schema_version
- --check exit 0 on a fresh build
- intentional hash break fails --check
- schema major mismatch fails --check
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import build_pedagogy_export as bpe  # noqa: E402

EXPORT_DIR = REPO / "data" / "pedagogy_export"
MANIFEST = EXPORT_DIR / "export_manifest.json"


@pytest.fixture(scope="module", autouse=True)
def _built_export():
    """Ensure a real export exists for the suite (idempotent rebuild)."""
    bpe.build_export()
    assert MANIFEST.is_file()
    yield


def test_manifest_schema_version_1_0_0():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert data["schema_version"] == "1.0.0"
    assert data["generator"] == "scripts/build_pedagogy_export.py"
    assert isinstance(data["feeds"], list) and len(data["feeds"]) >= 3
    hop = data["last_mile_hop_status"]
    assert hop["A_reader"] == "shipped-in-Systema"
    assert hop["B_srs"] == "shipped-in-Systema"
    assert hop["C_difficulty"] == "shipped-in-Systema"
    assert hop["rq4_harness"] == "shipped-flag-off"


def test_feeds_public_safe_rights_only():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    allowed = {"aggregate-public-safe", "pointer-only-no-bulk-gloss"}
    for feed in data["feeds"]:
        assert feed["rights"] in allowed, feed
        assert "sha256" in feed and len(feed["sha256"]) == 64
        path = REPO / feed["path"]
        assert path.is_file(), feed["path"]


def test_check_exit_0():
    assert bpe.check_export() == 0
    assert bpe.main(["--check"]) == 0


def test_check_fails_on_hash_break(tmp_path, monkeypatch):
    """Break one feed hash → --check must fail; restore after."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    feed = data["feeds"][0]
    path = REPO / feed["path"]
    original = path.read_bytes()
    try:
        path.write_bytes(original + b"\n#hash-break\n")
        assert bpe.check_export() == 1
    finally:
        path.write_bytes(original)
    assert bpe.check_export() == 0


def test_check_fails_on_schema_major_mismatch():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    original = MANIFEST.read_text(encoding="utf-8")
    try:
        data["schema_version"] = "2.0.0"
        MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        assert bpe.check_export(min_major=1) == 1
    finally:
        MANIFEST.write_text(original, encoding="utf-8")
    assert bpe.check_export() == 0


def test_rq4_and_difficulty_feeds_present():
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ids = {f["id"] for f in data["feeds"]}
    assert "rq4_item_bank" in ids
    assert "difficulty_ordering_stats" in ids
    assert "methodichka_corpus_layer_pointers" in ids
