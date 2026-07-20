#!/usr/bin/env python3
"""SG-SE-005 «Локатив» — beyond-quota native positive (locative + the locative absolute).

Beyond-quota core article (opening set already 19/19). A case sub-article of the
case-semantics cluster (overview = SG-SE-001). The headline is the LOCATIVE ABSOLUTE,
whose morphological fingerprint is directly native: feat_case='Loc' AND
feat_verbform='Part' (a participle standing in the locative — gate rāme "when Rama had
gone", udite sūrye "when the sun had risen").

Slot chosen by a scout+adversarial-verify workflow; the verify pass CONFIRMED the counts
but flagged an overclaim the article must respect: a "locative participle" is NOT the
same as a "locative absolute". The 20,973 count is the CANDIDATE set — it also contains
attributive Loc participles ("in the fallen X") and substantival/argument ones. DCS's
native dependency layer (deprel) would disambiguate, but it covers only ~578 (2.76%) of
them; where present it votes decisively adverbial (advcl:temp/advcl/advcl:cond dominate),
and a fully-native structural check (Loc noun heading an agreeing Loc participle) recovers
~222 explicit subject+participle pairs. So:
  * 20,973 = native CANDIDATE upper bound (morphology alone).
  * ~367 advcl*-tagged + ~222 subject-participle pairs = high-precision adjudicated FLOOR.
  * on the parsed subset ~65% are absolute-consistent, ~17% demonstrably non-absolute →
    extrapolated ~14-17% of the candidates are likely not absolutes.
Number skew (86.6% singular) is the diagnostic signature; feat_voice='Pass' isolates the
present-passive absolute; time-vs-place is NOT native (m_wordsem is a numeric sense id).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/locative/data/.
"""
import argparse
import csv
import hashlib
import json
import random
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "locative" / "data"

LP = "feat_case='Loc' AND feat_verbform='Part'"  # locative-participle = locative-absolute candidate
ADVCL = ("advcl:temp", "advcl", "advcl:cond")
SEED = 20260718
SAMPLE_SIZE = 50


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--skip-checksum", action="store_true")
    args = ap.parse_args()
    db = Path(args.db)
    if not db.exists():
        print(f"ERROR: DCS master not found: {db}", file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr)
        return 1
    sha = "skipped" if args.skip_checksum else sha256_file(db)

    total = cur.execute("SELECT COUNT(*) FROM token").fetchone()[0]
    # case-marked denominator family (SG-SE denominator contract, H1371) — the same basis
    # as the sibling case sub-articles: case_bearing incl the Cpd pseudo-case, real_vibhakti excl Cpd.
    case_bearing = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case IS NOT NULL").fetchone()[0]
    real_vibhakti = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case IN "
        "('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc')").fetchone()[0]
    loc = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Loc'").fetchone()[0]
    loc_number = {k: c for k, c in cur.execute(
        "SELECT feat_number, COUNT(*) FROM token WHERE feat_case='Loc' GROUP BY feat_number ORDER BY COUNT(*) DESC")}

    # locative-absolute candidate set: Loc participle
    lp = cur.execute(f"SELECT COUNT(*) FROM token WHERE {LP}").fetchone()[0]
    lp_number = {k: c for k, c in cur.execute(
        f"SELECT feat_number, COUNT(*) FROM token WHERE {LP} GROUP BY feat_number ORDER BY COUNT(*) DESC")}
    lp_voice_pass = cur.execute(f"SELECT COUNT(*) FROM token WHERE {LP} AND feat_voice='Pass'").fetchone()[0]
    lp_top = cur.execute(f"SELECT lemma, COUNT(*) c FROM token WHERE {LP} GROUP BY lemma ORDER BY c DESC LIMIT 12").fetchall()
    lp_deprel = {k: c for k, c in cur.execute(
        f"SELECT deprel, COUNT(*) FROM token WHERE {LP} AND deprel IS NOT NULL AND deprel!='' "
        "GROUP BY deprel ORDER BY COUNT(*) DESC LIMIT 12")}
    lp_deprel_total = sum(lp_deprel.values())
    lp_advcl = sum(lp_deprel.get(d, 0) for d in ADVCL)
    lp_attributive = lp_deprel.get("acl", 0)
    lp_oblique = sum(v for k, v in lp_deprel.items() if k.startswith("obl"))
    distinct_sent = cur.execute(f"SELECT COUNT(DISTINCT sentence_id) FROM token WHERE {LP}").fetchone()[0]

    # full subject+participle absolute pairs (native, high-precision): a Loc noun tagged nsubj that
    # DEPENDS ON (head->) a Loc participle, agreeing in number — the textbook absolute subject+predicate.
    # (direction matters: in the absolute the participle is the clause head and the noun is its nsubj child.)
    pairs = cur.execute(
        f"SELECT COUNT(*) FROM token n JOIN token p ON p.sentence_id=n.sentence_id AND p.idx=n.head "
        f"WHERE n.feat_case='Loc' AND n.deprel='nsubj' AND p.feat_case='Loc' AND p.feat_verbform='Part' "
        f"AND n.feat_number=p.feat_number").fetchone()[0]

    # pan-corpus spread
    by_text = cur.execute(
        f"SELECT x.name, COUNT(*) c FROM token t JOIN sentence se ON se.id=t.sentence_id "
        f"JOIN chapter c2 ON c2.chapter_id=se.chapter_id JOIN text x ON x.text_id=c2.text_id "
        f"WHERE t.feat_case='Loc' AND t.feat_verbform='Part' GROUP BY x.name ORDER BY c DESC LIMIT 6").fetchall()

    # seeded sample of loc participles
    ids = [r[0] for r in cur.execute(f"SELECT id FROM token WHERE {LP}")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT t.id, t.m_unsandhied, t.lemma, t.feat_number, t.feat_voice, t.deprel, x.name, c.ref, se.sent_counter "
            "FROM token t JOIN sentence se ON se.id=t.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "number", "voice", "deprel", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    non_absolute_annotated = lp_attributive + lp_oblique + lp_deprel.get("nsubj", 0)
    summary = {
        "study": "Sangram SG-SE-005 (Локатив) — locative + the locative absolute (native candidate + adjudicated floor)",
        "toc_ref": "SG-SE-005",
        "kind": "beyond-quota core ① (opening set already 19/19); native positive with adversarially-checked honesty framing",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "case_bearing_tokens": case_bearing,
                         "real_vibhakti_tokens": real_vibhakti, "locative_total": loc,
                         "locative_pct_of_case_bearing": round(100 * loc / case_bearing, 2),
                         "locative_pct_of_real_vibhakti": round(100 * loc / real_vibhakti, 2),
                         "locative_by_number": loc_number},
        "locative_absolute_candidate": {
            "loc_participle_candidate": lp,
            "pct_of_locative": round(100 * lp / loc, 1),
            "by_number": lp_number,
            "singular_pct": round(100 * lp_number.get("Sing", 0) / lp, 1),
            "voice_passive": lp_voice_pass,
            "top_lemmas": [f"{l} ({c})" for l, c in lp_top],
            "distinct_sentences": distinct_sent,
            "by_text_top": [f"{n} ({c})" for n, c in by_text],
            "candidate_note": "20,973 is the CANDIDATE / morphological upper bound (every Loc participle); it also "
                              "contains attributive and substantival Loc participles — the absolute is NOT natively flagged",
        },
        "adjudication_on_parsed_subset": {
            "any_deprel": lp_deprel_total,
            "pct_parsed": round(100 * lp_deprel_total / lp, 2),
            "adverbial_absolute_consistent_advcl": lp_advcl,
            "deprel_breakdown": lp_deprel,
            "attributive_acl": lp_attributive,
            "oblique_obl": lp_oblique,
            "structural_subject_participle_pairs": pairs,
            "note": "of the ~%d Loc participles carrying a deprel, advcl:temp/advcl/advcl:cond dominate (adverbial "
                    "clause = the absolute); acl (attributive) + obl (argument) are the non-absolute residue. "
                    "Extrapolating the ~65%%/~17%% split, roughly 14-17%% of the 20,973 candidates are likely non-absolute. "
                    "High-precision FLOOR = %d advcl*-tagged + %d subject-participle pairs." % (lp_deprel_total, lp_advcl, pairs),
        },
        "traditional_layer": {"witness": "Whitney 1889 §§303-305 (locative uses), §§303b (locative absolute / sati saptamī); "
                                          "Pāṇini 2.3.36-37 (adhikaraṇa) + 2.3.37 (bhāve / sati saptamī)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "candidate_not_construction": "loc participle (morphology) != locative absolute (construction); 20,973 is an upper bound",
            "deprel_partial": "the dependency layer covers only ~2.76%% of the candidates (and 74/270 texts); the absolute/attributive/argument split is native only on that subset",
            "tense_sparse": "feat_tense is None on 16,467/20,973 participles, so past-vs-present absolute cannot be totalled from feat_tense",
            "time_vs_place_not_native": "the locative's time-vs-place split is NOT a native field (m_wordsem is a numeric sense id); any such figure is an inferred lemma heuristic",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Loc {loc:,} (Sing {loc_number.get('Sing',0):,}); Loc-participle candidate {lp:,} ({round(100*lp/loc,1)}% of Loc)", file=sys.stderr)
    print(f"  singular {round(100*lp_number.get('Sing',0)/lp,1)}%; passive {lp_voice_pass:,}; parsed {lp_deprel_total} ({round(100*lp_deprel_total/lp,2)}%)", file=sys.stderr)
    print(f"  adverbial(advcl*) {lp_advcl}; attributive(acl) {lp_attributive}; obl {lp_oblique}; subj-part pairs {pairs}", file=sys.stderr)
    print(f"  top lemmas: {[f'{l}({c})' for l,c in lp_top[:6]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
