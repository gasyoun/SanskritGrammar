"""och_voice_stats.py — corpus instrument for the Ocherk-1978 voice claims (H1051, OCH-75..OCH-96).

The DCS snapshot's native `feat_voice` carries ONLY `Pass` (36,701 tokens) — there is no
Act/Mid tagging (the KZ-2 finding, reconfirmed here). Parasmaipada vs atmanepada is therefore
recovered from UNAMBIGUOUS personal endings on the unsandhied form of finite tokens; ambiguous
endings (-a, -ta, -tam, -tām, -e ...) are left unclassified and counted honestly.

Measures (→ och_voice_stats.json):
  1. P/Ā ending census over finite non-passive tokens (global + coverage).
  2. feat_voice=Pass distribution by tense (is the dedicated passive present-system + aorist?).
  3. √kram: krāma- vs krama- present stems × P/Ā (§117).
  4. √i: middle-classified finite tokens and their forms (adhi-i 'study' restriction, §127).
  5. √as: middle-classified finite tokens (claimed only inside future II, §127).
  6. √śī: media tantum — any P-classified tokens? (§127).
  7. -ayāna- middle participles of aya-stems (§115 fn).
  8. Impersonal-passive existence probes: passive forms of gam/sthā (§206).
  9. Passive-clause agent position: share of sentences with a finite Pass verb whose first
     token is instrumental (§214 «обычно имя в I. на первом месте»).

Deterministic; snapshot = dcs_full.sqlite (dcs-conllu 04e0778), path convention as in
och22_token_weighted.py.
"""
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
DCS_SQLITE = REPO.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT = Path(__file__).resolve().parent / "och_voice_stats.json"

P_UNAMB = ("ti", "thas", "si", "mi", "vas", "mas", "anti", "tu", "antu", "hi",
           "āni", "āva", "āma", "an", "us", "īt")
A_UNAMB = ("te", "ete", "ante", "ate", "se", "āthe", "dhve", "vahe", "mahe",
           "etām", "antām", "atām", "sva", "dhvam", "āmahai", "thās", "mahi",
           "vahi", "īta", "īran", "ire", "āte")


def classify(form):
    f = form.lower()
    p = any(f.endswith(e) for e in P_UNAMB)
    a = any(f.endswith(e) for e in A_UNAMB)
    if p and not a:
        return "P"
    if a and not p:
        return "A"
    return None


def main():
    db = sqlite3.connect(DCS_SQLITE)
    cur = db.cursor()
    out = {"instrument": "och_voice_stats.py over dcs_full.sqlite (dcs-conllu 04e0778)",
           "native_voice_values": {}, "sections": {}}

    for v, n in cur.execute("SELECT feat_voice, COUNT(*) FROM token GROUP BY feat_voice"):
        out["native_voice_values"][str(v)] = n

    # 1. global P/A census over finite non-passive tokens
    c = Counter()
    for form, n in cur.execute(
            "SELECT m_unsandhied, COUNT(*) FROM token WHERE feat_person IS NOT NULL "
            "AND feat_voice IS NULL AND m_unsandhied IS NOT NULL GROUP BY m_unsandhied"):
        c[classify(form) or "unclassified"] += n
    tot = sum(c.values())
    out["sections"]["pa_census"] = {
        "finite_nonpassive_tokens": tot, "P": c["P"], "A": c["A"],
        "unclassified": c["unclassified"],
        "coverage_pct": round(100 * (c["P"] + c["A"]) / tot, 1),
        "P_share_of_classified_pct": round(100 * c["P"] / (c["P"] + c["A"]), 1),
        "A_share_of_classified_pct": round(100 * c["A"] / (c["P"] + c["A"]), 1)}

    # 2. dedicated passive by tense
    by_tense = dict(cur.execute(
        "SELECT COALESCE(feat_tense,'(none)'), COUNT(*) FROM token "
        "WHERE feat_voice='Pass' GROUP BY feat_tense ORDER BY 2 DESC").fetchall())
    out["sections"]["passive_by_tense"] = by_tense

    # 3. kram: stem grade x voice
    kram = Counter()
    for form, n in cur.execute(
            "SELECT m_unsandhied, COUNT(*) FROM token WHERE lemma='kram' "
            "AND feat_person IS NOT NULL AND feat_voice IS NULL "
            "AND m_unsandhied IS NOT NULL GROUP BY m_unsandhied"):
        v = classify(form)
        f = form.lower()
        stem = "krāma" if "krāma" in f else ("krama" if "krama" in f else None)
        if v and stem:
            kram[f"{stem}-{v}"] += n
    out["sections"]["kram_grade_voice"] = dict(kram)

    # 4-6. per-lemma middle/active probes
    for lemma, key in (("i", "i_middle_forms"), ("as", "as_middle_forms"),
                       ("śī", "shi_forms")):
        rows = cur.execute(
            "SELECT m_unsandhied, COUNT(*) FROM token WHERE lemma=? "
            "AND feat_person IS NOT NULL AND feat_voice IS NULL "
            "AND m_unsandhied IS NOT NULL GROUP BY m_unsandhied ORDER BY 2 DESC",
            (lemma,)).fetchall()
        p_n = sum(n for f, n in rows if classify(f) == "P")
        a_n = sum(n for f, n in rows if classify(f) == "A")
        a_forms = [(f, n) for f, n in rows if classify(f) == "A"][:12]
        out["sections"][key] = {"P_tokens": p_n, "A_tokens": a_n,
                                "top_A_forms": a_forms}

    # 7. -ayāna- middle participles of aya-stems. Substring match alone over-captures
    #    śayāna- (the participle of śī itself) and other short-stem matches where 'ayāna'
    #    sits at index ≤1 — require the match at index ≥2 so a real aya-stem precedes it
    #    (darśayāna-, kāmayāna-), and report the surviving distinct forms for eyeballing.
    ay_forms = Counter()
    for form, n in cur.execute(
            "SELECT m_unsandhied, COUNT(*) FROM token WHERE m_unsandhied LIKE '%ayāna%' "
            "AND feat_verbform='Part' GROUP BY m_unsandhied"):
        if form.lower().find("ayāna") >= 2 and "ayamāna" not in form.lower():
            ay_forms[form] += n
    n_ayamana = cur.execute(
        "SELECT COUNT(*) FROM token WHERE m_unsandhied LIKE '%ayamāna%' "
        "AND feat_verbform='Part'").fetchone()[0]
    out["sections"]["ayana_participles"] = {
        "ayāna_index2plus": sum(ay_forms.values()),
        "ayāna_distinct_forms": sorted(ay_forms.items(), key=lambda x: -x[1])[:15],
        "ayamāna": n_ayamana}

    # 8. impersonal-passive probes: passive forms of motion/state intransitives
    probes = {}
    for lemma in ("gam", "sthā"):
        probes[lemma] = cur.execute(
            "SELECT COUNT(*) FROM token WHERE lemma=? AND feat_voice='Pass'",
            (lemma,)).fetchone()[0]
    out["sections"]["intransitive_passive_tokens"] = probes

    # 9. agent position in passive clauses (§214). Two readings measured honestly:
    #    (a) unconditional: share of finite-passive sentences whose FIRST token is Ins;
    #    (b) conditional on an expressed agent: among finite-passive sentences that
    #        CONTAIN a nominal Ins token at all, how often is the sentence-initial
    #        token that instrumental. (Agentless passives are the norm, so (b) is the
    #        fair operationalisation of «на первом месте обычно имя в I.».)
    cur.execute("""SELECT t.sent_id FROM token t
                   WHERE t.feat_voice='Pass' AND t.feat_person IS NOT NULL
                   GROUP BY t.sent_id""")
    sent_ids = [r[0] for r in cur.fetchall()]
    first_ins = with_ins = first_ins_given_ins = checked = 0
    for i in range(0, len(sent_ids), 900):
        chunk = sent_ids[i:i + 900]
        ph = ",".join("?" * len(chunk))
        firsts = dict(cur.execute(
            "SELECT sent_id, feat_case FROM token WHERE sent_id IN (%s) "
            "AND idx=(SELECT MIN(idx) FROM token t2 WHERE t2.sent_id=token.sent_id)"
            % ph, chunk).fetchall())
        has_ins = {r[0] for r in cur.execute(
            "SELECT DISTINCT sent_id FROM token WHERE sent_id IN (%s) "
            "AND feat_case='Ins' AND upos IN ('NOUN','PRON','PROPN')" % ph,
            chunk).fetchall()}
        for sid, case in firsts.items():
            checked += 1
            if case == "Ins":
                first_ins += 1
            if sid in has_ins:
                with_ins += 1
                if case == "Ins":
                    first_ins_given_ins += 1
    out["sections"]["passive_clause_agent_position"] = {
        "sentences_with_finite_passive": len(sent_ids), "checked": checked,
        "first_token_instrumental": first_ins,
        "unconditional_share_pct": round(100 * first_ins / checked, 1) if checked else None,
        "sentences_containing_nominal_ins": with_ins,
        "first_token_ins_given_ins_present": first_ins_given_ins,
        "conditional_share_pct": round(100 * first_ins_given_ins / with_ins, 1) if with_ins else None}

    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out["sections"], ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
