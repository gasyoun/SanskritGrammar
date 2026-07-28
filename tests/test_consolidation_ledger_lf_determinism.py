"""Line-ending determinism gate for the consolidation ledger writer (H1769).

`scripts/consolidation_ledger_refresh.py` writes
`sangram/editorial/data/consolidation_ledger.json` (and its own `--self-test`
round-trips the same file twice more). `Path.write_text` applies
universal-newline translation by default -- LF -> CRLF on Windows -- so every
one of those writes dirtied the working tree with host-dependent bytes.

`.gitattributes` already pins `*.json  text eol=lf`, so `git add` renormalises
the committed blob regardless of what the writer produced -- this is the
sibling of the H1768 defect class (a writer that is not itself hash-pinned,
but still produces non-deterministic bytes on disk), not a case of committed
drift. This test guards the writer directly rather than the git-normalised
blob, since the blob was never the thing at risk here.

`test_consolidation_ledger.py` cannot catch this: it reads everything back
via `Path.read_text` (also universal-newline, so CRLF and LF decode
identically) and never inspects raw bytes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import consolidation_ledger_refresh as clr  # noqa: E402


def test_ledger_write_helper_never_produces_crlf(tmp_path):
    """The exact write pattern the refresh script uses must emit LF only."""
    dest = tmp_path / "consolidation_ledger.json"
    serialized = '{"a": 1,\n "b": 2}\n'
    dest.write_text(serialized, encoding="utf-8", newline="\n")
    raw = dest.read_bytes()
    assert b"\r\n" not in raw


def test_refresh_main_writes_ledger_with_no_crlf(monkeypatch, tmp_path):
    """Run the REAL `main()` write path against a scratch path; assert LF bytes.

    This exercises the exact code in `main()` (not a re-implementation of it),
    so it fails on the pre-fix `LEDGER_PATH.write_text(serialized,
    encoding="utf-8")` (no `newline=`) on a Windows host, and passes once that
    call gains `newline="\n"`.
    """
    scratch = tmp_path / "consolidation_ledger.json"
    monkeypatch.setattr(clr, "LEDGER_PATH", scratch)
    monkeypatch.setattr(sys, "argv", ["consolidation_ledger_refresh.py", "--today", "2026-07-19"])
    rc = clr.main()
    assert rc == 0
    raw = scratch.read_bytes()
    assert b"\r\n" not in raw, (
        "consolidation_ledger_refresh.py's write must always emit LF -- "
        "Path.write_text without newline='\\n' translates to CRLF on Windows"
    )


def test_committed_ledger_has_no_crlf():
    """The blob actually shipped in the repo must not carry CRLF either.

    Belt-and-suspenders on top of `.gitattributes eol=lf`: reads the file
    straight off disk in bytes mode (no text-mode normalisation) so a
    checkout-time or pre-commit-hook regression would still be caught.
    """
    raw = clr.LEDGER_PATH.read_bytes()
    assert b"\r\n" not in raw, (
        "sangram/editorial/data/consolidation_ledger.json carries CRLF on disk"
    )
