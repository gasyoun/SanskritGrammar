"""Q4.1 difflib evaluation (ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md §4).

Validates precision_at() against a tiny hand-computed synthetic fixture, then
smoke-tests the real 128-pair run for internal consistency and reproducibility.
"""
import json

import q41_difflib_gold_evaluation as q41

# 5 synthetic rows: 2 spelling_variant, 1 length_mismatch, 2 low_similarity,
# scores chosen so a cutoff of 0.90 drops exactly the two low_similarity rows.
FIXTURE = [
    {"score": 0.95, "verdict": "spelling_variant"},
    {"score": 0.91, "verdict": "spelling_variant"},
    {"score": 0.90, "verdict": "length_mismatch"},
    {"score": 0.85, "verdict": "low_similarity"},
    {"score": 0.82, "verdict": "low_similarity"},
]


def test_precision_at_full_pool_hand_derivation():
    # n=5: spelling=2, boundary=1, low_sim=2
    # strict = 2/5 = 0.4 ; lenient = 3/5 = 0.6
    r = q41.precision_at(FIXTURE, 0.82)
    assert r["n_retained"] == 5
    assert r["tp_spelling_variant"] == 2
    assert r["boundary_length_mismatch"] == 1
    assert r["fp_low_similarity"] == 2
    assert abs(r["precision_strict"] - 0.4) < 1e-9
    assert abs(r["precision_lenient"] - 0.6) < 1e-9


def test_precision_at_higher_cutoff_drops_low_similarity():
    # cutoff 0.90 keeps rows with score >= 0.90: 2 spelling_variant + 1 length_mismatch
    r = q41.precision_at(FIXTURE, 0.90)
    assert r["n_retained"] == 3
    assert r["fp_low_similarity"] == 0
    assert abs(r["precision_strict"] - 2 / 3) < 1e-3
    assert r["precision_lenient"] == 1.0


def test_precision_at_empty_pool_is_none():
    r = q41.precision_at(FIXTURE, 0.99)
    assert r["n_retained"] == 0
    assert r["precision_strict"] is None
    assert r["precision_lenient"] is None


def test_score_stats_matches_hand_computation():
    stats = q41.score_stats([0.82, 0.85, 0.90, 0.95])
    assert stats["n"] == 4
    assert stats["min"] == 0.82
    assert stats["max"] == 0.95
    assert abs(stats["median"] - 0.875) < 1e-9
    assert abs(stats["mean"] - (0.82 + 0.85 + 0.90 + 0.95) / 4) < 1e-9


def test_score_stats_empty_is_none():
    assert q41.score_stats([]) is None


def test_load_gold_rejects_unknown_verdict(tmp_path, monkeypatch):
    bad_tsv = tmp_path / "bad.tsv"
    bad_tsv.write_text(
        "a_id\tb_id\tscore\tscript\tverdict\tnote\ta_text\tb_text\n"
        "x\ty\t0.9\tdeva\tsome_new_verdict\t\ta\tb\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(q41, "GOLD_TSV", bad_tsv)
    try:
        q41.load_gold()
        assert False, "expected ValueError on unknown verdict"
    except ValueError as e:
        assert "some_new_verdict" in str(e)


def test_real_gold_set_smoke_and_reproducibility():
    rows = q41.load_gold()
    assert len(rows) == 128
    verdicts = {r["verdict"] for r in rows}
    assert verdicts <= q41.KNOWN_VERDICTS
    assert all(0.82 <= r["score"] <= 1.0 for r in rows)

    op = q41.precision_at(rows, q41.OPERATING_THRESHOLD)
    assert op["n_retained"] == 128
    # deterministic on committed data — pin the actual counts so a silent
    # regeneration of matches_review.tsv is caught, not silently re-derived
    assert op["tp_spelling_variant"] == 58
    assert op["boundary_length_mismatch"] == 20
    assert op["fp_low_similarity"] == 50

    # raising the cutoff must never increase the retained pool or the FP count
    prev = None
    for tau in q41.SWEEP_CUTOFFS:
        cur = q41.precision_at(rows, tau)
        if prev is not None:
            assert cur["n_retained"] <= prev["n_retained"]
            assert cur["fp_low_similarity"] <= prev["fp_low_similarity"]
        prev = cur


def test_committed_json_matches_a_fresh_run(tmp_path, monkeypatch):
    """Committed scripts/data/q41_difflib_gold_evaluation.json must be
    byte-for-byte what main() would regenerate today (H5421-style drift
    guard) — catch a hand-edited or stale artifact."""
    monkeypatch.setattr(q41, "OUT_JSON", tmp_path / "out.json")
    monkeypatch.setattr(q41, "OUT_REPORT", tmp_path / "out.md")
    q41.main()
    fresh = json.loads((tmp_path / "out.json").read_text(encoding="utf-8"))
    committed = json.loads(q41.ROOT.joinpath(
        "scripts", "data", "q41_difflib_gold_evaluation.json"
    ).read_text(encoding="utf-8"))
    assert fresh == committed
