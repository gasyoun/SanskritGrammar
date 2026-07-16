#!/usr/bin/env python
"""causative_grade_detector.py — the causative detector for §167 (OCH-47).

The instrument OCH-47's diachronic half has waited for since the H797 drain
(and whose blocker H1000 narrowed from 'period tagging' to 'causative
detection'): §167 claims that guṇa-for-vṛddhi causatives (gamayati-type
instead of expected *gāmayati) are MORE common in the early language than
in the late one («в раннем языке таких отступлений больше, чем в позднем»).

DETECTION DESIGN (probed 16-07-2026 before building):
  DCS lemmatizes causatives (and formally identical class-10 / -aya-
  presents) as their OWN lemmas ending in -ay: janay, kāray, gamay,
  sthāpay. Detection is therefore LEMMA-level, no form matching:

  1. Enumerate VERB lemmas ending 'ay'.
  2. For the shapes §167 itself names (roots in am; seṭ roots in ar/al/an —
     'ar' in Zalizniak's 1978 citation practice = DCS ṛ-final roots plus
     genuine ar-roots like tvar), derive the grade pair:
       a-shape  Cam/Can/Cal : guṇa lemma C-a-C+ay  ~ vṛddhi lemma C-ā-C+ay
       r-shape  Cṛ / Car    : guṇa lemma C+aray    ~ vṛddhi lemma C+āray
  3. ANCHOR each pair on its root: the corresponding root lemma must exist
     as a VERB lemma in the same DB (janay -> jan exists; kathay finds no
     root 'kath' shape and is excluded) — this screens out denominatives,
     which share the -ay morphology (a residual risk for nouns homophonous
     with roots is documented, not hidden).
  4. Slice pair-member tokens by the H1000 period map (imported from
     period_style_gradient.py — one canonical map, not two) and compute
     the guṇa share per period.

  All layers used (lemma, upos, text identity) are annotation-robust —
  none of the sparse verbal FEATURES (FINDINGS §86) are consulted.

WHAT THE NUMBERS MEAN:
  guṇa_share_pct         guṇa-grade tokens / (guṇa + vṛddhi) tokens over
                         the pair inventory, per period. §167 predicts it
                         FALLS from early to late.
  Reported over two inventories:
    all_pairs            every anchored pair with >= MIN_TOKENS total.
    fluctuating_pairs    pairs with BOTH grades attested corpus-wide —
                         where the diachronic choice is actually visible
                         (fixed-guṇa roots like gam/jan are §1042's stable
                         exception class and dilute the diachrony).

Usage:  python ZalizniakOcherk_1978/causative_grade_detector.py [--db PATH]
Writes  och47_causative_stats.json next to this script.
"""
import argparse
import json
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from period_style_gradient import CORE_ORDER, PERIOD_MAP  # noqa: E402  one canonical period map

DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
MIN_TOKENS = 5  # pair floor: below this a 'share' is noise

A_SHAPE = re.compile(r"^(.+?)a([mnl])ay$")   # gamay, janay, jvalay ...
R_SHAPE = re.compile(r"^(.+?)aray$")          # smaray, tvaray, karay ...


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    verb_lemmas = {l for (l,) in cur.execute(
        "SELECT DISTINCT lemma FROM token WHERE upos='VERB' AND lemma IS NOT NULL")}

    # pair discovery from the guṇa side (the marked member)
    pairs = {}  # root -> {"guna": lemma, "vrddhi": lemma, "shape": ...}
    for lemma in sorted(verb_lemmas):
        m = A_SHAPE.match(lemma)
        if m:
            base, fin = m.group(1), m.group(2)
            root = f"{base}a{fin}"
            vrddhi = f"{base}ā{fin}ay"
            if root in verb_lemmas:
                pairs[root] = {"guna": lemma, "vrddhi": vrddhi, "shape": f"a-{fin}"}
            continue
        m = R_SHAPE.match(lemma)
        if m:
            base = m.group(1)
            root = next((r for r in (base + "ṛ", base + "ar") if r in verb_lemmas), None)
            if root:
                pairs[root] = {"guna": lemma, "vrddhi": base + "āray", "shape": "r"}
    # vṛddhi-only roots (kāray/kṛ with no *karay) — discover from the vṛddhi side too
    for lemma in sorted(verb_lemmas):
        m = re.match(r"^(.+?)ā([mnl])ay$", lemma)
        if m:
            base, fin = m.group(1), m.group(2)
            root = f"{base}a{fin}"
            if root in verb_lemmas and root not in pairs:
                pairs[root] = {"guna": f"{base}a{fin}ay", "vrddhi": lemma, "shape": f"a-{fin}"}
            continue
        m = re.match(r"^(.+?)āray$", lemma)
        if m:
            base = m.group(1)
            root = next((r for r in (base + "ṛ", base + "ar") if r in verb_lemmas), None)
            if root and root not in pairs:
                pairs[root] = {"guna": base + "aray", "vrddhi": lemma, "shape": "r"}

    # per-lemma token counts, total + per period
    text_period = {}
    for name, (period, _basis) in PERIOD_MAP.items():
        (tid,) = cur.execute("SELECT text_id FROM text WHERE name=?", (name,)).fetchone()
        text_period[tid] = period

    def counts(lemma):
        total = cur.execute(
            "SELECT COUNT(*) FROM token WHERE lemma=? AND upos='VERB'", (lemma,)).fetchone()[0]
        per = defaultdict(int)
        for tid, n in cur.execute("""
            SELECT c.text_id, COUNT(*)
            FROM token t JOIN sentence s ON t.sentence_id=s.id
            JOIN chapter c ON s.chapter_id=c.chapter_id
            WHERE t.lemma=? AND t.upos='VERB' GROUP BY c.text_id""", (lemma,)):
            p = text_period.get(tid)
            if p:
                per[p] += n
        return total, per

    inventory = {}
    for root, info in sorted(pairs.items()):
        g_tot, g_per = counts(info["guna"])
        v_tot, v_per = counts(info["vrddhi"])
        if g_tot + v_tot < MIN_TOKENS:
            continue
        inventory[root] = {
            "shape": info["shape"], "guna_lemma": info["guna"], "vrddhi_lemma": info["vrddhi"],
            "guna_total": g_tot, "vrddhi_total": v_tot,
            "fluctuating": g_tot > 0 and v_tot > 0,
            "per_period": {p: {"guna": g_per.get(p, 0), "vrddhi": v_per.get(p, 0)}
                           for p in CORE_ORDER + ["puranic"]},
        }

    def share_table(roots):
        table = {}
        for p in CORE_ORDER + ["puranic"]:
            g = sum(inventory[r]["per_period"][p]["guna"] for r in roots)
            v = sum(inventory[r]["per_period"][p]["vrddhi"] for r in roots)
            table[p] = {"guna": g, "vrddhi": v,
                        "guna_share_pct": round(100 * g / (g + v), 2) if g + v else None}
        return table

    all_roots = list(inventory)
    fluct_roots = [r for r in inventory if inventory[r]["fluctuating"]]
    all_tab = share_table(all_roots)
    fluct_tab = share_table(fluct_roots)

    def falling(tab):
        vals = [tab[p]["guna_share_pct"] for p in CORE_ORDER]
        return (None not in vals) and vals[0] >= vals[1] >= vals[2]

    checks = {
        "pairs_anchored": len(inventory),
        "fluctuating_pairs": len(fluct_roots),
        "gam_jan_fixed_guna": all(
            r in inventory and inventory[r]["vrddhi_total"] <= 1 for r in ("gam", "jan")),
        "kr_dhr_fixed_vrddhi": all(
            r in inventory and inventory[r]["guna_total"] == 0 for r in ("kṛ", "dhṛ")),
        "every_core_period_has_tokens_fluct": all(
            (fluct_tab[p]["guna"] + fluct_tab[p]["vrddhi"]) > 0 for p in CORE_ORDER),
    }

    out = {
        "instrument": "causative_grade_detector.py over dcs_full.sqlite (dcs-conllu 04e0778); "
                      "lemma-level grade pairs anchored on root lemmas; period map imported "
                      "from period_style_gradient.py (H1000); annotation-robust layers only",
        "min_tokens_floor": MIN_TOKENS,
        "guna_share_by_period": {"all_pairs": all_tab, "fluctuating_pairs": fluct_tab},
        "gradient": {
            "all_pairs_falling": falling(all_tab),
            "fluctuating_pairs_falling": falling(fluct_tab),
            "expected_by_s167": "guṇa share falls vedic -> epic -> classical",
        },
        "inventory": inventory,
        "validation": checks,
    }
    (HERE / "och47_causative_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"anchored pairs: {len(inventory)} ({len(fluct_roots)} fluctuating)")
    for label, tab in (("all", all_tab), ("fluctuating", fluct_tab)):
        cells = "  ".join(
            f"{p}: {tab[p]['guna']}/{tab[p]['guna'] + tab[p]['vrddhi']}"
            f" = {tab[p]['guna_share_pct']}%" for p in CORE_ORDER + ["puranic"])
        print(f"guṇa share [{label:11}] {cells}")
    print(f"falling per §167? all={out['gradient']['all_pairs_falling']} "
          f"fluctuating={out['gradient']['fluctuating_pairs_falling']}")
    bad = [k for k, v in checks.items() if v is False]
    print("validation:", "OK" if not bad else f"FAILED: {bad}")
    print("-> och47_causative_stats.json written")


if __name__ == "__main__":
    main()
