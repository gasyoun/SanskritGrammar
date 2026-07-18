#!/usr/bin/env python3
"""H1229 round 3 — final probes with the generation scripts' EXACT predicates.

Round 2 left ~11 numbers unexplained. Reading the generation scripts directly
(scripts/sg_*.py) recovered the true definitions round 1/2 had approximated:

  SE002-1/2   nsubj/obj totals have NO case filter (sg_se_002 line 78/88)
  SE002-6     CORE_OBJ = obj,iobj,xcomp,xcomp:result,ccomp (line 40)
  SE003-5/6   "top forms" are per-LEMMA NOUN counts (sg_se_003 profile top_noun)
  SE008-3     syat = lemma 'as' + mood Opt, NO FIN filter (sg_se_008 profile)
  MO017-5     peri "aux" = surface TAIL of the peri token itself (AUX_AS/KR/BHU)
  MO021-3     top forms grouped by (m_unsandhied, lemma) pairs (sg_mo_021)
  WF004-6     lemma LIKE '%vant'/'%mant' on NOUN+ADJ (sg_wf_004 SURFACE list)
  MO025-2     classifier includes retroflex 'ṭum'/'ṭuṃ' (drastum-type); SQL LIKE
              '%tum' and Python endswith('tum') both MISS retroflex ṭ
  MO024-2     exact regexes: (tavy|tvya), (aniy|niy), y[a..]?[..]* on m_unsandhied
  WF001-5     16.8 vs true 16.857 — rounding-direction probe

Output: sangram/audit/audit_results_round3.json.
"""
import json
import sqlite3
import sys
import re
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

GITHUB = Path(__file__).resolve().parents[3]
DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT = Path(__file__).resolve().parent / "audit_results_round3.json"

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

    # SE002-1/2: totals WITHOUT case filter (sg_se_002_nom_acc.py:78,88)
    check("R3-SE002-1", "nsubj total, no case filter", 20_062,
          q("SELECT COUNT(*) FROM token WHERE deprel='nsubj'"))
    check("R3-SE002-2", "obj total, no case filter", 16_933,
          q("SELECT COUNT(*) FROM token WHERE deprel='obj'"))

    # SE002-6: CORE_OBJ incl xcomp:result (sg_se_002_nom_acc.py:40)
    core = q("""SELECT COUNT(*) FROM (
        SELECT c.sentence_id, c.head FROM token c
        JOIN token h ON h.sentence_id=c.sentence_id AND h.idx=c.head AND h.upos='VERB'
        WHERE c.feat_case='Acc'
        AND c.deprel IN ('obj','iobj','xcomp','xcomp:result','ccomp')
        GROUP BY c.sentence_id, c.head HAVING COUNT(*) >= 2)""")
    check("R3-SE002-6", "double-acc CORE_OBJ obj/iobj/xcomp/xcomp:result/ccomp",
          872, core)

    # SE003-5/6: per-LEMMA NOUN counts (sg_se_003 profile top_noun_lemmas)
    check("R3-SE003-5", "Ins NOUN lemmas manas/sara/karman", (1_863, 1_603, 1_471),
          (q("SELECT COUNT(*) FROM token WHERE feat_case='Ins' AND upos='NOUN' AND lemma='manas'"),
           q("SELECT COUNT(*) FROM token WHERE feat_case='Ins' AND upos='NOUN' AND lemma='śara'"),
           q("SELECT COUNT(*) FROM token WHERE feat_case='Ins' AND upos='NOUN' AND lemma='karman'")))
    check("R3-SE003-6", "Dat NOUN lemmas agni/deva/indra", (1_221, 1_065, 997),
          (q("SELECT COUNT(*) FROM token WHERE feat_case='Dat' AND upos='NOUN' AND lemma='agni'"),
           q("SELECT COUNT(*) FROM token WHERE feat_case='Dat' AND upos='NOUN' AND lemma='deva'"),
           q("SELECT COUNT(*) FROM token WHERE feat_case='Dat' AND upos='NOUN' AND lemma='indra'")))

    # SE008-3: lemma as + Opt, NO FIN filter (sg_se_008 profile top_lemmas)
    check("R3-SE008-3", "lemma 'as' + mood Opt, no FIN filter", 9_505,
          q("SELECT COUNT(*) FROM token WHERE feat_mood='Opt' AND lemma='as'"))

    # MO017-5: auxiliary TAIL of the peri token's own unsandhied form
    AUX_AS = ("āsa", "āsuḥ", "āsatuḥ", "āsathur", "āsan", "āsam", "āsi", "āsuṣ")
    AUX_KR = ("cakāra", "cakruḥ", "cakre", "cakratuḥ", "cakrire", "cakartha", "cakruṣ")
    AUX_BHU = ("babhūva", "babhūvuḥ", "babhūvatuḥ")
    aux = Counter()
    for (uns,) in cur.execute(
            f"SELECT COALESCE(m_unsandhied,'') FROM token WHERE {FIN} "
            "AND feat_tense='Past' AND feat_formation='peri'"):
        if uns.endswith(AUX_AS):
            aux["as"] += 1
        elif uns.endswith(AUX_KR):
            aux["kṛ"] += 1
        elif uns.endswith(AUX_BHU):
            aux["bhū"] += 1
        else:
            aux["other"] += 1
    check("R3-MO017-5", "peri aux tails as/kr/bhu (surface of peri token)",
          (3_697, 298, 32), (aux["as"], aux["kṛ"], aux["bhū"]),
          note=f"other bucket: {aux['other']}")

    # MO021-3: grouped by (m_unsandhied, lemma) pair (sg_mo_021_future.py)
    pair = q(f"SELECT COUNT(*) FROM token WHERE {FIN} AND feat_tense='Fut' "
             "AND m_unsandhied='vakṣyāmi' AND lemma='vac'")
    check("R3-MO021-3", "vaksyami grouped with lemma vac", 579, pair,
          note="the 580th token carries a different lemma")

    # WF004-6: lemma LIKE %vant / %mant on NOUN+ADJ (sg_wf_004 SURFACE)
    check("R3-WF004-6", "lemma %vant tokens / bhagavant / %mant",
          (7_100, 5_188, 1_272),
          (q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE '%vant'"),
           q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma='bhagavant'"),
           q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE '%mant'")))

    # MO025-2: retroflex-aware classifier on m_unsandhied only (sg_mo_025 classify)
    suf = Counter()
    for (m,) in cur.execute("SELECT m_unsandhied FROM token WHERE feat_verbform='Inf'"):
        if not m:
            suf["(none)"] += 1
        elif m.endswith(("tum", "tuṃ", "ṭum", "ṭuṃ")):
            suf["tum"] += 1
        elif re.search(r"(tavai|tave)$", m):
            suf["tave"] += 1
        elif re.search(r"(toḥ|tos)$", m):
            suf["toḥ"] += 1
        elif m.endswith("dhyai"):
            suf["dhyai"] += 1
        else:
            suf["other"] += 1
    check("R3-MO025-2", "Inf split, script classifier (retroflex ṭum included)",
          (9_681, 320, 154, 97),
          (suf["tum"], suf["tave"], suf["toḥ"], suf["dhyai"]),
          note=f"other {suf['other']} / none {suf['(none)']}")

    # MO024-2: exact gerundive regexes on m_unsandhied (sg_mo_024 classify)
    gdv = Counter()
    for (m,) in cur.execute("SELECT m_unsandhied FROM token WHERE feat_verbform='Gdv'"):
        if not m:
            gdv["(none)"] += 1
        elif re.search(r"(tavy|tvya)", m):
            gdv["tavya"] += 1
        elif re.search(r"(anīy|nīy)", m):
            gdv["anīya"] += 1
        elif re.search(r"y[aāeoiu]?[mṃnḥst]*$", m):
            gdv["ya"] += 1
        else:
            gdv["other"] += 1
    check("R3-MO024-2", "Gdv split, script classifier -ya/-tavya/-aniya",
          (19_901, 5_740, 1_280), (gdv["ya"], gdv["tavya"], gdv["anīya"]),
          note=f"other {gdv['other']} / none {gdv['(none)']}")

    # WF001-5: rounding-direction probe for the 16.8% share
    share = 100 * (523_738 + 435_081) / 5_688_416
    check("R3-WF001-5", "root+affix share: true value vs published 16.8",
          16.8, round(share, 1),
          note=f"exact {share:.4f}%: round-half-up gives 16.9; published 16.8 "
               "can only come from truncation — a genuine (trivial) error")

    n_ok = sum(1 for r in results if r["match"])
    print(f"\n=== {n_ok}/{len(results)} matched ===")
    OUT.write_text(json.dumps({"checks": results}, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
