# SanskritGrammar

_Created: 05-07-2026 · Last updated: 06-07-2026_

A raw-source archive of classic Sanskrit-grammar textbooks and reference
works — Bühler's exercise course, Apte's syntax, Kochergina's textbook,
Knauer's phrasebook, Zaliznyak's two grammar sketches — kept beside their
faithful `.mdx` extraction, plus a small Docusaurus site to actually read
them rendered (tables included).

---

## Why this repo exists

Several teaching and digitization projects in this org need the text of
older, often hard-to-find Sanskrit grammar textbooks. These sources arrive
as large legacy `.doc`/`.docx` files, not something to duplicate across
every consuming repo and not something to edit in place. This repo is the
**one place** they live — one directory per work — so a consuming repo
(e.g.
[`buhler-sanskrit-book`](https://github.com/gasyoun/buhler-sanskrit-book),
which republishes the Bühler exercises as its own Docusaurus site) can point
back to a stable source instead of maintaining its own copy.

## Structure

One directory per source work, named `<Author><ShortTitle>_<year>`:

| Directory | Work | Format present |
|---|---|---|
| [ApteSyntax_1885](ApteSyntax_1885/) | Apte, Sanskrit syntax reference (reprint dated 1885 in the folder name; underlying `.doc` metadata shows a 2022 electronic edition) | `.doc`, `.docx`, `.mdx` |
| [BuhlerLeitfaden_1923](BuhlerLeitfaden_1923/) | Bühler, *Leitfaden für den elementaren Cursus des Sanskrit* (Stockholm, 1923) — electronic edition v2.0 by N. P. Likhushina | `.doc`, `.docx`, `.mdx` |
| [KnauerFrazy_1908](KnauerFrazy_1908/) | Knauer, Sanskrit phrase collection (`Frazy-Knauer`, reprint reference 1908) | `.doc`, `.docx`, `.mdx` |
| [KocherginaUchebnik_1998](KocherginaUchebnik_1998/) | Kochergina, Sanskrit textbook (*Учебник санскрита*, 1998) | `.docx`, `.mdx` |
| [ZalizniakKonspekt_2004](ZalizniakKonspekt_2004/) | Zaliznyak, grammar conspectus (2004) | `.doc`, `.docx`, `.mdx` |
| [ZalizniakOcherk_1978](ZalizniakOcherk_1978/) | Zaliznyak, *Очерк грамматики санскрита* (grammar sketch, 1978) — aligned edition | `.doc`, `.docx`, `.mdx` |

All `.doc` files are legacy Microsoft Word 97 binary format (`Composite
Document File V2`), mostly containing Devanāgarī + IAST text with embedded
formatting; several carry editorial metadata (author, revision count, last
save date) from the scanning/typing pass that produced them.

Every `.mdx` was produced by the org-wide `/docx-to-md` skill: `.docx` →
Pandoc (`markdown-simple_tables-multiline_tables`, forcing every table into
either a pipe table or a grid table — Pandoc's default "simple table" style
isn't valid GFM/MDX and would render as inert text), with every grid table
wrapped in a plain ```` ```rst-table ```` fenced code block and every stray
Pandoc-escaped `\<`/`\>` (comparative-linguistics notation like `a < ā`, or
garbage like a literal `<TBODY>` pasted into a source Word doc) converted to
`&lt;`/`&gt;` — both fixes exist because they were found to silently corrupt
data / crash the MDX build the first time this pipeline ran (06-07-2026).

## Reading the archive

This repo is itself a small Docusaurus site over the six `.mdx` files
directly (no copy into a `docs/` folder):

```sh
npm install
npm start          # dev server with hot reload
npm run build       # production build (onBrokenLinks: 'warn')
npm run convert     # re-run /docx-to-md's pipeline (scripts/docx_to_mdx.py)
```

`src/remark/rstTable.mjs` (+ `rstTableParser.mjs` + `rstTableAst.mjs`) is the
pure-JS remark plugin that renders `rst-table` fenced blocks as real
`<table>`s with true `rowSpan`/`colSpan` — no Pandoc dependency at build
time. Canonical original: `buhler-sanskrit-book/src/remark/rstTable.ts`;
also ported into `csl-guides/src/remark/rstTable.mjs`. Keep all three copies
in sync by hand — there is no shared npm package yet.

## Caveats found in the source files

- File-embedded metadata shows these `.doc` files were produced/edited by
  different people at different times (e.g. `anatoly.artemenko@gmail.com`
  for Apte, `Sumeru`/"Certified Windows" for Knauer) — provenance is mixed
  and not independently verified here.
- `KnauerFrazy_1908` and `ApteSyntax_1885`'s year suffixes refer to the
  original print edition; the actual `.doc` files are modern electronic
  transcriptions (2022–2023), not scans of the 1885/1908 originals.
- No license file governs the individual textbook contents (the repo-level
  [LICENSE](LICENSE) is MIT, which applies to any code/tooling here, not to
  the third-party textbook text itself — check the original publishers'
  rights before redistributing full texts).

---

_Dr. Mārcis Gasūns_
