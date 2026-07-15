#!/usr/bin/env python3
"""SG-MO-017 pilot P3: the perfect via form-class, not UD tense (C5 § 7 P3).

Direct test of evidence-limit EM2 (C5 § 5.2 / C3 defect Д1): DCS's UD conversion
collapses all preterites under `Tense=Past` — the perfect is NOT separable from
the aorist (and imperfect residue) by the tense feature. The C2 slot SG-MO-017
therefore specifies selection by *form-class* (`dcs:form-class perfect`), i.e.
reduplication, not `Tense=Past`. This pilot asks whether that form-class actually
exists in the corpus, and measures how much of the perfect it can isolate.

Empirical finding (what fires the kill-gate): DCS's own form-class feature
(`feat_formation`) has NO `perfect` value. Within the Past bucket it offers:
  - `peri`  (periphrastic perfect: -ām + auxiliary — deśayām **āsa**): the ONLY
            form-evidently-perfect tag.
  - `red`   (reduplicated) — but under Past this is the reduplicated **AORIST**
            (augmented: a-dad-at, a-jī-jan-at, a-vī-vṛdh-an), a FALSE FRIEND for
            the perfect, NOT the reduplicated perfect.
  - `s/is/sa/sis/them/root` : the sigmatic / thematic / root aorists.
  - NULL    : ~84 % of Past tokens carry no formation tag at all — and the
            canonical reduplicated perfect (ja-gau, ca-kāra, vi-duḥ, ja-gāda)
            lives HERE, morphologically indistinguishable from the untagged
            aorist / imperfect residue.

So the primary perfect formation (reduplication) is 0 % recoverable via the
corpus form-class feature; only the minor periphrastic sub-type (which is really
slot SG-MO-032) is form-attestable. Kill-gate P3 (< 95 % of the sample isolable
by form-class) fires hard → the quantitative perfect count is withdrawn; the
honest negative result is published, plus the one attestable sliver (periphrastic
perfect distribution) as a lower bound.

A conservative surface reduplication heuristic is run only to MEASURE that even a
bespoke rule cannot separate the perfect (it conflates reduplicated present
class III + reduplicated aorist + perfect) — a negative pilot recorded with
numbers, never used as a corpus fact (cf. the sibling programme's OCH-22/23 dead
ends).

Ground truth is consumed, never rebuilt (C3 § 2.1): the pinned VisualDCS SQLite
master. No external inventory is needed for this pilot (the question is internal
to DCS's own features).

Usage:
  python scripts/sg_mo_017_perfect_coverage.py [--db PATH] [--skip-checksum]
Outputs into sangram/articles/perfect/data/ .
"""
import argparse
import csv
import hashlib
import json
import random
import re
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "perfect" / "data"

SEED = 20260715
SAMPLE_SIZE = 80

# The preterite bucket EM2 conflates: finite verb, Tense=Past.
UNIV = ("t.upos = 'VERB' AND t.feat_tense = 'Past' "
        "AND (t.feat_verbform IS NULL OR t.feat_verbform = 'Fin')")

# feat_formation partition of the Past bucket.
FORM_PERFECT = {"peri"}                              # periphrastic perfect — form-evident
FORM_AORIST = {"s", "is", "sa", "sis", "them", "root", "red"}  # red = redupl. AORIST here

# Periphrastic-perfect auxiliary tails (Whitney §1070–1073: as / kṛ / bhū).
AUX_AS = ("āsa", "āsuḥ", "āsatuḥ", "āsathur", "āsan", "āsam", "āsi", "āsuṣ")
AUX_KR = ("cakāra", "cakruḥ", "cakre", "cakratuḥ", "cakrire", "cakartha", "cakruṣ")
AUX_BHU = ("babhūva", "babhūvuḥ", "babhūvatuḥ")

# Conservative surface reduplication heuristic (SECONDARY probe only).
# Augment a-/ā- before a consonant ⇒ aorist/imperfect, NOT perfect; the perfect
# is augmentless. Perfect endings on an augmentless stem.
AUGMENT = re.compile(r"^ā?a?[bcdgjklmnpstrvyśṣhḍṭṇñṅ]")
PF_END = re.compile(r"(atuḥ|uḥ|re|rire|iṣe|ima|iva|itha|tha|us|au|e|a)$")


def aux_of(uns: str) -> str:
    if not uns:
        return "?"
    if uns.endswith(AUX_AS):
        return "as"
    if uns.endswith(AUX_KR):
        return "kṛ"
    if uns.endswith(AUX_BHU):
        return "bhū"
    return "other"


def looks_reduplicated(uns: str) -> bool:
    """Very rough: initial C1 V (C2) ... where C1 echoes an early consonant, and
    no augment. Deliberately crude — its only job is to be shown inadequate."""
    if not uns or len(uns) < 4:
        return False
    if uns[0] in "aā":                       # augmented ⇒ not a perfect
        return False
    # first consonant repeats within the first 4 chars (jagāma: j..g; babhūva: b..bh)
    c1 = uns[0]
    palatal = {"j": "g", "c": "k"}           # Grassmann palatal reduplicant
    stem_c = palatal.get(c1, c1)
    body = uns[1:5]
    return (c1 in body or stem_c in body) and bool(PF_END.search(uns))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--skip-checksum", action="store_true")
    args = ap.parse_args()

    db = Path(args.db)
    if not db.exists():
        print(f"ERROR: DCS master not found: {db}")
        return 1
    con = sqlite3.connect(db)
    cur = con.cursor()

    prov = dict(cur.execute("SELECT * FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 § 2.1)")
        return 1
    sha256 = None
    if not args.skip_checksum:
        h = hashlib.sha256()
        with open(db, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 22), b""):
                h.update(chunk)
        sha256 = h.hexdigest()

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # ---- tense framing (context for the EM2 conflation) ----
    tense_ctx = {}
    for tn, n in cur.execute(
            "SELECT feat_tense, COUNT(*) FROM token t WHERE t.upos='VERB' "
            "AND (t.feat_verbform IS NULL OR t.feat_verbform='Fin') "
            "GROUP BY feat_tense").fetchall():
        tense_ctx[tn or "None"] = n

    total = cur.execute(f"SELECT COUNT(*) FROM token t WHERE {UNIV}").fetchone()[0]

    # ---- feat_formation partition of Past ----
    form_counts = Counter()
    for fm, n in cur.execute(
            f"SELECT t.feat_formation, COUNT(*) FROM token t WHERE {UNIV} "
            "GROUP BY t.feat_formation").fetchall():
        form_counts[fm or "NULL"] = n

    peri = sum(form_counts.get(f, 0) for f in FORM_PERFECT)
    aorist_formed = sum(form_counts.get(f, 0) for f in FORM_AORIST)
    unmarked = form_counts.get("NULL", 0)

    # ---- periphrastic-perfect distribution (the one attestable sliver) ----
    peri_rows = cur.execute(
        f"SELECT t.m_unsandhied, t.lemma, t.feat_person, t.feat_number, t.feat_voice "
        f"FROM token t WHERE {UNIV} AND t.feat_formation='peri'").fetchall()
    aux_counter = Counter()
    peri_pn = Counter()
    peri_lemma = Counter()
    peri_voice = Counter()
    for uns, lemma, person, number, voice in peri_rows:
        aux_counter[aux_of(uns)] += 1
        peri_pn[f"{person or '?'}{(number or '?')[:2]}"] += 1
        peri_lemma[lemma] += 1
        peri_voice[voice or "Act"] += 1

    # ---- red-tag false-friend demonstration (reduplicated aorist under Past) ----
    red_examples = cur.execute(
        f"SELECT t.m_unsandhied, t.lemma FROM token t WHERE {UNIV} "
        "AND t.feat_formation='red' ORDER BY t.m_unsandhied LIMIT 12").fetchall()

    # ---- pluperfect (separately tense-tagged, unlike the perfect) ----
    plp = cur.execute(
        "SELECT COUNT(*) FROM token t WHERE t.upos='VERB' "
        "AND t.feat_tense IN ('Plp','Pqp')").fetchone()[0]

    # ---- secondary surface reduplication heuristic over the NULL bucket ----
    heur_hits = 0
    for (uns,) in cur.execute(
            f"SELECT t.m_unsandhied FROM token t WHERE {UNIV} "
            "AND t.feat_formation IS NULL").fetchall():
        if looks_reduplicated(uns or ""):
            heur_hits += 1

    # ---------------------- kill-gate validation sample ---------------------- #
    ids = [r[0] for r in cur.execute(f"SELECT t.id FROM token t WHERE {UNIV}").fetchall()]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), SAMPLE_SIZE)
    detail_sql = (
        "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.lemma_id, l.grammar, "
        "t.feat_formation, t.feat_person, t.feat_number, t.feat_voice, "
        "s.text_sandhied, c.ref, x.name "
        "FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
        "JOIN sentence s ON s.id=t.sentence_id "
        "JOIN chapter c ON c.chapter_id=s.chapter_id "
        "JOIN text x ON x.text_id=c.text_id WHERE t.id=?")
    sample_rows = []
    formclass_isolable = 0            # tokens the form-class feature positively assigns
    for tid in chosen:
        r = cur.execute(detail_sql, (tid,)).fetchone()
        (_id, form, uns, lemma, lid, grammar, formation, person, number,
         voice, sent, ref, textname) = r
        if formation in FORM_PERFECT:
            fc = "perfect(peri)"
        elif formation in FORM_AORIST:
            fc = f"aorist({formation})"
        else:
            fc = "UNMARKED"
        if formation in FORM_PERFECT or formation in FORM_AORIST:
            formclass_isolable += 1
        sample_rows.append([
            tid, form, uns or "", lemma, lid, grammar or "", formation or "",
            fc, person or "", number or "", voice or "",
            (sent or "")[:160], ref or "", textname or "",
            "",  # adjudicated_category (perfect/aorist/imperfect/other) — filled by hand
            "",  # note
        ])

    # ---------------------------- write outputs ---------------------------- #
    with open(OUT_DIR / "formation_partition.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["feat_formation", "tokens", "pct_of_past", "reading"])
        readings = {
            "peri": "periphrastic perfect — form-evident PERFECT",
            "red": "reduplicated AORIST (augmented) — FALSE FRIEND, not the perfect",
            "s": "s-aorist", "is": "iṣ-aorist", "sa": "sa-aorist", "sis": "siṣ-aorist",
            "them": "thematic aorist", "root": "root aorist",
            "NULL": "UNMARKED — reduplicated perfect hides here, mixed with aorist/impf",
        }
        for fm, n in form_counts.most_common():
            w.writerow([fm, n, round(100 * n / total, 2), readings.get(fm, "")])

    with open(OUT_DIR / "periphrastic_perfect.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["dimension", "key", "tokens", "pct"])
        for k, n in aux_counter.most_common():
            w.writerow(["auxiliary", k, n, round(100 * n / peri, 2)])
        for k, n in peri_pn.most_common():
            w.writerow(["person_number", k, n, round(100 * n / peri, 2)])
        for k, n in peri_voice.most_common():
            w.writerow(["voice", k, n, round(100 * n / peri, 2)])
        for k, n in peri_lemma.most_common(20):
            w.writerow(["top_base_stem", k, n, round(100 * n / peri, 2)])

    with open(OUT_DIR / "validation_sample.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "lemma_id",
                    "dcs_grammar", "feat_formation", "form_class_reading",
                    "person", "number", "voice", "sentence", "chapter_ref",
                    "text", "adjudicated_category", "note"])
        w.writerows(sample_rows)

    summary = {
        "study": "SG-MO-017 pilot P3: the perfect via form-class, not UD tense",
        "method": "C5 § 3 (attested/generated/traditional) via C3 cycle; direct test of EM2 (§ 5.2)",
        "snapshot": {"master": str(db), "sha256": sha256, "provenance": prov},
        "universe_where_sql": UNIV,
        "universe_gloss": ("finite verb tokens with Tense=Past — the preterite bucket "
                           "EM2/Д1 collapses (aorist ∪ perfect ∪ imperfect residue); "
                           "the perfect is NOT separable from it by the tense feature"),
        "tense_context_finite": tense_ctx,
        "past_fin_tokens": total,
        "pluperfect_tokens_separately_tagged": plp,
        "em2_note": ("Tense=Past conflates the preterites (C3 Д1); the imperfect proper "
                     "is partly tense-tagged Impf (46 695) but residue leaks into Past; "
                     "the pluperfect IS separately tagged (Plp/Pqp) — the common perfect "
                     "is not"),
        "form_class_partition": {
            "instrument": "DCS feat_formation (the C2-intended `dcs:form-class` referent)",
            "peri_periphrastic_perfect": peri,
            "peri_pct": round(100 * peri / total, 2),
            "aorist_formed_total": aorist_formed,
            "aorist_formed_pct": round(100 * aorist_formed / total, 2),
            "unmarked_null": unmarked,
            "unmarked_pct": round(100 * unmarked / total, 2),
            "red_is_reduplicated_aorist": {
                "tokens": form_counts.get("red", 0),
                "note": "under Past, feat_formation='red' marks the augmented reduplicated "
                        "AORIST, not the perfect — a false friend for a naive redupl.=perfect rule",
                "examples": [{"form": u, "lemma": l} for u, l in red_examples],
            },
            "no_perfect_value": ("feat_formation has NO 'perfect' value; the reduplicated "
                                 "perfect — the primary formation — carries no tag and sits "
                                 "in the UNMARKED (NULL) bucket"),
        },
        "form_attestable_perfect": {
            "note": ("the ONLY form-evidently-perfect tokens are the periphrastic perfect; "
                     "the primary reduplicated perfect is 0 % recoverable via feat_formation"),
            "periphrastic_perfect_tokens": peri,
            "periphrastic_pct_of_past": round(100 * peri / total, 2),
            "auxiliary_split": {k: n for k, n in aux_counter.most_common()},
            "person_number": {k: n for k, n in peri_pn.most_common()},
            "voice": {k: n for k, n in peri_voice.most_common()},
            "belongs_to_slot": "SG-MO-032 (periphrastic perfect); here it is the lower bound for SG-MO-017",
        },
        "secondary_surface_heuristic": {
            "role": ("NEGATIVE probe only — measures that a bespoke augmentless-reduplication "
                     "rule cannot isolate the perfect (conflates redupl. present III + redupl. "
                     "aorist + perfect); never used as a corpus fact"),
            "null_bucket_hits": heur_hits,
            "null_bucket_size": unmarked,
            "hit_pct_of_unmarked": round(100 * heur_hits / unmarked, 2) if unmarked else None,
            "precision_measured_in": "validation_verdicts.tsv (sample adjudication)",
        },
        "kill_gate": {
            "rule": ("C5 § 7 P3: if form-class isolates the perfect from aorist/imperfect in "
                     "< 95 % of the sample → the quantitative part is withdrawn and an honest "
                     "negative result is published"),
            "form_class_isolable_pct_of_past": round(100 * (peri + aorist_formed) / total, 2),
            "perfect_form_attestable_pct_of_past": round(100 * peri / total, 2),
            "seed": SEED,
            "sample_size": SAMPLE_SIZE,
            "sample_form_class_isolable": formclass_isolable,
            "sample_form_class_isolable_pct": round(100 * formclass_isolable / SAMPLE_SIZE, 2),
            "fired": (peri + aorist_formed) / total < 0.95,
            "file": "validation_sample.tsv (+ manual adjudication in validation_verdicts.tsv)",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    kg = summary["kill_gate"]
    fp = summary["form_class_partition"]
    print(f"Past-fin universe: {total} tokens (EM2 preterite bucket)")
    print(f"form-class: peri(perfect) {fp['peri_pct']}%  aorist-formed "
          f"{fp['aorist_formed_pct']}%  UNMARKED {fp['unmarked_pct']}%")
    print(f"periphrastic perfect: {peri} tokens; aux {dict(aux_counter.most_common(3))}")
    print(f"red tag = reduplicated aorist (false friend): {form_counts.get('red', 0)} tokens")
    print(f"surface reduplication heuristic (negative probe): {heur_hits} NULL-bucket hits")
    print(f"pluperfect separately tagged: {plp}")
    print(f"KILL-GATE {'FIRED' if kg['fired'] else 'not fired'} "
          f"(form-class isolable {kg['form_class_isolable_pct_of_past']}%; "
          f"perfect form-attestable {kg['perfect_form_attestable_pct_of_past']}% ≪ 95%); "
          f"sample form-class isolable {kg['sample_form_class_isolable_pct']}%")
    print(f"wrote {OUT_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
