#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""parse_appendix1.py — extract the author's own Приложение 1 verb-root catalog
from the authoritative manual ``Talmud-2.1.6.mdx`` into ``data/talmud_appendix1.json``.

This is the SOURCE OF TRUTH for Ряд / Тип / seṭ, per the author's ruling on
issue #50 (Tolchelnikov, 08-07-2026): the latest manual is the sole authority for
these values; derived proposals and the older samskrtam.ru/z/ snapshot are NOT.
The verbatim values are read exactly as printed — un-indexed rows stay un-indexed
(ruling #3), no ``0``-index variants (a Table-2 artefact the author disowns).

Приложение 1 is a Pandoc grid table with no header row. Column semantics come from
the manual's own tables (NOT the split-page legend, which conflated Тип and seṭ):

  col1  root id label     (e.g. ``AKṢ.1`` — deep-morphology headword)
  col2  √ citation/deep   (e.g. ``akṣ``, ``øs``, ``iøj``)
  col3  homonym (manual)  (author's own homonym index; may differ from Whitney's)
  col4  Список Уитни      (Whitney nomenclature ref = the join key; ``NA`` if absent)
  col5  Тип               (Table 5: I/II/III/IV — type of alternation)
  col6  Ряд               (Table 4: A₁…N₂, or bare A/I/U/R/L/M/N when un-indexed)
  col7  seṭ               (Table 8: s=seṭ · a=aniṭ · v/v1..v4=veṭ · blank=undefined)
  col8  pada              (P/U/Ā)
  col9+ class / aorist / other forms / primary suffixes  (not consumed here)

Only PRIMARY rows (col1 non-empty) are captured — allomorph continuation rows
(empty col1: e.g. ``n̥ś`` under ``AŚ.1``) are alternate stems, not catalog entries.

Usage:  python tools/parse_appendix1.py
Run from the TolchelnikovTalmud_2026 folder.
"""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
MDX = os.path.join(FOLDER, "Talmud-2.1.6.mdx")
OUT = os.path.join(FOLDER, "data", "talmud_appendix1.json")
MANUAL_VERSION = "2.1.6"

FN_RE = re.compile(r"\[\^[^\]]*\]")          # pandoc footnote refs [^67]
PAREN_RE = re.compile(r"\s*\([^)]*\)")        # parentheticals, e.g. "kṛ (skṛ)"

# Table 8: seṭ-параметр code -> category. v1..v4 are veṭ sub-classes (kept in set_code).
SET_MAP = {"s": "seṭ", "a": "aniṭ", "v": "veṭ",
           "v1": "veṭ", "v2": "veṭ", "v3": "veṭ", "v4": "veṭ", "": None}


def clean(s):
    s = s.replace("\xa0", " ").strip()
    s = s.replace("**", "")
    s = FN_RE.sub("", s)
    return s.strip()


def ryad_conv(s):
    """As-printed Ряд: convert pandoc ``~1~``/``~2~`` to ₁/₂; leave bare letters bare."""
    s = clean(s)
    s = s.replace("~1~", "₁").replace("~2~", "₂").replace("~0~", "₀")
    # stray ascii-digit subscript survivors (one row prints "I1" not "I~1~")
    s = re.sub(r"^([AIURLMN])([012])$",
               lambda m: m.group(1) + "₀₁₂"[int(m.group(2))], s)
    return s


def parse_wref(wref):
    """(whitney_num|None, [spellings]) from col4, stripping parentheticals.

    ``"1 aś, aṃś"`` -> (``"1"``, [``"aś"``, ``"aṃś"``]); ``"NA"`` -> (None, [])."""
    w = wref.strip()
    if not w or w.upper() == "NA":
        return None, []
    m = re.match(r"^(\d+)\s+(.*)$", w)
    if m:
        num, rest = m.group(1), m.group(2)
    else:
        num, rest = None, w
    spellings = []
    for part in rest.split(","):
        p = PAREN_RE.sub("", part).strip()
        if p:
            spellings.append(p)
    return num, spellings


def extract():
    lines = open(MDX, encoding="utf-8").read().split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("# Приложение 1"))
    end = next(i for i, l in enumerate(lines) if l.startswith("# Приложение 2"))
    block = lines[start:end]

    catalog = []
    for ln in block:
        if not ln.startswith("|"):
            continue
        parts = ln.rstrip("\n").split("|")
        if len(parts) < 9:
            continue
        col1 = clean(parts[1])
        if not col1 or set(col1) <= set("-=:+ "):
            continue  # separator row / allomorph continuation (empty col1)
        wref = clean(parts[4])
        wnum, spellings = parse_wref(wref)
        set_code = clean(parts[7])
        catalog.append({
            "id": col1,
            "root": clean(parts[2]),
            "homonym": clean(parts[3]) or None,
            "whitney_ref": wref,
            "whitney_num": wnum,
            "whitney_spellings": spellings,
            "tip": clean(parts[5]) or None,
            "ryad": ryad_conv(parts[6]) or None,
            "set_code": set_code or None,
            "set": SET_MAP.get(set_code, None),
            "pada": clean(parts[8]) if len(parts) > 8 else None,
        })
    return catalog


def main():
    catalog = extract()
    from collections import Counter
    set_counts = Counter(r["set"] or "null" for r in catalog)
    ryad_counts = Counter(r["ryad"] or "null" for r in catalog)
    absent = sum(1 for r in catalog if not r["whitney_spellings"])

    payload = {
        "_meta": {
            "what": "The author's own Приложение 1 verb-root catalog, parsed verbatim "
                    "from the authoritative manual Talmud-" + MANUAL_VERSION + ".mdx. "
                    "SOURCE OF TRUTH for Ряд/Тип/seṭ per Tolchelnikov's ruling on issue #50.",
            "source": "Talmud-" + MANUAL_VERSION + ".mdx, Приложение 1 (I.E. Tolchelnikov)",
            "manual_version": MANUAL_VERSION,
            "generator": "tools/parse_appendix1.py",
            "columns": {
                "tip": "Table 5 — type of alternation I/II/III/IV",
                "ryad": "Table 4 — ablaut series A₁…N₂ (bare where un-indexed, ruling #3)",
                "set": "Table 8 — seṭ/aniṭ/veṭ; set_code keeps s/a/v1..v4",
                "whitney_ref": "Список Уитни — Whitney nomenclature (join key); NA if absent",
            },
            "counts": {
                "roots": len(catalog),
                "absent_from_whitney": absent,
                "set": dict(set_counts),
                "ryad": dict(ryad_counts),
            },
        },
        "roots": catalog,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}")
    print(f"  roots               : {len(catalog)}")
    print(f"  absent from Whitney : {absent}")
    print(f"  set                 : {dict(set_counts)}")


if __name__ == "__main__":
    main()
