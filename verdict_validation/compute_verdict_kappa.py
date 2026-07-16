"""compute_verdict_kappa.py — Cohen's κ for the A65 verdict-validation two-pass study (H1041).

Inputs (same directory):
  validation_sample_gold.json    — pass-1 register verdicts (annotator A).
  validation_sample_secondpass.json — blind annotator-B verdicts:
      [{"id": ..., "verdict": ..., "why": ...}, ...]

Outputs:
  verdict_kappa_stats.json — overall κ + 95% bootstrap CI (2,000 resamples,
  seed 20260716), raw agreement, per-book κ, per-category agreement, the
  4×4 confusion matrix (A rows × B columns), and the disagreement list.

Pure stdlib; deterministic.
"""
import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
CATS = ["TRUE", "OVERSTATED", "FALSE", "UNTESTABLE"]
SEED = 20260716
N_BOOT = 2000


def cohen_kappa(pairs):
    n = len(pairs)
    if n == 0:
        return float("nan")
    po = sum(1 for a, b in pairs if a == b) / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum((ca[c] / n) * (cb[c] / n) for c in CATS)
    if pe == 1.0:
        return 1.0
    return (po - pe) / (1 - pe)


def main():
    gold = json.loads((HERE / "validation_sample_gold.json").read_text(encoding="utf-8"))
    second = json.loads((HERE / "validation_sample_secondpass.json").read_text(encoding="utf-8"))
    b_by_id = {r["id"]: str(r["verdict"]).upper() for r in second}

    pairs, rows = [], []
    for cid, g in sorted(gold.items()):
        if cid not in b_by_id:
            print(f"WARN: no annotator-B verdict for {cid}")
            continue
        a, b = g["verdict_fact"], b_by_id[cid]
        pairs.append((a, b))
        rows.append({"id": cid, "book": g["book"], "a": a, "b": b, "agree": a == b})

    n = len(pairs)
    kappa = cohen_kappa(pairs)
    agreement = sum(1 for a, b in pairs if a == b) / n

    rng = random.Random(SEED)
    boots = sorted(
        cohen_kappa([pairs[rng.randrange(n)] for _ in range(n)]) for _ in range(N_BOOT)
    )
    ci_lo, ci_hi = boots[int(0.025 * N_BOOT)], boots[int(0.975 * N_BOOT)]

    per_book = {}
    for book in sorted({r["book"] for r in rows}):
        bp = [(r["a"], r["b"]) for r in rows if r["book"] == book]
        per_book[book] = {
            "n": len(bp),
            "kappa": round(cohen_kappa(bp), 3),
            "agreement": round(sum(1 for a, b in bp if a == b) / len(bp), 3),
        }

    conf = {a: {b: 0 for b in CATS} for a in CATS}
    for a, b in pairs:
        conf[a][b] += 1

    per_cat = {}
    for c in CATS:
        cp = [(a, b) for a, b in pairs if a == c]
        per_cat[c] = {
            "n_gold": len(cp),
            "recall_by_B": round(sum(1 for a, b in cp if a == b) / len(cp), 3) if cp else None,
        }

    disagreements = [r for r in rows if not r["agree"]]
    out = {
        "n": n,
        "kappa": round(kappa, 3),
        "kappa_ci95": [round(ci_lo, 3), round(ci_hi, 3)],
        "raw_agreement": round(agreement, 3),
        "bootstrap": {"resamples": N_BOOT, "seed": SEED},
        "per_book": per_book,
        "per_category": per_cat,
        "confusion_A_rows_B_cols": conf,
        "disagreements": disagreements,
        "annotators": {
            "A": "register pass-1 (mixed tiers, per-entry provenance in the registers)",
            "B": "Sonnet 5 (claude-sonnet-5), blind slices of 15-20 items, 16-07-2026",
        },
    }
    (HERE / "verdict_kappa_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"n={n}  kappa={kappa:.3f}  CI95=[{ci_lo:.3f},{ci_hi:.3f}]  agree={agreement:.1%}  "
          f"disagreements={len(disagreements)}")
    for b, s in per_book.items():
        print(f"  {b:11s} n={s['n']:3d}  kappa={s['kappa']}  agree={s['agreement']}")


if __name__ == "__main__":
    main()
