#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_widget_data.py — Phase-2 compact widget feed for the Talmud санскрита.

Reads the Phase-3 master crosswalk ``data/whitney_talmud.json`` (930 verbal
roots + 15 nominal) and emits a SMALL, browser-friendly ``data/widget_roots.json``
so the Docusaurus widgets (Ablaut machine, seṭ/aniṭ tree, …) can import a
few-KB example set instead of bundling the 776-KB master file into the client.

The subset is deliberately curated:
  * ``ablaut_examples`` — the ``first`` teaching cohort (DCS-rank ≤ 50), each with
    the fields the Ablaut machine needs to auto-select a series and show grades.
  * ``set_examples`` — first + second cohort roots that carry a DERIVED seṭ/aniṭ
    flag AND a p.p.p. (the evidence the decision tree cites). Advisory, gated.
  * ``nominal`` — the author's 15 Приложение-2 nominal roots, verbatim, for the
    Heteroclisis stem-map.

Everything here is a projection of the master file; provenance (derived vs
verbatim) is preserved so widgets can label it. Regenerate whenever
``whitney_talmud.json`` changes:  python tools/build_widget_data.py
(run from the TolchelnikovTalmud_2026 folder).
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_FOLDER = os.path.dirname(HERE)
MASTER = os.path.join(REPO_FOLDER, "data", "whitney_talmud.json")
ZMAP = os.path.join(REPO_FOLDER, "data", "z_root_map.json")
OUT = os.path.join(REPO_FOLDER, "data", "widget_roots.json")


def load_z_urls():
    """whitney_no -> samskrtam.ru/z/ verb.php URL (H329 deep-link; {} if map absent).

    ~107 Whitney roots have >1 /z/ row: a primary alphabetical listing (low id) plus a
    high-id (800-900s) s-mobile/variant cross-reference (e.g. kṛ id=594 vs skṛ id=895).
    Deep-link to the primary = the lowest z_id per whitney_no."""
    if not os.path.exists(ZMAP):
        return {}
    z = json.load(open(ZMAP, encoding="utf-8"))
    best = {}
    for r in z["roots"]:
        w = r.get("whitney_no")
        if not w:
            continue
        if w not in best or r["z_id"] < best[w][0]:
            best[w] = (r["z_id"], r["z_url"])
    return {w: url for w, (_, url) in best.items()}


def slim_ablaut(r, z_url=None):
    """Fields the Ablaut machine needs to seat a real root in its series."""
    return {
        "root": r["root_iast"],
        "gloss": r["gloss"],
        "class": r["class"],
        "ryad": r["ryad"],
        "ryad_confidence": r["ryad_confidence"],
        "ryad_note": r.get("ryad_note"),
        "set": r["set"],
        "dcs_rank": r["dcs_rank"],
        "z_url": z_url,
    }


def slim_set(r, z_url=None):
    return {
        "root": r["root_iast"],
        "gloss": r["gloss"],
        "ppp": r["ppp"],
        "set": r["set"],
        "set_confidence": r.get("set_confidence"),
        "dcs_rank": r["dcs_rank"],
        "z_url": z_url,
    }


def main():
    with open(MASTER, encoding="utf-8") as f:
        master = json.load(f)
    verbal = master["verbal_roots"]
    nominal = master["nominal_appendix2"]
    z_urls = load_z_urls()

    # De-dup by (root, ryad) so homonyms don't clutter the example picker;
    # keep the highest-frequency (lowest dcs_rank) representative.
    def rank_key(r):
        return r["dcs_rank"] if r.get("dcs_rank") is not None else 10**9

    first = [r for r in verbal if r.get("cohort") == "first"]
    first_second = [r for r in verbal if r.get("cohort") in ("first", "second")]

    seen = set()
    ablaut = []
    for r in sorted(first, key=rank_key):
        key = (r["root_iast"], r["ryad"])
        if key in seen:
            continue
        seen.add(key)
        ablaut.append(slim_ablaut(r, z_urls.get(r["whitney_no"])))

    seen = set()
    setex = []
    for r in sorted(first_second, key=rank_key):
        if not r.get("set") or not r.get("ppp"):
            continue
        key = (r["root_iast"], r["set"])
        if key in seen:
            continue
        seen.add(key)
        setex.append(slim_set(r, z_urls.get(r["whitney_no"])))

    out = {
        "_meta": {
            "what": "Compact Phase-2 widget feed projected from whitney_talmud.json",
            "generator": "tools/build_widget_data.py",
            "provenance": "ryad/set are DERIVED proposals (see whitney_talmud.schema.md); "
            "gloss/class/ppp/dcs_rank are verbatim WhitneyRoots; z_url deep-links to the "
            "samskrtam.ru/z/ verb-DB paradigm (H329, via data/z_root_map.json).",
            "counts": {
                "ablaut_examples": len(ablaut),
                "set_examples": len(setex),
                "nominal": len(nominal),
            },
        },
        "ablaut_examples": ablaut,
        "set_examples": setex,
        "nominal": nominal,
    }
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT}")
    print(f"  ablaut_examples={len(ablaut)}  set_examples={len(setex)}  nominal={len(nominal)}")


if __name__ == "__main__":
    main()
