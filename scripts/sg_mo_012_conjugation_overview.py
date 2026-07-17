#!/usr/bin/env python3
"""SG-MO-012 (Спряжение: обзор) — finite-verb category frequency frame.

Descriptive corpus frame for the conjugation domain (overview, no kill-gate):
the distribution of finite verb tokens across the five NATIVE morphological
categories DCS annotates directly — person × number × tense × mood × voice.
Unlike the declension stem-inventory (which needed an attested-ending trick),
these categories are stored in DCS `feat_*`, so the frame is the real attested
distribution with no approximation.

Every published number carries the pinned-snapshot provenance + denominator; a
few headline shares carry a Wilson 95% CI (C3 §4.4 / П1–П2). Read-only.
"""
import sqlite3
import sys
import json
import hashlib
import argparse
import math
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "conjugation-overview" / "data"

WHERE = ("t.upos='VERB' AND (t.feat_verbform='Fin' OR t.feat_verbform IS NULL) "
         "AND t.feat_person IS NOT NULL")


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


def dist(cur, col, total):
    out = {}
    for v, c in cur.execute(
        f"SELECT {col}, COUNT(*) FROM token t WHERE {WHERE} GROUP BY {col} ORDER BY COUNT(*) DESC"
    ):
        out[v if v is not None else "Act(∅)"] = {"tokens": c, "share": round(c / total, 4)}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--skip-checksum", action="store_true")
    args = ap.parse_args()
    db = Path(args.db)
    if not db.exists():
        print(f"ERROR: DB not found: {db}", file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr)
        return 1
    sha = "skipped" if args.skip_checksum else sha256_file(db)

    total = cur.execute(f"SELECT COUNT(*) FROM token t WHERE {WHERE}").fetchone()[0]
    person = dist(cur, "t.feat_person", total)
    number = dist(cur, "t.feat_number", total)
    tense = dist(cur, "t.feat_tense", total)
    mood = dist(cur, "t.feat_mood", total)
    voice = dist(cur, "t.feat_voice", total)

    def share(d, k):
        return d.get(k, {}).get("tokens", 0)
    headlines = {
        "third_person": {"k": share(person, "3"), "n": total, "ci95": wilson_ci(share(person, "3"), total)},
        "dual": {"k": share(number, "Dual"), "n": total, "ci95": wilson_ci(share(number, "Dual"), total)},
        "present": {"k": share(tense, "Pres"), "n": total, "ci95": wilson_ci(share(tense, "Pres"), total)},
        "optative": {"k": share(mood, "Opt"), "n": total, "ci95": wilson_ci(share(mood, "Opt"), total)},
        "passive": {"k": share(voice, "Pass"), "n": total, "ci95": wilson_ci(share(voice, "Pass"), total)},
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "study": "Sangram SG-MO-012 (Спряжение: обзор) — частотная рамка финитного глагола",
        "toc_ref": "SG-MO-012",
        "kind": "overview (no kill-gate)",
        "method": "распределение финитных глагольных токенов по пяти НАТИВНЫМ морфопризнакам DCS (лицо/число/время/наклонение/залог) — реальная аттестованная рамка, без приближения",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
        },
        "universe_where": WHERE,
        "denominator_finite_verb_tokens": total,
        "person": person, "number": number, "tense": tense, "mood": mood, "voice": voice,
        "headline_shares_ci95": headlines,
        "notes": {
            "voice": "средний залог отдельно не тегируется — NULL≈актив; Pass выделен (предел разметки)",
            "tense_past": "Tense=Past склеивает претериты (импф./аорист/перфект) — предел EM2, доказан пилотом P3",
            "class": "класс презенса не в признаках — join WhitneyRoots (предел EM1, пилот P2)",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    con.close()
    print(f"denominator (finite-verb tokens): {total:,}", file=sys.stderr)
    print(f"person: {person}", file=sys.stderr)
    print(f"tense: {tense}", file=sys.stderr)
    print(f"mood: {mood}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
