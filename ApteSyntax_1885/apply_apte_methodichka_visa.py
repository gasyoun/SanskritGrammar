#!/usr/bin/env python
"""apply_apte_methodichka_visa.py — fold an MG viza decisions.json into the Apte
print methodichka (METODICHKA_APTE_KOMMENTARII_2026.md).

The reviewer votes on the 9-card sheet
`review/sanskritgrammar-metodichka-apte-v1_17.07.26_review.html`, downloads
`..._decisions.json`, and this script writes the verdict into the manuscript so the
print draft carries the author's sign-off state:

  approve  -> the section is marked print-ready: `_✅ Виза MG (DATE): одобрено._`
             (+ `_Правка визы: <note>_` if the card carried a free-text tweak).
  reject   -> a prominent flag for a human rewrite (NOT auto-deleted — rewriting
             prose needs judgment): `> ⚠️ **Виза MG: снять/переписать.** <note>`
  defer    -> held out of the print draft: `> ⏸️ **Виза MG: отложено.** <note>`
  (unvoted / null) -> `_⏳ Виза: не голосовано._` so nothing silently passes.

Plus a `## Статус визы автора` summary table at the top. The marker goes right
under each section heading; re-running REPLACES prior markers (idempotent), so the
script is safe to run again after a re-vote. It never deletes section prose — the
only content it removes is its own previously-injected markers.

No HTML is emitted (the repo's .md files are HTML-free by policy); all markers are
plain Markdown (`_italics_` lines and `>` blockquotes). The viza date is taken from
the decisions.json `generated` field.

Usage:
  python ApteSyntax_1885/apply_apte_methodichka_visa.py <decisions.json>            # dry-run (default)
  python ApteSyntax_1885/apply_apte_methodichka_visa.py <decisions.json> --apply    # write the manuscript
  python ApteSyntax_1885/apply_apte_methodichka_visa.py --self-test
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_MS = HERE / "METODICHKA_APTE_KOMMENTARII_2026.md"
EXPECTED_SHEET = "sanskritgrammar-metodichka-apte-v1_17.07.26"

# card id -> heading-text prefix (matched after the leading "## ")
CARD_HEADING = [
    ("razdel-1-frame", "Как читать этот раздел"),
    ("zan-03",         "Занятие 3 "),
    ("zan-07",         "Занятие 7 "),
    ("zan-09",         "Занятие 9 "),
    ("zan-10",         "Занятие 10 "),
    ("zan-19",         "Занятие 19 "),
    ("zan-22",         "Занятие 22 "),
    ("zan-29",         "Занятия 29"),
    ("prilozhenie",    "Приложение"),
]
CARD_LABEL = {
    "razdel-1-frame": "Рамка + тезис", "zan-03": "Занятие 3", "zan-07": "Занятие 7",
    "zan-09": "Занятие 9", "zan-10": "Занятие 10", "zan-19": "Занятие 19",
    "zan-22": "Занятие 22", "zan-29": "Занятия 29–30", "prilozhenie": "Приложение",
}
SUMMARY_HEADING = "## Статус визы автора"
# any line this script previously injected (stripped before re-inserting)
MARKER_RE = re.compile(r"^(_[✅⏳]\s*Виза|_Правка визы:|>\s*[⚠⏸]️?\s*\*\*Виза)")
VERDICT_BADGE = {"approve": "✅ одобрено", "reject": "⚠️ снять/переписать",
                 "defer": "⏸️ отложено", None: "⏳ не голосовано"}


def load_decisions(path):
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    if d.get("sheet_id") != EXPECTED_SHEET:
        raise SystemExit(f"sheet_id mismatch: got {d.get('sheet_id')!r}, expected {EXPECTED_SHEET!r}")
    by_id = {it["id"]: it for it in d.get("items", [])}
    known = {cid for cid, _ in CARD_HEADING}
    missing = known - set(by_id)
    extra = set(by_id) - known
    return d, by_id, sorted(missing), sorted(extra)


def card_for_heading(heading_text):
    for cid, prefix in CARD_HEADING:
        if heading_text.startswith(prefix):
            return cid
    return None


def marker_lines(verdict, note, date):
    note = (note or "").strip()
    if verdict == "approve":
        out = [f"_✅ Виза MG ({date}): одобрено._"]
        if note:
            out.append(f"_Правка визы: {note}_")
        return out
    if verdict == "reject":
        return [f"> ⚠️ **Виза MG: снять/переписать.** {note}".rstrip()]
    if verdict == "defer":
        return [f"> ⏸️ **Виза MG: отложено.** {note}".rstrip()]
    return ["_⏳ Виза: не голосовано._"]


def strip_existing_markers(body_lines):
    """Drop leading blank + prior marker lines at the top of a section body."""
    i = 0
    while i < len(body_lines) and (not body_lines[i].strip() or MARKER_RE.match(body_lines[i])):
        i += 1
    return body_lines[i:]


def split_sections(lines):
    """-> (preamble_lines, [(heading_line, [body_lines]), ...]). A section runs from
    a '## ' heading up to the next '## ' heading or EOF."""
    heads = [i for i, ln in enumerate(lines) if ln.startswith("## ")]
    if not heads:
        return lines, []
    preamble = lines[:heads[0]]
    sections = []
    for j, h in enumerate(heads):
        end = heads[j + 1] if j + 1 < len(heads) else len(lines)
        sections.append((lines[h], lines[h + 1:end]))
    return preamble, sections


def build_summary(by_id, date):
    rows = [SUMMARY_HEADING, "",
            f"_Виза автора применена {date} · лист `{EXPECTED_SHEET}`._", "",
            "| Раздел | Вердикт | Правка визы |", "|---|---|---|"]
    for cid, _ in CARD_HEADING:
        it = by_id.get(cid, {})
        verdict = it.get("decision")
        note = (it.get("note") or "").replace("|", "\\|").strip() or "—"
        rows.append(f"| {CARD_LABEL[cid]} | {VERDICT_BADGE.get(verdict, verdict)} | {note} |")
    rows.append("")
    return rows


def apply(text, by_id, date):
    lines = text.split("\n")
    preamble, sections = split_sections(lines)
    # drop any prior summary section from the preamble/sections set
    sections = [(h, b) for (h, b) in sections if not h.startswith(SUMMARY_HEADING)]

    changed = []
    new_sections = []
    for heading, body in sections:
        heading_text = heading[3:].strip()
        cid = card_for_heading(heading_text)
        body = strip_existing_markers(body)
        if cid:
            it = by_id.get(cid, {})
            markers = marker_lines(it.get("decision"), it.get("note"), date)
            body = markers + [""] + body
            changed.append((cid, it.get("decision")))
        new_sections.append((heading, body))

    out = list(preamble)
    while out and out[-1].strip() == "":   # normalize trailing blanks -> exactly one
        out.pop()
    out.append("")
    out += build_summary(by_id, date)
    for heading, body in new_sections:
        out.append(heading)
        out += body
    return "\n".join(out), changed


def self_test():
    ms = ("# Title\n\n_intro_\n\n---\n\n"
          "## Как читать этот раздел\n\ntext-a\n\n---\n\n"
          "## Занятие 3 — foo\n\ntext-b\n\n"
          "## Приложение — bar\n\ntext-c\n\n_Dr. Mārcis Gasūns_\n")
    dec = {"sheet_id": EXPECTED_SHEET, "generated": "17-07-2026", "items": [
        {"id": "razdel-1-frame", "decision": "approve", "note": ""},
        {"id": "zan-03", "decision": "reject", "note": "переписать пример"},
        {"id": "prilozhenie", "decision": None, "note": ""},
    ]}
    by_id = {it["id"]: it for it in dec["items"]}
    out1, changed = apply(ms, by_id, "17-07-2026")
    assert "## Статус визы автора" in out1, out1
    assert "_✅ Виза MG (17-07-2026): одобрено._" in out1
    assert "> ⚠️ **Виза MG: снять/переписать.** переписать пример" in out1
    assert "_⏳ Виза: не голосовано._" in out1
    assert "text-a" in out1 and "text-b" in out1 and "text-c" in out1  # prose preserved
    # idempotency: applying to the already-applied output reproduces it
    out2, _ = apply(out1, by_id, "17-07-2026")
    assert out2 == out1, "not idempotent"
    # prose is never dropped and markers don't accumulate
    assert out1.count("_✅ Виза MG") == 1 and out2.count("_✅ Виза MG") == 1
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("decisions", nargs="?", help="path to ..._decisions.json")
    ap.add_argument("--manuscript", default=str(DEFAULT_MS))
    ap.add_argument("--apply", action="store_true", help="write the manuscript (default: dry-run)")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        print("self-test:", "PASS" if self_test() else "FAIL")
        return
    self_test()  # always guard before touching a real file
    if not args.decisions:
        ap.error("decisions.json path required (or use --self-test)")

    d, by_id, missing, extra = load_decisions(args.decisions)
    date = d.get("generated", "—")
    ms_path = Path(args.manuscript)
    text = ms_path.read_text(encoding="utf-8")
    out, changed = apply(text, by_id, date)

    counts = {}
    for _, v in changed:
        counts[v] = counts.get(v, 0) + 1
    print(f"decisions: {args.decisions}  (generated {date})")
    print("verdict counts:", {VERDICT_BADGE.get(k, k): n for k, n in counts.items()})
    if missing:
        print("  ⚠️ cards with NO vote in decisions.json (left as 'не голосовано'):", ", ".join(missing))
    if extra:
        print("  ⚠️ decisions.json has ids not in the sheet (ignored):", ", ".join(extra))
    if args.apply:
        ms_path.write_text(out, encoding="utf-8")
        print(f"-> WROTE {ms_path} (visa status folded in; re-runnable)")
        print("   next: update the .meta.md revision history + CHANGELOG, then ship via PR.")
    else:
        print(f"-> DRY-RUN (no write). Re-run with --apply to update {ms_path.name}.")
        rejects = [cid for cid, v in changed if v == "reject"]
        defers = [cid for cid, v in changed if v == "defer"]
        if rejects:
            print("   reject (need human rewrite):", ", ".join(rejects))
        if defers:
            print("   defer (held from print):", ", ".join(defers))


if __name__ == "__main__":
    main()
