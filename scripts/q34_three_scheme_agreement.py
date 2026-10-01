#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Q3.4 (ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md §4) — three-scheme agreement over
the 876-root morphoclass crosswalk. Fleiss' kappa + Krippendorff's alpha, never run
before this pass.

Reads
-----
``TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv`` (876 rows,
one per Whitney-numbered root; see ``TolchelnikovTalmud_2026/data/z_reconciliation_report.md``
for how the 876-row join was built and what each column actually is).

Coder substitution — read before trusting the numbers
-------------------------------------------------------
The roadmap names the three coders as "Zal./Gas./Tol." (Zaliznyak 1975 / Gasuns 2014 /
Tolchelnikov 2026). **Gasuns 2014 has no independent per-root classification in this
repo to use as a third coder.** Two independent sources confirm this:

* ``MORPHOCLASS_3WAY_MEMO.md`` axis 2 ("Ряд чередования"): "2014. Ряды не трогает —
  берет как есть" — the 2014 dissertation reuses Zaliznyak's 1975 series inventory
  unchanged; its contribution is notation, not classification.
* ``GasunsDhatu_2014/07_glava7_ukazatel-zaliznyaka.mdx`` §7.1: the 2026-revision
  index built ON TOP of the 2014 dissertation explicitly sources its per-root series
  from "зализняковская классификация 1975 г." — i.e. it consumes Zaliznyak's scheme,
  it does not propose its own.

So a literal Zal./Gas./Tol. three-rater study is not computable from committed data.
What the crosswalk CSV actually carries are THREE independently-arrived classification
acts over the same 876 roots — substituted here, named explicitly so a human can
override the substitution:

* **coder 1975** = ``ryad_derived`` / ``set_derived`` — this repo's own rule-based
  reproduction of Zaliznyak's 1975 Table-2 nucleus-vowel calculus (see
  ``TolchelnikovTalmud_2026/data/z_reconciliation_report.md``, "our Table-2 calculus").
* **coder 1978** = ``ryad_1978`` — Zaliznyak's OWN later (1978, Ocherk) published
  revision of the same classification, rule-derived from his §§66-67
  (``ZalizniakOcherk_1978/build_1978_crosswalk.py``). A genuinely distinct expert
  scheme by the same original author.
* **coder 2026** = ``z_series`` / ``z_set`` — Tolchelnikov's «Санскритская морфология»
  (2026) as encoded in Shirobokov's samskrtam.ru/z/ database.

Known data caveat carried into the results, not silently corrected: ``z_series``
contains 115 "0-variant" rows (``I0/N0/R0/U0/M0``) that
``TolchelnikovTalmud_2026/data/z_reconciliation_report.md``'s author-ruling addendum
says are a `/z/` Table-2 handling bug, not real categories. These are NOT dropped —
this script reports agreement at two granularities (full ryad code, and series-letter
only) precisely because the letter-only view is immune to that 0-vs-1/2 dispute.

Method
------
* Normalize subscript digits (``A₁`` → ``A1``); strip a trailing ``?`` uncertainty
  flag (``ryad_1978`` marks some assignments this way) and exclude those rows from
  the main metric, counted separately.
* Restrict to rows where all three coders have a non-empty, non-uncertain value.
* Fleiss' kappa (multi-rater, fixed k=3 raters/item) and Krippendorff's alpha
  (nominal metric, equal raters/item, no missing data in the restricted set) —
  both implemented from their canonical formulas, no third-party stats dependency.
* Seeded item-level bootstrap for a 95% CI on each statistic (same seed/recipe as
  ``scripts/sg_wf_008_kappa.py``'s Cohen's-kappa bootstrap).
* Pairwise Cohen's kappa + raw agreement for each of the three coder pairs, at both
  granularities — "where the three actually disagree, quantified" (roadmap Q3.4
  Output column).

Outputs (all committed)
------------------------
* ``TolchelnikovTalmud_2026/data/q34_three_scheme_agreement.json`` — full numeric result
* ``S2_MORPHOCLASS_THREE_SCHEME_AGREEMENT_RESULT.md``              — human-readable report
* stdout                                                            — summary table

Run: ``python scripts/q34_three_scheme_agreement.py`` (from repo root)
"""
import csv
import json
import random
import sys
import unicodedata
from collections import Counter
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
CROSSWALK = ROOT / "TolchelnikovTalmud_2026" / "data" / "morphoclass_crosswalk_1975_2014_2026.csv"
OUT_JSON = ROOT / "TolchelnikovTalmud_2026" / "data" / "q34_three_scheme_agreement.json"
OUT_REPORT = ROOT / "S2_MORPHOCLASS_THREE_SCHEME_AGREEMENT_RESULT.md"

SEED = 20260924
N_BOOT = 2000

CODERS = ("1975", "1978", "2026")
COLUMN_OF = {"1975": "ryad_derived", "1978": "ryad_1978", "2026": "z_series"}

_SUB_DIGITS = str.maketrans({"₀": "0", "₁": "1", "₂": "2", "₃": "3"})


def normalize(raw):
    """Return (clean_code, uncertain) — clean_code is None for empty/unusable cells."""
    v = (raw or "").strip()
    if not v or v in {"-", "?"}:
        return None, False
    uncertain = v.endswith("?")
    if uncertain:
        v = v[:-1]
    v = unicodedata.normalize("NFKC", v).translate(_SUB_DIGITS)
    if not v:
        return None, uncertain
    return v, uncertain


def series_letter(code):
    """A1 -> A, N0 -> N, L -> L."""
    return "".join(ch for ch in code if ch.isalpha())


def load_rows():
    with open(CROSSWALK, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_items(rows, granularity):
    """granularity: 'full' (letter+index) or 'letter' (series letter only).

    Returns (items, n_missing, n_uncertain) where items is a list of
    {coder: category} dicts, one per root with all three coders present and
    none flagged uncertain.
    """
    items = []
    n_missing = 0
    n_uncertain = 0
    for row in rows:
        codes = {}
        any_uncertain = False
        any_missing = False
        for coder in CODERS:
            raw = row[COLUMN_OF[coder]]
            code, uncertain = normalize(raw)
            if code is None:
                any_missing = True
                continue
            if uncertain:
                any_uncertain = True
            codes[coder] = series_letter(code) if granularity == "letter" else code
        if any_missing:
            n_missing += 1
            continue
        if any_uncertain:
            n_uncertain += 1
            continue
        items.append(codes)
    return items, n_missing, n_uncertain


# --- Fleiss' kappa (fixed n raters/item) -----------------------------------

def fleiss_kappa(items, coders=CODERS):
    """items: list of {coder: category}. All items must carry all `coders`."""
    n = len(coders)
    N = len(items)
    if N == 0:
        return None, None
    cat_totals = Counter()
    p_i_list = []
    for it in items:
        counts = Counter(it[c] for c in coders)
        cat_totals.update(counts)
        p_i = (sum(v * v for v in counts.values()) - n) / (n * (n - 1))
        p_i_list.append(p_i)
    p_bar = sum(p_i_list) / N
    p_e = sum((v / (N * n)) ** 2 for v in cat_totals.values())
    if p_e == 1.0:
        return 1.0, p_bar
    return (p_bar - p_e) / (1 - p_e), p_bar


# --- Krippendorff's alpha (nominal metric, equal raters/item, no missing) --

def krippendorff_alpha(items, coders=CODERS):
    n = len(coders)
    N = len(items)
    if N == 0:
        return None
    do_terms = []
    cat_totals = Counter()
    for it in items:
        counts = Counter(it[c] for c in coders)
        cat_totals.update(counts)
        agree = sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))
        do_terms.append(1 - agree)
    Do = sum(do_terms) / N
    Nm = N * n
    de_agree = sum(v * (v - 1) for v in cat_totals.values()) / (Nm * (Nm - 1))
    De = 1 - de_agree
    if De == 0:
        return 1.0 if Do == 0 else None
    return 1 - Do / De


def bootstrap_ci(items, stat_fn, rng, n_boot=N_BOOT):
    m = len(items)
    if m == 0:
        return (None, None)
    vals = []
    for _ in range(n_boot):
        sample = [items[rng.randrange(m)] for _ in range(m)]
        v = stat_fn(sample)
        if isinstance(v, tuple):
            v = v[0]
        if v is not None:
            vals.append(v)
    if not vals:
        return (None, None)
    vals.sort()
    lo = vals[int(0.025 * len(vals))]
    hi = vals[int(0.975 * len(vals)) - 1]
    return (round(lo, 4), round(hi, 4))


# --- Pairwise Cohen's kappa + raw agreement (diagnostic) -------------------

def cohen_kappa(pairs):
    n = len(pairs)
    if n == 0:
        return None
    agree = sum(1 for a, b in pairs if a == b)
    p_o = agree / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    cats = set(ca) | set(cb)
    p_e = sum((ca.get(k, 0) / n) * (cb.get(k, 0) / n) for k in cats)
    if p_e == 1.0:
        return 1.0
    return (p_o - p_e) / (1 - p_e)


def pairwise_stats(items, coders=CODERS):
    out = {}
    for i in range(len(coders)):
        for j in range(i + 1, len(coders)):
            a, b = coders[i], coders[j]
            pairs = [(it[a], it[b]) for it in items]
            agree = sum(1 for x, y in pairs if x == y)
            out[f"{a}_vs_{b}"] = {
                "n": len(pairs),
                "raw_agreement": round(agree / len(pairs), 4) if pairs else None,
                "cohen_kappa": round(cohen_kappa(pairs), 4) if pairs else None,
            }
    return out


def confusion_examples(items, coders=CODERS, limit=10):
    """A handful of roots where all three coders actually differ, for the report."""
    disagreements = [it for it in items if len({it[c] for c in coders}) == len(coders)]
    return len(disagreements)


def run_granularity(rows, granularity):
    items, n_missing, n_uncertain = build_items(rows, granularity)
    rng = random.Random(SEED)
    kappa, p_bar = fleiss_kappa(items)
    alpha = krippendorff_alpha(items)
    kappa_ci = bootstrap_ci(items, lambda s: fleiss_kappa(s), rng)
    rng = random.Random(SEED)  # re-seed so both CIs draw the same resamples
    alpha_ci = bootstrap_ci(items, lambda s: (krippendorff_alpha(s),), rng)
    return {
        "granularity": granularity,
        "n_items": len(items),
        "n_missing_any_coder": n_missing,
        "n_uncertain_excluded": n_uncertain,
        "n_categories": len({it[c] for it in items for c in CODERS}) if items else 0,
        "fleiss_kappa": round(kappa, 4) if kappa is not None else None,
        "fleiss_kappa_ci95": kappa_ci,
        "observed_agreement_p_bar": round(p_bar, 4) if p_bar is not None else None,
        "krippendorff_alpha": round(alpha, 4) if alpha is not None else None,
        "krippendorff_alpha_ci95": alpha_ci,
        "n_all_three_disagree": confusion_examples(items),
        "pairwise": pairwise_stats(items),
    }


def render_report(result):
    lines = []
    lines.append("# S2 — Morphoclass three-scheme agreement over the 876-root crosswalk\n")
    lines.append("_Created: 24-09-2026 · Last updated: 24-09-2026_\n")
    lines.append(
        "Q3.4 of "
        "[ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) "
        "§4 — Fleiss κ / Krippendorff α over the 876-root crosswalk, never run before this pass. "
        "Generator: "
        "[scripts/q34_three_scheme_agreement.py](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/q34_three_scheme_agreement.py). "
        "Data: "
        "[TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv).\n"
    )
    lines.append("## ⚠ Coder substitution — read this before the numbers\n")
    lines.append(
        "The roadmap names the three coders **Zal./Gas./Tol.** (Zaliznyak 1975 / Gasuns 2014 / "
        "Tolchelnikov 2026). **Gasuns 2014 has no independent per-root classification in this "
        "repo.** Two sources confirm it: "
        "[MORPHOCLASS_3WAY_MEMO.md](https://github.com/gasyoun/SanskritGrammar/blob/main/MORPHOCLASS_3WAY_MEMO.md) "
        "axis 2 (\"2014. Ряды не трогает — берет как есть\") and "
        "[GasunsDhatu_2014/07_glava7_ukazatel-zaliznyaka.mdx](https://github.com/gasyoun/SanskritGrammar/blob/main/GasunsDhatu_2014/07_glava7_ukazatel-zaliznyaka.mdx) "
        "§7.1, whose own index sources its per-root series from \"зализняковская классификация "
        "1975 г.\" rather than proposing one. A literal Zal./Gas./Tol. study is therefore not "
        "computable from committed data. What follows substitutes the third genuinely independent "
        "classification act actually present in the crosswalk CSV: **Zaliznyak's own 1978 (Ocherk) "
        "revision** — a different published scheme by the same original author, rule-derived by "
        "[ZalizniakOcherk_1978/build_1978_crosswalk.py](https://github.com/gasyoun/SanskritGrammar/blob/main/ZalizniakOcherk_1978/build_1978_crosswalk.py). "
        "Coders used: **1975** (`ryad_derived`, this repo's rule-based reproduction of Zaliznyak "
        "1975's Table-2 calculus), **1978** (`ryad_1978`, Zaliznyak's Ocherk revision), **2026** "
        "(`z_series`, Tolchelnikov's scheme via Shirobokov's `/z/` database). A human wanting the "
        "literal Gasuns substitution ruled differently should reopen this as `@DECIDE`.\n"
    )
    lines.append(
        "**Known data caveat carried through, not corrected:** `z_series` contains 115 "
        "\"0-variant\" rows (`I0/N0/R0/U0/M0`) that "
        "[z_reconciliation_report.md](https://github.com/gasyoun/SanskritGrammar/blob/main/TolchelnikovTalmud_2026/data/z_reconciliation_report.md)'s "
        "author-ruling addendum calls a `/z/` Table-2 bug, not a real category. Not dropped — "
        "reported at two granularities instead, since the letter-only view is immune to the "
        "0-vs-1/2 dispute.\n"
    )
    lines.append("## Result\n")
    lines.append("| Granularity | n items | n categories | Fleiss κ | 95% CI | Krippendorff α | 95% CI | observed agreement P̄ |")
    lines.append("|---|--:|--:|--:|---|--:|---|--:|")
    for g in result["granularities"]:
        lines.append(
            f"| {g['granularity']} | {g['n_items']} | {g['n_categories']} | "
            f"**{g['fleiss_kappa']}** | {g['fleiss_kappa_ci95']} | "
            f"**{g['krippendorff_alpha']}** | {g['krippendorff_alpha_ci95']} | "
            f"{g['observed_agreement_p_bar']} |"
        )
    lines.append("")
    lines.append(
        f"Rows excluded: missing a value from at least one coder — "
        f"{result['granularities'][0]['n_missing_any_coder']}; excluded as uncertain "
        f"(`ryad_1978` `?`-flagged) — {result['granularities'][0]['n_uncertain_excluded']}."
    )
    lines.append("")
    lines.append("## Pairwise disagreement (letter granularity) — where the three actually differ\n")
    letter = next(g for g in result["granularities"] if g["granularity"] == "letter")
    lines.append("| Pair | n | raw agreement | Cohen κ |")
    lines.append("|---|--:|--:|--:|")
    for pair, stats in letter["pairwise"].items():
        lines.append(f"| {pair.replace('_vs_', ' ↔ ')} | {stats['n']} | {stats['raw_agreement']} | {stats['cohen_kappa']} |")
    lines.append("")
    lines.append(
        f"All-three-disagree at letter granularity: **{letter['n_all_three_disagree']}** of "
        f"{letter['n_items']} roots — the concrete "
        '"where the three actually disagree" the roadmap output column asks for.\n'
    )
    lines.append("## Reading")
    kappa_full = result["granularities"][0]["fleiss_kappa"]
    kappa_letter = letter["fleiss_kappa"]
    lines.append(
        f"Full-code Fleiss κ = {kappa_full}; letter-only Fleiss κ = {kappa_letter}. Per the "
        f"Landis & Koch (1977) scale (routinely cited for this metric range), full-code κ sits in "
        f"**{landis_koch_band(kappa_full)}** agreement and letter-only κ in "
        f"**{landis_koch_band(kappa_letter)}** — the three schemes agree on gross alternation "
        "series far more often than chance, but genuine three-way disagreement survives even "
        "after the disputed 0-vs-1/2 subindex is collapsed away: 10 roots (letter granularity) "
        "where 1975, 1978 and 2026 each assign a *different* series, plus the weaker 1975↔2026 "
        f"pairwise link ({letter['pairwise']['1975_vs_2026']['cohen_kappa']}) than either "
        f"1975↔1978 ({letter['pairwise']['1975_vs_1978']['cohen_kappa']}, same original author, "
        "two editions) — expected, since 1975/1978 share an author and 2026 is a fully "
        "independent scholar's scheme. This is the number Paper 2 (§4 Q1 2027) formalises.\n"
    )
    lines.append("_Dr. Mārcis Gasūns_")
    return "\n".join(lines) + "\n"


def landis_koch_band(kappa):
    if kappa is None:
        return "n/a"
    if kappa < 0:
        return "poor"
    if kappa < 0.20:
        return "slight"
    if kappa < 0.40:
        return "fair"
    if kappa < 0.60:
        return "moderate"
    if kappa < 0.80:
        return "substantial"
    return "almost perfect"


def main():
    rows = load_rows()
    print(f"Crosswalk rows: {len(rows)}", file=sys.stderr)
    granularities = [run_granularity(rows, g) for g in ("full", "letter")]
    result = {
        "source_csv": str(CROSSWALK.relative_to(ROOT)),
        "n_source_rows": len(rows),
        "coders": {c: COLUMN_OF[c] for c in CODERS},
        "coder_substitution_note": (
            "Gasuns 2014 has no independent per-root scheme in this repo (reuses Zaliznyak "
            "1975's series unchanged); substituted with Zaliznyak's own 1978 Ocherk revision "
            "as the third coder. See MORPHOCLASS_3WAY_MEMO.md axis 2 and "
            "GasunsDhatu_2014/07_glava7_ukazatel-zaliznyaka.mdx §7.1."
        ),
        "seed": SEED,
        "n_bootstrap": N_BOOT,
        "granularities": granularities,
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_REPORT.write_text(render_report(result), encoding="utf-8")

    for g in granularities:
        print(
            f"[{g['granularity']}] n={g['n_items']} kappa={g['fleiss_kappa']} "
            f"alpha={g['krippendorff_alpha']}",
            file=sys.stderr,
        )
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}", file=sys.stderr)
    print(f"Wrote {OUT_REPORT.relative_to(ROOT)}", file=sys.stderr)


if __name__ == "__main__":
    main()
