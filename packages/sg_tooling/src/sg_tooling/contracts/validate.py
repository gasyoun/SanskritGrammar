"""Schema + graph validation for pipeline, work, and provenance contracts.

Two validation layers, deliberately separate:

1. **Schema** -- shape, required keys, enums, patterns, ``additionalProperties:
   false``. Delegated to ``jsonschema`` when installed (CI installs it via
   ``scripts/requirements-dev.txt``); a bounded builtin subset covers the same
   Draft-2020-12 keywords this repo's schemas actually use, so the contracts
   still validate in a plain environment. The repo already uses this
   real-jsonschema-preferred / builtin-fallback split in
   ``scripts/claims_schema_validate.py``; this follows that established pattern
   rather than inventing a second one.
2. **Graph** -- invariants a JSON Schema cannot express: unique step IDs, an
   acyclic dependency graph, ``needs`` resolving to a declared step, no two
   steps claiming the same output, and inputs/outputs not overlapping.

Both return a :class:`ValidationReport` rather than raising, so a caller can
report every problem in one pass. ``ContractError`` is reserved for a contract
that cannot be read at all (missing file, undecodable bytes, malformed JSON).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

CONTRACT_VERSION = 1

# Enumerated rights classes shared by the work and pipeline contracts.
# 'unknown' is representable -- and is never permission. See section 14 of the
# architecture doc: an absent, unknown, conflicting, or expired rights
# assertion fails closed at the PUBLICATION gate, not at the validation gate.
RIGHTS_VALUES = (
    "publishable",
    "publishable-derived-input",
    "restricted-source",
    "per-file",
    "unknown",
)

# Rights classes that the publication boundary accepts. Kept next to
# RIGHTS_VALUES so the two can never drift apart silently.
PUBLICATION_SAFE_RIGHTS = ("publishable", "publishable-derived-input")

_SCHEMA_DIR_CANDIDATES = ("pipelines",)


class ContractError(Exception):
    """A contract document could not be read or parsed at all."""


@dataclass
class ValidationReport:
    """Structured result of validating one document against one contract."""

    contract: str
    source: str
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def add(self, message: str) -> None:
        self.errors.append(message)

    def extend(self, messages: Iterable[str]) -> None:
        self.errors.extend(messages)

    def __bool__(self) -> bool:  # pragma: no cover - convenience only
        return self.ok

    def describe(self) -> str:
        if self.ok:
            return f"{self.contract}: {self.source}: OK"
        lines = [f"{self.contract}: {self.source}: {len(self.errors)} error(s)"]
        lines.extend(f"  - {e}" for e in self.errors)
        return "\n".join(lines)


def repo_root(start: Path | None = None) -> Path:
    """Locate the repository root by walking up for a marker directory.

    Uses ``pipelines/`` (Slice A owns it) and ``.git`` as markers so the CLI
    works from any working directory inside the repo or a linked worktree. In a
    worktree ``.git`` is a FILE, not a directory, so both are accepted.
    """
    here = (start or Path(__file__)).resolve()
    for candidate in (here, *here.parents):
        if not candidate.is_dir():
            continue
        if (candidate / "pipelines").is_dir() and (candidate / ".git").exists():
            return candidate
    # Fall back to the packaged layout: packages/sg_tooling/src/sg_tooling/contracts
    return Path(__file__).resolve().parents[4]


def schema_path(name: str, root: Path | None = None) -> Path:
    """Return the on-disk path of a named schema (``pipeline`` / ``work``)."""
    base = root or repo_root()
    for directory in _SCHEMA_DIR_CANDIDATES:
        candidate = base / directory / f"{name}.schema.json"
        if candidate.is_file():
            return candidate
    raise ContractError(f"schema not found for contract {name!r} under {base}")


def _read_text(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ContractError(f"{path}: file not found") from exc
    except UnicodeDecodeError as exc:
        raise ContractError(f"{path}: not valid UTF-8: {exc}") from exc
    if text.startswith("﻿"):
        raise ContractError(f"{path}: UTF-8 BOM is banned in this repo")
    return text


def _read_json(path: Path) -> Any:
    text = _read_text(path)
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ContractError(f"{path}: malformed JSON: {exc}") from exc


def read_contract(path: Path) -> Any:
    """Read a contract document, dispatching on suffix.

    Manifests are authored as YAML (``pipelines/*.yml``) while schemas and the
    provenance lock are JSON. Both arrive here, so the reader must dispatch --
    parsing a YAML manifest as JSON was the H2309 bug this replaced.

    ``yaml.safe_load`` (never ``load``) keeps a manifest from becoming hidden
    executable code, the injection risk named in architecture section 18.
    """
    if path.suffix in (".yml", ".yaml"):
        import yaml

        text = _read_text(path)
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise ContractError(f"{path}: malformed YAML: {exc}") from exc
    return _read_json(path)


def load_schema(name: str, root: Path | None = None) -> Mapping[str, Any]:
    return _read_json(schema_path(name, root))


# --------------------------------------------------------------- schema core --
# Bounded Draft-2020-12 subset: exactly the keywords the repo's own schemas use.
# Anything unrecognised is ignored rather than silently "passing" a construct
# this validator cannot actually check -- unknown keywords are reported by
# _assert_supported below so a future schema edit cannot quietly go unchecked.
_SUPPORTED_KEYWORDS = frozenset(
    {
        "$schema", "$id", "$ref", "$defs", "title", "description", "comment",
        "type", "const", "enum", "pattern", "minLength", "minimum", "maximum",
        "minItems", "uniqueItems", "items", "properties", "required",
        "additionalProperties",
    }
)

_TYPE_MAP = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "null": type(None),
}


def _resolve(schema: Mapping[str, Any], root: Mapping[str, Any]) -> Mapping[str, Any]:
    ref = schema.get("$ref")
    if not ref:
        return schema
    if not ref.startswith("#/"):
        raise ContractError(f"only local $ref supported, got {ref!r}")
    node: Any = root
    for part in ref[2:].split("/"):
        if not isinstance(node, Mapping) or part not in node:
            raise ContractError(f"unresolvable $ref {ref!r}")
        node = node[part]
    if not isinstance(node, Mapping):
        raise ContractError(f"$ref {ref!r} does not point at a schema object")
    merged = {k: v for k, v in schema.items() if k != "$ref"}
    return {**node, **merged}


def _matches_type(value: Any, declared: Any) -> bool:
    names = declared if isinstance(declared, list) else [declared]
    for name in names:
        if name == "integer":
            if isinstance(value, int) and not isinstance(value, bool):
                return True
            continue
        if name == "number":
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                return True
            continue
        expected = _TYPE_MAP.get(name)
        if expected is None:
            return True  # unknown type name: not ours to police
        if name == "boolean":
            if isinstance(value, bool):
                return True
            continue
        if isinstance(value, bool) and expected is not bool:
            continue
        if isinstance(value, expected):
            return True
    return False


def _validate_node(
    value: Any,
    schema: Mapping[str, Any],
    root: Mapping[str, Any],
    where: str,
    errors: list[str],
) -> None:
    schema = _resolve(schema, root)
    loc = where or "$"

    if "const" in schema and value != schema["const"]:
        errors.append(f"{loc}: expected const {schema['const']!r}, got {value!r}")
        return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(
            f"{loc}: {value!r} is not one of {sorted(map(str, schema['enum']))}"
        )
        return

    if "type" in schema and not _matches_type(value, schema["type"]):
        errors.append(f"{loc}: expected type {schema['type']!r}, got {type(value).__name__}")
        return

    if isinstance(value, str):
        pattern = schema.get("pattern")
        if pattern and not re.search(pattern, value):
            errors.append(f"{loc}: {value!r} does not match pattern {pattern!r}")
        min_length = schema.get("minLength")
        if min_length is not None and len(value) < min_length:
            errors.append(f"{loc}: shorter than minLength {min_length}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        if minimum is not None and value < minimum:
            errors.append(f"{loc}: {value} is below minimum {minimum}")
        maximum = schema.get("maximum")
        if maximum is not None and value > maximum:
            errors.append(f"{loc}: {value} is above maximum {maximum}")

    if isinstance(value, list):
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{loc}: needs at least {min_items} item(s), got {len(value)}")
        if schema.get("uniqueItems"):
            seen: list[Any] = []
            for item in value:
                if item in seen:
                    errors.append(f"{loc}: duplicate item {item!r}")
                    break
                seen.append(item)
        item_schema = schema.get("items")
        if isinstance(item_schema, Mapping):
            for index, item in enumerate(value):
                _validate_node(item, item_schema, root, f"{loc}[{index}]", errors)

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{loc}: missing required key {key!r}")
        properties = schema.get("properties")
        properties = properties if isinstance(properties, Mapping) else {}
        additional = schema.get("additionalProperties", True)
        for key, item in value.items():
            if key in properties:
                _validate_node(item, properties[key], root, f"{loc}.{key}", errors)
            elif isinstance(additional, Mapping):
                _validate_node(item, additional, root, f"{loc}.{key}", errors)
            elif additional is False:
                errors.append(f"{loc}: unknown key {key!r} is not allowed")


def _assert_supported(schema: Any, where: str = "$") -> list[str]:
    """Report schema keywords the builtin validator does not implement."""
    unknown: list[str] = []
    if isinstance(schema, Mapping):
        for key, value in schema.items():
            if key in ("properties", "$defs"):
                if isinstance(value, Mapping):
                    for name, sub in value.items():
                        unknown += _assert_supported(sub, f"{where}.{key}.{name}")
                continue
            if key not in _SUPPORTED_KEYWORDS:
                unknown.append(f"{where}: unsupported schema keyword {key!r}")
                continue
            if key in ("items", "additionalProperties") and isinstance(value, Mapping):
                unknown += _assert_supported(value, f"{where}.{key}")
    return unknown


def _schema_validate(
    document: Any,
    schema: Mapping[str, Any],
    report: ValidationReport,
) -> None:
    """Validate with jsonschema if available, else the builtin subset."""
    try:
        import jsonschema  # type: ignore
    except ImportError:
        report.extend(_assert_supported(schema))
        errors: list[str] = []
        _validate_node(document, schema, schema, "$", errors)
        report.extend(errors)
        return

    validator_cls = jsonschema.validators.validator_for(schema)
    validator = validator_cls(schema)
    for error in sorted(validator.iter_errors(document), key=lambda e: list(e.path)):
        location = "$" + "".join(
            f"[{p}]" if isinstance(p, int) else f".{p}" for p in error.path
        )
        report.add(f"{location}: {error.message}")


# ---------------------------------------------------------------- graph core --
def validate_pipeline_graph(manifest: Mapping[str, Any]) -> list[str]:
    """Check the pipeline invariants JSON Schema cannot express.

    Unique step IDs, resolvable ``needs``, an acyclic graph, one producer per
    output, and no input/output overlap within a step.
    """
    errors: list[str] = []
    steps = manifest.get("steps")
    if not isinstance(steps, Sequence):
        return ["$.steps: not a list; cannot check the graph"]

    ids: list[str] = []
    for index, step in enumerate(steps):
        if not isinstance(step, Mapping):
            errors.append(f"$.steps[{index}]: not an object")
            continue
        step_id = step.get("id")
        if not isinstance(step_id, str):
            errors.append(f"$.steps[{index}]: missing string id")
            continue
        if step_id in ids:
            errors.append(f"$.steps[{index}]: duplicate step id {step_id!r}")
        ids.append(step_id)

    known = set(ids)
    producers: dict[str, str] = {}
    graph: dict[str, list[str]] = {}

    for index, step in enumerate(steps):
        if not isinstance(step, Mapping):
            continue
        step_id = step.get("id")
        if not isinstance(step_id, str):
            continue

        needs = step.get("needs") or []
        if isinstance(needs, Sequence) and not isinstance(needs, (str, bytes)):
            for dep in needs:
                if dep == step_id:
                    errors.append(f"$.steps[{index}]: step {step_id!r} needs itself")
                elif dep not in known:
                    errors.append(
                        f"$.steps[{index}]: needs unknown step {dep!r}"
                    )
            graph[step_id] = [d for d in needs if isinstance(d, str)]
        else:
            graph[step_id] = []

        outputs = step.get("outputs") or []
        inputs = step.get("inputs") or []
        if isinstance(outputs, Sequence) and not isinstance(outputs, (str, bytes)):
            for out in outputs:
                if not isinstance(out, str):
                    continue
                if out in producers:
                    errors.append(
                        f"$.steps[{index}]: output {out!r} is already produced by "
                        f"step {producers[out]!r}; exactly one generator per output"
                    )
                else:
                    producers[out] = step_id
            if isinstance(inputs, Sequence) and not isinstance(inputs, (str, bytes)):
                overlap = sorted(set(map(str, inputs)) & set(map(str, outputs)))
                for path in overlap:
                    errors.append(
                        f"$.steps[{index}]: {path!r} is both an input and an output"
                    )

    # Depth-first cycle detection over `needs`.
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {node: WHITE for node in graph}

    def visit(node: str, trail: list[str]) -> None:
        colour[node] = GREY
        for dep in graph.get(node, []):
            if dep not in colour:
                continue
            if colour[dep] == GREY:
                cycle = " -> ".join([*trail, node, dep])
                errors.append(f"$.steps: dependency cycle: {cycle}")
                continue
            if colour[dep] == WHITE:
                visit(dep, [*trail, node])
        colour[node] = BLACK

    for node in list(graph):
        if colour.get(node) == WHITE:
            visit(node, [])

    return errors


# ------------------------------------------------------------- public façade --
def validate_pipeline(
    document: Mapping[str, Any] | Path | str,
    root: Path | None = None,
) -> ValidationReport:
    """Validate a pipeline manifest: schema, then graph invariants."""
    source = str(document) if isinstance(document, (Path, str)) else "<in-memory>"
    payload = read_contract(Path(document)) if isinstance(document, (Path, str)) else document
    report = ValidationReport(contract="pipeline", source=source)
    _schema_validate(payload, load_schema("pipeline", root), report)
    if isinstance(payload, Mapping):
        report.extend(validate_pipeline_graph(payload))
    return report


def validate_work(
    document: Mapping[str, Any] | Path | str,
    root: Path | None = None,
) -> ValidationReport:
    """Validate a work contract, plus the source/generated disjointness rule."""
    source = str(document) if isinstance(document, (Path, str)) else "<in-memory>"
    payload = read_contract(Path(document)) if isinstance(document, (Path, str)) else document
    report = ValidationReport(contract="work", source=source)
    _schema_validate(payload, load_schema("work", root), report)

    if isinstance(payload, Mapping):
        authority = payload.get("source_authority")
        outputs = payload.get("outputs") or []
        sources: list[str] = []
        if isinstance(authority, Mapping):
            primary = authority.get("primary")
            if isinstance(primary, str):
                sources.append(primary)
            witnesses = authority.get("witnesses") or []
            if isinstance(witnesses, Sequence) and not isinstance(witnesses, (str, bytes)):
                sources.extend(w for w in witnesses if isinstance(w, str))
        if isinstance(outputs, Sequence) and not isinstance(outputs, (str, bytes)):
            for clash in sorted(set(sources) & {o for o in outputs if isinstance(o, str)}):
                report.add(
                    f"$.outputs: {clash!r} is declared as both a source witness and a "
                    "generated output; a generated file may never also be a source"
                )
        for path in [*sources, *(o for o in outputs if isinstance(o, str))]:
            if ".." in Path(path).parts:
                report.add(f"$: path {path!r} escapes the work root via '..'")
    return report


def validate_provenance_lock(
    document: Mapping[str, Any] | Path | str | None = None,
    root: Path | None = None,
) -> ValidationReport:
    """Validate ``data/provenance.lock.json``.

    Every external input needs an immutable revision (a 40-hex commit), a
    rights class, and at least one named consumer. A mutable branch name or a
    bare tag is not immutable provenance.
    """
    base = root or repo_root()
    if document is None:
        document = base / "data" / "provenance.lock.json"
    source = str(document) if isinstance(document, (Path, str)) else "<in-memory>"
    payload = read_contract(Path(document)) if isinstance(document, (Path, str)) else document
    report = ValidationReport(contract="provenance", source=source)

    if not isinstance(payload, Mapping):
        report.add("$: provenance lock must be a JSON object")
        return report

    if payload.get("contract_version") != CONTRACT_VERSION:
        report.add(
            f"$.contract_version: expected {CONTRACT_VERSION}, got "
            f"{payload.get('contract_version')!r}"
        )

    inputs = payload.get("inputs")
    if not isinstance(inputs, Sequence) or isinstance(inputs, (str, bytes)):
        report.add("$.inputs: must be a list")
        return report

    seen_ids: list[str] = []
    for index, entry in enumerate(inputs):
        loc = f"$.inputs[{index}]"
        if not isinstance(entry, Mapping):
            report.add(f"{loc}: not an object")
            continue

        entry_id = entry.get("id")
        if not isinstance(entry_id, str) or not entry_id.startswith("external:"):
            report.add(f"{loc}.id: must be a string of the form 'external:<slug>'")
        elif entry_id in seen_ids:
            report.add(f"{loc}.id: duplicate id {entry_id!r}")
        else:
            seen_ids.append(entry_id)

        for key in ("owner", "revision", "rights"):
            if not entry.get(key):
                report.add(f"{loc}.{key}: required")

        revision = entry.get("revision")
        if isinstance(revision, str) and not re.fullmatch(r"[0-9a-f]{40}", revision):
            report.add(
                f"{loc}.revision: {revision!r} is not an immutable 40-hex commit; a "
                "branch name or bare tag is mutable and is not valid provenance"
            )

        rights = entry.get("rights")
        if rights is not None and rights not in RIGHTS_VALUES:
            report.add(f"{loc}.rights: {rights!r} is not one of {list(RIGHTS_VALUES)}")

        digest = entry.get("sha256")
        if digest is not None and not re.fullmatch(r"[0-9a-f]{64}", str(digest)):
            report.add(f"{loc}.sha256: must be 64 lowercase hex characters")

        consumers = entry.get("consumers")
        if not isinstance(consumers, Sequence) or isinstance(consumers, (str, bytes)) or not consumers:
            report.add(f"{loc}.consumers: at least one named consumer is required")

        if "repository" not in entry and "url" not in entry:
            report.add(f"{loc}: needs a 'repository' or immutable object 'url'")

    return report
