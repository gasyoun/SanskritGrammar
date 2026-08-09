"""Contract tests for the pipeline / work / provenance schemas (A2).

Each rule the contracts claim to enforce gets one positive and one negative case,
so a schema edit that quietly drops a rule fails here rather than in production.

The invariants JSON Schema *cannot* express — unique step IDs, an acyclic graph,
one producer per output, no input/output overlap — are checked separately through
``validate_pipeline_graph``.
"""
from __future__ import annotations

import copy

import pytest

from sg_tooling.contracts import (
    ContractError,
    validate_pipeline,
    validate_pipeline_graph,
    validate_provenance_lock,
    validate_work,
)
from sg_tooling.contracts.validate import repo_root

VALID_PIPELINE = {
    "contract_version": 1,
    "pipeline_id": "pipeline:work-example",
    "owner": "SanskritGrammar maintainers",
    "context": "work:example",
    "steps": [
        {
            "id": "convert",
            "command": "work.convert_docx",
            "inputs": ["content/works/example/sources/example.docx"],
            "outputs": ["content/works/example/generated/example.mdx"],
        },
        {
            "id": "errata",
            "command": "work.build_errata",
            "needs": ["convert"],
            "outputs": ["content/works/example/generated/ERRATA.mdx"],
        },
    ],
    "verification": ["work.golden"],
    "rollback": {"procedure": "Revert the cutover commit."},
}

VALID_WORK = {
    "contract_version": 1,
    "work_id": "work:example",
    "title": "Example work",
    "source_authority": {
        "primary": "sources/example.docx",
        "witnesses": ["sources/example.doc"],
    },
    "rights": {"source": "restricted-source", "generated_text": "publishable"},
    "stable_routes": {"primary": "Example_1900/example"},
    "outputs": ["generated/example.mdx"],
}


def _pipeline(**overrides):
    doc = copy.deepcopy(VALID_PIPELINE)
    doc.update(overrides)
    return doc


def _work(**overrides):
    doc = copy.deepcopy(VALID_WORK)
    doc.update(overrides)
    return doc


# ------------------------------------------------------------------ pipeline --
def test_valid_pipeline_passes():
    assert validate_pipeline(_pipeline()).ok


def test_unknown_key_is_rejected():
    """Silent acceptance of an unknown key could change execution."""
    report = validate_pipeline(_pipeline(surprise="value"))
    assert not report.ok


def test_wrong_contract_version_is_rejected():
    assert not validate_pipeline(_pipeline(contract_version=2)).ok


def test_malformed_pipeline_id_is_rejected():
    assert not validate_pipeline(_pipeline(pipeline_id="work-example")).ok


def test_missing_rollback_is_rejected():
    doc = _pipeline()
    del doc["rollback"]
    assert not validate_pipeline(doc).ok


def test_shell_text_as_command_is_rejected():
    """A command is a registered operation name, never shell text."""
    doc = _pipeline()
    doc["steps"][0]["command"] = "rm -rf / && echo pwned"
    assert not validate_pipeline(doc).ok


def test_unknown_rights_value_is_rejected():
    doc = _pipeline()
    doc["inputs"] = [{"id": "x", "rights": "totally-fine-trust-me"}]
    assert not validate_pipeline(doc).ok


def test_unknown_rights_is_representable_and_not_a_failure():
    """`unknown` is a legal value. It is still never permission."""
    doc = _pipeline()
    doc["inputs"] = [{"id": "x", "rights": "unknown"}]
    assert validate_pipeline(doc).ok


# ------------------------------------------------------------ pipeline graph --
def test_duplicate_step_id_is_caught():
    doc = _pipeline()
    doc["steps"][1]["id"] = "convert"
    errors = validate_pipeline_graph(doc)
    assert any("duplicate step id" in e for e in errors)


def test_needs_unknown_step_is_caught():
    doc = _pipeline()
    doc["steps"][1]["needs"] = ["nonexistent"]
    assert any("unknown step" in e for e in validate_pipeline_graph(doc))


def test_dependency_cycle_is_caught():
    doc = _pipeline()
    doc["steps"][0]["needs"] = ["errata"]
    assert any("cycle" in e for e in validate_pipeline_graph(doc))


def test_two_steps_claiming_one_output_is_caught():
    """Exactly one generator per output."""
    doc = _pipeline()
    doc["steps"][1]["outputs"] = doc["steps"][0]["outputs"]
    assert any("already produced by" in e for e in validate_pipeline_graph(doc))


def test_input_that_is_also_an_output_is_caught():
    doc = _pipeline()
    doc["steps"][0]["inputs"] = doc["steps"][0]["outputs"]
    assert any("both an input and an output" in e for e in validate_pipeline_graph(doc))


def test_self_dependency_is_caught():
    doc = _pipeline()
    doc["steps"][0]["needs"] = ["convert"]
    assert any("needs itself" in e for e in validate_pipeline_graph(doc))


# ---------------------------------------------------------------------- work --
def test_valid_work_passes():
    assert validate_work(_work()).ok


def test_work_id_must_be_semantic():
    assert not validate_work(_work(work_id="KnauerFrazy_1908")).ok


def test_generated_file_may_not_also_be_a_source():
    doc = _work()
    doc["outputs"] = ["sources/example.docx"]
    report = validate_work(doc)
    assert not report.ok
    assert any("may never also be a source" in e for e in report.errors)


def test_path_escaping_the_work_root_is_rejected():
    doc = _work()
    doc["outputs"] = ["../../etc/passwd"]
    report = validate_work(doc)
    assert not report.ok
    assert any("escapes the work root" in e for e in report.errors)


def test_missing_rights_is_rejected():
    doc = _work()
    del doc["rights"]
    assert not validate_work(doc).ok


# ---------------------------------------------------------------- provenance --
def test_repo_provenance_lock_is_valid():
    """The committed lock must satisfy its own contract."""
    report = validate_provenance_lock()
    assert report.ok, report.describe()


def test_mutable_tag_is_not_valid_provenance():
    doc = {
        "contract_version": 1,
        "inputs": [
            {
                "id": "external:example",
                "owner": "someone",
                "repository": "https://github.com/example/example",
                "revision": "v1.2.3",
                "rights": "publishable",
                "consumers": ["pipeline:x"],
            }
        ],
    }
    report = validate_provenance_lock(doc)
    assert not report.ok
    assert any("immutable 40-hex commit" in e for e in report.errors)


def test_provenance_entry_needs_a_consumer():
    doc = {
        "contract_version": 1,
        "inputs": [
            {
                "id": "external:example",
                "owner": "someone",
                "repository": "https://github.com/example/example",
                "revision": "a" * 40,
                "rights": "publishable",
            }
        ],
    }
    report = validate_provenance_lock(doc)
    assert any("consumer" in e for e in report.errors)


def test_committed_site_pipeline_validates():
    """pipelines/repo-site.yml — a YAML manifest, read as YAML not JSON."""
    manifest = repo_root() / "pipelines" / "repo-site.yml"
    report = validate_pipeline(manifest)
    assert report.ok, report.describe()


def test_unreadable_contract_raises_contract_error():
    with pytest.raises(ContractError):
        validate_pipeline(repo_root() / "pipelines" / "does-not-exist.yml")
