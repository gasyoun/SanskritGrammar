// H2272 probe: replicate @easyops-cn/docusaurus-search-local's SearchWorker.search()
// against the real build/search-index.json, using the same lunr + lunr-languages
// wiring the plugin's own buildIndex.js uses (ru + en multiLanguage, per
// docusaurus.config.mjs). Read-only — queries the built index, writes no site content.
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const lunr = require('lunr');
require('lunr-languages/lunr.stemmer.support')(lunr);
require('lunr-languages/lunr.ru')(lunr);
require('lunr-languages/lunr.sa')(lunr); // H2300: adds Devanagari to the trimmer's wordCharacters
require('lunr-languages/lunr.multi')(lunr);
const plugin = lunr.multiLanguage('ru', 'en', 'sa');

const idxPath = path.join(process.cwd(), 'build', 'search-index.json');
const raw = JSON.parse(fs.readFileSync(idxPath, 'utf8'));
const shards = raw.map(({ documents, index }) => ({
  documents,
  index: lunr.Index.load(index),
}));

function tokenize(text) {
  // client/utils/tokenize.js: 'sa' isn't in the {ja,jp,th,zh} special-cased
  // set, so language=['ru','en','sa'] still falls through to the same
  // regExpMatchWords = /[^-\s]+/g as the pre-H2300 ['ru','en'] config.
  return text.toLowerCase().match(/[^-\s]+/g) || [];
}

// Mirrors smartQueries.js's real fallback order: an exact pass (pipeline-processed,
// i.e. stemmed — usePipeline is NOT disabled without a wildcard) THEN a
// trailing-wildcard "still typing" pass (raw term, pipeline disabled per lunr's own
// "usePipeline unless wildcard" rule at lunr.js Index.prototype.query). A production
// search tries passes in order and stops once it has enough hits; for measurement we
// run both and report the best-ranked hit across them.
function runQuery(shard, tokens, wildcard) {
  const hits = shard.index.query((q) => {
    for (const tok of tokens) {
      q.term(tok, { presence: lunr.Query.presence.REQUIRED, wildcard });
    }
  });
  return hits.map((hit) => {
    const doc = shard.documents.find((d) => d.i.toString() === hit.ref);
    return doc ? { url: doc.u, score: hit.score } : null;
  }).filter(Boolean);
}

function searchTerm(term) {
  const tokens = tokenize(term);
  if (tokens.length === 0) return [];
  const byUrl = new Map();
  for (const shard of shards) {
    for (const wildcard of [lunr.Query.wildcard.NONE, lunr.Query.wildcard.TRAILING]) {
      for (const hit of runQuery(shard, tokens, wildcard)) {
        const prev = byUrl.get(hit.url);
        if (!prev || hit.score > prev.score) byUrl.set(hit.url, hit);
      }
    }
  }
  return [...byUrl.values()].sort((a, b) => b.score - a.score);
}

const cases = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const out = cases.map((c) => {
  const hits = searchTerm(c.term);
  const top = hits[0];
  const expectedHit = hits.find((h) => h.url.includes(c.expectedUrlFragment));
  return {
    ...c,
    topHitUrl: top ? top.url : null,
    expectedFound: !!expectedHit,
    expectedRank: expectedHit ? hits.indexOf(expectedHit) + 1 : null,
    totalHits: hits.length,
  };
});
console.log(JSON.stringify(out, null, 2));
