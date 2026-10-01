#!/usr/bin/env python
"""Compare regenerated outputs with HEAD, ignoring the generator's own date stamp.

Uprava H5423 (E016 wave 5). scripts/build_claims.py and scripts/build_errata.py stamp
today's date (DD-MM-YYYY) into every file they write, sometimes on the same line as a
count ("_Generated: 24-09-2026 · 40 verified ..._"). A plain `git diff --exit-code`
would therefore be red every day, and ignoring whole date-bearing lines would hide a
real count change. So this masks only the date tokens and compares the rest.

Run it AFTER the generators, in a git checkout:

    python scripts/build_claims.py && python scripts/build_errata.py
    python scripts/check_generated_outputs.py              # exit 1 on a real change
    python scripts/check_generated_outputs.py --restore-date-only

--restore-date-only resets every file whose ONLY change is the date stamp back to HEAD,
so an auto-commit carries content changes, never date churn.
"""

import argparse
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

# git output is read as raw bytes on purpose (paths via -z, blobs compared byte-wise).
DEFAULT_GLOBS = [
    "CLAIMS_VERIFIED.md",
    "ERRATA.md",
    "*/CLAIMS_VERIFIED.md",
    "*/claims.json",
    "*/ERRATA.mdx",
    "*/ERRATA.md",
]
DATE_RE = re.compile(r"\b\d{2}-\d{2}-\d{4}\b")


def git(*args, check=True):
    return subprocess.run(["git", *args], capture_output=True, check=check).stdout


def changed_paths(globs):
    tracked = git("diff", "--name-only", "-z", "--", *globs).split(b"\0")
    untracked = git("ls-files", "--others", "--exclude-standard", "-z", "--", *globs).split(b"\0")
    deleted = set(git("diff", "--name-only", "--diff-filter=D", "-z", "--", *globs).split(b"\0"))
    return [p.decode() for p in tracked if p and p not in deleted], \
        [p.decode() for p in untracked if p], sorted(p.decode() for p in deleted if p)


def masked(data):
    return DATE_RE.sub("DD-MM-YYYY", data.decode("utf-8", errors="replace"))


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--restore-date-only", action="store_true",
                    help="git checkout the files whose only change is the date stamp")
    ap.add_argument("globs", nargs="*", default=DEFAULT_GLOBS)
    args = ap.parse_args()

    modified, new, deleted = changed_paths(args.globs)
    real, date_only = list(new) + list(deleted), []
    for path in modified:
        before = git("show", f"HEAD:{path}")
        with open(path, "rb") as fh:
            after = fh.read()
        (date_only if masked(before) == masked(after) else real).append(path)

    if args.restore_date_only and date_only:
        git("checkout", "HEAD", "--", *date_only)
    for path in sorted(real):
        print(f"CHANGED {path}")
    print(f"{len(real)} file(s) with real changes, {len(date_only)} date-stamp-only")
    return 1 if real else 0


if __name__ == "__main__":
    sys.exit(main())
