#!/usr/bin/env python3
"""Cluster the cross-book sentence matches from matches.json into a single
chronological concordance (Buhler 1878/1923 -> Knauer 1908 -> Kochergina 1998)
and emit scripts/data/catalog.json + scripts/data/catalog.csv.

Devanagari matches are the primary signal (all three books share Devanagari
unambiguously); IAST matches are included only when both sides have >=4 words,
since single-word/paradigm-table noise dominates below that (see H311).
"""
import csv
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "scripts", "data")

BOOK_YEAR = {"buhler": 1878, "knauer": 1908, "kochergina": 1998}
BOOK_LABEL = {
    "buhler": "Bühler (1878/1923)",
    "knauer": "Knauer (1908)",
    "kochergina": "Kochergina (1998)",
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


def main():
    with open(os.path.join(DATA_DIR, "matches.json"), encoding="utf-8") as f:
        matches = json.load(f)

    uf = UnionFind()
    nodes = {}  # id -> sentence dict
    edges = []  # kept (a,b,score,exact) for provenance
    for m in matches:
        if m["script"] == "iast":
            if len(m["a"]["text"].split()) < 4 or len(m["b"]["text"].split()) < 4:
                continue
        a, b = m["a"], m["b"]
        nodes[a["id"]] = a
        nodes[b["id"]] = b
        uf.union(a["id"], b["id"])
        edges.append(m)

    clusters = {}
    for node_id in nodes:
        root = uf.find(node_id)
        clusters.setdefault(root, []).append(nodes[node_id])

    rows = []
    for members in clusters.values():
        by_book = {}
        for m in members:
            by_book.setdefault(m["book"], []).append(m)
        earliest_book = min(by_book, key=lambda b: BOOK_YEAR[b])
        # Prefer a Devanagari exemplar for display text; fall back to IAST.
        deva = [m for m in members if m["script"] == "deva"]
        exemplar = deva[0] if deva else members[0]
        rows.append({
            "earliest_book": earliest_book,
            "earliest_year": BOOK_YEAR[earliest_book],
            "text": exemplar["text"],
            "script": exemplar["script"],
            "books": {
                book: sorted({f"{m['lesson']}" for m in ms})
                for book, ms in by_book.items()
            },
        })

    rows.sort(key=lambda r: (r["earliest_year"], r["text"]))
    for i, r in enumerate(rows, 1):
        r["catalog_id"] = f"C{i:04d}"

    out_json = os.path.join(DATA_DIR, "catalog.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    out_csv = os.path.join(DATA_DIR, "catalog.csv")
    with open(out_csv, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["catalog_id", "earliest_book", "earliest_year", "script", "text",
                    "buhler_lessons", "knauer_lessons", "kochergina_lessons"])
        for r in rows:
            w.writerow([
                r["catalog_id"], r["earliest_book"], r["earliest_year"], r["script"], r["text"],
                ";".join(r["books"].get("buhler", [])),
                ";".join(r["books"].get("knauer", [])),
                ";".join(r["books"].get("kochergina", [])),
            ])

    n_all3 = sum(1 for r in rows if len(r["books"]) == 3)
    n_bk = sum(1 for r in rows if set(r["books"]) == {"buhler", "knauer"})
    n_bko = sum(1 for r in rows if set(r["books"]) == {"buhler", "kochergina"})
    n_ko = sum(1 for r in rows if set(r["books"]) == {"knauer", "kochergina"})
    print(f"{len(rows)} clusters total: {n_all3} in all three, "
          f"{n_bk} Bühler+Knauer only, {n_bko} Bühler+Kochergina only, {n_ko} Knauer+Kochergina only",
          file=sys.stderr)
    print(f"wrote {out_json}", file=sys.stderr)
    print(f"wrote {out_csv}", file=sys.stderr)


if __name__ == "__main__":
    main()
