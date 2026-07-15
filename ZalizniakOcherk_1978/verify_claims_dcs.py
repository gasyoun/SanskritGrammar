#!/usr/bin/env python
"""verify_claims_dcs.py — reproducible corpus statistics behind the Zaliznyak
Ocherk claim register (H797 Phase 2).

Unlike KocherginaUchebnik_1998's and BuhlerLeitfaden_1923's verify scripts, most of this
book's seed claims (OCH-1, OCH-3, OCH-5) REUSE ground truth already computed for those two
books rather than recomputing it — see claims.yml's synthesis for why (the cross-grammar
program's corpus infrastructure compounds; the same DCS fact doesn't need re-deriving every
time a new grammar happens to also state it). This script computes only the two claims that
needed fresh numbers: OCH-2 (class-I token share) and OCH-6 (thematic-suffix a/ya/aya ranking).

Ground-truth source: Digital Corpus of Sanskrit (Oliver Hellwig, DCS-2021, CC BY),
    ../../VisualDCS/verb_classes.json  (present-class token totals, P/A split, top roots)

Usage:  python verify_claims_dcs.py            # report + rewrite claims_dcs_stats.json
        python verify_claims_dcs.py --check     # report only, no file write
"""
import sys, json, re
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
VDCS = REPO.parent / "VisualDCS"
DCS = VDCS / "src" / "DCS-data-2021"
TALMUD_ROOTS = REPO / "TolchelnikovTalmud_2026" / "data" / "talmud_appendix1.json"

IAST_LETTERS = "a-zāīūṛṝḷḹṅñṭḍṇśṣḥṃṁ"
VOWEL_FINALS = set("aāiīuūṛṝḷḹeo")  # ai/au end in i/u and are caught by endswith below


def _timws():
    """Tense/mood token counts (same loader as the Kochergina battery)."""
    tok, label = {}, {}
    for ln in (DCS / "timws.csv").read_text(encoding="utf-8").splitlines()[1:]:
        m = re.match(r"\s*(\d+):(.*):(\d+)\s*$", ln)
        if m:
            c = int(m.group(1)); label[c] = m.group(2).strip(); tok[c] = int(m.group(3))
    return tok, label


def _forms(fn, code_idx, form_idx=2):
    for ln in (DCS / fn).read_text(encoding="utf-8").splitlines():
        p = ln.split(",")
        if len(p) <= code_idx:
            continue
        try:
            code = int(p[code_idx])
        except ValueError:
            continue
        yield p[form_idx].strip().strip("'"), code


def _surface_tokens():
    """Yield word tokens from the DCS running surface text (0.csv, IAST after the last ';')."""
    word_re = re.compile(f"[{IAST_LETTERS}]+")
    with open(DCS / "0.csv", encoding="utf-8") as f:
        for ln in f:
            i = ln.rfind(";")
            if i < 0:
                continue
            for w in word_re.findall(ln[i + 1:].lower()):
                yield w


def final_consonant_census():
    """§18 fn / §19 fn / §43 п.1: which consonants actually END words in running text.
    Backs: word-final l 'практически не встречается'; final ṇ/ṅ/ñ rare; final t the most
    common final stop (so its pre-nasal assimilation is the most-often-seen one)."""
    finals = Counter()
    n_words = 0
    for w in _surface_tokens():
        finals[w[-1]] += 1
        n_words += 1
    cons = {c: finals.get(c, 0) for c in "lṇṅñnmtdkṭpbḥṃṁrśṣs"}
    vowel_final = sum(v for k, v in finals.items() if k in VOWEL_FINALS)
    return {
        "n_word_tokens": n_words,
        "vowel_final_tokens": vowel_final,
        "final_counts": cons,
        "final_pct_of_words": {c: round(100 * v / n_words, 4) for c, v in cons.items()},
        "stop_ranking_ktTp": sorted(((c, cons[c]) for c in "ktṭp"), key=lambda x: -x[1]),
    }


def sah_so_sa():
    """§105 note: does saḥ actually surface mostly as so / sa in running text."""
    cnt = Counter()
    targets = {"saḥ", "so", "sa"}
    for w in _surface_tokens():
        if w in targets:
            cnt[w] += 1
    tot = sum(cnt.values())
    return {
        "counts": dict(cnt),
        "so_sa_share_pct": round(100 * (cnt["so"] + cnt["sa"]) / tot, 1) if tot else None,
        "note": "token 'sa' is overwhelmingly the pronoun in running text but includes a few "
                "homographs; direction test, not a clean count.",
    }


def vet_i_rates():
    """§63: does the connective i appear most readily before -sya-/-tar- and least before
    -ta-/-tvā-. Aggregate proxy over ALL distinct forms (per-root veṭ-only tagging would
    need the Talmud set_code join; the aggregate i-rate ranking is the direction test)."""
    fut = {f for f, c in _forms("15.csv", 3) if c == 5}
    ppf = {f for f, c in _forms("15.csv", 3) if c == 7}          # periphrastic future = -tar- stem
    ppp = {f for f, c in _forms("12.csv", 4) if c == 19}
    ger = {f for f, c in _forms("12.csv", 4) if c == 21}
    absx = {f for f, c in _forms("12.csv", 4) if c == 23}
    tva = {f for f in absx if f.endswith("tvā") or f.endswith("tvī")}

    def rate(forms, i_suffix, plain_suffix):
        i_n = sum(1 for f in forms if f.endswith(i_suffix))
        all_n = sum(1 for f in forms if f.endswith(plain_suffix))  # includes the i-forms
        return {"i_forms": i_n, "all_forms": all_n,
                "i_rate_pct": round(100 * i_n / all_n, 1) if all_n else None}

    fut_i = sum(1 for f in fut if "iṣy" in f)
    return {
        "before_sya": {"i_forms": fut_i, "all_forms": len(fut),
                       "i_rate_pct": round(100 * fut_i / len(fut), 1)},
        "before_tar_periphrastic": rate(ppf, "itā", "tā"),
        "before_tavya": rate(ger, "itavya", "tavya"),
        "before_ta_ppp": rate(ppp, "ita", "ta"),
        "before_tva": rate(tva, "itvā", "tvā"),
    }


def rare_moods():
    """§109: precative / injunctive / conditional 'сравнительно редко' vs the big three."""
    tok, _ = _timws()
    total_verbal = 781618
    return {
        "indicative_present": tok[1], "optative_active": tok[2], "imperative_active": tok[3],
        "benedictive_medium": tok[14], "injunctive": tok[30], "conditional": tok[6],
        "rare_three_pct_of_verbal": round(100 * (tok[14] + tok[30] + tok[6]) / total_verbal, 3),
    }


def talmud_set_by_series():
    """§68 FLAGSHIP: does the seṭ/aniṭ split correlate with alternation-series membership —
    open (vowel-final) roots of series I₁/U₁/R₁/M₁/N₁ + I₂ 'обычно aniṭ', other open roots
    'обычно seṭ'. Adjudicated against the Talmud Приложение-1 root catalog (the D-B
    root-morphoclass authority), joined on the author's own ryad × set columns."""
    if not TALMUD_ROOTS.exists():
        return None
    d = json.load(open(TALMUD_ROOTS, encoding="utf-8"))
    A_SERIES = {"I₁", "U₁", "R₁", "M₁", "N₁", "I₂"}
    ga, gb = Counter(), Counter()
    n_open = 0
    for r in d["roots"]:
        ryad, sset = r.get("ryad"), r.get("set")
        sp = (r.get("whitney_spellings") or [None])[0] or ""
        if not ryad or not sset or not sp:
            continue
        if sp[-1] not in VOWEL_FINALS and not sp.endswith(("ai", "au")):
            continue                                    # closed (consonant-final) root
        n_open += 1
        (ga if ryad in A_SERIES else gb)[sset] += 1
    return {
        "open_roots_with_ryad_and_set": n_open,
        "groupA_series_I1_U1_R1_M1_N1_I2": dict(ga),
        "groupA_anit_share_pct": round(100 * ga["aniṭ"] / sum(ga.values()), 1) if ga else None,
        "groupB_other_series": dict(gb),
        "groupB_set_share_pct": round(100 * gb["seṭ"] / sum(gb.values()), 1) if gb else None,
        "_source": "TolchelnikovTalmud_2026/data/talmud_appendix1.json (Приложение 1, manual "
                   "2.1.6) — ryad (Табл. 4) × set (Табл. 8), open roots only",
    }


def class_shares():
    """OCH-2 / OCH-6: present-stem class token shares. Class 1+6 share the bare-a suffix,
    class 4 the ya suffix, class 10 the aya suffix (Whitney's traditional class numbering)."""
    d = json.load(open(VDCS / "verb_classes.json", encoding="utf-8"))
    tot = sum(v["total"] for v in d.values())
    a_suffix = d["1"]["total"] + d["6"]["total"]
    ya_suffix = d["4"]["total"]
    aya_suffix = d["10"]["total"]
    ranked = sorted(((k, v["total"]) for k, v in d.items()), key=lambda x: -x[1])
    return {
        "total_present_tokens": tot,
        "class_1_tokens": d["1"]["total"],
        "class_1_pct": round(100 * d["1"]["total"] / tot, 2),
        "class_2_tokens": d["2"]["total"],
        "class_2_pct": round(100 * d["2"]["total"] / tot, 2),
        "largest_class": ranked[0][0],
        "a_suffix_tokens": a_suffix, "a_suffix_pct": round(100 * a_suffix / tot, 2),
        "ya_suffix_tokens": ya_suffix, "ya_suffix_pct": round(100 * ya_suffix / tot, 2),
        "aya_suffix_tokens": aya_suffix, "aya_suffix_pct": round(100 * aya_suffix / tot, 2),
        "ya_aya_gap_pct_points": round(100 * ya_suffix / tot - 100 * aya_suffix / tot, 2),
    }


def analyze():
    return {
        "_source": "DCS-2021 (Oliver Hellwig, CC BY) via VisualDCS + Talmud Приложение 1",
        "_note": "OCH-1/OCH-3/OCH-5 reuse Kochergina/Bühler's already-published stats verbatim "
                 "(see claims.yml refs) rather than recomputing here.",
        "OCH2_OCH6_class_shares": class_shares(),
        # --- H797 backlog-drain metrics (15-07-2026) ---
        "OCH_final_consonant_census": final_consonant_census(),
        "OCH_sah_so_sa": sah_so_sa(),
        "OCH_vet_i_rates": vet_i_rates(),
        "OCH_rare_moods": rare_moods(),
        "OCH68_talmud_set_by_series": talmud_set_by_series(),
    }


def report(s):
    c = s["OCH2_OCH6_class_shares"]
    print(f"OCH-2 CLASS I SHARE: {c['class_1_tokens']:,} tokens = {c['class_1_pct']}% of "
          f"{c['total_present_tokens']:,} present-system tokens (largest class: {c['largest_class']}, "
          f"next-largest class II = {c['class_2_pct']}%)")
    print(f"OCH-6 THEMATIC-SUFFIX RANKING: a-suffix (I+VI) {c['a_suffix_pct']}% > "
          f"ya-suffix (IV) {c['ya_suffix_pct']}% > aya-suffix (X) {c['aya_suffix_pct']}% "
          f"(ya/aya gap only {c['ya_aya_gap_pct_points']} points)")

    print("\n--- H797 backlog-drain metrics ---")
    fc = s["OCH_final_consonant_census"]
    print(f"FINAL-CONSONANT CENSUS ({fc['n_word_tokens']:,} word tokens): "
          f"final l {fc['final_counts']['l']:,} ({fc['final_pct_of_words']['l']}%), "
          f"ṇ {fc['final_counts']['ṇ']:,}, ṅ {fc['final_counts']['ṅ']:,}, ñ {fc['final_counts']['ñ']:,} "
          f"vs n {fc['final_counts']['n']:,} / m {fc['final_counts']['m']:,} / ṁ {fc['final_counts']['ṁ']:,}")
    print(f"  final-stop ranking: {fc['stop_ranking_ktTp']}")
    ss = s["OCH_sah_so_sa"]
    print(f"saḥ/so/sa SURFACE: {ss['counts']} → so+sa = {ss['so_sa_share_pct']}%")
    vr = s["OCH_vet_i_rates"]
    print("i-RATES BY SUFFIX (distinct forms): " + ", ".join(
        f"{k.replace('before_','')}: {v['i_rate_pct']}%" for k, v in vr.items()))
    rm = s["OCH_rare_moods"]
    print(f"RARE MOODS: benedictive-med {rm['benedictive_medium']} + injunctive {rm['injunctive']:,} "
          f"+ conditional {rm['conditional']} = {rm['rare_three_pct_of_verbal']}% of verbal "
          f"(vs optative {rm['optative_active']:,}, imperative {rm['imperative_active']:,})")
    ts = s["OCH68_talmud_set_by_series"]
    if ts:
        print(f"§68 SET×SERIES (Talmud, {ts['open_roots_with_ryad_and_set']} open roots): "
              f"groupA {ts['groupA_series_I1_U1_R1_M1_N1_I2']} → aniṭ {ts['groupA_anit_share_pct']}%; "
              f"groupB {ts['groupB_other_series']} → seṭ {ts['groupB_set_share_pct']}%")


def main():
    stats = analyze()
    report(stats)
    if "--check" not in sys.argv:
        out = HERE / "claims_dcs_stats.json"
        out.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n-> wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
