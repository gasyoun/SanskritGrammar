#!/usr/bin/env python
"""check_claims_consistency.py — guardrail against corpus figures drifting across the
claim registers (H1140, extended H1164).

THREE CHECKS. The first two run over every `*/claims.yml`; the third crosses a repo boundary:

  1. SUPERSESSION (CANONICAL_FIGURES) — a value that was recomputed and replaced must not
     reappear as a LIVE number. Seeded with the aorist: the DCS-2021 tense-code count
     (2,452 / 0.31%) was superseded by the feat_formation count (12,054 / 2.30%); any bare
     citation of the old value (without a correction marker) is drift.

  2. CONSISTENCY (CONSISTENCY_FIGURES) — a figure reused across registers must be cited with
     ONE value everywhere. If the same quantity appears with two different live values, that is
     drift too (this is how the DCS-2021 present count 157,003 and the DCS-2026 present-finite
     count 353,215 got flagged and reconciled). Correction/version-noted blocks are exempt.

  3. CROSS-REPO CONSISTENCY (CROSS_REPO_FIGURES, H2298) — the SAME property as check 2, applied
     across the VisualDCS boundary. Check 2's blind spot was reach, not logic: it reads only
     this repo's registers, so when `verify_claims_dcs.py` computed DCS-2021 Imperfect Active
     from timws.csv codes 4+8 while VisualDCS published 4,442 (code 8 alone, a name-keyed
     last-wins read — H1486), nothing compared them for months. Check 3 compares our own
     committed `claims_dcs_stats.json` against VisualDCS's published contract asset, vendored
     at `data/dcs_published_figures.json` (a workflow checks out ONE repo, so the gate cannot
     read a sibling clone; refresh with `scripts/refresh_published_figures.py`).

A block = the register's header/synthesis, or one `- id:` entry. A block carrying a correction
marker (`refreshed`, `undercounted`, `older …`, a version tag like `DCS-2021`) is treated as
documentation and never counts as a live citation.

Exit 0 = clean, 1 = drift found. Wired into CI via tests/test_claims_consistency.py and available
as `npm run check-claims`.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

CORRECTION_MARKERS = [
    "refresh", "undercount", "superseded", "older", "tense-code", "stale",
    "not the", "was verify_claims", "corrected",
]
# ---- check 1: superseded values that must not reappear as live numbers ----
CANONICAL_FIGURES = [
    {
        "name": "aorist token count",
        "canonical": "12,054 (2.30% of finite verbal; DCS feat_formation)",
        "stale_patterns": [
            r"2,452\s+aorist", r"aorist\s+2,452", r"aorist\s+tokens?\s*=\s*2,452",
            r"0\.31\s*%\s*of\s*(?:781,618\s*)?verbal", r"0,31\s*%\s*глаголь",
        ],
    },
]

# ---- check 2: figures reused across registers must cite only a KNOWN value. `capture` has one
# group = the cited number; `allowed` is the set of canonical value(s) (a figure may have two if
# they are genuinely version-distinguished, e.g. the DCS-2021 vs DCS-2026 present count). Any
# cited value outside `allowed` is drift (a typo, a stale figure, or an un-reconciled recompute).
# Captures are word-boundaried and number-format-specific to avoid false hits (e.g. `\bperfect`
# excludes the "perfect" inside "imperfect"; the present counts are 6-digit XXX,XXX so a 5-digit
# XX,XXX does not match). `allowed` values are comma-stripped, matching _norm().
# DCS-2026 canonical values (MG standardized the whole programme on DCS-2026, denominator =
# 523,738 finite verbal forms). Correction-marked blocks (`refreshed from 61,986 …`) are exempt.
CONSISTENCY_FIGURES = [
    {"name": "perfect tokens",     "capture": r"\bperfect\s+(\d{2,3},\d{3})\b",                 "allowed": {"90001"}},
    {"name": "imperfect tokens",   "capture": r"\bimperfect[ ~]*(\d{2,3},\d{3})\b",             "allowed": {"46695"}},
    {"name": "present tokens",     "capture": r"\bpresent[a-zé\- ]{0,18}?(\d{3},\d{3})\b",       "allowed": {"353215"}},
    {"name": "verbal denominator", "capture": r"(\d{3},\d{3})\s*(?:finite )?verbal\s*(?:form|token|словоуп)", "allowed": {"523738"}},
]


# ---- check 3: the cross-repo figure contract (H2298) ----
# VisualDCS publishes its headline DCS-2021 figures as a committed, list-shaped, unit-tagged
# asset; we vendor a copy so CI needs no sibling clone and no network.
PUBLISHED_FIGURES = ROOT / "data" / "dcs_published_figures.json"
# OUR side is not a hand-copied restatement of theirs — it is the committed output of our own
# `verify_claims_dcs.py`, which reads the same primary source (timws.csv) independently. That
# is what makes this a real comparison rather than a copy checked against a copy.
OUR_DCS2021_STATS = ROOT / "KocherginaUchebnik_1998" / "claims_dcs_stats.json"

# Each row pairs published figure id(s) with the path to OUR independently derived value, and
# pins the timws.csv code set both sides must be summing. `expect_codes` is the
# commensurability lock, and it is the whole reason this gate can be trusted: if VisualDCS
# ever republishes `Imperfect Active` over a different code set, the two numbers stop
# measuring the same thing, and the honest report is "re-adjudicate", not "drift".
#
# The list is deliberately SHORT. A gate seeded with one mismatched pair fires false alarms,
# and the standing response to a noisy blocking gate is to switch it off. Pairs considered and
# REJECTED (with reasons) are recorded in
# docs/CROSSREPO_FIGURE_COMMENSURABILITY_DCS_2026.md — read it before adding a row.
CROSS_REPO_FIGURES = [
    {"name": "DCS-2021 present active",
     "published": ["dcs2021_present_active"],
     "ours_path": ["HK1_aorist", "cf_present_tokens"],
     "expect_codes": [1], "unit": "tokens"},
    {"name": "DCS-2021 perfect active",
     "published": ["dcs2021_perfect_active"],
     "ours_path": ["HK15_past_tenses", "perfect_tokens"],
     "expect_codes": [15], "unit": "tokens"},
    # THE H2293 CASE. Our `imperfect_tokens` (47,554) is NOT the pair — it adds medium,
    # augmentless and passive codes. `imperfect_active_tokens` (codes 4+8) is.
    {"name": "DCS-2021 imperfect active",
     "published": ["dcs2021_imperfect_active"],
     "ours_path": ["HK15_past_tenses", "imperfect_active_tokens"],
     "expect_codes": [4, 8], "unit": "tokens"},
    # A legitimate decomposition, not a mismatch: they publish the aorist split by voice, we
    # derive it pooled, so the comparison sums their two rows. Same codes, same unit.
    {"name": "DCS-2021 aorist (both voices)",
     "published": ["dcs2021_aorist_active", "dcs2021_aorist_medium"],
     "ours_path": ["HK15_past_tenses", "aorist_tokens"],
     "expect_codes": [10, 11, 12, 13], "unit": "tokens"},
    {"name": "DCS-2021 verbal total",
     "published": ["dcs2021_verbal_total"],
     "ours_path": ["total_verbal_tokens"],
     "expect_codes": None, "unit": "tokens"},   # 42 codes; pinning them here adds nothing
]


def load_published(path=PUBLISHED_FIGURES):
    """Read the vendored contract asset, refusing the shapes that caused the bug it detects."""
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    figures = doc.get("figures")
    if not isinstance(figures, list):
        raise ValueError(f"{path}: `figures` must be a LIST of records, not "
                         f"{type(figures).__name__} — a name-keyed map is the H1486 defect")
    ids = [f["id"] for f in figures]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        raise ValueError(f"{path}: duplicate figure id(s) {dupes}")
    return figures


def _dig(obj, path):
    for key in path:
        if not isinstance(obj, dict) or key not in obj:
            return None
        obj = obj[key]
    return obj


def cross_repo_violations(published, ours):
    """Compare each seeded pair. Returns [(name, kind, detail)]; empty = the contract holds."""
    by_id = {f["id"]: f for f in published}
    out = []
    for fig in CROSS_REPO_FIGURES:
        rows = [by_id.get(i) for i in fig["published"]]
        if any(r is None for r in rows):
            missing = [i for i, r in zip(fig["published"], rows) if r is None]
            out.append((fig["name"], "missing-published",
                        f"the asset has no figure id(s) {missing} — refresh the vendored copy"))
            continue

        units = {r.get("unit") for r in rows}
        if units != {fig["unit"]}:
            out.append((fig["name"], "incommensurable",
                        f"published unit(s) {sorted(units)} != expected {fig['unit']!r} — "
                        f"these are not the same kind of quantity; re-adjudicate the pair"))
            continue

        if fig["expect_codes"] is not None:
            codes = sorted({c for r in rows for c in r.get("source_codes", [])})
            if codes != fig["expect_codes"]:
                out.append((fig["name"], "incommensurable",
                            f"published source_codes {codes} != pinned {fig['expect_codes']} — "
                            f"the published figure changed WHAT it measures; re-adjudicate "
                            f"the pair rather than 'fixing' either number"))
                continue

        theirs = sum(r["value"] for r in rows)
        mine = _dig(ours, fig["ours_path"])
        if mine is None:
            out.append((fig["name"], "missing-ours",
                        f"{'.'.join(fig['ours_path'])} absent from "
                        f"{OUR_DCS2021_STATS.name} — re-run verify_claims_dcs.py"))
            continue

        tol = max(r.get("tolerance", 0) for r in rows)
        if abs(theirs - mine) > tol:
            out.append((fig["name"], "drift",
                        f"VisualDCS publishes {theirs:,} but our "
                        f"{'.'.join(fig['ours_path'])} = {mine:,} "
                        f"(delta {theirs - mine:+,}, tolerance ±{tol})"))
    return out


def blocks(text):
    parts = re.split(r"(?m)^  - id:\s*(\S+)\s*$", text)
    yield ("<header/synthesis>", parts[0])
    for i in range(1, len(parts), 2):
        yield (parts[i], parts[i] + parts[i + 1])


def has_marker(block):
    low = block.lower()
    return any(m.lower() in low for m in CORRECTION_MARKERS)


def scan_file(path):
    """Check-1 (supersession) violations in one file."""
    text = path.read_text(encoding="utf-8")
    violations = []
    for bid, block in blocks(text):
        if has_marker(block):
            continue
        for fig in CANONICAL_FIGURES:
            if any(re.search(p, block) for p in fig["stale_patterns"]):
                violations.append((path.name, bid, fig["name"]))
                break
    return violations


def _norm(v):
    return v.replace(",", "").replace("~", "").strip()


def check_all():
    """Check-1 supersession violations across all registers (kept stable for the test API)."""
    files = sorted(ROOT.glob("*/claims.yml"))
    v = []
    for f in files:
        v.extend((f.parent.name, *rest[1:]) for rest in scan_file(f))
    return files, v


def consistency_violations(files):
    """Check-2: any figure cited with a value outside its `allowed` set (drift/typo/stale)."""
    out = []
    for f in files:
        book = f.parent.name
        for bid, block in blocks(f.read_text(encoding="utf-8")):
            if has_marker(block):   # a correction-documenting block may cite the old value
                continue
            for fig in CONSISTENCY_FIGURES:
                for m in re.finditer(fig["capture"], block):
                    val = _norm(m.group(1))
                    if val not in fig["allowed"]:
                        out.append((fig["name"], book, bid, m.group(1), sorted(fig["allowed"])))
    return out


def self_test():
    import tempfile
    # supersession
    bad = 'entries:\n\n  - id: X-1\n    number: "aorist 2,452 tokens = 0.31% of verbal"\n'
    ok = ('entries:\n\n  - id: X-2\n    number: "aorist 12,054 (feat_formation). REFRESHED from '
          '2,452 / 0.31% which undercounted"\n')
    for body, expect in [(bad, True), (ok, False)]:
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False, encoding="utf-8") as tf:
            tf.write(body); p = Path(tf.name)
        assert bool(scan_file(p)) == expect, body
        p.unlink()
    # consistency: a perfect value outside the allowed set -> flagged
    d = Path(tempfile.mkdtemp())
    (d / "A").mkdir(); (d / "B").mkdir()
    (d / "A" / "claims.yml").write_text('entries:\n\n  - id: A\n    n: "perfect 61,986"\n', encoding="utf-8")
    (d / "B" / "claims.yml").write_text('entries:\n\n  - id: B\n    n: "perfect 99,999"\n', encoding="utf-8")
    assert consistency_violations(sorted(d.glob("*/claims.yml"))), "out-of-set value not caught"
    # the canonical DCS-2026 value -> NOT flagged
    (d / "A" / "claims.yml").write_text('entries:\n\n  - id: A\n    n: "perfect 90,001"\n', encoding="utf-8")
    (d / "B" / "claims.yml").write_text('entries:\n\n  - id: B\n    n: "present-system 353,215"\n', encoding="utf-8")
    assert not consistency_violations(sorted(d.glob("*/claims.yml"))), "canonical value wrongly flagged"
    # an old value carried in a correction-marked block -> exempt (documents the supersession)
    (d / "A" / "claims.yml").write_text(
        'entries:\n\n  - id: A\n    n: "perfect 90,001 — REFRESHED from the older DCS-2021 61,986"\n',
        encoding="utf-8")
    assert not consistency_violations(sorted(d.glob("*/claims.yml"))), "correction-marked old value wrongly flagged"

    # --- check 3: cross-repo, including THE RETRODICTION (H2298) ---
    # Everything below is synthetic, so the gate's logic is pinned even if the real assets
    # are absent. Scope to the one row under test — the other seeded rows are legitimately
    # "missing-published" from a single-row synthetic asset.
    ours = {"HK15_past_tenses": {"imperfect_active_tokens": 40363}}
    row = lambda v: [x for x in v if x[0] == "DCS-2021 imperfect active"]
    base = {"id": "dcs2021_imperfect_active", "unit": "tokens", "tolerance": 0}
    true_figure = [dict(base, value=40363, source_codes=[4, 8])]
    assert not row(cross_repo_violations(true_figure, ours)), "the true figure was flagged"

    # The pre-H1486 published value, exactly as it stood: 4,442 = code 8 alone, because a
    # name-keyed read let code 8 overwrite code 4. If this does not fail, the gate would not
    # have caught the original divergence and is therefore not done.
    retrodiction = [dict(base, value=4442, source_codes=[8])]
    assert row(cross_repo_violations(retrodiction, ours)), \
        "RETRODICTION FAILED: the pre-H1486 figure 4,442 was not caught"

    # ... and a pure value drift (same code set, wrong number) is caught as drift, not merely
    # as a code-set mismatch — otherwise the gate would only ever notice re-derivations.
    drifted = [dict(base, value=4442, source_codes=[4, 8])]
    v = row(cross_repo_violations(drifted, ours))
    assert v and v[0][1] == "drift", f"value drift not reported as drift: {v}"

    # A changed code set is reported as INCOMMENSURABLE, never as drift — the two sides stopped
    # measuring the same thing, and telling someone to "fix the number" would be wrong advice.
    recoded = [dict(base, value=40363, source_codes=[4, 8, 9])]
    v = row(cross_repo_violations(recoded, ours))
    assert v and v[0][1] == "incommensurable", f"code-set change misreported: {v}"

    # The shape guard: a name-keyed object is refused outright.
    bad_shape = Path(tempfile.mkdtemp()) / "figs.json"
    bad_shape.write_text('{"figures": {"dcs2021_imperfect_active": 4442}}', encoding="utf-8")
    try:
        load_published(bad_shape)
        raise AssertionError("a name-keyed `figures` object was accepted")
    except ValueError:
        pass
    return True


def main():
    if "--self-test" in sys.argv:
        print("self-test:", "PASS" if self_test() else "FAIL")
        return
    assert self_test(), "self-test failed"
    files, stale = check_all()
    cons = consistency_violations(files)

    # Check 3 fails LOUDLY when its inputs are missing. A cross-repo gate that quietly skips
    # itself when the vendored asset is absent is indistinguishable from a gate that passes —
    # which is precisely how the divergence it exists to catch survived for months.
    try:
        cross = cross_repo_violations(
            load_published(),
            json.loads(OUR_DCS2021_STATS.read_text(encoding="utf-8")))
    except (OSError, ValueError) as exc:
        cross = [("cross-repo contract", "unavailable",
                  f"{exc} — refresh with scripts/refresh_published_figures.py")]

    print(f"checked {len(files)} registers · {len(CANONICAL_FIGURES)} supersession + "
          f"{len(CONSISTENCY_FIGURES)} consistency + {len(CROSS_REPO_FIGURES)} cross-repo "
          f"figure(s)")
    if not stale and not cons and not cross:
        print("OK — no superseded figure cited live, every shared figure has one value, and "
              "our DCS-2021 figures agree with what VisualDCS publishes.")
        sys.exit(0)
    if cross:
        print(f"\nCROSS-REPO drift ({len(cross)}):")
        for name, kind, detail in cross:
            print(f"  ✗ [{kind}] {name}: {detail}")
    if stale:
        print(f"\nSUPERSESSION drift ({len(stale)}):")
        for book, bid, name in stale:
            print(f"  ✗ {book} [{bid}] cites superseded '{name}'")
    if cons:
        print(f"\nCONSISTENCY drift ({len(cons)} out-of-set citation(s)):")
        for name, book, bid, val, allowed in cons:
            print(f"  ✗ {book} [{bid}] cites '{name}' = {val}, not in allowed {allowed}")
    print("\nFix: refresh to a canonical value, OR (supersession) add a correction marker "
          "if the mention documents the supersession.\nFor a CROSS-REPO row: an "
          "'incommensurable' report means the two sides stopped measuring the same thing — "
          "re-adjudicate the pair in docs/CROSSREPO_FIGURE_COMMENSURABILITY_DCS_2026.md "
          "rather than editing either number to match.")
    sys.exit(1)


if __name__ == "__main__":
    main()
