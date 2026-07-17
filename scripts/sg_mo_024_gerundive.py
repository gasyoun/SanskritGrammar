#!/usr/bin/env python3
"""SG-MO-024 «Герундив (причастие долженствования)» — beyond-quota native positive.

Beyond-quota core article (opening set already 19/19). The gerundive (participle of
necessity/obligation, "that which is to be X-ed") is NATIVE and clean in DCS via
`feat_verbform='Gdv'` — 28,260 tokens, a passive-in-sense verbal adjective.

The base set is native-clean (every Gdv token IS a gerundive), so unlike the taddhita
surface trap (~50% false over all nominals), splitting the CLEAN Gdv set by surface
morphology into the three traditional suffixes is reliable — a gerundive ending in
-tavya IS a -tavya gerundive:

  -ya     (kārya, kṛtya "to be done"; jñeya "to be known"; deya "to be given")
  -tavya  (kartavya "to be done / one's duty"; gantavya "to be gone to")
  -anīya  (karaṇīya "to be done")

feat_formation / feat_voice are None for Gdv (DCS does not split the suffix or tag the
inherent passive), so the suffix split is done here by surface morphology; ~5% remains
surface-ambiguous ("other"). The gerundive is inherently passive in sense (agent in the
instrumental), tying it to the passive (SG-MO-027); its -ya suffix is the very form that
floods the taddhita -ya surface bucket (kārya) as a false positive (P5 / SG-WF-004).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/gerundive/data/.
"""
import argparse
import csv
import hashlib
import json
import random
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "gerundive" / "data"

SEED = 20260717
SAMPLE_SIZE = 50


def classify(m):
    """Assign a clean Gdv token to one of the three traditional suffixes by surface."""
    if not m:
        return "(none)"
    if re.search(r"(tavy|tvya)", m):
        return "-tavya"
    if re.search(r"(anīy|nīy)", m):
        return "-anīya"
    if re.search(r"y[aāeoiu]?[mṃnḥstḥ]*$", m):
        return "-ya"
    return "other"


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
    all_part = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform IN ('Part','Conv','Gdv','Inf')").fetchone()[0]

    gdv_rows = cur.execute("SELECT m_unsandhied, lemma FROM token WHERE feat_verbform='Gdv'").fetchall()
    gdv = len(gdv_rows)
    suf = Counter(classify(m) for m, _ in gdv_rows)
    top = cur.execute(
        "SELECT lemma, COUNT(*) c FROM token WHERE feat_verbform='Gdv' GROUP BY lemma ORDER BY c DESC LIMIT 10").fetchall()
    # native fields that are NOT split
    formation = {f: n for f, n in cur.execute("SELECT feat_formation, COUNT(*) FROM token WHERE feat_verbform='Gdv' GROUP BY feat_formation")}
    voice = {v: n for v, n in cur.execute("SELECT feat_voice, COUNT(*) FROM token WHERE feat_verbform='Gdv' GROUP BY feat_voice")}

    # sibling non-finite counts (cross-ref)
    conv = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform='Conv'").fetchone()[0]
    inf = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform='Inf'").fetchone()[0]

    ids = [r[0] for r in cur.execute("SELECT id FROM token WHERE feat_verbform='Gdv'")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT s.id, s.m_unsandhied, s.lemma, x.name, c.ref, se.sent_counter FROM token s "
            "JOIN sentence se ON se.id=s.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE s.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "suffix", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow([r[0], r[1], r[2], classify(r[1]), r[3], r[4], r[5]])

    summary = {
        "study": "Sangram SG-MO-024 (Герундив) — native positive; suffix split within a clean set",
        "toc_ref": "SG-MO-024",
        "kind": "beyond-quota core ① (opening set already 19/19); native positive (VerbForm=Gdv)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "all_nonfinite_deverbal_part_conv_gdv_inf": all_part},
        "gerundive_native_positive": {
            "total_verbform_gdv": gdv,
            "suffix_split_by_surface": dict(suf),
            "suffix_note": "the Gdv SET is native-clean (every token is a gerundive); only the 3-way suffix "
                           "assignment uses surface morphology, ~5% surface-ambiguous ('other'). Reliable, "
                           "unlike the taddhita -ya surface trap (there the base SET was ~50% false).",
            "top_lemmas": [f"{l} ({c})" for l, c in top],
            "not_split_natively": {"feat_formation": formation, "feat_voice": voice},
            "voice_note": "feat_voice is None, but the gerundive is inherently PASSIVE in sense (agent in the "
                          "instrumental) — ties to the passive (SG-MO-027)",
        },
        "cross_reference": {
            "absolutive_conv": conv, "infinitive_inf": inf,
            "note": "sibling non-finite deverbal forms: absolutive (SG-MO-026, Conv), infinitive (SG-MO-025, Inf); "
                    "the -ya gerundive (kārya) is the P5/SG-WF-004 taddhita -ya false positive",
        },
        "traditional_layer": {"witness": "Whitney 1889 §§961–966 (gerundive / future passive participle: -ya, -tavya, -anīya)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "suffix_by_surface": "the 3-way suffix split is by surface morphology within the clean Gdv set (~5% ambiguous); DCS does not tag the suffix (feat_formation None)",
            "voice_not_tagged": "the inherent passive sense is not in feat_voice (None); it is a grammatical fact, not an annotation",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"gerundive (VerbForm=Gdv): {gdv:,}", file=sys.stderr)
    print(f"suffix split: {dict(suf)}", file=sys.stderr)
    print(f"top lemmas: {[f'{l}({c})' for l,c in top[:5]]}", file=sys.stderr)
    print(f"cross-ref: absolutive {conv:,} (SG-MO-026), infinitive {inf:,} (SG-MO-025)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
