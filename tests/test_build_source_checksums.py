"""Tests for scripts/build_source_checksums.py (B7, ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md
Angle-B site backlog): fixity checksums over every tracked .doc/.docx source."""
import json

import build_source_checksums as bsc


def test_tracked_source_files_only_doc_and_docx():
    files = bsc.tracked_source_files()
    assert files, "expected at least one tracked .doc/.docx source file"
    assert all(f.lower().endswith((".doc", ".docx")) for f in files)
    assert files == sorted(files)


def test_sha256_of_is_deterministic(tmp_path):
    sample = tmp_path / "sample.docx"
    sample.write_bytes(b"hello world")
    first = bsc.sha256_of(sample)
    second = bsc.sha256_of(sample)
    assert first == second
    assert len(first) == 64


def test_build_manifest_matches_committed_manifest():
    manifest = bsc.build_manifest()
    recorded = json.loads(bsc.MANIFEST.read_text(encoding="utf-8"))
    assert manifest == recorded, (
        "scripts/data/source_checksums.json is stale — "
        "run `python scripts/build_source_checksums.py` and commit the result"
    )


def test_check_mode_is_clean():
    manifest = bsc.build_manifest()
    recorded = json.loads(bsc.MANIFEST.read_text(encoding="utf-8"))
    problems = []
    recorded_files = recorded.get("files", {})
    for rel, info in manifest["files"].items():
        prior = recorded_files.get(rel)
        if prior is None:
            problems.append(f"UNRECORDED {rel}")
        elif prior["sha256"] != info["sha256"]:
            problems.append(f"DRIFT {rel}")
    for rel in recorded_files:
        if rel not in manifest["files"]:
            problems.append(f"REMOVED {rel}")
    assert problems == []
