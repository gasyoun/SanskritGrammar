#!/usr/bin/env python
"""unflagged_exceptions_probe.py — DCS-2021 probes behind dossier (ii)
UNFLAGGED_EXCEPTIONS_KOCHERGINA_2026.md (H7826).

Every candidate of the dossier carries a DCS-2021 number: either a distinct-form
(type) count from the verbal tables 15.csv/12.csv, or a running-text token count
from the 0.csv surface layer, or both. This script regenerates all of them in one
pass → unflagged_exceptions_stats.json.

Ground-truth source: Digital Corpus of Sanskrit (Oliver Hellwig, DCS-2021, CC BY),
located like verify_claims_dcs.py expects (VisualDCS sibling), overridable with
the DCS_2021_DIR environment variable for machines without the sibling clone.

Usage:  python unflagged_exceptions_probe.py            # report + write stats JSON
        python unflagged_exceptions_probe.py --check    # report only
"""
import sys, os, json, re
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent

CANDIDATES = [
    # env override first, then the sibling layouts used by verify_claims_dcs.py /
    # topic_order_frequency_kochergina.py (Mac hub has the real clone).
    Path(os.environ.get("DCS_2021_DIR", "")) if os.environ.get("DCS_2021_DIR") else None,
    REPO.parent / "VisualDCS" / "src" / "DCS-data-2021",
    Path.home() / "Documents" / "GitHub" / "VisualDCS" / "src" / "DCS-data-2021",
]
DCS = next((c for c in CANDIDATES if c and (c / "15.csv").exists()), None)
if DCS is None:
    raise SystemExit("DCS-2021 dir not found: set DCS_2021_DIR or clone VisualDCS sibling")

AOR = {10, 11, 12, 13}          # aorist codes (verify_claims_dcs.py convention)
PERF = {15}

# --- token probes on the 0.csv running-text surface (whole word, IAST) ---------
# id → [(label, regex)] ; regex applied to every whitespace-token of the surface
TOKEN_PROBES = {
    "HK174_kurvantī": [
        ("kurvantī (fem of athematic P. part.)", r"\bkurvantī"),
        ("kurvatī (weak-grade fem, Whitney §449i)", r"\bkurvatī"),
        ("gacchantī (I cls, strong — control)", r"\bgacchantī"),
        ("adatī (II cls weak — control)", r"\badatī"),
        ("bruvatī (control)", r"\bruvatī"),
    ],
    "Z10400_precative_stems": [
        ("pīyās- (pā 'пить')", r"\bpīyās"),
        ("pāyās- (pā 'защищать')", r"\bpāyās"),
        ("deyās- (dā)", r"\bdeyās"),
        ("stheyās- (sthā)", r"\bstheyās"),
    ],
    "Z9440_frequentative": [
        ("cañcurya- (car)", r"\bcañcur"),
        ("dandahya- (dah)", r"\bdandah"),
        ("panīpatya- (pat)", r"\bpanīpat"),
        ("panīpadya- (pad)", r"\bpanīpad"),
    ],
    "Z9345_adhijigāṃsa": [("adhijigāṃsa- (adhī)", r"jigāṃs")],
    "Z9351_Z9390_desiderative": [
        ("vivṛtsa-/vivartiṣa- (vart)", r"\bvivṛts|\bvivartiṣ"),
        ("pipṛchiṣa- (prach)", r"\bpipṛchiṣ"),
        ("sismayiṣa- (smi)", r"\bsismayiṣ"),
        ("jijñāsa- (jñā)", r"\bjijñās"),
        ("didṛkṣa- (darś)", r"\bdidṛkṣ"),
        ("śuśrūṣa- (śru)", r"\bśuśrūṣ"),
        ("susmūrṣa- (smar)", r"\bsusmūrṣ"),
        ("mumūrṣa- (mar)", r"\bmumūrṣ"),
    ],
    "Z9065_causative_paya": [
        ("pāyáya- (pā 'пить')", r"\bpāyay"),
        ("hvāyáya- (hvā)", r"hvāyay"),
        ("gāpáya- (gai — control)", r"\bgāpay"),
        ("arpáya- (ar — control)", r"\barpay"),
    ],
    "HK131_jāyate": [
        ("jāyat- (jan, '2nd passive stem')", r"\bjāyat"),
        ("jany- finite (jan passive)", r"\bjany"),
    ],
    "Z9659_aorist_II_tokens": [
        ("avocat (vac, aorist II — raw token)", r"\bavocat\b"),
        ("akhyat (khyā, aorist II — raw token)", r"\bakhyat\b"),
        ("asthat (as, aorist II — raw token)", r"\basthat\b"),
        ("apaptat (pat, aorist II — raw token)", r"\bapaptat\b"),
    ],
    "HK16_controls": [
        ("sakhā (m. nom.sg classical — control)", r"\bsakhā\b"),
        ("rathin- (m. 'возница' — control)", r"\brathin"),
    ],
    "HK35_controls": [
        ("makṣikā/makṣī (dvandva member)", r"\bmakṣ[iī]k"),
        ("yūkā (dvandva member)", r"\byūkā"),
    ],
    "Z5829_passive_div_sas": [
        ("dīvy- pass./denom. (div)", r"\bdīvy"),
        ("śiṣy- (śās)", r"\bśiṣy"),
    ],
    "Z2626_jeya": [("jeya- (gerundive of ji, e unchanged)", r"\bjeya")],
    "Z4952_jaghana": [
        ("jaghāna-/jaghn- perfect of han", r"\bjaghān|\bjaghm"),
    ],
    "HK35_triple_dvandva": [
        ("yūkāmakṣīkamatkuṇa- (Whitney §1253.2d n.sg.)", r"yūkāmakṣīkamatkuṇ"),
    ],
    "HK16_masc_ii_uu": [
        ("rathī (m. nom.sg)", r"\brathī\b"),
        ("senānī (m. nom.sg)", r"\bsenānī\b"),
        ("sakhī (m. nom.sg)", r"\bsakhī\b"),
        ("ahī (m. nom.sg)", r"\bahī\b"),
        ("sudhī (m. nom.sg)", r"\bsudhī\b"),
        ("prāçū/prāśū (m.)", r"\bprā[sçś]ū\b"),
    ],
    "HK14_masc_aa": [
        ("pathā/paṅthāḥ (nom.sg of panthās)", r"\bpa[nṅ]thā[ḥs]?\b|\bpathā\b"),
        ("mahā (m., Whitney §355a)", r"\bmahā\b"),
        ("gopā (m., Whitney §355a)", r"\bgopā\b"),
    ],
    "HK31_two_consonant_final": [
        ("ūrk (f. 'Wolle/force', final -rk)", r"\būrk\b"),
        ("vārk/várk-", r"\bvārk\b"),
        ("suhārt (§150b)", r"\bsuhārt\b"),
    ],
    "HK234_maha_prior": [
        ("tokens starting mahā- (prior member)", r"\bmahā\S*"),
        ("standalone mahā (independent word)", r"\bmahā\b"),
    ],
    "HK108_future_no_guṇa": [
        ("jīviṣy- (jīv, no guṇa)", r"\bjīviṣy"),
        ("ukṣiṣy- (uṣ, no guṇa)", r"\bukṣiṣy|\baukṣiṣy"),
        ("likhiṣy- (likh, no guṇa)", r"\blikhiṣy"),
        ("lekhiṣy- (guṇa control)", r"\blekhiṣy"),
    ],
    "HK4a_bhaviṣya": [("bhaviṣy- (bhū, iṣya against unified -sya)", r"\bbhaviṣy")],
    "HK105_ayus_3pl": [
        ("āyus (3pl impf. of yā, §621a)", r"\bāyus\b"),
        ("vāyus (3pl impf. of vā, §621a)", r"\bvāyus\b"),
    ],
    "HK112_kinship_vrddhi": [
        ("naptā (guṇa, 'most' kinship)", r"\bnaptā\b"),
        ("nāptā (vṛddhi variant)", r"\bnāptā\b"),
        ("svasṛ (guṇa)", r"\bsvasṛ\b"),
        ("svāsr-/svāsṛ (vṛddhi)", r"\bsvāsṛ"),
    ],
}

# --- verb-table probes (distinct forms with tense/category codes) -------------
# id → [(label, regex, {"file": "15"|"12", "codes": set|None})]
FORM_PROBES = {
    "HK174_kurvantī": [
        ("15.csv distinct kurvantī*", r"kurvantī", {"file": "15", "codes": None}),
        ("15.csv distinct kurvatī*", r"kurvatī", {"file": "15", "codes": None}),
    ],
    "Z10009_adiṣ_asthiṣ": [
        ("15.csv adiṣ* aorist codes", r"^adiṣ", {"file": "15", "codes": AOR}),
        ("15.csv asthiṣ* aorist codes", r"^asthiṣ", {"file": "15", "codes": AOR}),
    ],
    "Z9659_aorist_II_stems": [
        ("akhy- aorist (khyā)", r"^akhy", {"file": "15", "codes": AOR}),
        ("apapt- aorist (pat)", r"^apapt", {"file": "15", "codes": AOR}),
        ("avoc- aorist (vac)", r"^avoc", {"file": "15", "codes": AOR}),
        ("asth- aorist (as)", r"^asth", {"file": "15", "codes": AOR}),
    ],
    "Z4952_jaghana": [
        ("jaghān/jaghn- perfect", r"^jagh", {"file": "15", "codes": PERF}),
    ],
    "Z5829_passive_div_sas": [
        ("dīvy- finite (div)", r"^dīvy", {"file": "15", "codes": None}),
        ("śiṣy- finite (śās)", r"^śiṣy", {"file": "15", "codes": None}),
    ],
    "Z10400_precative_stems": [
        ("precative-coded pīyās/pāyās/deyās/stheyās", r"^(pīyās|pāyās|deyās|stheyās)", {"file": "15", "codes": {14}}),
    ],
    "Z9065_causative_paya": [
        ("15.csv pāyay* (caus. of pā)", r"pāyay", {"file": "15", "codes": None}),
        ("15.csv hvāyay* (caus. of hvā)", r"hvāyay", {"file": "15", "codes": None}),
    ],
}


def load_forms(fn, code_idx, form_idx=2):
    out = []
    for ln in (DCS / fn).read_text(encoding="utf-8").splitlines():
        p = ln.split(",")
        if len(p) <= code_idx:
            continue
        try:
            code = int(p[code_idx])
        except ValueError:
            continue
        out.append((p[form_idx].strip().strip("'"), code))
    return out


def main():
    write = "--check" not in sys.argv
    finite = load_forms("15.csv", 3)
    nonfin = load_forms("12.csv", 4)
    tables = {"15": finite, "12": nonfin}

    stats = {
        "_source": "DCS-2021 (Oliver Hellwig, CC BY) via VisualDCS/src/DCS-data-2021",
        "_dcs_dir": str(DCS),
        "_note": "token counts = 0.csv running-text surface (IAST); "
                 "distinct = 15.csv/12.csv type tables (codes: 10-13 aorist, 15 perfect, 14 precative)",
        "tokens": {},
        "distinct_forms": {},
        "vowel_rare": {},
    }

    # --- one pass over 0.csv surface tokens ---
    compiled = {cid: [(lbl, re.compile(rx)) for lbl, rx in probes]
                for cid, probes in TOKEN_PROBES.items()}
    counts = {cid: Counter() for cid in TOKEN_PROBES}
    rare_vowels = Counter()
    n_tokens = 0
    with open(DCS / "0.csv", encoding="utf-8") as f:
        import unicodedata
        for ln in f:
            i = ln.rfind(";")
            if i < 0:
                continue
            toks = unicodedata.normalize("NFC", ln[i + 1:]).split()
            n_tokens += len(toks)
            for t in toks:
                if "ḷ" in t:
                    rare_vowels["ḷ"] += t.count("ḷ")
                if "ḹ" in t:
                    rare_vowels["ḹ"] += t.count("ḹ")
                for cid, probes in compiled.items():
                    for lbl, rx in probes:
                        if rx.search(t):
                            counts[cid][lbl] += 1
    stats["tokens"]["_corpus_tokens_total"] = n_tokens
    for cid, ctr in counts.items():
        stats["tokens"][cid] = dict(ctr)
    stats["vowel_rare"] = {"ḷ": rare_vowels["ḷ"], "ḹ": rare_vowels["ḹ"]}

    # --- distinct-form probes on the verb tables ---
    for cid, probes in FORM_PROBES.items():
        stats["distinct_forms"][cid] = {}
        for lbl, rx, how in probes:
            rx = re.compile(rx)
            tbl = tables[how["file"]]
            codes = how.get("codes")
            hits = [f for f, c in tbl if rx.search(f) and (codes is None or c in codes)]
            stats["distinct_forms"][cid][lbl] = {
                "n": len(hits), "examples": sorted(set(hits))[:8],
            }

    # timws token totals for the categories the verdicts lean on
    tok, label = {}, {}
    for ln in (DCS / "timws.csv").read_text(encoding="utf-8").splitlines()[1:]:
        m = re.match(r"\s*(\d+):(.*):(\d+)\s*$", ln)
        if m:
            tok[int(m.group(1))] = int(m.group(3)); label[int(m.group(1))] = m.group(2).strip()
    stats["timws"] = {"precative": tok.get(14), "frequentative_note": "inside Present codes",
                      "aorist_total": sum(tok.get(c, 0) for c in AOR)}

    if write:
        (HERE / "unflagged_exceptions_stats.json").write_text(
            json.dumps(stats, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"DCS dir: {DCS}")
    print(f"corpus surface tokens: {n_tokens:,}; rare vowels: {dict(rare_vowels)}\n")
    for cid in stats["tokens"]:
        if cid.startswith("_"):
            continue
        print(f"[tokens] {cid}")
        for lbl, n in stats["tokens"][cid].items():
            print(f"   {n:6,}  {lbl}")
    for cid, rows in stats["distinct_forms"].items():
        print(f"[distinct] {cid}")
        for lbl, d in rows.items():
            print(f"   {d['n']:6,}  {lbl}   ex: {', '.join(d['examples'][:5])}")
    print(f"\ntimws: precative tokens={stats['timws']['precative']}, aorist total={stats['timws']['aorist_total']}")


if __name__ == "__main__":
    main()
