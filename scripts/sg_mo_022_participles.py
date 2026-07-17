#!/usr/bin/env python3
"""SG-MO-022 «Причастия презенса и перфекта» — beyond-quota (native positive + honest caveat).

Beyond-quota core article (opening set already 19/19; charter quota 15-25 ①). The
NON-FINITE participle system is largely native in DCS via `feat_verbform='Part'` +
`feat_tense`. This slot covers the two natively-marked classes the ta-na PPP article
(SG-MO-023) and the future-participle note (SG-MO-021) did NOT:

  PRESENT participle  = Part + Tense=Pres  — the clean positive (~64k):
      Voice=Pass  = passive present participle (-yamāna, kriyamāṇa "being done")
      Voice=None  = active + middle (-ant / -māna) — NOT natively split (EM caveat)
  PERFECT (reduplicated active) participle = the -vas form (vidvān "learned",
      cakṛvān "having done") — natively present but NOT cleanly bucketed: it rides
      under Tense=Past, whose Part bucket (~9k) also carries ta-na past forms
      (EM2-adjacent). A surface -vas filter isolates the perfect participle proper
      (led by vid); the count is a partial/recoverable lower bound.

(The ta-na PPP Tense=None Part = SG-MO-023, done; the future participle Tense=Fut =
noted at SG-MO-021. This article is the present + perfect complement.)

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/present-perfect-participles/data/.
"""
import argparse
import csv
import hashlib
import json
import random
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "present-perfect-participles" / "data"

# perfect active participle (-vas/-vaṃs) surface morphology across cases
VAS = re.compile(r"(vān|vāṃsam|vāṃs|vas|uṣ|uṣā|uṣe|uṣo|uṣā|vadbhi|vatsu|uṣām|vāṃ)$")
SEED = 20260717
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
    all_part = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform='Part'").fetchone()[0]

    # --- present participle (clean native positive) ---
    pres = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense='Pres'").fetchone()[0]
    pres_voice = {v: n for v, n in cur.execute(
        "SELECT feat_voice, COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense='Pres' "
        "GROUP BY feat_voice ORDER BY COUNT(*) DESC")}
    pres_top = cur.execute(
        "SELECT lemma, COUNT(*) c FROM token WHERE feat_verbform='Part' AND feat_tense='Pres' "
        "GROUP BY lemma ORDER BY c DESC LIMIT 10").fetchall()

    # --- perfect (reduplicated active) participle: partial, EM2-adjacent ---
    past_part_rows = cur.execute(
        "SELECT m_unsandhied, lemma FROM token WHERE feat_verbform='Part' AND feat_tense='Past'").fetchall()
    past_part_n = len(past_part_rows)
    vas_n = sum(1 for m, _ in past_part_rows if m and VAS.search(m))
    perf_top = cur.execute(
        "SELECT lemma, COUNT(*) c FROM token WHERE feat_verbform='Part' AND feat_tense='Past' "
        "GROUP BY lemma ORDER BY c DESC LIMIT 8").fetchall()

    # future participle (cross-ref only; owned by SG-MO-021)
    fut = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense='Fut'").fetchone()[0]
    tna = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense IS NULL").fetchone()[0]

    # seeded validation sample of present participles
    ids = [r[0] for r in cur.execute(
        "SELECT id FROM token WHERE feat_verbform='Part' AND feat_tense IN ('Pres','Past')")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT s.id, s.m_unsandhied, s.lemma, s.feat_tense, s.feat_voice, x.name, c.ref, se.sent_counter "
            "FROM token s JOIN sentence se ON se.id=s.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE s.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "tense", "voice", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "Sangram SG-MO-022 (Причастия презенса и перфекта) — non-finite, native + honest caveat",
        "toc_ref": "SG-MO-022",
        "kind": "beyond-quota core ① (opening set already 19/19); positive (present) + partial/EM2 (perfect)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "all_participles_verbform_part": all_part},
        "present_participle_native_positive": {
            "total": pres, "by_voice": pres_voice,
            "voice_note": "Voice=Pass = passive present participle (-yamāna); Voice=None = active+middle "
                          "(-ant/-māna) NOT natively split — the active/middle distinction is invisible (EM)",
            "top_lemmas": [f"{l} ({c})" for l, c in pres_top],
        },
        "perfect_active_participle_partial_EM2": {
            "past_tense_part_bucket": past_part_n,
            "vas_morphology_estimate": vas_n,
            "vas_pct_of_bucket": round(100 * vas_n / past_part_n, 1) if past_part_n else 0,
            "note": "the reduplicated perfect active participle (-vas, vidvān) rides under Tense=Past, whose "
                    "Part bucket also carries ta-na past forms (EM2-adjacent). The -vas surface filter is a "
                    "partial/recoverable lower bound; led by vid (vidvān 'learned').",
            "top_lemmas_in_bucket": [f"{l} ({c})" for l, c in perf_top],
        },
        "cross_reference": {
            "ta_na_ppp_tense_none": tna, "future_participle_tense_fut": fut,
            "note": "ta-na PPP (Tense=None) = SG-MO-023; future participle (Tense=Fut) = noted at SG-MO-021",
        },
        "traditional_layer": {"witness": "Whitney 1889 §§584–597 (present participle), §§802–806 (perfect participle)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "present_active_middle_not_split": "Voice=None conflates active (-ant) and middle (-māna); only passive is tagged",
            "perfect_EM2": "perfect active participle not cleanly bucketed (Tense=Past mixes ta-na past forms); -vas count is a lower bound",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"present participle: {pres:,} (Pass {pres_voice.get('Pass',0):,} / None {pres_voice.get(None,0):,})", file=sys.stderr)
    print(f"perfect active ptcp (-vas): ~{vas_n:,} of {past_part_n:,} Tense=Past Part ({round(100*vas_n/past_part_n,1)}%)", file=sys.stderr)
    print(f"cross-ref: ta-na PPP {tna:,} (SG-MO-023), future ptcp {fut:,} (SG-MO-021)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
