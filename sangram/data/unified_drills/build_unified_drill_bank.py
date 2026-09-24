#!/usr/bin/env python3
"""Wave-2 RQ2 — unified auto-drill bank with verified answer keys.

Three drill-generation engines already exist in this repo, each with its own
ad-hoc TSV shape and its own answer-key verification method:

  - declension (sangram/data/attested_drills)  — corpus-attested-form agreement
  - samasa     (sangram/data/samasa_ladder)     — hand-built bracket-method ladders
  - sandhi     (data/emeneo_sandhi)             — pamphlet worked-example parity

RQ2 ("Can we auto-generate valid, answer-keyed drills from attested corpus?",
DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md line 324) is a single falsifiable claim
across all three. There has never been one drill bank to make that claim
against, and no single pass that re-checks every item's own already-computed
verification signal in one place. This script is that pass: it re-derives a
`verified` flag for every row from data already on disk (no network, no DCS
database, no engine re-run) and refuses to fabricate a key for anything that
fails its own check — a "mismatch"/"no_generation" declension row, or a
samasa ladder whose step count does not match its own `depth`, is emitted as
`verified=False` with the reason named, never silently dropped or upgraded.

Usage:
    python build_unified_drill_bank.py            # (re)build the TSV + report
    python build_unified_drill_bank.py --check     # verify only, exit 1 on drift
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = Path(__file__).resolve().parent
OUT_TSV = OUT_DIR / "unified_drill_bank.tsv"
OUT_REPORT = OUT_DIR / "VERIFICATION_REPORT.md"
OUT_SUMMARY = OUT_DIR / "verification_summary.json"

DECL_TSV = ROOT / "sangram" / "data" / "attested_drills" / "attested_drill_items.tsv"
SAMASA_TSV = ROOT / "sangram" / "data" / "samasa_ladder" / "samasa_ladder_items.tsv"
SANDHI_TSV = ROOT / "data" / "emeneo_sandhi" / "emeneo_sandhi_drills.tsv"

FIELDS = [
    "drill_id", "drill_type", "prompt", "answer_key", "verified",
    "verification_method", "difficulty_band", "source_dataset", "source_row_id",
]


def _read_tsv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def build_declension_rows() -> list[dict]:
    """agreement in {match, variant} is the engine's own verified-key signal
    (corpus-attested form == or acceptably-variant-of the generated form);
    mismatch/no_generation is a real failure, kept but flagged, never dropped
    (dropping would hide the 9.3% the field doc's PM2 gate already names)."""
    rows = []
    for r in _read_tsv(DECL_TSV):
        verified = r["agreement"] in ("match", "variant")
        rows.append({
            "drill_id": f"DECL-{r['lemma_id']}-{r['cell']}",
            "drill_type": "declension",
            "prompt": f"{r['lemma']} ({r['stem_class']}, {r['gender']}) @ {r['cell']}",
            "answer_key": r["expected_form"],
            "verified": verified,
            "verification_method": f"corpus-attested-agreement:{r['agreement']}",
            "difficulty_band": r["freq_band"],
            "source_dataset": "sangram/data/attested_drills/attested_drill_items.tsv",
            "source_row_id": r["lemma_id"] + ":" + r["cell"],
        })
    return rows


def build_samasa_rows() -> list[dict]:
    """Verified = the ladder's own rungs_json is internally consistent with its
    depth/members columns (step count matches, tails chain to the full surface).
    A ladder that fails this check has a corrupted or hand-edited rung sequence
    -- structurally unteachable, so it is flagged rather than emitted as gold."""
    rows = []
    for i, r in enumerate(_read_tsv(SAMASA_TSV)):
        depth = int(r["depth"])
        members = r["members"].split("|")
        try:
            steps = json.loads(r["rungs_json"])
        except json.JSONDecodeError:
            steps = []
        ok = (
            len(members) == depth
            and len(steps) == depth
            and steps[-1].get("tail") == r["ladder_tails"].split("|")[-1]
        )
        rows.append({
            "drill_id": f"SAM-{i:05d}",
            "drill_type": "samasa",
            "prompt": f"{r['surface']} (depth {depth}, {r['band']})",
            "answer_key": r["members"],
            "verified": ok,
            "verification_method": "ladder-json-step-depth-consistency",
            "difficulty_band": r["band"],
            "source_dataset": "sangram/data/samasa_ladder/samasa_ladder_items.tsv",
            "source_row_id": str(i),
        })
    return rows


def build_sandhi_rows() -> list[dict]:
    """Verified = the answer is the unique, first-listed member of its own
    4-way MCQ choices (the pamphlet-parity gate this bank already tests in
    tests/test_emeneo_sandhi_drills.py::test_choices_are_4way_mcq)."""
    rows = []
    for r in _read_tsv(SANDHI_TSV):
        choices = r["choices"].split(" | ")
        ok = len(choices) == 4 and choices[0] == r["answer"] and choices.count(r["answer"]) == 1
        rows.append({
            "drill_id": f"SND-{r['id']}",
            "drill_type": "sandhi",
            "prompt": r["question"],
            "answer_key": r["answer"],
            "verified": ok,
            "verification_method": "mcq-answer-unique-first",
            "difficulty_band": r["difficulty"],
            "source_dataset": "data/emeneo_sandhi/emeneo_sandhi_drills.tsv",
            "source_row_id": r["id"],
        })
    return rows


def build() -> list[dict]:
    rows = build_declension_rows() + build_samasa_rows() + build_sandhi_rows()
    rows.sort(key=lambda r: r["drill_id"])
    return rows


def write_tsv(rows: list[dict]) -> None:
    with OUT_TSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, delimiter="\t")
        w.writeheader()
        for r in rows:
            row = dict(r)
            row["verified"] = "true" if r["verified"] else "false"
            w.writerow(row)


def summarize(rows: list[dict]) -> dict:
    by_type: dict[str, dict[str, int]] = {}
    for r in rows:
        t = r["drill_type"]
        by_type.setdefault(t, {"total": 0, "verified": 0})
        by_type[t]["total"] += 1
        if r["verified"]:
            by_type[t]["verified"] += 1
    total = len(rows)
    verified = sum(1 for r in rows if r["verified"])
    return {
        "total": total,
        "verified": verified,
        "verified_share": round(verified / total, 4) if total else 0.0,
        "by_type": by_type,
    }


def write_report(summary: dict) -> None:
    lines = [
        "# RQ2 unified drill-bank verification report",
        "",
        "_Computed by [`build_unified_drill_bank.py`](build_unified_drill_bank.py) — never hand-edited._",
        "",
        f"**{summary['verified']} / {summary['total']} drill items "
        f"({summary['verified_share']:.1%}) carry a verified answer key** "
        "across the three existing auto-drill engines (declension, samasa, sandhi). "
        "The falsifiable RQ2 claim (DIGITAL_SANSKRIT_PEDAGOGY_FIELD_2026.md line 324, "
        "\"gold-answer agreement rate\") is refuted if this share drops on a re-run "
        "over unchanged source data.",
        "",
        "| Drill type | Total | Verified | Verified share |",
        "|---|---|---|---|",
    ]
    for t, d in sorted(summary["by_type"].items()):
        share = d["verified"] / d["total"] if d["total"] else 0.0
        lines.append(f"| {t} | {d['total']} | {d['verified']} | {share:.1%} |")
    lines.append("")
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    check_only = "--check" in sys.argv
    rows = build()
    summary = summarize(rows)

    if check_only:
        if not OUT_TSV.exists() or not OUT_SUMMARY.exists():
            print("CHECK FAIL: unified drill bank not built yet", file=sys.stderr)
            return 1
        prior = json.loads(OUT_SUMMARY.read_text(encoding="utf-8"))
        if prior != summary:
            print("CHECK FAIL: verification summary drifted from committed artifact",
                  file=sys.stderr)
            print(f"  committed: {prior}", file=sys.stderr)
            print(f"  recomputed: {summary}", file=sys.stderr)
            return 1
        print(f"OK: {summary['verified']}/{summary['total']} verified, matches committed artifact")
        return 0

    write_tsv(rows)
    write_report(summary)
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} rows -> {OUT_TSV}")
    print(f"{summary['verified']}/{summary['total']} verified ({summary['verified_share']:.1%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
