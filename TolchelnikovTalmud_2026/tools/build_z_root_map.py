#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build data/z_root_map.json — the Whitney-no <-> samskrtam.ru/z/ verb-id join map.

Source: the single /z/ index page (data/raw_cache/z_index.html, gitignored raw), which
carries one row per verb root of Shirobokov A.P.'s interactive DB of Tolchelnikov's
«Санскритская морфология» v1.1.0. Columns (10):

    Verb root | Series | Verb by Whitney | seṭ-aniṭ | Type | P/Ā | PrS | AoS | Verb form | Translation

We join each row to data/whitney_talmud.json (keyed by whitney_no, with root_iast+homonym)
via the "Verb by Whitney" cell ("<homonym> <rootform>[, variant]") and REPORT the Ряд/seṭ
agreement rate vs our Phase-3 DERIVED values (H329). We DO NOT scrape the 905 detail pages:
the index alone supplies the join map + Ряд/seṭ, and deep-links only need z_id.

Emits:
    data/z_root_map.json          — the derived join map (committed)
    (report printed to stdout; persisted by the caller into the reconciliation log)

Provenance: index page authored by Толчельников И.Е. (source) + Широбоков А.П. (DB).
Run: python tools/build_z_root_map.py
"""
import json
import re
import sys
import unicodedata
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = __file__.rsplit("tools", 1)[0]
RAW = HERE + "data/raw_cache/z_index.html"
WT = HERE + "data/whitney_talmud.json"
OUT = HERE + "data/z_root_map.json"

# seṭ-aniṭ column code -> normalized value. v/v1..v5 are veṭ (optional) subtypes;
# "0" is the DB's unmarked/not-applicable slot; "s(ī?)" is a seṭ flagged uncertain.
SET_CODE = {"s": "seṭ", "a": "aniṭ", "0": None, "": None}


def norm_set(code):
    code = code.strip()
    if code in SET_CODE:
        return SET_CODE[code], code
    if code.startswith("v"):
        return "veṭ", code
    if code.startswith("s"):  # s(ī?)
        return "seṭ", code
    return None, code


SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")


def ryad_ascii(v):
    """A₁ -> A1 ; A1 -> A1 ; None-safe. Normalizes subscript digits to ASCII."""
    if not v:
        return None
    return v.translate(SUB).strip()


def nfc(s):
    return unicodedata.normalize("NFC", s) if s else s


def parse_verb_by_whitney(cell):
    """'1 aś, aṃś' -> (homonym='1', root='aś'); 'as' -> (None, 'as');
    '1 kṛ (skṛ)' -> ('1', 'kṛ') — trailing (alt-form) parentheticals are dropped."""
    cell = nfc(cell.strip())
    # take the part before the first comma (drop variant forms)
    head = cell.split(",")[0].strip()
    m = re.match(r"^(\d+)\s+(.+)$", head)
    if m:
        hom, root = m.group(1), m.group(2).strip()
    else:
        hom, root = None, head
    # drop a trailing parenthetical alternate form: 'kṛ (skṛ)' -> 'kṛ'
    root = re.sub(r"\s*\([^)]*\)\s*$", "", root).strip()
    return hom, root


def parse_index(html):
    body = html.split("<tbody>")[1].split("</tbody>")[0]
    rows = re.findall(r"<tr>(.*?)</tr>", body, re.S)
    recs = []
    for r in rows:
        cells = re.findall(r"<td[^>]*>(.*?)</td>", r, re.S)
        idm = re.search(r"verb\.php\?id=(\d+)", cells[0])
        txt = [nfc(re.sub(r"<[^>]*>", "", c).strip()) for c in cells]
        recs.append({"z_id": int(idm.group(1)) if idm else None, "cells": txt})
    return recs


def main():
    html = open(RAW, encoding="utf-8").read()
    wt = json.load(open(WT, encoding="utf-8"))["verbal_roots"]

    # index whitney_talmud by (root_iast NFC, homonym) and by root alone
    by_key = {}
    by_root = {}
    for e in wt:
        rt = nfc(e["root_iast"])
        by_key[(rt, e.get("homonym"))] = e
        by_root.setdefault(rt, []).append(e)

    recs = parse_index(html)
    out = []
    stats = Counter()
    ryad_cmp = Counter()  # agree / disagree / z_only / wt_only
    set_cmp = Counter()
    disagreements = []

    for r in recs:
        c = r["cells"]
        if len(c) < 10 or r["z_id"] is None:
            stats["skipped_malformed"] += 1
            continue
        hom, root = parse_verb_by_whitney(c[2])
        z_series = c[1].strip() or None
        z_set, z_set_code = norm_set(c[3])
        rec = {
            "z_id": r["z_id"],
            "root": root,
            "z_homonym": hom,
            "verb_by_whitney": c[2],
            "z_series": z_series,          # Ряд, ASCII (A1, U2, N0, L, ...)
            "z_set": z_set,               # seṭ / aniṭ / veṭ / None
            "z_set_code": z_set_code,     # raw code (s, a, v1..v5, 0, s(ī?))
            "z_pres_class": c[6].strip() or None,  # PrS column
            "z_aorist": c[7].strip() or None,      # AoS column
            "z_gloss_ru": c[9].strip() or None,
            "z_url": f"https://samskrtam.ru/z/verb.php?id={r['z_id']}",
            "whitney_no": None,
            "match": None,
        }
        # join
        e = by_key.get((root, hom))
        if e is None and hom is not None:
            e = by_key.get((root, None))  # /z/ gave homonym, wt has none
        if e is None:
            cands = by_root.get(root, [])
            if len(cands) == 1:
                e = cands[0]
                rec["match"] = "root_unique"
            elif len(cands) > 1:
                rec["match"] = "ambiguous_homonym"
                stats["match_ambiguous"] += 1
            else:
                rec["match"] = "no_whitney_row"
                stats["match_none"] += 1
        else:
            rec["match"] = "exact" if rec["match"] is None else rec["match"]

        if e is not None:
            rec["whitney_no"] = e["whitney_no"]
            if rec["match"] is None or rec["match"] == "exact":
                rec["match"] = "exact"
            stats["matched"] += 1
            # Ряд reconciliation
            zr, wr = rec["z_series"], ryad_ascii(e.get("ryad"))
            if zr and wr:
                if zr == wr:
                    ryad_cmp["agree"] += 1
                else:
                    ryad_cmp["disagree"] += 1
                    disagreements.append(
                        {"whitney_no": e["whitney_no"], "root": root, "z_id": rec["z_id"],
                         "field": "ryad", "z": zr, "derived": wr,
                         "z_conf": None, "derived_conf": e.get("ryad_confidence")})
            elif zr and not wr:
                ryad_cmp["z_only"] += 1
            elif wr and not zr:
                ryad_cmp["wt_only"] += 1
            # seṭ reconciliation (compare only where both assert seṭ/aniṭ; veṭ/None separate)
            zs, ws = rec["z_set"], e.get("set")
            if zs in ("seṭ", "aniṭ") and ws in ("seṭ", "aniṭ"):
                if zs == ws:
                    set_cmp["agree"] += 1
                else:
                    set_cmp["disagree"] += 1
                    disagreements.append(
                        {"whitney_no": e["whitney_no"], "root": root, "z_id": rec["z_id"],
                         "field": "set", "z": zs, "derived": ws,
                         "z_conf": None, "derived_conf": e.get("set_confidence")})
            elif zs and ws is None:
                set_cmp["z_fills_null"] += 1
            elif zs == "veṭ" and ws in ("seṭ", "aniṭ"):
                set_cmp["z_veṭ_vs_wt"] += 1
            elif ws and zs is None:
                set_cmp["wt_only"] += 1
        out.append(rec)

    meta = {
        "_meta": {
            "what": "Whitney-no <-> samskrtam.ru/z/ verb-id join map + reconciliation of "
                    "/z/'s authoritative Ряд/seṭ vs our Phase-3 DERIVED values (H329).",
            "source": {
                "z_index": "https://samskrtam.ru/z/ (single index page; no detail-page scrape)",
                "z_author": "Толчельников И.Е. «Санскритская морфология» v1.1.0 (data); "
                            "Широбоков А.П. (DB/algorithmisation)",
                "join_target": "data/whitney_talmud.json (whitney_no + root_iast + homonym)",
            },
            "generator": "tools/build_z_root_map.py",
            "join_key": "«Verb by Whitney» cell = '<homonym> <rootform>' -> (root_iast, homonym)",
            "notes": [
                "z_series (Ряд) incl. 0-variants (N0/I0/R0/U0/M0) and L absent from Talmud Table 2.",
                "z_set_code: s=seṭ, a=aniṭ, v/v1..v5=veṭ, 0=unmarked, s(ī?)=seṭ uncertain.",
                "Author-gating (H329): sourced Ряд/seṭ enter running text only as Ivan-approved "
                "footnotes, never silent overwrite.",
            ],
            "counts": {
                "z_rows": len(recs),
                "matched": stats["matched"],
                "match_ambiguous_homonym": stats["match_ambiguous"],
                "no_whitney_row": stats["match_none"],
            },
            "ryad_reconciliation": dict(ryad_cmp),
            "set_reconciliation": dict(set_cmp),
        },
        "roots": out,
    }
    json.dump(meta, open(OUT, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=1)

    # ---- report ----
    print("=== z_root_map build report ===")
    print(f"index rows            : {len(recs)}")
    print(f"matched to whitney_no : {stats['matched']}")
    print(f"ambiguous homonym     : {stats['match_ambiguous']}")
    print(f"no whitney row        : {stats['match_none']}")
    print()
    ra = ryad_cmp["agree"]; rd = ryad_cmp["disagree"]
    tot = ra + rd
    print("--- Ряд reconciliation (both sides present) ---")
    print(f"  agree     : {ra}")
    print(f"  disagree  : {rd}")
    if tot:
        print(f"  agreement : {ra}/{tot} = {100*ra/tot:.1f}%")
    print(f"  z-only (Ряд present in /z/, absent in derived): {ryad_cmp['z_only']}")
    print(f"  derived-only                                  : {ryad_cmp['wt_only']}")
    print()
    sa = set_cmp["agree"]; sd = set_cmp["disagree"]; stot = sa + sd
    print("--- seṭ reconciliation (both assert seṭ/aniṭ) ---")
    print(f"  agree     : {sa}")
    print(f"  disagree  : {sd}")
    if stot:
        print(f"  agreement : {sa}/{stot} = {100*sa/stot:.1f}%")
    print(f"  /z/ fills our null : {set_cmp['z_fills_null']}")
    print(f"  /z/ veṭ vs our seṭ/aniṭ : {set_cmp['z_veṭ_vs_wt']}")
    print(f"  derived-only            : {set_cmp['wt_only']}")
    print()
    print(f"disagreements logged: {len(disagreements)} (see z_root_map + reconciliation report)")
    # dump disagreements for the report
    json.dump(disagreements, open(HERE + "data/raw_cache/z_disagreements.json", "w",
              encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
