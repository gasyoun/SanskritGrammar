// @ts-check
// Docusaurus book site for the digitized Sanskrit grammar sources.
// The 6 books live as .mdx beside their .docx sources in per-book folders;
// this docs instance includes them directly (no copy into a docs/ dir).
// remarkRstTable renders the ```rst-table fenced grid tables as real <table>s.
import remarkRstTable from './src/remark/rstTable.mjs';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Sanskrit Grammar Sources',
  tagline: 'Digitized Sanskrit grammar & reader texts (Apte, Bühler, Gasūns, Kochergina, Knauer, Tolchelnikov, Zaliznyak)',
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
          include: [
            'ApteSyntax_1885/**.mdx',
            'BuhlerLeitfaden_1923/**.mdx',
            'GasunsDhatu_2014/**.mdx',
            'KnauerFrazy_1908/**.mdx',
            'KocherginaUchebnik_1998/**.mdx',
            'TolchelnikovTalmud_2026/**.mdx',
            'ZalizniakKonspekt_2004/**.mdx',
            'ZalizniakOcherk_1978/**.mdx',
          ],
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
