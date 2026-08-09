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
"""
from __future__ import annotations

from typing import Callable, Mapping

__all__ = ["available_commands", "is_registered", "register", "resolve"]

_REGISTRY: dict[str, Callable[..., object]] = {}


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
    try:
        return _REGISTRY[name]
    except KeyError:
        raise KeyError(
            f"command {name!r} is not a registered sg_tooling operation; "
            f"registered: {sorted(_REGISTRY)}"
        ) from None


def is_registered(name: str) -> bool:
    return name in _REGISTRY


def available_commands() -> Mapping[str, Callable[..., object]]:
    """Return a read-only snapshot of the registry."""
    return dict(_REGISTRY)
