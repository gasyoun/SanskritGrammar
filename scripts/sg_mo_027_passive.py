#!/usr/bin/env python3
"""SG-MO-027 «Вторичные спряжения: пассив» — the passive.

Core W2 ① article (content, no kill-gate). The passive (secondary conjugation:
weak root + -ya- + middle endings; ucyate "is said", dṛśyate "is seen") is
NATIVELY tagged in DCS (`Voice=Pass`), so — like the imperfect (SG-MO-016) — it
is directly measurable. It carries the EM1 border: the passive -ya- stem is
formally identical to the class-IV (divādi) present -ya- (paśyati, naśyati), and
DCS separates them by the voice tag, not by the stem shape (P2's class problem).

Three layers (C5 §3): ATTESTED — the passive's distribution (person/tense) over
the pinned snapshot; TRADITIONAL — weak root + -ya- + middle endings
(Whitney §§768–774); GENERATED — the -ya- passive stem by a conjugator.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators + Wilson CI on a headline share; seeded sample. Read-only. Emits into
sangram/articles/passive/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "passive" / "data"

FIN = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
       "AND feat_person IS NOT NULL")
FINPASS = f"{FIN} AND feat_voice='Pass'"

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


def dist(cur, col, where, total):
    out = {}
    for v, c in cur.execute(
            f"SELECT {col}, COUNT(*) FROM token WHERE {where} GROUP BY {col} ORDER BY COUNT(*) DESC"):
        out[v if v is not None else "∅"] = {"tokens": c, "share": round(c / total, 4)}
    return out


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
    fin_pass = cur.execute(f"SELECT COUNT(*) FROM token WHERE {FINPASS}").fetchone()[0]
    part_pass = cur.execute(
        "SELECT COUNT(*) FROM token WHERE upos='VERB' AND feat_verbform='Part' "
        "AND feat_voice='Pass'").fetchone()[0]

    person = dist(cur, "feat_person", FINPASS, fin_pass)
    number = dist(cur, "feat_number", FINPASS, fin_pass)
    tense = dist(cur, "feat_tense", FINPASS, fin_pass)
    third = person.get("3", {}).get("tokens", 0)
    pres = tense.get("Pres", {}).get("tokens", 0)

    top = cur.execute(
        f"SELECT lemma, COUNT(*) c FROM token WHERE {FINPASS} AND lemma IS NOT NULL "
        f"GROUP BY lemma ORDER BY c DESC LIMIT 15").fetchall()

    ids = [r[0] for r in cur.execute(f"SELECT id FROM token WHERE {FINPASS}")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        sample.append(cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.feat_person, t.feat_number, "
            "t.feat_tense, x.name, c.ref, s.sent_counter FROM token t "
            "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone())
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "person", "number",
                    "tense", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "SG-MO-027 «Пассив» — passive secondary conjugation (core W2 ①, content)",
        "toc_ref": "SG-MO-027",
        "kind": "content article (no kill-gate)",
        "method": "finite verbs with Voice=Pass — natively tagged (like the imperfect); distribution over person/tense; the -ya- stem overlaps class-IV present (EM1), separated by the voice tag not the stem",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {
            "finite_total": fin_total, "finite_passive": fin_pass,
            "finite_passive_share": round(fin_pass / fin_total, 4),
            "participial_passive": part_pass,
        },
        "person": person, "number": number, "tense": tense,
        "third_person_share_ci95": {"k": third, "n": fin_pass, "ci95": wilson_ci(third, fin_pass)},
        "present_share_ci95": {"k": pres, "n": fin_pass, "ci95": wilson_ci(pres, fin_pass)},
        "top_lemmas": [{"lemma": l, "tokens": c} for l, c in top],
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "EM1_ya_overlap": "the passive -ya- stem is formally identical to the class-IV (divādi) present -ya- (paśyati vs dṛśyate); DCS separates them by Voice=Pass, not the stem shape (P2's class problem)",
            "middle_vs_passive": "the passive uses middle (Ātmanepada) endings; DCS tags Voice=Pass explicitly, but morphologically passive ≈ middle in form outside the -ya- stem",
            "participial": "passive participles (VerbForm=Part, Voice=Pass) are counted separately from the finite passive",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"finite {fin_total:,}; finite passive {fin_pass:,} ({100*fin_pass/fin_total:.1f}%); participial passive {part_pass:,}", file=sys.stderr)
    print(f"person: {[(k, v['share']) for k, v in person.items()]}", file=sys.stderr)
    print(f"tense: {[(k, v['share']) for k, v in tense.items()]}", file=sys.stderr)
    print(f"top: {[(x['lemma'], x['tokens']) for x in summary['top_lemmas'][:8]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
