#!/usr/bin/env python3
"""Deterministic eval runner for SanskritGrammar (H6846).

Suite ``ud-claims-probe`` replays the repo's pre-registered UD claims register
through ``tools/verify_claims_ud.py --check`` and grades the live dual verdicts
against the frozen register verdicts. No model, no network, no new gold.

Usage::

    python evals/run_eval.py             # live replay, exit 0 iff verdicts match
    python evals/run_eval.py --canary    # gold passes AND a flipped verdict fails
    python evals/run_eval.py --json
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOL = REPO / "tools" / "verify_claims_ud.py"
LINE = re.compile(r"^(UDA-\d)\s+[^:]+:.*->\s*(TRUE|OVERSTATED|FALSE|UNTESTABLE|PENDING)\s*/\s*(PASS|OVERSTATED|FAIL)\s*$")
EXPECTED = {
    "UDA-1": ("TRUE", "PASS"),
    "UDA-2": ("TRUE", "PASS"),
    "UDA-3": ("TRUE", "PASS"),
    "UDA-4": ("OVERSTATED", "OVERSTATED"),
}


def run_probe():
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--check"],
        cwd=str(REPO),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        raise RuntimeError("verify_claims_ud.py exited %d: %s" % (proc.returncode, proc.stderr.strip()))
    verdicts = {}
    for line in proc.stdout.splitlines():
        match = LINE.match(line.strip())
        if match:
            verdicts[match.group(1)] = (match.group(2), match.group(3))
    return verdicts, proc.stdout


def grade(verdicts):
    errors = []
    for claim_id, want in EXPECTED.items():
        got = verdicts.get(claim_id)
        if got is None:
            errors.append("%s: verdict missing from the probe replay" % claim_id)
        elif got != want:
            errors.append("%s: got %s, expected %s" % (claim_id, got, want))
    return errors


def mutate(verdicts):
    mutated = dict(verdicts)
    if mutated:
        claim_id = sorted(mutated)[0]
        fact, ud = mutated[claim_id]
        mutated[claim_id] = (fact, "FAIL" if ud != "FAIL" else "PASS")
    return mutated


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--canary", action="store_true", help="also require a flipped verdict to fail")
    parser.add_argument("--json", action="store_true", help="print a JSON result object")
    args = parser.parse_args()

    verdicts, _stdout = run_probe()
    gold_errors = grade(verdicts)
    result = {
        "suite": "ud-claims-probe",
        "cases": len(EXPECTED),
        "gold": "PASS" if not gold_errors else "FAIL",
        "gold_errors": gold_errors,
        "verdicts": {k: list(v) for k, v in sorted(verdicts.items())},
    }

    ok = not gold_errors
    if args.canary:
        mutated_errors = grade(mutate(verdicts))
        result["canary"] = {
            "mutation": "first replayed UD verdict flipped",
            "mutation_result": "FAIL" if mutated_errors else "PASS",
            "mutation_errors": mutated_errors,
        }
        ok = ok and bool(mutated_errors)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        print("== ud-claims-probe: gold %s (%d claims) ==" % (result["gold"], result["cases"]))
        for claim_id, verdict in sorted(verdicts.items()):
            print("  %s: %s / %s" % (claim_id, verdict[0], verdict[1]))
        for err in gold_errors:
            print("  - " + err)
        if args.canary:
            canary = result["canary"]
            print("== canary: mutated answer %s (expected FAIL) ==" % canary["mutation_result"])
            for err in canary["mutation_errors"]:
                print("  - " + err)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
