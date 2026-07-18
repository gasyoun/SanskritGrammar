#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SG-SE-006 — Tense & aspect: the competition of the past tenses.

Reproduces the finite past-tense census for the Sangram corpus-grammar article
SG-SE-006 against the pinned DCS snapshot (contract C3).

Method / honesty (see index.mdx § 7):
  * feat_tense has NO 'Aor'/'Perf' value; the three classical pasts do NOT map
    cleanly onto it.
  * IMPERFECT is clean: feat_tense='Impf'.
  * AORIST lives in feat_tense='Past' + an aorist feat_formation
    (root/them/s/is/red/sa/sis); countable (cf. SG-MO-019).
  * PERFECT is corpus-dark: only the PERIPHRASTIC perfect is labeled
    (feat_tense='Past' + feat_formation='peri'). The SIMPLE (reduplicated)
    perfect has feat_formation NULL and no dedicated tag — it sits inside the
    large 'Past + None' bucket (dominated by uvāca/āha/cakāra…), inferable from
    reduplication but not natively countable.

Output: sangram/articles/past-tenses/data/coverage_summary.json
Re-running against the same pin reproduces every figure to the token.

Model: Opus 4.8 (claude-opus-4-8[1m]), 18-07-2026. Data probe+verify workflow.
"""
import sqlite3
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

DB = r"C:/Users/user/Documents/GitHub/VisualDCS/src/DCS-data-2026/dcs_full.sqlite"
PIN = "04e0778d3dc971030229179e25eea043d06ff397"

AORIST_FORMS = ("root", "them", "s", "is", "red", "sa", "sis")
FINITE = "upos='VERB' AND feat_verbform IS NULL"


def dist(cur, sql, params=()):
    return {(r[0] if r[0] is not None else "None"): r[1] for r in cur.execute(sql, params)}


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("SELECT COUNT(*) FROM token WHERE %s AND feat_tense IS NOT NULL AND feat_tense<>''" % FINITE)
    finite_with_tense = cur.fetchone()[0]

    tense = dist(cur, "SELECT feat_tense, COUNT(*) FROM token WHERE %s AND feat_tense IS NOT NULL AND feat_tense<>'' GROUP BY feat_tense ORDER BY 2 DESC" % FINITE)

    past_total = tense.get("Past", 0)
    impf = tense.get("Impf", 0)
    past_form = dist(cur, "SELECT feat_formation, COUNT(*) FROM token WHERE %s AND feat_tense='Past' GROUP BY feat_formation ORDER BY 2 DESC" % FINITE)

    ph = ",".join("?" * len(AORIST_FORMS))
    cur.execute("SELECT COUNT(*) FROM token WHERE %s AND feat_tense='Past' AND feat_formation IN (%s)" % (FINITE, ph), AORIST_FORMS)
    aorist = cur.fetchone()[0]
    peri = past_form.get("peri", 0)
    past_none = past_form.get("None", 0)

    # top reduplicated-perfect forms in Past+None
    perf_top = list(cur.execute(
        "SELECT form, lemma, COUNT(*) c FROM token WHERE %s AND feat_tense='Past' AND feat_formation IS NULL "
        "GROUP BY form ORDER BY c DESC LIMIT 12" % FINITE))

    print("finite verbs with tense: %d" % finite_with_tense)
    for k, v in tense.items():
        print("  %-6s %8d  %5.1f%%" % (k, v, 100.0 * v / finite_with_tense))
    print("--- Past bucket (%d) by formation ---" % past_total)
    for k, v in past_form.items():
        print("  %-8s %8d" % (k, v))
    print("classical pasts: imperfect %d (clean) | aorist %d (formation) | "
          "perfect: periphrastic %d (labeled) + simple ~%d (Past+None, UNTAGGED)"
          % (impf, aorist, peri, past_none))
    print("--- Past+None top forms (reduplicated perfects) ---")
    for form, lemma, c in perf_top[:8]:
        print("  %-14s (%-6s) %6d" % (form, lemma, c))

    out = {
        "article": "SG-SE-006",
        "pin": PIN,
        "finite_with_tense": finite_with_tense,
        "tense_dist": tense,
        "past_bucket_total": past_total,
        "past_by_formation": past_form,
        "imperfect": impf,
        "aorist_finite": aorist,
        "perfect_periphrastic": peri,
        "perfect_simple_untagged_bucket": past_none,
        "past_none_top_forms": [{"form": f, "lemma": l, "n": c} for f, l, c in perf_top],
        "notes": (
            "feat_tense has no Aor/Perf. Imperfect clean (Impf); aorist = Past + "
            "aorist feat_formation; perfect corpus-dark: only periphrastic (peri) "
            "labeled, simple/reduplicated perfect untagged inside Past+None "
            "(dominated by uvāca/āha 'said'). Simple perfect not natively countable."
        ),
    }
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.abspath(os.path.join(here, "..", "sangram", "articles", "past-tenses", "data"))
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "coverage_summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\nwrote %s" % path)
    con.close()


if __name__ == "__main__":
    main()
