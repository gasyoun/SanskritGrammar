"""Freshness + integrity gate for the Usha-gold-vs-deprel-proxy comparison (H1395).

Both inputs (Concordance/usha_karaka_gold/usha_karaka_gold.json and the karaka-case
coverage_summary.json) are committed, so the comparison is fully reproducible in CI.

- test_committed_matches_regeneration: the committed usha_gold_vs_proxy.json equals a fresh
  regeneration — a stale table can never merge green.
- test_role_vocab_is_the_nine: the gold uses exactly the nine documented roles, no more.
- test_proxy_blind_finding: hetu + tādarthya (roles with no deprel relation) carry the
  213 citation-backed attestations the article's § 7 finding names.
- test_gold_totals: the 581-dhātu / 1,372-citation headline reproduces from the gold JSON.
"""
import json

import compare_usha_gold_vs_proxy as cg

NINE_ROLES = {
    "kartṛ", "karman", "karaṇa", "sampradāna", "apādāna", "adhikaraṇa",
    "tādarthya", "hetu", "anya",
}


def test_committed_matches_regeneration():
    fresh = cg.build()
    committed = json.load(open(cg.OUT, encoding="utf-8"))
    assert committed == fresh, "usha_gold_vs_proxy.json is stale — rerun compare_usha_gold_vs_proxy.py"


def test_role_vocab_is_the_nine():
    res = cg.build()
    roles = {r["role"] for r in res["roles"]}
    assert roles == NINE_ROLES, f"unexpected role vocabulary: {roles ^ NINE_ROLES}"


def test_proxy_blind_finding():
    res = cg.build()
    blind = {r["role"] for r in res["roles"] if not r["in_deprel_proxy"]}
    assert blind == {"hetu", "tādarthya", "anya"}
    assert res["proxy_blind_semantic_citations"] == 213  # hetu 180 + tādarthya 33


def test_gold_totals():
    res = cg.build()
    assert res["gold"]["distinct_dhatus"] == 581
    assert res["gold"]["total_citations"] == 1372
