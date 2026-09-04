#!/usr/bin/env python3
"""Repository-gates runner for the OxAlpha review gate (H4074).

Runs the named gate commands in a clean checkout (design section 3 step 2:
"runs the repository gates ... green is a necessary condition, never
sufficient") and records each outcome in gates.json. Hard gates failing ->
verdict fail; soft gates (e.g. the repo's warn-only black check, mirroring
ci.yml) are recorded but never flip the verdict on their own.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

TAIL_BYTES = 4000


def run_gate(name: str, cmd: str, hard: bool, repo: str, timeout: int) -> dict:
    # shlex.split, not a shell route: the commands come from the committed
    # workflow, but there is no reason to route them through /bin/sh.
    import shlex
    proc = subprocess.run(
        shlex.split(cmd), shell=False, cwd=repo, capture_output=True,
        text=True, encoding="utf-8", errors="replace", timeout=timeout)
    tail = ((proc.stdout or "") + (proc.stderr or ""))[-TAIL_BYTES:]
    return {
        "name": name,
        "cmd": cmd,
        "hard": hard,
        "ok": proc.returncode == 0,
        "rc": proc.returncode,
        "output_tail": tail,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="OxAlpha gate repository-gates runner.")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", default="gates.json")
    ap.add_argument("--gate", action="append", default=[],
                    help="gate spec NAME|CMD|hard|timeout_s (repeatable)")
    args = ap.parse_args()

    gates = []
    for spec in args.gate:
        parts = spec.split("|", 3)
        if len(parts) != 4:
            print("bad --gate spec (need NAME|CMD|hard|timeout): %s" % spec,
                  file=sys.stderr)
            return 2
        name, cmd, hard, timeout = parts[0], parts[1], parts[2], int(parts[3])
        print("GATE %s: %s" % (name, cmd), file=sys.stderr)
        try:
            gates.append(run_gate(name, cmd, hard.lower() == "hard",
                                  args.repo, timeout))
        except subprocess.TimeoutExpired:
            gates.append({"name": name, "cmd": cmd, "hard": hard.lower() == "hard",
                          "ok": False, "rc": -9,
                          "output_tail": "TIMEOUT after %ss" % timeout})
        except OSError as exc:
            gates.append({"name": name, "cmd": cmd, "hard": hard.lower() == "hard",
                          "ok": False, "rc": -1,
                          "output_tail": "spawn failed: %s" % exc})
        print("GATE %s -> %s" % (name, "ok" if gates[-1]["ok"] else "FAIL"),
              file=sys.stderr)

    record = {"ran": bool(gates), "gates": gates}
    Path(args.out).write_text(
        json.dumps(record, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main() or 0)
