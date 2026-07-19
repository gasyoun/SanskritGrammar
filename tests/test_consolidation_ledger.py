"""Wires scripts/consolidation_ledger_refresh.py into CI (H1260).

The consolidation freeze ledger (sangram/editorial/data/consolidation_ledger.json)
is the machine-readable half of the H1260 freeze governance: every one of the
26 baseline candidate IDs must carry an explicit disposition before
freeze.active may flip to false, and a refresh run must NEVER silently drop or
duplicate a baseline ID, and must NEVER clobber a human verdict field
(disposition / blocking_note / source_links).

- test_self_test: the refresh script's own integrity + preservation suite.
- test_committed_ledger_has_exact_baseline: the committed ledger carries
  exactly the 26 frozen IDs (no more, no less) and the 9 published-context IDs.
- test_committed_ledger_is_fresh: re-running the refresh in-memory against the
  live repo state reproduces the committed non-judgmental fields (catches a
  ledger that was hand-edited out of sync with the repo it describes).
- test_disposition_totals_visible: the freeze-exit accounting
  (unknown/published/revised/rejected/kill_gated counts) is derivable and adds
  up to 26 — the DoD's "visible status totals" requirement.
"""
import json

import article_validate as av
import consolidation_ledger_refresh as clr


def _load_committed():
    return json.loads(clr.LEDGER_PATH.read_text(encoding="utf-8"))


def test_self_test():
    assert clr.self_test() == 0


def test_committed_ledger_has_exact_baseline():
    ledger = _load_committed()
    ids = [row["toc_ref"] for row in ledger["baseline_ids"]]
    assert len(ids) == 26, f"expected exactly 26 baseline rows, found {len(ids)}"
    assert len(set(ids)) == 26, "duplicate toc_ref in baseline_ids"
    assert set(ids) == {t for t, _ in clr.FROZEN_BASELINE}
    pub_ids = [row["toc_ref"] for row in ledger["published_context"]]
    assert len(pub_ids) == 9
    assert len(set(pub_ids)) == 9
    assert set(pub_ids) == {t for t, _ in clr.PUBLISHED_AT_FREEZE}
    assert set(ids).isdisjoint(pub_ids), "an ID cannot be both a baseline candidate and published-context"
    assert ledger["freeze"]["counts"] == {
        "published_at_freeze": 9, "candidate_at_freeze": 26, "total_at_freeze": 35,
    }


def test_committed_ledger_is_fresh():
    committed = _load_committed()
    fresh = clr.build_ledger(committed["last_refresh"]["date"], committed["last_refresh"]["build_status"])
    # Compare everything except the two fields that are legitimately
    # machine/timing-dependent even between two runs against the same repo
    # state: validator_evidence.checked_at (wall-clock) and visa_evidence
    # (depends on whether the local, gitignored review/ dir is present on
    # THIS machine — see consolidation_ledger_refresh.py's module docstring).
    def strip(ledger):
        out = json.loads(json.dumps(ledger))
        for row in out["baseline_ids"]:
            row["validator_evidence"]["checked_at"] = None
            row["visa_evidence"] = None
        return out
    assert strip(committed) == strip(fresh), (
        "the committed consolidation_ledger.json is stale relative to the repo state — "
        "run: python scripts/consolidation_ledger_refresh.py"
    )


def test_disposition_totals_visible():
    ledger = _load_committed()
    totals = clr.status_totals(ledger)
    assert sum(totals.values()) == 26
    assert set(totals) == {"unknown", "published", "revised", "rejected", "kill_gated"}


def test_freeze_ledger_is_schema_valid():
    try:
        import jsonschema
    except ImportError:
        return  # optional dependency, same fallback posture as article_validate.py
    schema = json.loads(clr.SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(_load_committed(), schema)


def test_article_validate_agrees_ledger_is_the_same_one_it_loads():
    # Both scripts must point at the same physical file — a path drift between
    # them would silently split the freeze gate from the ledger it enforces.
    assert av.FREEZE_LEDGER_PATH == clr.LEDGER_PATH
