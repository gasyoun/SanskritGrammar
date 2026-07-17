#!/usr/bin/env python3
"""SG-MO-028 «Вторичные спряжения: каузатив» — the causative.

Core W2 ① article (endgame slot, map-heavy). The causative (secondary
conjugation: strengthened root + -aya-; kāráyati "causes to do", darśáyati
"shows") is NOT natively tagged in DCS. There is no `Caus` feature anywhere in
the annotation; the causative surfaces only as a DERIVED lemma ending in -ay
whose `lemma.grammar` code is class 10 (`10.P.`/`10.Ā.`) — the curādi class.

That bucket (55 376 finite tokens, 10.57 %) is a CONFLATION: it merges genuine
causatives (kāray ← kṛ, janay ← jan, darśay ← dṛś, nāśay ← naś) with primary
curādi verbs that were never derived from a simpler root (kathay "tell", cintay
"think", pūjay "worship", kāmay "desire"). Both take the -aya- stem and both are
tagged class 10 — DCS does not separate them. So the causative as a derivational
CATEGORY is not recoverable from the annotation; only the merged class-X surface
is countable, and equating class-10 = causative over-counts by the primary-curādi
share (the article's measured limit, EM5-family: type not natively marked).

Three layers (C5 §3): ATTESTED — the class-10 -ay bucket's distribution and the
transparent-causative lower bound over the pinned snapshot; TRADITIONAL —
strengthened root + -aya- + either voice (Whitney §§1041–1052); GENERATED — the
causative -aya- stem by a conjugator, formally identical to primary curādi.

This script measures, reproducibly:
  (1) the class-10 -ay bucket size + share (Wilson CI) and its person/number/
      tense/mood profile;
  (2) a mechanical LOWER BOUND on the transparent-causative share — class-10
      lemmas whose de-strengthened base is attested as a primary (non-10) root;
  (3) a seeded sample of class-10 lemma TYPES (weighted by token freq) for the
      hand-adjudication that fixes the false-positive rate of class-10 = causative
      (recorded in adjudication.json, computed by the caller).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators + Wilson CI on the headline share; seeded sample. Read-only. Emits
into sangram/articles/causative/data/.
"""
import argparse
import csv
import hashlib
import json
import math
import random
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "causative" / "data"

FIN = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
       "AND feat_person IS NOT NULL")
# class-10 (curādi = causative + primary curādi, conflated) lemma grammar codes
CLASS10 = "(l.grammar LIKE '10%' OR l.grammar LIKE '%,10%' OR l.grammar LIKE '% 10%')"

SEED = 20260717
SAMPLE_SIZE = 60


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


def dist(cur, col, join_where, total):
    out = {}
    for v, c in cur.execute(
            f"SELECT t.{col}, COUNT(*) FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
            f"WHERE {join_where} GROUP BY t.{col} ORDER BY COUNT(*) DESC"):
        out[v if v is not None else "∅"] = {"tokens": c, "share": round(c / total, 4)}
    return out


# --- de-strengthening: candidate base roots for a class-10 -ay lemma ----------
# Reverse the causative vṛddhi/guṇa on the root vowel to propose primary bases.
# Conservative: generates a small candidate set; a hit against the primary-root
# lemma set proves a TRANSPARENT causative (lower bound — irregular strengthening
# and suppletion are missed, so the true causative share is higher).
_DESTRENGTH = [
    ("ār", "ṛ"), ("ar", "ṛ"), ("ār", "ṛ"),
    ("ai", "i"), ("e", "i"), ("ā", "a"),
    ("au", "u"), ("o", "u"),
]


def base_candidates(stem):
    """stem = class-10 lemma with trailing 'ay' already removed (e.g. 'kār')."""
    cands = {stem}
    # -p- causative augment (sthāp←sthā, jñāp←jñā, dāp←dā): drop trailing p
    if stem.endswith("p") and len(stem) > 2:
        cands.add(stem[:-1])
    # de-strengthen the (first) strengthened nucleus, one substitution at a time
    base = set(cands)
    for s in list(base):
        for a, b in _DESTRENGTH:
            i = s.find(a)
            if i != -1:
                cands.add(s[:i] + b + s[i + len(a):])
        # final -āy/-ay long → short already handled; also try vowel-final -ā→-a
    return {c for c in cands if c}


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

    fin_total = cur.execute(f"SELECT COUNT(*) FROM token WHERE {FIN}").fetchone()[0]

    join10 = f"{FIN} AND {CLASS10}"
    tok10 = cur.execute(
        f"SELECT COUNT(*) FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
        f"WHERE {join10}").fetchone()[0]
    types10 = cur.execute(
        f"SELECT COUNT(DISTINCT t.lemma_id) FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
        f"WHERE {join10}").fetchone()[0]

    joinden = f"{FIN} AND (l.grammar LIKE 'Denom%')"
    tokden = cur.execute(
        f"SELECT COUNT(*) FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
        f"WHERE {joinden}").fetchone()[0]

    # verbless-feature check: is there ANY explicit causative marker?
    caus_feat = cur.execute(
        "SELECT COUNT(*) FROM lemma WHERE grammar LIKE '%aus%'").fetchone()[0]

    person = dist(cur, "feat_person", join10, tok10)
    number = dist(cur, "feat_number", join10, tok10)
    tense = dist(cur, "feat_tense", join10, tok10)
    mood = dist(cur, "feat_mood", join10, tok10)
    third = person.get("3", {}).get("tokens", 0)
    pres = tense.get("Pres", {}).get("tokens", 0)

    # class-10 lemmas with token freq
    lem10 = cur.execute(
        f"SELECT l.lemma_id, l.lemma, l.grammar, COUNT(*) c FROM token t "
        f"JOIN lemma l ON l.lemma_id=t.lemma_id WHERE {join10} "
        f"GROUP BY l.lemma_id ORDER BY c DESC").fetchall()

    # primary-root lemma set (verb class 1..9, NOT 10) — for the base-match test
    prim = set()
    for (lm,) in cur.execute(
            "SELECT lemma FROM lemma WHERE grammar LIKE '_.%' AND grammar NOT LIKE '10%'"):
        prim.add(lm)
    # also single-char class forms like '1.P.' captured by '_.%'; add root strings
    for (lm,) in cur.execute(
            "SELECT lemma FROM lemma WHERE grammar GLOB '[1-9].*'"):
        prim.add(lm)

    # transparent-causative lower bound: class-10 lemma whose de-strengthened base
    # is an attested primary root
    matched_types = matched_tokens = 0
    matched_examples = []
    for lid, lem, gr, c in lem10:
        if not lem.endswith("ay"):
            continue
        stem = lem[:-2]  # drop 'ay'
        cands = base_candidates(stem)
        hit = sorted(cands & prim, key=len)
        if hit:
            matched_types += 1
            matched_tokens += c
            if len(matched_examples) < 30:
                matched_examples.append({"lemma": lem, "base": hit[0], "tokens": c})

    # seeded sample of class-10 lemma TYPES for hand-adjudication (freq-weighted:
    # sample token occurrences, dedup to types, keep order by draw)
    rng = random.Random(SEED)
    weighted = []
    for lid, lem, gr, c in lem10:
        weighted.append((lem, c))
    # build a freq-weighted draw of distinct types
    pool = []
    for lem, c in weighted:
        pool.append((lem, c))
    # sample SAMPLE_SIZE distinct types with probability ∝ token freq
    types_sorted = [l for l, _ in weighted]
    freqs = [c for _, c in weighted]
    chosen_types = []
    seen = set()
    tries = 0
    total_mass = sum(freqs)
    while len(chosen_types) < min(SAMPLE_SIZE, len(types_sorted)) and tries < 100000:
        r = rng.random() * total_mass
        acc = 0
        for lem, c in weighted:
            acc += c
            if acc >= r:
                if lem not in seen:
                    seen.add(lem)
                    chosen_types.append(lem)
                break
        tries += 1

    # one example form per sampled lemma
    sample_rows = []
    freq_by_lem = {l: c for l, c in weighted}
    for lem in chosen_types:
        ex = cur.execute(
            f"SELECT t.form, t.feat_person, t.feat_number, t.feat_tense "
            f"FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
            f"WHERE {join10} AND l.lemma=? LIMIT 1", (lem,)).fetchone()
        sample_rows.append((lem, freq_by_lem.get(lem, 0),
                            ex[0] if ex else "", ex[1] if ex else "",
                            ex[2] if ex else "", ex[3] if ex else ""))

    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "adjudication_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["lemma", "class10_tokens", "example_form", "person", "number",
                    "tense", "verdict(blank→adjudicate: caus|curadi|denom|unclear)"])
        for r in sample_rows:
            w.writerow(list(r) + [""])

    summary = {
        "study": "SG-MO-028 «Каузатив» — causative secondary conjugation (core W2 ①, endgame, map-heavy)",
        "toc_ref": "SG-MO-028",
        "kind": "content article (endgame slot; publishes its limit like the pilots)",
        "method": "the causative is NOT natively tagged (no Caus feature); it surfaces only as class-10 (-ay) lemmas, which conflate genuine causatives with primary curādi. We measure the class-10 bucket, a mechanical transparent-causative LOWER BOUND (de-strengthened base attested as a primary root), and a seeded sample for hand-adjudication of the conflation.",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "native_causative_feature": {
            "grammar_codes_mentioning_caus": caus_feat,
            "note": "zero — DCS carries no explicit causative marker; the class-X -aya- surface is the only handle",
        },
        "denominators": {
            "finite_total": fin_total,
            "class10_ay_bucket": tok10,
            "class10_ay_share": round(tok10 / fin_total, 4),
            "class10_ay_types": types10,
            "denominative_bucket": tokden,
            "denominative_share": round(tokden / fin_total, 4),
        },
        "class10_share_ci95": {"k": tok10, "n": fin_total, "ci95": wilson_ci(tok10, fin_total)},
        "person": person, "number": number, "tense": tense, "mood": mood,
        "third_person_share_ci95": {"k": third, "n": tok10, "ci95": wilson_ci(third, tok10)},
        "present_share_ci95": {"k": pres, "n": tok10, "ci95": wilson_ci(pres, tok10)},
        "transparent_causative_lower_bound": {
            "matched_types": matched_types, "class10_types": types10,
            "matched_tokens": matched_tokens, "class10_tokens": tok10,
            "matched_token_share_of_bucket": round(matched_tokens / tok10, 4) if tok10 else None,
            "method": "class-10 lemma ending -ay whose de-strengthened base (guṇa/vṛddhi reversed, -p- augment dropped) is attested as a primary (non-10) root lemma",
            "note": "LOWER bound — irregular strengthening and suppletion are missed, so the true causative share is higher; the residual mixes primary curādi + unmatched causatives",
            "examples": matched_examples,
        },
        "top_lemmas": [{"lemma": lem, "grammar": gr, "tokens": c}
                       for lid, lem, gr, c in lem10[:25]],
        "adjudication_sample": {"seed": SEED, "size": len(sample_rows),
                                "weighting": "freq-weighted draw of distinct types",
                                "file": "adjudication_sample.tsv"},
        "limits": {
            "EM5_family_type_not_marked": "the causative is a derivational category with no native tag; only the merged class-10 -ay surface is countable, and class-10 = causative over-counts by the primary-curādi share",
            "curadi_conflation": "primary curādi (kathay, cintay, pūjay, kāmay) and derived causatives (kāray, janay, darśay) share the -aya- stem and the class-10 code; DCS does not separate them",
            "base_match_lossy": "the transparent-causative lower bound under-counts: vṛddhi/suppletion (kāray←kṛ needs kār→kṛ) and multi-step strengthening escape the conservative de-strengthening ruleset",
            "denominatives_separate": "denominatives (Denom., 5 451) also take -aya-; counted separately",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"finite {fin_total:,}; class-10 -ay bucket {tok10:,} ({100*tok10/fin_total:.2f}%); "
          f"types {types10:,}; denom {tokden:,}", file=sys.stderr)
    print(f"native Caus feature rows: {caus_feat}", file=sys.stderr)
    print(f"transparent-causative LOWER bound: {matched_types}/{types10} types, "
          f"{matched_tokens:,}/{tok10:,} tokens ({100*matched_tokens/tok10:.1f}%)", file=sys.stderr)
    print(f"person: {[(k, v['share']) for k, v in person.items()]}", file=sys.stderr)
    print(f"tense: {[(k, v['share']) for k, v in tense.items()][:5]}", file=sys.stderr)
    print(f"top: {[(x['lemma'], x['tokens']) for x in summary['top_lemmas'][:8]]}", file=sys.stderr)
    print(f"sample → {OUT_DIR / 'adjudication_sample.tsv'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
