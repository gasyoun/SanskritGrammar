#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Q4.1 (ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md §4) — score `difflib` against the
128-pair gold set before any detector swap.

The roadmap frames ``scripts/data/matches_review.tsv`` as an already-existing gold
set: 128 near-match pairs (``exact=False``) that ``extract_sentences.py match()``
flagged via ``difflib.SequenceMatcher(None, a, b).ratio() >= 0.82``, each carrying
an H327 verdict (``spelling_variant`` / ``length_mismatch`` / ``low_similarity``)
assigned by ``scripts/review_near_matches.py``. That verdict is the target this
script scores difflib's own ``ratio()`` against.

Ground-truth mapping, sourced from the two places the verdict vocabulary is
already defined in this repo (not invented here):

* ``review_near_matches.py`` docstring calls ``low_similarity`` explicitly "a
  candidate false positive" — so it is the FP class below.
* ``spelling_variant`` is the clean, localized-diff case — unambiguous TP.
* ``length_mismatch`` is a genuine textual echo whose extraction boundary
  slipped (one side truncated/extended) — a real match, not a spurious one, but
  not what a threshold-only detector can fix; reported as its own class, not
  folded into either TP or FP, so no headline number hides it.

Method
------
* Precision of the ``score >= 0.82`` operating point actually shipped
  (``extract_sentences.py match(threshold=0.82)``): TP / (TP + FP) over all 128
  pairs, TP = spelling_variant, FP = low_similarity, length_mismatch excluded
  from the ratio and reported alongside.
* A precision sweep over the candidate-pool score cutoffs actually present in
  the data (0.82, 0.85, 0.90, 0.95, 0.98, 0.99): at each cutoff tau, precision
  and pairs-retained among pairs with score >= tau. This is precision-recall
  *within the flagged pool*, not corpus recall (see Scope note below).
* Per-verdict score summary (min/median/mean/max) — does the score difflib
  already computes separate the classes at all, before spending effort on
  chunk-size tuning (Q4.2) or any threshold retune.

Scope note (stated once, carried into the report — do not silently drop):
this file is 128 pairs difflib *already surfaced* at score >= 0.82. It cannot
measure difflib's recall against reused sentences it never surfaced (wrong
chunk size, script-normalization miss, below-threshold true matches) — that
requires an independent detector, which is exactly the Q4.2 gate this script
exists to clear.

Outputs (all committed)
------------------------
* ``scripts/data/q41_difflib_gold_evaluation.json`` — full numeric result
* ``Q4_1_DIFFLIB_EVALUATION_RESULT.md``              — human-readable report
* stdout                                              — summary table

Run: ``python scripts/q41_difflib_gold_evaluation.py`` (from repo root)
"""
import csv
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
GOLD_TSV = ROOT / "scripts" / "data" / "matches_review.tsv"
OUT_JSON = ROOT / "scripts" / "data" / "q41_difflib_gold_evaluation.json"
OUT_REPORT = ROOT / "Q4_1_DIFFLIB_EVALUATION_RESULT.md"

OPERATING_THRESHOLD = 0.82  # extract_sentences.py match(threshold=0.82)
SWEEP_CUTOFFS = (0.82, 0.85, 0.90, 0.95, 0.98, 0.99)

TP_VERDICT = "spelling_variant"
FP_VERDICT = "low_similarity"
BOUNDARY_VERDICT = "length_mismatch"
KNOWN_VERDICTS = {TP_VERDICT, FP_VERDICT, BOUNDARY_VERDICT}


def load_gold():
    with open(GOLD_TSV, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    for row in rows:
        row["score"] = float(row["score"])
        if row["verdict"] not in KNOWN_VERDICTS:
            raise ValueError(
                "unknown verdict %r in %s (row %s/%s) — extend KNOWN_VERDICTS or "
                "fix the source row" % (row["verdict"], GOLD_TSV, row["a_id"], row["b_id"])
            )
    return rows


def precision_at(rows, cutoff):
    """Precision among pairs with score >= cutoff, under both headline readings.

    strict:  TP = spelling_variant only,                  FP = length_mismatch + low_similarity
    lenient: TP = spelling_variant + length_mismatch,      FP = low_similarity only

    Both denominators are the full retained pool (TP+FP == n_retained in each
    reading) — no pair is silently excluded from either ratio.
    """
    pool = [r for r in rows if r["score"] >= cutoff]
    spelling = sum(1 for r in pool if r["verdict"] == TP_VERDICT)
    boundary = sum(1 for r in pool if r["verdict"] == BOUNDARY_VERDICT)
    low_sim = sum(1 for r in pool if r["verdict"] == FP_VERDICT)
    n = len(pool)
    # both readings share the same denominator: the whole retained pool
    strict = spelling / n if n else None
    lenient = (spelling + boundary) / n if n else None
    return {
        "cutoff": cutoff,
        "n_retained": n,
        "tp_spelling_variant": spelling,
        "boundary_length_mismatch": boundary,
        "fp_low_similarity": low_sim,
        "precision_strict": round(strict, 4) if strict is not None else None,
        "precision_lenient": round(lenient, 4) if lenient is not None else None,
    }


def score_stats(values):
    if not values:
        return None
    values = sorted(values)
    n = len(values)
    mid = n // 2
    median = values[mid] if n % 2 else (values[mid - 1] + values[mid]) / 2
    return {
        "n": n,
        "min": round(values[0], 3),
        "median": round(median, 3),
        "mean": round(sum(values) / n, 4),
        "max": round(values[-1], 3),
    }


def main():
    rows = load_gold()
    n_total = len(rows)

    from collections import Counter
    verdict_counts = Counter(r["verdict"] for r in rows)

    by_verdict_scores = {
        v: score_stats([r["score"] for r in rows if r["verdict"] == v])
        for v in KNOWN_VERDICTS
    }

    # operating_point IS the headline reading: the full 128-pair pool restricted
    # to score >= 0.82 is every row (that is how the pool was built), so its
    # strict/lenient precision are the headline strict/lenient numbers — computed
    # once, not re-derived a second way.
    operating_point = precision_at(rows, OPERATING_THRESHOLD)
    sweep = [precision_at(rows, tau) for tau in SWEEP_CUTOFFS]

    result = {
        "gold_set": str(GOLD_TSV.relative_to(ROOT)),
        "n_pairs": n_total,
        "operating_threshold": OPERATING_THRESHOLD,
        "verdict_counts": dict(verdict_counts),
        "score_stats_by_verdict": by_verdict_scores,
        "precision_at_operating_threshold": operating_point,
        "precision_sweep": sweep,
        "scope_limitation": (
            "This gold set is 128 pairs difflib already surfaced at score >= "
            f"{OPERATING_THRESHOLD}. It scores difflib's PRECISION at that operating "
            "point (of what it flagged, how much is genuine reuse) and how score "
            "separates the verdict classes. It cannot measure RECALL (reused "
            "sentences difflib never surfaced at all) — that needs an independent "
            "detector, which is the Q4.2 TRACER/Passim swap this evaluation gates."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    write_report(result)

    print(f"{n_total} gold pairs: {dict(verdict_counts)}", file=sys.stderr)
    print(
        "precision @ %.2f (n=%d): strict=%.4f (tp=%d)  lenient=%.4f (tp=%d+%d)"
        % (
            OPERATING_THRESHOLD,
            operating_point["n_retained"],
            operating_point["precision_strict"], operating_point["tp_spelling_variant"],
            operating_point["precision_lenient"], operating_point["tp_spelling_variant"],
            operating_point["boundary_length_mismatch"],
        ),
        file=sys.stderr,
    )
    print(f"wrote {OUT_JSON}", file=sys.stderr)
    print(f"wrote {OUT_REPORT}", file=sys.stderr)


def write_report(result):
    lines = []
    lines.append("# Q4.1 difflib evaluation — precision against the 128-pair gold set")
    lines.append("")
    lines.append(
        "_Created: 24-09-2026 · Last updated: 24-09-2026_"
    )
    lines.append("")
    lines.append(
        "[ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) "
        "§4 Q4.1: \"Evaluate `difflib` against the 128 labeled pairs\" — "
        "[`scripts/data/matches_review.tsv`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/matches_review.tsv) "
        "is already a gold set, use it before replacing anything. Generator: "
        "[`scripts/q41_difflib_gold_evaluation.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/q41_difflib_gold_evaluation.py)."
    )
    lines.append("")
    lines.append("## What is being scored")
    lines.append("")
    lines.append(
        "`extract_sentences.py match(threshold=0.82)` flags a pair as a candidate "
        "reuse whenever `difflib.SequenceMatcher(None, a, b).ratio() >= 0.82`. The "
        "128 non-exact pairs it has flagged so far each carry an H327 verdict "
        "(`spelling_variant` / `length_mismatch` / `low_similarity`) from "
        "[`scripts/review_near_matches.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/review_near_matches.py), "
        "whose own docstring calls `low_similarity` \"a candidate false positive\". "
        "That is the ground truth this script scores difflib's `ratio()` against."
    )
    lines.append("")
    lines.append("## Verdict counts (n=%d)" % result["n_pairs"])
    lines.append("")
    lines.append("| Verdict | n | score min | median | mean | max |")
    lines.append("|---|---|---|---|---|---|")
    for v in (TP_VERDICT, BOUNDARY_VERDICT, FP_VERDICT):
        stats = result["score_stats_by_verdict"][v]
        n = result["verdict_counts"].get(v, 0)
        if stats:
            lines.append(
                f"| `{v}` | {n} | {stats['min']} | {stats['median']} | {stats['mean']} | {stats['max']} |"
            )
        else:
            lines.append(f"| `{v}` | {n} | — | — | — | — |")
    lines.append("")
    lines.append("## Precision at the shipped operating point (score ≥ 0.82)")
    lines.append("")
    op = result["precision_at_operating_threshold"]
    lines.append(
        "Two readings over the same 128-pair pool, both reported (neither is "
        "hidden behind the other):"
    )
    lines.append("")
    lines.append(
        f"- **Strict** (TP = `spelling_variant` only; FP = `length_mismatch` + "
        f"`low_similarity`): {op['tp_spelling_variant']}/{op['n_retained']} = "
        f"**{op['precision_strict']:.4f}**."
    )
    lines.append(
        f"- **Lenient** (TP = `spelling_variant` + `length_mismatch`, both are "
        f"genuine textual echoes even if the boundary slipped; FP = "
        f"`low_similarity` only, per the pipeline's own documented false-positive "
        f"class): {op['tp_spelling_variant']+op['boundary_length_mismatch']}/"
        f"{op['n_retained']} = **{op['precision_lenient']:.4f}**."
    )
    lines.append("")
    lines.append("## Precision sweep across score cutoffs")
    lines.append("")
    lines.append(
        "Same strict/lenient definitions as above, applied to the sub-pool with "
        "score ≥ cutoff. This is precision *within the flagged pool*, not corpus "
        "recall — see Scope, below."
    )
    lines.append("")
    lines.append("| cutoff | n retained | spelling_variant | length_mismatch | low_similarity | precision (strict) | precision (lenient) |")
    lines.append("|---|---|---|---|---|---|---|")
    for row in result["precision_sweep"]:
        strict = f"{row['precision_strict']:.4f}" if row["precision_strict"] is not None else "—"
        lenient = f"{row['precision_lenient']:.4f}" if row["precision_lenient"] is not None else "—"
        lines.append(
            f"| {row['cutoff']} | {row['n_retained']} | {row['tp_spelling_variant']} | "
            f"{row['boundary_length_mismatch']} | {row['fp_low_similarity']} | {strict} | {lenient} |"
        )
    lines.append("")
    lines.append("## Scope — what this evaluation cannot say")
    lines.append("")
    lines.append(result["scope_limitation"])
    lines.append("")
    lines.append(
        "This is the evidence check "
        "[ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) "
        "§4's Q4.2 gate names (\"gate: Q4.1's evidence check accepted first\"): a "
        "TRACER/Passim swap (Q4.2) should report Δ recall against this precision "
        "baseline, not re-derive it."
    )
    lines.append("")
    lines.append("## Raw numbers")
    lines.append("")
    lines.append(
        "[`scripts/data/q41_difflib_gold_evaluation.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/q41_difflib_gold_evaluation.json)."
    )
    lines.append("")
    lines.append("_Гасунс_")
    lines.append("")

    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
