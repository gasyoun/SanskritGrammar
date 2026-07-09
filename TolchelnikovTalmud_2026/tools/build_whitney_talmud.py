#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_whitney_talmud.py — Phase-3 enrichment crosswalk for the Talmud санскрита.

Joins the canonical, READ-ONLY WhitneyRoots data (``crosswalk/roots.csv`` +
``crosswalk/ppp_validation.json``) with the Talmud's analytical overlay
(Ряд / Тип / seṭ) and writes ``data/whitney_talmud.json`` inside THIS repo.

Provenance discipline — REFRAMED by the author's ruling on issue #50
(Tolchelnikov, 08-07-2026; H329 Phase 3):
  * Fields copied verbatim from WhitneyRoots are tagged  source="whitney".
  * Ряд, Тип and seṭ are now taken VERBATIM from the author's own Приложение 1
    catalog in the authoritative manual (``data/talmud_appendix1.json``, parsed
    by ``tools/parse_appendix1.py``) and tagged  ryad_source="manual" /
    set_source="manual" / tip_source="manual".  The manual is the SOLE authority
    (ruling: «взять ряд/seṭ из последней версии руководства»).  The earlier
    vowel-derived Ряд and p.p.p.-inferred seṭ were untrustworthy proposals and
    are NO LONGER emitted; the derivation code is retained only to compute the
    manual-vs-derived agreement in the reconciliation audit.
  * A Whitney root ABSENT from the author's catalog carries  ryad=null /
    set=null / tip=null  (no derived fallback) — the author catalogs no series
    for it, so we assert none.  ``tip_default="s"`` (Table 3) is kept as the
    unmarked runtime behaviour.
  * Un-indexed Ряд stays un-indexed (ruling #3: bare ``N``/``R``/``L`` are
    printed without a subscript on purpose); no ``0``-index variants.
  * The ~15 nominal roots the author himself tabulated in Приложение 2 are
    carried VERBATIM in ``nominal_appendix2`` with source="tolchelnikov".

WhitneyRoots is only ever read here; nothing in it is written or edited
(its class fields are revert-prone; scripts/sanskrit_util.py is a canonical
donor — untouched).

Run order (regenerate the manual catalog first):
    python tools/parse_appendix1.py       # -> data/talmud_appendix1.json
    python tools/build_whitney_talmud.py  # -> data/whitney_talmud.json (this file)
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
MANUAL_JSON = os.path.join(REPO_FOLDER, "data", "talmud_appendix1.json")
OUT_JSON = os.path.join(REPO_FOLDER, "data", "whitney_talmud.json")
RECON_MD = os.path.join(REPO_FOLDER, "data", "manual_reconciliation_report.md")

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


# ---------------------------------------------------------------- manual overlay (Приложение 1)
def build_manual_index(catalog, verbal):
    """Map each author-catalog row to a WhitneyRoots record.

    Join key is col4 «Список Уитни» (the Whitney nomenclature ref = author's own
    cross-reference, ruling #5). Strategy per manual row, over its spelling variants:
      1. (spelling, whitney_num)         — exact ref + homonym
      2. spelling with a unique Whitney root of that citation form (num ignored — no
         ambiguity when there is only one candidate)
      3. spelling with a homonym-less Whitney root
      4. fall back to the manual's own deep-root citation + its homonym index
    Returns  {whitney_no: manual_row}  keeping the strongest match on collision.
    """
    from collections import defaultdict
    by_rh, by_root = {}, defaultdict(list)
    for r in verbal:
        by_rh[(r["root_iast"], r["homonym"])] = r
        by_root[r["root_iast"]].append(r)

    # match strength so a later collision can't downgrade a ref+hom match
    STRENGTH = {"ref+hom": 3, "root-uniq": 2, "root-none": 2, "manualroot": 1, "manualroot-uniq": 1}

    def match(row):
        for sp in row["whitney_spellings"]:
            if row["whitney_num"] is not None:
                rec = by_rh.get((sp, row["whitney_num"]))
                if rec:
                    return rec, "ref+hom"
            cands = by_root.get(sp)
            if cands:
                if len(cands) == 1:
                    return cands[0], "root-uniq"
                none_c = [c for c in cands if c["homonym"] is None]
                if len(none_c) == 1:
                    return none_c[0], "root-none"
        rec = by_rh.get((row["root"], row["homonym"]))
        if rec:
            return rec, "manualroot"
        cands = by_root.get(row["root"])
        if cands and len(cands) == 1:
            return cands[0], "manualroot-uniq"
        return None, None

    overlay, methods, unmatched = {}, [], []
    for row in catalog:
        rec, meth = match(row)
        if rec is None:
            if row["whitney_spellings"]:   # NA rows are expected misses, don't log
                unmatched.append(row)
            continue
        wno = rec["whitney_no"]
        if wno in overlay and STRENGTH[overlay[wno][1]] >= STRENGTH[meth]:
            continue                       # keep the stronger existing match
        overlay[wno] = (row, meth)
        methods.append(meth)
    return overlay, methods, unmatched


def build():
    with open(ROOTS_CSV, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(MANUAL_JSON, encoding="utf-8") as f:
        manual = json.load(f)

    # ppp_validation gives an independent seṭ witness (used only for the audit now).
    with open(PPP_JSON, encoding="utf-8") as f:
        pv = json.load(f)
    pv_by_no = {}
    for it in pv["items"]:
        pv_by_no.setdefault(it.get("whitney_no"), it)

    # --- pass 1: base Whitney records + the (now audit-only) derived values ---
    roots = []
    derived_ryad, derived_set = {}, {}
    for r in rows:
        wno = r["whitney_no"].strip()
        wno_i = int(wno) if wno.isdigit() else wno
        d_ryad, _, _ = derive_ryad(r["root_iast"])
        d_set, _ = derive_set(r["ppp"], r["root_iast"])
        pvi = pv_by_no.get(int(wno)) if wno.isdigit() else None
        if d_set is None and pvi:
            d_set, _ = derive_set(pvi.get("warnemyr_ppp", ""), r["root_iast"])
        derived_ryad[wno_i] = d_ryad
        derived_set[wno_i] = d_set

        classes = [c for c in r["class"].split("|") if c] if r["class"].strip() else []
        roots.append({
            "whitney_no": wno_i,
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
            # --- Talmud analytical overlay (filled from the manual in pass 2) ---
            "ryad": None,
            "ryad_source": None,
            "tip": None,                        # from the manual where the author gives it
            "tip_source": None,
            "tip_default": "s",                 # unmarked runtime behaviour (Table 3)
            "set": None,
            "set_code": None,
            "set_source": None,
            "pada": None,
            # --- teaching order ---
            "cohort": cohort(r["dcs_rank"]),
        })

    # --- pass 2: overlay the author's Приложение 1 catalog (source of truth) ---
    by_no = {r["whitney_no"]: r for r in roots}
    overlay, methods, unmatched = build_manual_index(manual["roots"], roots)

    ryad_agree = ryad_diff = set_agree = set_diff = 0
    ryad_diffs = []
    for wno, (row, meth) in overlay.items():
        rec = by_no[wno]
        rec["ryad"] = row["ryad"]
        rec["ryad_source"] = "manual"
        rec["tip"] = row["tip"]
        rec["tip_source"] = "manual" if row["tip"] else None
        rec["set"] = row["set"]
        rec["set_code"] = row["set_code"]
        rec["set_source"] = "manual" if row["set"] else None
        rec["pada"] = row["pada"]
        # reconciliation vs the retired derived values
        d_r, d_s = derived_ryad.get(wno), derived_set.get(wno)
        if row["ryad"] and d_r:
            if row["ryad"] == d_r:
                ryad_agree += 1
            else:
                ryad_diff += 1
                ryad_diffs.append((rec["root_iast"], rec["homonym"], d_r, row["ryad"]))
        if row["set"] and d_s:
            if row["set"] == d_s:
                set_agree += 1
            else:
                set_diff += 1

    from collections import Counter
    method_counts = dict(Counter(methods))
    ryad_counts = Counter(r["ryad"] or "null" for r in roots)
    set_counts = Counter(r["set"] or "null" for r in roots)
    manual_ryad = sum(1 for r in roots if r["ryad_source"] == "manual")
    manual_set = sum(1 for r in roots if r["set_source"] == "manual")

    # deterministic order: by whitney_no
    roots.sort(key=lambda x: (isinstance(x["whitney_no"], str), x["whitney_no"]))

    payload = {
        "_meta": {
            "what": "Whitney root inventory joined with the Talmud санскрита analytical "
                    "overlay (Ряд/Тип/seṭ). Phase-3 enrichment crosswalk for the "
                    "interactive companion to Zaliznyak. Ряд/Тип/seṭ are the author's own "
                    "values from the manual (issue #50 ruling), not derived proposals.",
            "source_data": {
                "whitney_roots": "WhitneyRoots/crosswalk/roots.csv (READ-ONLY)",
                "manual_catalog": "data/talmud_appendix1.json (Приложение 1, Talmud-2.1.6.mdx)",
            },
            "provenance": {
                "whitney_fields": "class, ppp, dcs_freq, dcs_rank, period_tags, mw_id, "
                                  "apte_id, warnemyr_url, section_refs, gloss — copied verbatim.",
                "ryad": "VERBATIM from the author's Приложение 1 where he catalogs the root "
                        "(ryad_source='manual'); null otherwise. Un-indexed stays un-indexed.",
                "tip": "VERBATIM Тип (I/II/III/IV, Table 5) from Приложение 1 where present; "
                       "null otherwise. tip_default='s' is the unmarked runtime behaviour.",
                "set": "VERBATIM seṭ/aniṭ/veṭ from Приложение 1 (set_source='manual'); "
                       "set_code keeps the s/a/v1..v4 granularity (Table 8).",
                "nominal_appendix2": "Carried VERBATIM from the author's own Приложение 2 "
                                     "(source=tolchelnikov).",
            },
            "generator": "tools/build_whitney_talmud.py",
            "counts": {
                "verbal_roots": len(roots),
                "ryad_manual": manual_ryad,
                "ryad_null": len(roots) - manual_ryad,
                "ryad": dict(ryad_counts),
                "set_manual": manual_set,
                "set": dict(set_counts),
                "nominal_appendix2": len(NOMINAL_APPENDIX2),
                "manual_match": {
                    "catalog_rows": len(manual["roots"]),
                    "matched_whitney_roots": len(overlay),
                    "unmatched_catalog_rows": len(unmatched),
                    "methods": method_counts,
                },
            },
        },
        "verbal_roots": roots,
        "nominal_appendix2": [
            {**n, "source": "tolchelnikov"} for n in NOMINAL_APPENDIX2
        ],
    }

    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)

    _write_reconciliation(overlay, unmatched, manual, ryad_agree, ryad_diff,
                          set_agree, set_diff, ryad_diffs, len(roots),
                          manual_ryad, manual_set, method_counts)

    print(f"wrote {OUT_JSON}")
    print(f"  verbal_roots        : {len(roots)}")
    print(f"  Ряд from manual     : {manual_ryad}  (null: {len(roots) - manual_ryad})")
    print(f"  seṭ from manual     : {manual_set}")
    print(f"  catalog matched     : {len(overlay)}/{len(manual['roots'])}  "
          f"unmatched: {len(unmatched)}  methods: {method_counts}")
    print(f"  Ряд vs derived      : {ryad_agree} agree / {ryad_diff} differ")
    print(f"  seṭ vs derived      : {set_agree} agree / {set_diff} differ")
    print(f"  nominal_appendix2   : {len(NOMINAL_APPENDIX2)}")


def _write_reconciliation(overlay, unmatched, manual, ryad_agree, ryad_diff,
                          set_agree, set_diff, ryad_diffs, n_roots,
                          manual_ryad, manual_set, method_counts):
    """Audit trail: why the retired derived Ряд/seṭ were untrustworthy, and how
    completely the author's catalog now covers the Whitney spine."""
    ra_tot = ryad_agree + ryad_diff
    sa_tot = set_agree + set_diff
    L = []
    L.append("# Manual-catalog reconciliation — Приложение 1 → whitney_talmud.json")
    L.append("")
    L.append("_Created: 08-07-2026 · Last updated: 08-07-2026_")
    L.append("")
    L.append("Audit trail for H329 Phase 3: the author (I.E. Tolchelnikov) ruled on "
             "[issue #50](https://github.com/gasyoun/SanskritGrammar/issues/50) that "
             "Ряд/seṭ must come from the latest manual, not from the vowel-derived "
             "proposals or the older samskrtam.ru/z/ snapshot. This records what "
             "changed when the author's own [Приложение 1]"
             "(https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/Talmud-2.1.6.mdx) "
             "catalog replaced the derived values.")
    L.append("")
    L.append("## Coverage")
    L.append("")
    L.append("| Metric | Value |")
    L.append("| :--- | ---: |")
    L.append(f"| Author-catalog rows (Приложение 1) | {len(manual['roots'])} |")
    L.append(f"| Matched to a Whitney root | {len(overlay)} |")
    L.append(f"| Unmatched catalog rows (excl. NA) | {len(unmatched)} |")
    L.append(f"| Whitney verbal roots total | {n_roots} |")
    L.append(f"| …carrying a manual Ряд | {manual_ryad} |")
    L.append(f"| …carrying a manual seṭ | {manual_set} |")
    L.append(f"| …with Ряд=null (not in the author's catalog) | {n_roots - manual_ryad} |")
    L.append("")
    L.append(f"Join methods: `{method_counts}` (ref+hom = Whitney ref number + spelling; "
             "root-uniq = unique citation form).")
    L.append("")
    L.append("## Manual vs the retired derived values")
    L.append("")
    L.append("The derivation code is kept only to quantify how wrong the proposals were.")
    L.append("")
    L.append("| Field | Agree | Differ | Agreement |")
    L.append("| :--- | ---: | ---: | ---: |")
    if ra_tot:
        L.append(f"| Ряд | {ryad_agree} | {ryad_diff} | {100*ryad_agree/ra_tot:.1f}% |")
    if sa_tot:
        L.append(f"| seṭ | {set_agree} | {set_diff} | {100*set_agree/sa_tot:.1f}% |")
    L.append("")
    L.append(f"So the vowel-derived Ряд disagreed with the author on **{ryad_diff}** of "
             f"{ra_tot} comparable roots — the concrete justification for the author's "
             "ruling. The dominant pattern is un-indexed bare series the derivation "
             "over-specified (`N`→`N₁`, `R`→`A₂`) and the systematic ṛ-nucleus divergence.")
    L.append("")
    L.append("### Sample Ряд disagreements (derived → manual)")
    L.append("")
    L.append("| Root | Hom. | Derived | Manual |")
    L.append("| :--- | :---: | :---: | :---: |")
    for root, hom, dr, mr in ryad_diffs[:30]:
        L.append(f"| `{root}` | {hom or '—'} | {dr} | {mr} |")
    L.append("")
    if unmatched:
        L.append("### Unmatched catalog rows (spelling not in WhitneyRoots)")
        L.append("")
        L.append("| Id | Root | Whitney ref |")
        L.append("| :--- | :--- | :--- |")
        for row in unmatched:
            L.append(f"| {row['id']} | `{row['root']}` | {row['whitney_ref']} |")
        L.append("")
    L.append("_Auto-generated by tools/build_whitney_talmud.py._")
    with open(RECON_MD, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print(f"wrote {RECON_MD}")


if __name__ == "__main__":
    build()
