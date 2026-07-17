#!/usr/bin/env python3
"""SG-MO-019 «Аорист: редуплицированный и сигматический» — beyond-quota native positive.

Beyond-quota core article (opening set already 19/19). A DEEPER dive into the aorist
than SG-MO-018 (which counted the aggregate 12,054 formation-marked aorists): here the
seven TRADITIONAL aorist formation types are split NATIVELY via `feat_formation` on
`feat_tense='Past'` + `upos='VERB'`:

  root  — root/simple aorist       (abhūt "became")          5,690
  them  — thematic / a-aorist      (avocat "said")           2,781
  s     — s-aorist (sigmatic)      (akārṣīt "did")           1,508
  is    — iṣ-aorist (sigmatic)     (avadhīt "slew")          1,077
  red   — reduplicated aorist      (ajījanat "generated")      833
  sa    — sa-aorist (sigmatic)     (adhukṣat "milked")         124
  sis   — siṣ-aorist (sigmatic)    (udagāsīt "sang up")         41

Total = 12,054 — exactly the SG-MO-018 aggregate (the split is a partition, not a
new count). NB: `feat_formation='peri'` on `Tense=Past` (4,046) is the PERIPHRASTIC
PERFECT, not an aorist — excluded here (it is SG-MO-032's slot).

This is a clean native positive: the aorist type SYSTEM (a classic grammar topic:
root vs thematic vs the three/four sigmatic vs reduplicated) is recovered directly
from native annotation, no surface guessing. Caveat inherited from SG-MO-018: the
aorist itself is a LOWER BOUND (only 12,054 of ~102k Tense=Past carry a formation
tag; EM2 conflates Past). Traditional layer: Whitney ch. IX §§824-930.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/aorist-types/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "aorist-types" / "data"

# the seven traditional aorist formation types (feat_formation values), in traditional order
AOR = {
    "root": ("root/simple", "корневой (простой)"),
    "them": ("thematic / a-aorist", "тематический (a-аорист)"),
    "red": ("reduplicated", "редуплицированный"),
    "s": ("s-aorist", "сигматический -s-"),
    "is": ("iṣ-aorist", "сигматический -iṣ-"),
    "sis": ("siṣ-aorist", "сигматический -siṣ-"),
    "sa": ("sa-aorist", "сигматический -sa-"),
}
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
    all_past = cur.execute("SELECT COUNT(*) FROM token WHERE feat_tense='Past'").fetchone()[0]

    WHERE = "feat_tense='Past' AND upos='VERB' AND feat_formation=?"
    types = {}
    for key, (en, ru) in AOR.items():
        n = cur.execute(f"SELECT COUNT(*) FROM token WHERE {WHERE}", (key,)).fetchone()[0]
        bases = cur.execute(f"SELECT COUNT(DISTINCT lemma) FROM token WHERE {WHERE}", (key,)).fetchone()[0]
        top = cur.execute(
            f"SELECT lemma, COUNT(*) c FROM token WHERE {WHERE} GROUP BY lemma ORDER BY c DESC LIMIT 5", (key,)).fetchall()
        types[key] = {"en": en, "ru": ru, "tokens": n, "distinct_lemmas": bases,
                      "top_lemmas": [f"{l} ({c})" for l, c in top]}
    aor_total = sum(v["tokens"] for v in types.values())
    # sanity: periphrastic perfect (peri under Past) is NOT an aorist
    peri_past = cur.execute("SELECT COUNT(*) FROM token WHERE feat_tense='Past' AND feat_formation='peri'").fetchone()[0]

    # seeded validation sample across the 7 types
    ids = [r[0] for r in cur.execute(
        "SELECT id FROM token WHERE feat_tense='Past' AND upos='VERB' AND feat_formation IN ('root','them','red','s','is','sis','sa')")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT s.id, s.m_unsandhied, s.lemma, s.feat_formation, x.name, c.ref, se.sent_counter FROM token s "
            "JOIN sentence se ON se.id=s.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE s.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "formation", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    sigmatic = types["s"]["tokens"] + types["is"]["tokens"] + types["sis"]["tokens"] + types["sa"]["tokens"]
    summary = {
        "study": "Sangram SG-MO-019 (Аорист: редупл. и сигматический) — 7 native aorist types",
        "toc_ref": "SG-MO-019",
        "kind": "beyond-quota core ① (opening set already 19/19); native positive — partition of SG-MO-018's aorist",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "all_tense_past": all_past},
        "aorist_types_native": {
            "types": types, "combined_tokens": aor_total,
            "sigmatic_subtotal": sigmatic,
            "note": "the 7 traditional aorist formation types via feat_formation on Tense=Past VERB; "
                    "combined = the SG-MO-018 aggregate 12,054 (a PARTITION, not a new count)",
        },
        "not_aorist_periphrastic_perfect": {
            "peri_under_past": peri_past,
            "note": "feat_formation='peri' on Tense=Past is the PERIPHRASTIC PERFECT (SG-MO-032), NOT an aorist; excluded",
        },
        "traditional_layer": {"witness": "Whitney 1889 ch. IX §§824-930 (aorist systems: root, thematic, reduplicated, sibilant)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "lower_bound": "inherits SG-MO-018's caveat — only 12,054 of ~102k Tense=Past carry a formation tag (EM2 conflates Past); the type split covers only formation-marked aorists",
            "native_partition": "the split itself is native (feat_formation) and exhaustive over the marked aorists — no surface guessing",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"aorist types (native, Tense=Past VERB feat_formation): total {aor_total:,}", file=sys.stderr)
    for k, v in types.items():
        print(f"  {k} ({v['en']}): {v['tokens']:,} / {v['distinct_lemmas']} lemmas", file=sys.stderr)
    print(f"sigmatic subtotal (s+is+sis+sa): {sigmatic:,}", file=sys.stderr)
    print(f"[excluded] periphrastic perfect (peri/Past): {peri_past:,} — NOT aorist (SG-MO-032)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
