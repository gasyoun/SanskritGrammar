#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""build_lemmatised_join_robustness.py — A63 wave-2 (W2) robustness check.

H913/build_difficulty_ordering.py's analysis B joined textbook vocabulary to corpus
frequency by EXACT SURFACE MATCH (no segmenter), so it matched mostly indeclinables and
pronouns (lemma == surface form) — 14-19% type coverage. The paper's own Limitations
section flags this: "a lemmatised join (W2) is needed to confirm [the near-zero
tau(lesson, freq-rank) result] for inflected content words."

This script adds a heuristic SUFFIX-STRIPPING lemmatiser for the two declension classes
that cover the large majority of Sanskrit nominal content words — thematic a-stems
(masc/neut nouns, most adjectives) and thematic aa-stems (fem nouns) — and re-runs the
textbook-vs-frequency join restricted to NOMINAL content-word POS tags (m/f/n/mf/mn/fn/
mfn/adj in the kosha frequency table), comparing:

  (i)  surface-only join, content-word subset  (the H913 method, content words only)
  (ii) lemmatised join, content-word subset    (this script's suffix-stripped join)

Scope / honest limitation: covers only a-stem and aa-stem declension (case-ending
suffixes for both are enumerated below, SLP1). i-stem, u-stem, consonant-stem nominals
and ALL verb conjugation are OUT OF SCOPE — deriving a verb root from a conjugated
surface form needs guna/vrddhi ablaut reversal, not suffix stripping, and consonant
stems are irregular enough that a hand suffix table would be unreliable. This is stated
as a limitation, not hidden — consistent with the paper's own reporting norm (see
DIFFICULTY_ORDERING_RESULT.md's Limitations section).

Outputs -> data/difficulty_ordering/: lemmatised_join.tsv, lemmatised_join_stats.json.
"""
import sys, json, csv, re
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

from scipy.stats import kendalltau, spearmanr
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "data" / "difficulty_ordering"

NOMINAL_POS = {"m", "f", "n", "mf", "mn", "fn", "mfn", "adj"}

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


# --- suffix -> stem-final-vowel maps (SLP1), longest suffix wins ---------------------
# a-stem (lemma citation form ends "a"): standard Whitney case endings, masc + neut
A_STEM_SUFFIXES = [
    "eByaH", "AnAm", "AByAm", "ayoH", "asya", "Aya", "ezu", "Ani",
    "aH", "am", "an", "ena", "At", "AH", "An", "EH", "au", "e",
]
# aa-stem (lemma citation form ends "A"): standard Whitney case endings, fem
AA_STEM_SUFFIXES = [
    "AByaH", "ABhyAm", "ABhiH", "AyAm", "AyAH", "AyE", "Asu", "AnAm",
    "ayA", "Am", "AH", "e",
]


def candidate_lemmas(token):
    """Yield (candidate_lemma, suffix_len) pairs, longest suffix first."""
    seen = set()
    for suf in sorted(A_STEM_SUFFIXES, key=len, reverse=True):
        if token.endswith(suf) and len(token) > len(suf):
            cand = token[: -len(suf)] + "a"
            if cand not in seen:
                seen.add(cand)
                yield cand, len(suf)
    for suf in sorted(AA_STEM_SUFFIXES, key=len, reverse=True):
        if token.endswith(suf) and len(token) > len(suf):
            cand = token[: -len(suf)] + "A"
            if cand not in seen:
                seen.add(cand)
                yield cand, len(suf)


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
            })
    return rows


def lemmatise_token(token, by_lemma_nominal):
    """Return (lemma, method, suffix_len) or None. Tries surface-exact first (still a
    valid 'lemma' if the token IS the citation form, e.g. voc sg a-stem), then the
    longest-suffix a-/aa-stem candidate that exists in the nominal lemma set."""
    if token in by_lemma_nominal:
        return token, "surface", 0
    best = None
    for cand, suf_len in candidate_lemmas(token):
        if cand in by_lemma_nominal:
            if best is None or suf_len > best[1]:
                best = (cand, suf_len)
    if best:
        return best[0], "suffix-strip", best[1]
    return None


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--freq", default=str(REPO.parent / "kosha" / "data" / "frequency" / "lemma_frequency.tsv"))
    args = ap.parse_args()

    freq_path = Path(args.freq)
    if not freq_path.exists():
        sys.exit(f"frequency table not found: {freq_path} (pass --freq)")
    OUT.mkdir(parents=True, exist_ok=True)

    freq = load_frequency(freq_path)
    # nominal-only lemma -> best (highest-count) row, since a lemma can repeat across POS variants
    by_lemma_nominal = {}
    for r in freq:
        if r["pos"] in NOMINAL_POS and r["rank_all"] is not None:
            cur = by_lemma_nominal.get(r["lemma"])
            if cur is None or (r["count_all"] or 0) > (cur["count_all"] or 0):
                by_lemma_nominal[r["lemma"]] = r

    sentences = json.load(open(REPO / "scripts" / "data" / "sentences.json", encoding="utf-8"))
    tok_re = re.compile(r"[a-zA-Z]+")

    per_book_tokens = defaultdict(lambda: defaultdict(int))  # book -> surface -> count
    per_book_lesson = defaultdict(dict)  # book -> surface -> earliest lesson
    for s in sentences:
        book = s["book"]
        li = lesson_to_int(book, s["lesson"])
        if li is None:
            continue
        slp1 = transliterate(s["text"], sanscript.DEVANAGARI, sanscript.SLP1)
        for tok in tok_re.findall(slp1):
            per_book_tokens[book][tok] += 1
            cur = per_book_lesson[book].get(tok)
            if cur is None or li < cur:
                per_book_lesson[book][tok] = li

    results = {}
    join_rows = []
    for book, lessons in per_book_lesson.items():
        surface_only_matched = []   # (surface, lesson, freq_row) — surface==lemma AND nominal
        lemmatised_matched = []     # (surface, lemma, lesson, freq_row, method, suffix_len)
        for tok, les in lessons.items():
            r_surface = by_lemma_nominal.get(tok)
            if r_surface is not None:
                surface_only_matched.append((tok, les, r_surface))
            hit = lemmatise_token(tok, by_lemma_nominal)
            if hit is not None:
                lemma, method, suf_len = hit
                lemmatised_matched.append((tok, lemma, les, by_lemma_nominal[lemma], method, suf_len))
                join_rows.append({
                    "book": book, "surface_slp1": tok, "lemma_slp1": lemma, "method": method,
                    "first_lesson": les, "rank_all": int(by_lemma_nominal[lemma]["rank_all"]),
                    "pos": by_lemma_nominal[lemma]["pos"],
                })

        types_total = len(lessons)

        def tau_of(matched, lesson_idx, rank_getter):
            les_ = [m[lesson_idx] for m in matched]
            rank_ = [rank_getter(m) for m in matched]
            if len(matched) < 8:
                return None, None, len(matched)
            t, p = kendalltau(les_, rank_)
            return round(t, 4), p, len(matched)

        tau_surf, p_surf, n_surf = tau_of(surface_only_matched, 1, lambda m: m[2]["rank_all"])
        tau_lem, p_lem, n_lem = tau_of(lemmatised_matched, 2, lambda m: m[3]["rank_all"])

        suffix_strip_n = sum(1 for m in lemmatised_matched if m[4] == "suffix-strip")

        results[book] = {
            "types_total_content_word_candidates": types_total,
            "surface_only_content_word_join": {
                "n_matched": n_surf, "type_coverage_pct": round(100 * n_surf / types_total, 1) if types_total else 0,
                "kendall_tau_lesson_vs_freqrank": tau_surf, "kendall_p": p_surf,
            },
            "lemmatised_join": {
                "n_matched": n_lem, "type_coverage_pct": round(100 * n_lem / types_total, 1) if types_total else 0,
                "n_via_suffix_strip": suffix_strip_n,
                "kendall_tau_lesson_vs_freqrank": tau_lem, "kendall_p": p_lem,
            },
            "coverage_gain_pct_points": round(
                (100 * n_lem / types_total if types_total else 0) - (100 * n_surf / types_total if types_total else 0), 1
            ),
        }

    with open(OUT / "lemmatised_join.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["book", "surface_slp1", "lemma_slp1", "method", "first_lesson", "rank_all", "pos"], delimiter="\t")
        w.writeheader()
        w.writerows(sorted(join_rows, key=lambda r: (r["book"], r["first_lesson"])))

    stats = {
        "handoff": "H1465", "rq": "RQ1", "wave": "W2 (lemmatised-join robustness)",
        "scope": "a-stem + aa-stem thematic nominal declension only (suffix-stripping); "
                 "i/u/consonant-stem nominals and all verb conjugation OUT OF SCOPE (see docstring)",
        "results": results,
    }
    with open(OUT / "lemmatised_join_stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    print("=== W2: lemmatised-join robustness (content-word / nominal POS subset) ===")
    for book, r in results.items():
        so = r["surface_only_content_word_join"]
        lj = r["lemmatised_join"]
        print(f"  {book}:")
        print(f"    surface-only (nominal subset): n={so['n_matched']:<4} cov={so['type_coverage_pct']}% "
              f"tau={so['kendall_tau_lesson_vs_freqrank']}")
        print(f"    lemmatised (a-/aa-stem):       n={lj['n_matched']:<4} cov={lj['type_coverage_pct']}% "
              f"(+{lj['n_via_suffix_strip']} via suffix-strip) tau={lj['kendall_tau_lesson_vs_freqrank']}")
    print(f"\nwrote -> {OUT}")


if __name__ == "__main__":
    main()
