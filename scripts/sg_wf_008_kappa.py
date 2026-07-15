#!/usr/bin/env python3
"""SG-WF-008 pilot P4: Cohen's κ between two independent samāsa-type passes.

Reads the two blind classification passes (compound_id -> type) and measures
inter-annotator agreement. Kill-gate C5 § 7 P4: κ < 0.7 → the type taxonomy is
revised before any type-frequency is published (the numbers are not reliable
enough to stand as corpus facts).

Two agreement levels are reported:
  - full 7-way κ over {tatpurusha, karmadharaya, dvigu, dvandva, bahuvrihi,
    avyayibhava, unclear};
  - collapsed binary κ: determinative (tatpurusha+karmadharaya+dvigu) vs
    non-determinative (dvandva+bahuvrihi+avyayibhava), which is the distinction
    SG-WF-008 actually rests on (is it a tatpuruṣa at all?). `unclear` from either
    pass is excluded from the binary κ and counted separately.

Provenance note: both passes are LLM annotators (Opus 4.8 + Sonnet 4.6), sharing
training bias — κ here is an UPPER bound on what two independent human annotators
would reach, not a lower bound. Reported honestly in the article.

Usage:
  python scripts/sg_wf_008_kappa.py PASS_A.json PASS_B.json
Writes sangram/articles/tatpurusha/data/kappa_summary.json + agreement_matrix.tsv
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DATA = Path(__file__).resolve().parents[1] / "sangram" / "articles" / "tatpurusha" / "data"

LABELS = ["tatpurusha", "karmadharaya", "dvigu", "dvandva",
          "bahuvrihi", "avyayibhava", "unclear"]
DETERMINATIVE = {"tatpurusha", "karmadharaya", "dvigu"}
NON_DET = {"dvandva", "bahuvrihi", "avyayibhava"}

# Leitan / Pāṇinian-Mahābhāṣya top level (MG ruling 15-07-2026): the 5 classes are
# tatpuruṣa · bahuvrīhi · dvandva · avyayībhāva · kevala-samāsa, with
# dvigu ⊂ karmadhāraya ⊂ tatpuruṣa (both fold UP into tatpuruṣa).
LEITAN5 = ["tatpurusha", "bahuvrihi", "dvandva", "avyayibhava", "kevala"]


def to_leitan5(lbl):
    if lbl in DETERMINATIVE:      # tatpurusha ∪ karmadharaya ∪ dvigu
        return "tatpurusha"
    if lbl == "unclear":
        return "kevala"           # residual / undeterminable ≈ kevala-samāsa bucket
    return lbl                    # bahuvrihi | dvandva | avyayibhava


def cohen_kappa(pairs, labels):
    """pairs: list of (a, b). Returns (po, pe, kappa, n)."""
    n = len(pairs)
    if n == 0:
        return None, None, None, 0
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    pe = sum((ca.get(l, 0) / n) * (cb.get(l, 0) / n) for l in labels)
    kappa = (po - pe) / (1 - pe) if pe != 1 else 1.0
    return po, pe, kappa, n


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: sg_wf_008_kappa.py PASS_A.json PASS_B.json")
        return 1
    a = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    b = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    ids = sorted(set(a) & set(b))
    missing_a = sorted(set(b) - set(a))
    missing_b = sorted(set(a) - set(b))

    pairs = [(a[i].strip().lower(), b[i].strip().lower()) for i in ids]

    # full 7-way
    po, pe, kappa, n = cohen_kappa(pairs, LABELS)

    # confusion matrix
    conf = defaultdict(Counter)
    for x, y in pairs:
        conf[x][y] += 1

    # collapsed binary (drop rows where either side is 'unclear')
    def coll(lbl):
        if lbl in DETERMINATIVE:
            return "det"
        if lbl in NON_DET:
            return "nondet"
        return "unclear"
    bin_pairs = [(coll(x), coll(y)) for x, y in pairs
                 if coll(x) != "unclear" and coll(y) != "unclear"]
    bpo, bpe, bkappa, bn = cohen_kappa(bin_pairs, ["det", "nondet"])
    unclear_either = sum(1 for x, y in pairs if coll(x) == "unclear" or coll(y) == "unclear")

    # Leitan / Pāṇinian 5-class top level — the codebook headline (MG ruling)
    l5_pairs = [(to_leitan5(x), to_leitan5(y)) for x, y in pairs]
    l5po, l5pe, l5kappa, l5n = cohen_kappa(l5_pairs, LEITAN5)

    dist_a = Counter(x for x, _ in pairs)
    dist_b = Counter(y for _, y in pairs)

    # write matrix
    with open(DATA / "agreement_matrix.tsv", "w", encoding="utf-8") as f:
        f.write("A\\B\t" + "\t".join(LABELS) + "\ttotal_A\n")
        for x in LABELS:
            row = [str(conf[x].get(y, 0)) for y in LABELS]
            f.write(x + "\t" + "\t".join(row) + "\t" + str(sum(conf[x].values())) + "\n")
        f.write("total_B\t" + "\t".join(str(dist_b.get(y, 0)) for y in LABELS) + "\t" + str(n) + "\n")

    def interp(k):
        if k is None:
            return "n/a"
        if k < 0.20:
            return "slight"
        if k < 0.40:
            return "fair"
        if k < 0.60:
            return "moderate"
        if k < 0.80:
            return "substantial"
        return "almost perfect"

    summary = {
        "study": "SG-WF-008 pilot P4: inter-annotator κ on samāsa type",
        "passes": {"A": Path(sys.argv[1]).name, "B": Path(sys.argv[2]).name,
                   "A_model": "Opus 4.8 (claude-opus-4-8)",
                   "B_model": "Sonnet 4.6 (claude-sonnet-4-6)"},
        "n_compared": n,
        "missing_in_A": missing_a,
        "missing_in_B": missing_b,
        "full_7way": {
            "observed_agreement": round(po, 4) if po is not None else None,
            "expected_agreement": round(pe, 4) if pe is not None else None,
            "cohen_kappa": round(kappa, 4) if kappa is not None else None,
            "landis_koch": interp(kappa),
        },
        "leitan_5class": {
            "codebook": ("Edgar Leitan / Pāṇinian-Mahābhāṣya (MG ruling 15-07-2026): 5 top "
                         "classes tatpuruṣa·bahuvrīhi·dvandva·avyayībhāva·kevala; "
                         "dvigu ⊂ karmadhāraya ⊂ tatpuruṣa fold up into tatpuruṣa"),
            "n": l5n,
            "observed_agreement": round(l5po, 4) if l5po is not None else None,
            "expected_agreement": round(l5pe, 4) if l5pe is not None else None,
            "cohen_kappa": round(l5kappa, 4) if l5kappa is not None else None,
            "landis_koch": interp(l5kappa),
            "note": ("this is the codebook headline; most 7-way disagreement is the "
                     "tatpuruṣa↔karmadhāraya sub-boundary, which is INTERNAL to one Leitan "
                     "class and vanishes here"),
        },
        "collapsed_determinative_binary": {
            "definition": "det = tatpurusha|karmadharaya|dvigu ; nondet = dvandva|bahuvrihi|avyayibhava",
            "n_after_dropping_unclear": bn,
            "unclear_either_pass": unclear_either,
            "observed_agreement": round(bpo, 4) if bpo is not None else None,
            "cohen_kappa": round(bkappa, 4) if bkappa is not None else None,
            "landis_koch": interp(bkappa),
        },
        "label_distribution": {
            "pass_A": {k: dist_a.get(k, 0) for k in LABELS},
            "pass_B": {k: dist_b.get(k, 0) for k in LABELS},
        },
        "kill_gate": {
            "rule": ("C5 § 7 P4: inter-annotator κ of two independent passes < 0.7 → "
                     "the type taxonomy is revised before publishing type frequencies"),
            "leitan_5class_kappa": round(l5kappa, 4) if l5kappa is not None else None,
            "full_7way_kappa": round(kappa, 4) if kappa is not None else None,
            "fired_at_codebook_level": (l5kappa is not None and l5kappa < 0.70),
            "fired_at_7way_level": (kappa is not None and kappa < 0.70),
            "primary": ("codebook = Leitan 5-class; 7-way reported to localise where "
                        "agreement breaks (the tatpuruṣa↔karmadhāraya sub-boundary)"),
        },
        "caveat": ("both passes are LLM annotators (Opus + Sonnet) sharing training bias; "
                   "κ is an UPPER bound on two-human agreement, not a lower bound"),
    }
    (DATA / "kappa_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"compared {n} compounds (A missing {len(missing_a)}, B missing {len(missing_b)})")
    print(f"full 7-way: po={po:.3f} pe={pe:.3f} κ={kappa:.3f} ({interp(kappa)})")
    print(f"Leitan 5-class (codebook): po={l5po:.3f} κ={l5kappa:.3f} ({interp(l5kappa)})")
    print(f"determinative binary: n={bn} po={bpo:.3f} κ={bkappa:.3f} ({interp(bkappa)}); "
          f"unclear-either {unclear_either}")
    print(f"pass A dist: {dict(dist_a.most_common())}")
    print(f"pass B dist: {dict(dist_b.most_common())}")
    kg = summary["kill_gate"]
    print(f"KILL-GATE codebook(5-class) {'FIRED' if kg['fired_at_codebook_level'] else 'not fired'} "
          f"(κ={l5kappa:.3f}); 7-way {'FIRED' if kg['fired_at_7way_level'] else 'not fired'} (κ={kappa:.3f})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
