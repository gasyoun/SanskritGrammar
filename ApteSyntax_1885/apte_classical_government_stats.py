#!/usr/bin/env python
"""apte_classical_government_stats.py — the Classical-corpus government instrument
for the ApteSyntax_1885 claim register (H1062).

WHY THIS EXISTS. The treebank drain (apte_treebank_stats.py, H1059) confirmed
Apte's PARTICLE-POSITION and AGREEMENT claims but left most CASE-GOVERNMENT
claims UNTESTABLE-thin: the dependency-tagged slice is only 3.9% of the corpus
AND is Vedic-skewed, so Apte's Classical lexeme-specific rules (ruc -> dative,
krudh -> dative, snih -> locative, ...) contribute <10 or zero case-tagged
ARGUMENTS. This instrument escapes both bottlenecks by NOT relying on dependency
tags at all:

  * feat_case is populated on 70.6% of the FULL 5.69M-token corpus (4.01M
    tokens), not just the 3.9% dependency slice.
  * DCS-2021 is overwhelmingly Classical/Epic (Mahābhārata, Rāmāyaṇa, Purāṇas,
    Kāvya, śāstra) — the register Apte actually teaches — so the full corpus is
    already the right genre, unlike the Vedic-skewed treebank slice.

METHOD: windowed cooccurrence + baseline lift (a standard collexeme proxy).
For a government claim "verb-set X governs case Y", find every verbal token of X,
collect the case-bearing NOUN/PRON tokens in the SAME sentence within +-W idx
(excluding Nom/Voc/Cpd — subjects and compounds), and tally their case. Compare
that local distribution against the CORPUS BASELINE oblique-case distribution
(Acc 44.4%, Ins 16.6%, Gen 16.2%, Loc 14.5%, Abl 4.5%, Dat 3.9%). The signal is
LIFT = local_share(Y) / baseline_share(Y): government shows up as a case
enriched near X far above its baseline rate. Lift neutralizes the confound that
a nearby oblique might belong to another head — random confounds sit in the
baseline too; only a SYSTEMATIC association with X survives as lift > 1.

This is a PROXY, not true dependency government (no head edges), so verdicts are
graded conservatively and always with the lift number. Two method controls guard
against reading noise as signal:
  * POSITIVE controls: bhī/jugups -> ablative already came out TRUE on the
    treebank (APT-16/17). If the proxy does NOT reproduce ablative-enrichment for
    them, the proxy is untrustworthy.
  * NEGATIVE control: dṛś 'see', a plain transitive — its neighborhood should
    show NO dative/ablative/genitive enrichment (lift ~1), only the accusative
    object. If dṛś spuriously "governs" the dative, the window is too loose.

Usage:  python ApteSyntax_1885/apte_classical_government_stats.py [--db PATH] [--window N]
Writes  apte_classical_government_stats.json next to this script.
"""
import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"

OBLIQUE = ("Acc", "Ins", "Gen", "Loc", "Abl", "Dat")
EXCLUDE_CASE = ("Nom", "Voc", "Cpd")
MIN_N = 30          # below this local sample -> UNTESTABLE-thin even here
LIFT_STRONG = 1.5   # predicted case enriched >=1.5x baseline -> support
LIFT_TOP_MARGIN = 1.15  # predicted case must also lead / near-lead by lift

# claim -> (verb lemmas, predicted case, description)
GOV_CLAIMS = {
    "APT-H-105": (["ruc"], "Dat", "ruc 'please' -> dative of the pleased (Whitney §287c)"),
    "APT-H-106": (["krudh", "druh", "īrṣy", "asūy"], "Dat", "anger verbs -> dative of the object of anger (Whitney §262)"),
    "APT-H-112": (["snih", "abhilaṣ", "anurañj"], "Loc", "love verbs -> locative of the object of feeling (Whitney §303b)"),
    "APT-H-113": (["kṣip", "muc"], "Loc", "throw verbs -> locative of the target"),
    "APT-H-115": (["īś", "prabhū", "smṛ", "adhī"], "Gen", "rule/remember verbs -> genitive of the object (Whitney §297c)"),
    "APT-H-110": (["jugups", "viram", "pramad"], "Abl", "disgust/cessation -> ablative"),
    "APT-H-111": (["bhī"], "Abl", "fear -> ablative of the source (Whitney §291)"),
}

CONTROLS_POS = {  # should reproduce ablative enrichment (treebank said TRUE)
    "ctrl_bhī_abl": (["bhī"], "Abl"),
    "ctrl_jugups_abl": (["jugups"], "Abl"),
}
CONTROL_NEG = (["dṛś"], "plain transitive — expect NO dat/abl/gen enrichment (lift ~1)")


def baseline_shares(cur):
    rows = cur.execute(
        f"SELECT feat_case, COUNT(*) FROM token WHERE feat_case IN {OBLIQUE} GROUP BY feat_case")
    d = dict(rows)
    tot = sum(d.values())
    return {c: d.get(c, 0) / tot for c in OBLIQUE}, tot


def local_case_tally(cur, lemmas, window):
    """Case tally of NOUN/PRON tokens within +-window idx of a verbal token of
    `lemmas`, in the same sentence, excluding subjects/compounds. Self-join on
    sentence_id (indexed)."""
    qs = ",".join("?" * len(lemmas))
    rows = cur.execute(
        f"""SELECT ch.feat_case, COUNT(*)
            FROM token v JOIN token ch ON ch.sentence_id = v.sentence_id
            WHERE v.lemma IN ({qs}) AND v.upos='VERB'
              AND ch.upos IN ('NOUN','PRON')
              AND ch.feat_case IN {OBLIQUE}
              AND ch.idx <> v.idx AND ABS(ch.idx - v.idx) <= ?
            GROUP BY ch.feat_case""", (*lemmas, window)).fetchall()
    return dict(rows)


def assess(tally, predicted, base):
    n = sum(tally.values())
    shares = {c: tally.get(c, 0) / n for c in OBLIQUE} if n else {}
    lift = {c: (shares.get(c, 0) / base[c]) if base[c] else None for c in OBLIQUE}
    top_case = max(OBLIQUE, key=lambda c: tally.get(c, 0)) if n else None
    top_by_lift = max(OBLIQUE, key=lambda c: (lift[c] or 0)) if n else None
    pred_lift = lift.get(predicted)
    if n < MIN_N:
        verdict = None
        reason = f"UNTESTABLE-thin: only {n} windowed obliques (<{MIN_N})"
    elif pred_lift is not None and pred_lift >= LIFT_STRONG and \
            (top_by_lift == predicted or pred_lift >= (lift[top_by_lift] or 0) / LIFT_TOP_MARGIN):
        verdict = "TRUE"
        reason = f"predicted {predicted} enriched {pred_lift:.2f}x baseline, top-lift oblique"
    elif pred_lift is not None and pred_lift >= LIFT_STRONG:
        verdict = "TRUE-partial"
        reason = f"predicted {predicted} enriched {pred_lift:.2f}x but not the top-lift case ({top_by_lift})"
    else:
        verdict = "OVERSTATED"
        lift_str = f"{pred_lift:.2f}x" if pred_lift is not None else "n/a (0 baseline)"
        reason = f"predicted {predicted} lift {lift_str} — not enriched; top-lift oblique is {top_by_lift}"
    return {
        "n_windowed_obliques": n,
        "case_tally": dict(sorted(tally.items(), key=lambda kv: -kv[1])),
        "local_share_pct": {c: round(100 * shares.get(c, 0), 1) for c in OBLIQUE} if n else {},
        "lift_over_baseline": {c: (round(lift[c], 2) if lift[c] is not None else None) for c in OBLIQUE},
        "predicted_case": predicted, "predicted_lift": round(pred_lift, 2) if pred_lift else None,
        "top_case_by_count": top_case, "top_case_by_lift": top_by_lift,
        "verdict": verdict, "reason": reason,
    }


def self_test():
    """In-memory corpus: verb 'g' governs Dat (its neighbors are dative-heavy);
    baseline is accusative-heavy. Proxy must flag Dat as enriched for 'g'."""
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE token (sentence_id INT, idx INT, lemma TEXT, upos TEXT, feat_case TEXT)")
    rows = []
    # 60 background accusative nouns (baseline) in filler sentences w/o the verb
    for i in range(60):
        rows.append((1000 + i, 1, "x", "NOUN", "Acc"))
    # 40 sentences with verb 'g' (idx 2) and a dative noun (idx 1) next to it
    for i in range(40):
        rows.append((i, 1, "y", "NOUN", "Dat"))
        rows.append((i, 2, "g", "VERB", None))
    db.executemany("INSERT INTO token VALUES (?,?,?,?,?)", rows)
    cur = db.cursor()
    base, _ = baseline_shares(cur)
    tally = local_case_tally(cur, ["g"], 5)
    res = assess(tally, "Dat", base)
    assert res["case_tally"].get("Dat") == 40, res
    assert res["verdict"] == "TRUE" and res["predicted_lift"] > 1.5, res
    # negative: verb 'g' does NOT govern Gen (no genitive neighbors)
    res2 = assess(tally, "Gen", base)
    assert res2["verdict"] == "OVERSTATED", res2
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--window", type=int, default=5)
    args = ap.parse_args()

    ok = self_test()
    db = sqlite3.connect(args.db)
    cur = db.cursor()
    base, base_n = baseline_shares(cur)

    claims = {}
    for cid, (lemmas, pred, desc) in GOV_CLAIMS.items():
        tally = local_case_tally(cur, lemmas, args.window)
        a = assess(tally, pred, base)
        a["lemmas"], a["desc"] = lemmas, desc
        claims[cid] = a

    controls = {}
    for name, (lemmas, pred) in CONTROLS_POS.items():
        controls[name] = assess(local_case_tally(cur, lemmas, args.window), pred, base)
    neg_tally = local_case_tally(cur, CONTROL_NEG[0], args.window)
    controls["neg_dṛś"] = {
        "desc": CONTROL_NEG[1],
        "lift_over_baseline": assess(neg_tally, "Acc", base)["lift_over_baseline"],
        "top_case_by_lift": assess(neg_tally, "Acc", base)["top_case_by_lift"],
        "n_windowed_obliques": sum(neg_tally.values()),
    }

    out = {
        "instrument": "apte_classical_government_stats.py — windowed cooccurrence + baseline "
                      "lift over the FULL DCS corpus (feat_case on 70.6% of 5.69M tokens); a "
                      "collexeme proxy for case government, NOT dependency government",
        "window": args.window,
        "baseline_oblique_shares_pct": {c: round(100 * base[c], 1) for c in OBLIQUE},
        "baseline_oblique_n": base_n,
        "controls": controls,
        "claims": claims,
        "self_test": {"passed": ok},
    }
    (HERE / "apte_classical_government_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"baseline obliques (n={base_n}):",
          {c: out["baseline_oblique_shares_pct"][c] for c in OBLIQUE})
    print(f"window=+-{args.window}")
    print("CONTROLS:")
    for name, cc in controls.items():
        if name.startswith("neg"):
            print(f"  {name}: top-lift {cc['top_case_by_lift']} (should be Acc; n={cc['n_windowed_obliques']}) "
                  f"dat/abl/gen lift {cc['lift_over_baseline'].get('Dat')}/{cc['lift_over_baseline'].get('Abl')}/{cc['lift_over_baseline'].get('Gen')}")
        else:
            print(f"  {name}: predicted lift {cc['predicted_lift']} -> {cc['verdict']} (n={cc['n_windowed_obliques']})")
    print("CLAIMS:")
    for cid, a in claims.items():
        print(f"  {cid} {a['predicted_case']}: lift {a['predicted_lift']}  n={a['n_windowed_obliques']}  "
              f"top-lift={a['top_case_by_lift']} -> {a['verdict']}  [{a['reason']}]")
    print("-> apte_classical_government_stats.json written")


if __name__ == "__main__":
    main()
