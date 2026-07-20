"""Commensurability gate — fails CI if any SANGRAM case article denominates its case counts
against a value that is not the one canonical case-marked total, or omits the master entirely (H1371).

This is the enforcement half of scripts/check_denominator_commensurability.py: the CI pytest job
already runs, so a PR that ships an incommensurable denominator (a drifted master, an unpinned
snapshot, or a case-cluster article with no case_bearing master) can never merge green.

- test_self_test: the checker's own logic (planted drift/gap/unpinned FAILs, a clean synthetic PASSes,
  the family arithmetic holds) — guards against the gate silently degrading to a no-op.
- test_registry_arithmetic: case_bearing == real_vibhakti + Cpd.
- test_cluster_present: every case-cluster article's coverage summary exists on disk.
- test_no_commensurability_drift: the real coverage summaries carry no violation.
- test_scan_flags_a_planted_gap: a synthetic case-cluster file missing the master IS caught.
"""
import json

import check_denominator_commensurability as dc


def test_self_test():
    assert dc.self_test() is True


def test_registry_arithmetic():
    assert dc.check_family_arithmetic(), (
        f"case_bearing {dc.CASE_BEARING:,} != real_vibhakti {dc.REAL_VIBHAKTI:,} + Cpd {dc.CPD:,}"
    )


def test_cluster_present():
    files, _ = dc.check_all()
    present = {f.parent.parent.name for f in files}
    missing = dc.CASE_CLUSTER - present
    assert not missing, f"case-cluster article(s) missing from disk: {sorted(missing)}"


def test_no_commensurability_drift():
    files, violations = dc.check_all()
    assert files, "no coverage_summary.json found — the gate would be a silent no-op"
    assert not violations, (
        "denominator-commensurability violation(s):\n" + "\n".join(f"  {v}" for v in violations)
    )


def test_scan_flags_a_planted_gap(tmp_path):
    d = tmp_path / "sangram" / "articles" / "karaka-case" / "data"
    d.mkdir(parents=True)
    (d / "coverage_summary.json").write_text(
        json.dumps({"denominators": {"all_tokens": dc.ALL_TOKENS}}), encoding="utf-8")
    viol = dc.check_file(d / "coverage_summary.json")
    assert any("case_bearing master" in v for v in viol), (
        "the gate failed to flag a case-cluster article missing the case_bearing master"
    )


def test_scan_flags_master_drift(tmp_path):
    d = tmp_path / "sangram" / "articles" / "instrumental-dative" / "data"
    d.mkdir(parents=True)
    (d / "coverage_summary.json").write_text(
        json.dumps({"denominators": {"case_bearing_tokens": 4_000_000}}), encoding="utf-8")
    viol = dc.check_file(d / "coverage_summary.json")
    assert any("master drift" in v for v in viol), "the gate failed to flag a drifted master value"
