"""JSON-schema and graph validation for pipeline declarations."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


class ContractError(ValueError):
    pass


def repository_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / "pipelines" / "pipeline.schema.json").is_file():
            return candidate
    raise ContractError("not inside a SanskritGrammar checkout")


def load_pipeline(pipeline_id: str, root: Path | None = None) -> tuple[Path, dict]:
    repo = repository_root(root)
    path = repo / "pipelines" / f"{pipeline_id}.json"
    if not path.is_file():
        raise FileNotFoundError(pipeline_id)
    return path, json.loads(path.read_text(encoding="utf-8"))


def validate_pipeline(document: dict, root: Path | None = None) -> None:
    repo = repository_root(root)
    schema = json.loads((repo / "pipelines" / "pipeline.schema.json").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda e: list(e.path))
    if errors:
        raise ContractError("; ".join(error.message for error in errors))
    steps = document["steps"]
    ids = [step["id"] for step in steps]
    if len(ids) != len(set(ids)):
        raise ContractError("step IDs must be unique")
    known = set(ids)
    producers: dict[str, str] = {}
    graph: dict[str, list[str]] = {}
    for step in steps:
        needs = step.get("needs", [])
        if step["id"] in needs:
            raise ContractError(f"step {step['id']} depends on itself")
        unknown = set(needs) - known
        if unknown:
            raise ContractError(f"step {step['id']} needs unknown steps: {sorted(unknown)}")
        overlap = set(step.get("inputs", [])) & set(step.get("outputs", []))
        if overlap:
            raise ContractError(f"step {step['id']} reads and writes {sorted(overlap)}")
        for output in step.get("outputs", []):
            if output in producers:
                raise ContractError(f"output {output} has multiple producers")
            producers[output] = step["id"]
        graph[step["id"]] = needs
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise ContractError("pipeline graph must be acyclic")
        if node in visited:
            return
        visiting.add(node)
        for dependency in graph[node]:
            visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for step_id in ids:
        visit(step_id)

