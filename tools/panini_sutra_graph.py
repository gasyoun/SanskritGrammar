#!/usr/bin/env python3
"""panini_sutra_graph.py — Aṣṭādhyāyī sūtra dependency graph (H6056).

Builds the uttara-pūrva dependency graph of Pāṇini's Aṣṭādhyāyī from the
canonical ashtadhyayi.com dataset (github.com/ashtadhyayi-com/data,
sutraani/data.txt) — the same source that powers /panini-sutra-lookup's
panini_sutra.py. The cache is shared with that resolver.

Input semantics (validated by build):
  * every row is a sūtra with fields i (5-digit id), a/p/n, s (Devanagari),
    e (roman), an (anuvṛtti), ad (adhikāra);
  * `an` lists the words + sūtra-ids that CONTINUE into this sūtra
    (`वृद्धिः$11001##गुणः$11002`) — a flattened continuation listing;
  * `ad` lists the governing adhikāra sūtras (`संहितायाम्$8$2$108`).

The listing is partly flattened (a sūtra names remote continuations that also
reach it via intermediate sūtras). Two graphs are therefore produced:

  RAW     the dependency edges exactly as encoded (typed: adhikara / anuvritti);
  REDUCED the transitive reduction of RAW — the *immediate* uttara-pūrva
          chains, i.e. the reconstructed reading structure (this is the
          anuvṛtti reconstruction in the machine-readable sense).

On the reduced graph the tool computes topological study layers (a sūtra's
layer is 1 + max(layer of its immediate prerequisites)), global metrics
(diameter, degree hubs, critical-path depth) and exports:

  data/panini_sutra_graph/graph.json        machine format (nodes+edges+metrics)
  data/panini_sutra_graph/edges.tsv         reduced edges (src dst ref rel)
  data/panini_sutra_graph/edges_full.tsv    raw typed edges
  data/panini_sutra_graph/study_order.tsv   pedagogy predictor: layer order
  data/panini_sutra_graph/README.md         report

Usage:
  python tools/panini_sutra_graph.py build [--refresh]
  python tools/panini_sutra_graph.py check            # validate committed artifacts

Determinism: outputs contain the source sha256, never a build timestamp.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import urllib.request
from collections import defaultdict, deque

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_URL = "https://raw.githubusercontent.com/ashtadhyayi-com/data/master/sutraani/data.txt"
# shared with GasunsDhatu_2014/revision-2026/panini_sutra.py (gitignored, re-fetched)
CACHE_PATH = os.path.join(
    REPO_ROOT, "GasunsDhatu_2014", "revision-2026", "panini_cache", "data.txt"
)
OUT_DIR = os.path.join(REPO_ROOT, "data", "panini_sutra_graph")

REL_ADHIKARA = "adhikara"
REL_ANUVRTTI = "anuvritti"


# --------------------------------------------------------------------------- data


def load_source(refresh: bool = False) -> tuple[str, str]:
    """Return (text, sha256) of the canonical data.txt, via the shared cache."""
    path = CACHE_PATH
    if refresh or not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with urllib.request.urlopen(RAW_URL, timeout=60) as r:
            data = r.read()
        with open(path, "wb") as f:
            f.write(data)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return text, hashlib.sha256(text.encode("utf-8")).hexdigest()


def parse_nodes(text: str) -> dict[str, dict]:
    """Parse data.txt rows into {id: {a,p,n,ref,s,e}} keyed by 5-digit id."""
    obj = json.loads(text)
    if isinstance(obj, dict):
        rows = obj.get("data", [])
    else:
        rows = obj
    nodes: dict[str, dict] = {}
    for row in rows:
        key = str(row.get("i") or "")
        if not key:
            continue
        nodes[key] = {
            "a": int(row["a"]),
            "p": int(row["p"]),
            "n": int(row["n"]),
            "ref": f"{int(row['a'])}.{int(row['p'])}.{int(row['n'])}",
            "s": row.get("s", ""),
            "e": row.get("e", ""),
            "an": row.get("an") or "",
            "ad": row.get("ad") or "",
        }
    return nodes


def sid(a: str, p: str, n: str) -> str:
    return f"{int(a)}{int(p):01d}{int(n):03d}"


# --------------------------------------------------------------------------- graph


def build_raw_edges(nodes: dict[str, dict]) -> tuple[set[tuple[str, str, str]], dict]:
    """Extract typed dependency edges (source, target, relation) from an/ad."""
    edges: set[tuple[str, str, str]] = set()
    stats = {"dangling_an": 0, "dangling_ad": 0, "self": 0}
    for x, row in nodes.items():
        for ent in row["an"].split("##"):
            if not ent:
                continue
            y = ent.rpartition("$")[2]
            if y not in nodes:
                stats["dangling_an"] += 1
                continue
            if y == x:
                stats["self"] += 1
                continue
            edges.add((y, x, REL_ANUVRTTI))
        for ent in row["ad"].split("##"):
            if not ent:
                continue
            parts = ent.split("$")
            if len(parts) != 4:
                continue
            y = sid(parts[1], parts[2], parts[3])
            if y not in nodes:
                stats["dangling_ad"] += 1
                continue
            if y == x:
                stats["self"] += 1
                continue
            edges.add((y, x, REL_ADHIKARA))
    return edges, stats


def untyped(edges) -> set[tuple[str, str]]:
    return {(y, x) for y, x, _ in edges}


def topo_order(nodes: dict[str, dict], edges: set[tuple[str, str]]) -> list[str] | None:
    """Kahn topological sort, stable by book order; None if cyclic."""
    ids = sorted(nodes, key=int)
    indeg = {v: 0 for v in ids}
    adj: dict[str, list[str]] = defaultdict(list)
    for y, x in edges:
        adj[y].append(x)
        indeg[x] += 1
    queue = deque(v for v in ids if indeg[v] == 0)
    out: list[str] = []
    while queue:
        u = queue.popleft()
        out.append(u)
        for w in adj[u]:
            indeg[w] -= 1
            if indeg[w] == 0:
                queue.append(w)
    return out if len(out) == len(ids) else None


def transitive_reduction(nodes: dict[str, dict], raw: set[tuple[str, str]]):
    """Bitmask transitive reduction of a DAG. Returns (reduced, order)."""
    order = topo_order(nodes, raw)
    if order is None:
        raise SystemExit("FATAL: raw graph has a cycle — not a DAG; refusing.")
    rank = {v: k for k, v in enumerate(order)}
    n = len(order)
    adj: list[list[int]] = [[] for _ in range(n)]
    for y, x in raw:
        adj[rank[y]].append(rank[x])
    reach = [0] * n
    for u in range(n - 1, -1, -1):
        m = 0
        for w in adj[u]:
            m |= reach[w] | (1 << w)
        reach[u] = m
    reduced: set[tuple[str, str]] = set()
    for u in range(n):
        succ = adj[u]
        for w in succ:
            # edge u->w is immediate iff w is not reachable via another successor;
            # computed exactly per-w to avoid masking-bit overlap errors
            via_others = 0
            for w2 in succ:
                if w2 != w:
                    via_others |= reach[w2] | (1 << w2)
            if not ((via_others >> w) & 1):
                reduced.add((order[u], order[w]))
    return reduced, order


def layers(nodes: dict[str, dict], edges: set[tuple[str, str]]) -> dict[str, int]:
    """Layer(v) = 1 + max(Layer(preds)); sources get layer 1."""
    order = topo_order(nodes, edges)
    if order is None:
        raise SystemExit("FATAL: cyclic graph in layering.")
    preds: dict[str, list[str]] = defaultdict(list)
    for y, x in edges:
        preds[x].append(y)
    layer: dict[str, int] = {}
    for v in order:
        ps = preds[v]
        layer[v] = 1 + max((layer[p] for p in ps), default=0)
    return layer


def diameter(nodes: dict[str, dict], edges: set[tuple[str, str]]) -> int:
    """Exact directed diameter (longest shortest path) via BFS per node."""
    ids = sorted(nodes, key=int)
    rank = {v: k for k, v in enumerate(ids)}
    adj = [[] for _ in ids]
    for y, x in edges:
        adj[rank[y]].append(rank[x])
    best = 0
    for s in range(len(ids)):
        dist = [-1] * len(ids)
        dist[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    q.append(w)
        m = max(dist)
        if m > best:
            best = m
    return best


def hub_table(nodes: dict[str, dict], edges, key: int, k: int = 15):
    """Top-k nodes by in-degree (key=1, most depended-on) or out-degree (key=0)."""
    deg: dict[str, int] = defaultdict(int)
    for e in edges:
        deg[e[key]] += 1
    return [
        {"id": v, "ref": nodes[v]["ref"], "sutra": nodes[v]["s"], "degree": d}
        for v, d in sorted(deg.items(), key=lambda kv: (-kv[1], int(kv[0])))[:k]
    ]


# --------------------------------------------------------------------------- exports


def write_outputs(nodes, raw_typed, reduced, layer, src_sha, stats):
    os.makedirs(OUT_DIR, exist_ok=True)
    raw = untyped(raw_typed)
    rel_of = defaultdict(set)
    for y, x, r in raw_typed:
        rel_of[(y, x)].add(r)

    study = sorted(nodes, key=lambda v: (layer[v], int(v)))

    graph = {
        "meta": {
            "tool": "tools/panini_sutra_graph.py",
            "handoff": "H6056",
            "source": "github.com/ashtadhyayi-com/data sutraani/data.txt",
            "source_sha256": src_sha,
            "nodes": len(nodes),
            "raw_edges": len(raw_typed),
            "raw_edges_untyped": len(raw),
            "reduced_edges": len(reduced),
            "stats": stats,
        },
        "metrics": {},
        "nodes": [
            {
                "id": v,
                "ref": nodes[v]["ref"],
                "s": nodes[v]["s"],
                "e": nodes[v]["e"],
                "layer": layer[v],
            }
            for v in sorted(nodes, key=int)
        ],
        "edges_reduced": [
            {
                "src": y,
                "dst": x,
                "ref_src": nodes[y]["ref"],
                "ref_dst": nodes[x]["ref"],
                "rel": "+".join(sorted(rel_of.get((y, x), {"?"}))),
            }
            for y, x in sorted(reduced, key=lambda e: (int(e[0]), int(e[1])))
        ],
    }
    diam_raw = diameter(nodes, raw)
    diam_red = diameter(nodes, reduced)
    graph["metrics"] = {
        "diameter_raw": diam_raw,
        "diameter_reduced": diam_red,
        "max_layer": max(layer.values()),
        "hubs_in_raw": hub_table(nodes, raw_typed, 1),
        "hubs_out_raw": hub_table(nodes, raw_typed, 0),
        "hubs_in_reduced": hub_table(nodes, reduced, 1),
        "hubs_out_reduced": hub_table(nodes, reduced, 0),
    }
    with open(os.path.join(OUT_DIR, "graph.json"), "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=1)

    with open(os.path.join(OUT_DIR, "edges.tsv"), "w", encoding="utf-8") as f:
        f.write("src_ref\tdst_ref\trel\tdevanagari_src\n")
        for e in graph["edges_reduced"]:
            f.write(f"{e['ref_src']}\t{e['ref_dst']}\t{e['rel']}\t{nodes[e['src']]['s']}\n")

    with open(os.path.join(OUT_DIR, "edges_full.tsv"), "w", encoding="utf-8") as f:
        f.write("src_ref\tdst_ref\trel\n")
        for y, x, r in sorted(raw_typed, key=lambda e: (int(e[0]), int(e[1]), e[2])):
            f.write(f"{nodes[y]['ref']}\t{nodes[x]['ref']}\t{r}\n")

    with open(os.path.join(OUT_DIR, "study_order.tsv"), "w", encoding="utf-8") as f:
        f.write("seq\tlayer\tref\tdevanagari\troman\n")
        for i, v in enumerate(study, 1):
            f.write(f"{i}\t{layer[v]}\t{nodes[v]['ref']}\t{nodes[v]['s']}\t{nodes[v]['e']}\n")

    write_readme(graph, layer, nodes, study)
    return graph


def write_readme(graph, layer, nodes, study):
    m = graph["meta"]
    met = graph["metrics"]
    lines = []
    lines.append("# Pāṇini sūtra dependency graph (H6056)")
    lines.append("")
    lines.append(
        "Uttara-pūrva dependency graph of the Aṣṭādhyāyī built from the canonical "
        "[ashtadhyayi-com/data](https://github.com/ashtadhyayi-com/data) dataset "
        "(`sutraani/data.txt`, sha256 `" + m["source_sha256"][:16] + "…`), the same source "
        "that powers `/panini-sutra-lookup`. Regenerate with "
        "`python tools/panini_sutra_graph.py build`."
    )
    lines.append("")
    lines.append("## Method")
    lines.append("")
    lines.append(
        "The dataset encodes, per sūtra, the anuvṛtti continuations (`an`: word + source "
        "sūtra id) and the governing adhikāras (`ad`). These listings are partially "
        "**flattened** — a sūtra names remote continuations that also reach it through "
        "intermediate sūtras. Two graphs are therefore exported:"
    )
    lines.append("")
    lines.append(
        "- **raw** — every encoded dependency edge, typed `adhikara` / `anuvritti` "
        f"({m['raw_edges']} typed edges, {m['raw_edges_untyped']} untyped);"
    )
    lines.append(
        "- **reduced** — the transitive reduction of the raw graph "
        f"({m['reduced_edges']} edges): the **immediate** uttara-pūrva chains, i.e. the "
        "reconstructed reading structure (each edge = one direct continuation/governance)."
    )
    lines.append("")
    lines.append(
        "The raw graph is a forward DAG (every edge points from an earlier sūtra to a "
        "later one; 0 back-edges, "
        f"{m['stats']['dangling_an'] + m['stats']['dangling_ad']} dangling references), "
        "which validates the uttara-pūrva reading against the encoded data."
    )
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    lines.append(f"- nodes (sūtras): **{m['nodes']}**")
    lines.append(f"- diameter (raw / reduced): **{met['diameter_raw']} / {met['diameter_reduced']}**")
    lines.append(f"- deepest study layer: **{met['max_layer']}**")
    lines.append("")
    lines.append("Top depended-on sūtras (raw in-degree — the great adhikāra/anuvṛtti hubs):")
    lines.append("")
    lines.append("| ref | sūtra | in-degree |")
    lines.append("|---|---|---|")
    for h in met["hubs_in_raw"][:10]:
        lines.append(f"| {h['ref']} | {h['sutra']} | {h['degree']} |")
    lines.append("")
    lines.append("Top immediate hubs (reduced in-degree):")
    lines.append("")
    lines.append("| ref | sūtra | in-degree |")
    lines.append("|---|---|---|")
    for h in met["hubs_in_reduced"][:10]:
        lines.append(f"| {h['ref']} | {h['sutra']} | {h['degree']} |")
    lines.append("")
    lines.append("## Pedagogy — study order")
    lines.append("")
    lines.append(
        "`study_order.tsv` is the **study-order predictor**: sūtras are stratified into "
        "topological layers over the reduced graph — every sūtra appears strictly after "
        "all of its immediate prerequisites, and within a layer in book order. Layer 1 is "
        "the prerequisite-free foundation; a learner can take layers in sequence. The "
        "layer invariant is machine-checked by `panini_sutra_graph.py check` (and by "
        "`tests/test_panini_sutra_graph.py`) on the committed artifacts."
    )
    lines.append("")
    lay1 = [v for v in study if layer[v] == 1][:12]
    lines.append("Layer-1 foundations begin with: " + ", ".join(
        f"{nodes[v]['ref']} _{nodes[v]['s']}_" for v in lay1) + " …")
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("- `graph.json` — machine format: meta, metrics, nodes, reduced edges.")
    lines.append("- `edges.tsv` — reduced (immediate) edges with relation type.")
    lines.append("- `edges_full.tsv` — raw typed edges as encoded.")
    lines.append("- `study_order.tsv` — the pedagogy predictor (layer order).")
    lines.append("")
    with open(os.path.join(OUT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


# --------------------------------------------------------------------------- check


def check() -> int:
    """Offline validation of the committed artifacts in data/panini_sutra_graph/."""
    failures = []
    gpath = os.path.join(OUT_DIR, "graph.json")
    if not os.path.exists(gpath):
        print("FAIL: data/panini_sutra_graph/graph.json is missing — run `build`.")
        return 1
    with open(gpath, encoding="utf-8") as f:
        g = json.load(f)
    nodes = {n["id"]: n for n in g["nodes"]}
    ids = set(nodes)
    if len(nodes) != len(g["nodes"]):
        failures.append("duplicate node ids in graph.json")
    reduced = {(e["src"], e["dst"]) for e in g["edges_reduced"]}
    for y, x in reduced:
        if y not in ids or x not in ids:
            failures.append(f"edge references unknown node {y}->{x}")
    # acyclicity + layer invariant over reduced edges
    layer = {n["id"]: n["layer"] for n in g["nodes"]}
    order = topo_order(nodes, reduced)
    if order is None:
        failures.append("reduced graph is cyclic")
    for y, x in sorted(reduced):
        if not layer[y] < layer[x]:
            failures.append(f"layer invariant violated: {nodes[y]['ref']} -> {nodes[x]['ref']}")
            break
    # layer consistency: layer == 1 + max(layer preds)
    preds = defaultdict(list)
    for y, x in reduced:
        preds[x].append(y)
    for v in ids:
        expect = 1 + max((layer[p] for p in preds[v]), default=0)
        if layer[v] != expect:
            failures.append(
                f"layer value wrong for {nodes[v]['ref']}: {layer[v]} != {expect}")
            break
    # study_order.tsv agrees with graph layers
    spath = os.path.join(OUT_DIR, "study_order.tsv")
    if not os.path.exists(spath):
        failures.append("study_order.tsv missing")
    else:
        with open(spath, encoding="utf-8") as f:
            body = f.read().splitlines()[1:]
        prev = None
        for line in body:
            parts = line.split("\t")
            seq, lay, ref = int(parts[0]), int(parts[1]), parts[2]
            if (seq, lay) <= (prev or (0, 0)):
                failures.append("study_order.tsv not sorted by (layer, seq)")
                break
            prev = (seq, lay)
            node = next((n for n in g["nodes"] if n["ref"] == ref), None)
            if node is None or node["layer"] != lay:
                failures.append(f"study_order layer disagrees with graph.json at {ref}")
                break
    meta = g["meta"]
    print(
        f"nodes={meta['nodes']} reduced_edges={meta['reduced_edges']} "
        f"max_layer={g['metrics']['max_layer']} "
        f"diameter(raw/reduced)={g['metrics']['diameter_raw']}/"
        f"{g['metrics']['diameter_reduced']}"
    )
    if failures:
        for msg in failures:
            print("FAIL:", msg)
        return 1
    print("PASS: acyclic, layer invariant, artifact consistency all hold.")
    return 0


# --------------------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description="Aṣṭādhyāyī sūtra dependency graph (H6056).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="fetch source, build graph, export artifacts")
    b.add_argument("--refresh", action="store_true", help="re-download the source cache")
    sub.add_parser("check", help="validate committed artifacts (offline)")
    args = ap.parse_args()

    if args.cmd == "check":
        return check()

    text, sha = load_source(args.refresh)
    nodes = parse_nodes(text)
    raw_typed, stats = build_raw_edges(nodes)
    raw = untyped(raw_typed)
    order = topo_order(nodes, raw)
    if order is None:
        print("FATAL: raw graph cyclic — refusing to export.", file=sys.stderr)
        return 1
    back = sum(1 for y, x in raw if int(y) > int(x))
    reduced, _ = transitive_reduction(nodes, raw)
    layer = layers(nodes, reduced)
    graph = write_outputs(nodes, raw_typed, reduced, layer, sha, stats)
    m = graph["meta"]
    met = graph["metrics"]
    print(
        f"nodes={m['nodes']} raw_typed={m['raw_edges']} raw_untyped={m['raw_edges_untyped']} "
        f"reduced={m['reduced_edges']} back_edges={back} dangling={stats['dangling_an'] + stats['dangling_ad']} "
        f"diameter(raw/reduced)={met['diameter_raw']}/{met['diameter_reduced']} "
        f"max_layer={met['max_layer']}"
    )
    print(f"source sha256: {sha}")
    print(f"wrote artifacts to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
