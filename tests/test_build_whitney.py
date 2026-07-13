"""Characterization tests for build_whitney's pure IAST/Devanagari helpers.

These lock the deterministic transliteration + OCR-repair gates that regenerate
Whitney's paradigm tables (H427), so a change in the transliteration path or the
cell classifiers shows up as a failed test rather than silently corrupted tables.
"""
import build_whitney as bw


class TestIastToDevanagari:
    def test_basic_words(self):
        assert bw.whitney_iast_to_deva("agni") == "अग्नि"
        assert bw.whitney_iast_to_deva("deva") == "देव"
        assert bw.whitney_iast_to_deva("bhū") == "भू"

    def test_final_consonant_gets_virama(self):
        assert bw.whitney_iast_to_deva("rājan") == "राजन्"

    def test_whitney_palatal_sibilant_c_cedilla(self):
        # Whitney writes the palatal sibilant as 'ç'; it must map like 'ś'.
        assert bw.whitney_iast_to_deva("aç") == "अश्"

    def test_whitney_diphthong_notation(self):
        # 'āi' is Whitney's spelling of the 'ai' diphthong.
        assert bw.whitney_iast_to_deva("āindra") == "ऐन्द्र"

    def test_deterministic(self):
        assert bw.whitney_iast_to_deva("agni") == bw.whitney_iast_to_deva("agni")


class TestCellClassifiers:
    def test_devanagari_cell(self):
        assert bw._is_deva_cell("अग्नि") is True
        assert bw._is_iast_cell("अग्नि") is False

    def test_iast_cell(self):
        assert bw._is_iast_cell("agni") is True
        assert bw._is_deva_cell("agni") is False

    def test_multitoken_cell_is_neither(self):
        # A space disqualifies a single-token cell.
        assert bw._is_deva_cell("अ ग") is False
        assert bw._is_iast_cell("अ ग") is False

    def test_empty_cell_is_neither(self):
        assert bw._is_deva_cell("") is False
        assert bw._is_iast_cell("") is False


class TestMdxSafe:
    def test_angle_brackets_to_entities(self):
        assert bw.mdx_safe("a<b>c") == "a&lt;b&gt;c"

    def test_braces_escaped(self):
        assert bw.mdx_safe("x{y}z") == r"x\{y\}z"

    def test_plain_text_untouched(self):
        assert bw.mdx_safe("plain") == "plain"


class TestRegenerateTableCells:
    def test_deva_cell_regenerated_from_next_iast_line(self):
        # A single-token Devanagari cell immediately followed by an IAST line is
        # replaced by a form freshly transliterated from that line; the count
        # reflects one fix and unrelated lines are untouched.
        lines = ["देव", "agni", "keep me"]
        out, n = bw.regenerate_table_cells(lines)
        assert n == 1
        assert out[0] == "अग्नि"
        assert out[2] == "keep me"

    def test_idempotent_when_no_corrupt_cells(self):
        lines = ["agni", "deva", "plain prose here"]
        out, n = bw.regenerate_table_cells(lines)
        assert n == 0
        assert out == lines
