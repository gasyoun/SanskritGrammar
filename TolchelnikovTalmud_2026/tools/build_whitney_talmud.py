#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_whitney_talmud.py — Phase-3 enrichment crosswalk for the Talmud санскрита.

Joins the canonical, READ-ONLY WhitneyRoots data (``crosswalk/roots.csv`` +
``crosswalk/ppp_validation.json``) with the Talmud's analytical overlay
(Ряд / Тип / seṭ) and writes ``data/whitney_talmud.json`` inside THIS repo.

Provenance discipline (per IMPROVEMENT_PLAN.md + footnote-proposals/README.md):
  * Fields copied verbatim from WhitneyRoots are tagged  source="whitney".
  * The ablaut series (Ряд) is DERIVED from each root's nucleus vowel by the
    Table-2 calculus of §II — tagged  ryad_source="derived"  with a per-root
    confidence, and every derived value is a PROPOSAL pending the author's
    (Ivan / I.E. Tolchelnikov) approval. It is never asserted as his own.
  * seṭ/aniṭ is DERIVED (advisory) from the presence of the connecting vowel in
    the p.p.p. — tagged  set_source="derived-ppp".
  * Тип (s/a/v) is a lexical property Whitney records that is ABSENT from the
    WhitneyRoots JSON, so verbal roots carry  tip=null, tip_default="s"  (the
    unmarked behaviour) — we do NOT invent per-root exceptions.
  * The ~15 nominal roots the author himself tabulated in Приложение 2 are
    carried VERBATIM in ``nominal_appendix2`` with source="tolchelnikov".

WhitneyRoots is only ever read here; nothing in it is written or edited
(its class fields are revert-prone; scripts/sanskrit_util.py is a canonical
donor — untouched).

Usage:  python tools/build_whitney_talmud.py
Run from the TolchelnikovTalmud_2026 folder with a WhitneyRoots sibling clone.
"""
import csv
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_FOLDER = os.path.dirname(HERE)                       # TolchelnikovTalmud_2026/
GITHUB_ROOT = os.path.dirname(os.path.dirname(REPO_FOLDER))  # GitHub/
WR = os.path.join(GITHUB_ROOT, "WhitneyRoots")
ROOTS_CSV = os.path.join(WR, "crosswalk", "roots.csv")
PPP_JSON = os.path.join(WR, "crosswalk", "ppp_validation.json")
OUT_JSON = os.path.join(REPO_FOLDER, "data", "whitney_talmud.json")

# ---------------------------------------------------------------- Ряд (ablaut series)
# Table 2 of §II. The series letter is fixed by the root's nucleus vowel; the
# subscript by its length (short → 1, long → 2). Nasal-final a-roots whose weak
# grade shows a syllabic sonant belong to the M/N series rather than A.
VOWELS = ["ai", "au", "ā", "ī", "ū", "ṝ", "a", "i", "u", "ṛ", "ḷ", "e", "o"]

# nucleus vowel -> (series, confidence). "high" = phonologically unambiguous.
VOWEL_SERIES = {
    "a":  ("A₁", "medium"),   # ø / a / ā   (weak grade = syncope)
    "ā":  ("A₂", "medium"),   # ø / ā / ā
    "i":  ("I₁", "high"),
    "ī":  ("I₂", "high"),
    "u":  ("U₁", "high"),
    "ū":  ("U₂", "high"),
    "ṛ":  ("R₁", "high"),
    "ṝ":  ("R₂", "high"),
    "ḷ":  ("L",  "high"),
    # already-graded citation vowels: series recoverable but the citation form is
    # itself guṇa/vṛddhi, so flag low-confidence for the author to confirm.
    "e":  ("I₁", "low"),
    "o":  ("U₁", "low"),
    "ai": ("I₂", "low"),
    "au": ("U₂", "low"),
}


def find_nucleus(root_iast):
    """Return the last (ablauting) vowel of the citation root, or None."""
    s = root_iast.strip()
    last = None
    i = 0
    while i < len(s):
        matched = None
        for v in VOWELS:  # longest-first so 'ā'/'ai' beat 'a'
            if s.startswith(v, i):
                matched = v
                break
        if matched:
            last = matched
            i += len(matched)
        else:
            i += 1
    return last


def derive_ryad(root_iast):
    """(ryad, confidence, note) derived from the root's shape, or (None, ...)."""
    nuc = find_nucleus(root_iast)
    if nuc is None:
        return None, "none", "no vowel found in citation form"
    series, conf = VOWEL_SERIES[nuc]
    note = ""
    # Nasal-final a-roots: weak grade often vocalises the nasal (gam→gm̥, han→ghn),
    # placing them in the M/N series rather than A. Flag for author verification.
    if nuc == "a":
        tail = root_iast.strip()[-1]
        if tail == "m":
            series, note = "M₁", "a-root, nasal-final: M-series if weak grade vocalises m̥ (verify vs A₁)"
            conf = "medium"
        elif tail in ("n", "ṇ"):
            series, note = "N₁", "a-root, nasal-final: N-series if weak grade vocalises n̥ (verify vs A₁)"
            conf = "medium"
    return series, conf, note


# ---------------------------------------------------------------- seṭ / aniṭ
# seṭ roots insert a connecting i/ī before the -ta p.p.p. suffix (pat→patitá,
# grah→gṛhītá); aniṭ roots attach it directly (kṛ→kṛtá, bhū→bhūtá, gam→gatá).
# A vowel-final root (nī→nītá, bhū→bhūtá) shows i/ī/u/ū before -ta that is the
# root's OWN nucleus, not a connecting vowel — so the connecting-i signal is only
# read on consonant-final roots.
VOWEL_CHARS = "aāiīuūṛṝḷeoau"
SET_RE = re.compile(r"[iī]t[áa]$")
ANIT_RE = re.compile(r"(?:[aāiīuūṛ]?[tnṇ]|ḍh|ṣṭ|kt|gdh|ddh|nn|tt)[áa]$")


def derive_set(ppp, root):
    """('seṭ'|'aniṭ'|None, confidence) from the p.p.p. connecting vowel."""
    p = (ppp or "").strip()
    rt = (root or "").strip()
    if not p:
        return None, "none"
    vowel_final = bool(rt) and rt[-1] in VOWEL_CHARS
    if not vowel_final and SET_RE.search(p):
        return "seṭ", "medium"
    if ANIT_RE.search(p):
        return "aniṭ", "medium"
    return None, "low"


# ---------------------------------------------------------------- cohort (teaching order)
def cohort(dcs_rank):
    if not dcs_rank.strip():
        return "unranked"
    r = int(dcs_rank)
    if r <= 50:
        return "first"
    if r <= 200:
        return "second"
    return "later"


# ---------------------------------------------------------------- Приложение 2 (author's own)
# Carried VERBATIM from talmud-appendix-2.mdx — the author's own Тип/Ряд values
# for the high-frequency nominal roots. source="tolchelnikov" (authoritative).
NOMINAL_APPENDIX2 = [
    {"headword": "AKṢN̥", "deep": "{akṣn̥/akṣin/akṣi/akṣīn}", "tip_ryad": "I/I/I/III · N₁/I₁/I₁/I₂", "suffixes": "{0}", "gloss": "глаз"},
    {"headword": "ADAS",  "deep": "{a/am/adas}",             "tip_ryad": "II/II/II · A₁/A₁/A₁",       "suffixes": "{0}", "gloss": "то (указат. мест.)"},
    {"headword": "ADHI",  "deep": "{adhi}",                   "tip_ryad": "I · I₁",                    "suffixes": "{1.īc/anc/ac}, сложн. слова", "gloss": "над-, сверх- (приставка)"},
    {"headword": "ASMAD", "deep": "{asma/n/asmad/vaya}",      "tip_ryad": "II/-/II/II · A₁/-/A₁/A₁",   "suffixes": "{0}", "gloss": "мы (личное мест., мн.ч.)"},
    {"headword": "IDAM",  "deep": "{i/a/idam}",               "tip_ryad": "I/II/II · I₁/A₁/A₁",        "suffixes": "{0}", "gloss": "это (указат. мест.)"},
    {"headword": "KØ",    "deep": "{kø//kim}",                "tip_ryad": "I//I · A₁//I₁",             "suffixes": "{0}", "gloss": "кто? что? какой?"},
    {"headword": "GO",    "deep": "{go/gā}",                  "tip_ryad": "II/II · U₂/A₂",             "suffixes": "{0}, {2.ø}", "gloss": "корова, бык"},
    {"headword": "CATUṚ", "deep": "{catuṛ} (ж.р. {catusṛ})",  "tip_ryad": "I · R₁",                    "suffixes": "{0}, {1.thø}", "gloss": "четыре"},
    {"headword": "TØ",    "deep": "{tø/sø/tad}",              "tip_ryad": "I/I/II · A₁/A₁/A₁",         "suffixes": "{0}", "gloss": "то, он (указат. мест.)"},
    {"headword": "DIV",   "deep": "{div/dyā/dyu}",            "tip_ryad": "I/II/I · I₁/A₂/U₁",         "suffixes": "{0}, {2.ø}", "gloss": "небо, светлый, дэва"},
    {"headword": "DV",    "deep": "{dv} (замена {dvi/vi})",   "tip_ryad": "I · I₁",                    "suffixes": "{2.ø}, {1.tīyø}", "gloss": "два"},
    {"headword": "PITṚ",  "deep": "{pitṛ}",                   "tip_ryad": "I · R₁",                    "suffixes": "{0}", "gloss": "отец"},
    {"headword": "STRĪ",  "deep": "{strī}",                   "tip_ryad": "I · I₂",                    "suffixes": "{1.ø.III}", "gloss": "женщина"},
    {"headword": "SAKHI", "deep": "{sakhi/sakhā}",            "tip_ryad": "I/II · I₁/A₁",              "suffixes": "{0}", "gloss": "друг"},
    {"headword": "HṚD",   "deep": "{hṛd}",                    "tip_ryad": "I · R₁",                    "suffixes": "{0}, {1.ayø}", "gloss": "сердце"},
]


def build():
    with open(ROOTS_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    # ppp_validation gives an independent seṭ witness for a subset of roots.
    with open(PPP_JSON, encoding="utf-8") as f:
        pv = json.load(f)
    pv_by_no = {}
    for it in pv["items"]:
        pv_by_no.setdefault(it.get("whitney_no"), it)

    roots = []
    conf_counts = {"high": 0, "medium": 0, "low": 0, "none": 0}
    set_counts = {"seṭ": 0, "aniṭ": 0, "null": 0}
    for r in rows:
        wno = r["whitney_no"].strip()
        ryad, conf, note = derive_ryad(r["root_iast"])
        conf_counts[conf] = conf_counts.get(conf, 0) + 1

        # seṭ: prefer roots.csv ppp; corroborate with warnemyr_ppp when present.
        set_val, set_conf = derive_set(r["ppp"], r["root_iast"])
        pvi = pv_by_no.get(int(wno)) if wno.isdigit() else None
        if set_val is None and pvi:
            set_val, set_conf = derive_set(pvi.get("warnemyr_ppp", ""), r["root_iast"])
        set_counts[set_val if set_val else "null"] += 1

        classes = [c for c in r["class"].split("|") if c] if r["class"].strip() else []

        roots.append({
            "whitney_no": int(wno) if wno.isdigit() else wno,
            "root_iast": r["root_iast"],
            "root_slp1": r["root_slp1"],
            "homonym": r["homonym"] or None,
            "gloss": r["gloss_short"],
            # --- reliable joins (source=whitney) ---
            "class": classes,
            "ppp": r["ppp"] or None,
            "dcs_freq": int(r["dcs_freq"]) if r["dcs_freq"].strip().isdigit() else None,
            "dcs_rank": int(r["dcs_rank"]) if r["dcs_rank"].strip().isdigit() else None,
            "period_tags": [t for t in r["period_tags"].split("|") if t] if r["period_tags"].strip() else [],
            "mw_id": r["mw_id"] or None,
            "apte_id": r["apte_id"] or None,
            "warnemyr_url": r["warnemyr_url"] or None,
            "section_refs": r["section_refs"] or None,
            # --- Talmud analytical overlay ---
            "ryad": ryad,                       # DERIVED (proposal, pending author)
            "ryad_source": "derived" if ryad else None,
            "ryad_confidence": conf,
            "ryad_note": note or None,
            "tip": None,                        # Whitney records it; absent from WR JSON
            "tip_default": "s",                 # unmarked behaviour per Table 3
            "set": set_val,                     # DERIVED-advisory
            "set_source": "derived-ppp" if set_val else None,
            "set_confidence": set_conf,
            # --- teaching order ---
            "cohort": cohort(r["dcs_rank"]),
        })

    # deterministic order: by whitney_no
    roots.sort(key=lambda x: (isinstance(x["whitney_no"], str), x["whitney_no"]))

    payload = {
        "_meta": {
            "what": "Whitney root inventory joined with the Talmud санскрита analytical "
                    "overlay (Ряд/Тип/seṭ). Phase-3 enrichment crosswalk for the "
                    "interactive companion to Zaliznyak.",
            "source_data": {
                "whitney_roots": "WhitneyRoots/crosswalk/roots.csv (READ-ONLY)",
                "ppp_validation": "WhitneyRoots/crosswalk/ppp_validation.json (advisory seṭ witness)",
            },
            "provenance": {
                "whitney_fields": "class, ppp, dcs_freq, dcs_rank, period_tags, mw_id, "
                                  "apte_id, warnemyr_url, section_refs, gloss — copied verbatim.",
                "ryad": "DERIVED from the nucleus vowel by the Table-2 calculus (§II). "
                        "Every value is a PROPOSAL pending the author's approval; see "
                        "footnote-proposals/. Not asserted as Tolchelnikov's own.",
                "tip": "Lexical property Whitney records but absent from the WhitneyRoots "
                       "JSON — left null; unmarked default is 's' (Table 3).",
                "set": "DERIVED-advisory from the p.p.p. connecting vowel.",
                "nominal_appendix2": "Carried VERBATIM from the author's own Приложение 2 "
                                     "(source=tolchelnikov).",
            },
            "generator": "tools/build_whitney_talmud.py",
            "counts": {
                "verbal_roots": len(roots),
                "ryad_confidence": conf_counts,
                "set": set_counts,
                "nominal_appendix2": len(NOMINAL_APPENDIX2),
            },
        },
        "verbal_roots": roots,
        "nominal_appendix2": [
            {**n, "source": "tolchelnikov"} for n in NOMINAL_APPENDIX2
        ],
    }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"wrote {OUT_JSON}")
    print(f"  verbal_roots       : {len(roots)}")
    print(f"  ryad confidence    : {conf_counts}")
    print(f"  set (seṭ/aniṭ/null): {set_counts}")
    print(f"  nominal_appendix2  : {len(NOMINAL_APPENDIX2)}")


if __name__ == "__main__":
    build()
