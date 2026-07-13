"""Characterization tests for build_claims' pure helpers.

norm_fact coerces YAML's unquoted TRUE/FALSE booleans back into the verdict
vocabulary; counts summarizes a claim register (total / verdicted / flagged).
"""
import datetime

import build_claims as bc


class TestSmallHelpers:
    def test_ddmmyyyy(self):
        assert bc.ddmmyyyy(datetime.date(2026, 7, 13)) == "13-07-2026"

    def test_md_cell_stringifies_escapes_and_strips(self):
        assert bc.md_cell("a|b\nc ") == r"a\|b c"
        assert bc.md_cell(None) == ""
        assert bc.md_cell(42) == "42"


class TestNormFact:
    def test_bool_true_false_become_words(self):
        assert bc.norm_fact(True) == "TRUE"
        assert bc.norm_fact(False) == "FALSE"

    def test_strings_pass_through(self):
        assert bc.norm_fact("OVERSTATED") == "OVERSTATED"
        assert bc.norm_fact(None) is None


class TestCounts:
    def test_counts_total_verdicted_flagged(self):
        entries = [
            {"verdict_fact": "TRUE", "verdict_pedagogy": "OK"},          # verdicted, not flagged
            {"verdict_fact": False, "verdict_pedagogy": "OK"},           # verdicted, flagged (FALSE)
            {"verdict_fact": None, "verdict_pedagogy": "MISLEADING"},    # not verdicted, flagged (pedagogy)
            {"verdict_fact": "OVERSTATED", "verdict_pedagogy": "OK"},    # verdicted, flagged (OVERSTATED)
        ]
        n, verdicted, flagged = bc.counts(entries)
        assert n == 4
        assert verdicted == 3      # verdict_fact is not None
        assert flagged == 3

    def test_empty_register(self):
        assert bc.counts([]) == (0, 0, 0)
