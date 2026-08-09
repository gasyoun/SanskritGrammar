// Remark plugin contract tests (A4).
//
// Covers the two plugins the site build depends on, at the level the
// verification doc asks for ("tests cover the rstTable parser/AST, heading-anchor
// behavior"):
//
//   * rstTableParser  — Pandoc/RST grid-table syntax → cell model
//   * rstTableAst     — cell model → mdast table with rowSpan/colSpan
//   * rstTable        — the remark transform that swaps the code node
//   * fixHeadingAnchors — h1→h2 demotion + in-page anchor repair
//
// These are pure functions over an AST, so they need no Docusaurus and no
// fixtures on disk.
//
// Run: npm run test:site
import { strict as assert } from 'node:assert';
import { describe, test } from 'node:test';

import remarkRstTable from '../../src/remark/rstTable.mjs';
import remarkFixHeadingAnchors from '../../src/remark/fixHeadingAnchors.mjs';
import { parseRstGridTable } from '../../src/remark/rstTableParser.mjs';
import { buildTableAst } from '../../src/remark/rstTableAst.mjs';

// A 2x2 grid table with a header row (=== separator marks the header).
const SIMPLE_GRID = [
  '+-------+-------+',
  '| Case  | Form  |',
  '+=======+=======+',
  '| nom.  | devaḥ |',
  '+-------+-------+',
  '| acc.  | devam |',
  '+-------+-------+',
].join('\n');

// A column-spanning cell: the header spans both columns.
const SPANNING_GRID = [
  '+-------+-------+',
  '| Spans both     |',
  '+-------+-------+',
  '| a     | b     |',
  '+-------+-------+',
].join('\n');

function collect(node, type, out = []) {
  if (!node || typeof node !== 'object') return out;
  if (node.type === type) out.push(node);
  for (const child of node.children ?? []) collect(child, type, out);
  return out;
}

function textOf(node) {
  let out = '';
  const walk = (n) => {
    if (!n || typeof n !== 'object') return;
    if (typeof n.value === 'string') out += n.value;
    for (const child of n.children ?? []) walk(child);
  };
  walk(node);
  return out.trim();
}

describe('rstTableParser', () => {
  test('parses a simple grid table into header and body rows', () => {
    // Contract: {headerRows, bodyRows}; a `===` rule separates the two.
    const { headerRows, bodyRows } = parseRstGridTable(SIMPLE_GRID);
    assert.equal(headerRows.length, 1, 'expected exactly one header row');
    assert.equal(bodyRows.length, 2, 'expected two body rows');
    assert.deepEqual(headerRows[0].map((c) => c.text), ['Case', 'Form']);
    assert.deepEqual(bodyRows[0].map((c) => c.text), ['nom.', 'devaḥ']);
    assert.ok(headerRows[0].every((c) => c.header), 'header cells must be flagged');
    assert.ok(bodyRows[0].every((c) => !c.header), 'body cells must not be flagged');
  });

  test('a table with no === rule is all body, no header', () => {
    const noHeader = [
      '+-----+-----+',
      '| a   | b   |',
      '+-----+-----+',
    ].join('\n');
    const { headerRows, bodyRows } = parseRstGridTable(noHeader);
    assert.equal(headerRows.length, 0);
    assert.equal(bodyRows.length, 1);
  });

  test('a spanning cell reports its colSpan', () => {
    const { bodyRows } = parseRstGridTable(SPANNING_GRID);
    const spanning = bodyRows.flat().find((c) => c.colSpan > 1);
    assert.ok(spanning, 'expected a cell with colSpan > 1');
    assert.equal(spanning.text, 'Spans both');
    assert.equal(spanning.colSpan, 2);
  });

  test('cell text survives the parse, Devanagari/IAST included', () => {
    const serialized = JSON.stringify(parseRstGridTable(SIMPLE_GRID));
    for (const needle of ['Case', 'Form', 'nom.', 'devaḥ', 'acc.', 'devam']) {
      assert.ok(serialized.includes(needle), `lost cell text: ${needle}`);
    }
  });

  test('an empty source yields empty rows rather than throwing', () => {
    assert.deepEqual(parseRstGridTable(''), { headerRows: [], bodyRows: [] });
  });

  test('a non-table source THROWS rather than silently rendering nothing', () => {
    // Deliberate contract: an author who labels a fence `rst-table` and writes
    // something that is not a grid table gets a loud build failure, not a
    // silently dropped table. Both guards are exercised.
    assert.throws(
      () => parseRstGridTable('just prose, no grid at all\n'),
      /need at least two border lines/,
    );
    assert.throws(
      () => parseRstGridTable('+\n+\n'),
      /need at least two column boundaries/,
    );
  });

  test('parsing is deterministic', () => {
    assert.deepEqual(
      parseRstGridTable(SIMPLE_GRID),
      parseRstGridTable(SIMPLE_GRID),
    );
  });
});

describe('rstTableAst', () => {
  test('builds an mdast node from a parsed model', () => {
    const ast = buildTableAst(parseRstGridTable(SIMPLE_GRID));
    assert.ok(ast, 'no AST produced');
    assert.equal(typeof ast.type, 'string');
  });

  test('the AST carries the cell text', () => {
    const ast = buildTableAst(parseRstGridTable(SIMPLE_GRID));
    const rendered = textOf(ast);
    for (const needle of ['Case', 'devaḥ', 'devam']) {
      assert.ok(rendered.includes(needle), `AST lost ${needle}`);
    }
  });

  test('a spanning cell produces a span attribute somewhere in the AST', () => {
    const serialized = JSON.stringify(buildTableAst(parseRstGridTable(SPANNING_GRID)));
    assert.match(serialized, /(colSpan|colspan|rowSpan|rowspan)/);
  });

  test('AST construction is deterministic', () => {
    const model = parseRstGridTable(SIMPLE_GRID);
    assert.deepEqual(buildTableAst(model), buildTableAst(model));
  });
});

describe('remarkRstTable', () => {
  const runPlugin = (tree) => {
    remarkRstTable()(tree);
    return tree;
  };

  test('replaces an rst-table code fence', () => {
    const tree = {
      type: 'root',
      children: [{ type: 'code', lang: 'rst-table', value: SIMPLE_GRID }],
    };
    runPlugin(tree);
    assert.equal(tree.children.length, 1);
    assert.notEqual(tree.children[0].type, 'code', 'the fence was not replaced');
  });

  test('leaves a fence with another language untouched', () => {
    const original = { type: 'code', lang: 'python', value: 'print(1)' };
    const tree = { type: 'root', children: [original] };
    runPlugin(tree);
    assert.equal(tree.children[0], original);
    assert.equal(tree.children[0].type, 'code');
  });

  test('leaves an unlabelled fence untouched', () => {
    const tree = {
      type: 'root',
      children: [{ type: 'code', lang: null, value: SIMPLE_GRID }],
    };
    runPlugin(tree);
    assert.equal(tree.children[0].type, 'code');
  });

  test('converts several tables on one page', () => {
    const tree = {
      type: 'root',
      children: [
        { type: 'code', lang: 'rst-table', value: SIMPLE_GRID },
        { type: 'paragraph', children: [{ type: 'text', value: 'between' }] },
        { type: 'code', lang: 'rst-table', value: SPANNING_GRID },
      ],
    };
    runPlugin(tree);
    assert.equal(collect(tree, 'code').length, 0, 'a fence survived');
  });

  test('a page with no tables is unchanged', () => {
    const tree = {
      type: 'root',
      children: [{ type: 'paragraph', children: [{ type: 'text', value: 'prose' }] }],
    };
    const before = JSON.stringify(tree);
    runPlugin(tree);
    assert.equal(JSON.stringify(tree), before);
  });
});

describe('remarkFixHeadingAnchors', () => {
  const heading = (depth, value) => ({
    type: 'heading',
    depth,
    children: [{ type: 'text', value }],
  });
  const link = (url, label = 'go') => ({
    type: 'paragraph',
    children: [{ type: 'link', url, children: [{ type: 'text', value: label }] }],
  });
  const run = (tree) => {
    remarkFixHeadingAnchors()(tree);
    return tree;
  };

  test('repairs a Pandoc trailing-period anchor onto its real heading', () => {
    // Pandoc emits `#урок-1.`; github-slugger drops the period → `урок-1`.
    const tree = { type: 'root', children: [link('#урок-1.'), heading(1, 'Урок 1.')] };
    run(tree);
    assert.equal(collect(tree, 'link')[0].url, '#урок-1');
  });

  test('demotes h1 to h2 so the theme assigns an id', () => {
    const tree = { type: 'root', children: [link('#section-one'), heading(1, 'Section one')] };
    run(tree);
    assert.equal(collect(tree, 'heading')[0].depth, 2);
  });

  test('an already-correct anchor is left alone', () => {
    const tree = { type: 'root', children: [link('#section-one'), heading(2, 'Section one')] };
    run(tree);
    assert.equal(collect(tree, 'link')[0].url, '#section-one');
  });

  test('an unresolvable anchor is left exactly as-is, never pointed elsewhere', () => {
    // The load-bearing safety property: a link with no matching heading must
    // NOT be rewritten to some other page anchor.
    const tree = { type: 'root', children: [link('#_Toc12345'), heading(2, 'Real heading')] };
    run(tree);
    assert.equal(collect(tree, 'link')[0].url, '#_Toc12345');
  });

  test('a page with no in-page links is untouched, h1 included', () => {
    const tree = {
      type: 'root',
      children: [heading(1, 'Title'), { type: 'paragraph', children: [{ type: 'text', value: 'x' }] }],
    };
    run(tree);
    assert.equal(collect(tree, 'heading')[0].depth, 1, 'demotion must be scoped to ToC pages');
  });

  test('an external link is ignored', () => {
    const tree = {
      type: 'root',
      children: [link('#real'), link('https://example.com/#real'), heading(1, 'Real')],
    };
    run(tree);
    assert.equal(collect(tree, 'link')[1].url, 'https://example.com/#real');
  });

  test('a percent-encoded Cyrillic anchor is decoded and repaired', () => {
    const tree = {
      type: 'root',
      children: [link('#' + encodeURIComponent('урок-2.')), heading(1, 'Урок 2.')],
    };
    run(tree);
    assert.equal(collect(tree, 'link')[0].url, '#урок-2');
  });

  test('a bare "#" is ignored', () => {
    const tree = { type: 'root', children: [link('#'), heading(1, 'X')] };
    assert.doesNotThrow(() => run(tree));
    assert.equal(collect(tree, 'link')[0].url, '#');
  });

  test('the transform is idempotent', () => {
    const build = () => ({ type: 'root', children: [link('#урок-1.'), heading(1, 'Урок 1.')] });
    const once = build();
    run(once);
    const twice = build();
    run(twice);
    run(twice);
    assert.equal(JSON.stringify(once), JSON.stringify(twice));
  });
});
