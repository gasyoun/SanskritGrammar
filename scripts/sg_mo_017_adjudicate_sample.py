#!/usr/bin/env python3
"""SG-MO-017 P3: manual adjudication of the 80-token Past sample.

For each sampled Tense=Past token, a hand verdict of its true preterite category
(perfect / aorist / imperfect / other) is recorded alongside what DCS's form-class
feature (feat_formation) isolated. The kill-gate metric is the recall of the
perfect by form-class: of the truly-perfect tokens, how many did the corpus
form-class feature flag as perfect.

Verdicts are model-provisional (Opus 4.8), flagged for scholarly review — the same
discipline as the P2 pilot's § 4 adjudication. Robust diagnostics used:
periphrastic -ām+aux ⇒ perfect; reduplication + perfect endings (-a/-uḥ/-e/-atuḥ/
-tha) with no augment ⇒ perfect; augment a- + sigmatic/thematic/root marker ⇒
aorist; augment + present stem + secondary ending ⇒ imperfect; injunctive/precative
⇒ other.

Reads   sangram/articles/perfect/data/validation_sample.tsv
Writes  sangram/articles/perfect/data/validation_verdicts.tsv
"""
import csv
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
DATA = Path(__file__).resolve().parents[1] / "sangram" / "articles" / "perfect" / "data"

# token_id -> (adjudicated_category, note). Categories: perfect | aorist | imperfect | other
VERDICT = {
    867893: ("perfect", "āha — defective perfect of ah 'he says/said'"),
    1690433: ("perfect", "vidadhe — perfect mid. 3sg, reduplicated dhā"),
    559419: ("perfect", "uvāca — perfect 3sg of vac (narrative 'said')"),
    4313052: ("aorist", "udapādi — passive -i aorist 3sg (Voice=Pass)"),
    1541444: ("perfect", "anumene — perfect mid. 3sg of anu-man"),
    1448120: ("aorist", "mā hiṃsīḥ — prohibitive injunctive/aorist 2sg"),
    1595970: ("perfect", "upajagmatuḥ — perfect 3du, jagm-atuḥ"),
    2390427: ("perfect", "uvāca — perfect 3sg"),
    1782379: ("imperfect", "parāpatat — imperfect 3sg of parā-pat"),
    3052088: ("perfect", "paripapraccha — perfect 3sg, reduplicated pracch"),
    196699: ("imperfect", "udakrāmat — imperfect 3sg of ut-kram"),
    4844858: ("aorist", "mā ... hiṃsiṣṭa — prohibitive iṣ-aorist 2pl of hiṃs"),
    1039765: ("aorist", "avocat — thematic aorist 3sg (form-class tagged them) ✓"),
    2294272: ("perfect", "uvāca — perfect 3sg"),
    4707401: ("perfect", "veda — perfect of vid used as present 'knows'"),
    3474201: ("perfect", "āha — defective perfect"),
    1188864: ("imperfect", "niramimīta — imperfect 3sg, class-III present stem mimī"),
    1554060: ("aorist", "abhūt — root aorist 3sg of bhū (form-class root) ✓"),
    4358046: ("perfect", "uvāca — perfect 3sg"),
    4841924: ("perfect", "prāha — perfect (pra + āha)"),
    4380901: ("perfect", "uvāca — perfect 3sg"),
    5572143: ("perfect", "īje — perfect mid. 3sg of yaj"),
    5303638: ("other", "aśīya — precative/benedictive 1sg mid. of aś"),
    672856: ("perfect", "uvāca — perfect 3sg"),
    1824614: ("perfect", "saṃbabhūva — perfect 3sg of sam-bhū"),
    2099324: ("perfect", "cacāra — perfect 3sg of car"),
    2764806: ("perfect", "cikṣepa — perfect 3sg of kṣip"),
    5491724: ("aorist", "mā saṃvādayiṣṭhāḥ — prohibitive iṣ-aorist 2sg mid. (caus.)"),
    2340522: ("perfect", "uvāsa — perfect 3sg of vas"),
    2782397: ("perfect", "pratijagrāha — perfect 3sg of prati-grah"),
    2162057: ("perfect", "āha — defective perfect"),
    5386053: ("perfect", "vettha — perfect 2sg of vid 'thou knowest'"),
    5481476: ("imperfect", "vyāśnuta — imperfect mid. 3sg of vi-aś (class V aśnu)"),
    5356131: ("perfect", "apacakrāma — perfect 3sg of apa-kram (ca- reduplication, no augment)"),
    4925234: ("perfect", "tatyāja — perfect 3sg of tyaj"),
    1584267: ("perfect", "ūce — perfect mid. 3sg of vac"),
    3633736: ("perfect", "veda — perfect-present of vid"),
    451815: ("aorist", "prāsāvīḥ — iṣ-aorist 2sg of pra-sū (form-class is) ✓"),
    1275998: ("perfect", "jajñāte — perfect 3du mid. of jan"),
    2154101: ("aorist", "abhūt — root aorist 3sg (form-class root) ✓"),
    771020: ("perfect", "uvāca — perfect 3sg"),
    137199: ("imperfect", "avyayaḥ — imperfect 2sg of vye (Vedic, augment a-)"),
    4237398: ("perfect", "upacakrame — perfect mid. 3sg of upa-kram"),
    1261640: ("perfect", "śuśubhe — perfect mid. 3sg of śubh"),
    2840791: ("perfect", "saṃbabhau — perfect 3sg of sam-bhā"),
    1315053: ("perfect", "dadṛśe — perfect mid. 3sg of dṛś"),
    2119729: ("perfect", "vivāsayāmāsa — PERIPHRASTIC perfect 3sg (form-class peri) ✓"),
    2807351: ("other", "mā śuco — prohibitive injunctive 2sg of śuc"),
    3182000: ("perfect", "āhuḥ — perfect 3pl of ah 'they say'"),
    465295: ("perfect", "prāhuḥ — perfect 3pl (pra + āhuḥ)"),
    5000741: ("aorist", "vocam — augmentless thematic aorist 1sg of vac"),
    5679772: ("perfect", "veda — perfect-present of vid"),
    1584921: ("aorist", "DCS-tagged them-aorist ✓ but context reads noun vyāpad 'calamity' — likely a DCS mistag"),
    623691: ("perfect", "ūcuḥ — perfect 3pl of vac"),
    4135938: ("perfect", "tāḍayāmāsa — PERIPHRASTIC perfect 3sg (form-class peri) ✓"),
    2590648: ("perfect", "mamṛṣe — perfect mid. 3sg of mṛṣ"),
    2758364: ("perfect", "niṣpetuḥ — perfect 3pl of niṣ-pat (pet reduplication)"),
    661156: ("perfect", "babhūva — perfect 3sg of bhū"),
    4422670: ("perfect", "uvāca — perfect 3sg"),
    3006293: ("perfect", "uvāca — perfect 3sg"),
    5522414: ("perfect", "jagṛbhmā — perfect 1pl of grah (Vedic)"),
    1267453: ("perfect", "uvāca — perfect 3sg"),
    2298290: ("perfect", "upaviveśa — perfect 3sg of upa-viś"),
    2543552: ("perfect", "cakruḥ — perfect 3pl of kṛ"),
    4178301: ("perfect", "vicacāra — perfect 3sg of vi-car"),
    1222985: ("perfect", "āha — defective perfect"),
    2096509: ("perfect", "babhūva — perfect 3sg of bhū"),
    3366230: ("perfect", "jajñe — perfect mid. 3sg of jan"),
    490403: ("perfect", "āha — defective perfect"),
    4227891: ("perfect", "cacāra — perfect 3sg of car"),
    3598372: ("perfect", "pratyuvāca — perfect 3sg of prati-vac"),
    1847886: ("perfect", "cacāra — perfect 3sg of car"),
    3503725: ("perfect", "uvāca — perfect 3sg"),
    5319754: ("perfect", "jaghnuḥ — perfect 3pl of han"),
    691263: ("perfect", "papraccha — perfect 3sg of pracch"),
    2543357: ("perfect", "uvāca — perfect 3sg"),
    5591879: ("aorist", "bhakṣi — Vedic aorist/injunctive 1sg mid. of bhaj"),
    2417683: ("perfect", "papāta — perfect 3sg of pat"),
    1392020: ("aorist", "abhūt — root aorist 3sg (form-class root) ✓"),
    3437699: ("perfect", "upatasthe — perfect mid. 3sg of upa-sthā"),
}

PERFECT_FORMS = {"peri"}
AORIST_FORMS = {"s", "is", "sa", "sis", "them", "root", "red"}


def main() -> int:
    src = DATA / "validation_sample.tsv"
    rows = list(csv.DictReader(open(src, encoding="utf-8"), delimiter="\t"))
    out = []
    cat = Counter()
    isolated_by_cat = Counter()
    perfect_total = perfect_isolated = 0
    formclass_isolable = 0
    for r in rows:
        tid = int(r["token_id"])
        verdict, note = VERDICT.get(tid, ("?", "UNADJUDICATED"))
        formation = r["feat_formation"].strip()
        isolated = formation in PERFECT_FORMS or formation in AORIST_FORMS
        # correct isolation = form-class reading matches the adjudicated category
        fc_is_perfect = formation in PERFECT_FORMS
        fc_is_aorist = formation in AORIST_FORMS
        correct = (fc_is_perfect and verdict == "perfect") or (fc_is_aorist and verdict == "aorist")
        cat[verdict] += 1
        if isolated:
            formclass_isolable += 1
        if verdict == "perfect":
            perfect_total += 1
            if fc_is_perfect:
                perfect_isolated += 1
        if correct:
            isolated_by_cat[verdict] += 1
        out.append([
            tid, r["form"], r["lemma"], formation or "-",
            r["form_class_reading"], verdict,
            "Y" if isolated else "N",
            "Y" if correct else "N", note,
        ])

    with open(DATA / "validation_verdicts.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "feat_formation",
                    "form_class_reading", "adjudicated_category",
                    "isolated_by_formclass", "correctly_isolated", "note"])
        w.writerows(out)

    n = len(rows)
    print(f"adjudicated {n} Past-bucket tokens")
    print(f"true categories: {dict(cat.most_common())}")
    print(f"form-class isolable (any tag): {formclass_isolable}/{n} "
          f"= {round(100*formclass_isolable/n,1)}%")
    print(f"correctly isolated by category: {dict(isolated_by_cat.most_common())}")
    print(f"PERFECT recall by form-class: {perfect_isolated}/{perfect_total} "
          f"= {round(100*perfect_isolated/perfect_total,1)}%  (kill-gate: <95% → FIRED)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
