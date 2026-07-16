#!/usr/bin/env python3
"""SG-WF-001 (Строение слова: корень, основа, аффикс) — word-structure frame.

Descriptive corpus frame for the word-formation «Основания» cluster (overview,
no kill-gate). Sanskrit word-structure (root -> stem -> affix) is a DERIVATIONAL
model DCS does not natively segment morpheme-by-morpheme; to keep the frame REAL
(not a textbook schema) it is anchored to three natively-measurable layers:

  A. Token-level structural composition — a priority partition of every token by
     how it is built: compound member (Case=Cpd) / non-finite deverbal
     (VerbForm in Part,Conv,Gdv,Inf = primary kṛt derivation) / finite verb
     (root + conjugational ending) / other nominal (NOUN/ADJ — primary root-noun
     + kṛt + taddhita, NOT natively separable, honest limit) / closed-class /
     punctuation. Exhaustive, non-overlapping.
  B. Root inventory — distinct finite-verb lemmas attested + token concentration
     (top-N share = productivity), against the WhitneyRoots gaṇa inventory
     (root_class.csv, the traditional root count) — see the gaṇa-join note
     (WhitneyRoots owns the traditional class, not DCS lemma.grammar).
  C. Stem-formation glimpse — feat_formation (root/them/red/s/is/peri/sa/sis),
     the ONE native marker of how a verb stem is built from the root; sparse
     (~1.7% of VERB tokens) so reported as a limited native window, not a headline.

The nominal primary/kṛt/taddhita split is NOT attempted by surface lemma-ending:
P5 (SG-WF-003) measured that surface kṛt match is ~59% false — carried as a limit.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators + Wilson CI on a headline share. Read-only. Emits coverage_summary.json.
"""
import sqlite3
import sys
import json
import csv
import hashlib
import argparse
import math
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
ROOT_CLASS = GITHUB / "WhitneyRoots" / "crosswalk" / "root_class.csv"
OUT_DIR = ROOT / "sangram" / "articles" / "word-structure-overview" / "data"

# Priority partition (first matching bucket wins) — exhaustive, non-overlapping.
PARTITION_SQL = """
SELECT CASE
  WHEN feat_case='Cpd' THEN 'compound_member'
  WHEN feat_verbform IN ('Part','Conv','Gdv','Inf') THEN 'nonfinite_deverbal'
  WHEN upos='VERB' THEN 'finite_verb'
  WHEN upos IN ('NOUN','ADJ') THEN 'nominal_mixed'
  WHEN upos IN ('PRON','PART','ADV','CONJ','SCONJ','ADP','NUM','INTJ') THEN 'closed_class'
  ELSE 'other_punct'
END AS bucket, COUNT(*) FROM token GROUP BY bucket
"""


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

    total = cur.execute("SELECT COUNT(*) FROM token").fetchone()[0]

    # --- Frame A: token-level structural composition ---
    partition = {b: c for b, c in cur.execute(PARTITION_SQL)}
    assert sum(partition.values()) == total, "partition not exhaustive"
    order = ["compound_member", "nonfinite_deverbal", "finite_verb",
             "nominal_mixed", "closed_class", "other_punct"]
    frame_a = {b: {"tokens": partition.get(b, 0),
                   "share": round(partition.get(b, 0) / total, 4)} for b in order}

    # --- Frame B: root inventory (attested finite-verb lemmas + concentration) ---
    fin_where = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
                 "AND feat_person IS NOT NULL")
    fin_total = cur.execute(f"SELECT COUNT(*) FROM token WHERE {fin_where}").fetchone()[0]
    distinct_fin_lemmas = cur.execute(
        f"SELECT COUNT(DISTINCT lemma) FROM token WHERE {fin_where} AND lemma IS NOT NULL"
    ).fetchone()[0]
    top = cur.execute(
        f"SELECT lemma, COUNT(*) c FROM token WHERE {fin_where} AND lemma IS NOT NULL "
        f"GROUP BY lemma ORDER BY c DESC LIMIT 100"
    ).fetchall()
    cum = 0
    conc = {}
    for i, (lem, c) in enumerate(top, 1):
        cum += c
        if i in (10, 50, 100):
            conc[f"top{i}_share_of_finite"] = round(cum / fin_total, 4)
    top10 = [{"lemma": lem, "tokens": c, "share": round(c / fin_total, 4)} for lem, c in top[:10]]

    # WhitneyRoots gaṇa inventory (traditional root count) — the traditional layer
    gana_dist = {}
    n_roots = 0
    if ROOT_CLASS.exists():
        rows = list(csv.DictReader(open(ROOT_CLASS, encoding="utf-8")))
        n_roots = len(rows)
        for r in rows:
            g = (r.get("gana") or "?").strip()
            gana_dist[g] = gana_dist.get(g, 0) + 1
        gana_dist = dict(sorted(gana_dist.items(), key=lambda kv: -kv[1]))

    # --- Frame C: stem-formation glimpse (feat_formation over VERB) ---
    formation = {}
    for v, c in cur.execute(
        "SELECT feat_formation, COUNT(*) FROM token WHERE upos='VERB' "
        "GROUP BY feat_formation ORDER BY COUNT(*) DESC"
    ):
        if v is not None:
            formation[v] = c
    formation_marked = sum(formation.values())
    verb_total = cur.execute("SELECT COUNT(*) FROM token WHERE upos='VERB'").fetchone()[0]

    con.close()

    dev = frame_a["nonfinite_deverbal"]["tokens"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "study": "Sangram SG-WF-001 (Строение слова: корень, основа, аффикс) — структурная рамка слова",
        "toc_ref": "SG-WF-001",
        "kind": "overview (no kill-gate)",
        "method": ("три нативно-измеримых слоя: A) приоритетное разбиение всех токенов по типу строения; "
                   "B) инвентарь корней (аттестованные финитные леммы + концентрация vs гана-инвентарь WhitneyRoots); "
                   "C) окно словообразования основы (feat_formation). Разбор нарицательных на первичные/kṛt/taddhita "
                   "по поверхностной финали НЕ делается — P5 показал ~59% ложных (предел, перенесён)"),
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned after dcs-conllu history rewrite; binding is provenance table + SHA-256",
        },
        "denominator_all_tokens": total,
        "frame_a_structural_partition": frame_a,
        "frame_a_note": "priority partition, first match wins; exhaustive + non-overlapping (sum == denominator)",
        "nonfinite_deverbal_share_ci95": {"k": dev, "n": total, "ci95": wilson_ci(dev, total)},
        "frame_b_root_inventory": {
            "finite_verb_tokens": fin_total,
            "distinct_finite_verb_lemmas_attested": distinct_fin_lemmas,
            "concentration": conc,
            "top10_lemmas": top10,
            "whitneyroots_gana_inventory_roots": n_roots,
            "whitneyroots_gana_distribution": gana_dist,
            "gana_join_note": "traditional gaṇa lives in WhitneyRoots root_class.csv, NOT DCS lemma.grammar (which is gender/POS); the DCS present-class code is a DCS-internal index, not the gaṇa",
        },
        "frame_c_stem_formation": {
            "verb_tokens": verb_total,
            "formation_marked": formation_marked,
            "formation_marked_share_of_verb": round(formation_marked / verb_total, 4),
            "distribution": formation,
            "note": "feat_formation = how the (aorist/perfect/present) stem is built from the root — the only native stem-formation marker; sparse (most VERB tokens NULL)",
        },
        "limits": {
            "nominal_split": "primary root-noun vs kṛt vs taddhita NOT natively separable; surface lemma-ending match is ~59% false (P5/SG-WF-003)",
            "no_morpheme_segmentation": "DCS gives lemma + features, not a root+affix segmentation per token",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"denominator (all tokens): {total:,}", file=sys.stderr)
    print(f"Frame A partition:", file=sys.stderr)
    for b in order:
        print(f"  {b}: {frame_a[b]['tokens']:,} ({frame_a[b]['share']*100:.1f}%)", file=sys.stderr)
    print(f"Frame B: {distinct_fin_lemmas:,} distinct finite-verb lemmas; conc={conc}", file=sys.stderr)
    print(f"  WhitneyRoots gaṇa inventory: {n_roots} roots; dist={gana_dist}", file=sys.stderr)
    print(f"Frame C: feat_formation marked {formation_marked:,} of {verb_total:,} VERB; {formation}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
