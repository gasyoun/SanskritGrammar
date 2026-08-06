#!/usr/bin/env python
"""refresh_published_figures.py — re-vendor VisualDCS's published-figures contract asset.

`scripts/check_claims_consistency.py` check 3 compares our DCS-2021 figures against the ones
VisualDCS publishes. A GitHub workflow checks out ONE repo, so the gate cannot read a sibling
clone and must consume a committed copy: `data/dcs_published_figures.json`. This script is the
refresh step — run it locally (where the sibling clone exists) and commit the result.

    python scripts/refresh_published_figures.py            # copy + validate + write
    python scripts/refresh_published_figures.py --check    # verify the vendored copy is current

Upstream regenerates its side with:
    python VisualDCS/src/DCS-data-2026/regen_widgets.py --figures-only

`--check` is the CI-safe mode: it never reaches for the sibling clone, it only re-validates the
shape of what is committed here. Exit 0 = fine, 1 = stale/invalid, 2 = upstream unavailable.
"""
import json
import shutil
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
VENDORED = ROOT / "data" / "dcs_published_figures.json"
UPSTREAM = ROOT.parent / "VisualDCS" / "dcs_published_figures.json"

REQUIRED = ("id", "value", "unit", "basis", "source_file", "source_codes", "corpus_release")


def validate(doc, where):
    """Refuse the shapes that caused the bug this asset exists to detect."""
    problems = []
    figures = doc.get("figures")
    if not isinstance(figures, list):
        return [f"{where}: `figures` must be a LIST of records, not "
                f"{type(figures).__name__} — a name-keyed map is the H1486 defect itself"]
    if not figures:
        problems.append(f"{where}: `figures` is empty — the gate would be a silent no-op")
    ids = [f.get("id") for f in figures]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        problems.append(f"{where}: duplicate figure id(s) {dupes}")
    for f in figures:
        missing = [k for k in REQUIRED if not f.get(k) and f.get(k) != 0]
        if missing:
            problems.append(f"{where}: figure {f.get('id')!r} missing {missing} — "
                            f"`unit` and `basis` are mandatory, not decoration")
    return problems


def main():
    check_only = "--check" in sys.argv

    if not check_only:
        if not UPSTREAM.is_file():
            print(f"ERROR: upstream asset not found at {UPSTREAM}\n"
                  f"  Clone gasyoun/VisualDCS beside this repo, then regenerate it with\n"
                  f"  python src/DCS-data-2026/regen_widgets.py --figures-only", file=sys.stderr)
            return 2
        upstream_doc = json.loads(UPSTREAM.read_text(encoding="utf-8"))
        problems = validate(upstream_doc, "upstream")
        if problems:
            print("REFUSING to vendor an invalid upstream asset:", file=sys.stderr)
            for p in problems:
                print(f"  ✗ {p}", file=sys.stderr)
            return 1
        VENDORED.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(UPSTREAM, VENDORED)
        print(f"vendored {UPSTREAM} -> {VENDORED.relative_to(ROOT)}")

    if not VENDORED.is_file():
        print(f"ERROR: {VENDORED.relative_to(ROOT)} is not committed — check 3 has no input",
              file=sys.stderr)
        return 1
    doc = json.loads(VENDORED.read_text(encoding="utf-8"))
    problems = validate(doc, "vendored")
    if problems:
        for p in problems:
            print(f"  ✗ {p}", file=sys.stderr)
        return 1

    if check_only and UPSTREAM.is_file():
        # Only meaningful when the sibling clone is present; CI has none, and its absence is
        # not an error — the committed copy is the contract of record for CI.
        if json.loads(UPSTREAM.read_text(encoding="utf-8")) != doc:
            print("STALE: the vendored copy differs from the sibling VisualDCS clone.\n"
                  "  Re-run without --check and commit, after confirming upstream is right.",
                  file=sys.stderr)
            return 1

    print(f"OK — {len(doc['figures'])} published figure(s):")
    for f in doc["figures"]:
        print(f"    {f['id']:<28} {f['value']:>9,} {f['unit']:<7} codes={f['source_codes']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
