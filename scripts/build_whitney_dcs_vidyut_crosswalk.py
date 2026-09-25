"""Q4.4 -- Whitney-no <-> DCS lemma <-> Vidyut dhatu crosswalk.

Joins the existing 876-root Whitney crosswalk
(TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv) against
two already-derived assets, consumed as-is per the roadmap boundary
(Q4.4: "net-new derived asset; boundary: consume VisualDCS, never re-derive"):

- VisualDCS dcs_lemma_summary.json (corpus attestation + frequency band)
- kosha data/e1/dhatu_crosswalk.json (Cologne bare root -> vidyut-prakriya
  aupadesika dhatu + dhatupatha code, H855)

Neither source is regenerated here; only read and joined via IAST->SLP1
root transliteration (indic_transliteration).
"""
import csv
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

REPO_ROOT = Path(__file__).resolve().parent.parent
WHITNEY_CROSSWALK = REPO_ROOT / "TolchelnikovTalmud_2026" / "data" / "morphoclass_crosswalk_1975_2014_2026.csv"
KOSHA_DHATU_CROSSWALK = REPO_ROOT.parent / "kosha" / "data" / "e1" / "dhatu_crosswalk.json"
DCS_LEMMA_SUMMARY = REPO_ROOT.parent / "VisualDCS" / "dcs_lemma_summary.json"
OUT_CSV = REPO_ROOT / "data" / "whitney_dcs_vidyut_crosswalk.csv"
OUT_JSON = REPO_ROOT / "data" / "whitney_dcs_vidyut_crosswalk_summary.json"


def load_kosha_by_bare_root():
    data = json.loads(KOSHA_DHATU_CROSSWALK.read_text(encoding="utf-8"))
    by_bare = {}
    for key, entry in data["crosswalk"].items():
        _model, bare = key.split("|", 1)
        by_bare.setdefault(bare, []).append(entry)
    return by_bare, data.get("vidyut_version", "unknown")


def load_dcs_lemmas():
    data = json.loads(DCS_LEMMA_SUMMARY.read_text(encoding="utf-8"))
    return data["lemmas"], data.get("corpusRelease", "unknown")


def main():
    kosha_by_bare, vidyut_version = load_kosha_by_bare_root()
    dcs_lemmas, dcs_release = load_dcs_lemmas()

    rows = list(csv.DictReader(WHITNEY_CROSSWALK.open(encoding="utf-8")))

    out_rows = []
    n_dcs_attested = 0
    n_vidyut_matched = 0
    n_vidyut_ambiguous = 0

    for r in rows:
        whitney_no = r["whitney_no"]
        root_iast = r["root"]
        root_slp1 = transliterate(root_iast, sanscript.IAST, sanscript.SLP1)

        dcs_entry = dcs_lemmas.get(root_slp1)
        dcs_attested = bool(dcs_entry and dcs_entry.get("attested"))
        dcs_freq_band = dcs_entry.get("freqBand") if dcs_entry else None
        if dcs_attested:
            n_dcs_attested += 1

        vidyut_matches = kosha_by_bare.get(root_slp1, [])
        vidyut_aupadeshika = ";".join(sorted({m["aupadeshika"] for m in vidyut_matches}))
        vidyut_codes = ";".join(sorted({m["code"] for m in vidyut_matches if m.get("code")}))
        vidyut_ambiguous = len({m["aupadeshika"] for m in vidyut_matches}) > 1
        if vidyut_matches:
            n_vidyut_matched += 1
        if vidyut_ambiguous:
            n_vidyut_ambiguous += 1

        out_rows.append({
            "whitney_no": whitney_no,
            "root_iast": root_iast,
            "root_slp1": root_slp1,
            "homonym": r.get("homonym", ""),
            "gloss": r.get("gloss", ""),
            "dcs_lemma_attested": dcs_attested,
            "dcs_freq_band": dcs_freq_band if dcs_freq_band is not None else "",
            "vidyut_aupadeshika": vidyut_aupadeshika,
            "vidyut_dhatupatha_code": vidyut_codes,
            "vidyut_match_count": len(vidyut_matches),
            "vidyut_ambiguous": vidyut_ambiguous,
        })

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(out_rows[0].keys()))
        writer.writeheader()
        writer.writerows(out_rows)

    summary = {
        "_about": (
            "Q4.4 crosswalk: Whitney root number <-> DCS corpus lemma attestation "
            "<-> vidyut-prakriya dhatupatha code. Joins two already-derived assets "
            "(VisualDCS dcs_lemma_summary.json, kosha data/e1/dhatu_crosswalk.json) "
            "via IAST->SLP1 root transliteration; neither source is re-derived."
        ),
        "generated_by": "scripts/build_whitney_dcs_vidyut_crosswalk.py",
        "sources": {
            "whitney_root_crosswalk": str(WHITNEY_CROSSWALK.relative_to(REPO_ROOT)).replace("\\", "/"),
            "dcs_lemma_summary": "VisualDCS/dcs_lemma_summary.json",
            "dcs_corpus_release": dcs_release,
            "kosha_dhatu_crosswalk": "kosha/data/e1/dhatu_crosswalk.json",
            "vidyut_version": vidyut_version,
        },
        "row_count": len(out_rows),
        "dcs_attested_count": n_dcs_attested,
        "dcs_attested_pct": round(100 * n_dcs_attested / len(out_rows), 2),
        "vidyut_matched_count": n_vidyut_matched,
        "vidyut_matched_pct": round(100 * n_vidyut_matched / len(out_rows), 2),
        "vidyut_ambiguous_count": n_vidyut_ambiguous,
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"wrote {OUT_CSV} ({len(out_rows)} rows)")
    print(f"wrote {OUT_JSON}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
