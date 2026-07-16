#!/usr/bin/env python
"""root_shape_parser.py — the root-shape parser for §59 (OCH-16).

§59 claims the structure of «подавляющее большинство» Sanskrit roots fits a
six-slot template:

    1: s | 2: шумная | 3: сонант | 4: чередующийся элемент (§50) | 5: сонант | 6: шумная

with only slot 4 obligatory. OCH-16 refused a naive regex («would misparse
exactly the interesting cases — not computed rather than miscomputed»); this
parser implements ZALIZNIAK'S OWN §59 rulings, all quoted from mdx line 822:

  - slot 1 is a dedicated initial 's' (sthā = s|th|ā; styā = s|t|y|ā);
  - «сочетание kṣ ведет себя как одиночная согласная» (kṣṇu, takṣ);
  - «изредка на месте 2 стоит v или m» (vyath, mlā) — granted extension;
  - «изредка ... на месте 6 — сочетание шумных согласных» (katth) — granted
    extension;
  - two internal CONSTRAINTS he states (checked as a separate census, since
    they restrict the language, not the template): the slot-3 sonant never
    equals the sonant inside slot 4; slots 2 and 6 are never both aspirated
    (h behaves as an aspirate).

INPUT = the author-catalog the claim's `sources: [talmud]` points at:
TolchelnikovTalmud_2026/data/talmud_appendix1.json (745 roots), parsed via
each root's `whitney_spellings` (IAST) with the ALTERNATING ELEMENT anchored
by the root's own `ryad` series letter (A/I/U/R/L/M/N per §§50/60) — the
series tells the parser WHAT the element is, so the split is Zalizniak-
faithful, not phonologically re-derived. A root FITS if any (spelling,
element-occurrence) split validates against the slot grammar; misfits are
inventoried with reasons, never silently dropped.

Usage:  python ZalizniakOcherk_1978/root_shape_parser.py
Writes  och16_root_shape_stats.json next to this script.
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
CATALOG = HERE.parent / "TolchelnikovTalmud_2026" / "data" / "talmud_appendix1.json"

# IAST segment inventory (multigraphs first for tokenization)
MULTI = ["kṣ", "kh", "gh", "ch", "jh", "ṭh", "ḍh", "th", "dh", "ph", "bh"]
OBSTRUENTS = {"k", "kh", "g", "gh", "c", "ch", "j", "jh", "ṭ", "ṭh", "ḍ", "ḍh",
              "t", "th", "d", "dh", "p", "ph", "b", "bh", "ś", "ṣ", "s", "h", "kṣ"}
ASPIRATES = {"kh", "gh", "ch", "jh", "ṭh", "ḍh", "th", "dh", "ph", "bh", "h"}
SONANTS = {"y", "r", "l", "v", "m", "n", "ṇ", "ṅ", "ñ", "ṃ"}

# citation-form realizations of the alternating element, by series letter
# (longest first per series; weak/nasalized citation variants included so
# defective-citation roots still anchor)
ELEMENT_PATTERNS = {
    # full three-grade citation realizations per §50 series (vṛddhi grades and
    # the I-series ai-class — gā/gai, kṣmai — included; longest tried first)
    "A": ["ā", "a"],
    "I": ["āy", "ay", "ai", "ī", "i", "e", "ā"],
    "U": ["āv", "av", "au", "ū", "u", "o"],
    "R": ["ār", "ar", "rā", "ra", "ṝ", "ṛ", "ir", "ur", "īr", "ūr"],
    "L": ["āl", "al", "ḹ", "ḷ"],
    "M": ["ām", "am", "ṛṃ", "ṛm", "ā", "a"],
    "N": ["ān", "an", "ṛṇ", "ṛn", "ṛṃ", "ā", "a"],
}
# sonant "inside" the element (for the slot-3 constraint census)
ELEMENT_SONANT = {"ar": "r", "al": "l", "am": "m", "an": "n", "ām": "m", "ān": "n",
                  "ār": "r", "āl": "l", "ir": "r", "ur": "r", "īr": "r", "ūr": "r",
                  "ṛṃ": "m", "ṛm": "m", "ṛṇ": "n", "ṛn": "n",
                  "ay": "y", "āy": "y", "av": "v", "āv": "v"}


def tokenize(s):
    out, i = [], 0
    while i < len(s):
        for m in MULTI:
            if s.startswith(m, i):
                out.append(m)
                i += len(m)
                break
        else:
            out.append(s[i])
            i += 1
    return out


def valid_prefix(segs):
    """slots 1-3: [s]? [obstruent|v|m]? [sonant]? — returns (ok, used_slots)."""
    used = {}
    i = 0
    if i < len(segs) and segs[i] == "s" and len(segs) > 1:
        # initial s occupies slot 1 only if something follows it in the prefix
        # (a bare s- onset like 'sad' is slot 2)
        if len(segs) - i >= 2:
            used["s1"] = True
            i += 1
    if i < len(segs) and (segs[i] in OBSTRUENTS or segs[i] in {"v", "m"}):
        used["c2"] = segs[i]
        used["c2_vm"] = segs[i] in {"v", "m"}
        i += 1
    if i < len(segs) and segs[i] in SONANTS:
        used["son3"] = segs[i]
        i += 1
    return (i == len(segs)), used


def valid_suffix(segs):
    """slots 5-6: [sonant]? [obstruent]{0,2} (cluster = granted-rare)."""
    used = {}
    i = 0
    if i < len(segs) and segs[i] in SONANTS:
        used["son5"] = segs[i]
        i += 1
    obst = []
    while i < len(segs) and segs[i] in OBSTRUENTS and len(obst) < 2:
        obst.append(segs[i])
        i += 1
    if obst:
        used["c6"] = obst
        used["c6_cluster"] = len(obst) > 1
    return (i == len(segs)), used


def parse_root(spelling, series):
    """Try every element occurrence; return (fits, best_split_info, reasons)."""
    s = spelling.replace("ç", "ś")
    reasons = []
    for pat in ELEMENT_PATTERNS.get(series, []):
        start = 0
        while True:
            j = s.find(pat, start)
            if j < 0:
                break
            pre, suf = s[:j], s[j + len(pat):]
            okp, up = valid_prefix(tokenize(pre)) if pre else (True, {})
            oks, us = valid_suffix(tokenize(suf)) if suf else (True, {})
            if okp and oks:
                info = {"element": pat, **up, **us}
                # constraint census (language restrictions, not template fit)
                viol = []
                es = ELEMENT_SONANT.get(pat)
                if es and up.get("son3") == es:
                    viol.append("slot3-sonant-equals-element-sonant")
                if up.get("c2") in ASPIRATES and us.get("c6") and us["c6"][-1] in ASPIRATES:
                    viol.append("slots-2-and-6-both-aspirated")
                return True, info, viol
            reasons.append(f"{pat}@{j}: pre={pre or '∅'} {'ok' if okp else 'BAD'}, "
                           f"suf={suf or '∅'} {'ok' if oks else 'BAD'}")
            start = j + 1
    return False, None, reasons


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    roots = data["roots"]

    fits, misfits, no_series = [], [], []
    ext = Counter()
    viol_census = Counter()
    for r in roots:
        series = (r.get("ryad") or "")[:1]
        # whitney spellings first; the catalog's own citation as fallback — some
        # rows (śikṣ, ryad I₁) list the BASE root (śak) in whitney_spellings
        # while the entry's series describes the catalog citation itself
        spellings = list(r.get("whitney_spellings") or [])
        own = r.get("root", "")
        if own and "ø" not in own and own not in spellings:
            spellings.append(own)
        if not spellings:
            spellings = [own]
        if series not in ELEMENT_PATTERNS:
            no_series.append(r.get("root"))
            continue
        for sp in spellings:
            ok, info, viol = parse_root(sp, series)
            if ok:
                fits.append({"root": sp, "series": series, **info})
                if info.get("s1"):
                    ext["slot1_s"] += 1
                if info.get("c2_vm"):
                    ext["slot2_v_or_m"] += 1
                if info.get("c6_cluster"):
                    ext["slot6_obstruent_cluster"] += 1
                for v in viol:
                    viol_census[v] += 1
                break
        else:
            misfits.append({"root": spellings[0], "series": series,
                            "ryad": r.get("ryad")})

    classified = len(fits) + len(misfits)
    share = round(100 * len(fits) / classified, 2) if classified else None

    # §59's own example roots must parse (series per the catalog where present,
    # else the §'s obvious series)
    EXAMPLES = [("i", "I"), ("nī", "I"), ("śru", "U"), ("sthā", "A"), ("styā", "A"),
                ("iṣ", "I"), ("pad", "A"), ("krudh", "U"), ("jīv", "I"), ("cumb", "U"),
                ("kṣṇu", "U"), ("takṣ", "A"), ("vyath", "A"), ("mlā", "A"), ("katth", "A")]
    example_results = {sp: parse_root(sp, ser)[0] for sp, ser in EXAMPLES}

    checks = {
        "catalog_roots": len(roots),
        "classified": classified,
        "unclassifiable_no_series": len(no_series),
        "all_s59_examples_parse": all(example_results.values()),
        "share_over_90pct": (share or 0) > 90,
    }

    out = {
        "instrument": "root_shape_parser.py over talmud_appendix1.json (745 roots); "
                      "§59 six-slot template with Zalizniak's own rulings (initial-s slot, "
                      "kṣ=single, v/m in slot 2, rare final obstruent cluster); element "
                      "anchored by each root's catalog ryad series",
        "template_fit_share_pct": share,
        "fits": len(fits),
        "misfits": len(misfits),
        "misfit_inventory": misfits,
        "granted_extension_usage": dict(ext),
        "constraint_violations (language census, not fit)": dict(viol_census),
        "slot_occupancy": {
            "slot1_s": ext["slot1_s"],
            "slot2": sum(1 for f in fits if f.get("c2")),
            "slot3": sum(1 for f in fits if f.get("son3")),
            "slot5": sum(1 for f in fits if f.get("son5")),
            "slot6": sum(1 for f in fits if f.get("c6")),
        },
        "s59_example_roots": example_results,
        "validation": checks,
    }
    (HERE / "och16_root_shape_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"classified {classified}/{len(roots)} (no-series: {len(no_series)})")
    print(f"TEMPLATE FIT: {len(fits)} = {share}%  |  misfits: {len(misfits)}")
    print("extension usage:", dict(ext))
    print("constraint violations:", dict(viol_census) or "none")
    print("misfit sample:", [m["root"] for m in misfits[:15]])
    print("§59 examples all parse:", checks["all_s59_examples_parse"])
    bad = [k for k, v in checks.items() if v is False]
    print("validation:", "OK" if not bad else f"FAILED: {bad}")
    print("-> och16_root_shape_stats.json written")


if __name__ == "__main__":
    main()
