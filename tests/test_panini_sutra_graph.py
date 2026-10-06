"""H6056 — tests for tools/panini_sutra_graph.py (offline; no network).

Three layers:
  1. unit tests over a synthetic mini-dataset with a hand-computable graph
     (parsing, edge extraction, transitive reduction, layers, cycle refusal);
  2. committed-artifact invariant tests over data/panini_sutra_graph/
     (acyclicity, layer invariant, artifact consistency — the on-our-data
     canary, runs without the source cache);
  3. a full-rebuild regression canary, skipped unless the shared
     panini_cache/data.txt is present (no network in CI).
"""
from __future__ import annotations

import importlib.util
import json
import os
from collections import defaultdict

import pytest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(REPO, "tools", "panini_sutra_graph.py")
OUT_DIR = os.path.join(REPO, "data", "panini_sutra_graph")
CACHE = os.path.join(
    REPO, "GasunsDhatu_2014", "revision-2026", "panini_cache", "data.txt"
)

spec = importlib.util.spec_from_file_location("psg", TOOL)
assert spec is not None and spec.loader is not None
psg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(psg)


# --------------------------------------------------------------------- fixtures

MINI = {
    "name": "mini",
    "data": [
        # 1.1.1 adhikara governs 1.1.3 (immediately) and 1.1.4 (flattened)
        {"i": "11001", "a": "1", "p": "1", "n": "1", "s": "अ", "e": "a",
         "an": "", "ad": ""},
        {"i": "11002", "a": "1", "p": "1", "n": "2", "s": "ब", "e": "b",
         "an": "", "ad": ""},
        {"i": "11003", "a": "1", "p": "1", "n": "3", "s": "क", "e": "k",
         "an": "अ$11001", "ad": "अ$1$1$1"},
        # 1.1.4: continues from 1.1.1 (flattened via 1.1.3) and governed by
        # adhikara 1.1.3 itself; also continues word from 1.1.2
        {"i": "11004", "a": "1", "p": "1", "n": "4", "s": "द", "e": "d",
         "an": "अ$11001##क$11003##ब$11002", "ad": "अ$1$1$1##क$1$1$3"},
        # 1.1.5: depends only on 1.1.4
        {"i": "11005", "a": "1", "p": "1", "n": "5", "s": "ए", "e": "e",
         "an": "द$11004", "ad": ""},
    ],
}


@pytest.fixture()
def mini_graph():
    nodes = psg.parse_nodes(json.dumps(MINI))
    raw_typed, stats = psg.build_raw_edges(nodes)
    raw = psg.untyped(raw_typed)
    reduced, _ = psg.transitive_reduction(nodes, raw)
    layer = psg.layers(nodes, reduced)
    return nodes, raw_typed, raw, reduced, layer, stats


# ----------------------------------------------------------------- unit tests

def test_parse_nodes(mini_graph):
    nodes = mini_graph[0]
    assert len(nodes) == 5
    assert nodes["11001"]["ref"] == "1.1.1"


def test_edge_extraction(mini_graph):
    raw_typed, stats = mini_graph[1], mini_graph[5]
    assert stats["dangling_an"] == 0 and stats["dangling_ad"] == 0
    # 1.1.4 -> {1.1.1 (an+ad, flattened), 1.1.3 (an+ad), 1.1.2 (an)}: 5 typed edges
    into4 = {(y, r) for y, x, r in raw_typed if x == "11004"}
    assert into4 == {
        ("11001", "anuvritti"),
        ("11001", "adhikara"),
        ("11002", "anuvritti"),
        ("11003", "anuvritti"),
        ("11003", "adhikara"),
    }


def test_transitive_reduction(mini_graph):
    raw, reduced = mini_graph[2], mini_graph[3]
    # flattened edge 1.1.1 -> 1.1.4 is redundant (1.1.1 -> 1.1.3 -> 1.1.4)
    assert ("11001", "11004") in raw
    assert ("11001", "11004") not in reduced
    # immediate chains survive
    assert ("11001", "11003") in reduced
    assert ("11003", "11004") in reduced
    assert ("11004", "11005") in reduced


def test_layers_and_invariant(mini_graph):
    reduced, layer = mini_graph[3], mini_graph[4]
    assert layer["11001"] == 1 and layer["11002"] == 1
    assert layer["11003"] == 2
    assert layer["11004"] == 3
    assert layer["11005"] == 4
    for y, x in reduced:
        assert layer[y] < layer[x]


def test_cycle_refused():
    nodes = psg.parse_nodes(json.dumps({
        "data": [
            {"i": "11001", "a": "1", "p": "1", "n": "1", "s": "अ", "e": "a",
             "an": "", "ad": ""},
            # 1.1.2 continues from a LATER sūtra 1.1.3 — a back-edge/cycle
            {"i": "11002", "a": "1", "p": "1", "n": "2", "s": "ब", "e": "b",
             "an": "क$11003", "ad": ""},
            {"i": "11003", "a": "1", "p": "1", "n": "3", "s": "क", "e": "k",
             "an": "ब$11002", "ad": ""},
        ]
    }))
    edges, _ = psg.build_raw_edges(nodes)
    assert psg.topo_order(nodes, psg.untyped(edges)) is None
    with pytest.raises(SystemExit):
        psg.transitive_reduction(nodes, psg.untyped(edges))


# ------------------------------------------------- committed-artifact canary

def test_committed_artifacts_present():
    for fname in ("graph.json", "edges.tsv", "edges_full.tsv",
                  "study_order.tsv", "README.md"):
        assert os.path.exists(os.path.join(OUT_DIR, fname)), fname


def test_committed_graph_invariants():
    with open(os.path.join(OUT_DIR, "graph.json"), encoding="utf-8") as f:
        g = json.load(f)
    nodes = {n["id"]: n for n in g["nodes"]}
    layer = {n["id"]: n["layer"] for n in g["nodes"]}
    assert len(nodes) == len(g["nodes"]), "duplicate node ids"
    reduced = {(e["src"], e["dst"]) for e in g["edges_reduced"]}
    assert reduced, "reduced edge set empty"
    # acyclic
    assert psg.topo_order(nodes, reduced) is not None, "committed graph cyclic"
    # layer invariant: prerequisites strictly earlier
    for y, x in reduced:
        assert layer[y] < layer[x], f"layer invariant violated {y}->{x}"
    # layer values = 1 + max(pred layers)
    preds = defaultdict(list)
    for y, x in reduced:
        preds[x].append(y)
    for v, ps in preds.items():
        assert layer[v] == 1 + max(layer[p] for p in ps)
    # meta sanity: forward-only uttara-pūrva on the raw typed encoding
    meta = g["meta"]
    assert meta["nodes"] == len(nodes)
    assert meta["stats"]["dangling_an"] == 0
    assert meta["stats"]["dangling_ad"] == 0


def test_committed_study_order_matches_graph():
    with open(os.path.join(OUT_DIR, "graph.json"), encoding="utf-8") as f:
        g = json.load(f)
    by_ref = {n["ref"]: n for n in g["nodes"]}
    prev_key = (0, 0)
    with open(os.path.join(OUT_DIR, "study_order.tsv"), encoding="utf-8") as f:
        rows = f.read().splitlines()[1:]
    assert len(rows) == len(g["nodes"])
    for line in rows:
        seq, lay, ref = line.split("\t")[:3]
        assert (int(lay), int(seq)) > prev_key, "not ordered by (layer, seq)"
        prev_key = (int(lay), int(seq))
        assert by_ref[ref]["layer"] == int(lay), f"layer mismatch at {ref}"


# ----------------------------------------------------- full rebuild (cached)

@pytest.mark.skipif(not os.path.exists(CACHE), reason="panini_cache/data.txt absent")
def test_full_rebuild_reproduces_committed_counts():
    with open(CACHE, encoding="utf-8") as f:
        text = f.read()
    nodes = psg.parse_nodes(text)
    raw_typed, stats = psg.build_raw_edges(nodes)
    raw = psg.untyped(raw_typed)
    reduced, _ = psg.transitive_reduction(nodes, raw)
    layer = psg.layers(nodes, reduced)
    with open(os.path.join(OUT_DIR, "graph.json"), encoding="utf-8") as f:
        committed = json.load(f)
    m = committed["meta"]
    assert len(nodes) == m["nodes"]
    assert len(raw_typed) == m["raw_edges"]
    assert len(reduced) == m["reduced_edges"]
    assert max(layer.values()) == committed["metrics"]["max_layer"]
    assert stats["dangling_an"] + stats["dangling_ad"] == 0
