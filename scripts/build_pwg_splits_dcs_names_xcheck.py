#!/usr/bin/env python3
"""H4712 — cross-check the PWG compound-split layer against DCS attested compounds.

Census A6. Joins data/pwg_compound_split/pwg_compound_splits.tsv (17,112 PWG
samāsa splits, post 26-07-2026 revision) against the DCS Kompozity names.csv
(168,880 attested compound word-forms w/ frequency vectors; kosha dataset
`dcs-compound-dictionary`, source VisualDCS derived-data/Kompozity/).

The join is ATTESTATION-level: is a compound PWG analyses also attested in the
DCS corpus-derived compound inventory? It is NOT a split-vs-split equality
check — PWG and DCS member chains are keyed differently (both give sandhi'd
stem chains, but stem selection differs: `rājan indra` vs `ābharant + vasu`
style), so member-level comparison would need stem normalization that is out
of scope here. What IS compared member-level, cheaply and honestly:

  * arity (PWG arity vs DCS arity, for attested rows)
  * seam-sandhi flag: does the concatenation of the PWG members reproduce the
    surface form exactly (no sandhi at the seam)? Reported per row; the
    no-sandhi subset is where a naive equality check is even possible.

Fold (form_key) is minimal and symmetric on both sides: NFC, anusvāra ṁ→ṃ,
avagraha dropped, trailing visarga stripped (DCS rows are inflected word-forms
`mahābalaḥ`, PWG headwords are stems `mahābala`), whitespace collapsed.

Read-only inputs; writes TSV + summary JSON under data/pwg_compound_split/.
Selftest: python3 scripts/build_pwg_splits_dcs_names_xcheck.py --selftest
"""

import argparse
import bisect
import json
import sys
import unicodedata
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SPLITS = REPO / "data/pwg_compound_split/pwg_compound_splits.tsv"
NAMES_CANDIDATES = [
    REPO.parent / "VisualDCS/derived-data/Kompozity/names.csv",
    REPO.parent / "kosha/data/dcs-compound-dictionary/names.csv",
]
OUT_TSV = REPO / "data/pwg_compound_split/pwg_splits_vs_dcs_names.tsv"
OUT_SUMMARY = REPO / "data/pwg_compound_split/pwg_splits_vs_dcs_names_summary.json"


def form_key(s: str) -> str:
    """Minimal symmetric fold for compound surface forms."""
    s = unicodedata.normalize("NFC", s)
    s = s.replace("ṁ", "ṃ").replace("’", "")
    s = s.rstrip("ḥ").strip()
    return " ".join(s.split())


def load_names(path: Path) -> dict:
    """names.csv → folded-key → list of (raw_compound, split, arity, freq_sum)."""
    idx: dict[str, list[tuple]] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split(";")
            if len(parts) < 3:
                continue
            raw = parts[0].strip()
            split = parts[1].strip()
            try:
                arity = int(parts[2])
            except ValueError:
                continue
            freq = 0
            for cell in parts[3:]:
                cell = cell.strip()
                if cell.isdigit():
                    freq += int(cell)
            idx.setdefault(form_key(raw), []).append((raw, split, arity, freq))
    return idx


def load_splits(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as f:
        header = f.readline().rstrip("\n").split("\t")
        assert header[:2] == ["headword_slp1", "headword_iast"], header
        for line in f:
            c = line.rstrip("\n").split("\t")
            rows.append(dict(zip(header, c)))
    return rows


def crosscheck(rows, idx) -> tuple[list[dict], dict]:
    out = []
    stats = Counter()
    keys = sorted(idx)
    for r in rows:
        hw = r["headword_iast"]
        key = form_key(hw)
        hits = idx.get(key, [])
        stats["rows"] += 1
        if not hits:
            # prefix evidence: any attested form starting with this stem?
            # (inflected form `anubandhabhayāt` for stem `anubandhabhaya`,
            #  or a longer compound sharing the stem — weak, ambiguous signal)
            i = bisect.bisect_left(keys, key)
            pref = 0
            while i < len(keys) and keys[i].startswith(key):
                pref += 1
                i += 1
            stats["prefix_evidence" if pref else "unattested"] += 1
            out.append(dict(r, dcs_status="prefix-evidence" if pref else "unattested",
                            dcs_compound_raw="", dcs_prefix_hits=str(pref),
                            dcs_split="", dcs_arity="", dcs_freq_sum="",
                            seam_no_sandhi="", key_form="folded-miss"))
            continue
        # pick highest-frequency attestation as the representative hit
        raw, split, arity, freq = max(hits, key=lambda h: h[3])
        exact = any(h[0] == hw for h in hits)
        stats["attested"] += 1
        stats["attested_exact_form" if exact else "attested_folded_only"] += 1
        if int(r["arity"]) == arity:
            stats["arity_agree"] += 1
        else:
            stats["arity_disagree"] += 1
        concat = form_key("".join(r["members_iast"].split("+"))).replace(" ", "")
        no_sandhi = "1" if concat == key else "0"
        stats["seam_no_sandhi" if no_sandhi == "1" else "seam_sandhi"] += 1
        out.append(dict(r, dcs_status="attested", dcs_compound_raw=raw,
                        dcs_prefix_hits="0",
                        dcs_split=split, dcs_arity=str(arity),
                        dcs_freq_sum=str(freq), seam_no_sandhi=no_sandhi,
                        key_form="exact" if exact else "folded"))
    return out, dict(stats)


def write_tsv(out, path):
    cols = ["headword_slp1", "headword_iast", "L_id", "arity",
            "members_slp1", "members_iast", "dcs_status", "dcs_compound_raw",
            "dcs_prefix_hits", "dcs_split", "dcs_arity", "dcs_freq_sum",
            "seam_no_sandhi", "key_form"]
    with path.open("w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for r in out:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")


def selftest():
    assert form_key("mahābalaḥ") == form_key("mahābala")
    assert form_key("caṁdrā") == form_key("caṃdrā") == "caṃdrā"
    assert form_key("rā’mā") == "rāmā"
    # seam logic
    assert form_key("".join("ā + bherī".split("+"))).replace(" ", "") == form_key("ābherī")
    assert form_key("".join("ābharant + vasu".split("+"))).replace(" ", "") != form_key("ābharadvasu")
    tmp = Path("/tmp/h4712_selftest_names.csv")
    tmp.write_text("mahābalaḥ; mahat bala;2;7;1\nrājendra; rājan indra;2;9;0\n",
                   encoding="utf-8")
    d = load_names(tmp)
    assert form_key("mahābala") in d and form_key("rājendra") in d
    rows = load_splits(SPLITS)
    assert rows and "members_iast" in rows[0]
    tmp.unlink()
    print("selftest PASS")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return
    names_path = next((p for p in NAMES_CANDIDATES if p.exists()), None)
    if names_path is None:
        sys.exit(f"names.csv not found in any of: {NAMES_CANDIDATES}")
    idx = load_names(names_path)
    rows = load_splits(SPLITS)
    out, stats = crosscheck(rows, idx)
    write_tsv(out, OUT_TSV)
    summary = {
        "study": "PWG compound-split layer × DCS attested compounds (census A6, H4712)",
        "as_of": "2026-09-15",
        "pwg_layer": str(SPLITS.relative_to(REPO)),
        "dcs_source": str(names_path.relative_to(REPO.parent)),
        "dcs_keys": len(idx),
        "pwg_rows": stats.get("rows", 0),
        "attested": stats.get("attested", 0),
        "prefix_evidence": stats.get("prefix_evidence", 0),
        "unattested": stats.get("unattested", 0),
        "attested_exact_form": stats.get("attested_exact_form", 0),
        "attested_folded_only": stats.get("attested_folded_only", 0),
        "arity_agree": stats.get("arity_agree", 0),
        "arity_disagree": stats.get("arity_disagree", 0),
        "seam_no_sandhi": stats.get("seam_no_sandhi", 0),
        "seam_sandhi": stats.get("seam_sandhi", 0),
    }
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
