#!/usr/bin/env python
"""Extract a build_visa_sheet.py JSON spec out of a hand-authored visa sheet.

MIGRATION AID, not part of the authoring path. Every visa sheet in `review/`
predates the generator (H1315): its content lives inline in the HTML, so the
only faithful way to put one through the generator — for a fidelity proof, or
to migrate a sheet a human wants to keep evolving — is to read the cards back
out mechanically. Hand-copying dense Russian card HTML risks silent
transcription drift, which is exactly what the fidelity proof is meant to rule
out.

This inverts `csl_pyutil.render_review_sheet`'s document assembly: the anchors
below (h1 / .sub / .filterbar / .card / footer) are the emitter's own template
literals, so any drift shows up as a parse failure here rather than as a quiet
mismatch.

What is raw HTML vs escaped follows the emitter exactly: config title/subtitle/
footer are interpolated raw, whereas each card's title/id/filt/note-placeholder
and the vote labels go through esc() — so only the latter are unescaped here.
Card `question` and panel bodies are author HTML and are copied verbatim.

Usage:
    python scripts/visa_sheet_spec_from_html.py review/<sheet>_review.html -o review/specs/<sheet_id>.json
"""

import argparse
import html as htmllib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

RE_H1 = re.compile(r'<h1>(?P<title>.*?) — (?P<n>\d+) items</h1>', re.S)
RE_SUB = re.compile(
    r'<div class="sub">Generated (?P<generated>.*?) &middot; sheet_id '
    r'<code>(?P<sheet_id>.*?)</code> &middot; (?P<subtitle>.*?)</div>', re.S)
RE_FILTERBAR = re.compile(r'<div class="filterbar" id="filterbar">(?P<body>.*?)</div>', re.S)
RE_FILTER_BTN = re.compile(r'<button data-filter="(?P<key>[^"]*)"(?P<cls>[^>]*)>(?P<label>.*?)</button>', re.S)
RE_FOOTER = re.compile(r'<footer class="hint">(?P<footer>.*?) Keyboard:', re.S)
RE_CARD = re.compile(
    r'<section class="card" data-id="(?P<id>[^"]*)" data-filt="(?P<filt>[^"]*)">\s*'
    r'<header><div class="hw">(?P<hw>.*?)</div>(?P<after_hw>.*?)</header>\s*'
    r'<div class="question">(?P<question>.*?)</div>\s*'
    r'(?P<panels>(?:<div class="panel">.*?</div>\s*)*)'
    r'<div class="controls">(?P<controls>.*?)</div>.*?'
    r'<textarea class="note" placeholder="(?P<note>[^"]*)"></textarea>\s*'
    r'</section>', re.S)
RE_PANEL = re.compile(r'<div class="panel"><h4>(?P<h4>.*?)</h4>(?P<body>.*?)</div>', re.S)
RE_BADGE = re.compile(r'<span class="badge">(?P<b>.*?)</span>', re.S)
RE_HWLINK = re.compile(r'<a class="hwlink" href="(?P<href>[^"]*)"[^>]*>(?P<text>.*?)</a>', re.S)
RE_APPROVE = re.compile(r'<button class="vote approve" data-vote="approve">&#9989; (?P<l>.*?)</button>', re.S)
RE_REJECT = re.compile(r'<button class="vote reject" data-vote="reject">&#10060; (?P<l>.*?)</button>', re.S)


def need(rx, text, what):
    m = rx.search(text)
    if not m:
        raise SystemExit("could not locate %s — sheet does not match the emitter's template" % what)
    return m


def extract_card(m):
    hw = m.group("hw")
    # V4: a linked header means the spec carries title_href.
    link = RE_HWLINK.search(hw)
    if link:
        title_html, title_href = link.group("text"), htmllib.unescape(link.group("href"))
    else:
        title_html, title_href = hw, None
    # render_card emits '%s %s' % (title, badges); with no badges a trailing
    # space is left behind, so strip after pulling the badges off.
    badges = [htmllib.unescape(b) for b in RE_BADGE.findall(title_html)]
    title_html = RE_BADGE.sub("", title_html)
    item = {
        "id": htmllib.unescape(m.group("id")),
        "filt": htmllib.unescape(m.group("filt")),
        "title": htmllib.unescape(title_html).strip(),
        "question": m.group("question").strip(),
        "panels": [[htmllib.unescape(h4), body.strip()]
                   for h4, body in RE_PANEL.findall(m.group("panels"))],
    }
    if title_href:
        item["title_href"] = title_href
    if badges:
        item["badges"] = badges
    return item, htmllib.unescape(m.group("note"))


def extract_spec(text):
    """Parse a rendered visa sheet back into a build_visa_sheet.py spec dict."""
    h1 = need(RE_H1, text, "the <h1> title")
    sub = need(RE_SUB, text, "the sheet_id/generated subtitle")
    footer = need(RE_FOOTER, text, "the footer")

    filters = []
    for fm in RE_FILTER_BTN.finditer(need(RE_FILTERBAR, text, "the filter bar").group("body")):
        key = htmllib.unescape(fm.group("key"))
        if key in ("all", "unvoted"):   # emitter adds these two itself
            continue
        filters.append([key, htmllib.unescape(fm.group("label"))])

    items, notes = [], set()
    for cm in RE_CARD.finditer(text):
        item, note = extract_card(cm)
        items.append(item)
        notes.add(note)

    declared = int(h1.group("n"))
    if len(items) != declared:
        raise SystemExit("parsed %d cards but the header declares %d — refusing to write a "
                         "lossy spec" % (len(items), declared))

    spec = {
        "sheet_id": sub.group("sheet_id"),
        "title": h1.group("title"),
        "subtitle": sub.group("subtitle").strip(),
        "footer": footer.group("footer").strip(),
        "generated": sub.group("generated").strip(),
        "approve_label": htmllib.unescape(need(RE_APPROVE, text, "the approve label").group("l")),
        "reject_label": htmllib.unescape(need(RE_REJECT, text, "the reject label").group("l")),
        "filters": filters,
        "highlight_cyrillic": True,
        "items": items,
    }
    # One shared placeholder is the norm; keep per-item only if they really differ.
    if len(notes) == 1:
        spec["note_placeholder"] = notes.pop()
    else:
        for item, cm in zip(items, RE_CARD.finditer(text)):
            item["note_placeholder"] = htmllib.unescape(cm.group("note"))
    return spec


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sheet", help="path to an existing review/<sheet>_review.html")
    ap.add_argument("-o", "--out", required=True, help="where to write the JSON spec")
    args = ap.parse_args()

    spec = extract_spec(Path(args.sheet).read_text(encoding="utf-8"))
    items = spec["items"]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("wrote %s (%d items, %d filters)" % (out, len(items), len(spec["filters"])))


if __name__ == "__main__":
    main()
