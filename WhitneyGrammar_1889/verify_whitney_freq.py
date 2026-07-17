#!/usr/bin/env python
"""verify_whitney_freq.py — reproducible DCS battery for the Whitney frequency-claim
register (H1101).

THE METHODOLOGICAL INVERSION. In every other book of this pipeline Whitney 1889 is the
SYSTEMATIC-FACT REFERENCE against which the textbook's claims are judged. Here Whitney is
the TARGET: his own falsifiable QUANTITATIVE claims (frequencies, rarity, class sizes,
explicit hand-counts) are verified against the DCS-2021 corpus + internal consistency —
NOT against a higher authority, because Whitney IS the authority. So `sources: [dcs]`
throughout; there is no `whitney` source column here (that would be circular).

Two caveats built into the reading of the results:
  1. Whitney's CLASS-SIZE claims count ROOTS ("the a-class is made from ~240 roots"); DCS
     gives TOKENS. Where a claim is about roots, the token census only corroborates the
     DIRECTION, and the root-count proper needs WhitneyRoots/crosswalk/roots.csv (flagged
     per claim, drained separately).
  2. Whitney's per-text hand-counts (§826 aorist in Nala/Manu/…, §925 precative, §941
     conditional) are the novel showcase but need an aorist/precative token identifier the
     DCS sqlite does not expose cleanly (feat_tense has no 'Aor'); those are PENDING for the
     drain, not force-verdicted in the seed.

Usage:  python WhitneyGrammar_1889/verify_whitney_freq.py [--db PATH]
Writes  whitney_freq_stats.json next to this script.
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

# frequent verb lemmas Whitney calls out by name
NAMED_VERBS = ["kṛ", "brū", "dā", "dhā", "gam", "vac", "bhū", "as"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    c = db.cursor()

    # WH-H-101 — present-system vs all other finite verb-systems (feat_tense on finite verbs)
    tenses = dict(c.execute(
        "SELECT feat_tense, COUNT(*) FROM token WHERE upos='VERB' AND feat_verbform IS NULL "
        "AND feat_tense IS NOT NULL GROUP BY feat_tense").fetchall())
    pres = tenses.get("Pres", 0)
    others = sum(v for k, v in tenses.items() if k != "Pres")

    # WH-H-21 — mood census (conditional the rarest finite mood?)
    moods = dict(c.execute(
        "SELECT feat_mood, COUNT(*) FROM token WHERE feat_mood IS NOT NULL GROUP BY feat_mood").fetchall())

    # WH-H-112/121/107/6/11 — named-verb lemma frequencies + verb-lemma rank
    named = {}
    for lem in NAMED_VERBS:
        n = c.execute("SELECT COUNT(*) FROM token WHERE lemma=?", (lem,)).fetchone()[0]
        rank = c.execute(
            "SELECT COUNT(*)+1 FROM (SELECT lemma FROM token WHERE upos='VERB' GROUP BY lemma "
            "HAVING COUNT(*) > ?)", (n,)).fetchone()[0]
        named[lem] = {"tokens": n, "verb_lemma_rank": rank}

    # WH-H-300/301 — a-stem share of noun/adjective lemmas (lemma-ending proxy for a-stems)
    nom = c.execute("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ')").fetchone()[0]
    astem = c.execute(
        "SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE '%a'").fetchone()[0]

    # WH-H-302/303 — i-stem vs u-stem noun/adj lemma counts
    istem = c.execute("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE '%i'").fetchone()[0]
    ustem = c.execute("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE '%u'").fetchone()[0]

    out = {
        "_source": "DCS-2021 (Oliver Hellwig, CC BY) via VisualDCS dcs_full.sqlite — Whitney is the "
                   "TARGET, verified against the corpus, not the adjudicator (methodological inversion)",
        "WH-H-101_present_vs_others": {
            "present_system_tokens": pres, "all_other_finite_tokens": others,
            "ratio": round(pres / others, 2) if others else None, "tense_census": tenses,
            "confirmed": pres > others},
        "WH-H-21_mood_census": {
            "moods": dict(sorted(moods.items(), key=lambda kv: kv[1])),
            "rarest_finite_mood": min(moods, key=moods.get) if moods else None},
        "named_verb_frequencies": named,
        "WH-H-300_a_stem_share": {
            "a_ending_lemmas": astem, "noun_adj_lemmas": nom,
            "pct": round(100 * astem / nom, 1) if nom else None, "majority": astem > nom / 2},
        "WH-H-302_i_vs_u_stems": {"i_ending_lemmas": istem, "u_ending_lemmas": ustem,
                                  "i_gt_u": istem > ustem},
        "reused_ground_truth": {
            "WH-H-2_aorist_pct_of_verbal": "0.31% (2,452 tokens) — KocherginaUchebnik_1998 HK-1",
            "WH-H-116_largest_present_class": "class I (thematic a) 30.34% of present-system tokens — ZalizniakOcherk_1978 OCH-2",
            "WH-H-212_perfect_vs_imperfect": "perfect 61,986 > imperfect 47,554 (DCS aggregate) — BuhlerLeitfaden_1923 HB",
        },
    }
    (HERE / "whitney_freq_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"WH-H-101 present {pres} vs all-other {others} = {out['WH-H-101_present_vs_others']['ratio']}:1  -> {pres>others}")
    print(f"WH-H-21 mood census (rarest = {out['WH-H-21_mood_census']['rarest_finite_mood']}):", moods)
    print("named verbs:", {k: (v['tokens'], "rank~" + str(v['verb_lemma_rank'])) for k, v in named.items()})
    print(f"WH-H-300 a-stem lemmas {astem}/{nom} = {out['WH-H-300_a_stem_share']['pct']}% (majority={astem>nom/2})")
    print(f"WH-H-302 i-stems {istem} vs u-stems {ustem} (i>u={istem>ustem})")
    print("-> whitney_freq_stats.json written")


if __name__ == "__main__":
    main()
