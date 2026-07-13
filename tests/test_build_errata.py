"""Characterization tests for build_errata's pure helpers + the load_book merge.

load_book is the load-bearing bit: it dedupes errata entries, unions their
`found_by` credits, keeps the earliest `date_added`, and sorts by page then
line-ref. These tests pin that behavior against a synthetic errata.yml fixture.
"""
import datetime

import build_errata as be


class TestSmallHelpers:
    def test_ddmmyyyy(self):
        assert be.ddmmyyyy(datetime.date(2026, 7, 13)) == "13-07-2026"

    def test_as_list(self):
        assert be.as_list(None) == []
        assert be.as_list("x") == ["x"]
        assert be.as_list([1, 2]) == [1, 2]

    def test_md_cell_escapes_pipes_and_newlines(self):
        assert be.md_cell("a|b\nc") == r"a\|b c"
        assert be.md_cell(None) == ""

    def test_dedup_key_stringifies_and_strips(self):
        e = {"page": 5, "line": " 8 сн. ", "read": "x", "instead": "y"}
        assert be.dedup_key(e) == ("5", "8 сн.", "x", "y")


class TestLineSortKey:
    def test_from_top_sorts_before_from_bottom(self):
        # 'св.' (from top) -> group 0; 'сн.' (from bottom) -> group 1.
        assert be.line_sort_key("13 св.")[0] == 0
        assert be.line_sort_key("8 сн.")[0] == 1

    def test_uses_first_number(self):
        assert be.line_sort_key("14, 12 сн.") == (1, 14)

    def test_empty_and_none_are_zero_from_bottom(self):
        assert be.line_sort_key("") == (1, 0)
        assert be.line_sort_key(None) == (1, 0)


class TestLoadBook:
    def _write(self, tmp_path, body):
        p = tmp_path / "errata.yml"
        p.write_text(body, encoding="utf-8")
        return p

    def test_duplicate_entries_merge(self, tmp_path):
        yml = (
            "work: TestBook\n"
            "entries:\n"
            '  - {page: 5, line: "8 сн.", read: "x", instead: "y", found_by: MG, date_added: "2026-01-02"}\n'
            '  - {page: 5, line: "8 сн.", read: "x", instead: "y", found_by: AB, date_added: "2026-01-01"}\n'
        )
        work, entries = be.load_book(self._write(tmp_path, yml))
        assert work == "TestBook"
        assert len(entries) == 1
        e = entries[0]
        # found_by unioned in first-seen order; earliest date_added wins.
        assert e["found_by"] == ["MG", "AB"]
        assert e["date_added"] == "2026-01-01"

    def test_entries_sorted_by_page(self, tmp_path):
        yml = (
            "work: TestBook\n"
            "entries:\n"
            '  - {page: 5, line: "8 сн.", read: "x", instead: "y", found_by: MG}\n'
            '  - {page: 3, line: "2 св.", read: "p", instead: "q", found_by: CD}\n'
        )
        _, entries = be.load_book(self._write(tmp_path, yml))
        assert [e["page"] for e in entries] == [3, 5]

    def test_empty_file_yields_no_entries(self, tmp_path):
        work, entries = be.load_book(self._write(tmp_path, ""))
        # work defaults to the yml's parent dir name; entries empty.
        assert entries == []


class TestChangelogVersions:
    def test_maps_version_to_date(self, tmp_path):
        cl = tmp_path / "CHANGELOG.md"
        cl.write_text("## [1.2.0] - 2026-03-01\n## [1.1.0] - 2026-02-01\n## [Unreleased]\n", encoding="utf-8")
        vs = be.changelog_versions(cl)
        assert vs["1.2.0"] == "2026-03-01"
        assert vs["1.1.0"] == "2026-02-01"
        assert vs["Unreleased"] == ""

    def test_missing_file_returns_empty(self, tmp_path):
        assert be.changelog_versions(tmp_path / "nope.md") == {}
