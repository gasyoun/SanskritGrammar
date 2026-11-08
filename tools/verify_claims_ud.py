#!/usr/bin/env python
"""verify_claims_ud.py — dependency/lemma probes for the UD_Sanskrit-UFAL
external gold layer (H6842, WHEEL9 visa item (b)).

Reads the mirrored CoNLL-U in data/ud_sanskrit/ and the probe register
data/ud_sanskrit/claims.yml, computes one measurable UD-schema proxy per row,
and emits the dual verdict (verdict_fact on the register axis, verdict_ud on
the UD-proxy axis) plus the numbers, into claims_ud_stats.json.

Schema: every number below is a **UD v2** measurement (DEPREL / UPOS / UD
lemma column, Devanagari) — see the mapping statement in claims.yml; not
comparable to DCS head/deprel slices without it.

Ground-truth source: UD_Sanskrit-UFAL (ÚFAL, Charles University; Dwivedi,
Zeman, Biagetti), CC BY-SA 4.0, mirrored at data/ud_sanskrit/
sa_ufal-ud-test.conllu (upstream master 80f88c8, fetched 22-10-2026; licence
facts in data/ud_sanskrit/README.md).

Usage:  python tools/verify_claims_ud.py            # report + write claims_ud_stats.json
        python tools/verify_claims_ud.py --check    # report only, no file write
"""
import json
import sys
from pathlib import Path
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
GOLD = REPO / "data" / "ud_sanskrit"
CONLLU = GOLD / "sa_ufal-ud-test.conllu"
CLAIMS = GOLD / "claims.yml"
OUT = GOLD / "claims_ud_stats.json"

NONVERBAL_ROOT_UPOS = {"NOUN", "ADJ", "PRON", "PROPN", "NUM", "INTJ"}


def load_conllu(path=CONLLU):
    """Parse CoNLL-U: skip comment lines and multi-word-token (id with '-')
    / empty-node (id with '.') rows; return list of sentences, each a list of
    token dicts with int id, form, lemma, upos, head, deprel."""
    sentences, cur = [], []
    for ln in path.read_text(encoding="utf-8").splitlines():
        if ln.startswith("#"):
            continue
        if not ln.strip():
            if cur:
                sentences.append(cur)
                cur = []
            continue
        cols = ln.split("\t")
        if len(cols) < 8:
            continue
        tid = cols[0]
        if "-" in tid or "." in tid:
            continue  # multi-word token / empty node
        cur.append({
            "id": int(tid),
            "form": cols[1],
            "lemma": cols[2],
            "upos": cols[3],
            "head": int(cols[6]) if cols[6].isdigit() else 0,
            "deprel": cols[7],
        })
    if cur:
        sentences.append(cur)
    return sentences


def probe_uda1_ca_position(sentences):
    """UDA-1 (replicates APT-3): ca never sentence-initial."""
    total = initial = 0
    for s in sentences:
        for i, t in enumerate(s):
            if t["upos"] == "CCONJ" and t["lemma"] == "च":
                total += 1
                if i == 0:
                    initial += 1
    share = round(100 * initial / total, 1) if total else 0.0
    verdict = "PASS" if initial == 0 else "FAIL"
    return {
        "proxy": "sentence-initial ca / total CCONJ-च tokens",
        "total_ca": total, "sentence_initial_ca": initial,
        "initial_share_pct": share,
        "threshold": "0 initial -> PASS",
        "verdict_ud": verdict,
        "verdict_fact": "TRUE" if initial == 0 else "FALSE",
    }


def probe_uda2_ov_order(sentences):
    """UDA-2: object-before-verb dominance (SOV doctrine)."""
    before = after = 0
    for s in sentences:
        for t in s:
            if t["deprel"] in ("obj", "iobj"):
                heads = [h for h in s if h["id"] == t["head"]]
                if not heads:
                    continue
                h = heads[0]
                if h["upos"] in ("VERB", "AUX"):
                    if t["id"] < h["id"]:
                        before += 1
                    else:
                        after += 1
    tot = before + after
    share = round(100 * before / tot, 1) if tot else 0.0
    verdict = "PASS" if tot and share >= 66.7 else ("OVERSTATED" if tot else "FAIL")
    return {
        "proxy": "obj/iobj preceding verbal head / all obj+iobj with VERB/AUX head",
        "ov": before, "vo": after, "total": tot, "ov_share_pct": share,
        "threshold": ">=66.7% -> PASS",
        "verdict_ud": verdict,
        "verdict_fact": {"PASS": "TRUE", "OVERSTATED": "OVERSTATED",
                         "FAIL": "FALSE"}[verdict],
    }


def probe_uda3_verbless(sentences):
    """UDA-3: verbless nominal sentences common."""
    nonverbal = 0
    for s in sentences:
        roots = [t for t in s if t["deprel"] == "root" and t["head"] == 0]
        if roots and all(r["upos"] in NONVERBAL_ROOT_UPOS for r in roots):
            nonverbal += 1
    n = len(sentences)
    share = round(100 * nonverbal / n, 1) if n else 0.0
    verdict = "PASS" if share >= 5.0 else "OVERSTATED"
    return {
        "proxy": "sentences with non-verbal root UPOS / all sentences",
        "nonverbal_root_sentences": nonverbal, "total_sentences": n,
        "share_pct": share,
        "threshold": ">=5% -> PASS, <5% -> OVERSTATED",
        "verdict_ud": verdict,
        "verdict_fact": {"PASS": "TRUE", "OVERSTATED": "OVERSTATED"}[verdict],
    }


def probe_uda4_top_lemma(sentences):
    """UDA-4: lemma अस् ('be') ranks #1 among VERB/AUX lemmas."""
    lemmas = Counter()
    for s in sentences:
        for t in s:
            if t["upos"] in ("VERB", "AUX") and t["lemma"] and t["lemma"] != "_":
                lemmas[t["lemma"]] += 1
    ranked = lemmas.most_common()
    rank = next((i + 1 for i, (l, _) in enumerate(ranked) if l == "अस्"), None)
    as_n = lemmas.get("अस्", 0)
    if rank == 1:
        verdict, fact = "PASS", "TRUE"
    elif rank in (2, 3):
        verdict, fact = "OVERSTATED", "OVERSTATED"
    else:
        verdict, fact = "FAIL", "FALSE"
    return {
        "proxy": "rank of lemma अस् among VERB/AUX lemmas by token count",
        "rank_as": rank, "count_as": as_n, "distinct_verb_lemmas": len(ranked),
        "top5": [[l, n] for l, n in ranked[:5]],
        "threshold": "rank 1 -> PASS, rank 2-3 -> OVERSTATED, worse -> FAIL",
        "verdict_ud": verdict,
        "verdict_fact": fact,
    }


def analyze():
    sentences = load_conllu()
    n_sent = len(sentences)
    n_tok = sum(len(s) for s in sentences)
    return {
        "_schema_label": "UD v2 (DEPREL/UPOS/lemma); NOT karaka-DCST — see data/ud_sanskrit/claims.yml mapping statement",
        "_source": "UD_Sanskrit-UFAL, CC BY-SA 4.0, mirror commit 80f88c8 (22-10-2026), data/ud_sanskrit/README.md",
        "_handoff": "H6842 (WHEEL9 visa item (b))",
        "n_sentences": n_sent,
        "n_tokens": n_tok,
        "UDA1_ca_position": probe_uda1_ca_position(sentences),
        "UDA2_ov_order": probe_uda2_ov_order(sentences),
        "UDA3_verbless": probe_uda3_verbless(sentences),
        "UDA4_top_lemma": probe_uda4_top_lemma(sentences),
    }


def report(s):
    print(f"UD GOLD: {s['n_sentences']} sentences / {s['n_tokens']} tokens "
          f"({s['_schema_label']})")
    u1 = s["UDA1_ca_position"]
    print(f"UDA-1 CA POSITION: {u1['sentence_initial_ca']}/{u1['total_ca']} "
          f"sentence-initial -> {u1['verdict_fact']} / {u1['verdict_ud']}")
    u2 = s["UDA2_ov_order"]
    print(f"UDA-2 OV ORDER: {u2['ov_share_pct']}% of {u2['total']} obj/iobj "
          f"precede the verb -> {u2['verdict_fact']} / {u2['verdict_ud']}")
    u3 = s["UDA3_verbless"]
    print(f"UDA-3 VERBLESS: {u3['share_pct']}% of {u3['total_sentences']} "
          f"sentences non-verbal-root -> {u3['verdict_fact']} / {u3['verdict_ud']}")
    u4 = s["UDA4_top_lemma"]
    top = ", ".join(f"{l}:{n}" for l, n in u4["top5"])
    print(f"UDA-4 TOP LEMMA: अस् rank {u4['rank_as']} (n={u4['count_as']}) "
          f"of {u4['distinct_verb_lemmas']} VERB/AUX lemmas [{top}] "
          f"-> {u4['verdict_fact']} / {u4['verdict_ud']}")


def write_back_verdicts(s):
    """Mirror the dual verdicts into claims.yml PENDING rows (idempotent)."""
    rows = {"UDA-1": "UDA1_ca_position", "UDA-2": "UDA2_ov_order",
            "UDA-3": "UDA3_verbless", "UDA-4": "UDA4_top_lemma"}
    text = CLAIMS.read_text(encoding="utf-8")
    for cid, key in rows.items():
        res = s[key]
        for field, value in (("verdict_fact", res["verdict_fact"]),
                             ("verdict_ud", res["verdict_ud"])):
            text = _replace_pending(text, cid, field, value)
    CLAIMS.write_text(text, encoding="utf-8")


def _replace_pending(text, cid, field, value):
    """Replace `field: PENDING` with the measured value, only inside the cid row."""
    lines = text.splitlines(keepends=True)
    in_row = False
    for i, ln in enumerate(lines):
        if ln.strip() == f"- id: {cid}":
            in_row = True
            continue
        if in_row:
            if ln.startswith("  - id: ") or ln.startswith("# "):
                in_row = False
                continue
            if ln.strip() == f"{field}: PENDING":
                lines[i] = ln.replace(f"{field}: PENDING", f"{field}: {value}")
                in_row = False
    return "".join(lines)


def main():
    stats = analyze()
    report(stats)
    if "--check" not in sys.argv:
        OUT.write_text(json.dumps(stats, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        write_back_verdicts(stats)
        print(f"\n-> wrote {OUT.relative_to(REPO)} and mirrored dual verdicts "
              f"into {CLAIMS.relative_to(REPO)}")


if __name__ == "__main__":
    main()
