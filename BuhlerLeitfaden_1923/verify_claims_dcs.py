#!/usr/bin/env python
"""verify_claims_dcs.py — reproducible corpus statistics behind the Bühler
claim register (H797 Phase 2 — pipeline ported from KocherginaUchebnik_1998).

Reads the committed DCS-2021 relational export in the sibling VisualDCS repo and
emits the numbers that back the `verdict_fact` fields in `claims.yml`. Same method
and ground truth as KocherginaUchebnik_1998/verify_claims_dcs.py (H768); see that
file's docstring for the DCS CSV column conventions this reuses verbatim.

Ground-truth source: Digital Corpus of Sanskrit (Oliver Hellwig, DCS-2021, CC BY),
    ../../VisualDCS/src/DCS-data-2021/
        15.csv  finite verb forms   : id,word_id,'form',tense_code,pn_code,...
        12.csv  non-finite forms    : id,word_id,'form','stem',cat_code,code2,...
    ../../VisualDCS/tense_case_data.json  (tense/mood + case token distributions)

Usage:  python verify_claims_dcs.py            # report + rewrite claims_dcs_stats.json
        python verify_claims_dcs.py --check     # report only, no file write
"""
import sys, json
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
VDCS = REPO.parent / "VisualDCS"
DCS = VDCS / "src" / "DCS-data-2021"


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


def imperative_person_distribution():
    """BU-3 (Урок XIV): 'второе и третье лицо императива большей частью выражают
    приказание' — distinct-form person distribution over Imperative Active (tc==3),
    same method as Kochergina HK-17."""
    imp_pn = Counter()
    for ln in (DCS / "15.csv").read_text(encoding="utf-8").splitlines():
        p = ln.split(",")
        if len(p) <= 4:
            continue
        try:
            tc = int(p[3]); pn = int(p[4].strip().rstrip(";"))
        except ValueError:
            continue
        if tc == 3:
            imp_pn[{1: "1", 2: "2", 3: "3"}[((pn - 1) % 3) + 1]] += 1
    tot = sum(imp_pn.values())
    return {
        "distinct_forms_by_person": dict(imp_pn),
        "total": tot,
        "second_person_share_pct": round(100 * imp_pn["2"] / tot, 1),
    }


def ppp_suffix_split():
    """BU-4 (Урок XXVII): PPP 'посредством суффикса ta ... или (реже) na' — distinct
    -ta vs -na Past Passive Participle (code 19) forms, same method as Kochergina HK-29."""
    nonfin = list(_forms("12.csv", 4))
    ppp_forms = {f for f, c in nonfin if c == 19}
    ta = na = 0
    for f in ppp_forms:
        if f.endswith(("na", "ṇa")):
            na += 1
        elif f.endswith(("ta", "ṭa")):
            ta += 1
    return {
        "distinct_forms_total": len(ppp_forms), "distinct_ta": ta, "distinct_na": na,
        "na_share_pct": round(100 * na / (ta + na), 1),
    }


def tense_token_shares():
    """BU-1/BU-2: perfect vs imperfect vs aorist token frequency, from the timws.csv
    tense/mood token census (VisualDCS/tense_case_data.json 'tenses'). Exact-label match
    (not substring) — 'Imperfect Active' contains 'perfect' as a substring, so a naive
    substring match on 'Perfect' silently double-counts imperfect tokens as perfect."""
    d = json.load(open(VDCS / "tense_case_data.json", encoding="utf-8"))
    tenses = d["tenses"]
    total_verbal = d["total_verbal"]

    def sum_labels(*exact_labels):
        wanted = {l.lower() for l in exact_labels}
        return sum(t["n"] for t in tenses if t["label"].strip().lower() in wanted)

    perfect = sum_labels("Perfect")
    imperfect = sum_labels("Imperfect", "Imperfect Med.")
    aorist = sum_labels("Aorist Act.", "Aorist Med.")
    return {
        "total_verbal_tokens": total_verbal,
        "perfect_tokens": perfect, "perfect_pct": round(100 * perfect / total_verbal, 2),
        "imperfect_tokens": imperfect, "imperfect_pct": round(100 * imperfect / total_verbal, 2),
        "aorist_tokens": aorist, "aorist_pct": round(100 * aorist / total_verbal, 2),
    }


def analyze():
    return {
        "_source": "DCS-2021 (Oliver Hellwig, CC BY) via VisualDCS/src/DCS-data-2021",
        "_note": "types = distinct forms (15.csv/12.csv); tokens = running-text counts (timws.csv / tense_case_data.json)",
        "BU3_imperative_person": imperative_person_distribution(),
        "BU4_ppp_suffix": ppp_suffix_split(),
        "BU1_BU2_tense_shares": tense_token_shares(),
    }


def report(s):
    ip = s["BU3_imperative_person"]
    print(f"BU-3 IMPERATIVE PERSON DISTRIBUTION: {ip['distinct_forms_by_person']} "
          f"-> 2nd person {ip['second_person_share_pct']}% of {ip['total']:,} distinct forms")
    pp = s["BU4_ppp_suffix"]
    print(f"BU-4 PPP SUFFIX: -ta {pp['distinct_ta']:,} / -na {pp['distinct_na']:,} distinct forms "
          f"-> -na is {pp['na_share_pct']}%")
    t = s["BU1_BU2_tense_shares"]
    print(f"BU-1/BU-2 TENSE TOKEN SHARES (of {t['total_verbal_tokens']:,} verbal tokens): "
          f"perfect {t['perfect_tokens']:,} ({t['perfect_pct']}%), "
          f"imperfect {t['imperfect_tokens']:,} ({t['imperfect_pct']}%), "
          f"aorist {t['aorist_tokens']:,} ({t['aorist_pct']}%)")


def main():
    stats = analyze()
    report(stats)
    if "--check" not in sys.argv:
        out = HERE / "claims_dcs_stats.json"
        out.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n-> wrote {out.relative_to(REPO)}")


if __name__ == "__main__":
    main()
