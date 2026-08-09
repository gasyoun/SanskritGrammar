import assert from 'node:assert/strict';
import test from 'node:test';

import fixHeadingAnchors from '../../src/remark/fixHeadingAnchors.mjs';
import {buildTableAst} from '../../src/remark/rstTableAst.mjs';
import {parseRstGridTable} from '../../src/remark/rstTableParser.mjs';

test('RST parser and AST retain header and spans', () => {
  const model = parseRstGridTable('+---+---+\n| A | B |\n+===+===+\n| x | y |\n+---+---+');
  assert.equal(model.headerRows.length, 1);
  assert.equal(model.bodyRows.length, 1);
  const ast = buildTableAst(model);
  assert.equal(ast.name, 'table');
  assert.deepEqual(ast.children.map((node) => node.name), ['thead', 'tbody']);
});

test('heading plugin demotes h1 and repairs Pandoc trailing-period anchors', () => {
  const tree = {
    type: 'root',
    children: [
      {type: 'link', url: '#урок-1.', children: [{type: 'text', value: 'jump'}]},
      {type: 'heading', depth: 1, children: [{type: 'text', value: 'Урок 1'}]},
    ],
  };
  fixHeadingAnchors()(tree);
  assert.equal(tree.children[0].url, '#урок-1');
  assert.equal(tree.children[1].depth, 2);
});

