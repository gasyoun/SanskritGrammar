"""Integration: the SG-MO-021 pilot pipeline end-to-end through the ``sg`` CLI
(H1913 Slice C2/C4).

Drives ``sg pipeline check/run sg-mo-021-future`` exactly as the V-C gate
does, against a temporary repository root holding the real manifest, the real
schemas, and the real provenance lock - with the off-Git DCS master replaced
by the deterministic fixture database (CI has no corpus). The outputs must be
byte-identical to the pre-cutover goldens and byte-stable across runs.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

from sg_tooling.cli.main import EXIT_FAILED, EXIT_OK, main

HERE = Path(__file__).resolve().parent
ROOT = HERE.resolve().parents[1]
GOLDEN_DIR = ROOT / "tests" / "golden" / "sg_mo_021_future"
EXPECTED_DIR = GOLDEN_DIR / "expected"

if str(GOLDEN_DIR) not in sys.path:
    sys.path.insert(0, str(GOLDEN_DIR))

import build_fixture  # noqa: E402


PIPELINE_ID = "sg-mo-021-future"


def norm(data: bytes) -> bytes:
    """Committed-artifact normalization contract (.gitattributes pins LF).

    A Windows-emitted CRLF working copy is the same artifact as its LF index
    form; content drift still fails loudly.
    """
    return data.replace(b"\r\n", b"\n")


def without_input_hash(data: bytes) -> str:
    """Blank the snapshot's embedded input sha256 (sqlite file bytes differ
    across platform sqlite builds); the hash binding itself is verified live
    in tests/golden/sg_mo_021_future/test_sg_mo_021_golden.py."""
    import re

    return re.sub(
        r'"sha256": "[0-9a-f]{64}"',
        '"sha256": "<input-hash>"',
        norm(data).decode("utf-8"),
    )
OUTPUTS = (
    "sangram/articles/future/data/coverage_summary.json",
    "sangram/articles/future/data/validation_sample.tsv",
)


def _make_repo(tmp_path: Path, db_path: Path) -> Path:
    """A minimal repo root carrying this pipeline's real contracts."""
    root = tmp_path / "repo"
    (root / "pipelines").mkdir(parents=True)
    (root / ".git").write_text("gitdir: fake\n", encoding="utf-8")
    for schema in ("pipeline.schema.json", "work.schema.json"):
        shutil.copyfile(ROOT / "pipelines" / schema, root / "pipelines" / schema)
    # The production manifest plus declarative overrides pointing at the
    # fixture master and a temp output dir - the option surface the schema
    # allows; production defaults resolve inside the real repository.
    text = (ROOT / "pipelines" / f"{PIPELINE_ID}.yml").read_text(encoding="utf-8")
    anchor = "  - id: generate\n"
    assert anchor in text
    text = text.replace(
        anchor,
        anchor
        + f"    options:\n"
        + f"      db: {db_path.as_posix()}\n"
        + f"      out_dir: {(tmp_path / 'out').as_posix()}\n",
        1,
    )
    (root / "pipelines" / f"{PIPELINE_ID}.yml").write_text(text, encoding="utf-8")
    (root / "data").mkdir()
    shutil.copyfile(ROOT / "data" / "provenance.lock.json", root / "data" / "provenance.lock.json")
    return root


@pytest.fixture()
def env(tmp_path, monkeypatch):
    db_path = build_fixture.build_dcs_fixture(tmp_path / "dcs_fixture.sqlite")
    root = _make_repo(tmp_path, db_path)
    # Defaults must resolve inside THIS temp root, never the real tree.
    import sg_tooling.generators.sg_mo_021_future as gen

    monkeypatch.setattr(gen, "repo_root", lambda start=None: root)
    return {"root": root, "db": db_path, "gen": gen, "out_dir": tmp_path / "out"}


def test_pipeline_check_is_green(env, capsys):
    assert main(["--root", str(env["root"]), "pipeline", "check", PIPELINE_ID]) == EXIT_OK
    captured = capsys.readouterr()
    assert "unregistered command" not in captured.err


def test_run_writes_golden_identical_outputs(env):
    out_dir = env["out_dir"]
    root = env["root"]
    assert main(["--root", str(root), "pipeline", "run", PIPELINE_ID]) == EXIT_OK
    for rel in OUTPUTS:
        produced = without_input_hash((out_dir / Path(rel).name).read_bytes())
        golden = without_input_hash((EXPECTED_DIR / Path(rel).name).read_bytes())
        assert produced == golden, f"{rel} drifted from the pre-cutover golden"


def test_run_twice_is_byte_stable(env):
    """The determinism half of V-C: a second full run changes nothing."""
    root = env["root"]
    assert main(["--root", str(root), "pipeline", "run", PIPELINE_ID]) == EXIT_OK
    before = {rel: norm((env["out_dir"] / Path(rel).name).read_bytes()) for rel in OUTPUTS}
    assert main(["--root", str(root), "pipeline", "run", PIPELINE_ID]) == EXIT_OK
    for rel in OUTPUTS:
        after = norm((env["out_dir"] / Path(rel).name).read_bytes())
        assert after == before[rel], f"{rel} is not deterministic across runs"


def test_unknown_pipeline_exits_3(env):
    assert main(["--root", str(env["root"]), "pipeline", "check", "no-such"]) == 3


def test_frozen_seed_and_sample_size_are_refused(env):
    step = {
        "options": {"seed": 1, "sample_size": 10},
    }
    with pytest.raises(ValueError, match="frozen"):
        env["gen"].generate(step, {})
