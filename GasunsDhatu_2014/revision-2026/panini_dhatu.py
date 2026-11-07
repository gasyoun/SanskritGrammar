#!/usr/bin/env python3
"""panini_dhatu.py — resolve Dhātupāṭha (Pāṇinian root list) references and keywords.

Companion to panini_sutra.py (H413); this one is H7815. Canonical data source:
the public ashtadhyayi.com dataset (github.com/ashtadhyayi-com/data,
dhatu/data.txt) — the same data that powers the site, no scraping.

Credit: data © ashtadhyayi.com — free to use with appropriate credits
(https://ashtadhyayi.com/about). Credit ashtadhyayi.com when reusing output.

Two modes:
    by-reference   panini_dhatu.py 01.0001     (baseindex gaṇa.sūtra)
                   panini_dhatu.py 1010001     (numeric id)
                   panini_dhatu.py bhū         (root, IAST or Devanagari)
    by-keyword     panini_dhatu.py --search "bhū"     (IAST/roman)
                   panini_dhatu.py --search "सत्ता"   (Devanagari)
                   panini_dhatu.py --search "exist"   (English meaning)

Output (default, format MG 07-11-2026): the root in IAST, its English meaning
(`artha_english` — the dhātupāṭha has no Vasu layer in the dataset), gaṇa/pada,
the ready-to-paste citation `ср. Dhātupāṭha gaṇa.sūtra (root)`, and the site URL
https://ashtadhyayi.com/dhatu/<id> . No Devanagari in the default output
(--devanagari adds the Devanagari line). Pass --prayoga to also print usage
attestations from dhatuprayogas.txt (keyed by baseindex).

Data is cached once under panini_cache/ (shared with panini_sutra.py; this
tool's files are prefixed dhatu_). Re-fetch with --refresh.
"""
import sys
import os
import json
import argparse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

RAW = "https://raw.githubusercontent.com/ashtadhyayi-com/data/master/dhatu/"
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "panini_cache")

CORE = "data.txt"                 # remote name; cached as dhatu_data.txt
PRAYOGA = "dhatuprayogas.txt"     # remote name == cache name (unique already)

# gaṇa number -> traditional name (bhvādi … churādi)
GANAS = {1: "bhvādi", 2: "adādi", 3: "juhotyādi", 4: "divādi", 5: "svādi",
         6: "tudādi", 7: "curādi", 8: "tanādi", 9: "kryādi", 10: "churādi"}
PADAS = {"P": "parasmaipada", "A": "ātmanepada", "U": "ubhayapada", "-": "—"}

# Devanagari -> IAST (dhatu/artha fields are Devanagari; output is IAST-only)
CONS = {
    "क": "k", "ख": "kh", "ग": "g", "घ": "gh", "ङ": "ṅ",
    "च": "c", "छ": "ch", "ज": "j", "झ": "jh", "ञ": "ñ",
    "ट": "ṭ", "ठ": "ṭh", "ड": "ḍ", "ढ": "ḍh", "ण": "ṇ",
    "त": "t", "थ": "th", "द": "d", "ध": "dh", "न": "n",
    "प": "p", "फ": "ph", "ब": "b", "भ": "bh", "म": "m",
    "य": "y", "र": "r", "ल": "l", "व": "v",
    "श": "ś", "ष": "ṣ", "स": "s", "ह": "h", "ळ": "ḷ",
}
VOWELS = {"अ": "a", "आ": "ā", "इ": "i", "ई": "ī", "उ": "u", "ऊ": "ū",
          "ऋ": "ṛ", "ॠ": "ṝ", "ऌ": "ḷ", "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au"}
MATRAS = {"ा": "ā", "ि": "i", "ी": "ī", "ु": "u", "ू": "ū", "ृ": "ṛ", "ॄ": "ṝ",
          "ॢ": "ḷ", "े": "e", "ै": "ai", "ो": "o", "ौ": "au"}
SIGNS = {"ं": "ṃ", "ः": "ḥ", "ँ": "m̐", "्": "", "़": "", "ऽ": "’",
         "।": ".", "॥": ".."}


def deva_to_iast(s):
    """Transliterate a short Devanagari string (root / artha) to IAST."""
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch in CONS:
            nxt = s[i + 1] if i + 1 < len(s) else ""
            if nxt == "्":                       # virāma — suppress inherent a
                out.append(CONS[ch]); i += 2
            elif nxt in MATRAS:
                out.append(CONS[ch] + MATRAS[nxt]); i += 2
            else:
                out.append(CONS[ch] + "a"); i += 1
        elif ch in VOWELS:
            out.append(VOWELS[ch]); i += 1
        elif ch in MATRAS:                        # stray matra
            out.append(MATRAS[ch]); i += 1
        elif ch in SIGNS:
            out.append(SIGNS[ch]); i += 1
        else:
            out.append(ch); i += 1
    return "".join(out)


def fetch(remote, refresh=False):
    """Fetch remote (under dhatu/) into the shared cache under a dhatu_ name."""
    os.makedirs(CACHE, exist_ok=True)
    cachename = remote if remote.startswith("dhatu") else "dhatu_" + remote
    path = os.path.join(CACHE, cachename)
    if refresh or not os.path.exists(path):
        try:
            with urllib.request.urlopen(RAW + remote, timeout=60) as r:
                data = r.read()
            with open(path, "wb") as f:
                f.write(data)
        except Exception as e:  # noqa: BLE001
            print(f"[warn] could not fetch {remote}: {e}", file=sys.stderr)
            return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_dhatus(refresh=False):
    """dhatu/data.txt -> {baseindex|i: row}. Fail loudly on schema drift."""
    raw = fetch(CORE, refresh)
    if raw is None:
        return {}
    rows = json.loads(raw).get("data", [])
    if not rows or "artha_english" not in rows[0] or "baseindex" not in rows[0]:
        print("[fail] dhatu/data.txt schema changed upstream "
              "(artha_english/baseindex missing) — H7815 fail route.", file=sys.stderr)
        return {}
    idx = {}
    for row in rows:
        idx[str(row.get("baseindex", ""))] = row
        idx[str(row.get("i", ""))] = row
    return idx


def load_prayogas(refresh=False):
    """dhatuprayogas.txt -> {baseindex: {prayoga: [{book,num,text}, ...]}}."""
    raw = fetch(PRAYOGA, refresh)
    if raw is None:
        return {}
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"[warn] dhatuprayogas.txt is not JSON as expected: {e}", file=sys.stderr)
        return {}


def render(row, want_prayoga, want_devanagari, refresh, prayoga_limit=5):
    base, rid = row["baseindex"], str(row["i"])
    iast = deva_to_iast(row.get("dhatu", ""))
    gana = int(row.get("gana") or 0)
    pada = row.get("pada", "-")
    gana_s = f"{gana} ({GANAS.get(gana, '?')})" if gana else "—"
    pada_s = f"{pada} ({PADAS.get(pada, pada)})" if pada in PADAS else pada
    print(f"## Dhātupāṭha {base}")
    print()
    if want_devanagari:
        print(f"- **дхату (деванагари):** {row.get('dhatu', '')}")
    print(f"- **дхату (IAST):** {iast}")
    print(f"- **artha (англ.):** {row.get('artha_english', '') or '—'}")
    print(f"- **gaṇa/pada:** {gana_s} / {pada_s}")
    print(f"- **цитата для текста:** `ср. Dhātupāṭha {base} ({iast})`")
    print(f"- **URL:** https://ashtadhyayi.com/dhatu/{rid}")
    if want_prayoga:
        pr = load_prayogas(refresh).get(base, {})
        shown = 0
        for pname, atts in pr.items():
            for a in atts:
                if shown >= prayoga_limit:
                    return
                if shown == 0:
                    print()
                    print("### Prayoga (употребления)")
                print(f"- **{pname}** — {a.get('book', '')} {a.get('num', '')}: "
                      f"{a.get('text', '')}")
                shown += 1
    print()


def matches(row, q):
    """Substring hit across Devanagari, IAST and English fields."""
    fields = [
        str(row.get("dhatu", "")), str(row.get("aupadeshik", "")),
        str(row.get("artha", "")), str(row.get("searchterms", "")),
        deva_to_iast(str(row.get("dhatu", ""))), deva_to_iast(str(row.get("artha", ""))),
        str(row.get("artha_english", "")), str(row.get("tags", "")),
    ]
    return any(q in f or q in f.lower() for f in fields if f)


def resolve_ref(ref, dhatus):
    """baseindex / numeric id / root text -> list of rows (root text may be homonymous)."""
    ref = ref.strip()
    if ref.isdigit() and ref in dhatus:            # numeric id, e.g. 1010001
        return [dhatus[ref]]
    if "." in ref and ref.replace(".", "").isdigit():
        gana, _, sutra = ref.partition(".")        # 01.0001 / 1.1 -> 01.0001
        key = f"{int(gana):02d}.{int(sutra):04d}"
        return [dhatus[key]] if key in dhatus else []
    return [r for r in dhatus.values()             # root text (deva or IAST)
            if r.get("dhatu") == ref or deva_to_iast(r.get("dhatu", "")) == ref]


def main():
    ap = argparse.ArgumentParser(description="Resolve Dhātupāṭha roots.")
    ap.add_argument("ref", nargs="?",
                    help="baseindex (01.0001), numeric id (1010001) or root (bhū / भू)")
    ap.add_argument("--search", help="keyword (Devanagari / IAST / English)")
    ap.add_argument("--prayoga", action="store_true",
                    help="also print usage attestations (dhatuprayogas.txt)")
    ap.add_argument("--devanagari", action="store_true",
                    help="also print the Devanagari line (off by default, MG 07-11-2026)")
    ap.add_argument("--refresh", action="store_true", help="re-download cache")
    ap.add_argument("--limit", type=int, default=10, help="max search hits")
    args = ap.parse_args()

    dhatus = load_dhatus(args.refresh)
    if not dhatus:
        print("No dhātu data — check network / cache.", file=sys.stderr)
        sys.exit(1)

    if args.ref:
        # de-dup (baseindex and i keys point at the same row)
        seen, uniq = set(), []
        for r in resolve_ref(args.ref, dhatus):
            if r["i"] not in seen:
                seen.add(r["i"]); uniq.append(r)
        if not uniq:
            print(f"Дхату «{args.ref}» не найдена.", file=sys.stderr)
            sys.exit(3)
        if len(uniq) > 1:
            print(f"_{len(uniq)} дхату с формой «{args.ref}» "
                  f"(показаны первые {min(args.limit, len(uniq))}):_\n")
        for r in uniq[:args.limit]:
            render(r, args.prayoga, args.devanagari, args.refresh)
    elif args.search:
        q = args.search.strip()
        hits = [r for r in dhatus.values() if matches(r, q)]
        uniq, seen = [], set()
        for r in hits:
            if r["i"] not in seen:
                seen.add(r["i"]); uniq.append(r)
        if not uniq:
            print(f"Ничего не найдено по «{args.search}».")
            return
        print(f"_{len(uniq)} совпадений по «{args.search}» "
              f"(показаны первые {min(args.limit, len(uniq))}):_\n")
        for r in uniq[:args.limit]:
            render(r, args.prayoga, args.devanagari, args.refresh)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
