#!/usr/bin/env python3
"""SG-MO-016 «Презентные основы: имперфект» — the imperfect (past narrative).

Core W2 ① article (content, no kill-gate). The imperfect (augment a- + present
stem + secondary endings: abhavat, akarot, abravīt) is the **recoverable
preterite** — the ONE past tense DCS tags distinctly (`Tense=Impf`), unlike the
aorist and perfect which are conflated under `Tense=Past` (evidence-limit EM2,
proven by pilot P3). So this article is the positive counterpart to P3: what the
corpus DOES let you measure about the past.

It carries two borders honestly:
  EM2 — its sibling preterites (aorist/perfect) are conflated under Past; the
    imperfect is the exception, tagged and measurable.
  EM1 — the imperfect is built on the PRESENT stem, so its formation depends on
    the present class (gaṇa), which is not in DCS features (P2); the corpus
    attests the surface imperfect, not the class that shapes its stem.

Three layers (C5 §3): ATTESTED — the imperfect's distribution (person/number/
voice) over the pinned snapshot; GENERATED/TRADITIONAL — augment + present stem +
secondary endings (Whitney §§ 585–600, ch. VIII).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators; seeded sample. Read-only. Emits into sangram/articles/imperfect/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "imperfect" / "data"

FIN = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
       "AND feat_person IS NOT NULL")
IMPF = f"{FIN} AND feat_tense='Impf'"

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
        out[v if v is not None else "Act(∅)"] = {"tokens": c, "share": round(c / total, 4)}
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

    # preterite context: how the past splits (EM2 story)
    fin_total = cur.execute(f"SELECT COUNT(*) FROM token WHERE {FIN}").fetchone()[0]
    tense = dist(cur, "feat_tense", FIN, fin_total)

    total = cur.execute(f"SELECT COUNT(*) FROM token WHERE {IMPF}").fetchone()[0]
    person = dist(cur, "feat_person", IMPF, total)
    number = dist(cur, "feat_number", IMPF, total)
    voice = dist(cur, "feat_voice", IMPF, total)
    third = person.get("3", {}).get("tokens", 0)

    top = cur.execute(
        f"SELECT lemma, COUNT(*) c FROM token WHERE {IMPF} AND lemma IS NOT NULL "
        f"GROUP BY lemma ORDER BY c DESC LIMIT 15").fetchall()

    ids = [r[0] for r in cur.execute(f"SELECT id FROM token WHERE {IMPF}")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        sample.append(cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.feat_person, t.feat_number, "
            "t.feat_voice, x.name, c.ref, s.sent_counter FROM token t "
            "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone())
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "person", "number",
                    "voice", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "SG-MO-016 «Имперфект» — past narrative tense (core W2 ①, content)",
        "toc_ref": "SG-MO-016",
        "kind": "content article (no kill-gate)",
        "method": "finite verbs with Tense=Impf — the ONE distinctly-tagged preterite (vs aorist/perfect conflated under Past, EM2); distribution over person/number/voice",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "preterite_context": {
            "finite_verb_total": fin_total, "tense_dist": tense,
            "note": "Past (aorist+perfect conflated, EM2) vs Impf (tagged, recoverable) vs Plp/Pqp (tiny)",
        },
        "denominator_imperfect_tokens": total,
        "person": person, "number": number, "voice": voice,
        "third_person_share_ci95": {"k": third, "n": total, "ci95": wilson_ci(third, total)},
        "top_lemmas": [{"lemma": l, "tokens": c} for l, c in top],
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "EM2_border_resolved": "the imperfect is the exception to EM2 — tagged Impf, so measurable, unlike the Past-conflated aorist/perfect (P3)",
            "EM1_stem_class": "the imperfect is built on the present stem, so its formation depends on the present class (gaṇa), not in DCS features (P2); the corpus attests the surface imperfect, not the class",
            "augment_not_tagged": "the augment a- is not a separate feature; identified via the Impf tag, not by surface a-",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"finite total: {fin_total:,}; imperfect: {total:,}", file=sys.stderr)
    print(f"person: {[(k, v['share']) for k, v in person.items()]}", file=sys.stderr)
    print(f"number: {[(k, v['share']) for k, v in number.items()]}", file=sys.stderr)
    print(f"top: {[(x['lemma'], x['tokens']) for x in summary['top_lemmas'][:8]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
