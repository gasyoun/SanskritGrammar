#!/usr/bin/env python3
"""panini_sutra.py — resolve Aṣṭādhyāyī sūtra references and keywords.

Backs the /panini-sutra-lookup skill. Canonical data source: the public
ashtadhyayi.com dataset (github.com/ashtadhyayi-com/data, sutraani/*.txt),
which is the same data that powers the site — no scraping.

Two modes:
    by-reference   panini_sutra.py 6.1.68
    by-keyword     panini_sutra.py --search "वृद्धि"      (Devanagari)
                   panini_sutra.py --search "vrddhi"       (IAST/roman)
                   panini_sutra.py --search "guna"

Output (default): the Devanagari sūtra, IAST, S.C. Vasu's English gloss when
available, the ready-to-paste citation `ср. Aṣṭādhyāyī a.p.n`, and the site URL
https://ashtadhyayi.com/sutraani/a/p/n . Pass --commentary to also pull the
Kāśikā / Mahābhāṣya (bhashya) / Kātyāyana-vārttika text mapped to that sūtra
(these partly serve the commentary-corpus need — see RWS_REPORT.md §6.7).

Data is cached once under tools/panini_cache/. Re-fetch with --refresh.
"""
import sys
import os
import json
import argparse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

RAW = "https://raw.githubusercontent.com/ashtadhyayi-com/data/master/sutraani/"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panini_cache")

# filename -> is it the core sutra list (known schema) vs auxiliary commentary
CORE = "data.txt"
AUX = {
    "vasu": "vasu_english.txt",
    "sutrartha": "sutrartha.txt",
    "sutrartha_en": "sutrartha_english.txt",
    "kashika": "kashika.txt",
    "bhashya": "bhashya.txt",       # Mahābhāṣya
    "vartika": "vartika.txt",       # Kātyāyana vārttikas
}


def fetch(fname, refresh=False):
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, fname)
    if refresh or not os.path.exists(path):
        url = RAW + fname
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                data = r.read()
            with open(path, "wb") as f:
                f.write(data)
        except Exception as e:  # noqa: BLE001
            print(f"[warn] could not fetch {fname}: {e}", file=sys.stderr)
            return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_json_list(fname, refresh=False):
    """Index a sutraani/*.txt by 5-digit sūtra id.

    Two schemas occur in the dataset:
      - core data.txt : {name, data:[{i,a,p,n,s,e}, ...]}  -> index by 'i'
      - commentaries  : {"11001": "text...", ...}          -> flat id->str
    """
    raw = fetch(fname, refresh)
    if raw is None:
        return {}
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[warn] {fname} is not JSON as expected: {e}", file=sys.stderr)
        return {}
    # flat id -> string (commentary files)
    if isinstance(obj, dict) and "data" not in obj:
        return {str(k): v for k, v in obj.items()}
    rows = obj.get("data", obj if isinstance(obj, list) else [])
    idx = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        key = str(row.get("i") or row.get("sutra_id") or "")
        if key:
            idx[key] = row
    return idx


def sid(a, p, n):
    """a.p.n -> 5-digit id, e.g. 6,1,68 -> '61068'."""
    return f"{int(a)}{int(p):01d}{int(n):03d}"


def strip_html(t):
    import re
    t = re.sub(r"<[^>]+>", "", t)
    return re.sub(r"[ \t]+\n", "\n", t).strip()


def aux_text(row):
    """Pull the human text out of an auxiliary entry (str or dict)."""
    if isinstance(row, str):
        return strip_html(row)
    if not isinstance(row, dict):
        return ""
    for k in ("text", "e", "s", "content", "meaning", "translation"):
        v = row.get(k)
        if isinstance(v, str) and v.strip():
            return strip_html(v)
    strs = [v for v in row.values() if isinstance(v, str) and len(v) > 3]
    return strip_html(max(strs, key=len)) if strs else ""


def render(row, sutras, want_commentary, refresh):
    a, p, n = row["a"], row["p"], row["n"]
    cite = f"{a}.{p}.{n}"
    print(f"## Aṣṭādhyāyī {cite}")
    print()
    print(f"- **сутра (деванагари):** {row.get('s', '')}")
    print(f"- **IAST:** {row.get('e', '')}")
    key = str(row["i"])
    vasu = load_json_list(AUX["vasu"], refresh)
    if key in vasu:
        t = aux_text(vasu[key])
        if t:
            print(f"- **Vasu (англ.):** {t}")
    sen = load_json_list(AUX["sutrartha_en"], refresh)
    if key in sen:
        t = aux_text(sen[key])
        if t:
            print(f"- **sūtrārtha (англ.):** {t}")
    print(f"- **цитата для текста:** `ср. Aṣṭādhyāyī {cite}`")
    print(f"- **URL:** https://ashtadhyayi.com/sutraani/{a}/{p}/{n}")
    if want_commentary:
        for label, k in (("Kāśikā", "kashika"),
                         ("Mahābhāṣya", "bhashya"),
                         ("Vārttika (Kātyāyana)", "vartika")):
            idx = load_json_list(AUX[k], refresh)
            if key in idx:
                t = aux_text(idx[key])
                if t:
                    print()
                    print(f"### {label}")
                    print(t)
    print()


def main():
    ap = argparse.ArgumentParser(description="Resolve Aṣṭādhyāyī sūtras.")
    ap.add_argument("ref", nargs="?", help="sutra reference a.p.n, e.g. 6.1.68")
    ap.add_argument("--search", help="keyword (Devanagari / IAST / English)")
    ap.add_argument("--commentary", action="store_true",
                    help="also print Kāśikā / Mahābhāṣya / Vārttika")
    ap.add_argument("--refresh", action="store_true", help="re-download cache")
    ap.add_argument("--limit", type=int, default=10, help="max search hits")
    args = ap.parse_args()

    sutras = load_json_list(CORE, args.refresh)
    if not sutras:
        print("No sūtra data — check network / cache.", file=sys.stderr)
        sys.exit(1)

    if args.ref:
        parts = args.ref.replace(",", ".").split(".")
        if len(parts) != 3:
            print("Reference must be a.p.n, e.g. 6.1.68", file=sys.stderr)
            sys.exit(2)
        key = sid(*parts)
        if key not in sutras:
            print(f"Сутра {args.ref} не найдена (id {key}).", file=sys.stderr)
            sys.exit(3)
        render(sutras[key], sutras, args.commentary, args.refresh)
    elif args.search:
        q = args.search.strip().lower()
        hits = [r for r in sutras.values()
                if q in str(r.get("s", "")).lower()
                or q in str(r.get("e", "")).lower()]
        if not hits:
            print(f"Ничего не найдено по «{args.search}».")
            return
        print(f"_{len(hits)} совпадений по «{args.search}» "
              f"(показаны первые {min(args.limit, len(hits))}):_\n")
        for r in hits[:args.limit]:
            render(r, sutras, args.commentary, args.refresh)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
