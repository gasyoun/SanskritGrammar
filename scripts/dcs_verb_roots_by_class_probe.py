#!/usr/bin/env python3
"""dcs_verb_roots_by_class_probe.py — H4178 wiring: first consumer of the
VisualDCS M9 dataset `dcs-verb-roots-by-class` (kosha manifest, 463 rows,
zero consumers at the 05-09-2026 REUSE_INDEX census).

Reads the ten per-class CSVs (root,corpus_count; IAST; one file per present
class 1..10) from the sibling VisualDCS checkout, read-only, and probes them
from the grammar/curriculum side:

  * per-class attested-root inventory (the census' "Zaliznyak drills;
    curriculum" target — class-sized drill material, not abstract paradigms);
  * roots attested in more than one class (the cross-class set a drill must
    not present as single-class);
  * per-class share of total corpus root occurrences (where the bulk of the
    verb system actually lives);
  * the 20 highest-frequency roots overall with their class spread — the
    natural seed of a frequency-ordered class drill.

Writes reports/DCS_VERB_ROOTS_BY_CLASS_PROBE_<date>.md and prints a summary.

Usage:  python scripts/dcs_verb_roots_by_class_probe.py
"""
from __future__ import annotations

import csv
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
MANIFEST_ROWS = 463  # kosha datasets.json dcs-verb-roots-by-class.rows

# present classes 1..10 (no 8 in the attested inventory; 2 =Svg/seT etc.)
CLASS_LABELS = {
    1: "1 (bhvādi)", 2: "2 (adādi)", 3: "3 (juhotyādi)", 4: "4 (divādi)",
    5: "5 (svādi)", 6: "6 (tudādi)", 7: "7 (rudhādi)", 8: "8 (tanādi)",
    9: "9 (kryādi)", 10: "10 (curādi)",
}


def github_root() -> Path:
    for candidate in (REPO, *REPO.parents):
        if (candidate / "VisualDCS").is_dir():
            return candidate
    raise SystemExit("VisualDCS sibling checkout not found above " + str(REPO))


def source_dir() -> Path:
    root = github_root()
    d = root / "VisualDCS" / "derived-data" / "Glagolnye-formy" / "Klassy" / \
        "Spiski-glagolnyh-kornej-po-klassam-2214" / "Imeyushchie-formy"
    if not d.is_dir():
        raise SystemExit(f"source inventory missing: {d}")
    return d


def sibling_commit() -> str | None:
    try:
        return subprocess.run(
            ["git", "log", "-1", "--format=%H",
             "--", "derived-data/Glagolnye-formy/Klassy/Spiski-glagolnyh-kornej-po-klassam-2214"],
            cwd=github_root() / "VisualDCS",
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (subprocess.CalledProcessError, OSError):
        return None


def load() -> dict[int, list[tuple[str, int]]]:
    per_class: dict[int, list[tuple[str, int]]] = {}
    for klass in range(1, 11):
        path = source_dir() / f"{klass}.csv"
        if not path.is_file():
            per_class[klass] = []
            continue
        rows: list[tuple[str, int]] = []
        with path.open(encoding="utf-8", newline="") as fh:
            for line in csv.reader(fh):
                if not line or not line[0].strip():
                    continue
                root = line[0].strip()
                count = int(line[1]) if len(line) > 1 and line[1].strip().isdigit() else 0
                rows.append((root, count))
        per_class[klass] = rows
    return per_class


def main() -> None:
    per_class = load()
    total_rows = sum(len(v) for v in per_class.values())
    occurrences = {k: sum(c for _, c in v) for k, v in per_class.items()}
    total_occ = sum(occurrences.values())

    class_of: defaultdict[str, set[int]] = defaultdict(set)
    freq: defaultdict[str, int] = defaultdict(int)
    for klass, rows in per_class.items():
        for root, count in rows:
            class_of[root].add(klass)
            freq[root] += count

    multi = {r: sorted(c) for r, c in class_of.items() if len(c) > 1}
    top20 = sorted(freq.items(), key=lambda kv: -kv[1])[:20]

    pin = sibling_commit()
    report = REPO / "reports" / f"DCS_VERB_ROOTS_BY_CLASS_PROBE_{date.today():%d.%m.%Y}.md"
    report.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append(f"# DCS verb-roots-by-class — first-consumer probe ({date.today():%d-%m-%Y})")
    lines.append("")
    lines.append("_H4178 wiring: first consumer of the VisualDCS M9 dataset "
                 "`dcs-verb-roots-by-class` (kosha manifest, zero consumers at the "
                 "05-09-2026 REUSE_INDEX census)._")
    lines.append("")
    lines.append("Source: VisualDCS `derived-data/Glagolnye-formy/Klassy/"
                 "Spiski-glagolnyh-kornej-po-klassam-2214/Imeyushchie-formy/` "
                 "(10 per-class CSVs, root + corpus count, IAST), read-only sibling "
                 f"pin `{pin}`. Curriculum target: class-sized attested drill "
                 "material (Zaliznyak drills lane).")
    lines.append("")
    lines.append("## Per-class attested inventory")
    lines.append("")
    lines.append("| Class | Attested roots | Corpus occurrences | Share of occurrences |")
    lines.append("|---|---|---|---|")
    for klass in sorted(per_class):
        share = f"{100 * occurrences[klass] / total_occ:.1f}%" if total_occ else "—"
        lines.append(f"| {CLASS_LABELS[klass]} | {len(per_class[klass])} | "
                     f"{occurrences[klass]} | {share} |")
    lines.append(f"| **total** | **{len(class_of)} distinct roots** ({total_rows} rows) | "
                 f"**{total_occ}** | 100% |")
    lines.append("")
    lines.append(f"Manifest parity: {total_rows} rows vs kosha manifest 463 — "
                 + ("**match**." if total_rows == MANIFEST_ROWS else f"**drift ({total_rows} != 463), flagged**."))
    lines.append("")
    lines.append(f"## Cross-class roots ({len(multi)})")
    lines.append("")
    lines.append("Attested in more than one present class — a drill must not "
                 "present these as single-class:")
    lines.append("")
    for root in sorted(multi, key=lambda r: -freq[r]):
        classes = ", ".join(CLASS_LABELS[c] for c in multi[root])
        lines.append(f"- {root} ({freq[root]} occ.) — {classes}")
    lines.append("")
    lines.append("## Top-20 roots by corpus frequency (drill seed)")
    lines.append("")
    lines.append("| Root | Occurrences | Class(es) |")
    lines.append("|---|---|---|")
    for root, count in top20:
        classes = ", ".join(CLASS_LABELS[c] for c in sorted(class_of[root]))
        lines.append(f"| {root} | {count} | {classes} |")
    lines.append("")
    lines.append("## Curriculum reading")
    lines.append("")
    bulk = sorted(occurrences.items(), key=lambda kv: -kv[1])[:3]
    lines.append("Three classes carry "
                 f"{100 * sum(c for _, c in bulk) / total_occ:.1f}% of all corpus "
                 "root occurrences — a frequency-ordered drill covers the verb "
                 "system with a fraction of the inventory. The "
                 f"{len(multi)} cross-class roots are the collision set where "
                 "single-class drill cards would teach a falsehood.")
    lines.append("")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"rows={total_rows} distinct_roots={len(class_of)} "
          f"multi_class={len(multi)} occurrences={total_occ}")
    print(f"manifest parity: {'OK' if total_rows == MANIFEST_ROWS else 'DRIFT'}")
    print(f"report: {report}")


if __name__ == "__main__":
    main()
