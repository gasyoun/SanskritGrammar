#!/usr/bin/env python3
"""Sangram pilot P4 (SG-WF-008, tatpuruṣa) — Cohen κ over two independent passes.

Reads pass_A.json + pass_B.json (each a list of {cpd_token_id, coarse, fine, ...}),
computes Cohen's κ for the coarse (5-class) and fine (Leitan tatpuruṣa-subtype)
layers with a seeded bootstrap 95% CI, writes validation_verdicts.tsv, and stamps
the kill-gate verdict into coverage_summary.json.

Kill-gate (C5 §7 P4): κ < 0.7 → the type taxonomy is revised before publication;
the negative result is itself publishable (C3 П7). Net-new code — no κ template
exists in the repo (P1/P2/P3 used single-annotator coverage/recall gates).
"""
import sys
import json
import csv
import random
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "sangram" / "articles" / "tatpurusha" / "data"
SEED = 20260715
N_BOOT = 2000
THRESHOLD = 0.7


def cohen_kappa(pairs):
    """pairs: list of (label_a, label_b). Returns κ."""
    n = len(pairs)
    if n == 0:
        return None
    agree = sum(1 for a, b in pairs if a == b)
    p_o = agree / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    cats = set(ca) | set(cb)
    p_e = sum((ca.get(k, 0) / n) * (cb.get(k, 0) / n) for k in cats)
    if p_e == 1.0:
        return 1.0  # degenerate: everything one label, perfect agreement
    return (p_o - p_e) / (1 - p_e)


def bootstrap_ci(pairs, rng, n_boot=N_BOOT):
    if not pairs:
        return (None, None)
    ks = []
    m = len(pairs)
    for _ in range(n_boot):
        sample = [pairs[rng.randrange(m)] for _ in range(m)]
        k = cohen_kappa(sample)
        if k is not None:
            ks.append(k)
    ks.sort()
    lo = ks[int(0.025 * len(ks))]
    hi = ks[int(0.975 * len(ks)) - 1]
    return (round(lo, 4), round(hi, 4))


def load_pass(name):
    data = json.loads((DATA / name).read_text(encoding="utf-8"))
    return {str(d["cpd_token_id"]): d for d in data}


def main():
    a = load_pass("pass_A.json")
    b = load_pass("pass_B.json")
    ids = sorted(set(a) & set(b), key=lambda x: (len(x), x))
    print(f"Pass A: {len(a)}  Pass B: {len(b)}  common: {len(ids)}", file=sys.stderr)

    rng = random.Random(SEED)

    # coarse κ over all common items
    coarse_pairs = [(a[i]["coarse"], b[i]["coarse"]) for i in ids]
    k_coarse = cohen_kappa(coarse_pairs)
    ci_coarse = bootstrap_ci(coarse_pairs, rng)
    coarse_agree = sum(1 for x, y in coarse_pairs if x == y)

    # fine κ over items BOTH passes called tatpuruṣa
    fine_ids = [i for i in ids if a[i]["coarse"] == "tatpurusha" and b[i]["coarse"] == "tatpurusha"]
    fine_pairs = [(a[i].get("fine", "n/a"), b[i].get("fine", "n/a")) for i in fine_ids]
    k_fine = cohen_kappa(fine_pairs)
    ci_fine = bootstrap_ci(fine_pairs, rng) if fine_pairs else (None, None)
    fine_agree = sum(1 for x, y in fine_pairs if x == y)

    # coarse confusion matrix
    cats = sorted(set(x for x, _ in coarse_pairs) | set(y for _, y in coarse_pairs))
    confusion = {ca: {cb: 0 for cb in cats} for ca in cats}
    for x, y in coarse_pairs:
        confusion[x][y] += 1

    # verdicts tsv
    with open(DATA / "validation_verdicts.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["cpd_token_id", "coarse_A", "coarse_B", "coarse_agree",
                    "fine_A", "fine_B", "fine_agree", "verdict"])
        for i in ids:
            ca_, cb_ = a[i]["coarse"], b[i]["coarse"]
            fa_, fb_ = a[i].get("fine", "n/a"), b[i].get("fine", "n/a")
            cag = ca_ == cb_
            fag = (fa_ == fb_) if (ca_ == "tatpurusha" and cb_ == "tatpurusha") else ""
            verdict = "agree" if cag and (fag in (True, "")) else "disagree"
            w.writerow([i, ca_, cb_, cag, fa_, fb_, fag, verdict])

    def fired(k):
        return k is not None and k < THRESHOLD

    result = {
        "n_common": len(ids),
        "coarse": {"kappa": round(k_coarse, 4) if k_coarse is not None else None,
                   "ci95": ci_coarse, "observed_agreement": round(coarse_agree / len(ids), 4),
                   "n": len(ids), "kill_gate_fired": fired(k_coarse)},
        "fine": {"kappa": round(k_fine, 4) if k_fine is not None else None,
                 "ci95": ci_fine, "observed_agreement": round(fine_agree / len(fine_pairs), 4) if fine_pairs else None,
                 "n": len(fine_pairs), "kill_gate_fired": fired(k_fine),
                 "subset": "both passes coarse=tatpurusha"},
        "coarse_confusion": confusion,
        "coarse_dist_A": dict(Counter(x for x, _ in coarse_pairs)),
        "coarse_dist_B": dict(Counter(y for _, y in coarse_pairs)),
        "threshold": THRESHOLD,
        "verdict": ("coarse " + ("FAIL" if fired(k_coarse) else "PASS")
                    + " / fine " + ("FAIL" if fired(k_fine) else "PASS")),
    }

    (DATA / "kappa_result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # stamp into coverage_summary.json
    cov_path = DATA / "coverage_summary.json"
    cov = json.loads(cov_path.read_text(encoding="utf-8"))
    cov["kill_gate"] = {
        "metric": "Cohen κ (coarse 5-class + fine Leitan tatpuruṣa subtype)",
        "threshold": THRESHOLD,
        "coarse_kappa": result["coarse"]["kappa"], "coarse_ci95": ci_coarse,
        "fine_kappa": result["fine"]["kappa"], "fine_ci95": ci_fine,
        "fine_n": len(fine_pairs),
        "annotators": "Pass A Opus 4.8 (claude-opus-4-8) · Pass B Sonnet 5 (claude-sonnet-5)",
        "verdict": result["verdict"],
        "rule": "κ<0.7 → revise type taxonomy before publication (C5 §7 P4); negative result publishable (C3 П7)",
    }
    cov_path.write_text(json.dumps(cov, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("=== κ RESULT ===")
    print(f"coarse κ = {result['coarse']['kappa']}  CI95 {ci_coarse}  (n={len(ids)}, agree={coarse_agree})")
    print(f"fine   κ = {result['fine']['kappa']}  CI95 {ci_fine}  (n={len(fine_pairs)}, agree={fine_agree})")
    print(f"verdict: {result['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
