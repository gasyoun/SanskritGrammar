"""Pure domain layer: stable identities, rights states, pipeline DAG semantics.

Forbidden dependency (architecture section 5.2): this layer must not touch the
filesystem, network, subprocesses, Docusaurus, or a database. Everything here
takes values in and returns values out, so it is testable without fixtures.
``tests/contract/test_sg_tooling_layering.py`` enforces that mechanically.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = [
    "PUBLICATION_SAFE_RIGHTS",
    "RIGHTS_VALUES",
    "StableId",
    "is_publication_safe",
    "parse_stable_id",
    "topological_order",
]

RIGHTS_VALUES = (
    "publishable",
    "publishable-derived-input",
    "restricted-source",
    "per-file",
    "unknown",
)

# Only these two are publication-safe. Absent / unknown / unrecognised fails
# closed: a technical ability to read material is not publication permission
# (architecture section 14).
PUBLICATION_SAFE_RIGHTS = ("publishable", "publishable-derived-input")

_ID_KINDS = ("work", "pipeline", "sangram", "external", "repo")
_SLUG = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


@dataclass(frozen=True)
class StableId:
    """A semantic identity of the form ``<kind>:<slug>``.

    Stable identities are semantic, never path-derived: a folder rename must not
    be able to mint a new scholarly entity (architecture section 6.4).
    """

    kind: str
    slug: str

    def __str__(self) -> str:
        return f"{self.kind}:{self.slug}"


def parse_stable_id(raw: str) -> StableId:
    """Parse ``work:knauer-frazy-1908`` into a :class:`StableId`.

    Raises ``ValueError`` on an unknown kind or a non-slug tail so a typo can
    never silently become a second entity.
    """
    if not isinstance(raw, str) or ":" not in raw:
        raise ValueError(f"stable id must look like '<kind>:<slug>', got {raw!r}")
    kind, _, slug = raw.partition(":")
    if kind not in _ID_KINDS:
        raise ValueError(f"unknown stable-id kind {kind!r}; expected one of {list(_ID_KINDS)}")
    if not _SLUG.match(slug):
        raise ValueError(f"{slug!r} is not a lowercase-hyphen slug")
    return StableId(kind=kind, slug=slug)


def is_publication_safe(rights: str | None) -> bool:
    """Fail closed: only an explicitly publication-safe rights class passes."""
    return rights in PUBLICATION_SAFE_RIGHTS


def topological_order(graph: dict[str, list[str]]) -> list[str]:
    """Return a deterministic execution order for a ``needs`` graph.

    ``graph`` maps a step id to the step ids it depends on. Ties are broken by
    sorted name so the order is identical on Windows and Linux -- determinism is
    a contract here, not a nicety (verification section 6). Raises ``ValueError``
    on a cycle or an unknown dependency.
    """
    unknown = {dep for deps in graph.values() for dep in deps if dep not in graph}
    if unknown:
        raise ValueError(f"unknown dependencies: {sorted(unknown)}")

    remaining = {node: sorted(set(deps)) for node, deps in graph.items()}
    ordered: list[str] = []
    while remaining:
        ready = sorted(node for node, deps in remaining.items() if not deps)
        if not ready:
            raise ValueError(f"dependency cycle among {sorted(remaining)}")
        for node in ready:
            ordered.append(node)
            del remaining[node]
        for deps in remaining.values():
            deps[:] = [d for d in deps if d not in ordered]
    return ordered
