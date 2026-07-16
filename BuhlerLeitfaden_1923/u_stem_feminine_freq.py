#!/usr/bin/env python
"""u_stem_feminine_freq.py — feminine-form frequency check for §XII.3б (HB-21).

Bühler §XII.3б: u-stem adjectives whose final -u is preceded by a SINGLE
consonant may take the nadī-type -ī suffix (with v-glide) in the feminine
instead of simply reusing the u-stem form — guru -> gurvī, bahu -> bahvī
(his own two named examples) — and states these -vī forms are "более
употребительны" (more common) than the plain-u feminine.

PRIOR VERDICT ASSUMED this needs "adjective-gender-pairing... lemma+
gender+agreement joins the relational dump does not carry." Not checked:
DCS lemmatizes guru/bahu to ONE lemma across all genders (adjectives don't
get separate per-gender lemmas), so every feminine-tagged token of that
SAME lemma already carries feat_gender='Fem' — no join needed, just a
surface-FORM split on the already-tagged feminine tokens: does the form
start with the -v- glide (gurv-/bahv-, the nadī-type inflection) or with
the plain u-stem (guru-/gurū-/bahu-/bahū-/bahav-, same shape as masc/neut)?

Usage:  python BuhlerLeitfaden_1923/u_stem_feminine_freq.py [--db PATH]
Writes  hb21_u_stem_feminine_freq.json next to this script.
"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"

# Buhler's own two named examples (mdx line 1574); each stem's -v- glide prefix
LEMMAS = {"guru": "gurv", "bahu": "bahv"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    results = {}
    for lemma, vglide in LEMMAS.items():
        rows = cur.execute(
            "SELECT form, COUNT(*) c FROM token WHERE lemma=? AND feat_gender='Fem' "
            "GROUP BY form ORDER BY c DESC", (lemma,)
        ).fetchall()
        vi_forms, plain_forms = [], []
        vi_total = plain_total = other_total = 0
        for form, c in rows:
            if form.startswith(vglide):
                vi_total += c
                vi_forms.append((form, c))
            elif form.startswith(lemma[:-1]):  # stem minus final -u, e.g. "gur"/"bah"
                plain_total += c
                plain_forms.append((form, c))
            else:
                other_total += c
        total = vi_total + plain_total + other_total
        results[lemma] = {
            "vi_pattern_tokens": vi_total, "vi_forms_top": vi_forms[:8],
            "plain_u_pattern_tokens": plain_total, "plain_forms_top": plain_forms[:8],
            "other_unclassified_tokens": other_total,
            "total_feminine_tokens": total,
            "vi_share_pct": round(100 * vi_total / total, 1) if total else None,
            "confirmed": vi_total > plain_total,
        }

    out = {
        "instrument": "u_stem_feminine_freq.py over dcs_full.sqlite — surface-form split "
                      "of already feat_gender=Fem-tagged tokens of the same lemma, no "
                      "agreement join needed (the prior verdict's blocker didn't hold up)",
        "lemmas": results,
        "expected_by_hb21": "vi_pattern_tokens > plain_u_pattern_tokens for both lemmas",
        "confirmed": all(r["confirmed"] for r in results.values()),
    }
    (HERE / "hb21_u_stem_feminine_freq.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for lemma, r in results.items():
        print(f"{lemma}: -vī {r['vi_pattern_tokens']} vs plain-u {r['plain_u_pattern_tokens']} "
              f"(of {r['total_feminine_tokens']} fem tokens) -> {r['vi_share_pct']}% -vī, "
              f"confirmed={r['confirmed']}")
    print("overall confirmed:", out["confirmed"])
    print("-> hb21_u_stem_feminine_freq.json written")


if __name__ == "__main__":
    main()
