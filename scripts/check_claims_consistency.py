#!/usr/bin/env python
"""check_claims_consistency.py — guardrail against corpus figures drifting across the
claim registers (H1140, extended H1164).

TWO CHECKS, both over every `*/claims.yml`:

  1. SUPERSESSION (CANONICAL_FIGURES) — a value that was recomputed and replaced must not
     reappear as a LIVE number. Seeded with the aorist: the DCS-2021 tense-code count
     (2,452 / 0.31%) was superseded by the feat_formation count (12,054 / 2.30%); any bare
     citation of the old value (without a correction marker) is drift.

  2. CONSISTENCY (CONSISTENCY_FIGURES) — a figure reused across registers must be cited with
     ONE value everywhere. If the same quantity appears with two different live values, that is
     drift too (this is how the DCS-2021 present count 157,003 and the DCS-2026 present-finite
     count 353,215 got flagged and reconciled). Correction/version-noted blocks are exempt.

A block = the register's header/synthesis, or one `- id:` entry. A block carrying a correction
marker (`refreshed`, `undercounted`, `older …`, a version tag like `DCS-2021`) is treated as
documentation and never counts as a live citation.

Exit 0 = clean, 1 = drift found. Wired into CI via tests/test_claims_consistency.py and available
as `npm run check-claims`.
"""
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
    return True


def main():
    if "--self-test" in sys.argv:
        print("self-test:", "PASS" if self_test() else "FAIL")
        return
    assert self_test(), "self-test failed"
    files, stale = check_all()
    cons = consistency_violations(files)
    print(f"checked {len(files)} registers · {len(CANONICAL_FIGURES)} supersession + "
          f"{len(CONSISTENCY_FIGURES)} consistency figure(s)")
    if not stale and not cons:
        print("OK — no superseded figure cited live, and every shared figure has one value.")
        sys.exit(0)
    if stale:
        print(f"\nSUPERSESSION drift ({len(stale)}):")
        for book, bid, name in stale:
            print(f"  ✗ {book} [{bid}] cites superseded '{name}'")
    if cons:
        print(f"\nCONSISTENCY drift ({len(cons)} out-of-set citation(s)):")
        for name, book, bid, val, allowed in cons:
            print(f"  ✗ {book} [{bid}] cites '{name}' = {val}, not in allowed {allowed}")
    print("\nFix: refresh to a canonical value, OR (supersession) add a correction marker "
          "if the mention documents the supersession.")
    sys.exit(1)


if __name__ == "__main__":
    main()
