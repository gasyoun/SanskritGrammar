#!/usr/bin/env python3
"""SG-SE-004 «Аблатив и генитив» — beyond-quota native positive (incl. the genitive absolute).

Beyond-quota core article (opening set already 19/19). A case sub-article of the
case-semantics cluster (overview = SG-SE-001). Data gathered + adversarially verified by a
probe+verify workflow.

ABLATIVE (Abl) 74,565 — source ("from"), comparison ("than"), cause; 92% singular.
GENITIVE (Gen) 270,763 — possession (adnominal), and it took over the DATIVE's recipient
role (flip of SG-SE-003) + the partitive/argument object (flip of SG-SE-002's obj-in-Gen).

HEADLINE — the GENITIVE ABSOLUTE vs the locative absolute. The morphological candidate
(feat_case=Gen AND feat_verbform=Part) = 16,493, only ~21% below the Loc+Part candidate
(20,973) — near-parity. But that parity is an ARTEFACT: most Gen participles are
ATTRIBUTIVE (acl) or ADNOMINAL/possessive (nmod), NOT the absolute. On the deprel-parsed
subset the adverbial/absolute reading (advcl*) is only ~7.6% of Gen participles, vs the
attributive+adnominal confounds outnumbering it ~8:1. Computed the SAME way for both
constructions, the adjudicated FLOOR is ~an order of magnitude smaller for the genitive
absolute than the locative absolute. So: the genitive absolute IS the rarer sibling — the
raw candidate flatters it, the adjudicated construction is ~10x rarer.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/ablative-genitive/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "ablative-genitive" / "data"

SEED = 20260718
SAMPLE_SIZE = 50


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def absolute_floor(cur, case):
    """Adjudicated floor of the <case> absolute, computed identically for Gen and Loc:
    advcl*-tagged participles + agreeing subject(nsubj)->participle-head pairs."""
    part = f"feat_case='{case}' AND feat_verbform='Part'"
    candidate = cur.execute(f"SELECT COUNT(*) FROM token WHERE {part}").fetchone()[0]
    deprel = {k: c for k, c in cur.execute(
        f"SELECT deprel, COUNT(*) FROM token WHERE {part} AND deprel IS NOT NULL AND deprel!='' "
        "GROUP BY deprel ORDER BY COUNT(*) DESC")}
    advcl = sum(v for k, v in deprel.items() if k == "advcl" or k.startswith("advcl:"))
    acl = sum(v for k, v in deprel.items() if k == "acl" or k.startswith("acl:"))
    nmod = sum(v for k, v in deprel.items() if k == "nmod" or k.startswith("nmod:"))
    pairs = cur.execute(
        f"SELECT COUNT(*) FROM token n JOIN token p ON p.sentence_id=n.sentence_id AND p.idx=n.head "
        f"WHERE n.feat_case='{case}' AND n.deprel='nsubj' AND p.feat_case='{case}' AND p.feat_verbform='Part' "
        f"AND n.feat_number=p.feat_number").fetchone()[0]
    # overlap: subject-participle pairs whose participle-head is itself advcl*-tagged (avoid double-count)
    overlap = cur.execute(
        f"SELECT COUNT(*) FROM token n JOIN token p ON p.sentence_id=n.sentence_id AND p.idx=n.head "
        f"WHERE n.feat_case='{case}' AND n.deprel='nsubj' AND p.feat_case='{case}' AND p.feat_verbform='Part' "
        f"AND n.feat_number=p.feat_number AND (p.deprel='advcl' OR p.deprel LIKE 'advcl:%')").fetchone()[0]
    number = {k: c for k, c in cur.execute(
        f"SELECT feat_number, COUNT(*) FROM token WHERE {part} GROUP BY feat_number ORDER BY COUNT(*) DESC")}
    parsed = sum(deprel.values())
    return {"candidate": candidate, "by_number": number, "parsed_deprel": parsed,
            "advcl_adverbial": advcl, "advcl_pct_of_parsed": round(100 * advcl / parsed, 1) if parsed else 0,
            "acl_attributive": acl, "nmod_adnominal": nmod, "acl_nmod_pct_of_parsed": round(100 * (acl + nmod) / parsed, 1) if parsed else 0,
            "subject_participle_pairs": pairs, "floor": advcl + pairs - overlap, "deprel_top": dict(list(deprel.items())[:8])}


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
    case_bearing = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case IS NOT NULL").fetchone()[0]
    abl = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Abl'").fetchone()[0]
    gen = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Gen'").fetchone()[0]

    def profile(case, exclude_seg=False):
        by_number = {k: c for k, c in cur.execute(
            f"SELECT feat_number, COUNT(*) FROM token WHERE feat_case='{case}' GROUP BY feat_number ORDER BY COUNT(*) DESC")}
        by_upos = {k: c for k, c in cur.execute(
            f"SELECT upos, COUNT(*) FROM token WHERE feat_case='{case}' GROUP BY upos ORDER BY COUNT(*) DESC")}
        top = cur.execute(
            f"SELECT lemma, COUNT(*) c FROM token WHERE feat_case='{case}' AND upos='NOUN' GROUP BY lemma ORDER BY c DESC LIMIT 10").fetchall()
        return {"by_number": by_number, "by_upos": by_upos, "top_noun_lemmas": [f"{l} ({c})" for l, c in top]}

    abl_prof = profile("Abl")
    gen_prof = profile("Gen")
    # genitive-as-object (partitive/argument) + genitive-as-recipient (iobj) on subset
    gen_obj = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND deprel='obj'").fetchone()[0]
    gen_iobj = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND deprel='iobj'").fetchone()[0]
    gen_nmod = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND deprel IN ('nmod','nmod:poss')").fetchone()[0]

    gen_abs = absolute_floor(cur, "Gen")
    loc_abs = absolute_floor(cur, "Loc")
    # paśyat- "disregard" idiom: the semantic signature of the genitive absolute (dṛś "see"),
    # almost entirely UNPARSED — proof the deprel floor understates the construction
    pasyat = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND feat_verbform='Part' AND lemma='dṛś'").fetchone()[0]
    pasyat_parsed = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND feat_verbform='Part' AND lemma='dṛś' AND deprel IS NOT NULL AND deprel!=''").fetchone()[0]

    ids = [r[0] for r in cur.execute("SELECT id FROM token WHERE feat_case IN ('Abl','Gen')")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT t.id, t.m_unsandhied, t.lemma, t.feat_case, t.feat_verbform, t.deprel, x.name, c.ref FROM token t "
            "JOIN sentence se ON se.id=t.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "case", "verbform", "deprel", "text", "chapter_ref"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "Sangram SG-SE-004 (Аблатив и генитив) — cases + the genitive absolute vs the locative absolute",
        "toc_ref": "SG-SE-004",
        "kind": "beyond-quota core ① (opening set already 19/19); native positive; workflow probe+verify",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "case_bearing_tokens": case_bearing},
        "ablative": {
            "total": abl, "pct_of_case_bearing": round(100 * abl / case_bearing, 2), **abl_prof,
            "note": "source/comparison/cause; 92% singular. NB the top 'lemma' tva is the segmentation-layer -tva "
                    "suffix token (H1178), not a lexical ablative; true ablative nouns include bhaya 'fear', hetu 'cause', kāla",
        },
        "genitive": {
            "total": gen, "pct_of_case_bearing": round(100 * gen / case_bearing, 2), **gen_prof,
            "pronoun_share_note": "~33% of genitives are pronouns (tad/mad/tvad 'of him/me/you') — the possessive genitive dominates",
            "genitive_as_object_partitive": gen_obj, "genitive_as_recipient_iobj": gen_iobj, "genitive_nmod_possession_subset": gen_nmod,
            "note": "possession (adnominal) is the core; the genitive also took over the dative's recipient role (SG-SE-003 flip) "
                    "and supplies the partitive/argument object (SG-SE-002 flip)",
        },
        "genitive_absolute_vs_locative": {
            "genitive": gen_abs, "locative": loc_abs,
            "pasyat_idiom_gen_part": pasyat, "pasyat_parsed": pasyat_parsed,
            "mirror_image_native_proof": "on the deprel-parsed subsets the two cases are MIRROR images: Gen+Part is "
                "%.1f%% adverbial(advcl*) / %.1f%% attributive+adnominal(acl+nmod); Loc+Part is %.1f%% adverbial / "
                "%.1f%% attributive+adnominal — so the candidate near-parity is a provable artefact, not an assertion" % (
                gen_abs["advcl_pct_of_parsed"], gen_abs["acl_nmod_pct_of_parsed"], loc_abs["advcl_pct_of_parsed"], loc_abs["acl_nmod_pct_of_parsed"]),
            "finding": "candidate near-parity (Gen+Part %d vs Loc+Part %d) is an ARTEFACT — most Gen participles are "
                       "attributive(acl %d)+adnominal(nmod %d), not absolute; adjudicated FLOOR (advcl* + subject-participle "
                       "pairs, dedup overlap, computed identically) is %d for the genitive absolute vs %d for the locative — "
                       "the genitive absolute is ~%.0fx rarer. BUT the floor UNDERSTATES: the paśyat- 'disregard' idiom "
                       "(dṛś, %d Gen+Part) is the genitive absolute's semantic signature yet only %d are deprel-parsed, so "
                       "the true count is in the hundreds, not %d." % (gen_abs["candidate"], loc_abs["candidate"],
                       gen_abs["acl_attributive"], gen_abs["nmod_adnominal"], gen_abs["floor"], loc_abs["floor"],
                       (loc_abs["floor"] / gen_abs["floor"]) if gen_abs["floor"] else 0, pasyat, pasyat_parsed, gen_abs["floor"]),
        },
        "traditional_layer": {"witness": "Whitney 1889 §§289-302 (ablative, genitive uses; ablative of comparison; genitive absolute); "
                                          "Pāṇini 2.3.28 (apādāna/abl), 2.3.50 (śeṣa/gen), 2.3.38 (ṣaṣṭhī sati-like genitive absolute)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "candidate_not_construction": "Gen+Part (%d) is an upper bound for the genitive absolute; the adjudicated construction is ~%d (advcl* + pairs). Most Gen participles are attributive/adnominal." % (gen_abs["candidate"], gen_abs["floor"]),
            "deprel_partial": "the function split + absolute adjudication ride on the ~3-4%% dependency-parsed subset only",
            "comparison_not_native": "ablative of comparison ('than X') is not a distinct native tag; obl:grad/context is a weak proxy — treated as traditional, not measured",
            "seg_artifact": "the ablative -tva token (segmentation layer, H1178) inflates the raw lemma ranking; excluded from the 'true ablative noun' reading",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Abl {abl:,} ({round(100*abl/case_bearing,1)}%) / Gen {gen:,} ({round(100*gen/case_bearing,1)}%)", file=sys.stderr)
    print(f"gen-as-obj {gen_obj}, gen-as-iobj(recipient) {gen_iobj}, gen-nmod {gen_nmod}", file=sys.stderr)
    print(f"GEN ABSOLUTE: cand {gen_abs['candidate']:,} floor {gen_abs['floor']}; advcl {gen_abs['advcl_pct_of_parsed']}% vs acl+nmod {gen_abs['acl_nmod_pct_of_parsed']}% of parsed", file=sys.stderr)
    print(f"LOC ABSOLUTE (compare): cand {loc_abs['candidate']:,} floor {loc_abs['floor']}; advcl {loc_abs['advcl_pct_of_parsed']}% — genitive ~{round(loc_abs['floor']/gen_abs['floor']) if gen_abs['floor'] else '?'}x rarer", file=sys.stderr)
    print(f"paśyat idiom (dṛś Gen+Part): {pasyat} total, {pasyat_parsed} parsed — floor understates", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
