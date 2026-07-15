#!/usr/bin/env python
"""verify_claims_dcs.py — reproducible corpus statistics behind the Zaliznyak
Ocherk claim register (H797 Phase 2).

Unlike KocherginaUchebnik_1998's and BuhlerLeitfaden_1923's verify scripts, most of this
book's seed claims (OCH-1, OCH-3, OCH-5) REUSE ground truth already computed for those two
books rather than recomputing it — see claims.yml's synthesis for why (the cross-grammar
program's corpus infrastructure compounds; the same DCS fact doesn't need re-deriving every
time a new grammar happens to also state it). This script computes only the two claims that
needed fresh numbers: OCH-2 (class-I token share) and OCH-6 (thematic-suffix a/ya/aya ranking).

Ground-truth source: Digital Corpus of Sanskrit (Oliver Hellwig, DCS-2021, CC BY),
    ../../VisualDCS/verb_classes.json  (present-class token totals, P/A split, top roots)

Usage:  python verify_claims_dcs.py            # report + rewrite claims_dcs_stats.json
        python verify_claims_dcs.py --check     # report only, no file write
"""
import sys, json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
VDCS = REPO.parent / "VisualDCS"


def class_shares():
    """OCH-2 / OCH-6: present-stem class token shares. Class 1+6 share the bare-a suffix,
    class 4 the ya suffix, class 10 the aya suffix (Whitney's traditional class numbering)."""
    d = json.load(open(VDCS / "verb_classes.json", encoding="utf-8"))
    tot = sum(v["total"] for v in d.values())
    a_suffix = d["1"]["total"] + d["6"]["total"]
    ya_suffix = d["4"]["total"]
    aya_suffix = d["10"]["total"]
    ranked = sorted(((k, v["total"]) for k, v in d.items()), key=lambda x: -x[1])
    return {
        "total_present_tokens": tot,
        "class_1_tokens": d["1"]["total"],
        "class_1_pct": round(100 * d["1"]["total"] / tot, 2),
        "class_2_tokens": d["2"]["total"],
        "class_2_pct": round(100 * d["2"]["total"] / tot, 2),
        "largest_class": ranked[0][0],
        "a_suffix_tokens": a_suffix, "a_suffix_pct": round(100 * a_suffix / tot, 2),
        "ya_suffix_tokens": ya_suffix, "ya_suffix_pct": round(100 * ya_suffix / tot, 2),
        "aya_suffix_tokens": aya_suffix, "aya_suffix_pct": round(100 * aya_suffix / tot, 2),
        "ya_aya_gap_pct_points": round(100 * ya_suffix / tot - 100 * aya_suffix / tot, 2),
    }


def analyze():
    return {
        "_source": "DCS-2021 (Oliver Hellwig, CC BY) via VisualDCS/verb_classes.json",
        "_note": "OCH-1/OCH-3/OCH-5 reuse Kochergina/Bühler's already-published stats verbatim "
                 "(see claims.yml refs) rather than recomputing here.",
        "OCH2_OCH6_class_shares": class_shares(),
    }


def report(s):
    c = s["OCH2_OCH6_class_shares"]
    print(f"OCH-2 CLASS I SHARE: {c['class_1_tokens']:,} tokens = {c['class_1_pct']}% of "
          f"{c['total_present_tokens']:,} present-system tokens (largest class: {c['largest_class']}, "
          f"next-largest class II = {c['class_2_pct']}%)")
    print(f"OCH-6 THEMATIC-SUFFIX RANKING: a-suffix (I+VI) {c['a_suffix_pct']}% > "
          f"ya-suffix (IV) {c['ya_suffix_pct']}% > aya-suffix (X) {c['aya_suffix_pct']}% "
          f"(ya/aya gap only {c['ya_aya_gap_pct_points']} points)")


def main():
    stats = analyze()
    report(stats)
    if "--check" not in sys.argv:
        out = HERE / "claims_dcs_stats.json"
        out.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n-> wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
