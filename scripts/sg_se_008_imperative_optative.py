#!/usr/bin/env python3
"""SG-SE-008 «Наклонения: императив и оптатив» — beyond-quota native positive (semantics from morphology).

Beyond-quota core article (opening set already 19/19). The two main non-indicative moods
are NATIVELY marked via `feat_mood` — imperative (Imp) and optative (Opt) — and their
person distributions recover a genuine SEMANTIC contrast directly from the corpus:

  IMPERATIVE  (Imp)  56,506 — skews 2nd person (command to the hearer): śṛṇu "listen!",
                     kuru "do!". Significant 3rd person = the jussive-like "let him …".
  OPTATIVE    (Opt)  91,912 — overwhelmingly 3rd-person singular (94.6% / 92.8%): the
                     impersonal PRESCRIPTION / POTENTIAL — kuryāt "one should do", syāt
                     "would/could be". This is the śāstric rule-giving register.

So the functional divergence (direct command vs general prescription/potential) is not a
claim imposed on the data — it is visible in the person profile, natively. This is the
domain-SE angle: the semantics read off native morphology (feat_mood + feat_person),
no C6 syntax needed.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/imperative-optative/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "imperative-optative" / "data"

SEED = 20260717
SAMPLE_SIZE = 50


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def profile(cur, mood):
    n = cur.execute("SELECT COUNT(*) FROM token WHERE feat_mood=?", (mood,)).fetchone()[0]
    by_person = {p: c for p, c in cur.execute(
        "SELECT feat_person, COUNT(*) FROM token WHERE feat_mood=? GROUP BY feat_person ORDER BY COUNT(*) DESC", (mood,))}
    by_number = {p: c for p, c in cur.execute(
        "SELECT feat_number, COUNT(*) FROM token WHERE feat_mood=? GROUP BY feat_number ORDER BY COUNT(*) DESC", (mood,))}
    by_voice = {p: c for p, c in cur.execute(
        "SELECT feat_voice, COUNT(*) FROM token WHERE feat_mood=? GROUP BY feat_voice ORDER BY COUNT(*) DESC", (mood,))}
    top = cur.execute(
        "SELECT lemma, COUNT(*) c FROM token WHERE feat_mood=? GROUP BY lemma ORDER BY c DESC LIMIT 8", (mood,)).fetchall()
    return {"total": n, "by_person": by_person, "by_number": by_number, "by_voice": by_voice,
            "top_lemmas": [f"{l} ({c})" for l, c in top]}


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
    all_mood = {m: c for m, c in cur.execute(
        "SELECT feat_mood, COUNT(*) FROM token WHERE feat_mood IS NOT NULL GROUP BY feat_mood ORDER BY COUNT(*) DESC")}

    imp = profile(cur, "Imp")
    opt = profile(cur, "Opt")

    ids = [r[0] for r in cur.execute("SELECT id FROM token WHERE feat_mood IN ('Imp','Opt')")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT s.id, s.m_unsandhied, s.lemma, s.feat_mood, s.feat_person, s.feat_number, x.name, c.ref, se.sent_counter "
            "FROM token s JOIN sentence se ON se.id=s.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE s.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "mood", "person", "number", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    def pct(d, k):
        s = sum(d.values())
        return round(100 * d.get(k, 0) / s, 1) if s else 0

    summary = {
        "study": "Sangram SG-SE-008 (Наклонения: императив и оптатив) — semantics read off native morphology",
        "toc_ref": "SG-SE-008",
        "kind": "beyond-quota core ① (opening set already 19/19); native positive (feat_mood); semantic contrast from person profile",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "all_moods": all_mood},
        "imperative": imp,
        "optative": opt,
        "semantic_contrast": {
            "imperative_2nd_person_pct": pct(imp["by_person"], "2"),
            "imperative_3rd_person_pct": pct(imp["by_person"], "3"),
            "optative_3rd_person_pct": pct(opt["by_person"], "3"),
            "optative_3sg_pct": round(100 * (opt["by_number"].get("Sing", 0)) / opt["total"], 1),
            "finding": "imperative skews 2nd person (direct command to the hearer); optative is overwhelmingly "
                       "3rd-person singular (impersonal prescription/potential — 'one should', 'it would be'), "
                       "the śāstric rule-giving register. The functional divergence is native (feat_mood+feat_person), "
                       "not a claim imposed on the data.",
        },
        "traditional_layer": {"witness": "Whitney 1889 §§569-582 (imperative), §§563-568 (optative/potential); "
                                          "the optative as prescription — classical śāstra usage"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "mood_native_not_function": "feat_mood is native and clean; the FUNCTION (command vs wish vs prescription) "
                                        "is inferred from the person/number profile + traditional grammar, not a semantic tag",
            "injunctive_subjunctive_separate": "other non-indicative moods (Jus 5,258, Sub 4,325, Prec 577, Cond 340) are "
                                               "their own slots; this article covers only Imp + Opt",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"imperative (Imp): {imp['total']:,} — person {imp['by_person']}", file=sys.stderr)
    print(f"optative (Opt): {opt['total']:,} — person {opt['by_person']}", file=sys.stderr)
    print(f"contrast: Imp 2nd={pct(imp['by_person'],'2')}% vs Opt 3rd={pct(opt['by_person'],'3')}%", file=sys.stderr)
    print(f"all moods: {all_mood}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
