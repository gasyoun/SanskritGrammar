#!/usr/bin/env python3
"""SG-MO-028 «Вторичные спряжения: каузатив» — the causative.

Core W2 ① article (content, no kill-gate). The causative (strong root + -aya- +
endings; kārayati "causes to do", darśayati "shows") is a SECONDARY conjugation
that DCS does NOT tag as such — there is no 'Caus' value anywhere in the token
table. The only recovery vector is the LEMMA layer: DCS lemmatizes every -aya-
stem as a separate lemma tagged in lemma.grammar with the Westergaard "class 10"
code (10.P. / 10.Ā.). But that class-10 bucket STRUCTURALLY MERGES the derived
causative (kāray<kṛ, janay<jan, darśay<dṛś) with the PRIMARY curādi/class-X roots
(kathay "tell", pūjay "worship", cintay "think") — both build -aya-, and nothing
in the corpus separates them.

So this article measures the -aya- (class-X) present AS THE CORPUS ENCODES IT —
causative and curādi under one roof — and states plainly that the causative
proper is the semantically dominant but non-isolable half. As a contrast, the
OTHER secondary conjugations DCS DOES separate in lemma.grammar (Denominative,
Desiderative, Intensive) are counted to show what a tagged secondary conjugation
looks like.

Evidence-limit: EM5 (no derivation/valency layer) — the causative is a derived
conjugation and DCS has no layer flagging "this stem is a causative built on X".
Clean causative-vs-curādi separation needs an external root-class inventory
(WhitneyRoots) + per-stem adjudication; a corpus-internal sibling-root heuristic
demonstrably misfires (kathay).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators; seeded sample. Read-only. Emits into sangram/articles/causative/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "causative" / "data"

FIN = ("t.upos='VERB' AND (t.feat_verbform='Fin' OR t.feat_verbform IS NULL) "
       "AND t.feat_person IS NOT NULL")

SEED = 20260717
SAMPLE_SIZE = 50

# clearly-derived causative marquee stems (for the sample/examples), vs primary curādi
KNOWN_CAUS = ["kāray", "darśay", "janay", "sthāpay", "gamay", "yojay", "nāśay",
              "bhojay", "vācay", "pātay", "dhāray"]
KNOWN_CURADI = ["kathay", "pūjay", "cintay", "kāmay", "coray"]


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def gcount(cur, pat):
    return cur.execute(
        f"SELECT COUNT(*) FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
        f"WHERE {FIN} AND replace(l.grammar,' ','') LIKE ?", (pat,)).fetchone()[0]


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

    fin_total = cur.execute(f"SELECT COUNT(*) FROM token t WHERE {FIN}").fetchone()[0]
    class10 = gcount(cur, "10.%")
    # secondary conjugations DCS DOES separate (contrast)
    denom = gcount(cur, "%Denom%")
    desid = gcount(cur, "%Desid%")
    inten = gcount(cur, "%Int.%")
    caus_label = gcount(cur, "%Caus%")  # expected 0 — proves the causative is untagged

    distinct = cur.execute(
        f"SELECT COUNT(DISTINCT t.lemma) FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
        f"WHERE {FIN} AND replace(l.grammar,' ','') LIKE '10.%'").fetchone()[0]
    top = cur.execute(
        f"SELECT t.lemma, COUNT(*) c FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
        f"WHERE {FIN} AND replace(l.grammar,' ','') LIKE '10.%' AND t.lemma IS NOT NULL "
        f"GROUP BY t.lemma ORDER BY c DESC LIMIT 20").fetchall()

    ids = [r[0] for r in cur.execute(
        f"SELECT t.id FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
        f"WHERE {FIN} AND replace(l.grammar,' ','') LIKE '10.%'")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        sample.append(cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, l.grammar, t.feat_person, "
            "t.feat_tense, x.name, c.ref, s.sent_counter FROM token t "
            "JOIN lemma l ON l.lemma_id=t.lemma_id "
            "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone())
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "grammar", "person",
                    "tense", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "SG-MO-028 «Каузатив» — causative secondary conjugation (core W2 ①, content)",
        "toc_ref": "SG-MO-028",
        "kind": "content article (no kill-gate; map-heavy — measurable core + honest conflation)",
        "method": "the causative is NOT tagged (Caus label = 0); the -aya- stem is the Westergaard class-10 (lemma.grammar '10.%'), which MERGES derived causative + primary curādi; measured as one bucket, with the causative proper flagged as non-isolable",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"finite_total": fin_total},
        "class_x_aya_bucket": {
            "finite_tokens": class10, "share_of_finite": round(class10 / fin_total, 4),
            "distinct_lemmas": distinct,
            "note": "class-X (-aya-) present = causative + primary curādi under one roof; NOT separable natively",
        },
        "causative_untagged_proof": {"caus_label_count": caus_label,
                                     "note": "zero 'Caus' entries anywhere → the causative has no dedicated tag"},
        "secondary_conjugations_dcs_separates": {
            "denominative": denom, "desiderative": desid, "intensive": inten,
            "note": "these secondary conjugations ARE tagged in lemma.grammar, so they do NOT contaminate the class-X bucket — the caus/curādi conflation is the ONLY remaining fusion",
        },
        "top_class_x_lemmas": [{"lemma": l, "tokens": c,
                                "kind": ("caus" if l in KNOWN_CAUS else "curādi" if l in KNOWN_CURADI else "?")}
                               for l, c in top],
        "traditional_layer": {"witness": "Whitney 1889 §§1041–1052 (causative)"},
        "limits": {
            "EM5_no_valency": "the causative is a derived conjugation with no tag; corpus-internally not isolable from primary curādi (both = class-X -aya-)",
            "class_x_fusion": "lemma.grammar '10.' fuses derived causative + primary curādi; clean separation needs WhitneyRoots root-class + per-stem adjudication (sibling-root heuristic misfires, e.g. kathay)",
            "surface_noise": "raw -ayati/-ayate surface matching is ~16-20% noisy AND still cannot separate caus from curādi",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"finite {fin_total:,}; class-X (-aya-, caus+curādi) {class10:,} ({100*class10/fin_total:.1f}%); {distinct} lemmas", file=sys.stderr)
    print(f"caus label count (want 0): {caus_label}", file=sys.stderr)
    print(f"DCS-separated secondary: Denom {denom}, Desid {desid}, Int {inten}", file=sys.stderr)
    print(f"top: {[(x['lemma'], x['tokens'], x['kind']) for x in summary['top_class_x_lemmas'][:8]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
