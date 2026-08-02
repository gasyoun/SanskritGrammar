"""Tests for scripts/render_catalog_mdx.py (H1839).

Pins pure helpers and the MDX render contract: front-matter, table headers,
lesson cells, pipe-escaping in sentence text, and pair-count summary line.
"""
import render_catalog_mdx as rcm


def test_cell_empty_is_em_dash():
    r = {"books": {}}
    assert rcm.cell(r, "buhler") == "—"


def test_cell_joins_lessons():
    r = {"books": {"buhler": ["1", "3"]}}
    assert rcm.cell(r, "buhler") == "1, 3"


def test_render_mdx_table_and_summary():
    rows = [
        {
            "catalog_id": "C0001",
            "earliest_book": "buhler",
            "earliest_year": 1878,
            "script": "deva",
            "text": "a | b pipe",
            "books": {"buhler": ["1"], "knauer": ["2"]},
        },
        {
            "catalog_id": "C0002",
            "earliest_book": "knauer",
            "earliest_year": 1908,
            "script": "deva",
            "text": "only knauer-koch",
            "books": {"knauer": ["9"], "kochergina": ["10"]},
        },
    ]
    body = rcm.render_mdx(rows)
    assert 'title: "Concordance — shared exercise sentences"' in body
    assert "| № | Earliest | Sentence |" in body
    assert "C0001" in body and "C0002" in body
    assert "a \\| b pipe" in body  # pipe escaped for MD table
    assert "2 shared-sentence clusters found" in body
    assert "1 shared only between Bühler and Knauer" in body
    assert "1 only between Knauer and Kochergina" in body
    assert "— do not hand-edit._" in body
