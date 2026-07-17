#!/usr/bin/env python3
"""SG-WF-004 taddhita residue — quantify -in / -ika / -ya from MW POS + base-attest + DCS.

The MWderivations `wsfx` layer (H1189) did NOT cover the author's key trio — possessive
-in, relational -ika, patronymic/relational -ya — because MW analyses them as compounds or
atomic stems, not as `wsfx` suffix derivations. This pass recovers them WITHOUT inventing a
classification: it uses MW's own headword inventory + grammatical gender (col5 of
MWderivations/step3/analysis2.txt, which carries MW's `mfn`/`m` marking).

Two dictionary-grounded measures per suffix:
  (a) POS-grounded TYPES — MW headwords ending in the suffix that MW marks adjectival
      (mfn = m:f:n, the possessive/relational signature). For -in the feminine -iṇī variant
      (`m:f#iRI:n`) is an extra-strong possessive marker.
  (b) BASE-ATTESTED subset — of (a), those whose stem-minus-suffix base (vṛddhi reversed for
      -ika/-ya) is ITSELF an attested MW headword → provably transparent derivation.
Both are then joined (SLP1→IAST) to the pinned DCS snapshot for corpus TOKEN counts.

Precision is bounded by a seeded hand-adjudication sample (emitted for the caller). The -ya
class is the noisy one (overlaps kṛt gerundive); the base-attested + adjectival filter is the
defence, and the sample measures what leaks through.

Read-only. Emits sangram/articles/taddhita-overview/data/residue_summary.json + sample TSV.
"""
import argparse, csv, json, random, re, sqlite3, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
DEFAULT_MWD = GITHUB / "MWderivations" / "step3" / "analysis2.txt"
OUT_DIR = ROOT / "sangram" / "articles" / "taddhita-overview" / "data"

SLP1 = {'A':'ā','I':'ī','U':'ū','f':'ṛ','F':'ṝ','x':'ḷ','X':'ḹ','E':'ai','O':'au',
        'M':'ṃ','H':'ḥ','K':'kh','G':'gh','N':'ṅ','C':'ch','J':'jh','Y':'ñ',
        'w':'ṭ','W':'ṭh','q':'ḍ','Q':'ḍh','R':'ṇ','T':'th','D':'dh','P':'ph','B':'bh',
        'S':'ś','z':'ṣ','~':'m̐','|':'','@':''}
def to_iast(s): return ''.join(SLP1.get(c, c) for c in s)

SEED = 20260717
SAMPLE = 60

# de-vṛddhi the FIRST syllable (relational/patronymic -ika/-ya vṛddhi the initial):
# vaidika<-vidyā, kOnteya<-kunti, dEva<-diva. Reverse: initial E->i, O->u, A->a, ai/au/ā.
def devrddhi_initial(stem):
    cands = {stem}
    if stem[:1] == 'E': cands.add('i' + stem[1:]); cands.add('e' + stem[1:])
    if stem[:1] == 'O': cands.add('u' + stem[1:]); cands.add('o' + stem[1:])
    if stem[:1] == 'A': cands.add('a' + stem[1:])
    # also internal ā/ai/au (some vṛddhi is not word-initial)
    for a, b in (('A','a'), ('E','i'), ('O','u')):
        i = stem.find(a)
        if i > 0: cands.add(stem[:i] + b + stem[i+1:])
    return cands


def load_mw(mwd):
    """Return: headword_set (SLP1), and per-headword gender string."""
    hw = set()
    gender = {}
    with open(mwd, encoding='utf-8') as f:
        for line in f:
            c = line.rstrip('\n').split('\t')
            if len(c) < 5: continue
            hw.add(c[2]); gender[c[2]] = c[4]
    return hw, gender


ADJ = lambda g: g == 'm:f:n' or g.startswith('m:f#') or g == 'm:f' or g == 'm:n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--mwd", default=str(DEFAULT_MWD))
    args = ap.parse_args()
    mwd, db = Path(args.mwd), Path(args.db)
    if not mwd.exists() or not db.exists():
        print("ERROR: missing MWderivations or DCS master", file=sys.stderr); return 1

    hw, gender = load_mw(mwd)
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing", file=sys.stderr); return 1
    NOMINAL = "upos IN ('NOUN','ADJ')"

    def dcs_tokens(lemmas_iast):
        lemmas = sorted(set(lemmas_iast)); tok = typ = 0
        for i in range(0, len(lemmas), 500):
            ch = lemmas[i:i+500]; ph = ",".join("?"*len(ch))
            for lem, c in cur.execute(
                    f"SELECT lemma, COUNT(*) FROM token WHERE {NOMINAL} AND lemma IN ({ph}) GROUP BY lemma", ch):
                tok += c; typ += 1
        return typ, tok

    # suffix specs: (name, ending, vrddhi_base)
    specs = [("in", "in", False), ("ika", "ika", True), ("ya", "ya", True)]
    results = []
    sample_pool = []
    for name, end, vrd in specs:
        pos_types = []      # POS-grounded adjectival headwords ending in suffix
        base_attested = []  # subset with attested base
        for w in hw:
            if not w.endswith(end) or len(w) <= len(end) + 1: continue
            g = gender.get(w, "")
            if not ADJ(g):  # require adjectival marking (possessive/relational signature)
                continue
            pos_types.append(w)
            stem = w[:-len(end)]
            bases = devrddhi_initial(stem) if vrd else {stem, stem.rstrip('a')}
            if bases & hw:
                base_attested.append(w)
        pos_iast = [to_iast(w) for w in pos_types]
        ba_iast = [to_iast(w) for w in base_attested]
        pt_typ, pt_tok = dcs_tokens(pos_iast)
        ba_typ, ba_tok = dcs_tokens(ba_iast)
        results.append({
            "suffix": name,
            "mw_adjectival_types": len(pos_types),
            "mw_base_attested_types": len(base_attested),
            "dcs_attested_types_posgrounded": pt_typ, "dcs_tokens_posgrounded": pt_tok,
            "dcs_attested_types_baseattested": ba_typ, "dcs_tokens_baseattested": ba_tok,
        })
        # add to hand-adjudication pool (base-attested, freq-weighted later)
        for w in base_attested:
            sample_pool.append((name, to_iast(w)))

    # seeded sample across the three classes (base-attested set)
    rng = random.Random(SEED)
    rng.shuffle(sample_pool)
    sample = sample_pool[:SAMPLE]

    con.close()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "residue_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["suffix_class", "lemma", "verdict(blank→adjudicate: taddhita|krt|primary|compound|name)"])
        for name, lem in sample:
            w.writerow([name, lem, ""])

    summary = {
        "study": "SG-WF-004 taddhita residue — -in/-ika/-ya via MW POS + base-attest + DCS",
        "toc_ref": "SG-WF-004",
        "method": "MW headwords ending in the suffix that MW marks adjectival (mfn/m:f#iṇī) = possessive/relational signature (POS-grounded); base-attested subset requires the vṛddhi-reversed stem to be an attested MW headword. Joined to pinned DCS for tokens.",
        "corpus_snapshot": {"source_commit": prov.get("source_commit"),
                            "note": "pin 04e0778 bound by provenance + tag c3-pin-04e0778-content"},
        "mw_headwords": len(hw),
        "per_suffix": results,
        "adjudication_sample": {"seed": SEED, "size": len(sample), "file": "residue_sample.tsv",
                                "weighting": "shuffled base-attested set across -in/-ika/-ya"},
        "limits": {
            "ya_polyfunctional": "-ya overlaps kṛt gerundive; the adjectival+base-attested filter is the defence, sample measures leakage",
            "pos_grounded_vs_base": "POS-grounded is broader (any MW adjectival -X); base-attested is the transparent-derivation lower bound",
            "compounds_included": "compound-final -in/-ya (aṃśa-bhāgin) are counted — they carry the suffix; not separated from simplex here",
        },
    }
    (OUT_DIR / "residue_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"MW headwords: {len(hw):,}", file=sys.stderr)
    for r in results:
        print(f"-{r['suffix']:4s} MW-adj {r['mw_adjectival_types']:6,} | base-attest {r['mw_base_attested_types']:6,} "
              f"| DCS(pos) {r['dcs_attested_types_posgrounded']:5,}t/{r['dcs_tokens_posgrounded']:8,}tok "
              f"| DCS(base) {r['dcs_attested_types_baseattested']:5,}t/{r['dcs_tokens_baseattested']:8,}tok", file=sys.stderr)
    print(f"sample → {OUT_DIR/'residue_sample.tsv'} ({len(sample)})", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
