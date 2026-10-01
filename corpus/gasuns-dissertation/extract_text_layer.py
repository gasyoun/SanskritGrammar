#!/usr/bin/env python3
"""H4479 — Gasuns PhD dissertation: text-layer extraction (derived-only).

Extracts the PDF text layer with PyMuPDF (pdftotext/poppler is FORBIDDEN on
Cyrillic PDFs — plausible-blank trap, DANGER_FACTS). Every page is quality-
gated: a page counts as GARBAGE/BLANK unless Cyrillic-bearing, and a FILE
fails loud when its text layer does not yield real Russian prose. PDF sources
stay gitignored (corpus/gasuns-dissertation/src/); only derived JSONL +
indexes are committed.

Usage: python3 extract_text_layer.py [--src SRC] [--out OUT]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

import pymupdf

CYR = re.compile(r"[\u0400-\u04FF]")
# Frequent Russian function words — a real text layer hits these within pages.
CANARY_WORDS = ("и", "в", "не", "на", "что", "как", "для", "или")
BAD_CHARS = re.compile(r"[\uFFFD\uE000-\uF8FF]")


def page_stats(text: str) -> dict:
    n = len(text)
    cyr = len(CYR.findall(text))
    bad = len(BAD_CHARS.findall(text))
    words = re.findall(r"[А-Яа-яЁёA-Za-z]+", text.lower())
    canary = sum(1 for w in CANARY_WORDS if w in words)
    return {
        "n_chars": n,
        "cyr_chars": cyr,
        "cyr_ratio": round(cyr / n, 3) if n else 0.0,
        "bad_chars": bad,
        "canary_hits": canary,
    }


def page_ok(st: dict) -> bool:
    """Garbage gate, not prose gate: supplements are IAST root tables, so a
    page fails only on real corruption (mojibake/PUA chars, empty layer)."""
    if st["n_chars"] < 40:
        return False
    if st["bad_chars"] > st["n_chars"] * 0.02:
        return False
    return True


def file_gate(pages: list[dict], text_join: str) -> str:
    """File-level fail-loud: real layer = nearly all pages carry text with low
    garbage AND a positive identity canary (Russian prose words, or the
    Приложение headers of the supplement tables)."""
    if not pages:
        return "FAIL"
    ok_ratio = sum(1 for p in pages if p["verdict"] == "ok") / len(pages)
    prose_canary = any(p["canary_hits"] >= 2 for p in pages[:10])
    suppl_canary = "Приложение" in text_join
    iast = len(re.findall(r"[āīūṛṝḷḹṅñṭḍṇśṣṁḥ]", text_join))
    iast_canary = iast > 200
    identity = prose_canary or (suppl_canary and iast_canary)
    return "PASS" if (ok_ratio >= 0.9 and identity) else "FAIL"


def extract_file(pdf: Path, out_dir: Path) -> dict:
    doc = pymupdf.open(pdf)
    out_path = out_dir / (pdf.stem + ".jsonl")
    pages = []
    with out_path.open("w", encoding="utf-8") as fh:
        for i in range(doc.page_count):
            page = doc.load_page(i)
            text = str(page.get_text("text"))
            text = unicodedata.normalize("NFC", text)
            st = page_stats(text)
            rec = {
                "file": pdf.name,
                "page": i + 1,
                "of": doc.page_count,
                "verdict": "ok" if page_ok(st) else "suspect",
                **st,
                "text": text,
            }
            pages.append(rec)
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    ok = sum(1 for p in pages if p["verdict"] == "ok")
    cyr_pages = sum(1 for p in pages if p["cyr_chars"] > 0)
    chars = sum(p["n_chars"] for p in pages)
    level = file_gate(pages, "\n".join(p["text"] for p in pages))
    return {
        "file": pdf.name,
        "size_bytes": pdf.stat().st_size,
        "pages": doc.page_count,
        "pages_ok": ok,
        "pages_cyr": cyr_pages,
        "chars": chars,
        "usable_ratio": round(ok / doc.page_count, 3) if doc.page_count else 0,
        "text_layer": level,
        "jsonl": str(out_path),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    here = Path(__file__).parent
    ap.add_argument("--src", type=Path, default=here / "src")
    ap.add_argument("--out", type=Path, default=here / "text")
    args = ap.parse_args()

    pdfs = sorted(args.src.glob("*.pdf"))
    if not pdfs:
        print(f"NO PDFs in {args.src} — download step missing", file=sys.stderr)
        return 2
    args.out.mkdir(parents=True, exist_ok=True)

    verdicts = [extract_file(p, args.out) for p in pdfs]
    report = args.out.parent / "EXTRACTION_REPORT.json"
    report.write_text(
        json.dumps({"tool": "extract_text_layer.py (PyMuPDF 1.28.x)",
                    "verdicts": verdicts}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    for v in verdicts:
        flag = "✅" if v["text_layer"] == "PASS" else "❌"
        print(f"{flag} {v['file']}: {v['pages']}p, ok={v['pages_ok']}, "
              f"chars={v['chars']}, layer={v['text_layer']}")
    return 0 if all(v["text_layer"] == "PASS" for v in verdicts) else 1


if __name__ == "__main__":
    sys.exit(main())
