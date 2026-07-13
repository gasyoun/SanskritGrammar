"""Characterization tests for mdx_postprocess's pure MDX-hardening helpers.

These pin the transforms that make Pandoc output safe for MDX v3 (brace escaping,
degenerate-table dropping, fence-aware splitting, frontmatter title resolution).
"""
import mdx_postprocess as mp


class TestEscBraces:
    def test_unescaped_braces_get_backslash(self):
        assert mp.esc_braces("a{b}c") == r"a\{b\}c"

    def test_already_escaped_brace_untouched(self):
        assert mp.esc_braces(r"a\{b") == r"a\{b"

    def test_no_braces_no_change(self):
        assert mp.esc_braces("none") == "none"


class TestSplitFences:
    def test_prose_only_is_single_non_fence_chunk(self):
        chunks = mp.split_fences("line1\nline2")
        assert chunks == [(False, "line1\nline2")]

    def test_fence_isolated_from_surrounding_prose(self):
        text = "before\n```py\ncode\n```\nafter"
        chunks = mp.split_fences(text)
        # (is_fence, chunk) tuples: prose, fenced block, prose.
        assert chunks[0] == (False, "before")
        assert chunks[1] == (True, "```py\ncode\n```")
        assert chunks[2] == (False, "after")

    def test_fenced_content_is_never_flagged_as_prose(self):
        text = "```\n{not escaped here}\n```"
        chunks = mp.split_fences(text)
        assert all(is_f for is_f, _ in chunks)


class TestDropDegenerateTables:
    def test_real_rst_table_kept(self):
        text = "x\n```rst-table\n+--+\n+==+\n+--+\n```\ny"
        # >= 2 border rows -> a real grid table, preserved verbatim.
        assert mp.drop_degenerate_tables(text) == text

    def test_degenerate_table_dropped(self):
        text = "x\n```rst-table\nnot a table\n```\ny"
        # < 2 border rows -> not a table, the whole fenced block is removed.
        assert mp.drop_degenerate_tables(text) == "x\ny"


class TestTitleFor:
    def test_known_path_uses_titles_map(self):
        title, label = mp.title_for("ApteSyntax_1885/Apte-unicode.mdx", "")
        assert title == "Apte — Sanskrit Syntax (1885)"
        assert label == "Apte 1885"

    def test_falls_back_to_first_h1(self):
        assert mp.title_for("foo/bar.mdx", "# Hello World\n") == ("Hello World", "Hello World")

    def test_falls_back_to_humanized_filename(self):
        assert mp.title_for("foo/some_file-name.mdx", "no h1") == ("some file name", "some file name")
