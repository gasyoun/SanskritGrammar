#!/usr/bin/env python
"""compound_type_tagger.py — structural compound-type tagging for §193 (OCH-58).

The last instrument-cluster the Ocherk register named after H1000/H1001:
compound statistics. §193 claims dvigu — karmadhāraya with a cardinal
numeral (other than eka-) as first member — is a «сравнительно редко»
karmadhāraya subtype. DCS carries no compound-TYPE tagging, but compound
STRUCTURE is fully visible: mwt spans give the members of every surface
word, and upos (100% complete, FINDINGS §86) classes each member. Dvigu
candidacy is a structural property (NUM-first), so §193 is measurable.

WHAT IS CLASSIFIED (structural, function-blind — stated, not hidden):
  A cluster = one DCS mwt span with >= 2 members whose LAST member is
  nominal (NOUN/ADJ) — i.e. one surface word segmenting into a nominal
  compound (plus a small sandhi-join contamination shared by all classes,
  same caveat as H1000's compound axis).
  first-member class:
    NUM-first, lemma != eka   -> dvigu candidate (§193's own definition)
    NUM-first, lemma  = eka   -> the §'s explicit exclusion, counted apart
    ADJ-first                 -> karmadhāraya-shaped candidate core
    NOUN-first                -> tatpuruṣa/other determinative territory
    other                     -> pronoun/preverb/indeclinable-first etc.
  DETERMINATIVE-CANDIDATE POOL for the §193 ratio = ADJ-first + NUM-first
  clusters. Function-blind: bahuvrīhis of the same ADJ/NUM-first shape are
  inside the pool (probed 16-07-2026: DCS tags bahuvrīhi last-members
  LEXICALLY — mahābāhu's bāhu is NOUN in 192/193 clusters — so function
  CANNOT be separated on this snapshot; that is exactly OCH-60's blocker,
  left honestly open). The §193 ratio is therefore measured within the
  structurally-defined pool; since bahuvrīhi contamination applies to both
  the ADJ-first and NUM-first shapes, the 'comparatively rare' comparison
  survives it.

Usage:  python ZalizniakOcherk_1978/compound_type_tagger.py [--db PATH]
Writes  och58_compound_stats.json next to this script.
"""
import argparse
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"

NOMINAL = {"NOUN", "ADJ"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    # one pass: every mwt member row, ordered so each span's members arrive together
    q = """
      SELECT m.id, t.idx, t.lemma, t.upos
      FROM mwt m
      JOIN token t ON t.sentence_id = m.sentence_id
        AND t.idx BETWEEN CAST(substr(m.span, 1, instr(m.span,'-')-1) AS INTEGER)
                      AND CAST(substr(m.span, instr(m.span,'-')+1) AS INTEGER)
      WHERE instr(m.span, '-') > 0
      ORDER BY m.id, t.idx
    """
    counts = Counter()
    dvigu_first_lemmas = Counter()
    examples = defaultdict(list)

    def classify(members):
        if len(members) < 2:
            return None
        last_upos = members[-1][2]
        if last_upos not in NOMINAL:
            return None
        first_lemma, first_upos = members[0][1], members[0][2]
        if first_upos == "NUM":
            return ("eka_first" if first_lemma == "eka" else "dvigu_candidate", first_lemma)
        if first_upos == "ADJ":
            return ("adj_first", first_lemma)
        if first_upos == "NOUN":
            return ("noun_first", first_lemma)
        return ("other_first", first_lemma)

    span_id, members = None, []
    def flush():
        res = classify(members)
        if not res:
            counts["non_nominal_or_single"] += 1
            return
        cls, first_lemma = res
        counts[cls] += 1
        if cls == "dvigu_candidate":
            dvigu_first_lemmas[first_lemma] += 1
        if len(examples[cls]) < 5:
            examples[cls].append(" + ".join(m[1] for m in members))

    for mid, idx, lemma, upos in cur.execute(q):
        if mid != span_id:
            if span_id is not None:
                flush()
            span_id, members = mid, []
        members.append((idx, lemma, upos))
    if span_id is not None:
        flush()

    nominal_clusters = sum(counts[k] for k in
                           ("dvigu_candidate", "eka_first", "adj_first", "noun_first", "other_first"))
    determinative_pool = counts["dvigu_candidate"] + counts["eka_first"] + counts["adj_first"]

    stats = {
        "clusters_nominal_total": nominal_clusters,
        "by_first_member": {k: counts[k] for k in
                            ("dvigu_candidate", "eka_first", "adj_first", "noun_first", "other_first")},
        "determinative_candidate_pool (ADJ+NUM first)": determinative_pool,
        "dvigu_share_of_determinative_pool_pct":
            round(100 * counts["dvigu_candidate"] / determinative_pool, 2) if determinative_pool else None,
        "dvigu_share_of_all_nominal_clusters_pct":
            round(100 * counts["dvigu_candidate"] / nominal_clusters, 2) if nominal_clusters else None,
        "adj_first_share_of_determinative_pool_pct":
            round(100 * counts["adj_first"] / determinative_pool, 2) if determinative_pool else None,
        "dvigu_top_numerals": dict(dvigu_first_lemmas.most_common(12)),
        "examples": dict(examples),
    }

    checks = {
        "dvigu_candidates_nonzero": counts["dvigu_candidate"] > 0,
        "adj_first_dominates_num_first": counts["adj_first"] > counts["dvigu_candidate"],
        "eka_excluded_separately": counts["eka_first"] > 0,
        "classic_numerals_present": all(n in dvigu_first_lemmas for n in ("dvi", "tri", "catur")),
    }

    out = {
        "instrument": "compound_type_tagger.py over dcs_full.sqlite (dcs-conllu 04e0778); "
                      "structural first-member classification of mwt nominal clusters; "
                      "function-blind by design (OCH-60's blocker, probed and documented)",
        "och60_probe": "DCS tags compound members lexically: mahābāhu last-member NOUN in "
                       "192/193 clusters — tatpuruṣa/bahuvrīhi FUNCTION is not recoverable "
                       "from this snapshot; OCH-60 stays honestly UNTESTABLE",
        "stats": stats,
        "validation": checks,
    }
    (HERE / "och58_compound_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"nominal clusters: {nominal_clusters:,}")
    for k in ("adj_first", "noun_first", "dvigu_candidate", "eka_first", "other_first"):
        print(f"  {k:<16} {counts[k]:>9,}")
    print(f"dvigu share of determinative pool: {stats['dvigu_share_of_determinative_pool_pct']}% "
          f"(pool {determinative_pool:,})")
    print(f"dvigu share of ALL nominal clusters: {stats['dvigu_share_of_all_nominal_clusters_pct']}%")
    print("top dvigu numerals:", dict(dvigu_first_lemmas.most_common(6)))
    bad = [k for k, v in checks.items() if v is False]
    print("validation:", "OK" if not bad else f"FAILED: {bad}")
    print("-> och58_compound_stats.json written")


if __name__ == "__main__":
    main()
