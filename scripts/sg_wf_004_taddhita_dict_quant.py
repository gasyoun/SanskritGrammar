#!/usr/bin/env python3
"""SG-WF-004 taddhita — dictionary quantification (MWderivations wsfx × DCS tokens).

Answers the author's visa (H1183, cards 03/06): DCS is not the only source of truth.
Sanskrit dictionaries mark derivation where the corpus does not. The
[MWderivations](https://github.com/sanskrit-lexicon/MWderivations) project analysed
every Monier-Williams (1899) headword's derivation using MW's own 4-level markup;
records tagged `wsfx:<suffix>:…` are secondary (taddhita) suffix derivations
(e.g. `aMSa-vat  wsfx:vat`). That gives a CURATED per-suffix taddhita TYPE inventory —
the classification DCS lacks. We join those headwords (SLP1→IAST) back to the pinned DCS
snapshot to get the corpus TOKEN counts the dictionary lacks.

This covers the abstract (-tva/-tā), possessive (-vat/-mat/-vin/-min/-vala), adverbial
(-tas/-śas) and comparison (-tara/-tama) classes — precisely the whole-lemmatized taddhita
the corpus segmentation layer could not isolate. It does NOT yet cover the possessive -in,
relational -ika, or patronymic -ya, which MWderivations tags as compounds/atomic stems, not
`wsfx` — that residue needs MW's "fr." etymology or the Apte/SKD/VCP entries (next step).

Read-only. Emits sangram/articles/taddhita-overview/data/dict_quant_summary.json.
"""
import argparse, json, re, sqlite3, sys
from collections import defaultdict
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

GROUP = {'tva':'абстракт','tA':'абстракт','tvana':'абстракт','tana':'абстракт',
         'vat':'поссессив','mat':'поссессив','vin':'поссессив','min':'поссессив','vala':'поссессив',
         'tas':'адверб','Sas':'адверб','tara':'сравнение','tama':'сравнение','ka':'уменьш./относит.'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--mwd", default=str(DEFAULT_MWD))
    args = ap.parse_args()
    mwd, db = Path(args.mwd), Path(args.db)
    if not mwd.exists():
        print(f"ERROR: MWderivations analysis not found: {mwd}", file=sys.stderr); return 1
    if not db.exists():
        print(f"ERROR: DCS master not found: {db}", file=sys.stderr); return 1

    per_suf = defaultdict(list)
    total = 0
    for line in mwd.open(encoding='utf-8'):
        cols = line.rstrip('\n').split('\t')
        if len(cols) < 8: continue
        m = re.match(r'wsfx1?:([A-Za-z]+):', cols[7])
        if not m: continue
        per_suf[m.group(1)].append(to_iast(cols[2]))
        total += 1

    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    cur = con.cursor()
    prov = dict(cur.execute("SELECT key, value FROM provenance").fetchall())
    if "source_commit" not in prov:
        print("ERROR: master has no provenance pin — refusing (C3 §2.1)", file=sys.stderr); return 1
    NOMINAL = "upos IN ('NOUN','ADJ')"

    rows = []
    g_mw = g_dcs = g_tok = 0
    for suf in sorted(per_suf, key=lambda s: -len(per_suf[s])):
        lemmas = sorted(set(per_suf[suf]))
        tok = typ = 0
        top = []
        for i in range(0, len(lemmas), 500):
            chunk = lemmas[i:i+500]
            ph = ",".join("?" * len(chunk))
            for lem, c in cur.execute(
                    f"SELECT lemma, COUNT(*) FROM token WHERE {NOMINAL} AND lemma IN ({ph}) GROUP BY lemma",
                    chunk):
                tok += c; typ += 1; top.append((lem, c))
        top.sort(key=lambda x: -x[1])
        rows.append({"suffix": suf, "group": GROUP.get(suf, "?"), "mw_types": len(lemmas),
                     "dcs_attested_types": typ, "dcs_tokens": tok,
                     "top_lemmas": [f"{l} ({c})" for l, c in top[:5]]})
        g_mw += len(lemmas); g_dcs += typ; g_tok += tok
    con.close()

    summary = {
        "study": "SG-WF-004 taddhita — dictionary quantification (MWderivations wsfx × DCS token join)",
        "toc_ref": "SG-WF-004",
        "method": "MW headwords tagged wsfx:<suffix> in MWderivations/step3/analysis2.txt (curated MW-markup derivation) → SLP1→IAST → joined to pinned DCS snapshot for token counts",
        "dictionary_source": {"repo": "sanskrit-lexicon/MWderivations", "file": "step3/analysis2.txt",
                              "signal": "wsfx:<suffix> = secondary (taddhita) suffix derivation of a MW headword"},
        "corpus_snapshot": {"source_commit": prov.get("source_commit"), "imported_at": prov.get("imported_at"),
                            "note": "pin 04e0778 bound by provenance + tag c3-pin-04e0778-content"},
        "mw_wsfx_records": total,
        "totals": {"mw_types": g_mw, "dcs_attested_types": g_dcs, "dcs_tokens": g_tok},
        "per_suffix": rows,
        "coverage_note": "covers abstract/possessive/adverbial/comparison taddhita; possessive -in, relational -ika, patronymic -ya are NOT wsfx-tagged in MWderivations (compounds/atomic stems) — residue for an Apte/MW-etymology pass",
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "dict_quant_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"MW wsfx taddhita records: {total}", file=sys.stderr)
    print(f"{'suffix':7s}{'group':20s}{'MWtyp':>7s}{'DCStyp':>8s}{'DCStok':>10s}", file=sys.stderr)
    for r in rows:
        print(f"{r['suffix']:7s}{r['group']:20s}{r['mw_types']:7d}{r['dcs_attested_types']:8d}{r['dcs_tokens']:10,d}", file=sys.stderr)
    print(f"TOTAL: MW types {g_mw:,}; DCS-attested types {g_dcs:,}; DCS tokens {g_tok:,}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
