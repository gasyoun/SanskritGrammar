"""CLI layer: argument parsing, dispatch, diagnostics, exit codes.

No scholarly transformation logic lives here (architecture section 5.2).
"""
from sg_tooling.cli.main import build_parser, main

__all__ = ["build_parser", "main"]
