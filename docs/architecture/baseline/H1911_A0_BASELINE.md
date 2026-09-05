# H1911 Slice A — baseline (A0)

_Created: 31-07-2026 · Last updated: 31-07-2026_

Recorded before any Slice A change, on branch `h1911-architecture-delivery-safety`
off `origin/main` HEAD `a29b50f4499d9db6063eaa3e1bb2803e8bce4f07`
(0.116.0).

## Commands and results

| Command | Result |
|---|---|
| `git status --short` | clean tree, five untracked files under `GasunsDhatu_2014/` (RWS review artefacts) + `curl.txt` |
| `git ls-files` count | 1215 tracked files |
| `python -m pytest -q` | **167 passed** (1 skipped), 88 `codecs.open` deprecation warnings from `indic_transliteration` |
| `npm ci` | already installed (lockfile present) |
| `npm run build` | **RED** locally — see populated-archive defect below |
| `gh run list --workflow=ci.yml --limit 1` | CI **green** on `main` for `a29b50f` (2m2s) |

## Known populated-archive discovery defect (A3 target)

`npm run build` fails locally with:

```text
Error: Can't process doc metadata for doc at path
  Concordance/UshaSanka_Ph.D_2014/Kriya Paryayas listed for Ph.D.mdx
  cause: js-yaml unknown escape sequence in front matter `\-`
```

Cause: `Concordance/UshaSanka_Ph.D_2014/` is **gitignored** (`.gitignore:149`),
so a fresh clone (CI) does not carry it and builds green. A populated working
tree carries the ignored archival MDX, and `docusaurus.config.mjs` auto-discovery
scans the **filesystem** (`fs.readdirSync`) rather than the tracked set, so the
private/archival MDX is read and breaks the YAML parse.

This is the defect Slice A3 must close: auto-discovery constrained to tracked
allowed content roots with explicit exclusions for ignored/private/raw/draft/
review/archive/scratch MDX. A fresh clone must keep building; a populated
clone must build the same way.

## Stop conditions (per handoff)

Stop this lane if the protected baseline fails for a reason unrelated to the
known populated archive discovery defect. The protected baseline is: pytest
green on a fresh clone; `npm run build` green on a fresh clone. Both hold.

Provenance: Sonnet 4.6 (`claude-sonnet-4-6`) executing H1911 on
opencode (`z-ai/glm-5.2`).

_Dr. Mārcis Gasūns_
