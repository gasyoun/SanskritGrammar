#!/usr/bin/env python3
"""Extract Usha Sanka's dhātu-kārakākāṅkṣā model into a structured
dhātu-group → kāraka-role → citation dataset (H1371 follow-up).

SOURCE (local, UNTRACKED — 361 MB trove, see Concordance/USHA_SANKA_KARAKA_TROVE_REUSE_SURVEY_2026.md):
  Concordance/UshaSanka_Ph.D_2014/धातुकारकाकांक्षा.docx  — clean Unicode (no OCR).
The bound thesis PDF has a broken text layer; this .docx is the machine-readable source.
Because the source is untracked local bulk, this script runs LOCALLY (like sangram/audit/
rederive_dcs_numbers.py), not in CI; its committed OUTPUT under Concordance/usha_karaka_gold/ is
what the repo ships and what any consumer (SG-SE-013) reads.

Structure parsed per verb-group:
  <sense title> · धातुकोशाः- · धातुविवरम्- <dhātu detail lines> · धात्वर्थः- <senses>
  · कारकाकाङ्क्षा- · <bold kāraka-role headers, each followed by citation paragraphs '…~source'>
Author's चर्चा/टिप्पणी (discussion) blocks are captured separately, never mixed into citations.

Output: Concordance/usha_karaka_gold/usha_karaka_gold.json (grouped) + .csv (flat, one row per
(group, role, citation)). Read-only on the source.

Model: Opus 4.8 (claude-opus-4-8[1m]), 20-07-2026 (H1371 follow-up).
"""
import csv
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "Concordance" / "UshaSanka_Ph.D_2014" / "धातुकारकाकांक्षा.docx"
OUT = ROOT / "Concordance" / "usha_karaka_gold"

ROLES = {
    "कर्ता": "kartṛ", "कर्तृ": "kartṛ",
    "कर्म": "karman", "कर्मन्": "karman",
    "करण": "karaṇa", "करणम्": "karaṇa",
    "सम्प्रदान": "sampradāna", "सम्प्रदानम्": "sampradāna", "संप्रदान": "sampradāna",
    "अपादान": "apādāna", "अपादानम्": "apādāna",
    "अधिकरण": "adhikaraṇa", "अधिकरणम्": "adhikaraṇa",
    "तादर्थ्य": "tādarthya", "तादर्थ्यम्": "tādarthya",
    "हेतु": "hetu", "हेतुः": "hetu",
    "अन्य": "anya", "अन्यः": "anya",
}
SECTIONS = {"धातुकोशाः", "धातुविवरम्", "धात्वर्थः", "कारकाकाङ्क्षा", "कारकाकांक्षा"}
DISCUSSION = {"चर्चा", "टिप्पणी", "निष्कर्षः"}


def paragraphs(docx):
    xml = zipfile.ZipFile(docx).read("word/document.xml").decode("utf-8")
    for p in re.findall(r"<w:p\b.*?</w:p>", xml, re.S):
        text = "".join(re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S))
        text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").strip()
        bold = ("<w:b/>" in p) or ("<w:b " in p)
        if text:
            yield text, bold


def section_of(text):
    m = re.match(r"^\s*([ऀ-ॿ]+?)[-–—]\s*$", text)
    return m.group(1) if m and m.group(1) in SECTIONS else None


def split_citation(text):
    out = []
    for chunk in re.split(r"(?=~)", text):
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("~"):
            src = chunk[1:].strip()
            if out:
                out[-1]["source"] = src
            else:
                out.append({"text": "", "source": src})
        else:
            out.append({"text": chunk, "source": None})
    return out


def parse(src):
    groups, cur, mode, role, prev = [], None, None, None, None
    for text, bold in paragraphs(src):
        sec = section_of(text)
        if sec == "धातुकोशाः":
            cur = {"sense_title": prev or "", "dhatus": [], "dhatu_details": [],
                   "senses": [], "karaka": {}, "discussion": []}
            groups.append(cur)
            mode, role = "kosha", None
            continue
        prev = text
        if sec == "धातुविवरम्":
            mode, role = "dhatu", None
            continue
        if sec == "धात्वर्थः":
            mode, role = "artha", None
            continue
        if sec in ("कारकाकाङ्क्षा", "कारकाकांक्षा"):
            mode, role = "karaka", None
            continue
        if cur is None:
            continue
        if mode == "dhatu":
            m = re.match(r"^\(\s*\d*\s*\)\.\s*([ऀ-ॿ].*)$", text)
            (cur["dhatus"] if m else cur["dhatu_details"]).append((m.group(1) if m else text).strip())
        elif mode == "artha":
            cur["senses"].append(text)
        elif mode in ("karaka", "carca"):
            hdr = re.match(r"^\s*([ऀ-ॿ]+?)[-–—]\s*(.*)$", text) if bold else None
            if hdr and hdr.group(1) in ROLES:
                role, mode = ROLES[hdr.group(1)], "karaka"
                cur["karaka"].setdefault(role, [])
                if hdr.group(2).strip():
                    cur["karaka"][role].extend(split_citation(hdr.group(2).strip()))
            elif hdr and hdr.group(1) in DISCUSSION:
                mode, role = "carca", None
                if hdr.group(2).strip():
                    cur["discussion"].append(hdr.group(2).strip())
            elif hdr:
                role = None
            elif mode == "carca":
                cur["discussion"].append(text)
            elif role:
                cur["karaka"][role].extend(split_citation(text))
    return [g for g in groups if g["dhatus"] or g["karaka"]]


def main():
    if not SRC.exists():
        print(f"ERROR: source not found (untracked local trove): {SRC}", file=sys.stderr)
        return 1
    groups = parse(SRC)
    for gi, g in enumerate(groups):
        g["group_id"] = gi

    rows = []
    for g in groups:
        dh = " ".join(g["dhatus"])
        for role, cits in g["karaka"].items():
            for c in cits:
                if c["text"] or c["source"]:
                    rows.append({"group_id": g["group_id"], "dhatus": dh, "karaka": role,
                                 "citation": c["text"], "source": c["source"] or ""})

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "usha_karaka_gold.json").write_text(
        json.dumps(groups, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    with open(OUT / "usha_karaka_gold.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["group_id", "dhatus", "karaka", "citation", "source"])
        w.writeheader()
        w.writerows(rows)

    rc = Counter(r["karaka"] for r in rows)
    with_src = sum(1 for r in rows if r["source"])
    print(f"groups: {len(groups)}")
    print(f"distinct dhātus: {len({d for g in groups for d in g['dhatus']})}")
    print(f"citation rows: {len(rows)}  (with a source: {with_src}, {round(100*with_src/len(rows))}%)")
    print(f"by role: {dict(rc)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
