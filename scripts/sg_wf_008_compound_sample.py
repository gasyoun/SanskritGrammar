#!/usr/bin/env python3
"""Sangram pilot P4 (SG-WF-008, tatpuruṣa) — compound sample builder.

Tests evidence-limit EM4: DCS marks compound *membership* (`Case=Cpd`) and
segmentation, but not the compound *type*. This script draws the seeded sample
of 2-member compounds that the two independent classification passes annotate;
the inter-annotator Cohen κ over those passes is the C5 §7 P4 kill-gate.

Reconstruction: within a sentence (ordered by idx), a maximal run of `Case=Cpd`
tokens + the immediately following inflected non-Cpd token = one compound.
A 2-member compound = run length 1 (one Cpd member) + the inflected head. The
2-member restriction isolates type-classification from recursive right-to-left
bracketing (multi-member compounds are reported as a limitation, not sampled).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256, seeded
random sample (never "first N"), recorded denominator. Emits coverage_summary.json
+ validation_sample.tsv into sangram/articles/tatpurusa/data/.
"""
import sqlite3
import sys
import json
import random
import hashlib
import argparse
import csv
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "tatpurusa" / "data"

SEED = 20260715
SAMPLE_SIZE = 120
PUNCT_UPOS = "PUNCT"


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def build_universe(cur):
    """Single ordered pass; reconstruct compounds per sentence.

    Returns (twomember_cpd_ids, counts) where twomember_cpd_ids is the list of
    the Cpd-token id that heads each 2-member compound (head is deterministic at
    idx+1), and counts holds the universe denominators.
    """
    rows = cur.execute(
        "SELECT sentence_id, idx, id, feat_case, upos FROM token "
        "ORDER BY sentence_id, idx"
    )
    two_member = []
    counts = {
        "total_compounds": 0,
        "two_member": 0,
        "multi_member": 0,
        "cpd_member_tokens": 0,
        "sentences_with_compounds": 0,
    }
    cur_sid = None
    buf = []  # list of (idx, id, feat_case, upos) for the current sentence

    def flush(buf):
        if not buf:
            return
        buf.sort(key=lambda r: r[0])
        by_idx = {r[0]: r for r in buf}
        had_compound = False
        i = 0
        n = len(buf)
        # walk positions in idx order
        idxs = [r[0] for r in buf]
        seen_run_start = set()
        for pos, idx in enumerate(idxs):
            rec = by_idx[idx]
            is_cpd = rec[2] == "Cpd"
            if not is_cpd:
                continue
            counts["cpd_member_tokens"] += 1
            # run start = this Cpd not preceded (idx-1) by a Cpd
            prev = by_idx.get(idx - 1)
            if prev is not None and prev[2] == "Cpd":
                continue  # not a run start; counted as member above
            # measure run length forward
            run_len = 1
            j = idx + 1
            while by_idx.get(j) is not None and by_idx[j][2] == "Cpd":
                run_len += 1
                j += 1
            head = by_idx.get(j)  # first non-Cpd token after the run
            if head is None or head[3] == PUNCT_UPOS:
                continue  # dangling run / punctuation head -> malformed, skip
            had_compound = True
            counts["total_compounds"] += 1
            if run_len == 1:
                counts["two_member"] += 1
                two_member.append(rec[1])  # the Cpd token id (head at idx+1)
            else:
                counts["multi_member"] += 1
        if had_compound:
            counts["sentences_with_compounds"] += 1

    for sid, idx, tid, fcase, upos in rows:
        if sid != cur_sid:
            flush(buf)
            buf = []
            cur_sid = sid
        buf.append((idx, tid, fcase, upos))
    flush(buf)
    return two_member, counts


def fetch_detail(cur, cpd_id):
    """Full detail for one 2-member compound given its Cpd token id."""
    c = cur.execute(
        "SELECT id, sentence_id, idx, form, m_unsandhied, lemma, lemma_id, upos, "
        "feat_case, feat_gender, feat_number FROM token WHERE id=?", (cpd_id,)
    ).fetchone()
    sid, cidx = c[1], c[2]
    h = cur.execute(
        "SELECT id, idx, form, m_unsandhied, lemma, lemma_id, upos, "
        "feat_case, feat_gender, feat_number FROM token "
        "WHERE sentence_id=? AND idx=?", (sid, cidx + 1)
    ).fetchone()
    sent = cur.execute(
        "SELECT s.sent_id, s.sent_counter, s.text_sandhied, c.ref, t.name "
        "FROM sentence s JOIN chapter c ON c.chapter_id=s.chapter_id "
        "JOIN text t ON t.text_id=c.text_id WHERE s.id=?", (sid,)
    ).fetchone()
    dep = cur.execute("SELECT lemma, grammar FROM lemma WHERE lemma_id=?", (c[6],)).fetchone()
    hd = cur.execute("SELECT lemma, grammar FROM lemma WHERE lemma_id=?", (h[5],)).fetchone()
    m1 = c[4] or c[3]
    m2 = h[3] or h[2]
    return {
        "cpd_token_id": c[0],
        "sentence_id": sid,
        "member1_form": c[3], "member1_unsandhied": c[4], "member1_lemma": c[5],
        "member1_lemma_id": c[6], "member1_upos": c[7],
        "member1_dict_grammar": (dep[1] if dep else None),
        "head_form": h[2], "head_unsandhied": h[3], "head_lemma": h[4],
        "head_lemma_id": h[5], "head_upos": h[6],
        "head_case": h[7], "head_gender": h[8], "head_number": h[9],
        "head_dict_grammar": (hd[1] if hd else None),
        "compound_reconstructed": f"{m1}-{m2}",
        "compound_surface": f"{c[3]}{h[2]}",
        "sent_dcs_id": (sent[0] if sent else None),
        "locus": (f"{sent[4]} {sent[3]} s{sent[1]}" if sent else None),
        "sentence_text": (sent[2] if sent else None),
    }


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

    print("Building compound universe (single ordered pass over token)...", file=sys.stderr)
    two_member, counts = build_universe(cur)
    print(f"  total compounds: {counts['total_compounds']:,}", file=sys.stderr)
    print(f"  2-member: {counts['two_member']:,}  multi-member: {counts['multi_member']:,}",
          file=sys.stderr)

    rng = random.Random(SEED)
    chosen = rng.sample(sorted(two_member), min(SAMPLE_SIZE, len(two_member)))
    detail = [fetch_detail(cur, cid) for cid in chosen]

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    summary = {
        "study": "Sangram P4 (SG-WF-008, tatpuruṣa) — compound-type inter-annotator κ study",
        "toc_ref": "SG-WF-008",
        "evidence_limit": "EM4 — compound type not annotated in DCS (segmentation only)",
        "method": "two independent classification passes over a seeded sample; Cohen κ; C5 §7 P4 kill-gate κ<0.7",
        "codebook_anchor": "Edgar Leitan (Э. З. Лейтан), Pāṇinian/Mahābhāṣya arrangement — dvigu ⊂ karmadhāraya ⊂ tatpuruṣa",
        "snapshot": {
            "master": str(db).replace(str(GITHUB), "<GitHub>"),
            "source_repo": prov.get("source_repo"),
            "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"),
            "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned after dcs-conllu history rewrite; binding is provenance table + SHA-256",
        },
        "universe_where": "token.feat_case='Cpd' reconstructed into compounds; 2-member = run length 1 + inflected head",
        "denominators": {
            "total_cpd_member_tokens": counts["cpd_member_tokens"],
            "sentences_with_compounds": counts["sentences_with_compounds"],
            "total_compounds": counts["total_compounds"],
            "two_member_compounds": counts["two_member"],
            "multi_member_compounds": counts["multi_member"],
        },
        "sample": {"seed": SEED, "size": len(detail),
                   "frame": "2-member compounds only (multi-member deferred as a limitation)"},
        "kill_gate": {"metric": "Cohen κ (coarse + fine)", "threshold": 0.7,
                      "rule": "κ<0.7 → revise type taxonomy before publication (C5 §7 P4); negative result publishable (C3 П7)",
                      "status": "PENDING — two annotation passes not yet run"},
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cols = ["cpd_token_id", "sent_dcs_id", "locus", "compound_reconstructed", "compound_surface",
            "member1_unsandhied", "member1_lemma", "member1_upos", "member1_dict_grammar",
            "head_unsandhied", "head_lemma", "head_upos", "head_case", "head_gender", "head_number",
            "head_dict_grammar", "sentence_text"]
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(cols)
        for d in detail:
            w.writerow([d.get(k, "") for k in cols])

    con.close()
    print(f"Wrote {OUT_DIR/'coverage_summary.json'} and validation_sample.tsv "
          f"({len(detail)} compounds).", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
