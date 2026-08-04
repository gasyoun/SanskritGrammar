"""End-to-end rebuild test for scripts/atlas_build_bundle.py (H2271, residual of H1839).

test_atlas_build_bundle.py pins the pure-helper contract only, because a full
rebuild needs the private Uprava hub path (MEGABOOK.md + interlinks_edges.tsv),
which CI does not have. This test exercises the real end-to-end path against
whatever local Uprava checkout the running machine has, then feeds the output
straight into atlas_validate_bundle.py so the two scripts are checked together.
Skips itself (not xfail, not error) when no local Uprava sibling is present —
this stays true to the "pure helpers only in CI" note in PR #578 (H1839-H1842).
"""
import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parent
SCRIPTS = REPO_ROOT / "scripts"
UPRAVA = REPO_ROOT.parent / "Uprava"

pytestmark = pytest.mark.skipif(
    not (UPRAVA / "MEGABOOK.md").exists() or not (UPRAVA / "interlinks_edges.tsv").exists(),
    reason="no local ../Uprava checkout with MEGABOOK.md + interlinks_edges.tsv — "
           "full atlas_build_bundle rebuild needs the private hub, not available in CI",
)


def _run_build(out_path):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "atlas_build_bundle.py"),
         "--uprava", str(UPRAVA), "--out", str(out_path),
         "--generated-by", "test_atlas_build_bundle_e2e.py", "--date", "2026-01-01"],
        cwd=REPO_ROOT, capture_output=True, encoding="utf-8",
    )


def test_full_rebuild_exits_zero_and_writes_bundle(tmp_path):
    out_path = tmp_path / "atlas.bundle.json"
    result = _run_build(out_path)
    assert result.returncode == 0, result.stdout + result.stderr
    assert out_path.exists()


def test_full_rebuild_output_passes_validator(tmp_path):
    out_path = tmp_path / "atlas.bundle.json"
    build = _run_build(out_path)
    assert build.returncode == 0, build.stdout + build.stderr

    validate = subprocess.run(
        [sys.executable, str(SCRIPTS / "atlas_validate_bundle.py"), str(out_path)],
        cwd=REPO_ROOT, capture_output=True, encoding="utf-8",
    )
    assert validate.returncode == 0, validate.stdout + validate.stderr


def test_full_rebuild_has_no_denylisted_repo_nodes(tmp_path):
    import atlas_build_bundle as abb

    out_path = tmp_path / "atlas.bundle.json"
    build = _run_build(out_path)
    assert build.returncode == 0, build.stdout + build.stderr

    bundle = json.loads(out_path.read_text(encoding="utf-8"))
    node_ids = {n["id"] for n in bundle["nodes"]}
    for repo in abb.DROP_REPOS:
        assert f"repo:{abb.slug(repo)}" not in node_ids, f"denylisted repo node leaked: {repo}"

    # Provenance is allowed to *name* the private hub (e.g. "MEGABOOK.md (Uprava,
    # приватный hub)") — only its URL/path/volatile-registry content must never
    # appear. Check the leakage patterns against the payload minus provenance.
    payload_without_provenance = {k: v for k, v in bundle.items() if k != "provenance"}
    serialized = json.dumps(payload_without_provenance, ensure_ascii=False)
    for pattern in abb.LEAKAGE_PATTERNS:
        assert pattern not in serialized, f"banned leakage pattern in bundle: {pattern!r}"


def test_full_rebuild_is_deterministic_given_same_date(tmp_path):
    out_a = tmp_path / "a.json"
    out_b = tmp_path / "b.json"
    build_a = _run_build(out_a)
    build_b = _run_build(out_b)
    assert build_a.returncode == 0, build_a.stdout + build_a.stderr
    assert build_b.returncode == 0, build_b.stdout + build_b.stderr
    assert out_a.read_text(encoding="utf-8") == out_b.read_text(encoding="utf-8")
