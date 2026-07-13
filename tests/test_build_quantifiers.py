"""Characterization tests for build_quantifiers' pure metric helpers.

bar renders a 20-cell ASCII share meter; sample_metrics derives the
precision/recall/agreement confusion-matrix stats from a human-vs-auto anchor
sample; pop_estimate un-stratifies the sample to a population share.
"""
import build_quantifiers as bq


class TestBar:
    def test_zero_is_all_dots(self):
        assert bq.bar(0) == "·" * 20

    def test_full_is_all_blocks(self):
        assert bq.bar(100) == "█" * 20

    def test_half(self):
        assert bq.bar(50) == "█" * 10 + "·" * 10

    def test_rounds_to_nearest_cell(self):
        # 12.5 / 5 = 2.5 -> rounds to 2 filled cells (banker's rounding).
        assert bq.bar(12.5) == "█" * 2 + "·" * 18


class TestSampleMetrics:
    def test_confusion_matrix_and_rates(self):
        sample = {"sample": [
            {"auto_anchored": True, "human_anchored": True},                          # tp
            {"auto_anchored": True, "human_anchored": False, "note": "lexicon-FP x"},  # fp (lexicon)
            {"auto_anchored": False, "human_anchored": True},                         # fn
            {"auto_anchored": False, "human_anchored": False},                        # tn
            {"auto_anchored": True, "human_anchored": None},                          # excluded
        ]}
        m = bq.sample_metrics(sample)
        assert (m["n"], m["tp"], m["fp"], m["fn"], m["tn"]) == (4, 1, 1, 1, 1)
        assert m["precision"] == 50.0
        assert m["recall"] == 50.0
        assert m["agreement"] == 50.0
        assert m["miss_rate"] == 0.5
        assert m["lexicon_fp"] == 1

    def test_no_scored_rows_returns_none(self):
        assert bq.sample_metrics({"sample": [{"auto_anchored": True, "human_anchored": None}]}) is None


class TestPopEstimate:
    def test_unstratifies_sample_to_population(self):
        s = {"precision": 50.0, "miss_rate": 0.5}
        # 40% auto-anchored: 0.4*0.5 + 0.6*0.5 = 0.5 -> 50.0%
        assert bq.pop_estimate(40, s) == 50.0
