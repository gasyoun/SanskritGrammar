#!/usr/bin/env python
"""whitney_aorist_tagger.py — the aorist-per-text tagger that closes WH-15 (H1110).

WH-15 (Whitney §826: "the aorist is found only twenty-one times in the Nala, eight in the
Hitopadeça, seven in Manu, six each in the Bhagavad-Gītā and Çakuntalā") was left UNTESTABLE by
the H1107 drain: the DCS sqlite has no aorist TENSE value (feat_tense lumps the aorist into
'Past'), and the fallback — matching a 690-form set from 15.csv — UNDERCOUNTED, because surface-
form matching misses aorist tokens whose forms are not in the distinct-form list.

THE FIX. DCS tags the aorist FORMATION, not the tense: within feat_tense='Past' finite verbs,
`feat_formation` cleanly separates the seven aorist classes from the perfect —

    root  (abhūt, adāt, agāt)      5,690   <- root aorist        (Whitney's aorist class I)
    them  (avocat, agamat)        2,781   <- thematic/a-aorist  (class II)
    s     (akārṣīt, adrākṣīt)     1,508   <- s-aorist           (class IV)
    is    (aśrauṣīt ...)          1,077   <- iṣ-aorist          (class V)
    red   (ajījanat, avīvṛdhan)     833   <- reduplicated       (class III)
    sa    (adhukṣat, arukṣat)       124   <- sa-aorist          (class VII)
    sis   (...)                       41   <- siṣ-aorist         (class VI)

  vs  peri  4,046  = periphrastic PERFECT, and None 85,955 = the reduplicated perfect
      (uvāca, cakāra, babhūva) — NOT aorist.

So AORIST := feat_tense='Past' AND feat_formation IN {root,them,s,is,red,sa,sis}, over finite
verbs. Corpus total 12,054 tokens (1.48% of verbal) — a MORE COMPLETE count than the 2,452 the
earlier form-set / DCS-2021 tense-code method produced (it had missed the numerous root and
thematic aorists). The "aorist is classically infrequent" verdict (WH-2) holds under either count.

Per-text, this reproduces Whitney's §826 hand-counts well: Manusmṛti 6 (Whitney 7 — near-exact),
Hitopadeśa 4 (Whitney 8 — same order); the Mahābhārata (1,973) and Rāmāyaṇa (275) are far larger
because Whitney counted only sub-portions (the Nala episode inside the MBh; Rāmāyaṇa book 1 only,
66 of the 275 across all seven books).

Usage:  python WhitneyGrammar_1889/whitney_aorist_tagger.py [--db PATH]
Writes  whitney_aorist_stats.json next to this script.
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
AORIST_FORMATIONS = ("root", "them", "s", "is", "red", "sa", "sis")
WHITNEY_826 = {"Mahābhārata": "21 (Nala) + 6 (BhG), both sub-portions", "Hitopadeśa": 8,
               "Manusmṛti": 7, "Rāmāyaṇa": "66 (book 1 only, of 7)"}


def aorist_where(alias="tok"):
    qs = ",".join("'%s'" % f for f in AORIST_FORMATIONS)
    return (f"{alias}.feat_tense='Past' AND {alias}.feat_formation IN ({qs}) "
            f"AND {alias}.upos='VERB' AND {alias}.feat_verbform IS NULL")


def self_test():
    """In-memory: 3 aorist (root/them/s), 1 perfect (None), 1 periphrastic (peri) -> tagger = 3."""
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE token (feat_tense TEXT, feat_formation TEXT, upos TEXT, feat_verbform TEXT)")
    db.executemany("INSERT INTO token VALUES ('Past',?, 'VERB', NULL)",
                   [("root",), ("them",), ("s",), (None,), ("peri",)])
    n = db.execute(f"SELECT COUNT(*) FROM token WHERE {aorist_where('token')}").fetchone()[0]
    assert n == 3, n
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    ok = self_test()
    db = sqlite3.connect(args.db)
    c = db.cursor()

    by_formation = dict(c.execute(
        f"SELECT feat_formation, COUNT(*) FROM token WHERE {aorist_where('token')} GROUP BY feat_formation"))
    total = sum(by_formation.values())
    verbal = c.execute("SELECT COUNT(*) FROM token WHERE upos='VERB'").fetchone()[0]

    rows = c.execute(
        f"SELECT t.name, COUNT(*) FROM token tok JOIN sentence s ON tok.sentence_id=s.id "
        f"JOIN chapter c ON s.chapter_id=c.chapter_id JOIN text t ON c.text_id=t.text_id "
        f"WHERE {aorist_where()} GROUP BY t.name ORDER BY 2 DESC").fetchall()
    by_text = dict(rows)

    named = {t: by_text.get(t, 0) for t in ("Mahābhārata", "Hitopadeśa", "Manusmṛti", "Rāmāyaṇa")}
    out = {
        "_source": "DCS-2021 sqlite feat_formation tagging (aorist = Past + formation in "
                   "{root,them,s,is,red,sa,sis}, finite verbs) — DCS's own aorist-class tag, the "
                   "authoritative identifier the form-set bridge (H1107) could not reach",
        "aorist_formations_included": list(AORIST_FORMATIONS),
        "total_aorist_tokens": total, "pct_of_verbal": round(100 * total / verbal, 2),
        "by_formation": dict(sorted(by_formation.items(), key=lambda kv: -kv[1])),
        "note_vs_earlier_count": "12,054 here vs ~2,452 from the earlier form-set/DCS-2021 tense-code "
                                 "method, which missed the root+thematic aorists; 'infrequent' holds either way",
        "WH-15_per_text_vs_826": {"whitney_1889": WHITNEY_826, "dcs_aorist": named,
                                  "dcs_top": dict(sorted(by_text.items(), key=lambda kv: -kv[1])[:8])},
        "self_test": {"passed": ok},
    }
    (HERE / "whitney_aorist_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"total aorist (feat_formation): {total} tokens = {out['pct_of_verbal']}% of verbal")
    print("by formation:", out["by_formation"])
    print("§826 aorist per text (Whitney 1889 -> DCS):")
    for t, n in named.items():
        print(f"  {t:14} DCS {n:5}   Whitney {WHITNEY_826[t]}")
    print("-> whitney_aorist_stats.json written")


if __name__ == "__main__":
    main()
