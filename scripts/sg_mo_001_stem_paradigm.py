#!/usr/bin/env python3
"""SG-MO-001 stem inventory — REAL paradigmatic classification (MG visa A4).

Replaces the lemma-final approximation with a classification grounded in how each
noun *actually declines in the corpus*: each noun lemma is assigned a declension
class by the ending of its attested **Instrumental singular** (the single most
class-diagnostic slot — a-stem -ena, ā-stem -ayā, i-stem -inā, u-stem -unā,
ī-stem -yā, ū-stem -vā, ṛ-stem -rā, consonant/n-stem -ā), with the majority
ending across a lemma's attestations winning. Lemmas with no Ins.Sg attestation
are counted honestly as «не классифицировано» (coverage reported).

C3: pinned snapshot + SHA-256; denominator + per-class token counts. Read-only.
"""
import sqlite3
import sys
import json
import hashlib
import argparse
from pathlib import Path
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "declension-overview" / "data"

# ending → class, checked in order (most specific first)
ENDING_RULES = [
    ("ena", "-a (тематические)"),
    ("ayā", "-ā"),
    ("inā", "-i"),
    ("unā", "-u"),
    ("ṛṇā", "-ṛ"),   # rare
    ("rā", "-ṛ"),
    ("ūvā", "-ū"),
    ("uvā", "-ū"),
    ("vā", "-ū"),
    ("yā", "-ī"),
    ("ñā", "n-основы"),
    ("ṇā", "n-основы"),
    ("nā", "n-основы"),
    ("sā", "s-основы"),
    ("ā", "прочие согласные"),
]


def classify_ending(form):
    if not form:
        return None
    for suf, cls in ENDING_RULES:
        if form.endswith(suf):
            return cls
    return None


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
        print(f"ERROR: DB not found: {db}", file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr)
        return 1
    sha = "skipped" if args.skip_checksum else sha256_file(db)

    where = "t.upos='NOUN' AND t.feat_case IS NOT NULL AND t.feat_case!='Cpd'"
    total = cur.execute(f"SELECT COUNT(*) FROM token t WHERE {where}").fetchone()[0]

    # per-lemma class vote from attested Ins.Sg unsandhied endings
    votes = defaultdict(Counter)
    for lemma_id, form in cur.execute(
        "SELECT lemma_id, m_unsandhied FROM token "
        "WHERE upos='NOUN' AND feat_case='Ins' AND feat_number='Sing' AND m_unsandhied IS NOT NULL"
    ):
        cls = classify_ending(form)
        if cls:
            votes[lemma_id][cls] += 1
    lemma_class = {lid: c.most_common(1)[0][0] for lid, c in votes.items()}

    # token-weight over the whole noun universe by each lemma's paradigmatic class
    class_tokens = Counter()
    classified_tokens = 0
    unclassified_tokens = 0
    for lemma_id, cnt in cur.execute(
        f"SELECT t.lemma_id, COUNT(*) FROM token t WHERE {where} GROUP BY t.lemma_id"
    ):
        cls = lemma_class.get(lemma_id)
        if cls:
            class_tokens[cls] += cnt
            classified_tokens += cnt
        else:
            unclassified_tokens += cnt

    coverage = round(classified_tokens / total, 4)
    dist = {k: {"tokens": v, "share_of_classified": round(v / classified_tokens, 4)}
            for k, v in class_tokens.most_common()}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    summary = {
        "study": "SG-MO-001 — REAL paradigmatic stem classification (attested Ins.Sg ending)",
        "method": "each noun lemma classified by the majority ending of its attested Instrumental singular; token-weighted over the noun universe; lemmas without Ins.Sg attestation counted as unclassified",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
        },
        "denominator_inflected_noun_tokens": total,
        "classified_tokens": classified_tokens,
        "unclassified_tokens": unclassified_tokens,
        "coverage_of_universe": coverage,
        "n_lemmas_classified": len(lemma_class),
        "class_distribution_over_classified": dist,
        "note": "класс определён по РЕАЛЬНОЙ атестованной парадигме (окончание Ins.Sg), не по финали цитатной леммы; доли — от классифицированного подмножества (покрытие явно указано)",
    }
    (OUT_DIR / "stem_paradigm_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    con.close()

    print(f"denominator: {total:,}", file=sys.stderr)
    print(f"classified: {classified_tokens:,} ({coverage*100:.1f}%); "
          f"unclassified: {unclassified_tokens:,}; lemmas classified: {len(lemma_class):,}", file=sys.stderr)
    print("class dist (of classified):", file=sys.stderr)
    for k, v in class_tokens.most_common():
        print(f"  {k}: {v:,} ({v/classified_tokens*100:.1f}%)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
