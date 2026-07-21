#!/usr/bin/env python3
"""SG-MO-026 «Именные формы глагола: абсолютив (-tvā / -ya)» .

Core W2 ① article (content, no kill-gate). The absolutive (gerund / converb,
"having done X") is an INDECLINABLE verbal form, so its frame is NOT case×number
but the -tvā / -ya ALLOMORPHY: -tvā on a simple (non-compounded) root (kṛtvā,
gatvā), -ya/-tya on a preverb-compounded root (praṇamya, āgatya, vihāya). Whitney
§§989–995.

The corpus TESTS this rule directly: DCS stores preverbs in `lemma.preverbs`, so
each Conv token's surface ending (-tvā vs -ya/-tya) can be cross-tabulated against
whether its lemma carries a preverb. This is an "attested confirms traditional"
measurement — how cleanly the corpus bears out the grammatical rule.

Three layers (C5 §3): ATTESTED — the -tvā/-ya split + the rule cross-tab over the
pinned snapshot; TRADITIONAL — Whitney §§989–995 (the -tvā/-ya allomorphy); the
form is indeclinable, so there is no GENERATED paradigm.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators; seeded sample. Read-only. Emits into sangram/articles/absolutive/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "absolutive" / "data"

SEED = 20260717
SAMPLE_SIZE = 50


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def ending_class(m):
    if m.endswith("tvā"):
        return "tvā"
    if m.endswith("tya"):
        return "ya"        # -tya is the -ya allomorph after a short-vowel root
    if m.endswith("ya"):
        return "ya"
    if m.endswith("am"):
        return "am"
    return "other"


def fine_ending_class(m):
    """MO26 reviewer follow-up (visa card MO26, H1346): "-ya/-tya на 97,8% -
    так сколько -ya и сколько -tya?". ending_class() above deliberately merges
    -tya into "ya" (it IS the -ya allomorph after a short-vowel root — Whitney
    §§989-995 — and that merge stays correct for the main distribution). This
    splits the same merged bucket by literal surface ending for a transparency
    breakdown the reviewer asked for; the two counts sum back to the "ya"
    total from ending_class() by construction."""
    if m.endswith("tya"):
        return "tya"
    if m.endswith("ya"):
        return "ya_pure"
    return None


def has_preverb(pv):
    return bool(pv and pv.strip())


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

    rows = cur.execute(
        "SELECT t.id, t.m_unsandhied, t.lemma, l.preverbs "
        "FROM token t JOIN lemma l ON l.lemma_id = t.lemma_id "
        "WHERE t.feat_verbform='Conv' AND t.m_unsandhied IS NOT NULL"
    ).fetchall()
    total = len(rows)

    ending = Counter()
    crosstab = Counter()  # (ending_class, has_preverb)
    ids_by_class = {}
    fine_ending = Counter()
    fine_crosstab = Counter()  # (fine_ending_class, has_preverb)
    fine_form_counts = {"tya": Counter(), "ya_pure": Counter()}  # (lemma, preverbs, m_unsandhied) -> n
    fine_ids_by_form = {}
    for tid, m, lemma, pv in rows:
        ec = ending_class(m)
        ending[ec] += 1
        if ec in ("tvā", "ya"):
            crosstab[(ec, has_preverb(pv))] += 1
        ids_by_class.setdefault(ec, []).append(tid)

        fc = fine_ending_class(m)
        if fc is not None:
            fine_ending[fc] += 1
            fine_crosstab[(fc, has_preverb(pv))] += 1
            fkey = (lemma, pv or "", m)
            fine_form_counts[fc][fkey] += 1
            fine_ids_by_form.setdefault((fc, lemma, pv or "", m), []).append(tid)

    tva_simple = crosstab[("tvā", False)]
    tva_pref = crosstab[("tvā", True)]
    ya_simple = crosstab[("ya", False)]
    ya_pref = crosstab[("ya", True)]

    # seeded validation sample across all classes
    rng = random.Random(SEED)
    allids = [tid for _, _, _, _ in rows]  # placeholder to keep order deterministic
    allids = sorted(tid for tid, *_ in rows)
    chosen = rng.sample(allids, min(SAMPLE_SIZE, len(allids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, l.preverbs, "
            "x.name, c.ref, s.sent_counter FROM token t "
            "JOIN lemma l ON l.lemma_id=t.lemma_id "
            "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone()
        sample.append(d)

    # MO26 reviewer follow-up (H1346): 5 frequent, distinct examples for each of
    # -tya and -ya (pure), picked by frequency rank rather than "first N" DB
    # order — a dedicated seeded RNG (same SEED constant as the article's
    # validation sample) chooses which attestation of each top-5 form to cite,
    # kept separate from the `rng` above so the pre-existing validation_sample
    # stays bit-identical.
    freq_rng = random.Random(SEED)
    fine_examples = {}
    for fc in ("tya", "ya_pure"):
        top5_keys = [k for k, _ in fine_form_counts[fc].most_common(5)]
        ex_list = []
        for key in top5_keys:
            lemma_k, pv_k, m_k = key
            ids = sorted(fine_ids_by_form[(fc, lemma_k, pv_k, m_k)])
            chosen_tid = freq_rng.choice(ids)
            d2 = cur.execute(
                "SELECT t.id, t.form, t.m_unsandhied, t.lemma, l.preverbs, "
                "x.name, c.ref, s.sent_counter FROM token t "
                "JOIN lemma l ON l.lemma_id=t.lemma_id "
                "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
                "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (chosen_tid,)).fetchone()
            ex_list.append({
                "token_id": d2[0], "form": d2[1], "unsandhied": d2[2], "lemma": d2[3],
                "preverbs": d2[4], "text": d2[5], "chapter_ref": d2[6], "sent_counter": d2[7],
                "form_freq_in_bucket": fine_form_counts[fc][key],
            })
        fine_examples[fc] = ex_list

    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "preverbs",
                    "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "SG-MO-026 «Абсолютив (-tvā/-ya)» — indeclinable converb (core W2 ①, content)",
        "toc_ref": "SG-MO-026",
        "kind": "content article (no kill-gate)",
        "method": "VerbForm=Conv; surface split -tvā vs -ya/-tya; cross-tab vs lemma.preverbs — corpus test of the rule (-tvā↔simple, -ya↔compounded)",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"conv_tokens": total},
        "ending_distribution": dict(ending.most_common()),
        "rule_test": {
            "description": "-tvā ↔ simple root (no preverb); -ya/-tya ↔ preverb-compounded root",
            "tva_simple": tva_simple, "tva_with_preverb": tva_pref,
            "tva_pct_simple": round(100 * tva_simple / (tva_simple + tva_pref), 1),
            "ya_simple": ya_simple, "ya_with_preverb": ya_pref,
            "ya_pct_compounded": round(100 * ya_pref / (ya_simple + ya_pref), 1),
        },
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "ya_tya_split_mo26": {
            "note": "Follow-up split of the merged 'ya' bucket (57,790) into true -ya vs "
                    "-tya surface endings, per reviewer note on visa card MO26 (H1346): "
                    "'-ya/-tya на 97,8% - так сколько -ya и сколько -tya?'. -tya remains "
                    "linguistically the -ya allomorph after a short-vowel root (Whitney "
                    "§§989-995) — this is a surface-form disaggregation for transparency, "
                    "not a change to the traditional rule or to ending_class() above.",
            "tya_tokens": fine_ending["tya"],
            "ya_pure_tokens": fine_ending["ya_pure"],
            "sum_matches_merged_ya_bucket": fine_ending["tya"] + fine_ending["ya_pure"] == ending["ya"],
            "tya_pct_of_conv_total": round(100 * fine_ending["tya"] / total, 1),
            "ya_pure_pct_of_conv_total": round(100 * fine_ending["ya_pure"] / total, 1),
            "tya_pct_of_merged_ya_bucket": round(100 * fine_ending["tya"] / ending["ya"], 1),
            "ya_pure_pct_of_merged_ya_bucket": round(100 * fine_ending["ya_pure"] / ending["ya"], 1),
            "crosstab": {
                "tya_simple": fine_crosstab[("tya", False)],
                "tya_with_preverb": fine_crosstab[("tya", True)],
                "ya_pure_simple": fine_crosstab[("ya_pure", False)],
                "ya_pure_with_preverb": fine_crosstab[("ya_pure", True)],
                "tya_pct_compounded": round(100 * fine_crosstab[("tya", True)] /
                                             (fine_crosstab[("tya", True)] + fine_crosstab[("tya", False)]), 1),
                "ya_pure_pct_compounded": round(100 * fine_crosstab[("ya_pure", True)] /
                                                 (fine_crosstab[("ya_pure", True)] + fine_crosstab[("ya_pure", False)]), 1),
            },
            "examples_seed": SEED,
            "examples_tya_top5": fine_examples["tya"],
            "examples_ya_pure_top5": fine_examples["ya_pure"],
        },
        "limits": {
            "indeclinable": "the absolutive has no case/number — the frame is the -tvā/-ya allomorphy, not a paradigm",
            "surface_classification": "-tvā/-ya split by m_unsandhied ending; the ~2% counter-rule residue is sandhi/lemmatization edge cases, not necessarily real exceptions",
            "am_type": "the rare -am absolutive (Vedic/idiomatic) is counted separately",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    rt = summary["rule_test"]
    print(f"Conv tokens: {total:,}; endings: {dict(ending.most_common())}", file=sys.stderr)
    print(f"RULE: -tvā {rt['tva_pct_simple']}% simple ({tva_simple}/{tva_simple+tva_pref}); "
          f"-ya/-tya {rt['ya_pct_compounded']}% compounded ({ya_pref}/{ya_simple+ya_pref})", file=sys.stderr)
    yt = summary["ya_tya_split_mo26"]
    print(f"MO26 split: -tya {yt['tya_tokens']:,} ({yt['tya_pct_of_conv_total']}%); "
          f"-ya (pure) {yt['ya_pure_tokens']:,} ({yt['ya_pure_pct_of_conv_total']}%); "
          f"sum_matches_merged={yt['sum_matches_merged_ya_bucket']}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
