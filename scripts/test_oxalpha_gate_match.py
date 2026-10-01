"""Tests for the OxAlpha gate executable-path matcher (design section 1)."""
import sys
import unittest
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))

import oxalpha_gate_match as M  # noqa: E402


class MatcherTests(unittest.TestCase):
    def test_executable_prefixes_match(self):
        for p in ("scripts/build_catalog.py", "tools/story_chapter_budget_check.py",
                  "pipelines/contract.py", "packages/sg_tooling/src/x.py",
                  "src/discovery.mjs", "apps/site/config.ts",
                  "patches/vendor-fix.patch", ".github/workflows/ci.yml",
                  "tests/test_visa_sheet_generator.py",
                  ".githooks/pre-push"):
            self.assertTrue(M.is_executable(p), p)

    def test_root_config_files_match(self):
        self.assertTrue(M.is_executable("docusaurus.config.mjs"))
        self.assertTrue(M.is_executable("sidebars.mjs"))

    def test_excluded_by_default_do_not_match(self):
        for p in ("content/lesson.mdx", "data/dataset.csv",
                  "CHANGELOG.md", ".ai_state.md", "README.md",
                  "docs/OXALPHA_STATUS_GATE_DESIGN_2026.md",
                  "sangram/editorial/data/consolidation_ledger.json",
                  "static/app.min.js", "package-lock.json"):
            self.assertFalse(M.is_executable(p), p)

    def test_generated_mdx_excluded_even_inside_prefix(self):
        self.assertFalse(M.is_executable("apps/site/generated/page.mdx"))
        self.assertFalse(M.is_executable("src/bundle.min.js"))

    def test_pycache_node_modules_excluded_inside_prefix(self):
        for p in ("scripts/__pycache__/x.py", "src/node_modules/x.js"):
            self.assertFalse(M.is_executable(p), p)

    def test_claims_yml_sensitive_anywhere(self):
        self.assertTrue(M.is_sensitive("GrammarRelations/claims.yml"))
        self.assertTrue(M.is_sensitive("claims.yml"))
        self.assertFalse(M.is_sensitive("scripts/build_catalog.py"))

    def test_sensitive_paths_flagged(self):
        for p in (".github/workflows/deploy.yml", ".githooks/pre-push",
                  "scripts/pre_push_stale_base_check.py", "scripts/eol_census.py",
                  "scripts/check_claims_consistency.py",
                  "scripts/refresh_published_figures.py",
                  "scripts/build_lessonpack.py"):
            self.assertTrue(M.is_sensitive(p), p)

    def test_classify_splits_and_sorts(self):
        out = M.classify(["CHANGELOG.md", "scripts/build_catalog.py",
                          "scripts/__pycache__/x.py", "content/x.mdx"])
        self.assertEqual(out["matched_paths"], ["scripts/build_catalog.py"])
        self.assertEqual(out["skipped_paths"],
                         ["CHANGELOG.md", "content/x.mdx",
                          "scripts/__pycache__/x.py"])
        self.assertTrue(out["executable"])

    def test_zero_match_is_a_valid_skip_outcome(self):
        out = M.classify(["CHANGELOG.md", "README.md", "content/page.mdx"])
        self.assertFalse(out["executable"])
        self.assertEqual(out["matched_paths"], [])


class CliTests(unittest.TestCase):
    def test_main_gha_outputs_zero_match(self):
        import subprocess
        repo = Path(__file__).resolve().parent.parent
        proc = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "oxalpha_gate_match.py"),
             "--base", "HEAD", "--head", "HEAD", "--repo", str(repo), "--gha"],
            capture_output=True, text=True, encoding="utf-8", timeout=60)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("executable=false", proc.stdout)

    def test_main_out_record_written(self):
        import json
        import subprocess
        import tempfile
        repo = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "match.json"
            proc = subprocess.run(
                [sys.executable, str(Path(__file__).parent / "oxalpha_gate_match.py"),
                 "--base", "HEAD", "--head", "HEAD", "--repo", str(repo),
                 "--out", str(out)],
                capture_output=True, text=True, encoding="utf-8", timeout=60)
            self.assertEqual(proc.returncode, 0)
            rec = json.loads(out.read_text(encoding="utf-8"))
            self.assertIn("executable", rec)
            self.assertIn("sensitive_paths", rec)


if __name__ == "__main__":
    unittest.main()
