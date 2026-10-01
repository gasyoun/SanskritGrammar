"""Tests for the OxAlpha gate conclusion state machine (design sections 3/5)."""
import sys
import unittest
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))

import oxalpha_gate_conclude as C  # noqa: E402


def gates(ok=True, hard=True, name="pytest"):
    return {"ran": True,
            "gates": [{"name": name, "ok": ok, "hard": hard, "rc": 0 if ok else 1,
                       "output_tail": "479 passed" if ok else "FAILED"}]}


def review(findings=None, spec="named"):
    axes = [{"axis": "spec", "verdict": spec, "evidence": spec},
            {"axis": "standards", "verdict": "ran", "evidence": "heuristics: ran",
             "lanes": []}]
    return {"axes": axes, "findings": findings or [], "hunks_reviewed": []}


class ConcludeTests(unittest.TestCase):
    def test_zero_match_is_skip_even_with_green_gates(self):
        out = C.conclude("false", {"matched_paths": [], "sensitive_paths": []},
                         gates(), review())
        self.assertEqual(out["state"], "skip")

    def test_zero_match_without_gates_still_skip(self):
        out = C.conclude("false", {"matched_paths": []}, None, None)
        self.assertEqual(out["state"], "skip")

    def test_hard_gate_failure_is_fail(self):
        out = C.conclude("true", {"matched_paths": ["ors_faq/bot.py"]},
                         gates(ok=False, hard=True), review())
        self.assertEqual(out["state"], "fail")
        self.assertIn("gate pytest failed", out["reasons"][0])

    def test_soft_gate_failure_does_not_fail(self):
        out = C.conclude("true", {"matched_paths": ["scripts/x.py"]},
                         gates(ok=False, hard=False, name="black"),
                         review())
        self.assertEqual(out["state"], "pass")

    def test_p0_finding_is_fail_with_evidence(self):
        f = {"severity": "P0", "file": "ors_faq/bot.py", "line": 12,
             "failure_mode": "hardcoded credential", "repro": "r1"}
        out = C.conclude("true", {"matched_paths": ["ors_faq/bot.py"]},
                         gates(), review(findings=[f]))
        self.assertEqual(out["state"], "fail")
        self.assertTrue(any("P0" in r for r in out["reasons"]))

    def test_p2_finding_is_pass_with_note(self):
        f = {"severity": "P2", "file": "scripts/x.py", "line": 3,
             "failure_mode": "subprocess without timeout", "repro": "r2"}
        out = C.conclude("true", {"matched_paths": ["scripts/x.py"]},
                         gates(), review(findings=[f]))
        self.assertEqual(out["state"], "pass")

    def test_spec_absent_is_fail(self):
        out = C.conclude("true", {"matched_paths": ["scripts/x.py"]},
                         gates(), review(spec="absent"))
        self.assertEqual(out["state"], "fail")

    def test_missing_review_on_matched_delta_is_infrastructure_fail(self):
        out = C.conclude("true", {"matched_paths": ["scripts/x.py"]}, gates(), None)
        self.assertEqual(out["state"], "fail")
        self.assertTrue(any("infrastructure" in r for r in out["reasons"]))

    def test_unknown_match_output_is_infrastructure_fail(self):
        out = C.conclude("unknown", None, None, None)
        self.assertEqual(out["state"], "fail")

    def test_pass_on_clean_matched_delta(self):
        out = C.conclude("true", {"matched_paths": ["scripts/x.py"],
                                  "sensitive_paths": []}, gates(), review())
        self.assertEqual(out["state"], "pass")
        self.assertTrue(any("ran clean" in r for r in out["reasons"]))

    def test_sensitive_paths_reported_on_pass(self):
        out = C.conclude("true", {"matched_paths": ["ors_faq/bot.py"],
                                  "sensitive_paths": ["ors_faq/bot.py"]},
                         gates(), review())
        self.assertTrue(any("human approval" in r for r in out["reasons"]))

    def test_ledger_row_shape(self):
        row = C.ledger_row(C.conclude("true", {"matched_paths": []}, None, None),
                           None, "412")
        self.assertIn('"pr": 412', row)
        self.assertIn('"state"', row)

    def test_render_mentions_never_silent(self):
        text = C.render(C.conclude("false", {"matched_paths": []}, None, None),
                        None, None)
        self.assertIn("silent record", text)


if __name__ == "__main__":
    unittest.main()
