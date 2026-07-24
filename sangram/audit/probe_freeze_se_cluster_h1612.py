#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""H1612 — W1-A1 freeze-exit C6 probes for the SE unknown cluster.

Writes per-article artifacts under sangram/audit/:

  probe_freeze_<slug>.py   (thin re-runnable wrapper → this runner, --only=slug)
  probe_freeze_<slug>.json
  probe_freeze_<slug>.md

and updates sangram/editorial/data/consolidation_ledger.json dispositions.

Rule (plan fence): never invent kill thresholds. Only C6 § 7 pilot kill-gates
carry numeric criteria. Non-pilot SE slots get integrity re-derive + blocking_note.

Model: Grok 4.5 (grok-4.5) — user-launched override of Opus 4.8, 24-07-2026.
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
AUDIT = ROOT / "sangram" / "audit"
LEDGER_PATH = ROOT / "sangram" / "editorial" / "data" / "consolidation_ledger.json"
DEFAULT_DB = Path(
    r"C:\Users\user\Documents\GitHub\VisualDCS\src\DCS-data-2026\dcs_full.sqlite"
)
PIN = "04e0778d3dc971030229179e25eea043d06ff397"
TODAY = date.today().isoformat()
PROVENANCE = {
    "handoff": "H1612",
    "model": "Grok 4.5 (grok-4.5)",
    "intended_executor": "Opus 4.8 (claude-opus-4-8) — user-launched override",
    "date": "2026-07-24",
    "plan": "docs/PLAN_SANSKRITGRAMMAR_FREEZE_EXIT_METHODICHKA_2026H2.md § A1",
}

# Inline matrix (H1611 A0 not yet on origin/main — proceed per Implementation § A1).
# Criteria quoted from sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx § 7 only.
# Non-pilot rows: criterion_status = MISSING (do not invent).
SE_CLUSTER = [
    {
        "toc_ref": "SG-SE-001",
        "art_id": "art:case-system-overview",
        "slug": "case-system-overview",
        "script": "scripts/sg_se_001_case_overview.py",
        "coverage": "sangram/articles/case-system-overview/data/coverage_summary.json",
        "c6_slot": "sem-a-case-overview",
        "pilot": None,
        "criterion_status": "MISSING",
        "criterion_quoted": None,
        "criterion_source": (
            "C6 § 7 pilots are only P1–P5; sem-a-case-overview is not a pilot. "
            "No numeric kill-gate in SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx § 7."
        ),
        "integrity_keys": "case_vibhakti",
    },
    {
        "toc_ref": "SG-SE-002",
        "art_id": "art:nominative-accusative",
        "slug": "nominative-accusative",
        "script": "scripts/sg_se_002_nom_acc.py",
        "coverage": "sangram/articles/nominative-accusative/data/coverage_summary.json",
        "c6_slot": "sem-a (Nom/Acc sub-article of case cluster)",
        "pilot": None,
        "criterion_status": "MISSING",
        "criterion_quoted": None,
        "criterion_source": (
            "C6 § 7 has no pilot for Nom/Acc. Not inventing a functional-split threshold "
            "from E1 deprel-partial notes."
        ),
        "integrity_keys": "nom_acc",
    },
    {
        "toc_ref": "SG-SE-003",
        "art_id": "art:instrumental-dative",
        "slug": "instrumental-dative",
        "script": "scripts/sg_se_003_instrumental_dative.py",
        "coverage": "sangram/articles/instrumental-dative/data/coverage_summary.json",
        "c6_slot": "sem-a-instrumental / sem-a-dative-experiencer",
        "pilot": None,
        "criterion_status": "MISSING",
        "criterion_quoted": None,
        "criterion_source": (
            "C6 § 7 has no pilot for Ins/Dat. Agent-proxy / deprel limits are honesty notes, "
            "not kill thresholds."
        ),
        "integrity_keys": "ins_dat",
    },
    {
        "toc_ref": "SG-SE-004",
        "art_id": "art:ablative-genitive",
        "slug": "ablative-genitive",
        "script": "scripts/sg_se_004_abl_gen.py",
        "coverage": "sangram/articles/ablative-genitive/data/coverage_summary.json",
        "c6_slot": "sem-a-genitive (+ Abl)",
        "pilot": None,
        "criterion_status": "MISSING",
        "criterion_quoted": None,
        "criterion_source": (
            "C6 § 7 has no pilot for Abl/Gen. Gen-absolute candidate≠construction is a limit, "
            "not a kill-gate threshold."
        ),
        "integrity_keys": "abl_gen",
    },
    {
        "toc_ref": "SG-SE-005",
        "art_id": "art:locative",
        "slug": "locative",
        "script": "scripts/sg_se_005_locative.py",
        "coverage": "sangram/articles/locative/data/coverage_summary.json",
        "c6_slot": "sem-a-locative",
        "pilot": None,
        "criterion_status": "MISSING",
        "criterion_quoted": None,
        "criterion_source": (
            "C6 § 7 P1 kill-gate belongs to syn-c-locative-absolute (construction pilot), "
            "not to SG-SE-005 sem-a-locative. Do not transfer P1's <80% retrieval threshold "
            "to this slot without a programme revision."
        ),
        "integrity_keys": "loc",
    },
    {
        "toc_ref": "SG-SE-006",
        "art_id": "art:past-tenses",
        "slug": "past-tenses",
        "script": "scripts/sg_se_006_past_tenses.py",
        "coverage": "sangram/articles/past-tenses/data/coverage_summary.json",
        "c6_slot": "sem-b-past-competition",
        "pilot": "P2",
        "criterion_status": "QUOTED",
        "criterion_quoted": (
            "Родные теги различают три претерита в <95% выборки → количественная часть "
            "снимается, статья публикует честный отрицательный результат"
        ),
        "criterion_source": (
            "sangram/SANGRAM_SYNTAX_SEMANTICS_PROGRAM_W3_W4.mdx § 7 row P2 "
            "(sem-b-past-competition)"
        ),
        "integrity_keys": "past",
    },
    {
        "toc_ref": "SG-SE-008",
        "art_id": "art:imperative-optative",
        "slug": "imperative-optative",
        "script": "scripts/sg_se_008_imperative_optative.py",
        "coverage": "sangram/articles/imperative-optative/data/coverage_summary.json",
        "c6_slot": "sem-b-optative / sem-b-imperative",
        "pilot": None,
        "criterion_status": "MISSING",
        "criterion_quoted": None,
        "criterion_source": (
            "C6 § 7 has no pilot for Imp/Opt (slots exist in § 6 SEM-B but are not P1–P5). "
            "feat_mood is native; no programme kill threshold named."
        ),
        "integrity_keys": "imp_opt",
    },
    {
        "toc_ref": "SG-SE-013",
        "art_id": "art:karaka-case",
        "slug": "karaka-case",
        "script": "scripts/sg_se_013_karaka_case.py",
        "coverage": "sangram/articles/karaka-case/data/coverage_summary.json",
        "c6_slot": "sem-a-karaka-vs-case",
        "pilot": None,
        "criterion_status": "MISSING",
        "criterion_quoted": None,
        "criterion_source": (
            "C6 § 7 has no pilot for kāraka↔case. E1 (no classical dependency trees) is a "
            "method rule (manual ≥100), not a freeze kill threshold — not inventing one."
        ),
        "integrity_keys": "karaka",
    },
]

AORIST_FORMS = ("root", "them", "s", "is", "red", "sa", "sis")
FINITE = "upos='VERB' AND feat_verbform IS NULL"


def load_json(rel: str) -> dict:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def connect(db: Path) -> sqlite3.Connection:
    if not db.exists():
        raise SystemExit(f"DCS master not found: {db}")
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    prov = dict(con.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        raise SystemExit("master has no provenance pin — refusing (C3 §2.1)")
    return con


def integrity_case_vibhakti(cur, cov: dict) -> dict:
    expected = {
        r["case"]: r["tokens"] for r in cov["case_system_native"]["eight_vibhakti"]
    }
    expected["Cpd"] = cov["case_system_native"].get("compound_pseudo_case_Cpd")
    live = {
        c: n
        for c, n in cur.execute(
            "SELECT feat_case, COUNT(*) FROM token WHERE feat_case IS NOT NULL "
            "GROUP BY feat_case"
        )
    }
    checks = {}
    for case, exp in expected.items():
        if exp is None:
            continue
        got = live.get(case)
        checks[case] = {"expected": exp, "live": got, "match": got == exp}
    return {
        "kind": "feat_case eight vibhakti (+ Cpd)",
        "all_match": all(v["match"] for v in checks.values()),
        "checks": checks,
    }


def integrity_nom_acc(cur, cov: dict) -> dict:
    tn = cov["totals_native"]
    exp_nom = tn["nom"]
    exp_acc = tn["acc"]
    live_nom = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Nom'"
    ).fetchone()[0]
    live_acc = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Acc'"
    ).fetchone()[0]
    checks = {
        "Nom": {"expected": exp_nom, "live": live_nom, "match": live_nom == exp_nom},
        "Acc": {"expected": exp_acc, "live": live_acc, "match": live_acc == exp_acc},
    }
    return {
        "kind": "Nom/Acc feat_case totals",
        "source": "coverage_summary.totals_native",
        "all_match": all(v["match"] for v in checks.values()),
        "checks": checks,
    }


def integrity_ins_dat(cur, cov: dict) -> dict:
    ins = cov.get("instrumental", {})
    dat = cov.get("dative", {})
    exp_ins = ins.get("total") or ins.get("tokens")
    exp_dat = dat.get("total") or dat.get("tokens")
    if exp_ins is None:
        exp_ins, exp_dat = 277143, 65423
        source = "fallback published vibhakti"
    else:
        source = "coverage_summary"
    live_ins = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Ins'"
    ).fetchone()[0]
    live_dat = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Dat'"
    ).fetchone()[0]
    checks = {
        "Ins": {"expected": exp_ins, "live": live_ins, "match": live_ins == exp_ins},
        "Dat": {"expected": exp_dat, "live": live_dat, "match": live_dat == exp_dat},
    }
    return {
        "kind": "Ins/Dat feat_case totals",
        "source": source,
        "all_match": all(v["match"] for v in checks.values()),
        "checks": checks,
    }


def integrity_abl_gen(cur, cov: dict) -> dict:
    abl = cov.get("ablative", {})
    gen = cov.get("genitive", {})
    exp_abl = abl.get("total") or abl.get("tokens")
    exp_gen = gen.get("total") or gen.get("tokens")
    if exp_abl is None:
        exp_abl, exp_gen = 74565, 270763
        source = "fallback published vibhakti"
    else:
        source = "coverage_summary"
    live_abl = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Abl'"
    ).fetchone()[0]
    live_gen = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Gen'"
    ).fetchone()[0]
    checks = {
        "Abl": {"expected": exp_abl, "live": live_abl, "match": live_abl == exp_abl},
        "Gen": {"expected": exp_gen, "live": live_gen, "match": live_gen == exp_gen},
    }
    return {
        "kind": "Abl/Gen feat_case totals",
        "source": source,
        "all_match": all(v["match"] for v in checks.values()),
        "checks": checks,
    }


def integrity_loc(cur, cov: dict) -> dict:
    exp_loc = cov["denominators"]["locative_total"]
    exp_part = cov["locative_absolute_candidate"]["loc_participle_candidate"]
    live_loc = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Loc'"
    ).fetchone()[0]
    live_part = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Loc' AND feat_verbform='Part'"
    ).fetchone()[0]
    checks = {
        "Loc": {"expected": exp_loc, "live": live_loc, "match": live_loc == exp_loc},
        "Loc+Part": {
            "expected": exp_part,
            "live": live_part,
            "match": live_part == exp_part,
        },
    }
    return {
        "kind": "Loc totals + Loc+Part absolute candidate",
        "source": "coverage_summary",
        "all_match": all(v["match"] for v in checks.values()),
        "checks": checks,
    }


def integrity_past(cur, cov: dict) -> dict:
    exp_finite = cov["finite_with_tense"]
    exp_impf = cov["imperfect"]
    exp_past = cov["past_bucket_total"]
    exp_aor = cov["aorist_finite"]
    exp_peri = cov["perfect_periphrastic"]
    exp_none = cov["perfect_simple_untagged_bucket"]
    live_finite = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINITE} AND feat_tense IS NOT NULL "
        "AND feat_tense<>''"
    ).fetchone()[0]
    live_impf = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINITE} AND feat_tense='Impf'"
    ).fetchone()[0]
    live_past = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINITE} AND feat_tense='Past'"
    ).fetchone()[0]
    ph = ",".join("?" * len(AORIST_FORMS))
    live_aor = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINITE} AND feat_tense='Past' "
        f"AND feat_formation IN ({ph})",
        AORIST_FORMS,
    ).fetchone()[0]
    live_peri = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINITE} AND feat_tense='Past' "
        "AND feat_formation='peri'"
    ).fetchone()[0]
    live_none = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINITE} AND feat_tense='Past' "
        "AND feat_formation IS NULL"
    ).fetchone()[0]
    checks = {
        "finite_with_tense": {
            "expected": exp_finite,
            "live": live_finite,
            "match": live_finite == exp_finite,
        },
        "Impf": {"expected": exp_impf, "live": live_impf, "match": live_impf == exp_impf},
        "Past": {"expected": exp_past, "live": live_past, "match": live_past == exp_past},
        "aorist_formation": {
            "expected": exp_aor,
            "live": live_aor,
            "match": live_aor == exp_aor,
        },
        "peri": {"expected": exp_peri, "live": live_peri, "match": live_peri == exp_peri},
        "Past_None": {
            "expected": exp_none,
            "live": live_none,
            "match": live_none == exp_none,
        },
    }
    return {
        "kind": "SE-006 past-tense census",
        "all_match": all(v["match"] for v in checks.values()),
        "checks": checks,
        "live": {
            "finite_with_tense": live_finite,
            "Impf": live_impf,
            "Past": live_past,
            "aorist": live_aor,
            "peri": live_peri,
            "Past_None": live_none,
        },
    }


def integrity_imp_opt(cur, cov: dict) -> dict:
    exp_imp = cov["imperative"]["total"]
    exp_opt = cov["optative"]["total"]
    live_imp = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINITE} AND feat_mood='Imp'"
    ).fetchone()[0]
    live_opt = cur.execute(
        f"SELECT COUNT(*) FROM token WHERE {FINITE} AND feat_mood='Opt'"
    ).fetchone()[0]
    checks = {
        "Imp": {"expected": exp_imp, "live": live_imp, "match": live_imp == exp_imp},
        "Opt": {"expected": exp_opt, "live": live_opt, "match": live_opt == exp_opt},
    }
    return {
        "kind": "feat_mood Imp/Opt totals",
        "all_match": all(v["match"] for v in checks.values()),
        "checks": checks,
    }


def integrity_karaka(cur, cov: dict) -> dict:
    exp_total = cov.get("total_tokens")
    exp_deprel = cov.get("deprel_nonnull")
    live_total = cur.execute("SELECT COUNT(*) FROM token").fetchone()[0]
    live_deprel = cur.execute(
        "SELECT COUNT(*) FROM token WHERE deprel IS NOT NULL AND deprel<>''"
    ).fetchone()[0]
    checks = {
        "total_tokens": {
            "expected": exp_total,
            "live": live_total,
            "match": live_total == exp_total,
        },
        "deprel_nonnull": {
            "expected": exp_deprel,
            "live": live_deprel,
            "match": live_deprel == exp_deprel,
        },
    }
    return {
        "kind": "token total + deprel coverage base",
        "all_match": all(v["match"] for v in checks.values()),
        "checks": checks,
        "deprel_coverage_pct_live": round(100.0 * live_deprel / live_total, 4),
    }


INTEGRITY_FNS = {
    "case_vibhakti": integrity_case_vibhakti,
    "nom_acc": integrity_nom_acc,
    "ins_dat": integrity_ins_dat,
    "abl_gen": integrity_abl_gen,
    "loc": integrity_loc,
    "past": integrity_past,
    "imp_opt": integrity_imp_opt,
    "karaka": integrity_karaka,
}


def apply_p2_killgate(integrity: dict) -> dict:
    """C6 § 7 P2 operationalisation.

    Universe = finite verbs with native past-ish tense (feat_tense in {Impf, Past}).
    A token is 'natively assigned to one classical preterite' iff:
      - Impf  (imperfect, clean tag), OR
      - Past + aorist formation (aorist), OR
      - Past + peri (periphrastic perfect only — the only natively tagged perfect).
    Past+None (simple/reduplicated perfect + residue) is NOT natively assigned.
    Kill-gate fires when assigned_share < 0.95.
    """
    live = integrity["live"]
    universe = live["Impf"] + live["Past"]
    assigned = live["Impf"] + live["aorist"] + live["peri"]
    share = assigned / universe if universe else 0.0
    threshold = 0.95
    fires = share < threshold
    return {
        "criterion_quoted": SE_CLUSTER[5]["criterion_quoted"],
        "criterion_source": SE_CLUSTER[5]["criterion_source"],
        "operationalisation": (
            "universe = count(finite ∧ feat_tense ∈ {Impf, Past}); "
            "assigned = Impf + (Past∧aorist-formation) + (Past∧peri); "
            "share = assigned/universe; fire if share < 0.95"
        ),
        "universe": universe,
        "assigned": assigned,
        "unassigned_Past_None": live["Past_None"],
        "share": round(share, 6),
        "share_pct": round(100.0 * share, 2),
        "threshold": threshold,
        "gate_fires": fires,
        "programme_consequence_if_fires": (
            "количественная часть снимается, статья публикует честный отрицательный результат"
        ),
        "freeze_disposition": "kill_gated" if fires else "survivor",
        "rationale": (
            "Native tags do not distinguish the three classical preterites on ≥95% of the "
            "finite past universe (simple perfect lives in untagged Past+None). Clear P2 fail → "
            "disposition kill_gated without human visa (freeze-exit mechanism)."
            if fires
            else "Native tags distinguish three preterites on ≥95% — survive to visa sheet."
        ),
    }


def probe_one(row: dict, cur) -> dict:
    cov = load_json(row["coverage"])
    integrity = INTEGRITY_FNS[row["integrity_keys"]](cur, cov)
    result = {
        "toc_ref": row["toc_ref"],
        "art_id": row["art_id"],
        "slug": row["slug"],
        "c6_slot": row["c6_slot"],
        "pilot": row["pilot"],
        "criterion_status": row["criterion_status"],
        "criterion_quoted": row["criterion_quoted"],
        "criterion_source": row["criterion_source"],
        "article_script": row["script"],
        "coverage_summary": row["coverage"],
        "pin_expected": PIN,
        "integrity": integrity,
        "provenance": PROVENANCE,
    }
    if row["criterion_status"] == "QUOTED" and row["pilot"] == "P2":
        kg = apply_p2_killgate(integrity)
        result["kill_gate"] = kg
        if not integrity["all_match"]:
            result["outcome"] = "blocking_note"
            result["blocking_note"] = (
                "P2 criterion evaluable but committed coverage_summary drifts from live pin — "
                "refuse disposition flip until numbers reconciled."
            )
            result["disposition"] = "unknown"
        elif kg["gate_fires"]:
            result["outcome"] = "kill_gated"
            result["disposition"] = "kill_gated"
            result["blocking_note"] = ""
        else:
            result["outcome"] = "survivor"
            result["disposition"] = "unknown"
            result["blocking_note"] = ""
    else:
        # MISSING programme kill-gate — park, do not invent.
        result["kill_gate"] = None
        result["outcome"] = "blocking_note"
        result["disposition"] = "unknown"
        note = (
            f"H1612 freeze probe: C6 programme kill-gate MISSING for {row['toc_ref']} "
            f"({row['c6_slot']}; not a § 7 pilot). {row['criterion_source']} "
            "Integrity re-derive against pin 04e0778: "
            + ("PASS." if integrity["all_match"] else "FAIL — number drift, see probe JSON.")
            + " Not inventing a threshold; leave disposition=unknown. "
            "Path to freeze exit: programme adds a named gate, or human visa→published "
            "outside the probe-first kill path."
        )
        result["blocking_note"] = note
    return result


def write_artifacts(result: dict) -> None:
    slug = result["slug"]
    json_path = AUDIT / f"probe_freeze_{slug}.json"
    md_path = AUDIT / f"probe_freeze_{slug}.md"
    py_path = AUDIT / f"probe_freeze_{slug}.py"

    json_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    kg = result.get("kill_gate")
    md = []
    md.append(f"# Freeze probe — {result['toc_ref']} (`{result['art_id']}`)")
    md.append("")
    md.append(f"_Created: 24-07-2026 · Last updated: 24-07-2026_")
    md.append("")
    md.append(f"**Handoff:** H1612 · **Model:** {PROVENANCE['model']}")
    md.append("")
    md.append("## Criterion")
    md.append("")
    md.append(f"- **Status:** `{result['criterion_status']}`")
    md.append(f"- **C6 slot:** {result['c6_slot']}")
    md.append(f"- **Pilot:** {result['pilot'] or '—'}")
    if result["criterion_quoted"]:
        md.append(f"- **Quoted (C6 § 7):** {result['criterion_quoted']}")
    md.append(f"- **Source / note:** {result['criterion_source']}")
    md.append("")
    md.append("## Integrity re-derive (pin 04e0778)")
    md.append("")
    md.append(f"- **all_match:** `{result['integrity']['all_match']}`")
    md.append(f"- **kind:** {result['integrity']['kind']}")
    md.append("")
    md.append("## Outcome")
    md.append("")
    md.append(f"- **outcome:** `{result['outcome']}`")
    md.append(f"- **ledger disposition:** `{result['disposition']}`")
    if result.get("blocking_note"):
        md.append(f"- **blocking_note:** {result['blocking_note']}")
    if kg:
        md.append("")
        md.append("## Kill-gate measurement (P2)")
        md.append("")
        md.append(f"- universe (Impf+Past): **{kg['universe']}**")
        md.append(f"- natively assigned: **{kg['assigned']}**")
        md.append(f"- unassigned Past+None: **{kg['unassigned_Past_None']}**")
        md.append(f"- share: **{kg['share_pct']}%** (threshold 95%)")
        md.append(f"- **gate_fires:** `{kg['gate_fires']}`")
        md.append(f"- rationale: {kg['rationale']}")
    md.append("")
    md.append("## Artifacts")
    md.append("")
    md.append(f"- JSON: `sangram/audit/probe_freeze_{slug}.json`")
    md.append(f"- runner: `sangram/audit/probe_freeze_{slug}.py`")
    md.append(f"- article script: `{result['article_script']}`")
    md.append("")
    md.append("_Dr. Mārcis Gasūns_")
    md.append("")
    md_path.write_text("\n".join(md), encoding="utf-8")

    py_body = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Thin re-run wrapper for H1612 freeze probe — {result["toc_ref"]} ({slug}).

Delegates to probe_freeze_se_cluster_h1612.py --only={slug}.
"""
from pathlib import Path
import runpy
import sys

sys.argv = [sys.argv[0], f"--only={slug}"] + sys.argv[1:]
runpy.run_path(str(Path(__file__).with_name("probe_freeze_se_cluster_h1612.py")), run_name="__main__")
'''
    py_path.write_text(py_body, encoding="utf-8")


def update_ledger(results: list[dict]) -> None:
    ledger = json.loads(LEDGER_PATH.read_text(encoding="utf-8"))
    by_toc = {r["toc_ref"]: r for r in results}
    for row in ledger["baseline_ids"]:
        toc = row["toc_ref"]
        if toc not in by_toc:
            continue
        res = by_toc[toc]
        slug = res["slug"]
        probe_link = (
            f"https://github.com/gasyoun/SanskritGrammar/blob/main/sangram/audit/"
            f"probe_freeze_{slug}.md"
        )
        handoff_link = (
            "https://github.com/gasyoun/Uprava/blob/main/handoffs/"
            "H1612-Opus_SanskritGrammar_freeze-probe-se-cluster_24.07.26.md"
        )
        row["disposition"] = res["disposition"]
        row["blocking_note"] = res.get("blocking_note") or ""
        links = list(row.get("source_links") or [])
        for link in (probe_link, handoff_link):
            if link not in links:
                links.append(link)
        row["source_links"] = links
    LEDGER_PATH.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--only", default=None, help="slug filter, e.g. past-tenses")
    ap.add_argument("--no-ledger", action="store_true")
    args = ap.parse_args()

    rows = SE_CLUSTER
    if args.only:
        rows = [r for r in SE_CLUSTER if r["slug"] == args.only]
        if not rows:
            print(f"unknown slug: {args.only}", file=sys.stderr)
            return 2

    con = connect(Path(args.db))
    cur = con.cursor()
    results = []
    for row in rows:
        print(f"--- probing {row['toc_ref']} ({row['slug']}) ---")
        res = probe_one(row, cur)
        write_artifacts(res)
        results.append(res)
        print(
            f"  integrity={res['integrity']['all_match']}  outcome={res['outcome']}  "
            f"disposition={res['disposition']}"
        )

    if not args.no_ledger and args.only is None:
        update_ledger(results)
        print("ledger updated")
    elif not args.no_ledger and args.only is not None:
        update_ledger(results)
        print("ledger updated (single-row)")

    survivors = [r["toc_ref"] for r in results if r["outcome"] == "survivor"]
    kill_gated = [r["toc_ref"] for r in results if r["outcome"] == "kill_gated"]
    blocked = [r["toc_ref"] for r in results if r["outcome"] == "blocking_note"]
    summary = {
        "survivors": survivors,
        "kill_gated": kill_gated,
        "blocking_note": blocked,
        "n": len(results),
        "provenance": PROVENANCE,
    }
    summary_path = AUDIT / "probe_freeze_se_cluster_H1612_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("SUMMARY", json.dumps(summary, ensure_ascii=False, indent=2))
    con.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
