#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""SG-H2 + SG-H9 (measure-now layer) for the GrammarRelations site page.

Companion to ``scripts/sequence_tau.py`` (S1 / SG-H1, already computed and
committed in ``scripts/data/sequence_tau_summary.csv``) — this script adds the
two remaining runs-today statistics from docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md
and deliberately does NOT recompute tau:

* SG-H2 — positional drift: within shared exercise clusters, is the
  *normalized* lesson position (lesson / total lessons of that book)
  systematically later in Kochergina 1998 than in Buehler 1923?
  Paired Wilcoxon signed-rank (normal approximation, zeros dropped) over the
  Buehler<->Kochergina pairs already emitted by sequence_tau.py.
* SG-H9 (proxy) — difficulty ramp: per textbook, mean sentence length (chars)
  by lesson-position quartile + Spearman rho between normalized lesson
  position and sentence length, from scripts/data/sentences.json.
  Honest caveat: character length is a surface proxy, not a Sanskrit
  readability model (Vajjala 2022 constraint stated in the agenda).

Stdlib only, deterministic. Outputs (committed):
* scripts/data/grammar_relations_stats.json
* stdout — markdown tables for the page

Run: ``python scripts/grammar_relations_stats.py``  (from repo root)
"""
import csv
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "scripts" / "data"

_ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s):
    total, prev = 0, 0
    for ch in reversed(s.strip().upper()):
        val = _ROMAN[ch]
        total += -val if val < prev else val
        prev = max(prev, val)
    return total


def parse_lesson(cell):
    """Earliest lesson number in a cell; auto-detect Arabic vs Roman per token."""
    cell = (cell or "").strip()
    if not cell:
        return None
    values = []
    for tok in re.split(r"[;,\s]+", cell):
        if not tok:
            continue
        values.append(int(tok) if tok.isdigit() else roman_to_int(tok))
    return min(values) if values else None


def spearman_rho(xs, ys):
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(
        sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry)
    )
    return num / den if den else float("nan")


def wilcoxon_signed_rank(diffs):
    """Two-sided normal-approximation p for paired diffs (zeros dropped)."""
    d = [x for x in diffs if x != 0]
    n = len(d)
    if n < 10:
        return None, None, n
    ad = sorted((abs(x), x > 0) for x in d)
    w_plus = 0.0
    i = 0
    while i < n:
        j = i
        while j + 1 < n and ad[j + 1][0] == ad[i][0]:
            j += 1
        avg_rank = (i + j) / 2 + 1
        for k in range(i, j + 1):
            if ad[k][1]:
                w_plus += avg_rank
        i = j + 1
    mu = n * (n + 1) / 4
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24)
    z = (w_plus - mu) / sigma
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))
    return z, p, n


def main():
    # ---- lesson scale + SG-H9 difficulty proxies from sentences.json -----
    with open(DATA / "sentences.json", encoding="utf-8") as f:
        sentences = json.load(f)
    by_book = defaultdict(list)
    for s in sentences:
        lesson = parse_lesson(str(s["lesson"]))
        if lesson is not None:
            by_book[s["book"]].append((lesson, len(s["text"])))

    book_stats = {}
    for book, items in sorted(by_book.items()):
        max_lesson = max(l for l, _ in items)
        norm = [(l / max_lesson, ln) for l, ln in items]
        quartiles = defaultdict(list)
        for pos, ln in norm:
            quartiles[min(3, int(pos * 4))].append(ln)
        q_means = [
            round(sum(v) / len(v), 1) for v in (quartiles[i] for i in range(4))
        ]
        rho = spearman_rho([p for p, _ in norm], [ln for _, ln in norm])
        book_stats[book] = {
            "n_sentences": len(items),
            "max_lesson": max_lesson,
            "mean_len_by_quartile": q_means,
            "ramp_q4_over_q1": round(q_means[3] / q_means[0], 2),
            "spearman_pos_vs_len": round(rho, 3),
        }

    # ---- SG-H2: positional drift over the committed tau pairs ------------
    with open(DATA / "sequence_tau_pairs.csv", encoding="utf-8") as f:
        pair_rows = [
            r
            for r in csv.DictReader(f)
            if r["pair"].startswith("Buehler") and "Kochergina" in r["pair"]
        ]
    tot_b = book_stats["buhler"]["max_lesson"]
    tot_k = book_stats["kochergina"]["max_lesson"]
    diffs = [
        int(r["lesson_b"]) / tot_k - int(r["lesson_a"]) / tot_b
        for r in pair_rows
    ]
    z, p, n_eff = wilcoxon_signed_rank(diffs)
    diffs_sorted = sorted(diffs)
    sg_h2 = {
        "pair": "Buehler 1923 -> Kochergina 1998",
        "n_pairs": len(diffs),
        "n_nonzero": n_eff,
        "total_lessons": {"buhler": tot_b, "kochergina": tot_k},
        "median_shift_normalized": round(diffs_sorted[len(diffs_sorted) // 2], 3),
        "share_later_in_kochergina": round(
            sum(1 for d in diffs if d > 0) / len(diffs), 3
        ),
        "wilcoxon_z": round(z, 2) if z is not None else None,
        "wilcoxon_p_two_sided": (
            float(f"{p:.2e}") if p is not None else None
        ),
    }

    out = {
        "source": (
            "scripts/grammar_relations_stats.py over "
            "scripts/data/sequence_tau_pairs.csv (SG-H2 pairs) + "
            "scripts/data/sentences.json (3213 sentences; SG-H9 proxies)"
        ),
        "sg_h2_positional_drift": sg_h2,
        "sg_h9_difficulty_proxies": book_stats,
        "caveats": [
            "Sentence length in characters is a surface proxy, not a Sanskrit readability model (SG-H9 / Vajjala 2022 caveat).",
            "Buehler text is the 1923 Stockholm reprint held as an unverified proxy for the 1878 first edition (D4 gate) — no borrowing-direction claims.",
            "Earliest lesson per multi-lesson cluster (sequence_tau.py policy).",
            "SG-H2 is a position claim, not a borrowing-direction claim (agenda wording).",
        ],
    }
    out_path = DATA / "grammar_relations_stats.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print("## SG-H2 positional drift (normalized lesson position)\n")
    for k, v in sg_h2.items():
        print(f"- {k}: {v}")
    print("\n## SG-H9 difficulty proxies\n")
    print("| book | sentences | lessons | mean len Q1-Q4 (chars) | Q4/Q1 | Spearman rho(pos, len) |")
    print("|---|---|---|---|---|---|")
    for b, v in book_stats.items():
        print(
            f"| {b} | {v['n_sentences']} | {v['max_lesson']} | "
            f"{v['mean_len_by_quartile']} | {v['ramp_q4_over_q1']} | "
            f"{v['spearman_pos_vs_len']} |"
        )
    print(f"\nwrote {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
