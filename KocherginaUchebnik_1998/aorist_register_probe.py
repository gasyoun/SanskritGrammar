#!/usr/bin/env python
"""aorist_register_probe.py — register-frequency probe for HK-207.

HK-207 claims the aorist is rare in narrative, more common in colloquial
speech / dialogue (dramas): "Аорист редко при повествовании, чаще в
разговорной речи, диалоге (драмы)." The prior verdict read "cannot be
measured against DCS-2021 (no register/speech-act tagging)" — true as far
as it goes (DCS carries NO drama/nāṭaka texts at all: checked the full
270-text inventory, zero — no Śakuntalā, no Mṛcchakaṭikā, no Bhāsa play;
Nāṭyaśāstra is a treatise ABOUT dramaturgy, not a play). So the literal
"dramas" comparison set does not exist in this corpus, full stop.

WHAT IS TESTABLE INSTEAD: a genre proxy at the TEXT level using structure
that's actually in DCS. Two textually well-defined register-classes:

  DIALOGUE proxy   = the classical Upaniṣads structurally built as
                      teacher-student catechism (guru-śiṣya direct-speech
                      exchange is their organizing frame, not incidental)
  NARRATIVE/PRESCRIPTIVE proxy
                    = Brāhmaṇas + Śrauta-sūtras: ritual-injunction prose,
                      procedural instruction, not dialogically framed

  Epic (Mahābhārata, Rāmāyaṇa) is reported SEPARATELY, not folded into
  either bucket — it genuinely mixes extended third-person narration with
  extensive quoted first-person dialogue, so it cannot cleanly stand in
  for "narrative" the way the claim's own contrast implies.

AORIST IDENTIFICATION (DCS-2026, annotation-robust): DCS collapses aorist
with perfect/pluperfect under feat_tense='Past' (no separate 'Aor' value)
— but 7 of the feat_formation subtypes under Past ARE aorist-specific and
unambiguous: root, them(atic), s(-aorist), is(-aorist), red(uplicated
aorist), sa(-aorist), sis(-aorist). The untagged remainder (feat_formation
IS NULL) is dominated by the reduplicated PERFECT (per H1000/OCH-68's own
finding) and is excluded — it cannot be cleanly split into perfect vs
aorist, and folding it in either direction would bias the count.

NOTE ON PROVENANCE: HK-1's cited 2,452-token aorist figure comes from the
OLDER DCS-2021 CSV export (a different tense-code scheme), not this
session's DCS-2026 dcs_full.sqlite. The two are not directly comparable
token-for-token; this probe is internally consistent (same DB, same method,
both register buckets) but should not be read as reproducing HK-1's number.

Usage:  python KocherginaUchebnik_1998/aorist_register_probe.py [--db PATH]
Writes  hk207_aorist_register_stats.json next to this script.
"""
import argparse
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"

AORIST_FORMATIONS = {"root", "them", "s", "is", "red", "sa", "sis"}

DIALOGUE_TEXTS = {
    "Bṛhadāraṇyakopaniṣad", "Chāndogyopaniṣad", "Kaṭhopaniṣad",
    "Kauṣītakyupaniṣad", "Śvetāśvataropaniṣad", "Muṇḍakopaniṣad",
    "Taittirīyopaniṣad", "Aitareyopaniṣad",
}
NARRATIVE_TEXTS = {
    "Aitareyabrāhmaṇa", "Śatapathabrāhmaṇa", "Jaiminīyabrāhmaṇa",
    "Pañcaviṃśabrāhmaṇa", "Kauṣītakibrāhmaṇa", "Gopathabrāhmaṇa",
    "Taittirīyabrāhmaṇa", "Ṣaḍviṃśabrāhmaṇa", "Sāmavidhānabrāhmaṇa",
    "Baudhāyanaśrautasūtra", "Āpastambaśrautasūtra", "Kātyāyanaśrautasūtra",
    "Āśvalāyanaśrautasūtra", "Āśvālāyanaśrautasūtra", "Śāṅkhāyanaśrautasūtra",
    "Mānavaśrautasūtra", "Vārāhaśrautasūtra", "Vaikhānasaśrautasūtra",
    "Drāhyāyaṇaśrautasūtra", "Hiraṇyakeśiśrautasūtra", "Jaiminīyaśrautasūtra",
    "Bhāradvājaśrautasūtra",
}
EPIC_TEXTS = {"Mahābhārata", "Rāmāyaṇa"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()

    text_ids = {}
    for name, tid in cur.execute("SELECT name, text_id FROM text"):
        text_ids[name] = tid

    def bucket_counts(names):
        ids = [text_ids[n] for n in names if n in text_ids]
        missing = [n for n in names if n not in text_ids]
        if not ids:
            return {"aorist": 0, "past_total": 0, "verbal_total": 0, "missing_texts": missing}
        placeholders = ",".join("?" * len(ids))
        verbal_total = cur.execute(f"""
            SELECT COUNT(*) FROM token tok
            JOIN sentence s ON tok.sentence_id = s.id
            JOIN chapter c ON s.chapter_id = c.chapter_id
            WHERE c.text_id IN ({placeholders}) AND tok.upos='VERB'
        """, ids).fetchone()[0]
        past_total = cur.execute(f"""
            SELECT COUNT(*) FROM token tok
            JOIN sentence s ON tok.sentence_id = s.id
            JOIN chapter c ON s.chapter_id = c.chapter_id
            WHERE c.text_id IN ({placeholders}) AND tok.upos='VERB' AND tok.feat_tense='Past'
        """, ids).fetchone()[0]
        fmt_placeholders = ",".join("?" * len(AORIST_FORMATIONS))
        aorist = cur.execute(f"""
            SELECT COUNT(*) FROM token tok
            JOIN sentence s ON tok.sentence_id = s.id
            JOIN chapter c ON s.chapter_id = c.chapter_id
            WHERE c.text_id IN ({placeholders}) AND tok.upos='VERB'
              AND tok.feat_tense='Past' AND tok.feat_formation IN ({fmt_placeholders})
        """, ids + list(AORIST_FORMATIONS)).fetchone()[0]
        return {"aorist": aorist, "past_total": past_total, "verbal_total": verbal_total,
                "missing_texts": missing}

    def pack(label, names):
        c = bucket_counts(names)
        return {
            "label": label, "texts": sorted(n for n in names if n in text_ids),
            "missing_texts": c["missing_texts"],
            "aorist_tokens": c["aorist"],
            "verbal_tokens": c["verbal_total"],
            "aorist_pct_of_verbal": round(100 * c["aorist"] / c["verbal_total"], 3)
                                    if c["verbal_total"] else None,
            "aorist_pct_of_past": round(100 * c["aorist"] / c["past_total"], 2)
                                   if c["past_total"] else None,
        }

    dialogue = pack("dialogue_proxy_upanisads", DIALOGUE_TEXTS)
    narrative = pack("narrative_prescriptive_brahmana_srautasutra", NARRATIVE_TEXTS)
    epic = pack("epic_mixed_narration_and_dialogue", EPIC_TEXTS)
    overall = bucket_counts(set(text_ids))
    overall_pack = {
        "label": "whole_corpus", "aorist_tokens": overall["aorist"],
        "verbal_tokens": overall["verbal_total"],
        "aorist_pct_of_verbal": round(100 * overall["aorist"] / overall["verbal_total"], 3)
                                if overall["verbal_total"] else None,
    }

    ratio = None
    if dialogue["aorist_pct_of_verbal"] and narrative["aorist_pct_of_verbal"]:
        ratio = round(dialogue["aorist_pct_of_verbal"] / narrative["aorist_pct_of_verbal"], 2)

    out = {
        "instrument": "aorist_register_probe.py over dcs_full.sqlite — genre-proxy test "
                      "(no drama texts exist in DCS at all; checked the full 270-text "
                      "inventory before building this proxy)",
        "aorist_definition": "feat_tense=Past AND feat_formation IN "
                              + str(sorted(AORIST_FORMATIONS))
                              + " (excludes the untagged Past remainder, which H1000/OCH-68 "
                                "found dominated by the untagged reduplicated perfect)",
        "dialogue_proxy": dialogue,
        "narrative_proxy": narrative,
        "epic_reported_separately": epic,
        "whole_corpus": overall_pack,
        "dialogue_over_narrative_ratio": ratio,
        "expected_by_hk207": "dialogue_proxy aorist share > narrative_proxy aorist share",
        "confirmed": (ratio is not None and ratio > 1),
        "caveat": "genre proxy, not the literal drama/colloquial-speech contrast the claim "
                  "names (that corpus doesn't exist in DCS) — Upaniṣad catechism-dialogue vs "
                  "Brāhmaṇa/Śrautasūtra ritual-prescriptive prose is the closest available "
                  "structural analogue, not identical to it",
    }
    (HERE / "hk207_aorist_register_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"dialogue proxy (Upaniṣads): {dialogue['aorist_tokens']} aorist / "
          f"{dialogue['verbal_tokens']} verbal = {dialogue['aorist_pct_of_verbal']}%")
    print(f"narrative proxy (Brāhmaṇa+Śrautasūtra): {narrative['aorist_tokens']} aorist / "
          f"{narrative['verbal_tokens']} verbal = {narrative['aorist_pct_of_verbal']}%")
    print(f"epic (reported separately): {epic['aorist_tokens']} aorist / "
          f"{epic['verbal_tokens']} verbal = {epic['aorist_pct_of_verbal']}%")
    print(f"whole corpus: {overall_pack['aorist_tokens']} aorist / "
          f"{overall_pack['verbal_tokens']} verbal = {overall_pack['aorist_pct_of_verbal']}%")
    print(f"dialogue/narrative ratio: {ratio}  confirmed: {out['confirmed']}")
    if dialogue["missing_texts"] or narrative["missing_texts"]:
        print("MISSING TEXTS (not in DB):", dialogue["missing_texts"], narrative["missing_texts"])
    print("-> hk207_aorist_register_stats.json written")


if __name__ == "__main__":
    main()
