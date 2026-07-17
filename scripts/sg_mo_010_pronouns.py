#!/usr/bin/env python3
"""SG-MO-010 «Склонение: местоимения» — pronominal declension.

Core W2 ① article (content, no kill-gate). Pronouns are the EM3 EXCEPTION: a
small, closed, high-frequency class, so — unlike the open noun inventory (median
1 attested cell per lemma, G2 asset) — they attest most of the paradigm. This
script measures that contrast over the pinned DCS snapshot.

Three layers (C5 §3), with a twist for the closed class:
  ATTESTED — PRON case×number coverage per lemma (fresh query; G2 is NOUN-only,
    so pronouns get their own coverage here).
  TRADITIONAL — Whitney 1889 ch. VII §§ 491–521 (pronominal declension); for the
    suppletive closed class the canonical table IS the reference — there is no
    productive generation rule, so GENERATED ≡ TRADITIONAL (transcribed in the
    article, not machine-generated).

DCS lemmatizes pronouns by oblique stem: mad = 1st person (aham/mām/mayā),
tvad = 2nd person, tad/idam/etad/adas = demonstratives, ka = interrogative,
yad = relative, kaścit = indefinite; sarva/anya/para/sama = pronominal adjectives.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators; seeded sample. Read-only. Emits into sangram/articles/pronouns/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "pronouns" / "data"

CASES = ["Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc", "Voc"]
NUMBERS = ["Sing", "Dual", "Plur"]
N_CELLS = 24

WHERE = ("t.upos='PRON' AND t.feat_case IN ('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc') "
         "AND t.feat_number IN ('Sing','Dual','Plur') AND t.lemma IS NOT NULL")

SEED = 20260716
SAMPLE_SIZE = 50


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


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

    # per-lemma coverage (one pass)
    lemmas = {}
    for lemma, case, num, n in cur.execute(
            f"SELECT lemma, feat_case, feat_number, COUNT(*) FROM token t WHERE {WHERE} "
            f"GROUP BY lemma, feat_case, feat_number"):
        rec = lemmas.setdefault(lemma, {"cells": {}, "tokens": 0})
        rec["cells"][f"{case}.{num}"] = n
        rec["tokens"] += n
    total_tokens = sum(r["tokens"] for r in lemmas.values())
    coverage = [len(r["cells"]) for r in lemmas.values()]
    per_lemma = sorted(
        [{"lemma": l, "tokens": r["tokens"], "cells_attested": len(r["cells"])}
         for l, r in lemmas.items()], key=lambda d: -d["tokens"])

    # class-level 24-cell attestation (how many pronoun lemmas attest each cell)
    cell_lemma = {f"{c}.{n}": 0 for c in CASES for n in NUMBERS}
    for r in lemmas.values():
        for cell in r["cells"]:
            cell_lemma[cell] += 1

    # seeded validation sample
    ids = [r[0] for r in cur.execute(f"SELECT t.id FROM token t WHERE {WHERE}")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        sample.append(cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.feat_case, t.feat_gender, "
            "t.feat_number, x.name, c.ref, s.sent_counter FROM token t "
            "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone())
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "case", "gender",
                    "number", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "SG-MO-010 «Склонение: местоимения» — pronominal declension (core W2 ①, content)",
        "toc_ref": "SG-MO-010",
        "kind": "content article (no kill-gate)",
        "method": "PRON case×number coverage per lemma (fresh; G2 is NOUN-only) — the EM3 exception; traditional paradigms = Whitney ch. VII §§491–521 (suppletive closed class → generated ≡ traditional)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "universe_where": WHERE,
        "denominators": {"pron_lemmas": len(lemmas), "case_number_tokens": total_tokens},
        "cells_per_lemma": {
            "median": median(coverage), "mean": round(sum(coverage) / len(coverage), 2),
            "max": max(coverage),
            "pct_lemmas_ge_18": round(100 * sum(1 for c in coverage if c >= 18) / len(coverage), 2),
            "contrast_noun_median": 1,  # G2 asset (H1048): noun median = 1 cell/lemma
        },
        "per_lemma": per_lemma,
        "cell_lemma_counts": cell_lemma,
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "EM3_exception": "pronouns invert EM3: closed high-frequency class → median coverage ≫ nouns (G2 median 1)",
            "suppletion": "pronoun stems are suppletive/irregular (aham↔mad, sa/sā/tat↔tad); DCS lemmatizes by oblique stem, no productive generation rule",
            "gender": "demonstratives (tad/idam/etad) inflect for gender; personals (mad/tvad) do not — coverage here is per lemma across genders",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    cp = summary["cells_per_lemma"]
    print(f"PRON lemmas: {len(lemmas)}; tokens: {total_tokens:,}", file=sys.stderr)
    print(f"cells/lemma: median {cp['median']}, mean {cp['mean']}, max {cp['max']}, "
          f"≥18 cells: {cp['pct_lemmas_ge_18']}% (noun median = 1)", file=sys.stderr)
    print(f"top: {[(d['lemma'], d['tokens'], d['cells_attested']) for d in per_lemma[:8]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
