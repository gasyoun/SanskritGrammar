#!/usr/bin/env python
"""gender_resolution_probe.py — sizing probe for §XX (HB-158).

HB-158 claims: an adjective referring to several nouns of DIFFERENT gender
is masculine for a masc+fem mix, neuter whenever a neuter conjunct is
present. This needs a genuine PREDICATE construction — an adjective whose
resolved gender covers the WHOLE coordinated noun phrase, not an ordinary
attributive adjective that merely happens to sit near a coordination (an
amod attaching to one conjunct trivially agrees with THAT noun's own
gender regardless of its siblings — that is not the phenomenon described,
and inflates the count with false positives if not filtered out).

METHOD: find NOUN `conj` groups (an anchor + its conjunct siblings, all
upos=NOUN) whose combined feat_gender set has >= 2 distinct values, then
find ADJ tokens that are PREDICATES (an nsubj child pointing to one member
of such a group — i.e. a verbless nominal sentence or copula construction
where the ADJ is root/xcomp over the coordinated subject).

RESULT (16-07-2026): only n=4 such constructions exist in the whole
223,751-token annotated slice. 2/4 match the stated rule exactly; the
other 2 show agreement with the nearest/first-listed conjunct instead
(itself a well-documented RIVAL Sanskrit agreement strategy — proximity/
attraction — not necessarily a refutation of Bühler's rule, just a
different pattern the corpus also attests). n=4 is far too thin to
support any verdict either way — this is a sizing result, not a test.

Usage:  python BuhlerLeitfaden_1923/gender_resolution_probe.py [--db PATH]
Writes  hb158_gender_resolution_probe.json next to this script.
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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    groups = defaultdict(list)
    for sid, head, idx, g in cur.execute(
        "SELECT sentence_id, head, idx, feat_gender FROM token "
        "WHERE deprel='conj' AND upos='NOUN'"
    ):
        groups[(sid, head)].append((idx, g))

    anchor_gender = {}
    for (sid, head) in groups:
        row = cur.execute(
            "SELECT feat_gender FROM token WHERE sentence_id=? AND idx=?", (sid, head)
        ).fetchone()
        anchor_gender[(sid, head)] = row[0] if row else None

    mixed = {}
    for (sid, head), deps in groups.items():
        genders = set([anchor_gender[(sid, head)]] + [g for _, g in deps])
        genders.discard(None)
        if len(genders) >= 2:
            mixed[(sid, head)] = (genders, [head] + [i for i, _ in deps])

    total_mixed_groups = len(mixed)

    hits = []
    for (sid, anchor), (genders, members) in mixed.items():
        member_set = set(members)
        for adj_idx, adjg, deprel in cur.execute(
            "SELECT idx, feat_gender, deprel FROM token "
            "WHERE sentence_id=? AND upos='ADJ'", (sid,)
        ):
            subj_rows = cur.execute(
                "SELECT idx FROM token WHERE sentence_id=? AND head=? "
                "AND deprel LIKE 'nsubj%'", (sid, adj_idx),
            ).fetchall()
            for (subj_idx,) in subj_rows:
                if subj_idx in member_set:
                    expected = "Neut" if "Neut" in genders else "Masc"
                    hits.append({
                        "sentence_id": sid, "anchor_idx": anchor,
                        "conjunct_genders": sorted(genders),
                        "adj_idx": adj_idx, "adj_gender": adjg, "adj_deprel": deprel,
                        "subj_idx": subj_idx,
                        "expected_by_rule": expected,
                        "matches_rule": adjg == expected,
                    })

    out = {
        "instrument": "gender_resolution_probe.py over dcs_full.sqlite — sizing probe, "
                      "not a full verdict instrument (see docstring for why n is this small)",
        "mixed_gender_noun_conjunction_groups": total_mixed_groups,
        "predicate_adj_over_mixed_gender_subject_n": len(hits),
        "matches": sum(1 for h in hits if h["matches_rule"]),
        "mismatches": sum(1 for h in hits if not h["matches_rule"]),
        "cases": hits,
        "conclusion": "n too thin to verdict; recorded as a sized negative pilot",
    }
    (HERE / "hb158_gender_resolution_probe.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"mixed-gender noun conjunction groups: {total_mixed_groups}")
    print(f"genuine predicate-over-coordination candidates: {len(hits)}")
    for h in hits:
        print(" ", h["sentence_id"], h["conjunct_genders"], "->",
              h["adj_gender"], "expected", h["expected_by_rule"],
              "MATCH" if h["matches_rule"] else "MISMATCH")
    print("-> hb158_gender_resolution_probe.json written")


if __name__ == "__main__":
    main()
