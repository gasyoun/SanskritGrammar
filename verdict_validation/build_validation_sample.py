"""build_validation_sample.py — stratified sample for the A65 verdict-validation κ pass (H1041).

Draws n=100 register entries for blind second annotation (A64 two-pass template):
  - ALL fact-flagged entries (verdict_fact in {OVERSTATED, FALSE}) — the finding-bearing set;
  - ALL UNTESTABLE entries — the honesty-bucket boundary is itself a judgment call;
  - a seeded random stratum of TRUE entries per book (Kochergina 20 · Bühler 25 ·
    Ocherk 10 · Konspekt 5) — the base-rate stratum.

Outputs (same directory):
  validation_sample_blind.json — id, book, loc, kind, claim_ru, falsifiable_as, evidence
      (number + ref) — NO verdicts, NO notes (notes carry pass-1 reasoning).
  validation_sample_gold.json  — id -> {verdict_fact, verdict_pedagogy} (pass-1 labels).

Deterministic: seed 20260716; register state = the committed claims.json files.
"""
import json
import random
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
BOOKS = {
    "kochergina": ROOT / "KocherginaUchebnik_1998" / "claims.json",
    "buhler": ROOT / "BuhlerLeitfaden_1923" / "claims.json",
    "ocherk": ROOT / "ZalizniakOcherk_1978" / "claims.json",
    "konspekt": ROOT / "ZalizniakKonspekt_2004" / "claims.json",
}
TRUE_QUOTA = {"kochergina": 20, "buhler": 25, "ocherk": 10, "konspekt": 5}
SEED = 20260716

def norm(v):
    return str(v).upper()

def main():
    rng = random.Random(SEED)
    blind, gold = [], {}
    for book, path in BOOKS.items():
        data = json.loads(path.read_text(encoding="utf-8"))
        entries = data["claims"] if isinstance(data, dict) else data
        flagged = [e for e in entries if norm(e.get("verdict_fact")) in ("OVERSTATED", "FALSE")]
        untestable = [e for e in entries if norm(e.get("verdict_fact")) == "UNTESTABLE"]
        true_pool = sorted(
            (e for e in entries if norm(e.get("verdict_fact")) == "TRUE"),
            key=lambda e: e["id"],
        )
        true_sample = rng.sample(true_pool, min(TRUE_QUOTA[book], len(true_pool)))
        for e in flagged + untestable + true_sample:
            blind.append({
                "id": e["id"],
                "book": book,
                "loc": e.get("loc", ""),
                "kind": e.get("kind", ""),
                "claim_ru": e.get("claim_ru", ""),
                "falsifiable_as": e.get("falsifiable_as", ""),
                "evidence": {"number": e.get("number", ""), "ref": e.get("ref", "")},
            })
            gold[e["id"]] = {
                "verdict_fact": norm(e.get("verdict_fact")),
                "verdict_pedagogy": str(e.get("verdict_pedagogy", "")),
                "book": book,
            }
    blind.sort(key=lambda x: (x["book"], x["id"]))
    out = Path(__file__).resolve().parent
    (out / "validation_sample_blind.json").write_text(
        json.dumps(blind, ensure_ascii=False, indent=1), encoding="utf-8")
    (out / "validation_sample_gold.json").write_text(
        json.dumps(gold, ensure_ascii=False, indent=1), encoding="utf-8")
    from collections import Counter
    print("sampled:", len(blind), Counter(g["verdict_fact"] for g in gold.values()),
          Counter(g["book"] for g in gold.values()))

if __name__ == "__main__":
    main()
