"""Tests for the repository-gates runner (H4074)."""
import json
import sys
import unittest
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))

import oxalpha_gate_gates as G  # noqa: E402


class GatesTests(unittest.TestCase):
    def test_run_gate_list_spawn_no_shell(self):
        # Regression (first live gate run): shell=True was flagged P1 by the
        # gate itself. The runner must spawn via argv list, not /bin/sh.
        rec = G.run_gate("echo", "echo hi", True, ".", 30)
        self.assertTrue(rec["ok"])
        self.assertIn("hi", rec["output_tail"])

    def test_run_gate_failure_recorded(self):
        rec = G.run_gate("false-gate", "false", True, ".", 30)
        self.assertFalse(rec["ok"])
        self.assertEqual(rec["rc"], 1)

    def test_hard_flag_carried(self):
        rec = G.run_gate("soft", "echo hi", False, ".", 30)
        self.assertFalse(rec["hard"])

    def test_source_has_no_shell_true(self):
        src = Path(__file__).parent.joinpath("oxalpha_gate_gates.py").read_text(
            encoding="utf-8")
        self.assertNotIn("shell=True", src)


if __name__ == "__main__":
    unittest.main()
