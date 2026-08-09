// Discovery-boundary contract tests (A4).
//
// Runs the fixture matrix the verification doc requires (V-A § "Discovery
// boundary"), against a REAL throwaway git repo in a temp dir — because the
// module's first layer is `git ls-files`, so a fake filesystem would not
// exercise the thing being tested.
//
// | Fixture                                        | Expected              |
// |------------------------------------------------|-----------------------|
// | valid MDX inside an allowed work/content zone  | discovered            |
// | valid Sangram MDX inside its allowed zone      | discovered            |
// | malformed MDX inside an ignored archive        | not read, build green |
// | MDX under raw/private/source/review/draft/     | not discovered        |
// |   archive/scratch                              |                       |
// | arbitrary root MDX                             | not discovered        |
// | cache, worktree, node_modules, build output    | not discovered        |
//
// Run: npm run test:discovery
import { strict as assert } from 'node:assert';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { after, before, describe, test } from 'node:test';

import {
  DENY_FILENAME_SUFFIXES,
  DENY_SEGMENTS,
  deniedAsRootMdx,
  deniedByFilename,
  deniedBySegment,
  denialReason,
  discoverBookDirs,
  discoverDeniedMdx,
  discoverExcludePatterns,
  discoverPublishableMdx,
  discoverSite,
  discoverTrackedMdx,
  frontmatterDenial,
} from '../../src/discovery.mjs';

const MDX = (title) => `---\ntitle: ${title}\n---\n\n# ${title}\n\nBody.\n`;

// Front matter that would crash an MDX compile if it were ever read — the
// H1911 failure mode: one malformed file in an ignored archive killed the
// local build while CI stayed green.
const MALFORMED_MDX = '---\ntitle: [unclosed\n  bad: : :\n---\n\n{ unbalanced\n';

let repo;

function git(...args) {
  execFileSync('git', args, { cwd: repo, stdio: ['ignore', 'pipe', 'ignore'] });
}

function write(rel, body) {
  const full = path.join(repo, rel);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, body, 'utf8');
  return rel;
}

before(() => {
  repo = fs.mkdtempSync(path.join(os.tmpdir(), 'sg-discovery-'));
  git('init', '--quiet');
  git('config', 'user.email', 'test@example.invalid');
  git('config', 'user.name', 'Discovery Fixture');
  git('config', 'commit.gpgsign', 'false');

  // .gitignore mirrors the real repo's shape: an archival dir stays out of git
  // but present on disk (the populated-archive case).
  write('.gitignore', 'IgnoredArchive/\nnode_modules/\nbuild/\n.docusaurus/\n');

  // --- publishable ---------------------------------------------------------
  write('ExampleWork_1900/example.mdx', MDX('Example work'));
  write('ExampleWork_1900/nested/second.mdx', MDX('Second page'));
  write('sangram/articles/future/index.mdx', MDX('Sangram future'));

  // --- tracked but denied --------------------------------------------------
  write('ExampleWork_1900/sources/transcription.mdx', MDX('Raw source'));
  write('ExampleWork_1900/review/sheet.mdx', MDX('Review sheet'));
  write('ExampleWork_1900/drafts/wip.mdx', MDX('Draft'));
  write('ExampleWork_1900/_private/notes.mdx', MDX('Private'));
  write('ExampleWork_1900/archive/old.mdx', MDX('Archived'));
  write('ExampleWork_1900/scratch/tmp.mdx', MDX('Scratch'));
  write('ExampleWork_1900/raw/ocr.mdx', MDX('Raw OCR'));
  write('ExampleWork_1900/notes.draft.mdx', MDX('Suffix draft'));
  write('ExampleWork_1900/secret.private.mdx', MDX('Suffix private'));
  write('ExampleWork_1900/flagged.mdx', '---\ntitle: Flagged\ndraft: true\n---\n\nBody.\n');
  write('ExampleWork_1900/unpublished.mdx', '---\ntitle: Held\npublish: false\n---\n\nBody.\n');
  write('root-level.mdx', MDX('Arbitrary root MDX'));
  write('docs/internal.mdx', MDX('Docs are not content'));
  write('tests/fixtures/sample.mdx', MDX('Test fixture'));

  git('add', '-A');
  git('commit', '--quiet', '-m', 'discovery fixture');

  // --- present on disk, NOT tracked (gitignored archive + build output) -----
  write('IgnoredArchive/UshaSanka_Ph.D_2014/thesis.mdx', MALFORMED_MDX);
  write('node_modules/some-pkg/readme.mdx', MDX('Dependency doc'));
  write('build/generated.mdx', MDX('Build output'));
});

after(() => {
  fs.rmSync(repo, { recursive: true, force: true });
});

describe('allowed zones are discovered', () => {
  test('valid MDX in an allowed work zone is discovered', () => {
    const publishable = discoverPublishableMdx(repo);
    assert.ok(publishable.includes('ExampleWork_1900/example.mdx'));
    assert.ok(publishable.includes('ExampleWork_1900/nested/second.mdx'));
  });

  test('valid Sangram MDX is discovered', () => {
    assert.ok(discoverPublishableMdx(repo).includes('sangram/articles/future/index.mdx'));
  });

  test('a newly tracked valid work appears with no config edit', () => {
    // Auto-discovery, not an allowlist (ruling 7): adding + tracking is enough.
    write('BrandNewWork_2026/page.mdx', MDX('Brand new'));
    git('add', '-A');
    git('commit', '--quiet', '-m', 'add a new work');
    try {
      const site = discoverSite(repo);
      assert.ok(site.bookDirs.includes('BrandNewWork_2026'));
      assert.ok(discoverPublishableMdx(repo).includes('BrandNewWork_2026/page.mdx'));
    } finally {
      fs.rmSync(path.join(repo, 'BrandNewWork_2026'), { recursive: true, force: true });
      git('add', '-A');
      git('commit', '--quiet', '-m', 'remove the new work again');
    }
  });
});

describe('deny policy: path segments', () => {
  for (const segment of ['sources', 'review', 'drafts', '_private', 'archive', 'scratch', 'raw']) {
    test(`MDX under ${segment}/ is not discovered`, () => {
      const denied = discoverDeniedMdx(repo).map((e) => e.path);
      const hit = denied.find((p) => p.includes(`/${segment}/`));
      assert.ok(hit, `expected a denied path containing /${segment}/`);
      assert.ok(!discoverPublishableMdx(repo).some((p) => p.includes(`/${segment}/`)));
    });
  }

  test('the denial reason names the offending segment', () => {
    const reason = denialReason('ExampleWork_1900/sources/transcription.mdx', repo);
    assert.match(reason, /denied path segment: sources/);
  });

  test('segment matching is case-insensitive and NFC-normalized', () => {
    assert.equal(deniedBySegment('Work/SOURCES/x.mdx'), 'sources');
    assert.equal(deniedBySegment('Work/Drafts/x.mdx'), 'drafts');
    // NFC: composed vs decomposed must classify identically.
    assert.equal(deniedBySegment('Work/archivé/x.mdx'), null);
  });

  test('a denied segment is caught at any depth', () => {
    assert.equal(deniedBySegment('a/b/c/private/d.mdx'), 'private');
  });

  test('the deny list covers every surface the architecture names', () => {
    for (const required of [
      'raw', 'private', 'sources', 'review', 'draft', 'drafts',
      'archive', 'archives', 'scratch', 'cache', 'worktree',
      'node_modules', 'build',
    ]) {
      assert.ok(DENY_SEGMENTS.has(required), `deny list is missing ${required}`);
    }
  });
});

describe('deny policy: filename suffixes', () => {
  for (const suffix of DENY_FILENAME_SUFFIXES) {
    test(`a ${suffix}.mdx filename is denied`, () => {
      assert.equal(deniedByFilename(`Work/file${suffix}.mdx`), suffix);
    });
  }

  test('tracked .draft.mdx and .private.mdx are not published', () => {
    const publishable = discoverPublishableMdx(repo);
    assert.ok(!publishable.includes('ExampleWork_1900/notes.draft.mdx'));
    assert.ok(!publishable.includes('ExampleWork_1900/secret.private.mdx'));
  });

  test('an ordinary filename is not denied', () => {
    assert.equal(deniedByFilename('Work/ordinary.mdx'), null);
    assert.equal(deniedByFilename('Work/drafting-table.mdx'), null);
  });
});

describe('deny policy: front matter', () => {
  test('draft: true withholds publication', () => {
    assert.match(frontmatterDenial('---\ndraft: true\n---\n'), /draft: true/);
  });

  test('private: true and archived: true withhold publication', () => {
    assert.ok(frontmatterDenial('---\nprivate: true\n---\n'));
    assert.ok(frontmatterDenial('---\narchived: true\n---\n'));
  });

  test('publish: false withholds publication', () => {
    assert.match(frontmatterDenial('---\npublish: false\n---\n'), /publish: false/);
  });

  test('draft: false publishes', () => {
    assert.equal(frontmatterDenial('---\ndraft: false\n---\n'), null);
  });

  test('quoted values are handled', () => {
    assert.ok(frontmatterDenial('---\ndraft: "true"\n---\n'));
  });

  test('a flag in the BODY does not withhold publication', () => {
    // Only the leading front-matter block is authoritative.
    assert.equal(frontmatterDenial('---\ntitle: X\n---\n\ndraft: true\n'), null);
  });

  test('no front matter at all publishes', () => {
    assert.equal(frontmatterDenial('# Just a heading\n'), null);
  });

  test('tracked flagged files are not published', () => {
    const publishable = discoverPublishableMdx(repo);
    assert.ok(!publishable.includes('ExampleWork_1900/flagged.mdx'));
    assert.ok(!publishable.includes('ExampleWork_1900/unpublished.mdx'));
  });
});

describe('deny policy: zones outside content', () => {
  test('arbitrary root MDX is not discovered', () => {
    assert.ok(deniedAsRootMdx('root-level.mdx'));
    assert.equal(deniedAsRootMdx('Work/page.mdx'), null);
    assert.ok(!discoverPublishableMdx(repo).includes('root-level.mdx'));
  });

  test('docs/ and tests/fixtures/ are not content zones', () => {
    const publishable = discoverPublishableMdx(repo);
    assert.ok(!publishable.includes('docs/internal.mdx'));
    assert.ok(!publishable.includes('tests/fixtures/sample.mdx'));
  });

  test('a non-content top-level dir is named in the reason', () => {
    assert.match(denialReason('docs/internal.mdx', repo), /non-content top-level directory: docs/);
  });
});

describe('populated archive vs clean clone', () => {
  test('a malformed MDX in an ignored archive is never a candidate', () => {
    // The H1911 defect: this file is on disk and would break an MDX compile.
    const archive = 'IgnoredArchive/UshaSanka_Ph.D_2014/thesis.mdx';
    assert.ok(fs.existsSync(path.join(repo, archive)), 'fixture must be on disk');
    assert.ok(!discoverTrackedMdx(repo).includes(archive));
    assert.ok(!discoverPublishableMdx(repo).includes(archive));
  });

  test('every on-disk non-publishable MDX gets an exclude pattern', () => {
    const site = discoverSite(repo);
    for (const onDisk of [
      'IgnoredArchive/UshaSanka_Ph.D_2014/thesis.mdx',
      'ExampleWork_1900/sources/transcription.mdx',
      'ExampleWork_1900/flagged.mdx',
    ]) {
      assert.ok(
        site.exclude.includes(onDisk),
        `${onDisk} must be excluded so a populated tree builds like a clean clone`,
      );
    }
  });

  test('node_modules and build output are never candidates', () => {
    const publishable = discoverPublishableMdx(repo);
    assert.ok(!publishable.some((p) => p.startsWith('node_modules/')));
    assert.ok(!publishable.some((p) => p.startsWith('build/')));
  });
});

describe('determinism', () => {
  test('the publishable list is sorted and stable across calls', () => {
    const first = discoverPublishableMdx(repo);
    const second = discoverPublishableMdx(repo);
    assert.deepEqual(first, second);
    assert.deepEqual(first, [...first].sort());
  });

  test('book dirs are sorted', () => {
    const dirs = discoverSite(repo).bookDirs;
    assert.deepEqual(dirs, [...dirs].sort());
  });

  test('exclude patterns are sorted', () => {
    const patterns = discoverSite(repo).exclude;
    assert.deepEqual(patterns, [...patterns].sort());
  });

  test('glob metacharacters in a filename are escaped', () => {
    const escaped = discoverExcludePatterns(['Work/A Approach (article).mdx']);
    assert.equal(escaped[0], 'Work/A Approach [(]article[)].mdx');
  });

  test('book dirs never include a root-level file', () => {
    assert.deepEqual(discoverBookDirs(['root.mdx', 'Work/page.mdx']), ['Work']);
  });
});

describe('fail-closed behaviour', () => {
  test('an unreadable candidate is denied, not published', () => {
    const reason = denialReason('ExampleWork_1900/does-not-exist-on-disk.mdx', repo);
    assert.match(reason, /could not be read/);
  });

  test('discovery outside a git repo yields nothing rather than scanning', () => {
    const notARepo = fs.mkdtempSync(path.join(os.tmpdir(), 'sg-not-a-repo-'));
    try {
      assert.deepEqual(discoverTrackedMdx(notARepo), []);
      assert.deepEqual(discoverPublishableMdx(notARepo), []);
    } finally {
      fs.rmSync(notARepo, { recursive: true, force: true });
    }
  });
});

describe('the real repository', () => {
  test('every discovered book dir is a real directory', () => {
    const root = path.resolve(import.meta.dirname, '..', '..');
    const site = discoverSite(root);
    assert.ok(site.bookDirs.length > 0, 'the repo must discover at least one book');
    for (const dir of site.bookDirs) {
      assert.ok(fs.statSync(path.join(root, dir)).isDirectory(), `${dir} is not a directory`);
    }
  });

  test('no publishable MDX sits in a denied zone', () => {
    const root = path.resolve(import.meta.dirname, '..', '..');
    for (const p of discoverPublishableMdx(root)) {
      assert.equal(denialReason(p, root), null, `${p} is published but denied`);
    }
  });
});
