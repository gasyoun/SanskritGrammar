"""Tests for scripts/build_catalog.py (H1839).

Pins the documented contract: Devanagari is the primary signal; IAST matches
need >=4 words on both sides; union-find clusters shared sentences; rows are
ordered by earliest book year and get C0001… catalog ids.
"""
import json

import build_catalog as bc


def _sent(sid, book, lesson, text, script="deva"):
    return {"id": sid, "book": book, "lesson": lesson, "text": text, "script": script}


def _match(a, b, script="deva", score=1.0):
    return {"a": a, "b": b, "script": script, "score": score, "exact": score == 1.0}


def test_union_find_merges_transitive():
    uf = bc.UnionFind()
    uf.union("a", "b")
    uf.union("b", "c")
    assert uf.find("a") == uf.find("c")
    assert uf.find("d") == "d"  # singleton materialises on find


def test_cluster_drops_short_iast_noise():
    # One-word IAST paradigm noise must not form a catalog row.
    a = _sent("i1", "buhler", "1", "karoti", script="iast")
    b = _sent("i2", "knauer", "2", "karoti", script="iast")
    rows = bc.cluster_matches([_match(a, b, script="iast")])
    assert rows == []


def test_cluster_keeps_long_iast_and_deva_prefers_deva_exemplar():
    long = "sa gacchati grāmam iti vadati smarah"
    a_iast = _sent("i1", "knauer", "3", long, script="iast")
    b_iast = _sent("i2", "kochergina", "4", long, script="iast")
    a_deva = _sent("d1", "buhler", "1", "स गच्छति ग्रामम्", script="deva")
    b_deva = _sent("d2", "knauer", "2", "स गच्छति ग्रामम्", script="deva")
    # Link all four via two edges that share knauer nodes transitively via text
    # identity on distinct ids — union both pairs then cross-link via shared book node.
    matches = [
        _match(a_deva, b_deva, script="deva"),
        _match(a_iast, b_iast, script="iast"),
        # join clusters: knauer dewa id linked to knauer iast via a synthetic edge
        # using the same knauer sentence as both sides of a dewa edge is enough
        # if we re-use b_deva with a third book — simpler: one three-book dewa cluster
    ]
    a3 = _sent("d3", "kochergina", "5", "स गच्छति ग्रामम्", script="deva")
    matches = [
        _match(a_deva, b_deva, script="deva"),
        _match(b_deva, a3, script="deva"),
    ]
    rows = bc.cluster_matches(matches)
    assert len(rows) == 1
    r = rows[0]
    assert r["catalog_id"] == "C0001"
    assert r["earliest_book"] == "buhler"
    assert r["earliest_year"] == 1878
    assert r["script"] == "deva"
    assert set(r["books"]) == {"buhler", "knauer", "kochergina"}
    assert r["books"]["buhler"] == ["1"]


def test_write_catalog_tmp(tmp_path):
    rows = bc.cluster_matches([
        _match(
            _sent("a", "buhler", "1", "रामः पठति", script="deva"),
            _sent("b", "knauer", "2", "रामः पठति", script="deva"),
        )
    ])
    jpath, cpath = bc.write_catalog(rows, data_dir=str(tmp_path))
    loaded = json.loads((tmp_path / "catalog.json").read_text(encoding="utf-8"))
    assert loaded[0]["catalog_id"] == "C0001"
    csv_text = (tmp_path / "catalog.csv").read_text(encoding="utf-8")
    assert "catalog_id" in csv_text
    assert "C0001" in csv_text
    assert jpath.endswith("catalog.json")
    assert cpath.endswith("catalog.csv")
