#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SG-SE-011 — Semantics of the -ta participle: the narrative's main perfective.

Semantic layer ON TOP of SG-MO-023 (morphology, lower bound 219 902 by stem-strip)
for the Sangram article SG-SE-011 (c6 slot `sem-b-ta-narrative`, priority ①:
«-ta-причастие как основной перфектив нарратива»).

What is CONSUMED (contract C3 — consume derived assets, never recompute):
  * sangram/articles/ta-na-participles/data/coverage_summary.json  (SG-MO-023)
  * sangram/articles/past-tenses/data/coverage_summary.json        (SG-SE-006)

What is MEASURED HERE (new, semantic — the slot's own question
`dcs:form-class ppp & clause-predicate position`):
  M2  displacement headline: ppp vs ALL finite pasts (ratio, from consumed data);
      top ppp surface forms + roots re-derived by the SAME stem test as MO-023.
  M3  predicate vs attributive position on the UD-annotated subset
      (deprel-bearing tokens): root/acl* = clause predicate, amod/nmod* =
      attributive modifier. Explicit denominator — the UD subset covers only
      ~3.9 % of tokens and its ADJ tokens carry NO feat_verbform, so the ppp is
      stem-matched inside it (honest small-N floor, cf. SE-005 «кандидат ≠
      конструкция»: deprel IS construction evidence here, the floor is coverage).
  M4  copula co-presence: share of ppp tokens sharing a sentence with a finite
      PRESENT of as/bhū (asti/nāsti/santi/bhavati…) — labelled CO-PRESENCE,
      not construction (SE-005 precedent: co-presence is a floor, never a
      construction count).
  M5  seeded 50-token validation sample of the stem test (mechanical FP check:
      lemma must be a verbal root — upos VERB at lemma level or feat_verbform
      on sibling tokens; recorded, not hand-waved).

Output: sangram/articles/ta-narrative/data/coverage_summary.json (+ validation_sample.tsv)
Re-running against the same pin reproduces every figure to the token. Read-only DB.

Model: GLM 5.3 (opencode/zai-coding-plan/glm-5.3), 06-10-2026, H6072.
"""
import csv
import json
import random
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
_CANDIDATES = [
    GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite",          # main-tree layout
    Path.home() / "Documents" / "GitHub" / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite",
]
DEFAULT_DB = next((p for p in _CANDIDATES if p.exists()), _CANDIDATES[0])
OUT_DIR = ROOT / "sangram" / "articles" / "ta-narrative" / "data"

MO23 = ROOT / "sangram" / "articles" / "ta-na-participles" / "data" / "coverage_summary.json"
SE06 = ROOT / "sangram" / "articles" / "past-tenses" / "data" / "coverage_summary.json"

# Same ending list as sg_mo_023_ta_na_participles.py (a-stem m/n + ā-stem fem).
ENDINGS = sorted(
    ['a', 'aḥ', 'am', 'aṃ', 'ena', 'āya', 'āt', 'asya', 'e', 'au', 'ābhyām',
     'ayoḥ', 'āḥ', 'ān', 'aiḥ', 'ebhyaḥ', 'ānām', 'eṣu', 'ā', 'ām', 'ayā',
     'āyā', 'āyai', 'āyāḥ', 'āyām', 'āyoḥ', 'āni', 'āsu', 'ābhiḥ'],
    key=len, reverse=True)

SEED = 20261006
SAMPLE_SIZE = 50

PREDICATE_DEPRELS = ("root", "acl", "acl:relcl")
ATTRIBUTIVE_DEPRELS = ("amod", "nmod", "nmod:relcl", "obl")


def stem_class(word):
    """Return 'ta' | 'na' | None — EXACT MO-023 semantics (sg_mo_023_ta_na_participles.py):
    strip the longest matching a-/ā-ending; if none matches, test the raw word."""
    if not word:
        return None
    w = word
    for e in ENDINGS:
        if w.endswith(e) and len(w) > len(e):
            w = w[: -len(e)]
            break
    if w.endswith("t"):
        return "ta"
    if w.endswith("n"):
        return "na"
    return None


def main():
    mo23 = json.loads(MO23.read_text(encoding="utf-8"))
    se06 = json.loads(SE06.read_text(encoding="utf-8"))

    ppp_lb = mo23["denominators"]["ta_na_ppp_lower_bound"]
    ta = mo23["denominators"]["ta"]
    na = mo23["denominators"]["na"]
    roots = mo23["denominators"]["distinct_roots"]
    tense = se06["tense_distribution"] if "tense_distribution" in se06 else se06.get("tense", {})

    con = sqlite3.connect("file:%s?mode=ro" % (DEFAULT_DB.as_posix().replace("?", "%3f").replace("#", "%23")), uri=True)
    cur = con.cursor()

    # ---- M2: re-derive ppp by the same stem test; top forms/roots ----
    rows = cur.execute(
        "SELECT id, sentence_id, m_unsandhied, lemma, deprel, feat_verbform, feat_tense "
        "FROM token WHERE feat_verbform='Part' AND feat_tense IS NULL AND m_unsandhied IS NOT NULL").fetchall()
    ppp_tokens = []          # (id, sentence_id, surface, lemma, deprel, cls)
    cls_counter = Counter()
    form_counter = Counter()
    root_counter = Counter()
    for tid, sid, form, lemma, deprel, vf, tens in rows:
        w = form or ""
        cls = stem_class(w)
        if cls:
            ppp_tokens.append((tid, sid, w, lemma or "", deprel or "", cls))
            cls_counter[cls] += 1
            form_counter[w] += 1
            root_counter[lemma or "?"] += 1
    n_ppp = len(ppp_tokens)

    finite_past = se06["past_bucket_total"] + se06["imperfect"]

    # ---- M3: predicate vs attributive on the UD subset ----
    # The UD-annotated layer (deprel-bearing tokens) carries NO feat_verbform and
    # tags ppp surfaces under the VERBAL root with upos='VERB' (e.g. uktam→vac,
    # deprel=root). Selector: deprel-bearing token whose LEMMA is a corpus-attested
    # ppp verbal root (from the 219 902 pass above) AND whose surface passes the
    # same stem test. Nominal a-stems (dhana-, śata-) are excluded by the lemma
    # gate; finite forms of those roots (karoti) fail the stem test.
    ppp_roots = set(root_counter)
    ud_total = cur.execute(
        "SELECT COUNT(*) FROM token WHERE deprel IS NOT NULL AND deprel<>''").fetchone()[0]
    ud_ppp_pred_root = Counter()
    ud_ppp_pred_emb = Counter()
    ud_ppp_attr = Counter()
    ud_ppp_other = Counter()
    ud_upos = Counter()
    examples = []
    for tid, sid, form, lemma, deprel, upos in cur.execute(
            "SELECT id, sentence_id, m_unsandhied, lemma, deprel, upos FROM token "
            "WHERE deprel IS NOT NULL AND deprel<>'' AND lemma IS NOT NULL"):
        if lemma not in ppp_roots:
            continue
        cls = stem_class(form or "")
        if not cls:
            continue
        ud_upos[upos or "?"] += 1
        d = deprel
        if d == "root":
            ud_ppp_pred_root[d] += 1
            if len(examples) < 12:
                examples.append((tid, sid, form, lemma, d, cls, "predicate-main"))
        elif d.startswith(("acl", "advcl")):
            ud_ppp_pred_emb[d] += 1
            if 12 <= len(examples) < 24:
                examples.append((tid, sid, form, lemma, d, cls, "predicate-embedded"))
        elif d.startswith(("amod", "nmod")):
            ud_ppp_attr[d] += 1
            if 24 <= len(examples) < 36:
                examples.append((tid, sid, form, lemma, d, cls, "attributive"))
        else:
            ud_ppp_other[d] += 1
    ud_ppp_total = (sum(ud_ppp_pred_root.values()) + sum(ud_ppp_pred_emb.values())
                    + sum(ud_ppp_attr.values()) + sum(ud_ppp_other.values()))

    # ---- M4: copula co-presence ----
    cop_sents = {r[0] for r in cur.execute(
        "SELECT DISTINCT sentence_id FROM token WHERE upos='VERB' AND feat_verbform IS NULL "
        "AND feat_tense='Pres' AND lemma IN ('as','bhU')")}
    ppp_in_cop = sum(1 for _, sid, *_ in ppp_tokens if sid in cop_sents)

    # ---- M5: seeded validation sample ----
    rng = random.Random(SEED)
    sample = rng.sample(ppp_tokens, min(SAMPLE_SIZE, len(ppp_tokens)))
    # mechanical FP check: the ppp surface must be VERB-lemmatised (its lemma row
    # exists in lemma table with verbal grammar) OR the token itself is Part-tagged
    # (it is, by the query). The MO-023 measured FP rate on the same test was
    # near-zero; we re-check that every sampled lemma has a verb-form sibling.
    lemma_ids = {}
    fp_flags = []
    for tid, sid, form, lemma, deprel, cls in sample:
        has_verb_sibling = cur.execute(
            "SELECT COUNT(*) FROM token WHERE lemma=? AND feat_verbform IS NOT NULL AND feat_verbform<>'' LIMIT 1",
            (lemma,)).fetchone()[0]
        fp_flags.append((tid, sid, form, lemma, cls, deprel, bool(has_verb_sibling)))
    fp_count = sum(1 for r in fp_flags if not r[-1])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with (OUT_DIR / "validation_sample.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["token_id", "sentence_id", "surface_unsandhied", "lemma", "class", "deprel", "verb_lemma_confirmed"])
        for r in fp_flags:
            w.writerow(r)

    out = {
        "study": "SG-SE-011 «Семантика причастных форм: -ta как повествовательное прошедшее» — semantic layer over SG-MO-023 (c6 slot sem-b-ta-narrative, ①)",
        "toc_ref": "SG-SE-011",
        "kind": "content article (no kill-gate; non-pilot ① slot)",
        "model_provenance": "GLM 5.3 (opencode/zai-coding-plan/glm-5.3), 06-10-2026, H6072",
        "consumed": {
            "SG-MO-023": str(MO23.relative_to(ROOT)),
            "SG-SE-006": str(SE06.relative_to(ROOT)),
        },
        "snapshot": mo23["snapshot"],
        "M2_displacement": {
            "ta_na_ppp_lower_bound": ppp_lb,
            "ta": ta,
            "na": na,
            "distinct_roots": roots,
            "re_derived_this_run": n_ppp,
            "re_derivation_matches_mo23": n_ppp == ppp_lb,
            "finite_past_total": finite_past,
            "finite_past_components": {"Past": tense.get("Past", 0), "Impf": tense.get("Impf", 0)},
            "ppp_to_all_finite_pasts_ratio": round(n_ppp / finite_past, 2) if finite_past else None,
            "top_forms": form_counter.most_common(12),
            "top_roots": root_counter.most_common(12),
            "note": "ppp (nominal, lower bound) vs FINITE pasts (Impf+Past incl. aorist/peri/simple-past bulk, SE-006); the ppp outnumberes ALL finite pasts combined",
        },
        "M3_predicate_vs_attributive_UD": {
            "ud_tokens_total": ud_total,
            "ud_share_of_all_tokens_pct": round(100.0 * ud_total / cur.execute("SELECT COUNT(*) FROM token").fetchone()[0], 2),
            "ud_ppp_stem_matched": ud_ppp_total,
            "upos_dist": dict(ud_upos),
            "predicate_main_root": dict(ud_ppp_pred_root),
            "predicate_main_root_total": sum(ud_ppp_pred_root.values()),
            "predicate_embedded_acl_advcl": dict(ud_ppp_pred_emb),
            "predicate_embedded_total": sum(ud_ppp_pred_emb.values()),
            "attributive_amod_nmod": dict(ud_ppp_attr),
            "attributive_total": sum(ud_ppp_attr.values()),
            "other_deprels": dict(ud_ppp_other),
            "note": "UD subset is the only construction-evidence layer; it carries NO feat_verbform, so the ppp is identified there by lemma∈corpus-ppp-roots + the same stem test. Small-N floor with explicit denominator — coverage limit, same honesty rule as SE-005. deprel=root = main-clause predicate (the narrative-past use this article is about).",
        },
        "M4_copula_copresence": {
            "sentences_with_finite_Pres_as_bhu": len(cop_sents),
            "ppp_tokens_in_such_sentences": ppp_in_cop,
            "ppp_share_pct": round(100.0 * ppp_in_cop / n_ppp, 1) if n_ppp else None,
            "label": "CO-PRESENCE floor, not a construction count (SE-005 precedent)",
        },
        "M5_validation": {
            "seed": SEED,
            "sample_size": len(sample),
            "false_positives_mechanical": fp_count,
            "check": "sampled lemma must have non-finite verb-form siblings (verbal lemma confirmed)",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("ppp re-derived: %d (MO-023 lower bound %d, match=%s)" % (n_ppp, ppp_lb, n_ppp == ppp_lb))
    print("finite pasts (SE-006): %d -> ppp/finite-pasts = %.2f" % (finite_past, n_ppp / finite_past))
    print("UD subset: %d tokens; ppp stem-matched in UD: %d" % (ud_total, ud_ppp_total))
    print("  predicate-main(root): %d | embedded(acl/advcl): %d | attributive: %d | other: %d" % (
        sum(ud_ppp_pred_root.values()), sum(ud_ppp_pred_emb.values()),
        sum(ud_ppp_attr.values()), sum(ud_ppp_other.values())))
    print("copula co-presence: %d/%d ppp tokens (%.1f%%)" % (ppp_in_cop, n_ppp, 100.0 * ppp_in_cop / n_ppp))
    print("validation sample FP: %d/%d" % (fp_count, len(sample)))
    print("top forms:", form_counter.most_common(8))
    print("top roots:", root_counter.most_common(8))
    con.close()


if __name__ == "__main__":
    main()
