#!/usr/bin/env python3
"""H1229: recompute the SG-WF-008/009 kappa + label-mix numbers from the
committed double-annotation TSV (sangram/articles/tatpurusha/data/
annotations_full.tsv). No DCS access needed — this checks the published
inter-annotator statistics against their own raw annotations.

Published values under audit:
  tatpurusha:81  coarse kappa 0.929 [0.836-1.000], n=120, agreement 117/120
  tatpurusha:87  agreed mix: tatpurusa 93, bahuvrihi 17, dvandva 6, unclear 1
  tatpurusha:103 fine kappa 0.720 [0.602-0.817], n=93, agreement 73/93
  bahuvrihi:77   combined 240 labels: tp 189, bv 36, dv 13, unclear 2
  bahuvrihi:78   both-passes-agree bahuvrihi: 17
  compounds-overview:81 restates the same study
"""
import csv
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

TSV = (Path(__file__).resolve().parents[2] / "sangram" / "articles" / "tatpurusha"
       / "data" / "annotations_full.tsv")


def cohen_kappa(pairs):
    n = len(pairs)
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / n
    ca, cb = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    pe = sum(ca[k] * cb.get(k, 0) for k in ca) / (n * n)
    k = (po - pe) / (1 - pe) if pe < 1 else 1.0
    return k, agree, n


def main():
    rows = list(csv.DictReader(open(TSV, encoding="utf-8"), delimiter="\t"))
    a = {r["cpd_token_id"]: r for r in rows if r["pass"] == "A"}
    b = {r["cpd_token_id"]: r for r in rows if r["pass"] == "B"}
    ids = sorted(set(a) & set(b))
    print(f"pass A: {len(a)}  pass B: {len(b)}  paired: {len(ids)}")

    coarse = [(a[i]["coarse"], b[i]["coarse"]) for i in ids]
    k, agree, n = cohen_kappa(coarse)
    print(f"coarse kappa = {k:.3f}  agreement {agree}/{n}   "
          f"(published 0.929, 117/120)")

    agreed = [a[i]["coarse"] for i in ids if a[i]["coarse"] == b[i]["coarse"]]
    print(f"agreed mix: {Counter(agreed)}   "
          "(published tatpurusa 93, bahuvrihi 17, dvandva 6, unclear 1)")

    tp_ids = [i for i in ids if a[i]["coarse"] == b[i]["coarse"] == "tatpurusa"]
    fine = [(a[i]["fine"], b[i]["fine"]) for i in tp_ids]
    k2, agree2, n2 = cohen_kappa(fine)
    print(f"fine kappa (tatpurusa subset) = {k2:.3f}  agreement {agree2}/{n2}   "
          f"(published 0.720, 73/93)")

    all_labels = Counter(r["coarse"] for r in rows)
    print(f"combined 240 labels: {all_labels}   "
          "(published tp 189, bv 36, dv 13, unclear 2)")

    bv_agree = sum(1 for i in ids if a[i]["coarse"] == b[i]["coarse"] == "bahuvrihi")
    print(f"both-agree bahuvrihi: {bv_agree}   (published 17)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
