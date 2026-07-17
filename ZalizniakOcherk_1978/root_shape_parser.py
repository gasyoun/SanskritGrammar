#!/usr/bin/env python
"""root_shape_parser.py — the root-shape parser for §59 (OCH-16).

§59 claims the overwhelming majority of Sanskrit roots fit a six-position
template:

    1        2                3       4                          5       6
    (s)  (obstruent)     (sonant)  ALTERNATING ELEMENT (§50)  (sonant)  (obstruent)

Only position 4 is mandatory; the rest may be empty (1 and 5 predominantly
so). §59 itself names the tricky edge cases a naive regex would misparse:
kṣ behaves as ONE consonant (√kṣṇu, √takṣ); v or m rarely fill position 2
(√vyath, √mlā); position 6 may be an obstruent CLUSTER (√katth); position 1
is only ever 's' before a further obstruent (√sthā, √styā).

DESIGN: this is a phonological onset-nucleus-coda parse over each catalog
root's own citation spelling, using the Talmud Приложение-1 catalog's own
`ryad` (ablaut-series) tag to know exactly which vowel/vowel+resonant
strings can realize position 4 for THAT root (weak/guṇa/vṛddhi per §50's
table) — not a guess. Whatever flanks that nucleus match is tokenized into
consonant UNITS (aspirate digraphs and kṣ count as one unit each, per §59)
and classified sonant vs obstruent (y/v/r/l/m/n/ṅ/ñ/ṇ vs the stops,
sibilants and h), then tested against the six slots. Citation grade
(weak/guṇa/vṛddhi) doesn't change the verdict: the three ablaut grades of
a series differ only in the vowel content of slot 4 itself, never in the
surrounding consonant skeleton, so parsing whichever grade a root happens
to be cited in is safe.

Primary spelling comes from the catalog's own `whitney_spellings` (plain
IAST, no Talmud-internal notation); the catalog's `root` field is a
fallback only for the 5 entries absent from Whitney (its ø/ø̄ marks — a
documented Talmud-manual convention, "нуль звука, слабая ступень ряда
А1/А2", legend in Talmud-2.1.6.mdx — are not used elsewhere here).

Usage:  python ZalizniakOcherk_1978/root_shape_parser.py
Writes  och16_root_shape_stats.json next to this script.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CATALOG = REPO / "TolchelnikovTalmud_2026" / "data" / "talmud_appendix1.json"

# §50's table of three-grade realizations, restricted to what a citation form
# can show (weak | guṇa | vṛddhi); bare (un-indexed) series get the union of
# their subseries since guṇa/vṛddhi never differ by subindex. I/U series also
# get their §54 before-vowel allomorphs (e→ay, ai→āy, o→av, au→āv) — some
# catalog citations show the pre-vocalic form (e.g. dhāv, not dhau). R₂ gets
# both weak-grade notations §53's note allows (plain ṛ and the Indian-
# tradition-specific ṝ).
RYAD_NUCLEI = {
    "A₁": ["a", "ā"],
    "A₂": ["i", "ī", "ā"],
    "I₁": ["i", "e", "ai", "ay", "āy"],
    "I₂": ["ī", "e", "ai", "ay", "āy"],
    "I": ["i", "ī", "e", "ai", "ay", "āy"],
    "U₁": ["u", "o", "au", "av", "āv"],
    "U₂": ["ū", "o", "au", "av", "āv"],
    "U": ["u", "ū", "o", "au", "av", "āv"],
    "R₁": ["ṛ", "ar", "ār"],
    "R₂": ["ṛ", "ṝ", "īr", "ūr", "ar", "ār"],
    "R": ["ṛ", "ṝ", "īr", "ūr", "ar", "ār"],
    "L": ["ḷ", "al", "āl"],
    "M₁": ["a", "am", "ām"],
    "M₂": ["am", "ām"],
    "M": ["a", "am", "ām"],
    "N₁": ["a", "an", "ān"],
    "N₂": ["ā", "an", "ān"],
    "N": ["a", "ā", "an", "ān"],
}
VOWELS = set("aāiīuūṛṝḷ") | {"e", "o", "ai", "au"}  # for the stray-extra-vowel guard

SONANTS = set("yvrlmnṇñṅṃ")  # ṃ (anusvara) is surface nasal+sibilant sandhi, underlyingly n/m
ASPIRATES = {"kh", "gh", "ch", "jh", "ṭh", "ḍh", "th", "dh", "ph", "bh"}
OBSTRUENT_SIMPLE = set("kgcjṭḍtdpbśṣshç")  # ç = Zaliznyak's own §59 spelling of ś
KS_DIGRAPH = "kṣ"  # §59's named exception: behaves as a single consonant


def classify(unit):
    if unit == KS_DIGRAPH or unit in ASPIRATES or unit in OBSTRUENT_SIMPLE:
        return "obstruent"
    if unit in SONANTS:
        return "sonant"
    return "unknown"


def tokenize_consonants(s):
    """Split a consonant-only run into phonemic units (kṣ and aspirate
    digraphs count as one unit each, per §59)."""
    units = []
    i = 0
    while i < len(s):
        two = s[i:i + 2]
        if two == KS_DIGRAPH or two in ASPIRATES:
            units.append(two)
            i += 2
        else:
            units.append(s[i])
            i += 1
    return units


def find_nucleus(spelling, ryad):
    """Locate §50's alternating element for this root's own ryad tag.
    Returns (start, end, matched_string) or None if no candidate matches."""
    candidates = RYAD_NUCLEI.get(ryad)
    if candidates is None:
        return None
    for cand in sorted(set(candidates), key=len, reverse=True):
        idx = spelling.find(cand)
        if idx != -1:
            return idx, idx + len(cand), cand
    return None


def fit_prefix(units):
    """Slots 1(s)/2(obstruent)/3(sonant), left to right, at most 3 units."""
    n = len(units)
    if n == 0:
        return {}
    if n == 1:
        k = classify(units[0])
        if k == "sonant":
            return {"3": units[0]}
        if k == "obstruent":
            return {"2": units[0]}
        return None
    if n == 2:
        c1, c2 = units
        k1, k2 = classify(c1), classify(c2)
        if k1 == "obstruent" and k2 == "sonant":
            return {"2": c1, "3": c2}
        if c1 == "s" and k2 == "obstruent":
            return {"1": c1, "2": c2}
        if c1 in ("v", "m") and k2 == "sonant":  # §59's named rare exception
            return {"2": c1, "3": c2, "irregular_slot2": c1}
        return None
    if n == 3:
        c1, c2, c3 = units
        if c1 == "s" and classify(c2) == "obstruent" and classify(c3) == "sonant":
            return {"1": c1, "2": c2, "3": c3}
        return None
    return None


def fit_suffix(units):
    """Slot 5(sonant, at most one, nucleus-adjacent) then slot 6(obstruent,
    possibly a cluster, per §59's √katth example)."""
    n = len(units)
    if n == 0:
        return {}
    first = units[0]
    if classify(first) == "sonant":
        rest = units[1:]
        if any(classify(c) != "obstruent" for c in rest):
            return None
        out = {"5": first}
        if rest:
            out["6"] = "".join(rest)
        return out
    if all(classify(c) == "obstruent" for c in units):
        return {"6": "".join(units)}
    return None


def classify_root(spelling, ryad):
    """Returns a dict verdict for one citation spelling under its ryad tag."""
    hit = find_nucleus(spelling, ryad)
    if hit is None:
        return {"outcome": "no_nucleus_found"}
    start, end, nucleus = hit
    pre, suf = spelling[:start], spelling[end:]
    if any(v in pre for v in VOWELS) or any(v in suf for v in VOWELS):
        return {"outcome": "extra_vowel", "nucleus": nucleus}
    pre_slots = fit_prefix(tokenize_consonants(pre)) if pre else {}
    suf_slots = fit_suffix(tokenize_consonants(suf)) if suf else {}
    if pre_slots is None or suf_slots is None:
        return {"outcome": "no_fit", "nucleus": nucleus, "prefix": pre, "suffix": suf}
    slots = {**pre_slots, "4": nucleus, **suf_slots}
    slots.pop("irregular_slot2", None)
    irregular = "irregular_slot2" in (pre_slots or {})
    # §59's two named internal constraints, checked but NOT fit-gating —
    # they describe a further regularity within fitting roots, not the
    # six-slot criterion itself.
    slot3_vs_nucleus_tail = (
        "3" in slots and nucleus and nucleus[-1] in SONANTS and slots["3"] == nucleus[-1]
    )
    slot2 = slots.get("2", "")
    slot6 = slots.get("6", "")
    both_aspirated = (
        (slot2 in ASPIRATES or slot2 == "h") and
        any(u in ASPIRATES or u == "h" for u in tokenize_consonants(slot6))
    )
    return {
        "outcome": "fit",
        "slots": slots,
        "occupied": sorted(slots),
        "irregular_slot2": irregular,
        "constraint_violations": {
            "slot3_equals_nucleus_sonant": slot3_vs_nucleus_tail,
            "slot2_and_6_both_aspirated": both_aspirated,
        },
    }


def spellings_for(entry):
    sp = list(entry.get("whitney_spellings") or [])
    if not sp:
        # fallback for the 5 entries absent from Whitney: use the catalog's
        # own citation, substituting the ø/ø̄ null-vowel mark with the A1/A2
        # guṇa realization (documented Talmud-manual convention) so a nucleus
        # search has something to match.
        root = entry.get("root", "")
        sp = [root.replace("ø̄", "ā").replace("ø", "a")]
    return sp


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    roots = data["roots"]

    results = {}
    for entry in roots:
        verdict = None
        for spelling in spellings_for(entry):
            v = classify_root(spelling, entry["ryad"])
            verdict = v
            if v["outcome"] == "fit":
                break
        verdict["spelling_used"] = spelling
        results[entry["id"]] = verdict

    outcomes = {}
    for v in results.values():
        outcomes.setdefault(v["outcome"], 0)
        outcomes[v["outcome"]] += 1

    fits = outcomes.get("fit", 0)
    total = len(roots)
    resolved = total - outcomes.get("no_nucleus_found", 0)

    occupied_hist = {}
    irregular_slot2_roots = []
    slot1_roots = []
    slot6_cluster_roots = []
    constraint_hits = {"slot3_equals_nucleus_sonant": [], "slot2_and_6_both_aspirated": []}
    for rid, v in results.items():
        if v["outcome"] != "fit":
            continue
        key = ",".join(v["occupied"])
        occupied_hist[key] = occupied_hist.get(key, 0) + 1
        if v.get("irregular_slot2"):
            irregular_slot2_roots.append(rid)
        if "1" in v["slots"]:
            slot1_roots.append(rid)
        if len(v["slots"].get("6", "")) > 1 or (
            len(tokenize_consonants(v["slots"].get("6", ""))) > 1
        ):
            slot6_cluster_roots.append(rid)
        for k, hit in v["constraint_violations"].items():
            if hit:
                constraint_hits[k].append(rid)

    self_test_cases = [
        ("i", "I₁", {"4"}),
        ("nī", "I₂", {"3", "4"}),
        ("çru", "U₁", {"2", "3", "4"}),
        ("sthā", "A₂", {"1", "2", "4"}),
        ("styā", "A₂", {"1", "2", "3", "4"}),
        ("iṣ", "I₁", {"4", "6"}),
        ("pad", "A₁", {"2", "4", "6"}),
        ("krudh", "U₁", {"2", "3", "4", "6"}),
        ("jīv", "I₂", {"2", "4", "5"}),
        ("cumb", "U₁", {"2", "4", "5", "6"}),
        ("kṣṇu", "U₁", {"2", "3", "4"}),
        ("takṣ", "A₁", {"2", "4", "6"}),
        ("vyath", "A₁", {"2", "3", "4", "6"}),
        ("mlā", "A₂", {"2", "3", "4"}),
        ("katth", "A₁", {"2", "4", "6"}),
    ]
    self_test_fails = []
    for spelling, ryad, expected in self_test_cases:
        v = classify_root(spelling, ryad)
        got = set(v.get("occupied", []))
        if v["outcome"] != "fit" or got != expected:
            self_test_fails.append(
                {"root": spelling, "ryad": ryad, "expected": sorted(expected),
                 "got": v.get("outcome") if v["outcome"] != "fit" else sorted(got)}
            )

    out = {
        "instrument": "root_shape_parser.py over TolchelnikovTalmud_2026/data/"
                      "talmud_appendix1.json (745-root Приложение-1 catalog); "
                      "nucleus located by the catalog's own ryad tag per §50's "
                      "three-grade table, flanking consonants slotted per §59",
        "totals": {"roots": total, "resolved": resolved, **outcomes},
        "fit_rate_pct_of_all": round(100 * fits / total, 1),
        "fit_rate_pct_of_resolved": round(100 * fits / resolved, 1) if resolved else None,
        "occupied_slot_histogram": dict(sorted(occupied_hist.items(),
                                                key=lambda kv: -kv[1])),
        "named_exception_counts": {
            "irregular_slot2_v_or_m": len(irregular_slot2_roots),
            "slot1_s_plus_obstruent": len(slot1_roots),
            "slot6_obstruent_cluster": len(slot6_cluster_roots),
        },
        "named_exception_examples": {
            "irregular_slot2_v_or_m": irregular_slot2_roots[:10],
            "slot1_s_plus_obstruent": slot1_roots[:10],
            "slot6_obstruent_cluster": slot6_cluster_roots[:10],
        },
        "constraint_violations": {k: {"count": len(v), "examples": v[:10]}
                                   for k, v in constraint_hits.items()},
        "no_fit_examples": [
            {"id": rid, **v} for rid, v in results.items() if v["outcome"] == "no_fit"
        ][:20],
        "no_nucleus_examples": [rid for rid, v in results.items()
                                 if v["outcome"] == "no_nucleus_found"][:20],
        "extra_vowel_examples": [rid for rid, v in results.items()
                                  if v["outcome"] == "extra_vowel"],
        "self_test": {"cases": len(self_test_cases), "failures": self_test_fails},
    }
    (HERE / "och16_root_shape_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"roots: {total}, resolved (nucleus found): {resolved}")
    print(f"outcomes: {outcomes}")
    print(f"fit rate: {out['fit_rate_pct_of_all']}% of all, "
          f"{out['fit_rate_pct_of_resolved']}% of resolved")
    print(f"named exceptions: {out['named_exception_counts']}")
    print(f"self-test: {len(self_test_cases)} cases, "
          f"{len(self_test_fails)} failures", self_test_fails if self_test_fails else "")
    print("-> och16_root_shape_stats.json written")


if __name__ == "__main__":
    main()
