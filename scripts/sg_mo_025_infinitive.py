#!/usr/bin/env python3
"""SG-MO-025 «Инфинитив» — beyond-quota native positive with a diachronic finding.

Beyond-quota core article (opening set already 19/19). The infinitive is NATIVE and
clean in DCS via `feat_verbform='Inf'` — 11,753 tokens. It completes the non-finite
deverbal quartet (`VerbForm∈{Part,Conv,Gdv,Inf}`) alongside the done participles,
absolutive (Conv, SG-MO-026) and gerundive (Gdv, SG-MO-024).

The base set is native-clean, so the surface suffix split is reliable (as for the
gerundive). It carries a DIACHRONIC finding: classical Sanskrit reduced the infinitive
to a single accusative form -tum, but the pinned corpus (much of it Vedic) still
preserves the Vedic infinitive plethora — the frozen case-forms of a verbal noun
(Whitney §§968–988):

  -tum          accusative — the ONLY classical infinitive (~82%): kartum, draṣṭum
  -tave/-tavai  dative (Vedic): jīvitave, sūtave
  -toḥ          genitive/ablative (Vedic): caritoḥ, etoḥ
  -dhyai        dative-like (Vedic): gṛṇadhyai, pibadhyai

So the corpus shows the reduction in numbers: -tum dominant, Vedic remnants ~5%.
feat_case=None (DCS does not tag the frozen case-nature); the case labels are the
traditional analysis, recovered here by surface morphology within the clean Inf set.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/infinitive/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "infinitive" / "data"

SEED = 20260717
SAMPLE_SIZE = 50


def classify(m):
    """Assign a clean Inf token to an infinitive suffix (traditional case-form) by surface."""
    if not m:
        return "(none)"
    if m.endswith("tum") or m.endswith("tuṃ") or m.endswith("ṭum") or m.endswith("ṭuṃ"):
        return "-tum (acc., classical)"
    if re.search(r"(tavai|tave)$", m):
        return "-tave/-tavai (dat., Ved.)"
    if re.search(r"(toḥ|tos)$", m):
        return "-toḥ (gen./abl., Ved.)"
    if m.endswith("dhyai"):
        return "-dhyai (Ved.)"
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
    all_nonfinite = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform IN ('Part','Conv','Gdv','Inf')").fetchone()[0]

    inf_rows = cur.execute("SELECT m_unsandhied, lemma FROM token WHERE feat_verbform='Inf'").fetchall()
    inf = len(inf_rows)
    suf = Counter(classify(m) for m, _ in inf_rows)
    top = cur.execute(
        "SELECT lemma, COUNT(*) c FROM token WHERE feat_verbform='Inf' GROUP BY lemma ORDER BY c DESC LIMIT 10").fetchall()
    # native fields not populated
    case = {c: n for c, n in cur.execute("SELECT feat_case, COUNT(*) FROM token WHERE feat_verbform='Inf' GROUP BY feat_case")}
    # Vedic remnant total (everything not classical -tum, minus 'other' sandhi)
    vedic = sum(n for k, n in suf.items() if "Ved." in k)

    # sibling non-finite (cross-ref)
    gdv = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform='Gdv'").fetchone()[0]
    conv = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform='Conv'").fetchone()[0]

    ids = [r[0] for r in cur.execute("SELECT id FROM token WHERE feat_verbform='Inf'")]
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
        "study": "Sangram SG-MO-025 (Инфинитив) — native positive; diachronic -tum reduction",
        "toc_ref": "SG-MO-025",
        "kind": "beyond-quota core ① (opening set already 19/19); native positive (VerbForm=Inf)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "all_nonfinite_deverbal_part_conv_gdv_inf": all_nonfinite},
        "infinitive_native_positive": {
            "total_verbform_inf": inf,
            "suffix_split_by_surface": dict(suf),
            "vedic_remnant_total": vedic,
            "vedic_remnant_pct": round(100 * vedic / inf, 1),
            "diachronic_note": "classical Sanskrit reduced the infinitive to the accusative -tum alone; the corpus "
                               "preserves the Vedic plethora (frozen case-forms of a verbal noun): -tave/-tavai (dat.), "
                               "-toḥ (gen./abl.), -dhyai. The -tum share (~82%) vs Vedic remnant (~5%) shows the reduction.",
            "top_lemmas": [f"{l} ({c})" for l, c in top],
            "not_split_natively": {"feat_case": case},
            "case_note": "feat_case=None; the frozen case-nature of the Vedic infinitives is the traditional analysis "
                         "(Whitney §§968-988), recovered by surface morphology, not a DCS annotation",
        },
        "cross_reference": {
            "gerundive_gdv": gdv, "absolutive_conv": conv,
            "note": "completes the non-finite deverbal quartet: gerundive (SG-MO-024, Gdv), absolutive (SG-MO-026, "
                    "Conv); the infinitive shares the -tavya/-tum base with the gerundive",
        },
        "traditional_layer": {"witness": "Whitney 1889 §§968-988 (infinitive: accusative -tum + the Vedic case-form infinitives)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "suffix_by_surface": "the suffix/case split is by surface morphology within the clean Inf set; DCS does not tag case (feat_case=None); 'other' ~ -tum sandhi variants",
            "vedic_bias": "the Vedic remnant share reflects the pinned corpus's Vedic content; not a claim about any single register",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"infinitive (VerbForm=Inf): {inf:,}", file=sys.stderr)
    print(f"suffix split: {dict(suf)}", file=sys.stderr)
    print(f"Vedic remnant: {vedic:,} ({round(100*vedic/inf,1)}%)", file=sys.stderr)
    print(f"top lemmas: {[f'{l}({c})' for l,c in top[:5]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
