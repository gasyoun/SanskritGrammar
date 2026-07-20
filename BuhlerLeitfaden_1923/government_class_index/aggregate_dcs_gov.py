#!/usr/bin/env python3
"""Stream all DCS CoNLL-U files once and build a verb-lemma -> governed-case aggregate.

For every VERB token we record:
  - verb_freq[lemma]            total occurrences of that verb lemma
  - dep_gov[lemma][case]        # times a case-C nominal is a DIRECT dependent (head==verb)
  - dep_deprel[lemma][deprel]   deprel distribution of those governed nominals (context)
  - cooc[lemma][case]           # sentences where a case-C nominal co-occurs with the verb
  - verb_parsed[lemma]          occurrences in a sentence that actually carries dependency arcs

Only real morphological cases are counted (Case=Cpd compound-members and caseless tokens skipped).
Output: dcs_gov_aggregate.json in the scratchpad.
"""
import sys, os, io, json, glob
from collections import defaultdict, Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

DCS_ROOT = r"C:\Users\user\Documents\GitHub\dcs-conllu\files"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dcs_gov_aggregate.json")

REAL_CASES = {"Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc"}  # drop Cpd, Voc handled below

def parse_feats(feats):
    if feats == "_" or not feats:
        return None
    for kv in feats.split("|"):
        if kv.startswith("Case="):
            return kv.split("=", 1)[1]
    return None

verb_freq = Counter()
verb_parsed = Counter()
dep_gov = defaultdict(Counter)      # lemma -> case -> count
dep_deprel = defaultdict(Counter)   # lemma -> deprel -> count
cooc = defaultdict(Counter)         # lemma -> case -> sentence-count
sent_with_case = Counter()          # case -> # sentences containing >=1 nominal in that case (base rate)

n_files = 0
n_sent = 0
n_sent_parsed = 0
n_tok = 0

files = glob.glob(os.path.join(DCS_ROOT, "**", "*.conllu"), recursive=True)
print(f"found {len(files)} conllu files", flush=True)

def flush_sentence(tokens):
    """tokens: list of dicts {id,lemma,upos,case,head,deprel}"""
    global n_sent, n_sent_parsed
    if not tokens:
        return
    n_sent += 1
    by_id = {t["id"]: t for t in tokens}
    parsed = any(t["head"] is not None for t in tokens)
    if parsed:
        n_sent_parsed += 1
    # cases present in this sentence (for co-occurrence)
    cases_here = {t["case"] for t in tokens if t["case"] in REAL_CASES}
    for c in cases_here:
        sent_with_case[c] += 1
    for t in tokens:
        if t["upos"] != "VERB":
            continue
        lem = t["lemma"]
        if not lem or lem == "_":
            continue
        verb_freq[lem] += 1
        if parsed:
            verb_parsed[lem] += 1
        # direct dependents whose head == this verb
        for u in tokens:
            if u["head"] == t["id"] and u["case"] in REAL_CASES:
                dep_gov[lem][u["case"]] += 1
                dep_deprel[lem][u["deprel"] or "_"] += 1
        # co-occurrence (once per case per sentence)
        for c in cases_here:
            cooc[lem][c] += 1

for fp in files:
    n_files += 1
    if n_files % 2000 == 0:
        print(f"  ...{n_files}/{len(files)} files, {n_sent} sents", flush=True)
    try:
        with io.open(fp, encoding="utf-8") as fh:
            tokens = []
            for line in fh:
                line = line.rstrip("\n")
                if not line:
                    flush_sentence(tokens)
                    tokens = []
                    continue
                if line.startswith("#"):
                    continue
                cols = line.split("\t")
                if len(cols) < 8:
                    continue
                tid = cols[0]
                if "-" in tid or "." in tid:   # multiword range / empty node
                    continue
                n_tok += 1
                head = cols[6]
                tokens.append({
                    "id": tid,
                    "lemma": cols[2],
                    "upos": cols[3],
                    "case": parse_feats(cols[5]),
                    "head": head if head not in ("_", "") else None,
                    "deprel": cols[7] if cols[7] != "_" else None,
                })
            flush_sentence(tokens)
    except Exception as e:
        print(f"  ERR {fp}: {e}", flush=True)

out = {
    "meta": {
        "n_files": n_files, "n_sent": n_sent, "n_sent_parsed": n_sent_parsed,
        "n_tok": n_tok, "n_verb_lemmas": len(verb_freq),
    },
    "sent_with_case": dict(sent_with_case),
    "verb_freq": dict(verb_freq),
    "verb_parsed": dict(verb_parsed),
    "dep_gov": {k: dict(v) for k, v in dep_gov.items()},
    "dep_deprel": {k: dict(v) for k, v in dep_deprel.items()},
    "cooc": {k: dict(v) for k, v in cooc.items()},
}
with io.open(OUT, "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False)
print("META:", json.dumps(out["meta"], ensure_ascii=False), flush=True)
print("wrote", OUT, flush=True)
