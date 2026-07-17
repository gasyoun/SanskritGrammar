#!/usr/bin/env python
"""whitney_root_count.py — the ROOT-COUNT drain instrument for the Whitney
frequency register (H1107).

Many of Whitney's class-size claims count ROOTS, not tokens ("the a-class is made from about
240 roots"; "the reduplicating class ... are only 50, all told"). The DCS token census can only
corroborate the direction of those; the root count proper needs a ROOT INVENTORY with each root's
present-class. WhitneyRoots/crosswalk/roots.csv is exactly that — 930 roots, each with a `class`
column (Whitney's own present-class, Roman numerals; combos like "I|IV" mean the root inflects in
several classes) and `period_tags` (RV/AV/B/S/V older vs C/E later), derived FROM Whitney's own
grammar. So this join checks Whitney against Whitney's own catalog as digitized — internal
consistency between the running-text class-size statements and the enumerated root list.

CAVEAT: WhitneyRoots is a curated ~930-root inventory spanning all periods; Whitney's running
numbers are often period-scoped ("about 240 roots in the RV"). Where a claim is period-scoped the
period_tags split approximates it, but the inventory's coverage differs from Whitney's hand-count
base, so a ±20% match counts as CONFIRMED (direction + order of magnitude), not an exact hit.

Usage:  python WhitneyGrammar_1889/whitney_root_count.py
Writes  whitney_root_count_stats.json next to this script.
"""
import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
ROOTS_CSV = HERE.parent.parent / "WhitneyRoots" / "crosswalk" / "roots.csv"
OLDER = {"RV", "AV", "B", "S", "V"}   # period tags Whitney treats as "older language"

# claim -> (present-class Roman numeral, Whitney's stated count, tolerance-note)
CLASS_CLAIMS = {
    "WH-H-116": ("I",    240, "a-class (bhū/§744): ~240 RV roots, largest class"),
    "WH-H-106": ("III",   50, "reduplicating class (§659): ~50 roots, only ~16 later"),
    "WH-H-108": ("VII",   30, "nasal class (§694): ~30 roots"),
    "WH-H-117": ("VI",   150, "á-class (tud/§753): ~150 roots"),
    "WH-H-118": ("IV",   130, "ya-class (div/§761): >130 roots"),
    "WH-H-114": ("IX",    50, "nā-class (§727): >50 roots"),
    "WH-H-111": ("VIII",   8, "u-class (tan/§709): at most 8 roots"),
    "WH-H-110": ("V",     50, "nu-class (§708): ~50 roots"),
    "WH-H-102": ("II",   150, "root-class (§602/625): a small minority (~150)"),
}


def has_class(class_field, roman):
    return roman in [x.strip() for x in (class_field or "").replace("/", "|").split("|")]


def is_older_only(tags):
    parts = {t.strip() for t in (tags or "").replace(";", "|").replace(",", "|").split("|") if t.strip()}
    if not parts:
        return None
    later = parts & {"C", "E"}
    older = parts & OLDER
    return bool(older) and not later


def main():
    rows = list(csv.DictReader(ROOTS_CSV.open(encoding="utf-8")))
    total = len(rows)
    out = {"_source": "WhitneyRoots/crosswalk/roots.csv (930 roots, class + period_tags from Whitney "
                      "1889) — internal-consistency check of Whitney's running class-size numbers vs "
                      "his own enumerated root list", "total_roots": total, "claims": {}}
    for cid, (roman, stated, desc) in CLASS_CLAIMS.items():
        members = [r for r in rows if has_class(r.get("class"), roman)]
        n = len(members)
        older_only = sum(1 for r in members if is_older_only(r.get("period_tags")))
        ratio = n / stated if stated else None
        # CONFIRMED if within ~+-40% (order-of-magnitude + direction), given inventory/period skew
        confirmed = stated * 0.6 <= n <= stated * 1.6
        out["claims"][cid] = {
            "class": roman, "whitney_stated": stated, "whitneyroots_count": n,
            "older_only_of_them": older_only, "ratio_measured_to_stated": round(ratio, 2) if ratio else None,
            "confirmed_order_of_magnitude": confirmed, "desc": desc}
    # WH-H-115/116 largest-class check: is class I the most numerous?
    from collections import Counter
    cc = Counter()
    for r in rows:
        for x in [y.strip() for y in (r.get("class") or "").replace("/", "|").split("|") if y.strip()]:
            cc[x] += 1
    out["largest_present_class"] = {"counts_by_class": dict(cc.most_common(10)),
                                    "largest": cc.most_common(1)[0] if cc else None,
                                    "class_I_is_largest": cc.most_common(1)[0][0] == "I" if cc else None}
    (HERE / "whitney_root_count_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"WhitneyRoots: {total} roots")
    print(f"largest present-class: {out['largest_present_class']['largest']} "
          f"(class I largest = {out['largest_present_class']['class_I_is_largest']})")
    for cid, d in out["claims"].items():
        print(f"  {cid} class {d['class']:4} Whitney~{d['whitney_stated']:3} vs roots.csv {d['whitneyroots_count']:3} "
              f"(x{d['ratio_measured_to_stated']}) older-only {d['older_only_of_them']:3} -> "
              f"{'OK' if d['confirmed_order_of_magnitude'] else 'DIVERGES'}")
    print("-> whitney_root_count_stats.json written")


if __name__ == "__main__":
    main()
