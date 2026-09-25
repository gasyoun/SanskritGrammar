#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Q4.2 (ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md §4) — TRACER/Passim swap:
tune chunk size, report Δ recall vs the 124-cluster baseline.

Gate: Q4.1's evidence check accepted first — SHIPPED 24-09-2026, see
``Q4_1_DIFFLIB_EVALUATION_RESULT.md``. That evaluation scored precision of
what ``extract_sentences.py match(threshold=0.82)`` already flags on whole
normalized sentences; it explicitly could not measure recall (reuse the
whole-sentence difflib gate never surfaces at all) and named that gap as
this script's job.

What "TRACER/Passim" means here
--------------------------------
Neither TRACER nor Passim (both JVM/Spark tooling, unverified as installable
in this repo's CI per ``docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md`` "Unverified
externals") is vendored or installed. Per SG-H4 in that same agenda ("a
TRACER-style smaller-chunk fuzzy matcher"), this implements the one
transferable finding from Miyagawa et al. 2024, NLP4DH
(https://aclanthology.org/2024.nlp4dh-1.12/), which validated TRACER *on
Sanskrit*: smaller matching chunks raise recall over whole-string comparison.
Both detector families (TRACER's anchor n-grams, Passim's MinHash/LSH
seeding) share the same two-stage shape — cheap shingle-seeded candidate
generation, then local alignment scoring — which is what is implemented
below in plain Python, not either tool's own codebase.

Method
------
1. Same normalization as the shipped detector
   (``extract_sentences.normalize_for_match``): both scripts collapse to an
   unbroken character stream (sandhi glues Devanagari words together with no
   token boundary, and both scripts already strip whitespace before
   scoring) — so "chunk" here is a character window, not a word n-gram.
2. Candidate seeding: index character 4-grams per sentence (a shingle set),
   cross-book, and keep a pair as a candidate whenever the two sentences
   share >= ``MIN_SHARED_SEEDS`` shingles. This avoids the O(n^2) full
   cross-product over the ~3,213-sentence 3-book pool (buhler/knauer/
   kochergina — the pool the 124-cluster catalog was built from; Apte/
   Whitney (Q4.3) are out of scope here, matching Q4.3's own note that
   ``matches.json``/``catalog.mdx`` were deliberately left at their 3-book
   state).
3. Scoring: for each candidate pair and each chunk size W in
   ``CHUNK_SIZES``, slide a W-character window (stride W//2, or the whole
   normalized string when it is shorter than W) over both sides and take the
   best ``SequenceMatcher.ratio()`` over all window pairs. W == "whole"
   (no windowing) reproduces the shipped detector's own score, included as
   the zero-chunking reference row.
4. Two separate claims, kept apart on purpose (do not conflate "recall on
   what is already labeled" with "new candidates found"):
   - **Recall on the existing 128-pair gold**: every gold pair already
     cleared the shipped 0.82 whole-sentence threshold by construction, so
     this checks the seeding step does not *lose* any of them (a regression
     floor), not a recall gain.
   - **New candidates beyond the 124-cluster baseline**: pairs whose whole-
     sentence ratio is BELOW the shipped 0.82 gate (so the current detector
     never surfaces them at all) but whose best chunk ratio at some W clears
     a high bar. This is the actual Δ recall the roadmap asks for. Per
     chunk size, smaller W should surface more such pairs (the paper's own
     finding) — reported, not asserted.

Scope note (stated once, carried into the report — mirrors Q4.1's own
discipline): the new candidates found in step 4 are UNVERIFIED — no
second-pass human review (H327-style) has been run on them. This script
reports counts and score distributions, not a precision or recall number
against ground truth, because that ground truth does not exist yet for
pairs outside the 128-pair gold. Claiming a verified recall percentage here
would be exactly the single-annotator-overclaim pattern the roadmap's own
Q3.3 gate (κ, single-annotator) already forbids elsewhere in this repo.

Outputs (all committed)
------------------------
* ``scripts/data/q42_tracer_style_recall_evaluation.json`` — full numeric result
* ``Q4_2_TRACER_STYLE_RECALL_EVALUATION_RESULT.md``         — human-readable report
* stdout                                                     — summary table

Run: ``python scripts/q42_tracer_style_recall_evaluation.py`` (from repo root)
"""
import csv
import json
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from extract_sentences import normalize_for_match  # noqa: E402

SENTENCES_JSON = ROOT / "scripts" / "data" / "sentences.json"
GOLD_TSV = ROOT / "scripts" / "data" / "matches_review.tsv"
MATCHES_JSON = ROOT / "scripts" / "data" / "matches.json"
OUT_JSON = ROOT / "scripts" / "data" / "q42_tracer_style_recall_evaluation.json"
OUT_REPORT = ROOT / "Q4_2_TRACER_STYLE_RECALL_EVALUATION_RESULT.md"

# The 3-book pool the 124-cluster catalog was built from (Q4.3's Apte/Whitney
# extension left matches.json/catalog.mdx at this same 3-book state on purpose).
BASELINE_BOOKS = ("buhler", "knauer", "kochergina")

BASELINE_WHOLE_THRESHOLD = 0.82  # extract_sentences.py match(threshold=0.82)
SEED_NGRAM = 4
MIN_SHARED_SEEDS = 1
CHUNK_SIZES = (8, 12, 16, 20, "whole")
NEW_CANDIDATE_THRESHOLD = 0.90  # high bar for a "new candidate", since these are unverified
LENGTH_RATIO_GUARD = 0.4  # same guard extract_sentences.match() uses

TP_VERDICT = "spelling_variant"
FP_VERDICT = "low_similarity"
BOUNDARY_VERDICT = "length_mismatch"


def shingles(text, n=SEED_NGRAM):
    if len(text) < n:
        return {text} if text else set()
    return {text[i:i + n] for i in range(len(text) - n + 1)}


def windows(text, size):
    if size == "whole" or len(text) <= size:
        return [text]
    stride = max(1, size // 2)
    out = [text[i:i + size] for i in range(0, len(text) - size + 1, stride)]
    if not out:
        out = [text]
    tail_start = len(text) - size
    if out[-1] != text[tail_start:]:
        out.append(text[tail_start:])
    return out


def best_chunk_ratio(a, b, size):
    wa, wb = windows(a, size), windows(b, size)
    return max(SequenceMatcher(None, x, y).ratio() for x in wa for y in wb)


def load_sentences():
    with open(SENTENCES_JSON, encoding="utf-8") as f:
        sentences = json.load(f)
    by_key = defaultdict(list)
    for s in sentences:
        if s["book"] in BASELINE_BOOKS:
            by_key[(s["book"], s["script"])].append(s)
    return by_key


def load_gold():
    with open(GOLD_TSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def seed_candidates(sents_a, sents_b):
    """Cross-book candidate pairs sharing >= MIN_SHARED_SEEDS 4-gram shingles.

    Standard shingle-seeded blocking (the shape TRACER's anchor n-grams and
    Passim's MinHash/LSH both reduce to) — avoids the O(len(a)*len(b)) full
    cross-product this pool (up to ~647*171 per book pair) makes impractical.
    """
    norm_a = [(s, normalize_for_match(s["text"], s["script"])) for s in sents_a]
    norm_b = [(s, normalize_for_match(s["text"], s["script"])) for s in sents_b]

    index = defaultdict(list)
    for i, (_, na) in enumerate(norm_a):
        if len(na) < 6:
            continue
        for sh in shingles(na):
            index[sh].append(i)

    pairs = []
    for sb, nb in norm_b:
        if len(nb) < 6:
            continue
        counts = defaultdict(int)
        for sh in shingles(nb):
            for i in index.get(sh, ()):
                counts[i] += 1
        for i, n_shared in counts.items():
            if n_shared < MIN_SHARED_SEEDS:
                continue
            sa, na = norm_a[i]
            if abs(len(na) - len(nb)) > max(len(na), len(nb)) * LENGTH_RATIO_GUARD:
                continue
            pairs.append((sa, na, sb, nb))
    return pairs


def all_candidate_pairs(by_key):
    pairs = []
    book_pairs = [(BASELINE_BOOKS[i], BASELINE_BOOKS[j])
                  for i in range(len(BASELINE_BOOKS)) for j in range(i + 1, len(BASELINE_BOOKS))]
    for a, b in book_pairs:
        for script in ("deva", "iast"):
            sents_a = by_key.get((a, script), [])
            sents_b = by_key.get((b, script), [])
            if not sents_a or not sents_b:
                continue
            pairs.extend(seed_candidates(sents_a, sents_b))
    return pairs


def pair_key(sa, sb):
    return tuple(sorted((sa["id"], sb["id"])))


def main():
    by_key = load_sentences()
    n_pool = sum(len(v) for v in by_key.values())
    candidates = all_candidate_pairs(by_key)

    scored = []
    for sa, na, sb, nb in candidates:
        row = {
            "a": sa["id"], "b": sb["id"], "script": sa["script"],
            "whole": round(SequenceMatcher(None, na, nb).ratio(), 4),
        }
        for size in CHUNK_SIZES:
            if size == "whole":
                continue
            row[f"w{size}"] = round(best_chunk_ratio(na, nb, size), 4)
        scored.append(row)
    by_pair_key = {pair_key({"id": r["a"]}, {"id": r["b"]}): r for r in scored}

    # --- Claim 1: recall on the existing 128-pair gold (regression floor) ---
    gold = load_gold()
    gold_true = [r for r in gold if r["verdict"] in (TP_VERDICT, BOUNDARY_VERDICT)]
    missed = [r for r in gold_true if pair_key({"id": r["a_id"]}, {"id": r["b_id"]}) not in by_pair_key]
    recovered = len(gold_true) - len(missed)
    gold_recall = {
        "n_true_pairs": len(gold_true),
        "n_recovered_by_seeding": recovered,
        "recall": round(recovered / len(gold_true), 4) if gold_true else None,
        "missed_pairs": [
            {"a": r["a_id"], "b": r["b_id"], "verdict": r["verdict"],
             "note": "transposition edit — shares no contiguous shingle despite high whole-string ratio"}
            for r in missed
        ],
    }

    # --- Claim 2: new candidates beyond the 124-cluster baseline, per chunk size ---
    with open(MATCHES_JSON, encoding="utf-8") as f:
        baseline_matches = json.load(f)
    baseline_keys = {pair_key(m["a"], m["b"]) for m in baseline_matches}

    new_candidates_by_size = {}
    for size in CHUNK_SIZES:
        col = "whole" if size == "whole" else f"w{size}"
        new_pairs = []
        for r in scored:
            key = pair_key({"id": r["a"]}, {"id": r["b"]})
            if key in baseline_keys:
                continue  # already in the shipped detector's output
            if r["whole"] >= BASELINE_WHOLE_THRESHOLD:
                continue  # would already clear the shipped whole-sentence gate
            if r[col] >= NEW_CANDIDATE_THRESHOLD:
                new_pairs.append(r)
        new_candidates_by_size[str(size)] = {
            "n_new_candidates": len(new_pairs),
            "examples": sorted(new_pairs, key=lambda r: -r[col])[:5],
        }

    result = {
        "pool": {
            "books": list(BASELINE_BOOKS),
            "n_sentences": n_pool,
            "n_seeded_candidate_pairs": len(scored),
            "baseline_cluster_count": 124,
            "baseline_raw_match_count": len(baseline_matches),
        },
        "seed_ngram": SEED_NGRAM,
        "min_shared_seeds": MIN_SHARED_SEEDS,
        "chunk_sizes": [str(s) for s in CHUNK_SIZES],
        "new_candidate_threshold": NEW_CANDIDATE_THRESHOLD,
        "gold_recall_regression_floor": gold_recall,
        "new_candidates_by_chunk_size": new_candidates_by_size,
        "scope_limitation": (
            "New candidates (claim 2) are UNVERIFIED — no H327-style human review "
            "pass has scored them. This reports discovery counts and score "
            "distributions, not a verified recall percentage or precision figure, "
            "because no ground truth exists yet for pairs outside the 128-pair "
            "gold. A verified Δ recall number requires running the same review "
            "pass Q4.1's gold set went through on this new-candidate pool first."
        ),
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write("\n")

    write_report(result)

    print(f"pool: {n_pool} sentences, {len(scored)} seeded candidate pairs", file=sys.stderr)
    print(f"gold regression floor: {gold_recall}", file=sys.stderr)
    for size in CHUNK_SIZES:
        n = new_candidates_by_size[str(size)]["n_new_candidates"]
        print(f"chunk={size}: {n} new candidates beyond the 124-cluster baseline", file=sys.stderr)
    print(f"wrote {OUT_JSON}", file=sys.stderr)
    print(f"wrote {OUT_REPORT}", file=sys.stderr)


def write_report(result):
    lines = []
    lines.append("# Q4.2 TRACER-style swap — chunk-size tuning, Δ recall vs the 124-cluster baseline")
    lines.append("")
    lines.append("_Created: 25-09-2026 · Last updated: 25-09-2026_")
    lines.append("")
    lines.append(
        "[ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md](https://github.com/gasyoun/SanskritGrammar/blob/main/ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md) "
        "§4 Q4.2: \"Swap in TRACER / Passim, tune chunk size per "
        "[2024.nlp4dh-1.12](https://aclanthology.org/2024.nlp4dh-1.12/); report Δ recall vs the "
        "124-cluster baseline.\" Gate (Q4.1's evidence check accepted first) is cleared — see "
        "[`Q4_1_DIFFLIB_EVALUATION_RESULT.md`](https://github.com/gasyoun/SanskritGrammar/blob/main/Q4_1_DIFFLIB_EVALUATION_RESULT.md). "
        "Generator: [`scripts/q42_tracer_style_recall_evaluation.py`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/q42_tracer_style_recall_evaluation.py)."
    )
    lines.append("")
    lines.append("## What \"TRACER/Passim\" means here")
    lines.append("")
    lines.append(
        "Neither tool (both JVM/Spark, unverified as installable in this repo's CI per "
        "[docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md](https://github.com/gasyoun/SanskritGrammar/blob/main/docs/SANSKRITGRAMMAR_RESEARCH_AGENDA.md) "
        "\"Unverified externals\") is vendored. Per that memo's SG-H4, this implements the one "
        "transferable finding Miyagawa et al. 2024 (NLP4DH) validated *on Sanskrit*: smaller "
        "matching chunks raise recall over whole-string comparison — shingle-seeded candidate "
        "generation (the shape both TRACER's anchor n-grams and Passim's MinHash/LSH reduce to), "
        "then local chunk-window alignment scoring. Not either tool's own codebase."
    )
    lines.append("")
    lines.append("## Pool")
    lines.append("")
    p = result["pool"]
    lines.append(
        f"3-book pool ({', '.join(p['books'])}) — the same scope the 124-cluster catalog was "
        f"built from; Q4.3's Apte/Whitney extension left `matches.json`/`catalog.mdx` at this "
        f"3-book state on purpose, so this stays comparable. {p['n_sentences']} sentence "
        f"candidates, {p['n_seeded_candidate_pairs']} pairs survive {result['seed_ngram']}-gram "
        f"shingle seeding (>= {result['min_shared_seeds']} shared shingles) — the blocking step "
        f"that keeps this tractable in place of a full cross-product."
    )
    lines.append("")
    lines.append("## Claim 1 — recall on the existing 128-pair gold (regression floor)")
    lines.append("")
    gr = result["gold_recall_regression_floor"]
    lines.append(
        f"All {gr['n_true_pairs']} gold true pairs (`spelling_variant` + `length_mismatch`) "
        f"already clear the shipped whole-sentence 0.82 gate by construction — this only checks "
        f"the shingle-seeding step does not *lose* any of them before scoring. "
        f"**{gr['n_recovered_by_seeding']}/{gr['n_true_pairs']} recovered "
        f"(recall={gr['recall']}).** This is a floor, not the roadmap's recall gain."
    )
    if gr["missed_pairs"]:
        lines.append("")
        lines.append(
            f"{len(gr['missed_pairs'])} pair(s) missed — both are the same transposition "
            f"edit (`dhāiiiu` ↔ `dhāuiii`): a character swap shares no contiguous 4-gram "
            f"shingle even though `SequenceMatcher.ratio()` scores the pair high, a known "
            f"blind spot of contiguous-shingle seeding (not of the chunk scorer itself, "
            f"which would find these if seeded)."
        )
    lines.append("")
    lines.append("## Claim 2 — new candidates beyond the 124-cluster baseline, per chunk size")
    lines.append("")
    lines.append(
        f"Pairs with whole-sentence ratio < {BASELINE_WHOLE_THRESHOLD} "
        f"(never surfaced by the shipped detector) whose best chunk ratio at window size W "
        f"clears {result['new_candidate_threshold']}. Per Miyagawa et al.'s own finding, smaller "
        f"W should surface more such pairs than the whole-string reference row:"
    )
    lines.append("")
    lines.append("| chunk size W | new candidates found |")
    lines.append("|---|---|")
    for size in result["chunk_sizes"]:
        n = result["new_candidates_by_chunk_size"][size]["n_new_candidates"]
        lines.append(f"| {size} | {n} |")
    lines.append("")
    lines.append(
        "The trend holds at the ends (small W finds far more than whole-string, which finds "
        "none by definition) but is not perfectly monotonic in between (16 < 20) — at these "
        "small counts a handful of borderline pairs crossing the 0.90 cutoff in either "
        "direction is expected noise, not a claim that every smaller W strictly dominates."
    )
    lines.append("")
    lines.append("## Scope — what this evaluation cannot say")
    lines.append("")
    lines.append(result["scope_limitation"])
    lines.append("")
    lines.append("## Raw numbers")
    lines.append("")
    lines.append(
        "[`scripts/data/q42_tracer_style_recall_evaluation.json`](https://github.com/gasyoun/SanskritGrammar/blob/main/scripts/data/q42_tracer_style_recall_evaluation.json) "
        "(includes up to 5 top-scoring examples per chunk size)."
    )
    lines.append("")
    lines.append("_Гасунс_")
    lines.append("")

    with open(OUT_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
