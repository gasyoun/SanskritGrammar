from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from sg_tooling.contracts import ContractError, load_pipeline, repository_root, validate_pipeline

OK = 0
INVALID = 1
NOT_FOUND = 3
EXECUTION_FAILED = 4


def _pipeline_ids(root: Path) -> list[str]:
    return sorted(path.stem for path in (root / "pipelines").glob("*.json") if not path.name.endswith(".schema.json"))


def _resolve(command: list[str], cwd: Path) -> list[str]:
    executable = command[0]
    resolved = shutil.which(executable)
    if resolved is None:
        candidate = (cwd / executable).resolve()
        if not candidate.is_file():
            raise ContractError(f"command is not resolvable: {executable}")
        resolved = os.fspath(candidate)
    return [resolved, *command[1:]]


def _check(pipeline_id: str, root: Path) -> int:
    try:
        path, document = load_pipeline(pipeline_id, root)
        validate_pipeline(document, root)
    except FileNotFoundError:
        print(f"pipeline not found: {pipeline_id}", file=sys.stderr)
        return NOT_FOUND
    except (ContractError, ValueError) as error:
        print(f"invalid pipeline {pipeline_id}: {error}", file=sys.stderr)
        return INVALID
    print(f"valid: {path.relative_to(root)}")
    return OK


def _run(pipeline_id: str, root: Path) -> int:
    try:
        _, document = load_pipeline(pipeline_id, root)
        validate_pipeline(document, root)
        resolved: list[tuple[list[str], Path]] = []
        for step in document["steps"]:
            cwd = (root / step.get("cwd", ".")).resolve()
            resolved.append((_resolve(step["command"], cwd), cwd))
    except FileNotFoundError:
        print(f"pipeline not found: {pipeline_id}", file=sys.stderr)
        return NOT_FOUND
    except (ContractError, ValueError) as error:
        print(f"pipeline refused before execution: {error}", file=sys.stderr)
        return INVALID
    for command, cwd in resolved:
        result = subprocess.run(command, cwd=cwd, check=False)
        if result.returncode:
            return EXECUTION_FAILED
    return OK


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="sg")
    groups = root.add_subparsers(dest="group", required=True)
    pipeline = groups.add_parser("pipeline")
    commands = pipeline.add_subparsers(dest="command", required=True)
    commands.add_parser("list")
    for command in ("check", "run"):
        item = commands.add_parser(command)
        item.add_argument("id")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = repository_root()
    if args.command == "list":
        for pipeline_id in _pipeline_ids(root):
            print(pipeline_id)
        return OK
    if args.command == "check":
        return _check(args.id, root)
    return _run(args.id, root)


if __name__ == "__main__":
    raise SystemExit(main())

