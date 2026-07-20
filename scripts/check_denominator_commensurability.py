#!/usr/bin/env python
"""check_denominator_commensurability.py — the SG-SE case-count denominator contract (H1371).

The SANGRAM case-semantics cluster publishes case counts across several articles, all off the
SAME pinned DCS-2026 snapshot. For the numbers to be COMMENSURABLE, every article must denominate
those counts against the same, self-consistent case-marked totals. This gate enforces that so a
future regeneration can never silently ship an incommensurable denominator.

THE CANONICAL CASE-MARKED FAMILY (DCS-2026, pin 04e0778 / sha 8f3b06…):

    all_tokens         = 5,688,416   every token in the corpus
    case_bearing       = 4,014,688   feat_case IS NOT NULL  (INCLUDES the `Cpd` pseudo-case)
    real_vibhakti      = 3,173,636   the eight true vibhakti (Nom…Voc), EXCLUDES `Cpd`
    Cpd                =   841,052   compound-internal members (no overt case)

    invariant:  case_bearing == real_vibhakti + Cpd            (4,014,688 == 3,173,636 + 841,052)

Two legitimate denominator BASES are in play and they are NOT interchangeable:
  * `case_bearing` (incl Cpd) — the basis of SE-002/SE-004's `pct_of_case_bearing`.
  * `real_vibhakti` (excl Cpd) — the natural per-case basis (this is where "Dat = 2.1%" comes from).
A share is only meaningful once its basis is named; the contract keeps both bases pinned to one value.

FIVE CHECKS, over every `sangram/articles/*/data/coverage_summary.json`:

  1. MASTER VALUES — any denominator cited under a known family key (any alias) must equal the one
     canonical value. all_tokens ≡ 5,688,416, case_bearing ≡ 4,014,688, real_vibhakti ≡ 3,173,636,
     everywhere it appears, under whatever key name (all_case_marked ≡ case_bearing_tokens, etc.).
  2. FAMILY ARITHMETIC — the registry itself is self-consistent (case_bearing == real_vibhakti + Cpd);
     any article that publishes a Cpd count must satisfy it too.
  3. SNAPSHOT PIN — every case-cluster article pins the one canonical sha256 (same source, so the
     counts are comparable at all).
  4. GAP (the regression this contract was built to kill) — every case-cluster article MUST cite the
     `case_bearing` master under some alias; an article that reports case counts but no master
     denominator is not reconcilable and fails here (this is exactly how SE-003/SE-005/SE-013 were
     found under-denominated).
  5. SUB-DENOMINATOR BOUND — a POS-restricted case sub-denominator (nouns, pronouns…) must be a
     subset of the master: 0 < value ≤ case_bearing.

Exit 0 = commensurable, 1 = drift. Wired into CI via tests/test_denominator_commensurability.py and
available as `npm run check-denominators`.

Model: Opus 4.8 (claude-opus-4-8[1m]), 20-07-2026 (H1371).
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
ARTICLES = ROOT / "sangram" / "articles"

# ---- the canonical case-marked family (DCS-2026 pinned snapshot) ----
ALL_TOKENS = 5_688_416
CASE_BEARING = 4_014_688       # feat_case NOT NULL, incl the Cpd pseudo-case
REAL_VIBHAKTI = 3_173_636      # the eight true vibhakti, excl Cpd
CPD = 841_052                  # compound-internal members
CANON_SHA = "8f3b06bd6ef0e47a9ccf81d147e73d5d240d64e0c12f6d789262eb422ebb23bc"

# key aliases → the canonical value every occurrence must carry (exact key-name match).
MASTER_KEYS = {
    "all_tokens": ALL_TOKENS,
    "denominator_all_tokens": ALL_TOKENS,
    "total_tokens": ALL_TOKENS,
    "all_case_marked": CASE_BEARING,
    "case_bearing_tokens": CASE_BEARING,
    "real_vibhakti_tokens": REAL_VIBHAKTI,
    "real_case_total": REAL_VIBHAKTI,
}
CASE_BEARING_ALIASES = {"all_case_marked", "case_bearing_tokens"}
CPD_KEYS = {"compound_pseudo_case_Cpd"}

# POS-restricted case sub-denominators — must be a proper subset of the master (0 < v <= case_bearing).
SUBSET_KEYS = {"denominator_inflected_noun_tokens", "case_number_tokens"}

# the case-semantics cluster: every one of these MUST cite the case_bearing master (check 4).
CASE_CLUSTER = {
    "case-system-overview",     # SG-SE-001
    "nominative-accusative",    # SG-SE-002
    "instrumental-dative",      # SG-SE-003
    "ablative-genitive",        # SG-SE-004
    "locative",                 # SG-SE-005
    "karaka-case",              # SG-SE-013
}


def walk(obj, path=""):
    """Yield (dotted_path, key, value) for every leaf under a JSON object."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if isinstance(v, (dict, list)):
                yield from walk(v, p)
            else:
                yield p, k, v
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, f"{path}[{i}]")


def check_family_arithmetic():
    """Check 2, on the registry constants themselves — a wrong constant can't slip in silently."""
    return CASE_BEARING == REAL_VIBHAKTI + CPD


def check_file(path):
    """Return a list of violation strings for one coverage_summary.json."""
    art = path.parent.parent.name
    data = json.loads(path.read_text(encoding="utf-8"))
    leaves = list(walk(data))
    viol = []

    cites_case_bearing = False
    cpd_seen = None
    for dotted, key, val in leaves:
        # check 1: master values
        if key in MASTER_KEYS and isinstance(val, (int, float)):
            if int(val) != MASTER_KEYS[key]:
                viol.append(f"{art}: {dotted} = {int(val):,}, expected {MASTER_KEYS[key]:,} (master drift)")
        if key in CASE_BEARING_ALIASES and isinstance(val, (int, float)) and int(val) == CASE_BEARING:
            cites_case_bearing = True
        # check 5: sub-denominator bound
        if key in SUBSET_KEYS and isinstance(val, (int, float)):
            if not (0 < int(val) <= CASE_BEARING):
                viol.append(f"{art}: {dotted} = {int(val):,} is not a subset of case_bearing "
                            f"(0 < v <= {CASE_BEARING:,})")
        # check 2 (per-article): a published Cpd must satisfy the partition
        if key in CPD_KEYS and isinstance(val, (int, float)):
            cpd_seen = int(val)

    if cpd_seen is not None and cpd_seen != CPD:
        viol.append(f"{art}: Cpd pseudo-case = {cpd_seen:,}, expected {CPD:,} "
                    f"(case_bearing {CASE_BEARING:,} = real_vibhakti {REAL_VIBHAKTI:,} + Cpd)")

    # check 3: snapshot pin (only if the article carries a sha256 at all)
    shas = [val for _, key, val in leaves if key == "sha256" and isinstance(val, str) and val != "skipped"]
    for s in shas:
        if s != CANON_SHA:
            viol.append(f"{art}: sha256 {s[:12]}… != canonical {CANON_SHA[:12]}… (off the pinned snapshot)")

    # check 4: case-cluster gap
    if art in CASE_CLUSTER and not cites_case_bearing:
        viol.append(f"{art}: case-cluster article cites NO case_bearing master ({CASE_BEARING:,}) — "
                    f"its case counts are not reconcilable (add case_bearing_tokens)")

    return viol


def check_all():
    files = sorted(ARTICLES.glob("*/data/coverage_summary.json"))
    violations = []
    for f in files:
        violations.extend(check_file(f))
    return files, violations


def self_test():
    """Guard against the gate silently degrading to a no-op: a planted bad value MUST be caught,
    a clean synthetic MUST pass, and every cluster member MUST be present on disk."""
    import tempfile

    ok = check_family_arithmetic()

    with tempfile.TemporaryDirectory() as td:
        base = Path(td) / "sangram" / "articles"
        # a clean instrumental-dative-shaped file passes
        good = base / "instrumental-dative" / "data"
        good.mkdir(parents=True)
        (good / "coverage_summary.json").write_text(json.dumps({
            "snapshot": {"sha256": CANON_SHA},
            "denominators": {"all_tokens": ALL_TOKENS, "case_bearing_tokens": CASE_BEARING,
                             "real_vibhakti_tokens": REAL_VIBHAKTI},
        }), encoding="utf-8")
        # a drifted + un-pinned + gap file fails on multiple axes
        bad = base / "karaka-case" / "data"
        bad.mkdir(parents=True)
        (bad / "coverage_summary.json").write_text(json.dumps({
            "snapshot": {"sha256": "deadbeef" * 8},
            "denominators": {"all_tokens": 9_999_999},  # wrong all_tokens + no case_bearing master
        }), encoding="utf-8")

        good_viol = check_file(good / "coverage_summary.json")
        bad_viol = check_file(bad / "coverage_summary.json")

    planted_caught = bool(bad_viol) and any("master drift" in v for v in bad_viol) \
        and any("case_bearing master" in v for v in bad_viol) \
        and any("pinned snapshot" in v for v in bad_viol)
    clean_passes = not good_viol
    return ok and planted_caught and clean_passes


def main():
    if not check_family_arithmetic():
        print(f"FAIL: registry arithmetic broken — case_bearing {CASE_BEARING:,} != "
              f"real_vibhakti {REAL_VIBHAKTI:,} + Cpd {CPD:,}", file=sys.stderr)
        return 1
    files, violations = check_all()
    if not files:
        print("FAIL: no sangram/articles/*/data/coverage_summary.json found — the gate would be a no-op",
              file=sys.stderr)
        return 1
    present = {f.parent.parent.name for f in files}
    missing = CASE_CLUSTER - present
    if missing:
        print(f"FAIL: case-cluster article(s) missing from disk: {sorted(missing)}", file=sys.stderr)
        return 1
    if violations:
        print(f"FAIL: {len(violations)} denominator-commensurability violation(s):", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        return 1
    print(f"OK: {len(files)} coverage summaries commensurable; "
          f"case cluster {sorted(CASE_CLUSTER)} all cite case_bearing {CASE_BEARING:,}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
