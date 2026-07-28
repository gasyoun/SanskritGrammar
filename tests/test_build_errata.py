"""Characterization tests for build_errata's pure helpers + the load_book merge.

load_book is the load-bearing bit: it dedupes errata entries, unions their
`found_by` credits, keeps the earliest `date_added`, and sorts by page then
line-ref. These tests pin that behavior against a synthetic errata.yml fixture.
"""
import datetime

import pytest

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
        assert be.dedup_key(e) == ("5", "8 сн.", "x", "y", "erratum", "print", "")

    def test_dedup_key_tier_disambiguates_same_page_line_text(self):
        e1 = {"page": 5, "line": "8 сн.", "read": "x", "instead": "y"}
        e2 = {"page": 5, "line": "8 сн.", "read": "x", "instead": "y", "tier": "retraction"}
        assert be.dedup_key(e1) != be.dedup_key(e2)

    def test_dedup_key_kind_disambiguates(self):
        e1 = {"page": 5, "line": "8 сн.", "read": "x", "instead": "y"}
        e2 = {**e1, "kind": "digitization"}
        assert be.dedup_key(e1) != be.dedup_key(e2)

    def test_dedup_key_locus_disambiguates_two_digitization_rows(self):
        """Two digitization fixes share an empty (page, line) and can share the
        same read/instead — only `locus` tells them apart. Without it they merged
        into one row (the занятие-30 / занятие-5 collision, H1795)."""
        base = {"page": "", "line": "", "read": "II.", "instead": "II",
                "kind": "digitization"}
        a = {**base, "locus": "file.mdx:7789"}
        b = {**base, "locus": "file.mdx:1113"}
        assert be.dedup_key(a) != be.dedup_key(b)


class TestChecksum:
    def test_deterministic_over_content_fields(self):
        e = {"page": 5, "line": "8 сн.", "read": "x", "instead": "y"}
        assert be.checksum(e) == be.checksum(dict(e))

    def test_changes_when_content_changes(self):
        e1 = {"page": 5, "line": "8 сн.", "read": "x", "instead": "y"}
        e2 = {"page": 5, "line": "8 сн.", "read": "x2", "instead": "y"}
        assert be.checksum(e1) != be.checksum(e2)

    def test_absent_locus_leaves_existing_checksums_untouched(self):
        """`locus` joins the payload only when set, so every print-errata row
        already published keeps its checksum byte-for-byte."""
        e = {"page": 5, "line": "8 сн.", "read": "x", "instead": "y"}
        assert be.checksum(e) == be.checksum({**e, "locus": ""})
        assert be.checksum(e) == be.checksum({**e, "locus": None})

    def test_locus_distinguishes_otherwise_identical_rows(self):
        e = {"page": "", "line": "", "read": "II.", "instead": "II"}
        assert be.checksum({**e, "locus": "a:1"}) != be.checksum({**e, "locus": "b:2"})

    def test_length(self):
        e = {"page": 5, "line": "8 сн.", "read": "x", "instead": "y"}
        assert len(be.checksum(e)) == be.CHECKSUM_LEN


class TestBookSlugYear:
    def test_splits_camelcase_and_trailing_year(self):
        assert be.book_slug_year("BuhlerLeitfaden_1923") == ("buhler-leitfaden", "1923")

    def test_single_word_name(self):
        assert be.book_slug_year("GasunsDhatu_2014") == ("gasuns-dhatu", "2014")

    def test_no_trailing_year_falls_back(self):
        assert be.book_slug_year("NoYearHere") == ("noyearhere", "")


class TestAssignTiers:
    def _entry(self, **kw):
        base = {"page": 5, "line": "8 сн.", "read": "x", "instead": "y",
                "found_by": [], "date_added": "2026-01-01", "fixed_in": None, "note": None,
                "tier": "erratum", "revises": None, "reason": None}
        base.update(kw)
        return base

    def test_erratum_gets_fresh_sequential_id_per_page(self):
        entries = [self._entry(page=5, line="8 сн."), self._entry(page=5, line="9 сн."),
                   self._entry(page=6, line="1 св.")]
        be.assign_tiers(entries, "TestBook_2020")
        assert [e["id"] for e in entries] == [
            "test-book-2020.5.1", "test-book-2020.5.2", "test-book-2020.6.1"]

    def test_checksum_and_date_populated(self):
        entries = [self._entry()]
        be.assign_tiers(entries, "TestBook_2020")
        assert entries[0]["checksum"] == be.checksum(entries[0])
        assert entries[0]["date"] == "2026-01-01"

    def test_revision_id_gains_v2_suffix(self):
        base = self._entry(page=5, line="8 сн.")
        be.assign_tiers([base], "TestBook_2020")  # look up the base id first, as an editor would
        rev = self._entry(page=5, line="9 сн.", tier="revision", revises=base["id"])
        be.assign_tiers([base, rev], "TestBook_2020")
        assert rev["id"] == f"{base['id']}.v2"

    def test_revision_chain_increments_version(self):
        base = self._entry(page=5, line="8 сн.")
        be.assign_tiers([base], "TestBook_2020")
        rev1 = self._entry(page=5, line="9 сн.", tier="revision", revises=base["id"])
        rev2 = self._entry(page=5, line="10 сн.", tier="revision", revises=base["id"])
        entries = [base, rev1, rev2]
        be.assign_tiers(entries, "TestBook_2020")
        assert rev1["id"] == f"{base['id']}.v2"
        assert rev2["id"] == f"{base['id']}.v3"

    def test_revision_without_revises_exits(self):
        entries = [self._entry(tier="revision")]
        with pytest.raises(SystemExit):
            be.assign_tiers(entries, "TestBook_2020")

    def test_revision_with_unknown_revises_exits(self):
        entries = [self._entry(tier="revision", revises="nope-2020.1.1")]
        with pytest.raises(SystemExit):
            be.assign_tiers(entries, "TestBook_2020")

    def test_retraction_without_reason_exits(self):
        entries = [self._entry(tier="retraction")]
        with pytest.raises(SystemExit):
            be.assign_tiers(entries, "TestBook_2020")

    def test_retraction_with_reason_gets_fresh_id(self):
        entries = [self._entry(tier="retraction", reason="withdrawn")]
        be.assign_tiers(entries, "TestBook_2020")
        assert entries[0]["id"] == "test-book-2020.5.1"

    def test_unknown_tier_exits(self):
        entries = [self._entry(tier="nonsense")]
        with pytest.raises(SystemExit):
            be.assign_tiers(entries, "TestBook_2020")


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
