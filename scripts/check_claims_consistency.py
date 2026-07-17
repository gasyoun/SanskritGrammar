#!/usr/bin/env python
"""check_claims_consistency.py — guardrail against superseded corpus figures drifting
back into the claim registers (H1140).

WHY THIS EXISTS. The aorist token count was refreshed from the DCS-2021 tense-code figure
(2,452 / 0.31%) to DCS's feat_formation count (12,054 / 2.30%) across Kochergina HK-1, Apte
APT-31 and Whitney WH-2/WH-15 (H1134/H1136/H1137). The refresh drifted once: WH-2 REUSED
Kochergina's number and was left stale for a turn, because nothing checked that a figure one
register borrows from another stays in sync. This script is that check.

WHAT IT CHECKS. A small CANONICAL_FIGURES registry lists corpus quantities that (a) are cited in
more than one register and (b) have a superseded old value that must not reappear as a LIVE figure.
For each register (`*/claims.yml`), split into blocks (the header/synthesis, then one per `- id:`
entry) and, for each canonical figure, FLAG any block that cites a superseded value WITHOUT a
correction marker (`refreshed`, `undercounted`, `older … figure`, etc.). A documented correction
(e.g. "refreshed from 2,452 … undercounted") is fine; a bare stale citation is a drift and fails.

Exit code 0 = clean, 1 = drift found (so it can gate `npm run check-claims` / CI / a pre-commit).

TO ADD A FIGURE: append to CANONICAL_FIGURES — the canonical (current) value, the stale patterns
that must not appear un-marked, and the correction-marker words that make a stale mention OK.

Usage:  python scripts/check_claims_consistency.py [--self-test]
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# Correction-marker words: if any appears in a block, a stale citation there is documentation.
CORRECTION_MARKERS = [
    "refresh", "undercount", "superseded", "older", "tense-code", "stale",
    "not the", "was verify_claims", "corrected", "REFRESHED",
]

CANONICAL_FIGURES = [
    {
        "name": "aorist token count",
        "canonical": "12,054 (2.30% of finite verbal; DCS feat_formation)",
        # stale = the DCS-2021 tense-code figure that must not reappear as a live number
        "stale_patterns": [
            r"2,452\s+aorist", r"aorist\s+2,452", r"aorist\s+tokens?\s*=\s*2,452",
            r"0\.31\s*%\s*of\s*(?:781,618\s*)?verbal", r"0,31\s*%\s*глаголь",
        ],
    },
    # Add further cross-register figures here as they are identified, e.g. present-system tokens,
    # class-I share — same shape: {name, canonical, stale_patterns}.
]


def blocks(text):
    """Yield (block_id, block_text). The preamble (header+work+synthesis, before the first
    '  - id:') is one block; each entry is its own block."""
    parts = re.split(r"(?m)^  - id:\s*(\S+)\s*$", text)
    yield ("<header/synthesis>", parts[0])
    for i in range(1, len(parts), 2):
        yield (parts[i], parts[i] + parts[i + 1])


def has_marker(block):
    low = block.lower()
    return any(m.lower() in low for m in CORRECTION_MARKERS)


def scan_file(path):
    text = path.read_text(encoding="utf-8")
    violations = []
    for bid, block in blocks(text):
        marked = has_marker(block)
        for fig in CANONICAL_FIGURES:
            for pat in fig["stale_patterns"]:
                if re.search(pat, block) and not marked:
                    violations.append((path.name, bid, fig["name"], pat))
                    break
    return violations


def check_all():
    all_v = []
    files = sorted(ROOT.glob("*/claims.yml"))
    for f in files:
        all_v.extend((f.parent.name, *v[1:]) for v in scan_file(f))
    return files, all_v


def self_test():
    stale_bad = ("  - id: X-1\n    number: \"aorist 2,452 tokens = 0.31% of verbal\"\n"
                 "    note: \"marginal\"\n")
    stale_ok = ("  - id: X-2\n    number: \"aorist 12,054 tokens (feat_formation). REFRESHED from "
                "2,452 / 0.31% which undercounted\"\n")
    clean = "  - id: X-3\n    number: \"present 353,215\"\n"
    import tempfile
    for name, body, expect_viol in [("bad", stale_bad, True), ("ok", stale_ok, False),
                                     ("clean", clean, False)]:
        txt = "entries:\n\n" + body
        with tempfile.NamedTemporaryFile("w", suffix=".yml", delete=False, encoding="utf-8") as tf:
            tf.write(txt); p = Path(tf.name)
        v = scan_file(p)
        p.unlink()
        assert bool(v) == expect_viol, (name, v)
    return True


def main():
    if "--self-test" in sys.argv:
        print("self-test:", "PASS" if self_test() else "FAIL")
        return
    assert self_test(), "self-test failed"
    files, violations = check_all()
    print(f"checked {len(files)} claim registers for {len(CANONICAL_FIGURES)} canonical figure(s)")
    if not violations:
        print("OK — no superseded figure cited as a live number. Registers consistent.")
        sys.exit(0)
    print(f"\nDRIFT: {len(violations)} superseded-figure citation(s) without a correction marker:")
    for book, bid, name, pat in violations:
        print(f"  ✗ {book}  [{bid}]  '{name}'  matched /{pat}/")
    print("\nFix: refresh the figure to the canonical value, OR add a correction marker "
          "(refreshed/undercounted/older …) if the mention is documenting the supersession.")
    sys.exit(1)


if __name__ == "__main__":
    main()
