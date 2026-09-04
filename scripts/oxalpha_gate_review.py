#!/usr/bin/env python3
"""Second-opinion review pass for the OxAlpha review gate (H4074).

Two axes, kept separate (design section 2):

- ``spec``     - deterministic evidence-chain check on the PR body: handoff id
                (H\\d+), issue reference (#n), or the literal declaration
                "no spec available". No PR context -> ``not-applicable``.
- ``standards`` - a bounded pass over the <=10 risk-ranked hunks of the
                executable delta. A deterministic heuristic scan always runs;
                when a human provisions OXALPHA_REVIEW_API_KEY +
                OXALPHA_REVIEW_MODEL repo secrets, the model lane's findings
                are merged in. An unprovisioned reviewer is recorded by name -
                the heuristic lane still ran, so the verdict is never a
                silent pass.

Inputs are the diff, the PR body and the committed matcher record only - the
verdict is produced without access to any author session's reasoning (design
section 2 independence rule). Every finding carries
severity/file/line/failure_mode/repro or it is not emitted.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HANDOFF_RE = re.compile(r"H\d{3,5}")
ISSUE_RE = re.compile(r"(\s)#(\d{2,6})\b")
NO_SPEC = "no spec available"

#: Bounds (the design's bounded second-opinion pass).
MAX_HUNKS = 10
MAX_DIFF_BYTES = 60_000
MAX_FINDINGS_PER_HUNK = 5

#: Added-line heuristics: (regex, severity, failure_mode, repro).
#: High precision on purpose - a shadow gate that cries wolf gets ignored.
HEURISTICS = (
    (re.compile(r"(?i)\b(api_key|apikey|token|password|secret|passwd)\s*=\s*[\"'][^\"' ]{8,}[\"']"),
     "P0", "hardcoded credential in source",
     "introduce KEY = \"...\" literal in an added line"),
    (re.compile(r"\beval\s*\("), "P1", "eval() executes attacker-influenceable strings",
     "call eval(<expr>) on a non-literal"),
    (re.compile(r"\bexec\s*\("), "P1", "exec() executes dynamic code",
     "call exec(<code>) on a non-literal"),
    (re.compile(r"\bos\.system\s*\("), "P1", "os.system shell injection surface",
     "call os.system(<cmd>) with interpolated input"),
    (re.compile(r"shell\s*=\s*True"), "P1", "shell=True subprocess injection surface",
     "pass shell=True to a subprocess call"),
    (re.compile(r"except\s*:"), "P2", "bare except swallows KeyboardInterrupt/SystemExit",
     "write `except:` around failing code"),
    (re.compile(r"\bpickle\.loads?\s*\("), "P2", "pickle deserialization of untrusted data",
     "pickle.loads(untrusted_bytes)"),
    (re.compile(r"\byaml\.load\s*\((?![^)]*Loader)"), "P2", "yaml.load without Loader",
     "yaml.load(text) without Loader arg"),
    (re.compile(r"subprocess\.(run|call|check_call|check_output|Popen)\((?![^)]*timeout)"),
     "P2", "subprocess without timeout can hang the pipeline",
     "subprocess.run([...]) without timeout="),
    (re.compile(r"requests\.(get|post|put|delete|head|patch)\((?![^)]*timeout)"),
     "P2", "requests call without timeout can hang the caller",
     "requests.get(url) without timeout="),
    (re.compile(r"\bPath\.home\(\)"), "P3", "Path.home() profile sandboxes lie (org rule)",
     "call Path.home() outside a test"),
    (re.compile(r"\b(TODO|FIXME|XXX)\b"), "P3", "placeholder marker committed",
     "add a TODO/FIXME comment"),
)

#: Weight added to a hunk's risk score per heuristic hit; sensitive paths add
#: a flat bonus so integrity/production surfaces are always reviewed first.
TOKEN_WEIGHT = 3
SENSITIVE_BONUS = 5

#: Versioned rubric for the model lane. Editing it is an executable-path
#: change (.github/workflows + scripts are matched by the gate itself).
RUBRIC = """You are the independent Standards reviewer for a pull request in \
this repository. Repo rules that matter: fail-closed guards over fail-open \
unless fail-open is the documented contract; every subprocess call carries \
encoding='utf-8' and a timeout; no Path.home() in module-level constants; no \
silent exception swallowing; published-figure truth gates \
(check_claims_consistency, refresh_published_figures --check, \
consolidation_ledger_refresh --check) must never be weakened or bypassed; \
generated stores (consolidation_ledger.json, book .mdx extractions, data/**) \
are never hand-edited - their committed generator gates are the fix path; \
patches/** files are behavior-bearing by definition.
Report ONLY defects you can demonstrate from the diff: each finding needs
severity (P0|P1|P2|P3), file, line, failure mode, and a repro sketch.
No prose outside JSON. Output shape:
{"findings": [{"severity": "...", "file": "...", "line": 0,
               "failure_mode": "...", "repro": "..."}]}
If you cannot demonstrate a defect, return {"findings": []}."""


def spec_axis(pr_body: str) -> dict:
    body = pr_body or ""
    if not body:
        return {"axis": "spec", "verdict": "not-applicable",
                "evidence": "no PR context (dispatch/scheduled run)"}
    if HANDOFF_RE.search(body):
        return {"axis": "spec", "verdict": "named",
                "evidence": "handoff id in PR body"}
    if ISSUE_RE.search(body):
        return {"axis": "spec", "verdict": "named",
                "evidence": "issue reference in PR body"}
    if NO_SPEC in body.lower():
        return {"axis": "spec", "verdict": "declared-absent",
                "evidence": NO_SPEC}
    return {"axis": "spec", "verdict": "absent",
            "evidence": "no handoff id, issue reference, or 'no spec available'"}


def diff_hunks(base: str, head: str, repo: str, paths: list[str]) -> list[dict]:
    """Parse `git diff -U0` over the matched paths into risk-ranked hunks."""
    if not paths:
        return []                 # empty pathspec would mean "whole diff"
    proc = subprocess.run(
        ["git", "diff", "--no-ext-diff", "-U0", base, head, "--"] + list(paths),
        cwd=repo, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120)
    text = proc.stdout or ""
    if len(text.encode("utf-8")) > MAX_DIFF_BYTES:
        text = text[:MAX_DIFF_BYTES]
    hunks: list[dict] = []
    cur: dict | None = None
    fname = ""
    new_line = 0
    for line in text.splitlines():
        if line.startswith("+++ b/"):
            fname = line[6:]
            if cur is not None:
                hunks.append(cur)
                cur = None
        elif line.startswith("@@"):
            m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)", line)
            new_line = int(m.group(1)) if m else 0
            cur = {"file": fname, "start": new_line, "added": [], "score": 0}
        elif cur is not None and line.startswith("+") and not line.startswith("+++"):
            cur["added"].append({"line": new_line, "text": line[1:]})
            new_line += 1
        elif cur is not None and line.startswith("-") and not line.startswith("---"):
            pass                       # removed line: no new-file number consumed
        elif cur is not None:
            new_line += 1              # context line
        if len(hunks) > 500:           # pathological diff guard
            break
    if cur is not None:
        hunks.append(cur)
    for h in hunks:
        score = SENSITIVE_BONUS if _sensitive_file(h["file"]) else 0
        for pat, _sev, _mode, _rep in HEURISTICS:
            for ln in h["added"]:
                if pat.search(ln["text"]):
                    score += TOKEN_WEIGHT
                    break
        h["score"] = score
    hunks.sort(key=lambda h: (-h["score"], h["file"], h["start"]))
    return hunks[:MAX_HUNKS]


def _sensitive_file(path: str) -> bool:
    from oxalpha_gate_match import is_sensitive
    return is_sensitive(path)


def heuristic_findings(hunks: list[dict]) -> list[dict]:
    findings: list[dict] = []
    for h in hunks:
        per_hunk = 0
        for ln in h["added"]:
            for pat, sev, mode, repro in HEURISTICS:
                if per_hunk >= MAX_FINDINGS_PER_HUNK:
                    break
                if pat.search(ln["text"]):
                    findings.append({
                        "severity": sev, "file": h["file"], "line": ln["line"],
                        "failure_mode": mode, "repro": repro,
                        "axis": "standards-heuristic",
                    })
                    per_hunk += 1
    return findings


def model_findings(diff_text: str, env: dict) -> dict:
    """Anthropic messages API, stdlib only."""
    key = env.get("OXALPHA_REVIEW_API_KEY") or env.get("ANTHROPIC_API_KEY") or ""
    model = env.get("OXALPHA_REVIEW_MODEL", "")
    import urllib.error
    import urllib.request
    payload = json.dumps({
        "model": model,
        "max_tokens": 2000,
        "messages": [{"role": "user",
                      "content": RUBRIC + "\n\nDIFF:\n" + diff_text}],
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages", data=payload,
        headers={"content-type": "application/json",
                 "x-api-key": key,
                 "anthropic-version": "2023-06-01"})
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
    except Exception as exc:  # noqa: BLE001 - the model lane must degrade, not crash
        return {"lane": "model", "verdict": "unavailable",
                "evidence": "reviewer call failed: %s" % str(exc)[:200]}
    text = ""
    for block in body.get("content", []):
        if isinstance(block, dict) and block.get("type") == "text":
            text += block.get("text", "")
    parsed = _parse_findings(text)
    if parsed is None:
        return {"lane": "model", "verdict": "unavailable",
                "evidence": "reviewer returned unparseable output"}
    return {"lane": "model", "verdict": "ran",
            "evidence": "%d finding(s)" % len(parsed), "findings": parsed}


def _parse_findings(text: str) -> list | None:
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        obj = json.loads(text[start:end + 1])
    except ValueError:
        return None
    if not isinstance(obj, dict) or not isinstance(obj.get("findings"), list):
        return None
    return obj["findings"]


def _diff_text_for_model(base: str, head: str, repo: str, paths: list[str]) -> str:
    proc = subprocess.run(
        ["git", "diff", "--no-ext-diff", "-U3", base, head, "--"] + list(paths),
        cwd=repo, capture_output=True, text=True, encoding="utf-8",
        errors="replace", timeout=120)
    text = proc.stdout or ""
    encoded = text.encode("utf-8")
    if len(encoded) <= MAX_DIFF_BYTES:
        return text
    return encoded[:MAX_DIFF_BYTES].decode("utf-8", errors="ignore") + \
        "\n... (diff truncated at %d bytes) ...\n" % MAX_DIFF_BYTES


def review(base: str, head: str, repo: str, pr_body: str, matched_paths: list[str],
           env: dict | None = None, run_model: bool = True) -> dict:
    env = os.environ if env is None else env
    hunks = diff_hunks(base, head, repo, matched_paths)
    findings = heuristic_findings(hunks)
    lane_records = [{"lane": "heuristics", "verdict": "ran",
                     "evidence": "%d hunk(s) scanned, %d finding(s)"
                                 % (len(hunks), len(findings))}]
    model_ready = bool(env.get("OXALPHA_REVIEW_API_KEY")
                       or env.get("ANTHROPIC_API_KEY")) and env.get("OXALPHA_REVIEW_MODEL")
    if not model_ready:
        lane_records.append({"lane": "model", "verdict": "unprovisioned",
                             "evidence": "OXALPHA_REVIEW_API_KEY/OXALPHA_REVIEW_MODEL "
                                         "not set - heuristic lane only"})
    elif run_model:
        mdl = model_findings(
            _diff_text_for_model(base, head, repo, matched_paths), env)
        lane_records.append(mdl)
        for f in mdl.get("findings", []):
            findings.append({
                "severity": str(f.get("severity", "P2")),
                "file": str(f.get("file", "unknown")),
                "line": int(f.get("line", 0) or 0),
                "failure_mode": str(f.get("failure_mode", "")),
                "repro": str(f.get("repro", "")),
                "axis": "standards-model",
            })
    return {
        "matched_paths": matched_paths,
        "hunks_reviewed": [h for h in hunks],
        "axes": [spec_axis(pr_body),
                 {"axis": "standards", "verdict": "ran",
                  "evidence": "; ".join("%s: %s" % (r["lane"], r["verdict"])
                                        for r in lane_records),
                  "lanes": lane_records}],
        "findings": findings,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="OxAlpha gate review pass.")
    ap.add_argument("--base", required=True)
    ap.add_argument("--head", required=True)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--matched-json", default="match.json",
                    help="match.json from oxalpha_gate_match.py")
    ap.add_argument("--pr-body-file", default=None,
                    help="file holding the PR body; default: env PR_BODY")
    ap.add_argument("--no-model", action="store_true",
                    help="deterministic lanes only (tests / offline runs)")
    ap.add_argument("--out", default="review.json")
    args = ap.parse_args()

    matched = json.loads(Path(args.matched_json).read_text(encoding="utf-8"))
    paths = matched.get("matched_paths", [])
    if args.pr_body_file:
        body = Path(args.pr_body_file).read_text(encoding="utf-8")
    else:
        body = os.environ.get("PR_BODY", "")
    out = review(args.base, args.head, args.repo, body, paths,
                 run_model=not args.no_model)
    Path(args.out).write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")
    for ax in out["axes"]:
        print("AXIS %s: %s (%s)" % (ax["axis"], ax["verdict"], ax["evidence"]),
              file=sys.stderr)
    print("FINDINGS: %d" % len(out["findings"]), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main() or 0)
