"""Generator extension registry."""

_GENERATORS: dict[str, object] = {}


def register(name: str, generator: object) -> None:
    if name in _GENERATORS:
        raise ValueError(f"generator already registered: {name}")
    _GENERATORS[name] = generator

