"""Generator layer + the registered-command registry.

A pipeline manifest names a command as a string (``work.convert_docx``); the
runner resolves that string against this registry. It never passes manifest text
to a shell. That is the security contract in architecture section 14: pipeline
commands are *registered operations*, not arbitrary shell text from YAML.

Named extension point for the Wave-1 pilots (H1911 delivery item 7)
-------------------------------------------------------------------
Slice A ships the registry and zero content generators. A pilot registers its
own without editing any Slice-A-owned file::

    # packages/sg_tooling/src/sg_tooling/generators/knauer.py   (Slice B / H1912)
    from sg_tooling.generators import register

    @register("work.convert_docx")
    def convert_docx(step, context):
        ...

Import the module from the pilot's own test or entry point; ``register`` refuses
a duplicate name so two pilots cannot silently claim one command.

Module discovery (H1913 Slice C)
--------------------------------
A pilot module dropped into this package registers itself at import time; the
registry discovers and imports every sibling ``*.py`` (except ``__init__``)
lazily, on the first registry query. That is what makes a bare
``uv run sg pipeline run <pilot>`` resolve pilot commands without any shared
file importing them: registration still lives ONLY in each pilot's own module,
so the ownership fence holds, and a broken generator module fails loudly rather
than silently disappearing from the registry.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Callable, Mapping

__all__ = ["available_commands", "is_registered", "register", "resolve"]

_REGISTRY: dict[str, Callable[..., object]] = {}
_DISCOVERED = False


def _discover_pilot_modules() -> None:
    """Import every sibling pilot module once, sorted for determinism."""
    global _DISCOVERED
    if _DISCOVERED:
        return
    _DISCOVERED = True
    package_dir = Path(__file__).resolve().parent
    for path in sorted(package_dir.glob("*.py")):
        if path.name == "__init__.py" or path.name.startswith("_"):
            continue
        importlib.import_module(f"{__name__}.{path.stem}")

def register(name: str) -> Callable[[Callable[..., object]], Callable[..., object]]:
    """Register a callable under a manifest command name.

    Raises ``ValueError`` on a duplicate so ownership of a command name is
    unambiguous -- the one-generator-per-output rule starts here.
    """

    def decorator(func: Callable[..., object]) -> Callable[..., object]:
        if name in _REGISTRY:
            raise ValueError(f"command {name!r} is already registered by {_REGISTRY[name]!r}")
        _REGISTRY[name] = func
        return func

    return decorator


def resolve(name: str) -> Callable[..., object]:
    """Look up a registered command, or raise ``KeyError`` with the known set."""
    _discover_pilot_modules()
    try:
        return _REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"command {name!r} is not a registered sg_tooling operation; "
            f"registered: {sorted(_REGISTRY)}"
        ) from None


def is_registered(name: str) -> bool:
    _discover_pilot_modules()
    return name in _REGISTRY


def available_commands() -> Mapping[str, Callable[..., object]]:
    """Return a read-only snapshot of the registry."""
    _discover_pilot_modules()
    return dict(_REGISTRY)
