"""Q4.2 TRACER-style swap (ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md §4).

Validates the shingle/windowing primitives against hand-derived fixtures,
then smoke-tests the real run for internal consistency and reproducibility.
"""
import json

import q42_tracer_style_recall_evaluation as q42


def test_shingles_short_text_is_single_shingle():
    assert q42.shingles("abc", n=4) == {"abc"}
    assert q42.shingles("", n=4) == set()


def test_shingles_exact_length_and_longer():
    assert q42.shingles("abcd", n=4) == {"abcd"}
    assert q42.shingles("abcde", n=4) == {"abcd", "bcde"}


def test_windows_whole_returns_single_window():
    assert q42.windows("abcdefgh", "whole") == ["abcdefgh"]


def test_windows_shorter_than_size_returns_whole_text():
    assert q42.windows("abc", 8) == ["abc"]


def test_windows_covers_the_tail():
    # size=4, stride=2 over an 9-char string must still include a window
    # ending exactly at the string's end, not just stride-aligned windows.
    ws = q42.windows("abcdefghi", 4)
    assert ws[-1] == "fghi"
    assert all(len(w) == 4 for w in ws)


def test_best_chunk_ratio_finds_a_shared_substring_missed_whole_string():
    from difflib import SequenceMatcher
    a = "xxxxxxSHAREDxxxxxx"
    b = "SHAREDyyyyyyyyyyyy"
    whole = SequenceMatcher(None, a, b).ratio()
    chunked = q42.best_chunk_ratio(a, b, 6)
    assert chunked > whole
    assert chunked == 1.0  # "SHARED" appears verbatim in both


def test_pair_key_is_order_independent():
    assert q42.pair_key({"id": "x"}, {"id": "y"}) == q42.pair_key({"id": "y"}, {"id": "x"})


def test_real_run_gold_recall_floor_and_reproducibility():
    """Pin the actual numbers so a silent regeneration of sentences.json or
    matches_review.tsv is caught, not silently re-derived (Q4.1's own
    committed-JSON drift-guard pattern)."""
    by_key = q42.load_sentences()
    candidates = q42.all_candidate_pairs(by_key)
    assert len(candidates) > 0

    scored = []
    for sa, na, sb, nb in candidates:
        scored.append({"a": sa["id"], "b": sb["id"]})
    by_pair_key = {q42.pair_key({"id": r["a"]}, {"id": r["b"]}) for r in scored}

    gold = q42.load_gold()
    gold_true = [r for r in gold if r["verdict"] in (q42.TP_VERDICT, q42.BOUNDARY_VERDICT)]
    assert len(gold_true) == 78  # 58 spelling_variant + 20 length_mismatch

    recovered = sum(
        1 for r in gold_true
        if q42.pair_key({"id": r["a_id"]}, {"id": r["b_id"]}) in by_pair_key
    )
    # deterministic on committed data — the shingle-seeded candidate step must
    # not regress below its known floor (2 transposition-edit pairs are a
    # documented, explained miss; a THIRD miss would be a real regression)
    assert recovered == 76


def test_committed_json_matches_a_fresh_run(tmp_path, monkeypatch):
    """Committed scripts/data/q42_tracer_style_recall_evaluation.json must be
    byte-for-byte what main() would regenerate today — catch a hand-edited or
    stale artifact."""
    monkeypatch.setattr(q42, "OUT_JSON", tmp_path / "out.json")
    monkeypatch.setattr(q42, "OUT_REPORT", tmp_path / "out.md")
    q42.main()
    fresh = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    committed = json.loads(q42.ROOT.joinpath(
        "scripts", "data", "q42_tracer_style_recall_evaluation.json"
    ).read_text(encoding="utf-8"))
    assert fresh == committed
