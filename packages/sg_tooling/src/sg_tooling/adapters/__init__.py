"""Adapter layer: all filesystem, YAML/JSON, and external-object access.

Adapters translate shape, encoding, and path conventions. They make no hidden
policy decisions (architecture section 5.2) and they never reinterpret upstream
scholarly meaning.

Ownership fence (plan ruling 11, architecture section 9) -- SanskritGrammar
consumes these through pinned adapters and does NOT fork their logic:

===========================  =========================================
Concern                      Canonical owner
===========================  =========================================
transliteration / normalize  sanskrit-util
DCS ingest / corpus master   VisualDCS
review-sheet rendering       csl-pyutil
Whitney root identity        WhitneyRoots
===========================  =========================================

Named extension point for the Wave-1 pilots: H1912 (Knauer) adds a DOCX/Pandoc
adapter here; H1913 (SG-MO-021) adds ``adapters/dcs.py`` as a thin, generic,
characterized wrapper over a pinned VisualDCS export. Neither may embed corpus
engine logic.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

__all__ = ["read_json", "read_yaml", "resolve_within"]


class PathEscapeError(ValueError):
    """A contract path resolved outside its allowed root."""


def resolve_within(root: Path, candidate: str | Path) -> Path:
    """Resolve ``candidate`` and prove it stays inside ``root``.

    Guards the traversal/junction rule in architecture section 14: every contract
    path is normalized, bounded to an allowed root, and checked against escaping
    links. ``Path.resolve()`` follows symlinks and junctions, so an escaping link
    is caught here rather than at read time.
    """
    base = Path(root).resolve()
    target = (base / candidate).resolve() if not Path(candidate).is_absolute() else Path(candidate).resolve()
    if base != target and base not in target.parents:
        raise PathEscapeError(f"{candidate!r} resolves outside {base}")
    return target


def read_json(path: str | Path) -> Any:
    """Read UTF-8 JSON, refusing a BOM (banned repo-wide)."""
    text = Path(path).read_text(encoding="utf-8")
    if text.startswith("﻿"):
        raise ValueError(f"{path}: UTF-8 BOM is banned in this repo")
    return json.loads(text)


def read_yaml(path: str | Path) -> Any:
    """Read a YAML contract with ``yaml.safe_load``.

    ``safe_load`` (never ``load``) keeps a YAML contract from becoming hidden
    executable code -- the injection risk named in architecture section 18.
    """
    import yaml  # local import: keeps the domain layer import-free of adapters

    text = Path(path).read_text(encoding="utf-8")
    if text.startswith("﻿"):
        raise ValueError(f"{path}: UTF-8 BOM is banned in this repo")
    return yaml.safe_load(text)
