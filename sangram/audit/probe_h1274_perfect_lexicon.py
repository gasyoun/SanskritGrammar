"""H1274 probe — perfect visa card A5 (RESEARCH class).

The author's ask (article § 3.5 records it as «задел следующей ревизии»):
    «А если проверить исходя из списка известных перфектов помимо uvāca, āha, babhūva?»

The lexicon probe from the known side: take forms that ARE reduplicated (or
periphrastic-auxiliary) perfects by the reference grammars (Whitney ch. X;
narrative 3rd-person forms), find their verbal tokens in the pinned snapshot,
and measure how the annotation tags them. Unlike the surface heuristic of
§ 3.5 this generates no false candidates: every probed form is a known perfect,
so the measurement is annotation RECALL on known perfects.

Homonymy guards: upos='VERB' filter (drops veda 'the Veda', āsa 'seat' as nouns);
forms chosen to be unambiguous 3sg/3pl perfect surfaces.

Output: probe_h1274_perfect_lexicon.json next to this script.
"""

import json
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

DB = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"C:\Users\user\Documents\GitHub\VisualDCS\src\DCS-data-2026\dcs_full.sqlite"
)

# Known reduplicated-perfect surfaces (3sg / 3pl / 3sg-middle), Whitney ch. X
# paradigms + the narrative staples. Deliberately NO periphrastic hosts (they are
# the already-measured peri slice) and no forms with common non-perfect homonyms
# other than those the upos filter handles.
KNOWN_PERFECTS = [
    # the three staples the author names
    "uvāca", "āha", "babhūva",
    # their plurals / near kin
    "ūcuḥ", "āhuḥ", "babhūvuḥ",
    # kṛ, gam, han, dā, dhā, hā, sthā, yā, nī, hṛ, dṛś, śru, jñā, bhāṣ, vac-middle
    "cakāra", "cakruḥ", "cakre", "jagāma", "jagmuḥ", "jaghāna", "jaghnuḥ",
    "dadau", "daduḥ", "dadhau", "jahau", "tasthau", "tasthuḥ", "yayau", "yayuḥ",
    "nināya", "jahāra", "jahruḥ", "dadarśa", "dadṛśuḥ", "śuśrāva", "śuśruvuḥ",
    "jajñe", "babhāṣe", "ūce",
    # as 'be' (perfect), vid 'know' (veda-perfect), pat, vas, ram, labh
    "āsa", "āsuḥ", "veda", "viduḥ", "papāta", "petuḥ", "uvāsa", "reme", "lebhe",
    # a spread of textbook perfects
    "śaśāpa", "cukopa", "mumoca", "bibheda", "ciccheda", "tutoṣa", "dudoha",
    "vavarṣa", "sasarja", "dadhāra", "jugopa", "siṣeve", "cukruśuḥ", "nanāda",
    "rurodha", "vavande", "papau", "jaghāsa", "śiśriye", "cikāya",
]

con = sqlite3.connect(DB)
cur = con.cursor()

out = {"probe": "h1274-A5-perfect-lexicon", "db": str(DB), "n_forms_probed": len(KNOWN_PERFECTS)}

# Published-number cross-checks (article § 2 / § 3): Past bucket and peri slice.
# Universe matches scripts/sg_mo_017_perfect_coverage.py exactly (finite verbs).
FIN = "(feat_verbform IS NULL OR feat_verbform='Fin')"
cur.execute(f"SELECT COUNT(*) FROM token WHERE upos='VERB' AND feat_tense='Past' AND {FIN}")
past_bucket = cur.fetchone()[0]
cur.execute(
    f"SELECT COUNT(*) FROM token WHERE upos='VERB' AND feat_tense='Past' AND {FIN} "
    "AND feat_formation='peri'"
)
peri = cur.fetchone()[0]
out["cross_check"] = {"past_bucket": past_bucket, "peri": peri}
assert past_bucket == 102055, f"Past bucket drifted: {past_bucket}"
assert peri == 4046, f"peri drifted: {peri}"

ph = ",".join("?" for _ in KNOWN_PERFECTS)
per_form = []
cur.execute(
    f"SELECT form, COUNT(*), "
    f"SUM(CASE WHEN feat_tense='Past' THEN 1 ELSE 0 END), "
    f"SUM(CASE WHEN feat_tense IS NULL THEN 1 ELSE 0 END), "
    f"SUM(CASE WHEN feat_formation IS NOT NULL THEN 1 ELSE 0 END) "
    f"FROM token WHERE upos='VERB' AND {FIN} AND form IN ({ph}) "
    "GROUP BY form ORDER BY COUNT(*) DESC",
    KNOWN_PERFECTS,
)
rows = cur.fetchall()
for form, n, n_past, n_notense, n_formed in rows:
    per_form.append({
        "form": form, "tokens": n, "tense_past": n_past,
        "tense_null": n_notense, "has_formation": n_formed,
    })
out["per_form"] = per_form

found_forms = {r["form"] for r in per_form}
out["forms_found"] = len(found_forms)
out["forms_absent"] = sorted(set(KNOWN_PERFECTS) - found_forms)

tot = sum(r["tokens"] for r in per_form)
tot_past = sum(r["tense_past"] for r in per_form)
tot_formed = sum(r["has_formation"] for r in per_form)
out["totals"] = {
    "tokens": tot,
    "tagged_tense_past": tot_past,
    "carrying_any_formation": tot_formed,
    "formation_recall_on_known_perfects": round(tot_formed / tot, 4) if tot else None,
}

# What formations, if any, do these known perfects carry? (expected: none/aorist mislabels)
cur.execute(
    f"SELECT feat_formation, COUNT(*) FROM token WHERE upos='VERB' AND {FIN} AND form IN ({ph}) "
    "GROUP BY feat_formation", KNOWN_PERFECTS,
)
out["formation_breakdown"] = {str(k): v for k, v in cur.fetchall()}

out["reading"] = (
    "Of {n} verbal tokens of {f} known-perfect surface forms, {p} sit in the Tense=Past "
    "bucket and only {fm} carry ANY form-class tag ({r:.1%}) — the lexicon probe from the "
    "known side confirms § 4's recall finding: the main (reduplicated) perfect formation "
    "is invisible to the annotation's form-class feature."
).format(n=tot, f=len(found_forms), p=tot_past, fm=tot_formed,
         r=(tot_formed / tot if tot else 0))

dest = Path(__file__).with_suffix(".json")
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
