"""The two `slugify` functions share a name but are deliberately DIFFERENT — this
suite pins that divergence so a future "let's dedupe these" refactor can't
silently merge them.

- `build_whitney.slugify`   -> underscores, case preserved, ASCII-only via a
  bare `[^A-Za-z0-9]` filter (so a non-ASCII leading char is simply dropped);
  can return "".
- `mdx_postprocess.slugify` -> hyphens, lowercased, NFKD-folded (so accents map
  to their ASCII base), never empty (falls back to "page").
"""
import build_whitney as bw
import mdx_postprocess as mp


class TestWhitneySlugify:
    def test_spaces_and_case_to_underscores(self):
        assert bw.slugify("Root Index") == "Root_Index"

    def test_runs_of_punctuation_collapse_and_strip(self):
        assert bw.slugify("  a.b--c  ") == "a_b_c"

    def test_non_ascii_leading_char_is_dropped_not_folded(self):
        # No NFKD here: the accented 'Ā' is a non-[A-Za-z0-9] char, so it is
        # treated as a separator and stripped — the opposite of mdx_postprocess.
        assert bw.slugify("Ābc Def!") == "bc_Def"

    def test_empty_and_all_punctuation_return_empty(self):
        assert bw.slugify("") == ""
        assert bw.slugify("!!!") == ""


class TestMdxPostprocessSlugify:
    def test_lowercased_hyphenated(self):
        assert mp.slugify("Root Index") == "root-index"

    def test_nfkd_folds_accents_to_ascii(self):
        assert mp.slugify("Ābc Déf!") == "abc-def"

    def test_empty_falls_back_to_page(self):
        assert mp.slugify("") == "page"
        assert mp.slugify("!!!") == "page"

    def test_realistic_title(self):
        assert mp.slugify("Zaliznyak — Ocherk (1978)") == "zaliznyak-ocherk-1978"


def test_the_two_slugifiers_genuinely_differ():
    # Guardrail: if someone makes them identical, this fails loudly.
    assert bw.slugify("Root Index") != mp.slugify("Root Index")
