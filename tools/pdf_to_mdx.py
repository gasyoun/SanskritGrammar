#!/usr/bin/env python3
"""pdf_to_mdx.py — extract the live text layer of a print-final PDF into a verbatim .mdx edition file.

H4628 wave-1 fallback (census D1 note: vols whose full body was never exported
as .idml): PyMuPDF text-layer extraction, mechanics only — verbatim page text,
page markers kept, no prose rewriting, nothing inferred from images.

Usage: python3 tools/pdf_to_mdx.py <file.pdf> <out.mdx> --source-path yadisk:<path> [--title ...] [--status ...]
"""
import argparse
import datetime
import os
import sys

import pymupdf


def main():
    ap = argparse.ArgumentParser(description="Extract PDF text layer into a verbatim .mdx edition file.")
    ap.add_argument("pdf")
    ap.add_argument("out")
    ap.add_argument("--source-path", required=True)
    ap.add_argument("--title")
    ap.add_argument("--status", default="wave-1 (H4628)")
    ap.add_argument("--extractor-tag", default="H4628")
    args = ap.parse_args()

    doc = pymupdf.open(args.pdf)
    parts, stats = [], {"pages_text": 0, "chars": 0, "deva": 0}
    pages_total = doc.page_count
    for i in range(pages_total):
        text = str(doc[i].get_text() or "").rstrip()
        if not text:
            continue
        stats["pages_text"] += 1
        stats["chars"] += len(text)
        stats["deva"] += sum(1 for ch in text if "\u0900" <= ch <= "\u097F")
        parts.append(f"<!-- стр. {i + 1} -->\n\n{text}")
    doc.close()
    body = "\n\n".join(parts)

    title = args.title or (args.pdf.rsplit("/", 1)[-1].rsplit(".", 1)[0] + " — вербатим-цифровая редакция")
    header = (
        "---\n"
        f"source_package: {args.pdf.rsplit('/', 1)[-1]}\n"
        f"source_path: {args.source_path}\n"
        f"source_exported: {datetime.date.fromtimestamp(os.path.getmtime(args.pdf)).isoformat()}\n"
        f"extractor: tools/pdf_to_mdx.py ({args.extractor_tag})\n"
        "method: >-\n"
        "  PyMuPDF text-layer extraction, page order, verbatim; page markers kept;\n"
        "  image-only pages yield nothing (no OCR). No prose rewritten (mechanics only).\n"
        "derived_only: print-final PDFs are never committed\n"
        f"pages_total: {pages_total}\n"
        f"pages_with_text: {stats['pages_text']}\n"
        f"chars: {stats['chars']}\n"
        f"devanagari_chars: {stats['deva']}\n"
        f"status: {args.status}\n"
        "---\n\n"
        f"# {title}\n\n"
    )
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(header + body + "\n")
    print(f"OK pages_with_text={stats['pages_text']} chars={stats['chars']} "
          f"devanagari={stats['deva']} -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
