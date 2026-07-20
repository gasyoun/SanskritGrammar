#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SG-SE-013 (H1399) — Per-lemma agreement: Usha kāraka gold vs DCS deprel proxy.

The H1395 tail. § 7.1 compared the two models at the ROLE level (aggregate). This script
answers the sharper, per-ROOT question: for each of the gold's 581 dhātus that DCS actually
attests as a governing verb, does the kāraka-demand the gold *claims* agree with what the
corpus *attests* (via the § 3 deprel→kāraka overlay)?

Method
------
1. Gold role set per root (GROUP level → all a group's dhātus share its role set; a root in
   several groups gets the UNION). Only the SIX core Pāṇinian kārakas are used: the three
   proxy-blind roles (tādarthya/hetu/anya) have no deprel relation, so a corpus can never
   confirm or deny them — comparing them would be unfair. `karman: अकर्मकः` is a valency note
   ("intransitive"), not a citation → treated as karman-ABSENT (README caveat).
2. Crosswalk: Devanagari → IAST (indic_transliteration.sanscript), parenthetical prefix/note
   stripped, matched directly to a DCS lemma. DCS lemmas ARE Dhātupāṭha-style roots in IAST
   (bhū, as, kṛ …), so the join is direct; the lossy part is that ~half the Dhātupāṭha tail is
   simply unattested in the corpus. Join coverage is reported explicitly, never silently capped.
3. Corpus role set per root: an argument token whose deprel maps to a kāraka (§ 3 KARAKA_MAP),
   joined to its GOVERNING verb (head) whose lemma is the root and whose upos is VERB. The role
   set the root actually governs, with per-role token counts.
4. Agreement per root: gold core role set vs corpus core role set → Jaccard + TP/FP/FN.
   Aggregate: mean Jaccard, per-role over/under-claim (does the § 7.1 rank divergence —
   adhikaraṇa gold-heavy, sampradāna corpus-heavy — reproduce per-root?).

Runs LOCALLY (needs the 920 MB untracked dcs_full.sqlite), like extract_usha_karaka_gold.py.
Commit the OUTPUT json; CI gates it via tests/test_usha_gold_perlemma_agreement.py.

Usage:  python scripts/usha_perlemma_agreement.py
Model:  Opus 4.8 (claude-opus-4-8[1m]), 20-07-2026.
"""
import json
import os
import re
import sqlite3
import sys
from collections import defaultdict

from indic_transliteration import sanscript

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD = os.path.join(ROOT, "Concordance", "usha_karaka_gold", "usha_karaka_gold.json")
COV = os.path.join(ROOT, "sangram", "articles", "karaka-case", "data", "coverage_summary.json")
OUT = os.path.join(ROOT, "sangram", "articles", "karaka-case", "data",
                   "usha_gold_perlemma_agreement.json")
DB = r"C:/Users/user/Documents/GitHub/VisualDCS/src/DCS-data-2026/dcs_full.sqlite"
PIN = "04e0778d3dc971030229179e25eea043d06ff397"

# The six core Pāṇinian kārakas (the only roles a deprel proxy can see). Order = article order.
CORE_ROLES = ["kartṛ", "karman", "karaṇa", "sampradāna", "apādāna", "adhikaraṇa"]
PROXY_BLIND = ["tādarthya", "hetu", "anya"]

# § 3 deprel → core kāraka (identical mapping to scripts/sg_se_013_karaka_case.py KARAKA_MAP).
DEPREL_TO_ROLE = {
    "nsubj": "kartṛ", "csubj": "kartṛ",
    "obl:agent": "kartṛ",              # passive agent — still kartṛ
    "obj": "karman",
    "obl:instr": "karaṇa",
    "iobj": "sampradāna", "obl:goal": "sampradāna", "obl:benef": "sampradāna",
    "obl:source": "apādāna",
    "obl:loc": "adhikaraṇa",
}
KARAKA_DEPRELS = list(DEPREL_TO_ROLE)

# Valency notes that appear INSIDE a karaka list but are not citations (README caveat).
VALENCY_NOTES = {"अकर्मकः", "सकर्मकः", "द्विकर्मकः", "उभयकर्मकः", "अकर्मक", "सकर्मक"}


def clean_dhatu(d):
    """Strip a trailing parenthetical prefix/query note: 'आप् (प्र-)' → 'आप्',
    'क्रम्((? …))' → 'क्रम्'. The bare root is what transliterates + joins."""
    return re.sub(r"\s*\(.*$", "", d).strip()


def gold_role_sets():
    """dhatu (Devanagari, cleaned) → set of CORE roles it demands (union over its groups),
    plus the full 9-role set for context. akarmaka-only karman is dropped."""
    gold = json.load(open(GOLD, encoding="utf-8"))
    core = defaultdict(set)
    allroles = defaultdict(set)
    for grp in gold:
        present_core, present_all = set(), set()
        for role, cites in grp.get("karaka", {}).items():
            real = [c for c in cites if (c.get("text") or "").strip() not in VALENCY_NOTES]
            if not real:
                continue
            present_all.add(role)
            if role in CORE_ROLES:
                present_core.add(role)
        for d in grp.get("dhatus", []):
            dc = clean_dhatu(d)
            if not dc:
                continue
            core[dc] |= present_core
            allroles[dc] |= present_all
    return core, allroles, len(gold)


def corpus_role_sets():
    """DCS VERB lemma → {core role: token count} governed via a kāraka-deprel argument.
    One full scan: collect VERB positions and kāraka arguments, then resolve arg→head verb."""
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    verb_at = {}                 # (sentence_id, idx) -> lemma  (upos=VERB only)
    args = []                    # (sentence_id, head, role)
    depset = set(KARAKA_DEPRELS)
    for sid, idx, lemma, upos, head, deprel in cur.execute(
            "SELECT sentence_id, idx, lemma, upos, head, deprel FROM token"):
        if upos == "VERB":
            verb_at[(sid, idx)] = lemma
        if deprel in depset and head is not None:
            args.append((sid, head, DEPREL_TO_ROLE[deprel]))
    counts = defaultdict(lambda: defaultdict(int))   # lemma -> role -> n
    for sid, head, role in args:
        lemma = verb_at.get((sid, head))
        if lemma is not None:
            counts[lemma][role] += 1
    con.close()
    return counts, prov, len(verb_at), len(args)


def main():
    gold_core, gold_all, n_groups = gold_role_sets()
    corpus, prov, n_verb_tokens, n_arg_tokens = corpus_role_sets()

    distinct = sorted(gold_core)   # cleaned distinct dhātus
    # A corpus role is "salient" for a root if it is not saturation noise: ≥2 tokens AND ≥5%
    # of that root's kāraka-arg tokens. High-frequency verbs (kṛ 1757 args) otherwise attest
    # every role with ≥1 token, so the binary set saturates to all six.
    SAL_MIN_TOK, SAL_MIN_FRAC = 2, 0.05
    per_root = []
    joined = []          # has ≥1 kāraka-tagged corpus argument
    comparable = []      # joined AND the gold makes ≥1 core-role claim for the root
    for d in distinct:
        iast = sanscript.transliterate(d, sanscript.DEVANAGARI, sanscript.IAST)
        crole = {r: n for r, n in corpus.get(iast, {}).items()}
        corpus_roles = set(crole)
        n_arg = sum(crole.values())
        salient = {r for r, n in crole.items() if n >= SAL_MIN_TOK and n / n_arg >= SAL_MIN_FRAC} if n_arg else set()
        gc = gold_core[d]
        matched = iast in corpus and n_arg > 0
        gold_claims = bool(gc)
        union = gc | corpus_roles
        jac = round(len(gc & corpus_roles) / len(union), 4) if union else None
        union_s = gc | salient
        jac_s = round(len(gc & salient) / len(union_s), 4) if union_s else None
        row = {
            "dhatu": d,
            "iast": iast,
            "gold_roles_core": sorted(gc),
            "gold_roles_all": sorted(gold_all[d]),
            "corpus_roles_core": sorted(corpus_roles),
            "corpus_roles_salient": sorted(salient),
            "corpus_role_counts": {r: crole[r] for r in sorted(crole)},
            "n_corpus_arg_tokens": n_arg,
            "joined": matched,
            "gold_makes_core_claim": gold_claims,
            "jaccard": jac if matched else None,
            "jaccard_salient": jac_s if matched else None,
            "tp": sorted(gc & corpus_roles),
            "corpus_only": sorted(corpus_roles - gc),   # corpus attests, gold silent
            "gold_only": sorted(gc - corpus_roles),     # gold claims, corpus never attests (robust to saturation)
        }
        per_root.append(row)
        if matched:
            joined.append(row)
            if gold_claims:
                comparable.append(row)

    # --- coverage ---
    n_total = len(distinct)
    n_joined = len(joined)
    n_comparable = len(comparable)
    n_gold_silent_joined = n_joined - n_comparable   # corpus has evidence, gold cited no core role

    # --- aggregate agreement (over COMPARABLE roots: gold actually makes a core claim) ---
    mean_jac = round(sum(r["jaccard"] for r in comparable) / n_comparable, 4) if n_comparable else None
    mean_jac_s = round(sum(r["jaccard_salient"] for r in comparable) / n_comparable, 4) if n_comparable else None
    per_role = {}
    for role in CORE_ROLES:
        g_present = sum(1 for r in comparable if role in r["gold_roles_core"])
        c_present = sum(1 for r in comparable if role in r["corpus_roles_core"])
        c_sal = sum(1 for r in comparable if role in r["corpus_roles_salient"])
        both = sum(1 for r in comparable if role in r["gold_roles_core"] and role in r["corpus_roles_core"])
        both_sal = sum(1 for r in comparable if role in r["gold_roles_core"] and role in r["corpus_roles_salient"])
        gold_only = g_present - both        # gold claims, corpus never attests
        corpus_only = c_present - both      # corpus attests (≥1 tok), gold silent
        corpus_only_sal = c_sal - both_sal  # corpus attests SALIENTLY, gold silent
        per_role[role] = {
            "gold_present": g_present, "corpus_present": c_present, "corpus_salient": c_sal, "both": both,
            "gold_only": gold_only, "corpus_only": corpus_only, "corpus_only_salient": corpus_only_sal,
            "recall_gold_confirmed_by_corpus": round(both / g_present, 4) if g_present else None,
            "precision_corpus_salient_in_gold": round(both_sal / c_sal, 4) if c_sal else None,
        }

    # § 7.1 rank-divergence reproduction at the per-root level:
    # adhikaraṇa was gold-heavy (gold rank 3, proxy rank 5) → expect gold_only high for adhikaraṇa;
    # sampradāna was corpus-heavy (gold rank 6, proxy rank 3) → expect corpus_only high for sampradāna.
    divergence = {
        "adhikaraṇa_gold_only": per_role["adhikaraṇa"]["gold_only"],
        "adhikaraṇa_corpus_only_salient": per_role["adhikaraṇa"]["corpus_only_salient"],
        "sampradāna_gold_only": per_role["sampradāna"]["gold_only"],
        "sampradāna_corpus_only_salient": per_role["sampradāna"]["corpus_only_salient"],
        "reproduces_role_level_divergence": (
            per_role["adhikaraṇa"]["gold_only"] > per_role["adhikaraṇa"]["corpus_only_salient"]
            and per_role["sampradāna"]["corpus_only_salient"] > per_role["sampradāna"]["gold_only"]
        ),
    }

    result = {
        "article": "SG-SE-013",
        "pin": PIN,
        "snapshot": {"source_repo": prov.get("source_repo"),
                     "source_commit": prov.get("source_commit"),
                     "imported_at": prov.get("imported_at")},
        "note": ("Per-lemma agreement join (H1399): the Usha Sanka native kāraka gold's claimed "
                 "role set per root vs the DCS deprel-proxy role set the corpus actually attests "
                 "for that root, over the six core Pāṇinian kārakas (the three proxy-blind roles — "
                 "tādarthya/hetu/anya — have no deprel relation and are excluded from agreement)."),
        "caveats": [
            "Gold granularity is the MEANING-GROUP, not the individual root: all dhātus in a group "
            "share that group's role set, so a per-root gold set is really its group's set.",
            "gold_makes_core_claim=false means the gold cited no core-kāraka for that root's group "
            "(missing data, e.g. group 121 'दाने-' gives only a hetu note) — NOT a claim of zero "
            "demand; such roots are EXCLUDED from the agreement metric (comparable set).",
            "The binary corpus role set saturates for high-frequency verbs (any role gets ≥1 token); "
            "the SALIENT set (≥2 tokens AND ≥5% of the root's kāraka args) is the saturation-guarded "
            "companion. gold_only (gold claims, corpus attests zero tokens) is robust to saturation.",
            "Crosswalk is direct Devanagari→IAST lemma match; ~half the Dhātupāṭha tail is unattested "
            "in DCS as a governing verb (reported below, never silently capped).",
        ],
        "core_roles": CORE_ROLES,
        "proxy_blind_roles_excluded": PROXY_BLIND,
        "salience_threshold": {"min_tokens": SAL_MIN_TOK, "min_fraction": SAL_MIN_FRAC},
        "gold": {"verb_groups": n_groups, "distinct_dhatus": n_total},
        "dcs": {"verb_tokens": n_verb_tokens, "karaka_arg_tokens": n_arg_tokens},
        "crosswalk": {
            "method": "indic_transliteration.sanscript Devanagari→IAST + parenthetical strip; "
                      "direct match to DCS VERB lemma governing ≥1 kāraka-deprel argument",
            "roots_total": n_total,
            "roots_with_karaka_evidence": n_joined,
            "join_coverage_pct": round(100.0 * n_joined / n_total, 2),
            "roots_comparable": n_comparable,
            "roots_joined_but_gold_silent_on_core": n_gold_silent_joined,
        },
        "summary": {
            "n_joined": n_joined,
            "n_comparable": n_comparable,
            "mean_jaccard": mean_jac,
            "mean_jaccard_salient": mean_jac_s,
            "per_role_agreement": per_role,
            "rank_divergence": divergence,
        },
        "per_root": per_root,
    }
    json.dump(result, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    print(f"gold: {n_groups} groups, {n_total} distinct dhātus (cleaned)")
    print(f"join coverage: {n_joined}/{n_total} = {result['crosswalk']['join_coverage_pct']}% "
          f"roots with ≥1 kāraka-tagged corpus argument")
    print(f"comparable (joined AND gold makes a core claim): {n_comparable}  "
          f"(gold-silent-on-core but joined: {n_gold_silent_joined})")
    print(f"mean Jaccard over comparable — binary: {mean_jac} | salient: {mean_jac_s}")
    print("\nper-role (over comparable): role | gold | corpus | corpus_sal | both | gold_only | corpus_only_sal")
    for role in CORE_ROLES:
        pr = per_role[role]
        print(f"  {role:11} {pr['gold_present']:4} {pr['corpus_present']:4} {pr['corpus_salient']:4} "
              f"{pr['both']:4} {pr['gold_only']:4} {pr['corpus_only_salient']:4}")
    print(f"\nrank-divergence reproduces per-root: {divergence['reproduces_role_level_divergence']}")


if __name__ == "__main__":
    main()
