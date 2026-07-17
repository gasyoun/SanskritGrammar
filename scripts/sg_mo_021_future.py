#!/usr/bin/env python3
"""SG-MO-021 «Будущее время и кондиционал» — the future and the conditional.

Core W2 ① article (content, no kill-gate). The future closes the finite tense
system: alongside present (SG-MO-013), imperfect (SG-MO-016), aorist (SG-MO-018)
and perfect (SG-MO-017), the future is NATIVELY tagged in DCS (`Tense=Fut`), so —
like the imperfect and passive — it is directly measurable.

The article's spine is the simple-vs-periphrastic contrast the C2 sketch calls for,
and DCS separates it natively:
  - SIMPLE (s-)future — root + -sya-/-iṣya- + primary endings (kariṣyati, bhaviṣyati):
    `feat_formation` NULL under Tense=Fut.
  - PERIPHRASTIC future — agent noun in -tṛ + auxiliary (kartā, bhavitā "will be"):
    `feat_formation='peri'` under Tense=Fut.
  - CONDITIONAL — the counterfactual "would have" (akariṣyat): augment + -sya- +
    secondary endings; DCS tags it `feat_mood='Cond'` within Tense=Fut.
  - FUTURE PARTICIPLE — VerbForm=Part & Tense=Fut (kariṣyant-), counted separately.

Three layers (C5 §3): ATTESTED — the future's distribution (simple/peri, person,
mood) over the pinned snapshot; TRADITIONAL — root + -sya-/-iṣya- / -tṛ + as
(Whitney §§931–949).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators + Wilson CI on a headline share; seeded sample. Read-only. Emits into
sangram/articles/future/data/.
"""
import argparse
import csv
import hashlib
import json
import math
import random
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "future" / "data"

FIN = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
       "AND feat_person IS NOT NULL")
FINFUT = f"{FIN} AND feat_tense='Fut'"

SEED = 20260717
SAMPLE_SIZE = 50


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


def dist(cur, col, where, total):
    out = {}
    for v, c in cur.execute(
            f"SELECT {col}, COUNT(*) FROM token WHERE {where} GROUP BY {col} ORDER BY COUNT(*) DESC"):
        out[v if v is not None else "∅"] = {"tokens": c, "share": round(c / total, 4)}
    return out


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
    fin_fut = cur.execute(f"SELECT COUNT(*) FROM token WHERE {FINFUT}").fetchone()[0]

    # simple vs periphrastic (feat_formation='peri')
    peri = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINFUT} AND feat_formation='peri'").fetchone()[0]
    simple = fin_fut - peri
    # conditional (feat_mood='Cond') within Fut
    cond = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINFUT} AND feat_mood='Cond'").fetchone()[0]
    # future participle
    fut_part = cur.execute(
        "SELECT COUNT(*) FROM token WHERE upos='VERB' AND feat_verbform='Part' "
        "AND feat_tense='Fut'").fetchone()[0]

    person = dist(cur, "feat_person", FINFUT, fin_fut)
    number = dist(cur, "feat_number", FINFUT, fin_fut)
    mood = dist(cur, "feat_mood", FINFUT, fin_fut)
    first = person.get("1", {}).get("tokens", 0)
    third = person.get("3", {}).get("tokens", 0)

    top = cur.execute(
        f"SELECT m_unsandhied, lemma, COUNT(*) c FROM token WHERE {FINFUT} "
        f"AND m_unsandhied IS NOT NULL GROUP BY m_unsandhied, lemma ORDER BY c DESC LIMIT 15").fetchall()
    top_peri = cur.execute(
        f"SELECT m_unsandhied, lemma, COUNT(*) c FROM token WHERE {FINFUT} AND feat_formation='peri' "
        f"AND m_unsandhied IS NOT NULL GROUP BY m_unsandhied, lemma ORDER BY c DESC LIMIT 8").fetchall()

    ids = [r[0] for r in cur.execute(f"SELECT id FROM token WHERE {FINFUT}")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        sample.append(cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.feat_person, t.feat_number, "
            "t.feat_formation, t.feat_mood, x.name, c.ref, s.sent_counter FROM token t "
            "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone())
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "person", "number",
                    "formation", "mood", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "SG-MO-021 «Будущее время и кондиционал» — future + conditional (core W2 ①, content)",
        "toc_ref": "SG-MO-021",
        "kind": "content article (no kill-gate) — closes the finite tense system",
        "method": "finite verbs with Tense=Fut — natively tagged (like the imperfect); simple vs periphrastic separated by feat_formation='peri'; conditional by feat_mood='Cond'; future participle (VerbForm=Part & Tense=Fut) counted separately",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {
            "finite_total": fin_total, "finite_future": fin_fut,
            "finite_future_share": round(fin_fut / fin_total, 4),
            "simple_future": simple, "periphrastic_future": peri,
            "periphrastic_share_of_future": round(peri / fin_fut, 4),
            "conditional": cond, "future_participle": fut_part,
        },
        "future_share_ci95": {"k": fin_fut, "n": fin_total, "ci95": wilson_ci(fin_fut, fin_total)},
        "periphrastic_share_ci95": {"k": peri, "n": fin_fut, "ci95": wilson_ci(peri, fin_fut)},
        "person": person, "number": number, "mood": mood,
        "first_person_share_ci95": {"k": first, "n": fin_fut, "ci95": wilson_ci(first, fin_fut)},
        "third_person_share_ci95": {"k": third, "n": fin_fut, "ci95": wilson_ci(third, fin_fut)},
        "top_forms": [{"form": m, "lemma": l, "tokens": c} for m, l, c in top],
        "top_periphrastic": [{"form": m, "lemma": l, "tokens": c} for m, l, c in top_peri],
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "conditional_rare": "the conditional (feat_mood=Cond) is very rare (340); it is the counterfactual 'would have', not a plain future",
            "periphrastic_via_formation": "simple vs periphrastic rests on feat_formation='peri'; the periphrastic future (-tṛ + as) shares the -tṛ agent-noun shape with the periphrastic PERFECT — DCS separates them by Tense (Fut vs Past), the tag we trust",
            "future_participle_separate": "the future participle (VerbForm=Part & Tense=Fut) is counted apart from the finite future",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"finite {fin_total:,}; finite future {fin_fut:,} ({100*fin_fut/fin_total:.2f}%)", file=sys.stderr)
    print(f"simple {simple:,} ({100*simple/fin_fut:.1f}%); periphrastic {peri:,} ({100*peri/fin_fut:.1f}%); "
          f"conditional {cond}; future participle {fut_part:,}", file=sys.stderr)
    print(f"person: {[(k, v['share']) for k, v in person.items()]}", file=sys.stderr)
    print(f"top: {[(x['form'], x['tokens']) for x in summary['top_forms'][:6]]}", file=sys.stderr)
    print(f"top peri: {[(x['form'], x['tokens']) for x in summary['top_periphrastic'][:5]]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
