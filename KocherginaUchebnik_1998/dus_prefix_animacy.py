#!/usr/bin/env python
"""dus_prefix_animacy.py — animacy check for dus-+S nouns (HK-221).

HK-221: "dus-+S: сравнительно немногие наименования лиц; основная масса —
неодушевлённые" — dus-prefixed nouns are comparatively few person-names;
the main mass are inanimate. Uses animacy_lookup.py's lemma-level animacy
classification (built from the DCS m_wordsem -> Sanskrit WordNet sembank,
see that script's docstring) — no compound-contamination risk here (unlike
HK-86's derivational-suffix check): this classifies whole NOUN lemmas by
referent animacy, which doesn't change whether that lemma also occurs
compound-internally elsewhere.

Usage:  python KocherginaUchebnik_1998/dus_prefix_animacy.py [--db PATH]
Writes  hk221_dus_prefix_animacy_stats.json next to this script.
"""
import argparse
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
DEFAULT_ANIMACY = HERE / "animacy_lemma_lookup.json"

DUS_VARIANTS = ("dus", "dur", "duṣ", "duś")  # sandhi variants of the dus- prefix


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--animacy-json", default=str(DEFAULT_ANIMACY))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()
    animacy = json.loads(Path(args.animacy_json).read_text(encoding="utf-8"))
    lc = animacy["lemma_classification"]

    noun_lemmas = [l for (l,) in cur.execute(
        "SELECT DISTINCT lemma FROM token WHERE upos='NOUN'")]
    dus_lemmas = [l for l in noun_lemmas
                  if any(l.startswith(p) and len(l) > len(p) + 1 for p in DUS_VARIANTS)]

    classified = {l: lc.get(l, {}).get("classification", "untagged") for l in dus_lemmas}
    counts = Counter(classified.values())
    animate_ex = sorted(l for l, c in classified.items() if c == "animate")
    inanimate_ex = sorted(l for l, c in classified.items() if c == "inanimate")

    classified_total = counts["animate"] + counts["inanimate"] + counts.get("tied", 0)
    animate_share = round(100 * counts["animate"] / classified_total, 1) if classified_total else None

    out = {
        "instrument": "dus_prefix_animacy.py, reusing animacy_lookup.py's lemma "
                      "classification (H1048/H1047)",
        "dus_prefixed_noun_lemma_candidates": len(dus_lemmas),
        "by_animacy": dict(counts),
        "classified_total": classified_total,
        "animate_share_pct_of_classified": animate_share,
        "untagged_count": counts.get("untagged", 0),
        "animate_examples": animate_ex[:15],
        "inanimate_examples": inanimate_ex[:20],
        "expected_by_hk221": "animate (person) share is a small minority",
        "confirmed": animate_share is not None and animate_share < 30,
    }
    (HERE / "hk221_dus_prefix_animacy_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"dus-prefixed noun lemma candidates: {len(dus_lemmas)}")
    print(f"by animacy: {dict(counts)}")
    print(f"animate share of classified: {animate_share}%")
    print("confirmed:", out["confirmed"])
    print("-> hk221_dus_prefix_animacy_stats.json written")


if __name__ == "__main__":
    main()
