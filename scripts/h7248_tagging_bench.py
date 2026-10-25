#!/usr/bin/env python3
"""H7248 — re-derive every number in the H7248 report from the frozen sample.

Inputs (all committed):
  data/h7248/manifest.json            frozen stratified sample + provenance + sha256
  data/h7248/gold_sample.jsonl        gold CoNLL-U columns for the frozen sentences
  data/h7248/byt5_paper_numbers.json  Arm A figures pinned from the published paper
  data/h7248/predictions/*.jsonl      optional system predictions (Arm B), same keys

Outputs:
  reports/h7248_results.json          every number in the report, per stratum

Modes:
  --check          verify gold sha256 against the manifest (frozen-sample integrity)
  (default)        compute Arm A (pinned), Arm C (majority floor) and, if a
                   predictions file exists, Arm B token-level metrics.

Deterministic: no sampling, no network, no wall-clock in the payload.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "h7248"
MANIFEST = DATA / "manifest.json"
GOLD = DATA / "gold_sample.jsonl"
PAPER = DATA / "byt5_paper_numbers.json"
PRED_DIR = DATA / "predictions"
OUT = ROOT / "reports" / "h7248_results.json"


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def feats_labels(feats: str) -> set[str]:
    if feats in ("_", ""):
        return set()
    return set(feats.split("|"))


def corpus_metrics(gold: list[dict], pred: dict[tuple[str, int], dict]) -> dict:
    """Token metrics over one population; every count keeps its denominator."""
    n = 0
    upos_ok = 0
    lemma_ok = 0
    feats_exact = 0
    tp = fp = fn = 0
    missing = 0
    for row in gold:
        key = (row["sent"], row["i"])
        p = pred.get(key)
        if p is None:
            missing += 1
            continue
        n += 1
        upos_ok += p.get("upos") == row["upos"]
        lemma_ok += p.get("lemma") == row["lemma"]
        feats_exact += p.get("feats", "_") == row["feats"]
        g = feats_labels(row["feats"])
        h = feats_labels(p.get("feats", "_"))
        tp += len(g & h)
        fp += len(h - g)
        fn += len(g - h)
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {
        "tokens_scored": n,
        "tokens_missing_prediction": missing,
        "upos_accuracy": round(upos_ok / n, 4) if n else None,
        "upos_correct": upos_ok,
        "lemma_accuracy": round(lemma_ok / n, 4) if n else None,
        "lemma_correct": lemma_ok,
        "feats_exact_match": round(feats_exact / n, 4) if n else None,
        "feats_exact_correct": feats_exact,
        "feats_micro_precision": round(prec, 4),
        "feats_micro_recall": round(rec, 4),
        "feats_micro_f1": round(f1, 4),
        "feats_tp": tp,
        "feats_fp": fp,
        "feats_fn": fn,
    }


def reset():
    """no-op: token identity is carried explicitly by the 'i' field."""


def arm_a(paper: dict) -> dict:
    """Arm A: published ByT5-Sanskrit figures, pinned and metric-labelled."""
    return {
        "arm": "A-byt5-sanskrit-published",
        "measured_here": False,
        "source": paper["source"],
        "metric": paper["metric"],
        "comparable_to_arm_b_at_token_level": False,
        "why": paper["comparability_note"],
        "tables": paper["tables"],
    }


def arm_c(gold: list[dict], strata: dict[str, str]) -> dict:
    """Majority floor: per stratum, predict the most frequent lemma/UPOS/feats
    observed in the *other* strata (leave-one-stratum-out, so no leakage)."""
    reset()
    tagged = [(r, r["i"]) for r in gold]
    out: dict[str, dict] = {}
    for stratum in sorted(set(strata.values())):
        train = [(r, i) for r, i in tagged if strata[r["sent"]] != stratum]
        test = [(r, i) for r, i in tagged if strata[r["sent"]] == stratum]
        top_lemma = Counter(r["lemma"] for r, _ in train).most_common(1)[0][0]
        top_upos = Counter(r["upos"] for r, _ in train).most_common(1)[0][0]
        top_feats = Counter(r["feats"] for r, _ in train).most_common(1)[0][0]
        pred = {(r["sent"], i): {"upos": top_upos, "lemma": top_lemma, "feats": top_feats} for r, i in test}
        reset()
        sub = [r for r, _ in test]
        out[stratum] = corpus_metrics(sub, pred)
        out[stratum]["denominator"] = "tokens"
        out[stratum]["constant_prediction"] = {
            "lemma": top_lemma,
            "upos": top_upos,
            "feats": top_feats,
        }
    return {
        "arm": "C-majority-floor",
        "measured_here": True,
        "note": (
            "zero-knowledge floor: per stratum the single most frequent lemma/UPOS/FEATS "
            "string from the other three strata is assigned to every token. Not a tagger; "
            "a sanity anchor that any real system must beat."
        ),
        "per_stratum": out,
    }


def render_tables(result: dict) -> dict:
    """Markdown tables generated from the same dict the report quotes."""
    c = result["arm_c"]["per_stratum"]
    strata = sorted(c)
    arm_c = ["| stratum | tokens | UPOS acc | FEATS exact | FEATS micro-F1 | lemma acc |",
             "|---|---|---|---|---|---|"]
    for s in strata:
        v = c[s]
        arm_c.append(
            f"| {s} | {v['tokens_scored']} | {v['upos_accuracy']} | {v['feats_exact_match']} | "
            f"{v['feats_micro_f1']} | {v['lemma_accuracy']} |"
        )
    t7 = result["arm_a"]["tables"]["table_7_dcs_joint_tasks_sentence_perfect_match"]
    arm_a = ["| " + " | ".join(t7["columns"]) + " |", "|" + "---|" * len(t7["columns"])]
    for row in t7["rows"]:
        arm_a.append("| " + " | ".join("" if x is None else str(x) for x in row) + " |")
    return {
        "arm_a_table_7": "\n".join(arm_a),
        "arm_c_per_stratum": "\n".join(arm_c),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--predictions", default=None, help="Arm B predictions jsonl")
    args = ap.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    gold_bytes = GOLD.read_bytes()
    gold_sha = hashlib.sha256(gold_bytes).hexdigest()
    if gold_sha != manifest["gold_sample"]["sha256"]:
        print(f"FAIL gold sha256 {gold_sha} != manifest {manifest['gold_sample']['sha256']}")
        return 1
    if args.check:
        print(f"PASS gold_sample sha256 {gold_sha} ({manifest['counts']['tokens']} tokens, "
              f"{manifest['counts']['sentences']} sentences)")
        return 0

    gold = load_jsonl(GOLD)
    strata = {s["id"]: s["stratum"] for s in manifest["sentences"]}
    paper = json.loads(PAPER.read_text(encoding="utf-8"))

    # gold-only stratum denominators (independent of any arm)
    denom = Counter()
    for row in gold:
        denom[strata[row["sent"]]] += 1
    overall_rows = gold

    result = {
        "handoff": "H7248",
        "manifest_sha256": manifest["manifest_sha256"],
        "gold_sample_sha256": gold_sha,
        "sample": {
            "sentences": manifest["counts"]["sentences"],
            "tokens": manifest["counts"]["tokens"],
            "bound_by": manifest["caps"]["bound_by"],
            "by_stratum": manifest["counts"]["by_stratum"],
        },
        "arm_a": arm_a(paper),
    }

    # Arm B: token-level metrics from a predictions file, if one is committed.
    pred_path = Path(args.predictions) if args.predictions else None
    arm_b = None
    if pred_path and pred_path.exists():
        preds = {(p["sent"], p["i"]): p for p in load_jsonl(pred_path)}
        b_all: dict[str, dict] = {}
        for stratum in sorted(set(strata.values())):
            sub = [r for r in gold if strata[r["sent"]] == stratum]
            b_all[stratum] = corpus_metrics(sub, preds)
            b_all[stratum]["denominator"] = "tokens"
        arm_b = {"arm": "B-llm", "measured_here": True, "predictions": str(pred_path.relative_to(ROOT)),
                 "per_stratum": b_all, "overall": corpus_metrics(gold, preds)}
        result["arm_b"] = arm_b
    else:
        result["arm_b"] = {
            "arm": "B-llm",
            "measured_here": False,
            "status": "NOT MEASURED",
            "blocker": (
                "no Qwen3.5-9B weights reachable from this box: no local Ollama endpoint "
                "(127.0.0.1:11434 refused) and no sanctioned API lane for this model; "
                "Arm B therefore has no numbers and the comparison stays open."
            ),
            "runner": "python scripts/h7248_tagging_bench.py --predictions data/h7248/predictions/<arm>.jsonl",
        }

    result["arm_c"] = arm_c(gold, strata)
    result["arm_c"]["per_stratum"] = {
        k: {**v, "gold_tokens_in_stratum": denom[k]} for k, v in result["arm_c"]["per_stratum"].items()
    }

    result["tables_markdown"] = render_tables(result)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8", newline="\n")
    (OUT.parent / "h7248_tables.md").write_text(
        "<!-- generated by scripts/h7248_tagging_bench.py; do not hand-edit -->\n\n"
        "### Arm A (pinned, sentence-level perfect match, split+metric adjusted)\n\n"
        + result["tables_markdown"]["arm_a_table_7"]
        + "\n\n### Arm C majority floor (token-level, this sample)\n\n"
        + result["tables_markdown"]["arm_c_per_stratum"]
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({
        "sentences": result["sample"]["sentences"],
        "tokens": result["sample"]["tokens"],
        "arm_b_measured": result["arm_b"]["measured_here"],
        "arm_c": {k: {"upos": v["upos_accuracy"], "feats_f1": v["feats_micro_f1"]}
                  for k, v in result["arm_c"]["per_stratum"].items()},
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
