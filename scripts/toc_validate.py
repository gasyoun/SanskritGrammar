#!/usr/bin/env python3
"""Validate the Sangram C2 article-network registry (sangram/toc/data/articles.json).

Normative checks (the registry's contract is sangram/toc/SANGRAM_TOC_NETWORK.mdx):
  1. id grammar ^SG-(PH|WF|MO|SE|SY|DI|VA)-[0-9]{3}$, unique, domain code matches
  2. append-only: retired_ids disjoint from live ids
  3. prerequisites reference existing ids; the prerequisite graph is acyclic
  4. every article: >=1 witness (known work slug), query.engine + query.sketch non-empty
  5. whitney anchors well-formed (whitney-sec:LO[-HI], 1..1316, LO<=HI)
  6. form_classes exist in SubjectConcordance/typed_link_thematic.tsv (H540 canon)
  7. every declared domain has >=1 core article
  8. generated pages in sangram/toc/ are in sync with the registry
     (re-runs toc_build_pages.py --check)

Exit 0 = clean; exit 1 = violations (each printed as "TOC-E<nn> ...").
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "sangram" / "toc" / "data" / "articles.json"
TSV = ROOT / "SubjectConcordance" / "typed_link_thematic.tsv"

ID_RE = re.compile(r"^SG-(PH|WF|MO|SE|SY|DI|VA)-([0-9]{3})$")
ANCHOR_RE = re.compile(r"^whitney-sec:([0-9]{1,4})(?:-([0-9]{1,4}))?$")
LAYERS = {"core", "layered"}

# The 33 article slots of the merged C6 programme (sangram/
# SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx §6; its own "Итого 32" line
# undercounts the actual table rows by one). C6 defers ID canon to C2:
# every slot must be mapped to exactly one registry article via c6_slots.
C6_SLOTS = {
    "sem-a-case-overview", "sem-a-instrumental", "sem-a-genitive",
    "sem-a-dative-experiencer", "sem-a-locative", "sem-a-karaka-vs-case",
    "sem-b-past-competition", "sem-b-ta-narrative", "sem-b-optative",
    "sem-b-imperative", "sem-b-nonfinite-taxis",
    "sem-c-passive", "sem-c-middle", "sem-c-causative",
    "syn-a-word-order", "syn-a-nominal-clause", "syn-a-agreement",
    "syn-a-negation",
    "syn-b-correlatives", "syn-b-iti", "syn-b-conditionals",
    "syn-b-coordination",
    "syn-c-absolutive-chain", "syn-c-locative-absolute", "syn-c-gerundive",
    "syn-c-dative-possessive",
    "is-a-eva", "is-a-second-position", "is-a-tense-switching",
    "is-a-direct-speech",
    "reg-a-prose-verse", "reg-a-layer-vedic-classical",
    "reg-a-epic-deviations",
}

errors = []


def err(code: str, msg: str) -> None:
    errors.append(f"TOC-E{code} {msg}")


def main() -> int:
    data = json.loads(REG.read_text(encoding="utf-8"))
    domains = {d["code"] for d in data["domains"]}
    works = {w["slug"] for w in data["works"]}
    articles = data["articles"]

    # canonical form-class slugs (H540 typed-link dataset)
    slugs = set()
    for line in TSV.read_text(encoding="utf-8").splitlines()[1:]:
        cols = line.split("\t")
        if len(cols) > 3:
            slugs.add(cols[3].rsplit(":", 1)[-1])

    ids = [a["id"] for a in articles]
    seen = set()
    for a in articles:
        aid = a["id"]
        m = ID_RE.match(aid)
        if not m:
            err("01", f"{aid}: id violates grammar")
            continue
        if aid in seen:
            err("02", f"{aid}: duplicate id")
        seen.add(aid)
        if m.group(1) not in domains:
            err("03", f"{aid}: domain code not declared")
        if a.get("layer") not in LAYERS:
            err("04", f"{aid}: layer must be one of {sorted(LAYERS)}")
        if not a.get("title_ru", "").strip():
            err("05", f"{aid}: empty title_ru")
        for p in a.get("prerequisites", []):
            if p not in ids:
                err("06", f"{aid}: prerequisite {p} does not exist")
            if p == aid:
                err("06", f"{aid}: self-prerequisite")
        ws = a.get("witnesses", [])
        if not ws:
            err("07", f"{aid}: no witnesses (>=1 required)")
        for w in ws:
            if w.get("work") not in works:
                err("08", f"{aid}: unknown witness work {w.get('work')!r}")
            if not w.get("locus", "").strip():
                err("08", f"{aid}: witness {w.get('work')} has empty locus")
        q = a.get("query", {})
        if not q.get("engine") or not q.get("sketch", "").strip():
            err("09", f"{aid}: query.engine/query.sketch required")
        for anc in a.get("whitney", []):
            am = ANCHOR_RE.match(anc)
            if not am:
                err("10", f"{aid}: malformed anchor {anc}")
                continue
            lo = int(am.group(1))
            hi = int(am.group(2) or lo)
            if not (1 <= lo <= hi <= 1316):
                err("10", f"{aid}: anchor {anc} out of Whitney range 1-1316")
        for fc in a.get("form_classes", []):
            if fc not in slugs:
                err("11", f"{aid}: form_class {fc!r} not in typed_link_thematic.tsv")

    # C6 crosswalk: every C6 slot mapped to exactly one article, no unknowns
    slot_owner = {}
    for a in articles:
        for s in a.get("c6_slots", []):
            if s not in C6_SLOTS:
                err("16", f"{a['id']}: unknown C6 slot {s!r}")
            elif s in slot_owner:
                err("16", f"C6 slot {s} mapped twice ({slot_owner[s]}, {a['id']})")
            else:
                slot_owner[s] = a["id"]
    for s in sorted(C6_SLOTS - set(slot_owner)):
        err("16", f"C6 slot {s} not mapped to any article")

    # retired ids are append-only bookkeeping, never live
    for rid in data.get("retired_ids", []):
        if rid in seen:
            err("12", f"{rid}: listed both live and retired")

    # acyclicity (iterative DFS, three-color)
    graph = {a["id"]: [p for p in a.get("prerequisites", []) if p in seen]
             for a in articles}
    color = dict.fromkeys(graph, 0)
    for start in graph:
        if color[start]:
            continue
        stack = [(start, iter(graph[start]))]
        color[start] = 1
        while stack:
            node, it = stack[-1]
            for nxt in it:
                if color[nxt] == 1:
                    err("13", f"prerequisite cycle through {nxt}")
                    color[nxt] = 2
                elif color[nxt] == 0:
                    color[nxt] = 1
                    stack.append((nxt, iter(graph[nxt])))
                    break
            else:
                color[node] = 2
                stack.pop()

    # domain coverage
    per_dom = {d: 0 for d in domains}
    for a in articles:
        m = ID_RE.match(a["id"])
        if m:
            per_dom[m.group(1)] += 1
    for d, n in sorted(per_dom.items()):
        if n == 0:
            err("14", f"domain {d} has no articles")

    # generated pages in sync
    check = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "toc_build_pages.py"), "--check"],
        capture_output=True, encoding="utf-8")
    if check.returncode != 0:
        err("15", "generated pages out of sync with registry -- "
                  "run: python scripts/toc_build_pages.py")
        if check.stdout.strip():
            print(check.stdout.strip())

    if errors:
        print("\n".join(errors))
        print(f"FAIL: {len(errors)} violation(s) across {len(articles)} articles")
        return 1
    print(f"OK: {len(articles)} articles, {len(domains)} domains, "
          f"{sum(len(a.get('prerequisites', [])) for a in articles)} prerequisite edges, "
          f"0 violations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
