"""Q3.4 three-scheme agreement (ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md §4).

Validates the two statistics (Fleiss' kappa, Krippendorff's alpha) against
hand-derived exact-fraction expectations on a tiny synthetic fixture, plus a
smoke test that the real 876-root crosswalk run produces a sane, reproducible
result and that the coder-substitution note ships with every result.
"""
import json

import q34_three_scheme_agreement as q34

# --- synthetic fixture, independently hand-computed (see the mint pass'
#     scratch derivation): 3 raters, 4 items, categories {"X", "Y"}
#   item1: X,X,X   item2: Y,Y,Y   item3: X,X,Y   item4: X,Y,Y
# Fleiss' kappa (by hand, exact fractions): P_bar=2/3, P_e=1/2 -> kappa=1/3
# Krippendorff's alpha (by hand): Do=1/3, De=6/11 -> alpha=7/18
FIXTURE = [
    {"1975": "X", "1978": "X", "2026": "X"},
    {"1975": "Y", "1978": "Y", "2026": "Y"},
    {"1975": "X", "1978": "X", "2026": "Y"},
    {"1975": "X", "1978": "Y", "2026": "Y"},
]


def test_fleiss_kappa_matches_hand_derivation():
    kappa, p_bar = q34.fleiss_kappa(FIXTURE)
    assert abs(kappa - 1 / 3) < 1e-9
    assert abs(p_bar - 2 / 3) < 1e-9


def test_krippendorff_alpha_matches_hand_derivation():
    alpha = q34.krippendorff_alpha(FIXTURE)
    assert abs(alpha - 7 / 18) < 1e-9


def test_perfect_agreement_is_one():
    perfect = [{"1975": "A", "1978": "A", "2026": "A"} for _ in range(10)]
    kappa, p_bar = q34.fleiss_kappa(perfect)
    alpha = q34.krippendorff_alpha(perfect)
    assert kappa == 1.0
    assert p_bar == 1.0
    assert alpha == 1.0


def test_normalize_strips_subscripts_and_uncertainty_flag():
    assert q34.normalize("A₁") == ("A1", False)
    assert q34.normalize("N?") == ("N", True)
    assert q34.normalize("") == (None, False)
    assert q34.normalize("-") == (None, False)


def test_series_letter():
    assert q34.series_letter("A1") == "A"
    assert q34.series_letter("N0") == "N"
    assert q34.series_letter("L") == "L"


def test_pairwise_stats_symmetry_and_shape():
    stats = q34.pairwise_stats(FIXTURE)
    assert set(stats) == {"1975_vs_1978", "1975_vs_2026", "1978_vs_2026"}
    for pair in stats.values():
        assert pair["n"] == 4
        assert 0.0 <= pair["raw_agreement"] <= 1.0


def test_real_crosswalk_run_is_reproducible_and_carries_the_substitution_note():
    rows = q34.load_rows()
    assert len(rows) == 876  # the roadmap's own "876-root crosswalk" figure

    run_a = q34.run_granularity(rows, "letter")
    run_b = q34.run_granularity(rows, "letter")
    assert run_a["fleiss_kappa"] == run_b["fleiss_kappa"]  # seeded, deterministic
    assert run_a["krippendorff_alpha"] == run_b["krippendorff_alpha"]

    # Sane bounds: this is real disagreement data, not perfect or degenerate.
    assert 0.0 < run_a["fleiss_kappa"] < 1.0
    assert 0.0 < run_a["krippendorff_alpha"] < 1.0
    assert run_a["n_items"] > 800  # most of the 876 survive the completeness filter

    full = q34.run_granularity(rows, "full")
    # Collapsing to series-letter can only raise or hold agreement, never lower it.
    assert full["fleiss_kappa"] <= run_a["fleiss_kappa"] + 1e-9


def test_committed_outputs_exist_and_parse():
    assert q34.OUT_JSON.exists(), "run scripts/q34_three_scheme_agreement.py to (re)generate it"
    data = json.loads(q34.OUT_JSON.read_text(encoding="utf-8"))
    assert "coder_substitution_note" in data
    assert "Gasuns 2014" in data["coder_substitution_note"]
    assert {g["granularity"] for g in data["granularities"]} == {"full", "letter"}

    report = q34.OUT_REPORT.read_text(encoding="utf-8")
    assert "Coder substitution" in report
    assert "Fleiss" in report and "Krippendorff" in report
