#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""build_difficulty_ordering.py — RQ1 of the digital-Sanskrit-pedagogy field.

Question: does corpus frequency predict/optimise Sanskrit *learning order*, or does an
expert "learn-these-first" curation systematically depart from raw frequency? And do the
textbooks themselves front-load high-frequency vocabulary?

Three analyses (all reproducible from committed/sibling data, no segmenter):

  A. core_rank (Leonchenko "learn-these-first", kosha lemma_frequency.tsv) vs rank_all
     (raw DCS corpus frequency). Kendall-tau + Spearman over lemmas carrying both, plus a
     per-POS divergence breakdown (which word classes the curriculum promotes / demotes).

  B. Textbook introduction order vs corpus frequency. Per-book word-form -> first-lesson
     derived from scripts/data/sentences.json (Devanagari -> SLP1), joined by EXACT surface
     match to the frequency table. Coverage is reported honestly: a surface-form join with
     no lemmatiser matches mostly indeclinables/pronouns (lemma == surface), so type-coverage
     is low; the result is stated with that limitation, not hidden.

  C. Context: the existing S1 textbook-vs-textbook tau (sequence_tau_summary.csv).

Outputs -> data/difficulty_ordering/: core_vs_frequency.tsv, pos_divergence.tsv,
textbook_frequency_join.tsv, stats.json.

Model provenance: Opus 4.8 (claude-opus-4-8[1m]), 14-07-2026. Handoff H913 (wave-1a).
Aggregate numbers only (no in-copyright textbook text is emitted).
"""
import sys, json, csv, re, argparse
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from scipy.stats import kendalltau, spearmanr, rankdata
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "difficulty_ordering"

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}


def roman_to_int(s):
    s = s.strip().upper()
    if not s or any(ch not in ROMAN for ch in s):
        return None
    total, prev = 0, 0
    for ch in reversed(s):
        v = ROMAN[ch]
        total += -v if v < prev else v
        prev = max(prev, v)
    return total


def lesson_to_int(book, lesson):
    lesson = str(lesson).strip()
    if book == "knauer":
        m = re.match(r"\d+", lesson)
        return int(m.group()) if m else None
    return roman_to_int(re.split(r"[^IVXLCDM]", lesson, maxsplit=1)[0])


def load_frequency(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f, delimiter="\t"):
            def num(k):
                v = (row.get(k) or "").strip()
                return float(v) if v else None
            rows.append({
                "lemma": row["lemma_slp1"],
                "pos": (row.get("grammar_all") or "").strip() or "?",
                "count_all": num("count_all"),
                "rank_all": num("rank_all"),
                "core_rank": num("core_rank"),
            })
    return rows


def dense_rank(items, key, reverse=False):
    """Return {id: 1-based dense rank} ranking items by key (asc, or desc if reverse)."""
    order = sorted(items, key=lambda x: x[key], reverse=reverse)
    ranks, last, r = {}, object(), 0
    for it in order:
        if it[key] != last:
            r += 1
            last = it[key]
        ranks[it["lemma"]] = r
    return ranks


def analysis_A(freq):
    sub = [r for r in freq if r["core_rank"] is not None and r["rank_all"] is not None]
    core = [r["core_rank"] for r in sub]
    rall = [r["rank_all"] for r in sub]
    tau, tau_p = kendalltau(core, rall)
    rho, rho_p = spearmanr(core, rall)

    # symmetric average-tie ranks within the shared subset: both span 1..N with ties
    # averaged the SAME way, so delta is centred at 0 (a dense rank would ties-compress the
    # count_all side and skew every delta negative — an artefact, not a real demotion).
    freq_r = rankdata([-r["count_all"] for r in sub], method="average")  # 1 = most frequent
    core_r = rankdata([r["core_rank"] for r in sub], method="average")   # 1 = learn first
    for i, r in enumerate(sub):
        r["rank_freq_sub"] = round(float(freq_r[i]), 1)
        r["rank_core_sub"] = round(float(core_r[i]), 1)
        r["delta"] = round(float(freq_r[i] - core_r[i]), 1)  # + = promoted, - = demoted

    promoted = sorted(sub, key=lambda r: r["delta"], reverse=True)[:15]
    demoted = sorted(sub, key=lambda r: r["delta"])[:15]

    def ex(r):  # raw kosha ranks (most interpretable) + the centred subset delta
        return (r["lemma"], r["pos"], int(r["rank_all"]), int(r["core_rank"]), r["delta"])

    # per-POS mean delta (now centred at 0 across all lemmas)
    bypos = defaultdict(list)
    for r in sub:
        bypos[r["pos"]].append(r)
    pos_rows = []
    for pos, rs in bypos.items():
        if len(rs) < 20:
            continue
        srt = sorted(rs, key=lambda r: r["rank_all"])
        pos_rows.append({
            "pos": pos, "n": len(rs),
            "mean_delta": round(sum(r["delta"] for r in rs) / len(rs), 1),
            "median_rank_all": int(sorted(r["rank_all"] for r in rs)[len(rs) // 2]),
            "median_core_rank": int(sorted(r["core_rank"] for r in rs)[len(rs) // 2]),
        })
    pos_rows.sort(key=lambda x: x["mean_delta"], reverse=True)

    # THE key pedagogical finding: the curated list does not reorder frequency, it EXCLUDES.
    # For the top-K frequency lemmas, how many carry no core_rank, and of what POS?
    core_lemmas = {r["lemma"] for r in sub}
    ranked = sorted([r for r in freq if r["rank_all"] is not None], key=lambda r: r["rank_all"])
    exclusion = {}
    for K in (50, 100, 200):
        excluded = [r for r in ranked[:K] if r["lemma"] not in core_lemmas]
        pos_ct = defaultdict(int)
        for r in excluded:
            pos_ct[r["pos"]] += 1
        exclusion[f"top{K}"] = {
            "n_excluded": len(excluded),
            "pct_excluded": round(100 * len(excluded) / K, 1),
            "by_pos": dict(sorted(pos_ct.items(), key=lambda x: -x[1])),
        }
    top50_absent = [r["lemma"] for r in ranked[:50] if r["lemma"] not in core_lemmas]

    return {
        "n_shared": len(sub),
        "kendall_tau": round(tau, 4), "kendall_p": tau_p,
        "spearman_rho": round(rho, 4), "spearman_p": rho_p,
        "top50_freq_absent_from_core_n": len(top50_absent),
        "top50_freq_absent_from_core": top50_absent,
        "exclusion_by_frequency_band": exclusion,
        "promoted": [ex(r) for r in promoted],
        "demoted": [ex(r) for r in demoted],
        "pos_divergence": pos_rows,
        "_sub": sub,
    }


def analysis_B(freq, sentences_path):
    by_lemma = {r["lemma"]: r for r in freq}
    sentences = json.load(open(sentences_path, encoding="utf-8"))

    # per-book: surface SLP1 form -> earliest lesson int
    first_lesson = defaultdict(dict)
    tok_re = re.compile(r"[a-zA-Z]+")
    total_tokens = defaultdict(int)
    for s in sentences:
        book = s["book"]
        li = lesson_to_int(book, s["lesson"])
        if li is None:
            continue
        slp1 = transliterate(s["text"], sanscript.DEVANAGARI, sanscript.SLP1)
        for tok in tok_re.findall(slp1):
            total_tokens[book] += 1
            cur = first_lesson[book].get(tok)
            if cur is None or li < cur:
                first_lesson[book][tok] = li

    results, join_rows = {}, []
    for book, fl in first_lesson.items():
        matched = [(tok, les, by_lemma[tok]) for tok, les in fl.items() if tok in by_lemma and by_lemma[tok]["rank_all"] is not None]
        types_total = len(fl)
        types_matched = len(matched)
        # token coverage: sum corpus... no, coverage of the textbook's own token stream
        tok_cov = sum(1 for s in sentences if s["book"] == book
                      for t in tok_re.findall(transliterate(s["text"], sanscript.DEVANAGARI, sanscript.SLP1))
                      if t in by_lemma)
        les = [m[1] for m in matched]
        rank = [m[2]["rank_all"] for m in matched]
        tau, tau_p = kendalltau(les, rank) if len(matched) >= 8 else (None, None)
        # per-lesson mean frequency-rank of newly-introduced matched words
        by_lesson = defaultdict(list)
        for tok, l, fr in matched:
            by_lesson[l].append(fr["rank_all"])
        lesson_means = sorted((l, round(sum(v) / len(v), 1), len(v)) for l, v in by_lesson.items())
        # does mean rank_all rise (words get rarer) as lessons progress?
        if len(lesson_means) >= 5:
            trend_rho, trend_p = spearmanr([x[0] for x in lesson_means], [x[1] for x in lesson_means])
        else:
            trend_rho, trend_p = None, None
        results[book] = {
            "types_total": types_total, "types_matched": types_matched,
            "type_coverage_pct": round(100 * types_matched / types_total, 1) if types_total else 0,
            "token_coverage_pct": round(100 * tok_cov / total_tokens[book], 1) if total_tokens[book] else 0,
            "kendall_tau_lesson_vs_freqrank": round(tau, 4) if tau is not None else None,
            "kendall_p": tau_p,
            "lesson_meanfreqrank_trend_rho": round(trend_rho, 4) if trend_rho is not None else None,
            "lesson_meanfreqrank_trend_p": trend_p,
            "lesson_means_sample": lesson_means[:8],
        }
        for tok, l, fr in sorted(matched, key=lambda m: (m[1], m[2]["rank_all"])):
            join_rows.append({"book": book, "surface_slp1": tok, "first_lesson": l,
                              "rank_all": int(fr["rank_all"]), "count_all": int(fr["count_all"]) if fr["count_all"] else "",
                              "pos": fr["pos"]})
    return results, join_rows


def analysis_C(summary_path):
    if not summary_path.exists():
        return []
    with open(summary_path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--freq", default=str(REPO.parent / "kosha" / "data" / "frequency" / "lemma_frequency.tsv"))
    args = ap.parse_args()

    freq_path = Path(args.freq)
    if not freq_path.exists():
        sys.exit(f"frequency table not found: {freq_path} (pass --freq)")
    OUT.mkdir(parents=True, exist_ok=True)

    freq = load_frequency(freq_path)
    A = analysis_A(freq)
    B, join_rows = analysis_B(freq, REPO / "scripts" / "data" / "sentences.json")
    C = analysis_C(REPO / "scripts" / "data" / "sequence_tau_summary.csv")

    # write core_vs_frequency.tsv
    with open(OUT / "core_vs_frequency.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["lemma_slp1", "pos", "rank_all", "core_rank", "rank_freq_sub", "rank_core_sub", "delta"])
        for r in sorted(A["_sub"], key=lambda r: r["rank_core_sub"]):
            w.writerow([r["lemma"], r["pos"], int(r["rank_all"]), int(r["core_rank"]),
                        r["rank_freq_sub"], r["rank_core_sub"], r["delta"]])

    with open(OUT / "pos_divergence.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["pos", "n", "mean_delta", "median_rank_all", "median_core_rank"])
        for r in A["pos_divergence"]:
            w.writerow([r["pos"], r["n"], r["mean_delta"], r["median_rank_all"], r["median_core_rank"]])

    with open(OUT / "textbook_frequency_join.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["book", "surface_slp1", "first_lesson", "rank_all", "count_all", "pos"], delimiter="\t")
        w.writeheader()
        w.writerows(join_rows)

    A_out = {k: v for k, v in A.items() if k != "_sub"}
    stats = {
        "handoff": "H913", "rq": "RQ1", "model": "Opus 4.8 (claude-opus-4-8[1m])",
        "date": "2026-07-14", "freq_source": str(freq_path.name),
        "analysis_A_core_vs_frequency": A_out,
        "analysis_B_textbook_vs_frequency": B,
        "analysis_C_textbook_vs_textbook_S1": C,
    }
    with open(OUT / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # console summary
    print("=== Analysis A: core_rank (learn-first) vs rank_all (raw frequency) ===")
    print(f"  shared lemmas: {A['n_shared']}")
    print(f"  Kendall tau = {A['kendall_tau']} (p={A['kendall_p']:.2e})")
    print(f"  Spearman rho = {A['spearman_rho']} (p={A['spearman_p']:.2e})")
    print("  EXCLUSION — top-frequency lemmas absent from the curated learn-first list:")
    for band, e in A["exclusion_by_frequency_band"].items():
        print(f"    {band}: {e['n_excluded']} excluded ({e['pct_excluded']}%) — by POS: {e['by_pos']}")
    print("    (top-50 absent: " + " ".join(A["top50_freq_absent_from_core"][:25]) + ")")
    print("  most curriculum-PROMOTED (learned earlier than raw frequency warrants):")
    for lemma, pos, ra, cr, d in A["promoted"][:6]:
        print(f"    {lemma:12} {pos:8} rank_all#{ra:<5} core#{cr:<5} delta={d:+.0f}")
    print("  most curriculum-DEMOTED (frequent but learned very late):")
    for lemma, pos, ra, cr, d in A["demoted"][:6]:
        print(f"    {lemma:12} {pos:8} rank_all#{ra:<5} core#{cr:<5} delta={d:+.0f}")
    print("  per-POS mean delta (+ promoted / - demoted) + medians:")
    for r in A["pos_divergence"][:6] + A["pos_divergence"][-6:]:
        print(f"    {r['pos']:9} n={r['n']:<5} mean_delta={r['mean_delta']:+7.1f}  med(rank_all)={r['median_rank_all']:<6} med(core)={r['median_core_rank']}")
    print("=== Analysis B: textbook introduction order vs corpus frequency ===")
    for book, b in B.items():
        print(f"  {book}: types matched {b['types_matched']}/{b['types_total']} ({b['type_coverage_pct']}%), "
              f"token-cov {b['token_coverage_pct']}%, tau(lesson,freqrank)={b['kendall_tau_lesson_vs_freqrank']}, "
              f"per-lesson rarity trend rho={b['lesson_meanfreqrank_trend_rho']}")
    print("=== Analysis C: existing S1 textbook-vs-textbook tau ===")
    for row in C:
        print(f"  {row['pair']}: tau={row['tau']} (n={row['n']})")
    print(f"\nwrote -> {OUT}")


if __name__ == "__main__":
    main()
