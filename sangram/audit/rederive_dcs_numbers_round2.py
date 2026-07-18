#!/usr/bin/env python3
"""H1229 round 2 — resolve the 30 definitional mismatches from round 1.

Round 1 (rederive_dcs_numbers.py) re-derived 129 published numbers; 97 matched
exactly. Of the 32 mismatches, 2 were deliberate refutation proofs (the -tṛ
encoding trap, the preverbs ut cell). This script re-tests the remaining 30
with the generation scripts' EXACT predicates (recovered from scripts/) to
separate "my approximation differed" from "the published number is wrong".
Output: sangram/audit/audit_results_round2.json.
"""
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

GITHUB = Path(__file__).resolve().parents[3]
DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT = Path(__file__).resolve().parent / "audit_results_round2.json"

FIN = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
       "AND feat_person IS NOT NULL")

results = []


def check(cid, label, expected, derived, note=""):
    ok = (expected == derived)
    results.append({"id": cid, "label": label, "expected": expected,
                    "derived": derived, "match": ok, "note": note})
    flag = "OK " if ok else "*** MISMATCH"
    print(f"[{cid}] {flag} expected={expected} derived={derived}  {label}")


def main():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = con.cursor()

    def q(sql, *args):
        return cur.execute(sql, args).fetchone()[0]

    def dist(sql, *args):
        return {r[0]: r[1] for r in cur.execute(sql, args)}

    # G2 grouped by lemma_id (round 1 grouped by lemma string)
    rows = cur.execute(
        "SELECT lemma_id, COUNT(DISTINCT feat_case||'/'||feat_number) FROM token "
        "WHERE upos='NOUN' AND feat_case IS NOT NULL AND feat_case<>'' "
        "AND feat_case<>'Cpd' AND feat_number IS NOT NULL GROUP BY lemma_id").fetchall()
    cells = sorted(r[1] for r in rows)
    n = len(cells)
    check("R2-MO001-4", "G2 lemma universe by lemma_id", 57_144, n)
    one = sum(1 for c in cells if c == 1)
    med = cells[n // 2] if n % 2 else (cells[n // 2 - 1] + cells[n // 2]) / 2
    check("R2-MO001-5", "G2 median / %exactly-1 / fill% (by lemma_id)",
          (1, 58.9, 10.44),
          (med, round(100 * one / n, 1), round(100 * sum(cells) / (24 * n), 2)))

    # SE002: nsubj / obj denominators including Cpd
    check("R2-SE002-1", "nsubj case-tagged incl Cpd", 20_062,
          q("SELECT COUNT(*) FROM token WHERE deprel='nsubj' "
            "AND feat_case IS NOT NULL AND feat_case<>''"))
    check("R2-SE002-2", "obj case-tagged incl Cpd", 16_933,
          q("SELECT COUNT(*) FROM token WHERE deprel='obj' "
            "AND feat_case IS NOT NULL AND feat_case<>''"))
    # (round 1 already filtered <>''; the missing tokens must be Cpd-case rows
    #  — count them explicitly)
    check("R2-SE002-1b", "nsubj with feat_case='Cpd'", 63,
          q("SELECT COUNT(*) FROM token WHERE deprel='nsubj' AND feat_case='Cpd'"))
    check("R2-SE002-2b", "obj with feat_case='Cpd'", 59,
          q("SELECT COUNT(*) FROM token WHERE deprel='obj' AND feat_case='Cpd'"))

    # SE002 cop-head denominator: heads of cop including case-less heads
    tot_heads = q("""SELECT COUNT(DISTINCT h.id) FROM token c
        JOIN token h ON h.sentence_id=c.sentence_id AND h.idx=c.head
        WHERE c.deprel='cop'""")
    check("R2-SE002-3", "cop-head denominator (all heads, incl case-less)",
          1_661, tot_heads)

    # SE002 double-acc corrected: core roles obj/iobj/xcomp/ccomp
    core = q("""SELECT COUNT(*) FROM (
        SELECT c.sentence_id, c.head FROM token c
        JOIN token h ON h.sentence_id=c.sentence_id AND h.idx=c.head AND h.upos='VERB'
        WHERE c.feat_case='Acc' AND c.deprel IN ('obj','iobj','xcomp','ccomp')
        GROUP BY c.sentence_id, c.head HAVING COUNT(*) >= 2)""")
    check("R2-SE002-6", "corrected double-acc, script's core set obj/iobj/xcomp/ccomp",
          872, core)

    # SE003: obl:soc restricted to Ins (article prints Ins-only, as with obl:instr)
    check("R2-SE003-1", "obl:soc that are Ins", 488,
          q("SELECT COUNT(*) FROM token WHERE deprel='obl:soc' AND feat_case='Ins'"))
    # SE003: Ins co-occurring with a Pass verb — sentence-level
    check("R2-SE003-3", "Ins tokens in a sentence containing a Pass verb", 21_472,
          q("""SELECT COUNT(*) FROM token i WHERE i.feat_case='Ins' AND EXISTS (
               SELECT 1 FROM token v WHERE v.sentence_id=i.sentence_id
               AND v.upos='VERB' AND v.feat_voice='Pass')"""))
    # SE003: mad counts without the upos filter
    check("R2-SE003-4", "mad Ins (no upos filter)", 5_605,
          q("SELECT COUNT(*) FROM token WHERE feat_case='Ins' AND lemma='mad'"))
    check("R2-SE003-7", "mad Dat (no upos filter)", 5_834,
          q("SELECT COUNT(*) FROM token WHERE feat_case='Dat' AND lemma='mad'"))
    # SE003: top noun forms via m_unsandhied only (NULLs dropped)
    f_ins = dist("SELECT m_unsandhied, COUNT(*) FROM token WHERE feat_case='Ins' "
                 "AND upos='NOUN' AND m_unsandhied IS NOT NULL GROUP BY m_unsandhied "
                 "ORDER BY COUNT(*) DESC LIMIT 10")
    check("R2-SE003-5", "top Ins noun m_unsandhied manasā/śareṇa/karmaṇā",
          (1_863, 1_603, 1_471),
          (f_ins.get("manasā"), f_ins.get("śareṇa"), f_ins.get("karmaṇā")),
          note=f"top: {list(f_ins.items())[:6]}")
    f_dat = dist("SELECT m_unsandhied, COUNT(*) FROM token WHERE feat_case='Dat' "
                 "AND upos='NOUN' AND m_unsandhied IS NOT NULL GROUP BY m_unsandhied "
                 "ORDER BY COUNT(*) DESC LIMIT 10")
    check("R2-SE003-6", "top Dat noun m_unsandhied agnaye/devāya/indrāya",
          (1_221, 1_065, 997),
          (f_dat.get("agnaye"), f_dat.get("devāya"), f_dat.get("indrāya")),
          note=f"top: {list(f_dat.items())[:6]}")

    # SE004: Gen+Part deprel composition — find the 334 and the advcl lemma list
    gp_deprels = dist("SELECT deprel, COUNT(*) FROM token WHERE feat_case='Gen' "
                      "AND feat_verbform='Part' AND deprel IS NOT NULL AND deprel<>'' "
                      "GROUP BY deprel ORDER BY COUNT(*) DESC")
    acl_nmod = sum(v for k, v in gp_deprels.items()
                   if k.startswith("acl") or k.startswith("nmod"))
    check("R2-SE004-6", "Gen+Part acl*+nmod* (nmod subtypes included)", 334, acl_nmod,
          note=f"full deprel dist: {gp_deprels}")
    advcl_lemmas = dist("SELECT lemma, COUNT(*) FROM token WHERE feat_case='Gen' "
                        "AND feat_verbform='Part' AND deprel LIKE 'advcl%' GROUP BY lemma")
    check("R2-SE004-7", "Gen+Part advcl lemma set contains a paś/dṛś watcher", True,
          any(l in advcl_lemmas for l in ("dṛś", "paś", "prapaś", "sampaś")),
          note=f"advcl lemmas: {advcl_lemmas}")

    # SE005: Loc+Part deprel dist — top-12 truncation hypothesis
    lp = dist("SELECT deprel, COUNT(*) FROM token WHERE feat_case='Loc' "
              "AND feat_verbform='Part' AND deprel IS NOT NULL AND deprel<>'' "
              "GROUP BY deprel ORDER BY COUNT(*) DESC")
    top12 = sum(sorted(lp.values(), reverse=True)[:12])
    check("R2-SE005-4", "Loc+Part: top-12-deprel sum (article's 557) vs true total",
          (557, 578), (top12, sum(lp.values())),
          note=f"full dist: {lp}")

    # SE008: syāt — lemma as, Opt, 3rd Sing (all surface variants)
    check("R2-SE008-3", "as+Opt+3+Sing tokens (syāt incl sandhi variants)", 9_505,
          q(f"SELECT COUNT(*) FROM token WHERE {FIN} AND lemma='as' AND feat_mood='Opt' "
            "AND feat_person='3' AND feat_number='Sing'"))

    # MO021: vakṣyāmi via m_unsandhied only
    check("R2-MO021-3", "vakṣyāmi count by m_unsandhied only", 579,
          q(f"SELECT COUNT(*) FROM token WHERE {FIN} AND feat_tense='Fut' "
            "AND m_unsandhied='vakṣyāmi'"))

    # MO010: pronouns with the script's exact universe (8 real cases, 3 numbers)
    PW = ("upos='PRON' AND feat_case IN "
          "('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc') "
          "AND feat_number IN ('Sing','Dual','Plur') AND lemma IS NOT NULL")
    check("R2-MO010-1", "PRON universe (script WHERE): tokens / lemmas",
          (544_999, 38),
          (q(f"SELECT COUNT(*) FROM token WHERE {PW}"),
           q(f"SELECT COUNT(DISTINCT lemma) FROM token WHERE {PW}")))
    per = {}
    for lemma_, case, num, cnt in cur.execute(
            f"SELECT lemma, feat_case, feat_number, COUNT(*) FROM token WHERE {PW} "
            "GROUP BY lemma, feat_case, feat_number"):
        rec = per.setdefault(lemma_, [set(), 0])
        rec[0].add((case, num))
        rec[1] += cnt
    got = tuple((l, per[l][1], len(per[l][0])) for l in
                ("tad", "yad", "mad", "idam", "tvad", "etad", "sarva", "ka"))
    check("R2-MO010-2", "top-8 pronoun tokens/cells (script universe)",
          (("tad", 184_809, 21), ("yad", 61_421, 21), ("mad", 60_575, 21),
           ("idam", 52_461, 22), ("tvad", 49_725, 21), ("etad", 40_991, 21),
           ("sarva", 22_865, 18), ("ka", 14_087, 18)), got)
    cov = sorted(len(v[0]) for v in per.values())
    m = len(cov)
    med = cov[m // 2] if m % 2 else (cov[m // 2 - 1] + cov[m // 2]) / 2
    check("R2-MO010-3", "pronoun median cells / mean / % >=18",
          (12.5, 12.13, 39.5),
          (med, round(sum(cov) / m, 2),
           round(100 * sum(1 for c in cov if c >= 18) / m, 1)))

    # MO002: flagship lemmas WITH the per-gender filter
    for cid, lemma_, g, exp_tok, exp_cells in (
            ("R2-MO002-3", "putra", "Masc", 9_729, 23),
            ("R2-MO002-4", "deva", "Masc", 17_536, 22),
            ("R2-MO002-5", "netra", "Neut", 385, 22),
            ("R2-MO002-6", "phala", "Neut", 3_973, 17)):
        tok = q("SELECT COUNT(*) FROM token WHERE upos='NOUN' AND lemma=? "
                "AND feat_gender=? AND feat_case IS NOT NULL AND feat_case<>'' "
                "AND feat_case<>'Cpd'", lemma_, g)
        cells_ = q("SELECT COUNT(DISTINCT feat_case||'/'||feat_number) FROM token "
                   "WHERE upos='NOUN' AND lemma=? AND feat_gender=? "
                   "AND feat_case IS NOT NULL AND feat_case<>'' AND feat_case<>'Cpd' "
                   "AND feat_number IS NOT NULL", lemma_, g)
        check(cid, f"{lemma_} ({g}): tokens / cells", (exp_tok, exp_cells), (tok, cells_))

    # MO002: tva as neuter lemma — round 1 matched 9,972; recheck netra oddity via
    # gender-free count for the record
    check("R2-MO002-5b", "netra tokens gender-free (round-1 got 712)", 712,
          q("SELECT COUNT(*) FROM token WHERE upos='NOUN' AND lemma='netra' "
            "AND feat_case IS NOT NULL AND feat_case<>'' AND feat_case<>'Cpd'"),
          note="the excess over 385 is netra tagged with other/missing gender")

    # WF004: -vant/-mant possessive class — variant hunt for 7,100 / 5,188 / 1,272
    variants = {
        "ADJ %vat": q("SELECT COUNT(*) FROM token WHERE upos='ADJ' AND lemma LIKE '%vat'"),
        "NOUN+ADJ %vat": q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') "
                           "AND lemma LIKE '%vat'"),
        "bhagavat all-upos": q("SELECT COUNT(*) FROM token WHERE lemma='bhagavat'"),
        "bhagavat NOUN": q("SELECT COUNT(*) FROM token WHERE lemma='bhagavat' "
                           "AND upos='NOUN'"),
        "bhagavat non-Cpd case": q("SELECT COUNT(*) FROM token WHERE lemma='bhagavat' "
                                   "AND feat_case IS NOT NULL AND feat_case<>'' "
                                   "AND feat_case<>'Cpd'"),
        "ADJ %mat": q("SELECT COUNT(*) FROM token WHERE upos='ADJ' AND lemma LIKE '%mat'"),
        "NOUN+ADJ %mat": q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') "
                           "AND lemma LIKE '%mat'"),
    }
    print(f"[R2-WF004-6] variant hunt for 7,100/-vant, 5,188/bhagavant, 1,272/-mant: "
          f"{variants}")
    results.append({"id": "R2-WF004-6", "label": "vant/mant variant hunt",
                    "expected": (7_100, 5_188, 1_272), "derived": variants,
                    "match": None, "note": "manual adjudication from variants"})

    # MO025: the -tuṃ anusvara gap
    check("R2-MO025-2", "Inf ending -tum OR -tuṃ (anusvara variant)", 9_681,
          q("SELECT COUNT(*) FROM token WHERE feat_verbform='Inf' AND "
            "(COALESCE(m_unsandhied,form) LIKE '%tum' "
            "OR COALESCE(m_unsandhied,form) LIKE '%tuṃ')"))

    n_ok = sum(1 for r in results if r["match"])
    n_j = sum(1 for r in results if r["match"] is None)
    print(f"\n=== {n_ok}/{len(results) - n_j} matched (+{n_j} manual) ===")
    OUT.write_text(json.dumps({"checks": results}, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
