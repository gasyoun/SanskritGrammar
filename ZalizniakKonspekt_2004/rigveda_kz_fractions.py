#!/usr/bin/env python
"""rigveda_kz_fractions.py — Rigveda-period isolation for the five KZ exact-fraction claims.

THE INSTRUMENT the Konspekt register's blocked queue was waiting for (H797): Zaliznyak states
five Rigveda-specific declension/conjugation variant frequencies as exact fractions (mdx lines
507-519). The corpus-wide DCS aggregates cannot adjudicate them; this script isolates the
Ṛgveda inside the pinned VisualDCS SQLite master (the same snapshot the Sangram a-stems pilot
consumes — provenance table pins dcs-conllu commit 04e0778) and computes each fraction from
per-token morph features + unsandhied forms.

Slices are resolved by text NAME ('Ṛgveda'), never a hardcoded text_id. a-stem membership =
lemma ending in short -a; nominal counts use upos NOUN/ADJ (pronouns excluded — their NVpl is
the pronominal -e type, outside Zaliznyak's а-склонение scope).

Usage:  python ZalizniakKonspekt_2004/rigveda_kz_fractions.py [--db PATH]
Writes  rigveda_kz_stats.json next to this script.
"""
import argparse, json, sqlite3, sys
from fractions import Fraction
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"


def rv_tokens(cur, extra_where, params=()):
    q = f"""
      SELECT t.m_unsandhied, t.form, t.lemma
      FROM token t
      JOIN sentence s ON t.sentence_id = s.id
      JOIN chapter  c ON s.chapter_id = c.chapter_id
      JOIN text     x ON c.text_id = x.text_id
      WHERE x.name = 'Ṛgveda' AND {extra_where}"""
    for uns, form, lemma in cur.execute(q, params):
        yield (uns or form or ""), (lemma or "")


def is_a_stem(lemma):
    return lemma.endswith("a") and not lemma.endswith("ā")


def split_counts(rows, enders):
    """enders: dict bucket -> tuple of endings (longest first tested)."""
    out = {k: 0 for k in enders}
    ordered = sorted(((k, e) for k, es in enders.items() for e in es),
                     key=lambda t: -len(t[1]))
    for uns, lemma in rows:
        for k, e in ordered:
            if uns.endswith(e):
                out[k] += 1
                break
    return out


def frac(n, d):
    return round(100 * n / d, 1) if d else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance"))

    stats = {"_source": "VisualDCS/src/DCS-data-2026/dcs_full.sqlite, text='Ṛgveda'",
             "_provenance": {k: prov.get(k) for k in
                             ("source_repo", "source_commit", "n_texts", "n_tokens")}}

    # KZ line 507: NVpl m a-stems — -āsas vs -ās (claim: āsas in 1/3 of cases)
    rows = [(u, l) for u, l in rv_tokens(cur,
            "t.feat_case IN ('Nom','Voc') AND t.feat_number='Plur' AND t.feat_gender='Masc' "
            "AND t.upos IN ('NOUN','ADJ')") if is_a_stem(l)]
    c = split_counts(rows, {"āsas": ("āsaḥ", "āsas"), "ās": ("āḥ", "ās")})
    stats["KZ13_nvpl_m_asas"] = {**c, "asas_share_pct": frac(c["āsas"], c["āsas"] + c["ās"]),
                                 "claimed": "1/3 = 33.3%"}

    # KZ line 509: NVA du m a-stems — -ā vs -au (claim: ā in 7/8)
    rows = [(u, l) for u, l in rv_tokens(cur,
            "t.feat_case IN ('Nom','Voc','Acc') AND t.feat_number='Dual' AND t.feat_gender='Masc' "
            "AND t.upos IN ('NOUN','ADJ')") if is_a_stem(l)]
    c = split_counts(rows, {"ā": ("ā",), "au": ("au",)})
    stats["KZ14_nvadu_m_aa"] = {**c, "aa_share_pct": frac(c["ā"], c["ā"] + c["au"]),
                                "claimed": "7/8 = 87.5%"}

    # KZ line 511: NVApl n a-stems — -ā vs -āni (claim: ā in 3/5)
    rows = [(u, l) for u, l in rv_tokens(cur,
            "t.feat_case IN ('Nom','Voc','Acc') AND t.feat_number='Plur' AND t.feat_gender='Neut' "
            "AND t.upos IN ('NOUN','ADJ')") if is_a_stem(l)]
    c = split_counts(rows, {"āni": ("āni",), "ā": ("ā",)})
    stats["KZ15_nvapl_n_aa"] = {**c, "aa_share_pct": frac(c["ā"], c["ā"] + c["āni"]),
                                "claimed": "3/5 = 60%"}

    # KZ line 513: Ipl m/n a-stems — -ebhis vs -ais (claim: ebhis in 1/2)
    rows = [(u, l) for u, l in rv_tokens(cur,
            "t.feat_case='Ins' AND t.feat_number='Plur' AND t.feat_gender IN ('Masc','Neut') "
            "AND t.upos IN ('NOUN','ADJ')") if is_a_stem(l)]
    c = split_counts(rows, {"ebhis": ("ebhiḥ", "ebhis"), "ais": ("aiḥ", "ais")})
    stats["KZ16_ipl_ebhis"] = {**c, "ebhis_share_pct": frac(c["ebhis"], c["ebhis"] + c["ais"]),
                               "claimed": "1/2 = 50%"}

    # KZ line 519: 1pl present indicative — -masi vs -mas (claim: masi in 5/6)
    rows = list(rv_tokens(cur,
            "t.upos='VERB' AND t.feat_person='1' AND t.feat_number='Plur' "
            "AND t.feat_tense='Pres' AND t.feat_mood='Ind'"))
    c = split_counts(rows, {"masi": ("masi",), "mas": ("maḥ", "mas")})
    stats["KZ17_1pl_masi"] = {**c, "masi_share_pct": frac(c["masi"], c["masi"] + c["mas"]),
                              "claimed": "5/6 = 83.3%"}

    # KZ-11 (mdx line 545): injunctive much commoner in RV than Epic; optative the reverse.
    # Same instrument, second slice: per-text mood shares (finite verbs only).
    def mood_shares(text_name):
        q = """
          SELECT t.feat_mood, COUNT(*) FROM token t
          JOIN sentence s ON t.sentence_id=s.id
          JOIN chapter c ON s.chapter_id=c.chapter_id
          JOIN text x ON c.text_id=x.text_id
          WHERE x.name=? AND t.upos='VERB' AND t.feat_mood IS NOT NULL
          GROUP BY t.feat_mood"""
        d = dict(cur.execute(q, (text_name,)))
        tot = sum(d.values())
        return {"total_finite_mooded": tot,
                "injunctive_Jus": d.get("Jus", 0),
                "injunctive_pct": frac(d.get("Jus", 0), tot),
                "optative_Opt": d.get("Opt", 0),
                "optative_pct": frac(d.get("Opt", 0), tot)}

    stats["KZ11_mood_by_period"] = {
        "Rigveda": mood_shares("Ṛgveda"),
        "Mahābhārata": mood_shares("Mahābhārata"),
        "Rāmāyaṇa": mood_shares("Rāmāyaṇa"),
        "claimed": "injunctive much commoner in RV than Epic; optative rarer in RV",
    }

    # KZ-12 (mdx line 549): ta-participle predication rarer in RV than Epic, finite verbs
    # dominant. Dependency-root census (caveat: MBh/Rām dependency annotation covers a SUBSET
    # of their sentences — a sample, not the full text; RV coverage is dense).
    def root_predicates(text_name):
        q = """
          SELECT
            SUM(CASE WHEN t.upos='VERB' AND t.feat_verbform IS NULL THEN 1 ELSE 0 END),
            SUM(CASE WHEN t.feat_verbform='Part' AND t.feat_tense='Past' THEN 1 ELSE 0 END),
            COUNT(*)
          FROM token t
          JOIN sentence s ON t.sentence_id=s.id
          JOIN chapter c ON s.chapter_id=c.chapter_id
          JOIN text x ON c.text_id=x.text_id
          WHERE x.name=? AND t.deprel='root'"""
        fin, ppp, allroots = next(iter(cur.execute(q, (text_name,))))
        return {"root_tokens": allroots, "finite_verb_roots": fin, "past_part_roots": ppp,
                "ppp_share_of_verbal_roots_pct": frac(ppp, (fin or 0) + (ppp or 0))}

    stats["KZ12_root_predicates"] = {
        "Rigveda": root_predicates("Ṛgveda"),
        "Mahābhārata_sample": root_predicates("Mahābhārata"),
        "Rāmāyaṇa_sample": root_predicates("Rāmāyaṇa"),
        "caveat": "epic dependency annotation covers a subset of sentences (sample, not census)",
        "claimed": "ta-participle predication comparatively rare in RV; finite verbs dominant",
    }

    out = HERE / "rigveda_kz_stats.json"
    out.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    for k, v in stats.items():
        if k.startswith("KZ"):
            print(k, v)
    print(f"-> wrote {out.name}")


if __name__ == "__main__":
    main()
