"""Drift gate — fails CI if any claim register cites a superseded corpus figure as a
live number (H1140).

This is the enforcement half of scripts/check_claims_consistency.py: the CI pytest job
already runs, so making the cross-register figure check a test means a PR that reintroduces
a stale figure (e.g. the pre-refresh aorist count 2,452 / 0.31%) can never merge green.

- test_self_test: the checker's own scan logic (stale-without-marker FAILs, corrected PASSes).
- test_no_drift_in_registers: the real */claims.yml carry no undocumented superseded figure.
- test_scan_flags_a_planted_stale: a synthetic stale citation is caught (guards against the
  gate silently degrading to a no-op).
- test_cross_repo_*: the H2298 figure contract with VisualDCS, including the retrodiction —
  the pre-H1486 published Imperfect Active (4,442) must FAIL. A gate that would not have
  caught the divergence it was built for is not a gate.
"""
import json

import pytest

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


# ---------------------------------------------------------------------------
# check 3 — the cross-repo figure contract with VisualDCS (H2298)
# ---------------------------------------------------------------------------

def _published():
    if not cc.PUBLISHED_FIGURES.is_file():
        pytest.fail(f"{cc.PUBLISHED_FIGURES} is missing — the cross-repo gate has no input "
                    f"and would silently pass; run scripts/refresh_published_figures.py")
    return cc.load_published()


def _ours():
    return json.loads(cc.OUR_DCS2021_STATS.read_text(encoding="utf-8"))


def test_vendored_asset_is_list_shaped_with_units():
    """The asset must not carry the very defect it is published to detect."""
    figures = _published()
    assert isinstance(figures, list) and figures
    for f in figures:
        assert f.get("unit"), f"{f['id']}: `unit` is mandatory"
        assert f.get("basis"), f"{f['id']}: `basis` must name the denominator"
        assert f.get("source_codes"), f"{f['id']}: `source_codes` must be explicit"


def test_cross_repo_contract_holds_on_real_data():
    v = cc.cross_repo_violations(_published(), _ours())
    assert not v, ("our DCS-2021 figures disagree with what VisualDCS publishes:\n"
                   + "\n".join(f"  [{kind}] {name}: {detail}" for name, kind, detail in v))


def test_every_seeded_pair_actually_resolves():
    """Guards against the gate degrading to a no-op through a renamed id or stats key."""
    published, ours = _published(), _ours()
    assert cc.CROSS_REPO_FIGURES, "no seeded pairs — the check would be vacuous"
    ids = {f["id"] for f in published}
    for fig in cc.CROSS_REPO_FIGURES:
        assert set(fig["published"]) <= ids, f"{fig['name']}: unknown published id(s)"
        assert cc._dig(ours, fig["ours_path"]) is not None, \
            f"{fig['name']}: {'.'.join(fig['ours_path'])} missing from claims_dcs_stats.json"


def test_retrodiction_pre_h1486_figure_is_caught():
    """THE acceptance criterion: plant the figure VisualDCS actually published for months.

    4,442 is code 8 alone — what a name-keyed reader produced by letting code 8 overwrite
    code 4 (35,921). If this gate would not have failed on it, it would not have caught the
    divergence it was built for.
    """
    published = [f if f["id"] != "dcs2021_imperfect_active" else dict(f, value=4442)
                 for f in _published()]
    v = [x for x in cc.cross_repo_violations(published, _ours())
         if x[0] == "DCS-2021 imperfect active"]
    assert v, "RETRODICTION FAILED: the pre-H1486 figure 4,442 was not caught"
    assert v[0][1] == "drift"


def test_planted_divergence_in_each_seeded_pair_is_caught():
    """Every seeded row must be load-bearing — not just the imperfect one."""
    ours = _ours()
    for fig in cc.CROSS_REPO_FIGURES:
        target = fig["published"][0]
        published = [f if f["id"] != target else dict(f, value=f["value"] + 10_000)
                     for f in _published()]
        v = [x for x in cc.cross_repo_violations(published, ours) if x[0] == fig["name"]]
        assert v, f"{fig['name']}: a planted +10,000 divergence was NOT caught"


def test_changed_code_set_is_incommensurable_not_drift():
    """A different code set means the sides stopped measuring the same thing.

    Reporting that as 'drift' would tell a maintainer to edit a number until it matches —
    the wrong fix, and how a types-vs-tokens pair gets silently reconciled to nonsense.
    """
    published = [f if f["id"] != "dcs2021_imperfect_active"
                 else dict(f, source_codes=[4, 8, 9]) for f in _published()]
    v = [x for x in cc.cross_repo_violations(published, _ours())
         if x[0] == "DCS-2021 imperfect active"]
    assert v and v[0][1] == "incommensurable", f"code-set change misreported: {v}"


def test_missing_asset_fails_loudly_rather_than_skipping(tmp_path):
    """A cross-repo gate that skips itself when its input is absent is a gate that passes."""
    p = tmp_path / "figs.json"
    p.write_text('{"figures": {"dcs2021_imperfect_active": 4442}}', encoding="utf-8")
    with pytest.raises(ValueError):
        cc.load_published(p)
