"""Regression tests for the stale-base guard's removal scanner (H3550/F1).

`removed_line_numbers()` parses a `git diff -w -U0` body. The defect: the
`---`/`+++` FILE-header test ran on every line, so inside a hunk a removed
line whose CONTENT starts with `--` (a Markdown `---` rule, a `-- comment`)
was silently skipped — and, worse, never incremented `old_line`, so every
subsequent removed line in the same hunk was reported at a shifted number.
The guard then blamed and survivor-checked the wrong lines: real silent
reverts slipped through (false negative) and legitimate edits could be
misattributed (false positive).
"""
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import pre_push_stale_base_check as guard  # noqa: E402


def run_scanner(diff_body: str, monkeypatch) -> list[int]:
    monkeypatch.setattr(guard, "git", lambda *args, **kwargs: diff_body)
    return guard.removed_line_numbers("origin/main", "HEAD", "x.md")


FILE_HEADERS = "--- a/x.md\n+++ b/x.md\n"


def test_removed_dashdash_content_line_is_counted_and_keeps_later_numbers(monkeypatch):
    """A removed `---` rule inside a hunk counts as a removal and does not
    shift the numbers of the removals after it."""
    body = (
        FILE_HEADERS
        + "@@ -10,3 +10,2 @@\n"
        + "-row A\n"
        + "----\n"        # removed content line `---` (Markdown rule)
        + "-row C\n"
        + "+new row\n"
    )
    assert run_scanner(body, monkeypatch) == [10, 11, 12]


def test_removed_double_dash_comment_line_is_counted(monkeypatch):
    body = (
        FILE_HEADERS
        + "@@ -4,2 +4,1 @@\n"
        + "-- comment line\n"
        + "-kept line\n"
        + "+replacement\n"
    )
    assert run_scanner(body, monkeypatch) == [4, 5]


def test_file_headers_before_first_hunk_are_still_ignored(monkeypatch):
    body = FILE_HEADERS + "@@ -7,1 +7,1 @@\n-old row\n+new row\n"
    assert run_scanner(body, monkeypatch) == [7]


def test_pure_addition_hunk_reports_no_removals(monkeypatch):
    body = FILE_HEADERS + "@@ -7,0 +8,2 @@\n+added one\n+added two\n"
    assert run_scanner(body, monkeypatch) == []


def test_multi_hunk_numbers_stay_independent(monkeypatch):
    body = (
        FILE_HEADERS
        + "@@ -10,2 +10,2 @@\n-old a\n----\n+new a\n+new rule\n"
        + "@@ -40,1 +41,1 @@\n-old b\n+new b\n"
    )
    assert run_scanner(body, monkeypatch) == [10, 11, 40]
