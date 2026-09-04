"""Tests for the OxAlpha gate review pass: spec axis, heuristics, hunk cap."""
import sys
import unittest
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))

import oxalpha_gate_review as R  # noqa: E402


class SpecAxisTests(unittest.TestCase):
    def test_handoff_id_named(self):
        ax = R.spec_axis("Implements H3548 acceptance criteria.")
        self.assertEqual(ax["verdict"], "named")

    def test_issue_reference_named(self):
        ax = R.spec_axis("Fixes #412 for the funnel digest.")
        self.assertEqual(ax["verdict"], "named")

    def test_declared_absent(self):
        ax = R.spec_axis("No spec available - mechanical dependency bump.")
        self.assertEqual(ax["verdict"], "declared-absent")

    def test_absent_when_nothing_named(self):
        ax = R.spec_axis("Update stuff.")
        self.assertEqual(ax["verdict"], "absent")

    def test_not_applicable_without_pr_body(self):
        ax = R.spec_axis("")
        self.assertEqual(ax["verdict"], "not-applicable")


class HunkTests(unittest.TestCase):
    def test_heuristics_catch_dangerous_added_lines(self):
        hunks = [{"file": "ors_faq/newmod.py", "start": 10, "score": 0,
                  "added": [
                      {"line": 11, "text": "except:"},
                      {"line": 12, "text": "    pass"},
                      {"line": 13, "text": "api_key = \"sk-abcdef123456\""},
                  ]}]
        findings = R.heuristic_findings(hunks)
        modes = {f["failure_mode"] for f in findings}
        self.assertIn("bare except swallows KeyboardInterrupt/SystemExit", modes)
        self.assertIn("hardcoded credential in source", modes)
        cred = [f for f in findings if f["severity"] == "P0"][0]
        self.assertEqual(cred["file"], "ors_faq/newmod.py")
        self.assertEqual(cred["line"], 13)
        for f in findings:
            self.assertTrue(all(f.get(k) is not None for k in
                                ("severity", "file", "line", "failure_mode", "repro")))

    def test_clean_lines_produce_no_findings(self):
        hunks = [{"file": "tools/utm_audit.py", "start": 1, "score": 0,
                  "added": [{"line": 2, "text": "def total(rows):"},
                            {"line": 3, "text": "    return sum(rows)}"}]}]
        self.assertEqual(R.heuristic_findings(hunks), [])

    def test_max_ten_hunks_bounded(self):
        hunks = [{"file": "tools/x.py", "start": i, "score": i, "added": []}
                 for i in range(40)]
        hunks.sort(key=lambda h: (-h["score"], h["file"], h["start"]))
        self.assertLessEqual(len(hunks[:R.MAX_HUNKS]), R.MAX_HUNKS)

    def test_rubric_mentions_findings_shape(self):
        self.assertIn('"findings"', R.RUBRIC)
        self.assertIn("severity", R.RUBRIC)


if __name__ == "__main__":
    unittest.main()
