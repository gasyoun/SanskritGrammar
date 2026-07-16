#!/usr/bin/env python
"""period_style_gradient.py — the period-tagging instrument for §207 (OCH-63).

THE FLAGSHIP open target of the Ocherk register (H797/H1000): §207 claims a
diachronic style shift — style I (verbal sentences, active constructions,
word groups) dominant in the Vedas and the early post-Vedic language, style II
(compounds, nominal sentences, passive constructions) dominant in late
classical Sanskrit. The corpus-wide DCS aggregates cannot see time; this
script adds the missing axis: a CURATED text->period crosswalk over the
pinned VisualDCS SQLite master (provenance pins dcs-conllu commit 04e0778,
the same snapshot the Sangram pilots and rigveda_kz_fractions.py consume),
then computes per-period style metrics.

PERIOD MAP DESIGN (the scholarly-judgment layer, kept explicit):
  - The 40+ token-heaviest DCS texts are hand-assigned to {vedic, epic,
    classical} with a one-line dating basis each; standard datings, no
    original chronology claimed. Unmapped texts are excluded and counted
    (never silently bucketed).
  - Puranas get their own bucket ('puranic') OUTSIDE the core gradient:
    their verse deliberately imitates epic style, so folding them into
    'late classical' would dilute the very signal §207 describes. They are
    still measured and reported — as a fourth column, not a core period.
  - Register-confounded texts are EXCLUDED with a reason: Buddhist (hybrid)
    Sanskrit prose is its own register, not a period sample; nighaṇṭu/
    lexica are word lists, not sentences.

ANNOTATION-ROBUSTNESS RULING (measured 16-07-2026, baked into the design):
  DCS verbal FEATURE annotation is wildly non-uniform by text — tagged
  past participles fall RV 1,874 -> MBh 465 -> Kathāsaritsāgara 14 ->
  Daśakumāracarita 0 (a prose text FULL of them), and person-annotation
  density falls 13.9% -> 6.4% over the same span. Any metric built on
  feats therefore measures ANNOTATION density, not language change.
  upos, by contrast, is 100% complete on every text probed. So:
    ROBUST (verdict-bearing):  upos-based + mwt-segmentation-based metrics.
    CONDITIONAL (reported with caveat): passive share among the finite
      verbs that ARE annotated — internally normalized, but assumes voice
      is not correlated with a text's annotation sparsity.
    CONFOUNDED (reported only inside annotation_coverage, never verdict-
      bearing): finite-verb rates, ta-participle rates, nominal-sentence
      shares — these need uniformly annotated data this snapshot lacks.

METRIC DEFINITIONS:
  compound_member_pct   share of NOUN/ADJ tokens that sit inside one DCS
                        mwt span (one surface word) together with >= 1
                        other NOUN/ADJ member — compound membership.
                        PROXY CAVEAT: mwt spans also cover sandhi-joined
                        sequences; nominal+nominal inside one surface word
                        is overwhelmingly compounding, and the residual
                        contamination applies to every period alike, so
                        the GRADIENT survives even if the level is inflated.
  mean_nominal_cluster  mean number of nominal members in such spans —
                        style II also means LONGER compounds.
  nominal_share_pct     NOUN+ADJ share of all tokens (upos-based).
  noun_verb_ratio       (NOUN+ADJ) / VERB tokens (upos-based; VERB includes
                        participles+absolutives, so this understates the
                        finite-verb story but is annotation-robust).
  finite_passive_pct    feat_voice=Pass share among annotated finite verbs
                        (CONDITIONAL — see ruling above).

OCH-47's diachronic half ('guṇa-for-vṛddhi causatives commoner early') stays
instrument-blocked: the snapshot carries no causative marking (xpos/feats
probed empty 16-07-2026) — that needs a causative detector, not this map.

Usage:  python ZalizniakOcherk_1978/period_style_gradient.py [--db PATH]
Writes  och63_period_style_stats.json next to this script.
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

NOMINAL = {"NOUN", "ADJ"}
NONFINITE = {"Part", "Conv", "Gdv", "Inf"}

# text name (exact DCS spelling) -> (period, dating basis)
PERIOD_MAP = {
    # ── vedic: saṃhitās, brāhmaṇas, śrautasūtras (Vedic language sphere) ──
    "Ṛgveda": ("vedic", "RV saṃhitā, ~1200-1000 BCE"),
    "Atharvaveda (Śaunaka)": ("vedic", "AV saṃhitā, early 1st mill. BCE"),
    "Atharvaveda (Paippalāda)": ("vedic", "AV saṃhitā, early 1st mill. BCE"),
    "Maitrāyaṇīsaṃhitā": ("vedic", "YV saṃhitā, early 1st mill. BCE"),
    "Kāṭhakasaṃhitā": ("vedic", "YV saṃhitā, early 1st mill. BCE"),
    "Taittirīyasaṃhitā": ("vedic", "YV saṃhitā, early 1st mill. BCE"),
    "Śatapathabrāhmaṇa": ("vedic", "brāhmaṇa prose, ~800-600 BCE"),
    "Aitareyabrāhmaṇa": ("vedic", "brāhmaṇa prose, ~800-600 BCE"),
    "Jaiminīyabrāhmaṇa": ("vedic", "brāhmaṇa prose, ~800-600 BCE"),
    "Pañcaviṃśabrāhmaṇa": ("vedic", "brāhmaṇa prose, ~800-600 BCE"),
    "Gopathabrāhmaṇa": ("vedic", "late brāhmaṇa, ~600-400 BCE"),
    "Baudhāyanaśrautasūtra": ("vedic", "śrautasūtra, late-Vedic, ~600-300 BCE"),
    "Āpastambaśrautasūtra": ("vedic", "śrautasūtra, late-Vedic, ~600-300 BCE"),
    "Vaikhānasaśrautasūtra": ("vedic", "śrautasūtra, late-Vedic sphere"),
    # ── epic / early post-Vedic ──
    "Mahābhārata": ("epic", "epic core+layers, ~400 BCE-400 CE"),
    "Rāmāyaṇa": ("epic", "epic, ~200 BCE-200 CE"),
    "Harivaṃśa": ("epic", "MBh appendix, ~1-300 CE"),
    "Manusmṛti": ("epic", "early smṛti verse, ~100 BCE-200 CE"),
    "Carakasaṃhitā": ("epic", "early medical prose (layered), ~100 BCE-200 CE core"),
    "Suśrutasaṃhitā": ("epic", "early medical prose (layered), ~1-300 CE core"),
    # ── classical (kāvya, story literature, śāstra/commentary, tantra, alchemy) ──
    "Daśakumāracarita": ("classical", "Daṇḍin prose kāvya, ~7th c. CE"),
    "Harṣacarita": ("classical", "Bāṇa prose kāvya, ~7th c. CE"),
    "Aṣṭāṅgahṛdayasaṃhitā": ("classical", "Vāgbhaṭa, ~7th c. CE"),
    "Bṛhatkathāślokasaṃgraha": ("classical", "Budhasvāmin, ~8-9th c. CE"),
    "Kathāsaritsāgara": ("classical", "Somadeva, 11th c. CE"),
    "Bhāratamañjarī": ("classical", "Kṣemendra, 11th c. CE"),
    "Tantrāloka": ("classical", "Abhinavagupta, ~1000 CE"),
    "Āyurvedadīpikā": ("classical", "Cakrapāṇidatta commentary prose, 11th c. CE"),
    "Rasārṇava": ("classical", "alchemical, ~12th c. CE"),
    "Rasaratnākara": ("classical", "alchemical, ~13th c. CE"),
    "Rasaratnasamuccaya": ("classical", "alchemical, ~13-14th c. CE"),
    "Ānandakanda": ("classical", "alchemical, ~13th c. CE"),
    "Mugdhāvabodhinī": ("classical", "late commentary"),
    "Haribhaktivilāsa": ("classical", "Gauḍīya ritual digest, 16th c. CE"),
    # ── puranic: measured, reported, NOT part of the core gradient ──
    "Liṅgapurāṇa": ("puranic", "purāṇa, ~5-10th c. CE (epic-imitative verse)"),
    "Matsyapurāṇa": ("puranic", "purāṇa, ~3-10th c. CE (epic-imitative verse)"),
    "Skandapurāṇa (Revākhaṇḍa)": ("puranic", "purāṇa, late (epic-imitative verse)"),
    "Viṣṇupurāṇa": ("puranic", "purāṇa, ~4-6th c. CE (epic-imitative verse)"),
    "Kūrmapurāṇa": ("puranic", "purāṇa, ~7-9th c. CE (epic-imitative verse)"),
    "Bhāgavatapurāṇa": ("puranic", "purāṇa, ~9-10th c. CE (epic-imitative verse)"),
    "Garuḍapurāṇa": ("puranic", "purāṇa, ~9-10th c. CE (epic-imitative verse)"),
}

EXCLUDED = {
    "Divyāvadāna": "Buddhist (hybrid) Sanskrit register, not a period sample",
    "Aṣṭasāhasrikā": "Buddhist (hybrid) Sanskrit register, not a period sample",
    "Saddharmapuṇḍarīkasūtra": "Buddhist (hybrid) Sanskrit register, not a period sample",
    "Rājanighaṇṭu": "nighaṇṭu (lexicon): word lists, not sentences",
}

CORE_ORDER = ["vedic", "epic", "classical"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()
    cur2 = db.cursor()  # second cursor: never nest queries on one cursor

    names = {n for (n,) in cur.execute("SELECT name FROM text")}
    missing = [n for n in list(PERIOD_MAP) + list(EXCLUDED) if n not in names]
    assert not missing, f"period-map names absent from DB: {missing}"

    text_period = {}
    for name, (period, _basis) in PERIOD_MAP.items():
        (tid,) = cur.execute("SELECT text_id FROM text WHERE name=?", (name,)).fetchone()
        text_period[tid] = (name, period)

    Z = lambda: {"tokens": 0, "nominal": 0, "verb": 0,
                 "finite_annot": 0, "finite_pass": 0,
                 "clusters": 0, "cluster_members": 0}
    acc = defaultdict(Z)
    per_text = defaultdict(Z)

    for tid, (tname, period) in text_period.items():
        both = (acc[period], per_text[tname])
        for (tot, nom, verb, fin, finpass) in cur.execute("""
          SELECT COUNT(*),
                 SUM(CASE WHEN t.upos IN ('NOUN','ADJ') THEN 1 ELSE 0 END),
                 SUM(CASE WHEN t.upos='VERB' THEN 1 ELSE 0 END),
                 SUM(CASE WHEN t.feat_person IS NOT NULL AND t.feat_person!=''
                          AND (t.feat_verbform IS NULL OR t.feat_verbform NOT IN
                               ('Part','Conv','Gdv','Inf')) THEN 1 ELSE 0 END),
                 SUM(CASE WHEN t.feat_voice='Pass' AND t.feat_person IS NOT NULL
                          AND t.feat_person!='' THEN 1 ELSE 0 END)
          FROM token t JOIN sentence s ON t.sentence_id=s.id
          JOIN chapter c ON s.chapter_id=c.chapter_id
          WHERE c.text_id=?""", (tid,)):
            for a in both:
                a["tokens"] += tot
                a["nominal"] += nom or 0
                a["verb"] += verb or 0
                a["finite_annot"] += fin or 0
                a["finite_pass"] += finpass or 0

        # compound pass — separate cursor for the inner member lookup
        for sid, span in cur.execute("""
          SELECT m.sentence_id, m.span
          FROM mwt m JOIN sentence s ON m.sentence_id=s.id
          JOIN chapter c ON s.chapter_id=c.chapter_id
          WHERE c.text_id=?""", (tid,)):
            try:
                lo, hi = (int(x) for x in span.split("-"))
            except ValueError:
                continue
            nom = sum(1 for (u,) in cur2.execute(
                "SELECT upos FROM token WHERE sentence_id=? AND idx BETWEEN ? AND ?",
                (sid, lo, hi)) if u in NOMINAL)
            if nom >= 2:
                for a in both:
                    a["clusters"] += 1
                    a["cluster_members"] += nom

    def derive(a):
        t = a["tokens"] or 1
        return {
            "tokens": a["tokens"],
            "compound_member_pct": round(100 * a["cluster_members"] / (a["nominal"] or 1), 2),
            "mean_nominal_cluster": round(a["cluster_members"] / (a["clusters"] or 1), 2),
            "nominal_share_pct": round(100 * a["nominal"] / t, 2),
            "noun_verb_ratio": round(a["nominal"] / (a["verb"] or 1), 2),
            "finite_passive_pct_CONDITIONAL": round(100 * a["finite_pass"] / (a["finite_annot"] or 1), 2),
            "annotation_coverage": {
                "finite_annotated_per_1000": round(1000 * a["finite_annot"] / t, 2),
            },
        }

    (total_tokens,) = cur.execute("SELECT COUNT(*) FROM token").fetchone()
    mapped_tokens = sum(a["tokens"] for a in acc.values())

    periods = {p: derive(acc[p]) for p in CORE_ORDER + ["puranic"] if p in acc}
    texts = {n: dict(period=PERIOD_MAP[n][0], basis=PERIOD_MAP[n][1], **derive(per_text[n]))
             for n in sorted(per_text)}

    grad = {}
    for metric, direction, robust in [
            ("compound_member_pct", "rising", True),
            ("mean_nominal_cluster", "rising", True),
            ("nominal_share_pct", "rising", True),
            ("noun_verb_ratio", "rising", True),
            ("finite_passive_pct_CONDITIONAL", "rising", False)]:
        vals = [periods[p][metric] for p in CORE_ORDER]
        ok = all(vals[i] <= vals[i + 1] for i in range(2)) if direction == "rising" \
            else all(vals[i] >= vals[i + 1] for i in range(2))
        grad[metric] = {"vedic_epic_classical": vals, "expected": direction,
                        "monotonic": ok, "annotation_robust": robust}

    checks = {
        "all_map_names_resolve": True,
        "coverage_pct_of_corpus": round(100 * mapped_tokens / total_tokens, 1),
        "vedic_tokens_over_500k": acc["vedic"]["tokens"] > 500_000,
        "epic_tokens_over_1m": acc["epic"]["tokens"] > 1_000_000,
        "classical_tokens_over_400k": acc["classical"]["tokens"] > 400_000,
        "compound_pass_nonzero_every_period": all(
            acc[p]["cluster_members"] > 0 for p in CORE_ORDER + ["puranic"]),
    }

    out = {
        "instrument": "period_style_gradient.py over dcs_full.sqlite (dcs-conllu 04e0778); "
                      "curated 41-text period map; metric semantics per module docstring "
                      "(upos/mwt metrics annotation-robust; feats-based CONDITIONAL only)",
        "period_map_size": len(PERIOD_MAP),
        "excluded": EXCLUDED,
        "corpus_tokens": total_tokens,
        "mapped_tokens": mapped_tokens,
        "periods": periods,
        "core_gradient": grad,
        "per_text": texts,
        "validation": checks,
    }
    (HERE / "och63_period_style_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"corpus {total_tokens:,} tokens; mapped {mapped_tokens:,} "
          f"({checks['coverage_pct_of_corpus']}%) across {len(PERIOD_MAP)} texts")
    for p in CORE_ORDER + ["puranic"]:
        d = periods[p]
        print(f"{p:10} tok {d['tokens']:>9,}  compound% {d['compound_member_pct']:6.2f}  "
              f"cluster {d['mean_nominal_cluster']:4.2f}  nominal% {d['nominal_share_pct']:5.2f}  "
              f"N/V {d['noun_verb_ratio']:4.2f}  pass%(cond) {d['finite_passive_pct_CONDITIONAL']:5.2f}")
    print("gradient (vedic -> epic -> classical):")
    for m, g in grad.items():
        tag = "ROBUST" if g["annotation_robust"] else "conditional"
        print(f"  {m:32} {g['vedic_epic_classical']} expected {g['expected']:7} "
              f"monotonic={g['monotonic']} [{tag}]")
    bad = [k for k, v in checks.items() if v is False]
    print(f"validation: {'OK' if not bad else 'FAILED: ' + ', '.join(bad)} "
          f"(coverage {checks['coverage_pct_of_corpus']}%)")
    print("-> och63_period_style_stats.json written")


if __name__ == "__main__":
    main()
