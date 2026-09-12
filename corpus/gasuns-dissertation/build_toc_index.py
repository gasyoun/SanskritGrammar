#!/usr/bin/env python3
"""H4479 — build toc_index.json from the extracted text layers.

Deterministic: reads text/*.jsonl produced by extract_text_layer.py, parses
the dissertation's own Оглавление (whitespace-normalized), maps printed page
markers, and records per-volume ranges. Output is committed; src/ PDFs are not.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).parent
TEXT = HERE / "text"

TOC_PAGE_TITLE = re.compile(r"(О|о)главлени")


def load(stem: str) -> list[dict]:
    return [json.loads(l) for l in (TEXT / f"{stem}.jsonl").open(encoding="utf-8")]


def squash(s: str) -> str:
    """TOC pages arrive letter-spaced (one char per cell); word boundaries are
    runs of 2+ whitespace. Protect those, then join single-space letter runs."""
    s = re.sub(r"(\s)\1+", "\u0001", s)   # 2+ ws -> word separator
    s = re.sub(r"\s+", "", s)             # remaining single ws = letter joins
    return s.replace("\u0001", " ").strip()


def printed_page(text: str) -> int | None:
    m = re.search(r"[—–]\s*(\d{1,3})\s*[—–]", text)
    return int(m.group(1)) if m else None


def parse_toc(raw_pages: list[dict]) -> list[dict]:
    # pdf pages 2-3 carry the Оглавление (p3 continues it without the heading)
    toc_src = [p for p in raw_pages if p["page"] in (2, 3)] or raw_pages[:4]
    body = "\n".join(p["text"] for p in toc_src)
    entries = []
    for line in body.splitlines():
        m = re.match(r"\s*(.+?)\s*\.{3,}\s*(\d{1,3})\s*$", line)
        if not m:
            continue
        title = re.sub(r"\s+", " ", m.group(1)).strip(" .—–-")
        page = int(m.group(2))
        if len(title) < 3 or not (1 <= page <= 223):
            continue
        entries.append({"section": title, "printed_page": page})
    return entries


def main() -> None:
    main_p = load("02_gasuns-dhatu-PhD-text")
    ref_p = load("01_gasuns-dhatu-PhD-ref")
    toc = parse_toc(main_p)

    def rng(stem: str) -> dict:
        p = load(stem)
        first, last = printed_page(p[0]["text"]), printed_page(p[-1]["text"])
        return {"pdf_pages": [1, len(p)],
                "printed_pages": [first, last] if first and last else None}

    index = {
        "handoff": "H4479",
        "source": "yadisk:Sanskrityatina/34_Диссертация/Итоговый текст",
        "method": "PyMuPDF text-layer extraction (pdftotext forbidden on Cyrillic)",
        "pdf_page_eq_printed_page": True,
        "volumes": {
            "01_gasuns-dhatu-PhD-ref": {
                "role": "автореферат (author's résumé)",
                "title": "СОСТАВ И СТРОЙ ДРЕВНЕИНДИЙСКИХ КОРНЕЙ: ИСТОРИЯ ИЗУЧЕНИЯ",
                **rng("01_gasuns-dhatu-PhD-ref")},
            "02_gasuns-dhatu-PhD-text": {
                "role": "основной текст диссертации",
                **rng("02_gasuns-dhatu-PhD-text")},
            "03_01-gasuns-dhatu-suppl": {"role": "Приложение 1 — список корней Уитни и Бакнелла",
                                         **rng("03_01-gasuns-dhatu-suppl")},
            "04_02-gasuns-dhatu-suppl": {"role": "Приложение 2 — корни Уитни по префиксам",
                                         **rng("04_02-gasuns-dhatu-suppl")},
            "05_03-gasuns-dhatu-suppl": {"role": "Приложение 3 — конкорданс корней Palsule/Whitney/Mayrhofer EWA/Werba VIA/Böhtlingk PWG (цель PALSULE_AUDIT)",
                                         **rng("05_03-gasuns-dhatu-suppl")},
            "06_04-gasuns-dhatu-suppl": {"role": "Приложение 4 — список корней Ж. Юэта (580 корней)",
                                         **rng("06_04-gasuns-dhatu-suppl")},
            "07_05-gasuns-dhatu-suppl": {"role": "Приложение 5 — бинарное сопоставление книг-источников",
                                         **rng("07_05-gasuns-dhatu-suppl")},
        },
        "toc_main_text": toc,
        "toc_entry_count": len(toc),
    }
    out = HERE / "toc_index.json"
    out.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"toc_index.json: {len(toc)} TOC entries, 7 volumes")
    for e in toc[:6]:
        print("  ", e)


if __name__ == "__main__":
    main()
