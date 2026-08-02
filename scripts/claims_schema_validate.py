#!/usr/bin/env python3
"""Validate grammar claim registers (*/claims.yml) against claims.schema.json (H1842).

Structural twin of scripts/article_validate.py for the six book claim registers.
Enums and required keys are taken verbatim from each claims.yml header
(verdict_fact / verdict_pedagogy / kind) — no invented categories.

Checks:
  1. JSON Schema conformance (sangram/editorial/data/claims.schema.json) when
     the `jsonschema` package is importable; otherwise a built-in structural
     subset (required keys, closed enums).
  2. YAML TRUE/FALSE booleans (unquoted TRUE/FALSE) are coerced to the string
     verdict vocabulary before schema validation — same rule as build_claims.norm_fact.
  3. Entry ids unique within a file.

Usage:
  python scripts/claims_schema_validate.py KocherginaUchebnik_1998/claims.yml
  python scripts/claims_schema_validate.py --all
  python scripts/claims_schema_validate.py --self-test

Exit 0 = valid; exit 1 = one or more violations (all printed).
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SCHEMA_PATH = ROOT / "sangram" / "editorial" / "data" / "claims.schema.json"

VERDICT_FACT = {"TRUE", "OVERSTATED", "FALSE", "UNTESTABLE", "PENDING"}
VERDICT_PEDAGOGY = {
    "JUSTIFIED", "MISLEADING", "RARE-AS-CENTRAL", "FREQUENCY-HIDDEN", "ORDER-QUESTIONABLE",
}
KINDS = {"typology", "universality", "allomorphy", "statistic", "rule", "government"}
ENTRY_REQUIRED = ("id", "loc", "claim_ru", "kind", "verdict_fact", "verdict_pedagogy")
ENTRY_OPTIONAL = (
    "falsifiable_as", "sources", "number", "ref", "note", "mg_footnote", "methodichka",
)
ENTRY_ALLOWED = set(ENTRY_REQUIRED) | set(ENTRY_OPTIONAL)
TOP_ALLOWED = {"work", "synthesis", "entries"}


def norm_fact(v):
    """YAML reads unquoted TRUE/FALSE as booleans — coerce back to the verdict vocabulary."""
    if v is True:
        return "TRUE"
    if v is False:
        return "FALSE"
    return v


def normalize_register(data: dict) -> dict:
    """Deep-copy and coerce entry.verdict_fact booleans to strings for schema validation.

    Does not invent missing keys — a register without ``entries`` must still fail
    the schema's required-key check.
    """
    out = copy.deepcopy(data) if data else {}
    entries = out.get("entries")
    if isinstance(entries, list):
        for e in entries:
            if isinstance(e, dict) and "verdict_fact" in e:
                e["verdict_fact"] = norm_fact(e.get("verdict_fact"))
    return out


def discover_claims_files() -> list[Path]:
    return sorted(ROOT.glob("*/claims.yml"))


def _builtin_schema_subset(data: dict, err) -> None:
    """Structural subset used when `jsonschema` is unavailable."""
    if not isinstance(data, dict):
        err("root must be a mapping")
        return
    unknown_top = set(data) - TOP_ALLOWED
    if unknown_top:
        err(f"unknown top-level keys: {sorted(unknown_top)}")
    if not isinstance(data.get("work"), str) or not data.get("work"):
        err("work must be a non-empty string")
    if "synthesis" in data and data["synthesis"] is not None and not isinstance(data["synthesis"], str):
        err("synthesis must be a string when present")
    entries = data.get("entries")
    if not isinstance(entries, list):
        err("entries must be an array")
        return
    for i, e in enumerate(entries):
        prefix = f"entries[{i}]"
        if not isinstance(e, dict):
            err(f"{prefix}: must be an object")
            continue
        unknown = set(e) - ENTRY_ALLOWED
        if unknown:
            err(f"{prefix}: unknown keys {sorted(unknown)}")
        for key in ENTRY_REQUIRED:
            val = e.get(key)
            if val is None or val == "":
                err(f"{prefix}.{key} missing")
        kind = e.get("kind")
        if kind is not None and kind not in KINDS:
            err(f"{prefix}.kind {kind!r} not in {sorted(KINDS)}")
        vf = norm_fact(e.get("verdict_fact"))
        if vf is not None and vf not in VERDICT_FACT:
            err(f"{prefix}.verdict_fact {vf!r} not in {sorted(VERDICT_FACT)}")
        vp = e.get("verdict_pedagogy")
        if vp is not None and vp not in VERDICT_PEDAGOGY:
            err(f"{prefix}.verdict_pedagogy {vp!r} not in {sorted(VERDICT_PEDAGOGY)}")
        if "sources" in e and e["sources"] is not None:
            if not isinstance(e["sources"], list) or not all(
                isinstance(s, str) and s for s in e["sources"]
            ):
                err(f"{prefix}.sources must be an array of non-empty strings")


def validate(data: dict) -> list[str]:
    """Return a list of error strings (empty = pass)."""
    errors: list[str] = []
    err = errors.append
    if not isinstance(data, dict):
        return ["root must be a mapping"]

    normalized = normalize_register(data)

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(schema)
        for v in validator.iter_errors(normalized):
            path = "/".join(str(p) for p in v.absolute_path)
            err(f"schema: {path or '<root>'}: {v.message}")
    except ImportError:
        _builtin_schema_subset(normalized, err)

    # Semantic: unique ids within the file
    seen: dict[str, int] = {}
    for i, e in enumerate(normalized.get("entries") or []):
        if not isinstance(e, dict):
            continue
        cid = e.get("id")
        if not isinstance(cid, str) or not cid:
            continue
        if cid in seen:
            err(f"entries[{i}].id {cid!r} duplicates entries[{seen[cid]}].id")
        else:
            seen[cid] = i

    return errors


def run_file(path: Path) -> int:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (yaml.YAMLError, OSError) as e:
        print(f"ERROR {path}: unreadable YAML ({e})")
        return 1
    if raw is None:
        raw = {}
    errors = validate(raw if isinstance(raw, dict) else {"_bad": raw})
    for e in errors:
        print(f"ERROR {path.name}: {e}")
    n = len((raw or {}).get("entries") or []) if isinstance(raw, dict) else 0
    print(f"{'PASS' if not errors else 'FAIL'}  {path}: "
          f"{n} entries, {len(errors)} error(s)")
    return 0 if not errors else 1


def minimal_fixture() -> dict:
    return {
        "work": "Fixture Grammar (0000)",
        "synthesis": "Synthetic register for self-test only.",
        "entries": [
            {
                "id": "FX-1",
                "loc": "§1",
                "claim_ru": "A synthetic universal for schema self-test.",
                "kind": "universality",
                "verdict_fact": "TRUE",
                "verdict_pedagogy": "JUSTIFIED",
                "sources": ["dcs"],
            }
        ],
    }


def self_test() -> int:
    """Minimal fixture must pass; characteristic mutations must each fail."""
    failures: list[str] = []
    fixture = minimal_fixture()
    if validate(fixture):
        failures.append(f"fixture should pass but got: {validate(fixture)}")

    def mutated(mutate) -> list[str]:
        m = copy.deepcopy(fixture)
        mutate(m)
        return validate(m)

    cases = {
        "missing work": lambda m: m.pop("work"),
        "missing entries": lambda m: m.pop("entries"),
        "unknown top-level key": lambda m: m.__setitem__("invented_field", True),
        "entry missing id": lambda m: m["entries"][0].pop("id"),
        "entry missing claim_ru": lambda m: m["entries"][0].pop("claim_ru"),
        "bad verdict_fact": lambda m: m["entries"][0].__setitem__("verdict_fact", "MAYBE"),
        "bad verdict_pedagogy": lambda m: m["entries"][0].__setitem__(
            "verdict_pedagogy", "FINE"),
        "bad kind": lambda m: m["entries"][0].__setitem__("kind", "opinion"),
        "unknown entry key": lambda m: m["entries"][0].__setitem__("invented", 1),
        "duplicate id": lambda m: m["entries"].append(copy.deepcopy(m["entries"][0])),
        "boolean TRUE coerces and passes": None,  # positive case handled below
    }
    for name, mutate in cases.items():
        if mutate is None:
            continue
        if not mutated(mutate):
            failures.append(f"mutation {name!r} should fail but passed")

    # Positive: YAML-style boolean TRUE/FALSE must coerce, not fail
    m = copy.deepcopy(fixture)
    m["entries"][0]["verdict_fact"] = True
    if validate(m):
        failures.append(f"boolean TRUE verdict_fact should coerce/pass, got: {validate(m)}")
    m2 = copy.deepcopy(fixture)
    m2["entries"][0]["verdict_fact"] = False
    if validate(m2):
        failures.append(f"boolean FALSE verdict_fact should coerce/pass, got: {validate(m2)}")

    for f in failures:
        print(f"SELF-TEST FAIL: {f}")
    total = len([k for k, v in cases.items() if v is not None]) + 1 + 2  # fixture + 2 coerce
    print(f"{'PASS' if not failures else 'FAIL'}  self-test: "
          f"{total - len(failures)}/{total} checks green")
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("path", nargs="?", help="path to a claims.yml file")
    ap.add_argument("--all", action="store_true",
                    help="validate every */claims.yml under the repo root")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if args.all:
        targets = discover_claims_files()
        if not targets:
            print("ERROR: no */claims.yml files found", file=sys.stderr)
            return 1
        return max((run_file(p) for p in targets), default=0)
    if not args.path:
        ap.error("give a claims.yml path, --all, or --self-test")
    return run_file(Path(args.path))


if __name__ == "__main__":
    sys.exit(main())
