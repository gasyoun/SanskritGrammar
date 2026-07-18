#!/usr/bin/env python3
"""SG-SE-003 «Инструменталис и датив» — beyond-quota native positive (case sub-article).

Beyond-quota core article (opening set already 19/19). A case sub-article of the
case-semantics cluster (overview = SG-SE-001). Both cases are native via `feat_case`;
this article adds two MEASURED functional findings beyond the bare counts:

INSTRUMENTAL (Ins) 277,143 — a poly-functional case (instrument / passive agent /
accompaniment). Two native signals split the functions:
  * PASSIVE AGENT: an instrumental in a clause with a passive verb (Voice=Pass). ~21,472
    (7.7%) of instrumentals co-occur with a passive finite verb — a lower-bound proxy for
    the agent function (mayā ... kṛtam "by-me it-was-done"). Ties to SG-MO-027 (passive).
  * DCS deprel natively distinguishes obl:instr (instrument) vs obl:soc (accompaniment /
    sociative, "together with") — on the parsed subset.

DATIVE (Dat) 65,423 — the RAREST case (2.1%). Its recipient role largely retreated into
the genitive in classical Sanskrit (Gen 270,763 >> Dat 65,423). It survives strongly in
(a) the RITUAL recipient (agnaye "to Agni", devāya "to the god" — top noun lemmas) and
(b) personal pronouns (mahyam/tubhyam "to me/you"), plus the dative of purpose.

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + denominators;
seeded sample. Read-only. Emits into sangram/articles/instrumental-dative/data/.
"""
import argparse
import csv
import hashlib
import json
import random
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "instrumental-dative" / "data"

SEED = 20260718
SAMPLE_SIZE = 50


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def profile(cur, case):
    n = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case=?", (case,)).fetchone()[0]
    by_number = {k: c for k, c in cur.execute(
        "SELECT feat_number, COUNT(*) FROM token WHERE feat_case=? GROUP BY feat_number ORDER BY COUNT(*) DESC", (case,))}
    top = cur.execute(
        "SELECT lemma, COUNT(*) c FROM token WHERE feat_case=? GROUP BY lemma ORDER BY c DESC LIMIT 10", (case,)).fetchall()
    deprel = {k: c for k, c in cur.execute(
        "SELECT deprel, COUNT(*) FROM token WHERE feat_case=? AND deprel IS NOT NULL AND deprel!='' "
        "GROUP BY deprel ORDER BY COUNT(*) DESC LIMIT 10", (case,))}
    # top NOUN lemmas (excluding pronouns) for the semantic flavour
    top_noun = cur.execute(
        "SELECT lemma, COUNT(*) c FROM token WHERE feat_case=? AND upos='NOUN' GROUP BY lemma ORDER BY c DESC LIMIT 8", (case,)).fetchall()
    return {"total": n, "by_number": by_number, "top_lemmas": [f"{l} ({c})" for l, c in top],
            "top_noun_lemmas": [f"{l} ({c})" for l, c in top_noun], "deprel": deprel}


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

    total = cur.execute("SELECT COUNT(*) FROM token").fetchone()[0]
    ins = profile(cur, "Ins")
    dat = profile(cur, "Dat")
    gen_total = cur.execute("SELECT COUNT(*) FROM token WHERE feat_case='Gen'").fetchone()[0]

    # instrumental as passive agent (co-occurs with a passive finite verb in the same sentence)
    agent = cur.execute(
        "SELECT COUNT(*) FROM token t WHERE t.feat_case='Ins' AND EXISTS "
        "(SELECT 1 FROM token v WHERE v.sentence_id=t.sentence_id AND v.feat_voice='Pass' AND v.upos='VERB')").fetchone()[0]
    # obl:instr vs obl:soc (native functional split, parsed subset)
    obl_instr = ins["deprel"].get("obl:instr", 0)
    obl_soc = ins["deprel"].get("obl:soc", 0)

    ids = [r[0] for r in cur.execute("SELECT id FROM token WHERE feat_case IN ('Ins','Dat')")]
    rng = random.Random(SEED)
    chosen = rng.sample(sorted(ids), min(SAMPLE_SIZE, len(ids)))
    sample = []
    for tid in chosen:
        d = cur.execute(
            "SELECT t.id, t.m_unsandhied, t.lemma, t.feat_case, t.feat_number, t.deprel, x.name, c.ref, se.sent_counter "
            "FROM token t JOIN sentence se ON se.id=t.sentence_id JOIN chapter c ON c.chapter_id=se.chapter_id "
            "JOIN text x ON x.text_id=c.text_id WHERE t.id=?", (tid,)).fetchone()
        sample.append(d)
    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "validation_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["token_id", "form", "lemma", "case", "number", "deprel", "text", "chapter_ref", "sent_counter"])
        for r in sample:
            w.writerow(r)

    summary = {
        "study": "Sangram SG-SE-003 (Инструменталис и датив) — case sub-article, native",
        "toc_ref": "SG-SE-003",
        "kind": "beyond-quota core ① (opening set already 19/19); native positive (feat_case) + measured function signals",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "denominators": {"all_tokens": total},
        "instrumental": {
            **ins,
            "passive_agent_cooccurrence": agent,
            "passive_agent_pct": round(100 * agent / ins["total"], 1),
            "obl_instr_deprel": obl_instr, "obl_soc_deprel": obl_soc,
            "note": "poly-functional (instrument/agent/accompaniment); agent proxy = Ins in a clause with a "
                    "Voice=Pass verb (lower bound, ties to SG-MO-027); deprel splits obl:instr vs obl:soc on the parsed subset",
        },
        "dative": {
            **dat,
            "genitive_total_for_comparison": gen_total,
            "note": "the RAREST case; recipient role largely retreated into the genitive (Gen >> Dat); survives in "
                    "ritual recipient (agnaye/devāya) + personal pronouns (mahyam/tubhyam) + dative of purpose",
        },
        "traditional_layer": {"witness": "Whitney 1889 §§278-286 (instrumental), §§285-287 (dative); "
                                          "Pāṇini 1.4.42 (karaṇa), 1.4.32 (sampradāna)"},
        "validation_sample": {"seed": SEED, "size": len(sample), "file": "validation_sample.tsv"},
        "limits": {
            "function_not_native": "feat_case is the vibhakti; the agent/instrument/accompaniment split is inferred "
                                   "(passive co-occurrence + partial deprel), not a full native tag (SE-013 kāraka endgame)",
            "agent_proxy_lower_bound": "the passive-agent proxy counts any Ins in a passive clause — a lower bound, may include non-agent Ins",
            "deprel_partial": "obl:instr/obl:soc are on the dependency-parsed subset only (~small fraction of Ins)",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Ins {ins['total']:,} — passive-agent proxy {agent:,} ({round(100*agent/ins['total'],1)}%); obl:instr {obl_instr}, obl:soc {obl_soc}", file=sys.stderr)
    print(f"Ins top nouns: {ins['top_noun_lemmas'][:5]}", file=sys.stderr)
    print(f"Dat {dat['total']:,} (rarest) vs Gen {gen_total:,}; top nouns {dat['top_noun_lemmas'][:5]}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
