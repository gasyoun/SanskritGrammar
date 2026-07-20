#!/usr/bin/env python3
"""Adjudicate Scherzl's 1 168 case-government relations against the DCS treebank.

Input
-----
1. government_lexicon.jsonl        (this folder) — 763 root/stem rows, 1 168 governed-case
                                    relations, page-anchored to Scherzl.
2. dcs_gov_aggregate.json          — verb-lemma -> governed-case aggregate built by
                                    aggregate_dcs_gov.py from the DCS CoNLL-U treebank
                                    (sibling repo dcs-conllu, 15 900 files / 5.69 M tokens).

Method
------
Each Scherzl relation is (root R, reading-stem S, case C). We resolve the DCS verb lemma(s)
by EXACT match on {S, R} against DCS VERB lemmas (the principled key: Scherzl catalogues the
bare/attested root's government; prefixed forms are separate lemmas with their own frames).
For the matched lemma(s) we read two evidence tiers from the treebank:

  * dep_gov[C]  — a case-C nominal is a DIRECT dependency child of the verb (HEAD==verb).
                  Strong government evidence. Only ~3.9 % of DCS sentences carry arcs, so
                  a dep-count of 0 is NOT disconfirming on its own.
  * cooc[C]     — a case-C nominal co-occurs in the same sentence as the verb (all sentences).
                  Weak: for high-frequency verbs nearly every case co-occurs, so co-occurrence
                  is only *discriminating when it is zero*.

Verdict tiers (raw counts kept in the JSONL so the thresholds are auditable):
  CONFIRMED     dep_gov[C] >= 1                      — treebank shows this exact government arc
  COOCCURRENCE  dep_gov[C] == 0 and cooc[C] >= 1     — case attested with the verb, no parsed arc
  UNATTESTED    dep_gov[C] == 0 and cooc[C] == 0     — verb present in DCS, this case never pairs
                 (flag high_freq if verb_freq >= 100 — then the absence is genuinely notable)
  ABSENT        no bare-verb lemma for R/S in DCS    — cannot adjudicate from the treebank

Outputs (this folder):
  government_vs_dcs_adjudication.jsonl   one line per relation (1 168) + verdict + evidence
  dcs_verb_government_profiles.json      DCS-attested valency frame for each matched verb
  GOVERNMENT_VS_DCS_ADJUDICATION.md      human report (verdict distribution + notable cases)
"""
import sys, io, json, os
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "government_lexicon.jsonl")
# aggregate lives in scratchpad during the build; override with env DCS_AGG
AGG = os.environ.get("DCS_AGG", os.path.join(HERE, "dcs_gov_aggregate.json"))

OUT_JSONL = os.path.join(HERE, "government_vs_dcs_adjudication.jsonl")
OUT_PROFILES = os.path.join(HERE, "dcs_verb_government_profiles.json")
OUT_MD = os.path.join(HERE, "GOVERNMENT_VS_DCS_ADJUDICATION.md")

CASE_MAP = {"nom": "Nom", "acc": "Acc", "instr": "Ins", "dat": "Dat",
            "abl": "Abl", "gen": "Gen", "loc": "Loc"}
HIGH_FREQ = 100  # verb_freq at/above which a zero-co-occurrence is "notable"

def match_lemma(key, dcs_verbs):
    """Resolve a Scherzl root/stem string to a DCS verb lemma, exact then a light
    orthographic normalisation. Scherzl writes anusvāra as ṁ (U+1E41) where DCS uses
    ṃ (U+1E43); normalising recovers 11 genuinely distinct prefixed verbs (saṃdhā,
    praśaṃs, saṃyuj, śaṃs …) that would otherwise mis-fall-back to their bare root."""
    if not key:
        return None
    if key in dcs_verbs:
        return key
    v = key.replace("ṁ", "ṃ")
    if v != key and v in dcs_verbs:
        return v
    return None

def main():
    rows = [json.loads(l) for l in io.open(LEX, encoding="utf-8") if l.strip()]
    agg = json.load(io.open(AGG, encoding="utf-8"))
    verb_freq = agg["verb_freq"]
    verb_parsed = agg["verb_parsed"]
    dep_gov = agg["dep_gov"]
    dep_deprel = agg["dep_deprel"]
    cooc = agg["cooc"]
    dcs_verbs = set(verb_freq)
    meta = agg["meta"]

    records = []
    matched_lemmas = set()
    for r in rows:
        root = r["root"]
        for rd in r.get("readings", []):
            stem = rd.get("stem")
            cls = rd.get("class")
            voice = rd.get("voice")
            for rel in rd.get("relations", []):
                c = rel.get("case")
                cu = CASE_MAP.get(c)
                # Resolve to the MOST SPECIFIC DCS verb lemma: the reading's stem IS the
                # verb the relation is about (e.g. prefixed `vidhā`), so match it exactly
                # and only fall back to the bare root when the stem form is not a DCS
                # lemma. Never sum stem+root — that would credit a prefixed reading with
                # the bare root's government and inflate the counts.
                cand = []
                m = match_lemma(stem, dcs_verbs) or match_lemma(root, dcs_verbs)
                if m:
                    cand = [m]
                matched_lemmas.update(cand)
                dep = sum(dep_gov.get(m, {}).get(cu, 0) for m in cand) if cu else 0
                co = sum(cooc.get(m, {}).get(cu, 0) for m in cand) if cu else 0
                freq = sum(verb_freq.get(m, 0) for m in cand)
                parsed = sum(verb_parsed.get(m, 0) for m in cand)
                if not cand:
                    verdict = "ABSENT"
                elif dep >= 1:
                    verdict = "CONFIRMED"
                elif co >= 1:
                    verdict = "COOCCURRENCE"
                else:
                    verdict = "UNATTESTED"
                rec = {
                    "root": root, "stem": stem, "class": cls, "voice": voice,
                    "scherzl_case": c, "ud_case": cu, "subtype": rel.get("subtype"),
                    "pages": rel.get("pages"), "example_only": rel.get("example_only", False),
                    "hidden": rel.get("hidden", False),
                    "replaceable_by": rel.get("replaceable_by"),
                    "dcs_lemmas": cand,
                    "dep_gov_count": dep, "cooc_count": co,
                    "verb_freq": freq, "verb_parsed_freq": parsed,
                    "verdict": verdict,
                    "high_freq": bool(verdict == "UNATTESTED" and freq >= HIGH_FREQ),
                }
                records.append(rec)

    with io.open(OUT_JSONL, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # DCS-attested valency frame per matched verb (governed-case profile, dep-level)
    profiles = {}
    for m in sorted(matched_lemmas):
        profiles[m] = {
            "verb_freq": verb_freq.get(m, 0),
            "verb_parsed_freq": verb_parsed.get(m, 0),
            "dep_gov": dict(sorted(dep_gov.get(m, {}).items(), key=lambda x: -x[1])),
            "dep_deprel": dict(sorted(dep_deprel.get(m, {}).items(), key=lambda x: -x[1])),
        }
    with io.open(OUT_PROFILES, "w", encoding="utf-8") as fh:
        json.dump(profiles, fh, ensure_ascii=False, indent=0)

    write_report(records, meta, matched_lemmas, dep_deprel)
    print(f"relations adjudicated: {len(records)}")
    vc = Counter(r["verdict"] for r in records)
    for v in ("CONFIRMED", "COOCCURRENCE", "UNATTESTED", "ABSENT"):
        print(f"  {v:13} {vc[v]:5}  ({100*vc[v]/len(records):.1f}%)")
    print(f"matched DCS verb lemmas: {len(matched_lemmas)}")

def write_report(records, meta, matched_lemmas, dep_deprel):
    n = len(records)
    vc = Counter(r["verdict"] for r in records)
    # per-case verdict breakdown
    per_case = defaultdict(Counter)
    for r in records:
        per_case[r["ud_case"]][r["verdict"]] += 1
    # notable unattested: high-freq verb, Scherzl-claimed case never co-occurs
    notable = [r for r in records if r["high_freq"]]
    notable.sort(key=lambda x: -x["verb_freq"])
    # strongest confirmations
    confirmed = [r for r in records if r["verdict"] == "CONFIRMED"]
    confirmed.sort(key=lambda x: -x["dep_gov_count"])

    L = []
    A = L.append
    A("# Scherzl government relations vs the DCS treebank — adjudication\n")
    A("_Created: 20-07-2026 · Last updated: 20-07-2026_\n")
    A("Auto-generated by `adjudicate_government_vs_dcs.py` (Opus 4.8 `claude-opus-4-8`, "
      "handoff [H1372](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1372-Opus_SanskritGrammar_scherzl-government-relations-vs-dcs-treebank-adjudication_20.07.26.md)). "
      "Regenerate: rebuild `dcs_gov_aggregate.json` with `aggregate_dcs_gov.py` over the "
      "[dcs-conllu](https://github.com/gasyoun/dcs-conllu) treebank, then run this script.\n")
    A("## What this is\n")
    A("Every one of Scherzl's **1 168 case-government relations** "
      "([government_lexicon.jsonl](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/government_class_index/government_lexicon.jsonl)) "
      "checked, root by root, against the DCS dependency treebank "
      f"({meta['n_files']:,} CoNLL-U files, {meta['n_tok']:,} tokens, "
      f"{meta['n_sent']:,} sentences of which **{meta['n_sent_parsed']:,} "
      f"({100*meta['n_sent_parsed']/meta['n_sent']:.1f} %) carry dependency arcs**).\n")
    A("> **Read the tiers correctly.** Only ~3.9 % of DCS sentences are dependency-parsed, so a "
      "**CONFIRMED** (a real government arc was found) is strong positive evidence, but a low or "
      "zero dep-count is *not* disconfirming by itself. Co-occurrence fills the gap but is only "
      "discriminating when it is **zero**: a frequent verb co-occurs with nearly every case, so "
      "**UNATTESTED at high verb frequency** is the meaningful negative signal — Scherzl claims a "
      "government the corpus never pairs with that verb.\n")

    A("## Verdict distribution\n")
    A("| Verdict | Relations | % | Meaning |")
    A("|---|---:|---:|---|")
    meanings = {
        "CONFIRMED": "direct government arc found in the treebank",
        "COOCCURRENCE": "case co-occurs with the verb; no parsed arc (consistent, weaker)",
        "UNATTESTED": "verb present in DCS but this case never pairs with it",
        "ABSENT": "no bare-verb lemma for the root/stem in DCS — not adjudicable",
    }
    for v in ("CONFIRMED", "COOCCURRENCE", "UNATTESTED", "ABSENT"):
        A(f"| {v} | {vc[v]:,} | {100*vc[v]/n:.1f} % | {meanings[v]} |")
    A(f"| **Total** | **{n:,}** | 100 % | |")
    adjudicable = n - vc["ABSENT"]
    A(f"\nOf the **{adjudicable:,}** relations whose root occurs as a bare verb in DCS "
      f"(**{vc['ABSENT']:,}** are not), **{vc['CONFIRMED']:,}** "
      f"({100*vc['CONFIRMED']/adjudicable:.1f} %) are directly confirmed by a government arc and "
      f"**{vc['CONFIRMED']+vc['COOCCURRENCE']:,}** "
      f"({100*(vc['CONFIRMED']+vc['COOCCURRENCE'])/adjudicable:.1f} %) find at least co-occurrence "
      "support.\n")
    A("> **On the ABSENT bucket — don't read it as \"Scherzl is wrong\".** ABSENT means only that "
      "Scherzl's root/stem *string* is not a DCS verb lemma. The dominant cause is a **lemma-form "
      "mismatch**, not a missing verb: Scherzl often lists the guṇa/attested stem while DCS keys the "
      "bare root — e.g. Scherzl `sarj` vs DCS `sṛj`, so √sṛj's government lands in ABSENT (and its "
      "handful of matched relations show a spurious low-frequency `sarj` lemma). Closing that gap "
      "needs a stem→root normaliser (guṇa/vṛddhi/sandhi undo) and is left as a follow-up; the "
      "CONFIRMED rate above is therefore a *lower* bound on Scherzl's corpus support.\n")

    A("## By case\n")
    A("| Case | Relations | CONFIRMED | COOCCURRENCE | UNATTESTED | ABSENT |")
    A("|---|---:|---:|---:|---:|---:|")
    order = ["Acc", "Ins", "Abl", "Dat", "Gen", "Loc", "Nom"]
    for c in order:
        pc = per_case.get(c, Counter())
        tot = sum(pc.values())
        A(f"| {c} | {tot} | {pc['CONFIRMED']} | {pc['COOCCURRENCE']} | "
          f"{pc['UNATTESTED']} | {pc['ABSENT']} |")

    A(f"\n## Notable UNATTESTED — Scherzl claims a case a common verb never governs "
      f"(verb_freq ≥ {HIGH_FREQ})\n")
    A("These are the relations most worth a human's eye: the root is well attested in DCS "
      "(hundreds–thousands of occurrences) yet the Scherzl-claimed case never once co-occurs with "
      "it. Either a genuine Scherzl over-reach / page mis-read, a case Scherzl records only from a "
      "rare construction outside the DCS corpus, or a lemma-identity mismatch worth checking.\n")
    if notable:
        A("| root | stem | case | subtype | verb_freq | pages | example_only |")
        A("|---|---|---|---|---:|---|:--:|")
        for r in notable[:40]:
            st = "·" if r["example_only"] else ""
            pg = ",".join(str(p) for p in (r["pages"] or []))
            A(f"| {r['root']} | {r['stem']} | {r['scherzl_case']} | {r['subtype'] or ''} | "
              f"{r['verb_freq']:,} | {pg} | {st} |")
        if len(notable) > 40:
            A(f"\n_…and {len(notable)-40} more; full list in the JSONL "
              "(`verdict==UNATTESTED && high_freq`)._")
    else:
        A("_None._")

    A("\n## Strongest confirmations — most-attested government arcs\n")
    A("| root | stem | case | dep arcs | verb_freq | top deprels on that verb (all cases) |")
    A("|---|---|---|---:|---:|---|")
    seen = set()
    shown = 0
    for r in confirmed:
        key = (r["stem"] or r["root"], r["ud_case"])
        if key in seen:
            continue
        seen.add(key)
        lem = (r["dcs_lemmas"] or [None])[0]
        drl = dep_deprel.get(lem, {})
        top3 = ", ".join(f"{k}·{v}" for k, v in
                         sorted(drl.items(), key=lambda x: -x[1])[:3])
        A(f"| {r['root']} | {r['stem']} | {r['scherzl_case']} | {r['dep_gov_count']} | "
          f"{r['verb_freq']:,} | {top3} |")
        shown += 1
        if shown >= 30:
            break

    A("\n## Files\n")
    A("| File | What |")
    A("|---|---|")
    A("| `government_vs_dcs_adjudication.jsonl` | one line per relation (1 168): verdict + "
      "`dep_gov_count` / `cooc_count` / `verb_freq` / `verb_parsed_freq` evidence |")
    A("| `dcs_verb_government_profiles.json` | for each matched DCS verb: its treebank-attested "
      "governed-case profile (`dep_gov`) and deprel distribution — the corpus valency frame to "
      "compare against Scherzl's |")
    A("| `adjudicate_government_vs_dcs.py` | this builder |")
    A("| `aggregate_dcs_gov.py` | one-pass DCS CoNLL-U → verb-government aggregate (upstream input) |")

    with io.open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("wrote", OUT_MD)
    if notable:
        print(f"notable high-freq UNATTESTED: {len(notable)}")

if __name__ == "__main__":
    main()
