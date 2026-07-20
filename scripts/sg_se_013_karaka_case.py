#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SG-SE-013 — Kāraka ↔ case: two (three) models over one evidence set.

Reproduces the kāraka→case cross-tabulation for the Sangram corpus-grammar
article SG-SE-013 against the pinned DCS snapshot (contract C3).

Method / honesty (see index.mdx § 7):
  * DCS has NO kāraka annotation. The six Pāṇinian kārakas are OVERLAID onto the
    Universal-Dependencies `deprel` layer (a non-Pāṇinian, Western dependency
    model). The kāraka→deprel mapping below is a scholarly claim, not native data.
  * `deprel` is PARTIAL (~3.93 % of tokens). The whole overlay sees <4 % of corpus.
  * DCS uses NO `nsubj:pass`: active agent and passive patient are both `nsubj`,
    so the classic passive karman→Nom case-swap is not natively separable on the
    subject side (only the agent side, via `obl:agent`→Ins, is visible).

Output: sangram/articles/karaka-case/data/coverage_summary.json
Re-running against the same pin reproduces every figure to the token.

Model: Opus 4.8 (claude-opus-4-8[1m]), 18-07-2026. Data probe+verify workflow.
"""
import hashlib
import sqlite3
import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

DB = r"C:/Users/user/Documents/GitHub/VisualDCS/src/DCS-data-2026/dcs_full.sqlite"
PIN = "04e0778d3dc971030229179e25eea043d06ff397"


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()

# Kāraka (Pāṇini 1.4.23–55) overlaid on UD deprel proxies. NOT native kāraka tags.
KARAKA_MAP = [
    ("kartR (agent, active)",     ["nsubj", "csubj"]),
    ("kartR-passive (agent)",     ["obl:agent"]),
    ("karman (patient/object)",   ["obj"]),
    ("karaNa (instrument)",       ["obl:instr"]),
    ("sampradAna-recipient",      ["iobj"]),
    ("sampradAna-goal",           ["obl:goal"]),
    ("sampradAna-benef",          ["obl:benef"]),
    ("apAdAna (source)",          ["obl:source"]),
    ("adhikaraNa (locus)",        ["obl:loc"]),
]

CASE_ORDER = ["Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc", "Voc", "Cpd"]


def case_dist(cur, deprels):
    ph = ",".join("?" * len(deprels))
    q = (
        "SELECT feat_case, COUNT(*) c FROM token "
        "WHERE deprel IN (%s) AND feat_case IS NOT NULL AND feat_case<>'' "
        "GROUP BY feat_case" % ph
    )
    d = {r[0]: r[1] for r in cur.execute(q, deprels)}
    total = sum(d.values())
    return d, total


def main():
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr)
        return 1
    sha = sha256_file(DB)

    cur.execute("SELECT COUNT(*) FROM token")
    total_tokens = cur.fetchone()[0]
    # case-marked denominator family (SG-SE denominator contract, H1371) — same basis as
    # the sibling case sub-articles (SE-001/002/003/004): case_bearing incl the Cpd pseudo-case,
    # real_vibhakti = the eight true vibhakti excl Cpd.
    case_bearing = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case IS NOT NULL").fetchone()[0]
    real_vibhakti = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case IN "
        "('Nom','Acc','Ins','Dat','Abl','Gen','Loc','Voc')").fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM token WHERE deprel IS NOT NULL AND deprel<>''")
    deprel_nonnull = cur.fetchone()[0]
    coverage = round(100.0 * deprel_nonnull / total_tokens, 4)

    rows = []
    for karaka, deprels in KARAKA_MAP:
        d, total = case_dist(cur, deprels)
        if total:
            top_case = max(d, key=d.get)
            top_n = d[top_case]
            top_pct = round(100.0 * top_n / total, 2)
        else:
            top_case, top_n, top_pct = None, 0, 0.0
        ordered = {k: d[k] for k in CASE_ORDER if k in d}
        rows.append({
            "karaka": karaka,
            "deprels": ",".join(deprels),
            "case_tagged_total": total,
            "top_case": top_case,
            "top_case_n": top_n,
            "top_case_pct": top_pct,
            "full_dist": ordered,
        })
        print("%-26s %-12s -> %-4s %6d (%5.1f%%)  [n=%d]" % (
            karaka, ",".join(deprels), top_case, top_n, top_pct, total))

    # Native check for the passive-collapse honesty limit.
    cur.execute("SELECT COUNT(*) FROM token WHERE deprel='nsubj:pass'")
    nsubj_pass = cur.fetchone()[0]
    print("\nnsubj:pass rows (passive-subject deprel): %d  "
          "(0 => active agent and passive patient share `nsubj`)" % nsubj_pass)

    # Passive is massively attested on the verb side, but the karman->Nom swap
    # is only visible for the tiny slice of nsubj tokens whose head verb is
    # tagged Pass (predicate-side route through the 3.93% deprel layer).
    cur.execute("SELECT COUNT(*) FROM token WHERE feat_voice='Pass'")
    passive_verbs = cur.fetchone()[0]
    cur.execute(
        "SELECT s.feat_case, COUNT(*) c FROM token s "
        "JOIN token v ON v.sentence_id=s.sentence_id AND v.idx=s.head "
        "WHERE s.deprel='nsubj' AND v.feat_voice='Pass' "
        "GROUP BY s.feat_case"
    )
    passive_subj = {r[0] if r[0] else "None": r[1] for r in cur.fetchall()}
    passive_subj_total = sum(passive_subj.values())
    passive_subj_nom = passive_subj.get("Nom", 0)
    print("passive verbs (feat_voice=Pass): %d" % passive_verbs)
    print("nsubj of a passive-verb head: %d total, Nom %d (%.1f%%) -- the only "
          "native window on karman->Nom" % (
              passive_subj_total, passive_subj_nom,
              100.0 * passive_subj_nom / passive_subj_total if passive_subj_total else 0))

    out = {
        "article": "SG-SE-013",
        "pin": PIN,
        "snapshot": {
            "source_repo": prov.get("source_repo"),
            "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"),
            "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {
            "all_tokens": total_tokens,
            "case_bearing_tokens": case_bearing,
            "real_vibhakti_tokens": real_vibhakti,
        },
        "total_tokens": total_tokens,
        "deprel_nonnull": deprel_nonnull,
        "deprel_coverage_pct": coverage,
        "nsubj_pass_rows": nsubj_pass,
        "passive_verbs": passive_verbs,
        "passive_subject_case_dist": passive_subj,
        "passive_subject_total": passive_subj_total,
        "passive_subject_nom": passive_subj_nom,
        "karaka_case_crosstab": rows,
        "notes": (
            "Kāraka overlaid on UD deprel (no native kāraka tags). deprel partial "
            "(~3.93%%). nsubj:pass=%d: passive karman->Nom not natively separable "
            "on subject side; only predicate-side route (nsubj of a Pass verb) is "
            "visible = %d subjects, Nom %d, vs %d passive verbs total." % (
                nsubj_pass, passive_subj_total, passive_subj_nom, passive_verbs)
        ),
    }

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(here, "..", "sangram", "articles", "karaka-case", "data")
    outdir = os.path.abspath(outdir)
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "coverage_summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\nwrote %s" % path)

    con.close()


if __name__ == "__main__":
    main()
