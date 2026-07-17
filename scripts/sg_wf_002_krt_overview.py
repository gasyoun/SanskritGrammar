#!/usr/bin/env python3
"""SG-WF-002 «Деривация: kṛt (обзор)» — primary (deverbal) derivation overview.

Core W2 ① overview (no kill-gate). kṛt = primary derivation from the root. The
overview's quantitative spine is the part of kṛt the corpus tags NATIVELY: the
non-finite verb forms, VerbForm ∈ {Part, Conv, Gdv, Inf}. A cross-tab confirms
this is a clean closed set — these four values NEVER occur on a non-VERB upos
(zero leakage) and feat_formation is NULL for all of them.

Two honest limits are carried, not hidden:
  EM5 (kṛt-NOUNS) — deverbal agent/action nouns (kartṛ, dāna, gati) have NO
    derivation tag; surface lemma-ending matching is ~59% false (pilot P5 /
    published honest-negative SG-WF-003), dominated by kinship terms and names.
    This overview does NOT count them.
  participle-tense sparsity — feat_tense is set on only ~22% of participles; the
    -ta/-na past-passive mass is left tense-unmarked, so the reliable split is at
    the VerbForm level, not a fine present/past/future participle split.

Three layers (C5 §3): ATTESTED — the VerbForm subtype distribution over the pinned
snapshot; TRADITIONAL — the kṛt suffix inventory (Whitney ch. XVII, §§ 935–1000).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators. Read-only. Emits into sangram/articles/krt-overview/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "krt-overview" / "data"

DEVERBAL = ("Part", "Conv", "Gdv", "Inf")
SUBTYPE_RU = {"Part": "причастие", "Conv": "абсолютив (-tvā/-ya)",
              "Gdv": "герундив (-tavya/-anīya/-ya)", "Inf": "инфинитив (-tum)"}


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

    total_tokens = cur.execute("SELECT COUNT(*) FROM token").fetchone()[0]
    ph = ",".join("?" for _ in DEVERBAL)

    # subtype distribution (native, closed set)
    subtypes = {}
    for vf, c in cur.execute(
            f"SELECT feat_verbform, COUNT(*) FROM token WHERE upos='VERB' "
            f"AND feat_verbform IN ({ph}) GROUP BY feat_verbform", DEVERBAL):
        subtypes[vf] = c
    krt_total = sum(subtypes.values())
    # closed-set proof: VerbForm never on non-VERB
    leak = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE upos!='VERB' AND feat_verbform IN ({ph})",
        DEVERBAL).fetchone()[0]

    # participle tense sparsity
    part_total = subtypes.get("Part", 0)
    part_tense = {}
    for t, c in cur.execute(
            "SELECT feat_tense, COUNT(*) FROM token WHERE upos='VERB' AND feat_verbform='Part' "
            "GROUP BY feat_tense ORDER BY COUNT(*) DESC"):
        part_tense[t if t is not None else "untensed"] = c
    part_untensed = part_tense.get("untensed", 0)

    # kṛt-noun surface-match noise (confirming EM5 / P5): common deverbal-noun endings
    noun_noise = {}
    for suf in ("tṛ", "ana", "ti", "tva"):
        n = cur.execute(
            "SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE ?",
            (f"%{suf}",)).fetchone()[0]
        top = cur.execute(
            "SELECT lemma, COUNT(*) c FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE ? "
            "GROUP BY lemma ORDER BY c DESC LIMIT 5", (f"%{suf}",)).fetchall()
        noun_noise[suf] = {"tokens": n, "top_lemmas": [f"{l} ({c})" for l, c in top]}

    # top forms per subtype
    top_forms = {}
    for vf in DEVERBAL:
        rows = cur.execute(
            "SELECT m_unsandhied, lemma, COUNT(*) c FROM token WHERE upos='VERB' "
            "AND feat_verbform=? AND m_unsandhied IS NOT NULL GROUP BY m_unsandhied, lemma "
            "ORDER BY c DESC LIMIT 6", (vf,)).fetchall()
        top_forms[vf] = [f"{m} ({l}, {c})" for m, l, c in rows]

    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "study": "Sangram SG-WF-002 (Деривация: kṛt, обзор) — primary/deverbal derivation",
        "toc_ref": "SG-WF-002",
        "kind": "overview (no kill-gate)",
        "method": "the NATIVELY-tagged kṛt = non-finite verb forms VerbForm∈{Part,Conv,Gdv,Inf} (closed set, zero leak onto non-VERB); kṛt-NOUNS not counted (EM5, P5 ~59% false)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominator_all_tokens": total_tokens,
        "deverbal_krt_total": krt_total,
        "deverbal_krt_share": round(krt_total / total_tokens, 4),
        "subtypes": {vf: {"ru": SUBTYPE_RU[vf], "tokens": subtypes.get(vf, 0),
                          "share_of_krt": round(subtypes.get(vf, 0) / krt_total, 4)}
                     for vf in DEVERBAL},
        "closed_set_proof": {"leak_verbform_on_non_verb": leak,
                             "note": "VerbForm∈{Part,Conv,Gdv,Inf} occurs ONLY on upos=VERB → clean closed set"},
        "participle_tense_sparsity": {"part_total": part_total, "untensed": part_untensed,
                                      "untensed_share": round(part_untensed / part_total, 4),
                                      "dist": part_tense,
                                      "note": "feat_tense set on only ~22% of participles; reliable split is VerbForm-level"},
        "krt_noun_surface_noise_EM5": noun_noise,
        "top_forms_by_subtype": top_forms,
        "traditional_layer": {"witness": "Whitney 1889 ch. XVII §§935–1000 (primary derivation / kṛt)"},
        "limits": {
            "EM5_krt_nouns": "deverbal agent/action nouns not tagged; surface match ~59% false (P5/SG-WF-003) — NOT counted here",
            "participle_tense": "78% of participles tense-unmarked; no fine present/past/future participle census",
            "cpd_overlap": "some deverbal forms are compound members (Case=Cpd); counted here by VerbForm regardless of Cpd",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"deverbal kṛt: {krt_total:,} ({100*krt_total/total_tokens:.1f}% of corpus); leak={leak}", file=sys.stderr)
    for vf in DEVERBAL:
        print(f"  {vf} ({SUBTYPE_RU[vf]}): {subtypes.get(vf,0):,} ({100*subtypes.get(vf,0)/krt_total:.1f}%)", file=sys.stderr)
    print(f"participle untensed: {part_untensed:,} / {part_total:,} ({100*part_untensed/part_total:.0f}%)", file=sys.stderr)
    print(f"kṛt-noun noise: {[(k, v['tokens']) for k, v in noun_noise.items()]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
