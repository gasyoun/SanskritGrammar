#!/usr/bin/env python3
"""SG-WF-008 pilot P4: determinative compounds (tatpuruṣa) — extract the sample.

Direct test of evidence-limit EM4 (C5 § 5.2): the traditional samāsa TYPE
(tatpuruṣa / karmadhāraya / dvandva / bahuvrīhi / avyayībhāva) is NOT annotated in
DCS. DCS marks only *that* a token is inside a compound — non-final members carry
feat_case = 'Cpd' (841 052 tokens) — and for 98.6 % of them the dependency relation
is NULL too. So the type must be classified by hand, and pilot P4 measures whether
two INDEPENDENT classification passes even agree (Cohen's κ). If κ < 0.7 the type
taxonomy is revised before any type-frequency is published (C5 § 7 P4 kill-gate).

This script only builds the classification sample; the two passes and κ are
computed by sg_wf_008_kappa.py over the two agent verdict files.

Compound reconstruction (no reliance on head-pointers, which are mostly NULL):
within a sentence ordered by idx, a compound instance is a maximal run of
consecutive tokens t_i … t_{j-1} all with feat_case = 'Cpd', closed by the
idx-adjacent following token t_j whose feat_case != 'Cpd' — the inflected head that
carries the whole compound's case/gender/number. The head's inflection is kept
because a gender/number mismatch with the head noun's lexical gender is the classic
bahuvrīhi signal.

Ground truth consumed, never rebuilt (C3 § 2.1): the pinned VisualDCS SQLite master.

Usage:
  python scripts/sg_wf_008_compound_sample.py [--db PATH] [--n 100] [--skip-checksum]
Outputs into sangram/articles/tatpurusha/data/ .
"""
import argparse
import csv
import hashlib
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
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT_DIR = ROOT / "sangram" / "articles" / "tatpurusha" / "data"

SEED = 20260715
NOMINAL_HEAD = {"NOUN", "ADJ", "PRON", "NUM"}


def reconstruct(tokens):
    """tokens: list of dicts for one sentence, ordered by idx.
    Yield compound instances: dict(members=[...], head=..., member_count)."""
    n = len(tokens)
    i = 0
    while i < n:
        if tokens[i]["feat_case"] == "Cpd":
            j = i
            while j < n and tokens[j]["feat_case"] == "Cpd":
                j += 1
            # members = tokens[i:j]; head candidate = tokens[j] if idx-adjacent & nominal
            members = tokens[i:j]
            head = None
            if j < n and tokens[j]["idx"] == members[-1]["idx"] + 1 \
                    and tokens[j]["upos"] in NOMINAL_HEAD \
                    and tokens[j]["feat_case"] not in (None, "Cpd"):
                head = tokens[j]
            yield {"members": members, "head": head}
            i = j
        else:
            i += 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--n", type=int, default=100)
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

    cpd_members = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Cpd'").fetchone()[0]
    cpd_null_deprel = cur.execute(
        "SELECT COUNT(*) FROM token WHERE feat_case='Cpd' AND deprel IS NULL").fetchone()[0]

    # sentences that contain at least one Cpd member
    sids = [r[0] for r in cur.execute(
        "SELECT DISTINCT sentence_id FROM token WHERE feat_case='Cpd'").fetchall()]

    # reconstruct every compound instance with a clean adjacent nominal head
    detail = ("SELECT t.idx, t.form, t.m_unsandhied, t.lemma, t.upos, t.feat_case, "
              "t.feat_gender, t.feat_number, t.deprel "
              "FROM token t WHERE t.sentence_id=? ORDER BY t.idx")
    sent_sql = ("SELECT s.text_sandhied, c.ref, x.name FROM sentence s "
                "JOIN chapter c ON c.chapter_id=s.chapter_id "
                "JOIN text x ON x.text_id=c.text_id WHERE s.id=?")

    all_instances = []          # (sid, members, head)
    size_hist = Counter()
    headless = 0
    for sid in sids:
        toks = [dict(idx=r[0], form=r[1], m_unsandhied=r[2], lemma=r[3], upos=r[4],
                     feat_case=r[5], feat_gender=r[6], feat_number=r[7], deprel=r[8])
                for r in cur.execute(detail, (sid,)).fetchall()]
        for inst in reconstruct(toks):
            if inst["head"] is None:
                headless += 1
                continue
            mc = len(inst["members"]) + 1
            size_hist[mc] += 1
            all_instances.append((sid, inst["members"], inst["head"]))

    total_instances = len(all_instances)

    # sample N compound instances with a clean binary/multi head, seed-locked
    rng = random.Random(SEED)
    idxs = rng.sample(range(total_instances), min(args.n, total_instances))
    sample = [all_instances[i] for i in sorted(idxs)]

    rows = []
    for k, (sid, members, head) in enumerate(sample, 1):
        sent = cur.execute(sent_sql, (sid,)).fetchone()
        text_sandhied, ref, textname = sent or ("", "", "")
        lemma_form = "-".join(m["lemma"] for m in members) + "-" + head["lemma"]
        surface = " ".join(m["m_unsandhied"] or m["form"] for m in members) \
            + " " + (head["m_unsandhied"] or head["form"])
        deprels = "|".join((m["deprel"] or "-") for m in members)
        rows.append({
            "compound_id": f"cpd:{k:03d}",
            "compound_lemma": lemma_form,
            "compound_surface": surface,
            "member_count": len(members) + 1,
            "head_lemma": head["lemma"],
            "head_upos": head["upos"],
            "head_case": head["feat_case"] or "",
            "head_gender": head["feat_gender"] or "",
            "head_number": head["feat_number"] or "",
            "member_deprels": deprels,
            "chapter_ref": ref or "",
            "text": textname or "",
            "sentence": (text_sandhied or "")[:200],
        })

    fields = list(rows[0].keys())
    with open(OUT_DIR / "classification_sample.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        w.writerows(rows)

    summary = {
        "study": "SG-WF-008 pilot P4: determinative compounds (tatpuruṣa) — inter-annotator κ",
        "method": "C5 § 3 via C3 cycle; direct test of EM4 (§ 5.2); kill-gate = Cohen's κ < 0.7",
        "snapshot": {"master": str(db), "sha256": sha256, "provenance": prov},
        "em4_evidence": {
            "cpd_members_total": cpd_members,
            "cpd_members_deprel_null": cpd_null_deprel,
            "cpd_members_deprel_null_pct": round(100 * cpd_null_deprel / cpd_members, 2),
            "note": ("DCS marks only that a token is inside a compound (feat_case='Cpd'); "
                     "the traditional samāsa TYPE is not a feature, and for 98.6 % of "
                     "members even the UD dependency relation is NULL — the type is "
                     "unrecoverable from annotation"),
        },
        "compound_instances": {
            "definition": ("maximal consecutive Cpd-run + idx-adjacent inflected nominal head "
                           "(NOUN/ADJ/PRON/NUM); head carries whole-compound case/gender/number"),
            "total_with_clean_head": total_instances,
            "headless_or_nonadjacent_runs_skipped": headless,
            "member_count_distribution": {str(k): v for k, v in sorted(size_hist.items())},
        },
        "sample": {
            "seed": SEED,
            "n": len(rows),
            "file": "classification_sample.tsv",
            "purpose": ("two independent blind passes classify each into "
                        "{tatpuruṣa, karmadhāraya, dvigu, dvandva, bahuvrīhi, avyayībhāva, unclear}; "
                        "κ computed by sg_wf_008_kappa.py"),
        },
    }
    (OUT_DIR / "sample_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"Cpd members: {cpd_members} ({summary['em4_evidence']['cpd_members_deprel_null_pct']}% deprel NULL)")
    print(f"compound instances with clean head: {total_instances}")
    print(f"member-count distribution: {dict(sorted(size_hist.items())[:8])}")
    print(f"sample: {len(rows)} instances (seed {SEED}) -> {OUT_DIR}/classification_sample.tsv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
