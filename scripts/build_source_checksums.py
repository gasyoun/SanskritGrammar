#!/usr/bin/env python3
"""B7 (Angle-B site backlog, ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md §3): checksums on
every source .doc/.docx — fixity for the digitized editions.

Each per-book directory carries a legacy `.doc`/`.docx` beside its `.mdx` extraction
(see the repo CLAUDE.md "raw-source archive" layer). Nothing currently detects a
silent bit-rot or accidental overwrite of those originals. This script hashes every
tracked `.doc`/`.docx` under the repo (SHA-256) and writes a manifest; `--check`
re-hashes and fails if a tracked source file's bytes drifted from the manifest
without the manifest being regenerated alongside it.

    python scripts/build_source_checksums.py           # regenerate the manifest
    python scripts/build_source_checksums.py --check   # verify, exit 1 on drift
"""

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "scripts" / "data" / "source_checksums.json"
EXTENSIONS = (".doc", ".docx")


def tracked_source_files():
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, check=True,
        encoding="utf-8",
    ).stdout
    paths = [p for p in out.split("\0") if p]
    return sorted(p for p in paths if p.lower().endswith(EXTENSIONS))


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest():
    files = tracked_source_files()
    entries = {}
    for rel in files:
        path = ROOT / rel
        entries[rel] = {
            "sha256": sha256_of(path),
            "bytes": path.stat().st_size,
        }
    return {"files": entries, "count": len(entries)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                     help="verify the manifest matches the working tree; exit 1 on drift")
    args = ap.parse_args()

    manifest = build_manifest()

    if args.check:
        if not MANIFEST.exists():
            print(f"MISSING {MANIFEST}")
            return 1
        recorded = json.loads(MANIFEST.read_text(encoding="utf-8"))
        problems = []
        recorded_files = recorded.get("files", {})
        for rel, info in manifest["files"].items():
            prior = recorded_files.get(rel)
            if prior is None:
                problems.append(f"UNRECORDED {rel}")
            elif prior["sha256"] != info["sha256"]:
                problems.append(f"DRIFT {rel} (checksum changed, manifest not regenerated)")
        for rel in recorded_files:
            if rel not in manifest["files"]:
                problems.append(f"REMOVED {rel} (still in manifest)")
        for line in problems:
            print(line)
        print(f"{len(problems)} problem(s) across {manifest['count']} tracked .doc/.docx file(s)")
        return 1 if problems else 0

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {MANIFEST} — {manifest['count']} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
