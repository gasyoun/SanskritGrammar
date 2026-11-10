"""Offline orchestration fixtures for the nightly ledger refresh PR (H7967).

Proves the fail-closed contract of
``scripts/consolidation_ledger_pr_orchestrate.py`` without touching a network
or a repo:

* two changed runs reuse the SAME rolling branch and the SAME PR -- the update
  path never calls ``gh pr create`` while the PR is open;
* a no-change run performs zero mutations and creates no PR;
* a refreshed diff touching anything outside the ledger fails closed before
  any git/gh mutation (the exact single-file scope guard);
* an unrelated branch/PR is never updated -- the unowned-tip case fails closed
  with zero mutations, and no command in any scenario ever names a branch
  other than ``chore/ledger-refresh`` (legacy dated refresh branches/PRs stay
  untouched).

Also wires ``.github/workflows/consolidation-ledger-nightly.yml`` to the
orchestrator (same assertion style as ``test_same_sha_workflow.py``).
"""
from __future__ import annotations

import consolidation_ledger_pr_orchestrate as orch

LEDGER = orch.LEDGER_REL
ROLLING = orch.ROLLING_BRANCH
SHA1 = "a" * 40
SHA2 = "b" * 40
FOREIGN_DATED_BRANCH = "chore/ledger-refresh-20261105"
FOREIGN_PR_BRANCH = "chore/someone-elses-fix"

# Read-only probes vs mutations (the fail-closed guarantees are about mutation).
_PROBE_GIT = {"diff", "ls-remote", "fetch", "log"}
_PROBE_GH = {("pr", "list")}


def _is_mutation(tool, args):
    if tool == "git":
        return args[0] not in _PROBE_GIT
    if tool == "gh":
        return tuple(args[:2]) not in _PROBE_GH
    return True


class FakeRunner:
    """Records every invocation; answers scripted probe results by exact call."""

    def __init__(self, responses=None):
        self.calls = []
        self.responses = dict(responses or {})

    def run(self, tool, *args):
        self.calls.append((tool, args))
        return self.responses.get((tool,) + args, (0, "", ""))

    def mutations(self):
        return [(t, a) for t, a in self.calls if _is_mutation(t, a)]

    def argv_text(self):
        return [" ".join((t,) + a) for t, a in self.calls]


def _state(changed=True, branch=False, tip="", owned=False, pr=False):
    files = (LEDGER,) if changed else ()
    return orch.RemoteState(files, branch, tip, owned, pr)


def _pr_list_response(*numbers):
    body = "[" + ",".join('{"number":%d}' % n for n in numbers) + "]"
    return ("gh", "pr", "list", "--head", ROLLING, "--state", "open",
            "--json", "number"), (0, body, "")


def _is_pr_create(call):
    return call[0] == "gh" and call[1][:2] == ("pr", "create")


def test_two_changed_runs_reuse_the_same_branch_and_pr():
    # Run 1: nothing on the remote -> create branch + PR once.
    r1 = FakeRunner()
    rc = orch.execute(orch.plan(_state(changed=True)), r1)
    assert rc == 0
    assert len([c for c in r1.calls if _is_pr_create(c)]) == 1
    assert ("git", ("push", "origin", f"HEAD:refs/heads/{ROLLING}")) in r1.calls

    # Run 2: same rung, new refresh -> same branch, same PR, no new PR.
    r2 = FakeRunner()
    plan2 = orch.plan(_state(changed=True, branch=True, tip=SHA1, owned=True, pr=True))
    rc = orch.execute(plan2, r2)
    assert rc == 0
    assert not [c for c in r2.calls if _is_pr_create(c)], \
        "a second PR must never be created while the rolling PR is open"
    assert ("git", ("push", f"--force-with-lease=refs/heads/{ROLLING}:{SHA1}",
                    "origin", f"HEAD:refs/heads/{ROLLING}")) in r2.calls
    # Exactly one PR created across both runs; both runs named the same branch.
    assert sum(1 for c in r1.calls + r2.calls if _is_pr_create(c)) == 1
    for text in r1.argv_text() + r2.argv_text():
        for branchish in (ROLLING + "-", FOREIGN_PR_BRANCH):
            assert branchish not in text


def test_no_change_run_creates_no_pr_and_touches_nothing():
    r = FakeRunner()
    rc = orch.execute(orch.plan(_state(changed=False, branch=True, tip=SHA1,
                                       owned=True, pr=False)), r)
    assert rc == 0
    assert r.calls == [], "a no-change run must perform zero git/gh calls"
    assert not [c for c in r.calls if c[0] == "gh"]


def test_unrelated_changes_fail_closed_before_any_mutation():
    state = orch.RemoteState((LEDGER, "README.md"), False, "", False, False)
    r = FakeRunner()
    rc = orch.execute(orch.plan(state), r)
    assert rc == 1
    assert r.calls == [], "fail-closed means no command runs at all"
    assert "README.md" in orch.plan(state).reason


def test_unowned_rolling_branch_is_never_updated():
    # Somebody else's work sits on the rolling name: tip lacks the marker.
    state = _state(changed=True, branch=True, tip=SHA2, owned=False, pr=True)
    r = FakeRunner()
    rc = orch.execute(orch.plan(state), r)
    assert rc == 1
    assert r.calls == [], "an unowned branch is never force-updated"
    assert orch.plan(state).outcome == "fail"


def test_unrelated_branches_and_prs_are_never_named():
    # A legacy dated refresh branch and a foreign PR exist; the rolling branch
    # does not. The create path must name nothing but the rolling branch.
    r = FakeRunner({
        ("git", "ls-remote", "--heads", "origin", ROLLING): (0, "", ""),
    })
    state, err = orch.collect_state(r)
    assert err is None and state is not None and not state.branch_exists
    rc = orch.execute(orch.plan(_state(changed=True)), r)
    assert rc == 0
    for text in r.argv_text():
        assert FOREIGN_DATED_BRANCH not in text
        assert FOREIGN_PR_BRANCH not in text
        for chunk in text.split():
            if chunk.startswith("chore/") or chunk.startswith("refs/heads/chore/"):
                assert ROLLING in chunk, f"unexpected branch name in: {text}"


def test_collect_state_parses_probes_and_ownership():
    responses = {
        ("git", "diff", "--name-only"): (0, f"{LEDGER}\n", ""),
        ("git", "ls-remote", "--heads", "origin", ROLLING):
            (0, f"{SHA1}\trefs/heads/{ROLLING}\n", ""),
        ("git", "log", "-1", "--format=%B", SHA1):
            (0, orch.OWNER_MARKER + "\n\nbody\n", ""),
        _pr_list_response(7)[0]: _pr_list_response(7)[1],
    }
    state, err = orch.collect_state(FakeRunner(responses))
    assert err is None
    assert state.changed_files == (LEDGER,)
    assert state.branch_exists and state.branch_tip_sha == SHA1
    assert state.branch_tip_owned and state.open_pr

    responses[("git", "log", "-1", "--format=%B", SHA1)] = (0, "not ours\n", "")
    state, err = orch.collect_state(FakeRunner(responses))
    assert err is None and not state.branch_tip_owned

    responses[("git", "ls-remote", "--heads", "origin", ROLLING)] = (0, "", "")
    state, err = orch.collect_state(FakeRunner(responses))
    assert err is None and not state.branch_exists and not state.open_pr


def test_probe_failure_is_not_silently_skipped():
    # A branch/PR probe that cannot run must stop the run (never proceed on an
    # unchecked remote state).
    responses = {("gh", "pr", "list", "--head", ROLLING, "--state", "open",
                  "--json", "number"): (1, "", "gh not authed")}
    responses[("git", "diff", "--name-only")] = (0, f"{LEDGER}\n", "")
    responses[("git", "ls-remote", "--heads", "origin", ROLLING)] = \
        (0, f"{SHA1}\trefs/heads/{ROLLING}\n", "")
    responses[("git", "log", "-1", "--format=%B", SHA1)] = \
        (0, orch.OWNER_MARKER + "\n", "")
    state, err = orch.collect_state(FakeRunner(responses))
    assert state is None and "unchecked" in err


def test_workflow_calls_orchestrator_and_drops_dated_branch_pattern():
    from pathlib import Path
    root = Path(__file__).resolve().parents[1]
    text = (root / ".github" / "workflows" /
            "consolidation-ledger-nightly.yml").read_text(encoding="utf-8")
    assert "scripts/consolidation_ledger_pr_orchestrate.py" in text
    assert "chore/ledger-refresh-$(date" not in text, \
        "the dated per-night branch pattern must be gone"
    assert "consolidation_ledger_refresh.py --check" in text, \
        "the required ledger check stays in the workflow"
    assert "fetch-depth: 0" in text
