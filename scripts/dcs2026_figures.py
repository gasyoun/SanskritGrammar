#!/usr/bin/env python
"""dcs2026_figures.py — the single authoritative table of DCS-2026 corpus figures used across
the claim registers (H-standardize-2026).

MG ruled 17-07-2026 to standardize the whole claim programme on DCS-2026 (the current sqlite),
replacing the DCS-2021 vintage numbers that had been the shared basis. This script computes every
figure the registers cite, from ONE source (dcs_full.sqlite), so all six registers can cite the
same values. It prints the OLD (DCS-2021) -> NEW (DCS-2026) mapping and writes dcs2026_figures.json.

Denominator convention (fixed here for the whole programme): FINITE VERBAL FORMS =
upos='VERB' AND feat_verbform IS NULL (mood/tense-bearing finite verbs). Percentages are of that.

Category identification in the 2026 sqlite:
  present     feat_tense='Pres'                     imperfect  feat_tense='Impf'
  aorist      feat_tense='Past' + feat_formation in {root,them,s,is,red,sa,sis}  (H1134)
  perfect     feat_tense='Past' and NOT aorist  (= reduplicated 'None' + periphrastic 'peri')
  future      feat_tense='Fut'                      pluperfect feat_tense in ('Plp','Pqp')
  optative    feat_mood='Opt'    imperative feat_mood='Imp'   conditional feat_mood='Cond'
  precative   feat_mood='Prec'   injunctive feat_mood='Jus'   subjunctive feat_mood='Sub'
"""
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
AOR = ("root", "them", "s", "is", "red", "sa", "sis")
FIN = "upos='VERB' AND feat_verbform IS NULL"

# DCS-2021 figures the registers currently cite, for the OLD->NEW mapping
OLD_2021 = {
    "present": 157003, "imperfect": 47554, "perfect": 61986, "aorist_old": 2452,
    "future": 18004, "optative": 72826, "imperative": 32750, "injunctive": 2366,
    "periphrastic_future": 1290, "conditional": 269, "precative": 221,
    "finite_verbal_denominator": 781618,
}


def main():
    db = sqlite3.connect(str(DB))
    c = db.cursor()

    def n(w):
        return c.execute(f"SELECT COUNT(*) FROM token WHERE {w}").fetchone()[0]

    aor_in = ",".join("'%s'" % f for f in AOR)
    denom = n(FIN)
    fig = {
        "present":     n(f"{FIN} AND feat_tense='Pres'"),
        "imperfect":   n(f"{FIN} AND feat_tense='Impf'"),
        "aorist":      n(f"{FIN} AND feat_tense='Past' AND feat_formation IN ({aor_in})"),
        "future":      n(f"{FIN} AND feat_tense='Fut'"),
        "pluperfect":  n(f"{FIN} AND feat_tense IN ('Plp','Pqp')"),
        "optative":    n(f"{FIN} AND feat_mood='Opt'"),
        "imperative":  n(f"{FIN} AND feat_mood='Imp'"),
        "conditional": n(f"{FIN} AND feat_mood='Cond'"),
        "precative":   n(f"{FIN} AND feat_mood='Prec'"),
        "injunctive":  n(f"{FIN} AND feat_mood='Jus'"),
        "subjunctive": n(f"{FIN} AND feat_mood='Sub'"),
    }
    # perfect = Past-finite minus aorist (reduplicated 'None' + periphrastic 'peri')
    past = n(f"{FIN} AND feat_tense='Past'")
    fig["perfect"] = past - fig["aorist"]
    fig["periphrastic_perfect"] = n(f"{FIN} AND feat_tense='Past' AND feat_formation='peri'")
    # periphrastic future is not separately tagged in the sqlite tense set — flag it
    fig["finite_verbal_denominator"] = denom

    out = {"_source": "DCS-2026 dcs_full.sqlite; denominator = finite verbal forms (%d)" % denom,
           "denominator": denom, "figures": fig,
           "pct_of_finite_verbal": {k: round(100 * v / denom, 2) for k, v in fig.items()
                                    if k != "finite_verbal_denominator"}}
    (HERE / "dcs2026_figures.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"finite verbal denominator (2026): {denom}  (2021 was {OLD_2021['finite_verbal_denominator']})")
    print(f"{'category':22} {'2021':>9} {'2026':>9}  {'2026 %':>7}")
    order = ["present", "imperfect", "perfect", "aorist", "future", "optative", "imperative",
             "injunctive", "subjunctive", "conditional", "precative", "pluperfect"]
    for k in order:
        old = OLD_2021.get(k, OLD_2021.get(k + "_old", "—"))
        pct = out["pct_of_finite_verbal"][k]
        print(f"{k:22} {str(old):>9} {fig[k]:>9}  {pct:>6}%")
    print(f"{'(periphrastic perfect)':22} {'—':>9} {fig['periphrastic_perfect']:>9}")
    print("NOTE: periphrastic FUTURE (2021: 1,290) has no distinct tense tag in the 2026 sqlite — "
          "flag per-claim, do not silently drop.")
    print("-> dcs2026_figures.json written")


if __name__ == "__main__":
    main()
