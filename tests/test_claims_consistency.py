"""Drift gate — fails CI if any claim register cites a superseded corpus figure as a
live number (H1140).

This is the enforcement half of scripts/check_claims_consistency.py: the CI pytest job
already runs, so making the cross-register figure check a test means a PR that reintroduces
a stale figure (e.g. the pre-refresh aorist count 2,452 / 0.31%) can never merge green.

- test_self_test: the checker's own scan logic (stale-without-marker FAILs, corrected PASSes).
- test_no_drift_in_registers: the real */claims.yml carry no undocumented superseded figure.
- test_scan_flags_a_planted_stale: a synthetic stale citation is caught (guards against the
  gate silently degrading to a no-op).
"""
import check_claims_consistency as cc


def test_self_test():
    assert cc.self_test() is True


def test_no_supersession_drift_in_registers():
    files, violations = cc.check_all()
    assert files, "no */claims.yml registers found — the check would be a silent no-op"
    assert not violations, (
        "superseded corpus figure(s) cited as a live number without a correction marker:\n"
        + "\n".join(f"  {book} [{bid}] {name}" for book, bid, name in violations)
    )


def test_no_consistency_drift_in_registers():
    files, _ = cc.check_all()
    v = cc.consistency_violations(files)
    assert not v, (
        "shared corpus figure(s) cited with a value outside the allowed set:\n"
        + "\n".join(f"  {book} [{bid}] {name} = {val}, allowed {allowed}"
                    for name, book, bid, val, allowed in v)
    )


def test_scan_flags_a_planted_stale(tmp_path):
    p = tmp_path / "claims.yml"
    p.write_text('entries:\n\n  - id: Z-1\n    number: "aorist 2,452 tokens = 0.31% of verbal"\n',
                 encoding="utf-8")
    assert cc.scan_file(p), "the gate failed to flag a planted stale aorist figure"


def test_corrected_mention_is_allowed(tmp_path):
    p = tmp_path / "claims.yml"
    p.write_text('entries:\n\n  - id: Z-2\n    number: "aorist 12,054 (feat_formation); '
                 'REFRESHED from 2,452 / 0.31% which undercounted root+thematic"\n', encoding="utf-8")
    assert not cc.scan_file(p), "a documented correction should not be flagged"
