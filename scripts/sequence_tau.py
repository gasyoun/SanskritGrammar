#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""S1 — Textbook sequencing corpus: Kendall's tau over shared-sentence clusters.

Reads ``scripts/data/catalog.csv`` — the committed shared-sentence concordance,
one row per cluster, with the lesson each shared exercise sentence occupies in
Buehler (1878/1923), Knauer (1908) and Kochergina (1998). Each pair of books is
an independent *ordering* of the same material; Kendall's tau-b measures how much
the two orderings agree on the sequence in which shared material is introduced.

Method
------
* For a book pair, keep only clusters present in BOTH books.
* A sentence appearing in several lessons uses the EARLIEST (min) lesson — the
  point of first introduction. (Only 2 cells carry multi-lesson values.)
* Buehler and Kochergina number lessons in Roman numerals, Knauer in Arabic; the
  parser auto-detects each token's form, so column order does not matter.
* tau-b via scipy.stats.kendalltau (ties-corrected), with its two-sided p-value.

Outputs (all committed):
* ``scripts/data/sequence_tau_pairs.csv``   — the (lesson_a, lesson_b) pairs used
* ``scripts/data/sequence_tau_summary.csv`` — tau, p, n, interpretation per pair
* stdout                                    — the summary table

Run: ``python scripts/sequence_tau.py``  (from repo root)
"""
import csv
import re
import sys
from pathlib import Path

from scipy.stats import kendalltau

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "scripts" / "data" / "catalog.csv"
OUT_PAIRS = ROOT / "scripts" / "data" / "sequence_tau_pairs.csv"
OUT_SUMMARY = ROOT / "scripts" / "data" / "sequence_tau_summary.csv"

# Book pairs to score: (column_a, column_b, label). Order-independent for tau.
PAIRS = [
    ("buhler_lessons", "knauer_lessons", "Buehler↔Knauer"),
    ("buhler_lessons", "kochergina_lessons", "Buehler↔Kochergina"),
    ("knauer_lessons", "kochergina_lessons", "Knauer↔Kochergina"),
]

_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s):
    """Standard subtractive Roman-numeral parse (e.g. 'XLVIII' -> 48)."""
    s = s.strip().upper()
    total, prev = 0, 0
    for ch in reversed(s):
        if ch not in _ROMAN:
            raise ValueError(f"not a roman numeral: {s!r}")
        val = _ROMAN[ch]
        total += -val if val < prev else val
        prev = max(prev, val)
    return total


def parse_lesson(cell, column):
    """Return the earliest lesson number in a cell, or None if empty.

    Cells may hold several lessons separated by ';' ',' or whitespace; we take
    the minimum (first introduction). Each token is auto-detected as Arabic
    (Knauer) or Roman (Buehler, Kochergina) — column order is irrelevant.
    """
    cell = (cell or "").strip()
    if not cell:
        return None
    values = []
    for tok in re.split(r"[;,\s]+", cell):
        if not tok:
            continue
        values.append(int(tok) if tok.isdigit() else roman_to_int(tok))
    return min(values) if values else None


def main():
    rows = list(csv.DictReader(CATALOG.open(encoding="utf-8")))

    pair_records = []
    summary = []
    for col_a, col_b, label in PAIRS:
        xs, ys, ids = [], [], []
        for r in rows:
            a = parse_lesson(r[col_a], col_a)
            b = parse_lesson(r[col_b], col_b)
            if a is None or b is None:
                continue
            xs.append(a)
            ys.append(b)
            ids.append(r["catalog_id"])
            pair_records.append(
                {"pair": label, "catalog_id": r["catalog_id"],
                 "lesson_a": a, "lesson_b": b}
            )
        n = len(xs)
        if n < 3:
            summary.append({"pair": label, "n": n, "tau": "", "p_value": "",
                            "interpretation": "too few shared clusters for tau"})
            continue
        tau, p = kendalltau(xs, ys)
        summary.append({
            "pair": label, "n": n,
            "tau": round(float(tau), 4),
            "p_value": f"{p:.3e}",
            "interpretation": interpret(tau, p),
        })

    with OUT_PAIRS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["pair", "catalog_id", "lesson_a", "lesson_b"])
        w.writeheader()
        w.writerows(pair_records)

    with OUT_SUMMARY.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["pair", "n", "tau", "p_value", "interpretation"])
        w.writeheader()
        w.writerows(summary)

    print(f"catalog: {CATALOG.relative_to(ROOT)}  ({len(rows)} clusters)")
    print("policy:  earliest-lesson; auto-detect Roman/Arabic per token; tau-b (scipy)")
    print()
    hdr = f"{'pair':<22} {'n':>4} {'tau-b':>8} {'p-value':>11}  interpretation"
    print(hdr)
    print("-" * len(hdr))
    for s in summary:
        print(f"{s['pair']:<22} {s['n']:>4} {str(s['tau']):>8} "
              f"{str(s['p_value']):>11}  {s['interpretation']}")
    print()
    print(f"wrote {OUT_PAIRS.relative_to(ROOT)}")
    print(f"wrote {OUT_SUMMARY.relative_to(ROOT)}")


def interpret(tau, p):
    sig = "significant" if p < 0.05 else "NOT significant (p>=0.05)"
    if tau >= 0.7:
        strength = "very strong agreement"
    elif tau >= 0.5:
        strength = "strong agreement"
    elif tau >= 0.3:
        strength = "moderate agreement"
    elif tau >= 0.1:
        strength = "weak agreement"
    elif tau > -0.1:
        strength = "no monotonic agreement"
    else:
        strength = "inverse ordering"
    return f"{strength}; {sig}"


if __name__ == "__main__":
    main()
