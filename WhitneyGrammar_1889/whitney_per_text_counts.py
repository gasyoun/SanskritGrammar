#!/usr/bin/env python
"""whitney_per_text_counts.py — the PER-TEXT hand-count drain instrument for the
Whitney frequency register (H1107).

Whitney's most striking quantitative claims are explicit HAND-COUNTS per named text — a 19th-
century philologist counting by hand: "the aorist is found only twenty-one times in the Nala,
eight in the Hitopadeça, seven in Manu" (§826); "the conditional ... not an example occurs in
Nala, Bhagavad-Gītā, or Hitopadeça; only one in Manu; and two in Çakuntalā" (§941); "the
precative ... occurs once and no more" in each of five texts (§925). This instrument reproduces
those counts from DCS-2021 per text.

TWO IDENTIFICATION PATHS:
  * conditional / precative — DIRECT: the sqlite tags them (feat_mood 'Cond' / 'Prec'); count per
    text via the text-name join.
  * aorist — BRIDGED: the sqlite lumps the aorist into feat_tense='Past' (no 'Aor'), so aorist
    tokens are identified by matching against the set of ~690 distinct aorist FORMS extracted from
    the DCS-2021 analysis table 15.csv (finite forms, tense_code in {10,11,12,13} = the four
    aorist categories). A surface form can in principle be ambiguous, so per-text aorist counts
    are an upper-ish bound, reported as such.

THE POINT is not an exact match — DCS's texts are full critical editions, often far larger than
the specific editions/portions Whitney counted in 1889, so absolute counts differ. What is
checked is (a) DIRECTION/rarity (does the form stay rare where Whitney says rare, absent where he
says absent) and (b) the RANK ORDER across texts.

Usage:  python WhitneyGrammar_1889/whitney_per_text_counts.py [--db PATH]
Writes  whitney_per_text_stats.json next to this script.
"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
FORMS_CSV = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2021" / "15.csv"
AOR_CODES = {10, 11, 12, 13}
# Whitney's §826 named texts (Nala/BhG are episodes inside the Mahābhārata in DCS)
WHITNEY_TEXTS = ["Mahābhārata", "Hitopadeśa", "Manusmṛti", "Rāmāyaṇa"]


def aorist_form_set():
    forms = set()
    for ln in FORMS_CSV.read_text(encoding="utf-8").splitlines()[1:]:
        p = ln.split(",")
        if len(p) < 4:
            continue
        try:
            if int(p[3]) in AOR_CODES:
                forms.add(p[2].strip().strip("'"))
        except ValueError:
            continue
    return forms


def per_text(cur, where, params=()):
    q = (f"SELECT t.name, COUNT(*) FROM token tok "
         f"JOIN sentence s ON tok.sentence_id=s.id JOIN chapter c ON s.chapter_id=c.chapter_id "
         f"JOIN text t ON c.text_id=t.text_id WHERE {where} GROUP BY t.name ORDER BY 2 DESC")
    return dict(cur.execute(q, params).fetchall())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    aor_forms = aorist_form_set()
    # per-text aorist: count Past-tagged tokens whose unsandhied form is a known aorist form
    qs = ",".join("?" * min(len(aor_forms), 900))
    aor_by_text = {}
    forms_list = list(aor_forms)
    # chunk the IN list (sqlite param cap) and sum
    from collections import Counter
    acc = Counter()
    for i in range(0, len(forms_list), 900):
        chunk = forms_list[i:i + 900]
        qch = ",".join("?" * len(chunk))
        rows = cur.execute(
            f"SELECT t.name, COUNT(*) FROM token tok JOIN sentence s ON tok.sentence_id=s.id "
            f"JOIN chapter c ON s.chapter_id=c.chapter_id JOIN text t ON c.text_id=t.text_id "
            f"WHERE tok.feat_tense='Past' AND tok.m_unsandhied IN ({qch}) GROUP BY t.name", chunk).fetchall()
        for name, n in rows:
            acc[name] += n
    aor_by_text = dict(acc)

    cond_by_text = per_text(cur, "tok.feat_mood='Cond'")
    prec_by_text = per_text(cur, "tok.feat_mood='Prec'")

    def named(d):
        return {t: d.get(t, 0) for t in WHITNEY_TEXTS}

    out = {
        "_source": "DCS-2021 sqlite (per-text token counts) + 15.csv aorist form-set (%d forms). "
                   "Reproduces Whitney's per-text hand-counts (§826 aorist, §941 conditional, §925 "
                   "precative). Absolute counts differ from Whitney's 1889 hand-counts because DCS "
                   "uses full critical editions; direction/rarity/rank is what is checked." % len(aor_forms),
        "aorist_form_set_size": len(aor_forms),
        "WH-H-1_aorist_per_text_826": {
            "whitney_1889": {"Nala(inside MBh)": 21, "Hitopadeśa": 8, "Manu": 7, "BhG(inside MBh)": 6, "Rāmāyaṇa_bk1": 66},
            "dcs_named": named(aor_by_text),
            "dcs_top": dict(sorted(aor_by_text.items(), key=lambda kv: -kv[1])[:8])},
        "WH-H-21_conditional_per_text_941": {
            "whitney_1889": {"Nala": 0, "BhG": 0, "Hitopadeśa": 0, "Manu": 1, "Śakuntalā": 2, "MBh": "~25"},
            "dcs_named": named(cond_by_text),
            "dcs_top": dict(sorted(cond_by_text.items(), key=lambda kv: -kv[1])[:8]),
            "hitopadeśa_absent_confirmed": cond_by_text.get("Hitopadeśa", 0) == 0},
        "WH-H-18_precative_per_text_925": {
            "whitney_1889": "once each in Manu/Nala/BhG/Śakuntalā/Hitopadeśa; <6 in the epics",
            "dcs_named": named(prec_by_text),
            "dcs_top": dict(sorted(prec_by_text.items(), key=lambda kv: -kv[1])[:8])},
    }
    (HERE / "whitney_per_text_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"aorist form-set: {len(aor_forms)} forms")
    print("§826 aorist per text (Whitney 1889 -> DCS):")
    for t in WHITNEY_TEXTS:
        print(f"  {t:14} DCS {aor_by_text.get(t,0)}")
    print("  DCS top aorist texts:", out["WH-H-1_aorist_per_text_826"]["dcs_top"])
    print("§941 conditional per text (Whitney: Hitopadeśa 0, Manu 1, MBh ~25):")
    print("  ", named(cond_by_text), " | Hitopadeśa absent:", out["WH-H-21_conditional_per_text_941"]["hitopadeśa_absent_confirmed"])
    print("§925 precative per text:", named(prec_by_text))
    print("-> whitney_per_text_stats.json written")


if __name__ == "__main__":
    main()
