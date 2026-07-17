#!/usr/bin/env python3
"""SG-WF-011 «Глаголы с превербами (upasarga)» — beyond-quota native positive.

Beyond-quota core article (opening set already 19/19). The preverb (upasarga) system —
verbal prefixes that modify a root's meaning (gam "go" → ā-gam "come", sam-gam "unite",
ni-gam "enter") — is NATIVELY recoverable in DCS: the `lemma` table carries a `preverbs`
field, and the lemma itself is the preverb+root compound. So this is a large clean native
positive, not a derivation-layer guess:

  369,870 VERB tokens (36.7% of all verbs) belong to a preverbed lemma.
  Top single preverbs (by verb-token): pra 55,479 · ā 47,901 · vi 37,425 · sam 31,386 ·
  upa 20,305 · ni 19,994 · ut 17,275 · abhi 14,959 · pari 13,597 · ...
  Productive STACKING: 968 distinct preverb strings, incl. multi-preverb (samā 7,711 =
  sam+ā). Top preverbed verbs: prāp (pra+āp "obtain") 6,022, āgam (ā+gam "come") 4,640.

The `preverbs` field stores the preverb string (single "pra" or concatenated "samā");
the split into the ~22 canonical upasargas is by prefix-matching that string. That
matching is over a NATIVE, clean set (every such lemma genuinely carries a preverb) —
unlike the taddhita surface trap.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/preverbs/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "preverbs" / "data"

# the ~22 canonical upasargas (Whitney §1076), longest-first for prefix matching
UPASARGA = ["adhi", "anu", "antar", "apa", "api", "abhi", "ava", "ā", "ut", "upa",
            "ni", "niḥ", "nis", "parā", "pari", "pra", "prati", "vi", "sam", "su", "dus", "acchā"]
UPASARGA.sort(key=len, reverse=True)
SEED = 20260717
SAMPLE_SIZE = 50


def first_upasarga(pv):
    for u in UPASARGA:
        if pv.startswith(u):
            return u
    return "(other)"


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
    all_verb = cur.execute("SELECT COUNT(*) FROM token WHERE upos='VERB'").fetchone()[0]
    lemmas_total = cur.execute("SELECT COUNT(*) FROM lemma").fetchone()[0]
    lemmas_pv = cur.execute("SELECT COUNT(*) FROM lemma WHERE preverbs IS NOT NULL AND preverbs != ''").fetchone()[0]

    WITH = ("FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
            "WHERE t.upos='VERB' AND l.preverbs IS NOT NULL AND l.preverbs != ''")
    preverbed = cur.execute(f"SELECT COUNT(*) {WITH}").fetchone()[0]
    distinct_pv = cur.execute("SELECT COUNT(DISTINCT preverbs) FROM lemma WHERE preverbs IS NOT NULL AND preverbs != ''").fetchone()[0]

    # by preverb string (verb-token weighted)
    by_string = cur.execute(
        f"SELECT l.preverbs, COUNT(*) c {WITH} GROUP BY l.preverbs ORDER BY c DESC LIMIT 20").fetchall()
    # collapse to leading canonical upasarga
    lead = {}
    for pv, c in cur.execute(f"SELECT l.preverbs, COUNT(*) c {WITH} GROUP BY l.preverbs"):
        lead[first_upasarga(pv)] = lead.get(first_upasarga(pv), 0) + c
    lead_sorted = sorted(lead.items(), key=lambda kv: kv[1], reverse=True)
    # multi-preverb (leading upasarga stripped leaves another upasarga)
    multi = 0
    for pv, c in cur.execute(f"SELECT l.preverbs, COUNT(*) c {WITH} GROUP BY l.preverbs"):
        u = first_upasarga(pv)
        rest = pv[len(u):] if u != "(other)" else ""
        if rest and first_upasarga(rest) != "(other)":
            multi += c
    # top preverbed verb lemmas
    top_verbs = cur.execute(
        f"SELECT l.lemma, l.preverbs, COUNT(*) c {WITH} GROUP BY l.lemma_id ORDER BY c DESC LIMIT 10").fetchall()

    # seeded sample
    ids = [r[0] for r in cur.execute(f"SELECT t.id {WITH}")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT t.id, t.m_unsandhied, l.lemma, l.preverbs, x.name, c.ref, se.sent_counter FROM token t "
            "JOIN lemma l ON l.lemma_id=t.lemma_id JOIN sentence se ON se.id=t.sentence_id "
            "JOIN chapter c ON c.chapter_id=se.chapter_id JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "preverbs", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "Sangram SG-WF-011 (Глаголы с превербами / upasarga) — native positive",
        "toc_ref": "SG-WF-011",
        "kind": "beyond-quota core ① (opening set already 19/19); native positive (lemma.preverbs)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total, "all_verb_tokens": all_verb,
                         "lemmas_total": lemmas_total, "lemmas_with_preverb": lemmas_pv},
        "preverbs_native_positive": {
            "preverbed_verb_tokens": preverbed,
            "preverbed_pct_of_verbs": round(100 * preverbed / all_verb, 1),
            "distinct_preverb_strings": distinct_pv,
            "by_preverb_string_top20": [{"preverb": p, "tokens": c} for p, c in by_string],
            "by_leading_upasarga": [{"upasarga": u, "tokens": c} for u, c in lead_sorted[:22]],
            "multi_preverb_tokens": multi,
            "top_preverbed_verbs": [f"{l} ({pv}, {c})" for l, pv, c in top_verbs],
            "note": "the preverbs field is native (every such lemma carries a preverb); the split into canonical "
                    "upasargas is by prefix-matching a NATIVE set — not the taddhita surface trap",
        },
        "traditional_layer": {"witness": "Whitney 1889 §§1076-1087 (verbal prefixes / upasarga); Pāṇini 1.4.58-97 (gati/upasarga)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "prefix_match": "the ~22-upasarga split is by prefix-matching the native preverbs string; a few concatenations are ambiguous ('(other)')",
            "lemma_level": "preverb attaches at the LEMMA level (lemma.preverbs); token-level sandhi/tmesis (esp. Vedic detached preverbs) is not separately resolved here",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"preverbed verb tokens: {preverbed:,} ({round(100*preverbed/all_verb,1)}% of verbs)", file=sys.stderr)
    print(f"distinct preverb strings: {distinct_pv}; multi-preverb tokens: {multi:,}", file=sys.stderr)
    print(f"top leading upasargas: {lead_sorted[:8]}", file=sys.stderr)
    print(f"top preverbed verbs: {[f'{l}({pv})={c}' for l,pv,c in top_verbs[:5]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
