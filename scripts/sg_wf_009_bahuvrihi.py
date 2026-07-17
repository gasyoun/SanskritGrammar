#!/usr/bin/env python3
"""SG-WF-009 «Композиты: bahuvrīhi (обзор)» — the endgame limit article.

Core W2 ① overview, the LAST of the 19-slot core (18/19 → 19/19). It is
C6-BLOCKED and publishes the LIMIT, exactly like the honest-negative pilots
(P3 perfect, P5 kṛt-names, SG-WF-004 taddhita's whole-lemmatized half).

Why bahuvrīhi cannot be counted from the corpus (EM4 + C6):
  A bahuvrīhi is an EXOCENTRIC (possessive) compound — its referent lies
  OUTSIDE the compound: bahu-vrīhi "much-rice" does not denote rice but "one
  who has much rice". So it is NOT identifiable from the compound's internal
  structure alone (unlike tatpuruṣa/dvandva, whose head is internal). Deciding
  bahuvrīhi requires reading the external referent — semantics/syntax — which
  is the C6 program (semantics/syntax), not yet built. DCS annotates compound
  TYPE with 0 features (EM4). So no census is possible.

What CAN be shown (no census — a P4-SAMPLE exemplar set):
  The tatpuruṣa pilot P4 (SG-WF-008) blind-double-annotated 120 sampled
  compounds by the Leitan codebook; coarse-type inter-annotator κ = 0.93.
  Incidentally, that sample carried bahuvrīhi labels: this script reads the
  committed P4 annotations, isolates the compounds BOTH passes labeled
  bahuvrīhi (the cleanest exemplars), and reports the sample-level type mix
  as ILLUSTRATIVE ONLY (explicitly NOT a corpus frequency).

Contract C3: consumes the committed P4 data; optional DCS enrichment for loci
under the pinned snapshot (refuse without provenance pin). Read-only.
Emits into sangram/articles/bahuvrihi/data/.
"""
import argparse
import csv
import hashlib
import json
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
P4_ANNOT = ROOT / "sangram" / "articles" / "tatpurusha" / "data" / "annotations_full.tsv"
OUT_DIR = ROOT / "sangram" / "articles" / "bahuvrihi" / "data"


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def locus_for(cur, tid):
    r = cur.execute(
        "SELECT s.m_unsandhied, s.lemma, x.name, c.ref, se.sent_counter FROM token s "
        "JOIN sentence se ON se.id=s.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
        "JOIN text x ON x.text_id=c.text_id WHERE s.id=?", (tid,)).fetchone()
    if not r:
        return None
    return {"first_member_form": r[0], "first_member_lemma": r[1],
            "text": r[2], "ref": f"{r[3]} (s{r[4]})"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--skip-checksum", action="store_true")
    args = ap.parse_args()

    if not P4_ANNOT.exists():
        print(f"ERROR: P4 annotations not found: {P4_ANNOT}", file=sys.stderr)
        return 1
    rows = list(csv.DictReader(open(P4_ANNOT, encoding="utf-8"), delimiter="\t"))

    # sample-level coarse-type mix (ILLUSTRATIVE, NOT a census)
    coarse = Counter(r["coarse"] for r in rows)
    n_annotations = len(rows)
    n_compounds = len({r["cpd_token_id"] for r in rows})

    # compounds BOTH passes labeled bahuvrihi = the clean exemplar pool
    by_id = defaultdict(dict)
    for r in rows:
        by_id[r["cpd_token_id"]][r["pass"]] = r
    agreed = [(tid, d["A"]) for tid, d in by_id.items()
              if d.get("A", {}).get("coarse") == "bahuvrihi"
              and d.get("B", {}).get("coarse") == "bahuvrihi"]

    # optional DCS enrichment for loci (needs the pinned snapshot)
    prov, sha, exemplars = {}, "not-read", []
    db = Path(args.db)
    if db.exists():
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        cur = con.cursor()
        prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
        if "source_commit" not in prov:
            print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr)
            return 1
        sha = "skipped" if args.skip_checksum else sha256_file(db)
        for tid, a in agreed:
            loc = locus_for(cur, int(tid))
            exemplars.append({"cpd_token_id": int(tid), "vigraha": a["vigraha"],
                              "coarse": "bahuvrihi", "locus": loc})
        con.close()
    else:
        print(f"WARN: DCS master absent ({db}); loci not enriched", file=sys.stderr)
        for tid, a in agreed:
            exemplars.append({"cpd_token_id": int(tid), "vigraha": a["vigraha"],
                              "coarse": "bahuvrihi", "locus": None})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "bahuvrihi_exemplars.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["cpd_token_id", "vigraha", "first_member_form", "text", "ref"])
        for e in exemplars:
            loc = e["locus"] or {}
            w.writerow([e["cpd_token_id"], e["vigraha"],
                        loc.get("first_member_form", ""), loc.get("text", ""), loc.get("ref", "")])

    summary = {
        "study": "Sangram SG-WF-009 (Композиты: bahuvrīhi, обзор) — the endgame LIMIT article",
        "toc_ref": "SG-WF-009",
        "kind": "overview (no kill-gate); C6-BLOCKED — publishes the limit, no census (EM4 + exocentricity)",
        "why_no_census": (
            "bahuvrīhi is exocentric: referent lies OUTSIDE the compound, so type is not "
            "identifiable from internal structure — needs external semantics/syntax (C6, not built). "
            "DCS annotates compound type with 0 features (EM4)."),
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "p4_sample_illustrative_NOT_census": {
            "source": "SG-WF-008 tatpuruṣa pilot P4 blind double-annotation (Leitan codebook), coarse κ=0.93",
            "sampled_compounds": n_compounds, "annotations_both_passes": n_annotations,
            "coarse_mix": dict(coarse),
            "bahuvrihi_both_passes_agreed": len(agreed),
            "caveat": "the P4 sample was drawn FOR the tatpuruṣa study, not as a compound-type census; "
                      "the ~15% bahuvrihi share is a SAMPLE artefact, NOT a corpus frequency",
        },
        "traditional_layer": {"witness": "Whitney 1889 §§1293–1308 (possessive / bahuvrīhi compounds); Leitan codebook (Pāṇinian)"},
        "exemplars_both_passes_agreed": exemplars,
        "limits": {
            "C6_blocked": "no census possible without the semantics/syntax program (C6)",
            "EM4": "compound type unannotated in DCS (0 features)",
            "exocentricity": "vigraha of every exemplar ends in an EXTERNAL relative (yasya saḥ / yeṣāṃ te) — the mark of the referent lying outside the compound",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"P4 sample: {n_compounds} compounds, coarse mix {dict(coarse)}", file=sys.stderr)
    print(f"bahuvrihi both-pass agreed: {len(agreed)} (exemplar pool)", file=sys.stderr)
    print("NO CENSUS — C6-blocked (exocentric, EM4). Publishes the limit.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
