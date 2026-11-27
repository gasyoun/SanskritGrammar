"""Recover stress marks from the source HTML's font spans into Unicode.

The site encodes a stressed vowel as a one-character span with
style="font-family: Times New Roman CyrAC" (e.g. <span ...>а</span>).
Because that font bakes an acute into every vowel glyph, the visual stress is
real but was lost in plain-text extraction. This script re-fetches each page,
appends U+0301 COMBINING ACUTE ACCENT to vowels in those spans only, and
writes a parallel layer derived/stress/<same stem as derived/text>.txt.

The original text files and their manifest hashes are untouched.
"""

from __future__ import annotations

import json
import pathlib
import re
import time
from urllib.parse import parse_qs, urlparse

import requests
from lxml import html as lxml_html

ROOT = pathlib.Path(__file__).resolve().parent
VOWELS = set("аеёиоуыэюяАЕЁИОУЫЭЮЯ")

m = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
out_dir = ROOT / "derived" / "stress"
out_dir.mkdir(parents=True, exist_ok=True)
session = requests.Session()
session.headers.update({"User-Agent": "VisualDCS-stress-recovery/1.0 (low-rate)"})

skipped = 0
stats = {"pages": 0, "stressed_vowels": 0, "pages_with_stress": 0, "errors": 0, "resumed_existing": 0}
errors = []
for row in m["page_index"]:
    dest = out_dir / (pathlib.Path(row["path"]).stem + ".txt")
    if dest.is_file():
        # Resume after an interrupted run: already recovered pages stay as-is.
        skipped += 1
        continue
    try:
        resp = session.get(row["url"], timeout=30)
        resp.raise_for_status()
        doc = lxml_html.fromstring(resp.content.decode("utf-8", errors="replace"))
        bodies = doc.xpath('//div[contains(@class,"PlainText")]')
        if not bodies:
            continue
        body = bodies[0]
        n = 0
        for span in body.xpath('.//span[contains(@style,"CyrAC")]'):
            text = "".join(span.itertext())
            if not text:
                continue
            new = "".join(ch + "\u0301" if ch in VOWELS else ch for ch in text)
            n += new.count("\u0301")
            span.text = new
            for child in list(span):
                span.remove(child)
        text = "\n".join(
            part.replace("\xa0", " ").strip()
            for part in body.itertext()
            if part.strip()
        )
        dest.write_text(text, encoding="utf-8")
        stats["pages"] += 1
        stats["stressed_vowels"] += n
        if n:
            stats["pages_with_stress"] += 1
    except Exception as exc:
        stats["errors"] += 1
        errors.append({"url": row["url"], "error": str(exc)})
    time.sleep(0.3)

stats["resumed_existing"] = skipped

report = {
    "source_mechanism": "span[style*=Times New Roman CyrAC] -> U+0301 on its vowel",
    "retrieved_utc": "2026-11-27",
    "stats": stats,
    "errors": errors,
    "note": "Parallel layer; manifest hashes for derived/text are unchanged.",
}
(ROOT / "stress.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps(stats, ensure_ascii=False))
