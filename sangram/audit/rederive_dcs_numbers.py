#!/usr/bin/env python3
"""H1229 adversarial re-derivation of published DCS-derived Sangram statistics.

Independent re-derivation of every mechanically checkable number published in
sangram/articles/*/index.mdx + manifests + the W2 checkpoint, straight from the
pinned DCS master (raw `token`/`lemma`/`sentence` tables — NOT by re-running the
generation scripts). Expected values below are the PUBLISHED values (with their
file anchors); the script recomputes each from scratch and reports OK/MISMATCH.

The five instrument caveats under audit (each check that touches one names it):
  C1 gana-code       lemma.grammar "N.P./Ā." is a DCS-internal code, not gaṇa
  C2 red-aorist      feat_formation has no 'perfect'; red@Past = redup. AORIST
  C3 krt-surface     kṛt surface-ending lemma match ~59% false positives
  C4 taddhita-seg    -tva/-tā/-maya/-vat are segmentation-layer morpheme-tokens
  C5 compound-type   compound TYPE unannotated; sample shares ≠ corpus freqs

Contract C3 (pin): refuses to run without the provenance pin. Read-only.
Output: sangram/audit/audit_results.json + console table.
"""
import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[2]
GITHUB = ROOT.parent
DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
OUT = Path(__file__).resolve().parent / "audit_results.json"

FIN = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
       "AND feat_person IS NOT NULL")
CLASS10 = "(l.grammar LIKE '10%' OR l.grammar LIKE '%,10%' OR l.grammar LIKE '% 10%')"

results = []


def check(cid, anchor, label, expected, derived, note=""):
    ok = (expected == derived)
    results.append({"id": cid, "anchor": anchor, "label": label,
                    "expected": expected, "derived": derived,
                    "match": ok, "note": note})
    flag = "OK " if ok else "*** MISMATCH"
    print(f"[{cid}] {flag} expected={expected} derived={derived}  {label}")
    return ok


def main():
    if not DB.exists():
        print(f"ERROR: DCS master not found: {DB}", file=sys.stderr)
        return 1
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr)
        return 1
    print(f"pin: {prov.get('source_commit')} imported {prov.get('imported_at')}\n")

    def q(sql, *args):
        return cur.execute(sql, args).fetchone()[0]

    def dist(sql, *args):
        return {r[0]: r[1] for r in cur.execute(sql, args)}

    # ---------- BASE (corpus pin, cited in every article §2) ----------
    check("BASE-1", "SANGRAM_CORPUS_EVIDENCE_METHOD.mdx:44", "total tokens",
          5_688_416, q("SELECT COUNT(*) FROM token"))
    check("BASE-2", "same", "texts", 270, q("SELECT COUNT(*) FROM text"))
    check("BASE-3", "same", "sentences", 754_726, q("SELECT COUNT(*) FROM sentence"))
    check("BASE-4", "preverbs manifest", "lemmas", 180_176, q("SELECT COUNT(*) FROM lemma"))
    check("BASE-5", "karaka-case:54", "deprel-tagged tokens (parsed subset)",
          223_751, q("SELECT COUNT(*) FROM token WHERE deprel IS NOT NULL AND deprel<>''"))
    check("BASE-6", "SANGRAM_CORPUS_EVIDENCE_METHOD.mdx:44", "texts with syntax trees",
          74, q("SELECT COUNT(*) FROM text WHERE has_dependencies=1"))

    # ---------- SG-MO-012 conjugation-overview ----------
    fin_total = q(f"SELECT COUNT(*) FROM token WHERE {FIN}")
    check("MO012-1", "conjugation-overview:50", "finite verb tokens", 523_721, fin_total)
    d = dist(f"SELECT feat_person, COUNT(*) FROM token WHERE {FIN} GROUP BY feat_person")
    check("MO012-2", "conjugation-overview:65", "person 3/2/1",
          (420_305, 63_865, 39_551), (d.get("3"), d.get("2"), d.get("1")))
    d = dist(f"SELECT feat_number, COUNT(*) FROM token WHERE {FIN} GROUP BY feat_number")
    check("MO012-3", "conjugation-overview:67", "number Sing/Plur/Dual",
          (420_271, 94_078, 9_372), (d.get("Sing"), d.get("Plur"), d.get("Dual")))
    d = dist(f"SELECT feat_tense, COUNT(*) FROM token WHERE {FIN} GROUP BY feat_tense")
    check("MO012-4", "conjugation-overview:73", "tense Pres/Past/Impf/Fut",
          (353_215, 102_055, 46_695, 21_556),
          (d.get("Pres"), d.get("Past"), d.get("Impf"), d.get("Fut")),
          note=f"full tense dist: {sorted(d.items(), key=lambda x: -x[1])}")
    d = dist(f"SELECT feat_mood, COUNT(*) FROM token WHERE {FIN} GROUP BY feat_mood")
    check("MO012-5", "conjugation-overview:84 + imperative-optative:110",
          "mood Ind/Opt/Imp/Jus/Sub/Prec/Cond/Pot",
          (364_771, 91_912, 56_506, 5_258, 4_325, 577, 340, 32),
          tuple(d.get(m) for m in ("Ind", "Opt", "Imp", "Jus", "Sub", "Prec", "Cond", "Pot")))
    n_pass = q(f"SELECT COUNT(*) FROM token WHERE {FIN} AND feat_voice='Pass'")
    check("MO012-6", "conjugation-overview:96 + passive:48", "finite passive",
          29_699, n_pass)
    check("MO012-7", "conjugation-overview:96", "finite active (unmarked)",
          494_022, fin_total - n_pass)

    # ---------- SG-WF-001 word-structure-overview ----------
    d = dist("""SELECT CASE
        WHEN feat_case='Cpd' THEN 'compound_member'
        WHEN feat_verbform IN ('Part','Conv','Gdv','Inf') THEN 'nonfinite_deverbal'
        WHEN upos='VERB' THEN 'finite_verb'
        WHEN upos IN ('NOUN','ADJ') THEN 'nominal_mixed'
        WHEN upos IN ('PRON','PART','ADV','CONJ','SCONJ','ADP','NUM','INTJ') THEN 'closed_class'
        ELSE 'other_punct' END, COUNT(*) FROM token GROUP BY 1""")
    check("WF001-1", "word-structure-overview:67", "partition nominal/closed/Cpd/finite/krt",
          (2_271_734, 1_616_811, 841_052, 523_738, 435_081),
          (d.get("nominal_mixed"), d.get("closed_class"), d.get("compound_member"),
           d.get("finite_verb"), d.get("nonfinite_deverbal")),
          note="finite_verb bucket (no person filter) vs MO012 universe differs by design")
    check("WF001-2", "word-structure-overview:78", "distinct finite-verb lemmas",
          8_053, q(f"SELECT COUNT(DISTINCT lemma) FROM token WHERE {FIN} AND lemma IS NOT NULL"))
    tops = [r[1] for r in cur.execute(
        f"SELECT lemma, COUNT(*) c FROM token WHERE {FIN} AND lemma IS NOT NULL "
        "GROUP BY lemma ORDER BY c DESC LIMIT 100")]
    check("WF001-3", "word-structure-overview:80", "top-10/50/100 finite concentration %",
          (29.7, 48.7, 58.6),
          (round(100 * sum(tops[:10]) / fin_total, 1),
           round(100 * sum(tops[:50]) / fin_total, 1),
           round(100 * sum(tops[:100]) / fin_total, 1)))
    d = dist("SELECT feat_formation, COUNT(*) FROM token WHERE upos='VERB' "
             "AND feat_formation IS NOT NULL GROUP BY feat_formation")
    check("WF001-4", "word-structure-overview:95", "feat_formation on all VERB [C2]",
          (17_440, 5_690, 5_386, 2_781, 1_508, 1_077, 833, 124, 41),
          (sum(d.values()), d.get("root"), d.get("peri"), d.get("them"),
           d.get("s"), d.get("is") or d.get("iṣ"), d.get("red"), d.get("sa"),
           d.get("sis") or d.get("siṣ")),
          note=f"formation values present: {sorted(d)}")
    check("WF001-5", "word-structure-overview:49+73", "root+affix transparent share %",
          16.8, round(100 * (d_part := (523_738 + 435_081)) / 5_688_416, 1))

    # ---------- SG-MO-001 declension-overview ----------
    NOUNW = ("upos='NOUN' AND feat_case IS NOT NULL AND feat_case<>'' "
             "AND feat_case<>'Cpd'")
    noun_total = q(f"SELECT COUNT(*) FROM token WHERE {NOUNW}")
    check("MO001-1", "declension-overview:44", "inflected common-noun tokens",
          1_790_270, noun_total)
    d = dist(f"SELECT feat_number, COUNT(*) FROM token WHERE {NOUNW} GROUP BY feat_number")
    check("MO001-2", "declension-overview:58", "noun number Sing/Plur/Dual",
          (1_419_826, 332_943, 37_501), (d.get("Sing"), d.get("Plur"), d.get("Dual")))
    d = dist(f"SELECT feat_case, COUNT(*) FROM token WHERE {NOUNW} GROUP BY feat_case")
    check("MO001-3", "declension-overview:67", "noun case dist Nom..Dat",
          (692_647, 430_396, 184_609, 177_320, 138_883, 65_363, 61_862, 39_190),
          tuple(d.get(c) for c in ("Nom", "Acc", "Ins", "Loc", "Gen", "Voc", "Abl", "Dat")))
    check("MO001-4", "checkpoint:87 (G2)", "distinct declined-noun lemmas",
          57_144, q(f"SELECT COUNT(DISTINCT lemma) FROM token WHERE {NOUNW}"))
    rows = cur.execute(
        f"SELECT lemma, COUNT(DISTINCT feat_case||'/'||feat_number) FROM token "
        f"WHERE {NOUNW} AND feat_number IS NOT NULL GROUP BY lemma").fetchall()
    cells = sorted(r[1] for r in rows)
    n_lem = len(cells)
    one = sum(1 for c in cells if c == 1)
    full = sum(1 for c in cells if c >= 24)
    med = cells[n_lem // 2] if n_lem % 2 else (cells[n_lem // 2 - 1] + cells[n_lem // 2]) / 2
    check("MO001-5", "checkpoint:87 (G2)", "G2: median cells / %exactly-1 / %all-24 / fill%",
          (1, 58.9, 0.0, 10.44),
          (med, round(100 * one / n_lem, 1), round(100 * full / n_lem, 2),
           round(100 * sum(cells) / (24 * n_lem), 2)),
          note=f"lemma universe here {n_lem} (G2 asset says 57,144)")

    # ---------- SG-SE-001 case-system-overview ----------
    case_all = q("SELECT COUNT(*) FROM token WHERE feat_case IS NOT NULL AND feat_case<>''")
    cpd = q("SELECT COUNT(*) FROM token WHERE feat_case='Cpd'")
    check("SE001-1", "case-system-overview:40", "tokens with feat_case (any upos)",
          4_014_688, case_all)
    check("SE001-2", "case-system-overview:41", "8 vibhakti total / Cpd excluded",
          (3_173_636, 841_052), (case_all - cpd, cpd))
    d = dist("SELECT feat_case, COUNT(*) FROM token WHERE feat_case IS NOT NULL "
             "AND feat_case<>'' GROUP BY feat_case")
    check("SE001-3", "case-system-overview:53 + SE002/3/4/5 universes",
          "all-upos case dist Nom/Acc/Ins/Gen/Loc/Voc/Abl/Dat",
          (1_419_146, 742_293, 277_143, 270_763, 243_215, 81_088, 74_565, 65_423),
          tuple(d.get(c) for c in ("Nom", "Acc", "Ins", "Gen", "Loc", "Voc", "Abl", "Dat")))
    check("SE001-4", "case-system-overview:65", "Nom+Acc share of 8-vibhakti %",
          68, round(100 * (d["Nom"] + d["Acc"]) / (case_all - cpd)))

    # ---------- SG-SE-002 nominative-accusative ----------
    nsubj = dist("SELECT feat_case, COUNT(*) FROM token WHERE deprel='nsubj' "
                 "AND feat_case IS NOT NULL AND feat_case<>'' GROUP BY feat_case")
    check("SE002-1", "nominative-accusative:55", "nsubj case-tagged: total/Nom/Loc/Gen/Acc",
          (20_062, 19_626, 266, 43, 43),
          (sum(nsubj.values()), nsubj.get("Nom"), nsubj.get("Loc"),
           nsubj.get("Gen"), nsubj.get("Acc")))
    obj = dist("SELECT feat_case, COUNT(*) FROM token WHERE deprel='obj' "
               "AND feat_case IS NOT NULL AND feat_case<>'' GROUP BY feat_case")
    check("SE002-2", "nominative-accusative:76", "obj case-tagged: total/Acc",
          (16_933, 15_269), (sum(obj.values()), obj.get("Acc")))
    cop_heads = dist("""SELECT h.feat_case, COUNT(DISTINCT h.id) FROM token c
        JOIN token h ON h.sentence_id=c.sentence_id AND h.idx=c.head
        WHERE c.deprel='cop' AND h.feat_case IS NOT NULL AND h.feat_case<>''
        GROUP BY h.feat_case""")
    tot_cop = sum(cop_heads.values())
    check("SE002-3", "nominative-accusative:61", "cop-head Nom count / % of cop-heads",
          (1_372, 82.6),
          (cop_heads.get("Nom"), round(100 * (cop_heads.get("Nom") or 0) / tot_cop, 1)
           if tot_cop else None),
          note=f"cop-head case dist: {cop_heads}")
    two_obj = q("""SELECT COUNT(*) FROM (
        SELECT d.sentence_id, d.head FROM token d
        WHERE d.deprel='obj' AND d.feat_case='Acc'
        GROUP BY d.sentence_id, d.head HAVING COUNT(*) >= 2)""")
    check("SE002-4", "nominative-accusative:84", "verbs with two true obj (Acc)",
          36, two_obj)
    naive = q("""SELECT COUNT(*) FROM (
        SELECT d.sentence_id, d.head FROM token d
        JOIN token h ON h.sentence_id=d.sentence_id AND h.idx=d.head AND h.upos='VERB'
        WHERE d.feat_case='Acc'
        GROUP BY d.sentence_id, d.head HAVING COUNT(*) >= 2)""")
    check("SE002-5", "nominative-accusative:84", "naive double-acc (>=2 Acc deps of a verb)",
          2_747, naive)
    core = q("""SELECT COUNT(*) FROM (
        SELECT d.sentence_id, d.head FROM token d
        JOIN token h ON h.sentence_id=d.sentence_id AND h.idx=d.head AND h.upos='VERB'
        WHERE d.feat_case='Acc' AND d.deprel IN ('obj','iobj','xcomp','obl:goal')
        GROUP BY d.sentence_id, d.head HAVING COUNT(*) >= 2)""")
    check("SE002-6", "nominative-accusative:84", "corrected double-acc (core roles) ~872",
          872, core, note="exact deprel set is the article's method choice")

    # ---------- SG-SE-003 instrumental-dative ----------
    check("SE003-1", "instrumental-dative:58", "obl:instr case-tagged total / obl:soc",
          (2_692, 488),
          (q("SELECT COUNT(*) FROM token WHERE deprel='obl:instr' "
             "AND feat_case IS NOT NULL AND feat_case<>''"),
           q("SELECT COUNT(*) FROM token WHERE deprel='obl:soc' "
             "AND feat_case IS NOT NULL AND feat_case<>''")),
          note="SE003 article prints Ins-only 2,569; SE013 prints case-tagged 2,692")
    check("SE003-2", "instrumental-dative:58", "obl:instr that are Ins (article's 2,569)",
          2_569, q("SELECT COUNT(*) FROM token WHERE deprel='obl:instr' AND feat_case='Ins'"))
    ins_pass = q("""SELECT COUNT(*) FROM token i
        JOIN token h ON h.sentence_id=i.sentence_id AND h.idx=i.head
        WHERE i.feat_case='Ins' AND h.feat_voice='Pass'""")
    check("SE003-3", "instrumental-dative:55", "Ins with Pass head (passive-agent proxy)",
          21_472, ins_pass)
    d = dist("SELECT lemma, COUNT(*) FROM token WHERE feat_case='Ins' AND upos='PRON' "
             "GROUP BY lemma ORDER BY COUNT(*) DESC LIMIT 5")
    check("SE003-4", "instrumental-dative:61", "Ins pronouns tad/mad",
          (13_256, 5_605), (d.get("tad"), d.get("mad")))
    forms = dist("SELECT COALESCE(m_unsandhied, form), COUNT(*) FROM token "
                 "WHERE feat_case='Ins' AND upos='NOUN' GROUP BY 1 "
                 "ORDER BY COUNT(*) DESC LIMIT 12")
    check("SE003-5", "instrumental-dative:51", "top Ins noun forms manasā/śareṇa/karmaṇā",
          (1_863, 1_603, 1_471),
          (forms.get("manasā"), forms.get("śareṇa"), forms.get("karmaṇā")),
          note=f"top-12: {sorted(forms.items(), key=lambda x: -x[1])[:6]}")
    forms = dist("SELECT COALESCE(m_unsandhied, form), COUNT(*) FROM token "
                 "WHERE feat_case='Dat' AND upos='NOUN' GROUP BY 1 "
                 "ORDER BY COUNT(*) DESC LIMIT 12")
    check("SE003-6", "instrumental-dative:71", "top Dat noun forms agnaye/devāya/indrāya",
          (1_221, 1_065, 997),
          (forms.get("agnaye"), forms.get("devāya"), forms.get("indrāya")))
    d = dist("SELECT lemma, COUNT(*) FROM token WHERE feat_case='Dat' AND upos='PRON' "
             "GROUP BY lemma")
    check("SE003-7", "instrumental-dative:74", "Dat pronouns mad/tvad",
          (5_834, 5_215), (d.get("mad"), d.get("tvad")))

    # ---------- SG-SE-004 ablative-genitive ----------
    abl_sg = q("SELECT COUNT(*) FROM token WHERE feat_case='Abl' AND feat_number='Sing'")
    check("SE004-1", "ablative-genitive:53", "Abl singular %",
          92, round(100 * abl_sg / 74_565))
    d = dist("SELECT lemma, COUNT(*) FROM token WHERE feat_case='Abl' AND upos='NOUN' "
             "GROUP BY lemma ORDER BY COUNT(*) DESC LIMIT 10")
    check("SE004-2", "ablative-genitive:58+61", "Abl lemmas bhaya/hetu/tva [C4]",
          (747, 458, 3_429), (d.get("bhaya"), d.get("hetu"), d.get("tva")),
          note="tva is the C4 segmentation-artifact 'lemma', excluded by the article")
    gen_pron = q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND upos='PRON'")
    check("SE004-3", "ablative-genitive:69", "Gen pronoun share ~33%",
          33, round(100 * gen_pron / 270_763))
    check("SE004-4", "ablative-genitive:69/73/75", "Gen deprel nmod/iobj/obl:benef/obj",
          (6_696, 86, 188, 333),
          (q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND deprel='nmod'"),
           q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND deprel='iobj'"),
           q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND deprel='obl:benef'"),
           q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND deprel='obj'")))
    gp = q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND feat_verbform='Part'")
    lp = q("SELECT COUNT(*) FROM token WHERE feat_case='Loc' AND feat_verbform='Part'")
    check("SE004-5", "ablative-genitive:85 + locative:45", "Gen+Part / Loc+Part candidates",
          (16_493, 20_973), (gp, lp))
    gadv = q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND feat_verbform='Part' "
             "AND deprel LIKE 'advcl%'")
    gacl = q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND feat_verbform='Part' "
             "AND (deprel LIKE 'acl%' OR deprel='nmod')")
    check("SE004-6", "ablative-genitive:86", "Gen+Part advcl* / acl*+nmod",
          (40, 334), (gadv, gacl))
    drs = q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND feat_verbform='Part' "
            "AND lemma='dṛś'")
    drs_adv = q("SELECT COUNT(*) FROM token WHERE feat_case='Gen' AND feat_verbform='Part' "
                "AND lemma='dṛś' AND deprel LIKE 'advcl%'")
    check("SE004-7", "ablative-genitive:101", "paśyataḥ idiom: dṛś Gen+Part / advcl-tagged",
          (373, 1), (drs, drs_adv))

    # ---------- SG-SE-005 locative ----------
    d = dist("SELECT feat_number, COUNT(*) FROM token WHERE feat_case='Loc' GROUP BY feat_number")
    check("SE005-1", "locative:54", "Loc number Sing/Plur/Dual",
          (204_735, 35_656, 2_824), (d.get("Sing"), d.get("Plur"), d.get("Dual")))
    lp_sing = q("SELECT COUNT(*) FROM token WHERE feat_case='Loc' AND feat_verbform='Part' "
                "AND feat_number='Sing'")
    lp_pass = q("SELECT COUNT(*) FROM token WHERE feat_case='Loc' AND feat_verbform='Part' "
                "AND feat_voice='Pass'")
    check("SE005-2", "locative:71", "Loc+Part singular / natively-passive",
          (18_165, 1_091), (lp_sing, lp_pass))
    d = dist("SELECT lemma, COUNT(*) FROM token WHERE feat_case='Loc' AND feat_verbform='Part' "
             "GROUP BY lemma ORDER BY COUNT(*) DESC LIMIT 12")
    check("SE005-3", "locative:77", "Loc+Part top lemmas gam/as/vac/kṛ",
          (910, 830, 662, 637), (d.get("gam"), d.get("as"), d.get("vac"), d.get("kṛ")))
    lp_parsed = q("SELECT COUNT(*) FROM token WHERE feat_case='Loc' AND feat_verbform='Part' "
                  "AND deprel IS NOT NULL AND deprel<>''")
    lp_advcl = q("SELECT COUNT(*) FROM token WHERE feat_case='Loc' AND feat_verbform='Part' "
                 "AND deprel IN ('advcl','advcl:temp','advcl:cond')")
    lp_acl = q("SELECT COUNT(*) FROM token WHERE feat_case='Loc' AND feat_verbform='Part' "
               "AND deprel LIKE 'acl%'")
    lp_obl = q("SELECT COUNT(*) FROM token WHERE feat_case='Loc' AND feat_verbform='Part' "
               "AND deprel LIKE 'obl%'")
    check("SE005-4", "locative:88", "Loc+Part parsed / advcl-set / acl / obl",
          (557, 367, 35, 48), (lp_parsed, lp_advcl, lp_acl, lp_obl))
    texts = dist("""SELECT x.name, COUNT(*) FROM token t
        JOIN sentence se ON se.id=t.sentence_id
        JOIN chapter c ON c.chapter_id=se.chapter_id
        JOIN text x ON x.text_id=c.text_id
        WHERE t.feat_case='Loc' AND t.feat_verbform='Part'
        GROUP BY x.name ORDER BY COUNT(*) DESC LIMIT 8""")
    check("SE005-5", "locative:79", "Loc-abs candidate by text: MBh / Suśruta / Rām",
          (3_925, 832, 825),
          (next((v for k, v in texts.items() if "Mahābhārata" in k), None),
           next((v for k, v in texts.items() if "Suśruta" in k), None),
           next((v for k, v in texts.items() if "Rāmāyaṇa" in k), None)),
          note=f"top texts: {list(texts.items())[:6]}")

    # ---------- SG-SE-008 imperative-optative ----------
    for cid, mood, exp in (
            ("SE008-1", "Imp", (56_506, 38_144, 17_373, 989, 44_051)),
            ("SE008-2", "Opt", (91_912, 981, 86_918, 4_013, 85_274))):
        tot = q(f"SELECT COUNT(*) FROM token WHERE {FIN} AND feat_mood=?", mood)
        p = dist(f"SELECT feat_person, COUNT(*) FROM token WHERE {FIN} AND feat_mood=? "
                 "GROUP BY feat_person", mood)
        sing = q(f"SELECT COUNT(*) FROM token WHERE {FIN} AND feat_mood=? "
                 "AND feat_number='Sing'", mood)
        check(cid, "imperative-optative:40+51", f"{mood}: total/2nd/3rd/1st/Sing",
              exp, (tot, p.get("2"), p.get("3"), p.get("1"), sing))
    syat = q("SELECT COUNT(*) FROM token WHERE lemma='as' AND feat_mood='Opt' "
             "AND COALESCE(m_unsandhied, form)='syāt'")
    check("SE008-3", "imperative-optative:63", "syāt (lemma as, Opt)", 9_505, syat)

    # ---------- SG-SE-013 karaka-case ----------
    KMAP = [("kartR-active", ("nsubj", "csubj"), 20_230, "Nom", 97.8),
            ("karman", ("obj",), 16_874, "Acc", 90.5),
            ("karaNa", ("obl:instr",), 2_692, "Ins", 95.4),
            ("apAdAna", ("obl:source",), 981, "Abl", 85.7),
            ("adhikaraNa", ("obl:loc",), 1_720, "Loc", 84.5),
            ("kartR-passive", ("obl:agent",), 408, "Ins", 61.8),
            ("sampradAna-recip", ("iobj",), 2_771, "Dat", 66.4),
            ("sampradAna-goal", ("obl:goal",), 2_336, "Acc", 64.0)]
    for i, (name, deprels, exp_n, exp_case, exp_pct) in enumerate(KMAP, 1):
        ph = ",".join("?" * len(deprels))
        d = dist(f"SELECT feat_case, COUNT(*) FROM token WHERE deprel IN ({ph}) "
                 "AND feat_case IS NOT NULL AND feat_case<>'' GROUP BY feat_case", *deprels)
        tot = sum(d.values())
        pct = round(100 * (d.get(exp_case) or 0) / tot, 1) if tot else None
        check(f"SE013-{i}", "karaka-case:84-88", f"{name}: N / %{exp_case}",
              (exp_n, exp_pct), (tot, pct))
    check("SE013-9", "karaka-case:166", "nsubj:pass rows", 0,
          q("SELECT COUNT(*) FROM token WHERE deprel='nsubj:pass'"))
    check("SE013-10", "karaka-case:166 + passive:48", "Pass-voice verb tokens (all forms)",
          36_701, q("SELECT COUNT(*) FROM token WHERE upos='VERB' AND feat_voice='Pass'"))
    d = dist("""SELECT s.feat_case, COUNT(*) FROM token s
        JOIN token h ON h.sentence_id=s.sentence_id AND h.idx=s.head
        WHERE s.deprel='nsubj' AND h.feat_voice='Pass' GROUP BY s.feat_case""")
    check("SE013-11", "karaka-case:166", "nsubj at Pass head: total / Nom",
          (607, 563), (sum(d.values()), d.get("Nom")))
    check("SE013-12", "karaka-case:173", "kartR (nsubj+csubj) Loc off-diagonal",
          272, q("SELECT COUNT(*) FROM token WHERE deprel IN ('nsubj','csubj') "
                 "AND feat_case='Loc'"))
    check("SE013-13", "karaka-case:88", "obl:benef Dat/Gen split %",
          (47.0, 42.9),
          (lambda dd, tt: (round(100 * (dd.get("Dat") or 0) / tt, 1),
                           round(100 * (dd.get("Gen") or 0) / tt, 1)))(
              dist("SELECT feat_case, COUNT(*) FROM token WHERE deprel='obl:benef' "
                   "AND feat_case IS NOT NULL AND feat_case<>'' GROUP BY feat_case"),
              q("SELECT COUNT(*) FROM token WHERE deprel='obl:benef' "
                "AND feat_case IS NOT NULL AND feat_case<>''")))

    # ---------- SG-MO-016 imperfect ----------
    IMPF = f"{FIN} AND feat_tense='Impf'"
    p = dist(f"SELECT feat_person, COUNT(*) FROM token WHERE {IMPF} GROUP BY feat_person")
    n = dist(f"SELECT feat_number, COUNT(*) FROM token WHERE {IMPF} GROUP BY feat_number")
    v_pass = q(f"SELECT COUNT(*) FROM token WHERE {IMPF} AND feat_voice='Pass'")
    tot = sum(p.values())
    check("MO016-1", "imperfect:66", "Impf person/number/voice profile %",
          (94.1, 3.3, 2.5, 75.1, 22.6, 2.3, 96.9, 3.1),
          (round(100 * p.get("3", 0) / tot, 1), round(100 * p.get("1", 0) / tot, 1),
           round(100 * p.get("2", 0) / tot, 1), round(100 * n.get("Sing", 0) / 46_695, 1),
           round(100 * n.get("Plur", 0) / 46_695, 1), round(100 * n.get("Dual", 0) / 46_695, 1),
           round(100 * (46_695 - v_pass) / 46_695, 1), round(100 * v_pass / 46_695, 1)))
    d = dist(f"SELECT lemma, COUNT(*) FROM token WHERE {IMPF} GROUP BY lemma "
             "ORDER BY COUNT(*) DESC LIMIT 8")
    check("MO016-2", "imperfect:69", "Impf top roots brū/bhū/as/paś/kṛ",
          (5_669, 3_769, 3_032, 1_385, 1_002),
          (d.get("brū"), d.get("bhū"), d.get("as"), d.get("paś"), d.get("kṛ")),
          note=f"top-8: {list(d.items())}")

    # ---------- SG-MO-017/018/019 perfect + aorist [C2] ----------
    PAST = f"{FIN} AND feat_tense='Past'"
    d = dist(f"SELECT COALESCE(feat_formation,'NULL'), COUNT(*) FROM token WHERE {PAST} "
             "GROUP BY 1")
    check("MO017-1", "perfect:77 + aorist:65 + aorist-types:53",
          "Past formation NULL/peri/root/them/s/is/red/sa/sis [C2]",
          (85_955, 4_046, 5_690, 2_781, 1_508, 1_077, 833, 124, 41),
          (d.get("NULL"), d.get("peri"), d.get("root"), d.get("them"), d.get("s"),
           d.get("is") or d.get("iṣ"), d.get("red"), d.get("sa"),
           d.get("sis") or d.get("siṣ")),
          note=f"values present: {sorted(d)}")
    aor = sum(v for k, v in d.items() if k not in ("NULL", "peri"))
    check("MO017-2", "aorist:60 + aorist-types:41", "formation-tagged aorist total [C2]",
          12_054, aor)
    check("MO017-3", "aorist-types:61", "non-sigmatic / sigmatic split [C2]",
          (9_304, 2_750),
          ((d.get("root", 0) + d.get("them", 0) + d.get("red", 0)),
           (d.get("s", 0) + (d.get("is") or d.get("iṣ") or 0) + d.get("sa", 0)
            + (d.get("sis") or d.get("siṣ") or 0))))
    tense_all = dist("SELECT feat_tense, COUNT(*) FROM token WHERE upos='VERB' "
                     "AND feat_tense IS NOT NULL GROUP BY feat_tense")
    check("MO017-4", "perfect:66", "pluperfect-tagged tokens ~200",
          200, sum(v for k, v in tense_all.items() if k in ("Plp", "Plup", "Pqp")),
          note=f"tense values on VERB: {sorted(tense_all)}")
    lem = {}
    for k in list(d):
        if k in ("NULL", "peri"):
            continue
        lem[k] = q(f"SELECT COUNT(DISTINCT lemma) FROM token WHERE {PAST} "
                   "AND feat_formation=?", k)
    check("MO019-1", "aorist-types:53", "aorist lemma counts root/them/red/s/is/sa/sis",
          (210, 175, 150, 216, 170, 37, 14),
          (lem.get("root"), lem.get("them"), lem.get("red"), lem.get("s"),
           lem.get("is") or lem.get("iṣ"), lem.get("sa"), lem.get("sis") or lem.get("siṣ")))
    d2 = dist(f"SELECT lemma, COUNT(*) FROM token WHERE {PAST} AND feat_formation IS NOT NULL "
              "AND feat_formation NOT IN ('peri') GROUP BY lemma ORDER BY COUNT(*) DESC LIMIT 8")
    check("MO018-1", "aorist:78", "tagged-aorist top roots bhū/vac/gam/kṛ/gā/dā",
          (2_360, 837, 664, 452, 312, 255),
          (d2.get("bhū"), d2.get("vac"), d2.get("gam"), d2.get("kṛ"),
           d2.get("gā"), d2.get("dā")))
    aux = dist(f"SELECT lemma, COUNT(*) FROM token WHERE {PAST} AND feat_formation='peri' "
               "GROUP BY lemma ORDER BY COUNT(*) DESC LIMIT 6")
    check("MO017-5", "perfect:118", "peri tokens by lemma: as/kṛ/bhū",
          (3_697, 298, 32), (aux.get("as"), aux.get("kṛ"), aux.get("bhū")),
          note=f"peri lemma dist: {list(aux.items())}")
    pn = dist(f"SELECT feat_person||feat_number, COUNT(*) FROM token WHERE {PAST} "
              "AND feat_formation='peri' GROUP BY 1")
    check("MO017-6", "perfect:121", "peri person-number 3Sing/3Plur/3Dual/1Sing/2Sing",
          (3_503, 466, 68, 8, 1),
          (pn.get("3Sing"), pn.get("3Plur"), pn.get("3Dual"), pn.get("1Sing"), pn.get("2Sing")))

    # ---------- SG-MO-021 future ----------
    FUT = f"{FIN} AND feat_tense='Fut'"
    p = dist(f"SELECT feat_person, COUNT(*) FROM token WHERE {FUT} GROUP BY feat_person")
    tot = sum(p.values())
    check("MO021-1", "future:68", "Fut person % 3rd/1st/2nd",
          (51.6, 36.4, 12.0),
          (round(100 * p.get("3", 0) / tot, 1), round(100 * p.get("1", 0) / tot, 1),
           round(100 * p.get("2", 0) / tot, 1)))
    f = dist(f"SELECT COALESCE(feat_formation,'simple'), COUNT(*) FROM token WHERE {FUT} "
             "GROUP BY 1")
    check("MO021-2", "future:80", "Fut simple / periphrastic",
          (20_216, 1_340), (f.get("simple"), f.get("peri")),
          note=f"formation on Fut: {sorted(f.items())}")
    forms = dist(f"SELECT COALESCE(m_unsandhied, form), COUNT(*) FROM token WHERE {FUT} "
                 "GROUP BY 1 ORDER BY COUNT(*) DESC LIMIT 8")
    check("MO021-3", "future:73", "top Fut forms bhaviṣyati/vakṣyāmi/pravakṣyāmi",
          (2_013, 579, 532),
          (forms.get("bhaviṣyati"), forms.get("vakṣyāmi"), forms.get("pravakṣyāmi")),
          note=f"top-8: {list(forms.items())}")
    peri_forms = dist(f"SELECT COALESCE(m_unsandhied, form), COUNT(*) FROM token WHERE {FUT} "
                      "AND feat_formation='peri' GROUP BY 1 ORDER BY COUNT(*) DESC LIMIT 4")
    check("MO021-4", "future:80", "top periphrastic-future forms bhavitā/kartā",
          (332, 55), (peri_forms.get("bhavitā"), peri_forms.get("kartā")),
          note=f"top-4: {list(peri_forms.items())}")
    check("MO021-5", "future:91", "conditional (feat_mood=Cond) total", 340,
          q("SELECT COUNT(*) FROM token WHERE feat_mood='Cond'"))
    check("MO021-6", "future:47", "future participles (Part & Fut)", 1_575,
          q("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense='Fut'"))

    # ---------- SG-WF-002 krt-overview + SG-MO-022..026 nonfinite quartet ----------
    vf = dist("SELECT feat_verbform, COUNT(*) FROM token WHERE feat_verbform IN "
              "('Part','Conv','Gdv','Inf') GROUP BY feat_verbform")
    quartet = sum(vf.values())
    check("WF002-1", "krt-overview:47+60", "quartet total / Part / Conv / Gdv / Inf",
          (483_623, 341_556, 102_054, 28_260, 11_753),
          (quartet, vf.get("Part"), vf.get("Conv"), vf.get("Gdv"), vf.get("Inf")))
    check("WF002-2", "krt-overview:47", "quartet leakage onto non-VERB", 0,
          q("SELECT COUNT(*) FROM token WHERE feat_verbform IN ('Part','Conv','Gdv','Inf') "
            "AND upos<>'VERB'"))
    tnull = q("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense IS NULL")
    check("WF002-3", "krt-overview:66 + ta-na-participles:48", "tense-NULL participles",
          266_660, tnull)
    check("WF002-4", "krt-overview:73 [C3]", "surface tokens -ana / -ti / -tṛ(IAST)",
          (95_263, 74_927, 31_042),
          (q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE '%ana'"),
           q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE '%ti'"),
           q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') AND lemma LIKE '%tṛ'")))
    check("WF003-1", "krt-suffixes:60 [C3]", "lemma counts -ana / -ti / -in",
          (3_438, 1_886, 2_926),
          (q("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ') "
             "AND lemma LIKE '%ana'"),
           q("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ') "
             "AND lemma LIKE '%ti'"),
           q("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ') "
             "AND lemma LIKE '%in'")))
    check("WF003-2", "krt-suffixes:60 — THE -tṛ ENCODING TRAP [C3]",
          "lemmas ending SLP1 'tf' (published: 0 => 'DCS never lemmatises -tṛ') "
          "vs IAST 'tṛ' reality",
          (0, 0),
          (q("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ') "
             "AND lemma LIKE '%tf'"),
           q("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN ('NOUN','ADJ') "
             "AND lemma LIKE '%tṛ'")),
          note="expected (0,0) states the PUBLISHED claim; second derived value is the "
               "IAST truth — a nonzero second element REFUTES the published scoping claim")

    # ---------- SG-MO-022 participles ----------
    check("MO022-1", "present-perfect-participles:60+65", "Pres Part total / Pass / None-voice",
          (64_209, 7_002, 57_207),
          (q("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense='Pres'"),
           q("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense='Pres' "
             "AND feat_voice='Pass'"),
           q("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense='Pres' "
             "AND feat_voice IS NULL")))
    d = dist("SELECT lemma, COUNT(*) FROM token WHERE feat_verbform='Part' "
             "AND feat_tense='Pres' GROUP BY lemma ORDER BY COUNT(*) DESC LIMIT 8")
    check("MO022-2", "present-perfect-participles:68", "top Pres-Part lemmas as/yaj/kṛ",
          (3_430, 2_783, 1_384), (d.get("as"), d.get("yaj"), d.get("kṛ")))
    past_part = q("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense='Past'")
    check("MO022-3", "present-perfect-participles:80", "Past+Part bucket", 9_112, past_part)
    vid = q("SELECT COUNT(*) FROM token WHERE feat_verbform='Part' AND feat_tense='Past' "
            "AND lemma='vid'")
    check("MO022-4", "present-perfect-participles:82", "vid in Past+Part (-vas leader)",
          1_279, vid)

    # ---------- SG-MO-024/025/026 gerundive, infinitive, absolutive ----------
    d = dist("SELECT lemma, COUNT(*) FROM token WHERE feat_verbform='Gdv' GROUP BY lemma "
             "ORDER BY COUNT(*) DESC LIMIT 6")
    check("MO024-1", "gerundive:61", "top Gdv lemmas kṛ/jñā/dā/grah/vijñā",
          (3_576, 1_427, 1_319, 694, 683),
          (d.get("kṛ"), d.get("jñā"), d.get("dā"), d.get("grah"), d.get("vijñā")))
    gdv_split = {"tavya": 0, "anīya": 0, "ya": 0, "amb": 0}
    for (m,), cnt in [((r[0],), r[1]) for r in cur.execute(
            "SELECT COALESCE(m_unsandhied, form), COUNT(*) FROM token "
            "WHERE feat_verbform='Gdv' GROUP BY 1")]:
        w = (m or "").rstrip("ḥmṃdt").lower()
        stem = m or ""
        if "tavy" in stem:
            gdv_split["tavya"] += cnt
        elif "anīy" in stem:
            gdv_split["anīya"] += cnt
        elif "y" in stem[-4:]:
            gdv_split["ya"] += cnt
        else:
            gdv_split["amb"] += cnt
    check("MO024-2", "gerundive:54", "Gdv suffix split -ya/-tavya/-anīya (approx surface)",
          (19_901, 5_740, 1_280),
          (gdv_split["ya"], gdv_split["tavya"], gdv_split["anīya"]),
          note=f"my crude classifier; ambiguous bucket {gdv_split['amb']} "
               "(article: 1,339) — treat near-match as method-consistent")
    d = dist("SELECT lemma, COUNT(*) FROM token WHERE feat_verbform='Inf' GROUP BY lemma "
             "ORDER BY COUNT(*) DESC LIMIT 6")
    check("MO025-1", "infinitive:69", "top Inf lemmas kṛ/dṛś/vac/śru/gam",
          (906, 628, 613, 522, 360),
          (d.get("kṛ"), d.get("dṛś"), d.get("vac"), d.get("śru"), d.get("gam")))
    inf = {"tum": 0, "tave": 0, "toḥ": 0, "dhyai": 0, "other": 0}
    for m, cnt in cur.execute("SELECT COALESCE(m_unsandhied, form), COUNT(*) FROM token "
                              "WHERE feat_verbform='Inf' GROUP BY 1"):
        s = m or ""
        if s.endswith("tum"):
            inf["tum"] += cnt
        elif s.endswith("tave") or s.endswith("tavai"):
            inf["tave"] += cnt
        elif s.endswith("toḥ") or s.endswith("tos"):
            inf["toḥ"] += cnt
        elif s.endswith("dhyai"):
            inf["dhyai"] += cnt
        else:
            inf["other"] += cnt
    check("MO025-2", "infinitive:56+66", "Inf split -tum/-tave/-toḥ/-dhyai",
          (9_681, 320, 154, 97), (inf["tum"], inf["tave"], inf["toḥ"], inf["dhyai"]),
          note=f"other bucket {inf['other']} (article 'прочее' 1,339; Vedic residue 571)")
    ab = {"tvā": 0, "ya": 0, "am": 0, "other": 0}
    ab_pv = {("tvā", False): 0, ("tvā", True): 0, ("ya", False): 0, ("ya", True): 0}
    for m, pv, cnt in cur.execute(
            "SELECT COALESCE(t.m_unsandhied, t.form), COALESCE(l.preverbs,''), COUNT(*) "
            "FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
            "WHERE t.feat_verbform='Conv' GROUP BY 1, 2"):
        s = m or ""
        has_pv = pv != ""
        if s.endswith("tvā"):
            ab["tvā"] += cnt
            ab_pv[("tvā", has_pv)] += cnt
        elif s.endswith("tya") or s.endswith("ya"):
            ab["ya"] += cnt
            ab_pv[("ya", has_pv)] += cnt
        elif s.endswith("am"):
            ab["am"] += cnt
        else:
            ab["other"] += cnt
    check("MO026-1", "absolutive:61", "Conv split -ya(-tya)/-tvā/other/-am",
          (57_790, 34_816, 8_980, 468), (ab["ya"], ab["tvā"], ab["other"], ab["am"]))
    check("MO026-2", "absolutive:71", "allomorphy cross-tab tvā-nopv/tvā-pv/ya-nopv/ya-pv",
          (34_293, 523, 1_289, 56_501),
          (ab_pv[("tvā", False)], ab_pv[("tvā", True)],
           ab_pv[("ya", False)], ab_pv[("ya", True)]))

    # ---------- SG-MO-028 causative [C1] ----------
    c10 = q(f"SELECT COUNT(*) FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
            f"WHERE {FIN.replace('upos', 't.upos').replace('feat_', 't.feat_')} AND {CLASS10}")
    c10lem = q(f"SELECT COUNT(DISTINCT t.lemma_id) FROM token t "
               f"JOIN lemma l ON l.lemma_id=t.lemma_id "
               f"WHERE {FIN.replace('upos', 't.upos').replace('feat_', 't.feat_')} AND {CLASS10}")
    check("MO028-1", "causative:44 [C1]", "class-10 bucket finite tokens / lemma types",
          (55_376, 2_006), (c10, c10lem))
    den = q(f"SELECT COUNT(*) FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
            f"WHERE {FIN.replace('upos', 't.upos').replace('feat_', 't.feat_')} "
            f"AND l.grammar LIKE 'Denom%'")
    check("MO028-2", "causative:47 [C1]", "denominative finite tokens", 5_451, den)
    d = dist(f"SELECT t.lemma, COUNT(*) FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
             f"WHERE {FIN.replace('upos', 't.upos').replace('feat_', 't.feat_')} AND {CLASS10} "
             "GROUP BY t.lemma ORDER BY COUNT(*) DESC LIMIT 8")
    check("MO028-3", "causative:64 [C1]", "top class-10 lemmas kathay/dhāray/kāray/pūjay",
          (2_083, 1_337, 1_327, 1_249),
          (d.get("kathay"), d.get("dhāray"), d.get("kāray"), d.get("pūjay")),
          note=f"top-8: {list(d.items())}")

    # ---------- SG-MO-013 thematic-present [C1] ----------
    PRES = f"{FIN} AND feat_tense='Pres'"
    check("MO013-1", "thematic-present:46", "finite Pres tokens / distinct lemma_ids",
          (353_215, 7_186),
          (q(f"SELECT COUNT(*) FROM token WHERE {PRES}"),
           q(f"SELECT COUNT(DISTINCT lemma_id) FROM token WHERE {PRES}")))

    # ---------- SG-MO-010 pronouns ----------
    check("MO010-1", "pronouns:55", "PRON tokens / distinct lemmas",
          (544_999, 38),
          (q("SELECT COUNT(*) FROM token WHERE upos='PRON'"),
           q("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos='PRON'")))
    prow = []
    for lemma_, exp_tok, exp_cells in (("tad", 184_809, 21), ("yad", 61_421, 21),
                                       ("mad", 60_575, 21), ("idam", 52_461, 22),
                                       ("tvad", 49_725, 21), ("etad", 40_991, 21),
                                       ("sarva", 22_865, 18), ("ka", 14_087, 18)):
        tok = q("SELECT COUNT(*) FROM token WHERE upos='PRON' AND lemma=?", lemma_)
        cells_ = q("SELECT COUNT(DISTINCT feat_case||'/'||feat_number) FROM token "
                   "WHERE upos='PRON' AND lemma=? AND feat_case IS NOT NULL "
                   "AND feat_case<>'' AND feat_case<>'Cpd' AND feat_number IS NOT NULL",
                   lemma_)
        prow.append((lemma_, exp_tok == tok and exp_cells == cells_, tok, cells_))
    check("MO010-2", "pronouns:73", "top-8 pronoun tokens+cells all match",
          True, all(x[1] for x in prow), note=f"{prow}")

    # ---------- SG-MO-002 a-stems (universe only; cells via emitted data) ----------
    for cid, g, exp_lem, exp_tok in (("MO002-1", "Masc", 21_837, 716_864),
                                     ("MO002-2", "Neut", 13_857, 359_194)):
        lemc = q("SELECT COUNT(DISTINCT lemma) FROM token WHERE upos='NOUN' "
                 "AND feat_gender=? AND feat_case IS NOT NULL AND feat_case<>'' "
                 "AND feat_case<>'Cpd' AND lemma LIKE '%a' AND lemma NOT LIKE '%ā'", g)
        tokc = q("SELECT COUNT(*) FROM token WHERE upos='NOUN' "
                 "AND feat_gender=? AND feat_case IS NOT NULL AND feat_case<>'' "
                 "AND feat_case<>'Cpd' AND lemma LIKE '%a' AND lemma NOT LIKE '%ā'", g)
        check(cid, "a-stems:54", f"-a stems {g}: lemmas/tokens (approx universe, "
              "no dictionary-gender whitelist)", (exp_lem, exp_tok), (lemc, tokc),
              note="script additionally filters by lemma.grammar gender whitelist; "
                   "near-match = universe reproduced, exact match needs whitelist")
    for cid, lemma_, exp_tok, exp_cells in (("MO002-3", "putra", 9_729, 23),
                                            ("MO002-4", "deva", 17_536, 22),
                                            ("MO002-5", "netra", 385, 22),
                                            ("MO002-6", "phala", 3_973, 17)):
        tok = q("SELECT COUNT(*) FROM token WHERE upos='NOUN' AND lemma=? "
                "AND feat_case IS NOT NULL AND feat_case<>'' AND feat_case<>'Cpd'", lemma_)
        cells_ = q("SELECT COUNT(DISTINCT feat_case||'/'||feat_number) FROM token "
                   "WHERE upos='NOUN' AND lemma=? AND feat_case IS NOT NULL "
                   "AND feat_case<>'' AND feat_case<>'Cpd' AND feat_number IS NOT NULL",
                   lemma_)
        check(cid, "a-stems:67+118", f"{lemma_}: tokens / attested cells",
              (exp_tok, exp_cells), (tok, cells_))
    check("MO002-7", "a-stems:185 [C4]", "tva as neuter 'lemma' token count",
          9_972, q("SELECT COUNT(*) FROM token WHERE upos='NOUN' AND lemma='tva' "
                   "AND feat_gender='Neut' AND feat_case IS NOT NULL AND feat_case<>'' "
                   "AND feat_case<>'Cpd'"))

    # ---------- SG-WF-004 taddhita [C4] ----------
    check("WF004-1", "taddhita-overview:55", "NOUN+ADJ universe / NOUN / ADJ",
          (2_996_410, 2_395_188, 601_222),
          (q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ')"),
           q("SELECT COUNT(*) FROM token WHERE upos='NOUN'"),
           q("SELECT COUNT(*) FROM token WHERE upos='ADJ'")))
    seg = {}
    for name, lid in (("tva", 163_754), ("tā", 203_679), ("maya", 109_021), ("vat", 167_498)):
        seg[name] = q("SELECT COUNT(*) FROM token WHERE lemma_id=?", lid)
    check("WF004-2", "taddhita-overview:77+80 [C4]",
          "segmentation-suffix tokens tva/tā/vat/maya + total",
          (10_850, 5_919, 4_125, 3_214, 24_108),
          (seg["tva"], seg["tā"], seg["vat"], seg["maya"], sum(seg.values())))
    base_ok = q("""SELECT COUNT(*) FROM token s
        JOIN token b ON b.sentence_id=s.sentence_id AND b.idx=s.idx-1
        WHERE s.lemma_id IN (163754, 203679, 109021, 167498)""")
    check("WF004-3", "taddhita-overview:77 [C4]", "base recoverable at idx-1 %",
          99.8, round(100 * base_ok / sum(seg.values()), 1))
    bpos = dist("""SELECT b.upos, COUNT(*) FROM token s
        JOIN token b ON b.sentence_id=s.sentence_id AND b.idx=s.idx-1
        WHERE s.lemma_id=163754 GROUP BY b.upos""")
    check("WF004-4", "taddhita-overview:86 [C4]", "-tva base POS ADJ/NOUN/VERB",
          (4_876, 4_441, 1_107), (bpos.get("ADJ"), bpos.get("NOUN"), bpos.get("VERB")),
          note=f"full base-POS dist: {sorted(bpos.items(), key=lambda x: -x[1])}")
    check("WF004-5", "taddhita-overview:157 [C3]", "-ya surface selection tokens",
          224_191, q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') "
                     "AND lemma LIKE '%ya'"))
    bhag = q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') "
             "AND lemma='bhagavat'")
    vant = q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') "
             "AND (lemma LIKE '%vat' OR lemma LIKE '%vant')")
    mant = q("SELECT COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') "
             "AND (lemma LIKE '%mat' OR lemma LIKE '%mant')")
    check("WF004-6", "taddhita-overview:195", "possessive -vant (bhagavant) / -mant "
          "(surface variants tried)", (7_100, 5_188, 1_272), (vant, bhag, mant),
          note="lemmatisation form (-vat vs -vant) is the method variable here")

    # ---------- SG-WF-006/008 compounds [C5] ----------
    cpd_sent_raw = q("SELECT COUNT(DISTINCT sentence_id) FROM token WHERE feat_case='Cpd'")
    check("WF006-1", "P4-design:22 vs tatpurusha:53", "sentences with >=1 Cpd token (raw)",
          396_571, cpd_sent_raw,
          note="the P4 design doc's 396,571; the articles' 396,305 counts only sentences "
               "with a WELL-FORMED reconstructed compound (dangling runs skipped)")
    print("  ... reconstructing compounds (single pass over 5.7M tokens) ...")
    hist = {}
    total_c = 0
    sents_with = 0
    cur2 = con.cursor()
    last_sent = None
    seq = []

    def flush(seq_):
        nonlocal total_c, sents_with
        had = False
        i = 0
        n = len(seq_)
        while i < n:
            if seq_[i][1] == "Cpd" and (i == 0 or seq_[i - 1][1] != "Cpd"
                                        or seq_[i - 1][0] != seq_[i][0] - 1):
                run = 1
                j = i + 1
                while j < n and seq_[j][1] == "Cpd" and seq_[j][0] == seq_[j - 1][0] + 1:
                    run += 1
                    j += 1
                if j < n and seq_[j][0] == seq_[j - 1][0] + 1:
                    total_c += 1
                    members = run + 1
                    hist[members] = hist.get(members, 0) + 1
                    had = True
                i = j
            else:
                i += 1
        if had:
            sents_with += 1

    for sid, idx, case in cur2.execute(
            "SELECT sentence_id, idx, COALESCE(feat_case,'') FROM token "
            "ORDER BY sentence_id, idx"):
        if sid != last_sent:
            if last_sent is not None:
                flush(seq)
            seq = []
            last_sent = sid
        seq.append((idx, "Cpd" if case == "Cpd" else ("" if case == "" else "infl")))
    if seq:
        flush(seq)
    two = hist.get(2, 0)
    three = hist.get(3, 0)
    four = hist.get(4, 0)
    five_plus = sum(v for k, v in hist.items() if k >= 5)
    check("WF006-2", "compounds-overview:51+59", "reconstructed compounds / sentences-with",
          (595_021, 396_305), (total_c, sents_with))
    check("WF006-3", "compounds-overview:65", "member histogram 2/3/4/5+",
          (442_649, 104_460, 28_372, 19_540), (two, three, four, five_plus))
    check("WF006-4", "tatpurusha:53", "two-member / multi-member",
          (442_649, 152_372), (two, total_c - two))
    coord = q("SELECT COUNT(*) FROM token WHERE deprel='compound:coord'")
    cname = q("SELECT COUNT(*) FROM token WHERE deprel='compound:name'")
    cgen = q("SELECT COUNT(*) FROM token WHERE deprel='compound'")
    check("WF006-5", "compounds-overview:73 [C5]", "compound:coord / :name / generic",
          (2_044, 51, 119), (coord, cname, cgen))
    check("WF008-1", "tatpurusha:70 [C5]",
          "the '2,214 compound:coord' claim = coord+name+generic sum, not coord alone",
          2_214, coord + cname + cgen,
          note="published label says compound:coord covers 2,214; true coord alone is "
               f"{coord}; 2,214 is the sum of all three compound deprels")

    # ---------- SG-WF-011 preverbs ----------
    UP = ["adhi", "anu", "antar", "apa", "api", "abhi", "ava", "ā", "ut", "upa",
          "ni", "niḥ", "nis", "parā", "pari", "pra", "prati", "vi", "sam", "su",
          "dus", "acchā"]
    UP.sort(key=len, reverse=True)

    def first_up(pv):
        for u in UP:
            if pv.startswith(u):
                return u
        return "(other)"

    WITH = ("FROM token t JOIN lemma l ON l.lemma_id=t.lemma_id "
            "WHERE t.upos='VERB' AND l.preverbs IS NOT NULL AND l.preverbs != ''")
    pv_total = q(f"SELECT COUNT(*) {WITH}")
    check("WF011-1", "preverbs:41", "preverbed verb tokens / % of verbs / lemmas",
          (369_870, 36.7, 10_017),
          (pv_total, round(100 * pv_total / 1_007_361, 1),
           q("SELECT COUNT(*) FROM lemma WHERE preverbs IS NOT NULL AND preverbs != ''")))
    lead = {}
    multi = 0
    for pv, c in cur.execute(f"SELECT l.preverbs, COUNT(*) c {WITH} GROUP BY l.preverbs"):
        u = first_up(pv)
        lead[u] = lead.get(u, 0) + c
        rest = pv[len(u):] if u != "(other)" else ""
        if rest and first_up(rest) != "(other)":
            multi += c
    check("WF011-2", "preverbs:54 — the ut cell", "leading-upasarga ut (published 17,275)",
          17_275, lead.get("ut"),
          note="published table is leading-upasarga fold everywhere else; ut cell was "
               "copied from the exact-string column (17,275); fold value is "
               f"{lead.get('ut')}")
    check("WF011-3", "preverbs:54", "leading-upasarga pra/ā/sam/vi/upa/ni/abhi",
          (58_118, 48_139, 47_613, 40_856, 22_195, 20_423, 17_824),
          tuple(lead.get(u) for u in ("pra", "ā", "sam", "vi", "upa", "ni", "abhi")))
    check("WF011-4", "preverbs:67+111", "multi-preverb tokens / (other) bucket",
          (25_906, 28_956), (multi, lead.get("(other)")))

    # ---------- summary ----------
    n_ok = sum(1 for r in results if r["match"])
    print(f"\n=== {n_ok}/{len(results)} checks matched exactly ===")
    OUT.write_text(json.dumps({"pin": prov.get("source_commit"),
                               "checks": results}, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8")
    print(f"written: {OUT}")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
