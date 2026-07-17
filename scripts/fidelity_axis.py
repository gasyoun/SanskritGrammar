#!/usr/bin/env python3
"""Fidelity axis over the Bühler/Knauer/Kochergina concordance.

For every shared-sentence cluster in the concordance, decide whether the copies
are *identical* (verbatim), differ only by *orthography* (spelling/transcription
variants — anusvāra vs homorganic nasal, geminate cluster spelling, visarga
dropped, etc.), or are *modified* (a clause/word added, dropped, or changed —
genuine textual reworking).

Reuses the H311/H327 pipeline data:
  * scripts/data/matches.json        — 235 pairwise matches (both texts + score/exact)
  * scripts/data/matches_review.tsv  — H327 verdicts for the 128 non-exact pairs
Clustering reproduces build_catalog.py (union-find, same IAST >=4-word filter),
so cluster identity lines up 1:1 with catalog.json's C0001..C0124.

Output:
  * scripts/data/fidelity.json  — per-cluster verdict + per-edge detail
  * scripts/data/fidelity.csv   — flat table
  * prints summary counts (overall + per book-pair) to stderr
"""
import csv
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("FIDELITY_IN_DIR", os.path.join(ROOT, "scripts", "data"))
OUT_DIR = os.environ.get("FIDELITY_OUT_DIR", DATA_DIR)

BOOK_YEAR = {"buhler": 1878, "knauer": 1908, "kochergina": 1998}
# fidelity ranks: higher = more divergent; a cluster takes the max over its edges
RANK = {"identical": 0, "orthographic": 1, "modified": 2}
RANK_NAME = {v: k for k, v in RANK.items()}
# H327 near-match verdicts -> fidelity bucket
VERDICT_MAP = {
    "spelling_variant": "orthographic",
    "length_mismatch": "modified",
    "low_similarity": "modified",
}


class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def load_matches():
    with open(os.path.join(DATA_DIR, "matches.json"), encoding="utf-8") as f:
        matches = json.load(f)
    kept = []
    for m in matches:
        if m["script"] == "iast":
            if len(m["a"]["text"].split()) < 4 or len(m["b"]["text"].split()) < 4:
                continue
        kept.append(m)
    return kept


def load_review():
    """(a_id,b_id) -> (verdict, note) for the 128 non-exact pairs."""
    out = {}
    path = os.path.join(DATA_DIR, "matches_review.tsv")
    with open(path, encoding="utf-8") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            out[(row["a_id"], row["b_id"])] = (row["verdict"], row["note"])
    return out


def edge_fidelity(m, review):
    if m.get("exact") or m["score"] >= 0.999:
        return "identical", ""
    key = (m["a"]["id"], m["b"]["id"])
    if key in review:
        verdict, note = review[key]
        return VERDICT_MAP.get(verdict, "modified"), note
    # not in review sheet but non-exact: classify by score as a fallback
    return ("orthographic" if m["score"] >= 0.95 else "modified"), ""


def main():
    matches = load_matches()
    review = load_review()

    uf = UnionFind()
    nodes = {}
    for m in matches:
        a, b = m["a"], m["b"]
        nodes[a["id"]] = a
        nodes[b["id"]] = b
        uf.union(a["id"], b["id"])

    clusters = {}
    for nid in nodes:
        clusters.setdefault(uf.find(nid), []).append(nodes[nid])

    # per-cluster
    rows = []
    for members in clusters.values():
        member_ids = {m["id"] for m in members}
        by_book = {}
        for m in members:
            by_book.setdefault(m["book"], []).append(m)
        earliest_book = min(by_book, key=lambda b: BOOK_YEAR[b])
        deva = [m for m in members if m["script"] == "deva"]
        exemplar = deva[0] if deva else members[0]

        edges = []
        for m in matches:
            if m["a"]["id"] in member_ids and m["b"]["id"] in member_ids:
                fid, note = edge_fidelity(m, review)
                pair = tuple(sorted((m["a"]["book"], m["b"]["book"])))
                edges.append({
                    "a_id": m["a"]["id"], "b_id": m["b"]["id"],
                    "a_book": m["a"]["book"], "b_book": m["b"]["book"],
                    "pair": "↔".join(pair),
                    "score": m["score"], "fidelity": fid, "note": note,
                    "a_text": m["a"]["text"], "b_text": m["b"]["text"],
                })
        worst = max((RANK[e["fidelity"]] for e in edges), default=0)
        rows.append({
            "text": exemplar["text"],
            "script": exemplar["script"],
            "earliest_year": BOOK_YEAR[earliest_book],
            "books": {b: sorted({m["lesson"] for m in ms}) for b, ms in by_book.items()},
            "fidelity": RANK_NAME[worst],
            "edges": edges,
        })

    rows.sort(key=lambda r: (r["earliest_year"], r["text"]))
    for i, r in enumerate(rows, 1):
        r["catalog_id"] = f"C{i:04d}"

    with open(os.path.join(OUT_DIR, "fidelity.json"), "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    with open(os.path.join(OUT_DIR, "fidelity.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["catalog_id", "fidelity", "books", "script", "text"])
        for r in rows:
            w.writerow([r["catalog_id"], r["fidelity"],
                        "+".join(sorted(r["books"])), r["script"], r["text"]])

    # ---- summaries ----
    from collections import Counter
    overall = Counter(r["fidelity"] for r in rows)
    print("Per-cluster fidelity (n=%d): %s" % (
        len(rows), dict(overall)), file=sys.stderr)

    # per book-pair, over the DIRECTED edges (earliest -> later)
    pair_counts = {}
    for r in rows:
        for e in r["edges"]:
            years = {e["a_book"]: BOOK_YEAR[e["a_book"]], e["b_book"]: BOOK_YEAR[e["b_book"]]}
            src = min(years, key=years.get)
            dst = max(years, key=years.get)
            if src == dst:
                continue
            label = "%s->%s" % (src, dst)
            pair_counts.setdefault(label, Counter())[e["fidelity"]] += 1
    print("Per directed book-pair edge fidelity:", file=sys.stderr)
    for label, c in sorted(pair_counts.items()):
        tot = sum(c.values())
        print("  %-24s n=%3d  identical=%d orthographic=%d modified=%d"
              % (label, tot, c["identical"], c["orthographic"], c["modified"]),
              file=sys.stderr)

    # list the modified clusters (the pedagogically interesting deliberate changes)
    mod = [r for r in rows if r["fidelity"] == "modified"]
    print("\nMODIFIED clusters (%d):" % len(mod), file=sys.stderr)
    for r in mod:
        print("  %s [%s] %s" % (r["catalog_id"], "+".join(sorted(r["books"])),
                                r["text"][:70]), file=sys.stderr)


if __name__ == "__main__":
    main()
