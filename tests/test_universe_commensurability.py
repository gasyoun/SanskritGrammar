"""Commensurability gate over the COMMITTED universe verdicts (H1371).

`sangram/audit/universe_commensurability.py` re-derives the case-cluster universes from the
pinned DCS master (920 MB, local-only, gitignored) — like `rederive_dcs_numbers.py`, it is a
local audit, not a CI test. Its committed product, `universe_commensurability_verdicts.json`,
IS in the tree, so CI validates THAT: every cross-article pair carries a verdict (zero
unclassified), no divergence is left UNDECLARED, the four universes re-derived to their expected
values, and the seed Nom pair (SG-SE-001 44.7 % vs SG-MO-001 38.7 %) is present and typed.

A regeneration that reintroduces a silently-different universe (a pair with no verdict, or an
INCOMMENSURABLE-UNDECLARED one) can no longer merge green.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERDICTS = ROOT / "sangram" / "audit" / "universe_commensurability_verdicts.json"

VALID_VERDICTS = {"COMMENSURABLE", "INCOMMENSURABLE-DECLARED", "INCOMMENSURABLE-UNDECLARED"}


def _load():
    return json.loads(VERDICTS.read_text(encoding="utf-8"))


def test_verdicts_file_present():
    assert VERDICTS.exists(), "universe_commensurability_verdicts.json missing — run sangram/audit/universe_commensurability.py"


def test_universes_rederived_to_expected():
    d = _load()
    bad = {k: v for k, v in d["universes"].items() if not v["match"]}
    assert not bad, f"universe denominator drift vs expected: {bad}"


def test_zero_unclassified():
    d = _load()
    assert d["unclassified"] == 0, f"{d['unclassified']} cross-article pair(s) with no verdict"
    assert d["pairs_total"] == len(d["verdicts"]) > 0
    for v in d["verdicts"]:
        assert v["verdict"] in VALID_VERDICTS, f"unknown verdict {v['verdict']!r}"


def test_no_undeclared_divergence():
    d = _load()
    undeclared = [v for v in d["verdicts"] if v["verdict"] == "INCOMMENSURABLE-UNDECLARED"]
    assert not undeclared, (
        "case-cluster pair(s) diverge over an UNDECLARED universe — the article must state its "
        f"denominator and cross-link the sibling:\n{json.dumps(undeclared, ensure_ascii=False, indent=1)}"
    )


def test_seed_nom_pair_typed():
    d = _load()
    seed = [v for v in d["verdicts"] if v["category"] == "Nom"
            and {v["a"]["toc_ref"], v["b"]["toc_ref"]} == {"SG-SE-001", "SG-MO-001"}]
    assert len(seed) == 1, "the seed Nom SG-SE-001 vs SG-MO-001 pair is not enumerated"
    assert seed[0]["verdict"] == "INCOMMENSURABLE-DECLARED"
    assert seed[0]["universe_relation"] == "nested"  # NOUN-only ⊂ real vibhakti
