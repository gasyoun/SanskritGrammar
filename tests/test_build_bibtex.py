"""Tests for scripts/build_bibtex.py (Angle-B B3+B4+B6,
ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md §3): per-book BibTeX + bulk all.bib
from scripts/data/books.yml, the multi-representation ID layer
(static/id/<key>.json + <key>.html + index.json), and the author-identity
people layer (static/people/<slug>.* from scripts/data/people.yml)."""
import json

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


def _sample_books():
    return [
        {"dir": "B_1998", "key": "b-1998", "type": "book",
         "author": "B, A", "title": "T", "year": 1998},
        {"dir": "A_1889", "key": "a-1889", "type": "book",
         "author": "A, A", "title": "T", "year": 1889},
    ]


def _sample_people():
    return [
        {"slug": "b-a", "name": "B, A", "variants": [], "roles": ["author"],
         "works": ["b-1998"]},
        {"slug": "a-a", "name": "A, A",
         "variants": [{"form": "A, Anton"}, {"form": "AA", "rejected": True, "note": "no"}],
         "roles": ["author"], "works": ["a-1889"]},
    ]


def test_bulk_file_is_key_sorted_concatenation():
    files = bb.render_all(_sample_books(), _sample_people())
    assert files["bibtex/all.bib"] == (
        files["bibtex/a-1889.bib"] + files["bibtex/b-1998.bib"]
    )


def test_meta_json_lists_its_own_representations():
    meta = json.loads(bb.render_meta({
        "dir": "B_1998", "key": "b-1998", "type": "book",
        "author": "B, A", "title": "T", "year": 1998,
    }))
    assert meta["id"] == "b-1998"
    assert meta["representations"]["bibtex"] == f"{bb.SITE_BASE}/bibtex/b-1998.bib"
    assert meta["representations"]["json"] == f"{bb.SITE_BASE}/id/b-1998.json"
    assert meta["representations"]["html"] == f"{bb.SITE_BASE}/id/b-1998"


def test_landing_html_alternates_and_escapes():
    page = bb.render_landing({
        "dir": "B_1998", "key": "b-1998", "type": "book",
        "author": "B, A & C", "title": "T <i>title</i>", "year": 1998,
    })
    assert '<link rel="alternate" type="application/x-bibtex"' in page
    assert '<link rel="alternate" type="application/json"' in page
    assert "B, A &amp; C" in page and "<i>title</i>" not in page


def test_id_index_lists_sorted_ids():
    files = bb.render_all(_sample_books(), _sample_people())
    index = json.loads(files["id/index.json"])
    assert index == {"count": 2, "ids": ["a-1889", "b-1998"]}


def test_person_meta_carries_variants_and_work_links():
    person = _sample_people()[1]
    files = bb.render_all(_sample_books(), _sample_people())
    meta = json.loads(files["people/a-a.json"])
    assert meta["name"] == "A, A"
    assert [v["form"] for v in meta["variants"]] == ["A, Anton", "AA"]
    assert meta["variants"][1]["rejected"] is True
    assert meta["works"][0]["id"] == "a-1889"
    assert meta["works"][0]["representations"]["bibtex"].endswith("a-1889.bib")


def test_person_page_lists_works_with_bib_links():
    files = bb.render_all(_sample_books(), _sample_people())
    page = files["people/a-a.html"]
    assert "<h1>A, A</h1>" in page
    assert 'href="https://gasyoun.github.io/SanskritGrammar/id/a-1889"' in page
    assert "a-1889.bib" in page and "not used here" in page


def test_people_index_sorted_by_slug():
    files = bb.render_all(_sample_books(), _sample_people())
    index = json.loads(files["people/index.json"])
    assert index == {"count": 2, "people": ["a-a", "b-a"]}


def test_validate_people_rejects_author_gap_and_unknown_work():
    books = _sample_books()
    broken = [
        {"slug": "b-a", "name": "WRONG, Name", "variants": [], "roles": ["author"],
         "works": ["b-1998", "no-such-book"]},
    ]
    try:
        bb.validate_people(broken, books)
    except ValueError as err:
        text = str(err)
        assert "unknown work key 'no-such-book'" in text
        assert "is no person's canonical name" in text
    else:
        raise AssertionError("validate_people() accepted invalid registry")


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


def test_committed_files_match_the_registry():
    books = bb.load_registry()
    people = bb.load_people()
    bb.validate_people(people, books)
    expected = bb.render_all(books, people)
    assert expected, "registry rendered to nothing"
    for rel, text in expected.items():
        on_disk = (bb.ROOT / "static" / rel).read_text(encoding="utf-8")
        assert on_disk == text, (
            f"static/{rel} is stale — "
            "run `python scripts/build_bibtex.py` and commit the result"
        )
