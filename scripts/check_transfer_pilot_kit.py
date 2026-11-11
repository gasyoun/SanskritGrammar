#!/usr/bin/env python3
"""H8030 acceptance gate for the reading-transfer pilot kit (docs/teaching-pilot/).

Fail-closed structural checks; linguistic review is OUT of scope here and stays
PENDING (machine checks never substitute for it — protocol §3/§10).

Checks
  1  manifest shape: 3 sets, 30 items, 10/10/10, unique ids/surfaces/members-pair
  2  set disjointness by item_id, surface and members pair
  3  held-out leakage: no held-out surface/members in worked|practice rows or in
     any learner-visible answer-key row; held-out key rows are examiner-only
  4  answer key: exactly one row per item, full coverage, provenance vs
     gold_ladder_30.tsv (surface+members+type must match the cited gold row)
  5  RESULTS_PENDING.md: zero data rows while status is PENDING
  6  protocol: every proposed parameter carries its PROPOSED/approval label and
     the pre-study approval checklist exists
  7  canary: pinned golden rows (split rule idx%3, first worked item)

Exit 0 = all green; exit 1 = first failure line printed.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KIT = ROOT / "docs" / "teaching-pilot"
ITEMS = KIT / "transfer_pilot_items.tsv"
KEY = KIT / "transfer_pilot_answer_key.tsv"
RESULTS = KIT / "RESULTS_PENDING.md"
PROTOCOL = KIT / "READING_TRANSFER_PILOT_PROTOCOL_2026.md"
GOLD = ROOT / "sangram" / "data" / "samasa_ladder" / "gold_ladder_30.tsv"

SETS = ("worked", "practice", "heldout")
CANARY_COUNTS = {"worked": 10, "practice": 10, "heldout": 10}
CANARY_FIRST_WORKED = ("W01", "rājendra")  # idx 0 of gold -> worked (idx % 3 == 0)


def _rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def check() -> list[str]:
    errs: list[str] = []
    for p in (ITEMS, KEY, RESULTS, PROTOCOL, GOLD):
        if not p.exists():
            return [f"MISSING FILE: {p.relative_to(ROOT)}"]

    items, key, gold = _rows(ITEMS), _rows(KEY), _rows(GOLD)
    gold_by_idx = {i: r for i, r in enumerate(gold, start=1)}  # gold_row_index = 1-based
    # manifest carries no answers: members come from the key
    members_by_id = {r["item_id"]: r.get("members", "") for r in key}

    def pair(row: dict) -> str:
        return members_by_id.get(row["item_id"], row["surface"])

    # 1 shape
    if len(items) != 30:
        errs.append(f"manifest has {len(items)} items, expected 30")
    seen_id: set[str] = set()
    by_set: dict[str, list[dict]] = {s: [] for s in SETS}
    for r in items:
        if r["set"] not in SETS:
            errs.append(f"unknown set {r['set']!r} on {r['item_id']}")
            continue
        if r["item_id"] in seen_id:
            errs.append(f"duplicate item_id {r['item_id']}")
        seen_id.add(r["item_id"])
        by_set[r["set"]].append(r)
    for s, n in CANARY_COUNTS.items():
        if len(by_set[s]) != n:
            errs.append(f"set {s}: {len(by_set[s])} items, expected {n}")

    # 2 disjointness
    for field in ("surface", "members_pair"):
        seen: dict[str, str] = {}
        for r in items:
            key_v = r["surface"] if field == "surface" else pair(r)
            if key_v in seen and seen[key_v] != r["set"]:
                errs.append(f"DISJOINTNESS: {field} {key_v!r} in {seen[key_v]} and {r['set']}")
            seen.setdefault(key_v, r["set"])

    # 3 leakage
    held_surfaces = {r["surface"] for r in by_set["heldout"]}
    held_pairs = {pair(r) for r in by_set["heldout"]}
    for s in ("worked", "practice"):
        for r in by_set[s]:
            if r["surface"] in held_surfaces:
                errs.append(f"LEAKAGE: held-out surface {r['surface']} in {s}")
            if pair(r) in held_pairs:
                errs.append(f"LEAKAGE: held-out members pair in {s} ({r['item_id']})")
    for r in key:
        vis = r["visibility"]
        if r["set"] == "heldout" and vis != "examiner-only":
            errs.append(f"LEAKAGE: held-out key row {r['item_id']} visibility={vis}")
        if r["set"] in ("worked", "practice"):
            if vis != "learner-visible":
                errs.append(f"key visibility {r['item_id']} = {vis}, expected learner-visible")
            if r["surface"] in held_surfaces:
                errs.append(f"LEAKAGE: held-out surface in learner-visible key row {r['item_id']}")

    # 4 key coverage + provenance
    if len(key) != len(items):
        errs.append(f"key has {len(key)} rows, manifest has {len(items)}")
    key_ids = [r["item_id"] for r in key]
    if sorted(key_ids) != sorted(seen_id):
        errs.append("key item_id set != manifest item_id set")
    item_by_id = {r["item_id"]: r for r in items}
    for r in key:
        m = item_by_id.get(r["item_id"])
        if m is None:
            continue
        if m["surface"] != r["surface"]:
            errs.append(f"key/manifest surface mismatch {r['item_id']}")
        gi = m.get("gold_row_index", "")
        g = gold_by_idx.get(int(gi.replace("gold_r", ""))) if gi.startswith("gold_r") else None
        if g is None:
            errs.append(f"{r['item_id']}: bad gold provenance {gi!r}")
            continue
        if (g["surface"], g["members"], g["type"]) != (r["surface"], r["members"], r["type"]):
            errs.append(f"{r['item_id']}: key row diverges from cited gold row {gi}")
        if not r.get("alternative_status"):
            errs.append(f"{r['item_id']}: alternative_status empty (must be explicit)")

    # 5 blank results
    txt = RESULTS.read_text(encoding="utf-8")
    data_rows = [ln for ln in txt.splitlines() if ln.startswith("| R-")]
    if data_rows:
        errs.append(f"RESULTS_PENDING.md is not blank: {len(data_rows)} run row(s)")
    if "INCONCLUSIVE" not in txt:
        errs.append("RESULTS_PENDING.md missing INCONCLUSIVE status")

    # 6 protocol labels
    ptxt = PROTOCOL.read_text(encoding="utf-8")
    for label in ("Sample size", "Scoring rubric", "Retention interval", "Expansion threshold"):
        if label not in ptxt:
            errs.append(f"protocol missing parameter {label!r}")
    if ptxt.count("**PROPOSED — approval required**") < 4:
        errs.append("protocol: fewer than 4 PROPOSED parameter labels")
    if "approval checklist" not in ptxt:
        errs.append("protocol missing pre-study approval checklist")
    if "H8028" not in ptxt:
        errs.append("protocol does not name the upstream approved-pack dependency (H8028)")
    if "consent" not in ptxt.lower() or "152-FZ" not in ptxt:
        errs.append("protocol missing consent/privacy procedures")

    # 7 canary
    w = by_set["worked"]
    if w and (w[0]["item_id"], w[0]["surface"]) != CANARY_FIRST_WORKED:
        errs.append(f"canary: first worked item is {w[0]['item_id']}/{w[0]['surface']}, "
                    f"expected {CANARY_FIRST_WORKED[0]}/{CANARY_FIRST_WORKED[1]}")
    return errs



def main() -> int:
    errs = check()
    if errs:
        for e in errs:
            print(f"FAIL {e}")
        return 1
    print("PASS transfer-pilot kit: 30 items 10/10/10 disjoint, no held-out leakage, "
          "key complete, results blank/PENDING, PROPOSED labels present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
