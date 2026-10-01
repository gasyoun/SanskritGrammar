# Standing directive — never-print toms: e-publish from the final block PDF

_Created: 13-09-2026 · Last updated: 13-09-2026_

**Ruling:** MG 13-09-2026, vote D3 (10-card interactive chat vote): том XVIII
«Канун древнеиндийской философии» **никогда не печатается** — он издаётся
электронно из финального блочного PDF. This directive registers the standing
route so any future never-print tom follows it without a new decision.

## Directive

1. For a tom ruled never-print, the e-publish source of record is the **final
   block PDF in `В печать/`** of that tom on `yadisk:Bibliotheca/NN том …/`.
2. Extraction is **PyMuPDF only** (`tools/pdf_to_mdx.py`, H4642) — poppler is
   banned on Cyrillic PDFs (plausible-garbage hazard, DANGER_FACTS).
3. Extraction is verbatim per page (mechanics only): no prose rewriting, no
   reordering; page order preserved; empty pages counted in front matter.
4. Quotes mined from the edition carry **page provenance** from the
   `<!-- page N -->` markers in the mdx.
5. Derived-only: print-production PDFs, `.indd`/`.idml` binaries are never
   committed; only the derived `.mdx` lands in `BibliothecaSanscritica/<Tom>/`.
6. Each such edition registers its front-matter provenance (source path,
   print date, extractor, status) exactly like the idml-pilot scheme (H4484).

## Applied to

- Tom XVIII «Канун древнеиндийской философии» (block PDF 2022-12-02, 272 pp) →
  [KanunDrevneindiyskoyFilosofii_2022/](https://github.com/gasyoun/SanskritGrammar/tree/main/BibliothecaSanscritica/KanunDrevneindiyskoyFilosofii_2022) (H4642).

_Гасунс_
