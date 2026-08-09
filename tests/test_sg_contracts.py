from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from sg_tooling.contracts import ContractError, validate_pipeline


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def pipeline() -> dict:
    return {
        "schema_version": "1.0.0",
        "id": "fixture",
        "owner": "tests",
        "generator": "tests.fixture",
        "inputs": [{"path": "in", "version": "1", "sha256": "0" * 64}],
        "outputs": ["out"],
        "checks": ["pytest"],
        "external_consumers": [],
        "rollback": {"command": ["git", "restore", "out"]},
        "steps": [
            {"id": "prepare", "command": ["python", "--version"], "outputs": ["tmp"]},
            {"id": "build", "command": ["python", "--version"], "needs": ["prepare"], "inputs": ["tmp"], "outputs": ["out"]},
        ],
    }


def test_pipeline_schema_accepts_complete_contract(pipeline: dict) -> None:
    validate_pipeline(pipeline, ROOT)


@pytest.mark.parametrize("mutation", ["duplicate", "cycle", "producer", "overlap", "unknown"])
def test_graph_invariants_fail_closed(pipeline: dict, mutation: str) -> None:
    broken = copy.deepcopy(pipeline)
    if mutation == "duplicate":
        broken["steps"][1]["id"] = "prepare"
    elif mutation == "cycle":
        broken["steps"][0]["needs"] = ["build"]
    elif mutation == "producer":
        broken["steps"][1]["outputs"] = ["tmp"]
    elif mutation == "overlap":
        broken["steps"][1]["outputs"] = ["tmp"]
    else:
        broken["steps"][0]["needs"] = ["missing"]
    with pytest.raises(ContractError):
        validate_pipeline(broken, ROOT)


def test_work_schema_keeps_unknown_rights_representable() -> None:
    from jsonschema import Draft202012Validator

    schema = json.loads((ROOT / "pipelines" / "work.schema.json").read_text(encoding="utf-8"))
    document = {
        "schema_version": "1.0.0",
        "id": "work",
        "authority": "source edition",
        "source_pointers": ["source.docx"],
        "generated_roots": ["Work"],
        "media_roots": [],
        "routes": ["/grammars/work"],
        "rights": {"status": "unknown", "statement": "No determination recorded."},
        "pipelines": [],
    }
    Draft202012Validator(schema).validate(document)

