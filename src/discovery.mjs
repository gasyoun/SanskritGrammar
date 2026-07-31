// Tracked-content discovery for the Docusaurus book site.
//
// The previous implementation scanned the filesystem (`fs.readdirSync`) for
// top-level directories containing at least one `.mdx`. On a populated working
// tree that reads **ignored** archival MDX (e.g. `Concordance/UshaSanka_Ph.D_2014/`
// is gitignored but present on disk), and a single malformed front-matter file
// in such an archive killed `npm run build` locally while CI stayed green on
// the fresh clone. See docs/architecture/baseline/H1911_A0_BASELINE.md.
//
// This module derives the discovered set from `git ls-files`, so anything
// `.gitignore`'d is never read. A newly-tracked `.mdx` is still picked up
// automatically at build time — this is not a publication allowlist, it is
// "respect .gitignore". The directory-level skip set is retained only to keep
// non-content top-level dirs (src, scripts, build) out of the sidebar even if
// a tracked `.mdx` lands there.
//
// Part of H1911 Slice A (delivery and publication safety).

import { execSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';

export const DEFAULT_SKIP_DIRS = new Set([
  'node_modules',
  'build',
  '.docusaurus',
  'src',
  '.git',
  '.github',
  'scripts',
  'tests',
  'docs',
  'data',
  'pipelines',
  'packages',
  'apps',
]);

function runGit(cwd, args) {
  try {
    return execSync(`git ${args}`, {
      cwd,
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    });
  } catch (_err) {
    return null;
  }
}

// List all tracked (cached) files. Filtering by extension is done in JS to
// avoid the shell-quoting trap that `'*.mdx'` is passed literally to git on
// Windows (cmd.exe does not strip single quotes), which returns nothing.
function listTrackedFiles(cwd) {
  const out = runGit(cwd, 'ls-files -z');
  return out === null ? null : out.split('\0').filter(Boolean);
}

export function discoverTrackedMdx(cwd = process.cwd()) {
  const tracked = listTrackedFiles(cwd);
  if (tracked === null) return [];
  return tracked.filter((p) => p.endsWith('.mdx'));
}

// Walk the filesystem for every `.mdx` under the repo root, skipping build
// artifacts and node_modules. Used to compute the untracked/ignored MDX set
// (on-disk minus tracked), which Docusaurus must exclude so a populated
// working tree builds the same as a fresh clone. A filesystem walk is used
// (rather than `git ls-files -i -o --exclude-standard`) because the latter is
// flaky for filenames with spaces/dots under Windows cmd quoting.
function listDiskMdx(root, skipDirs) {
  const out = [];
  const stack = [root];
  while (stack.length) {
    const dir = stack.pop();
    let entries;
    try {
      entries = fs.readdirSync(dir, { withFileTypes: true });
    } catch (_err) {
      continue;
    }
    for (const e of entries) {
      if (e.name.startsWith('.')) continue;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) {
        if (skipDirs.has(e.name)) continue;
        stack.push(full);
      } else if (e.isFile() && e.name.endsWith('.mdx')) {
        out.push(path.relative(root, full).split(path.sep).join('/'));
      }
    }
  }
  return out.sort();
}

export function discoverIgnoredMdx(cwd = process.cwd(), skipDirs = DEFAULT_SKIP_DIRS) {
  const tracked = new Set(discoverTrackedMdx(cwd));
  return listDiskMdx(cwd, skipDirs).filter((p) => !tracked.has(p));
}

export function discoverBookDirs(trackedMdx, skipDirs = DEFAULT_SKIP_DIRS) {
  const dirs = new Set();
  for (const path of trackedMdx) {
    const top = path.split('/')[0];
    if (!top || skipDirs.has(top) || top.startsWith('.')) continue;
    dirs.add(top);
  }
  return [...dirs].sort();
}

// Escape a literal path for use as a glob pattern in fast-glob/picomatch.
// `()[]*?!+|@` are metacharacters; wrap each in a single-char bracket class so
// the pattern matches the literal character. Backslashes are also escaped.
// Used for `exclude` patterns derived from ignored MDX paths, so filenames
// like `A NonPaninian Approach (article).mdx` don't get misread as extglob.
function escapeGlob(pattern) {
  return pattern.replace(/[\\*?[\]()!+|@]/g, (ch) => `[${ch}]`);
}

// Derive `exclude` glob patterns that suppress every ignored MDX file, so a
// populated working tree (carrying gitignored archival MDX) builds the same as
// a fresh clone. Per-file excludes (not per-directory) so that a tracked book
// .mdx sitting beside an ignored draft .mdx in the same directory stays
// published. Each path is escaped for fast-glob/picomatch metacharacters.
export function discoverExcludePatterns(ignoredMdx) {
  return [...ignoredMdx].sort().map((p) => escapeGlob(p));
}

export function discoverSite(cwd = process.cwd(), skipDirs = DEFAULT_SKIP_DIRS) {
  const trackedMdx = discoverTrackedMdx(cwd);
  const ignoredMdx = discoverIgnoredMdx(cwd);
  const bookDirs = discoverBookDirs(trackedMdx, skipDirs);
  return {
    bookDirs,
    include: bookDirs.map((d) => `${d}/**/*.mdx`),
    exclude: discoverExcludePatterns(ignoredMdx),
    trackedCount: trackedMdx.length,
    ignoredCount: ignoredMdx.length,
  };
}
