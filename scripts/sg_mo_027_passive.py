#!/usr/bin/env python3
"""SG-MO-027 «Вторичные спряжения: пассив» — the passive.

Core W2 ① article (content, no kill-gate). The passive (secondary conjugation:
weak root + -ya- + middle endings; ucyate "is said", dṛśyate "is seen") is
NATIVELY tagged in DCS (`Voice=Pass`), so — like the imperfect (SG-MO-016) — it
is directly measurable. It carries the EM1 border: the passive -ya- stem is
formally identical to the class-IV (divādi) present -ya- (paśyati, naśyati), and
DCS separates them by the voice tag, not by the stem shape (P2's class problem).

Three layers (C5 §3): ATTESTED — the passive's distribution (person/tense) over
the pinned snapshot; TRADITIONAL — weak root + -ya- + middle endings
(Whitney §§768–774); GENERATED — the -ya- passive stem by a conjugator.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators + Wilson CI on a headline share; seeded sample. Read-only. Emits into
sangram/articles/passive/data/.
"""
import argparse
import csv
import hashlib
import json
import math
import random
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "passive" / "data"

# H1346 card MO27 follow-up (visa note: "Доля пассива со временем растет?").
# The pinned snapshot's own tables (token/sentence/chapter/text) carry no
# composition-date column (confirmed via PRAGMA table_info, 21-07-2026). But
# dcs-conllu's own lookup file maps each chapter to a DCS dcsTimeSlot stratum,
# and — verified empirically, not assumed — its <chapterId> is the SAME integer
# as this DB's chapter.chapter_id (15789/15790 DB chapters match by
# chapter_id+text_id; 1 orphan chapter has no XML counterpart). slot_era_map.csv
# supplies the slot->era label already used for the varga-series diachrony study.
CHAPTER_INFO = GITHUB / "dcs-conllu" / "lookup" / "chapter-info.xml"
SLOT_ERA_MAP = (GITHUB / "VisualDCS" / "derived-data" / "Fonetika"
                 / "varga-series-diachrony" / "slot_era_map.csv")

FIN = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
       "AND feat_person IS NOT NULL")
FINPASS = f"{FIN} AND feat_voice='Pass'"

SEED = 20260717
SAMPLE_SIZE = 50


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def wilson_ci(k, n, z=1.96):
    if n == 0:
        return (None, None)
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
    return (round(centre - half, 4), round(centre + half, 4))


def dist(cur, col, where, total):
    out = {}
    for v, c in cur.execute(
            f"SELECT {col}, COUNT(*) FROM token WHERE {where} GROUP BY {col} ORDER BY COUNT(*) DESC"):
        out[v if v is not None else "∅"] = {"tokens": c, "share": round(c / total, 4)}
    return out


def load_chapter_slots(xml_path):
    """chapter_id (int) -> dcsTimeSlot ('1'..'5'), keyed by DCS chapterId.

    Regex block-scan (same style as VisualDCS's dcs_phono_engine.load_slots,
    which keys by conllu-path basename instead — here we key by the numeric
    chapterId because that is what joins directly onto this DB's chapter_id).
    """
    txt = open(xml_path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r"<chapter>(.*?)</chapter>", txt, re.S):
        block = m.group(1)
        cid = re.search(r"<chapterId>(.*?)</chapterId>", block)
        slot = re.search(r"<dcsTimeSlot>(.*?)</dcsTimeSlot>", block)
        if cid and slot:
            out[int(cid.group(1))] = slot.group(1)
    return out


def load_slot_era(csv_path):
    """slot ('1'..'5') -> {era_ru, approx_date}, from the VisualDCS diachrony map."""
    out = {}
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            out[row["slot"]] = {"era_ru": row["era_ru"], "approx_date": row["approx_date"]}
    return out


def era_breakdown(cur, chapter_info_path, slot_era_map_path):
    """Finite/finite-passive tokens by dcsTimeSlot era, via chapter_id join."""
    if not chapter_info_path.exists() or not slot_era_map_path.exists():
        return {"available": False,
                "reason": f"missing {chapter_info_path if not chapter_info_path.exists() else slot_era_map_path}"}
    chap_slot = load_chapter_slots(chapter_info_path)
    slot_era = load_slot_era(slot_era_map_path)

    fin_by_chapter = cur.execute(
        f"SELECT c.chapter_id, COUNT(*) FROM token t JOIN sentence s ON s.id=t.sentence_id "
        f"JOIN chapter c ON c.chapter_id=s.chapter_id WHERE {FIN} GROUP BY c.chapter_id").fetchall()
    pass_by_chapter = cur.execute(
        f"SELECT c.chapter_id, COUNT(*) FROM token t JOIN sentence s ON s.id=t.sentence_id "
        f"JOIN chapter c ON c.chapter_id=s.chapter_id WHERE {FINPASS} GROUP BY c.chapter_id").fetchall()

    slot_fin, slot_pass = {}, {}
    unmatched_fin = unmatched_pass = 0
    for cid, c in fin_by_chapter:
        slot = chap_slot.get(cid)
        if slot is None:
            unmatched_fin += c
        else:
            slot_fin[slot] = slot_fin.get(slot, 0) + c
    for cid, c in pass_by_chapter:
        slot = chap_slot.get(cid)
        if slot is None:
            unmatched_pass += c
        else:
            slot_pass[slot] = slot_pass.get(slot, 0) + c

    by_slot = {}
    for slot in sorted(slot_era, key=int):
        n = slot_fin.get(slot, 0)
        k = slot_pass.get(slot, 0)
        by_slot[slot] = {
            "era_ru": slot_era[slot]["era_ru"], "approx_date": slot_era[slot]["approx_date"],
            "finite_total": n, "finite_passive": k,
            "share": round(k / n, 4) if n else None,
            "share_ci95": wilson_ci(k, n) if n else (None, None),
        }
    return {
        "available": True,
        "join_method": ("token->sentence->chapter; chapter.chapter_id == dcs-conllu "
                         "lookup/chapter-info.xml <chapterId> (verified 15789/15790 DB "
                         "chapters match by chapter_id+text_id, 1 orphan, 21-07-2026)"),
        "chapter_info_source": "gasyoun/dcs-conllu lookup/chapter-info.xml",
        "slot_era_source": "VisualDCS derived-data/Fonetika/varga-series-diachrony/slot_era_map.csv",
        "unmatched_finite_tokens": unmatched_fin,
        "unmatched_passive_tokens": unmatched_pass,
        "by_slot": by_slot,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--skip-checksum", action="store_true")
    args = ap.parse_args()
    db = Path(args.db)
    if not db.exists():
        print(f"ERROR: DCS master not found: {db}", file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr)
        return 1
    sha = "skipped" if args.skip_checksum else sha256_file(db)

    fin_total = cur.execute(f"SELECT COUNT(*) FROM token WHERE {FIN}").fetchone()[0]
    fin_pass = cur.execute(f"SELECT COUNT(*) FROM token WHERE {FINPASS}").fetchone()[0]
    part_pass = cur.execute(
        "SELECT COUNT(*) FROM token WHERE upos='VERB' AND feat_verbform='Part' "
        "AND feat_voice='Pass'").fetchone()[0]

    person = dist(cur, "feat_person", FINPASS, fin_pass)
    number = dist(cur, "feat_number", FINPASS, fin_pass)
    tense = dist(cur, "feat_tense", FINPASS, fin_pass)
    third = person.get("3", {}).get("tokens", 0)
    pres = tense.get("Pres", {}).get("tokens", 0)

    top = cur.execute(
        f"SELECT lemma, COUNT(*) c FROM token WHERE {FINPASS} AND lemma IS NOT NULL "
        f"GROUP BY lemma ORDER BY c DESC LIMIT 15").fetchall()

    by_era = era_breakdown(cur, CHAPTER_INFO, SLOT_ERA_MAP)

    ids = [r[0] for r in cur.execute(f"SELECT id FROM token WHERE {FINPASS}")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        sample.append(cur.execute(
            "SELECT t.id, t.form, t.m_unsandhied, t.lemma, t.feat_person, t.feat_number, "
            "t.feat_tense, x.name, c.ref, s.sent_counter FROM token t "
            "JOIN sentence s ON s.id=t.sentence_id JOIN chapter c ON c.chapter_id=s.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone())
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "unsandhied", "lemma", "person", "number",
                    "tense", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "SG-MO-027 «Пассив» — passive secondary conjugation (core W2 ①, content)",
        "toc_ref": "SG-MO-027",
        "kind": "content article (no kill-gate)",
        "method": "finite verbs with Voice=Pass — natively tagged (like the imperfect); distribution over person/tense; the -ya- stem overlaps class-IV present (EM1), separated by the voice tag not the stem",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {
            "finite_total": fin_total, "finite_passive": fin_pass,
            "finite_passive_share": round(fin_pass / fin_total, 4),
            "participial_passive": part_pass,
        },
        "person": person, "number": number, "tense": tense,
        "third_person_share_ci95": {"k": third, "n": fin_pass, "ci95": wilson_ci(third, fin_pass)},
        "present_share_ci95": {"k": pres, "n": fin_pass, "ci95": wilson_ci(pres, fin_pass)},
        "top_lemmas": [{"lemma": l, "tokens": c} for l, c in top],
        "era_breakdown": by_era,
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "EM1_ya_overlap": "the passive -ya- stem is formally identical to the class-IV (divādi) present -ya- (paśyati vs dṛśyate); DCS separates them by Voice=Pass, not the stem shape (P2's class problem)",
            "middle_vs_passive": "the passive uses middle (Ātmanepada) endings; DCS tags Voice=Pass explicitly, but morphologically passive ≈ middle in form outside the -ya- stem",
            "participial": "passive participles (VerbForm=Part, Voice=Pass) are counted separately from the finite passive",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"finite {fin_total:,}; finite passive {fin_pass:,} ({100*fin_pass/fin_total:.1f}%); participial passive {part_pass:,}", file=sys.stderr)
    print(f"person: {[(k, v['share']) for k, v in person.items()]}", file=sys.stderr)
    print(f"tense: {[(k, v['share']) for k, v in tense.items()]}", file=sys.stderr)
    print(f"top: {[(x['lemma'], x['tokens']) for x in summary['top_lemmas'][:8]]}", file=sys.stderr)
    if by_era.get("available"):
        print("era breakdown (slot: era, finite, passive, share):", file=sys.stderr)
        for slot, d in by_era["by_slot"].items():
            print(f"  {slot}: {d['era_ru']} — {d['finite_total']:,} fin, "
                  f"{d['finite_passive']:,} pass, share={d['share']}", file=sys.stderr)
        print(f"unmatched: fin={by_era['unmatched_finite_tokens']:,} "
              f"pass={by_era['unmatched_passive_tokens']:,}", file=sys.stderr)
    else:
        print(f"era breakdown unavailable: {by_era.get('reason')}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
