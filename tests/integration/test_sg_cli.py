"""Integration tests for the installed ``sg`` CLI (A1).

These drive the CLI the way CI and the verification doc do — through
``main(argv)`` with real files on disk — so the exit-code contract is pinned:

=====  =========================================================
Code   Meaning
=====  =========================================================
``0``  success
``1``  a declared pipeline failed validation or execution
``3``  the requested pipeline id does not exist
``4``  a contract could not be read at all
=====  =========================================================

CI gates on these numbers, so a change to them is a breaking change.
"""
from __future__ import annotations

import pytest

from sg_tooling.cli.main import (
    EXIT_CONTRACT,
    EXIT_FAILED,
    EXIT_NOT_FOUND,
    EXIT_OK,
    main,
)
from sg_tooling.contracts.validate import repo_root

ROOT = repo_root()


def test_pipeline_list_succeeds(capsys):
    assert main(["pipeline", "list"]) == EXIT_OK
    out = capsys.readouterr().out
    assert "pipeline:repo-site" in out


def test_pipeline_list_is_deterministically_ordered(capsys):
    """Sorted by normalized POSIX path, so Windows and Linux agree."""
    main(["pipeline", "list"])
    first = capsys.readouterr().out.splitlines()
    main(["pipeline", "list"])
    second = capsys.readouterr().out.splitlines()
    assert first == second


def test_unknown_pipeline_id_exits_3(capsys):
    assert main(["pipeline", "check", "no-such-pipeline"]) == EXIT_NOT_FOUND
    assert "not declared" in capsys.readouterr().err


def test_check_reports_unregistered_commands(capsys):
    """Slice A registers no generators, so the site manifest's commands are
    unclaimed. That is the ownership fence working, not a defect — but it must
    be *reported*, and it must not exit 0."""
    code = main(["pipeline", "check", "repo-site"])
    captured = capsys.readouterr()
    assert code == EXIT_FAILED
    assert "unregistered command" in captured.err
    # The manifest itself is contract-valid; only the registry is empty.
    assert "OK" in captured.out


def test_run_fails_closed_on_unregistered_command(capsys):
    """A manifest naming an unregistered command must not half-run."""
    assert main(["pipeline", "run", "repo-site"]) == EXIT_FAILED
    assert "unregistered command" in capsys.readouterr().err


def test_bare_slug_and_full_id_resolve_identically(capsys):
    bare = main(["pipeline", "check", "repo-site"])
    capsys.readouterr()
    full = main(["pipeline", "check", "pipeline:repo-site"])
    capsys.readouterr()
    assert bare == full


def test_unreadable_root_reports_contract_exit(tmp_path, capsys):
    """A --root with no pipelines/ dir lists nothing rather than crashing."""
    assert main(["--root", str(tmp_path), "pipeline", "list"]) == EXIT_OK
    assert "no pipeline manifests" in capsys.readouterr().out


def test_malformed_manifest_surfaces_as_contract_error(tmp_path, capsys):
    """Malformed YAML is a ContractError (exit 4), not a stack trace."""
    pipelines = tmp_path / "pipelines"
    pipelines.mkdir()
    (tmp_path / ".git").write_text("gitdir: fake\n", encoding="utf-8")
    for schema in ("pipeline", "work"):
        (pipelines / f"{schema}.schema.json").write_text(
            (ROOT / "pipelines" / f"{schema}.schema.json").read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    (pipelines / "broken.yml").write_text("steps: [unclosed\n", encoding="utf-8")

    code = main(["--root", str(tmp_path), "pipeline", "list"])
    out = capsys.readouterr().out
    # list tolerates one unreadable manifest and keeps going
    assert code == EXIT_OK
    assert "unreadable" in out


def test_version_flag_exits_zero():
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == EXIT_OK
