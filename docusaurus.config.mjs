// @ts-check
// Docusaurus book site for the digitized Sanskrit grammar sources.
// Each book lives as .mdx beside its .docx source in its own top-level folder;
// this docs instance includes them directly (no copy into a docs/ dir).
// remarkRstTable renders the ```rst-table fenced grid tables as real <table>s.
import remarkRstTable from './src/remark/rstTable.mjs';
import remarkFixHeadingAnchors from './src/remark/fixHeadingAnchors.mjs';
import { discoverSite } from './src/discovery.mjs';

// Auto-discover book folders from the **tracked** `.mdx` set (`git ls-files`),
// not a filesystem scan. A folder dropped in, converted, and `git add`ed is
// picked up on the next build with zero config edits — while anything
// `.gitignore`'d (private/archival/raw MDX that should never publish) is never
// read. The earlier filesystem scan read ignored archival MDX and a single
// malformed front-matter file in such an archive killed `npm run build`
// locally while CI stayed green on the fresh clone (H1911 Slice A,
// docs/architecture/baseline/H1911_A0_BASELINE.md).
//
// The previous static array silently omitted any new book until someone
// remembered to add it by hand (found 06-07-2026: ZalizniakMorphology_1975
// converted fine but was never in `include`, so the build reported [SUCCESS]
// with the book simply absent from the site) — tracked-file discovery keeps
// that property without the ignore-poisoning failure mode.
const { bookDirs, include: includePaths, exclude: excludePatterns, trackedCount, ignoredCount } = discoverSite();

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Sanskrit Grammar Sources',
  tagline: 'Digitized Sanskrit grammar & reader texts (Apte, Bühler, Gasūns, Kochergina, Knauer, Tolchelnikov, Whitney, Zalizniak)',
  favicon: undefined,

  url: 'https://gasyoun.github.io',
  baseUrl: '/SanskritGrammar/',
  organizationName: 'gasyoun',
  projectName: 'SanskritGrammar',

  // 'throw' (not 'warn'): broken in-site links now fail the build + CI, so a
  // dead cross-link can't silently ship again. All broken links were cleared
  // first (catalog #169, Fortunatovskiye #170, papers de-link #171).
  // onBrokenAnchors stays a warning — the OCR'd book pages still carry ~60
  // self-referential `#-N` anchors that are a separate, owner-gated cleanup.
  onBrokenLinks: 'throw',
  onBrokenAnchors: 'warn',

  i18n: { defaultLocale: 'ru', locales: ['ru'] },

  // ```mermaid fences (sangram charter and the B/C-wave atlas pages) render
  // as diagrams instead of dead code blocks.
  // onBrokenMarkdownLinks moved under markdown.hooks — the top-level option is
  // deprecated and removed in Docusaurus v4 (was warning on every build).
  markdown: { mermaid: true, hooks: { onBrokenMarkdownLinks: 'warn' } },
  themes: [
    '@docusaurus/theme-mermaid',
    // Offline full-text search (H1841) — no Algolia key/account. Site default
    // locale is Russian with mixed Cyrillic / IAST / Devanagari content; lunr
    // `ru` tokenizes Cyrillic, `en` covers Latin/IAST word runs. Devanagari is
    // indexed as raw terms (no zh-style segmenter); multi-script pages remain
    // findable by their Cyrillic/IAST headings and prose.
    [
      require.resolve('@easyops-cn/docusaurus-search-local'),
      {
        hashed: true,
        language: ['ru', 'en'],
        indexDocs: true,
        indexBlog: false,
        indexPages: false,
        docsRouteBasePath: 'grammars',
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
      },
    ],
  ],

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: '.',
          routeBasePath: 'grammars',
          sidebarPath: './sidebars.mjs',
          include: includePaths,
          exclude: [
            '**/node_modules/**',
            '**/build/**',
            '**/.docusaurus/**',
            '**/src/**',
            // RWS review worksheet: tracked but not MDX-safe (escaped markdown,
            // bare { } / * expressions). Public book reading pages are unaffected;
            // keep the .mdx in git as the editorial work product (H1841 build fix).
            '**/GasunsDhatu_2026_RWS_review.mdx',
            ...excludePatterns,
          ],
          remarkPlugins: [remarkRstTable, remarkFixHeadingAnchors],
          editUrl: undefined,
        },
        blog: false,
        theme: {},
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      navbar: {
        title: 'Sanskrit Grammar Sources',
        items: [
          { type: 'docSidebar', sidebarId: 'grammarsSidebar', position: 'left', label: 'Grammars' },
          { href: 'https://github.com/gasyoun/SanskritGrammar', label: 'GitHub', position: 'right' },
        ],
      },
      footer: { style: 'dark', links: [], copyright: 'Digitized Sanskrit grammar sources · CC BY-SA 4.0' },
    }),
};

export default config;
