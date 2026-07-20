"""Integrity gate for the Usha-gold-vs-DCS per-lemma agreement table (H1399).

Unlike test_usha_gold_vs_proxy.py, this table is NOT regenerable in CI: the join needs the
920 MB untracked dcs_full.sqlite. So the committed JSON is the artifact of record, and this
test validates its schema + invariants (roles ⊆ the six core kārakas, agreement ∈ [0,1],
coverage counts consistent) rather than re-deriving it.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TABLE = os.path.join(ROOT, "sangram", "articles", "karaka-case", "data",
                     "usha_gold_perlemma_agreement.json")

CORE = {"kartṛ", "karman", "karaṇa", "sampradāna", "apādāna", "adhikaraṇa"}
NINE = CORE | {"tādarthya", "hetu", "anya"}


def _load():
    return json.load(open(TABLE, encoding="utf-8"))


def test_core_roles_are_the_six():
    d = _load()
    assert set(d["core_roles"]) == CORE
    assert set(d["proxy_blind_roles_excluded"]) == {"tādarthya", "hetu", "anya"}


def test_per_root_role_vocab_and_bounds():
    d = _load()
    assert len(d["per_root"]) == d["gold"]["distinct_dhatus"]
    for r in d["per_root"]:
        assert isinstance(r["iast"], str) and r["iast"]
        assert set(r["gold_roles_core"]) <= CORE
        assert set(r["corpus_roles_core"]) <= CORE
        assert set(r["corpus_roles_salient"]) <= set(r["corpus_roles_core"])
        assert set(r["gold_roles_all"]) <= NINE
        for key in ("jaccard", "jaccard_salient"):
            if r[key] is not None:
                assert 0.0 <= r[key] <= 1.0
        # gold_only ⊆ gold, corpus_only ⊆ corpus, tp = intersection
        assert set(r["gold_only"]) <= set(r["gold_roles_core"])
        assert set(r["corpus_only"]) <= set(r["corpus_roles_core"])
        assert set(r["tp"]) == set(r["gold_roles_core"]) & set(r["corpus_roles_core"])


def test_coverage_counts_consistent():
    d = _load()
    cw = d["crosswalk"]
    joined = [r for r in d["per_root"] if r["joined"]]
    comparable = [r for r in joined if r["gold_makes_core_claim"]]
    assert cw["roots_total"] == d["gold"]["distinct_dhatus"]
    assert cw["roots_with_karaka_evidence"] == len(joined)
    assert cw["roots_comparable"] == len(comparable)
    assert cw["roots_joined_but_gold_silent_on_core"] == len(joined) - len(comparable)
    assert 0.0 <= cw["join_coverage_pct"] <= 100.0
    assert d["summary"]["n_comparable"] <= d["summary"]["n_joined"] <= cw["roots_total"]


def test_summary_agreement_bounds():
    d = _load()
    s = d["summary"]
    for key in ("mean_jaccard", "mean_jaccard_salient"):
        assert s[key] is None or 0.0 <= s[key] <= 1.0
    for role, pr in s["per_role_agreement"].items():
        assert role in CORE
        assert pr["both"] <= pr["gold_present"]
        assert pr["both"] <= pr["corpus_present"]
        assert pr["corpus_salient"] <= pr["corpus_present"]
        assert pr["gold_only"] == pr["gold_present"] - pr["both"]
