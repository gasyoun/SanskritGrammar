#!/usr/bin/env python3
"""pdf_to_mdx.py — extract text from a final block PDF into a Markdown (mdx) edition file.

H4642 wave 1 (Bibliotheca Sanscritica, tom XVIII «Канун древнеиндийской философии»,
ruling MG 13-09-2026 / vote D3): the tom never prints — it is e-published from the
final block PDF (`В печать/…pdf`). PyMuPDF only: poppler is banned on Cyrillic PDFs
(plausible-garbage hazard, DANGER_FACTS).

Mechanics only (book-press-prep guardrail): text is extracted verbatim per page —
no prose rewriting, no reordering, no invented content.

Usage: python3 tools/pdf_to_mdx.py <file.pdf> <out.mdx> [--key=value ...]

Optional --key=value pairs set front-matter fields (source_package, source_path,
source_printed, extractor, status, title).
"""
import sys
import pymupdf


def main():
    pos, overrides = [], {}
    for a in sys.argv[1:]:
        if a.startswith("--") and "=" in a:
            k, v = a[2:].split("=", 1)
            overrides[k] = v
        else:
            pos.append(a)
    if len(pos) != 2:
        print(__doc__)
        return 2
    src, out = pos

    meta = {
        "source_package": "",
        "source_path": "",
        "source_printed": "",
        "extractor": "tools/pdf_to_mdx.py (H4642)",
        "status": "wave 1 (H4642)",
        "title": "",
    }
    meta.update(overrides)

    doc_pdf = pymupdf.open(src)
    body, stats = [], {"pages": 0, "chars": 0, "deva": 0, "empty_pages": 0}
    for pno in range(int(doc_pdf.page_count)):
        page = doc_pdf.load_page(pno)
        text = str(page.get_text("text"))
        if not text.strip():
            stats["empty_pages"] += 1
            continue
        stats["pages"] += 1
        stats["chars"] += len(text)
        stats["deva"] += sum(1 for ch in text if "\u0900" <= ch <= "\u097F")
        body.append(f"<!-- page {pno} -->\n\n{text.strip()}")

    lines = [
        "---",
        f"source_package: {meta['source_package']}",
        f"source_path: {meta['source_path']}",
        f"source_printed: {meta['source_printed']}",
        f"extractor: {meta['extractor']}",
        "method: >-",
        "  Final block PDF verbatim per-page extraction via PyMuPDF get_text",
        "  (poppler banned on Cyrillic). Page order preserved; empty pages skipped",
        "  and counted. No prose rewritten (mechanics only).",
        "derived_only: print-production PDFs are never committed",
        f"pages_with_text: {stats['pages']}",
        f"pages_empty: {stats['empty_pages']}",
        f"chars: {stats['chars']}",
        f"devanagari_chars: {stats['deva']}",
        f"status: {meta['status']}",
        "---",
        "",
        meta["title"],
        "",
    ]
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n" + "\n\n".join(body) + "\n")
    print(f"OK pages={stats['pages']}+{stats['empty_pages']}empty "
          f"chars={stats['chars']} devanagari={stats['deva']} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
