"""extract_sentences.py — Q4.3 (ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md §4):
extend the exercise-sentence pool from 3 to 5 books (add Apte 1885 + Whitney
1889 to Buhler/Knauer/Kochergina).
"""
import json

import extract_sentences as es


def test_five_books_configured_or_scoped():
    # apte joins BOOKS like the original three; whitney is deliberately NOT a
    # BOOKS entry (see the module comment) — it gets its own bounded extractor.
    assert set(es.BOOKS.keys()) == {"buhler", "knauer", "kochergina", "apte"}
    assert es.BOOKS["apte"]["path"].endswith("Apte-unicode.mdx")


def test_apte_lesson_header_regex():
    lesson_re = es.BOOKS["apte"]["lesson_re"]
    assert lesson_re.match("# Урок 4")
    m = lesson_re.match("# **Урок 1.**")
    assert m and m.group(1) == "1"
    # TOC lines must not match (they start with `[`, not `#`).
    assert lesson_re.match("[**Урок 1.** 6](#урок-1)") is None


def test_whitney_appendix_extraction_is_the_clean_fable_only():
    sentences = es.extract_whitney_appendix()
    assert len(sentences) == 15
    assert all(s["book"] == "whitney" and s["script"] == "iast" for s in sentences)
    assert all(s["lesson"] == "appendix" for s in sentences)
    assert sentences[0]["text"].startswith("āsīt kalyāṇakaṭakavāstavyo")
    assert sentences[0]["id"] == "whitney-1889.appendix.1"
    # the excluded Rig-Veda passage / paradigm chapters must not leak in.
    joined = " ".join(s["text"] for s in sentences)
    assert "rudrébhir" not in joined


def test_sentences_json_has_five_books_and_is_append_only(tmp_path, monkeypatch):
    monkeypatch.setattr(es, "DATA_DIR", str(tmp_path))
    es.extract()
    with open(tmp_path / "sentences.json", encoding="utf-8") as f:
        data = json.load(f)
    books = {s["book"] for s in data}
    assert books == {"buhler", "knauer", "kochergina", "apte", "whitney"}
    assert sum(1 for s in data if s["book"] == "whitney") == 15
    assert sum(1 for s in data if s["book"] == "apte") > 1000
