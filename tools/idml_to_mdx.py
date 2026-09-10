#!/usr/bin/env python3
"""idml_to_mdx.py — extract text from an InDesign IDML package into a Markdown (mdx) edition file.

H4484 pilot (Bibliotheca Sanscritica, Lihushina chrestomathy): the house rule binds the
pilot to the NEWEST .indd-DERIVED content (ruling MG 09-09-2026, point 4) — an .idml
export is XML text derived from the .indd, so it is both newer and ingestible without
InDesign. No .indd binary is ever committed; only the derived .mdx lands.

Mechanics only (book-press-prep guardrail): text is extracted verbatim — no prose
rewriting, no reordering inside paragraphs, no invented content.

Method:
  1. Read designmap.xml for the document-order list of Spreads.
  2. Walk each Spread; collect TextFrame @ParentStory refs; order frames geometrically
     (ItemTransform: top, then left) within the spread.
  3. For each story in that placed order, extract Story XML text: ParagraphStyleRange →
     CharacterStyleRange → <Content>, with <Br/> as line breaks.
  4. Emit YAML-front-mattered .mdx with provenance + verbatim body.

Usage: python3 tools/idml_to_mdx.py <file.idml> <out.mdx>
"""
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

IDML_NS = {
    "idpkg": "http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging",
}
def q(tag):
    return tag

def local(el):
    return el.tag.rsplit("}", 1)[-1]

def spread_order(zf):
    designmap = ET.fromstring(zf.read("designmap.xml"))
    out = []
    for node in designmap.iter():
        if node.tag.endswith("Spread"):
            src = node.get("src")
            if src:
                out.append(src)
    return out

def frames_in_spread(root):
    """TextFrames in a spread, ordered by (top, left) from ItemTransform."""
    frames = []
    for tf in root.iter():
        if local(tf) == "TextFrame" and tf.get("ParentStory"):
            attr = tf.get("ItemTransform")
            top = left = 0.0
            if attr:
                parts = attr.split()
                if len(parts) == 6:
                    left, top = float(parts[4]), float(parts[5])
            frames.append((top, left, tf.get("ParentStory")))
    frames.sort()
    return [s for _, _, s in frames]

def story_text(zf, story_id):
    path = f"Stories/Story_{story_id}.xml"
    try:
        root = ET.fromstring(zf.read(path))
    except KeyError:
        return None
    paras = []
    for para in root.iter():
        if local(para) != "ParagraphStyleRange":
            continue
        buf = []
        for crange in para.iter():
            if local(crange) != "CharacterStyleRange":
                continue
            for el in crange:
                if local(el) == "Content" and el.text:
                    buf.append(el.text)
                elif local(el) == "Br":
                    buf.append("\n")
        text = "".join(buf)
        if text.strip():
            paras.append(text)
    return paras

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src, out = sys.argv[1], sys.argv[2]
    zf = zipfile.ZipFile(src)
    ordered, seen = [], set()
    for sp in spread_order(zf):
        try:
            root = ET.fromstring(zf.read(sp))
        except KeyError:
            continue
        for sid in frames_in_spread(root):
            if sid not in seen:
                seen.add(sid)
                ordered.append(sid)
    all_stories = {n.rsplit("/", 1)[-1][len("Story_"):-len(".xml")]
                   for n in zf.namelist()
                   if n.startswith("Stories/Story_") and n.endswith(".xml")}
    unplaced = sorted(all_stories - seen)

    body, stats = [], {"paras": 0, "chars": 0, "deva": 0}
    for sid in ordered + unplaced:
        paras = story_text(zf, sid)
        if not paras:
            continue
        story_md = "\n\n".join(p.replace("\n", "  \n") for p in paras)
        body.append(f"<!-- Story {sid} -->\n\n{story_md}")
        stats["paras"] += len(paras)
        stats["chars"] += sum(len(p) for p in paras)
        stats["deva"] += sum(1 for p in paras for ch in p if "\u0900" <= ch <= "\u097F")
    doc = "\n\n".join(body)

    header = (
        "---\n"
        "source_package: lihusina-15.12.14.idml\n"
        "source_path: yadisk:Sanskrityatina/33_Lihusina/lihusina-15.12.14.idml\n"
        "source_exported: 2014-12-16\n"
        "extractor: tools/idml_to_mdx.py (H4484)\n"
        "method: >-\n"
        "  IDML Story XML verbatim extraction; spread order from designmap.xml,\n"
        "  frames ordered by ItemTransform (top,left) per spread; stories not placed\n"
        "  on any spread follow in Story-ID order. No prose rewritten (mechanics only).\n"
        "derived_only: .indd/.idml binaries are never committed\n"
        f"stories_placed: {len(seen)}\n"
        f"stories_unplaced: {len(unplaced)}\n"
        f"paragraphs: {stats['paras']}\n"
        f"chars: {stats['chars']}\n"
        f"devanagari_chars: {stats['deva']}\n"
        "status: pilot (H4484)\n"
        "---\n\n"
        "# Хрестоматия (верстка lihusina, IDML 15.12.2014) — пилотная цифровая редакция\n\n"
    )
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(header + doc + "\n")
    print(f"OK stories={len(seen)}+{len(unplaced)} paras={stats['paras']} "
          f"chars={stats['chars']} devanagari={stats['deva']} -> {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
