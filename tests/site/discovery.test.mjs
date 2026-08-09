import assert from 'node:assert/strict';
import {execFileSync} from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';

import {discoverSite} from '../../src/discovery.mjs';

function fixture() {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'sg-discovery-'));
  execFileSync('git', ['init', '-q'], {cwd: root});
  fs.writeFileSync(path.join(root, '.gitignore'), 'Archive/\n');
  for (const file of ['Work/index.mdx', 'sangram/topic.mdx', 'review/note.mdx', 'private/note.mdx', 'ROOT.mdx']) {
    fs.mkdirSync(path.dirname(path.join(root, file)), {recursive: true});
    fs.writeFileSync(path.join(root, file), '---\ntitle: ok\n---\n');
  }
  fs.mkdirSync(path.join(root, 'Archive'), {recursive: true});
  fs.writeFileSync(path.join(root, 'Archive', 'broken.mdx'), '--- malformed');
  execFileSync('git', ['add', '.'], {cwd: root});
  return root;
}

test('tracked content zones auto-discover work and sangram, not root or ignored archives', () => {
  const root = fixture();
  try {
    const site = discoverSite(root);
    assert.deepEqual(site.bookDirs, ['Work', 'sangram']);
    assert.equal(site.trackedCount, 5);
    assert.equal(site.ignoredCount, 1);
    assert.match(site.exclude[0], /Archive/);
    assert.deepEqual(site.denied.map((item) => item.file).sort(), ['ROOT.mdx', 'private/note.mdx', 'review/note.mdx']);
  } finally {
    fs.rmSync(root, {recursive: true, force: true});
  }
});
