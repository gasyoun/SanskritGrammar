"""H3966 — before/after delta between the v0.48.0 and v0.49 imperfect-switching runs.

v0.48.0 (`imperfect_switching_stats.json`, 17-07-2026) classified finite past forms with
`feat_person IS NOT NULL` and no mood guard, so the `PERF` bucket absorbed 8,726 finite
non-indicative past tokens by construction (H3878 finding G22: DCS never assigns `Formation`
outside the indicative). v0.49 (`imperfect_switching_stats_v049.json`) adds
`feat_mood='Ind'` to every `CAT_SQL` branch. This script diffs the two runs so the corrected
report can show the delta on every headline number instead of quietly renumbering — the
pre-registration (T2607-26) is only protected if both runs stay legible side by side.

MATERIALITY RULE (stated, because v0.48.0 published no confidence intervals). The handoff
asks whether a headline number "moves past its stated confidence interval". The original
report states decision thresholds, not intervals, so a move is called MATERIAL when it
crosses one of the pre-registered lines rather than when it exceeds an interval that was
never published:
  * a Markov `lift` crosses 1.0 — attraction and repulsion are opposite claims;
  * a runs-test verdict crosses p = 0.001 (the report's own "< 0,001" column) or flips
    the observed-vs-shuffled direction;
  * a turnover `diff` changes sign, or its one-sided p crosses the pre-registered 0.01;
  * a bucket size moves by more than the 10.15 % contamination the caveat predicted, which
    would mean the guard did something other than remove the known non-indicative mass.
Everything else is reported as a numeric shift without a materiality claim.

Usage:  python ZalizniakOcherk_1978/imperfect_switching_delta.py
Writes  imperfect_switching_delta_v048_v049.json next to this script and prints the
markdown tables the v0.49 report embeds.

Claude Code Opus 5 (claude-opus-5[1m]), 06-09-2026, H3966.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
OLD = HERE / "imperfect_switching_stats.json"
NEW = HERE / "imperfect_switching_stats_v049.json"
OUT = HERE / "imperfect_switching_delta_v048_v049.json"

CATS = ("IMPF", "PERF", "AOR")
SLICE_RU = {"vedic": "веды", "epic": "эпос", "classical": "классика", "puranic": "пураны"}
PREREG_TURNOVER_ALPHA = 0.01
RUNS_ALPHA = 0.001
CONTAMINATION_SHARE = 0.1015


def _d(new, old):
    if new is None or old is None:
        return None
    return round(new - old, 4)


def _pct(new, old):
    if not old:
        return None
    return round(100.0 * (new - old) / old, 2)


def bucket_delta(old, new):
    rows = []
    for key in sorted(new["slices"], key=lambda k: list(SLICE_RU).index(k)):
        o = old["slices"][key]["category_tokens"]
        n = new["slices"][key]["category_tokens"]
        for cat in CATS:
            ov, nv = o.get(cat, 0), n.get(cat, 0)
            share = abs(nv - ov) / ov if ov else 0.0
            if cat == "PERF":
                # The caveat predicted a corpus-wide 10.15 % contamination. A slice that
                # loses materially more than that is a fact the caveat did not carry.
                material = share > CONTAMINATION_SHARE
                note = ("removed share %.2f %% vs the %.2f %% the caveat predicted "
                        "corpus-wide" % (100 * share, 100 * CONTAMINATION_SHARE))
            else:
                material = nv != ov
                note = ("IMPF/AOR were already 100 % indicative — any change here means "
                        "the guard did more than remove non-indicative mass"
                        if material else "unchanged, as expected")
            rows.append({
                "slice": key, "slice_ru": SLICE_RU[key], "category": cat,
                "v048": ov, "v049": nv, "delta": nv - ov, "delta_pct": _pct(nv, ov),
                "material": material, "note": note,
            })
    return rows


def markov_delta(old, new):
    rows = []
    for key in sorted(new["slices"], key=lambda k: list(SLICE_RU).index(k)):
        om, nm = old["slices"][key]["markov"], new["slices"][key]["markov"]
        for a in CATS:
            for b in CATS:
                if a not in om or a not in nm:
                    continue
                oc, nc = om[a].get(b), nm[a].get(b)
                if oc is None or nc is None:
                    continue
                crossed = (oc["lift"] is not None and nc["lift"] is not None
                           and (oc["lift"] - 1.0) * (nc["lift"] - 1.0) < 0)
                rows.append({
                    "slice": key, "slice_ru": SLICE_RU[key], "from": a, "to": b,
                    "p_v048": oc["p"], "p_v049": nc["p"], "p_delta": _d(nc["p"], oc["p"]),
                    "lift_v048": oc["lift"], "lift_v049": nc["lift"],
                    "lift_delta": _d(nc["lift"], oc["lift"]),
                    "n_v048": oc["n"], "n_v049": nc["n"],
                    "material": crossed,
                    "note": "lift crossed 1.0 — attraction/repulsion flipped" if crossed else "",
                })
    return rows


def runs_delta(old, new):
    rows = []
    for key in sorted(new["slices"], key=lambda k: list(SLICE_RU).index(k)):
        ot, nt = old["slices"][key]["runs_tests"], new["slices"][key]["runs_tests"]
        for text in sorted(set(ot) | set(nt)):
            o, n = ot.get(text), nt.get(text)
            if o is None or n is None:
                rows.append({
                    "slice": key, "slice_ru": SLICE_RU[key], "text": text,
                    "present_v048": o is not None, "present_v049": n is not None,
                    "material": False,
                    "note": ("text entered the slice's top-5-by-length in v0.49"
                             if o is None else
                             "text left the slice's top-5-by-length in v0.49"),
                })
                continue
            crossed = ((o["p_clustering_le"] < RUNS_ALPHA) != (n["p_clustering_le"] < RUNS_ALPHA))
            flipped = ((o["observed_runs"] < o["expected_runs_shuffled"])
                       != (n["observed_runs"] < n["expected_runs_shuffled"]))
            rows.append({
                "slice": key, "slice_ru": SLICE_RU[key], "text": text,
                "present_v048": True, "present_v049": True,
                "observed_v048": o["observed_runs"], "observed_v049": n["observed_runs"],
                "expected_v048": o["expected_runs_shuffled"],
                "expected_v049": n["expected_runs_shuffled"],
                "impf_v048": o["impf_tokens"], "impf_v049": n["impf_tokens"],
                "seq_len_v048": o["seq_len"], "seq_len_v049": n["seq_len"],
                "p_v048": o["p_clustering_le"], "p_v049": n["p_clustering_le"],
                "material": crossed or flipped,
                "note": ("clustering direction flipped" if flipped else
                         "p crossed %g" % RUNS_ALPHA if crossed else ""),
            })
    return rows


def turnover_delta(old, new):
    rows = []
    for key in sorted(new["slices"], key=lambda k: list(SLICE_RU).index(k)):
        o = old["slices"][key].get("turnover")
        n = new["slices"][key].get("turnover")
        if o is None or n is None:
            rows.append({"slice": key, "slice_ru": SLICE_RU[key],
                         "present_v048": o is not None, "present_v049": n is not None,
                         "material": True,
                         "note": "the slice lost or gained a computable turnover test"})
            continue
        sign_flip = o["diff"] * n["diff"] < 0
        alpha_cross = ((o["p_one_sided"] < PREREG_TURNOVER_ALPHA)
                       != (n["p_one_sided"] < PREREG_TURNOVER_ALPHA))
        rows.append({
            "slice": key, "slice_ru": SLICE_RU[key],
            "present_v048": True, "present_v049": True,
            "impf_points_v048": o["impf_insertion_points"],
            "impf_points_v049": n["impf_insertion_points"],
            "perf_points_v048": o["background_perf_points"],
            "perf_points_v049": n["background_perf_points"],
            "at_impf_v048": o["mean_turnover_at_impf"],
            "at_impf_v049": n["mean_turnover_at_impf"],
            "at_perf_v048": o["mean_turnover_at_perf"],
            "at_perf_v049": n["mean_turnover_at_perf"],
            "diff_v048": o["diff"], "diff_v049": n["diff"],
            "diff_delta": _d(n["diff"], o["diff"]),
            "p_v048": o["p_one_sided"], "p_v049": n["p_one_sided"],
            "material": sign_flip or alpha_cross,
            "note": ("Δ changed sign" if sign_flip else
                     "p crossed the pre-registered %g" % PREREG_TURNOVER_ALPHA
                     if alpha_cross else ""),
        })
    return rows


def _md_table(header, rows):
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def _mark(flag):
    return "**ДА**" if flag else "нет"


def print_markdown(delta):
    print("### Размеры корзин\n")
    print(_md_table(
        ["Срез", "Категория", "v0.48.0", "v0.49", "Δ", "Δ %", "материально"],
        [[r["slice_ru"], r["category"], r["v048"], r["v049"], r["delta"],
          r["delta_pct"], _mark(r["material"])] for r in delta["buckets"]]))
    print("\n### Марковские переходы\n")
    print(_md_table(
        ["Срез", "Переход", "p v0.48.0", "p v0.49", "Δp", "lift v0.48.0", "lift v0.49",
         "Δlift", "материально"],
        [[r["slice_ru"], f'{r["from"]}→{r["to"]}', r["p_v048"], r["p_v049"], r["p_delta"],
          r["lift_v048"], r["lift_v049"], r["lift_delta"], _mark(r["material"])]
         for r in delta["markov"]]))
    print("\n### Runs-test\n")
    print(_md_table(
        ["Срез", "Текст", "серий v0.48.0", "серий v0.49", "ожид. v0.48.0", "ожид. v0.49",
         "p v0.48.0", "p v0.49", "материально"],
        [[r["slice_ru"], r["text"], r.get("observed_v048", "—"), r.get("observed_v049", "—"),
          r.get("expected_v048", "—"), r.get("expected_v049", "—"),
          r.get("p_v048", "—"), r.get("p_v049", "—"), _mark(r["material"])]
         for r in delta["runs"]]))
    print("\n### Жаккардовый оборот\n")
    print(_md_table(
        ["Срез", "точек IMPF", "фона", "при IMPF", "фон", "Δ v0.48.0", "Δ v0.49",
         "p v0.48.0", "p v0.49", "материально"],
        [[r["slice_ru"],
          f'{r.get("impf_points_v048","—")}→{r.get("impf_points_v049","—")}',
          f'{r.get("perf_points_v048","—")}→{r.get("perf_points_v049","—")}',
          f'{r.get("at_impf_v048","—")}→{r.get("at_impf_v049","—")}',
          f'{r.get("at_perf_v048","—")}→{r.get("at_perf_v049","—")}',
          r.get("diff_v048", "—"), r.get("diff_v049", "—"),
          r.get("p_v048", "—"), r.get("p_v049", "—"), _mark(r["material"])]
         for r in delta["turnover"]]))


def main():
    old = json.loads(OLD.read_text(encoding="utf-8"))
    new = json.loads(NEW.read_text(encoding="utf-8"))
    delta = {
        "compares": {"v048": OLD.name, "v049": NEW.name},
        "guard": new.get("mood_guard"),
        "guard_effect": new.get("mood_guard_effect"),
        "materiality_rule": {
            "markov_lift_crosses": 1.0,
            "runs_alpha": RUNS_ALPHA,
            "turnover_prereg_alpha": PREREG_TURNOVER_ALPHA,
            "caveat_contamination_share": CONTAMINATION_SHARE,
            "note": "v0.48.0 published decision thresholds, not confidence intervals; "
                    "materiality is evaluated against those thresholds and said so out loud",
        },
        "buckets": bucket_delta(old, new),
        "markov": markov_delta(old, new),
        "runs": runs_delta(old, new),
        "turnover": turnover_delta(old, new),
    }
    delta["material_count"] = sum(
        1 for k in ("buckets", "markov", "runs", "turnover") for r in delta[k] if r["material"])
    OUT.write_text(json.dumps(delta, ensure_ascii=False, indent=1), encoding="utf-8")
    print_markdown(delta)
    print("\nmaterial changes:", delta["material_count"])
    print("->", OUT)


if __name__ == "__main__":
    main()
