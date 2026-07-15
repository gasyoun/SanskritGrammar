#!/usr/bin/env python3
"""SG-MO-013 pilot P2: thematic present classes (attested / generated / traditional).

Tests evidence-limit EM1 of the C5 morphology programme (§ 5.2): the present
CLASS (gaṇa I–X) is NOT stored in DCS per-token morphology, and — as this pilot
establishes — is NOT recoverable from DCS's own lemma-dictionary code either
(the `grammar` field number, e.g. "6. Ā.", is a DCS-internal index that does not
correspond to the Pāṇinian gaṇa: tud is class VI but coded 7, viś VI→3, grah
IX→4). The traditional class can be recovered only by joining the token's root
to an external inventory — WhitneyRoots roots.csv `class` / root_class.csv gaṇa —
and that join is itself lossy and ambiguous. The pilot measures exactly how much.

Attribution tiers of the present-finite universe (mutually exclusive):
  - AYA        : form-evident secondary thematic — a `-aya-` stem (lemma ends
                 -ay, or DCS grammar marks Denom./Caus.). Thematic by surface
                 morphology (class-X-like); no inventory join needed.
  - SINGLE     : the token's root joins to a WhitneyRoots root with exactly ONE
                 gaṇa — cleanly, unambiguously classable.
  - MULTI      : the root joins but WhitneyRoots assigns it several gaṇa
                 (kṛ = I|II|V|VIII, dā = I|II|III|IV) — the token-level class is
                 NOT determined by the root alone; only an athematic surface
                 marker (or accent, absent in the corpus) could disambiguate.
  - UNJOINED   : a DCS derived/preverbed stem-lemma with no bare-root match in
                 WhitneyRoots (EM6: root-inventory granularity divergence).

Headline kill-gate (C5 § 7 P2): the "cleanly classable" share = AYA + SINGLE.
If < 90 %, gaṇa frequencies are published as inventory-weighted estimates over
the cleanly-classable subset, NOT as token-level corpus facts (C3 P4).

Present-system universe: finite verb tokens with Tense=Pres (present indicative/
optative/imperative/subjunctive — present stem). The imperfect (Tense=Impf) is a
present-stem preterite reported separately to avoid the EM2/Д1 Tense=Past
preterite-conflation; aorist/perfect/future are out of scope by construction.

Ground truth is consumed, never rebuilt (C3 § 2.1): the pinned VisualDCS SQLite
master + WhitneyRoots crosswalk.

Usage:
  python scripts/sg_mo_013_thematic_present_coverage.py [--db PATH] [--skip-checksum]
Outputs into sangram/articles/thematic-present/data/ .
"""
import argparse
import csv
import hashlib
import json
import random
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
WHITNEY = GITHUB / "WhitneyRoots" / "crosswalk"
OUT_DIR = ROOT / "sangram" / "articles" / "thematic-present" / "data"

THEMATIC = {1, 4, 6, 10}          # gaṇa I (bhū), IV (div/-ya-), VI (tud), X (cur/-aya-)
ALL_CLASSES = list(range(1, 11))
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII",
         8: "VIII", 9: "IX", 10: "X"}

SEED = 20260715
SAMPLE_SIZE = 80

UNIV = ("t.upos = 'VERB' AND t.feat_tense = 'Pres' "
        "AND (t.feat_verbform IS NULL OR t.feat_verbform = 'Fin')")

GRAM_CLASS = re.compile(r"(\d+)\s*\.")
ROMAN_RE = re.compile(r"[IVX]+")
AYA_LEMMA = re.compile(r"ay$")


def dcs_code(grammar: str) -> list:
    """The DCS lemma.grammar numeric code(s) — NOT the gaṇa; kept only to
    measure its divergence from the traditional class."""
    return sorted(set(int(m) for m in GRAM_CLASS.findall(grammar or "")))


def is_aya(lemma: str, grammar: str) -> bool:
    return bool(AYA_LEMMA.search(lemma)) or "Denom" in (grammar or "") or "Caus" in (grammar or "")


def roman_to_int(tok: str) -> int:
    vals = {"I": 1, "V": 5, "X": 10}
    total, prev = 0, 0
    for ch in reversed(tok):
        v = vals.get(ch, 0)
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


def load_whitney():
    """root_iast -> set(gaṇa int), union of roots.csv `class` and root_class.csv
    over all homonym rows of that root string."""
    gana_by_no = defaultdict(set)
    with open(WHITNEY / "root_class.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            g = (row.get("gana") or "").strip()
            if ROMAN_RE.fullmatch(g):
                gana_by_no[row["whitney_no"]].add(roman_to_int(g))
    by_root = defaultdict(set)
    with open(WHITNEY / "roots.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            root = (row.get("root_iast") or "").strip()
            if not root:
                continue
            for tok in (row.get("class") or "").split("|"):
                tok = tok.strip()
                if ROMAN_RE.fullmatch(tok):
                    by_root[root].add(roman_to_int(tok))
            by_root[root] |= gana_by_no.get(row["whitney_no"], set())
    return by_root


def bare_root(lemma: str, preverbs: str) -> str:
    if not preverbs:
        return lemma
    for pv in sorted((p.strip() for p in preverbs.split(",")), key=len, reverse=True):
        if pv and lemma.startswith(pv) and len(lemma) > len(pv):
            return lemma[len(pv):]
    return lemma


def classify(lemma, grammar, preverbs, whitney):
    """Return (tier, gana_set). tier in AYA/SINGLE/MULTI/UNJOINED."""
    if is_aya(lemma, grammar):
        return "AYA", {10}
    gs = whitney.get(bare_root(lemma, preverbs or ""), set())
    if not gs:
        return "UNJOINED", set()
    return ("SINGLE" if len(gs) == 1 else "MULTI"), gs


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

    whitney = load_whitney()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    total = cur.execute(f"SELECT COUNT(*) FROM token t WHERE {UNIV}").fetchone()[0]
    rows = cur.execute(
        "SELECT t.lemma_id, t.lemma, l.grammar, l.preverbs, COUNT(*) n "
        "FROM token t JOIN lemma l ON l.lemma_id = t.lemma_id "
        f"WHERE {UNIV} GROUP BY t.lemma_id ORDER BY n DESC").fetchall()

    tier_tok = Counter()
    gana_tok_single = Counter()     # gaṇa distribution over cleanly-classable (SINGLE + AYA)
    gana_tok_all = Counter()        # fractional over every joined token (for reference)
    them_clean = ath_clean = 0
    ivi_tok = 0                     # any token whose root gaṇa set meets {I,VI}
    dcs_match = dcs_mismatch = 0
    multi_root_counter = Counter()  # which multi-gaṇa roots carry the mass
    lemma_records = []
    for lid, lemma, grammar, preverbs, n in rows:
        tier, gs = classify(lemma, grammar, preverbs, whitney)
        tier_tok[tier] += n
        if tier == "AYA":
            gana_tok_single[10] += n
            gana_tok_all[10] += n
            them_clean += n
        elif tier == "SINGLE":
            g = next(iter(gs))
            gana_tok_single[g] += n
            gana_tok_all[g] += n
            if g in THEMATIC:
                them_clean += n
            else:
                ath_clean += n
        if gs:
            if tier == "MULTI":
                for g in gs:
                    gana_tok_all[g] += n / len(gs)
                multi_root_counter[bare_root(lemma, preverbs or "")] += n
            if gs & {1, 6}:
                ivi_tok += n
        # DCS-code vs Whitney-gaṇa divergence (tokens where both exist)
        code = set(dcs_code(grammar))
        if gs and code:
            if code & gs:
                dcs_match += n
            else:
                dcs_mismatch += n
        lemma_records.append({
            "lemma_id": lid, "lemma": lemma, "tokens": n, "tier": tier,
            "dcs_grammar": grammar or "",
            "whitney_gana": "|".join(ROMAN[g] for g in sorted(gs)),
        })

    passive_tok = cur.execute(
        f"SELECT COUNT(*) FROM token t WHERE {UNIV} AND t.feat_voice='Pass'").fetchone()[0]
    impf_tok = cur.execute(
        "SELECT COUNT(*) FROM token t WHERE t.upos='VERB' AND t.feat_tense='Impf' "
        "AND (t.feat_verbform IS NULL OR t.feat_verbform='Fin')").fetchone()[0]

    clean = tier_tok["AYA"] + tier_tok["SINGLE"]
    clean_classified = them_clean + ath_clean + tier_tok["AYA"]  # AYA counted thematic
    # them_clean already includes AYA; recompute split cleanly:
    them_clean_total = them_clean
    ath_clean_total = ath_clean

    # ---- kill-gate sample: tier of each sampled token ----
    ids = [r[0] for r in cur.execute(f"SELECT t.id FROM token t WHERE {UNIV}").fetchall()]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), SAMPLE_SIZE)
    detail_sql = (
        "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.lemma_id, l.grammar, "
        "l.preverbs, t.feat_mood, t.feat_person, t.feat_number, t.feat_voice, "
        "s.text_sandhied, c.ref, x.name "
        "FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
        "JOIN sentence s ON s.id=t.sentence_id "
        "JOIN chapter c ON c.chapter_id=s.chapter_id "
        "JOIN text x ON x.text_id=c.text_id WHERE t.id=?")
    sample_rows = []
    clean_sample = 0
    for tid in chosen:
        r = cur.execute(detail_sql, (tid,)).fetchone()
        (_id, form, uns, lemma, lid, grammar, preverbs, mood, person, number,
         voice, sent, ref, textname) = r
        tier, gs = classify(lemma, grammar, preverbs, whitney)
        if tier in ("AYA", "SINGLE"):
            clean_sample += 1
        sample_rows.append([
            tid, form, uns or "", lemma, lid, grammar or "",
            bare_root(lemma, preverbs or ""),
            "|".join(ROMAN[g] for g in sorted(gs)), tier,
            "clean" if tier in ("AYA", "SINGLE") else "CHECK",
            mood or "", person or "", number or "", voice or "",
            (sent or "")[:160], ref or "", textname or "",
        ])

    # ---------------------------- write outputs ---------------------------- #
    with open(OUT_DIR / "class_distribution.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["gana", "roman", "kind", "cleanly_classable_tokens",
                    "all_joined_tokens_fractional"])
        for c in ALL_CLASSES:
            w.writerow([c, ROMAN[c], "thematic" if c in THEMATIC else "athematic",
                        round(gana_tok_single.get(c, 0), 1),
                        round(gana_tok_all.get(c, 0), 1)])

    with open(OUT_DIR / "lemma_class_join_top.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lemma_id", "lemma", "tokens", "tier", "dcs_grammar", "whitney_gana"])
        for rec in lemma_records[:200]:
            w.writerow([rec["lemma_id"], rec["lemma"], rec["tokens"], rec["tier"],
                        rec["dcs_grammar"], rec["whitney_gana"]])

    with open(OUT_DIR / "validation_sample.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "lemma_id",
                    "dcs_grammar", "bare_root", "whitney_gana", "tier",
                    "auto_verdict", "mood", "person", "number", "voice",
                    "sentence", "chapter_ref", "text"])
        w.writerows(sample_rows)

    top_multi = multi_root_counter.most_common(15)
    summary = {
        "study": "SG-MO-013 pilot P2: thematic present classes (attested/generated/traditional)",
        "method": "C5 § 3 (attested/generated/traditional) via C3 cycle; tests EM1 (§ 5.2)",
        "snapshot": {"master": str(db), "sha256": sha256, "provenance": prov},
        "universe_where_sql": UNIV,
        "universe_gloss": ("finite verb tokens, Tense=Pres (present indicative/"
                           "optative/imperative/subjunctive — present stem); "
                           "imperfect and past-stem tenses excluded"),
        "present_fin_tokens": total,
        "present_fin_lemma_ids": len(rows),
        "imperfect_fin_tokens_excluded": impf_tok,
        "class_source_traditional": "WhitneyRoots roots.csv `class` + root_class.csv gaṇa (I–X)",
        "dcs_grammar_is_not_gana": (
            "the DCS lemma.grammar numeric code is a DCS-internal index, NOT the "
            "Pāṇinian gaṇa (e.g. tud VI->7, viś VI->3, grah IX->4, i II->9); it is "
            "measured only for its divergence, never used as the class"),
        "thematic_classes": sorted(THEMATIC),
        "attribution_tiers": {
            "AYA_secondary_thematic": tier_tok["AYA"],
            "AYA_pct": round(100 * tier_tok["AYA"] / total, 2),
            "SINGLE_gana_root": tier_tok["SINGLE"],
            "SINGLE_pct": round(100 * tier_tok["SINGLE"] / total, 2),
            "MULTI_gana_root": tier_tok["MULTI"],
            "MULTI_pct": round(100 * tier_tok["MULTI"] / total, 2),
            "UNJOINED": tier_tok["UNJOINED"],
            "UNJOINED_pct": round(100 * tier_tok["UNJOINED"] / total, 2),
            "cleanly_classable_tokens": clean,
            "cleanly_classable_pct": round(100 * clean / total, 2),
        },
        "distribution_cleanly_classable": {
            "thematic_tokens": them_clean_total,
            "athematic_tokens": ath_clean_total,
            "thematic_pct": round(100 * them_clean_total / clean, 2),
            "by_gana": {ROMAN[c]: round(gana_tok_single.get(c, 0), 1) for c in ALL_CLASSES},
        },
        "dcs_code_vs_gana": {
            "match_tokens": dcs_match,
            "mismatch_tokens": dcs_mismatch,
            "match_pct_of_tokens_with_both": (
                round(100 * dcs_match / (dcs_match + dcs_mismatch), 2)
                if (dcs_match + dcs_mismatch) else None),
            "note": "loose (set-intersection over multi-class union); stark single-class "
                    "counterexamples: tud VI vs code 7, viś VI vs 3, grah IX vs 4, i II vs 9",
        },
        "collapses": {
            "root_gana_meets_I_or_VI_tokens": ivi_tok,
            "root_gana_meets_I_or_VI_pct": round(100 * ivi_tok / total, 2),
            "passive_tagged_tokens": passive_tok,
            "passive_pct": round(100 * passive_tok / total, 2),
            "note": "I and VI are both plain-thematic (-a-); their surface present is "
                    "identical without accent. IV (-ya-) collides with passive/"
                    "denominative -ya-.",
        },
        "top_multi_gana_roots": [{"root": r, "tokens": n} for r, n in top_multi],
        "kill_gate": {
            "rule": ("C5 § 7 P2: cleanly-classable (single-gaṇa root + form-evident "
                     "-aya) < 90 % -> gaṇa frequencies published as inventory-weighted "
                     "estimates over the cleanly-classable subset, not token-level facts"),
            "cleanly_classable_pct": round(100 * clean / total, 2),
            "fired": clean / total < 0.90,
            "seed": SEED,
            "sample_size": SAMPLE_SIZE,
            "sample_cleanly_classable": clean_sample,
            "sample_cleanly_classable_pct": round(100 * clean_sample / SAMPLE_SIZE, 2),
            "file": "validation_sample.tsv (+ manual adjudication in validation_verdicts.tsv)",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    a = summary["attribution_tiers"]
    print(f"present-fin universe: {total} tokens / {len(rows)} lemma_ids")
    print(f"tiers: AYA {a['AYA_pct']}%  SINGLE {a['SINGLE_pct']}%  "
          f"MULTI {a['MULTI_pct']}%  UNJOINED {a['UNJOINED_pct']}%")
    print(f"cleanly-classable {a['cleanly_classable_pct']}%  "
          f"-> thematic {summary['distribution_cleanly_classable']['thematic_pct']}%")
    print(f"DCS-code vs gaṇa match {summary['dcs_code_vs_gana']['match_pct_of_tokens_with_both']}%")
    print(f"root gaṇa meets I/VI {summary['collapses']['root_gana_meets_I_or_VI_pct']}%  "
          f"passive {summary['collapses']['passive_pct']}%")
    print(f"KILL-GATE {'FIRED' if summary['kill_gate']['fired'] else 'not fired'} "
          f"(cleanly-classable {a['cleanly_classable_pct']}% < 90%); "
          f"sample {summary['kill_gate']['sample_cleanly_classable_pct']}%")
    print(f"wrote {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
