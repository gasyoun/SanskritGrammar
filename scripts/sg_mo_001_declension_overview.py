#!/usr/bin/env python3
"""Sangram overview SG-MO-001 (Склонение: обзор) — declension frequency frame.

Descriptive corpus frame for the declension cluster (not a kill-gate pilot):
  (1) the case × number matrix over inflected DCS nouns — the domain's base
      frequency frame (registry query `POS=NOUN & Case=* & Number=*`);
  (2) the stem-type inventory — token distribution across lemma-final stem
      classes (-a / -ā / -ī,-ū / -i,-u / -ṛ / n- / t- / s- / r- / other-cons),
      which motivates and links the sub-articles SG-MO-002…011.

Every published number carries the pinned-snapshot provenance + denominator; a
few headline shares carry a Wilson 95% CI (C3 §4.4 / П1–П2). Read-only; refuses
without the provenance pin. Emits coverage_summary.json.
"""
import sqlite3
import sys
import json
import hashlib
import argparse
import math
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "declension-overview" / "data"

CASES = ["Nom", "Voc", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc"]
NUMBERS = ["Sing", "Dual", "Plur"]


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


def stem_class(lemma):
    """Approximate stem class by the lemma's final sound (IAST citation form)."""
    if not lemma:
        return "other"
    L = lemma
    if L.endswith("ā"):
        return "-ā"
    if L.endswith("ī"):
        return "-ī"
    if L.endswith("ū"):
        return "-ū"
    if L.endswith("ṛ"):
        return "-ṛ"
    if L.endswith("a"):
        return "-a"
    if L.endswith("i"):
        return "-i"
    if L.endswith("u"):
        return "-u"
    if L.endswith(("n",)):
        return "n-основы (-an/-in/-man)"
    if L.endswith(("t", "d")):
        return "t-основы (-ant/-mat/-vat)"
    if L.endswith("s"):
        return "s-основы (-as/-is/-us)"
    if L.endswith("r"):
        return "r-основы"
    return "прочие согласные"


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

    # Universe: inflected common nouns (exclude compound members Case=Cpd and NULL case)
    where = "t.upos='NOUN' AND t.feat_case IS NOT NULL AND t.feat_case!='Cpd'"
    total = cur.execute(f"SELECT COUNT(*) FROM token t WHERE {where}").fetchone()[0]

    # (1) case × number matrix
    matrix = {c: {n: 0 for n in NUMBERS} for c in CASES}
    other_case = Counter()
    for c, n, cnt in cur.execute(
        f"SELECT t.feat_case, t.feat_number, COUNT(*) FROM token t WHERE {where} "
        "GROUP BY t.feat_case, t.feat_number"
    ):
        if c in matrix and n in NUMBERS:
            matrix[c][n] = cnt
        else:
            other_case[f"{c}/{n}"] += cnt
    case_totals = {c: sum(matrix[c].values()) for c in CASES}
    number_totals = {n: sum(matrix[c][n] for c in CASES) for n in NUMBERS}

    # (2) stem-type inventory by lemma final (token-weighted, over the same universe)
    stem = Counter()
    for lemma, cnt in cur.execute(
        f"SELECT t.lemma, COUNT(*) FROM token t WHERE {where} GROUP BY t.lemma"
    ):
        stem[stem_class(lemma)] += cnt
    stem_share = {k: round(v / total, 4) for k, v in stem.most_common()}

    # a few headline shares with Wilson CI
    nom = case_totals["Nom"]; acc = case_totals["Acc"]; gen = case_totals["Gen"]
    sing = number_totals["Sing"]; dual = number_totals["Dual"]
    a_stem = stem.get("-a", 0)
    headlines = {
        "sing_share": {"k": sing, "n": total, "share": round(sing / total, 4), "ci95": wilson_ci(sing, total)},
        "dual_share": {"k": dual, "n": total, "share": round(dual / total, 4), "ci95": wilson_ci(dual, total)},
        "nom_share": {"k": nom, "n": total, "share": round(nom / total, 4), "ci95": wilson_ci(nom, total)},
        "a_stem_share": {"k": a_stem, "n": total, "share": round(a_stem / total, 4), "ci95": wilson_ci(a_stem, total)},
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "study": "Sangram SG-MO-001 (Склонение: обзор) — частотная рамка домена склонения",
        "toc_ref": "SG-MO-001",
        "kind": "overview (no kill-gate)",
        "snapshot": {
            "master": str(db).replace(str(GITHUB), "<GitHub>"),
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "пин 04e0778 осиротел после перезаписи истории dcs-conllu; привязка — provenance-таблица + SHA-256 + тег c3-pin-04e0778-content",
        },
        "universe_where": where,
        "denominator_inflected_noun_tokens": total,
        "case_number_matrix": matrix,
        "case_totals": case_totals,
        "number_totals": number_totals,
        "other_case_number": dict(other_case),
        "stem_type_tokens": dict(stem.most_common()),
        "stem_type_share": stem_share,
        "stem_note": "приближение по финали леммы (цитатная форма ≠ основа); согласные подтипы — по конечному звуку",
        "headline_shares_ci95": headlines,
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    con.close()

    print(f"denominator (inflected noun tokens): {total:,}", file=sys.stderr)
    print(f"Sing/Dual/Plur: {number_totals}", file=sys.stderr)
    print(f"top stem types: {stem.most_common(6)}", file=sys.stderr)
    print(f"Wrote {OUT_DIR/'coverage_summary.json'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
