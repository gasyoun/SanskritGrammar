# SanskritGrammar

_Created: 05-07-2026 · Last updated: 05-07-2026_

A raw-source archive of classic Sanskrit-grammar textbooks and reference works,
kept in their original scanned/converted form so that downstream projects have
a stable, citable source to digitize from — rather than each project holding
its own copy of the same reprint.

## What problem this solves

Several teaching and digitization projects in this org need the text of
older, often hard-to-find Sanskrit grammar textbooks (Bühler's exercise
course, Apte's syntax, Kochergina's textbook, Knauer's phrasebook, Zaliznyak's
grammar sketches). These source documents are large `.doc`/`.docx` files —
not something to duplicate across every consuming repo, and not something to
edit in place. This repo is the **one place** they live, organized one
directory per work, so a consuming repo (e.g.
[`buhler-sanskrit-book`](https://github.com/alexander-myltsev/buhler-sanskrit-book),
which republishes the Bühler exercises as a Docusaurus site) can point back
to a stable source instead of re-scanning or re-typing the text.

This is a **content/data repo, not an application** — there is no build
step, server, or package to install for the repo as a whole (individual
consumer repos may have their own tooling).

## Structure

One directory per source work, named `<Author><ShortTitle>_<year>`:

| Directory | Work | Format present |
|---|---|---|
| [ApteSyntax_1885](ApteSyntax_1885/) | Apte, Sanskrit syntax reference (reprint dated 1885 in the folder name; underlying `.doc` metadata shows a 2022 electronic edition) | `.doc` only |
| [BuhlerLeitfaden_1923](BuhlerLeitfaden_1923/) | Bühler, *Leitfaden für den elementaren Cursus des Sanskrit* (Stockholm, 1923) — electronic edition v2.0 by N. P. Likhushina | `.doc` (original), `.docx` (LibreOffice-converted), `.md` (pandoc-extracted, formatting-faithful) |
| [KnauerFrazy_1908](KnauerFrazy_1908/) | Knauer, Sanskrit phrase collection (`Frazy-Knauer`, reprint reference 1908) | `.doc` only |
| [KocherginaUchebnik_1998](KocherginaUchebnik_1998/) | Kochergina, Sanskrit textbook (*Учебник санскрита*, 1998) | `.docx` only |
| [ZalizniakKonspekt_2004](ZalizniakKonspekt_2004/) | Zaliznyak, grammar conspectus (2004) — **directory exists but is currently empty**, no source file has been added yet | — |
| [ZalizniakOcherk_1978](ZalizniakOcherk_1978/) | Zaliznyak, *Очерк грамматики санскрита* (grammar sketch, 1978) — aligned edition | `.doc` only |

All `.doc` files are legacy Microsoft Word 97 binary format (`Composite
Document File V2`), mostly containing Devanāgarī + IAST text with embedded
formatting; several carry editorial metadata (author, revision count, last
save date) from the scanning/typing pass that produced them. `.docx`/`.md`
conversions exist only where a downstream consumer needed a
machine-readable extraction (currently just Bühler).

## How the Bühler conversion was done

The one worked example of turning a `.doc` source into a usable Markdown
edition, in case the same needs to be repeated for the other works:

1. `.doc` → `.docx` via LibreOffice 26.2.1, headless.
2. `.docx` → GitHub-Flavored-Markdown via pandoc 3.9, which preserves
   italics and `rowspan`/`colspan` paradigm tables (an earlier
   piece-table-parser extraction, done when neither Word nor LibreOffice
   was available locally, had flattened these — see the git history on
   [`BuhlerLeitfaden_1923/Buhler_Unicode.md`](BuhlerLeitfaden_1923/Buhler_Unicode.md)
   for both attempts).

The result, [`BuhlerLeitfaden_1923/Buhler_Unicode.md`](BuhlerLeitfaden_1923/Buhler_Unicode.md),
is the D3 source feeding lessons 21–48 of the `buhler-sanskrit-book`
Docusaurus site (per the commit history — cross-check that repo before
assuming this file's role is only archival).

## Status

Active / early-stage. The repo was created 03-07-2026 and has three commits
total, all adding or refining the Bühler material; the other five works are
present as raw source only and have not yet been converted or consumed
downstream. Treat this as a working source archive that will grow as more
of these grammars get digitized, not a finished, stable dataset.

## Caveats found in the source files

- File-embedded metadata shows these `.doc` files were produced/edited by
  different people at different times (e.g. `anatoly.artemenko@gmail.com`
  for Apte, `Sumeru`/"Certified Windows" for Knauer) — provenance is mixed
  and not independently verified here.
- `KnauerFrazy_1908` and `ApteSyntax_1885`'s year suffixes refer to the
  original print edition; the actual `.doc` files are modern electronic
  transcriptions (2022–2023), not scans of the 1885/1908 originals.
- `ZalizniakKonspekt_2004` is an empty placeholder directory — do not
  assume its source material exists yet.
- No license file governs the individual textbook contents (the repo-level
  [LICENSE](LICENSE) is MIT, which applies to any code/tooling here, not to
  the third-party textbook text itself — check the original publishers'
  rights before redistributing full texts).

_Dr. Mārcis Gasūns_
