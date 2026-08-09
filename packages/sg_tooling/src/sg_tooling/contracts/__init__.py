"""Versioned schemas and validators for the SanskritGrammar contracts.

This layer owns schema loading and validation only. It has no generator-specific
side effects and it never decides policy: a caller asks whether a document
satisfies a contract and gets structured errors back.

Contracts (docs/ARCHITECTURE_SANSKRITGRAMMAR_MODULAR_MONOREPO.md section 6):

* ``pipeline`` -- ``pipelines/pipeline.schema.json``
* ``work``     -- ``pipelines/work.schema.json``
* ``provenance`` -- ``data/provenance.lock.json``

Validation rejects unknown keys wherever silent acceptance would change
execution. A missing optional rights determination stays representable as
``unknown`` and is NOT a validation failure -- but it is never permission
either; the publication gate is separate and fails closed.
"""
from sg_tooling.contracts.validate import (
    CONTRACT_VERSION,
    RIGHTS_VALUES,
    ContractError,
    ValidationReport,
    read_contract,
    schema_path,
    validate_pipeline,
    validate_pipeline_graph,
    validate_provenance_lock,
    validate_work,
)

__all__ = [
    "CONTRACT_VERSION",
    "RIGHTS_VALUES",
    "ContractError",
    "ValidationReport",
    "read_contract",
    "schema_path",
    "validate_pipeline",
    "validate_pipeline_graph",
    "validate_provenance_lock",
    "validate_work",
]
