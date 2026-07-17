#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aorist_class_census.py — count the per-root aorist-class assignments (col 10)
of the author's Приложение 1 catalog in ``Talmud-2.1.6.mdx``.

Built for H1054 (aorist registry entries vs the Talmud): the Talmud's Приложение 1
carries, for each of the 745 verbal roots, the list of aorist classes (1–7, the
manual's Таблица 16 numbering = Whitney's seven types: 1 root, 2 thematic a-,
3 reduplicated, 4 s-, 5 iṣ-, 6 siṣ-, 7 sa-) available to that root. This census
answers, from the SYSTEMATIC (catalog) side, the question the registries' HK-5
answers from the corpus side: which aorist type is "most common" — by root count,
i.e. by class size / productivity, not by token frequency.

Also splits each class by the root's pada column (P/Ā/U) — a *rough* voice signal
only: pada in Приложение 1 is a per-root property, not a per-aorist-class one, so
it cannot by itself confirm or refute per-formation voice defectivity (root and
siṣ aorists active-only in the classical language).

Additionally cross-tabulates aorist class × seṭ/aniṭ/veṭ (joined from
data/talmud_appendix1.json by root id) — the systematic check for the s-aorist ≈
aniṭ / iṣ-aorist ≈ seṭ conditioning stated by HK-214, HB-376, HB-380.

Row logic follows tools/parse_appendix1.py (the canonical Приложение-1 parser):
only PRIMARY rows (col1 non-empty) are counted; allomorph continuation rows are
alternate stems of the same catalog entry. Wrapped continuation lines of a
primary row (col1 AND col2 empty) contribute their col-10 content to the open
primary row, so multi-line aorist cells are not truncated.

Usage:  python tools/aorist_class_census.py
Run from the TolchelnikovTalmud_2026 folder. Writes data/aorist_class_census.json.
"""
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
MDX = os.path.join(FOLDER, "Talmud-2.1.6.mdx")
APP1 = os.path.join(FOLDER, "data", "talmud_appendix1.json")
OUT = os.path.join(FOLDER, "data", "aorist_class_census.json")
MANUAL_VERSION = "2.1.6"

FN_RE = re.compile(r"\[\^[^\]]*\]")
CLASS_RE = re.compile(r"[1-7]")


def clean(s):
    s = s.replace("\xa0", " ").strip()
    s = s.replace("**", "")
    s = FN_RE.sub("", s)
    return s.strip()


def extract():
    lines = open(MDX, encoding="utf-8").read().split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("# Приложение 1"))
    end = next(i for i, l in enumerate(lines) if l.startswith("# Приложение 2"))

    entries = []          # (id, pada, aorist_cell_text)
    current = None
    for ln in lines[start:end]:
        if not ln.startswith("|"):
            continue
        parts = ln.rstrip("\n").split("|")
        if len(parts) < 12:
            continue
        col1 = clean(parts[1])
        col2 = clean(parts[2])
        if col1 and not (set(col1) <= set("-=:+ ")):
            current = {"id": col1, "pada": clean(parts[8]),
                       "aorist_raw": clean(parts[10])}
            entries.append(current)
        elif current is not None and not col1 and not col2:
            # wrapped continuation of the open primary row
            extra = clean(parts[10])
            if extra:
                current["aorist_raw"] += " " + extra
    return entries


def main():
    entries = extract()
    with open(APP1, encoding="utf-8") as f:
        set_by_id = {r["id"]: (r["set"] or "?")
                     for r in json.load(f)["roots"]}

    per_class = Counter()
    per_class_pada = {c: Counter() for c in "1234567"}
    per_class_set = {c: Counter() for c in "1234567"}
    combo = Counter()
    no_aorist = 0
    for e in entries:
        classes = sorted(set(CLASS_RE.findall(e["aorist_raw"])))
        e["classes"] = classes
        if not classes:
            no_aorist += 1
            continue
        combo[", ".join(classes)] += 1
        pada = e["pada"] or "?"
        set_cat = set_by_id.get(e["id"], "?")
        for c in classes:
            per_class[c] += 1
            per_class_pada[c][pada] += 1
            per_class_set[c][set_cat] += 1

    payload = {
        "_meta": {
            "what": "Census of per-root aorist-class assignments (col 10 of "
                    "Приложение 1) in the author's manual Talmud-" + MANUAL_VERSION
                    + ".mdx — class size by ROOT COUNT (systematic productivity), "
                    "not corpus token frequency. Built for H1054.",
            "source": "Talmud-" + MANUAL_VERSION + ".mdx, Приложение 1 "
                      "(I.E. Tolchelnikov)",
            "generator": "tools/aorist_class_census.py",
            "class_key": {"1": "root", "2": "thematic a-", "3": "reduplicated",
                          "4": "s-", "5": "is-", "6": "sis-", "7": "sa-"},
            "pada_caveat": "pada is a per-root column, not per-aorist-class — "
                           "the per-class pada split is indicative only",
        },
        "roots_total": len(entries),
        "roots_with_no_aorist_class": no_aorist,
        "roots_per_class": dict(per_class),
        "per_class_pada": {c: dict(v) for c, v in per_class_pada.items() if v},
        "per_class_set": {c: dict(v) for c, v in per_class_set.items() if v},
        "top_class_combinations": dict(combo.most_common(15)),
        "roots": [{"id": e["id"], "pada": e["pada"], "classes": e["classes"]}
                  for e in entries],
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}")
    print(f"  roots total           : {len(entries)}")
    print(f"  no aorist class       : {no_aorist}")
    print(f"  roots per class       : {dict(sorted(per_class.items()))}")
    for c in sorted(per_class_pada):
        if per_class_pada[c]:
            print(f"  class {c} pada          : {dict(per_class_pada[c])}")
    for c in sorted(per_class_set):
        if per_class_set[c]:
            print(f"  class {c} set           : {dict(per_class_set[c])}")


if __name__ == "__main__":
    main()
