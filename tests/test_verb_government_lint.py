"""Contract tests for the Kochergina verb-government lint (H5400).

Offline by construction: no NKRYa call, no network, no repo-file dependency beyond the
harvest test, which only asserts the shape of what the key sections yield.
"""

import importlib.util
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
MODULE = REPO / "KocherginaUchebnik_1998" / "verb_government_lint.py"

pytest.importorskip("pymorphy3", reason="pymorphy3 not installed (pip install pymorphy3)")


def _load():
    spec = importlib.util.spec_from_file_location("verb_government_lint", MODULE)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["verb_government_lint"] = mod
    spec.loader.exec_module(mod)
    return mod


vgl = _load()


def test_selftest_passes():
    assert vgl.selftest() == 0


def test_no_evidence_is_never_a_clean_verdict():
    """An uncached pair must read `unknown`, never an empty (clean) flag."""
    ex = vgl.Extractor()
    pair = next(p for p in ex.pairs("Кони падали на землю.", "t", "T-1") if p["prep"])
    assert vgl.lint_pair(pair, None, rare_hits=20)["flag"] == "unknown"


def test_preposition_disambiguates_the_case():
    """«в саду» is locative, «в лес» accusative — the preposition resolves the parse."""
    ex = vgl.Extractor()
    loc = [p for p in ex.pairs("В саду я видел девушек.", "t", "T-2")
           if p["dependent"] == "сад"]
    acc = [p for p in ex.pairs("Волк ушел в лес.", "t", "T-3") if p["dependent"] == "лес"]
    assert loc and loc[0]["case"] == "loct", loc
    assert acc and acc[0]["case"] == "accs", acc


def test_harvest_reads_both_key_sources():
    rows = vgl.harvest()
    sources = {r["source"] for r in rows}
    assert "metodichka_keys" in sources and "metodichka_translations" in sources
    assert any(s.startswith("lessonpack_") for s in sources), sources
    # No locus may come from inline emphasis («candramāḥ **м.**»): loci are X-N shaped.
    bad = [r for r in rows if r["source"].startswith("metodichka")
           and not any(c.isdigit() for c in r["locus"])]
    assert not bad, bad[:3]
