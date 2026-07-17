#!/usr/bin/env python3
"""SG-MO-018 «Аорист» — the aorist, partially recoverable within Tense=Past.

Core W2 ① article (content, no kill-gate). The aorist is a preterite conflated
with the perfect under `Tense=Past` (evidence-limit EM2, pilot P3). It fills the
MIDDLE of the preterite-recoverability gradient:
  imperfect (SG-MO-016) — fully tagged (Tense=Impf), recoverable;
  AORIST (this slot) — PARTIALLY recoverable: `feat_formation` marks aorist
    stem-types (root/s/is/sa/sis/red + thematic) on a subset of Past tokens;
  perfect (P3) — unmarked, unrecoverable (recall 3.3%).

The feat_formation-marked aorist is a LOWER BOUND: P3 measured the perfect at
~76% of a Past sample, so the true aorist is ~24%; the marked ~12k is roughly
half — the unmarked aorists sit indistinguishably in the Tense=Past/None bulk
with the perfect. (Note the known adjacency: 'them' Past ≈ thematic aorist vs
imperfect; 'red' Past ≈ reduplicated aorist vs reduplicated-present imperfect,
e.g. adadat — P3's false friend.)

Three layers (C5 §3): ATTESTED — the Past split + aorist-formation breakdown over
the pinned snapshot; TRADITIONAL — the seven aorist formations (Whitney §§824–930).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators; seeded sample. Read-only. Emits into sangram/articles/aorist/data/.
"""
import argparse
import csv
import hashlib
import json
import math
import random
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "aorist" / "data"

FIN = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
       "AND feat_person IS NOT NULL")
PAST = f"{FIN} AND feat_tense='Past'"
# aorist stem-formation types (within Tense=Past): root/s/is/sa/sis/red aorists + thematic (a-)aorist
AORIST_FORMATIONS = ("root", "s", "is", "sa", "sis", "red", "them")

SEED = 20260717
SAMPLE_SIZE = 50


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def wilson_ci(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
    return (round(centre - half, 4), round(centre + half, 4))


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

    fin_total = cur.execute(f"SELECT COUNT(*) FROM token WHERE {FIN}").fetchone()[0]
    past_total = cur.execute(f"SELECT COUNT(*) FROM token WHERE {PAST}").fetchone()[0]

    formation = {}
    for v, c in cur.execute(
            f"SELECT feat_formation, COUNT(*) FROM token WHERE {PAST} "
            f"GROUP BY feat_formation ORDER BY COUNT(*) DESC"):
        formation[v if v is not None else "None(unmarked)"] = c

    ph = ",".join("?" for _ in AORIST_FORMATIONS)
    aor_total = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {PAST} AND feat_formation IN ({ph})",
        AORIST_FORMATIONS).fetchone()[0]
    aor_by_type = {t: cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {PAST} AND feat_formation=?", (t,)).fetchone()[0]
        for t in AORIST_FORMATIONS}
    peri = formation.get("peri", 0)
    unmarked = formation.get("None(unmarked)", 0)

    top = cur.execute(
        f"SELECT lemma, COUNT(*) c FROM token WHERE {PAST} AND feat_formation IN ({ph}) "
        f"AND lemma IS NOT NULL GROUP BY lemma ORDER BY c DESC LIMIT 15", AORIST_FORMATIONS
    ).fetchall()

    ids = [r[0] for r in cur.execute(
        f"SELECT id FROM token WHERE {PAST} AND feat_formation IN ({ph})", AORIST_FORMATIONS)]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        sample.append(cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.feat_formation, t.feat_person, "
            "t.feat_number, x.name, c.ref, s.sent_counter FROM token t "
            "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone())
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "formation", "person",
                    "number", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "SG-MO-018 «Аорист» — partially-recoverable preterite (core W2 ①, content)",
        "toc_ref": "SG-MO-018",
        "kind": "content article (no kill-gate)",
        "method": "within Tense=Past (aorist+perfect conflated, EM2), feat_formation marks aorist stem-types (root/s/is/sa/sis/red/them) — a LOWER BOUND on the aorist; the unmarked bulk is inseparable from the perfect (P3)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "preterite_recoverability_gradient": {
            "imperfect_SG_MO_016": "fully tagged (Tense=Impf), recoverable",
            "aorist_this_slot": "partially recoverable via feat_formation (lower bound)",
            "perfect_P3": "unmarked, unrecoverable (recall 3.3%)",
        },
        "denominators": {"finite_total": fin_total, "past_total": past_total},
        "past_formation_breakdown": formation,
        "aorist_lower_bound": {
            "aorist_formation_marked": aor_total,
            "share_of_past": round(100 * aor_total / past_total, 1),
            "share_of_past_ci95": wilson_ci(aor_total, past_total),
            "by_type": aor_by_type,
            "note": "LOWER BOUND — P3 estimated perfect ~76% of Past → aorist ~24%; the marked ~12k is roughly half, the rest sits unmarked with the perfect",
        },
        "perfect_ish_remainder": {"unmarked_none": unmarked, "periphrastic_peri": peri,
                                  "note": "None (unmarked, mostly reduplicated perfect + hidden aorists) + peri (periphrastic perfect)"},
        "top_aorist_lemmas": [{"lemma": l, "tokens": c} for l, c in top],
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "EM2": "aorist conflated with perfect under Tense=Past; only feat_formation-marked aorists are separable — a lower bound",
            "them_red_adjacency": "'them' Past ≈ thematic aorist vs imperfect; 'red' Past ≈ reduplicated aorist vs reduplicated-present imperfect (adadat, P3's false friend) — the marker is trusted but these classes are morphologically adjacent",
            "augment": "augment a- not a separate feature; aorist type read from feat_formation, not surface",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lb = summary["aorist_lower_bound"]
    print(f"finite {fin_total:,}; Past {past_total:,}", file=sys.stderr)
    print(f"aorist-marked (lower bound): {aor_total:,} ({lb['share_of_past']}% of Past); by type: {aor_by_type}", file=sys.stderr)
    print(f"perfect-ish remainder: None {unmarked:,} + peri {peri:,}", file=sys.stderr)
    print(f"top: {[(x['lemma'], x['tokens']) for x in summary['top_aorist_lemmas'][:8]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
