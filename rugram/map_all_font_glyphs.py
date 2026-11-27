"""Map all 71 font-encoded CJK code points to Unicode.

The publisher's Grammatica TTF maps phonetic/Greek glyphs into U+3000–30FF.
Each mapping below was chosen by rendering the actual glyph from the TTF
(contact sheets in FONT_UNICODE_AUDIT.md) plus, where available, the source
context. `high` = unambiguous letter + diacritic or superscript digit;
`medium` = intonation/tone marks and a few Greek letters in bibliographies
whose shape is clear but whose scholarly reading is context-dependent.

This is a shape-faithful transcription, not an invention of phonetic meaning.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
MACRON = "\u0304"
ACUTE = "\u0301"
DIAER = "\u0308"
BREVE = "\u0306"
OGONEK = "\u0328"
CEDILLA = "\u0327"

MAPPING = {
    # already evidenced by glyph + context (first pass)
    "\u3019": ("ш" + MACRON, "high", "long ш"),
    "\u3007": ("ж" + MACRON, "high", "long ж"),
    "\u300e": ("н" + MACRON, "high", "long н"),
    "\u3017": ("ц" + MACRON, "high", "long ц"),
    # high-confidence letters with diacritics
    "\u318d": ("й" + MACRON, "high", "Й with macron"),
    "\u318f": ("й" + ACUTE, "high", "Й with acute"),
    "\u318e": ("е" + ACUTE, "high", "e with acute"),
    "\u3012": ("е" + MACRON, "high", "e with macron"),
    "\u3008": ("е" + MACRON, "high", "e with macron"),
    "\u3006": ("е" + MACRON, "high", "e with macron"),
    "\u3010": ("п" + MACRON, "high", "П with macron"),
    "\u3003": ("в" + MACRON, "high", "В with macron"),
    "\u3013": ("т" + MACRON, "high", "Т with macron"),
    "\u301b": ("б" + MACRON, "high", "Б with macron"),
    "\u301f": ("ю" + MACRON, "high", "Ю with macron"),
    "\u3169": ("б" + MACRON, "high", "б with macron"),
    "\u3005": ("д" + MACRON, "high", "д with macron"),
    "\u3011": ("р" + MACRON, "high", "р with macron"),
    "\u301c": ("ы" + MACRON, "high", "Ы with macron"),
    "\u3163": ("э" + MACRON, "high", "э with macron"),
    "\u3063": ("ё" + MACRON, "high", "ё with macron"),
    "\u306e": ("э" + ACUTE, "high", "э with acute"),
    "\u3189": ("а" + DIAER + ACUTE, "high", "a with diaeresis + acute"),
    "\u318b": ("у" + DIAER + ACUTE, "high", "y with diaeresis + acute"),
    "\u318a": ("о" + DIAER + ACUTE, "high", "o with diaeresis + acute"),
    "\u3186": ("а" + DIAER, "high", "a with diaeresis"),
    "\u3188": ("у" + DIAER, "high", "u with diaeresis"),
    "\u3043": ("ё", "high", "ё"),
    "\u3046": ("е" + "\u0302", "high", "e with circumflex"),
    "\u318c": ("е" + "\u0302", "high", "e with circumflex"),
    "\u3066": ("е" + MACRON + CEDILLA, "high", "e with macron + cedilla"),
    "\u3064": ("е" + ACUTE + CEDILLA, "high", "e with acute + cedilla"),
    "\u305b": ("е" + OGONEK, "high", "e with ogonek"),
    "\u3085": ("и" + "\u030c", "high", "i with caron"),
    "\u3161": ("ъ" + MACRON + "\u00b2", "high", "ъ with macron + superscript 2"),
    "\u3034": ("ү", "high", "u with stroke"),
    "\u3169": ("б" + MACRON, "high", "б with macron"),
    # letters with a small arc below (rendered as a hook under the letter)
    "\u3040": ("я" + BREVE, "medium", "я with arc below"),
    "\u302c": ("л" + BREVE, "medium", "Л with arc below"),
    "\u303f": ("ю" + BREVE, "medium", "Ю with arc below"),
    "\u3028": ("з" + BREVE, "medium", "з with arc below"),
    "\u302d": ("м" + BREVE, "medium", "М with arc below"),
    "\u3033": ("т" + BREVE, "medium", "Т with arc below"),
    "\u3031": ("р" + BREVE, "medium", "р with arc below"),
    "\u3027": ("ж" + BREVE, "medium", "ж with arc below"),
    "\u302b": ("к" + BREVE, "medium", "К with arc below"),
    "\u3164": ("з" + ACUTE, "medium", "з with acute"),
    # Greek letters in bibliographic references
    "\u3004": ("Γ", "medium", "Greek Gamma glyph"),
    "\u3184": ("Λ", "medium", "Greek lambda glyph"),
    # standalone tone/stress marks (rendered as bar / arc / slash)
    "\u3179": ("¯", "medium", "spacing macron, precedes stressed vowel"),
    "\u317a": ("¯", "medium", "spacing macron, precedes stressed vowel"),
    "\u317d": ("˘", "medium", "breve mark"),
    "\u3183": ("˘", "medium", "arc below/breve"),
    "\u3185": ("˘", "medium", "arc below/breve"),
    "\u3180": ("⌒", "medium", "arc above"),
    "\u317c": ("⌒", "medium", "intonation arc"),
    "\u317e": ("⌒", "medium", "intonation arc"),
    "\u317f": ("⌒", "medium", "intonation arc"),
    "\u316c": ("┐", "medium", "corner mark"),
    "\u316b": ("^", "medium", "caret mark"),
    "\u3170": ("\\", "medium", "slash mark"),
    "\u3176": ("\\", "medium", "slash mark"),
    "\u3173": ("/", "medium", "slash mark"),
    "\u3178": ("\\", "medium", "slash mark"),
    "\u3177": ("\\", "medium", "slash mark"),
    # superscript digits in intonation notation
    "\u3160": ("1²", "high", "1 + superscript 2"),
    "\u3162": ("4⁶", "high", "4 + superscript 6"),
    "\u3167": ("5³", "high", "5 + superscript 3"),
    "\u3168": ("5⁷", "high", "5 + superscript 7"),
    "\u3165": ("4²", "high", "4 + superscript 2"),
    "\u315a": ("1\u0323", "high", "1 with dot below"),
    # remaining
    "\u30e6": ("о" + MACRON, "high", "o with macron"),
}
assert len(MAPPING) == 71, f"expected 71 mappings, got {len(MAPPING)}"

m_path = ROOT / "manifest.json"
m = json.loads(m_path.read_text(encoding="utf-8"))
counts = {}
for row in m["page_index"]:
    p = ROOT / row["path"]
    text = p.read_text(encoding="utf-8")
    changed = False
    for old, (new, _conf, _desc) in MAPPING.items():
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

for d in ("derived/stress", "derived/doc"):
    for p in (ROOT / d).glob("*.txt"):
        text = p.read_text(encoding="utf-8")
        changed = False
        for old, (new, _conf, _desc) in MAPPING.items():
            n = text.count(old)
            if n:
                text = text.replace(old, new)
                counts[old] = counts.get(old, 0) + n
                changed = True
        if changed:
            p.write_text(text, encoding="utf-8")

m["page_chars"] = sum(r["chars"] for r in m["page_index"])
m["font_glyph_map"] = {
    "date": "2026-11-27",
    "count": len(MAPPING),
    "entries": {hex(ord(k)): {"unicode": v[0], "confidence": v[1], "glyph": v[2]}
                for k, v in MAPPING.items()},
    "occurrences": {hex(ord(k)): v for k, v in counts.items()},
    "method": "shape-faithful transcription from Grammatica TTF glyph rendering; "
              "medium-confidence tone/Greek marks need scholarly review",
}
m_path.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
with (ROOT / "derived" / "pages.jsonl").open("w", encoding="utf-8") as fh:
    for row in m["page_index"]:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
print("mappings", len(MAPPING), "occurrences replaced", sum(counts.values()))
