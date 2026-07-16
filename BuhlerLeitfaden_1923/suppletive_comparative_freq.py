#!/usr/bin/env python
"""suppletive_comparative_freq.py — corpus-frequency check for §XXXII.3 (HB-256).

Bühler §XXXII.3 gives a CLOSED list of the "most frequent" irregular
(root-suppletive) comparative/superlative pairs — as opposed to §XXXII.2's
REGULAR -īyas/-iṣṭha formation (attached to a root, productive: pāpa ->
pāpīyas, paṭu -> paṭīyas, mahat -> mahīyas, etc., which is NOT the closed
set this claim is about). The 9 pairs named in point 3, read directly from
the mdx (not reconstructed from memory):

    antika -> nedīyas/nediṣṭha        guru -> garīyas/gariṣṭha
    alpa -> kanīyas/kaniṣṭha (alt: alpīyas/alpiṣṭha)
    dīrgha -> drāghīyas/drāghiṣṭha    praśasya -> śreyas/śreṣṭha (alt: jyāyas/jyeṣṭha)
    priya -> preyas/preṣṭha           bahu -> bhūyas/bhūyiṣṭha
    yuvan -> yavīyas/yaviṣṭha         vṛddha -> varṣīyas/varṣiṣṭha (alt: jyāyas/jyeṣṭha)

CLAIM: these occur "most frequently" — read as an ABSOLUTE-frequency claim
(these are common, everyday comparative expressions) against the wider
population of possible -īyas/-iṣṭha forms (§XXXII.2's rule can in
principle apply to any root, but rarely actually surfaces that way in
real usage) — not a strict internal ranking claim among the 9 themselves.

METHOD: rank ALL upos=ADJ lemmas ending in "yas" (comparative) or "iṣṭha"
(superlative) by DCS-2026 token frequency, after excluding known
false-positive homographs that are NOT suppletive comparative/superlative
forms at all (checked individually, not presumed): ṣaṣṭha (ordinal
'sixth'), vāsiṣṭha (patronymic 'descendant of Vasiṣṭha'), niṣṭha
('devoted/fixed'), apratiṣṭha ('unstable'), vihāyas ('vast, of the sky'),
dhāyas/pravayas (unrelated age/nurture nouns-as-adjectives).

Usage:  python BuhlerLeitfaden_1923/suppletive_comparative_freq.py [--db PATH]
Writes  hb256_suppletive_comparative_freq.json next to this script.
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

EXCLUDE = {"ṣaṣṭha", "vāsiṣṭha", "niṣṭha", "apratiṣṭha", "vihāyas", "dhāyas", "pravayas"}

# the 9 pairs read directly from Bühler §XXXII.3 (mdx line 4587-4607)
NAMED_PAIRS = [
    ("antika", "nedīyas", "nediṣṭha"),
    ("alpa", "kanīyas", "kaniṣṭha"),
    ("guru", "garīyas", "gariṣṭha"),
    ("dīrgha", "drāghīyas", "drāghiṣṭha"),
    ("praśasya", "śreyas", "śreṣṭha"),
    ("priya", "preyas", "preṣṭha"),
    ("bahu", "bhūyas", "bhūyiṣṭha"),
    ("yuvan", "yavīyas", "yaviṣṭha"),
    ("vṛddha", "varṣīyas", "varṣiṣṭha"),
]
NAMED_ALT_FORMS = {"alpīyas", "alpiṣṭha", "jyāyas", "jyeṣṭha"}  # alternates cited in the same §


def ranked(cur, suffix):
    rows = cur.execute(
        "SELECT lemma, COUNT(*) c FROM token WHERE upos='ADJ' AND lemma LIKE ? "
        "GROUP BY lemma ORDER BY c DESC", (f"%{suffix}",)
    ).fetchall()
    return [(l, c) for l, c in rows if l not in EXCLUDE]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    comp = ranked(cur, "yas")
    # -iṣṭha's vowel grades to -eṣṭha for e-grade roots (śreṣṭha, preṣṭha) — match the
    # bare -ṣṭha suffix (broader than -iṣṭha) and rely on the exclusion list for the
    # genuine non-superlative homographs (ṣaṣṭha 'sixth', etc.), same as the comparative side.
    supl = ranked(cur, "ṣṭha")

    comp_rank = {l: i + 1 for i, (l, c) in enumerate(comp)}
    supl_rank = {l: i + 1 for i, (l, c) in enumerate(supl)}
    comp_freq = dict(comp)
    supl_freq = dict(supl)

    pairs_out = []
    for root, cf, sf in NAMED_PAIRS:
        pairs_out.append({
            "root": root, "comparative": cf, "superlative": sf,
            "comparative_tokens": comp_freq.get(cf, 0),
            "comparative_rank_of_n": [comp_rank.get(cf), len(comp)],
            "superlative_tokens": supl_freq.get(sf, 0),
            "superlative_rank_of_n": [supl_rank.get(sf, None), len(supl)],
        })

    named_comp_lemmas = {p[1] for p in NAMED_PAIRS} | NAMED_ALT_FORMS
    named_supl_lemmas = {p[2] for p in NAMED_PAIRS} | NAMED_ALT_FORMS
    top10_comp = [l for l, c in comp[:10]]
    top10_supl = [l for l, c in supl[:10]]
    named_in_top10_comp = sum(1 for l in top10_comp if l in named_comp_lemmas)
    named_in_top10_supl = sum(1 for l in top10_supl if l in named_supl_lemmas)

    out = {
        "instrument": "suppletive_comparative_freq.py over dcs_full.sqlite — lemma "
                      "frequency ranking of ADJ comparatives (-yas) and superlatives "
                      "(-iṣṭha), false-positive homographs excluded (checked individually)",
        "excluded_false_positives": sorted(EXCLUDE),
        "named_pairs_from_buhler_XXXII_3": pairs_out,
        "comparative_ranking_top15": comp[:15],
        "superlative_ranking_top15": supl[:15],
        "named_forms_in_comparative_top10": named_in_top10_comp,
        "named_forms_in_superlative_top10": named_in_top10_supl,
        "total_comparative_lemma_types": len(comp),
        "total_superlative_lemma_types": len(supl),
        "expected_by_hb256": "the named 9 pairs occupy most of the top ranks (high "
                              "absolute frequency), not necessarily strict #1..#9 order",
        "confirmed": named_in_top10_comp >= 6 and named_in_top10_supl >= 6,
    }
    (HERE / "hb256_suppletive_comparative_freq.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"comparative lemma types: {len(comp)}, superlative lemma types: {len(supl)}")
    print(f"named forms in comparative top-10: {named_in_top10_comp}/10 "
          f"({top10_comp})")
    print(f"named forms in superlative top-10: {named_in_top10_supl}/10 "
          f"({top10_supl})")
    for p in pairs_out:
        print(f"  {p['root']:10} {p['comparative']:12} {p['comparative_tokens']:5} tok "
              f"(rank {p['comparative_rank_of_n'][0]}/{p['comparative_rank_of_n'][1]})  "
              f"{p['superlative']:12} {p['superlative_tokens']:5} tok "
              f"(rank {p['superlative_rank_of_n'][0]}/{p['superlative_rank_of_n'][1]})")
    print("confirmed:", out["confirmed"])
    print("-> hb256_suppletive_comparative_freq.json written")


if __name__ == "__main__":
    main()
