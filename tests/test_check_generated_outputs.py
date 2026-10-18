"""Date masking in scripts/check_generated_outputs.py (H5691 sibling, 17-10-2026).

The register drift gate masks the generator's own DD-MM-YYYY stamp and compares
the rest, so today's calendar alone never reds a PR. The mask used `\\b` word
boundaries, which do not fire between a digit and `_` -- and the root index
writes the stamp markdown-italicised (`_Generated: 13-10-2026_`), so exactly
that line was never masked and every PR that regenerated the registers was
refused as real drift (measured on PR #1106: "1 file(s) with real changes" was
the date line itself).
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import check_generated_outputs as cgo  # noqa: E402


def test_masks_date_wrapped_in_markdown_italics():
    assert cgo.masked(b"_Generated: 13-10-2026_\n") == "_Generated: DD-MM-YYYY_\n"


def test_masks_date_before_a_colon_or_period():
    assert cgo.masked(b"Generated: 17-10-2026. Next") == "Generated: DD-MM-YYYY. Next"
    assert cgo.masked(b"on 17-10-2026: ok") == "on DD-MM-YYYY: ok"


def test_masks_plain_date():
    assert cgo.masked(b"date 01-02-2026") == "date DD-MM-YYYY"


def test_does_not_eat_a_longer_number():
    # A real count must survive: 123-45-6789 is not a DD-MM-YYYY stamp.
    assert cgo.masked(b"123-45-6789") == "123-45-6789"
    assert cgo.masked(b"117-10-20261") == "117-10-20261"
