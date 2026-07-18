#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SG-SE-009 — Voice: active, middle, passive (semantics).

Reproduces the voice census for the Sangram corpus-grammar article SG-SE-009
against the pinned DCS snapshot (contract C3).

Method / honesty (see index.mdx § 7):
  * The traditional three-way voice system maps onto DCS only PARTIALLY.
  * PASSIVE (karmaṇi) is the only voice that is a native per-token tag:
    `feat_voice='Pass'`. It is overwhelmingly a present-system phenomenon
    (the -ya- passive stem).
  * ACTIVE vs MIDDLE (parasmaipada vs ātmanepada, P./Ā.) is NOT tagged per
    token — `feat_voice` is one of only {NULL, 'Pass'}, and `xpos` is NULL for
    every verb. The P/Ā distinction survives only as a LEXICAL property of the
    root, recoverable from `lemma.grammar` (e.g. '1.P.' / '1.Ā.' / '1.P.,1.Ā.').
    So one can classify ROOTS by pada, but cannot count middle-voice TOKENS.

Output: sangram/articles/voice/data/coverage_summary.json
Re-running against the same pin reproduces every figure to the token.

Model: Opus 4.8 (claude-opus-4-8[1m]), 18-07-2026. Data probe+verify workflow.
"""
import sqlite3
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

DB = r"C:/Users/user/Documents/GitHub/VisualDCS/src/DCS-data-2026/dcs_full.sqlite"
PIN = "04e0778d3dc971030229179e25eea043d06ff397"

ROOT_PADA = re.compile(r"\d+\s*\.\s*(P|Ā)\.")
HAS_P = re.compile(r"\d+\s*\.\s*P\.")
HAS_A = re.compile(r"\d+\s*\.\s*Ā\.")


def dist(cur, sql, params=()):
    return {(r[0] if r[0] is not None else "None"): r[1] for r in cur.execute(sql, params)}


def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # --- Passive: the only native per-token voice ---
    cur.execute("SELECT COUNT(*) FROM token WHERE upos='VERB'")
    verb_tokens = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM token WHERE upos='VERB' AND feat_voice='Pass'")
    passive_tokens = cur.fetchone()[0]
    passive_pct = round(100.0 * passive_tokens / verb_tokens, 2)

    voice_values = dist(cur, "SELECT feat_voice, COUNT(*) FROM token GROUP BY feat_voice")
    pass_by_tense = dist(
        cur, "SELECT feat_tense, COUNT(*) FROM token WHERE feat_voice='Pass' "
             "GROUP BY feat_tense ORDER BY 2 DESC")
    pass_by_verbform = dist(
        cur, "SELECT feat_verbform, COUNT(*) FROM token WHERE feat_voice='Pass' "
             "GROUP BY feat_verbform ORDER BY 2 DESC")
    top_pass_lemmas = dist(
        cur, "SELECT lemma, COUNT(*) FROM token WHERE feat_voice='Pass' AND lemma IS NOT NULL "
             "GROUP BY lemma ORDER BY 2 DESC LIMIT 12")

    # --- Active/middle: lexical only, from lemma.grammar ---
    p_only = a_only = both = 0
    for (g,) in cur.execute("SELECT grammar FROM lemma WHERE grammar IS NOT NULL AND grammar<>''"):
        if not ROOT_PADA.search(g):
            continue
        hp, ha = bool(HAS_P.search(g)), bool(HAS_A.search(g))
        if hp and ha:
            both += 1
        elif hp:
            p_only += 1
        elif ha:
            a_only += 1
    roots = p_only + a_only + both

    # xpos never carries pada
    xpos_vals = dist(cur, "SELECT xpos, COUNT(*) FROM token WHERE upos='VERB' GROUP BY xpos")

    print("verb tokens (upos=VERB): %d" % verb_tokens)
    print("passive (feat_voice=Pass): %d (%.2f%%)" % (passive_tokens, passive_pct))
    print("  feat_voice value set: %s" % ", ".join("%s:%d" % (k, v) for k, v in voice_values.items()))
    print("  passive by tense: %s" % ", ".join("%s:%d" % (k, v) for k, v in pass_by_tense.items()))
    print("  passive by verbform: %s" % ", ".join("%s:%d" % (k, v) for k, v in pass_by_verbform.items()))
    print("root pada (from lemma.grammar): %d classified" % roots)
    print("  parasmaipada-only P.: %d (%.1f%%)" % (p_only, 100.0 * p_only / roots))
    print("  atmanepada-only  Ā.: %d (%.1f%%)" % (a_only, 100.0 * a_only / roots))
    print("  ubhayapada P.,Ā.:    %d (%.1f%%)" % (both, 100.0 * both / roots))
    print("  xpos on verbs: %s (NULL => no per-token pada)" % ", ".join(
        "%s:%d" % (k, v) for k, v in xpos_vals.items()))

    out = {
        "article": "SG-SE-009",
        "pin": PIN,
        "verb_tokens": verb_tokens,
        "passive_tokens": passive_tokens,
        "passive_pct": passive_pct,
        "feat_voice_values": voice_values,
        "passive_by_tense": pass_by_tense,
        "passive_by_verbform": pass_by_verbform,
        "top_passive_lemmas": top_pass_lemmas,
        "root_pada": {
            "roots_classified": roots,
            "parasmaipada_only": p_only,
            "atmanepada_only": a_only,
            "ubhayapada": both,
        },
        "xpos_on_verbs": xpos_vals,
        "notes": (
            "Passive is the only native per-token voice (feat_voice in {NULL, Pass}); "
            "active/middle (P/Ā) is a lexical root property from lemma.grammar, not a "
            "token frequency; xpos is NULL for every verb so per-token pada is unrecoverable."
        ),
    }
    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.abspath(os.path.join(here, "..", "sangram", "articles", "voice", "data"))
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, "coverage_summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("\nwrote %s" % path)
    con.close()


if __name__ == "__main__":
    main()
