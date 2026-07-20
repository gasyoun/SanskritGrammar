#!/usr/bin/env python3
"""Adjudicate Scherzl's 1 168 case-government relations against the DCS treebank.

Pre-registered evidence rules (fixed BEFORE inspecting outcomes — the honest-threshold
requirement of handoff H1372):

  Join.   Each relation (root R, reading-stem S, case C) resolves to its MOST SPECIFIC DCS
          verb lemma: exact match on S first (with anusvāra ṁ→ṃ normalisation, which recovers
          11 prefixed verbs like saṃdhā/praśaṃs/śaṃs), else exact match on R. Never stem+root
          summed — that would credit a prefixed reading with the bare root's frame.

  Two evidence layers, kept strictly separate:
    dep_gov[C]  a case-C nominal is a DIRECT dependency child of the verb (HEAD==verb). Strong
                government evidence, but only ~3.9 % of DCS sentences carry arcs.
    cooc[C]     # sentences where a case-C nominal co-occurs with the verb (all sentences).
                Compared against CHANCE — expected = verb_freq · baserate[C], where
                baserate[C] = (sentences containing case C) / (all sentences). cooc_ratio =
                observed / expected: >1 associated, <1 dispreferred.

  Verdict (every relation gets exactly one):
    CONFIRMED               dep_gov[C] >= 1.
    CONTRADICTED            dep_gov[C] == 0 AND the verb is well observed
                            (verb_parsed >= MIN_PARSED and dep_total >= MIN_DEPTOT — we can SEE
                            its government frame) AND case C is dispreferred in co-occurrence
                            (cooc_ratio < MAX_CONTRA_RATIO). The corpus positively shows a frame
                            that excludes C. Hand-checked below for homonym/preverb misjoins.
    UNATTESTED-INSUFFICIENT dep_gov[C] == 0 and not CONTRADICTED — either the verb is too thinly
                            parsed to judge, or C co-occurs at/above chance (weak positive) but no
                            arc confirms it. Cannot confirm or contradict.
    NOT-ADJUDICABLE         no bare-verb lemma for R/S in DCS (dominant cause: a lemma-form
                            mismatch such as Scherzl guṇa `sarj` vs DCS `sṛj`, not a missing verb).

  example_only relations (Scherzl gives one illustrative example, not a stated rule) and
  replaceable_by alternations are adjudicated identically; both flags are carried in the output
  so a reader can filter. `hidden` relations are carried too.

Inputs : government_lexicon.jsonl (this folder) + dcs_gov_aggregate.json (built by
         aggregate_dcs_gov.py over the dcs-conllu treebank — the CoNLL-U serialisation of the
         same DCS-2026 master as VisualDCS/.../dcs_full.sqlite; token count 5 688 416 and
         11 096 verb lemmas match the sqlite exactly).
Outputs: government_corpus_verdicts.tsv, government_vs_dcs_adjudication.jsonl,
         dcs_verb_government_profiles.json, SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md
"""
import sys, io, json, os
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
LEX = os.path.join(HERE, "government_lexicon.jsonl")
AGG = os.environ.get("DCS_AGG", os.path.join(HERE, "dcs_gov_aggregate.json"))

OUT_TSV = os.path.join(HERE, "government_corpus_verdicts.tsv")
OUT_JSONL = os.path.join(HERE, "government_vs_dcs_adjudication.jsonl")
OUT_PROFILES = os.path.join(HERE, "dcs_verb_government_profiles.json")
OUT_MD = os.path.join(HERE, "SCHERZL_GOVERNMENT_CORPUS_ADJUDICATION_2026.md")

CASE_MAP = {"nom": "Nom", "acc": "Acc", "instr": "Ins", "dat": "Dat",
            "abl": "Abl", "gen": "Gen", "loc": "Loc"}

# Pre-registered thresholds (see docstring). CONTRADICTED needs BOTH enough observed government
# to see the frame AND co-occurrence below half of chance — deliberately conservative so a sparse
# parse cannot manufacture a contradiction.
MIN_PARSED = 20        # verb must appear in >=20 dependency-parsed sentences
MIN_DEPTOT = 15        # verb must have >=15 observed direct case-dependents (frame is visible)
MAX_CONTRA_RATIO = 0.5 # case C co-occurs at < half its chance rate with this verb

# Hand-adjudication of the CONTRADICTED screening set (keyed by (root, scherzl_case)). Each note
# classifies the survivor as a genuine Scherzl DEFECT, a HOMONYM/PREVERB misjoin, or SYSTEM-VS-USAGE
# / marginal divergence — the human pass H1372 asks for. A CONTRADICTED relation with no note here
# is reported as UNREVIEWED so the report never silently claims a hand-check that did not happen.
HAND_ADJUDICATION = {
    ("arc", "abl"): (
        "system-vs-usage (marginal)",
        "√arc/ṛc 'praise, sing, shine'. Scherzl's ablative here is flagged **example_only** AND "
        "`replaceable_by: instr`, on p.223 (his ablative-with-preverbs section). The corpus shows "
        "arc governing Acc·14 / Dat·9 / **Ins·3** but zero ablative — i.e. it attests Scherzl's own "
        "noted *instrumental* alternant ('praise WITH [hymns]'), not the bare ablative. Correctly "
        "matched (no homonym/preverb misjoin) and no transcription error: a marginal example-only "
        "reading the corpus does not corroborate. **No erratum** — downgrade confidence on the "
        "bare-ablative frame and prefer the corpus-attested instrumental.",
    ),
}

def match_lemma(key, dcs_verbs):
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
    meta = agg["meta"]
    n_sent = meta["n_sent"]
    baserate = {c: agg["sent_with_case"].get(c, 0) / n_sent for c in CASE_MAP.values()}
    dcs_verbs = set(verb_freq)

    records = []
    matched_lemmas = set()
    for r in rows:
        root = r["root"]
        for rd in r.get("readings", []):
            stem = rd.get("stem")
            for rel in rd.get("relations", []):
                c = rel.get("case")
                cu = CASE_MAP.get(c)
                lem = match_lemma(stem, dcs_verbs) or match_lemma(root, dcs_verbs)
                if lem:
                    matched_lemmas.add(lem)
                dep = dep_gov.get(lem, {}).get(cu, 0) if lem else 0
                dep_total = sum(dep_gov.get(lem, {}).values()) if lem else 0
                co = cooc.get(lem, {}).get(cu, 0) if lem else 0
                freq = verb_freq.get(lem, 0) if lem else 0
                parsed = verb_parsed.get(lem, 0) if lem else 0
                expected = freq * baserate.get(cu, 0) if lem else 0.0
                ratio = (co / expected) if expected > 0 else None
                if not lem:
                    verdict = "NOT-ADJUDICABLE"
                elif dep >= 1:
                    verdict = "CONFIRMED"
                elif (parsed >= MIN_PARSED and dep_total >= MIN_DEPTOT
                      and ratio is not None and ratio < MAX_CONTRA_RATIO):
                    verdict = "CONTRADICTED"
                else:
                    verdict = "UNATTESTED-INSUFFICIENT"
                records.append({
                    "root": root, "stem": stem, "class": rd.get("class"),
                    "voice": rd.get("voice"),
                    "scherzl_case": c, "ud_case": cu, "subtype": rel.get("subtype"),
                    "pages": rel.get("pages"),
                    "example_only": rel.get("example_only", False),
                    "hidden": rel.get("hidden", False),
                    "replaceable_by": rel.get("replaceable_by"),
                    "dcs_lemma": lem,
                    "dep_gov_count": dep, "dep_total": dep_total,
                    "cooc_count": co, "cooc_expected": round(expected, 1),
                    "cooc_ratio": round(ratio, 3) if ratio is not None else None,
                    "verb_freq": freq, "verb_parsed_freq": parsed,
                    "verdict": verdict,
                })

    # JSONL
    with io.open(OUT_JSONL, "w", encoding="utf-8") as fh:
        for rec in records:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # TSV (spec deliverable)
    cols = ["root", "stem", "dcs_lemma", "scherzl_case", "ud_case", "subtype",
            "example_only", "pages", "verdict", "dep_gov_count", "dep_total",
            "cooc_count", "cooc_expected", "cooc_ratio", "verb_freq", "verb_parsed_freq"]
    with io.open(OUT_TSV, "w", encoding="utf-8") as fh:
        fh.write("\t".join(cols) + "\n")
        for rec in records:
            row = []
            for k in cols:
                v = rec.get(k)
                if k == "pages":
                    v = ",".join(str(p) for p in (v or []))
                row.append("" if v is None else str(v))
            fh.write("\t".join(row) + "\n")

    # per-verb corpus valency frame
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

    write_report(records, meta, matched_lemmas, baserate, dep_deprel)

    vc = Counter(r["verdict"] for r in records)
    print(f"relations: {len(records)}")
    for v in ("CONFIRMED", "CONTRADICTED", "UNATTESTED-INSUFFICIENT", "NOT-ADJUDICABLE"):
        print(f"  {v:24} {vc[v]:5}  ({100*vc[v]/len(records):.1f}%)")
    print(f"matched DCS verb lemmas: {len(matched_lemmas)}")

def write_report(records, meta, matched_lemmas, baserate, dep_deprel):
    n = len(records)
    vc = Counter(r["verdict"] for r in records)
    per_case = defaultdict(Counter)
    for r in records:
        per_case[r["ud_case"]][r["verdict"]] += 1
    contra = [r for r in records if r["verdict"] == "CONTRADICTED"]
    contra.sort(key=lambda x: (x["cooc_ratio"] if x["cooc_ratio"] is not None else 9))
    confirmed = [r for r in records if r["verdict"] == "CONFIRMED"]
    confirmed.sort(key=lambda x: -x["dep_gov_count"])

    parsed_pct = 100 * meta["n_sent_parsed"] / meta["n_sent"]
    adjudicable = n - vc["NOT-ADJUDICABLE"]

    L = []
    A = L.append
    A("# Scherzl's case-government catalogue vs the DCS treebank — corpus adjudication (2026)\n")
    A("_Created: 20-07-2026 · Last updated: 20-07-2026_\n")
    A("Auto-generated by `adjudicate_government_vs_dcs.py` (Opus 4.8 `claude-opus-4-8`, handoff "
      "[H1372](https://github.com/gasyoun/Uprava/blob/main/handoffs/H1372-Opus_SanskritGrammar_scherzl-government-relations-vs-dcs-treebank-adjudication_20.07.26.md)).\n")

    A("## Headline: the adjudicability ceiling\n")
    A(f"The DCS treebank is **{meta['n_sent']:,} sentences / {meta['n_tok']:,} tokens**, but only "
      f"**{meta['n_sent_parsed']:,} sentences ({parsed_pct:.1f} %) carry dependency arcs**. Direct "
      "government evidence therefore exists for only ~4 % of the corpus, and this — not the "
      "confirmation rate — is the honest headline: **a zero dep-count can never, by itself, "
      "disconfirm a Scherzl relation.** Every verdict below is built to respect that ceiling. Of "
      f"Scherzl's **1 168 relations**, **{adjudicable:,}** have a bare-verb lemma in DCS at all "
      f"(**{vc['NOT-ADJUDICABLE']:,}** do not — see the lemma-form caveat), and only those are "
      "adjudicable.\n")

    A("## Verdicts\n")
    A("| Verdict | Relations | % of all | % of adjudicable |")
    A("|---|---:|---:|---:|")
    for v in ("CONFIRMED", "CONTRADICTED", "UNATTESTED-INSUFFICIENT", "NOT-ADJUDICABLE"):
        adj = f"{100*vc[v]/adjudicable:.1f} %" if v != "NOT-ADJUDICABLE" else "—"
        A(f"| {v} | {vc[v]:,} | {100*vc[v]/n:.1f} % | {adj} |")
    A(f"| **Total** | **{n:,}** | 100 % | |")
    is_are = "is" if vc["CONTRADICTED"] == 1 else "are"
    A(f"\n**{vc['CONFIRMED']:,} of {adjudicable:,} adjudicable relations "
      f"({100*vc['CONFIRMED']/adjudicable:.1f} %) are confirmed by a direct government arc; only "
      f"{vc['CONTRADICTED']} {is_are} contradicted** — and even that survives to a hand pass below, "
      "not an automatic verdict. Scherzl's 19th-century catalogue holds up against the modern "
      "corpus to the extent the corpus can test it.\n")

    A("### How the tiers are drawn (pre-registered, not fitted)\n")
    A("- **CONFIRMED** — a case-marked nominal is a direct dependency child of the verb.\n")
    A(f"- **CONTRADICTED** — the verb is well enough parsed to *see* its frame "
      f"(≥{MIN_PARSED} parsed occurrences, ≥{MIN_DEPTOT} observed case-dependents), the "
      "Scherzl case appears in **zero** of those arcs, **and** it co-occurs with the verb at "
      f"less than **half its chance rate** (cooc_ratio < {MAX_CONTRA_RATIO}; chance = "
      "verb_freq · corpus-base-rate of the case). Both gates are required so a sparse parse "
      "cannot manufacture a contradiction — a case that co-occurs heavily (e.g. jñā + genitive) "
      "is *never* called contradicted just because the parser missed the arc.\n")
    A("- **UNATTESTED-INSUFFICIENT** — no arc, and either the verb is too thinly parsed to judge "
      "or the case co-occurs at/above chance (weak positive) with no arc to confirm it.\n")
    A("- **NOT-ADJUDICABLE** — the root/stem string is not a DCS verb lemma.\n")
    A("\nCorpus base rate of each case (share of sentences containing it), used for the chance "
      "expectation: " + " · ".join(f"{c} {100*baserate[c]:.0f}%" for c in
      ["Acc", "Ins", "Abl", "Dat", "Gen", "Loc", "Nom"]) + ".\n")

    A("## By case\n")
    A("| Case | Relations | CONFIRMED | CONTRADICTED | UNATT-INSUF | NOT-ADJ |")
    A("|---|---:|---:|---:|---:|---:|")
    for c in ["Acc", "Ins", "Abl", "Dat", "Gen", "Loc", "Nom"]:
        pc = per_case.get(c, Counter())
        A(f"| {c} | {sum(pc.values())} | {pc['CONFIRMED']} | {pc['CONTRADICTED']} | "
          f"{pc['UNATTESTED-INSUFFICIENT']} | {pc['NOT-ADJUDICABLE']} |")

    rel_word = "relation" if len(contra) == 1 else "relations"
    A(f"\n## The {len(contra)} CONTRADICTED {rel_word} (candidate{'' if len(contra)==1 else 's'} "
      "— hand-adjudicated below)\n")
    A("Verb well-observed, Scherzl's case absent from every government arc, and dispreferred in "
      "co-occurrence. Ranked by co-occurrence ratio (lowest = strongest signal). `cooc_ratio` is "
      "observed ÷ chance co-occurrence.\n")
    A("| root | stem | DCS lemma | case | dep_total | cooc/exp | ratio | verb_freq | pages |")
    A("|---|---|---|---|---:|---|---:|---:|---|")
    for r in contra:
        pg = ",".join(str(p) for p in (r["pages"] or []))
        A(f"| {r['root']} | {r['stem']} | {r['dcs_lemma']} | {r['scherzl_case']} | "
          f"{r['dep_total']} | {r['cooc_count']}/{r['cooc_expected']:.0f} | "
          f"{r['cooc_ratio']} | {r['verb_freq']:,} | {pg} |")
    # Hand-adjudication of the CONTRADICTED set
    A("\n## Hand-adjudication of the CONTRADICTED set\n")
    reviewed = [r for r in contra if (r["root"], r["scherzl_case"]) in HAND_ADJUDICATION]
    defects = [r for r in reviewed
               if HAND_ADJUDICATION[(r["root"], r["scherzl_case"])][0].startswith("DEFECT")]
    A(f"Every screening survivor is hand-checked below. **{len(defects)} genuine Scherzl "
      f"defect(s)** found → **{len(defects)} erratum/errata routed** to "
      "[`errata.yml`](https://github.com/gasyoun/SanskritGrammar/blob/main/BuhlerLeitfaden_1923/errata.yml). "
      "The rest are homonym/preverb misjoins or system-vs-usage divergence and are **not** errata.\n")
    for r in contra:
        key = (r["root"], r["scherzl_case"])
        if key in HAND_ADJUDICATION:
            cls, note = HAND_ADJUDICATION[key]
            A(f"- **{r['root']} ({r['scherzl_case']}, p.{','.join(str(p) for p in (r['pages'] or []))}) "
              f"— {cls}.** {note}\n")
        else:
            A(f"- **{r['root']} ({r['scherzl_case']}) — UNREVIEWED.** No hand note on file; "
              "treat as a screening candidate only.\n")

    A("## Strongest confirmations\n")
    A("| root | stem | case | dep arcs | verb_freq | top deprels (verb, all cases) |")
    A("|---|---|---|---:|---:|---|")
    seen = set(); shown = 0
    for r in confirmed:
        key = (r["dcs_lemma"], r["ud_case"])
        if key in seen:
            continue
        seen.add(key)
        drl = dep_deprel.get(r["dcs_lemma"], {})
        top3 = ", ".join(f"{k}·{v}" for k, v in sorted(drl.items(), key=lambda x: -x[1])[:3])
        A(f"| {r['root']} | {r['stem']} | {r['scherzl_case']} | {r['dep_gov_count']} | "
          f"{r['verb_freq']:,} | {top3} |")
        shown += 1
        if shown >= 25:
            break

    A("\n## Files\n")
    A("| File | What |")
    A("|---|---|")
    A("| `government_corpus_verdicts.tsv` | one row per relation (1 168): verdict + evidence, spreadsheet-friendly |")
    A("| `government_vs_dcs_adjudication.jsonl` | same, richer (class/voice/subtype/replaceable_by/expected/ratio) |")
    A("| `dcs_verb_government_profiles.json` | per matched verb: DCS-attested governed-case frame + deprel distribution |")
    A("| `adjudicate_government_vs_dcs.py` · `aggregate_dcs_gov.py` | reproducible builders over the [dcs-conllu](https://github.com/gasyoun/dcs-conllu) treebank |")

    A("\n## Limitations\n")
    A("- **NOT-ADJUDICABLE is not \"Scherzl is wrong\".** It is dominated by lemma-form mismatches "
      "— Scherzl lists the guṇa/attested stem (`sarj`, `darś`) while DCS keys the bare root "
      "(`sṛj`, `dṛś`). A stem→root normaliser (guṇa/vṛddhi/sandhi undo) plus the DCS `lemma` "
      "table's preverb column would recover most of these and is the clear follow-up.\n")
    A("- The **~4 % parse ceiling** means CONFIRMED counts are a floor and UNATTESTED-INSUFFICIENT "
      "is genuinely \"unknown\", not \"absent\". As DCS dependency coverage grows, rerun.\n")
    A("- CONTRADICTED is a **screening** verdict, hand-checked below; a homonym or preverb misjoin "
      "(the README names har/hṛ, idh/indh, kar/kṛ) can masquerade as one.\n")

    A("\n_Dr. Mārcis Gasūns_\n")
    with io.open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    print("wrote", OUT_MD)

if __name__ == "__main__":
    main()
