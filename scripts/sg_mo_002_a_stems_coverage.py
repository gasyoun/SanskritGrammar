#!/usr/bin/env python3
"""SG-MO-002 pilot P1: a-stem case x number cell coverage (attested / generated / traditional).

Measures the share of ATTESTED cells of the 8 case x 3 number paradigm matrix
for thematic a-stem nouns (masc + neut) in the pinned DCS snapshot, against the
GENERATED full paradigm (MWinflect nominals/pydecl) and the TRADITIONAL one
(Whitney 1889 ch. V), per the C5 morphology programme S 3 / S 5.3 and the C3
corpus-evidence cycle (query -> sample -> validation -> claim -> examples).

Corpus surface: the VisualDCS SQLite master (consume, don't rebuild — C3 S 2.1).
Its `provenance` table pins the dcs-conllu source commit; this script refuses
to run if the pin is missing, and records master-file SHA-256 unless
--skip-checksum.

Universe (recorded verbatim in the output JSON):
  token.upos = 'NOUN'
  AND token.feat_gender IN ('Masc' | 'Neut')     -- per-gender slices
  AND token.feat_case IN (8 real cases)          -- 'Cpd' + NULL excluded
  AND token.feat_number IN ('Sing','Dual','Plur')
  AND token.lemma LIKE '%a'                      -- IAST: plain 'a', not 'ā'
  AND lemma.grammar in the per-gender dictionary whitelist
The dictionary join (lemma_id -> lemma.grammar) implements the C2 query note
for SG-MO-002: stem type via lemma ending + dictionary gender; homonyms are
keyed by lemma_id (EM7).

Validation sample: SAMPLE_SIZE tokens drawn by random.Random(SEED).sample from
the combined universe (C3 P3: recorded seed, never "first N"), with sentence
context + locus for manual adjudication. Kill-gate (C5 S 7 P1): false-positive
rate > 10 % drops the cell-coverage claim (C3 P4).

Usage:
  python scripts/sg_mo_002_a_stems_coverage.py [--db PATH] [--skip-checksum]
Outputs into sangram/articles/a-stems/data/ .
"""
import argparse
import csv
import hashlib
import json
import random
import sqlite3
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "a-stems" / "data"
MWINFLECT = GITHUB / "MWinflect"

CASES = ["Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc", "Voc"]
NUMBERS = ["Sing", "Dual", "Plur"]
N_CELLS = len(CASES) * len(NUMBERS)  # 24

# Dictionary-gender whitelists (DCS dictionary.csv grammar codes seen in the
# lemma table). 'mn'/'mf' lemmas contribute to a slice only through tokens of
# that slice's feat_gender.
GRAMMAR_MASC = ("m", "mn", "mf")
GRAMMAR_NEUT = ("n", "mn", "nf", "fn")

SEED = 20260715
SAMPLE_SIZE = 60  # C3 S 4.2 floor is 50; 60 keeps the estimate above the floor
                  # even if a few sampled tokens prove unadjudicable.

UNIVERSE_WHERE = (
    "t.upos = 'NOUN' "
    "AND t.feat_gender = ? "
    "AND t.feat_case IN ('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc') "
    "AND t.feat_number IN ('Sing','Dual','Plur') "
    "AND t.lemma LIKE '%a' "
    "AND l.grammar IN ({marks})"
)

CELL_SQL = (
    "SELECT t.lemma_id, t.lemma, t.feat_case, t.feat_number, COUNT(*) AS n "
    "FROM token t JOIN lemma l ON l.lemma_id = t.lemma_id "
    "WHERE " + UNIVERSE_WHERE + " "
    "GROUP BY t.lemma_id, t.feat_case, t.feat_number"
)

IDS_SQL = (
    "SELECT t.id FROM token t JOIN lemma l ON l.lemma_id = t.lemma_id "
    "WHERE " + UNIVERSE_WHERE
)

SAMPLE_DETAIL_SQL = (
    "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.lemma_id, l.grammar, "
    "t.feat_case, t.feat_gender, t.feat_number, s.text_sandhied, "
    "c.ref AS chapter_ref, x.name AS text_name, s.sent_counter, s.sent_subcounter "
    "FROM token t "
    "JOIN lemma l ON l.lemma_id = t.lemma_id "
    "JOIN sentence s ON s.id = t.sentence_id "
    "JOIN chapter c ON c.chapter_id = s.chapter_id "
    "JOIN text x ON x.text_id = c.text_id "
    "WHERE t.id = ?"
)


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


def gender_slice(cur, gender: str, marks: tuple) -> dict:
    ph = ",".join("?" for _ in marks)
    sql = CELL_SQL.format(marks=ph)
    rows = cur.execute(sql, (gender, *marks)).fetchall()
    lemmas = {}
    for lemma_id, lemma, case, num, n in rows:
        rec = lemmas.setdefault(lemma_id, {"lemma": lemma, "cells": {}, "tokens": 0})
        rec["cells"][f"{case}.{num}"] = n
        rec["tokens"] += n

    n_lemmas = len(lemmas)
    n_tokens = sum(r["tokens"] for r in lemmas.values())
    coverage = sorted((len(r["cells"]) for r in lemmas.values()), reverse=True)
    total_cells_attested = sum(coverage)

    # class-level: how many lemmas attest each of the 24 cells
    cell_lemma_counts = {f"{c}.{n}": 0 for c in CASES for n in NUMBERS}
    cell_token_counts = {f"{c}.{n}": 0 for c in CASES for n in NUMBERS}
    for r in lemmas.values():
        for cell, n in r["cells"].items():
            cell_lemma_counts[cell] += 1
            cell_token_counts[cell] += n

    # coverage by frequency band
    bands = {}
    for r in lemmas.values():
        b = bands.setdefault(freq_band(r["tokens"]), {"lemmas": 0, "cells": 0})
        b["lemmas"] += 1
        b["cells"] += len(r["cells"])
    for b in bands.values():
        b["mean_cells"] = round(b["cells"] / b["lemmas"], 2)

    def pct_at_least(k):
        return round(100 * sum(1 for c in coverage if c >= k) / n_lemmas, 2)

    med = coverage[n_lemmas // 2] if n_lemmas % 2 else (
        (coverage[n_lemmas // 2 - 1] + coverage[n_lemmas // 2]) / 2)

    top = sorted(lemmas.items(), key=lambda kv: -kv[1]["tokens"])[:100]

    return {
        "n_lemmas": n_lemmas,
        "n_tokens": n_tokens,
        "cells_per_lemma": {
            "mean": round(total_cells_attested / n_lemmas, 2),
            "median": med,
            "max": coverage[0],
            "pct_lemmas_full_24": pct_at_least(24),
            "pct_lemmas_ge_12": pct_at_least(12),
            "pct_lemmas_1_cell": round(
                100 * sum(1 for c in coverage if c == 1) / n_lemmas, 2),
        },
        "lemma_cell_space_attested_pct": round(
            100 * total_cells_attested / (N_CELLS * n_lemmas), 2),
        "cell_lemma_counts": cell_lemma_counts,
        "cell_token_counts": cell_token_counts,
        "freq_bands": bands,
        "top_lemmas": [
            {"lemma_id": lid, "lemma": r["lemma"], "tokens": r["tokens"],
             "cells_attested": len(r["cells"])}
            for lid, r in top
        ],
        "_lemmas": lemmas,  # stripped before JSON dump
    }


def showcase(slice_data: dict, lemma: str) -> dict:
    for lid, r in slice_data["_lemmas"].items():
        if r["lemma"] == lemma:
            return {"lemma_id": lid, "lemma": lemma, "tokens": r["tokens"],
                    "cells_attested": len(r["cells"]),
                    "cells": {f"{c}.{n}": r["cells"].get(f"{c}.{n}", 0)
                              for c in CASES for n in NUMBERS}}
    return {"lemma": lemma, "error": "not in universe"}


def generated_paradigms() -> dict:
    sys.path.insert(0, str(MWINFLECT / "nominals" / "pydecl"))
    sys.path.insert(0, str(GITHUB / "sanskrit-util" / "py"))
    import decline  # noqa: E402
    import sanskrit_util as su  # noqa: E402

    def table(cls, key_slp1):
        forms = cls(key_slp1).table  # 24 forms, row-major case x (Sing,Dual,Plur)
        out = {}
        i = 0
        for c in CASES:
            for n in NUMBERS:
                slp = forms[i]
                out[f"{c}.{n}"] = {"slp1": slp, "iast": su.from_slp1(slp)}
                i += 1
        return out

    commit = subprocess.run(
        ["git", "-C", str(MWINFLECT), "rev-parse", "HEAD"],
        capture_output=True, text=True, encoding="utf-8").stdout.strip()
    return {
        "generator": "MWinflect nominals/pydecl decline.py (Decline_m_a / Decline_n_a)",
        "generator_commit": commit,
        "cells": N_CELLS,
        "deva_masc": table(decline.Decline_m_a, "deva"),
        "phala_neut": table(decline.Decline_n_a, "Pala"),
    }


def draw_validation_sample(cur) -> list:
    ids = []
    for gender, marks in (("Masc", GRAMMAR_MASC), ("Neut", GRAMMAR_NEUT)):
        ph = ",".join("?" for _ in marks)
        ids.extend(r[0] for r in cur.execute(
            IDS_SQL.format(marks=ph), (gender, *marks)).fetchall())
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), SAMPLE_SIZE)
    rows = []
    for tid in chosen:
        r = cur.execute(SAMPLE_DETAIL_SQL, (tid,)).fetchone()
        rows.append(r)
    return rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--skip-checksum", action="store_true")
    args = ap.parse_args()

    db = Path(args.db)
    if not db.exists():
        print(f"ERROR: DCS master not found: {db}")
        return 1
    con = sqlite3.connect(db)
    cur = con.cursor()

    prov = dict(cur.execute("SELECT * FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 S 2.1)")
        return 1

    sha256 = None
    if not args.skip_checksum:
        h = hashlib.sha256()
        with open(db, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 22), b""):
                h.update(chunk)
        sha256 = h.hexdigest()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    masc = gender_slice(cur, "Masc", GRAMMAR_MASC)
    neut = gender_slice(cur, "Neut", GRAMMAR_NEUT)
    show = {"deva_masc": showcase(masc, "deva"), "phala_neut": showcase(neut, "phala")}

    # per-cell CSVs (class level)
    for name, sl in (("masc", masc), ("neut", neut)):
        with open(OUT_DIR / f"cell_coverage_{name}.csv", "w", newline="",
                  encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["cell", "lemmas_attesting", "tokens"])
            for c in CASES:
                for n in NUMBERS:
                    cell = f"{c}.{n}"
                    w.writerow([cell, sl["cell_lemma_counts"][cell],
                                sl["cell_token_counts"][cell]])

    with open(OUT_DIR / "lemma_coverage_top.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["gender", "lemma_id", "lemma", "tokens", "cells_attested"])
        for g, sl in (("Masc", masc), ("Neut", neut)):
            for r in sl["top_lemmas"]:
                w.writerow([g, r["lemma_id"], r["lemma"], r["tokens"],
                            r["cells_attested"]])

    sample = draw_validation_sample(cur)
    with open(OUT_DIR / "validation_sample.tsv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "lemma_id",
                    "dict_grammar", "case", "gender", "number",
                    "sentence", "text", "chapter_ref", "sent_counter",
                    "sent_subcounter"])
        for r in sample:
            w.writerow(r)

    gen = generated_paradigms()
    (OUT_DIR / "generated_paradigm_deva_phala.json").write_text(
        json.dumps(gen, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for sl in (masc, neut):
        sl.pop("_lemmas")

    summary = {
        "study": "SG-MO-002 pilot P1: a-stem case x number cell coverage",
        "method": "C5 S 3 (attested/generated/traditional) via C3 cycle",
        "snapshot": {
            "master": str(db),
            "sha256": sha256,
            "provenance": prov,
        },
        "universe_where_sql": UNIVERSE_WHERE,
        "cell_sql": CELL_SQL,
        "grammar_whitelists": {"Masc": GRAMMAR_MASC, "Neut": GRAMMAR_NEUT},
        "matrix_cells": N_CELLS,
        "validation_sample": {"seed": SEED, "size": SAMPLE_SIZE,
                              "file": "validation_sample.tsv"},
        "generated_layer": {"generator": gen["generator"],
                            "generator_commit": gen["generator_commit"],
                            "cells": 24},
        "traditional_layer": {
            "witness": "Whitney 1889, ch. V (a-stems)",
            "cells": 24,
        },
        "masc": masc,
        "neut": neut,
        "showcase": show,
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")

    print(f"masc: {masc['n_lemmas']} lemmas / {masc['n_tokens']} tokens; "
          f"mean cells {masc['cells_per_lemma']['mean']}/24, "
          f"median {masc['cells_per_lemma']['median']}, "
          f"full-24 {masc['cells_per_lemma']['pct_lemmas_full_24']}%")
    print(f"neut: {neut['n_lemmas']} lemmas / {neut['n_tokens']} tokens; "
          f"mean cells {neut['cells_per_lemma']['mean']}/24, "
          f"median {neut['cells_per_lemma']['median']}, "
          f"full-24 {neut['cells_per_lemma']['pct_lemmas_full_24']}%")
    print(f"showcase deva: {show['deva_masc'].get('cells_attested')}/24, "
          f"phala: {show['phala_neut'].get('cells_attested')}/24")
    print(f"wrote {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
