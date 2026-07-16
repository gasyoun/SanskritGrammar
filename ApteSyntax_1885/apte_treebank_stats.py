#!/usr/bin/env python
"""apte_treebank_stats.py — the dependency-treebank drain instrument for the
ApteSyntax_1885 claim register (H1059).

Apte's *Student's Guide to Sanskrit Composition* is a SYNTAX manual, so its
claims_harvest.yml backlog is dominated by three testable shapes, each a query
over dcs_full.sqlite's own head/deprel/feat_case columns (the same fully-tagged
UD-style slice used by ../ZalizniakOcherk_1978/treebank_syntax_stats.py —
~223k tokens / 29,433 sentences, concentrated in Vedic/early prose):

  A. PARTICLE POSITION (robustly drainable, n = hundreds–thousands): is a
     postpositive particle (ca, tu, ced, iva, eva, ...) genuinely never / rarely
     sentence-initial (idx==1)? Directly tests APT-3/APT-4 and harvest
     APT-H-218/310/313/315/312, plus the enclitic-pronoun-form claim (APT-8/
     APT-H-200) by matching the enclitic FORMS (mā/me/naḥ/nau/tvā/te/vāṃ/vaḥ).

  B. AGREEMENT (robustly drainable): subject–verb number/person agreement
     (APT-H-4), attributive adjective (amod) case/gender/number agreement with
     its head noun (APT-2/APT-H-10), and relative-pronoun-precedes-antecedent
     order (APT-H-12).

  C. CASE GOVERNMENT (mostly UNTESTABLE-thin — the honest finding): "verb X
     governs case Y" (APT-H-105/106/110/111/112/113/115, ...). The governing
     verbs have healthy TOTAL token counts (krudh 1659, ruc 501, ...) but their
     case-tagged DEPENDENT arguments collapse to n<5 in the tagged slice, because
     (1) most tokens of these Classical lexemes sit in untagged sentences and
     (2) the object-of-emotion is often pronominal/elided. The instrument reports
     the dependent-case tally + n for each set so the verdict is data-driven, and
     marks any set with n<10 case-tagged obliques UNTESTABLE-thin rather than
     verdicting on noise.

  D. MOTION-GOAL CASE (APT-5 corroboration): among the arguments of motion
     verbs (gam/yā/i/car/...), how marginal is the non-accusative (dative/
     locative) goal against the accusative default? Puts a number on the APT-5
     OVERSTATED flag.

Usage:  python ApteSyntax_1885/apte_treebank_stats.py [--db PATH]
Writes  apte_treebank_stats.json next to this script.
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

THIN = 10  # < this many case-tagged obliques -> UNTESTABLE-thin, do not verdict


def prefix(deprel):
    return deprel.split(":")[0] if deprel else deprel


def _pct(hits, n):
    return round(100 * hits / n, 2) if n else None


# ---------- A. particle position ----------

PARTICLES = {
    # lemma : (harvest id, claim, "never" | "postposed")
    "ca":   ("APT-3/APT-H-314",  "ca never sentence-initial",        "never"),
    "tu":   ("APT-4/APT-H-316",  "tu never sentence-initial",        "never"),
    "ced":  ("APT-H-218",        "ced never sentence-initial",       "never"),
    "iva":  ("APT-H-310",        "iva stands after object of simile","postposed"),
    "eva":  ("APT-H-313",        "eva follows the emphasized word",  "postposed"),
    "kila": ("APT-H-315",        "kila followed by emphasized word", "postposed"),
    "uta":  ("APT-H-312",        "uta 'or', paired with kim",        "postposed"),
    "hi":   ("(control)",        "hi (causal, postpositive control)","postposed"),
}


def particle_position(cur):
    out = {}
    for lem, (cid, claim, mode) in PARTICLES.items():
        n = cur.execute(
            "SELECT COUNT(*) FROM token WHERE lemma=? AND deprel IS NOT NULL", (lem,)).fetchone()[0]
        init = cur.execute(
            "SELECT COUNT(*) FROM token WHERE lemma=? AND deprel IS NOT NULL AND idx=1", (lem,)).fetchone()[0]
        out[lem] = {
            "claim": cid, "desc": claim, "mode": mode,
            "n": n, "sentence_initial": init, "initial_pct": _pct(init, n),
            "verdict": None if n < THIN else (
                "TRUE" if (mode == "never" and init == 0) or
                          (init / n) < 0.05 else "OVERSTATED"),
        }
    return out


ENCLITIC_FORMS = ["mā", "me", "naḥ", "nau", "tvā", "te", "vāṃ", "vaḥ"]


def enclitic_position(cur):
    """APT-8/APT-H-200: enclitic pronoun FORMS never sentence-initial. Matched on
    surface form (post-sandhi) among PRON tokens, restricted to the tagged slice."""
    qs = ",".join("?" * len(ENCLITIC_FORMS))
    n = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE form IN ({qs}) AND upos='PRON' AND deprel IS NOT NULL",
        ENCLITIC_FORMS).fetchone()[0]
    init = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE form IN ({qs}) AND upos='PRON' AND deprel IS NOT NULL AND idx=1",
        ENCLITIC_FORMS).fetchone()[0]
    by_form = dict(cur.execute(
        f"SELECT form, COUNT(*) FROM token WHERE form IN ({qs}) AND upos='PRON' AND deprel IS NOT NULL AND idx=1 GROUP BY form",
        ENCLITIC_FORMS))
    return {
        "claim": "APT-8/APT-H-200", "desc": "enclitic pronoun forms never sentence-initial",
        "forms": ENCLITIC_FORMS, "n": n, "sentence_initial": init,
        "initial_pct": _pct(init, n), "initial_by_form": by_form,
        "verdict": None if n < THIN else ("TRUE" if init == 0 else
                   ("TRUE" if init / n < 0.02 else "OVERSTATED")),
        "note": "form match is post-sandhi surface; a handful of initials may be homographs "
                "(mā = prohibitive particle; te = Nom.pl 'they') — inspect initial_by_form",
    }


# ---------- B. agreement ----------

def subject_verb_agreement(cur):
    """APT-H-4: verb agrees with subject in number and person. Among nsubj edges
    to a finite root/verb where both carry number, measure the match rate."""
    rows = cur.execute(
        """SELECT s.feat_number, v.feat_number, s.feat_person, v.feat_person
           FROM token s JOIN token v ON s.sentence_id=v.sentence_id AND s.head=v.idx
           WHERE s.deprel='nsubj' AND v.upos='VERB' AND v.feat_verbform IS NULL
             AND s.feat_number IS NOT NULL AND v.feat_number IS NOT NULL""").fetchall()
    n = len(rows)
    num_match = sum(1 for sn, vn, sp, vp in rows if sn == vn)
    # person: subject person defaults to 3 when unmarked (nouns); compare where both marked
    pboth = [(sp, vp) for sn, vn, sp, vp in rows if sp and vp]
    per_match = sum(1 for sp, vp in pboth if sp == vp)
    return {
        "claim": "APT-H-4", "desc": "verb agrees with subject in number and person",
        "n_number": n, "number_match": num_match, "number_match_pct": _pct(num_match, n),
        "n_person_bothmarked": len(pboth), "person_match": per_match,
        "person_match_pct": _pct(per_match, len(pboth)),
        "verdict": None if n < THIN else ("TRUE" if num_match / n > 0.85 else "OVERSTATED"),
    }


def adjective_noun_agreement(cur):
    """APT-2/APT-H-10: attributive adjectives agree with the noun in gender,
    number, case. Among amod(ADJ)->NOUN edges where both carry the feature."""
    rows = cur.execute(
        """SELECT a.feat_case, h.feat_case, a.feat_gender, h.feat_gender,
                  a.feat_number, h.feat_number
           FROM token a JOIN token h ON a.sentence_id=h.sentence_id AND a.head=h.idx
           WHERE a.deprel='amod' AND h.upos='NOUN'""").fetchall()
    def rate(i, j):
        pairs = [(r[i], r[j]) for r in rows if r[i] and r[j]]
        return len(pairs), sum(1 for x, y in pairs if x == y)
    cn, cm = rate(0, 1); gn, gm = rate(2, 3); nn, nm = rate(4, 5)
    return {
        "claim": "APT-2/APT-H-10", "desc": "adjective agrees with noun in gender, number, case",
        "case":   {"n": cn, "match": cm, "pct": _pct(cm, cn)},
        "gender": {"n": gn, "match": gm, "pct": _pct(gm, gn)},
        "number": {"n": nn, "match": nm, "pct": _pct(nm, nn)},
        "verdict": None if cn < THIN else (
            "TRUE" if min(_pct(cm, cn), _pct(gm, gn), _pct(nm, nn)) > 0.85 * 100 else "OVERSTATED"),
    }


def relative_pronoun_order(cur):
    """APT-H-12: the relative pronoun (yad) usually precedes the noun it refers
    to. Among acl:rel(rel-verb)->NOUN edges whose rel subtree contains a yad PRON,
    is the yad token before the head noun?"""
    # simpler surface proxy: among sentences with both a 'yad' PRON and a 'tad'
    # PRON, does yad precede tad (antecedent/correlative order)?
    rows = cur.execute(
        """SELECT y.sentence_id, MIN(y.idx), MIN(t.idx)
           FROM token y JOIN token t ON y.sentence_id=t.sentence_id
           WHERE y.lemma='yad' AND t.lemma='tad' AND y.deprel IS NOT NULL
           GROUP BY y.sentence_id""").fetchall()
    n = len(rows)
    yad_first = sum(1 for sid, ymin, tmin in rows if ymin < tmin)
    return {
        "claim": "APT-H-12", "desc": "relative (yad) precedes its correlative (tad)",
        "n": n, "yad_precedes_tad": yad_first, "pct": _pct(yad_first, n),
        "verdict": None if n < THIN else ("TRUE" if yad_first / n > 0.6 else "OVERSTATED"),
    }


# ---------- C. case government (mostly thin) ----------

GOV_SETS = {
    "APT-H-105": (["ruc"], "Dat", "verb ruc 'please' governs dative of the pleased"),
    "APT-H-106": (["krudh", "druh", "īrṣy", "asūy"], "Dat", "anger verbs govern dative of the object of anger"),
    "APT-H-110": (["jugups", "viram", "pramad"], "Abl", "disgust/cessation govern ablative"),
    "APT-H-111": (["bhī"], "Abl", "fear verbs put the source of fear in ablative"),
    "APT-H-112": (["snih", "abhilaṣ", "anurañj"], "Loc", "love verbs govern locative of the object"),
    "APT-H-113": (["kṣip", "muc"], "Loc", "throw verbs govern locative of the target"),
    "APT-H-115": (["īś", "prabhū", "smṛ", "adhī"], "Gen", "ruling/remembering verbs govern genitive"),
}


def _dependent_cases(cur, lemmas):
    """Case tally of NOUN/PRON dependents (excluding nsubj) of the given verb lemmas."""
    qs = ",".join("?" * len(lemmas))
    rows = cur.execute(
        f"""SELECT ch.feat_case, COUNT(*) FROM token p
            JOIN token ch ON ch.sentence_id=p.sentence_id AND ch.head=p.idx
            WHERE p.lemma IN ({qs}) AND p.upos='VERB'
              AND ch.upos IN ('NOUN','PRON') AND ch.deprel NOT IN ('nsubj')
              AND ch.feat_case IS NOT NULL AND ch.feat_case NOT IN ('Cpd')
            GROUP BY ch.feat_case ORDER BY 2 DESC""", lemmas).fetchall()
    return dict(rows)


def government(cur):
    out = {}
    for cid, (lemmas, predicted, desc) in GOV_SETS.items():
        cases = _dependent_cases(cur, lemmas)
        oblique = {k: v for k, v in cases.items() if k not in ("Nom", "Voc")}
        n_obl = sum(oblique.values())
        pred = cases.get(predicted, 0)
        top = max(oblique, key=oblique.get) if oblique else None
        out[cid] = {
            "desc": desc, "predicted_case": predicted, "lemmas": lemmas,
            "dependent_case_tally": cases, "n_oblique": n_obl,
            "predicted_hits": pred, "predicted_share_of_oblique_pct": _pct(pred, n_obl),
            "top_oblique_case": top,
            "verdict": None if n_obl < THIN else (
                "TRUE" if top == predicted else "OVERSTATED"),
            "verdict_reason": ("UNTESTABLE-thin: <%d case-tagged obliques in the tagged slice "
                               "(Classical lexeme under-represented in the Vedic-skewed treebank; "
                               "object often pronominal/elided)" % THIN) if n_obl < THIN else "measured",
        }
    return out


# ---------- D. motion-goal case (APT-5) ----------

MOTION_VERBS = ["gam", "yā", "i", "car", "vraj", "sṛ", "dhāv", "ā-gam", "abhi-gam"]


def motion_goal_case(cur):
    """APT-5/APT-H-15: 'all motion verbs govern the accusative'. Among case-tagged
    NOUN/PRON dependents (excl nsubj) of motion verbs, how dominant is Acc vs the
    dative/locative goal? Quantifies how marginal the non-accusative goal is."""
    cases = _dependent_cases(cur, MOTION_VERBS)
    goalish = {k: cases.get(k, 0) for k in ("Acc", "Dat", "Loc")}
    n = sum(goalish.values())
    return {
        "claim": "APT-5/APT-H-15", "desc": "motion verbs and the case of the goal",
        "verbs": MOTION_VERBS, "dependent_case_tally": cases,
        "goal_cases": goalish, "n_goal_cases": n,
        "acc_share_pct": _pct(goalish["Acc"], n),
        "non_acc_goal_pct": _pct(goalish["Dat"] + goalish["Loc"], n),
        "note": "Acc is the heavy default; Dat+Loc goal is the attested minority that makes "
                "«все… винительным» OVERSTATED (APT-5). Loc here conflates goal-of-motion with "
                "locative-of-place, so non_acc_goal_pct is an upper bound on the true goal-dative/-locative.",
    }


def self_test():
    """In-memory DB with hand-built rows exercising each battery's core query."""
    db = sqlite3.connect(":memory:")
    db.execute("""CREATE TABLE token (sentence_id INT, idx INT, form TEXT, lemma TEXT,
        upos TEXT, head INT, deprel TEXT, feat_case TEXT, feat_gender TEXT,
        feat_number TEXT, feat_person TEXT, feat_verbform TEXT)""")
    rows = [
        # sentence 1: "devān ca" — ca (idx 2) not initial
        (1, 1, "devān", "deva", "NOUN", 3, "obj", "Acc", "Masc", "Plur", None, None),
        (1, 2, "ca", "ca", "PART", 1, "cc", None, None, None, None, None),
        (1, 3, "gacchati", "gam", "VERB", 0, "root", None, None, "Sing", "3", None),
        # sentence 2: krudh with a Dat dependent (object of anger)
        (2, 1, "rājā", "rājan", "NOUN", 2, "nsubj", "Nom", "Masc", "Sing", None, None),
        (2, 2, "krudhyati", "krudh", "VERB", 0, "root", None, None, "Sing", "3", None),
        (2, 3, "śatrave", "śatru", "NOUN", 2, "obl", "Dat", "Masc", "Sing", None, None),
        # sentence 3: amod agreement (adj Acc/Masc/Sing -> noun Acc/Masc/Sing)
        (3, 1, "mahat", "mahat", "ADJ", 2, "amod", "Acc", "Masc", "Sing", None, None),
        (3, 2, "vṛkṣam", "vṛkṣa", "NOUN", 3, "obj", "Acc", "Masc", "Sing", None, None),
        (3, 3, "paśyati", "paś", "VERB", 0, "root", None, None, "Sing", "3", None),
    ]
    db.executemany("INSERT INTO token VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    cur = db.cursor()
    pp = particle_position(cur)
    assert pp["ca"]["n"] == 1 and pp["ca"]["sentence_initial"] == 0, pp["ca"]
    gov = government(cur)
    assert gov["APT-H-106"]["dependent_case_tally"].get("Dat") == 1, gov["APT-H-106"]
    an = adjective_noun_agreement(cur)
    assert an["case"]["match"] == 1 and an["gender"]["match"] == 1, an
    sv = subject_verb_agreement(cur)
    assert sv["n_number"] == 1 and sv["number_match"] == 1, sv
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()

    ok = self_test()

    db = sqlite3.connect(args.db)
    cur = db.cursor()
    total = cur.execute("SELECT COUNT(*) FROM token").fetchone()[0]
    tagged = cur.execute("SELECT COUNT(*) FROM token WHERE deprel IS NOT NULL").fetchone()[0]

    out = {
        "instrument": "apte_treebank_stats.py over dcs_full.sqlite head/deprel/feat_case "
                      "(same fully-tagged UD slice as ZalizniakOcherk_1978/treebank_syntax_stats.py)",
        "coverage": {"total_tokens": total, "tagged_tokens": tagged,
                     "tagged_pct": round(100 * tagged / total, 2)},
        "A_particle_position": particle_position(cur),
        "A_enclitic_position": enclitic_position(cur),
        "B_subject_verb_agreement": subject_verb_agreement(cur),
        "B_adjective_noun_agreement": adjective_noun_agreement(cur),
        "B_relative_pronoun_order": relative_pronoun_order(cur),
        "C_case_government": government(cur),
        "D_motion_goal_case": motion_goal_case(cur),
        "self_test": {"passed": ok},
    }
    (HERE / "apte_treebank_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"coverage: {tagged}/{total} tagged ({out['coverage']['tagged_pct']}%)")
    print("A particle position:")
    for lem, d in out["A_particle_position"].items():
        print(f"  {lem:5} n={d['n']:5} init={d['sentence_initial']:3} ({d['initial_pct']}%) -> {d['verdict']}")
    e = out["A_enclitic_position"]
    print(f"  enclitics n={e['n']} init={e['sentence_initial']} ({e['initial_pct']}%) -> {e['verdict']} {e['initial_by_form']}")
    print("B agreement:")
    sv = out["B_subject_verb_agreement"]; an = out["B_adjective_noun_agreement"]; ro = out["B_relative_pronoun_order"]
    print(f"  subj-verb number {sv['number_match_pct']}% (n={sv['n_number']}) person {sv['person_match_pct']}% -> {sv['verdict']}")
    print(f"  adj-noun case {an['case']['pct']}% gender {an['gender']['pct']}% number {an['number']['pct']}% (n={an['case']['n']}) -> {an['verdict']}")
    print(f"  rel yad<tad {ro['pct']}% (n={ro['n']}) -> {ro['verdict']}")
    print("C case government (thin-flagged):")
    for cid, d in out["C_case_government"].items():
        print(f"  {cid} pred={d['predicted_case']} tally={d['dependent_case_tally']} n_obl={d['n_oblique']} -> {d['verdict']} [{d['verdict_reason'][:40]}]")
    m = out["D_motion_goal_case"]
    print(f"D motion goal: Acc {m['acc_share_pct']}% vs non-Acc {m['non_acc_goal_pct']}% (n={m['n_goal_cases']}) tally={m['dependent_case_tally']}")
    print("-> apte_treebank_stats.json written")


if __name__ == "__main__":
    main()
