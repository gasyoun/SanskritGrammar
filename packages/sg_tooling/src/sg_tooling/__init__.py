"""sg_tooling — installable Python tooling for the SanskritGrammar monorepo.

Layer contract (docs/ARCHITECTURE_SANSKRITGRAMMAR_MODULAR_MONOREPO.md section 5.2):

======================  ====================================================
Layer                   Responsibility
======================  ====================================================
``cli``                 Argument parsing, dispatch, diagnostics, exit codes.
``domain``              Stable IDs, pipeline DAG semantics, rights states.
                        No filesystem, network, subprocess, or DB access.
``adapters``            Filesystem, YAML/JSON, external object access.
``generators``          Deterministic source-to-artifact transformations.
``contracts``           Versioned schemas and validators.
======================  ====================================================

Slice A (H2309) delivers the package skeleton, the pipeline/work/provenance
contracts, and the ``sg pipeline check|run|list`` CLI seam. The Wave-1 pilots
(H1912 Knauer, H1913 SG-MO-021) register their generators through the named
extension points documented in ``sg_tooling.generators``.
"""

__all__ = ["__version__"]

__version__ = "0.1.0"
