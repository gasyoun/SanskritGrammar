"""Tests for scripts/build_bibtex.py (B3, ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md
Angle-B site backlog): per-book BibTeX + bulk all.bib from scripts/data/books.yml."""
import build_bibtex as bb


def test_registry_is_valid_against_the_real_repo():
    books = bb.load_registry()
    bb.validate(books)  # raises on any invariant breach — no assertion needed
    assert len(books) == len({b["key"] for b in books})


def test_entry_field_order_and_derived_url():
    entry = bb.render_entry({
        "dir": "KnauerFrazy_1908", "key": "knauer-1908", "type": "book",
        "author": "Knauer, Friedrich", "title": "Фразы",
        "note": "n", "year": 1908,
    })
    assert entry.startswith("@book{knauer-1908,\n")
    order = [line.split(" =")[0].strip() for line in entry.splitlines()[1:-1]]
    assert order == ["author", "title", "year", "note", "url"]
    assert entry.rstrip().endswith(
        f"url = {{{bb.REPO_URL}/tree/main/KnauerFrazy_1908}}\n}}".rstrip()
    )


def test_bulk_file_is_key_sorted_concatenation():
    books = [
        {"dir": "B_1998", "key": "b-1998", "type": "book",
         "author": "B, A", "title": "T", "year": 1998},
        {"dir": "A_1889", "key": "a-1889", "type": "book",
         "author": "A, A", "title": "T", "year": 1889},
    ]
    files = bb.render_all(books)
    assert set(files) == {"a-1889.bib", "b-1998.bib", "all.bib"}
    assert files["all.bib"] == files["a-1889.bib"] + files["b-1998.bib"]


def test_validate_rejects_dir_year_mismatch_and_undiscovered_dir(monkeypatch):
    monkeypatch.setattr(bb, "publishable_book_dirs", lambda: {"Good_1908"})
    try:
        bb.validate([
            {"dir": "Good_1908", "key": "g", "type": "book",
             "author": "G", "title": "T", "year": 1907},        # year mismatch
            {"dir": "Missing_2000", "key": "m", "type": "book",
             "author": "M", "title": "T", "year": 2000},        # not discovered
        ])
    except ValueError as err:
        text = str(err)
        assert "dir suffix year 1908 != registry year 1907" in text
        assert "not a publishable book dir" in text
    else:
        raise AssertionError("validate() accepted invalid entries")


def test_committed_bib_files_match_the_registry():
    books = bb.load_registry()
    expected = bb.render_all(books)
    for name, text in expected.items():
        on_disk = (bb.OUT_DIR / name).read_text(encoding="utf-8")
        assert on_disk == text, (
            f"static/bibtex/{name} is stale — "
            "run `python scripts/build_bibtex.py` and commit the result"
        )
