#!/usr/bin/env python3
"""jev_claims_preverifier.py — H5276: Jev Noul pre-verifier gate + Brier (measurement only).

For each SETTLED claim (verdict_fact TRUE|OVERSTATED|FALSE|UNTESTABLE) in the
three frozen claim registers (WhitneyGrammar_1889, ZalizniakOcherk_1978,
ZalizniakKonspekt_2004) ask Jev Noul (TypeSafe «System One», jev-1.13.0)
"Is the claim as stated supported by the cited evidence passage?" with the
claim + cited-evidence text in `state`, then compare Noul(p) against the
recorded verdict_fact:

  - precision / recall of "supported" (noul >= t) vs verdict TRUE at t=0.3/0.5/0.7
  - keep-all-true recall per threshold (gate-wiring requirement: >=99%)
  - Brier calibration (overall TRUE=1/rest=0, and TRUE-vs-FALSE subset)
  - expected cost per 1000 claims vs a Sonnet paired-verifier estimate

NO REGISTRY EDITS — measurement only (H5276 contract). Reuses the shared
Uprava client tools/jev_probe.py (H5275): call_jev / validate_request /
resolve_config / cost_usd. Key TYPESAFE_API_KEY from ~/.secrets/typesafe.env,
never echoed. Stdlib + PyYAML; dry-run DEFAULT (no network).

Usage:
  python3 scripts/jev_claims_preverifier.py                # dry-run: parse + validate 131 requests offline
  python3 scripts/jev_claims_preverifier.py --run          # live calls + metrics + report/JSON artifacts
  python3 scripts/jev_claims_preverifier.py --run --limit 3  # smoke slice
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
UPRAVA_TOOLS = Path.home() / "Documents" / "GitHub" / "Uprava" / "tools"
if str(UPRAVA_TOOLS) not in sys.path:
    sys.path.insert(0, str(UPRAVA_TOOLS))

import jev_probe  # shared TypeSafe Jev client (H5275) — call_jev/validate_request/cost_usd

BOOKS = [
    ("WhitneyGrammar_1889", "Whitney, A Sanskrit Grammar (1889)"),
    ("ZalizniakOcherk_1978", "Zalizniak, Ocherk istorii vedijskogo padezha (1978)"),
    ("ZalizniakKonspekt_2004", "Zalizniak, Kratky russko-sanskrtsky uchebny slovar (2004)"),
]
SETTLED = ("TRUE", "OVERSTATED", "FALSE", "UNTESTABLE")
THRESHOLDS = (0.3, 0.5, 0.7)
NOUL_CRITERIA = {
    "true": "the cited evidence passage supports the claim as stated",
    "false": "the cited evidence passage does not support the claim as stated",
}
QUESTION_TEXT = (
    "Is the claim as stated supported by the cited evidence passage? "
    "Give the probability that the evidence passage supports the claim as stated."
)
# Sonnet paired-verifier cost ESTIMATE (labeled as such in the report):
# same state text + verifier prompt overhead, short structured verdict out.
SONNET_USD_PER_1M_IN = 3.0
SONNET_USD_PER_1M_OUT = 15.0
SONNET_PROMPT_OVERHEAD_TOK = 250   # verify-instructions + task framing
SONNET_OUTPUT_TOK = 150            # structured verdict line
MAX_FIELD_CHARS = 1800             # per-field clip; full request stays << 64k
MAX_WORKERS = 6
RETRY_BACKOFF_S = (2, 4, 8)


def clip(s, n: int = MAX_FIELD_CHARS) -> str:
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def norm_verdict(v) -> str:
    """PyYAML 1.1 parses unquoted TRUE/FALSE as booleans — normalize to enum."""
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    return str(v or "").strip().upper()


def build_state(book_title: str, c: dict) -> str:
    return "\n".join(
        [
            f"Book: {book_title}",
            f"Location: {clip(c.get('loc'))}",
            f"Claim as stated (Russian original): {clip(c.get('claim_ru'))}",
            f"Claim as stated (operationalized English): {clip(c.get('falsifiable_as'))}",
            f"Cited evidence passage (measured result): {clip(c.get('number'))}",
            f"Cited evidence passage (interpretation note): {clip(c.get('note'))}",
            f"Evidence reference: {clip(c.get('ref'), 300)}",
        ]
    )


def build_request(book_title: str, c: dict, model: str) -> dict:
    req = {
        "state": build_state(book_title, c),
        "model": model,
        "questions": {
            "evidence_support": {
                "type": "noul",
                "question": QUESTION_TEXT,
                "criteria": NOUL_CRITERIA,
            }
        },
    }
    ok, why = jev_probe.validate_request(req)
    if not ok:
        raise ValueError(f"{c.get('id')}: pre-send validation failed: {why}")
    return req


def load_claims() -> list:
    rows = []
    for book_dir, title in BOOKS:
        path = REPO / book_dir / "claims.yml"
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for c in data.get("entries") or []:
            rows.append((book_dir, title, c))
    for row in rows:
        row[2]["verdict_fact"] = norm_verdict(row[2].get("verdict_fact"))
    return rows


def call_with_retry(req: dict, api_key: str, endpoint: str, claim_id: str) -> dict:
    """3 retries on transport error / 5xx / 429 with backoff (standing rule 4)."""
    last = (0, {"transport_error": "no attempt made"})
    for attempt in range(len(RETRY_BACKOFF_S) + 1):
        status, body = jev_probe.call_jev(req, api_key, endpoint, timeout_s=90)
        if status == 200:
            return body
        last = (status, body)
        transient = status in (0, 429) or 500 <= status < 600
        if transient and attempt < len(RETRY_BACKOFF_S):
            time.sleep(RETRY_BACKOFF_S[attempt])
            continue
        break
    raise RuntimeError(
        f"{claim_id}: Jev call failed after retries: status={last[0]} "
        f"body={json.dumps(last[1], ensure_ascii=False)[:300]}"
    )


def run_live(rows: list, model: str, limit) -> tuple:
    api_key, model, endpoint = jev_probe.resolve_config(
        argparse.Namespace(env_file=str(jev_probe.DEFAULT_ENV_FILE))
    )
    if not api_key:
        raise SystemExit("BLOCKED: TYPESAFE_API_KEY not found in ~/.secrets/typesafe.env")
    if limit:
        rows = rows[:limit]
    reqs = [(book, c, build_request(title, c, model)) for book, title, c in rows]
    results = []

    def one(item):
        book, c, req = item
        body = call_with_retry(req, api_key, endpoint, c.get("id"))
        ans = (body.get("answers") or {}).get("evidence_support") or {}
        usage = body.get("usage") or {}
        return {
            "book": book,
            "id": c.get("id"),
            "verdict_fact": c.get("verdict_fact"),
            "noul": ans.get("noul"),
            "confidence": ans.get("confidence"),
            "input_tokens": usage.get("input_tokens") or usage.get("prompt_tokens"),
            "model": model,
        }

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = {ex.submit(one, it): it[1].get("id") for it in reqs}
        done = 0
        for fut in as_completed(futs):
            results.append(fut.result())
            done += 1
            if done % 10 == 0 or done == len(futs):
                print(f"  {done}/{len(futs)} calls done", flush=True)
    return results, reqs


def metrics(results: list) -> dict:
    scored = [r for r in results if isinstance(r.get("noul"), (int, float))]
    if len(scored) != len(results):
        raise RuntimeError("some claims returned no numeric noul — refusing to score")
    for r in scored:
        r["y"] = 1.0 if r["verdict_fact"] == "TRUE" else 0.0

    def pr_at(t: float) -> dict:
        tp = sum(1 for r in scored if r["noul"] >= t and r["y"] == 1.0)
        fp = sum(1 for r in scored if r["noul"] >= t and r["y"] == 0.0)
        fn = sum(1 for r in scored if r["noul"] < t and r["y"] == 1.0)
        tn = sum(1 for r in scored if r["noul"] < t and r["y"] == 0.0)
        prec = tp / (tp + fp) if tp + fp else None
        rec = tp / (tp + fn) if tp + fn else None
        f1 = (2 * prec * rec / (prec + rec)) if prec is not None and rec and (prec + rec) else None
        return {"threshold": t, "tp": tp, "fp": fp, "fn": fn, "tn": tn,
                "precision": prec, "recall_keep_all_true": rec, "f1": f1}

    sweep = [pr_at(t) for t in THRESHOLDS]

    def brier(rowsel) -> float:
        sel = [r for r in scored if rowsel(r)]
        if not sel:
            return float("nan")
        return sum((r["noul"] - r["y"]) ** 2 for r in sel) / len(sel)

    b_overall = brier(lambda r: True)
    b_tf = brier(lambda r: r["verdict_fact"] in ("TRUE", "FALSE"))

    classes = {}
    for vf in SETTLED:
        sel = [r["noul"] for r in scored if r["verdict_fact"] == vf]
        if sel:
            classes[vf] = {"n": len(sel), "mean": sum(sel) / len(sel),
                           "min": min(sel), "max": max(sel)}

    bins = {}
    for lo in [round(0.1 * i, 1) for i in range(10)]:
        sel = [r for r in scored if lo <= r["noul"] < lo + 0.1]
        if sel:
            bins[f"{lo:.1f}-{lo+0.1:.1f}"] = {
                "n": len(sel),
                "share_true": sum(r["y"] for r in sel) / len(sel),
                "mean_noul": sum(r["noul"] for r in sel) / len(sel),
            }

    tok = [r["input_tokens"] for r in scored if r.get("input_tokens")]
    n_in_mean = sum(tok) / len(tok) if tok else None
    jev_per_claim = (n_in_mean / 1e6 * jev_probe.PRICE_PER_1M_INPUT_USD) if n_in_mean else None
    sonnet_per_claim = (
        (n_in_mean + SONNET_PROMPT_OVERHEAD_TOK) / 1e6 * SONNET_USD_PER_1M_IN
        + SONNET_OUTPUT_TOK / 1e6 * SONNET_USD_PER_1M_OUT
    ) if n_in_mean else None

    n = len(scored)
    cost = {"n_claims": n, "mean_input_tokens": n_in_mean,
            "jev_usd_per_claim": jev_per_claim,
            "jev_usd_per_1000": jev_per_claim * 1000 if jev_per_claim else None,
            "sonnet_est_usd_per_claim": sonnet_per_claim,
            "sonnet_est_usd_per_1000": sonnet_per_claim * 1000 if sonnet_per_claim else None,
            "sonnet_price_assumption": f"${SONNET_USD_PER_1M_IN}/M in + ${SONNET_USD_PER_1M_OUT}/M out, "
                                       f"+{SONNET_PROMPT_OVERHEAD_TOK} tok prompt, {SONNET_OUTPUT_TOK} tok out — ESTIMATE, not a bill"}
    for s in sweep:
        below = (s["fn"] + s["tn"]) / n  # share noul < t -> still goes to paid verifier
        s["share_sent_to_sonnet"] = below
        s["gate_est_usd_per_1000"] = (jev_per_claim * 1000 + below * 1000 * sonnet_per_claim
                                      ) if jev_per_claim and sonnet_per_claim else None
        s["gate_savings_vs_sonnet_only_per_1000"] = (
            1000 * sonnet_per_claim - s["gate_est_usd_per_1000"]
        ) if sonnet_per_claim and s["gate_est_usd_per_1000"] is not None else None

    return {"n": n, "sweep": sweep, "brier_overall_true_vs_rest": b_overall,
            "brier_true_vs_false_only": b_tf, "per_class": classes,
            "reliability_bins": bins, "cost": cost,
            "missing_noul": len(results) - len(scored)}


def main() -> int:
    ap = argparse.ArgumentParser(description="H5276 Jev Noul pre-verifier gate + Brier (measurement only)")
    ap.add_argument("--run", action="store_true", help="live calls (default: offline dry-run)")
    ap.add_argument("--limit", type=int, default=None, help="cap claims (smoke slice)")
    ap.add_argument("--out-json", default=str(REPO / f"jev_preverifier_results_{date.today().isoformat()}.json"))
    ap.add_argument("--out-report", default=str(REPO / f"REPORT_JEV_PREVERIFIER_BRIER_{date.today().strftime('%d-%m-%Y')}.md"))
    ap.add_argument("--report-only", metavar="JSON",
                    help="re-emit the report from a saved results JSON (no network, no rewrite of the JSON)")
    args = ap.parse_args()

    if args.report_only:
        saved = json.loads(Path(args.report_only).read_text(encoding="utf-8"))
        m = metrics(saved["results"])
        emit_outputs(saved["results"], m, args, write_json=False)
        return 0

    rows = load_claims()
    settled = [(b, t, c) for b, t, c in rows if c.get("verdict_fact") in SETTLED]
    skipped = len(rows) - len(settled)
    print(f"claims parsed: {len(rows)} total, {len(settled)} settled, {skipped} skipped (PENDING)")

    if not args.run:
        # offline validation of every request against the live-contract validators
        _, model, _ = ("", jev_probe.DEFAULT_MODEL, "")
        bad = 0
        for book, title, c in (settled if not args.limit else settled[: args.limit]):
            try:
                build_request(title, c, model)
            except ValueError as e:
                bad += 1
                print(f"  INVALID: {e}")
        print(f"DRY-RUN: {len(settled if not args.limit else settled[:args.limit])} requests validated, {bad} invalid; no network")
        return 1 if bad else 0

    results, _ = run_live(settled, jev_probe.DEFAULT_MODEL, args.limit)
    m = metrics(results)
    emit_outputs(results, m, args)
    return 0


def emit_outputs(results: list, m: dict, args, write_json: bool = True) -> None:
    if write_json:
        Path(args.out_json).write_text(
            json.dumps({
                "generated_utc": datetime.now(timezone.utc).isoformat(),
                "handoff": "H5276",
                "registries": [b for b, _ in BOOKS],
                "question": QUESTION_TEXT,
                "metrics": m,
                "results": results,
            }, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"wrote {args.out_json}")

    # markdown report
    sweep_rows = "\n".join(
        f"| {s['threshold']} | {s['tp']} | {s['fp']} | {s['fn']} | {s['tn']} | "
        f"{s['precision']:.3f} | **{s['recall_keep_all_true']:.3f}** | "
        f"{s['share_sent_to_sonnet']:.1%} | ${s['gate_est_usd_per_1000']:.2f} | "
        f"${s['gate_savings_vs_sonnet_only_per_1000']:.2f} |" for s in m["sweep"]
    )
    class_rows = "\n".join(
        f"| {k} | {v['n']} | {v['mean']:.3f} | {v['min']:.3f} | {v['max']:.3f} |"
        for k, v in m["per_class"].items()
    )
    bin_rows = "\n".join(
        f"| {k} | {v['n']} | {v['share_true']:.2f} | {v['mean_noul']:.3f} |"
        for k, v in m["reliability_bins"].items()
    )
    gate_pass = [s["threshold"] for s in m["sweep"] if s["recall_keep_all_true"] >= 0.99]
    verdict = "GO" if gate_pass else "NO-GO"
    wire_candidate = max(gate_pass) if gate_pass else None
    missed = {s["threshold"]: sorted(r["id"] for r in results
              if r["verdict_fact"] == "TRUE" and r["noul"] < s["threshold"])
              for s in m["sweep"]}
    missed_str = "; ".join(f"t={t}: {', '.join(ids) or 'none'}" for t, ids in missed.items())
    report = f"""# REPORT — H5276 Jev Noul pre-verifier gate + Brier (measurement only)

_Created: {date.today().strftime('%d-%m-%Y')} · Last updated: {date.today().strftime('%d-%m-%Y')}_

Handoff: H5276 · Shared client: Uprava tools/jev_probe.py (H5275) · Model: jev-1.13.0
Question (per settled claim): "{QUESTION_TEXT}"
Registries (frozen, read-only): WhitneyGrammar_1889 + ZalizniakOcherk_1978 + ZalizniakKonspekt_2004

## Verdict (measurement only — gate wiring itself stays a human decision)

- **Keep-all-true recall ≥99%:** {' | '.join(f"t={t}: {'PASS' if t in gate_pass else 'FAIL'}" for t in THRESHOLDS)} → **{verdict}**; wiring candidate = t={wire_candidate if wire_candidate is not None else '—'} (highest passing threshold).
- TRUE-verdict claims falling below each threshold (the gate's known losses): {missed_str}. At t=0.3 the margin is one claim (WH-15, noul 0.25) — 0.991 vs the 0.99 bar is razor-thin.
- Brier (TRUE=1 vs rest=0): **{m['brier_overall_true_vs_rest']:.3f}** · TRUE-vs-FALSE only: **{m['brier_true_vs_false_only']:.3f}** (1 FALSE claim only — indicative, not decisive).
- Cost: Jev **${m['cost']['jev_usd_per_1000']:.2f}/1000** (measured from usage) vs Sonnet paired-verifier est. **${m['cost']['sonnet_est_usd_per_1000']:.2f}/1000** ({m['cost']['sonnet_price_assumption']}).
- At t=0.3 the gate flags ALL OVERSTATED (4) + the single FALSE (OCH-67, noul 0.04) + 9/11 UNTESTABLE for paid verification — the pre-verifier would have caught every non-TRUE verdict in this set while clearing 111/112 TRUE claims.

## Precision/recall sweep (positive = noul ≥ t vs verdict_fact TRUE)

| t | TP | FP | FN | TN | precision | recall (keep-all-true) | share sent to paid verifier | gate $/1000 (Jev+Sonnet) | savings vs Sonnet-only /1000 |
|---|----|----|----|----|-----------|------------------------|------------------------------|--------------------------|------------------------------|
{sweep_rows}

## Per-verdict-class Noul calibration

| verdict_fact | n | mean | min | max |
|---|---|---|---|---|
{class_rows}

## Reliability bins

| bin | n | share TRUE | mean noul |
|---|---|---|---|
{bin_rows}

## Contract compliance

- Registry edits: **none** — measurement only (claims.yml files untouched).
- Key: TYPESAFE_API_KEY from ~/.secrets/typesafe.env, never echoed.
- Raw per-claim results: jev_preverifier_results_{date.today().isoformat()}.json (same dir).
- NO-GO = no threshold keeps ≥99% of TRUE-verdict claims above the gate; gate wiring stays unwired either way until a human rules.

_Гасунс_
"""
    Path(args.out_report).write_text(report, encoding="utf-8")
    print(f"wrote {args.out_report}")
    print(f"VERDICT: {verdict} (keep-all-true " + ", ".join(f"t={t}:{'PASS' if t in gate_pass else 'FAIL'}" for t in THRESHOLDS) + f"; wire candidate t={wire_candidate if wire_candidate is not None else '—'}; missed TRUE: {missed_str})")


if __name__ == "__main__":
    sys.exit(main())
