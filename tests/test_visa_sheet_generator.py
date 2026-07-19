# -*- coding: utf-8 -*-
"""Fidelity proof for the visa-sheet generator (H1315).

The claim under test: putting an existing hand-authored «виза» sheet through
`scripts/build_visa_sheet.py` reproduces its REVIEWABLE CONTENT exactly — same
sheet_id, same card ids in the same order, same titles, same question and panel
HTML — inventing nothing and dropping nothing. Only the shell changes (the
v0.3.0 standard surface the org ratified), which is the whole point of retiring
the copy-paste skeleton.

`review/sanskritgrammar-sg-mo-021-future_visa_review.html` is the fixture: it is
tracked, fully voted, and its decisions were already applied (H1180), so
exercising it orphans nothing. The two sheets whose votes H1316 is applying are
deliberately NOT touched here, and the generator writes to tmp_path — this test
never rewrites a sheet in place.

Cyrillic highlighting (V7) wraps Russian runs in <mark class="hl">; that markup
is stripped before comparison, since it is presentation, not content.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

import pytest

import build_visa_sheet
from visa_sheet_spec_from_html import extract_spec

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "review" / "sanskritgrammar-sg-mo-021-future_visa_review.html"

RE_MARK = re.compile(r'</?mark class="hl">|</mark>')


def unmark(html_text):
    """Drop V7 highlight wrappers so content compares against the pre-standard sheet."""
    return re.sub(r'<mark class="hl">(.*?)</mark>', r"\1", html_text, flags=re.S)


@pytest.fixture(scope="module")
def original():
    if not FIXTURE.exists():                      # pragma: no cover - fixture is tracked
        pytest.skip("fixture sheet missing: %s" % FIXTURE)
    return extract_spec(FIXTURE.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def regenerated(original, tmp_path_factory):
    """Round-trip: original sheet -> spec -> generated sheet -> spec."""
    out = tmp_path_factory.mktemp("visa")
    spec_path = out / "spec.json"
    spec_path.write_text(json.dumps(original, ensure_ascii=False, indent=2), encoding="utf-8")
    html_doc = build_visa_sheet.render_review_sheet(
        build_visa_sheet.build_items(original), build_visa_sheet.build_config(original))
    return extract_spec(html_doc), html_doc


def test_sheet_identity_survives(original, regenerated):
    got, _ = regenerated
    assert got["sheet_id"] == original["sheet_id"]
    # `generated` comes from the spec, never stamped at build time - a rebuild
    # tomorrow must not silently re-date a sheet a human already voted.
    assert got["generated"] == original["generated"]


def test_card_ids_identical_and_ordered(original, regenerated):
    got, _ = regenerated
    assert [i["id"] for i in got["items"]] == [i["id"] for i in original["items"]]


def test_no_card_content_invented_or_dropped(original, regenerated):
    got, _ = regenerated
    assert len(got["items"]) == len(original["items"])
    for new, old in zip(got["items"], original["items"]):
        assert new["title"] == old["title"], "title drift on %s" % old["id"]
        assert unmark(new["question"]) == old["question"], "question drift on %s" % old["id"]
        assert [(h, unmark(b)) for h, b in new["panels"]] == \
               [(h, b) for h, b in old["panels"]], "panel drift on %s" % old["id"]


def test_standard_surface_present(regenerated):
    """The point of the port: V3 id chips, V6 taller notes, V8 save banner, V7 marks."""
    _, html_doc = regenerated
    assert 'class="idchip"' in html_doc                                   # V3
    assert "min-height:88px;" in html_doc                                 # V6
    assert "SanskritGrammar\\review\\" in html_doc                        # V8
    assert '<mark class="hl">' in html_doc                                # V7
    assert "sanskritgrammar-sg-mo-021-future_visa_decisions.json" in html_doc


def test_no_rating_row(regenerated):
    """Visa sheets are categorical approve/reject/defer - they do not score."""
    _, html_doc = regenerated
    assert 'class="ratingrow"' not in html_doc
    assert 'data-rate=' not in html_doc


def test_decided_is_an_integer_count(regenerated):
    """Org decisions contract: `decided` is a count, not an ISO timestamp."""
    _, html_doc = regenerated
    assert "decided: decided" in html_doc
    assert re.search(r"var decided = ids\.filter\(.*\)\.length;", html_doc, re.S)


def test_generator_cli_runs(tmp_path, original):
    spec_path = tmp_path / "cli.json"
    spec_path.write_text(json.dumps(original, ensure_ascii=False, indent=2), encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_visa_sheet.py"),
         str(spec_path), "--out-dir", str(tmp_path)],
        capture_output=True, text=True, encoding="utf-8")
    assert r.returncode == 0, r.stderr
    assert (tmp_path / ("%s_review.html" % original["sheet_id"])).exists()
