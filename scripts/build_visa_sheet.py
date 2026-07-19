#!/usr/bin/env python
"""Generate a SanskritGrammar «виза» review sheet from a JSON spec.

THE ONLY SANCTIONED WAY to author a new visa sheet (H1315, 19-07-2026). Until
now every sheet in `review/` was a hand-authored copy-paste of an identical
inline <style>/<script> skeleton — the exact drift the org review-sheet
standard exists to kill. The shell now comes from ONE place,
`csl_pyutil.render_review_sheet` at the v0.3.0 standard (V1-V8, ratified from
the h178_da vote), and this script only maps the SanskritGrammar item shape
onto it.

Contract, "hand-edited source + generated output" like scripts/build_errata.py:
    review/specs/<sheet_id>.json     is the SOURCE (hand-edited)
    review/<sheet_id>_review.html    is GENERATED, never edited by hand

Standard options applied here (see the handoff for why each):
    show_ids=True            V3 - visible copyable card-id chip
    note_min_height_px=88    V6 - taller note box
    save_as=...              V8 - banner naming sheet_id + export destination
    mark_cyrillic()          V7 - Russian runs highlighted (these sheets are
                                  heavily Russian; applied to question/panel
                                  HTML only, never to the escaped title)
    title_href               V4 - per item, only where a stable URL exists
NO rating row (V1/V5): visa sheets are categorical approve/reject/defer, they
do not score on a scale. `decided` stays the integer count the org contract
uses, and `generated` is read from the spec, never computed here, so a rebuild
is reproducible.

Existing hand-authored sheets are NOT rewritten en masse, and an already-voted
sheet must never be regenerated in place (it would orphan its decisions.json).

Usage:
    python scripts/build_visa_sheet.py review/specs/<sheet_id>.json
    python scripts/build_visa_sheet.py <spec.json> --out-dir <dir>   # proof runs
"""

import argparse
import json
import sys
from pathlib import Path

from csl_pyutil import mark_cyrillic, render_review_sheet

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# V8: the exact destination the reviewer should save the export to. Backslashes
# because the humans voting these sheets are on Windows.
SAVE_AS_TEMPLATE = "SanskritGrammar\\review\\%s_decisions.json"

DEFAULT_APPROVE = "✅ Одобрить"
DEFAULT_REJECT = "❌ Отклонить"


def build_items(spec):
    """Map the spec's item shape onto the emitter's.

    Emitter item shape: {id, filt, title, badges[], question(HTML),
    panels[(heading, html_body)], note_placeholder, title_href}. The spec
    carries panels as [heading, body] pairs (JSON has no tuples).

    `question` and panel bodies are author-supplied HTML and are passed
    through as-is; when the sheet is Russian they get mark_cyrillic(), which
    only touches text between tags, so existing markup survives intact.
    """
    highlight = spec.get("highlight_cyrillic", True)
    default_note = spec.get("note_placeholder")
    items = []
    for raw in spec["items"]:
        question = raw["question"]
        panels = [(h, body) for h, body in raw.get("panels", [])]
        if highlight:
            question = mark_cyrillic(question)
            panels = [(h, mark_cyrillic(body)) for h, body in panels]
        item = {
            "id": raw["id"],
            "filt": raw.get("filt", "all"),
            "title": raw["title"],
            "question": question,
            "panels": panels,
        }
        if raw.get("badges"):
            item["badges"] = raw["badges"]
        # V4: only where the spec supplies a stable per-item URL; never invented.
        if raw.get("title_href"):
            item["title_href"] = raw["title_href"]
        note = raw.get("note_placeholder", default_note)
        if note:
            item["note_placeholder"] = note
        items.append(item)
    return items


def build_config(spec):
    sheet_id = spec["sheet_id"]
    config = {
        "sheet_id": sheet_id,
        "title": spec["title"],
        "subtitle": spec.get("subtitle", ""),
        "footer": spec.get("footer", ""),
        "approve_label": spec.get("approve_label", DEFAULT_APPROVE),
        "reject_label": spec.get("reject_label", DEFAULT_REJECT),
        "filters": [(k, label) for k, label in spec.get("filters", [])],
        # Reproducibility: the spec owns the date, the generator never stamps one.
        "generated": spec["generated"],
        "show_ids": True,
        "note_min_height_px": 88,
        "save_as": SAVE_AS_TEMPLATE % sheet_id,
    }
    return config


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("spec", help="path to review/specs/<sheet_id>.json")
    ap.add_argument("--out-dir", default=None,
                    help="write the sheet here instead of review/ "
                         "(use for fidelity proofs; never overwrite a voted sheet)")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    html_doc = render_review_sheet(build_items(spec), build_config(spec))

    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "review"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / ("%s_review.html" % spec["sheet_id"])
    out.write_text(html_doc, encoding="utf-8")
    print("wrote %s (%d items, %d bytes)" % (out, len(spec["items"]), len(html_doc)))


if __name__ == "__main__":
    main()
