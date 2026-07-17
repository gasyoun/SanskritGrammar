#!/usr/bin/env python3
"""SG-WF-006 (Композиты: обзор) — compound-membership & member-count frame.

Descriptive corpus frame for the compound cluster (overview, no kill-gate).
Reuses the P4 (SG-WF-008) reconstruction: within a sentence (ordered by idx), a
maximal run of Case=Cpd tokens + the immediately following inflected non-Cpd
token = one compound. Here the frame is:
  1. compound membership (Case=Cpd token count) + sentences carrying a compound;
  2. member-count histogram (2-member, 3-member, 4-member, 5+ member) — the finer
     split P4 collapsed into 2-member vs multi-member;
  3. the sole NATIVE type signal — the UD `compound:coord` deprel (≈ dvandva),
     present only in the dependency-parsed subset (flagged, not projected).

Type classification proper (tatpuruṣa/bahuvrīhi/dvandva shares) is NOT recomputed
here: it is annotation, not a corpus count — the exemplar is P4's two-pass κ over a
120-sample (reported honestly in the article as a sample, not a full-corpus count).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators + Wilson CI on the headline share. Read-only. Emits coverage_summary.json.
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
OUT_DIR = ROOT / "sangram" / "articles" / "compounds-overview" / "data"
PUNCT_UPOS = "PUNCT"


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


def build_universe(cur):
    """Single ordered pass; reconstruct compounds per sentence with member counts."""
    rows = cur.execute(
        "SELECT sentence_id, idx, feat_case, upos FROM token ORDER BY sentence_id, idx"
    )
    counts = {
        "total_compounds": 0,
        "cpd_member_tokens": 0,
        "sentences_with_compounds": 0,
    }
    # histogram of member count = run_len + 1 (the run of Cpd members + inflected head)
    hist = {}
    cur_sid = None
    buf = []

    def flush(buf):
        if not buf:
            return
        by_idx = {r[0]: r for r in buf}
        had_compound = False
        for idx in sorted(by_idx):
            rec = by_idx[idx]
            is_cpd = rec[1] == "Cpd"
            if not is_cpd:
                continue
            counts["cpd_member_tokens"] += 1
            prev = by_idx.get(idx - 1)
            if prev is not None and prev[1] == "Cpd":
                continue  # not a run start
            run_len = 1
            j = idx + 1
            while by_idx.get(j) is not None and by_idx[j][1] == "Cpd":
                run_len += 1
                j += 1
            head = by_idx.get(j)
            if head is None or head[2] == PUNCT_UPOS:
                continue  # dangling run / punctuation head -> malformed, skip
            had_compound = True
            counts["total_compounds"] += 1
            members = run_len + 1  # Cpd members + inflected head
            hist[members] = hist.get(members, 0) + 1
        if had_compound:
            counts["sentences_with_compounds"] += 1

    for sid, idx, fcase, upos in rows:
        if sid != cur_sid:
            flush(buf)
            buf = []
            cur_sid = sid
        buf.append((idx, fcase, upos))
    flush(buf)
    return counts, hist


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

    # native membership denominator (independent of reconstruction)
    cpd_members = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Cpd'").fetchone()[0]
    total_sentences = cur.execute("SELECT COUNT(*) FROM sentence").fetchone()[0]

    # native type signal: compound:coord deprel (≈ dvandva), if the deprel column exists
    coord = None
    parsed_deprel = None
    try:
        coord = cur.execute(
            "SELECT COUNT(*) FROM token WHERE deprel='compound:coord'").fetchone()[0]
        parsed_deprel = cur.execute(
            "SELECT COUNT(*) FROM token WHERE deprel IS NOT NULL AND deprel<>''").fetchone()[0]
    except sqlite3.OperationalError:
        pass  # no deprel column in this master build

    print("Building compound universe (single ordered pass over token)...", file=sys.stderr)
    counts, hist = build_universe(cur)
    con.close()

    total_c = counts["total_compounds"]
    two = hist.get(2, 0)
    multi = total_c - two
    # collapse the long tail into buckets for the article table
    buckets = {
        "2": hist.get(2, 0),
        "3": hist.get(3, 0),
        "4": hist.get(4, 0),
        "5+": sum(v for k, v in hist.items() if k >= 5),
    }
    hist_full = {str(k): hist[k] for k in sorted(hist)}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "study": "Sangram SG-WF-006 (Композиты: обзор) — частотная рамка композитов",
        "toc_ref": "SG-WF-006",
        "kind": "overview (no kill-gate)",
        "method": ("реконструкция композитов из Case=Cpd (пробег + флективная вершина, как P4); "
                   "рамка = членство + гистограмма числа членов + нативный сигнал compound:coord (≈dvandva). "
                   "Классификация типов (татпуруша/бахуврихи/двандва) — не корпусный подсчёт, а разметка: "
                   "экземпляр — двухпроходная κ P4 (SG-WF-008) по выборке 120, честно как выборка"),
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned after dcs-conllu history rewrite; binding is provenance table + SHA-256",
        },
        "denominators": {
            "cpd_member_tokens_native": cpd_members,
            "total_sentences": total_sentences,
            "sentences_with_compounds": counts["sentences_with_compounds"],
            "cpd_member_tokens_reconstructed": counts["cpd_member_tokens"],
            "total_compounds_reconstructed": total_c,
            "two_member": two,
            "multi_member": multi,
        },
        "member_count_buckets": buckets,
        "member_count_histogram": hist_full,
        "member_count_shares": {k: round(v / total_c, 4) for k, v in buckets.items()},
        "two_member_share_ci95": {"k": two, "n": total_c, "ci95": wilson_ci(two, total_c)},
        "native_type_signal": {
            "deprel_available": coord is not None,
            "compound_coord_tokens": coord,
            "parsed_deprel_tokens": parsed_deprel,
            "note": "compound:coord ≈ dvandva; present only in the dependency-parsed subset — flagged, not projected to the full corpus (EM4: type not natively annotated)",
        },
        "type_classification_reference": {
            "study": "P4 / SG-WF-008 (tatpuruṣa)",
            "basis": "two-pass Cohen κ over a seeded 120-compound sample (NOT a full-corpus type count)",
            "note": "codebook anchored on Edgar Leitan's Pāṇinian arrangement (dvigu ⊂ karmadhāraya ⊂ tatpuruṣa)",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"cpd_member_tokens (native Case=Cpd): {cpd_members:,}", file=sys.stderr)
    print(f"total compounds reconstructed: {total_c:,}", file=sys.stderr)
    print(f"member-count buckets: {buckets}", file=sys.stderr)
    print(f"sentences with compounds: {counts['sentences_with_compounds']:,} / {total_sentences:,}",
          file=sys.stderr)
    print(f"compound:coord (native dvandva signal): {coord} of {parsed_deprel} parsed-deprel tokens",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
