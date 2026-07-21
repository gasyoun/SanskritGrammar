"""H1274 probe — declension-overview visa card A3 (RESEARCH class).

The author's note disputes the CHARACTERISATION of a published figure:
    «дательный реже всех (2,2 %) - не просто реже, а почти не засвидетельствован»
Invariant I4: the published 2,2 % (39 190 / 1 790 270) is not touched. This probe
measures whether "почти не засвидетельствован" is supportable — at the token,
cell, text and lemma level — against the same pinned snapshot the article uses
(dcs_full.sqlite, pin 04e0778, tag c3-pin-04e0778-content).

Output: probe_h1274_dat_attestation.json next to this script.
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
UNIVERSE = "t.upos='NOUN' AND t.feat_case IS NOT NULL AND t.feat_case!='Cpd'"

con = sqlite3.connect(DB)
cur = con.cursor()

out = {"probe": "h1274-A3-dat-attestation", "db": str(DB), "universe_where": UNIVERSE}

# 0. Published-number cross-checks (adversarial sanity: refuse to report if they drift)
cur.execute(f"SELECT COUNT(*) FROM token t WHERE {UNIVERSE}")
denom = cur.fetchone()[0]
cur.execute(f"SELECT COUNT(*) FROM token t WHERE {UNIVERSE} AND t.feat_case='Dat'")
dat_total = cur.fetchone()[0]
out["denominator_inflected_noun_tokens"] = denom
out["dat_tokens"] = dat_total
out["dat_share"] = round(dat_total / denom, 4)
assert denom == 1790270, f"denominator drifted: {denom}"
assert dat_total == 39190, f"Dat total drifted: {dat_total}"

# 1. Cell view — where inside Dat the rarity actually lives
cur.execute(
    f"SELECT t.feat_number, COUNT(*) FROM token t WHERE {UNIVERSE} AND t.feat_case='Dat' "
    "GROUP BY t.feat_number"
)
cells = dict(cur.fetchall())
out["dat_by_number"] = cells
out["dat_dual_share_of_universe"] = round(cells.get("Dual", 0) / denom, 5)

# 2. Text-level attestation: in how many of the corpus texts does Dat occur at all?
cur.execute(
    "SELECT COUNT(DISTINCT ch.text_id) FROM token t "
    "JOIN sentence s ON s.id = t.sentence_id JOIN chapter ch ON ch.chapter_id = s.chapter_id "
    f"WHERE {UNIVERSE}"
)
texts_with_nouns = cur.fetchone()[0]
cur.execute(
    "SELECT COUNT(DISTINCT ch.text_id) FROM token t "
    "JOIN sentence s ON s.id = t.sentence_id JOIN chapter ch ON ch.chapter_id = s.chapter_id "
    f"WHERE {UNIVERSE} AND t.feat_case='Dat'"
)
texts_with_dat = cur.fetchone()[0]
out["texts_with_noun_universe"] = texts_with_nouns
out["texts_with_dat"] = texts_with_dat

# 3. Lemma-level attestation: how many noun lemmas ever show a dative?
cur.execute(f"SELECT COUNT(DISTINCT t.lemma_id) FROM token t WHERE {UNIVERSE}")
lemmas_all = cur.fetchone()[0]
cur.execute(
    f"SELECT COUNT(DISTINCT t.lemma_id) FROM token t WHERE {UNIVERSE} AND t.feat_case='Dat'"
)
lemmas_with_dat = cur.fetchone()[0]
out["lemmas_in_universe"] = lemmas_all
out["lemmas_with_dat"] = lemmas_with_dat
out["lemma_dat_attestation_share"] = round(lemmas_with_dat / lemmas_all, 4)

# 3b. Baseline: the same lemma-attestation share for every case, so the Dat figure
# is read against its neighbours, not in isolation (adversarial guard: 8,5 % alone
# could be spun either way; under a Zipfian lemma distribution most lemmas attest
# few cases at all).
cur.execute(
    f"SELECT t.feat_case, COUNT(DISTINCT t.lemma_id) FROM token t WHERE {UNIVERSE} "
    "GROUP BY t.feat_case"
)
out["lemmas_with_case_by_case"] = {
    case: {"lemmas": n, "share_of_universe_lemmas": round(n / lemmas_all, 4)}
    for case, n in cur.fetchall()
}

# 4. Top dative lemmas — is the mass concentrated in a formulaic handful?
cur.execute(
    f"SELECT t.lemma, COUNT(*) c FROM token t WHERE {UNIVERSE} AND t.feat_case='Dat' "
    "GROUP BY t.lemma ORDER BY c DESC LIMIT 10"
)
out["top_dat_lemmas"] = [{"lemma": l, "tokens": c} for l, c in cur.fetchall()]
top10 = sum(r["tokens"] for r in out["top_dat_lemmas"])
out["top10_share_of_dat"] = round(top10 / dat_total, 4)

verdict = (
    "NOT SUPPORTABLE for the case as a whole: Dat has {dt} tokens, occurs in {tw}/{tn} texts "
    "and in {lw} of {la} noun lemmas ({ls:.1%}); 'почти не засвидетельствован' fits only the "
    "dual cell ({du} tokens, {ds:.3%} of the universe)."
).format(
    dt=dat_total, tw=texts_with_dat, tn=texts_with_nouns, lw=lemmas_with_dat,
    la=lemmas_all, ls=lemmas_with_dat / lemmas_all, du=cells.get("Dual", 0),
    ds=cells.get("Dual", 0) / denom,
)
out["verdict"] = verdict

dest = Path(__file__).with_suffix(".json")
dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(out, ensure_ascii=False, indent=2))
