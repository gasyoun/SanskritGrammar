#!/usr/bin/env python3
"""SG-WF-004 «Вторичная деривация (taddhita): обзор» — corrected version.

Core W2 ① overview (no kill-gate). taddhita = secondary derivation from a nominal.
This SUPERSEDES the earlier "honest negative" take (H1168) with a more complete
finding: taddhita is NOT entirely invisible to the corpus. DCS's SEGMENTATION
layer isolates the four most productive taddhita suffixes as their OWN
morpheme-tokens (each a bare suffix cited as a standalone lemma carrying the case
ending), and the derivational base is recoverable at (sentence_id, idx-1) with
~99.8% coverage:
  -tva (lemma_id 163754, n abstract) · -tā (203679, f abstract) ·
  -maya (109021, adj material) · -vat (167498, comparative)
So productive ABSTRACT and MATERIAL taddhita is natively countable (~24k tokens).

The honest negative still holds for the REST — possessive/relational/patronymic
taddhita (-in, -mant/-vant, -ika, -ya) is lemmatized WHOLE (invisible to the
segmentation trick) and only reachable by surface lemma-ending matching, which is
~50%+ false (pilot P5): proper names, PPP feminines, primary derivatives flood it.

So the article is a productivity survey of the four segmented suffixes (a lower
bound — misses whole-lemmatized sattva/tattva/devatā), plus a structural map +
EM5 caveat for the whole-lemmatized classes. Traditional layer: Whitney ch. XVII
§§1136–1245.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators; seeded sample. Read-only. Emits into sangram/articles/taddhita-overview/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "taddhita-overview" / "data"

# the four productive taddhita suffixes DCS segments as morpheme-tokens
SEG = {163754: ("-tva", "n", "абстракт"), 203679: ("-tā", "f", "абстракт"),
       109021: ("-maya", "adj", "материал «сделанный из»"),
       167498: ("-vat", "ind", "сравнит. «подобно»")}
# whole-lemmatized classes probed by surface ending (EM5-noisy — NOT native)
SURFACE = ["ya", "in", "ika", "vant", "mant"]

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
    noun_adj = cur.execute("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ')").fetchone()[0]

    # --- native segmentation-layer taddhita (the positive finding) ---
    seg = {}
    ids = ",".join(str(i) for i in SEG)
    for lid, (name, g, ru) in SEG.items():
        n = cur.execute("SELECT COUNT(*) FROM token WHERE lemma_id=?", (lid,)).fetchone()[0]
        bases = cur.execute(
            "SELECT COUNT(DISTINCT b.lemma) FROM token s JOIN token b "
            "ON b.sentence_id=s.sentence_id AND b.idx=s.idx-1 WHERE s.lemma_id=?", (lid,)).fetchone()[0]
        top = cur.execute(
            "SELECT b.lemma, COUNT(*) c FROM token s JOIN token b "
            "ON b.sentence_id=s.sentence_id AND b.idx=s.idx-1 WHERE s.lemma_id=? "
            "GROUP BY b.lemma ORDER BY c DESC LIMIT 6", (lid,)).fetchall()
        seg[name] = {"lemma_id": lid, "gender": g, "ru": ru, "tokens": n,
                     "distinct_bases": bases, "top_bases": [f"{b} ({c})" for b, c in top]}
    seg_total = sum(v["tokens"] for v in seg.values())
    with_base = cur.execute(
        f"SELECT COUNT(*) FROM token s JOIN token b ON b.sentence_id=s.sentence_id "
        f"AND b.idx=s.idx-1 WHERE s.lemma_id IN ({ids})").fetchone()[0]
    # -tva base POS profile
    tva_pos = {p: c for p, c in cur.execute(
        "SELECT b.upos, COUNT(*) FROM token s JOIN token b ON b.sentence_id=s.sentence_id "
        "AND b.idx=s.idx-1 WHERE s.lemma_id=163754 GROUP BY b.upos ORDER BY COUNT(*) DESC")}

    # --- surface-ending noise for the whole-lemmatized classes (the honest negative) ---
    surface = {}
    for suf in SURFACE:
        n = cur.execute(
            "SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE ?",
            (f"%{suf}",)).fetchone()[0]
        top = cur.execute(
            "SELECT lemma, COUNT(*) c FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE ? "
            "GROUP BY lemma ORDER BY c DESC LIMIT 5", (f"%{suf}",)).fetchall()
        surface[suf] = {"tokens": n, "top_lemmas": [f"{l} ({c})" for l, c in top]}

    # seeded validation sample of segmented taddhita (base + suffix + locus)
    sids = [r[0] for r in cur.execute(f"SELECT id FROM token WHERE lemma_id IN ({ids})")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(sids), min(SAMPLE_SIZE, len(sids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT s.id, s.m_unsandhied, s.lemma, b.m_unsandhied, b.lemma, b.upos, "
            "x.name, c.ref, se.sent_counter FROM token s "
            "LEFT JOIN token b ON b.sentence_id=s.sentence_id AND b.idx=s.idx-1 "
            "JOIN sentence se ON se.id=s.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE s.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["suffix_token_id", "suffix_form", "suffix_lemma", "base_form",
                    "base_lemma", "base_upos", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "Sangram SG-WF-004 (Деривация: taddhita, обзор) — secondary derivation (corrected)",
        "toc_ref": "SG-WF-004",
        "kind": "overview (no kill-gate); supersedes the 'honest negative' H1168 with the segmentation-layer finding",
        "method": "productive taddhita natively countable via the DCS SEGMENTATION layer — 4 suffixes segmented as morpheme-tokens (lemma_id), base at idx-1; whole-lemmatized possessive/relational/patronymic NOT countable (EM5, surface ~50% false)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "nominal_universe_noun_adj": noun_adj},
        "native_segmented_taddhita": {
            "suffixes": seg, "combined_tokens": seg_total,
            "base_recovery_idx_minus_1": with_base,
            "base_recovery_pct": round(100 * with_base / seg_total, 1),
            "tva_base_pos": tva_pos,
            "note": "the ONE natively countable slice — productive abstract/material derivation; a LOWER BOUND (misses whole-lemmatized sattva/tattva/devatā)",
        },
        "surface_noise_whole_lemmatized_EM5": {
            "endings": surface,
            "note": "possessive/relational/patronymic taddhita is whole-lemmatized; surface-ending matching is ~50%+ false (P5) — proper names, PPP feminines, primary derivatives; NOT counted",
        },
        "traditional_layer": {"witness": "Whitney 1889 ch. XVII §§1136–1245 (secondary derivation / taddhita)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "lower_bound": "native count captures only the 4 segmented suffixes + transparently segmented tokens; whole-lemmatized derivatives (sattva, tattva, devatā, śūnyatā) are missed",
            "EM5_whole_classes": "possessive -in/-mant/-vant, relational -ika, patronymic -ya not natively countable (surface ~50% false, P5)",
            "supersedes": "replaces the earlier honest-negative version (H1168, PR #368) which missed the segmentation-layer signal",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"segmented taddhita: {seg_total:,} tokens ({round(100*with_base/seg_total,1)}% base-recovered)", file=sys.stderr)
    for name, v in seg.items():
        print(f"  {name} ({v['ru']}): {v['tokens']:,} / {v['distinct_bases']} bases", file=sys.stderr)
    print(f"-tva base POS: {tva_pos}", file=sys.stderr)
    print(f"surface noise (EM5): { {k: v['tokens'] for k, v in surface.items()} }", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
