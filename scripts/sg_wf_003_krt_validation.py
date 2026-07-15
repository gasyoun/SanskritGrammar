#!/usr/bin/env python3
"""SG-WF-003 pilot P5: primary kṛt suffixes (-ana / -ti / -in) — surface match
validated by MW dictionary derivation (EM5).

Direct test of evidence-limit EM5 (C5 § 5.2): DCS carries NO derivational
(suffix) annotation, and sandhi erases morpheme boundaries. So the slot's query
selects lemmas by surface ending — `dcs:lemma /(ana|ti|tf|in)$/` — and the pilot
asks how noisy that surface match is by validating each candidate against
dictionary derivation. Kill-gate C5 § 7 P5: dictionary validation discards
> 20 % of surface candidates → the query is reworked before any suffix-productivity
claim is asserted.

Scoping finding recorded up front: **`-tṛ` (SLP1 `tf`) is not surface-matchable
in DCS lemmas at all** — 0 NOUN/ADJ lemmas end in `tf` (DCS does not lemmatise
agent nouns to a -tṛ-final form). So the pilot runs on -ana / -ti / -in.

Two validation signals per surface lemma (a lemma is dictionary-confirmed as a
root derivative if EITHER fires):
  S1  MW etymology — the lemma is an MW headword MW explicitly derives from a root
      (csl-orig mw_etymology.tsv, root_via ∈ {parse, fr-root}). Authoritative but
      low-recall (MW rarely spells out an etymology).
  S2  dhātu strip-check — strip the suffix, undo guṇa/vṛddhi on the final, and match
      the residue against the canonical dhātu list. Broader, but a rough phonological
      heuristic (samprasāraṇa / nasal-loss under -ti is not modelled).

The automatic discard rate is a first estimate; the 80-lemma manual adjudication
(sg_wf_003_adjudicate_sample.py) is the AUTHORITATIVE false-positive measure for
the kill-gate — it separates true surface noise (vana, dhana, proper names) from
genuine kṛt derivatives MW simply doesn't gloss.

Ground truth consumed, never rebuilt (C3 § 2.1): pinned VisualDCS master +
csl-orig MW etymology + canonical dhātu list.

Usage:
  python scripts/sg_wf_003_krt_validation.py [--db PATH] [--skip-checksum]
Outputs into sangram/articles/krt-suffixes/data/ .
"""
import argparse
import csv
import hashlib
import json
import random
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
MW_ETYM = GITHUB / "csl-orig" / "v02" / "mw" / "mw_etymology.tsv"
DHATU = GITHUB / "csl-orig" / "v02" / "etymology_stats" / "dhatu_roots.txt"
OUT_DIR = ROOT / "sangram" / "articles" / "krt-suffixes" / "data"

SEED = 20260715
SUFFIXES = ["ana", "ti", "in"]          # -tṛ (tf) not surface-matchable in DCS lemmas
PER_SUFFIX_SAMPLE = 27                    # ~81 total, uniform over distinct lemmas


def load_mw_confirmed():
    s = set()
    with open(MW_ETYM, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            if r["root_via"] in ("parse", "fr-root") and r["root_slp1"].strip():
                s.add(r["headword_slp1"].strip())
    return s


def load_dhatu():
    return set(l.strip() for l in open(DHATU, encoding="utf-8")
              if l.strip() and not l.startswith("#"))


_GUNA = [("ar", ["f"]), ("Ar", ["F", "f"]), ("al", ["x"]),
         ("ay", ["i", "I", "e"]), ("Ay", ["E"]),
         ("av", ["u", "U", "o"]), ("Av", ["O"])]


def strip_candidates(lemma, suf):
    """Residual root candidates after stripping the suffix and undoing guṇa/vṛddhi
    — at the LAST vowel nucleus, so internal guṇa is reversed too (darśana → darś →
    dṛś; kāraṇa → kār → kṛ). A rough heuristic: -ti nasal-loss (gati<gam) is only
    partially modelled; its output is cross-checked by the manual sample, never
    trusted as truth."""
    stem = lemma[:-len(suf)]
    c = {stem}
    for pat, repls in _GUNA:
        i = stem.rfind(pat)
        if i != -1:
            for r in repls:
                c.add(stem[:i] + r + stem[i + len(pat):])
    j = stem.rfind("A")                    # internal vṛddhi ā<a (vād<vad, gām<gam)
    if j != -1:
        c.add(stem[:j] + "a" + stem[j + 1:])
    if suf == "ti":                        # weak/nasal-loss: gati<gam, try nasal restore
        c |= {stem + "m", stem + "n"}
    return {x for x in c if x}


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
        print("ERROR: master has no provenance pin — refusing (C3 § 2.1)")
        return 1
    sha256 = None
    if not args.skip_checksum:
        h = hashlib.sha256()
        with open(db, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 22), b""):
                h.update(chunk)
        sha256 = h.hexdigest()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mw = load_mw_confirmed()
    dhatu = load_dhatu()

    # -tṛ scoping evidence
    tf_lemmas = cur.execute(
        "SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ') "
        "AND lemma LIKE '%tf'").fetchone()[0]

    per_suffix = {}
    all_records = []
    sample_pool = {}
    for suf in SUFFIXES:
        rows = cur.execute(
            "SELECT t.lemma, COUNT(*) n FROM token t "
            "WHERE t.upos IN ('NOUN','ADJ') AND t.lemma LIKE ? "
            "GROUP BY t.lemma ORDER BY n DESC", (f"%{suf}",)).fetchall()
        types = len(rows)
        tokens = sum(n for _, n in rows)
        conf_types = conf_tokens = 0
        s1_only = s2_only = both = 0
        recs = []
        for lemma, n in rows:
            s1 = lemma in mw
            s2 = bool(strip_candidates(lemma, suf) & dhatu)
            conf = s1 or s2
            if conf:
                conf_types += 1
                conf_tokens += n
            if s1 and s2:
                both += 1
            elif s1:
                s1_only += 1
            elif s2:
                s2_only += 1
            rec = {"lemma": lemma, "suffix": suf, "tokens": n,
                   "mw_etym": int(s1), "dhatu_strip": int(s2), "confirmed": int(conf)}
            recs.append(rec)
            all_records.append(rec)
        per_suffix[suf] = {
            "types": types, "tokens": tokens,
            "confirmed_types": conf_types, "confirmed_tokens": conf_tokens,
            "discard_types": types - conf_types,
            "discard_rate_types_pct": round(100 * (types - conf_types) / types, 2),
            "discard_rate_tokens_pct": round(100 * (tokens - conf_tokens) / tokens, 2),
            "signal_overlap": {"both": both, "mw_only": s1_only, "dhatu_only": s2_only},
        }
        sample_pool[suf] = [r["lemma"] for r in recs]

    # overall
    T = sum(p["types"] for p in per_suffix.values())
    Tok = sum(p["tokens"] for p in per_suffix.values())
    CT = sum(p["confirmed_types"] for p in per_suffix.values())
    CTok = sum(p["confirmed_tokens"] for p in per_suffix.values())

    # 80-lemma adjudication sample: uniform over distinct lemmas per suffix
    rng = random.Random(SEED)
    sample = []
    for suf in SUFFIXES:
        pool = sorted(sample_pool[suf])
        pick = rng.sample(pool, min(PER_SUFFIX_SAMPLE, len(pool)))
        for lemma in pick:
            rec = next(r for r in all_records if r["lemma"] == lemma and r["suffix"] == suf)
            sample.append(rec)

    # attach one example sentence per sampled lemma
    detail = ("SELECT s.text_sandhied, c.ref, x.name FROM token t "
              "JOIN sentence s ON s.id=t.sentence_id "
              "JOIN chapter c ON c.chapter_id=s.chapter_id "
              "JOIN text x ON x.text_id=c.text_id "
              "WHERE t.lemma=? AND t.upos IN ('NOUN','ADJ') LIMIT 1")
    with open(OUT_DIR / "validation_all.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lemma", "suffix", "tokens", "mw_etym", "dhatu_strip", "confirmed"])
        for r in sorted(all_records, key=lambda r: -r["tokens"]):
            w.writerow([r["lemma"], r["suffix"], r["tokens"], r["mw_etym"],
                        r["dhatu_strip"], r["confirmed"]])

    with open(OUT_DIR / "adjudication_sample.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["lemma", "suffix", "tokens", "mw_etym", "dhatu_strip",
                    "auto_confirmed", "chapter_ref", "text", "sentence",
                    "adjudicated_genuine_krt", "note"])
        for r in sorted(sample, key=lambda r: (r["suffix"], -r["tokens"])):
            d = cur.execute(detail, (r["lemma"],)).fetchone() or ("", "", "")
            w.writerow([r["lemma"], r["suffix"], r["tokens"], r["mw_etym"],
                        r["dhatu_strip"], r["confirmed"], d[1], d[2],
                        (d[0] or "")[:150], "", ""])

    summary = {
        "study": "SG-WF-003 pilot P5: primary kṛt suffixes — surface match validated by MW derivation",
        "method": "C5 § 3 via C3; direct test of EM5; kill-gate = dictionary discard > 20 %",
        "snapshot": {"master": str(db), "sha256": sha256, "provenance": prov},
        "suffixes_tested": SUFFIXES,
        "tf_scoping": {
            "tf_final_nominal_lemmas": tf_lemmas,
            "note": ("-tṛ (SLP1 tf) is NOT surface-matchable — 0 NOUN/ADJ lemmas end in tf; "
                     "DCS does not lemmatise agent nouns to a -tṛ-final form (an EM5 finding)"),
        },
        "validation_sources": {
            "mw_etymology_confirmed_headwords": len(mw),
            "mw_etymology_file": "csl-orig/v02/mw/mw_etymology.tsv (root_via ∈ parse|fr-root)",
            "dhatu_list": len(dhatu),
            "dhatu_file": "csl-orig/v02/etymology_stats/dhatu_roots.txt",
            "s2_caveat": "dhātu strip-check is a rough guṇa/vṛddhi heuristic; -ti nasal-loss under-recalled",
        },
        "per_suffix": per_suffix,
        "overall": {
            "types": T, "tokens": Tok,
            "confirmed_types": CT, "confirmed_tokens": CTok,
            "auto_discard_rate_types_pct": round(100 * (T - CT) / T, 2),
            "auto_discard_rate_tokens_pct": round(100 * (Tok - CTok) / Tok, 2),
        },
        "kill_gate": {
            "rule": ("C5 § 7 P5: dictionary validation discards > 20 % of surface candidates "
                     "→ query reworked before asserting suffix productivity"),
            "auto_discard_rate_types_pct": round(100 * (T - CT) / T, 2),
            "authoritative_measure": ("manual false-positive rate on the 80-lemma sample "
                                      "(adjudication_sample.tsv) — separates surface noise from "
                                      "MW coverage gaps; see sg_wf_003_adjudicate_sample.py"),
            "seed": SEED, "sample_size": len(sample),
        },
    }
    (OUT_DIR / "validation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    o = summary["overall"]
    print(f"-tṛ surface-matchable lemmas: {tf_lemmas} (not surface-matchable)")
    for suf in SUFFIXES:
        p = per_suffix[suf]
        print(f"-{suf}: {p['types']} types / {p['tokens']} tok; "
              f"auto-discard types {p['discard_rate_types_pct']}% tokens {p['discard_rate_tokens_pct']}%")
    print(f"OVERALL auto-discard: types {o['auto_discard_rate_types_pct']}%  "
          f"tokens {o['auto_discard_rate_tokens_pct']}%")
    print(f"sample {len(sample)} lemmas -> adjudication_sample.tsv (manual FP rate is the kill-gate authority)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
