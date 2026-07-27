"""Line-ending determinism gate for the pedagogy export (H1768).

`export_manifest.json` pins a sha256 per feed, and the Systema consumer
(`pedagogy:sync-sg-export`) verifies it. Those hashes must therefore be a
property of the CONTENT, not of the OS that ran the build.

They were not. `Path.write_text` uses universal newlines (LF -> CRLF on
Windows) and `shutil.copy2` carried the CRLF bytes of the `.tsv` sources, which
`.gitattributes` did not cover. So a Windows build pinned CRLF hashes, and
`--check` failed on 4 of 6 feeds on every LF checkout (fresh clone, Linux, CI)
with a "sha256 drift" that reads as data corruption but is pure line-ending
skew.

`tests/test_pedagogy_export.py` could not catch it: its module-scope autouse
fixture calls `build_export()` first, so every assertion there runs against a
manifest freshly regenerated on the current platform — it compares the build to
itself and passes everywhere. This module deliberately does NOT rebuild, and
reads the COMMITTED blobs via `git show`, so it tests the artifact that
actually ships.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import build_pedagogy_export as bpe  # noqa: E402

EXPORT_DIR = REPO / "data" / "pedagogy_export"
MANIFEST = EXPORT_DIR / "export_manifest.json"


def _git_show(path: str) -> bytes | None:
    """Committed bytes for `path`, or None if git/the blob is unavailable.

    Intentionally captures BYTES (no `encoding=`): the whole point is to hash
    the exact committed octets, and decoding would normalise the line endings
    this test exists to detect.
    """
    try:
        proc = subprocess.run(
            ["git", "-C", str(REPO), "show", f"HEAD:{path}"],
            capture_output=True,
        )
    except (OSError, subprocess.SubprocessError):  # pragma: no cover - no git
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def test_committed_manifest_hashes_match_committed_feeds():
    """The shipped manifest must validate against the shipped feed bytes.

    Order-independent and platform-independent: reads committed blobs, so a
    sibling module's rebuild cannot mask a mismatch.
    """
    committed_manifest = _git_show("data/pedagogy_export/export_manifest.json")
    if committed_manifest is None:
        pytest.skip("git unavailable or export not committed")

    manifest = json.loads(committed_manifest.decode("utf-8"))
    drift = []
    for feed in manifest["feeds"]:
        blob = _git_show(feed["path"])
        if blob is None:
            pytest.skip(f"committed blob unavailable: {feed['path']}")
        actual = hashlib.sha256(blob).hexdigest()
        if actual != feed["sha256"]:
            drift.append(f"{feed['id']}: manifest={feed['sha256'][:12]} committed={actual[:12]}")

    assert not drift, (
        "committed manifest does not match committed feed bytes — most likely "
        "the manifest was rebuilt on a checkout with CRLF line endings:\n  "
        + "\n  ".join(drift)
    )


@pytest.mark.parametrize("kind", ["committed", "checked-out"])
def test_export_feeds_carry_no_crlf(kind):
    """No exported feed may contain CRLF, in git or in the working tree."""
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    offenders = []
    for feed in manifest["feeds"]:
        if kind == "committed":
            data = _git_show(feed["path"])
            if data is None:
                pytest.skip(f"committed blob unavailable: {feed['path']}")
        else:
            data = (REPO / feed["path"]).read_bytes()
        if b"\r\n" in data:
            offenders.append(feed["path"])

    assert not offenders, (
        f"{kind} export feeds contain CRLF, which makes their pinned sha256 "
        f"platform-dependent: {offenders}"
    )


def test_generated_json_written_lf_on_every_platform():
    """`build_export()` must emit LF regardless of host OS."""
    bpe.build_export()
    for name in ("export_manifest.json", "methodichka_corpus_layer_pointers.json"):
        raw = (EXPORT_DIR / name).read_bytes()
        assert b"\r\n" not in raw, f"{name} was written with CRLF by build_export()"
    assert bpe.check_export() == 0


def test_copy_feed_normalises_crlf(tmp_path):
    """A CRLF source must land in the export as LF (the `.tsv` case)."""
    src = tmp_path / "feed.tsv"
    src.write_bytes(b"a\tb\r\nc\td\r\n")
    dest = tmp_path / "out.tsv"
    bpe._copy_feed(src, dest)
    assert dest.read_bytes() == b"a\tb\nc\td\n"
