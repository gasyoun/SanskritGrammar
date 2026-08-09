"""Contract test: the sg_tooling layer boundaries hold mechanically.

The architecture assigns each layer a forbidden dependency
(docs/ARCHITECTURE_SANSKRITGRAMMAR_MODULAR_MONOREPO.md section 5.2). Prose alone
cannot keep those boundaries: this test reads the AST of each layer and fails if
a forbidden import appears, so the fence survives future edits.

The load-bearing rule is the domain layer: it must stay pure (no filesystem,
network, subprocess, or database access) so scholarly semantics are testable
without fixtures.
"""
from __future__ import annotations

import ast
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = REPO_ROOT / "packages" / "sg_tooling" / "src" / "sg_tooling"

# Modules the pure domain layer may never reach for, directly or transitively
# through a module-level import.
IMPURE_MODULES = frozenset(
    {
        "os",
        "io",
        "pathlib",
        "shutil",
        "glob",
        "subprocess",
        "socket",
        "sqlite3",
        "urllib",
        "urllib.request",
        "requests",
        "httpx",
        "yaml",
        "json",
    }
)


def _module_files(layer: str) -> list[Path]:
    layer_root = PACKAGE_ROOT / layer
    if not layer_root.exists():
        return []
    return sorted(p for p in layer_root.rglob("*.py"))


def _imported_names(path: Path) -> set[str]:
    """Return every module name imported at module level in ``path``.

    Imports nested inside a function body are deliberately excluded: a local
    import is how the adapter layer keeps a heavy dependency out of import time,
    and the layering rule is about what a module pulls in when it loads.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in tree.body:  # module level only
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module)
    return names


def test_package_layout_exists() -> None:
    """Every layer named by the architecture is present."""
    for layer in ("cli", "domain", "adapters", "generators", "contracts"):
        assert (PACKAGE_ROOT / layer / "__init__.py").is_file(), f"missing layer: {layer}"


@pytest.mark.parametrize("path", _module_files("domain"), ids=lambda p: p.name)
def test_domain_layer_is_pure(path: Path) -> None:
    """The domain layer touches no filesystem, network, subprocess, or DB."""
    offenders = sorted(_imported_names(path) & IMPURE_MODULES)
    assert not offenders, (
        f"{path.relative_to(REPO_ROOT).as_posix()} imports {offenders} at module level; "
        "the domain layer must stay pure (architecture section 5.2)"
    )


@pytest.mark.parametrize("path", _module_files("domain"), ids=lambda p: p.name)
def test_domain_does_not_import_sibling_layers(path: Path) -> None:
    """Domain sits at the bottom: it imports no other sg_tooling layer."""
    forbidden = {
        name
        for name in _imported_names(path)
        if name.startswith("sg_tooling.")
        and not name.startswith("sg_tooling.domain")
    }
    assert not forbidden, f"{path.name} imports {sorted(forbidden)}; domain may not depend upward"


def test_cli_carries_no_scholarly_transformation() -> None:
    """The CLI dispatches; it does not transform content itself."""
    source = (PACKAGE_ROOT / "cli" / "main.py").read_text(encoding="utf-8")
    for banned in ("indic_transliteration", "sanscript", "sqlite3", "docx"):
        assert banned not in source, (
            f"cli/main.py references {banned!r}; scholarly transformation belongs "
            "in generators/adapters, not the CLI layer"
        )


def test_generators_registry_is_empty_in_slice_a() -> None:
    """Slice A ships the registry with zero content generators.

    The Wave-1 pilots (H1912 Knauer, H1913 SG-MO-021) register their own. If this
    starts failing, a generator landed in a Slice-A-owned file, which is exactly
    the ownership fence the plan draws.
    """
    sys.path.insert(0, str(PACKAGE_ROOT.parent))
    try:
        from sg_tooling.generators import available_commands
    finally:
        sys.path.pop(0)
    assert available_commands() == {}, (
        "Slice A must not register content generators; a pilot owns its own"
    )
