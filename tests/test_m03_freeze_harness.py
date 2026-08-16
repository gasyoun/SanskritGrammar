"""Planted-defect tests for the M03 freeze harness (H2871).

Both checkers report green against most of the current manuscript, which is exactly
when a checker is easiest to get wrong: a regex that matches nothing is also silent.
These tests plant each defect class in synthetic input and assert it is caught, and
assert that a full run leaves every manuscript byte untouched.

Same pattern as `tests/test_claims_consistency.py::test_scan_flags_a_planted_stale`.
"""
import sys
from pathlib import Path

import pytest

HARNESS = Path(__file__).resolve().parent.parent / "GasunsDhatu_2014" / "revision-2026"
sys.path.insert(0, str(HARNESS))

gost = pytest.importorskip("gost_bibliography_check")
numbers = pytest.importorskip("numbers_crosscheck")
common = pytest.importorskip("m03_checkers_common")


def numbered(lines):
    return list(enumerate(lines, start=1))


# --------------------------------------------------------------- ГОСТ checker

def parse_one(body):
    entries, _start = gost.parse_bibliography(numbered(["# Библиография", body]))
    return entries


def codes(findings):
    return {f.code for f in findings}


def test_sigil_year_disagreeing_with_the_imprint_is_caught():
    found = gost.check_entries(parse_one(
        "7. **Иванов** 1970 -- Иванов И. И. Заглавие. -- М. : Наука, 1985."))
    assert "G2" in codes(found)


def test_imprint_colon_without_a_space_is_caught():
    found = gost.check_entries(parse_one(
        "7. **Иванов** 1985 -- Иванов И. И. Заглавие. -- М.: Наука, 1985."))
    assert "G3" in codes(found)


def test_initials_without_a_space_are_caught():
    found = gost.check_entries(parse_one(
        "7. **Иванов** 1985 -- Иванов И.И. Заглавие. -- М. : Наука, 1985."))
    assert "G5" in codes(found)


def test_intraword_double_hyphen_is_caught_but_a_page_range_is_not():
    artefact = gost.check_entries(parse_one(
        "7. **Иванов** 1985 -- Иванов И. И. Изд--во. -- М. : Наука, 1985."))
    assert "G7" in codes(artefact)
    clean = gost.check_entries(parse_one(
        "7. **Иванов** 1985 -- Иванов И. И. Заглавие // Сборник. -- М. : Наука, "
        "1985. -- С. 12--30."))
    assert "G7" not in codes(clean)


def test_analytic_record_without_a_page_range_is_caught():
    found = gost.check_entries(parse_one(
        "7. **Иванов** 1985 -- Иванов И. И. Статья // Сборник. -- М. : Наука, 1985."))
    assert "G8" in codes(found)


def test_duplicate_and_missing_entry_numbers_are_caught():
    entries, _ = gost.parse_bibliography(numbered([
        "# Библиография",
        "1. **Иванов** 1985 -- Иванов И. И. Заглавие. -- М. : Наука, 1985.",
        "1. **Петров** 1986 -- Петров П. П. Заглавие. -- М. : Наука, 1986.",
        "4. **Сидоров** 1987 -- Сидоров С. С. Заглавие. -- М. : Наука, 1987.",
    ]))
    messages = " ".join(f.message for f in gost.check_entries(entries) if f.code == "G1")
    assert "номер 1" in messages
    assert "2, 3" in messages


def test_bold_seam_inside_the_sigil_is_caught_and_still_parses():
    entries = parse_one(
        "7. **Иванов** 1985** **-- Иванов И. И. Заглавие. -- М. : Наука, 1985.")
    assert entries[0]["year"] == "1985"
    assert "G12" in codes(gost.check_entries(entries))


def test_citation_without_an_entry_is_dangling_and_one_with_an_entry_is_not():
    entries = parse_one(
        "7. **Иванов** 1985 -- Иванов И. И. Заглавие. -- М. : Наука, 1985.")
    cites = [("t.mdx", 3, ("иванов",), "Иванов", "1985"),
             ("t.mdx", 4, ("петров",), "Петров", "1990")]
    found = gost.check_references(entries, cites, {})
    dangling = [f for f in found if f.code == "R1"]
    assert len(dangling) == 1
    assert "Петров" in dangling[0].message
    assert not [f for f in found if f.code == "R2"]


def test_an_abbreviation_resolves_its_target_and_flags_a_year_outside_the_range():
    lines = numbered([
        "# Принятые сокращения",
        "EWA -- Mayrhofer 1986--2001",
        "# Библиография",
    ])
    abbrevs = gost.parse_abbreviations(lines)
    assert gost.abbr_key("EWA") in abbrevs
    entries = parse_one(
        "7. **Mayrhofer** 1986--2001 -- Mayrhofer M. EWA. -- Heidelberg : Winter, 1986.")
    inside = gost.check_references(
        entries, [("t.mdx", 3, ("ewa",), "EWA", "1992")], abbrevs)
    assert not [f for f in inside if f.code in ("R1", "R2", "A2")]
    outside = gost.check_references(
        entries, [("t.mdx", 3, ("ewa",), "EWA", "1932")], abbrevs)
    assert [f for f in outside if f.code == "A2"]


def test_a_page_reference_is_not_read_as_a_citation_year():
    cited = gost.CITE_BODY_RE.search("MW 1132")
    assert cited is None


# ------------------------------------------------------------ numbers checker

def test_a_broken_ratio_column_is_caught_and_a_sound_one_is_not():
    grid = numbered([
        "| текст | V | C | k |",
        "|---|---|---|---|",
        "| A | 100 | 133 | 1.33 |",
        "| B | 200 | 278 | 1.39 |",
        "| C | 400 | 552 | 1.38 |",
        "| D | 800 | 1104 | 1.38 |",
        "",
    ])
    tables = numbers.parse_tables(grid, set())
    found, confirmed = numbers.check_tables("t.mdx", tables)
    assert not found and confirmed

    broken = grid[:4] + numbered(["| C | 400 | 552 | 1.98 |"])[:1] + grid[5:]
    broken = numbered([t for _n, t in broken])
    tables = numbers.parse_tables(broken, set())
    found, _ = numbers.check_tables("t.mdx", tables)
    assert [f for f in found if f.code == "N1"]


def test_a_miscomputed_percentage_is_caught_and_truncation_is_tolerated():
    bad, _ = numbers.check_prose_arithmetic(
        "t.mdx", numbered(["Итого 590 из 935 корней (73,1 %)."]), set())
    assert [f for f in bad if f.code == "N2"]

    good, confirmed = numbers.check_prose_arithmetic(
        "t.mdx", numbered(["Итого 590 из 935 корней (63,1 %)."]), set())
    assert not good and confirmed

    # 16.857 % truncated to 16,8 % is accepted; see the DCS ledger, H1229 REFUTED #1.
    truncated, _ = numbers.check_prose_arithmetic(
        "t.mdx", numbered(["Доля 16857 из 100000 (16,8 %)."]), set())
    assert not truncated


def test_prose_arithmetic_that_does_not_add_up_is_caught():
    found, _ = numbers.check_prose_arithmetic(
        "t.mdx", numbered(["Всего 750 + 1 363 = 2 200 статей."]), set())
    assert [f for f in found if f.code == "N3"]


def test_an_unresolvable_section_reference_is_caught_and_an_external_one_is_not():
    per_file = [("t.mdx", numbered(["# Глава 4. Заголовок", "## 4.1. Раздел",
                                    "См. §4.9 ниже.", "См. BOOK_PLAN §8."]), set())]
    sections, chapters, captions = numbers.build_targets(per_file)
    found = numbers.check_crossrefs(per_file, sections, chapters, captions, {},
                                    (None, None))
    messages = " ".join(f.message for f in found)
    assert "§ 4.9" in messages
    assert "§ 8" not in messages


def test_the_illustration_list_block_is_not_its_own_witness():
    main = numbered([
        "# Список иллюстративного материала",
        "Таблица 5 Распределение рядов согласных (в диахронии) 122",
        "# Библиография",
    ])
    block = numbers.illustration_block(main)
    _s, _c, captions = numbers.build_targets(
        [(common.MAIN_TEXT, main, set())], skip_main=block)
    assert "5" not in captions["Таблица"]
    found = numbers.check_illustration_list(main, captions, block)
    assert [f for f in found if "Таблица 5" in f.message]


# ------------------------------------------------------------------- the fence

def test_a_full_run_of_both_checkers_leaves_the_manuscript_untouched():
    paths = common.manuscript_paths()
    before = {p: p.read_bytes() for p in paths}
    sys.argv = ["numbers_crosscheck.py", "--stdout"]
    numbers.main()
    sys.argv = ["gost_bibliography_check.py", "--stdout"]
    gost.main()
    for path in paths:
        assert path.read_bytes() == before[path], f"{path.name} was modified"
