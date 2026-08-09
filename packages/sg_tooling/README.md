# `sg_tooling`

_Created: 09-08-2026 · Last updated: 09-08-2026_

Installable Python tooling for the [SanskritGrammar](https://github.com/gasyoun/SanskritGrammar)
monorepo. Delivered by Slice A of the
[architecture modernization plan](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/PLAN_SANSKRITGRAMMAR_ARCHITECTURE_MODERNIZATION_2026_2027.md).

## Install and run

```powershell
uv sync --frozen
uv run sg pipeline list
```

A clean environment must be able to install this and run `sg --help` with no
`PYTHONPATH` edit.

## Layers

| Layer | Responsibility | Forbidden dependency |
|---|---|---|
| [`cli`](https://github.com/gasyoun/SanskritGrammar/blob/main/packages/sg_tooling/src/sg_tooling/cli/main.py) | Argument parsing, dispatch, diagnostics, exit codes | No scholarly transformation logic |
| [`domain`](https://github.com/gasyoun/SanskritGrammar/blob/main/packages/sg_tooling/src/sg_tooling/domain/__init__.py) | Stable IDs, rights states, pipeline DAG semantics | No filesystem, network, subprocess, or database access |
| [`adapters`](https://github.com/gasyoun/SanskritGrammar/blob/main/packages/sg_tooling/src/sg_tooling/adapters/__init__.py) | Filesystem, YAML/JSON, external-object access | No hidden policy decisions |
| [`generators`](https://github.com/gasyoun/SanskritGrammar/blob/main/packages/sg_tooling/src/sg_tooling/generators/__init__.py) | Deterministic source-to-artifact transformations | No direct access outside adapters |
| [`contracts`](https://github.com/gasyoun/SanskritGrammar/blob/main/packages/sg_tooling/src/sg_tooling/contracts/validate.py) | Versioned schemas and validators | No generator-specific side effects |

The layering rule is enforced mechanically by
[`tests/contract/test_sg_tooling_layering.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/tests/contract/test_sg_tooling_layering.py),
not by convention alone.

## CLI

```powershell
sg pipeline list          # every declared manifest, sorted deterministically
sg pipeline check <id>    # schema + graph + provenance, no side effects
sg pipeline run <id>      # execute through registered commands
```

Exit codes are contractual because CI gates on them: `0` success · `1` a declared
pipeline failed · `2` usage error · `3` unknown pipeline id · `4` unreadable
contract.

## Extension points for the Wave-1 pilots

Slice A ships the registry and **zero** content generators. A pilot registers its
own without editing a Slice-A-owned file:

```python
# packages/sg_tooling/src/sg_tooling/generators/knauer.py   (Slice B / H1912)
from sg_tooling.generators import register

@register("work.convert_docx")
def convert_docx(step, context):
    ...
```

`register` refuses a duplicate name, so two pilots cannot silently claim one
command. [H1912](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1912-Codex_SanskritGrammar_architecture-knauer-vertical-pilot_29.07.26.md)
adds the DOCX/Pandoc adapter; [H1913](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1913-Codex_SanskritGrammar_architecture-sg-mo-021-vertical-pilot_29.07.26.md)
adds `adapters/dcs.py` over a pinned VisualDCS export.

## Ownership fence

This package owns grammar-specific adapters and repo-local contracts only.
Transliteration belongs to [`sanskrit-util`](https://github.com/sanskrit-lexicon/sanskrit-util),
DCS ingest to [`VisualDCS`](https://github.com/gasyoun/VisualDCS), review-sheet
rendering to [`csl-pyutil`](https://github.com/sanskrit-lexicon/csl-pyutil), and
root identity to [`WhitneyRoots`](https://github.com/gasyoun/WhitneyRoots).
Consume them through adapters; do not fork their logic.

_Dr. Mārcis Gasūns_
