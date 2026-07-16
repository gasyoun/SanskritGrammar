#!/usr/bin/env python
"""aorist_type_ranking.py — formation-type frequency ranking for HK-5.

HK-5 claims Whitney's Type II (thematic a-aorist, avadat-type) is "самый
распространенный" (the most widespread) of Sanskrit's ~7 aorist formation
types. Prior verdict assumed DCS-2021 couldn't distinguish formation types
at all ("tags aorist only as Act/Med"). Not checked: DCS-2026's own
feat_formation tag under feat_tense=Past DOES distinguish exactly these 7
types (root/them/s/is/red/sa/sis = Whitney's types I/II/IV/V/III/VII/VI —
this is the SAME aorist-identification method built for HK-207/H1040).

RESULT IS GENUINELY MIXED, not a clean confirm or refute — dug into it
properly (genre split + a lexical-outlier check) before settling on a
verdict, same as OCH-66/67 earlier:

  WHOLE CORPUS, raw tokens:      root (Type I) leads, not them (Type II)
  WHOLE CORPUS, excluding bhū:   root STILL leads (not just a bhū artifact)
  WHOLE CORPUS, distinct lemmas: s (Type IV) leads, them is 3rd
  CLASSICAL subset, raw tokens:  root leads (but driven by bhū there)
  CLASSICAL subset, excl. bhū:   them (Type II) leads — the claim's best case
  CLASSICAL subset, distinct lemmas: them leads

So the claim holds specifically in classical (non-Vedic) narrative prose
once bhū's near-auxiliary "was/became" formula usage is set aside — but
does NOT hold as a flat, corpus-wide statement: root-aorist dominates the
whole (Vedic/Brāhmaṇa-heavy) corpus by raw token count even excluding bhū,
and s-aorist has the widest root-type distribution overall.

Usage:  python KocherginaUchebnik_1998/aorist_type_ranking.py [--db PATH]
Writes  hk5_aorist_type_ranking.json next to this script.
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

# DCS feat_formation -> Whitney's traditional aorist type number
FORMATION_TO_TYPE = {
    "root": "I (root aorist)", "them": "II (thematic a-aorist)",
    "red": "III (reduplicated aorist)", "s": "IV (s-aorist)",
    "is": "V (iṣ-aorist)", "sis": "VI (siṣ-aorist)", "sa": "VII (sa-aorist)",
}
CLASSICAL_TEXTS = {
    "Mahābhārata", "Manusmṛti", "Arthaśāstra", "Rāmāyaṇa", "Buddhacarita",
    "Kāmasūtra", "Suśrutasaṃhitā", "Carakasaṃhitā", "Kūrmapurāṇa", "Viṣṇupurāṇa",
    "Matsyapurāṇa", "Nyāyabindu", "Avadānaśataka", "Abhidharmakośa",
    "Bhāratamañjarī", "Aṣṭāṅgahṛdayasaṃhitā", "Haṭhayogapradīpikā",
    "Rasaratnasamuccayaṭīkā",
}


def rank(cur, text_ids=None, exclude_lemma=None):
    where = ["upos='VERB'", "feat_tense='Past'",
             "feat_formation IN ({})".format(",".join(f"'{k}'" for k in FORMATION_TO_TYPE))]
    params = []
    join = ""
    if text_ids is not None:
        join = "JOIN sentence s ON tok.sentence_id=s.id JOIN chapter c ON s.chapter_id=c.chapter_id"
        where.append(f"c.text_id IN ({','.join('?' * len(text_ids))})")
        params.extend(text_ids)
    if exclude_lemma:
        where.append("lemma != ?")
        params.append(exclude_lemma)
    q = f"""SELECT feat_formation, COUNT(*) tok, COUNT(DISTINCT lemma) lem
            FROM token tok {join} WHERE {' AND '.join(where)}
            GROUP BY feat_formation ORDER BY tok DESC"""
    rows = cur.execute(q, params).fetchall()
    return [{"formation": f, "type": FORMATION_TO_TYPE[f], "tokens": t, "distinct_lemmas": l}
            for f, t, l in rows]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    classical_ids = [tid for name, tid in cur.execute("SELECT name, text_id FROM text")
                     if name in CLASSICAL_TEXTS]

    whole_all = rank(cur, None, None)
    whole_excl_bhu = rank(cur, None, "bhū")
    classical_all = rank(cur, classical_ids, None)
    classical_excl_bhu = rank(cur, classical_ids, "bhū")

    def top_by_tokens(rows):
        return rows[0]["formation"] if rows else None

    def top_by_lemmas(rows):
        return max(rows, key=lambda r: r["distinct_lemmas"])["formation"] if rows else None

    checks = {
        "whole_corpus_tokens": top_by_tokens(whole_all) == "them",
        "whole_corpus_tokens_excl_bhu": top_by_tokens(whole_excl_bhu) == "them",
        "whole_corpus_lemma_types": top_by_lemmas(whole_all) == "them",
        "classical_tokens": top_by_tokens(classical_all) == "them",
        "classical_tokens_excl_bhu": top_by_tokens(classical_excl_bhu) == "them",
        "classical_lemma_types": top_by_lemmas(classical_all) == "them",
    }

    out = {
        "instrument": "aorist_type_ranking.py over dcs_full.sqlite — reuses the "
                      "feat_formation aorist-type identification built for HK-207 (H1040)",
        "whole_corpus": {"all_lemmas": whole_all, "excluding_bhu": whole_excl_bhu},
        "classical_subset": {"all_lemmas": classical_all, "excluding_bhu": classical_excl_bhu},
        "checks_them_is_top": checks,
        "confirmed_count": sum(checks.values()),
        "total_checks": len(checks),
        "conclusion": "mixed — thematic (Type II) leads only in the classical-subset, "
                      "bhū-excluded readings (both by token count and lemma-type count); "
                      "root aorist (Type I) leads the whole corpus even excluding bhū, "
                      "and s-aorist (Type IV) has the widest root-type distribution overall",
    }
    (HERE / "hk5_aorist_type_ranking.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for label, rows in (("whole corpus", whole_all), ("whole corpus (excl. bhū)", whole_excl_bhu),
                         ("classical", classical_all), ("classical (excl. bhū)", classical_excl_bhu)):
        print(f"--- {label} ---")
        for r in rows:
            print(f"  {r['type']:25} {r['tokens']:5} tok, {r['distinct_lemmas']:4} lemmas")
    print("checks (them = top):", checks)
    print(f"confirmed {out['confirmed_count']}/{out['total_checks']}")
    print("-> hk5_aorist_type_ranking.json written")


if __name__ == "__main__":
    main()
