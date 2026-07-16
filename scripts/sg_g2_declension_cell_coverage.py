#!/usr/bin/env python3
"""Sangram G2 derived asset — attested declension cells per lemma (whole corpus).

Materializes the "attested cells per lemma" table the W2-core checkpoint (§ 5, G2)
recommends building at the start of the core: for EVERY noun lemma, which of the
8 case × 3 number = 24 paradigm cells actually occur in the pinned DCS snapshot,
with token counts. This is the general (all-stem-type, all-gender) version of the
a-stem-only P1 coverage (SG-MO-002); it is a cross-article layer that strengthens
the declension articles SG-MO-001/002/006/010.

It also measures evidence-limit EM3 (overgeneration) at corpus scale: the pilot P1
found median 1 attested cell per a-stem lemma; this asset reports that distribution
over the whole noun inventory, per stem type, gender, and frequency band.

Universe (recorded verbatim in the output JSON), same shape as P1 minus the a-stem
and gender restriction:
  token.upos = 'NOUN'
  AND token.feat_case IN (8 real cases)          -- 'Cpd' + NULL excluded
  AND token.feat_number IN ('Sing','Dual','Plur')
  AND token.lemma IS NOT NULL
Homonyms are keyed by lemma_id (EM7). Stem type is a lemma-final approximation
(the SG-MO-001 §6.1 caveat: citation form ≠ stem) — a convenience tag for filtering,
NOT a paradigmatic classification; each article does its own precise stem-typing.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators. Read-only. Emits lemma_cell_coverage.csv + coverage_summary.json + README.
"""
import argparse
import csv
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "data" / "declension_cell_coverage"

CASES = ["Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc", "Voc"]
NUMBERS = ["Sing", "Dual", "Plur"]
CELLS = [f"{c}.{n}" for c in CASES for n in NUMBERS]  # 24, row-major case × number
N_CELLS = len(CELLS)

UNIVERSE_WHERE = (
    "t.upos = 'NOUN' "
    "AND t.feat_case IN ('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc') "
    "AND t.feat_number IN ('Sing','Dual','Plur') "
    "AND t.lemma IS NOT NULL"
)

CELL_SQL = (
    "SELECT t.lemma_id, t.lemma, t.feat_gender, t.feat_case, t.feat_number, COUNT(*) AS n "
    "FROM token t WHERE " + UNIVERSE_WHERE + " "
    "GROUP BY t.lemma_id, t.feat_case, t.feat_number, t.feat_gender"
)

# Lemma-final stem tag (IAST). Order matters: test 2-char endings before 1-char.
# Convenience only — the SG-MO-001 §6.1 caveat holds (citation form ≠ stem).
STEM_TAGS = [
    ("ā", "aa"), ("ī", "ii"), ("ū", "uu"), ("ṛ", "r_vocalic"),
    ("i", "i"), ("u", "u"), ("a", "a"),
    ("an", "an"), ("in", "in"), ("as", "as"), ("is", "is"), ("us", "us"),
]


def stem_final(lemma: str) -> str:
    for suf, tag in STEM_TAGS:
        if lemma.endswith(suf):
            return tag
    return "other_consonant"


def freq_band(n: int) -> str:
    if n == 1:
        return "1"
    if n < 10:
        return "2-9"
    if n < 100:
        return "10-99"
    if n < 1000:
        return "100-999"
    return "1000+"


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def median(sorted_desc):
    n = len(sorted_desc)
    if n == 0:
        return 0
    return sorted_desc[n // 2] if n % 2 else (
        (sorted_desc[n // 2 - 1] + sorted_desc[n // 2]) / 2)


def dist_block(lemmas):
    """Aggregate cells-per-lemma stats over a dict lemma_id -> record."""
    n_lemmas = len(lemmas)
    if n_lemmas == 0:
        return {"n_lemmas": 0}
    coverage = sorted((len(r["cells"]) for r in lemmas.values()), reverse=True)
    total_cells = sum(coverage)
    n_tokens = sum(r["tokens"] for r in lemmas.values())

    def pct_at_least(k):
        return round(100 * sum(1 for c in coverage if c >= k) / n_lemmas, 2)

    return {
        "n_lemmas": n_lemmas,
        "n_tokens": n_tokens,
        "cells_per_lemma": {
            "mean": round(total_cells / n_lemmas, 2),
            "median": median(coverage),
            "max": coverage[0],
            "pct_lemmas_full_24": pct_at_least(24),
            "pct_lemmas_ge_12": pct_at_least(12),
            "pct_lemmas_ge_6": pct_at_least(6),
            "pct_lemmas_1_cell": round(
                100 * sum(1 for c in coverage if c == 1) / n_lemmas, 2),
        },
        "lemma_cell_space_attested_pct": round(
            100 * total_cells / (N_CELLS * n_lemmas), 2),
    }


def main() -> int:
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

    # Build per-lemma coverage. A lemma_id can carry >1 gender (mn/mf); track the
    # dominant gender + gender set, but the cell coverage is over the lemma_id.
    lemmas = {}
    for lemma_id, lemma, gender, case, num, n in cur.execute(CELL_SQL):
        rec = lemmas.setdefault(lemma_id, {
            "lemma": lemma, "cells": {}, "tokens": 0, "gender_tokens": {}})
        cell = f"{case}.{num}"
        rec["cells"][cell] = rec["cells"].get(cell, 0) + n
        rec["tokens"] += n
        g = gender or "?"
        rec["gender_tokens"][g] = rec["gender_tokens"].get(g, 0) + n
    con.close()

    total_lemmas = len(lemmas)
    total_tokens = sum(r["tokens"] for r in lemmas.values())

    # class-level: how many lemmas attest each of the 24 cells + token counts
    cell_lemma_counts = {c: 0 for c in CELLS}
    cell_token_counts = {c: 0 for c in CELLS}
    for r in lemmas.values():
        for cell, n in r["cells"].items():
            cell_lemma_counts[cell] += 1
            cell_token_counts[cell] += n

    # breakdowns
    by_gender = {}
    by_stem = {}
    by_band = {}
    for lid, r in lemmas.items():
        dom_g = max(r["gender_tokens"], key=r["gender_tokens"].get)
        st = stem_final(r["lemma"])
        r["dom_gender"] = dom_g
        r["stem_final"] = st
        by_gender.setdefault(dom_g, {})[lid] = r
        by_stem.setdefault(st, {})[lid] = r
        by_band.setdefault(freq_band(r["tokens"]), {})[lid] = r

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # --- the materialized per-lemma asset (CSV) ---
    with open(OUT_DIR / "lemma_cell_coverage.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lemma_id", "lemma", "dom_gender", "stem_final",
                    "tokens", "cells_attested", "cells_bits24"])
        for lid, r in sorted(lemmas.items(), key=lambda kv: -kv[1]["tokens"]):
            bits = "".join("1" if c in r["cells"] else "0" for c in CELLS)
            w.writerow([lid, r["lemma"], r["dom_gender"], r["stem_final"],
                        r["tokens"], len(r["cells"]), bits])

    summary = {
        "asset": "Sangram G2 — attested declension cells per lemma (derived data asset)",
        "checkpoint_ref": "W2-core opening checkpoint §5 G2 (materialized attested-cells-per-lemma table)",
        "consumers": ["SG-MO-001", "SG-MO-002", "SG-MO-006", "SG-MO-010"],
        "method": "per lemma_id, the set of attested (case.number) cells of the 24-cell matrix over the pinned DCS snapshot; general (all stem types, all genders) version of the a-stem-only P1 coverage",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned after dcs-conllu history rewrite; binding is provenance table + SHA-256",
        },
        "universe_where": UNIVERSE_WHERE,
        "matrix_cells": N_CELLS,
        "cells_order": CELLS,
        "denominators": {"noun_lemmas": total_lemmas, "case_number_tokens": total_tokens},
        "overall": dist_block(lemmas),
        "cell_lemma_counts": cell_lemma_counts,
        "cell_token_counts": cell_token_counts,
        "by_dominant_gender": {g: dist_block(d) for g, d in sorted(by_gender.items())},
        "by_stem_final_approx": {s: dist_block(d) for s, d in sorted(
            by_stem.items(), key=lambda kv: -len(kv[1]))},
        "by_frequency_band": {b: dist_block(d) for b, d in sorted(by_band.items())},
        "limits": {
            "EM3": "overgeneration — attested cells per lemma is almost always << 24 (P1 median 1); this asset quantifies it corpus-wide",
            "stem_final": "stem_final is a lemma-ending approximation (citation form ≠ stem, SG-MO-001 §6.1), a convenience tag, not a paradigmatic classification",
            "EM7": "homonyms keyed by lemma_id; a citation string with two lemma_ids is two rows",
            "pin": "orphaned pin bound by provenance table + SHA-256 + tag c3-pin-04e0778-content (as pilots P1–P5)",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    ov = summary["overall"]["cells_per_lemma"]
    print(f"noun lemmas: {total_lemmas:,}; case×number tokens: {total_tokens:,}", file=sys.stderr)
    print(f"cells/lemma: mean {ov['mean']}, median {ov['median']}, max {ov['max']}, "
          f"full-24 {ov['pct_lemmas_full_24']}%, 1-cell {ov['pct_lemmas_1_cell']}%", file=sys.stderr)
    print(f"lemma×cell space attested: {summary['overall']['lemma_cell_space_attested_pct']}%", file=sys.stderr)
    print(f"wrote {OUT_DIR}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
