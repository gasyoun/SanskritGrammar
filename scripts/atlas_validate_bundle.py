#!/usr/bin/env python3
"""Validate a Sangram atlas bundle against the B1 data contract (H623).

Checks, in order:
  1. JSON Schema conformance (sangram/atlas/data/atlas.schema.json) when the
     `jsonschema` package is importable; otherwise a built-in structural
     subset (required keys, closed enums, id patterns, kind-specific fields).
  2. Referential integrity — every edge endpoint and every `owner`/`parent`
     reference resolves to an existing node id; node and edge ids are unique.
  3. Contract semantics — assessed items carry `as_of`; `status` only on
     assessed edges; internal evidence carries no URL; five views with
     unique ids; view node/edge kinds actually occur in the bundle.
  4. Private-data leakage — the serialized bundle contains no private hub
     URL, no local filesystem path, no volatile-registry pattern, and no
     node for a denylisted repo. Leakage must be exactly 0 to pass.

Usage:
  python scripts/atlas_validate_bundle.py sangram/atlas/data/atlas.bundle.json
  python scripts/atlas_validate_bundle.py --self-test

Exit 0 = valid; exit 1 = one or more violations (all printed).
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE.parent / "sangram" / "atlas" / "data" / "atlas.schema.json"
FIXTURE_PATH = HERE.parent / "sangram" / "atlas" / "data" / "atlas.fixture.json"

NODE_KINDS = {"thesis", "source-class", "repo", "asset", "external-stack", "stage", "surface"}
EDGE_KINDS = {"replenishes", "generates", "attests", "crosslinks", "fills",
              "feeds", "consumes", "vendors", "produces", "cites",
              "creates", "strengthens", "funds", "scales", "anchors", "owns"}
VIEW_IDS = {"attention", "reuse", "value-chain", "dependencies", "provenance"}
NODE_ID_RE = re.compile(r"^(thesis|class|repo|asset|ext|stage|surface):[a-z0-9][a-z0-9.-]*$")
EDGE_ID_RE = re.compile(r"^e:[a-z0-9][a-z0-9.:-]*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

REQUIRED_BY_KIND = {
    "thesis": ["section", "importance", "state", "scores", "verdict", "gates", "as_of"],
    "source-class": ["tier"],
    "repo": ["org", "name", "url"],
    "asset": ["asset_types", "owner", "prohibition_ru", "rights"],
    "stage": ["chain"],
}

DENYLISTED_REPO_NAMES = {
    "Uprava", "github-spine", "RuWritingStyles-corpus", "telegram-sanskrit-corpus",
    "Sundara-commentaries", "prefaces_ieg", "samskrutam-crossword",
}
LEAKAGE_PATTERNS = [
    "github.com/gasyoun/Uprava",
    "github.com/gasyoun/github-spine",
    "RuWritingStyles-corpus",
    "telegram-sanskrit-corpus",
    "C:/Users", "C:\\Users", "/home/", "Documents/GitHub",
    "GTD_NEXT_ACTIONS", "BOTTLENECKS.md", "NEXT_TASK_QUEUE",
    "@DECIDE", "@WAITING", ".claim",
    "\U0001f512",  # 🔒 — private-tier rows are dropped, never marked
]


def validate(bundle, serialized):
    errors = []
    err = errors.append

    # -- 1. schema ----------------------------------------------------------
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(schema)
        for v in validator.iter_errors(bundle):
            path = "/".join(str(p) for p in v.absolute_path)
            err(f"schema: {path or '<root>'}: {v.message[:200]}")
    except ImportError:
        for key in ["contract_version", "provenance", "nodes", "edges", "views"]:
            if key not in bundle:
                err(f"schema*: missing top-level key {key!r}")
        if not re.match(r"^\d+\.\d+\.\d+$", str(bundle.get("contract_version", ""))):
            err("schema*: contract_version is not semver")
        prov = bundle.get("provenance", {})
        for key in ["generated", "generator", "generated_by", "series_slot", "sources", "sanitisation"]:
            if key not in prov:
                err(f"schema*: provenance missing {key!r}")

    nodes = bundle.get("nodes", [])
    edges = bundle.get("edges", [])
    views = bundle.get("views", [])

    # -- built-in structural checks (always run; schema lib may be absent) --
    node_ids = {}
    for n in nodes:
        nid = n.get("id", "<missing>")
        if nid in node_ids:
            err(f"nodes: duplicate id {nid}")
        node_ids[nid] = n
        if not NODE_ID_RE.match(nid):
            err(f"nodes: bad id pattern {nid!r}")
        kind = n.get("kind")
        if kind not in NODE_KINDS:
            err(f"nodes: {nid}: unknown kind {kind!r}")
        if not n.get("label_ru"):
            err(f"nodes: {nid}: missing label_ru")
        if n.get("temperature") not in {"structural", "assessed"}:
            err(f"nodes: {nid}: temperature must be structural|assessed")
        for field in REQUIRED_BY_KIND.get(kind, []):
            if field not in n:
                err(f"nodes: {nid}: kind {kind} requires {field!r}")
        if n.get("temperature") == "assessed" and not DATE_RE.match(n.get("as_of", "")):
            err(f"nodes: {nid}: assessed node needs as_of date")

    edge_ids = set()
    for e in edges:
        eid = e.get("id", "<missing>")
        if eid in edge_ids:
            err(f"edges: duplicate id {eid}")
        edge_ids.add(eid)
        if not EDGE_ID_RE.match(eid):
            err(f"edges: bad id pattern {eid!r}")
        if e.get("kind") not in EDGE_KINDS:
            err(f"edges: {eid}: unknown kind {e.get('kind')!r}")
        if e.get("temperature") not in {"structural", "assessed"}:
            err(f"edges: {eid}: temperature must be structural|assessed")
        if e.get("temperature") == "assessed" and not DATE_RE.match(e.get("as_of", "")):
            err(f"edges: {eid}: assessed edge needs as_of date")
        if "status" in e:
            if e["status"] not in {"live", "queued", "proposed", "unverified"}:
                err(f"edges: {eid}: unknown status {e['status']!r}")
            if e.get("temperature") != "assessed":
                err(f"edges: {eid}: status implies temperature=assessed")

    # -- 2. referential integrity -------------------------------------------
    for e in edges:
        for endpoint in ("source", "target"):
            ref = e.get(endpoint)
            if ref not in node_ids:
                err(f"integrity: edge {e.get('id')}: {endpoint} {ref!r} is not a node")
    for n in nodes:
        for ref_field in ("owner", "parent"):
            if ref_field in n and n[ref_field] not in node_ids:
                err(f"integrity: node {n['id']}: {ref_field} {n[ref_field]!r} is not a node")

    # -- 3. contract semantics ----------------------------------------------
    def check_evidence(holder, where):
        ev = holder.get("evidence")
        if ev is None:
            return
        if ev.get("visibility") not in {"public", "internal"}:
            err(f"evidence: {where}: visibility must be public|internal")
        if not ev.get("label_ru"):
            err(f"evidence: {where}: missing label_ru")
        if ev.get("visibility") == "internal" and "url" in ev:
            err(f"evidence: {where}: internal evidence must not carry a URL")
        if ev.get("visibility") == "public" and not str(ev.get("url", "")).startswith("https://"):
            err(f"evidence: {where}: public evidence needs an https URL")

    for n in nodes:
        check_evidence(n, f"node {n.get('id')}")
    for e in edges:
        check_evidence(e, f"edge {e.get('id')}")

    seen_views = set()
    node_kinds_present = {n.get("kind") for n in nodes}
    edge_kinds_present = {e.get("kind") for e in edges}
    for v in views:
        vid = v.get("id")
        if vid not in VIEW_IDS:
            err(f"views: unknown view id {vid!r}")
        if vid in seen_views:
            err(f"views: duplicate view id {vid}")
        seen_views.add(vid)
        for kind in v.get("node_kinds", []):
            if kind not in node_kinds_present:
                err(f"views: {vid}: node_kind {kind!r} has no nodes in the bundle")
        for kind in v.get("edge_kinds", []):
            if kind not in edge_kinds_present:
                err(f"views: {vid}: edge_kind {kind!r} has no edges in the bundle")
    if seen_views != VIEW_IDS:
        err(f"views: expected exactly {sorted(VIEW_IDS)}, got {sorted(seen_views)}")

    # -- 4. leakage -----------------------------------------------------------
    for pattern in LEAKAGE_PATTERNS:
        if pattern in serialized:
            err(f"LEAKAGE: banned pattern present: {pattern!r}")
    for n in nodes:
        if n.get("kind") == "repo" and n.get("name") in DENYLISTED_REPO_NAMES:
            err(f"LEAKAGE: denylisted repo node present: {n['name']}")

    return errors


def run_file(path):
    serialized = Path(path).read_text(encoding="utf-8")
    bundle = json.loads(serialized)
    errors = validate(bundle, serialized)
    if errors:
        print(f"INVALID: {path} — {len(errors)} violation(s)")
        for e in errors:
            print(f"  - {e}")
        return 1
    prov = bundle["provenance"]
    print(f"VALID: {path} — {len(bundle['nodes'])} nodes, {len(bundle['edges'])} edges, "
          f"{len(bundle['views'])} views; generated {prov['generated']} by {prov['generated_by']}; "
          f"leakage=0")
    return 0


def self_test():
    """Fixture must pass; four deliberately broken variants must each fail."""
    serialized = FIXTURE_PATH.read_text(encoding="utf-8")
    fixture = json.loads(serialized)
    failures = []

    if validate(fixture, serialized):
        failures.append("fixture unexpectedly INVALID:\n  " +
                        "\n  ".join(validate(fixture, serialized)))

    def broken(mutate, name, expect_substr):
        b = json.loads(serialized)
        mutate(b)
        s = json.dumps(b, ensure_ascii=False)
        errs = validate(b, s)
        if not any(expect_substr in e for e in errs):
            failures.append(f"negative case {name!r}: expected a violation containing "
                            f"{expect_substr!r}, got {errs or 'none'}")

    broken(lambda b: b["edges"][0].update(target="repo:does-not-exist"),
           "dangling-edge", "is not a node")
    broken(lambda b: b["nodes"][0].update(kind="banana"),
           "bad-kind", "unknown kind")
    broken(lambda b: b["nodes"][0].setdefault("evidence", {"label_ru": "x", "visibility": "internal"}).update(
               url="https://github.com/gasyoun/kosha"),
           "internal-with-url", "must not carry a URL")
    broken(lambda b: b["nodes"][0].update(label_ru="см. GTD_NEXT_ACTIONS.md строку 5"),
           "leakage", "banned pattern")

    if failures:
        print("SELF-TEST FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("SELF-TEST OK: fixture valid; 4 negative cases correctly rejected")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("bundle", nargs="?", help="path to a bundle JSON")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        sys.exit(self_test())
    if not args.bundle:
        ap.error("bundle path required unless --self-test")
    sys.exit(run_file(args.bundle))


if __name__ == "__main__":
    main()
