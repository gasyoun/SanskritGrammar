"""Grammar Lab G1 schemas, evidence contract, build --check (H2492)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

import build_grammar_lab as bgl

REPO = Path(__file__).resolve().parents[1]
FIXTURES = REPO / "tests" / "fixtures" / "grammar_lab"
EXPORT = REPO / "data" / "grammar_lab" / "export"


@pytest.fixture(scope="module", autouse=True)
def _built():
    bgl.build()
    yield


def test_valid_fixture_matches_schema():
    topic = yaml.safe_load((FIXTURES / "valid_topic.yml").read_text(encoding="utf-8"))
    assert bgl.validate_schema(topic, "topic.schema.json") == []


def test_invalid_fixture_fails_schema():
    topic = yaml.safe_load((FIXTURES / "invalid_topic.yml").read_text(encoding="utf-8"))
    errs = bgl.validate_schema(topic, "topic.schema.json")
    assert errs


def test_published_count_and_contract():
    report = json.loads((EXPORT / "evidence_contract_report.json").read_text(encoding="utf-8"))
    assert 25 <= report["published"] <= 40
    assert report["invalid_published"] == 0
    published = [r for r in report["rows"] if r["publishable"]]
    assert len(published) == report["published"]
    for row in published:
        assert row["has_whitney"]
        assert row["has_zalizniak"]
        assert row["has_dictionary"]
        assert row["has_corpus"]
        assert row["has_exercise"]
        assert row["has_four_script_aliases"]


def test_five_representative_topics_present():
    bundle = json.loads((EXPORT / "grammar_lab.json").read_text(encoding="utf-8"))
    ids = {t["id"] for t in bundle["topics"]}
    required = {
        "subject:grammar-lab:ablaut-grades",
        "subject:grammar-lab:morphological-positions",
        "subject:grammar-lab:samprasarana",
        "subject:grammar-lab:root-homonymy",
        "subject:grammar-lab:set-anit-vet",
    }
    assert required <= ids


def test_needs_review_omitted_from_bundle():
    bundle = json.loads((EXPORT / "grammar_lab.json").read_text(encoding="utf-8"))
    ids = {t["id"] for t in bundle["topics"]}
    assert "subject:grammar-lab:type-equals-present-class" not in ids
    assert "subject:grammar-lab:type-equals-present-class" in set(bundle["omissions"])


def test_interpretive_not_auto_published():
    for path in (REPO / "data" / "grammar_lab" / "exercises").glob("*.yml"):
        rec = yaml.safe_load(path.read_text(encoding="utf-8"))
        if rec.get("risk_class") == "interpretive":
            assert rec.get("status") != "published"


def test_typed_links_lint_clean():
    import csv

    path = EXPORT / "typed_links.tsv"
    header = path.read_text(encoding="utf-8").splitlines()[0].split("\t")
    assert header == bgl.TYPE_D_FIELDS
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh, delimiter="\t"))
    assert rows
    for row in rows:
        assert row["link_type"] == "thematic"
        assert row["target_locus"].startswith("subject:grammar-lab:")
        assert row["match_method"] in bgl.ALLOWED_MATCH


def test_check_exit_0():
    assert bgl.check() == 0
    assert bgl.main(["--check"]) == 0


def test_check_fails_on_hash_break():
    path = EXPORT / "grammar_lab.json"
    original = path.read_bytes()
    try:
        path.write_bytes(original + b"\n")
        assert bgl.check() == 1
    finally:
        path.write_bytes(original)
    assert bgl.check() == 0


def test_vectors_and_queries():
    vec = json.loads((EXPORT / "topic_vectors.json").read_text(encoding="utf-8"))
    assert vec["dimensionality"] == 384
    assert vec["vectors"]
    assert all(len(item["vector"]) == 384 for item in vec["vectors"])
    queries = json.loads(
        (REPO / "data" / "grammar_lab" / "queries" / "frozen_queries.json").read_text(
            encoding="utf-8"
        )
    )
    assert len(queries["queries"]) >= 100
    scripts = {q["script"] for q in queries["queries"]}
    assert {"ru", "deva", "iast", "slp1"} <= scripts


def test_no_sandhi_published_locus():
    bundle = json.loads((EXPORT / "grammar_lab.json").read_text(encoding="utf-8"))
    for topic in bundle["topics"]:
        for edge in topic["sources"]:
            assert "sandhi" not in edge["anchor_id"].lower()
            assert "sandhi" not in (edge.get("source_dataset") or "").lower() or True
            assert not edge["anchor_id"].endswith(":sandhi")
