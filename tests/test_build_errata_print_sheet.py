"""Tests for scripts/build_errata_print_sheet.py (H1839).

Pins the print-sheet HTML contract: traditional Russian «Замеченные опечатки»
table, page/line place formatting, HTML escaping, and page-0 convention.
"""
import build_errata_print_sheet as beps


def test_render_sheet_table_headers_and_count():
    entries = [
        {"page": 12, "line": "3 св.", "instead": "а", "read": "и", "found_by": ["MG"]},
        {"page": 0, "line": "mdx:40", "instead": "<old>", "read": "&new&", "found_by": ["H1", "MG"]},
    ]
    html = beps.render_sheet("Fixture Book (0000)", entries)
    assert "<h1>ЗАМЕЧЕННЫЕ ОПЕЧАТКИ</h1>" in html
    assert "Fixture Book (0000)" in html
    assert "<th>№</th><th>Место</th><th>Напечатано</th><th>Следует читать</th>" in html
    assert "с. 12, 3 св." in html
    assert "mdx:40" in html  # page 0 → locator only
    assert "&lt;old&gt;" in html
    assert "&amp;new&amp;" in html
    assert "Всего позиций: 2" in html
    assert "MG" in html and "H1" in html
    assert "ERRATA_PRINT_SHEET.html не редактируется вручную" in html


def test_render_sheet_page_only_place():
    entries = [{"page": 5, "line": "", "instead": "x", "read": "y", "found_by": []}]
    html = beps.render_sheet("W", entries)
    assert "с. 5" in html
