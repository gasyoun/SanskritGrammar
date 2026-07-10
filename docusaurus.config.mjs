// @ts-check
// Docusaurus book site for the digitized Sanskrit grammar sources.
// Each book lives as .mdx beside its .docx source in its own top-level folder;
// this docs instance includes them directly (no copy into a docs/ dir).
// remarkRstTable renders the ```rst-table fenced grid tables as real <table>s.
import fs from 'fs';
import remarkRstTable from './src/remark/rstTable.mjs';

// Auto-discover book folders (any top-level dir containing at least one .mdx),
// instead of a hand-maintained static list. A folder dropped in and converted
// to .mdx is picked up on the next build with zero config edits — the previous
// static array silently omitted any new book until someone remembered to add
// it by hand (found 06-07-2026: ZalizniakMorphology_1975 converted fine but
// was never in `include`, so the build reported [SUCCESS] with the book
// simply absent from the site).
const SKIP_DIRS = new Set(['node_modules', 'build', '.docusaurus', 'src', '.git', '.github', 'scripts']);
const bookDirs = fs
  .readdirSync('.', { withFileTypes: true })
  .filter((d) => d.isDirectory() && !SKIP_DIRS.has(d.name) && !d.name.startsWith('.'))
  .filter((d) => fs.readdirSync(d.name).some((f) => f.endsWith('.mdx')))
  .map((d) => d.name)
  .sort();

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Sanskrit Grammar Sources',
  tagline: 'Digitized Sanskrit grammar & reader texts (Apte, Bühler, Gasūns, Kochergina, Knauer, Tolchelnikov, Whitney, Zalizniak)',
  favicon: undefined,

  url: 'https://gasyoun.github.io',
  baseUrl: '/SanskritGrammar/',
  organizationName: 'gasyoun',
  projectName: 'SanskritGrammar',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',

  i18n: { defaultLocale: 'ru', locales: ['ru'] },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: '.',
          routeBasePath: 'grammars',
          sidebarPath: './sidebars.mjs',
          include: bookDirs.map((d) => `${d}/**/*.mdx`),
          exclude: ['**/node_modules/**', '**/build/**', '**/.docusaurus/**', '**/src/**'],
          remarkPlugins: [remarkRstTable],
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
