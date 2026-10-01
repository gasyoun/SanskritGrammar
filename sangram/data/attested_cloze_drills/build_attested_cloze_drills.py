#!/usr/bin/env python3
"""Attested-sentence cloze drills — generic RQ2 auto-drill generation, cloze type.

RQ2 ("Can we auto-generate valid, answer-keyed drills (sandhi-split, cloze,
paradigm-fill) from attested corpus?") names three drill shapes. Two already
shipped as Wave 2 additions: sandhi-split (``scripts/build_emeneo_sandhi_drills.py``)
and paradigm-fill for nominal declension (``sangram/data/attested_drills/``, W2-add-a).
This builder ships the third: **cloze** -- blank one word out of an attested DCS
sentence and ask the learner to supply it.

The "verified answer key" for a cloze item needs no generation step to agree or
disagree with: the answer IS the corpus attestation itself (the blanked token's
own ``form``), so there is nothing to verify against except the corpus that
produced the question in the first place. This is a *stronger* verification
guarantee than the declension drill's generated-vs-attested comparison, not a
weaker one -- there is no "mismatch" case because the question and the answer
come from the same sentence.

Pipeline (all deterministic, no model in the loop):

  1. select sentences of readable length (4-12 tokens) from the pinned DCS
     snapshot, up to ``--scan-limit`` candidates (default 150 000, a fraction
     of the 651 322 sentences in that length band -- plenty for --limit final
     items after filtering);
  2. per sentence, walk tokens in word order and pick the FIRST eligible
     target: a NOUN with (case, number) both tagged, or a FINITE verb
     (feat_verbform IS NULL) with (tense, mood, person, number) all tagged;
  3. compute each target lemma's corpus-wide token frequency (a self-contained
     substitute for kosha's core_rank -- this builder depends on nothing but
     the pinned DCS snapshot) and drop targets below ``--min-lemma-freq``: a
     hapax target teaches nothing and rarely yields a distractor pool;
  4. cap to at most ``--max-per-lemma`` sentences per lemma (topic variety,
     same discipline as the declension drill's per-stem-class quota) and take
     the top ``--limit`` items by lemma frequency;
  5. for the final item set only, look up up to 3 DISTRACTOR forms per target
     -- other attested (cell, m_unsandhied) pairs of the SAME lemma, i.e.
     other corpus-real forms that are wrong for this slot, never invented ones.

**Past-tense transparency (CLAUDE.md trap, H3966):** DCS tags Aorist/Perfect
indicative under one ``feat_tense='Past'`` value; the split lives in
``feat_formation`` (a formation code, or NULL for the untagged Perfect
default). This builder never folds that into a bucket -- every VERB item
carries its raw ``tense`` and ``formation`` columns unmodified, so a Perfect
default is visibly a default, never silently presented as if it were
independently tagged.

**feat_voice discipline (VisualDCS gen_paradigm_attested.py precedent):** DCS
only distinguishes Passive from non-passive, never Parasmaipada from
Atmanepada. Voice is emitted as ``NonPass``/``Pass`` -- never ``Act`` -- so no
item claims a P./A. split the corpus cannot support.

Stdlib-only (csv/json/sqlite3/argparse). Read-only on every input. Regenerate:

    python sangram/data/attested_cloze_drills/build_attested_cloze_drills.py

Outputs (all under this directory):
    attested_cloze_items.tsv        the drill corpus (one row per cloze item)
    coverage_by_type.json           per-upos/per-cell instrumentation, machine-readable
    COVERAGE_REPORT.md              the human-readable report -- computed, never hand-edited
    ../../../src/components/talmud/attestedClozeData.js   widget payload (stratified subset)

Corpus numbers are DCS (Oliver Hellwig) via the pinned VisualDCS snapshot; attribute
accordingly wherever they surface.
"""
import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
GITHUB = ROOT.parent
OUT_DIR = ROOT / "sangram" / "data" / "attested_cloze_drills"

DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
DEFAULT_WIDGET_DATA = ROOT / "src" / "components" / "talmud" / "attestedClozeData.js"

NOUN_CASES = {"Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc", "Voc"}
NUMBERS = {"Sing", "Dual", "Plur"}

MIN_TOKENS = 4
MAX_TOKENS = 12

# The widget ships a stratified subset: up to this many items per target upos,
# so the payload is not 90% NOUN cloze because nouns outnumber finite verbs in
# the eligible pool.
WIDGET_ITEMS_PER_UPOS = 150


def voice_label(feat_voice):
    """DCS only distinguishes Passive from non-passive (never P./A.) -- never emit 'Act'."""
    return "Pass" if feat_voice == "Pass" else "NonPass"


def noun_cell(feat_case, feat_number):
    if feat_case in NOUN_CASES and feat_number in NUMBERS:
        return f"{feat_case}.{feat_number}"
    return None


def verb_cell(feat_tense, feat_mood, feat_person, feat_number, feat_voice):
    if feat_tense and feat_mood and feat_person and feat_number in NUMBERS:
        return f"{feat_tense}.{feat_mood}.{feat_person}.{feat_number}.{voice_label(feat_voice)}"
    return None


def pick_target(tokens):
    """First eligible NOUN or finite VERB token, walking word order. tokens are
    dicts sorted by idx. Returns the token dict (with a `cell` key added) or None.
    """
    for tok in tokens:
        if tok["upos"] == "NOUN":
            cell = noun_cell(tok["feat_case"], tok["feat_number"])
            if cell:
                return {**tok, "cell": cell}
        elif tok["upos"] == "VERB" and tok["feat_verbform"] is None:
            cell = verb_cell(tok["feat_tense"], tok["feat_mood"], tok["feat_person"],
                              tok["feat_number"], tok["feat_voice"])
            if cell:
                return {**tok, "cell": cell}
    return None


def build_cloze_text(tokens, target_idx):
    return " ".join("___" if t["idx"] == target_idx else t["form"] for t in tokens)


def build_full_text(tokens):
    return " ".join(t["form"] for t in tokens)


def scan_candidates(conn, scan_limit):
    """Sentence ids with token count in [MIN_TOKENS, MAX_TOKENS], plus every
    token of each, fetched in exactly two queries (candidate scan, then a
    temp-table join) -- never one query per sentence.
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT sentence_id FROM token GROUP BY sentence_id "
        "HAVING COUNT(*) BETWEEN ? AND ? LIMIT ?",
        (MIN_TOKENS, MAX_TOKENS, scan_limit),
    )
    sentence_ids = [r[0] for r in cur.fetchall()]
    print(f"candidate sentences (length {MIN_TOKENS}-{MAX_TOKENS}): {len(sentence_ids)}",
          file=sys.stderr)

    cur.execute("CREATE TEMP TABLE want_sent(sentence_id INTEGER PRIMARY KEY)")
    cur.executemany("INSERT OR IGNORE INTO want_sent VALUES (?)", ((i,) for i in sentence_ids))
    cur.execute(
        "SELECT t.sentence_id, t.idx, t.form, t.lemma, t.lemma_id, t.upos, "
        "t.feat_case, t.feat_number, t.feat_tense, t.feat_mood, t.feat_voice, "
        "t.feat_person, t.feat_verbform, t.feat_formation, t.m_unsandhied "
        "FROM token t JOIN want_sent w ON w.sentence_id = t.sentence_id "
        "ORDER BY t.sentence_id, t.idx"
    )
    by_sentence = defaultdict(list)
    for row in cur.fetchall():
        (sentence_id, idx, form, lemma, lemma_id, upos, feat_case, feat_number,
         feat_tense, feat_mood, feat_voice, feat_person, feat_verbform, feat_formation,
         m_unsandhied) = row
        by_sentence[sentence_id].append({
            "idx": idx, "form": form, "lemma": lemma, "lemma_id": lemma_id, "upos": upos,
            "feat_case": feat_case, "feat_number": feat_number, "feat_tense": feat_tense,
            "feat_mood": feat_mood, "feat_voice": feat_voice, "feat_person": feat_person,
            "feat_verbform": feat_verbform, "feat_formation": feat_formation,
            "m_unsandhied": m_unsandhied,
        })
    print(f"tokens fetched: {sum(len(v) for v in by_sentence.values())}", file=sys.stderr)
    return by_sentence


def read_sentence_meta(conn, sentence_ids):
    """sentence_id -> (sent_id citation string, chapter_id)."""
    cur = conn.cursor()
    cur.execute("CREATE TEMP TABLE want_meta(id INTEGER PRIMARY KEY)")
    cur.executemany("INSERT OR IGNORE INTO want_meta VALUES (?)", ((i,) for i in sentence_ids))
    cur.execute(
        "SELECT s.id, s.sent_id, s.chapter_id FROM sentence s "
        "JOIN want_meta w ON w.id = s.id"
    )
    return {row[0]: (row[1] or "", row[2]) for row in cur.fetchall()}


def lemma_frequency(conn, lemma_ids):
    """lemma_id -> corpus-wide token count, any upos. Self-contained substitute
    for kosha core_rank -- this builder has no cross-repo dependency but VisualDCS.
    """
    cur = conn.cursor()
    cur.execute("CREATE TEMP TABLE want_lemma(lemma_id INTEGER PRIMARY KEY)")
    cur.executemany("INSERT OR IGNORE INTO want_lemma VALUES (?)", ((i,) for i in lemma_ids))
    cur.execute(
        "SELECT t.lemma_id, COUNT(*) FROM token t JOIN want_lemma w ON w.lemma_id = t.lemma_id "
        "GROUP BY t.lemma_id"
    )
    return dict(cur.fetchall())


def fetch_distractors(conn, lemma_id, upos, own_cell, own_form, max_forms):
    """Up to `max_forms` other attested (cell, m_unsandhied) forms of the same
    lemma+upos, excluding the target's own cell -- other corpus-real forms
    that are wrong for THIS slot, never an invented form.

    Also excludes any form textually EQUAL to the target's own answer: a
    different cell can share a surface form through syncretism (neuter
    Nom.Sing = Acc.Sing is the common case, e.g. ``karma``) -- a distractor
    identical to the correct answer would make the item unanswerable, so
    excluding by cell alone is not enough.
    """
    cur = conn.cursor()
    if upos == "NOUN":
        cur.execute(
            "SELECT feat_case, feat_number, m_unsandhied, COUNT(*) n FROM token "
            "WHERE lemma_id = ? AND upos = 'NOUN' AND feat_case IS NOT NULL "
            "AND feat_number IS NOT NULL AND m_unsandhied IS NOT NULL "
            "GROUP BY feat_case, feat_number, m_unsandhied ORDER BY n DESC",
            (lemma_id,),
        )
        rows = [(noun_cell(c, n), f, cnt) for c, n, f, cnt in cur.fetchall()]
    else:
        cur.execute(
            "SELECT feat_tense, feat_mood, feat_person, feat_number, feat_voice, "
            "m_unsandhied, COUNT(*) n FROM token "
            "WHERE lemma_id = ? AND upos = 'VERB' AND feat_verbform IS NULL "
            "AND feat_tense IS NOT NULL AND feat_mood IS NOT NULL "
            "AND feat_person IS NOT NULL AND feat_number IS NOT NULL "
            "AND m_unsandhied IS NOT NULL "
            "GROUP BY feat_tense, feat_mood, feat_person, feat_number, feat_voice, m_unsandhied "
            "ORDER BY n DESC",
            (lemma_id,),
        )
        rows = [(verb_cell(t, m, p, num, v), f, cnt) for t, m, p, num, v, f, cnt in cur.fetchall()]

    out, seen_forms = [], {own_form}
    for cell, form, _cnt in rows:
        if cell is None or cell == own_cell or form in seen_forms:
            continue
        seen_forms.add(form)
        out.append(form)
        if len(out) >= max_forms:
            break
    return out


def build(args):
    conn = sqlite3.connect(f"file:{args.db}?mode=ro", uri=True)
    try:
        by_sentence = scan_candidates(conn, args.scan_limit)

        raw_items = []
        for sentence_id, tokens in by_sentence.items():
            tokens_sorted = sorted(tokens, key=lambda t: t["idx"])
            target = pick_target(tokens_sorted)
            if target is None:
                continue
            raw_items.append({
                "sentence_id": sentence_id,
                "tokens": tokens_sorted,
                "target_idx": target["idx"],
                "lemma_id": target["lemma_id"],
                "lemma": target["lemma"],
                "upos": target["upos"],
                "cell": target["cell"],
                "formation": (target["feat_formation"] or "") if target["upos"] == "VERB" else "",
                "form": target["form"],
                "unsandhied": target["m_unsandhied"] or "",
            })
        print(f"sentences with an eligible target: {len(raw_items)}", file=sys.stderr)

        lemma_ids = {it["lemma_id"] for it in raw_items}
        freq = lemma_frequency(conn, lemma_ids)
        for it in raw_items:
            it["corpus_freq"] = freq.get(it["lemma_id"], 0)

        raw_items = [it for it in raw_items if it["corpus_freq"] >= args.min_lemma_freq]
        print(f"after min-lemma-freq >= {args.min_lemma_freq}: {len(raw_items)}", file=sys.stderr)

        raw_items.sort(key=lambda it: (-it["corpus_freq"], it["sentence_id"]))

        selected, per_lemma = [], defaultdict(int)
        for it in raw_items:
            if per_lemma[it["lemma_id"]] >= args.max_per_lemma:
                continue
            per_lemma[it["lemma_id"]] += 1
            selected.append(it)
            if len(selected) >= args.limit:
                break
        print(f"selected (limit {args.limit}, max {args.max_per_lemma}/lemma): {len(selected)}",
              file=sys.stderr)

        meta = read_sentence_meta(conn, [it["sentence_id"] for it in selected])

        distractor_cache = {}
        items = []
        for it in selected:
            key = (it["lemma_id"], it["upos"], it["cell"], it["unsandhied"])
            if key not in distractor_cache:
                distractor_cache[key] = fetch_distractors(
                    conn, it["lemma_id"], it["upos"], it["cell"], it["unsandhied"],
                    args.max_distractors)
            distractors = distractor_cache[key]
            sent_id, chapter_id = meta.get(it["sentence_id"], ("", None))
            items.append({
                "sentence_id": it["sentence_id"],
                "sent_id": sent_id,
                "chapter_id": chapter_id if chapter_id is not None else "",
                "n_tokens": len(it["tokens"]),
                "target_idx": it["target_idx"],
                "lemma_id": it["lemma_id"],
                "lemma": it["lemma"],
                "upos": it["upos"],
                "cell": it["cell"],
                "formation": it["formation"],
                "form": it["form"],
                "unsandhied": it["unsandhied"],
                "corpus_freq": it["corpus_freq"],
                "sentence_cloze": build_cloze_text(it["tokens"], it["target_idx"]),
                "sentence_full": build_full_text(it["tokens"]),
                "distractor_forms": "|".join(distractors),
                "n_distractors": len(distractors),
                "drill_mode": "mcq" if len(distractors) >= 2 else "open",
            })
    finally:
        conn.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fields = ["sentence_id", "sent_id", "chapter_id", "n_tokens", "target_idx", "lemma_id",
              "lemma", "upos", "cell", "formation", "form", "unsandhied", "corpus_freq",
              "sentence_cloze", "sentence_full", "distractor_forms", "n_distractors", "drill_mode"]
    import csv
    with (OUT_DIR / "attested_cloze_items.tsv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(items)
    print(f"wrote attested_cloze_items.tsv: {len(items)} rows", file=sys.stderr)

    report = coverage_report(items)
    (OUT_DIR / "coverage_by_type.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT_DIR / "COVERAGE_REPORT.md").write_text(render_report(report), encoding="utf-8")
    print("wrote coverage_by_type.json + COVERAGE_REPORT.md", file=sys.stderr)

    write_widget_data(args.widget_data, items)
    print(f"wrote {args.widget_data.name}", file=sys.stderr)
    return report


def coverage_report(items):
    by_upos = defaultdict(lambda: {"items": 0, "mcq": 0, "open": 0})
    by_cell = defaultdict(int)
    lemmas = set()
    for it in items:
        b = by_upos[it["upos"]]
        b["items"] += 1
        b[it["drill_mode"]] += 1
        by_cell[it["cell"]] += 1
        lemmas.add(it["lemma_id"])

    return {
        "asset": "Attested-sentence cloze drills (RQ2 cloze type)",
        "method": ("candidate sentences of 4-12 tokens from the pinned DCS snapshot; "
                   "first eligible NOUN (case+number) or finite VERB (tense+mood+person+"
                   "number) target per sentence, walking word order; answer is the "
                   "token's own attested form -- no generation step, nothing to disagree "
                   "with; distractors are other attested forms of the same lemma in a "
                   "different cell"),
        "corpus_attribution": "DCS (Oliver Hellwig) via the pinned VisualDCS snapshot",
        "items": len(items),
        "distinct_lemmas": len(lemmas),
        "by_upos": dict(by_upos),
        "cells_ranked": dict(sorted(by_cell.items(), key=lambda kv: -kv[1])[:20]),
    }


def render_report(rep):
    lines = [
        "_Created: 25-09-2026 · Last updated: 25-09-2026_",
        "",
        "# Attested-sentence cloze drills — coverage report",
        "",
        "Generated by [`build_attested_cloze_drills.py`](build_attested_cloze_drills.py). "
        "Do not hand-edit — every number here is computed.",
        "",
        f"**{rep['items']} cloze items · {rep['distinct_lemmas']} distinct target lemmas.**",
        "",
        f"Corpus numbers: {rep['corpus_attribution']}.",
        "",
        "## By target part of speech",
        "",
        "| upos | items | MCQ (≥2 distractors) | open-answer |",
        "|---|---:|---:|---:|",
    ]
    for upos, b in rep["by_upos"].items():
        lines.append(f"| {upos} | {b['items']} | {b['mcq']} | {b['open']} |")

    lines += [
        "",
        "## Top 20 cells by item count",
        "",
        "| Cell | Items |",
        "|---|---:|",
    ]
    for cell, n in rep["cells_ranked"].items():
        lines.append(f"| `{cell}` | {n} |")
    lines += ["", "_Dr. Mārcis Gasūns_", ""]
    return "\n".join(lines)


def write_widget_data(path, items):
    """Stratified subset for the interactive widget -- up to WIDGET_ITEMS_PER_UPOS
    per target upos, so the payload does not lopsidedly favour whichever upos is
    more common in the eligible pool.
    """
    per_upos = defaultdict(int)
    out = []
    for it in items:
        if per_upos[it["upos"]] >= WIDGET_ITEMS_PER_UPOS:
            continue
        per_upos[it["upos"]] += 1
        out.append({
            "sentenceId": it["sentence_id"],
            "sentId": it["sent_id"],
            "lemma": it["lemma"],
            "upos": it["upos"],
            "cell": it["cell"],
            "cloze": it["sentence_cloze"],
            "full": it["sentence_full"],
            "answer": it["form"],
            "unsandhied": it["unsandhied"],
            "distractors": it["distractor_forms"].split("|") if it["distractor_forms"] else [],
            "mode": it["drill_mode"],
        })

    header = (
        "// GENERATED by sangram/data/attested_cloze_drills/build_attested_cloze_drills.py "
        "-- do not hand-edit.\n"
        "// Attested-sentence cloze drills (RQ2 cloze type): the answer is the corpus's "
        "own attested word, never a generated one.\n"
        "// Corpus: DCS (Oliver Hellwig) via the pinned VisualDCS snapshot.\n\n"
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        header + "export const ATTESTED_CLOZE_DRILLS = " +
        json.dumps(out, ensure_ascii=False, indent=1) + ";\n\n" +
        "export const CLOZE_DRILL_COUNT = ATTESTED_CLOZE_DRILLS.length;\n",
        encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--widget-data", type=Path, default=DEFAULT_WIDGET_DATA)
    ap.add_argument("--scan-limit", type=int, default=150_000,
                    help="candidate sentences to scan before filtering (default 150000)")
    ap.add_argument("--limit", type=int, default=3000, help="final drill item cap")
    ap.add_argument("--min-lemma-freq", type=int, default=10,
                    help="drop targets whose lemma occurs fewer times corpus-wide")
    ap.add_argument("--max-per-lemma", type=int, default=3,
                    help="cap sentences drawn from the same target lemma (topic variety)")
    ap.add_argument("--max-distractors", type=int, default=3)
    args = ap.parse_args()

    if not args.db.exists():
        sys.exit(f"FATAL: missing DCS database: {args.db}")

    build(args)


if __name__ == "__main__":
    main()
