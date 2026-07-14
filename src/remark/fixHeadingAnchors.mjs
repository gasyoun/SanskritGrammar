// remarkFixHeadingAnchors — reconcile in-page anchor links to their heading slugs.
//
// The book pages are converted from Word/OCR by Pandoc, which bakes a table of
// contents whose links use Pandoc's slug form (e.g. `#урок-1.`, keeping the
// trailing period). Docusaurus assigns heading ids with github-slugger, which
// DROPS the trailing period → slug `урок-1`. The mismatch makes the ToC links
// broken anchors (docusaurus build reported 34 on Apte, 25 on Talmud fixable
// this way; H889).
//
// This build-time plugin edits nothing on disk. For each in-page `#anchor`
// link it recomputes the slug with the SAME github-slugger Docusaurus uses and
// rewrites the link **only when the recomputed slug matches a real heading on
// that page** — so a link that can't be reconciled (a genuinely missing target,
// a `_Toc…` Word bookmark, or the gasuns-dhatu ToC whose structure is off) is
// left exactly as-is rather than pointed somewhere wrong.
import {visit} from 'unist-util-visit';
import GithubSlugger from 'github-slugger';

function headingText(node) {
  let out = '';
  visit(node, (n) => {
    if (n.type === 'text' || n.type === 'inlineCode') out += n.value;
  });
  return out.trim();
}

export default function remarkFixHeadingAnchors() {
  return (tree) => {
    // Only touch pages that actually carry an in-page ToC (a `#…` link). Pages
    // with no in-page anchors are left exactly as-is, so the heading demotion
    // below is scoped to the handful of Word-converted pages that need it.
    let hasInPageLink = false;
    visit(tree, 'link', (n) => {
      if (typeof n.url === 'string' && n.url.startsWith('#') && n.url.length > 1) {
        hasInPageLink = true;
      }
    });
    if (!hasInPageLink) return;

    // Pass 1: demote content h1 → h2 and record each heading's slug.
    // Docusaurus's theme only assigns anchor ids to h2–h6, but these
    // Word-converted pages use `#` (h1) for every section heading (the page
    // title comes from frontmatter), so an h1 renders with NO id and no in-page
    // anchor can resolve. Re-titling each h1 as h2 lets the theme id it; the
    // slug is computed with the same stateful github-slugger the theme uses, so
    // `valid` holds exactly the ids the built page will carry.
    const slugger = new GithubSlugger();
    const valid = new Set();
    visit(tree, 'heading', (node) => {
      if (node.depth === 1) node.depth = 2;
      const text = headingText(node);
      if (text) valid.add(slugger.slug(text));
    });

    // Pass 2: repair in-page anchor links that resolve onto a real heading.
    visit(tree, 'link', (node) => {
      if (typeof node.url !== 'string' || !node.url.startsWith('#')) return;
      let frag;
      try {
        frag = decodeURIComponent(node.url.slice(1));
      } catch {
        frag = node.url.slice(1);
      }
      if (!frag || valid.has(frag)) return; // empty, or already correct
      const repaired = new GithubSlugger().slug(frag);
      if (repaired !== frag && valid.has(repaired)) {
        node.url = '#' + repaired;
      }
    });
  };
}
