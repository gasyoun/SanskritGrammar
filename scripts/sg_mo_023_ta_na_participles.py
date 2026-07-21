#!/usr/bin/env python3
"""SG-MO-023 «Именные формы глагола: -ta/-na (причастия прош. страд.)» .

Core W2 ① article (content, no kill-gate). The -ta/-na past passive participle
(ppp: kṛta, gata, bhinna) is the most important verbal adjective — base of the
periphrastic passive/perfect and a productive adjective. It declines like an
a-stem (masc/neut) + ā-stem (fem), so it is a NOMINAL verb-form.

Evidence-limit note (EM5-type): DCS marks `VerbForm=Part` but does NOT distinctly
tag the -ta/-na class — the ppp sits in the tense=NULL participle bulk (the tense
attribute is used for the PRESENT participle, Pres). So the -ta/-na ppp is
identified by STEM: strip the a-/ā-stem inflection from `m_unsandhied`, then test
whether the consonant stem ends in -t (→ -ta) or -n (→ -na). This is a **lower
bound**: it excludes sandhi-assimilated variants (labdha, rūḍha, baddha, dagdha —
phonologically -ta but surface -dha/-ḍha/-bdha/-gdha). A seeded validation sample
records the (measured near-zero) false-positive rate.

Three layers (C5 §3): ATTESTED — this stem-strip count over the pinned snapshot;
GENERATED/TRADITIONAL — the ppp declines as an a-stem (see SG-MO-002); the -ta/-na
allotment + sandhi is Whitney 1889 §§952–966.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators; seeded sample. Read-only. Emits into sangram/articles/ta-na-participles/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "ta-na-participles" / "data"

# a-stem (m/n) + ā-stem (f) endings that consume the thematic vowel; strip longest.
ENDINGS = sorted(
    ['a', 'aḥ', 'am', 'aṃ', 'ena', 'āya', 'āt', 'asya', 'e', 'au', 'ābhyām',
     'ayoḥ', 'āḥ', 'ān', 'aiḥ', 'ebhyaḥ', 'ānām', 'eṣu', 'ā', 'ām', 'ayā',
     'āyā', 'āyai', 'āyāḥ', 'āyām', 'āyoḥ', 'āni', 'āsu', 'ābhiḥ'],
    key=len, reverse=True)

SEED = 20260717
SAMPLE_SIZE = 50


def stem_of(w):
    for e in ENDINGS:
        if w.endswith(e) and len(w) > len(e):
            return w[:-len(e)]
    return w


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

    # participle system context
    part_total = cur.execute("SELECT COUNT(*) FROM token WHERE feat_verbform='Part'").fetchone()[0]
    tense_dist = {(t or "None"): c for t, c in cur.execute(
        "SELECT feat_tense, COUNT(*) FROM token WHERE feat_verbform='Part' GROUP BY feat_tense")}

    # broader deverbal-formation context (H1346 card MO23, follow-up to visa note):
    # every non-finite VerbForm-tagged category in the pinned snapshot, so the -ta/-na
    # ppp count can be checked against deverbal formations OTHER than participles too
    # (converb/absolutive, gerundive, infinitive) -- not just against other participle
    # sub-types. No stem-strip needed here: Conv/Gdv/Inf are tagged directly.
    verbform_dist = {(v or "None"): c for v, c in cur.execute(
        "SELECT feat_verbform, COUNT(*) FROM token WHERE feat_verbform IS NOT NULL "
        "GROUP BY feat_verbform")}
    # finite verbal forms, same convention as scripts/dcs2026_figures.py: upos='VERB' AND
    # feat_verbform IS NULL -- NOT "feat_mood is set" (17 upos='VERB' tokens carry neither
    # feat_verbform nor feat_mood and are still finite-denominator members under this rule;
    # an earlier draft of this article mis-described the criterion as "feat_mood set", which
    # undercounts by those 17 -- fixed here so the number is reproducible under its own stated rule)
    finite_verbal_total = cur.execute(
        "SELECT COUNT(*) FROM token WHERE upos='VERB' AND feat_verbform IS NULL").fetchone()[0]

    # -ta/-na ppp = tense-NULL participles whose stripped stem ends in t / n
    rows = cur.execute(
        "SELECT id, m_unsandhied, lemma, feat_case, feat_number, feat_gender "
        "FROM token WHERE feat_verbform='Part' AND feat_tense IS NULL AND m_unsandhied IS NOT NULL"
    ).fetchall()
    tense_null = len(rows)
    ta, na, other = [], [], 0
    roots = set()
    case_counter = Counter()
    for tid, m, lemma, case, num, gen in rows:
        s = stem_of(m)
        if s.endswith("t"):
            ta.append((tid, m, lemma, case, num, gen)); roots.add(lemma)
            case_counter[case or "Cpd?"] += 1
        elif s.endswith("n"):
            na.append((tid, m, lemma, case, num, gen)); roots.add(lemma)
            case_counter[case or "Cpd?"] += 1
        else:
            other += 1
    ppp = ta + na
    n_ppp = len(ppp)

    # top ppp roots by ppp-token frequency
    root_freq = Counter(r[2] for r in ppp)

    # seeded validation sample (for FP audit)
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(range(len(ppp))), min(SAMPLE_SIZE, len(ppp)))
    sample = []
    for i in chosen:
        tid = ppp[i][0]
        d = cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.feat_case, t.feat_gender, "
            "t.feat_number, x.name, c.ref, s.sent_counter FROM token t "
            "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "case", "gender",
                    "number", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "SG-MO-023 «Именные формы: -ta/-na причастия» — past passive participle (core W2 ①, content)",
        "toc_ref": "SG-MO-023",
        "kind": "content article (no kill-gate)",
        "method": "VerbForm=Part & tense IS NULL, stem-strip (a-/ā-stem ending removed), stem-final t→-ta / n→-na; lower bound (excludes sandhi-assimilated -dha/-ḍha/-bdha/-gdha)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "participle_system": {"verbform_part_total": part_total, "tense_dist": tense_dist,
                              "note": "tense marks the PRESENT participle (Pres); the -ta/-na ppp is in the tense=NULL bulk"},
        "denominators": {
            "tense_null_participles": tense_null,
            "ta_na_ppp_lower_bound": n_ppp,
            "ta": len(ta), "na": len(na),
            "ta_na_ratio": round(len(ta) / len(na), 1) if na else None,
            "share_of_tense_null": round(100 * n_ppp / tense_null, 1),
            "share_of_all_participles": round(100 * n_ppp / part_total, 1),
            "distinct_roots": len(roots),
            "non_tn_stem_remainder": other,
        },
        "deverbal_context": {
            "note": "non-finite VerbForm-tagged categories in the pinned snapshot (Part/Conv/Gdv/Inf); "
                    "-ta/-na ppp is a subset of Part (tense=NULL, stem-strip, see above)",
            "verbform_counts": verbform_dist,
            "total_non_finite_deverbal": sum(verbform_dist.values()),
            "ta_na_ppp_share_of_all_deverbal": round(100 * n_ppp / sum(verbform_dist.values()), 1),
            "next_largest_non_participle_category": max(
                ((k, v) for k, v in verbform_dist.items() if k != "Part"), key=lambda kv: kv[1]),
            "finite_verbal_forms": {
                "criterion": "upos='VERB' AND feat_verbform IS NULL (dcs2026_figures.py convention; "
                              "does NOT require feat_mood to be set)",
                "count": finite_verbal_total,
                "excluded_from_deverbal_comparison": True,
            },
        },
        "case_distribution": dict(case_counter.most_common()),
        "top_ppp_roots": [{"root": r, "ppp_tokens": c} for r, c in root_freq.most_common(20)],
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "EM5_class_not_tagged": "DCS does not distinctly tag the -ta/-na class; identified by stem — a surface method",
            "lower_bound": "excludes sandhi-assimilated ppp (labdha/rūḍha/baddha/dagdha: -dha/-ḍha/-bdha/-gdha) — true count is higher",
            "declension": "ppp declines as a-stem (m/n) + ā-stem (f) — see SG-MO-002; not re-generated here",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    d = summary["denominators"]
    print(f"Part total: {part_total:,}; tense dist: {tense_dist}", file=sys.stderr)
    print(f"-ta/-na ppp (lower bound): {n_ppp:,} = -ta {d['ta']:,} + -na {d['na']:,} "
          f"(ratio {d['ta_na_ratio']}:1); {d['share_of_tense_null']}% of tense-NULL, "
          f"{d['share_of_all_participles']}% of all participles; {d['distinct_roots']:,} roots", file=sys.stderr)
    print(f"top roots: {[(x['root'], x['ppp_tokens']) for x in summary['top_ppp_roots'][:8]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
