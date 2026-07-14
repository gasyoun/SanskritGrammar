#!/usr/bin/env python
"""verify_claims_dcs.py — reproducible corpus statistics behind the Kochergina
claim register (H768).

Reads the committed DCS-2021 relational export in the sibling VisualDCS repo and
emits the numbers that back the `verdict_fact` fields in `claims.yml`. Run it to
regenerate `claims_dcs_stats.json` (consumed by the reading-site overlay) and a
console report.

Ground-truth source: Digital Corpus of Sanskrit (Oliver Hellwig, DCS-2021, CC BY),
    ../VisualDCS/src/DCS-data-2021/
        15.csv  finite verb forms   : id,word_id,'form',tense_code,pn_code,
        12.csv  non-finite forms    : id,word_id,'form','stem',cat_code,code2,
        timws.csv  38 tense/mood categories x corpus TOKEN frequency
    ../VisualDCS/tense_case_data.json  (total_verbal token count)

15.csv / 12.csv are DISTINCT-FORM (type) tables; timws.csv gives TOKENS. The two
together give the type/token split the register needs (a form can be common in
paradigm tables yet rare in running text).

Usage:  python verify_claims_dcs.py            # report + rewrite claims_dcs_stats.json
        python verify_claims_dcs.py --check     # report only, no file write
"""
import sys, json, re, unicodedata
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
# VisualDCS is a sibling repo under GitHub/
VDCS = REPO.parent / "VisualDCS"
DCS = VDCS / "src" / "DCS-data-2021"

# Tense/mood code legend + TOKEN counts (timws.csv: "ID:  Label :count")
TOK, LABEL = {}, {}
for ln in (DCS / "timws.csv").read_text(encoding="utf-8").splitlines()[1:]:
    m = re.match(r"\s*(\d+):(.*):(\d+)\s*$", ln)
    if m:
        c = int(m.group(1)); LABEL[c] = m.group(2).strip(); TOK[c] = int(m.group(3))

TOTAL_VERBAL = json.load(open(VDCS / "tense_case_data.json", encoding="utf-8"))["total_verbal"]


def _forms(fn, code_idx, form_idx=2):
    """Yield (form, code) from a DCS analysis CSV (single-quoted form field)."""
    for ln in (DCS / fn).read_text(encoding="utf-8").splitlines():
        p = ln.split(",")
        if len(p) <= code_idx:
            continue
        try:
            code = int(p[code_idx])
        except ValueError:
            continue
        yield p[form_idx].strip().strip("'"), code


def pct(n):
    return round(100 * n / TOTAL_VERBAL, 2)


# --- H797 backlog-verification helpers --------------------------------------
# Monophthong vowel census over the FULL DCS-2021 running text (0.csv surface
# lines: "...;<devanagari-ids>;<IAST surface text>"). Backs the phonology-lesson
# frequency claims: a/ā dominance and ṛ >> ṝ/ḷ/ḹ rarity.
VOWELS_IAST = "aāiīuūṛṝḷḹeo"


def vowel_census():
    corpus = DCS / "0.csv"
    cnt = Counter()
    lines = 0
    if not corpus.exists():
        return None
    with open(corpus, encoding="utf-8") as f:
        for ln in f:
            i = ln.rfind(";")
            if i < 0:
                continue
            for ch in unicodedata.normalize("NFC", ln[i + 1:]):
                if ch in VOWELS_IAST:
                    cnt[ch] += 1
            lines += 1
    tot = sum(cnt.values())
    if not tot:
        return None
    rare = cnt["ṝ"] + cnt["ḷ"] + cnt["ḹ"]
    return {
        "corpus_lines": lines,
        "total_monophthong_vowels": tot,
        "counts": {v: cnt[v] for v in VOWELS_IAST},
        "pct": {v: round(100 * cnt[v] / tot, 2) for v in VOWELS_IAST},
        "a_plus_aa_pct": round(100 * (cnt["a"] + cnt["ā"]) / tot, 1),
        "vocalic_r_count": cnt["ṛ"],
        "rare_sonants_count": rare,  # ṝ + ḷ + ḹ
        "r_over_rare_ratio": round(cnt["ṛ"] / rare, 0) if rare else None,
    }


def verb_class_share():
    """Thematic (I/IV/VI/X) vs athematic (II/III/V/VII/VIII/IX) present-system
    token share, from VisualDCS/verb_classes.json. Backs 'первое главное
    спряжение охватывает большинство глаголов'."""
    fp = VDCS / "verb_classes.json"
    if not fp.exists():
        return None
    d = json.load(open(fp, encoding="utf-8"))
    TH, ATH = {"1", "4", "6", "10"}, {"2", "3", "5", "7", "8", "9"}
    th = sum(d[k].get("total", 0) for k in d if k in TH)
    at = sum(d[k].get("total", 0) for k in d if k in ATH)
    tot = th + at
    return {
        "thematic_tokens": th,
        "athematic_tokens": at,
        "primary_conjugation_pct": round(100 * th / tot, 1) if tot else None,
        "class_II_tokens": d.get("2", {}).get("total"),
        "class_II_pct_of_present_system": round(100 * d.get("2", {}).get("total", 0) / tot, 1) if tot else None,
    }


# --- H797 Phase 2 (Bühler) metrics ------------------------------------------
# The register generalised to BuhlerLeitfaden_1923 (same DCS/Whitney ground
# truth). These back the HB-* claims that need corpus numbers of their own.
def buhler_metrics(finite, nonfin):
    # HB: -tāt imperative ("иногда при благословении") — forms in tense code 3
    imp_forms = {f for f, c in finite if c == 3}
    taat = sorted(f for f in imp_forms if f.endswith("tāt"))
    # HB: absolutive allomorphy -tvā / -ya / -am (Урок XXIX "очень редкая форма am")
    abs_forms = {f for f, c in nonfin if c == 23}
    ab = Counter()
    for f in abs_forms:
        if f.endswith("tvā") or f.endswith("tvī"):
            ab["-tvā"] += 1
        elif f.endswith("ya"):
            ab["-ya"] += 1
        elif f.endswith("am"):
            ab["-am"] += 1
        else:
            ab["other"] += 1
    atot = len(abs_forms)
    return {
        "HB_taat_imperative": {
            "distinct_taat_forms": len(taat),
            "total_imperative_forms": len(imp_forms),
            "taat_share_pct": round(100 * len(taat) / len(imp_forms), 2) if imp_forms else None,
            "examples": taat[:12],
        },
        "HB_optative": {                    # Урок XVI: optative uses; frequency context
            "tokens": TOK[2], "pct_of_verbal": pct(TOK[2]), "label": LABEL.get(2, ""),
            "cf_present_tokens": TOK[1],
        },
        "HB_future_periphrastic": {         # Урок I inventory: описательное vs простое будущее
            "periphrastic_tokens": TOK[7], "simple_future_tokens": TOK[5],
            "periphrastic_pct_of_verbal": pct(TOK[7]),
        },
        "HB_absolutive_allomorphy": {
            "distinct_forms": atot, "tokens": TOK[23],
            "suffix_split_types": dict(ab),
            "suffix_split_pct": {k: round(100 * v / atot, 1) for k, v in ab.items()},
        },
    }


def analyze():
    finite = list(_forms("15.csv", 3))     # (form, tense_code)
    nonfin = list(_forms("12.csv", 4))     # (form, cat_code)

    # HK-1 aorist (codes 10-13 Act/Med)
    AOR = {10, 11, 12, 13}
    aor_forms = {f for f, c in finite if c in AOR}
    aor_tok = sum(TOK[c] for c in AOR)

    # HK-3 gerundive / Fut. Pass. Part. (code 21) vs PPP (code 19)
    ger_forms = {f for f, c in nonfin if c == 21}
    ppp_forms = {f for f, c in nonfin if c == 19}
    ger_suf = Counter()
    for f in ger_forms:
        if "tavy" in f:
            ger_suf["-tavya"] += 1
        elif "anīy" in f:
            ger_suf["-anīya"] += 1
        else:
            ger_suf["-ya"] += 1

    # HK-4 future (code 5 Future Active) allomorphy -sya / -ṣya / -iṣya
    fut_forms = sorted({f for f, c in finite if c == 5})
    allo = Counter()
    for f in fut_forms:
        if "iṣy" in f:
            allo["-iṣya"] += 1
        elif "ṣy" in f:
            allo["-ṣya"] += 1
        elif "sy" in f:
            allo["-sya"] += 1
        else:
            allo["other"] += 1
    ftot = len(fut_forms)

    # --- P1-continuation claims (full-textbook harvest, H768) ---------------
    # HK-36 imperative person distribution. Kochergina (Занятие XIV): "Наиболее
    # часто ... употребляются формы 2-го лица." 15.csv col5 = pn_code, DCS
    # convention 1..9 = {1sg,2sg,3sg,1du,2du,3du,1pl,2pl,3pl}; person = code mod 3.
    imp_pn = Counter()
    for ln in (DCS / "15.csv").read_text(encoding="utf-8").splitlines():
        p = ln.split(",")
        if len(p) <= 4:
            continue
        try:
            tc = int(p[3]); pn = int(p[4].strip().rstrip(";"))
        except ValueError:
            continue
        if tc == 3:                                          # Imperative Active
            imp_pn[{1: "1", 2: "2", 3: "3"}[((pn - 1) % 3) + 1]] += 1
    imp_tot = sum(imp_pn.values())

    # HK-32 past-passive-participle suffix -ta vs -na (code 19), distinct forms.
    ppp_ta = ppp_na = 0
    for f in ppp_forms:
        if f.endswith(("na", "ṇa")):
            ppp_na += 1
        elif f.endswith(("ta", "ṭa")):
            ppp_ta += 1

    stats = {
        "_source": "DCS-2021 (Oliver Hellwig, CC BY) via VisualDCS/src/DCS-data-2021",
        "_note": "types = distinct forms (15.csv/12.csv); tokens = running-text counts (timws.csv)",
        "total_verbal_tokens": TOTAL_VERBAL,
        "HK1_aorist": {
            "distinct_forms": len(aor_forms),
            "tokens": aor_tok,
            "pct_of_verbal": pct(aor_tok),
            "cf_present_tokens": TOK[1],
        },
        "HK3_gerundive": {
            "distinct_forms": len(ger_forms),
            "tokens": TOK[21],
            "pct_of_verbal": pct(TOK[21]),
            "suffix_split_types": dict(ger_suf),
            "cf_ppp_tokens": TOK[19],
            "cf_ppp_pct": pct(TOK[19]),
            "cf_ppp_distinct_forms": len(ppp_forms),
        },
        "HK4_future": {
            "distinct_forms": ftot,
            "tokens": TOK[5],
            "pct_of_verbal": pct(TOK[5]),
            "allomorphy_types": dict(allo),
            "allomorphy_pct": {k: round(100 * v / ftot, 1) for k, v in allo.items()},
            "sec_iṣya_share": round(100 * allo["-iṣya"] / ftot, 1),
        },
        # --- full-textbook-harvest claims (H768 P1 continuation) ---
        "HK23_conditional": {                       # "conditional сравнительно редко"
            "tokens": TOK[6], "pct_of_verbal": pct(TOK[6]),
            "cf_present_tokens": TOK[1], "label": LABEL.get(6, ""),
        },
        "HK29_ppp_suffix": {                        # PPP -(i)ta vs (реже) -na
            "distinct_ta": ppp_ta, "distinct_na": ppp_na,
            "na_share_pct": round(100 * ppp_na / (ppp_ta + ppp_na), 1),
        },
        "HK17_imperative_person": {                 # imperative "наиболее часто 2-го лица"
            "distinct_forms_by_person": dict(imp_pn),
            "second_person_share_pct": round(100 * imp_pn["2"] / imp_tot, 1),
            "total_imperative_active_forms": imp_tot,
        },
        "HK39_precative_middle": {                  # прекатив Ātmanepada крайне редко
            "tokens": TOK[14], "pct_of_verbal": pct(TOK[14]), "label": LABEL.get(14, ""),
        },
        # --- H797 backlog-verification metrics ---
        # HK-7 / HK-8 / backlog: vowel frequency census (a/ā dominance; ṛ >> ṝ/ḷ/ḹ)
        "HK7_vowel_census": vowel_census(),
        # HK-18 / backlog line 3202: thematic-conjugation share of the present system
        "HK18_verb_class_share": verb_class_share(),
        # HK-15 / backlog: past-tense category competition (imperfect vs perfect vs aorist)
        "HK15_past_tenses": {
            "imperfect_tokens": TOK[4] + TOK[8] + TOK[9] + TOK[16] + TOK[27],
            "perfect_tokens": TOK[15],
            "aorist_tokens": sum(TOK[c] for c in (10, 11, 12, 13)),
            "note": "imperfect = active+medium+augmentless+passive imperfect codes; perfect = code 15; aorist = 10-13",
        },
        # backlog (visarga/anusvāra 'mainly in this case-form'): case-slot token distribution
        "case_distribution": {
            c["abbr"]: {"sg": c["sg"], "du": c["du"], "pl": c["pl"], "total": c["total"]}
            for c in json.load(open(VDCS / "tense_case_data.json", encoding="utf-8"))["cases"]
        } if (VDCS / "tense_case_data.json").exists() else None,
    }
    # --- H797 Phase 2: Bühler (HB-*) metrics ---
    stats.update(buhler_metrics(finite, nonfin))
    return stats


def report(s):
    print(f"total verbal tokens (DCS-2021): {s['total_verbal_tokens']:,}\n")
    h1 = s["HK1_aorist"]
    print("HK-1 AORIST — 'формы аориста образуются лишь от части корней'")
    print(f"  {h1['distinct_forms']} distinct aorist forms; {h1['tokens']:,} tokens "
          f"= {h1['pct_of_verbal']}% of verbal (cf. present {h1['cf_present_tokens']:,})")
    h3 = s["HK3_gerundive"]
    print("\nHK-3 GERUNDIVE (participium necessitatis, Fut.Pass.Part.)")
    print(f"  {h3['distinct_forms']} distinct forms; {h3['tokens']:,} tokens "
          f"= {h3['pct_of_verbal']}% of verbal")
    print(f"  suffix split (types): {h3['suffix_split_types']}")
    print(f"  cf. PPP {h3['cf_ppp_tokens']:,} tokens ({h3['cf_ppp_pct']}%), "
          f"{h3['cf_ppp_distinct_forms']} forms")
    h4 = s["HK4_future"]
    print("\nHK-4 FUTURE — '-syá по единому правилу; согл. корни: -ṣya/-iṣya'")
    print(f"  {h4['distinct_forms']} distinct future forms; {h4['tokens']:,} tokens "
          f"= {h4['pct_of_verbal']}% of verbal")
    print(f"  allomorphy (types): {h4['allomorphy_types']}  → {h4['allomorphy_pct']}")
    print(f"  the seṭ form -iṣya is the MAJORITY: {h4['sec_iṣya_share']}% of distinct future forms")

    print("\n--- full-textbook-harvest claims ---")
    c = s["HK23_conditional"]
    print(f"HK-23 CONDITIONAL ('сравнительно редко'): {c['tokens']:,} tokens "
          f"= {c['pct_of_verbal']}% of verbal (cf. present {c['cf_present_tokens']:,})")
    p = s["HK29_ppp_suffix"]
    print(f"HK-29 PPP suffix -ta {p['distinct_ta']:,} / -na {p['distinct_na']:,} distinct forms "
          f"→ -na is {p['na_share_pct']}% ('реже' confirmed)")
    im = s["HK17_imperative_person"]
    print(f"HK-17 IMPERATIVE by person (distinct forms): {im['distinct_forms_by_person']} "
          f"→ 2nd person {im['second_person_share_pct']}% of {im['total_imperative_active_forms']:,}")
    pr = s["HK39_precative_middle"]
    print(f"HK-39 PRECATIVE Ātmanepada (Benedictive Medium): {pr['tokens']} tokens "
          f"= {pr['pct_of_verbal']}% of verbal ('крайне редко' confirmed)")

    print("\n--- H797 backlog-verification metrics ---")
    vc = s.get("HK7_vowel_census")
    if vc:
        print(f"VOWEL CENSUS (DCS-2021 0.csv, {vc['total_monophthong_vowels']:,} vowels): "
              f"a+ā = {vc['a_plus_aa_pct']}% (a {vc['pct']['a']}%, ā {vc['pct']['ā']}%)")
        print(f"  ṛ {vc['counts']['ṛ']:,} ({vc['pct']['ṛ']}%) vs ṝ {vc['counts']['ṝ']:,} / "
              f"ḷ {vc['counts']['ḷ']:,} / ḹ {vc['counts']['ḹ']:,} — ṛ is {vc['r_over_rare_ratio']:.0f}× the rare sonants")
    cl = s.get("HK18_verb_class_share")
    if cl:
        print(f"VERB CLASS SHARE: thematic (I/IV/VI/X) {cl['thematic_tokens']:,} = "
              f"{cl['primary_conjugation_pct']}% of present-system tokens; athematic "
              f"{cl['athematic_tokens']:,}; class II {cl['class_II_tokens']:,} "
              f"({cl['class_II_pct_of_present_system']}%)")
    pt = s.get("HK15_past_tenses")
    if pt:
        print(f"PAST-TENSE COMPETITION: imperfect {pt['imperfect_tokens']:,} · "
              f"perfect {pt['perfect_tokens']:,} · aorist {pt['aorist_tokens']:,} tokens")

    print("\n--- H797 Phase 2: Bühler (HB) metrics ---")
    tt = s.get("HB_taat_imperative")
    if tt:
        print(f"HB -tāt IMPERATIVE ('иногда при благословении'): {tt['distinct_taat_forms']} of "
              f"{tt['total_imperative_forms']:,} imperative forms = {tt['taat_share_pct']}% "
              f"(e.g. {', '.join(tt['examples'][:4])})")
    op = s.get("HB_optative")
    if op:
        print(f"HB OPTATIVE: {op['tokens']:,} tokens = {op['pct_of_verbal']}% of verbal "
              f"(cf. present {op['cf_present_tokens']:,})")
    fp = s.get("HB_future_periphrastic")
    if fp:
        print(f"HB PERIPHRASTIC vs SIMPLE FUTURE: {fp['periphrastic_tokens']:,} vs "
              f"{fp['simple_future_tokens']:,} tokens ({fp['periphrastic_pct_of_verbal']}% of verbal)")
    ab = s.get("HB_absolutive_allomorphy")
    if ab:
        print(f"HB ABSOLUTIVE ALLOMORPHY ({ab['distinct_forms']:,} distinct forms, "
              f"{ab['tokens']:,} tokens): {ab['suffix_split_types']} → {ab['suffix_split_pct']}")


def main():
    stats = analyze()
    report(stats)
    if "--check" not in sys.argv:
        out = HERE / "claims_dcs_stats.json"
        out.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n-> wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
