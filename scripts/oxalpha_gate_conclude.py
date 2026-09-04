#!/usr/bin/env python3
"""Conclusion renderer for the OxAlpha review gate (H4074, SanskritGrammar).

The design allows exactly three check conclusions -- ``pass``, ``fail``
(evidence-backed), ``skip`` (diff matches no executable-code pattern) -- and
NEVER a silent success: a verdict is always written (verdict.json +
ledger-row.jsonl), uploaded as an artifact, and posted as a PR comment when a
PR context exists. A crashed or missing review is a ``fail`` with reason
``infrastructure``, never an absence.

Rung 1 is reporting-only (design section 4 rollout: non-required first): the
job exits 0 and the verdict travels in the summary/artifact/comment. --enforce
(a later human-gated flip to required) is where exit codes start to matter.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

BLOCKING_SEVERITIES = ("P0", "P1")
STATE_SKIP = "skip"
TESTS_RE = re.compile(r"(\d+) passed")


def run_url() -> str:
    base = os.environ.get("GITHUB_SERVER_URL", "https://github.com")
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run = os.environ.get("GITHUB_RUN_ID", "")
    if not repo or not run:
        return ""
    return "%s/%s/actions/runs/%s" % (base, repo, run)


def gates_conclusion(gates: dict | None) -> tuple[bool, list[str]]:
    """(all_hard_ok, reason_lines). Missing record counts as not-run."""
    if not gates or not gates.get("ran"):
        return True, ["repository gates did not run"]
    reasons = []
    ok = True
    for g in gates.get("gates", []):
        if not g.get("ok"):
            line = "gate %s failed (rc=%s)" % (g.get("name"), g.get("rc"))
            reasons.append(line)
            if g.get("hard"):
                ok = False
    return ok, reasons


def conclude(matched: str, match: dict | None, gates: dict | None,
             review: dict | None) -> dict:
    """Inputs -> {state, reasons[], evidence{}} per the design's conclusion table."""
    evidence: dict = {"run_url": run_url(),
                      "sha": os.environ.get("GITHUB_SHA", "")}
    if matched == "unknown":
        return {"state": "fail",
                "reasons": ["infrastructure: match step produced no output"],
                "evidence": evidence}
    if not match:
        return {"state": "fail",
                "reasons": ["infrastructure: match record absent"],
                "evidence": evidence}

    hard_ok, gate_reasons = gates_conclusion(gates)
    tests = ""
    if gates and gates.get("ran"):
        for g in gates.get("gates", []):
            if g.get("name") == "pytest" and g.get("ok"):
                m = TESTS_RE.search(g.get("output_tail", ""))
                tests = "%s passed" % m.group(1) if m else "pytest green"
    if tests:
        evidence["tests"] = tests
    evidence["gates"] = ("; ".join(
        "%s=%s" % (g.get("name"), "ok" if g.get("ok") else "FAIL")
        for g in (gates or {}).get("gates", [])) or "not-run")
    evidence["sensitive_paths"] = (match or {}).get("sensitive_paths", [])

    if matched != "true":
        reasons = ["diff matches no executable-code pattern (design section 1) "
                   "- exclusion note: nothing to review"]
        if gates and gates.get("ran"):
            reasons += gate_reasons or ["repository gates green (periodic audit)"]
        return {"state": STATE_SKIP, "reasons": reasons, "evidence": evidence}

    if not hard_ok:
        return {"state": "fail", "reasons": gate_reasons, "evidence": evidence}
    if review is None:
        return {"state": "fail",
                "reasons": ["infrastructure: executable delta matched but no "
                            "review record was produced"],
                "evidence": evidence}

    findings = review.get("findings", [])
    blocking = [f for f in findings
                if str(f.get("severity", "")).upper() in BLOCKING_SEVERITIES]
    reasons = list(gate_reasons)
    axes = {ax.get("axis"): ax for ax in review.get("axes", [])}
    spec = axes.get("spec", {})
    if spec.get("verdict") == "absent":
        reasons.append("spec source absent: %s" % spec.get("evidence", ""))
    if blocking:
        reasons.append("%d blocking finding(s): %s" % (
            len(blocking), "; ".join(
                "%s %s:%s %s" % (f.get("severity"), f.get("file"),
                                 f.get("line"), f.get("failure_mode"))
                for f in blocking)))
        return {"state": "fail", "reasons": reasons, "evidence": evidence}
    if spec.get("verdict") == "absent":
        return {"state": "fail", "reasons": reasons, "evidence": evidence}
    reasons = reasons or ["repository gates green"]
    reasons.append("review ran clean: %d non-blocking finding(s), %d hunk(s) scanned"
                   % (len(findings), len(review.get("hunks_reviewed", []))))
    if match.get("sensitive_paths"):
        reasons.append("integrity/production paths touched (design section 3, "
                       "human approval + regression tests required before any "
                       "required-check flip): %s"
                       % ", ".join(match["sensitive_paths"]))
    return {"state": "pass", "reasons": reasons, "evidence": evidence}


def render(result: dict, review: dict | None, match: dict | None) -> str:
    lines = ["## OxAlpha review gate - verdict: `%s`" % result["state"], ""]
    for r in result["reasons"]:
        lines.append("- %s" % r)
    lines += ["", "| axis | verdict | evidence |", "|---|---|---|"]
    for ax in (review or {}).get("axes", []):
        lines.append("| `%s` | %s | %s |" % (ax.get("axis"), ax.get("verdict"),
                                             ax.get("evidence", "")))
    findings = (review or {}).get("findings", [])
    if findings:
        lines += ["", "| sev | file:line | mode | repro |", "|---|---|---|---|"]
        for f in findings:
            lines.append("| %s | `%s:%s` | %s | %s |" % (
                f.get("severity"), f.get("file"), f.get("line"),
                f.get("failure_mode"), f.get("repro")))
    if not findings:
        lines += ["", "_Never-silent record: this verdict is posted and archived "
                     "even when nothing was found._"]
    ev = result.get("evidence", {})
    if ev.get("run_url"):
        lines.append("")
        lines.append("Evidence: run %s @ %s" % (ev["run_url"], ev.get("sha", "")[:12]))
    return "\n".join(lines) + "\n"


def ledger_row(result: dict, review: dict | None, pr_number: str) -> str:
    axes = {ax.get("axis"): ax.get("verdict") for ax in (review or {}).get("axes", [])}
    finding_ids = ["%s:%s:%s" % (f.get("severity"), f.get("file"), f.get("line"))
                   for f in (review or {}).get("findings", [])]
    row = {
        "date": datetime.datetime.now(datetime.timezone.utc)
                .strftime("%Y-%m-%dT%H:%M:%SZ"),
        "pr": int(pr_number) if pr_number.isdigit() else None,
        "state": result["state"],
        "axes": axes,
        "finding_ids": finding_ids,
        "run_url": result.get("evidence", {}).get("run_url", ""),
    }
    return json.dumps(row, ensure_ascii=False) + "\n"


def annotations(result: dict, review: dict | None) -> list[str]:
    out = []
    for f in (review or {}).get("findings", []):
        if str(f.get("severity", "")).upper() in BLOCKING_SEVERITIES:
            out.append("::warning file=%s,line=%s::OxAlpha gate %s: %s"
                       % (f.get("file", "unknown"), f.get("line", 0),
                          f.get("severity"), f.get("failure_mode", "")))
    for r in result["reasons"]:
        if result["state"] == STATE_SKIP:
            out.append("::notice::OxAlpha gate skip: %s" % r)
        elif result["state"] == "fail" and "infrastructure" in r:
            out.append("::error::OxAlpha gate infrastructure fail: %s" % r)
    return out


def _load(path: str) -> dict | None:
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except ValueError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="OxAlpha gate conclusion.")
    ap.add_argument("--matched", required=True,
                    help="executable=true|false|unknown from the match step")
    ap.add_argument("--match", default="match.json")
    ap.add_argument("--gates", default="gates.json")
    ap.add_argument("--review", default="review.json")
    ap.add_argument("--pr-number", default=os.environ.get("PR_NUMBER", ""))
    ap.add_argument("--verdict-out", default="verdict.json")
    ap.add_argument("--ledger-out", default="ledger-row.jsonl")
    ap.add_argument("--comment-out", default="comment.md")
    ap.add_argument("--enforce", action="store_true",
                    help="required-check mode: exit 1 on fail")
    ap.add_argument("--gha", action="store_true",
                    help="write GITHUB_STEP_SUMMARY + annotations on stdout")
    args = ap.parse_args()

    result = conclude(args.matched.strip().lower(), _load(args.match),
                      _load(args.gates), _load(args.review))
    review = _load(args.review)
    match = _load(args.match)

    Path(args.verdict_out).write_text(
        json.dumps(result, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")
    Path(args.ledger_out).write_text(
        ledger_row(result, review, args.pr_number),
        encoding="utf-8", newline="\n")
    text = render(result, review, match)
    Path(args.comment_out).write_text(text, encoding="utf-8", newline="\n")

    if args.gha:
        summary = os.environ.get("GITHUB_STEP_SUMMARY", "")
        if summary:
            with Path(summary).open("a", encoding="utf-8", newline="\n") as fh:
                fh.write(text + "\n")
        for ann in annotations(result, review):
            print(ann)
    print(text)
    if args.enforce and result["state"] == "fail":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main() or 0)
