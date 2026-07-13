"""Retroactive H327 review pass: classify the 128 exact=false pairs in matches.json.

Reads scripts/data/matches.json, diffs each near-match pair's text, and writes a
verdict + note to scripts/data/matches_review.tsv. Heuristic, not exhaustive:
- spelling_variant: short, localized character-level diff (typical sandhi/OCR variant)
- length_mismatch: one side is a truncated/extended run of the other (extraction boundary)
- low_similarity: broad, non-localized diff at a low score (candidate false positive)
"""
import csv
import difflib
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


def classify(a_text, b_text, score):
    len_a, len_b = len(a_text), len(b_text)
    len_ratio = min(len_a, len_b) / max(len_a, len_b) if max(len_a, len_b) else 1.0
    sm = difflib.SequenceMatcher(None, a_text, b_text)
    opcodes = [op for op in sm.get_opcodes() if op[0] != "equal"]
    if len_ratio < 0.85:
        return "length_mismatch", f"len {len_a} vs {len_b} (ratio {len_ratio:.2f})"
    if len(opcodes) <= 3 and score >= 0.85:
        spans = "; ".join(
            f"{a_text[i1:i2]!r}->{b_text[j1:j2]!r}" for tag, i1, i2, j1, j2 in opcodes
        )
        return "spelling_variant", spans or "no-op-diff"
    return "low_similarity", f"{len(opcodes)} diff spans, score {score:.3f}"


def main():
    with open("scripts/data/matches.json", encoding="utf-8") as f:
        data = json.load(f)
    near = [m for m in data if not m.get("exact", True)]
    rows = []
    for m in near:
        a, b = m["a"], m["b"]
        verdict, note = classify(a["text"], b["text"], m["score"])
        rows.append(
            {
                "a_id": a["id"],
                "b_id": b["id"],
                "score": round(m["score"], 3),
                "script": m["script"],
                "verdict": verdict,
                "note": note,
                "a_text": a["text"],
                "b_text": b["text"],
            }
        )

    with open("scripts/data/matches_review.tsv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["a_id", "b_id", "score", "script", "verdict", "note", "a_text", "b_text"],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    import collections

    counts = collections.Counter(r["verdict"] for r in rows)
    print(f"{len(rows)} near-matches reviewed:")
    for verdict, n in counts.most_common():
        print(f"  {verdict}: {n}")


if __name__ == "__main__":
    main()
