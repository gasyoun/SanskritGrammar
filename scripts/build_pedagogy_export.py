#!/usr/bin/env python3
"""Build / check the versioned pedagogy_export package (H1643).

Packages public-safe SanskritGrammar pedagogy feeds for Systema (and future
consumers) under data/pedagogy_export/ with a semver schema_version and
sha256 integrity checks.

Usage:
    python scripts/build_pedagogy_export.py           # build
    python scripts/build_pedagogy_export.py --check   # validate existing export
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

# Windows console: avoid UnicodeEncodeError on non-ASCII paths/logs.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

REPO = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO / "data" / "pedagogy_export"
MANIFEST_NAME = "export_manifest.json"
SCHEMA_VERSION = "1.0.0"
SUPPORTED_MAJOR = 1

# Source feeds relative to REPO. rights must stay public-safe aggregates.
FEED_SPECS = [
    {
        "id": "rq4_item_bank",
        "source": REPO / "TolchelnikovTalmud_2026" / "data" / "rq4_item_bank.json",
        "export_name": "rq4_item_bank.json",
        "rights": "aggregate-public-safe",
        "consumer_hint": "Systema resources/data/rq4_item_bank.json",
        "mode": "copy",
    },
    {
        "id": "difficulty_ordering_stats",
        "source": REPO / "data" / "difficulty_ordering" / "stats.json",
        "export_name": "difficulty_ordering_stats.json",
        "rights": "aggregate-public-safe",
        "consumer_hint": "advisory sequencing metadata (Hop C)",
        "mode": "copy",
    },
    {
        "id": "difficulty_ordering_core_vs_frequency",
        "source": REPO / "data" / "difficulty_ordering" / "core_vs_frequency.tsv",
        "export_name": "difficulty_ordering_core_vs_frequency.tsv",
        "rights": "aggregate-public-safe",
        "consumer_hint": "frequency vs core_rank join",
        "mode": "copy",
    },
    {
        "id": "difficulty_ordering_pos_divergence",
        "source": REPO / "data" / "difficulty_ordering" / "pos_divergence.tsv",
        "export_name": "difficulty_ordering_pos_divergence.tsv",
        "rights": "aggregate-public-safe",
        "consumer_hint": "POS-level frequency divergence",
        "mode": "copy",
    },
    {
        "id": "difficulty_ordering_textbook_join",
        "source": REPO / "data" / "difficulty_ordering" / "textbook_frequency_join.tsv",
        "export_name": "difficulty_ordering_textbook_frequency_join.tsv",
        "rights": "aggregate-public-safe",
        "consumer_hint": "textbook lesson vs frequency join",
        "mode": "copy",
    },
]

METHODICHKA_POINTERS = [
    {
        "id": "apte_corpus_layer",
        "title": "Apte methodichka corpus layer",
        "path": "ApteSyntax_1885/METODICHKA_APTE_CORPUS_LAYER_2026.md",
        "corpus_tsv": "ApteSyntax_1885/corpus_layer/corpus_layer.tsv",
        "visa_status": "pending-or-applied",  # re-audited by consumers; pointer only
    },
    {
        "id": "kochergina_corpus_layer",
        "title": "Kochergina methodichka corpus layer",
        "path": "KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_CORPUS_LAYER_2026.md",
        "corpus_tsv": "KocherginaUchebnik_1998/corpus_layer/corpus_layer.tsv",
        "visa_status": "pending-or-applied",
    },
]

LAST_MILE_HOP_STATUS = {
    "A_reader": "shipped-in-Systema",
    "B_srs": "shipped-in-Systema",
    "C_difficulty": "shipped-in-Systema",
    "rq4_harness": "shipped-flag-off",
}


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def _rel(path: Path) -> str:
    return path.relative_to(REPO).as_posix()


def build_export() -> dict:
    """Write data/pedagogy_export/ and return the manifest dict."""
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    feeds: list[dict] = []
    omitted: list[str] = []

    for spec in FEED_SPECS:
        src: Path = spec["source"]
        if not src.is_file():
            omitted.append(f"{spec['id']}: missing source {_rel(src) if src.is_relative_to(REPO) else src}")
            print(f"OMIT {spec['id']}: source missing ({src})", file=sys.stderr)
            continue
        dest = EXPORT_DIR / spec["export_name"]
        shutil.copy2(src, dest)
        feeds.append(
            {
                "id": spec["id"],
                "path": _rel(dest),
                "sha256": _sha256_file(dest),
                "rights": spec["rights"],
                "consumer_hint": spec["consumer_hint"],
            }
        )

    # Methodichka corpus-layer pointers only (no full textbook OCR).
    pointers_path = EXPORT_DIR / "methodichka_corpus_layer_pointers.json"
    live_pointers = []
    for ptr in METHODICHKA_POINTERS:
        md = REPO / ptr["path"]
        tsv = REPO / ptr["corpus_tsv"]
        if not md.is_file():
            omitted.append(f"{ptr['id']}: missing {ptr['path']}")
            print(f"OMIT {ptr['id']}: path missing", file=sys.stderr)
            continue
        entry = {
            "id": ptr["id"],
            "title": ptr["title"],
            "path": ptr["path"],
            "corpus_tsv": ptr["corpus_tsv"] if tsv.is_file() else None,
            "visa_status": ptr["visa_status"],
            "rights": "pointer-only-no-bulk-gloss",
        }
        live_pointers.append(entry)
    pointers_path.write_text(
        json.dumps(live_pointers, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    feeds.append(
        {
            "id": "methodichka_corpus_layer_pointers",
            "path": _rel(pointers_path),
            "sha256": _sha256_file(pointers_path),
            "rights": "pointer-only-no-bulk-gloss",
            "consumer_hint": "paths to methodichka corpus layers; not redistributable textbook text",
        }
    )

    manifest = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "generator": "scripts/build_pedagogy_export.py",
        "feeds": feeds,
        "last_mile_hop_status": dict(LAST_MILE_HOP_STATUS),
        "omissions": omitted,
    }
    manifest_path = EXPORT_DIR / MANIFEST_NAME
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote { _rel(manifest_path) } schema_version={SCHEMA_VERSION} feeds={len(feeds)}")
    if omitted:
        print(f"Omissions logged: {len(omitted)}", file=sys.stderr)
    return manifest


def check_export(min_major: int = SUPPORTED_MAJOR) -> int:
    """Validate existing export. Return process exit code (0 = ok)."""
    manifest_path = EXPORT_DIR / MANIFEST_NAME
    if not manifest_path.is_file():
        print(f"FAIL: missing { _rel(manifest_path) }", file=sys.stderr)
        return 1
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"FAIL: manifest JSON: {exc}", file=sys.stderr)
        return 1

    version = str(manifest.get("schema_version", ""))
    if not version:
        print("FAIL: schema_version missing", file=sys.stderr)
        return 1
    try:
        major = int(version.split(".", 1)[0])
    except ValueError:
        print(f"FAIL: unparseable schema_version {version!r}", file=sys.stderr)
        return 1
    if major != min_major:
        print(
            f"FAIL: schema major {major} != supported {min_major} (version={version})",
            file=sys.stderr,
        )
        return 1

    feeds = manifest.get("feeds")
    if not isinstance(feeds, list) or not feeds:
        print("FAIL: feeds must be a non-empty list", file=sys.stderr)
        return 1

    errors = 0
    for feed in feeds:
        fid = feed.get("id", "?")
        rel = feed.get("path")
        expected = feed.get("sha256")
        if not rel or not expected:
            print(f"FAIL: feed {fid}: path/sha256 missing", file=sys.stderr)
            errors += 1
            continue
        path = REPO / rel
        if not path.is_file():
            print(f"FAIL: feed {fid}: file missing ({rel})", file=sys.stderr)
            errors += 1
            continue
        actual = _sha256_file(path)
        if actual != expected:
            print(
                f"FAIL: feed {fid}: sha256 drift (manifest={expected[:12]}… file={actual[:12]}…)",
                file=sys.stderr,
            )
            errors += 1

    hop = manifest.get("last_mile_hop_status")
    if not isinstance(hop, dict) or not hop:
        print("FAIL: last_mile_hop_status missing or empty", file=sys.stderr)
        errors += 1

    if errors:
        print(f"FAIL: {errors} error(s)", file=sys.stderr)
        return 1
    print(f"OK: {len(feeds)} feeds, schema_version={version}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="validate existing data/pedagogy_export (no rebuild)",
    )
    parser.add_argument(
        "--min-major",
        type=int,
        default=SUPPORTED_MAJOR,
        help="required schema major for --check (default: 1)",
    )
    args = parser.parse_args(argv)
    if args.check:
        return check_export(min_major=args.min_major)
    build_export()
    return check_export(min_major=args.min_major)


if __name__ == "__main__":
    raise SystemExit(main())
