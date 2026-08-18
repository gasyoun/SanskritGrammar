#!/usr/bin/env python
"""apte_pada_preverb_stats.py -- extend the H1081 voice instrument
(apte_pada_stats.py) from root-default pada (APT-26..29) to the fine
preverb-conditioned voice rules of Apte lessons 29-30 (H1090 followup 2b,
zan-29 / H3113).

zan-29's escalation note (review sheet sanskritgrammar-metodichka-apte-v1_17.07.26)
said the fine rules split into two separately-extractable layers:

  1. P/A itself is recoverable from the observed finite-present ending, EVEN
     for preverb-compound lemmas -- DCS's `lemma` field already encodes the
     preverb (e.g. lemma 'saMgam' for sam+gam, 'vinI' for vi+nI). This script
     runs the same ending classifier as apte_pada_stats.py, but keyed on the
     preverb-compound lemma instead of the bare root.
  2. The SENSE condition Apte adds ('when duration is implied', 'in the sense
     protect/rule', 'if transitive') is NOT tagged in DCS. Where the sense
     condition is transitivity, this script uses the sparse UD-style
     dependency layer (deprel='obj'/'iobj' with head==this token) as an
     approximate signal and reports it only when the classified subset is
     large enough to mean anything -- most preverb+root pairs turn out too
     thin for this (see MIN_N_TRANS below); that thinness is itself the
     finding, not a bug in the method.
  Sense conditions that are NOT transitivity (a specific gloss like 'worship',
  'practice' vs 'resemble', 'protect/rule') have NO DCS signal at all and stay
  UNTESTABLE -- this script does not attempt them from the treebank. See
  apte_pada_preverb_sense_spotcheck.md for a manual Russian-corpus spot-check
  of a sample of those forms instead.

CORRECTION over apte_pada_stats.py (H3113 hand spot-check, 18-08-2026): several
preverb-compound lemmas (bhuj, upasthā, vikrī, bodhay) have a substantial share
of -ya- PASSIVE present forms (bhujyate, upasthīyate, vikrīyate, bodhyate) whose
endings are indistinguishable from Ātmanepada endings by ending-shape alone, but
which DCS DOES separately tag via feat_voice='Pass'. The original apte_pada_stats.py
does not filter these out, which silently inflates the 'Ā' bucket for lemmas with
many passive attestations. This script filters feat_voice='Pass' before
classifying -- a genuine methodological tightening, not a divergence in scope.

Usage:  python ApteSyntax_1885/apte_pada_preverb_stats.py [--db PATH]
Writes  apte_pada_preverb_stats.json + apte_pada_preverb_stats.csv next to
this script.
"""
import argparse
import csv
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"

A_END = re.compile(r"(nte|ante|ate|mahe|vahe|dhve|ethe|āte|ete|se|te|e)$")
P_END = re.compile(r"(anti|nti|masi|mas|vas|tha|thas|tas|ti|si|mi)$")
MIN_N = 40           # below this -> UNTESTABLE-thin for pure P/A split
MIN_N_TRANS = 15      # below this -> transitivity split not reported
DECISIVE = 0.80
LEAN = 0.60

# rule id -> (harvest id, expected pada / condition prose, lemma list,
#             transitivity-relevant?, sense condition beyond transitivity?)
RULES = [
    dict(id="APT-H-601", root="kram", lemmas=["kram"], expected="A",
         condition="duration/intensity/increase implied", trans=False,
         sense_only=True),
    dict(id="APT-H-603", root="sam+gam", lemmas=["saṃgam"], expected="A",
         condition="sense 'associate/join with'", trans=False, sense_only=True),
    dict(id="APT-H-604", root="ud+car", lemmas=["uccar"], expected="A",
         condition="transitive", trans=True, sense_only=False),
    dict(id="APT-H-605", root="vi/parā+ji", lemmas=["viji", "parāji"], expected="A",
         condition="sense 'conquer/rout'", trans=False, sense_only=True),
    dict(id="APT-H-606", root="vi/ud+tap", lemmas=["vitap", "uttap"], expected="A",
         condition="intransitive / body-part object", trans=True, sense_only=False),
    dict(id="APT-H-607", root="nī (bare/ud/upa/vi)", lemmas=["nī", "unnī", "upanī", "vinī"],
         expected="A", condition="no prefix, or +ud/upa/vi", trans=False, sense_only=False),
    dict(id="APT-H-608", root="vi+nī", lemmas=["vinī"], expected="P",
         condition="sense 'teach/train/tame' (exception to APT-H-607's own vi+nī row)",
         trans=False, sense_only=True),
    dict(id="APT-H-610", root="upa+sthā", lemmas=["upasthā"], expected="A",
         condition="sense 'worship/wait upon a deity'", trans=False, sense_only=True),
    dict(id="APT-H-611", root="anu+hṛ", lemmas=["anuhṛ"], expected="A",
         condition="sense 'practice' (A) vs 'resemble' (P) -- two senses, one lemma",
         trans=False, sense_only=True),
    dict(id="APT-H-613", root="sam+śru", lemmas=["saṃśru"], expected="split",
         condition="Parasmaipada if transitive, Ātmanepada if intransitive",
         trans=True, sense_only=False),
    dict(id="APT-H-614", root="bhuj", lemmas=["bhuj"], expected="A",
         condition="except sense 'protect/rule' -> P", trans=False, sense_only=True),
    dict(id="APT-H-615", root="pra/upa+yuj", lemmas=["prayuj", "upayuj"], expected="A",
         condition="except re sacrificial vessels", trans=False, sense_only=True),
    dict(id="APT-H-616", root="jñā (desiderative)", lemmas=["jijñās"], expected="A",
         condition="desiderative stem only -- no sense condition", trans=False, sense_only=False),
    dict(id="APT-H-617", root="causatives of budh/yudh/naś/jan/i+adhi/dru/sru",
         lemmas=["bodhay", "yodhay", "nāśay", "janay", "adhyāpay", "drāvay", "srāvay"],
         expected="P", condition="none -- pure lexical list, no sense condition",
         trans=False, sense_only=False),
    dict(id="APT-H-619", root="pari/vi/ava+krī", lemmas=["parikrī", "vikrī", "avakrī"],
         expected="A", condition="sense 'buy' (inherent to krī)", trans=False, sense_only=True),
]


def classify(cur, lemma):
    rows = cur.execute(
        """SELECT id, m_unsandhied FROM token
           WHERE lemma=? AND upos='VERB' AND feat_tense='Pres'
             AND feat_verbform IS NULL AND m_unsandhied IS NOT NULL
             AND (feat_voice IS NULL OR feat_voice != 'Pass')""", (lemma,)).fetchall()
    P = A = other = 0
    p_ids, a_ids = [], []
    for tid, f in rows:
        f = (f or "").strip().lower()
        if not f:
            other += 1
        elif A_END.search(f):
            A += 1
            a_ids.append(tid)
        elif P_END.search(f):
            P += 1
            p_ids.append(tid)
        else:
            other += 1
    n = P + A
    return {"finite_pres": len(rows), "P": P, "A": A, "unclassified": other,
            "P_pct": round(100 * P / n, 1) if n else None,
            "A_pct": round(100 * A / n, 1) if n else None, "n_classified": n,
            "p_ids": p_ids, "a_ids": a_ids}


def observed_pada(c):
    n = c["n_classified"]
    if n < MIN_N:
        return None
    ppc = c["P"] / n
    if ppc >= DECISIVE:
        return "P"
    if (1 - ppc) >= DECISIVE:
        return "A"
    if LEAN <= ppc < DECISIVE:
        return "P-lean"
    if LEAN <= (1 - ppc) < DECISIVE:
        return "A-lean"
    return "both"


def transitivity_split(cur, ids):
    """For a set of token ids, count how many have a direct dependent
    (deprel obj/iobj, head==this token's id) -- an approximate transitivity
    signal. Returns (n_with_obj, n_total_checked) or None if ids is empty."""
    if not ids:
        return None
    n_obj = 0
    for tid in ids:
        row = cur.execute(
            "SELECT COUNT(*) FROM token WHERE head=? AND deprel IN ('obj','iobj')",
            (tid,)).fetchone()
        if row[0] > 0:
            n_obj += 1
    return n_obj, len(ids)


def verdict(expected, observed, c):
    if observed is None:
        return "UNTESTABLE-thin", f"<{MIN_N} classified present forms (n={c['n_classified']})"
    obs_base = observed.replace("-lean", "")
    if expected == "split":
        return "MIXED-observed", f"P{c['P_pct']}%/A{c['A_pct']}% (n={c['n_classified']}) -- consistent with a real P/A split, but DCS cannot attribute which occurrences are transitive vs intransitive at scale"
    if obs_base == expected:
        strong = "-lean" not in observed
        return ("TRUE" if strong else "TRUE-lean"), f"expected {expected}-dominant; observed {observed} (P{c['P_pct']}%/A{c['A_pct']}%, n={c['n_classified']})"
    return "OVERSTATED", f"expected {expected}-dominant; observed {observed} (P{c['P_pct']}%/A{c['A_pct']}%, n={c['n_classified']})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    results = []
    for rule in RULES:
        merged = {"finite_pres": 0, "P": 0, "A": 0, "unclassified": 0, "p_ids": [], "a_ids": []}
        per_lemma = {}
        for lem in rule["lemmas"]:
            c = classify(cur, lem)
            per_lemma[lem] = {k: v for k, v in c.items() if k not in ("p_ids", "a_ids")}
            merged["finite_pres"] += c["finite_pres"]
            merged["P"] += c["P"]
            merged["A"] += c["A"]
            merged["unclassified"] += c["unclassified"]
            merged["p_ids"] += c["p_ids"]
            merged["a_ids"] += c["a_ids"]
        n = merged["P"] + merged["A"]
        merged["n_classified"] = n
        merged["P_pct"] = round(100 * merged["P"] / n, 1) if n else None
        merged["A_pct"] = round(100 * merged["A"] / n, 1) if n else None

        obs = observed_pada(merged)
        v, reason = verdict(rule["expected"], obs, merged)

        trans_note = None
        if rule["trans"]:
            all_ids = merged["p_ids"] + merged["a_ids"]
            tsplit = transitivity_split(cur, all_ids)
            if tsplit and tsplit[1] >= MIN_N_TRANS:
                n_obj, n_tot = tsplit
                trans_note = f"{n_obj}/{n_tot} classified occurrences ({round(100*n_obj/n_tot,1)}%) have a DCS obj/iobj dependent (approximate transitivity signal)"
            else:
                trans_note = f"transitivity check too thin to report (n={tsplit[1] if tsplit else 0} < {MIN_N_TRANS})"

        results.append({
            "id": rule["id"], "root": rule["root"], "lemmas": rule["lemmas"],
            "expected": rule["expected"], "condition": rule["condition"],
            "sense_only": rule["sense_only"],
            "per_lemma": per_lemma,
            "P": merged["P"], "A": merged["A"], "P_pct": merged["P_pct"], "A_pct": merged["A_pct"],
            "n_classified": n, "observed_pada": obs, "verdict": v, "reason": reason,
            "transitivity_note": trans_note,
        })

    out_json = HERE / "apte_pada_preverb_stats.json"
    out_json.write_text(json.dumps({"instrument": "apte_pada_preverb_stats.py -- H3113 (zan-29) "
                                     "preverb-conditioned voice extraction, extends apte_pada_stats.py",
                                     "rules": results}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    out_csv = HERE / "apte_pada_preverb_stats.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "root", "lemmas", "expected", "P", "A", "P_pct", "A_pct",
                    "n_classified", "observed_pada", "verdict", "sense_only", "transitivity_note", "reason"])
        for r in results:
            w.writerow([r["id"], r["root"], "|".join(r["lemmas"]), r["expected"], r["P"], r["A"],
                        r["P_pct"], r["A_pct"], r["n_classified"], r["observed_pada"], r["verdict"],
                        r["sense_only"], r["transitivity_note"] or "", r["reason"]])

    print("id".ljust(12), "root".ljust(30), "P".rjust(5), "A".rjust(5), "n".rjust(6), "verdict")
    for r in results:
        print(r["id"].ljust(12), r["root"][:30].ljust(30), str(r["P"]).rjust(5), str(r["A"]).rjust(5),
              str(r["n_classified"]).rjust(6), r["verdict"])
    print(f"-> {out_json.name} + {out_csv.name} written")


if __name__ == "__main__":
    main()
