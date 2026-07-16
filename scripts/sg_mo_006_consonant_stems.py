#!/usr/bin/env python3
"""SG-MO-006 «Склонение: согласные основы» — consonant-stem declension.

Core W2 ① article (content, no kill-gate — the method is proven by pilots P1–P5).
Three layers per the C5 morphology programme:
  ATTESTED — CONSUMES the G2 asset (sangram/data/declension_cell_coverage), the
    materialized attested-cells-per-lemma table (H1048); this script does NOT
    recompute cell coverage, it reads the consonant-stem slice + adds a seeded
    validation sample (loci) from the pinned master for the C3 query→sample cycle.
  GENERATED — MWinflect nominals/pydecl for representative subclass paradigms
    (rājan m-an, karman n-an, manas n-as, cakṣus n-us, yogin m-in); the table is
    row-major CASE × NUMBER (same mapping as pilot P1).
  TRADITIONAL — Whitney 1889 ch. V (consonant stems, §§ 383–465): strong / middle
    / weak stem gradation, the defining property of the class.

Consonant-stem class = G2 stem_final ∈ {an, in, as, is, us, other_consonant};
r-stems (ṛ) are a separate class (agent nouns) and are excluded, noted as a limit.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators; seeded sample (never "first N"). Read-only. Emits into
sangram/articles/consonant-stems/data/.
"""
import argparse
import csv
import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
G2_CSV = ROOT / "sangram" / "data" / "declension_cell_coverage" / "lemma_cell_coverage.csv"
OUT_DIR = ROOT / "sangram" / "articles" / "consonant-stems" / "data"
MWINFLECT = GITHUB / "MWinflect"

CASES = ["Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc", "Voc"]
NUMBERS = ["Sing", "Dual", "Plur"]
CONS_CLASSES = {"an", "in", "as", "is", "us", "other_consonant"}

SEED = 20260716
SAMPLE_SIZE = 50  # C3 §4.2 floor is 50

# representative attested subclass exemplars → (MWinflect class name, SLP1 stem)
REPRESENTATIVES = [
    ("an_masc", "Decline_m_an", "rAjan", "rājan", "царь"),
    ("an_neut", "Decline_n_an", "karman", "karman", "деяние"),
    ("as_neut", "Decline_n_as", "manas", "manas", "ум"),
    ("us_neut", "Decline_n_us", "cakzus", "cakṣus", "глаз"),
    ("in_masc", "Decline_m_in", "yogin", "yogin", "йогин"),
]


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def read_g2_consonant_slice():
    rows = list(csv.DictReader(open(G2_CSV, encoding="utf-8")))
    cons = [r for r in rows if r["stem_final"] in CONS_CLASSES]
    by_class = {}
    for r in cons:
        c = r["stem_final"]
        b = by_class.setdefault(c, {"lemmas": 0, "tokens": 0, "cells": 0})
        b["lemmas"] += 1
        b["tokens"] += int(r["tokens"])
        b["cells"] += int(r["cells_attested"])
    for b in by_class.values():
        b["mean_cells"] = round(b["cells"] / b["lemmas"], 2)
    coverage = sorted((int(r["cells_attested"]) for r in cons), reverse=True)
    n = len(cons)
    med = coverage[n // 2] if n % 2 else (coverage[n // 2 - 1] + coverage[n // 2]) / 2
    top = sorted(cons, key=lambda r: -int(r["tokens"]))[:20]
    return {
        "source": "G2 asset sangram/data/declension_cell_coverage/lemma_cell_coverage.csv (H1048)",
        "consonant_classes": sorted(CONS_CLASSES),
        "n_lemmas": n,
        "n_tokens": sum(int(r["tokens"]) for r in cons),
        "cells_per_lemma": {"mean": round(sum(coverage) / n, 2), "median": med, "max": coverage[0]},
        "by_class": dict(sorted(by_class.items(), key=lambda kv: -kv[1]["lemmas"])),
        "top_lemmas": [{"lemma": r["lemma"], "gender": r["dom_gender"], "stem_final": r["stem_final"],
                        "tokens": int(r["tokens"]), "cells_attested": int(r["cells_attested"])}
                       for r in top],
    }, cons


def generated_paradigms():
    sys.path.insert(0, str(MWINFLECT / "nominals" / "pydecl"))
    sys.path.insert(0, str(GITHUB / "sanskrit-util" / "py"))
    import decline
    import sanskrit_util as su
    commit = subprocess.run(
        ["git", "-C", str(MWINFLECT), "rev-parse", "HEAD"],
        capture_output=True, text=True, encoding="utf-8").stdout.strip()
    out = {"generator": "MWinflect nominals/pydecl decline.py", "generator_commit": commit, "paradigms": {}}
    for key, clsname, slp, iast, gloss in REPRESENTATIVES:
        cls = getattr(decline, clsname)
        forms = cls(slp).table  # 24, row-major case × (Sing,Dual,Plur)
        cells = {}
        i = 0
        for c in CASES:
            for n in NUMBERS:
                cells[f"{c}.{n}"] = su.from_slp1(forms[i])
                i += 1
        out["paradigms"][key] = {"class": clsname, "stem_slp1": slp, "lemma": iast,
                                 "gloss_ru": gloss, "cells": cells}
    return out


def sample_by_lemmas(cur, lemmas):
    ph = ",".join("?" for _ in lemmas)
    ids = [r[0] for r in cur.execute(
        f"SELECT t.id FROM token t WHERE t.upos='NOUN' "
        f"AND t.feat_case IN ('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc') "
        f"AND t.feat_number IN ('Sing','Dual','Plur') AND t.lemma IN ({ph})", tuple(lemmas))]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    rows = []
    for tid in chosen:
        r = cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.lemma_id, "
            "t.feat_case, t.feat_gender, t.feat_number, x.name, c.ref, s.sent_counter "
            "FROM token t JOIN sentence s ON s.id=t.sentence_id "
            "JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone()
        rows.append(r)
    return rows


def main():
    import sqlite3
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--skip-checksum", action="store_true")
    args = ap.parse_args()
    db = Path(args.db)
    if not db.exists():
        print(f"ERROR: DCS master not found: {db}", file=sys.stderr)
        return 1
    if not G2_CSV.exists():
        print(f"ERROR: G2 asset not found: {G2_CSV} (build H1048 first)", file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr)
        return 1
    sha = "skipped" if args.skip_checksum else sha256_file(db)

    attested, cons_lemmas = read_g2_consonant_slice()
    # cap the sample lemma set for the IN() clause (SQLite ~999 var limit): use top-N by tokens
    top_lemmas = [r["lemma"] for r in sorted(cons_lemmas, key=lambda r: -int(r["tokens"]))[:900]]
    sample = sample_by_lemmas(cur, top_lemmas)
    gen = generated_paradigms()
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "lemma_id",
                    "case", "gender", "number", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)
    (OUT_DIR / "generated_paradigms.json").write_text(
        json.dumps(gen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {
        "study": "SG-MO-006 «Склонение: согласные основы» — consonant-stem declension (core W2 ①, content)",
        "toc_ref": "SG-MO-006",
        "kind": "content article (no kill-gate; method proven by P1–P5)",
        "method": "three-layer C5 §3: ATTESTED consumes the G2 asset (H1048); GENERATED = MWinflect; TRADITIONAL = Whitney ch. V §§383–465 (strong/middle/weak gradation)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "attested_layer_from_g2": attested,
        "generated_layer": {"generator": gen["generator"], "generator_commit": gen["generator_commit"],
                            "paradigms": list(gen["paradigms"].keys())},
        "traditional_layer": {"witness": "Whitney 1889 ch. V §§383–465 (consonant stems)"},
        "validation_sample": {"seed": SEED, "size": len(sample),
                              "frame": "top-900 consonant-stem lemmas by tokens; seeded random",
                              "file": "validation_sample.tsv"},
        "limits": {
            "EM3": "attested cells per consonant-stem lemma is almost always ≪ 24 (median from G2) — coverage a frequency artifact",
            "r_stems_excluded": "ṛ-stems (agent nouns pitṛ/kartṛ) are a separate class, excluded here",
            "gradation_not_in_features": "strong/middle/weak stem gradation is not a DCS feature; the generated layer supplies it, the corpus only attests surface forms",
            "stem_final_approx": "consonant class via G2 lemma-final tag (citation form ≠ stem, SG-MO-001 §6.1); a filter, not paradigmatic",
            "EM7": "homonyms keyed by lemma_id in G2",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"consonant-stem lemmas (G2): {attested['n_lemmas']:,} / {attested['n_tokens']:,} tokens", file=sys.stderr)
    print(f"by class: {[(k, v['lemmas']) for k, v in attested['by_class'].items()]}", file=sys.stderr)
    print(f"cells/lemma: mean {attested['cells_per_lemma']['mean']}, median {attested['cells_per_lemma']['median']}", file=sys.stderr)
    print(f"validation sample: {len(sample)} tokens (seed {SEED})", file=sys.stderr)
    print(f"generated paradigms: {list(gen['paradigms'].keys())}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
