"""Wires scripts/article_validate.py's own --self-test into CI (H1260).

Before this file, `article_validate.py --self-test` and `--all` were manual-only
checks — nothing in tests/ (the suite `python -m pytest` actually runs in CI,
see .github/workflows/ci.yml) exercised them, so a regression in the C4
editorial-contract validator, OR in the new H1260 consolidation-freeze gate,
could land on main without CI ever noticing.

- test_self_test: the validator's own fixture + mutation-case + freeze-gate
  suite (article_validate.self_test()).
- test_all_real_manifests_pass: every committed sangram/articles/*/
  article.manifest.json (35 at H1260-time) validates clean right now — a
  concrete regression gate distinct from the fixture-only self-test.
- test_freeze_gate_rejects_new_toc_ref / test_freeze_gate_allows_baseline_toc_ref:
  the H1260 positive/negative freeze-gate cases, written directly against
  validate() (not just via self_test()) so a future self_test() refactor can't
  silently drop freeze coverage without pytest also catching it.
- test_freeze_gate_inactive_ledger_bypasses: freeze.active=false must not
  reject anything, proving the gate is a freeze-scoped mechanism, not a
  permanent closed-world toc_ref allowlist.
"""
import copy
import json

import article_validate as av


def test_self_test():
    assert av.self_test() == 0


def test_all_real_manifests_pass():
    targets = sorted(av.HERE.parent.glob("sangram/**/article.manifest.json"))
    assert targets, "no article.manifest.json files found — the glob would be a silent no-op"
    failures = []
    for p in targets:
        serialized = p.read_text(encoding="utf-8")
        manifest = json.loads(serialized)
        errors, _warnings = av.validate(manifest, serialized)
        if errors:
            failures.append((str(p), errors))
    assert not failures, "\n".join(f"{p}: {e}" for p, e in failures)


def _fixture():
    serialized = av.FIXTURE_PATH.read_text(encoding="utf-8")
    return json.loads(serialized), serialized


def test_freeze_gate_rejects_new_toc_ref():
    active, allowed, warn = av.load_freeze_baseline()
    assert warn is None, f"could not load the real consolidation ledger: {warn}"
    assert active is True, "H1260 freeze should be active — if it was lifted, update this test"
    fixture, _ = _fixture()
    m = copy.deepcopy(fixture)
    m["article"]["toc_ref"] = "SG-MO-999"  # not a member of the frozen 35-ID baseline
    errors, _ = av.validate(m, json.dumps(m, ensure_ascii=False))
    assert any("freeze active" in e for e in errors), errors


def test_freeze_gate_allows_baseline_toc_ref():
    active, allowed, warn = av.load_freeze_baseline()
    assert warn is None and active and allowed
    baseline_toc_ref = sorted(allowed)[0]
    fixture, _ = _fixture()
    m = copy.deepcopy(fixture)
    m["article"]["toc_ref"] = baseline_toc_ref
    errors, _ = av.validate(m, json.dumps(m, ensure_ascii=False))
    assert not any("freeze active" in e for e in errors), errors


def test_freeze_gate_inactive_ledger_bypasses(tmp_path):
    ledger = tmp_path / "consolidation_ledger.json"
    ledger.write_text(json.dumps({
        "freeze": {"active": False}, "baseline_ids": [], "published_context": [],
    }), encoding="utf-8")
    active, allowed, warn = av.load_freeze_baseline(ledger)
    assert warn is None
    assert active is False
    assert allowed == set()


def test_freeze_gate_missing_ledger_warns_not_crashes(tmp_path):
    active, allowed, warn = av.load_freeze_baseline(tmp_path / "does-not-exist.json")
    assert active is False
    assert allowed is None
    assert warn is not None
