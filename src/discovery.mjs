// Tracked-content discovery for the Docusaurus book site.
//
// The original implementation scanned the filesystem (`fs.readdirSync`) for
// top-level directories containing at least one `.mdx`. On a populated working
// tree that reads **ignored** archival MDX (e.g. `Concordance/UshaSanka_Ph.D_2014/`
// is gitignored but present on disk), and a single malformed front-matter file
// in such an archive killed `npm run build` locally while CI stayed green on
// the fresh clone. See docs/architecture/baseline/H1911_A0_BASELINE.md.
//
// This module derives the discovered set from `git ls-files`, so anything
// `.gitignore`'d is never read. A newly-tracked `.mdx` is still picked up
// automatically at build time — this is not a publication allowlist, it is
// "respect .gitignore" plus an explicit, tested deny policy.
//
// Two layers, both required (architecture § 8.2). Neither substitutes for the
// other, and both fail closed:
//
//   1. TRACKED — only `git ls-files` output is a discovery candidate (A3).
//   2. DENY    — a candidate is rejected when any path segment names a
//                raw/private/source/review/draft/archive/scratch/cache/
//                worktree/build surface, when the filename carries a denied
//                suffix, when front matter marks it draft/private/archived/
//                unpublished, or when it is arbitrary root MDX outside a
//                content zone.
//
// Measured when the deny layer landed (H2309, 09-08-2026): **265** tracked
// `.mdx`, of which **zero** were denied — no tracked MDX sits in a denied
// segment, none carries a denied suffix, none is flagged in front matter, and
// the 14 discovered book dirs are unchanged. So this layer is a no-op on today's
// content by construction and changes nothing about the published set; it exists
// so a future private/draft/archival MDX that someone `git add`s cannot silently
// publish merely because it is tracked.
//
// That 265 is why `listTrackedFiles` uses `-z` and filters in JS. `git ls-files`
// WITHOUT `-z` C-quotes any path containing non-ASCII bytes (`"Ap\303\250..."`),
// so the line stops ending in `.mdx` and a naive `git ls-files | grep '\.mdx$'`
// audit undercounts — it reported 203 here, missing 62 Cyrillic/IAST-named
// files. An audit that reads this module's output is authoritative; one that
// greps unquoted `ls-files` is not.
//
// Part of Slice A (delivery and publication safety): A3 discovery, A4 tests.

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

// Path segments that are never publishable, at ANY depth. Compared after NFC
// normalization, case-insensitively (architecture § 8.2 steps 3–4), because a
// Windows checkout and a Linux checkout must agree.
export const DENY_SEGMENTS = new Set([
  'raw', '_raw',
  'private', '_private',
  'source', 'sources',
  'review', '_review', 'reviews',
  'draft', 'drafts', '_draft',
  'archive', 'archives', '_archive',
  'scratch', '_scratch',
  'cache', '_cache',
  'ignored', '_ignored',
  'worktree', 'worktrees',
  'node_modules', 'build', '.docusaurus', '.git',
  'fixtures', '__pycache__',
]);

// A filename whose stem ends in one of these is denied even inside an allowed
// zone: `notes.draft.mdx` is a draft wherever it sits.
export const DENY_FILENAME_SUFFIXES = ['.ignored', '.private', '.draft', '.archive'];

// Front-matter keys that withhold publication. `publish: false` is the inverse
// form; the rest are positive flags.
const DENY_FRONTMATTER_TRUE = ['draft', 'private', 'archived'];
const DENY_FRONTMATTER_FALSE = ['publish'];

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

function normalizeSegment(segment) {
  return segment.normalize('NFC').toLowerCase();
}

// ---------------------------------------------------------------- deny rules --

export function deniedBySegment(relPath) {
  const segments = relPath.split('/').slice(0, -1).map(normalizeSegment);
  return segments.find((s) => DENY_SEGMENTS.has(s)) ?? null;
}

export function deniedByFilename(relPath) {
  const base = normalizeSegment(relPath.split('/').pop() ?? '');
  if (!base.endsWith('.mdx')) return null;
  const stem = base.slice(0, -'.mdx'.length);
  return DENY_FILENAME_SUFFIXES.find((suffix) => stem.endsWith(suffix)) ?? null;
}

// Arbitrary root MDX is not publishable: a content zone is a directory. The
// previous implementation happened to drop these only because a root file
// produced a `foo.mdx/**/*.mdx` include glob that matched nothing — correct
// outcome, accidental mechanism. This makes it a rule.
export function deniedAsRootMdx(relPath) {
  return relPath.includes('/') ? null : 'arbitrary root MDX outside a content zone';
}

// Parse only the leading front-matter block, and only within a bounded prefix:
// an MDX file is untrusted input (architecture § 14) and must not be able to
// cost unbounded work at config time.
export function frontmatterDenial(text) {
  if (typeof text !== 'string') return null;
  const head = text.slice(0, 4096);
  if (!/^---\r?\n/.test(head)) return null;
  const end = head.indexOf('\n---', 4);
  const block = end === -1 ? head : head.slice(4, end);
  for (const line of block.split(/\r?\n/)) {
    const match = /^([A-Za-z_][A-Za-z0-9_-]*)\s*:\s*(.+?)\s*$/.exec(line);
    if (!match) continue;
    const key = match[1].toLowerCase();
    const value = match[2].toLowerCase().replace(/^["']|["']$/g, '');
    if (DENY_FRONTMATTER_TRUE.includes(key) && value === 'true') return `${key}: true`;
    if (DENY_FRONTMATTER_FALSE.includes(key) && value === 'false') return `${key}: false`;
  }
  return null;
}

// Classify one candidate. Returns null when publishable, else the reason.
// Fail-closed: an unreadable candidate is denied, never silently published.
export function denialReason(relPath, cwd = process.cwd(), skipDirs = DEFAULT_SKIP_DIRS) {
  const rootDenial = deniedAsRootMdx(relPath);
  if (rootDenial) return rootDenial;

  const top = relPath.split('/')[0];
  if (skipDirs.has(top) || top.startsWith('.')) {
    return `non-content top-level directory: ${top}`;
  }

  const segment = deniedBySegment(relPath);
  if (segment) return `denied path segment: ${segment}`;

  const suffix = deniedByFilename(relPath);
  if (suffix) return `denied filename suffix: ${suffix}.mdx`;

  let text;
  try {
    const fd = fs.openSync(path.join(cwd, relPath), 'r');
    try {
      const buffer = Buffer.alloc(4096);
      const read = fs.readSync(fd, buffer, 0, 4096, 0);
      text = buffer.subarray(0, read).toString('utf8');
    } finally {
      fs.closeSync(fd);
    }
  } catch (_err) {
    // Tracked but absent from this checkout (sparse/partial): nothing to read,
    // so nothing to publish.
    return 'candidate could not be read';
  }

  const flagged = frontmatterDenial(text);
  return flagged ? `front matter withholds publication (${flagged})` : null;
}

// --------------------------------------------------------------- discovery ---

export function discoverTrackedMdx(cwd = process.cwd()) {
  const tracked = listTrackedFiles(cwd);
  if (tracked === null) return [];
  return tracked.filter((p) => p.endsWith('.mdx'));
}

// Tracked MDX that survives the deny policy. This is the publishable set.
export function discoverPublishableMdx(cwd = process.cwd(), skipDirs = DEFAULT_SKIP_DIRS) {
  return discoverTrackedMdx(cwd)
    .filter((p) => denialReason(p, cwd, skipDirs) === null)
    .sort();
}

// Tracked MDX the deny policy rejected, with the reason — surfaced so a build
// log shows WHY something is unpublished instead of it vanishing silently.
export function discoverDeniedMdx(cwd = process.cwd(), skipDirs = DEFAULT_SKIP_DIRS) {
  return discoverTrackedMdx(cwd)
    .map((p) => ({ path: p, reason: denialReason(p, cwd, skipDirs) }))
    .filter((entry) => entry.reason !== null)
    .sort((a, b) => a.path.localeCompare(b.path));
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

// Every on-disk MDX that is NOT publishable — gitignored archival material and
// tracked-but-denied files alike. Docusaurus excludes these per-file, so a
// populated working tree builds the same as a fresh clone.
export function discoverIgnoredMdx(cwd = process.cwd(), skipDirs = DEFAULT_SKIP_DIRS) {
  const publishable = new Set(discoverPublishableMdx(cwd, skipDirs));
  return listDiskMdx(cwd, skipDirs).filter((p) => !publishable.has(p));
}

export function discoverBookDirs(publishableMdx, skipDirs = DEFAULT_SKIP_DIRS) {
  const dirs = new Set();
  for (const p of publishableMdx) {
    const top = p.split('/')[0];
    if (!top || skipDirs.has(top) || top.startsWith('.') || !p.includes('/')) continue;
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

// Derive `exclude` glob patterns that suppress every non-publishable MDX file.
// Per-file excludes (not per-directory) so that a publishable book .mdx sitting
// beside an ignored draft .mdx in the same directory stays published. Each path
// is escaped for fast-glob/picomatch metacharacters.
export function discoverExcludePatterns(ignoredMdx) {
  return [...ignoredMdx].sort().map((p) => escapeGlob(p));
}

export function discoverSite(cwd = process.cwd(), skipDirs = DEFAULT_SKIP_DIRS) {
  const trackedMdx = discoverTrackedMdx(cwd);
  const publishableMdx = discoverPublishableMdx(cwd, skipDirs);
  const deniedMdx = discoverDeniedMdx(cwd, skipDirs);
  const ignoredMdx = discoverIgnoredMdx(cwd, skipDirs);
  const bookDirs = discoverBookDirs(publishableMdx, skipDirs);
  return {
    bookDirs,
    // Sorted by normalized POSIX path so the include list is byte-identical on
    // Windows and Linux (architecture § 8.1).
    include: bookDirs.map((d) => `${d}/**/*.mdx`),
    exclude: discoverExcludePatterns(ignoredMdx),
    trackedCount: trackedMdx.length,
    publishableCount: publishableMdx.length,
    deniedCount: deniedMdx.length,
    denied: deniedMdx,
    ignoredCount: ignoredMdx.length,
  };
}
