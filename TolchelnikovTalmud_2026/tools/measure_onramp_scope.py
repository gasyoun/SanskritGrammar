"""Measure PM6 — on-ramp scope transfer (digital-Sanskrit-pedagogy field metric register).

PM6 asks: of Приложение 1's root catalogue, how much do the **4 ablaut rows the on-ramp
actually teaches** (A₁/I₁/U₁/R₁) cover — by type, and by DCS token mass? The type figure
says how much of the catalogue a learner can classify after the on-ramp; the token figure
says how much of *running text* that corresponds to. Reporting only the first would let an
on-ramp completion claim read as broader than it is.

Both figures are needed because they can diverge: if the taught rows happened to hold the
high-frequency roots, token coverage would run far ahead of type coverage and the on-ramp
would be a frequency shortcut. Measured 27-07-2026 they are near-identical (56.5 % vs
56.2 %), so the on-ramp buys scope roughly proportional to its size.

Inputs (all committed):
  - data/talmud_appendix1.json      745 roots, Ряд/Тип/seṭ-tagged
  - ../kosha/data/frequency/lemma_frequency.tsv   DCS token counts per lemma
  - sanskrit-util `to_slp1`         the canonical IAST→SLP1 transliteration

The join MUST go through `to_slp1`: the catalogue spells roots in IAST and the frequency
table keys on SLP1, so a direct string join silently keeps only the diacritic-free roots
(29 % of the catalogue) and reports a token share inflated by ~26 pp.

Usage:
    python TolchelnikovTalmud_2026/tools/measure_onramp_scope.py [--freq <lemma_frequency.tsv>]
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "sanskrit-util" / "py"))
from sanskrit_util import to_slp1  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
APPENDIX1_PATH = REPO_ROOT / "TolchelnikovTalmud_2026" / "data" / "talmud_appendix1.json"
DEFAULT_FREQUENCY_TSV = REPO_ROOT.parent / "kosha" / "data" / "frequency" / "lemma_frequency.tsv"

# The rows the on-ramp teaches — AblautMachine's `rows` whitelist for the on-ramp,
# the same restriction the RQ4 item bank uses.
ON_RAMP_ROWS = {"A₁", "I₁", "U₁", "R₁"}


def load_counts(freq_tsv: Path) -> dict[str, int]:
    """slp1 lemma -> DCS token count (max, when a lemma repeats across grammar tags)."""
    counts: dict[str, int] = {}
    if not freq_tsv.is_file():
        raise SystemExit(f"frequency table not found: {freq_tsv}")
    with freq_tsv.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh, delimiter="\t")
        for row in reader:
            lemma = row.get("lemma_slp1")
            raw = row.get("count_all")
            if not lemma or not raw:
                continue
            try:
                count = int(raw)
            except ValueError:
                continue
            if count > counts.get(lemma, 0):
                counts[lemma] = count
    return counts


def slp1_candidates(root_row: dict) -> set[str]:
    """Every SLP1 spelling worth trying for one catalogue root."""
    out: set[str] = set()
    for spelling in [root_row.get("root"), *(root_row.get("whitney_spellings") or [])]:
        if not spelling:
            continue
        try:
            out.add(to_slp1(spelling))
        except Exception:  # noqa: BLE001 — an unconvertible spelling is a miss, not a crash
            continue
    return out


def measure(freq_tsv: Path) -> dict:
    roots = json.loads(APPENDIX1_PATH.read_text(encoding="utf-8"))["roots"]
    counts = load_counts(freq_tsv)

    n_total = len(roots)
    n_on_ramp = sum(1 for r in roots if r.get("ryad") in ON_RAMP_ROWS)
    tagged = [r for r in roots if r.get("ryad") and r.get("tip") and r.get("set")]
    n_tagged_on_ramp = sum(1 for r in tagged if r.get("ryad") in ON_RAMP_ROWS)

    joined = 0
    tokens_all = 0
    tokens_on_ramp = 0
    for row in roots:
        best = max((counts[c] for c in slp1_candidates(row) if c in counts), default=None)
        if best is None:
            continue
        joined += 1
        tokens_all += best
        if row.get("ryad") in ON_RAMP_ROWS:
            tokens_on_ramp += best

    return {
        "roots_total": n_total,
        "roots_on_ramp": n_on_ramp,
        "type_coverage_pct": round(100 * n_on_ramp / n_total, 1),
        "roots_fully_tagged": len(tagged),
        "roots_fully_tagged_on_ramp": n_tagged_on_ramp,
        "roots_joined_to_frequency": joined,
        "join_rate_pct": round(100 * joined / n_total, 1),
        "tokens_joined_total": tokens_all,
        "tokens_on_ramp": tokens_on_ramp,
        "token_coverage_pct": round(100 * tokens_on_ramp / tokens_all, 1) if tokens_all else None,
        "on_ramp_rows": sorted(ON_RAMP_ROWS),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--freq", type=Path, default=DEFAULT_FREQUENCY_TSV,
                        help="path to kosha lemma_frequency.tsv")
    parser.add_argument("--json", action="store_true", help="emit the raw result dict")
    args = parser.parse_args()

    result = measure(args.freq)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print("PM6 — on-ramp scope transfer")
    print(f"  taught rows            : {', '.join(result['on_ramp_rows'])}")
    print(f"  type coverage          : {result['roots_on_ramp']}/{result['roots_total']} "
          f"= {result['type_coverage_pct']}%")
    print(f"  (fully tagged subset)  : {result['roots_fully_tagged_on_ramp']}/"
          f"{result['roots_fully_tagged']}")
    print(f"  join to DCS frequency  : {result['roots_joined_to_frequency']}/{result['roots_total']} "
          f"= {result['join_rate_pct']}%")
    print(f"  token-mass coverage    : {result['tokens_on_ramp']:,}/{result['tokens_joined_total']:,} "
          f"= {result['token_coverage_pct']}%")


if __name__ == "__main__":
    main()
