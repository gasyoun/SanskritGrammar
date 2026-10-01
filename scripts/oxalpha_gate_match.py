#!/usr/bin/env python3
"""Executable-path matcher for the OxAlpha review gate (H4074, reporting only).

Implements section 1 of docs/OXALPHA_STATUS_GATE_DESIGN_2026.md: the gate fires
only when a diff touches reviewable executable code. Zero matched paths is a
valid outcome (the design's ``skip`` case), never an error.

Deterministic and side-effect-free apart from the optional --out record.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

#: Executable prefixes, per design section 1. tests/** is listed there too:
#: "reviewed as spec evidence, not as churn" - a tests-only diff fires the
#: gate (the #870 lesson: a broken import in tests held CI red for four days).
#: .githooks/ is design section 3 (sensitive) and behavior-bearing, so it also
#: fires the gate.
EXECUTABLE_PREFIXES = (
    "scripts/",
    "tools/",
    "pipelines/",
    "packages/sg_tooling/src/",
    "src/",
    "apps/site/",
    "patches/",
    ".github/workflows/",
    ".githooks/",
    "tests/",
)

#: Root-anchored executable files (design section 1).
EXECUTABLE_FILES = (
    "docusaurus.config.mjs",
    "sidebars.mjs",
)

#: Exclusions INSIDE the executable prefixes (design decision 5): generated
#: book extractions, derived stores, minified bundles.
EXCLUDED_SUBSTRINGS = (
    "__pycache__",
    "node_modules",
)
EXCLUDED_SUFFIXES = (
    ".mdx",       # generated book extractions
    ".min.js",
    ".jsonl",
)

#: Sensitive paths (design section 3: integrity / production / data-truth
#: surfaces). They rank first in the review pass; the design requires a human
#: approval recorded in the PR body for them on top of a green gate.
SENSITIVE_PREFIXES = (
    ".github/workflows/",
    ".githooks/",
)
SENSITIVE_FILES = (
    "scripts/pre_push_stale_base_check.py",
    "scripts/eol_census.py",
    "scripts/check_claims_consistency.py",
    "scripts/refresh_published_figures.py",
    "scripts/build_lessonpack.py",
)


def _changed_paths(base: str, head: str, repo: str) -> list[str]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        cwd=repo, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(
            "git diff failed (rc=%s): %s" % (proc.returncode, proc.stderr.strip()[:200]))
    return [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]


def is_executable(path: str) -> bool:
    """One path -> executable True/False, per the design's matcher table."""
    p = path.replace("\\", "/")
    while p.startswith("./"):        # NOT lstrip("./"): that would eat the
        p = p[2:]                    # leading dot of .githooks/ and .github/
    if any(x in p for x in EXCLUDED_SUBSTRINGS):
        return False
    if p.endswith(EXCLUDED_SUFFIXES):
        return False
    if p in EXECUTABLE_FILES:
        return True
    return p.startswith(EXECUTABLE_PREFIXES)


def is_sensitive(path: str) -> bool:
    p = path.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    if p.startswith(SENSITIVE_PREFIXES) or p in SENSITIVE_FILES:
        return True
    return p.endswith("/claims.yml") or p == "claims.yml"


def classify(paths: list[str]) -> dict:
    matched = sorted({p for p in paths if is_executable(p)})
    skipped = sorted(set(paths) - set(matched))
    return {
        "executable": bool(matched),
        "matched_paths": matched,
        "sensitive_paths": sorted(p for p in matched if is_sensitive(p)),
        "skipped_paths": skipped,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="OxAlpha gate executable-path matcher.")
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", default=None, help="write the full record as JSON here")
    ap.add_argument("--gha", action="store_true",
                    help="emit GitHub Actions outputs (executable, matched-n)")
    args = ap.parse_args()

    record = classify(_changed_paths(args.base, args.head, args.repo))
    if args.out:
        Path(args.out).write_text(
            json.dumps(record, indent=1, ensure_ascii=False) + "\n",
            encoding="utf-8", newline="\n")
    if args.gha:
        for key, val in (("executable", str(record["executable"]).lower()),
                         ("matched-n", str(len(record["matched_paths"]))),
                         ("sensitive-n", str(len(record["sensitive_paths"])))):
            print("%s=%s" % (key, val))
        if record["matched_paths"]:
            print("matched-paths<<EOF")
            print("\n".join(record["matched_paths"]))
            print("EOF")
    for p in record["matched_paths"]:
        print("EXEC: %s" % p, file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main() or 0)
