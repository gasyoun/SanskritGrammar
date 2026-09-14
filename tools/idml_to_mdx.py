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

Usage: python3 tools/idml_to_mdx.py <file.idml> <out.mdx> --source-path yadisk:<path> [--title ...] [--status ...]

H4628 wave 1: per-volume provenance flags (--source-path/--title/--status); the
Lihushina pilot mdx (H4484) stays as committed and is NOT regenerated.
"""
import argparse
import datetime
import os
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
    ap = argparse.ArgumentParser(description="Extract an InDesign IDML package into a verbatim .mdx edition file.")
    ap.add_argument("idml", help="input .idml package")
    ap.add_argument("out", help="output .mdx path")
    ap.add_argument("--source-path", required=True,
                    help="upstream provenance path (e.g. yadisk:Bibliotheca/…)")
    ap.add_argument("--title", help="edition title line (default derived from file name)")
    ap.add_argument("--status", default="wave-1 (H4628)",
                    help="status line recorded in the mdx front matter")
    ap.add_argument("--extractor-tag", default="H4628",
                    help="handoff tag recorded after 'extractor: tools/idml_to_mdx.py'")
    args = ap.parse_args()
    src, out = args.idml, args.out
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

    exported_date = datetime.date.fromtimestamp(os.path.getmtime(src)).isoformat()
    title = args.title or (
        src.rsplit("/", 1)[-1].rsplit(".", 1)[0] + " — вербатим-цифровая редакция")
    header = (
        "---\n"
        f"source_package: {src.rsplit('/', 1)[-1]}\n"
        f"source_path: {args.source_path}\n"
        f"source_exported: {exported_date}\n"
        f"extractor: tools/idml_to_mdx.py ({args.extractor_tag})\n"
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
        f"status: {args.status}\n"
        "---\n\n"
        f"# {title}\n\n"
    )
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(header + doc + "\n")
    print(f"OK stories={len(seen)}+{len(unplaced)} paras={stats['paras']} "
          f"chars={stats['chars']} devanagari={stats['deva']} -> {out}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
