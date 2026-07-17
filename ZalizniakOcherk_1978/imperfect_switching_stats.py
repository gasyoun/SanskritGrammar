"""H1053 — imperfect as a narrative-switching marker among perfects (MG's note to HK-15).

Pre-registered design: Uprava/QUESTIONS_LOG.md T2607-26 (frozen 17-07-2026 BEFORE this
script first ran). Deterministic; snapshot = dcs_full.sqlite (dcs-conllu 04e0778), path
convention as in och_voice_stats.py; genre slices reuse period_style_gradient.PERIOD_MAP.

Categories (validated against the snapshot before prereg):
  IMPF = feat_tense='Impf'
  PERF = feat_tense='Past' AND feat_formation IS NULL   (top forms: uvāca, babhūva, jagāma)
  AOR  = feat_tense='Past' AND feat_formation IN (root,them,s,is,red,sa,sis)
  peri/Plp/Pqp excluded.

Metrics per the prereg: (a) Markov transitions + lift; (b) IMPF runs-test vs within-text
shuffle (1000 permutations, seed 20260717); (c) content-lemma Jaccard turnover at IMPF
insertions inside perfect chains (>=4 of 6 finite-past neighbours PERF) vs background
PERF points of the same chains, windows of +/-5 sentences.

Fable 5 (claude-fable-5), 17-07-2026, per MG's authorization to run the Opus-tier row.
"""

import json
import random
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent))
from period_style_gradient import PERIOD_MAP  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
DCS_SQLITE = REPO.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT = Path(__file__).resolve().parent / "imperfect_switching_stats.json"

SEED = 20260717
N_PERM = 1000
WINDOW_SENTS = 5
CHAIN_NEIGHBOURS = 6
CHAIN_MIN_PERF = 4
CONTENT_UPOS = ("NOUN", "VERB", "PROPN", "ADJ")
AOR_FORMATIONS = ("root", "them", "s", "is", "red", "sa", "sis")

CAT_SQL = f"""
CASE
  WHEN feat_tense='Impf' THEN 'IMPF'
  WHEN feat_tense='Past' AND feat_formation IS NULL THEN 'PERF'
  WHEN feat_tense='Past' AND feat_formation IN {AOR_FORMATIONS!r} THEN 'AOR'
END
"""


def load(db):
    """Per text: ordered finite-past sequence + sentence content-lemma sets."""
    cur = db.cursor()
    texts = dict(cur.execute("SELECT text_id, name FROM text"))
    # ordered finite past forms (global sentence order key per text)
    seqs = defaultdict(list)  # text_id -> [(order_key, sent_key, cat)]
    q = f"""
    SELECT c.text_id, c.chapter_id, s.sent_counter, s.sent_subcounter, s.id, t.idx,
           {CAT_SQL} AS cat
    FROM token t
    JOIN sentence s ON t.sentence_id = s.id
    JOIN chapter c ON s.chapter_id = c.chapter_id
    WHERE t.feat_person IS NOT NULL AND ({CAT_SQL}) IS NOT NULL
    ORDER BY c.text_id, c.chapter_id, s.sent_counter, s.sent_subcounter, t.idx
    """
    for text_id, chap_pos, sc, ssc, sent_pk, idx, cat in cur.execute(q):
        seqs[text_id].append(((chap_pos, sc or 0, ssc or 0, idx or 0), sent_pk, cat))
    # sentence order + content lemmas, per text (only for texts we analyse deeply)
    return texts, seqs


def sent_lemmas(db, text_id):
    """Ordered sentences of a text -> (ordered sent_pk list, {sent_pk: set(lemmas)})."""
    cur = db.cursor()
    order = []
    for (pk,) in cur.execute(
            "SELECT s.id FROM sentence s JOIN chapter c ON s.chapter_id=c.chapter_id "
            "WHERE c.text_id=? ORDER BY c.chapter_id, s.sent_counter, s.sent_subcounter",
            (text_id,)):
        order.append(pk)
    pos = {pk: i for i, pk in enumerate(order)}
    lem = defaultdict(set)
    for pk, lemma in cur.execute(
            "SELECT t.sentence_id, t.lemma FROM token t "
            "JOIN sentence s ON t.sentence_id=s.id "
            "JOIN chapter c ON s.chapter_id=c.chapter_id "
            "WHERE c.text_id=? AND t.upos IN (?,?,?,?) AND t.lemma IS NOT NULL",
            (text_id, *CONTENT_UPOS)):
        lem[pk].add(lemma)
    return order, pos, lem


def markov(seq):
    trans = Counter()
    for a, b in zip(seq, seq[1:]):
        trans[(a, b)] += 1
    return trans


def runs_count(seq, cat="IMPF"):
    runs, prev = 0, None
    for c in seq:
        is_cat = (c == cat)
        if is_cat and prev is not True:
            runs += 1
        prev = is_cat
    return runs


def runs_test(seq, rng):
    """Observed IMPF runs vs within-sequence shuffles. Fewer runs = clustering."""
    obs = runs_count(seq)
    n_impf = sum(1 for c in seq if c == "IMPF")
    if n_impf < 10 or n_impf == len(seq):
        return None
    le = 0
    sims = []
    pool = list(seq)
    for _ in range(N_PERM):
        rng.shuffle(pool)
        r = runs_count(pool)
        sims.append(r)
        if r <= obs:
            le += 1
    mean_sim = sum(sims) / len(sims)
    return {"observed_runs": obs, "impf_tokens": n_impf, "seq_len": len(seq),
            "expected_runs_shuffled": round(mean_sim, 1),
            "p_clustering_le": round(le / N_PERM, 4)}


def jaccard(a, b):
    if not a and not b:
        return None
    u = a | b
    return len(a & b) / len(u) if u else None


def turnover_at(points, pos, order, lem):
    """1 - Jaccard between the +/-WINDOW_SENTS lemma windows around each point."""
    vals = []
    for sent_pk in points:
        i = pos.get(sent_pk)
        if i is None or i < WINDOW_SENTS or i + WINDOW_SENTS >= len(order):
            continue
        before = set().union(*(lem[order[j]] for j in range(i - WINDOW_SENTS, i)))
        after = set().union(*(lem[order[j]] for j in range(i + 1, i + 1 + WINDOW_SENTS)))
        j = jaccard(before, after)
        if j is not None:
            vals.append(1.0 - j)
    return vals


def switch_points(entries):
    """IMPF tokens whose CHAIN_NEIGHBOURS finite-past neighbours are >=CHAIN_MIN_PERF PERF,
    plus matched background PERF points passing the same neighbourhood test."""
    cats = [c for _, _, c in entries]
    impf_pts, perf_pts = [], []
    half = CHAIN_NEIGHBOURS // 2
    for i, (_, sent_pk, cat) in enumerate(entries):
        neigh = cats[max(0, i - half):i] + cats[i + 1:i + 1 + half]
        if len(neigh) < CHAIN_NEIGHBOURS:
            continue
        if sum(1 for c in neigh if c == "PERF") >= CHAIN_MIN_PERF:
            if cat == "IMPF":
                impf_pts.append(sent_pk)
            elif cat == "PERF":
                perf_pts.append(sent_pk)
    return impf_pts, perf_pts


def perm_diff_p(a_vals, b_vals, rng):
    """One-sided permutation test: mean(a) > mean(b)."""
    if not a_vals or not b_vals:
        return None
    obs = sum(a_vals) / len(a_vals) - sum(b_vals) / len(b_vals)
    pool = a_vals + b_vals
    na = len(a_vals)
    ge = 0
    for _ in range(N_PERM):
        rng.shuffle(pool)
        d = sum(pool[:na]) / na - sum(pool[na:]) / (len(pool) - na)
        if d >= obs:
            ge += 1
    return obs, ge / N_PERM


def main():
    rng = random.Random(SEED)
    db = sqlite3.connect(DCS_SQLITE)
    texts, seqs = load(db)
    name_to_period = {n: p for n, (p, _) in PERIOD_MAP.items()}

    out = {"instrument": "imperfect_switching_stats.py over dcs_full.sqlite (dcs-conllu 04e0778)",
           "prereg": "Uprava/QUESTIONS_LOG.md T2607-26 (frozen before first run)",
           "seed": SEED, "n_perm": N_PERM,
           "design": {"window_sents": WINDOW_SENTS, "chain_neighbours": CHAIN_NEIGHBOURS,
                      "chain_min_perf": CHAIN_MIN_PERF, "content_upos": CONTENT_UPOS},
           "slices": {}}

    by_period = defaultdict(list)  # period -> [(text_id, entries)]
    for text_id, entries in seqs.items():
        period = name_to_period.get(texts.get(text_id, ""))
        if period:
            by_period[period].append((text_id, entries))

    for period, items in sorted(by_period.items()):
        sl = {"texts": len(items)}
        # (a) Markov
        trans = Counter()
        marg = Counter()
        for _, entries in items:
            cats = [c for _, _, c in entries]
            trans.update(markov(cats))
            marg.update(cats)
        tot = sum(marg.values())
        sl["category_tokens"] = dict(marg)
        matrix = {}
        for a in ("IMPF", "PERF", "AOR"):
            row_tot = sum(trans[(a, b)] for b in ("IMPF", "PERF", "AOR"))
            if not row_tot:
                continue
            matrix[a] = {}
            for b in ("IMPF", "PERF", "AOR"):
                p = trans[(a, b)] / row_tot
                lift = p / (marg[b] / tot) if marg[b] else None
                matrix[a][b] = {"p": round(p, 4), "lift": round(lift, 2) if lift else None,
                                "n": trans[(a, b)]}
        sl["markov"] = matrix
        # (b) runs test on the 5 largest texts of the slice
        sl["runs_tests"] = {}
        for text_id, entries in sorted(items, key=lambda kv: -len(kv[1]))[:5]:
            r = runs_test([c for _, _, c in entries], rng)
            if r:
                sl["runs_tests"][texts[text_id]] = r
        # (c) switch-point turnover — only where perfect chains exist
        impf_vals, perf_vals, n_texts_used = [], [], 0
        for text_id, entries in items:
            impf_pts, perf_pts = switch_points(entries)
            if len(impf_pts) < 5 or len(perf_pts) < 5:
                continue
            order, pos, lem = sent_lemmas(db, text_id)
            iv = turnover_at(impf_pts, pos, order, lem)
            pv = turnover_at(perf_pts, pos, order, lem)
            if iv and pv:
                impf_vals += iv
                perf_vals += pv
                n_texts_used += 1
        if impf_vals and perf_vals:
            res = perm_diff_p(list(impf_vals), list(perf_vals), rng)
            if res:
                obs, p = res
                sl["turnover"] = {
                    "texts_with_chains": n_texts_used,
                    "impf_insertion_points": len(impf_vals),
                    "background_perf_points": len(perf_vals),
                    "mean_turnover_at_impf": round(sum(impf_vals) / len(impf_vals), 4),
                    "mean_turnover_at_perf": round(sum(perf_vals) / len(perf_vals), 4),
                    "diff": round(obs, 4), "p_one_sided": round(p, 4)}
        out["slices"][period] = sl

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out["slices"], ensure_ascii=False, indent=1)[:3000])
    print("->", OUT)


if __name__ == "__main__":
    main()
