"""H984 -- RQ4 diagnostic item bank builder.

Builds the held-out root pool for the RQ4 evaluation protocol
(docs/RQ4_EVALUATION_PROTOCOL_2026.md Section 4): given a root, the learner
names its Ryad, Tip, and set/anit status. Items must NOT overlap the on-ramp's
own worked examples (data/widget_roots.json ablaut_examples + set_examples --
those are what a learner actually sees in the on-ramp/talmud-02 material), or
the diagnostic would be measuring memorisation, not transfer.

Scope restriction (documented, not hidden): items are drawn ONLY from the four
ablaut rows the on-ramp actually teaches (A1/I1/U1/R1 -- AblautMachine's
`rows` whitelist for the on-ramp). Testing a row the on-ramp never covers
would not be a fair on-ramp-vs-Talmud comparison, since only the Talmud-first
arm would have seen material for it.

Source of truth: data/talmud_appendix1.json (745 roots, the author's own
Ryad/Tip/set catalogue) minus widget_roots.json's worked roots, restricted to
the 4 rows, requiring all three of ryad/tip/set to be non-null (a root with a
gap can't be a fair test item), and requiring a single (non-homonym) sense
(avoids item ambiguity).

Output: 3 pre-registered item sets (pre-test, post-test, retention-test),
matched for Ryad distribution across the 4 rows (protocol Section 4: "same
Ryad/Tip distribution across sets, not identical items").
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "sanskrit-util" / "py"))
from sanskrit_util import to_slp1  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]
APPENDIX1_PATH = REPO_ROOT / "TolchelnikovTalmud_2026" / "data" / "talmud_appendix1.json"
WIDGET_ROOTS_PATH = REPO_ROOT / "TolchelnikovTalmud_2026" / "data" / "widget_roots.json"
FREQUENCY_TSV = REPO_ROOT.parent / "kosha" / "data" / "frequency" / "lemma_frequency.tsv"
OUT_PATH = REPO_ROOT / "TolchelnikovTalmud_2026" / "data" / "rq4_item_bank.json"

ON_RAMP_ROWS = {"A₁", "I₁", "U₁", "R₁"}  # the on-ramp's own AblautMachine `rows` whitelist
ITEMS_PER_SET = 8  # 2 per row x 4 rows, protocol section 4 recommends 8-10
N_SETS = 3  # pre-test, post-test, retention-test


def load_worked_roots() -> set[str]:
    data = json.loads(WIDGET_ROOTS_PATH.read_text(encoding="utf-8"))
    worked = set()
    for key in ("ablaut_examples", "set_examples"):
        for row in data.get(key, []):
            worked.add(row["root"])
    return worked


def load_frequency_ranks() -> dict[str, int]:
    """slp1 -> rank_all, for an optional difficulty-balance hint (not a hard filter)."""
    ranks: dict[str, int] = {}
    if not FREQUENCY_TSV.is_file():
        return ranks
    with FREQUENCY_TSV.open(encoding="utf-8", newline="") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        slp1_idx = header.index("lemma_slp1")
        rank_idx = header.index("rank_all")
        for line in fh:
            cols = line.rstrip("\n").split("\t")
            if len(cols) <= max(slp1_idx, rank_idx):
                continue
            slp1, rank_raw = cols[slp1_idx], cols[rank_idx]
            if slp1 and rank_raw:
                ranks[slp1] = int(rank_raw)
    return ranks


def eligible_candidates() -> list[dict]:
    appendix = json.loads(APPENDIX1_PATH.read_text(encoding="utf-8"))
    worked_roots = load_worked_roots()
    freq_ranks = load_frequency_ranks()

    candidates = []
    for row in appendix["roots"]:
        if row["ryad"] not in ON_RAMP_ROWS:
            continue
        if row["homonym"] is not None:
            continue  # ambiguous headword, not a clean single-answer item
        if not (row["ryad"] and row["tip"] and row["set"]):
            continue  # incomplete tag -- not a fair, gradeable item
        if row["root"] in worked_roots:
            continue  # already seen in the on-ramp / talmud-02 worked material

        try:
            slp1 = to_slp1(row["root"])
        except Exception:
            slp1 = None
        rank_all = freq_ranks.get(slp1) if slp1 else None

        candidates.append(
            {
                "root": row["root"],
                "slp1": slp1,
                "ryad": row["ryad"],
                "tip": row["tip"],
                "set": row["set"],
                "set_code": row["set_code"],
                "whitney_ref": row["whitney_ref"],
                "rank_all": rank_all,
            }
        )
    return candidates


def build_item_bank() -> dict:
    candidates = eligible_candidates()

    by_row: dict[str, list[dict]] = {row: [] for row in ON_RAMP_ROWS}
    for c in candidates:
        by_row[c["ryad"]].append(c)

    # Frequency-sort within each row (rank_all ascending; unranked roots sort last)
    # so the highest-frequency, most-plausibly-encountered roots are drawn first --
    # a Kochergina-stage learner is more likely to have met a common root's forms
    # elsewhere, which is the honest population this instrument targets.
    for row in by_row:
        by_row[row].sort(key=lambda c: (c["rank_all"] is None, c["rank_all"] or 0))

    per_row_needed = ITEMS_PER_SET // len(ON_RAMP_ROWS)  # 2 per row per set
    total_needed_per_row = per_row_needed * N_SETS  # 6 per row across all 3 sets

    shortfall = {row: max(0, total_needed_per_row - len(items)) for row, items in by_row.items()}

    sets = []
    for set_index in range(N_SETS):
        items = []
        for row in sorted(ON_RAMP_ROWS):
            start = set_index * per_row_needed
            end = start + per_row_needed
            items.extend(by_row[row][start:end])
        sets.append(items)

    set_names = ["pre_test", "post_test", "retention_test"]
    return {
        "method": (
            "Roots drawn from Приложение 1 (talmud_appendix1.json), restricted to the "
            "on-ramp's 4 taught rows (A1/I1/U1/R1), excluding widget_roots.json's worked "
            "examples, requiring complete ryad+tip+set tags and no homonym ambiguity. "
            "Frequency-sorted (kosha lemma_frequency.tsv rank_all) within each row; the 3 "
            "sets partition that ranking so no item repeats across sets."
        ),
        "on_ramp_rows": sorted(ON_RAMP_ROWS),
        "items_per_set": ITEMS_PER_SET,
        "candidate_pool_size": len(candidates),
        "shortfall_by_row": shortfall,
        "sets": dict(zip(set_names, sets)),
    }


def main() -> None:
    bank = build_item_bank()
    OUT_PATH.write_text(json.dumps(bank, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    counts = {name: len(items) for name, items in bank["sets"].items()}
    print(f"wrote {OUT_PATH} -- pool={bank['candidate_pool_size']}, sets={counts}, shortfall={bank['shortfall_by_row']}")


if __name__ == "__main__":
    main()
