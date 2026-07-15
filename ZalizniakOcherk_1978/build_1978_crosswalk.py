#!/usr/bin/env python
"""build_1978_crosswalk.py — the 1978 column of the morphoclass crosswalk (H797 follow-up).

Adds Zaliznyak-1978 (Ocherk) attributes per root — ряд чередования (series+index),
открытость (open/closed) and полноизменяемость (fully-alternating vs defective) — to the
per-root crosswalk that so far carried only 1975/2014/2026 taxonomies
(TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv). This is the
instrument OCH-21..OCH-23 named as their blocker: the naive series join recorded in OCH-23
equated 2026 ryad with 1978 series and skipped the полноизменяемость filter, inverting §68.

FAITHFUL-TO-TEXT DESIGN (same contract as the Morphology-1975 classifier): the attributes are
computed from Zaliznyak's OWN §§60-68 — his deterministic surface rules (§66 series-from-
citation-form, §67 изменяемость rules) plus his explicit named-root lists, which OVERRIDE the
rules and the 2014 z_series where they speak. No independent phonological re-derivation.

Two print-corruption suspects found in the source while encoding (recorded here, errata-class):
  §66 lists open-M₁ «√mam наклоняться» — no such root; clearly √nam 'bow' (encoded as nam);
  §67's rule-1 header reads «оканчивающиеся на a(ā), u(ū)» yet its own examples are ji, nī,
  çru, bhū (i/ī/u/ū) and §67 itself splits open A₂ roots ~50/50 two paragraphs later — the
  header must read «на i(ī), u(ū)» (encoded accordingly).

Usage:  python ZalizniakOcherk_1978/build_1978_crosswalk.py
Writes  crosswalk_1978.csv + och_1978_stats.json next to this script.
"""
import csv, io, json, sys, unicodedata
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
BASE = REPO / "TolchelnikovTalmud_2026" / "data" / "morphoclass_crosswalk_1975_2014_2026.csv"

VOWELS = "aāiīuūṛṝeo"          # + ai/au via endswith
LONG_NUCLEUS = set("āīūṝ") | {"e", "o", "ai", "au"}
SONANTS = set("rlmn")

# --- §66 explicit index lists for open R/M/N roots (citation forms as in the crosswalk) ---
R2_OPEN = {"kṝ", "gṝ", "jṝ", "tṝ", "pṝ", "mṝ", "śṝ"}                     # §66 п.2 (kar kṝ …)
M1_OPEN = {"gam", "yam", "nam", "ram"}                                    # §66 п.3 («mam» = nam)
N1_OPEN = {"han", "man", "kṣan", "tan"}                                   # tan «с колебаниями к N₂»
N2_OPEN = {"jan", "khan", "san"}
M2_OPEN = {"kram", "dam", "bhram", "śram"}                                # «корней ряда M₂ больше»

# --- §67 named полноизменяемость lists ---
A1_FULL = {"as", "vac", "vad", "vas", "yaj", "svap", "grah", "gṛh", "prach", "vyadh"}
A1_FULL_EXCL = {("vas", "2"), ("vadh", None)}   # vas 'dress' and vadh stay defective
A2_FULL = {"sthā", "dā", "dhā", "mā", "gā", "pā", "hā", "jyā", "vyā", "śyā", "hvā", "śvā"}
A2_DEFECTIVE = {"khyā", "glā", "ghrā", "jñā", "trā", "dhmā", "dhyā", "pyā", "bhā", "yā", "vā", "snā"}
RMN_DEFECTIVE = {"kṣar", "tvar", "garh", "garj", "an", "stan", "kamp", "nand", "lamb", "vand"}
HEAVY_FULL_EXC = {"śās", "sīv", "siv"}                                    # §67 exceptions
L_FULL = {"kalp", "kḷp"}                                                  # §67: L defective except kalp
SPECIAL = {"mṛj": "special-vrddhi (§67 прим.)"}


def nfc(s):
    return unicodedata.normalize("NFC", s or "")


def nucleus_and_coda(root):
    """Return (nucleus, coda_len, pre) for the LAST vowel group of the citation form."""
    r = nfc(root)
    # find last vowel (incl. digraphs ai/au treated via single chars a+i? IAST uses ai/au as a+i chars;
    # in NFC 'ai' is two chars — detect digraph)
    idx = max((r.rfind(v) for v in VOWELS), default=-1)
    if idx < 0:
        return None, 0, r
    nuc = r[idx]
    if nuc in "ae" and idx + 1 < len(r) and r[idx + 1] in "iu":  # ai/au (rare in roots)
        nuc = r[idx:idx + 2]
        coda = r[idx + 2:]
    else:
        coda = r[idx + 1:]
    return nuc, coda, r[:idx]


def series_1978(root, z_series):
    """§66: series + index from the citation form; explicit lists override; z fills gaps."""
    r = nfc(root)
    nuc, coda, _ = nucleus_and_coda(r)
    if nuc is None:
        return None, "unparsed"
    # explicit open-root lists first
    if r in R2_OPEN:
        return "R₂", "§66-list"
    if r in M1_OPEN:
        return "M₁", "§66-list"
    if r in N1_OPEN:
        return "N₁", "§66-list"
    if r in N2_OPEN:
        return "N₂", "§66-list"
    if r in M2_OPEN:
        return "M₂", "§66-list"
    # citation-vowel rules
    if coda == "" or (len(coda) >= 1 and coda[0] in SONANTS):
        pass  # handled below by nucleus/sonant logic
    if nuc == "i":
        return "I₁", "§66-rule"
    if nuc == "ī":
        return "I₂", "§66-rule"
    if nuc == "u":
        return "U₁", "§66-rule"
    if nuc == "ū":
        return "U₂", "§66-rule"
    if nuc == "ṛ":
        return "R₁", "§66-rule"
    if nuc == "ṝ":
        return "R₂", "§66-rule"
    if nuc in ("a", "ā") and coda and coda[0] in SONANTS:
        S = {"r": "R", "l": "L", "m": "M", "n": "N"}[coda[0]]
        if len(coda) > 1:                       # closed R/M/N → index 1 (§66 п.1)
            return (S + "₁") if S != "L" else "L", "§66-rule-closed"
        # open -am/-an not in the lists: M₂ majority per §66; N unknown → z fallback
        if S == "M":
            return "M₂", "§66-default-open-M"
        z = (z_series or "").replace("1", "₁").replace("2", "₂").replace("0", "")
        if z.startswith(S) and len(z) > 1:
            return z, "z-series"
        return S + "?", "index-unknown"
    if nuc == "a":
        return "A₁", "§66-rule"
    if nuc == "ā":
        return "A₂", "§66-rule"
    if nuc in ("e", "o", "ai", "au"):
        return "A₂", "§66-special(e/o/ai/au→ā-line, §70)"
    return None, "unparsed"


def openness(root, series):
    r = nfc(root)
    nuc, coda, _ = nucleus_and_coda(r)
    if nuc is None:
        return None
    if coda == "":
        return "open"
    if coda[0] in SONANTS and len(coda) == 1 and (series or "").rstrip("₁₂?") in ("R", "L", "M", "N"):
        return "open"                            # gam, han, san, kar-type: sonant is the element's tail
    return "closed"


def polnoizm(root, series, opn, homonym):
    """§67 — returns (значение, basis)."""
    r = nfc(root)
    S = (series or "").rstrip("₁₂?")
    nuc, coda, _ = nucleus_and_coda(r)
    if nuc is None:
        return "unknown", "unparsed-citation-form"
    if r in SPECIAL:
        return "full", SPECIAL[r]
    if r in HEAVY_FULL_EXC:
        return "full", "§67-exception-list"
    if S == "A" and series == "A₁":
        if (r, homonym or None) in A1_FULL_EXCL or (r == "vas" and (homonym or "") == "2"):
            return "defective", "§67-A1-named-exclusion"
        return ("full", "§67-A1-list") if r in A1_FULL else ("defective", "§67-A1-default")
    if series == "A₂" and opn == "open":
        if r in A2_FULL:
            return "full", "§67-A2-list"
        if r in A2_DEFECTIVE:
            return "defective", "§67-A2-list"
        return "fluctuating", "§67-A2-unlisted (ряд корней колеблется)"
    if opn == "open" and nuc in "iīuū":
        return "full", "§67-rule-1 (open i/ī/u/ū)"
    if opn == "open" and S in ("R", "M", "N"):
        return ("defective", "§67-RMN-list") if r in RMN_DEFECTIVE else ("full", "§67-RMN-default(majority)")
    if opn == "open" and S == "L":
        return ("full", "§67-L-exception") if r in L_FULL else ("defective", "§67-L-default")
    # closed roots
    heavy = (nuc in LONG_NUCLEUS) or (nuc in "iuṛ" and coda and len(coda) >= 2)
    if heavy:
        return "defective", "§67-rule-2 (heavy closed)"
    if nuc in "iu" and coda and len(coda) == 1:
        return "full", "§67-rule-1 (closed short i/u + C)"
    if S in ("R", "M", "N"):
        return ("defective", "§67-RMN-list") if r in RMN_DEFECTIVE else ("full", "§67-RMN-default(majority)")
    if S == "L":
        return ("full", "§67-L-exception") if r in L_FULL else ("defective", "§67-L-default")
    if series == "A₁":
        return ("full", "§67-A1-list") if r in A1_FULL else ("defective", "§67-A1-default")
    return "unknown", "no-§67-rule"


def main():
    rows, seen = [], set()
    for r in csv.DictReader(io.open(BASE, encoding="utf-8")):
        key = (r["whitney_no"], nfc(r["root"]), r.get("homonym") or "")
        if key in seen:
            continue
        seen.add(key)
        rows.append(r)

    out_rows = []
    for r in rows:
        root = nfc(r["root"])
        ser, ser_basis = series_1978(root, r.get("z_series"))
        opn = openness(root, ser)
        pz, pz_basis = polnoizm(root, ser, opn, r.get("homonym"))
        out_rows.append({
            "whitney_no": r["whitney_no"], "root": root, "homonym": r.get("homonym") or "",
            "gloss": r.get("gloss") or "", "ryad_1978": ser or "", "ryad_1978_basis": ser_basis,
            "openness_1978": opn or "", "polnoizm_1978": pz, "polnoizm_1978_basis": pz_basis,
            "z_set": r.get("z_set") or "", "ryad_2026": r.get("ryad_derived") or "",
            "z_series_2014": r.get("z_series") or "",
        })

    with io.open(HERE / "crosswalk_1978.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        w.writeheader()
        w.writerows(out_rows)

    # --- validation against §§66-68's own named roots ---
    ix = {(o["root"], o["homonym"]): o for o in out_rows}
    def get(root):
        for (rr, h), o in ix.items():
            if rr == root:
                return o
        return None
    checks = [
        ("gam", {"ryad_1978": "M₁", "openness_1978": "open", "polnoizm_1978": "full"}),
        ("han", {"ryad_1978": "N₁", "openness_1978": "open", "polnoizm_1978": "full"}),
        ("jan", {"ryad_1978": "N₂", "openness_1978": "open"}),
        ("kram", {"ryad_1978": "M₂", "openness_1978": "open"}),
        ("bhū", {"ryad_1978": "U₂", "openness_1978": "open", "polnoizm_1978": "full"}),
        ("ji", {"ryad_1978": "I₁", "openness_1978": "open", "polnoizm_1978": "full"}),
        ("chid", {"ryad_1978": "I₁", "openness_1978": "closed", "polnoizm_1978": "full"}),
        ("jīv", {"polnoizm_1978": "defective"}),
        ("cumb", {"polnoizm_1978": "defective"}),
        ("tap", {"ryad_1978": "A₁", "polnoizm_1978": "defective"}),
        ("sthā", {"ryad_1978": "A₂", "polnoizm_1978": "full"}),
        ("jñā", {"ryad_1978": "A₂", "polnoizm_1978": "defective"}),
        ("kṣar", {"polnoizm_1978": "defective"}),
        ("śās", {"polnoizm_1978": "full"}),
        ("mṛj", {"polnoizm_1978": "full"}),
    ]
    fails = []
    for root, want in checks:
        o = get(root)
        if not o:
            fails.append(f"{root}: NOT IN CROSSWALK")
            continue
        for k, v in want.items():
            if o[k] != v:
                fails.append(f"{root}: {k}={o[k]!r}, want {v!r}")
    print(f"validation: {len(checks) - len([f for f in fails])} checks", "OK" if not fails else "")
    for f in fails:
        print("  FAIL", f)

    # --- OCH-23 / §68: the PROPER join ---
    A_SERIES = {"I₁", "U₁", "R₁", "M₁", "N₁", "I₂"}
    ga, gb = Counter(), Counter()
    for o in out_rows:
        if o["openness_1978"] != "open" or not o["z_set"]:
            continue
        if o["ryad_1978"] in ("A₁", "A₂"):
            continue                                   # §63 note: A₂ outside the opposition
        if o["ryad_1978"] in A_SERIES and o["polnoizm_1978"] == "full":
            ga[o["z_set"]] += 1
        else:
            gb[o["z_set"]] += 1

    def pct(c, k):
        tot = sum(c.values())
        return round(100 * c[k] / tot, 1) if tot else None

    stats = {
        "_source": "crosswalk_1978.csv (this script) x z_set (2014 Zaliznyak DB via the base crosswalk)",
        "OCH23_s68_proper_join": {
            "groupA_full_I1_U1_R1_M1_N1_I2": dict(ga),
            "groupA_anit_pct": pct(ga, "aniṭ"), "groupA_anit_plus_vet_pct":
                round(100 * (ga["aniṭ"] + ga["veṭ"]) / sum(ga.values()), 1) if ga else None,
            "groupB_other_open_non_A": dict(gb),
            "groupB_set_pct": pct(gb, "seṭ"), "groupB_set_plus_vet_pct":
                round(100 * (gb["seṭ"] + gb["veṭ"]) / sum(gb.values()), 1) if gb else None,
        },
    }

    # --- OCH-21: open A₂ split ---
    a2 = Counter(o["polnoizm_1978"] for o in out_rows
                 if o["ryad_1978"] == "A₂" and o["openness_1978"] == "open")
    stats["OCH21_openA2_split"] = dict(a2)

    # --- OCH-22: R/M/N roots, полноизменяемость (type counts; token weights via DCS lemmas) ---
    rmn = [o for o in out_rows if (o["ryad_1978"] or "").rstrip("₁₂?") in ("R", "M", "N")]
    stats["OCH22_RMN_type_counts"] = dict(Counter(o["polnoizm_1978"] for o in rmn))
    lemma_file = REPO.parent / "VisualDCS" / "dcs_lemma_summary.json"
    if lemma_file.exists():
        try:
            lem = json.load(io.open(lemma_file, encoding="utf-8"))
            def tok(root):
                v = lem.get(root)
                if isinstance(v, dict):
                    return v.get("total") or v.get("count") or 0
                return v if isinstance(v, (int, float)) else 0
            wt = Counter()
            for o in rmn:
                wt[o["polnoizm_1978"]] += tok(o["root"])
            if sum(wt.values()):
                stats["OCH22_RMN_token_weighted"] = dict(wt)
        except Exception as e:
            stats["OCH22_note"] = f"lemma join skipped: {e}"

    io.open(HERE / "och_1978_stats.json", "w", encoding="utf-8").write(
        json.dumps(stats, ensure_ascii=False, indent=2))
    print(json.dumps(stats, ensure_ascii=False, indent=2)[:2200])
    print(f"-> wrote crosswalk_1978.csv ({len(out_rows)} roots) + och_1978_stats.json")


if __name__ == "__main__":
    main()
