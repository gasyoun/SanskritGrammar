#!/usr/bin/env python3
"""SG-SE-001 «Система падежных значений: обзор» — beyond-quota native positive (case overview).

Beyond-quota core article (opening set already 19/19). The cluster-representative OVERVIEW
of the case-semantics domain. Case is NATIVELY marked on every nominal via `feat_case`, so
the whole case system is directly countable:

  Nom 1,419,146 · Acc 742,293 · Ins 277,143 · Gen 270,763 · Loc 243,215 · Voc 81,088 ·
  Abl 74,565 · Dat 65,423 — eight vibhakti. PLUS a pseudo-case `Cpd` 841,052 = compound-
  internal members (no overt case; NOT one of the eight) — the honesty caveat.

This overview gives the native frequency spine + the traditional functional range of each
case (Whitney), and maps to the sub-articles (SE-002 Nom/Acc, SE-003 Ins/Dat, SE-004
Abl/Gen, SE-005 Loc, SE-013 kāraka-vs-case). It does NOT re-derive kāraka roles — that
mapping (agent/patient/instrument ↔ case) is SE-013's endgame; here case = the morphological
vibhakti, natively counted.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/case-system-overview/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "case-system-overview" / "data"

# the eight vibhakti (traditional order 1..8) + Russian gloss of the primary function
CASES = [
    ("Nom", "именительный (kartṛ / подлежащее)"),
    ("Acc", "винительный (karman / прямой объект, цель)"),
    ("Ins", "творительный (karaṇa / орудие, агент пассива, совместность)"),
    ("Dat", "дательный (sampradāna / адресат, цель)"),
    ("Abl", "отложительный (apādāna / источник, сравнение, причина)"),
    ("Gen", "родительный (относит. / принадлежность)"),
    ("Loc", "местный (adhikaraṇa / место, время, локатив абсолютный)"),
    ("Voc", "звательный (обращение)"),
]
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
    all_case = {c: n for c, n in cur.execute(
        "SELECT feat_case, COUNT(*) FROM token WHERE feat_case IS NOT NULL GROUP BY feat_case ORDER BY COUNT(*) DESC")}
    cpd = all_case.get("Cpd", 0)
    real_cases = {k: all_case.get(k, 0) for k, _ in CASES}
    real_total = sum(real_cases.values())

    # by number for each real case (dual is a Sanskrit feature)
    case_number = {}
    for k, _ in CASES:
        case_number[k] = {nn: c for nn, c in cur.execute(
            "SELECT feat_number, COUNT(*) FROM token WHERE feat_case=? GROUP BY feat_number ORDER BY COUNT(*) DESC", (k,))}

    # seeded sample across the 8 real cases
    ids = [r[0] for r in cur.execute(
        "SELECT id FROM token WHERE feat_case IN ('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc')")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT t.id, t.m_unsandhied, t.lemma, t.feat_case, t.feat_number, x.name, c.ref, se.sent_counter FROM token t "
            "JOIN sentence se ON se.id=t.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "case", "number", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "Sangram SG-SE-001 (Система падежных значений: обзор) — case system, native",
        "toc_ref": "SG-SE-001",
        "kind": "beyond-quota core ① (opening set already 19/19); cluster-representative overview; native positive (feat_case)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "all_case_marked": sum(all_case.values())},
        "case_system_native": {
            "eight_vibhakti": [{"case": k, "function_ru": ru, "tokens": real_cases[k],
                                "by_number": case_number[k]} for k, ru in CASES],
            "real_case_total": real_total,
            "compound_pseudo_case_Cpd": cpd,
            "cpd_note": "feat_case='Cpd' (841,052) marks a COMPOUND-INTERNAL member — no overt case ending, "
                        "NOT one of the eight vibhakti; excluded from the case-function counts",
            "note": "case is native on every nominal (feat_case); this overview counts the morphological "
                    "vibhakti — the kāraka mapping (agent/patient ↔ case) is SE-013's endgame, not re-derived here",
        },
        "traditional_layer": {"witness": "Whitney 1889 §§267-305 (case uses); Pāṇini 2.3 (vibhakti) + 1.4.23-55 (kāraka)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "cpd_pseudo_case": "Cpd is not a real case (compound member); the eight vibhakti exclude it",
            "case_not_function": "feat_case is the morphological vibhakti; the FUNCTION (kāraka role, adverbial use) "
                                 "is the traditional layer + SE-013, not a native tag — one case covers many functions",
            "syncretism": "some endings are syncretic (a-stem Abl=Gen sg -asya vs -āt distinct, but Nom/Acc du/pl overlap); counts are by DCS analysis, not by surface",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"case-marked tokens: {sum(all_case.values()):,}", file=sys.stderr)
    for k, ru in CASES:
        print(f"  {k}: {real_cases[k]:,}", file=sys.stderr)
    print(f"real vibhakti total: {real_total:,}; Cpd pseudo-case (excluded): {cpd:,}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
