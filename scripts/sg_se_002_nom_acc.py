#!/usr/bin/env python3
"""SG-SE-002 «Номинатив и аккузатив» — beyond-quota native positive (the two largest cases).

Beyond-quota core article (opening set already 19/19). A case sub-article of the
case-semantics cluster (overview = SG-SE-001). Nominative and accusative are the two
largest of the eight vibhakti, both from the native feat_case field. Beyond the raw
totals, the dependency layer (deprel, PARTIAL ~3.93% of tokens) gives the function split.

Slot data was gathered + ADVERSARIALLY VERIFIED by a probe+verify workflow; the verify
pass caught three overclaims this script and article respect:
  1. DOUBLE ACCUSATIVE: "verb heads with >=2 Acc dependents" (2,747) is NOT the classical
     dvikarmaka double-OBJECT — those Acc pairs mix object + adverbial-Acc (advmod) +
     directional/temporal-Acc (obl:goal/temp/path) + coordinated-Acc (conj). Restricted to
     genuine CORE-OBJECT roles (obj/iobj/xcomp/xcomp:result/ccomp) it is only ~760-870
     (36 heads have two true `obj`). We report the corrected number, not 2,747.
  2. feat_case='Cpd' (compound-member placeholder, 841,052) is LARGER than Acc; "two
     largest CASES" holds only excluding Cpd — stated.
  3. % must be reported both of all tokens and of case-bearing tokens (29.4% are caseless).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/nominative-accusative/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "nominative-accusative" / "data"

CORE_OBJ = ("obj", "iobj", "xcomp", "xcomp:result", "ccomp")
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
    case_bearing = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case IS NOT NULL").fetchone()[0]
    nom = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Nom'").fetchone()[0]
    acc = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Acc'").fetchone()[0]
    cpd = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Cpd'").fetchone()[0]
    deprel_tokens = cur.execute("SELECT COUNT(*) FROM token WHERE deprel IS NOT NULL AND deprel!=''").fetchone()[0]

    # nominative function (deprel-subset)
    nsubj_total = cur.execute("SELECT COUNT(*) FROM token WHERE deprel='nsubj'").fetchone()[0]
    nsubj_nom = cur.execute("SELECT COUNT(*) FROM token WHERE deprel='nsubj' AND feat_case='Nom'").fetchone()[0]
    nsubj_by_case = {k: c for k, c in cur.execute(
        "SELECT feat_case, COUNT(*) FROM token WHERE deprel='nsubj' GROUP BY feat_case ORDER BY COUNT(*) DESC")}
    # predicate nominative: a Nom token that is the HEAD of a cop child
    pred_nom = cur.execute(
        "SELECT COUNT(*) FROM token h JOIN token c ON c.sentence_id=h.sentence_id AND c.head=h.idx "
        "WHERE h.feat_case='Nom' AND c.deprel='cop'").fetchone()[0]

    # accusative function (deprel-subset)
    obj_total = cur.execute("SELECT COUNT(*) FROM token WHERE deprel='obj'").fetchone()[0]
    obj_acc = cur.execute("SELECT COUNT(*) FROM token WHERE deprel='obj' AND feat_case='Acc'").fetchone()[0]
    def acc_deprel(d):
        return cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Acc' AND deprel=?", (d,)).fetchone()[0]
    obl_goal = acc_deprel("obl:goal"); obl_temp = acc_deprel("obl:temp"); obl_path = acc_deprel("obl:path")
    iobj_acc = acc_deprel("iobj")

    # DOUBLE ACCUSATIVE — efficient aggregation, corrected to genuine core-object dvikarmaka.
    # naive: verb heads with >=2 Acc dependents of ANY deprel
    ph = ",".join("?" for _ in CORE_OBJ)
    naive = cur.execute(
        "SELECT COUNT(*) FROM (SELECT c.sentence_id, c.head FROM token c JOIN token h "
        "ON h.sentence_id=c.sentence_id AND h.idx=c.head "
        "WHERE c.feat_case='Acc' AND h.upos='VERB' GROUP BY c.sentence_id, c.head HAVING COUNT(*)>=2)").fetchone()[0]
    # corrected: verb heads with >=2 Acc CORE-OBJECT dependents
    dvikarmaka = cur.execute(
        f"SELECT COUNT(*) FROM (SELECT c.sentence_id, c.head FROM token c JOIN token h "
        f"ON h.sentence_id=c.sentence_id AND h.idx=c.head "
        f"WHERE c.feat_case='Acc' AND c.deprel IN ({ph}) AND h.upos='VERB' "
        f"GROUP BY c.sentence_id, c.head HAVING COUNT(*)>=2)", CORE_OBJ).fetchone()[0]
    # strictest: two true `obj`
    two_obj = cur.execute(
        "SELECT COUNT(*) FROM (SELECT c.sentence_id, c.head FROM token c JOIN token h "
        "ON h.sentence_id=c.sentence_id AND h.idx=c.head "
        "WHERE c.feat_case='Acc' AND c.deprel='obj' AND h.upos='VERB' "
        "GROUP BY c.sentence_id, c.head HAVING COUNT(*)>=2)").fetchone()[0]

    # seeded sample of Nom+Acc
    ids = [r[0] for r in cur.execute("SELECT id FROM token WHERE feat_case IN ('Nom','Acc')")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT t.id, t.m_unsandhied, t.lemma, t.feat_case, t.deprel, x.name, c.ref FROM token t "
            "JOIN sentence se ON se.id=t.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "case", "deprel", "text", "chapter_ref"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "Sangram SG-SE-002 (Номинатив и аккузатив) — two largest cases; native totals + deprel-subset function split",
        "toc_ref": "SG-SE-002",
        "kind": "beyond-quota core ① (opening set already 19/19); native positive; workflow-probed + adversarially verified",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "case_bearing_tokens": case_bearing, "deprel_parsed_tokens": deprel_tokens,
                         "deprel_parsed_pct": round(100 * deprel_tokens / total, 2)},
        "totals_native": {
            "nom": nom, "acc": acc, "cpd_pseudo_case": cpd,
            "nom_pct_of_corpus": round(100 * nom / total, 2), "acc_pct_of_corpus": round(100 * acc / total, 2),
            "nom_pct_of_case_bearing": round(100 * nom / case_bearing, 2), "acc_pct_of_case_bearing": round(100 * acc / case_bearing, 2),
            "note": "Nom and Acc are the two largest of the eight vibhakti; feat_case='Cpd' (%d, compound-member placeholder, not a case) is LARGER than Acc and is excluded from the 'largest case' claim" % cpd,
        },
        "nominative_function_deprel_subset": {
            "nsubj_total": nsubj_total, "nsubj_nom": nsubj_nom, "nsubj_pct_nom": round(100 * nsubj_nom / nsubj_total, 1),
            "nsubj_by_case": nsubj_by_case,
            "predicate_nominative": pred_nom,
            "note": "subject↔Nom near-canonical on the parsed subset; non-Nom nsubj include Loc (the locative-absolute subject, SG-SE-005) and Gen",
        },
        "accusative_function_deprel_subset": {
            "obj_total": obj_total, "obj_acc": obj_acc, "obj_pct_acc": round(100 * obj_acc / obj_total, 1),
            "beyond_object": {"obl_goal_acc": obl_goal, "obl_temp_acc": obl_temp, "obl_path_acc": obl_path, "iobj_acc": iobj_acc},
            "note": "the accusative reaches beyond the direct object: goal of motion (obl:goal), duration/time (obl:temp), path (obl:path) — all natively tagged; obj is ~90% Acc (rest Cpd/Gen)",
        },
        "double_accusative_CORRECTED": {
            "naive_any_Acc_pair": naive,
            "genuine_dvikarmaka_core_object": dvikarmaka,
            "two_true_obj": two_obj,
            "note": "the classical double-OBJECT (dvikarmaka) is ~%d verb heads (>=2 Acc in core-object roles obj/iobj/xcomp/ccomp), "
                    "NOT the naive %d (which mixes object + adverbial/directional/temporal/coordinated Acc). The adversarial "
                    "verify caught this ~3x over-count; %d heads have two true `obj` deps (e.g. yāc 'ask X for Y')." % (dvikarmaka, naive, two_obj),
        },
        "traditional_layer": {"witness": "Whitney 1889 §§267-281 (nominative, accusative uses; accusative of goal/duration; double accusative); "
                                          "Pāṇini 1.4.49 (karman), 1.4.51 (dvikarmaka), 2.3.2 (Acc)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "function_subset_only": "deprel covers only ~3.93%% of tokens; ALL function splits (nsubj/obj/obl/iobj/predicate-nom/double-acc) are on that subset and must not be generalised to the whole case",
            "obj_not_acc": "'direct object' (obj) and 'accusative' (feat_case) are distinct layers: ~10%% of obj are Cpd/Gen, not Acc",
            "double_acc_definition_sensitive": "the double accusative depends on the deprel filter; the genuine dvikarmaka is ~%d, not the naive %d" % (dvikarmaka, naive),
            "cpd_larger_than_acc": "feat_case='Cpd' (%d) outranks Acc; 'two largest cases' excludes the compound-member placeholder" % cpd,
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Nom {nom:,} ({round(100*nom/case_bearing,1)}% of case-bearing) / Acc {acc:,} ({round(100*acc/case_bearing,1)}%); Cpd {cpd:,} (>Acc)", file=sys.stderr)
    print(f"nsubj {nsubj_total:,} ({round(100*nsubj_nom/nsubj_total,1)}% Nom); pred-nom {pred_nom}; obj {obj_total:,} ({round(100*obj_acc/obj_total,1)}% Acc)", file=sys.stderr)
    print(f"Acc beyond obj: goal {obl_goal}, duration {obl_temp}, path {obl_path}, iobj {iobj_acc}", file=sys.stderr)
    print(f"double-acc: genuine dvikarmaka {dvikarmaka} (two-obj {two_obj}) vs naive {naive}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
