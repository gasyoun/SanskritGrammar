#!/usr/bin/env python
"""two_grade_root_vowel_check.py — root-vowel check for HK-88.

HK-88 claims: roots with only two ablaut grades (неполноизменяемый /
"defective" in this programme's terminology — weak and guṇa coincide, or
one grade is simply unattested) are usually roots with the vowel -a-
(i.e. ablaut series A₁/A₂), as opposed to I/U/R/L/M/N series roots.

REUSES EXISTING DATA, no new corpus query: the morphoclass crosswalk CSV
(TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv)
already carries `ryad_1978` (ablaut series, per Zaliznyak's own §66 rules)
and `polnoizm_1978` (full/defective/fluctuating alternation-grade status)
for 876 roots — built earlier today (H978/build_1978_crosswalk.py) for a
different claim (OCH-21..23) but directly answers this one too.

Usage:  python KocherginaUchebnik_1998/two_grade_root_vowel_check.py
Writes  hk88_two_grade_root_vowel_stats.json next to this script.
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
CROSSWALK = (HERE.parent / "TolchelnikovTalmud_2026" / "data"
             / "morphoclass_crosswalk_1975_2014_2026.csv")


def family(ryad):
    return ryad.rstrip("₁₂?") if ryad else None


def main():
    rows = list(csv.DictReader(CROSSWALK.open(encoding="utf-8")))
    defective = [r for r in rows if r["polnoizm_1978"] == "defective"]
    full = [r for r in rows if r["polnoizm_1978"] == "full"]

    def fam_counts(subset):
        return Counter(family(r["ryad_1978"]) for r in subset)

    def_fam = fam_counts(defective)
    full_fam = fam_counts(full)

    def_a = def_fam.get("A", 0)
    full_a = full_fam.get("A", 0)

    out = {
        "instrument": "two_grade_root_vowel_check.py — reuses the H978 morphoclass "
                      "crosswalk (ryad_1978 + polnoizm_1978), no new corpus query",
        "total_roots": len(rows),
        "defective_roots": {
            "n": len(defective), "by_ryad_family": dict(def_fam),
            "A_series_count": def_a,
            "A_series_share_pct": round(100 * def_a / len(defective), 1) if defective else None,
        },
        "full_alternating_roots": {
            "n": len(full), "by_ryad_family": dict(full_fam),
            "A_series_count": full_a,
            "A_series_share_pct": round(100 * full_a / len(full), 1) if full else None,
        },
        "expected_by_hk88": "A-series share among defective roots >> A-series share among full-alternating roots",
        "confirmed": def_a / len(defective) > full_a / len(full) if defective and full else None,
    }
    (HERE / "hk88_two_grade_root_vowel_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"defective roots: {len(defective)}, A-series: {def_a} "
          f"({out['defective_roots']['A_series_share_pct']}%)")
    print(f"full-alternating roots: {len(full)}, A-series: {full_a} "
          f"({out['full_alternating_roots']['A_series_share_pct']}%)")
    print("confirmed:", out["confirmed"])
    print("-> hk88_two_grade_root_vowel_stats.json written")


if __name__ == "__main__":
    main()
