# Tests

Unit tests for the Python build scripts under [`scripts/`](../scripts). Run from the repo root:

```bash
pip install -r scripts/requirements-dev.txt
python -m pytest
```

These are **characterization tests**: they pin the *current* behavior of the pure
helper functions so that a future refactor which changes that behavior fails loudly
instead of silently corrupting generated output. Every asserted value was produced by
running the function under test, not hand-guessed.

| File | Covers |
|---|---|
| `test_slugify.py` | the two divergent `slugify` functions (`build_whitney` vs `mdx_postprocess`) |
| `test_build_whitney.py` | IAST→Devanagari transliteration, cell classifiers, MDX-safe escaping, table-cell regeneration |
| `test_mdx_postprocess.py` | brace escaping, fence splitting, degenerate-table dropping, frontmatter title resolution |
| `test_build_errata.py` | small helpers + the `load_book` dedup/merge and `changelog_versions` parsing |
| `test_build_claims.py` | `norm_fact` verdict coercion, `md_cell`, register `counts` |
| `test_build_quantifiers.py` | the ASCII `bar` meter, `sample_metrics` confusion matrix, `pop_estimate` |

`conftest.py` puts `scripts/` on `sys.path` so the standalone scripts import as modules
(each guards its entry point with `if __name__ == "__main__":`, so importing runs nothing).

CI runs this suite plus a full Docusaurus build on every PR — see
[`.github/workflows/ci.yml`](../.github/workflows/ci.yml).
