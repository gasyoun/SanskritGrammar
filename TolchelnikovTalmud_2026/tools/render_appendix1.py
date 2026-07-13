#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_appendix1.py — emit the first-cohort catalog table for Приложение 1
from data/whitney_talmud.json.

The full 930-root catalog lives in the JSON; the MDX page shows the
teaching-relevant **first cohort** (DCS-rank ≤ 50) as a static, auto-generated
table. Every Ряд/seṭ cell is the author's own value from Приложение 1 of the
manual (H329 Phase 3 — issue #50 ruling); a `—` means the author does not
catalog that root, so no series is asserted for it.

Writes the fenced markdown table between the AUTOGEN markers in
talmud-appendix-1.mdx. Idempotent.

Usage:  python tools/render_appendix1.py
"""
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
FOLDER = os.path.dirname(HERE)
JSON = os.path.join(FOLDER, "data", "whitney_talmud.json")
ZMAP = os.path.join(FOLDER, "data", "z_root_map.json")
MDX = os.path.join(FOLDER, "talmud-appendix-1.mdx")

BEGIN = "{/* AUTOGEN:appendix1-cohort BEGIN — regenerate with tools/render_appendix1.py */}"
END = "{/* AUTOGEN:appendix1-cohort END */}"


def cell(v):
    return "—" if v in (None, "", []) else str(v)


def load_z_urls():
    """whitney_no -> samskrtam.ru/z/ verb.php URL (H329 deep-link; {} if map absent).

    Where a Whitney root has >1 /z/ row (primary listing + a high-id s-mobile/variant
    cross-reference, e.g. kṛ id=594 vs skṛ id=895), deep-link to the lowest z_id."""
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


def main():
    d = json.load(open(JSON, encoding="utf-8"))
    z_urls = load_z_urls()
    first = [r for r in d["verbal_roots"] if r["cohort"] == "first"]
    first.sort(key=lambda r: (r["dcs_rank"] if r["dcs_rank"] else 10**9, r["root_iast"]))

    lines = []
    lines.append("| DCS-ранг | № Уитни | √ | Ряд | Тип | seṭ | Класс | p.p.p. | Значение | /z/ |")
    lines.append("| ---: | ---: | :--- | :---: | :---: | :---: | :--- | :--- | :--- | :---: |")
    for r in first:
        cls = "/".join(r["class"]) if r["class"] else "—"
        zurl = z_urls.get(r["whitney_no"])
        zcell = f"[↗]({zurl})" if zurl else "—"
        lines.append(
            f"| {cell(r['dcs_rank'])} | {cell(r['whitney_no'])} | "
            f"`{r['root_iast']}` | {cell(r['ryad'])} | {cell(r.get('tip'))} | {cell(r['set'])} | "
            f"{cls} | {cell(r['ppp'])} | {cell(r['gloss'])} | {zcell} |"
        )
    table = "\n".join(lines)

    counts = d["_meta"]["counts"]
    intro = (
        f"Ниже — **первая когорта** ({len(first)} наиболее частотных по DCS корней, ранг ≤ 50), "
        f"с которой начинается самостоятельное изучение. Ряд, Тип и seṭ приведены "
        f"**по каталогу Приложения 1** из руководства (авторские значения). Полный каталог всех "
        f"{counts['verbal_roots']} глагольных корней Уитни — в машиночитаемом виде в "
        f"[`data/whitney_talmud.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/whitney_talmud.json), "
        f"а авторский каталог целиком — в "
        f"[`data/talmud_appendix1.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/talmud_appendix1.json). "
        f"Ссылка **↗** в столбце «/z/» ведёт на полную сгенерированную парадигму корня в "
        f"базе [samskrtam.ru/z/](https://samskrtam.ru/z/) (Толчельников/Широбоков)."
    )
    block = f"{BEGIN}\n\n{intro}\n\n{table}\n\n{END}"

    src = open(MDX, encoding="utf-8").read()
    if BEGIN in src and END in src:
        pre = src[: src.index(BEGIN)]
        post = src[src.index(END) + len(END):]
        src = pre + block + post
    else:
        src = src.rstrip() + "\n\n" + block + "\n"
    open(MDX, "w", encoding="utf-8").write(src)
    print(f"rendered {len(first)} first-cohort roots into {os.path.basename(MDX)}")


if __name__ == "__main__":
    main()
