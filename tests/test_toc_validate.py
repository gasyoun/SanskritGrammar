"""Tests for scripts/toc_validate.py (H1839).

The live C2 registry must pass; ID grammar and C6 slot set are pinned.
"""
import re

import toc_validate as tv


def test_id_grammar_accepts_and_rejects():
    assert tv.ID_RE.match("SG-MO-001")
    assert tv.ID_RE.match("SG-SE-013")
    assert not tv.ID_RE.match("SG-XX-001")
    assert not tv.ID_RE.match("SG-MO-1")  # needs three digits
    assert not tv.ID_RE.match("art:mo-001")


def test_whitney_anchor_grammar():
    assert tv.ANCHOR_RE.match("whitney-sec:274")
    assert tv.ANCHOR_RE.match("whitney-sec:100-105")
    assert not tv.ANCHOR_RE.match("whitney:274")


def test_c6_slots_count_is_33():
    assert len(tv.C6_SLOTS) == 33


def test_live_registry_validates_clean():
    # toc_validate.main() mutates module-level errors[] — clear first.
    tv.errors.clear()
    rc = tv.main()
    assert rc == 0, "toc_validate failed:\n" + "\n".join(tv.errors)
