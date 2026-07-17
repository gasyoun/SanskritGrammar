#!/usr/bin/env python
"""apte_pada_stats.py — the voice (pada) instrument for Apte's lessons 29-30
(H1081).

Lessons 29-30 of Apte are a Pāṇinian voice-assignment appendix: which roots take
Parasmaipada (active), which Ātmanepada (middle), and how preverbs/senses flip
the choice. DCS-2021 does NOT annotate this: feat_voice carries only 'Pass'
(passive) vs NULL — the P/Ā distinction is absent from the feature columns. So
this domain looked UNTESTABLE.

But pada IS recoverable from the ENDING of the finite present-indicative form:
Parasmaipada 3sg -ti / 3pl -(a)nti / 1sg -mi ... vs Ātmanepada 3sg -te /
3pl -(a)nte/-ate / 1sg -e, -mahe, -dhve. This instrument classifies each root's
finite present forms (m_unsandhied) by ending and reports the P vs Ā split,
which cleanly drains the ROOT-DEFAULT-voice claims (e.g. 'ram normally
Ātmanepada', 'han normally Parasmaipada').

SCOPE LIMIT (honest): only the root-DEFAULT voice is testable this way. The
fine preverb+semantic rules that dominate lessons 29-30 ('kram takes Ātmanepada
WHEN duration is implied', 'tap+ud is Ātmanepada WHEN intransitive or with a
body-part object') condition on a SENSE the corpus does not tag, so they stay
UNTESTABLE — flagged, not force-verdicted. The ending heuristic is also just a
heuristic: it excludes non-present and non-indicative forms (whose endings
differ) and a few syncretic endings are ambiguous; a >80% split is treated as
decisive, 60-80% as a lean, <60% as genuinely mixed ('both').

METHOD CONTROLS: as/bhū are canonical Parasmaipada roots (expect P-dominant);
labh/īś are canonical Ātmanepada (expect Ā-dominant). If the classifier inverts
these, the ending regex is wrong.

Usage:  python ApteSyntax_1885/apte_pada_stats.py [--db PATH]
Writes  apte_pada_stats.json next to this script.
"""
import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"

# Ātmanepada present-indicative endings (checked FIRST — more distinctive)
A_END = re.compile(r"(nte|ante|ate|mahe|vahe|dhve|ethe|āte|ete|se|te|e)$")
# Parasmaipada present-indicative endings
P_END = re.compile(r"(anti|nti|masi|mas|vas|tha|thas|tas|ti|si|mi)$")
MIN_N = 40           # below this -> UNTESTABLE-thin
DECISIVE = 0.80      # >=80% one pada -> that pada is the default
LEAN = 0.60          # 60-80% -> lean; <60% -> genuinely mixed ('both')

# claim -> (root lemma, expected 'P'|'A'|'both', description)
PADA_CLAIMS = {
    "APT-H-609": ("ram", "A", "ram 'rest' normally Ātmanepada"),
    "APT-H-612": ("han", "P", "han normally Parasmaipada"),
    "APT-H-602": ("krīḍ", "P", "krīḍ 'play' normally Parasmaipada"),
    "APT-H-600a": ("bhāṣ", "A", "bhāṣ single-voice (Ātmanepada)"),
    "APT-H-600b": ("nam", "P", "nam single-voice (Parasmaipada)"),
    "APT-H-600c": ("kṛ", "both", "kṛ both voices"),
    "APT-H-600d": ("duh", "both", "duh both voices"),
}
CONTROLS = {"ctrl_as_P": ("as", "P"), "ctrl_bhū_P": ("bhū", "P"),
            "ctrl_labh_A": ("labh", "A"), "ctrl_īś_A": ("īś", "A")}


def classify(cur, lemma):
    rows = cur.execute(
        """SELECT m_unsandhied FROM token
           WHERE lemma=? AND upos='VERB' AND feat_tense='Pres'
             AND feat_verbform IS NULL AND m_unsandhied IS NOT NULL""", (lemma,)).fetchall()
    P = A = other = 0
    for (f,) in rows:
        f = (f or "").strip().lower()
        if not f:
            other += 1
        elif A_END.search(f):
            A += 1
        elif P_END.search(f):
            P += 1
        else:
            other += 1
    n = P + A
    return {"finite_pres": len(rows), "P": P, "A": A, "unclassified": other,
            "P_pct": round(100 * P / n, 1) if n else None,
            "A_pct": round(100 * A / n, 1) if n else None, "n_classified": n}


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


BOTH_MINORITY = 20   # for a 'both-voice' claim, the minority pada must be >= this %


def verdict(expected, observed, c=None):
    if observed is None:
        return None, "UNTESTABLE-thin (<%d classified present forms)" % MIN_N
    obs_base = observed.replace("-lean", "")
    if expected == "both":
        # "both voices" is TRUE when both are substantially attested, not only at 50/50
        minority = min(c["P_pct"], c["A_pct"]) if c else 0
        return ("TRUE" if minority >= BOTH_MINORITY else "OVERSTATED"), \
            f"expected both-voice; observed {observed} (minority pada {minority}%)"
    if obs_base == expected:
        strong = "-lean" not in observed
        return ("TRUE" if strong else "TRUE-partial"), \
            f"expected {expected}-dominant; observed {observed}"
    return "OVERSTATED", f"expected {expected}-dominant; observed {observed}"


def self_test():
    db = sqlite3.connect(":memory:")
    db.execute("""CREATE TABLE token (lemma TEXT, upos TEXT, feat_tense TEXT,
        feat_verbform TEXT, m_unsandhied TEXT)""")
    rows = ([("r", "VERB", "Pres", None, "ramate")] * 90 +
            [("r", "VERB", "Pres", None, "ramati")] * 10)  # 90% Ā
    db.executemany("INSERT INTO token VALUES (?,?,?,?,?)", rows)
    c = classify(db.cursor(), "r")
    assert c["A"] == 90 and c["P"] == 10, c
    v, _ = verdict("A", observed_pada(c))
    assert v == "TRUE", (c, v)
    v2, _ = verdict("P", observed_pada(c))
    assert v2 == "OVERSTATED", v2
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    ok = self_test()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    controls = {}
    for name, (lem, exp) in CONTROLS.items():
        c = classify(cur, lem)
        obs = observed_pada(c)
        v, reason = verdict(exp, obs, c)
        controls[name] = {"lemma": lem, "expected": exp, "observed": obs,
                          "P_pct": c["P_pct"], "A_pct": c["A_pct"],
                          "n": c["n_classified"], "control_holds": v in ("TRUE", "TRUE-partial")}

    claims = {}
    for cid, (lem, exp, desc) in PADA_CLAIMS.items():
        c = classify(cur, lem)
        obs = observed_pada(c)
        v, reason = verdict(exp, obs, c)
        claims[cid] = {"lemma": lem, "expected": exp, "desc": desc,
                       "P": c["P"], "A": c["A"], "P_pct": c["P_pct"], "A_pct": c["A_pct"],
                       "n_classified": c["n_classified"], "observed_pada": obs,
                       "verdict": v, "reason": reason}

    out = {
        "instrument": "apte_pada_stats.py — Parasmaipada/Ātmanepada recovered from finite "
                      "present-indicative endings (DCS feat_voice tags only Pass, not P/Ā); "
                      "root-default voice only, preverb+semantic rules out of scope",
        "controls": controls,
        "claims": claims,
        "scope_note": "Lessons 29-30's fine preverb+semantic voice rules are NOT testable — they "
                      "condition on a sense the corpus does not tag; only root-default voice is drained here.",
        "self_test": {"passed": ok},
    }
    (HERE / "apte_pada_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("CONTROLS (should all hold):")
    for name, cc in controls.items():
        print(f"  {name}: {cc['lemma']} expected {cc['expected']} -> P{cc['P_pct']}%/A{cc['A_pct']}% "
              f"(n={cc['n']}) holds={cc['control_holds']}")
    print("CLAIMS:")
    for cid, a in claims.items():
        print(f"  {cid} {a['lemma']} exp={a['expected']}: P{a['P_pct']}%/A{a['A_pct']}% "
              f"(n={a['n_classified']}) obs={a['observed_pada']} -> {a['verdict']}")
    print("-> apte_pada_stats.json written")


if __name__ == "__main__":
    main()
