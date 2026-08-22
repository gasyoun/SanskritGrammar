#!/usr/bin/env python
"""Generate a SanskritGrammar «виза» review sheet from a JSON spec.

THE ONLY SANCTIONED WAY to author a new visa sheet (H1315, 19-07-2026). Until
now every sheet in `review/` was a hand-authored copy-paste of an identical
inline <style>/<script> skeleton — the exact drift the org review-sheet
standard exists to kill. The shell now comes from ONE place,
`csl_pyutil.render_review_sheet` at the v0.9.0 standard (V1-V8 + V9 evidence
manifest, ratified from the h178_da vote / H1889), and this script only maps
the SanskritGrammar item shape onto it.

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
    manifest=                V9 - EvidenceManifest (spec path joined; every card
                                  carries title+question evidence fields) so the
                                  missing-manifest PreflightWarning is gone and
                                  csl-pyutil 1.0.0 will not hard-fail this path
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

from csl_pyutil import EvidenceManifest, mark_cyrillic, render_review_sheet

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent

# U6 (H2847) Russian-only reviewer chrome, defined locally against the
# csl-pyutil v0.9.0 UI_STRINGS contract. The pinned emitter exports no
# RU_UI_STRINGS - the H3103 import referenced an unpinned local edit and broke
# test collection repo-wide (required CI job red since 57dadc4). Keys mirror
# csl_pyutil.review_sheet.UI_STRINGS exactly; every value is the REPLACEMENT
# TEXT for that chrome element (for regex keys, the new ``body`` group).
# save_banner stays out: its default bakes in this sheet's own sheet_id/save_as,
# so build_config overrides it per sheet below.
RU_LEGEND = (
    "<b>Одобрить</b> &mdash; принять предложенное изменение/ответ на карточке "
    "(отдельного «одобрить как есть» нет: одобрение означает согласие с написанным). "
    "<b>Отклонить</b> &mdash; оставить текущую запись/ответ без изменений. "
    "<b>Отложить</b> &mdash; пока не решено, вернуться позже. Поле заметки &mdash; "
    "для запроса частичной правки вместо полного отклонения."
)
RU_DEFER_BUTTON = "Отложить"
RU_REJECT_REASON_LABEL = "Причина"


def _ru_ui_strings(approve_label, reject_label):
    """Per-sheet Russian chrome; the keyboard hint embeds this sheet's own vote labels."""
    return {
        "download_button": "Скачать decisions.json",
        "save_button": "Сохранить в папку\u2026",
        "legend": RU_LEGEND,
        "defer_button": RU_DEFER_BUTTON,
        "reject_reason_label": RU_REJECT_REASON_LABEL,
        "footer_hint": (
            "Клавиатура: <kbd>a</kbd> %(approve)s &middot; <kbd>r</kbd> %(reject)s "
            "&middot; <kbd>d</kbd> отложить &middot; <kbd>&darr;</kbd>/<kbd>&uarr;</kbd> "
            "вперёд/назад. Голоса автосохраняются в localStorage этого браузера; "
            "по завершении нажмите «Скачать decisions.json» "
            "(неразобранные пункты экспортируются со значением decision:null)."
        ) % {"approve": approve_label, "reject": reject_label},
    }

# V8: the exact destination the reviewer should save the export to. Backslashes
# because the humans voting these sheets are on Windows.
SAVE_AS_TEMPLATE = "SanskritGrammar\\review\\%s_decisions.json"

DEFAULT_APPROVE = "✅ Одобрить"
DEFAULT_REJECT = "❌ Отклонить"

# Relative path the screening block already names as the sheet's evidence source.
SPEC_EVIDENCE_TEMPLATE = "review/specs/%s.json"


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


# File/format tokens that appear in visa-sheet prose (paths like
# `sangram/articles/.../index.mdx`) and trip the V9 SLP1 detector's
# CamelCase/marker heuristics even though they are not Sanskrit encodings.
# Tunable via the spec's optional `allow_slp1_tokens` list (appended).
DEFAULT_ALLOW_SLP1 = ("mdx", "MDX", "html", "HTML", "json", "JSON", "tsv", "TSV")


def build_config(spec):
    sheet_id = spec["sheet_id"]
    allow = list(DEFAULT_ALLOW_SLP1)
    allow.extend(spec.get("allow_slp1_tokens") or [])
    approve_label = spec.get("approve_label", DEFAULT_APPROVE)
    reject_label = spec.get("reject_label", DEFAULT_REJECT)
    config = {
        "sheet_id": sheet_id,
        "title": spec["title"],
        "subtitle": spec.get("subtitle", ""),
        "footer": spec.get("footer", ""),
        "approve_label": approve_label,
        "reject_label": reject_label,
        "filters": [(k, label) for k, label in spec.get("filters", [])],
        # Reproducibility: the spec owns the date, the generator never stamps one.
        "generated": spec["generated"],
        "show_ids": True,
        "note_min_height_px": 88,
        "save_as": SAVE_AS_TEMPLATE % sheet_id,
        # V9: domain file extensions are not SLP1 leaks (H2355 residual).
        "preflight": {"allow_slp1_tokens": allow},
        # U6 (H2847): Russian-only reviewer chrome. save_banner overridden
        # because RU_UI_STRINGS excludes it by design (its default bakes in
        # this sheet's own sheet_id/save_as).
        "ui_strings": dict(_ru_ui_strings(approve_label, reject_label), save_banner=(
            "&#128229; Ваш экспорт скачивается как <code>%s_decisions.json</code> "
            "&rarr; сохраните его в <code>%s</code> (значение <code>sheet_id</code> "
            "внутри файла &mdash; <code>%s</code> &mdash; так следующая сессия узнаёт, "
            "к какому листу относятся эти решения)."
            % (sheet_id, SAVE_AS_TEMPLATE % sheet_id, sheet_id))),
    }
    return config


def build_screening(spec):
    """H1649 screening block: visa sheets have no upstream screening pass —
    every item here is already human-required, so it is reported as such
    (0 deterministic/lookup/agent, 100% human) rather than inventing a step
    that never ran.
    """
    return {
        "deterministic": 0,
        "lookup": 0,
        "agent": 0,
        "human": len(spec["items"]),
        "evidence_path": SPEC_EVIDENCE_TEMPLATE % spec["sheet_id"],
        "rules": [],
    }


def build_manifest(spec, repo_root=None):
    """V9 evidence-reuse manifest (csl-pyutil H1889 / v0.9.0+).

    Without ``manifest=``, ``render_review_sheet`` emits a PreflightWarning that
    becomes a hard error in csl-pyutil 1.0.0. The sheet's source of truth is the
    JSON spec (same path the screening block names); each card carries the
    title + question the human is asked to decide on as its evidence fields.

    ``repo_root`` defaults to this repo root so the prior-art walk stays scoped
    to SanskritGrammar (not the process CWD of a foreign caller).
    """
    sheet_id = spec["sheet_id"]
    row_ids = [raw["id"] for raw in spec["items"]]
    man = EvidenceManifest(
        sheet_id,
        row_ids,
        repo_root=str(repo_root if repo_root is not None else ROOT),
        min_evidence_fields=2,
    )
    man.declare_joined(
        SPEC_EVIDENCE_TEMPLATE % sheet_id,
        ["id", "title", "question", "panels"],
    )
    for raw in spec["items"]:
        man.add_card(raw["id"], ["title", "question"])
    return man


def render_visa_sheet(spec, repo_root=None):
    """Build items/config/screening/manifest and render. Single entry for CLI + tests."""
    return render_review_sheet(
        build_items(spec),
        build_config(spec),
        screening=build_screening(spec),
        manifest=build_manifest(spec, repo_root=repo_root),
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("spec", help="path to review/specs/<sheet_id>.json")
    ap.add_argument("--out-dir", default=None,
                    help="write the sheet here instead of review/ "
                         "(use for fidelity proofs; never overwrite a voted sheet)")
    args = ap.parse_args()

    spec = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    html_doc = render_visa_sheet(spec)

    out_dir = Path(args.out_dir) if args.out_dir else ROOT / "review"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / ("%s_review.html" % spec["sheet_id"])
    out.write_text(html_doc, encoding="utf-8")
    print("wrote %s (%d items, %d bytes)" % (out, len(spec["items"]), len(html_doc)))


if __name__ == "__main__":
    main()
