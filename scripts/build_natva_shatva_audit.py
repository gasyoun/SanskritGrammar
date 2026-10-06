#!/usr/bin/env python3
"""build_natva_shatva_audit.py — H6054: ṇatva/śaṭva rule-vs-fact coverage audit.

Compares the Paninian ṇatva/śaṭva rules as materialised by kosha's H185
"hybrid-natva-fix" layer (vidyut-prakriya derivations, MG-ruled HYBRIDIZE
05-07-2026) against the FACTS shipped by MWinflect + csl-inflect
(`cologne_mwinflect` rows in kosha.db, ingested verbatim from
MWinflect/nominals/pysanskritv2/tables/calc_tables.txt — the exact file
csl-inflect's own sqlite/lgtab1/lgtab2 builders consume; sha256-pinned in
kosha.db meta.build_source_lock).

Audit universe (the H185 characterization draft): the E1 top-10k frequency
sample — reproduced set-equivalently to scripts/compare_vidyut_cologne.py
--limit 10000 (entries-joined, rank_all-ordered; see reproduce_sample for the
linear rebuild and its ≤1-lemma boundary note) — intersected with the
ṇatva-fix rows. Expected per E1_DIVERGENCE_REPORT.md: 89 stems / 326 cells.

Per-cell outputs (data/natva_shatva_rule_audit/):
  natva_cells_matrix.tsv — one row per affected cell: rule form (vidyut fix),
      MWinflect/csl-inflect fact (DB + raw calc_tables.txt line), n↔ṇ-only
      re-verification, śaṭva (s→ṣ) evidence from the same paradigm, rule-class.
  shatva_coverage_check.tsv — per affected paradigm: loc.pl form(s) from the
      shipped table (śaṭva applied by MWinflect) + the re-verified natva-only
      property of the fix cells (⇒ śaṭva forms untouched by the fix).
  coverage_matrix.md — rule × engine coverage matrix + divergence taxonomy.
  summary.json — machine-readable rollup.

Inputs (all read-only):
  kosha.db (data/db/kosha.db), MWinflect calc_tables.txt (hash-checked
  against the DB's build_source_lock pin), diff_nopada_m_a.txt (recovered
  from MWinflect git 2c512cc; the MWinflect#6 818-stem with/without-pada
  diff list drdhaval2785 analysed).

Usage:
  python3 scripts/build_natva_shatva_audit.py            # defaults
  python3 scripts/build_natva_shatva_audit.py --db ... --calc-tables ...
"""
import argparse
import hashlib
import json
import re
import sqlite3
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DB = Path("/Users/mac/Documents/GitHub/kosha/data/db/kosha.db")
DEFAULT_CALC = Path("/Users/mac/Documents/GitHub/MWinflect/nominals/pysanskritv2/tables/calc_tables.txt")
DEFAULT_NOPADA = REPO / "data" / "natva_shatva_rule_audit" / "inputs" / "diff_nopada_m_a.txt"
OUT_DIR = REPO / "data" / "natva_shatva_rule_audit"

SAMPLE_LIMIT = 10000  # the E1 characterization sample (H185)

# SLP1 vowels (for the monosyllabic-final-member test drdhaval2785 posted on
# MWinflect#6; regex from the issue thread, applied to the hyphenated stem).
VOWELS = "aAiIuUfFxXeEoO"
MONO_FINAL_RE = re.compile(r"[-][^%s]*[%s][^%s]*$" % (VOWELS, VOWELS, VOWELS))
R_CLASS = set("rfFR")  # SLP1 retroflexion triggers: r, ṛ(f), ṝ(F) — 8.4.1 + ṛ-vārttika

CASES = ["nom", "acc", "instr", "dat", "abl", "gen", "loc", "voc"]
NUMBERS = ["sg", "du", "pl"]


def open_db(db_path: Path) -> sqlite3.Connection:
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    return con


def check_calc_hash(con, calc_path: Path) -> str:
    """Verify the calc_tables.txt we read is the exact file the DB ingested."""
    pin = json.loads(con.execute(
        "SELECT value FROM meta WHERE key='build_source_lock'").fetchone()[0])
    expected = pin["mwinflect_nominals"]["sha256"]
    got = hashlib.sha256(calc_path.read_bytes()).hexdigest()
    if got != expected:
        sys.exit(f"FATAL: calc_tables.txt sha256 {got} != DB pin {expected}")
    return expected


def reproduce_sample(con, limit: int):
    """Set-equivalent reproduction of the E1 select_stems top-`limit` sample.

    The original SQL (DISTINCT inflections⋈entries⋈lemmas ORDER BY rank_all)
    materialises too slowly on the current 6.9M-row DB, so we rebuild the same
    tuple set linearly: rank lemmas exactly as the SQL ordered them, keep only
    lemmas with a dict entry, and emit each lemma's nominal (lemma, model,
    gender) paradigms in order until `limit` tuples are reached. Whole-lemma
    batches are emitted (the original could cut mid-lemma at the boundary —
    a ≤1-lemma wobble documented in the README).
    """
    ranked = con.execute(
        "SELECT slp1, rank_all FROM lemmas ORDER BY (rank_all IS NULL), "
        "rank_all ASC, slp1 ASC").fetchall()
    entries = {r[0] for r in con.execute("SELECT slp1_key FROM entries")}
    nominal = defaultdict(list)  # lemma -> [(model, gender), ...]
    n = 0
    cur = con.execute(
        "SELECT lemma_slp1, model, gender FROM inflections "
        "WHERE person IS NULL AND gender IN ('m','n','f')")
    while True:
        batch = cur.fetchmany(500000)
        if not batch:
            break
        for lemma, model, gender in batch:
            if (model, gender) not in nominal[lemma]:
                nominal[lemma].append((model, gender))
        n += len(batch)
    print(f"[H6054] paradigm scan done: {n:,} nominal rows, {len(nominal):,} lemmas")
    sample = set()
    emitted = 0
    for lem, rank in ranked:  # already in the SQL's order
        if emitted >= limit:
            break
        if lem not in entries or lem not in nominal:
            continue
        for model, gender in sorted(nominal[lem]):
            sample.add((lem, model))
            emitted += 1
    return sample


def load_calc_stems(calc_path: Path) -> dict:
    """{(model, dehyphenated stem): hyphenated stem} from calc_tables.txt."""
    out = {}
    with open(calc_path, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            model, stem = parts[0], parts[1]
            out.setdefault((model, stem.replace("-", "")), stem)
    return out


def load_nopada(path: Path) -> set:
    stems = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith(";"):
            stems.add(line)
    return stems


def classify(hyphenated: str) -> tuple:
    """Surface rule classification of one affected paradigm.

    Returns (class_code, has_hyphen, r_in_final, r_in_prefix, mono_final,
    in_818_list) — the raw features plus a class label:
      A_compound_mono_final  — compound, r/ṛ in a non-final member, final
                               member monosyllabic → Pāṇini 8.4.12 antaraṅga
                               (the MWinflect#6 / drdhaval2785 "69" class).
      B_key2_split           — key2 hyphen present, final member polysyllabic
                               (e.g. upasarga splits like pra-Bu-tvAkzepa-type
                               or single-pada stems split as pra-Bu) — the
                               with-pada algorithm suppresses ṇatva although
                               the analysis is one pada / not final-member.
      C_r_in_final           — r/ṛ inside the FINAL member too (inspection
                               bucket; intra-final-pada ṇ expected to agree).
      D_no_hyphen            — no pada split in key2 (inspection bucket).
    """
    has_hyphen = "-" in hyphenated
    if has_hyphen:
        final_seg = hyphenated.rsplit("-", 1)[1]
        prefix = hyphenated.rsplit("-", 1)[0]
        r_final = bool(set(final_seg) & R_CLASS)
        r_prefix = bool(set(prefix) & R_CLASS)
        mono_final = bool(MONO_FINAL_RE.search(hyphenated))
        if r_prefix and not r_final and mono_final:
            cls = "A_compound_mono_final_8_4_12"
        elif r_prefix and not r_final:
            cls = "B_key2_split"
        else:
            cls = "C_r_in_final"
    else:
        final_seg, prefix = hyphenated, ""
        r_final = bool(set(hyphenated) & R_CLASS)
        r_prefix, mono_final = False, False
        cls = "D_no_hyphen"
    return cls, has_hyphen, r_final, r_prefix, mono_final


def attested(con, form: str) -> int:
    """DCS-corpus attestation rows for a surface form (kosha `forms` table,
    built from SanskritRussian/dcs_form2lemma.tsv — sha-pinned in build lock)."""
    return con.execute("SELECT COUNT(*) FROM forms WHERE form_slp1=?",
                       (form,)).fetchone()[0]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--calc-tables", type=Path, default=DEFAULT_CALC)
    ap.add_argument("--nopada", type=Path, default=DEFAULT_NOPADA)
    ap.add_argument("--out", type=Path, default=OUT_DIR)
    args = ap.parse_args()

    t0 = time.time()
    con = open_db(args.db)
    sha = check_calc_hash(con, args.calc_tables)
    print(f"[H6054] calc_tables.txt sha256 matches DB pin: {sha[:16]}…")

    calc_stems = load_calc_stems(args.calc_tables)
    nopada = load_nopada(args.nopada) if args.nopada.exists() else set()
    print(f"[H6054] calc stems loaded: {len(calc_stems):,}; nopada-818 list: {len(nopada)}")

    sample = reproduce_sample(con, SAMPLE_LIMIT)
    print(f"[H6054] E1 top-{SAMPLE_LIMIT} sample reproduced: {len(sample)} paradigms")

    # --- collect natva-fix cells inside the sample -------------------------
    fix_rows = con.execute(
        "SELECT lemma_slp1, model, gender, gcase, number, form_slp1 "
        "FROM inflections WHERE source='hybrid-natva-fix'").fetchall()
    cells = []
    for r in fix_rows:
        if (r["lemma_slp1"], r["model"]) not in sample:
            continue
        key = (r["lemma_slp1"], r["model"], r["gender"], r["gcase"], r["number"])
        cells.append((key, r["form_slp1"]))
    fix_map = defaultdict(set)
    for key, form in cells:
        fix_map[key].add(form)

    # cologne facts for the same cells
    col_map = defaultdict(set)
    for r in con.execute(
        "SELECT lemma_slp1, model, gender, gcase, number, form_slp1 "
        "FROM inflections WHERE source='cologne_mwinflect' AND person IS NULL"):
        key = (r["lemma_slp1"], r["model"], r["gender"], r["gcase"], r["number"])
        if key in fix_map:
            col_map[key].add(r["form_slp1"])

    # raw calc_tables.txt data for exactly the affected (model, lemma) pairs
    needed = {(k[1], k[0]) for k in fix_map}  # (model, lemma) — key order of raw_lines
    raw_lines = {}
    with open(args.calc_tables, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 4:
                continue
            model, stem, data = parts[0], parts[1], parts[3]
            pair = (model, stem.replace("-", ""))
            if pair in needed and pair not in raw_lines:
                raw_lines[pair] = data

    # loc.pl (śaṭva evidence) from the shipped tables, model-agnostic via DB
    loc_pl_map = defaultdict(set)
    affected_paradigms = {(k[0], k[1], k[2]) for k in fix_map}
    for r in con.execute(
        "SELECT lemma_slp1, model, gender, form_slp1 FROM inflections "
        "WHERE source='cologne_mwinflect' AND person IS NULL AND gcase='loc' "
        "AND number='pl'"):
        p = (r["lemma_slp1"], r["model"], r["gender"])
        if p in affected_paradigms:
            loc_pl_map[p].add(r["form_slp1"])

    # --- build the per-cell matrix -----------------------------------------
    rows_out = []
    class_counts = Counter()
    model_counts = Counter()
    case_counts = Counter()
    natva_only_ok = natva_only_fail = 0
    raw_line_ok = raw_line_miss = 0
    stems_affected = set()

    for key in sorted(fix_map, key=lambda k: (k[0], k[1], k[2], k[3], k[4])):
        lemma, model, gender, gcase, number = key
        vid = fix_map[key]
        col = col_map.get(key, set())
        # re-verify the n↔ṇ-only property (is_natva_diff, E1 engine)
        if col and vid and {f.replace("R", "n") for f in vid} == {f.replace("R", "n") for f in col}:
            natva_only_ok += 1
            natva_only = "yes"
        else:
            natva_only_fail += 1
            natva_only = "NO"
        hyph = calc_stems.get((model, lemma), lemma)
        in818 = hyph in nopada
        cls, has_hyph, r_fin, r_pre, mono_fin = classify(hyph)
        class_counts[cls] += 1
        model_counts[model] += 1
        case_counts[f"{gcase}.{number}"] += 1
        stems_affected.add((lemma, model))
        # raw line check: every cologne fact form present in a slot of the
        # shipped calc_tables.txt line (slots ':'-separated, variants '/')
        data = raw_lines.get((model, lemma))
        if data is None:
            raw_line_miss += 1
            raw_ok = "line-missing"
        else:
            present = all(
                any(f in slot.split("/") for slot in data.split(":")) for f in col)
            raw_ok = "yes" if present else "NO"
            raw_line_ok += int(present)
            raw_line_miss += int(not present)
        # śaṭva evidence from this paradigm's loc.pl (shipped table)
        loc = loc_pl_map.get((lemma, model, gender), set())
        shatva = "z-applied" if any("z" in f for f in loc) else ("no-z" if loc else "no-loc.pl-row")
        # DCS-corpus attestation: the ṇ-form(s) vs the shipped n-form(s)
        att_R = sum(attested(con, f) for f in vid)
        att_n = sum(attested(con, f) for f in col)
        rows_out.append({
            "lemma_slp1": lemma, "model": model, "gender": gender,
            "cell": f"{gcase}.{number}",
            "rule_form_vidyut": "|".join(sorted(vid)),
            "fact_mwinflect_csl": "|".join(sorted(col)),
            "natva_only_diff_reverified": natva_only,
            "rule_class": cls,
            "hyphenated_stem_key2": hyph,
            "final_member_mono": str(mono_fin).lower(),
            "r_trigger_in_final_member": str(r_fin).lower(),
            "r_trigger_in_prefix": str(r_pre).lower(),
            "in_mwinflect6_818_list": str(in818).lower(),
            "raw_calc_line_check": raw_ok,
            "shatva_loc_pl_in_table": shatva,
            "shatva_loc_pl_form": "|".join(sorted(loc)),
            "dcs_rows_rule_R_form": att_R,
            "dcs_rows_fact_n_form": att_n,
        })

    # --- write artifacts ----------------------------------------------------
    args.out.mkdir(parents=True, exist_ok=True)
    cols = list(rows_out[0].keys()) if rows_out else []
    with open(args.out / "natva_cells_matrix.tsv", "w", encoding="utf-8") as f:
        f.write("\t".join(cols) + "\n")
        for r in rows_out:
            f.write("\t".join(str(r[c]) for c in cols) + "\n")

    shatva_rows = []
    for p in sorted(affected_paradigms):
        lemma, model, gender = p
        loc = loc_pl_map.get(p, set())
        hyph = calc_stems.get((model, lemma), lemma)
        cls, *_ = classify(hyph)
        shatva_rows.append({
            "lemma_slp1": lemma, "model": model, "gender": gender,
            "rule_class": cls,
            "loc_pl_mwinflect_csl": "|".join(sorted(loc)),
            "shatva_s_to_z_applied": "yes" if any("z" in f for f in loc) else ("n/a" if not loc else "NO"),
        })
    with open(args.out / "shatva_coverage_check.tsv", "w", encoding="utf-8") as f:
        f.write("\t".join(shatva_rows[0].keys()) + "\n")
        for r in shatva_rows:
            f.write("\t".join(str(r[c]) for c in shatva_rows[0].keys()) + "\n")

    # stem-level rollup (89 paradigms): 818-list and 69-regex-class overlap
    stem_stats = {"stems_in_818_list": 0, "stems_mono_final_class": 0,
                  "stems_m_a": 0}
    seen_hyph = set()
    for (lemma, model) in stems_affected:
        hyph = calc_stems.get((model, lemma), lemma)
        if hyph in seen_hyph:
            continue
        seen_hyph.add(hyph)
        if hyph in nopada:
            stem_stats["stems_in_818_list"] += 1
        if MONO_FINAL_RE.search(hyph):
            stem_stats["stems_mono_final_class"] += 1
        if model == "m_a":
            stem_stats["stems_m_a"] += 1

    summary = {
        "handoff": "H6054",
        "sample_limit": SAMPLE_LIMIT,
        "sample_paradigms": len(sample),
        "natva_cells": len(rows_out),
        "natva_stems_paradigms": len(stems_affected),
        "natva_stems_lemmas": len({l for l, _ in stems_affected}),
        "natva_only_reverified": {"ok": natva_only_ok, "fail": natva_only_fail},
        "raw_line_check": {"ok": raw_line_ok, "miss_or_fail": raw_line_miss},
        "rule_classes": dict(class_counts),
        "models": dict(model_counts),
        "stem_level": stem_stats,
        "cells_by_case": dict(case_counts),
        "calc_tables_sha256": sha,
        "elapsed_s": round(time.time() - t0, 1),
    }
    (args.out / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"[H6054] wrote {args.out}/ (matrix rows: {len(rows_out)})")


if __name__ == "__main__":
    main()
