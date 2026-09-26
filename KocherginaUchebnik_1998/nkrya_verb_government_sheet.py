#!/usr/bin/env python3
"""Review sheet for the NKRYa verb-government lint of the Кочергина методичка keys (H5400).

Reads nkrya_government/verb_government_lint.tsv (written by nkrya_verb_government_lint.py)
and nkrya_government/hint_proposals.tsv (the agent's modern hint per flagged frame, its
own NKRYa numbers measured by the same lint), and cuts one sheet of at most 10 cards.

Grill 23-09-2026 Q3: the key's wording stays. Approve = add the modern hint beside the
key's wording (in brackets); Reject = leave the key exactly as it is. Nothing is applied
here — an approved hint is folded into METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md by
/decisions-apply after the vote.

Screening: `soft_rare` alone is a note (the H5285 Q4 rule, carried over); flagged rows
with no hint proposal are counted in the report, not carded.

  python KocherginaUchebnik_1998/nkrya_verb_government_sheet.py --out review/<id>_review.html
"""

import argparse
import csv
import html
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
DIR = HERE / "nkrya_government"
LINT = DIR / "verb_government_lint.tsv"
PROPOSALS = DIR / "hint_proposals.tsv"
BLOB = "https://github.com/gasyoun/SanskritGrammar/blob/main/"
REL = "KocherginaUchebnik_1998/nkrya_government/"
SOURCE = "KocherginaUchebnik_1998/METODICHKA_KOCHERGINA_V1_UPRAZHNENIIA_2026.md"
REPORT = "KocherginaUchebnik_1998/NKRYA_VERB_GOVERNMENT_KOCHERGINA_KEYS_REPORT_24-09-2026.md"
SHEET_ID = "sanskritgrammar-kochergina-keys-verb-government_24-09-2026"
MAX_CARDS = 10
VERIFIER = "Claude Code Opus 5.5 (claude-opus-5-5)"
DATE = "24-09-2026"
CARDED = {"no_modern", "rare_modern", "c19_leaning"}
FLAG_RU = {"no_modern": "после 1950 г. не встречается", "rare_modern": "после 1950 г. редко",
           "c19_leaning": "тяготеет к XIX веку", "soft_rare": "малая доля употреблений глагола",
           "ok": "в норме", "pending": "не измерено"}
CASE_RU = {"gen": "род. п.", "dat": "дат. п.", "acc": "вин. п.", "ins": "твор. п.",
           "loc": "предл. п."}


def read_tsv(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def frame_ru(frame):
    verb, _, rest = frame.partition(" + ")
    parts = rest.split()
    case = CASE_RU.get(parts[-1], parts[-1])
    return "%s + %s%s" % (verb, (" ".join(parts[:-1]) + " + ") if len(parts) > 1 else "", case)


def pct(x):
    return "—" if x in ("", None) else ("%.2f %%" % (100 * float(x))).replace(".", ",")


def screen(rows, proposals):
    counts = {"total": len(rows), "ok": 0, "note_only": 0, "carded": 0, "no_proposal": 0,
              "pending": 0}
    cand = []
    for r in rows:
        fl = set(r["flags"].split(","))
        if "pending" in fl:
            counts["pending"] += 1
        elif fl & CARDED:
            if r["pair_id"] in proposals:
                cand.append(r)
            else:
                counts["no_proposal"] += 1
        elif "soft_rare" in fl:
            counts["note_only"] += 1
        else:
            counts["ok"] += 1
    counts["carded"] = len(cand)
    return counts, cand


def card(r, prop):
    from csl_pyutil import mark_cyrillic
    e = html.escape
    fl = [f for f in r["flags"].split(",") if f]
    c19 = ("в XIX веке: %s совпадений, %s употреблений глагола (%s)"
           % (r["frame_c19"], r["verb_c19"], pct(r["share_c19"]))) if r["frame_c19"] else \
        "XIX век не запрашивался (современных примеров достаточно)"
    q = ("<p><b>Что это?</b> Ключ <b>%s</b> методички к Кочергиной (раздел II). В ключе: %s</p>"
         "<p><b>Что проверено?</b> Управление глагола: %s. В Национальном корпусе русского "
         "языка после 1950 года такое сочетание встречается %s раз на %s употреблений глагола "
         "(%s); %s.</p>"
         "<p><b>Что изменится?</b> Если «да»: формулировка ключа остаётся, рядом в скобках "
         "появляется современная подсказка — %s. Если «нет»: ключ остаётся как есть.</p>"
         "<p>✓ добавить подсказку · ✕ оставить как есть · ⏸ позже</p>") % (
        e(r["pair_id"].split("|")[0]), mark_cyrillic("«%s»" % e(r["sentence"])),
        mark_cyrillic(e(frame_ru(r["frame"]))), e(r["frame_modern"]), e(r["verb_modern"]),
        pct(r["share_modern"]), e(c19), mark_cyrillic("«%s»" % e(prop["hint"])))
    ev = ("<p>НКРЯ (ruscorpora.ru API, основной корпус, lex-gramm, %s). Запрос: глагол "
          "<code>%s</code>%s, зависимое в том же направлении, что в ключе, на расстоянии "
          "1–3 слов. Современный срез 1950–2026: <b>%s</b> совпадений / %s употреблений "
          "глагола. %s.</p><p>Пример из корпуса: %s</p>"
          "<p>Подсказка: %s. Её числа: %s.</p>"
          "<p>Числа: <a href=\"%s%sevidence_cache.tsv\">evidence_cache.tsv</a>; строка линта: "
          "<a href=\"%s%sverb_government_lint.tsv\">verb_government_lint.tsv</a>. "
          "Позиция агента: %s.</p>") % (
        DATE, e(r["verb"]), e(" + " + r["frame"].split(" + ", 1)[1]),
        e(r["frame_modern"]), e(r["verb_modern"]), e(c19.capitalize()),
        mark_cyrillic(e(r["example_modern"] or "нет")), mark_cyrillic(e(prop["hint"])),
        e(prop["evidence"]), BLOB, REL, BLOB, REL, e(prop["stance"]))
    src = "<p>Источник: <a href=\"%s%s\">%s</a> · отметки линта: %s</p>" % (
        BLOB, SOURCE, e(SOURCE), e(", ".join(FLAG_RU.get(f, f) for f in fl)))
    cid = "gov-" + r["pair_id"].replace("|", "-").replace("-", "_")
    item = {"id": cid, "filt": "keys",
            "title": "%s: %s — добавить подсказку «%s»?" % (
                r["pair_id"].split("|")[0], frame_ru(r["frame"]), prop["hint"]),
            "title_href": BLOB + REL + "verb_government_lint.tsv",
            "badges": [FLAG_RU.get(f, f) for f in fl],
            "question": q, "panels": [("Evidence", ev), ("Строка", src)],
            "note_placeholder": "своя подсказка, если предложенная не годится"}
    stamp = {"verifier": VERIFIER, "method": "corpus_number",
             "sources": ["ruscorpora.ru API /lex-gramm/concordance",
                         REL + "evidence_cache.tsv", REL + "hint_proposals.tsv"],
             "verified_date": DATE}
    return item, stamp


def build(out):
    from csl_pyutil import render_review_sheet
    from csl_pyutil.evidence import EvidenceManifest
    rows = read_tsv(LINT)
    proposals = {p["pair_id"]: p for p in read_tsv(PROPOSALS)}
    counts, cand = screen(rows, proposals)
    cand.sort(key=lambda r: (int(r["frame_modern"] or 0), r["pair_id"]))
    items, stamps = [], {}
    for r in cand[:MAX_CARDS]:
        it, st = card(r, proposals[r["pair_id"]])
        items.append(it)
        stamps[it["id"]] = st
    if not items:
        return {"cards": 0, "screening": counts, "out": None}
    manifest = EvidenceManifest(SHEET_ID, [it["id"] for it in items], repo_root=str(REPO))
    manifest.declare_joined(REL + "verb_government_lint.tsv",
                            ["frame", "frame_modern", "verb_modern", "flags"])
    manifest.declare_joined(REL + "evidence_cache.tsv", ["hits", "docs", "example"])
    manifest.declare_joined(REL + "hint_proposals.tsv", ["hint", "evidence", "stance"])
    for it in items:
        manifest.add_card(it["id"], ["nkrya_frame_modern", "nkrya_hint_modern"])
    overflow = max(0, len(cand) - MAX_CARDS)
    config = {
        "sheet_id": SHEET_ID,
        "title": "Ключи к Кочергиной: редкое управление глаголов — добавить подсказку?",
        "subtitle": ("%d карточек. Сочетания «глагол + предлог + падеж» из ключей методички, "
                     "которые в НКРЯ после 1950 года редки. Формулировка ключа не меняется — "
                     "решается только, добавить ли рядом современную подсказку.%s") % (
            len(items), (" Ещё %d — в следующем листе." % overflow) if overflow else ""),
        "footer": "H5400 · nkrya_verb_government_lint.py · " + VERIFIER,
        "approve_label": "Добавить", "reject_label": "Оставить",
        "filters": [("keys", "Ключи, раздел II")],
        "generated": DATE,
        "show_ids": True, "note_min_height_px": 88,
        "identity_gate": {"patterns": [r"\bH\d{3,5}\b"], "labels": {}},
        "save_as": "SanskritGrammar/review/%s_decisions.json" % SHEET_ID,
        "preflight": {"allow_slp1_tokens": ("soft_rare", "rare_modern", "no_modern",
                                            "c19_leaning")},
    }
    screening = {**counts, "evidence_path": BLOB + REPORT,
                 "rules": ["no_modern / rare_modern / c19_leaning + a hint -> card",
                           "soft_rare only -> note (H5285 grill Q4)",
                           "flagged without a hint -> report only"]}
    page = render_review_sheet(items, config, screening=screening, manifest=manifest)
    page = page.replace("</body>", "<!-- ssb-evidence: %s -->\n</body>" %
                        json.dumps(stamps, ensure_ascii=False))
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(page, encoding="utf-8")
    return {"cards": len(items), "candidates": len(cand), "screening": counts, "out": str(out)}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default=str(REPO / "review" / (SHEET_ID + "_review.html")))
    a = ap.parse_args(argv)
    print(json.dumps(build(a.out), ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
