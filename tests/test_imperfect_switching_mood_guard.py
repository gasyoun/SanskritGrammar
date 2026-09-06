"""H3966 regression guard: `imperfect_switching_stats.py` must never lose `feat_mood='Ind'`.

The defect this pins (H3878 finding G22, VisualDCS): DCS never assigns `Formation` outside
the indicative — 17,440 occurrences in the pinned dcs-conllu `04e0778` snapshot, not one of
them non-indicative. The study's `PERF` bucket is defined as `Tense=Past` with `Formation`
absent, so with finiteness filtered by `feat_person IS NOT NULL` alone, every finite
non-indicative past token lands in `PERF` **by construction**: 8,726 of 85,955 (10.15 %) —
Jus 4,067, Imp 1,700, Sub 1,317, Opt 1,065, Prec 577. That is what shipped as v0.48.0 and
what the v0.49 re-run corrected.

The tests are hermetic — they import the module and read its SQL, and never open the 920 MB
snapshot, so they run in CI where the DCS master is absent.
"""
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
MODULE_PATH = ROOT / "ZalizniakOcherk_1978" / "imperfect_switching_stats.py"


def _load():
    """Import the study module by path (it lives beside its book, not in scripts/)."""
    sys.path.insert(0, str(MODULE_PATH.parent))
    try:
        spec = importlib.util.spec_from_file_location("imperfect_switching_stats", MODULE_PATH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    finally:
        sys.path.remove(str(MODULE_PATH.parent))


@pytest.fixture(scope="module")
def mod():
    return _load()


class TestMoodGuardPresent:
    def test_guard_is_the_indicative(self, mod):
        assert mod.MOOD_INDICATIVE == "Ind"
        assert mod.MOOD_GUARD_SQL == "feat_mood='Ind'"

    def test_every_cat_sql_branch_carries_the_guard(self, mod):
        branches = mod.CAT_SQL.split("WHEN")[1:]
        assert len(branches) == 3, "CAT_SQL should classify exactly IMPF, PERF and AOR"
        for branch in branches:
            assert mod.MOOD_GUARD_SQL in branch, (
                "a CAT_SQL branch lost the mood guard:\n" + branch
            )

    def test_all_three_categories_still_produced(self, mod):
        for cat in ("'IMPF'", "'PERF'", "'AOR'"):
            assert cat in mod.CAT_SQL

    def test_finiteness_filter_and_guard_are_both_applied(self, mod):
        # The WHERE clause filters finiteness; the guard rides inside CAT_SQL, which the
        # same clause re-evaluates as `IS NOT NULL`. Dropping either half re-opens H3878.
        source = MODULE_PATH.read_text(encoding="utf-8")
        assert "t.feat_person IS NOT NULL AND ({CAT_SQL}) IS NOT NULL" in source


class TestMoodGuardEnforcement:
    def test_assert_mood_guard_passes_as_shipped(self, mod):
        mod.assert_mood_guard()  # must not raise

    def test_assert_mood_guard_refuses_the_pre_h3966_sql(self, mod, monkeypatch):
        pre_h3966 = """
        CASE
          WHEN feat_tense='Impf' THEN 'IMPF'
          WHEN feat_tense='Past' AND feat_formation IS NULL THEN 'PERF'
          WHEN feat_tense='Past' AND feat_formation IN ('root','them') THEN 'AOR'
        END
        """
        monkeypatch.setattr(mod, "CAT_SQL", pre_h3966)
        with pytest.raises(SystemExit) as excinfo:
            mod.assert_mood_guard()
        assert "H3966" in str(excinfo.value)

    def test_assert_mood_guard_refuses_a_partially_guarded_sql(self, mod, monkeypatch):
        # The realistic regression: someone guards PERF only, reasoning that IMPF and AOR
        # are clean anyway. They are — today, in this snapshot. The guard stays uniform so
        # the claim does not silently depend on that.
        half_guarded = """
        CASE
          WHEN feat_tense='Impf' THEN 'IMPF'
          WHEN feat_mood='Ind' AND feat_tense='Past' AND feat_formation IS NULL THEN 'PERF'
          WHEN feat_mood='Ind' AND feat_tense='Past' AND feat_formation IN ('s') THEN 'AOR'
        END
        """
        monkeypatch.setattr(mod, "CAT_SQL", half_guarded)
        with pytest.raises(SystemExit):
            mod.assert_mood_guard()


class TestPreRegistrationRecordIsProtected:
    def test_guarded_run_writes_its_own_file(self, mod):
        assert mod.OUT.name == "imperfect_switching_stats_v049.json"

    def test_legacy_v048_json_is_never_the_output_target(self, mod):
        assert mod.LEGACY_OUT.name == "imperfect_switching_stats.json"
        assert mod.OUT != mod.LEGACY_OUT

    def test_frozen_design_constants_survived_the_re_run(self, mod):
        # The prereg (T2607-26) fixes these; a re-run that quietly retunes them is not a
        # re-run of the registered study.
        assert mod.SEED == 20260717
        assert mod.N_PERM == 1000
        assert mod.WINDOW_SENTS == 5
        assert mod.CHAIN_NEIGHBOURS == 6
        assert mod.CHAIN_MIN_PERF == 4
        assert mod.AOR_FORMATIONS == ("root", "them", "s", "is", "red", "sa", "sis")
