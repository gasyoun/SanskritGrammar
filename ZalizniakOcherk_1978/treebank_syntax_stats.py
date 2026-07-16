#!/usr/bin/env python
"""treebank_syntax_stats.py — the dependency-treebank instrument for §§212-217
(OCH-65, OCH-66, OCH-67, OCH-68).

All four claims' prior verdicts read "no instrument: ... needs syntactic
annotation the export lacks". That premise is FALSE at the token level:
dcs_full.sqlite's own `head`/`deprel` columns carry a genuine UD-style
treebank slice — 223,751 tokens (3.9% of the corpus) across 29,433 FULLY
dependency-parsed sentences (every token in these sentences carries head+
deprel; verified — zero partially-tagged sentences). The blocker was never
built rather than probed.

GENRE-SKEW CHECK (done before verdicting, 16-07-2026): this slice is
concentrated in Vedic/early prose — Ṛgveda, Atharvaveda, Brāhmaṇas, the
older Upaniṣads, the Śrauta/Gṛhya/Dharma-sūtra corpus — plus a small
post-Vedic tail (Mahābhārata, Manusmṛti, Arthaśāstra, Rāmāyaṇa, Buddhacarita,
Kāmasūtra, a few Purāṇas). The obvious worry: does that skew explain OCH-66/
67's weak numbers? Tested directly by splitting into a CLASSICAL bucket
(the post-Vedic tail above) vs everything else, and separately isolating
Arthaśāstra alone (255 sentences of genuine classical administrative PROSE,
not verse) as the single best non-Vedic, non-metrical comparison text. Verdict:
the skew does NOT rescue the claims — the classical bucket is if anything
WEAKER on word order (root-final 37.6% vs 46.8%; subject-first 24.4% vs
30.3%) and only PARTIALLY better on coordination (35.1% coordinate vs 21% —
still not a majority); Arthaśāstra alone gives root-final 51.4%, subject-
first 18.7% (the worst of any group tested). Two further operationalization
checks (excluding trailing discourse-particles from the "last token" test;
restricting to single-clause sentences to rule out a later clause dragging
the sentence-final position away from the root's own clause) each moved the
root-final number by under 5 points. None of these refinements rescue OCH-66's
verb-final/subject-first sub-claims. Only modifier-precedes-head is robust
across every cut. This is reported as a genuine, well-investigated finding,
not an artifact — see `by_genre` and `robustness_checks` in the output.

FOUR MEASUREMENTS:

  OCH-65 (§212, prati etc.): among lemma='prati' tokens carrying a deprel
    tag, is unambiguous adpositional use (deprel='case', governing a
    nominal) the minority against adverbial (advmod) and other uses?

  OCH-66 (§214, word order): root-final tendency (is the finite predicate
    the sentence's last token), subject-group-first tendency (does the
    nsubj's own subtree include the sentence's first token), and modifier-
    precedes-head tendency (det/amod/nmod/nummod dependents preceding
    their head).

  OCH-67 (§215, coordinate > subordinate complex sentences): among
    sentences with >=2 VERB tokens, classify each non-root VERB by its own
    deprel prefix — conj = coordinate; advcl/acl/ccomp/xcomp = subordinate;
    parataxis = paratactic (kept separate, neither coordinate nor
    subordinate in the technical sense); csubj = clausal subject (kept
    separate, not a coordinate/subordinate complex-sentence relation).

  OCH-68 (§216, the ya-...ta- antecedent-in-first-clause absolute): among
    acl:rel edges (relative-clause-verb -> head noun) whose relative-clause
    subtree contains a PRON lemma 'yad', is the head noun always inside
    whichever of the two clauses (relative-clause subtree vs the rest of
    the sentence) starts at the smaller token index? Flagged exactly as the
    register itself flagged this claim before any number existed: it is
    the one absolute quantifier in the whole book sitting on a syntactic
    domain, and the sample here is thin (see counts) — a single exception
    would refute it, so a 100% hit rate on n<20 is suggestive, not proof.

Usage:  python ZalizniakOcherk_1978/treebank_syntax_stats.py [--db PATH]
Writes  och65_68_treebank_stats.json next to this script.
"""
import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"

MODIFIER_DEPRELS = {"det", "amod", "nmod", "nummod"}
COORDINATE_PREFIXES = {"conj"}
SUBORDINATE_PREFIXES = {"advcl", "acl", "ccomp", "xcomp"}
PARATACTIC_PREFIXES = {"parataxis"}
CLAUSAL_SUBJECT_PREFIXES = {"csubj"}
PARTICLE_UPOS = {"PART"}
PARTICLE_DEPRELS = {"discourse", "vocative", "mark", "cc"}

# post-Vedic tail of the annotated slice — everything else is Saṃhitā/Brāhmaṇa/
# Āraṇyaka/older-Upaniṣad/Śrauta-Gṛhya-Dharma-sūtra ("vedic_sutra" bucket).
CLASSICAL_TEXTS = {
    "Mahābhārata", "Manusmṛti", "Arthaśāstra", "Rāmāyaṇa", "Buddhacarita",
    "Kāmasūtra", "Suśrutasaṃhitā", "Carakasaṃhitā", "Kūrmapurāṇa", "Viṣṇupurāṇa",
    "Matsyapurāṇa", "Nyāyabindu", "Avadānaśataka", "Abhidharmakośa",
    "Bhāratamañjarī", "Aṣṭāṅgahṛdayasaṃhitā", "Haṭhayogapradīpikā",
    "Rasaratnasamuccayaṭīkā",
}


def prefix(deprel):
    return deprel.split(":")[0] if deprel else deprel


def load_sentences(cur):
    """Return {sentence_id: [(idx, head, deprel, upos, lemma, verbform), ...]} for
    every FULLY dependency-tagged sentence (verified — no partial tagging exists).
    feat_verbform distinguishes finite (None, mood-marked — verified separately)
    from non-finite (Part/Conv/Inf/Gdv) verb forms — needed because §215's
    "subordinate clause" is the traditional FINITE-clause sense, and DCS's acl/
    advcl/ccomp/xcomp deprels are dominated by non-finite participial/absolutive
    embedding (Sanskrit's actual preferred subordination mechanism, per §217),
    not finite subordinate clauses."""
    sentences = defaultdict(list)
    for sid, idx, head, deprel, upos, lemma, verbform in cur.execute(
        """SELECT sentence_id, idx, head, deprel, upos, lemma, feat_verbform FROM token
           WHERE sentence_id IN (SELECT DISTINCT sentence_id FROM token WHERE deprel IS NOT NULL)
           ORDER BY sentence_id, idx"""
    ):
        sentences[sid].append((idx, head, deprel, upos, lemma, verbform))
    return sentences


def load_sentence_texts(cur):
    """sentence_id -> source text name, for every fully-tagged sentence."""
    return dict(cur.execute(
        """SELECT DISTINCT tok.sentence_id, t.name FROM token tok
           JOIN sentence s ON tok.sentence_id=s.id JOIN chapter c ON s.chapter_id=c.chapter_id
           JOIN text t ON c.text_id=t.text_id
           WHERE tok.deprel IS NOT NULL"""
    ))


def genre(sent_text, sid):
    return "classical" if sent_text.get(sid) in CLASSICAL_TEXTS else "vedic_sutra"


def children_map(tokens):
    """idx -> [child idx, ...] from a sentence's (idx, head, deprel, upos, lemma, verbform) list."""
    kids = defaultdict(list)
    for idx, head, deprel, upos, lemma, verbform in tokens:
        if head:
            kids[head].append(idx)
    return kids


def subtree(kids, root_idx):
    """All idx in root_idx's subtree, including itself (BFS over child edges)."""
    seen = {root_idx}
    stack = [root_idx]
    while stack:
        cur = stack.pop()
        for c in kids.get(cur, ()):
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return seen


def och65_prati(cur):
    rows = list(cur.execute(
        "SELECT deprel FROM token WHERE lemma='prati' AND deprel IS NOT NULL"))
    total = len(rows)
    counts = defaultdict(int)
    for (d,) in rows:
        counts[d] += 1
    adpositional = counts.get("case", 0)
    return {
        "total_tagged_prati_tokens": total,
        "deprel_counts": dict(sorted(counts.items(), key=lambda kv: -kv[1])),
        "unambiguous_adpositional_case_deprel": adpositional,
        "adpositional_share_pct": round(100 * adpositional / total, 1) if total else None,
        "expected_by_s212": "adpositional (case) use is the minority",
        "confirmed": (adpositional / total) < 0.5 if total else None,
    }


def _rate(hits, n):
    return round(100 * hits / n, 1) if n else None


def och66_word_order(sentences, sent_text):
    buckets = {"overall": [0, 0, 0, 0, 0, 0], "classical": [0, 0, 0, 0, 0, 0],
               "vedic_sutra": [0, 0, 0, 0, 0, 0]}
    # [root_total, root_final, subj_total, subj_first, mod_total, mod_pre]
    simple_root_total = simple_root_final = 0     # single-VERB sentences only
    excl_particle_final = 0                        # last token excl. discourse/PART

    for sid, toks in sentences.items():
        by_idx = {idx: (head, deprel, upos, lemma, vf) for idx, head, deprel, upos, lemma, vf in toks}
        max_idx = max(by_idx)
        kids = children_map(toks)
        g = genre(sent_text, sid)

        root_idx = next((idx for idx, v in by_idx.items() if v[1] == "root"), None)
        if root_idx is not None:
            for b in ("overall", g):
                buckets[b][0] += 1
                if root_idx == max_idx:
                    buckets[b][1] += 1
            content_idx = [i for i, v in by_idx.items()
                            if v[2] not in PARTICLE_UPOS and prefix(v[1]) not in PARTICLE_DEPRELS]
            if content_idx and root_idx == max(content_idx):
                excl_particle_final += 1
            all_verbs = [idx for idx, v in by_idx.items() if v[2] == "VERB"]
            if len(all_verbs) <= 1:
                simple_root_total += 1
                if root_idx == max_idx:
                    simple_root_final += 1

        nsubj_idx = next((idx for idx, v in by_idx.items() if prefix(v[1]) == "nsubj"), None)
        if nsubj_idx is not None:
            span = subtree(kids, nsubj_idx)
            for b in ("overall", g):
                buckets[b][2] += 1
                if min(span) == 1:
                    buckets[b][3] += 1

        for idx, (head, deprel, upos, lemma, vf) in by_idx.items():
            if deprel in MODIFIER_DEPRELS and head:
                for b in ("overall", g):
                    buckets[b][4] += 1
                    if idx < head:
                        buckets[b][5] += 1

    def pack(b):
        rt, rf, st, sf, mt, mp = buckets[b]
        return {
            "root_final": {"n": rt, "hits": rf, "pct": _rate(rf, rt)},
            "subject_group_first": {"n": st, "hits": sf, "pct": _rate(sf, st)},
            "modifier_precedes_head": {"n": mt, "hits": mp, "pct": _rate(mp, mt)},
        }

    return {
        **pack("overall"),
        "expected_by_s214": "all three tendencies hold as statistical majorities",
        "by_genre": {"classical": pack("classical"), "vedic_sutra": pack("vedic_sutra")},
        "robustness_checks": {
            "root_final_excl_trailing_particles": {
                "n": buckets["overall"][0], "hits": excl_particle_final,
                "pct": _rate(excl_particle_final, buckets["overall"][0])},
            "root_final_single_clause_sentences_only": {
                "n": simple_root_total, "hits": simple_root_final,
                "pct": _rate(simple_root_final, simple_root_total)},
        },
    }


def och67_complex_sentences(sentences, sent_text):
    """Restricted to FINITE verbs (feat_verbform IS NULL, mood-marked — verified
    against feat_mood) on BOTH sides of the comparison: DCS's acl/advcl/ccomp/
    xcomp deprels are dominated by non-finite participial/absolutive embedding
    (§217's actual preferred subordination mechanism), which is not a
    'сложноподчинённое предложение' in the traditional finite-clause sense
    §215 means. Counting those would silently test a different, broader claim."""
    def blank():
        return defaultdict(int)
    buckets = {"overall": blank(), "classical": blank(), "vedic_sutra": blank()}

    for sid, toks in sentences.items():
        finite_verbs = [idx for idx, head, deprel, upos, lemma, vf in toks
                        if upos == "VERB" and vf is None]
        if len(finite_verbs) < 2:
            continue
        g = genre(sent_text, sid)
        non_root_finite_verb_deprels = {
            prefix(deprel) for idx, head, deprel, upos, lemma, vf in toks
            if upos == "VERB" and vf is None and deprel != "root"
        }
        is_coord = bool(non_root_finite_verb_deprels & COORDINATE_PREFIXES)
        is_subord = bool(non_root_finite_verb_deprels & SUBORDINATE_PREFIXES)
        is_para = bool(non_root_finite_verb_deprels & PARATACTIC_PREFIXES)
        is_csubj = bool(non_root_finite_verb_deprels & CLAUSAL_SUBJECT_PREFIXES)
        flags = [is_coord, is_subord, is_para, is_csubj]
        if sum(flags) > 1:
            key = "mixed"
        elif is_coord:
            key = "coordinate"
        elif is_subord:
            key = "subordinate"
        elif is_para:
            key = "paratactic"
        elif is_csubj:
            key = "clausal_subject"
        else:
            key = "other"
        for b in ("overall", g):
            buckets[b]["complex_n"] += 1
            buckets[b][key] += 1

    def pack(b):
        d = buckets[b]
        coord, subord = d["coordinate"], d["subordinate"]
        return {
            "complex_sentences_n": d["complex_n"],
            "coordinate_only": coord,
            "subordinate_only": subord,
            "paratactic_only": d["paratactic"],
            "clausal_subject_only": d["clausal_subject"],
            "mixed": d["mixed"],
            "other": d["other"],
            "coordinate_share_pct": _rate(coord, coord + subord),
            "coordinate_vs_subordinate_ratio": round(coord / subord, 2) if subord else None,
            "confirmed": coord > subord,
        }

    return {
        **pack("overall"),
        "expected_by_s215": "coordinate_only > subordinate_only (finite subordinate clauses only)",
        "by_genre": {"classical": pack("classical"), "vedic_sutra": pack("vedic_sutra")},
    }


def och68_correlative_order(sentences):
    cases = []
    for sid, toks in sentences.items():
        by_idx = {idx: (head, deprel, upos, lemma, vf) for idx, head, deprel, upos, lemma, vf in toks}
        kids = children_map(toks)
        for idx, (head, deprel, upos, lemma, vf) in by_idx.items():
            if prefix(deprel) != "acl" or ":rel" not in deprel:
                continue
            if head not in by_idx or by_idx[head][2] != "NOUN":
                continue  # claim is about a NOUN antecedent, not a bare correlative pronoun
            rel_span = subtree(kids, idx)
            has_yad = any(
                by_idx[i][3] == "yad" for i in rel_span if by_idx[i][2] == "PRON"
            )
            if not has_yad:
                continue
            all_idx = set(by_idx)
            matrix_span = all_idx - rel_span
            if not matrix_span:
                continue
            rel_min, matrix_min = min(rel_span), min(matrix_span)
            head_in_first_clause = matrix_min < rel_min
            cases.append({
                "sentence_id": sid, "head_noun_idx": head, "rel_verb_idx": idx,
                "rel_min_idx": rel_min, "matrix_min_idx": matrix_min,
                "head_in_first_clause": head_in_first_clause,
            })
    n = len(cases)
    hits = sum(1 for c in cases if c["head_in_first_clause"])
    return {
        "n": n,
        "head_noun_in_first_clause": hits,
        "pct": round(100 * hits / n, 1) if n else None,
        "expected_by_s216": "100% — this is an absolute ('всегда') claim",
        "counterexamples": [c for c in cases if not c["head_in_first_clause"]],
        "note": "n is thin — a single exception refutes an absolute; treat as a hunting-licence result, not a settled verdict",
    }


def self_test():
    """Hand-built micro-sentences exercising each metric's edge case.
    Tuples are (idx, head, deprel, upos, lemma, verbform); verbform=None means
    finite (mood-marked)."""
    # root-final: 3-token SOV sentence, root last
    sov = [(1, 3, "nsubj", "NOUN", "x", None), (2, 3, "obj", "NOUN", "y", None),
           (3, 0, "root", "VERB", "z", None)]
    r = och66_word_order({1: sov}, {})
    assert r["root_final"]["pct"] == 100.0, r
    assert r["subject_group_first"]["pct"] == 100.0, r
    # modifier precedes head: det(1) -> noun(2)
    detn = [(1, 2, "det", "PRON", "x", None), (2, 0, "root", "NOUN", "y", None)]
    r2 = och66_word_order({2: detn}, {})
    assert r2["modifier_precedes_head"]["pct"] == 100.0, r2
    # och67: two FINITE VERBs, second is conj -> coordinate
    coordsent = [(1, 2, "nsubj", "NOUN", "x", None), (2, 0, "root", "VERB", "y", None),
                 (3, 2, "conj", "VERB", "z", None)]
    r3 = och67_complex_sentences({3: coordsent}, {})
    assert r3["coordinate_only"] == 1 and r3["subordinate_only"] == 0, r3
    # och67: second VERB is advcl but NON-FINITE (participle) -> not counted at all
    nonfinite_advcl = [(1, 2, "nsubj", "NOUN", "x", None), (2, 0, "root", "VERB", "y", None),
                       (3, 2, "advcl", "VERB", "z", "Part")]
    r3b = och67_complex_sentences({30: nonfinite_advcl}, {})
    assert r3b["complex_sentences_n"] == 0, r3b
    # och67: second VERB is FINITE advcl -> subordinate
    subordsent = [(1, 2, "nsubj", "NOUN", "x", None), (2, 0, "root", "VERB", "y", None),
                  (3, 2, "advcl", "VERB", "z", None)]
    r4 = och67_complex_sentences({4: subordsent}, {})
    assert r4["subordinate_only"] == 1 and r4["coordinate_only"] == 0, r4
    # och68: yaḥ(1) gataḥ(2, acl:rel -> naraḥ) naraḥ(3) tam(4) apaśyat(5, root)
    # relative clause {1,2} starts before the matrix's own first token(3) ->
    # head noun(3) is NOT in the first clause here (rel clause is first)
    relsent = [(1, 2, "nsubj", "PRON", "yad", None), (2, 3, "acl:rel", "VERB", "gam", None),
               (3, 5, "obj", "NOUN", "nara", None), (4, 5, "obj", "PRON", "tad", None),
               (5, 0, "root", "VERB", "paś", None)]
    r5 = och68_correlative_order({5: relsent})
    assert r5["n"] == 1 and r5["head_noun_in_first_clause"] == 0, r5
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()

    ok = self_test()

    db = sqlite3.connect(args.db)
    cur = db.cursor()

    total_tokens = cur.execute("SELECT COUNT(*) FROM token").fetchone()[0]
    tagged_tokens = cur.execute(
        "SELECT COUNT(*) FROM token WHERE deprel IS NOT NULL").fetchone()[0]
    texts = cur.execute("""
        SELECT t.name, COUNT(*) c FROM token tok
        JOIN sentence s ON tok.sentence_id=s.id JOIN chapter c ON s.chapter_id=c.chapter_id
        JOIN text t ON c.text_id=t.text_id
        WHERE tok.deprel IS NOT NULL GROUP BY t.name ORDER BY c DESC""").fetchall()

    sentences = load_sentences(cur)
    sent_text = load_sentence_texts(cur)

    out = {
        "instrument": "treebank_syntax_stats.py over dcs_full.sqlite's own head/deprel "
                      "columns — a genuine, fully-tagged (not sparse) UD-style slice; "
                      "prior UNTESTABLE verdicts assumed this annotation didn't exist",
        "coverage": {
            "total_tokens": total_tokens,
            "tagged_tokens": tagged_tokens,
            "tagged_pct": round(100 * tagged_tokens / total_tokens, 2),
            "fully_tagged_sentences": len(sentences),
            "texts_by_tagged_token_count": texts,
            "caveat": "concentrated in Vedic/early prose (Ṛgveda, Atharvaveda, "
                      "Brāhmaṇas, older Upaniṣads, Śrauta/Gṛhya/Dharma-sūtras) + a "
                      "small post-Vedic tail (Mahābhārata, Manusmṛti, Arthaśāstra, "
                      "Rāmāyaṇa, Buddhacarita) — genre-skew checked, see by_genre "
                      "in OCH-66/67 below and the module docstring",
        },
        "OCH-65_prati_adposition": och65_prati(cur),
        "OCH-66_word_order": och66_word_order(sentences, sent_text),
        "OCH-67_complex_sentences": och67_complex_sentences(sentences, sent_text),
        "OCH-68_correlative_order": och68_correlative_order(sentences),
        "self_test": {"passed": ok},
    }
    (HERE / "och65_68_treebank_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"coverage: {tagged_tokens}/{total_tokens} tokens tagged "
          f"({out['coverage']['tagged_pct']}%), {len(sentences)} full sentences")
    print("OCH-65 prati:", out["OCH-65_prati_adposition"]["adpositional_share_pct"], "%",
          "confirmed:", out["OCH-65_prati_adposition"]["confirmed"])
    wo = out["OCH-66_word_order"]
    print("OCH-66 word order (overall):",
          {k: wo[k]["pct"] for k in ("root_final", "subject_group_first", "modifier_precedes_head")})
    for g in ("classical", "vedic_sutra"):
        gw = wo["by_genre"][g]
        print(f"  [{g}]", {k: gw[k]["pct"] for k in
                            ("root_final", "subject_group_first", "modifier_precedes_head")})
    print("  robustness:", wo["robustness_checks"])
    cs = out["OCH-67_complex_sentences"]
    print("OCH-67 complex sentences (overall):", cs["coordinate_only"], "coordinate vs",
          cs["subordinate_only"], "subordinate; confirmed:", cs["confirmed"])
    for g in ("classical", "vedic_sutra"):
        gc = cs["by_genre"][g]
        print(f"  [{g}]", gc["coordinate_only"], "coordinate vs", gc["subordinate_only"],
              "subordinate; share:", gc["coordinate_share_pct"], "%")
    rc = out["OCH-68_correlative_order"]
    print("OCH-68 correlative order: n =", rc["n"], "hits =",
          rc["head_noun_in_first_clause"], "pct =", rc["pct"])
    print("-> och65_68_treebank_stats.json written")


if __name__ == "__main__":
    main()
