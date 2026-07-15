#!/usr/bin/env python
"""Generate print-ready errata sheets (листы опечаток) from each book's errata.yml.

Sibling of scripts/build_errata.py and same "hand-edited source + generated output"
contract: `<Book>/errata.yml` is the source; `<Book>/ERRATA_PRINT_SHEET.html` is
GENERATED and must never be edited by hand.

Why a separate output from ERRATA.md: the Markdown register is a repo document
(git links, found_by provenance, fix-tracking against the changelog); the print
sheet is the classic publisher's «Замеченные опечатки» insert — a compact,
self-contained A4 page a human can print from any browser and tuck into the
physical book, hand to a reprint editor, or mail to the electronic-edition
maintainer. Layout follows the traditional Russian лист опечаток: one numbered
table «Место | Напечатано | Следует читать», sources and generation date in
small print, long rationales left to ERRATA.md.

Parsing, dedup and ordering are IMPORTED from build_errata.py (load_book) — one
canonical reader for errata.yml, not two.

Only books whose errata.yml has entries get a sheet (no empty printouts);
a stale ERRATA_PRINT_SHEET.html whose register has since been emptied is removed.

Usage:
    python scripts/build_errata_print_sheet.py                    # all populated books
    python scripts/build_errata_print_sheet.py KnauerFrazy_1908   # one book
"""

import datetime
import html
import sys
from pathlib import Path

from build_errata import ROOT, ddmmyyyy, load_book

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

STYLE = """
  @page { size: A4; margin: 20mm; }
  body { font-family: 'PT Serif', Georgia, 'Times New Roman', serif; color: #111;
         max-width: 175mm; margin: 0 auto; padding: 12px; line-height: 1.45; }
  h1 { font-size: 20px; margin: 0 0 2px; letter-spacing: 0.04em; }
  p.work { font-size: 14px; font-style: italic; margin: 0 0 14px; }
  table { border-collapse: collapse; width: 100%; font-size: 13px; }
  th, td { border: 1px solid #333; padding: 4px 8px; vertical-align: top; text-align: left; }
  th { font-weight: bold; background: #f2f2f2; }
  td.n { text-align: right; white-space: nowrap; width: 1%; }
  td.loc { width: 24%; }
  del { text-decoration: none; }  /* «Напечатано» is quoted, not struck through */
  p.small { font-size: 11px; color: #444; margin-top: 12px; }
  @media print { body { padding: 0; } p.small { page-break-inside: avoid; } }
"""


def render_sheet(work: str, entries: list) -> str:
    rows = []
    for i, e in enumerate(entries, 1):
        page = str(e.get("page", "")).strip()
        loc = e.get("line", "")
        # page 0 = the repo's "no anchorable print page" convention — show only the locator.
        place = loc if page in ("", "0") else f"с. {page}, {loc}" if loc else f"с. {page}"
        rows.append(
            "    <tr>"
            f'<td class="n">{i}</td>'
            f'<td class="loc">{html.escape(place)}</td>'
            f"<td>{html.escape(e.get('instead', ''))}</td>"
            f"<td>{html.escape(e.get('read', ''))}</td>"
            "</tr>"
        )

    sources = sorted({src for e in entries for src in e.get("found_by", [])})
    today = ddmmyyyy(datetime.date.today())
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Замеченные опечатки — {html.escape(work)}</title>
<style>{STYLE}</style>
</head>
<body>
<h1>ЗАМЕЧЕННЫЕ ОПЕЧАТКИ</h1>
<p class="work">{html.escape(work)}</p>
<table>
  <thead>
    <tr><th>№</th><th>Место</th><th>Напечатано</th><th>Следует читать</th></tr>
  </thead>
  <tbody>
{chr(10).join(rows)}
  </tbody>
</table>
<p class="small">Источники: {html.escape('; '.join(sources))}.<br>
Всего позиций: {len(entries)}. Лист сгенерирован {today} из errata.yml
(полные обоснования каждой позиции — в ERRATA.md той же папки); файл
ERRATA_PRINT_SHEET.html не редактируется вручную.</p>
</body>
</html>
"""


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    ymls = sorted(ROOT.glob("*/errata.yml"))
    if only:
        ymls = [y for y in ymls if y.parent.name == only]
        if not ymls:
            sys.exit(f"no {only}/errata.yml found")

    written, removed, skipped = [], [], []
    for yml in ymls:
        work, entries = load_book(yml)
        out = yml.parent / "ERRATA_PRINT_SHEET.html"
        if not entries:
            if out.exists():
                out.unlink()
                removed.append(out)
            skipped.append(yml.parent.name)
            continue
        out.write_text(render_sheet(work, entries), encoding="utf-8", newline="\n")
        written.append((out, len(entries)))

    for out, n in written:
        print(f"-> {out.relative_to(ROOT)} ({n} позиций)")
    for out in removed:
        print(f"-> removed stale {out.relative_to(ROOT)}")
    if skipped:
        print(f"(empty registers, no sheet: {', '.join(skipped)})")


if __name__ == "__main__":
    main()
