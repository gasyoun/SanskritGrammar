"""``sg`` console entry point.

Slice A (H2309) delivers the three orchestration verbs the Wave-1 pilots build
on::

    sg pipeline list
    sg pipeline check <id>
    sg pipeline run <id>

Exit codes are part of the contract, because CI gates on them:

=====  =========================================================
Code   Meaning
=====  =========================================================
``0``  success
``1``  a declared pipeline failed validation or execution
``2``  usage error (argparse convention)
``3``  the requested pipeline id does not exist
``4``  a contract could not be read at all (ContractError)
=====  =========================================================

``sg pipeline run`` resolves every step command against the
:mod:`sg_tooling.generators` registry BEFORE executing anything, so a manifest
naming an unregistered command fails closed instead of half-running. Slice A
registers no content generators, so a manifest declaring real work is expected
to report its unregistered commands until its pilot lands -- that is the fence
working, not a defect.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Sequence

from sg_tooling import __version__
from sg_tooling.contracts import (
    ContractError,
    ValidationReport,
    validate_pipeline,
    validate_provenance_lock,
)
from sg_tooling.contracts.validate import read_contract, repo_root
from sg_tooling.domain import topological_order
from sg_tooling.generators import is_registered

EXIT_OK = 0
EXIT_FAILED = 1
EXIT_USAGE = 2
EXIT_NOT_FOUND = 3
EXIT_CONTRACT = 4


def _pipelines_dir(root: Path | None = None) -> Path:
    return (root or repo_root()) / "pipelines"


def _discover_manifests(root: Path | None = None) -> list[Path]:
    """Return every pipeline manifest, sorted by normalized POSIX path.

    Sorted so the listing is byte-identical on Windows and Linux. ``*.schema.json``
    is the contract itself, not a manifest, so it is excluded.
    """
    directory = _pipelines_dir(root)
    if not directory.is_dir():
        return []
    found = [
        p
        for p in directory.iterdir()
        if p.is_file() and p.suffix in (".yml", ".yaml", ".json") and not p.name.endswith(".schema.json")
    ]
    return sorted(found, key=lambda p: p.as_posix())


def _load_manifest(path: Path) -> dict:
    """Read a manifest through the contracts reader, so the CLI and the
    validators can never disagree about how a manifest is parsed."""
    payload = read_contract(path)
    if not isinstance(payload, dict):
        raise ContractError(f"{path}: manifest must be a mapping at the top level")
    return payload


def _manifest_for(pipeline_id: str, root: Path | None = None) -> tuple[Path, dict] | None:
    """Find the manifest declaring ``pipeline_id``.

    Matches the declared ``pipeline_id`` field, accepting either the full
    ``pipeline:slug`` form or the bare slug, so ``sg pipeline check knauer-frazy-1908``
    works as the verification doc writes it.
    """
    wanted = pipeline_id if pipeline_id.startswith("pipeline:") else f"pipeline:{pipeline_id}"
    for path in _discover_manifests(root):
        try:
            payload = _load_manifest(path)
        except ContractError:
            continue
        if payload.get("pipeline_id") == wanted:
            return path, payload
    return None


def _print_report(report: ValidationReport, stream) -> None:
    print(report.describe(), file=stream)


def _cmd_pipeline_list(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else None
    manifests = _discover_manifests(root)
    if not manifests:
        print(
            "no pipeline manifests declared yet "
            f"(searched {_pipelines_dir(root).as_posix()})"
        )
        return EXIT_OK
    for path in manifests:
        try:
            payload = _load_manifest(path)
        except ContractError as exc:
            print(f"{path.name}\t<unreadable: {exc}>")
            continue
        print(f"{payload.get('pipeline_id', '<no id>')}\t{payload.get('owner', '<no owner>')}\t{path.name}")
    return EXIT_OK


def _cmd_pipeline_check(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else None
    found = _manifest_for(args.pipeline_id, root)
    if found is None:
        print(f"pipeline {args.pipeline_id!r} is not declared", file=sys.stderr)
        return EXIT_NOT_FOUND
    path, payload = found

    report = validate_pipeline(path, root)
    _print_report(report, sys.stdout if report.ok else sys.stderr)

    provenance = validate_provenance_lock(root=root)
    if not provenance.ok:
        _print_report(provenance, sys.stderr)

    unregistered = sorted(
        {
            step.get("command")
            for step in payload.get("steps", [])
            if isinstance(step, dict)
            and isinstance(step.get("command"), str)
            and not is_registered(step["command"])
        }
    )
    if unregistered:
        print(
            "unregistered command(s), no generator claims them: "
            + ", ".join(unregistered),
            file=sys.stderr,
        )

    return EXIT_OK if (report.ok and provenance.ok and not unregistered) else EXIT_FAILED


def _cmd_pipeline_run(args: argparse.Namespace) -> int:
    root = Path(args.root).resolve() if args.root else None
    found = _manifest_for(args.pipeline_id, root)
    if found is None:
        print(f"pipeline {args.pipeline_id!r} is not declared", file=sys.stderr)
        return EXIT_NOT_FOUND
    path, payload = found

    # Fail closed before side effects: validate, then resolve every command.
    report = validate_pipeline(path, root)
    if not report.ok:
        _print_report(report, sys.stderr)
        return EXIT_FAILED

    steps = {
        step["id"]: step
        for step in payload.get("steps", [])
        if isinstance(step, dict) and isinstance(step.get("id"), str)
    }
    graph = {sid: list(step.get("needs") or []) for sid, step in steps.items()}
    try:
        order = topological_order(graph)
    except ValueError as exc:
        print(f"{path.name}: {exc}", file=sys.stderr)
        return EXIT_FAILED

    missing = [sid for sid in order if not is_registered(steps[sid].get("command", ""))]
    if missing:
        for sid in missing:
            print(
                f"{path.name}: step {sid!r} names unregistered command "
                f"{steps[sid].get('command')!r}",
                file=sys.stderr,
            )
        return EXIT_FAILED

    from sg_tooling.generators import resolve

    for sid in order:
        step = steps[sid]
        print(f"[{payload.get('pipeline_id')}] {sid}: {step.get('command')}")
        resolve(step["command"])(step, payload)
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sg",
        description="SanskritGrammar monorepo tooling (pipeline orchestration).",
    )
    parser.add_argument("--version", action="version", version=f"sg {__version__}")
    parser.add_argument(
        "--root",
        default=None,
        help="repository root (defaults to auto-detection from the working directory)",
    )
    sub = parser.add_subparsers(dest="group", required=True)

    pipeline = sub.add_parser("pipeline", help="inspect and execute declared pipelines")
    actions = pipeline.add_subparsers(dest="action", required=True)

    listing = actions.add_parser("list", help="list every declared pipeline")
    listing.set_defaults(func=_cmd_pipeline_list)

    check = actions.add_parser("check", help="validate a pipeline without running it")
    check.add_argument("pipeline_id")
    check.set_defaults(func=_cmd_pipeline_check)

    run = actions.add_parser("run", help="execute a pipeline through registered commands")
    run.add_argument("pipeline_id")
    run.set_defaults(func=_cmd_pipeline_run)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    # UTF-8 on Windows consoles: the repo standard for every printing script.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):  # pragma: no cover - non-tty capture
            pass

    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except ContractError as exc:
        print(f"contract error: {exc}", file=sys.stderr)
        return EXIT_CONTRACT


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
