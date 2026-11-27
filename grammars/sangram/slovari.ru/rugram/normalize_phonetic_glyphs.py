"""Map font-encoded phonetic glyphs at CJK code points to real Unicode.

Evidence: rendering the publisher's Grammatica TTF shows these glyphs as
Cyrillic letters with a macron (long consonants); the surrounding text
confirms it (ви[〇']ать = визжать, о[〗]а = отца, весе[『']ий = весенний,
[〙'е]пка = щепка). They are NOT CJK punctuation and must not render as such.

Only the four glyphs attested by both glyph shape and context are mapped.
The other 67 CJK-range code points in the corpus remain untouched: their
meaning is not established, so guessing would corrupt the source.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
MAP = {
    "\u3019": "\u0448\u0304",  # 〙 -> ш̄  (long ш; follows with ' = soft)
    "\u3007": "\u0436\u0304",  # 〇 -> ж̄  (long ж)
    "\u300e": "\u043d\u0304",  # 『 -> н̄  (long н)
    "\u3017": "\u0446\u0304",  # 〗 -> ц̄  (long ц)
}

m_path = ROOT / "manifest.json"
m = json.loads(m_path.read_text(encoding="utf-8"))
counts = {}

for row in m["page_index"]:
    for rel in (row["path"],):
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        changed = False
        for old, new in MAP.items():
            n = text.count(old)
            if n:
                text = text.replace(old, new)
                counts[old] = counts.get(old, 0) + n
                changed = True
        if changed:
            p.write_text(text, encoding="utf-8")
            payload = text.encode("utf-8")
            row["chars"] = len(text)
            row["sha256"] = hashlib.sha256(payload).hexdigest()

# Parallel layers, if present.
for d in ("derived/stress", "derived/doc"):
    for p in (ROOT / d).glob("*.txt"):
        text = p.read_text(encoding="utf-8")
        changed = False
        for old, new in MAP.items():
            n = text.count(old)
            if n:
                text = text.replace(old, new)
                counts[old] = counts.get(old, 0) + n
                changed = True
        if changed:
            p.write_text(text, encoding="utf-8")

m["page_chars"] = sum(r["chars"] for r in m["page_index"])
m["phonetic_glyph_map"] = {
    "date": "2026-11-27",
    "mapping": {hex(ord(k)): v for k, v in MAP.items()},
    "counts": {hex(ord(k)): v for k, v in counts.items()},
    "evidence": "Grammatica TTF glyph rendering + textual context; 67 other CJK-range code points left untouched",
}
m_path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
with (ROOT / "derived" / "pages.jsonl").open("w", encoding="utf-8") as fh:
    for row in m["page_index"]:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
print({hex(ord(k)): v for k, v in counts.items()})
