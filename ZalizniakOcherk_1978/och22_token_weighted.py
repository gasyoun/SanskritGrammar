#!/usr/bin/env python
"""OCH-22 strict token-weighted replication (Ocherk 1978 §67).

Claim: "Корни рядов R, M, N могут быть обоих типов, но большинство
употребительных корней — полноизменяемые, например: √darç, √gam, √bandh."

The type-count measurement (139/21 full/defective over 160 root+homonym
pairs) already settled 'большинство' by type; this script performs the
strict token-weighted replication the OCH-22 note deferred: a
lemma-frequency join keyed to citation forms against the DCS-2026 SQLite
master (dcs_full.sqlite, dcs-conllu commit 04e0778).

Join design (the divergences the note warned about, resolved):
  - R/M/N membership + полноизменяемость come from the 1978 columns of
    TolchelnikovTalmud_2026/data/morphoclass_crosswalk_1975_2014_2026.csv
    (maintained by build_1978_crosswalk.py). 147 distinct citation forms;
    homonyms never disagree on class/полноизменяемость, so DCS-side
    conflation of homonyms is harmless.
  - DCS verbal lemmas = grammar containing a P./Ā. class tag; simplex =
    empty preverbs field. Preverbed lemmas store the compound in `lemma`
    with the preverb split out in `preverbs`; they are attributed to a
    root by stripping the preverb concatenation off the front (boundary
    sandhi makes a small unattributable residue, which is counted and
    reported, never silently dropped).
  - Citation-key aliases (Whitney/Talmud form -> DCS key), identity-certain
    only: ṛc->arc, bṛh->bṛṃh, jambh->jabh, tark->tarkay, carc->carcay
    (the last two are DCS's denominative-stem citations of the same item).
  - Roots with no DCS verbal lemma at all (phar, jhar, pard, śran, ...)
    are reported as unattested, not fabricated as zero-frequency evidence.

Outputs och22_token_weighted.json next to this script and prints a summary.
"""
import io
import json
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CROSSWALK = REPO / "TolchelnikovTalmud_2026" / "data" / "morphoclass_crosswalk_1975_2014_2026.csv"
DCS_SQLITE = REPO.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"

ALIASES = {"ṛc": "arc", "bṛh": "bṛṃh", "jambh": "jabh", "tark": "tarkay", "carc": "carcay"}


def load_rmn():
    import csv
    rmn = {}
    with io.open(CROSSWALK, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            ry = r["ryad_1978"]
            if ry and ry[0] in "RMN":
                prev = rmn.get(r["root"])
                cur = (ry, r["polnoizm_1978"])
                if prev is not None:
                    # duplicate crosswalk rows may disagree on the series INDEX
                    # (e.g. car: R? vs R₂) but полноизменяемость — the only field
                    # OCH-22 classifies by — must agree; keep the indexed variant
                    assert prev[1] == cur[1], f"polnoizm conflict at {r['root']}"
                    if "?" not in ry and "?" in prev[0]:
                        rmn[r["root"]] = cur
                else:
                    rmn[r["root"]] = cur
    return rmn


def main():
    if len(sys.argv) > 1:
        globals()["DCS_SQLITE"] = Path(sys.argv[1])
    rmn = load_rmn()
    db = sqlite3.connect(DCS_SQLITE)
    c = db.cursor()

    tok = dict(c.execute("SELECT lemma_id, COUNT(*) FROM token GROUP BY lemma_id"))
    verbal = list(c.execute(
        "SELECT lemma_id, lemma, preverbs FROM lemma "
        "WHERE grammar LIKE '%P.%' OR grammar LIKE '%Ā.%'"))

    dcs_key = {root: ALIASES.get(root, root) for root in rmn}
    key_to_root = defaultdict(list)
    for root, key in dcs_key.items():
        key_to_root[key].append(root)
    assert all(len(v) == 1 for v in key_to_root.values()), "alias collision"

    simplex = defaultdict(int)
    preverbed = defaultdict(int)
    prev_unattributed_tokens = 0
    for lemma_id, lemma, preverbs in verbal:
        n = tok.get(lemma_id, 0)
        if not n:
            continue
        if not preverbs:
            if lemma in key_to_root:
                simplex[key_to_root[lemma][0]] += n
            continue
        parts = [p for p in re.split(r"[,\s]+", preverbs) if p]
        residual = None
        for cand in ("".join(parts), "".join(reversed(parts))):
            if lemma.startswith(cand) and len(lemma) > len(cand):
                residual = lemma[len(cand):]
                break
        if residual is None:
            prev_unattributed_tokens += n
            continue
        if residual in key_to_root:
            preverbed[key_to_root[residual][0]] += n

    attested = {r for r in rmn if simplex.get(r) or preverbed.get(r)}
    unattested = sorted(set(rmn) - attested)

    def shares(counts):
        tot = sum(counts.values())
        full = sum(n for r, n in counts.items() if rmn[r][1] == "full")
        return {"total_tokens": tot, "full_tokens": full,
                "defective_tokens": tot - full,
                "full_share_pct": round(100.0 * full / tot, 2) if tot else None}

    combined = {r: simplex.get(r, 0) + preverbed.get(r, 0) for r in rmn}
    ranked = sorted(((n, r) for r, n in combined.items() if n), reverse=True)

    def topn(n):
        top = ranked[:n]
        full = sum(1 for _, r in top if rmn[r][1] == "full")
        return {"n": len(top), "full_roots": full, "defective_roots": len(top) - full,
                "defective_members": sorted(r for _, r in top if rmn[r][1] != "full")}

    named = {r: {"tokens": combined.get(r, 0),
                 "rank": next((i + 1 for i, (_, x) in enumerate(ranked) if x == r), None)}
             for r in ("dṛś", "gam", "bandh") if r in rmn}

    checks = []

    def check(label, ok):
        checks.append((label, bool(ok)))

    check("147 distinct RMN citation forms", len(rmn) == 147)
    verbal_keys = {l for _, l, _ in verbal}
    check("alias targets all present as DCS verbal keys",
          all(v in verbal_keys for v in ALIASES.values()))
    check("gam in top 5 by tokens", any(r == "gam" for _, r in ranked[:5]))
    check("named examples darś/gam/bandh all attested and full", all(
        named.get(r, {}).get("tokens", 0) > 0 and rmn[r][1] == "full"
        for r in ("dṛś", "gam", "bandh") if r in rmn))
    check("simplex full-share > 90%", shares(simplex)["full_share_pct"] > 90)
    check("combined full-share > 90%", shares(combined)["full_share_pct"] > 90)
    check("top-20 majority full", topn(20)["full_roots"] > 10)
    check("top-50 majority full", topn(50)["full_roots"] > 25)

    out = {
        "instrument": "och22_token_weighted.py over dcs_full.sqlite (dcs-conllu 04e0778) "
                      "x morphoclass_crosswalk_1975_2014_2026.csv 1978 columns",
        "rmn_citation_forms": len(rmn),
        "type_counts": {"full": sum(1 for v in rmn.values() if v[1] == "full"),
                        "defective": sum(1 for v in rmn.values() if v[1] != "full")},
        "aliases_applied": ALIASES,
        "attested_roots": len(attested),
        "unattested_roots": unattested,
        "simplex": shares(simplex),
        "simplex_plus_preverbed": shares(combined),
        "preverbed_unattributed_tokens_corpuswide": prev_unattributed_tokens,
        "top20": topn(20),
        "top50": topn(50),
        "named_examples": named,
        "top20_table": [{"root": r, "tokens": n, "ryad": rmn[r][0], "polnoizm": rmn[r][1]}
                        for n, r in ranked[:20]],
        "defective_tokens_by_root": {r: combined[r] for r in sorted(combined)
                                     if combined[r] and rmn[r][1] != "full"},
        "validation": {label: ok for label, ok in checks},
    }
    io.open(HERE / "och22_token_weighted.json", "w", encoding="utf-8").write(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n")

    print(f"RMN roots: {len(rmn)} ({out['type_counts']})")
    print(f"simplex: {out['simplex']}")
    print(f"simplex+preverbed: {out['simplex_plus_preverbed']}")
    print(f"top-20: {out['top20']}")
    print(f"top-50: {out['top50']}")
    print(f"named: {named}")
    print(f"unattested ({len(unattested)}): {unattested}")
    bad = [label for label, ok in checks if not ok]
    print(f"validation: {len(checks) - len(bad)}/{len(checks)} checks OK"
          + (f" — FAILED: {bad}" if bad else ""))
    print("-> och22_token_weighted.json written")


if __name__ == "__main__":
    main()
