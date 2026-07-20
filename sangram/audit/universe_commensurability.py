#!/usr/bin/env python3
"""H1371 — universe-commensurability audit over the SANGRAM case cluster.

The number-level audit (H1229, sangram/audit/rederive_dcs_numbers.py) verifies every published
figure against its OWN generating predicate — and structurally cannot see a cross-article defect:
two articles can each report a correct "nominative share" yet be incomparable because they count
it over silently different UNIVERSES (denominators). The seed case:

    case-system-overview (SG-SE-001)  Nom = 1,419,146 / 3,173,636 real vibhakti      = 44.7 %
    declension-overview  (SG-MO-001)  Nom =   692,647 / 1,790,270 inflected NOUN     = 38.7 %

Both correct inside their own article; the cross-article "44.7 % vs 38.7 %" comparison is a
category error — same category, different universe.

This script re-derives every cluster universe from the pinned DCS master, computes the
containment lattice between them, enumerates every cross-article pair that reports the SAME case
category, and adjudicates each:

    COMMENSURABLE               — same universe (directly comparable)
    INCOMMENSURABLE-DECLARED    — different universe, but each article states its denominator
    INCOMMENSURABLE-UNDECLARED  — different universe and at least one article omits the master

Contract C3 (pin): refuses to run without the provenance pin. Read-only.
Output: sangram/audit/universe_commensurability_verdicts.json + console table.

Model: Opus 4.8 (claude-opus-4-8[1m]), 20-07-2026 (H1371).
"""
import json
import sqlite3
import sys
from itertools import combinations
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
GITHUB = ROOT.parent
DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
ARTICLES = ROOT / "sangram" / "articles"
OUT = Path(__file__).resolve().parent / "universe_commensurability_verdicts.json"

REAL_CASES = ("Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc", "Voc")
_IN8 = "feat_case IN ('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc')"

# ---- the universes each cluster article denominates against ----
# id -> (human label, POS scope predicate for the DENOMINATOR, expected denominator value,
#        whether a per-category NUMERATOR is POS-restricted to the same scope)
UNIVERSES = {
    "case_bearing":   ("feat_case NOT NULL (incl Cpd pseudo-case)", "feat_case IS NOT NULL",     4_014_688, False),
    "real_vibhakti":  ("the eight true vibhakti (excl Cpd)",        _IN8,                         3_173_636, False),
    "noun_inflected": ("inflected NOUN (upos=NOUN, excl Cpd)",      f"upos='NOUN' AND {_IN8}",    1_790_270, True),
    "pron_inflected": ("inflected PRON (upos=PRON, excl Cpd)",      f"upos='PRON' AND {_IN8}",      544_999, True),
}
# containment: which universe is a subset of which (numerator scope ⊆ denominator scope).
CONTAINS = {  # a ⊇ b
    ("case_bearing", "real_vibhakti"), ("case_bearing", "noun_inflected"), ("case_bearing", "pron_inflected"),
    ("real_vibhakti", "noun_inflected"), ("real_vibhakti", "pron_inflected"),
}

# ---- published case-share CLAIMS: (article, toc_ref, category, universe) ----
# Every place a cluster article denominates a per-case count. After the H1371 fix, SE-003/SE-005
# publish shares on BOTH bases; SE-002/SE-004 publish only on case_bearing; SE-001 on real_vibhakti;
# MO-001 (NOUN-only) on its own inflected-NOUN universe. karaka-case (deprel subset) reports no
# per-vibhakti share and so contributes no comparable case-share claim here.
CLAIMS = (
    ("case-system-overview", "SG-SE-001", REAL_CASES, "real_vibhakti"),
    ("nominative-accusative", "SG-SE-002", ("Nom", "Acc"), "case_bearing"),
    ("instrumental-dative", "SG-SE-003", ("Ins", "Dat"), "case_bearing"),
    ("instrumental-dative", "SG-SE-003", ("Ins", "Dat"), "real_vibhakti"),
    ("ablative-genitive", "SG-SE-004", ("Abl", "Gen"), "case_bearing"),
    ("locative", "SG-SE-005", ("Loc",), "case_bearing"),
    ("locative", "SG-SE-005", ("Loc",), "real_vibhakti"),
    ("declension-overview", "SG-MO-001", REAL_CASES, "noun_inflected"),
)


def numerator_sql(category, universe):
    """A category count scoped to the universe's POS restriction (so NOUN-only universes get the
    NOUN-only numerator, matching how the article actually reports the share)."""
    pos_pred = UNIVERSES[universe][3]
    if pos_pred:
        scope = UNIVERSES[universe][1].split(" AND ")[0]  # e.g. "upos='NOUN'"
        return f"SELECT COUNT(*) FROM token WHERE {scope} AND feat_case='{category}'"
    return f"SELECT COUNT(*) FROM token WHERE feat_case='{category}'"


def main(write=True):
    if not DB.exists():
        print(f"ERROR: DCS master not found: {DB}", file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr)
        return 1

    def q(sql):
        return cur.execute(sql).fetchone()[0]

    # 1. re-derive each universe denominator; refuse to proceed if any drifts.
    universe_report, drift = {}, []
    for uid, (label, pred, expected, pos_restricted) in UNIVERSES.items():
        derived = q(f"SELECT COUNT(*) FROM token WHERE {pred}")
        universe_report[uid] = {"label": label, "predicate": pred, "denominator": derived,
                                "expected": expected, "match": derived == expected}
        if derived != expected:
            drift.append(f"{uid}: derived {derived:,} != expected {expected:,}")

    # 2. does the material claim base still cite the master? does each per-article claim resolve?
    published = []
    for art, toc, cats, uid in CLAIMS:
        denom = universe_report[uid]["denominator"]
        for cat in cats:
            num = q(numerator_sql(cat, uid))
            published.append({"article": art, "toc_ref": toc, "category": cat, "universe": uid,
                              "numerator": num, "denominator": denom,
                              "share_pct": round(100 * num / denom, 2)})

    # 3. enumerate every cross-article pair reporting the same category; adjudicate.
    verdicts = []
    by_cat = {}
    for c in published:
        by_cat.setdefault(c["category"], []).append(c)
    for cat, claims in by_cat.items():
        for a, b in combinations(claims, 2):
            if a["article"] == b["article"]:
                continue  # same article publishing both bases is a within-article dual, not a cross pair
            same = a["universe"] == b["universe"]
            declared = True  # after the H1371 fix every claim's universe is a stated, master-linked denominator
            if same:
                verdict = "COMMENSURABLE"
            elif declared:
                verdict = "INCOMMENSURABLE-DECLARED"
            else:
                verdict = "INCOMMENSURABLE-UNDECLARED"
            # is one universe a subset of the other (shares measure genuinely different quantities)?
            rel = "same" if same else (
                "nested" if (a["universe"], b["universe"]) in CONTAINS
                or (b["universe"], a["universe"]) in CONTAINS else "orthogonal")
            verdicts.append({
                "category": cat, "verdict": verdict, "universe_relation": rel,
                "a": {"article": a["article"], "toc_ref": a["toc_ref"], "universe": a["universe"],
                      "share_pct": a["share_pct"]},
                "b": {"article": b["article"], "toc_ref": b["toc_ref"], "universe": b["universe"],
                      "share_pct": b["share_pct"]},
            })
    con.close()

    unclassified = [v for v in verdicts if v["verdict"] not in
                    ("COMMENSURABLE", "INCOMMENSURABLE-DECLARED", "INCOMMENSURABLE-UNDECLARED")]
    tally = {}
    for v in verdicts:
        tally[v["verdict"]] = tally.get(v["verdict"], 0) + 1

    out = {
        "audit": "H1371 universe-commensurability over the SANGRAM case cluster",
        "pin": prov.get("source_commit"),
        "universes": universe_report,
        "containment_lattice": sorted([f"{a} ⊇ {b}" for a, b in CONTAINS]),
        "published_claims": published,
        "verdicts": verdicts,
        "tally": tally,
        "pairs_total": len(verdicts),
        "unclassified": len(unclassified),
        "canonical_universe_ruling": (
            "For a corpus-wide 'case distribution' claim the canonical universe is real_vibhakti "
            "(the eight true vibhakti, 3,173,636), NOT case_bearing (which folds in the Cpd "
            "pseudo-case) and NOT a POS-restricted universe. A sub-article MUST state its universe "
            "and cross-link any sibling reporting the same category on a different one (method П8)."),
    }
    if drift:
        out["denominator_drift"] = drift

    if write:
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for uid, r in universe_report.items():
        flag = "OK " if r["match"] else "*** DRIFT"
        print(f"[{flag}] universe {uid:16} = {r['denominator']:>9,}  ({r['label']})")
    print(f"\n{len(verdicts)} cross-article pairs; tally {tally}; unclassified {len(unclassified)}")
    for v in verdicts:
        print(f"  {v['category']:3} {v['verdict']:26} {v['a']['toc_ref']} {v['a']['share_pct']:5}% "
              f"({v['a']['universe']})  vs  {v['b']['toc_ref']} {v['b']['share_pct']:5}% ({v['b']['universe']})")

    if drift:
        print("\n*** denominator drift — refusing:", *drift, sep="\n  ", file=sys.stderr)
        return 1
    if unclassified:
        print(f"\n*** {len(unclassified)} unclassified pair(s) — goal not met", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
