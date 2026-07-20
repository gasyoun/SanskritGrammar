"""SG-SE-013 — measure the Usha Sanka native kāraka gold against the DCS deprel proxy.

Both inputs are COMMITTED (unlike the extractor, which needs the untracked .docx), so this
runs in CI. It compares the two models at the ROLE level — the level both datasets expose
cleanly — and surfaces the roles the deprel proxy has no relation for at all.

A per-lemma agreement join (which of the gold's dhātus appear in DCS with deprel-tagged
kāraka evidence, and whether the assignment agrees) needs the 920 MB dcs_full.sqlite plus a
Dhātupāṭha-root ↔ DCS-lemma crosswalk — left as an explicit follow-up (see article § 7).

Usage:  python scripts/compare_usha_gold_vs_proxy.py [--check]
  (no arg) regenerate sangram/articles/karaka-case/data/usha_gold_vs_proxy.json
  --check  regenerate in-memory and assert it matches the committed file (CI gate)
"""
import sys, os, json, argparse
sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLD = os.path.join(ROOT, "Concordance", "usha_karaka_gold", "usha_karaka_gold.json")
COV  = os.path.join(ROOT, "sangram", "articles", "karaka-case", "data", "coverage_summary.json")
OUT  = os.path.join(ROOT, "sangram", "articles", "karaka-case", "data", "usha_gold_vs_proxy.json")

# The nine roles the gold uses (six Pāṇinian kārakas + tādarthya/hetu/anya), and which
# have a deprel proxy in the article's § 3 kāraka→deprel map. hetu/tādarthya/anya do NOT.
PROXY_ROLE = {  # gold role -> list of crosstab "karaka" labels that proxy it (or None)
    "kartṛ":      ["kartR (agent, active)", "kartR-passive (agent)"],
    "karman":     ["karman (patient/object)"],
    "karaṇa":     ["karaNa (instrument)"],
    "sampradāna": ["sampradAna-recipient", "sampradAna-goal", "sampradAna-benefactive"],
    "apādāna":    ["apAdAna (source)"],
    "adhikaraṇa": ["adhikaraNa (locus)"],
    "tādarthya":  None,
    "hetu":       None,
    "anya":       None,
}

def build():
    gold = json.load(open(GOLD, encoding="utf-8"))
    cov  = json.load(open(COV, encoding="utf-8"))
    crosstab = {r["karaka"]: r for r in cov["karaka_case_crosstab"]}

    # gold: per-role citation count. (Citations are attached at the verb-GROUP level, so a
    # per-dhātu-per-role count is not separable from the source — we report citations only.)
    gold_cit = {}
    all_dhatus = set()
    for grp in gold:
        all_dhatus |= set(grp.get("dhatus", []))
        for role, cites in grp.get("karaka", {}).items():
            # a citation whose text is a valency note (e.g. अकर्मकः) still counts as a row,
            # matching the README's 1,372 total; keep parity with the committed dataset.
            gold_cit[role] = gold_cit.get(role, 0) + len(cites)

    # rank the six core kārakas by count in each model (for the divergence finding)
    core = [r for r in PROXY_ROLE if PROXY_ROLE[r] is not None]
    proxy_vis = {r: sum(crosstab[l]["case_tagged_total"]
                        for l in PROXY_ROLE[r] if l in crosstab) for r in core}
    gold_rank  = {r: i + 1 for i, r in enumerate(sorted(core, key=lambda r: -gold_cit.get(r, 0)))}
    proxy_rank = {r: i + 1 for i, r in enumerate(sorted(core, key=lambda r: -proxy_vis[r]))}

    rows = []
    for role, labels in PROXY_ROLE.items():
        in_proxy = labels is not None
        proxy_visible = proxy_dom = None
        if in_proxy:
            proxy_visible = proxy_vis[role]
            biggest = max((crosstab[l] for l in labels if l in crosstab),
                          key=lambda r: r["case_tagged_total"])
            proxy_dom = f'{biggest["top_case"]} {biggest["top_case_pct"]}%'
        rows.append({
            "role": role,
            "in_deprel_proxy": in_proxy,
            "gold_citations": gold_cit.get(role, 0),
            "gold_rank_core": gold_rank.get(role),
            "proxy_deprels": ",".join(labels) if labels else None,
            "proxy_visible_tokens": proxy_visible,
            "proxy_rank_core": proxy_rank.get(role),
            "proxy_dominant_case": proxy_dom,
        })

    proxy_blind = [r for r in rows if not r["in_deprel_proxy"]]
    result = {
        "article": "SG-SE-013",
        "note": ("Role-level comparison of the Usha Sanka native kāraka gold "
                 "(Concordance/usha_karaka_gold/) against the DCS deprel proxy "
                 "(coverage_summary.json). Per-lemma agreement join is a follow-up "
                 "(needs dcs_full.sqlite + root↔lemma crosswalk)."),
        "gold": {
            "verb_groups": len(gold),
            "distinct_dhatus": len(all_dhatus),
            "total_citations": sum(gold_cit.values()),
        },
        "proxy": {
            "deprel_coverage_pct": cov["deprel_coverage_pct"],
            "deprel_nonnull_tokens": cov["deprel_nonnull"],
        },
        "roles": rows,
        "proxy_blind_roles": [r["role"] for r in proxy_blind],
        "proxy_blind_citations": sum(r["gold_citations"] for r in proxy_blind),
        "proxy_blind_semantic_citations": sum(
            r["gold_citations"] for r in proxy_blind if r["role"] in ("hetu", "tādarthya")),
    }
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    res = build()
    if a.check:
        have = json.load(open(OUT, encoding="utf-8"))
        if have != res:
            print("MISMATCH — committed usha_gold_vs_proxy.json is stale; regenerate.")
            sys.exit(1)
        print("OK — usha_gold_vs_proxy.json matches regeneration.")
        return
    json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"wrote {os.path.relpath(OUT, ROOT)}")
    print(f"gold: {res['gold']['distinct_dhatus']} dhātus, {res['gold']['total_citations']} citations")
    print(f"proxy-blind roles: {res['proxy_blind_roles']} "
          f"= {res['proxy_blind_citations']} citations "
          f"({res['proxy_blind_semantic_citations']} in hetu+tādarthya)")
    print("\nrole | in_proxy | gold_cit (rank) | proxy_visible (rank) | proxy_dom")
    for r in res["roles"]:
        print(f"  {r['role']:11} {str(r['in_deprel_proxy']):5} "
              f"{r['gold_citations']:5} ({r['gold_rank_core'] or '-'}) "
              f"{str(r['proxy_visible_tokens']):>8} ({r['proxy_rank_core'] or '-'}) "
              f"{r['proxy_dominant_case'] or '—'}")

if __name__ == "__main__":
    main()
