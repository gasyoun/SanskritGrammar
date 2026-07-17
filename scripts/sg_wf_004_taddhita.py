#!/usr/bin/env python3
"""SG-WF-004 «Вторичная деривация (taddhita): обзор» — secondary nominal derivation.

Core W2 ① overview (endgame slot, honest negative). taddhita = secondary
derivation: a nominal stem + a secondary suffix → a new noun/adjective (nara →
nara-tva «человечность»; go → gav-ya «бычий»; vidyā → vaidya «учёный»). Whitney
ch. XVII §§ 1136–1245.

Where the kṛt overview (SG-WF-002) had a NATIVELY-tagged half to lean on (the
non-finite verb forms VerbForm∈{Part,Conv,Gdv,Inf} = 483 623 tokens, a clean
closed set), taddhita has **none**: it is purely nominal, and DCS carries **no
derivation feature at all** (0 grammar codes mention taddhita/suffix; form_classes
for SG-WF-004 in the C2 TOC is empty). So taddhita as a CATEGORY is invisible.

The only handle is **surface suffix-matching on lemmas** — and this overview's job
is to show, reproducibly, that it FAILS: every canonical taddhita suffix collides
with something else in the corpus.
  - The "most diagnostic" abstract suffixes -tā/-tva are polluted by lemmatized
    PRONOUN forms (bare `tā`, `tva`), proper NAMES (sītā), and PRIMARY nouns
    (latā «лиана», cintā «мысль», sattva «существо»).
  - The productive relational/possessive suffixes -ya/-in/-ika/-aka/-maya collide
    with kṛt (-ya gerundive, -aka agent pāvaka), primary consonant stems (pathin),
    primary nouns (udaka «вода», sūrya «солнце», maya), and compound finals.

So the honest result: **taddhita is not recoverable from DCS annotation**. A seeded
hand-adjudication of surface matches fixes the false-positive rate; the only path
to the category is MW etymology, which pilot P5 (SG-WF-003) already measured as
low-recall (precision 0.75, recall 0.09). The hardest negative of the W2 endgame.

Three layers (C5 §3): ATTESTED — the nominal universe + the surface-suffix noise
over the pinned snapshot; TRADITIONAL — the taddhita suffix inventory (Whitney
ch. XVII).

Contract C3: pinned snapshot (refuse without provenance pin) + SHA-256 + recorded
denominators + seeded sample. Read-only. Emits into
sangram/articles/taddhita-overview/data/.
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
OUT_DIR = ROOT / "sangram" / "articles" / "taddhita-overview" / "data"

NOMINAL = "('NOUN','ADJ')"
# canonical taddhita suffix inventory (Whitney ch. XVII), grouped by function
SUFFIXES = [
    ("tā", "абстракт «-ность/-ство» (f)"),
    ("tva", "абстракт «-ность/-ство» (n)"),
    ("maya", "«состоящий из»"),
    ("in", "поссессив «обладающий»"),
    ("vat", "поссессив «обладающий»"),
    ("mat", "поссессив «обладающий»"),
    ("ika", "относительный/vṛddhi"),
    ("īya", "относительный «принадлежащий»"),
    ("eya", "относительный/vṛddhi"),
    ("ya", "относительный/абстракт"),
    ("aka", "уменьшит./относит."),
    ("tara", "сравнит. степень"),
    ("tama", "превосх. степень"),
    ("tas", "аблативно-наречный"),
]
SEED = 20260717
SAMPLE_SIZE = 60


def sha256_file(path, chunk=4 * 1024 * 1024):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


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

    total_tokens = cur.execute("SELECT COUNT(*) FROM token").fetchone()[0]
    noun_tok = cur.execute("SELECT COUNT(*) FROM token WHERE upos='NOUN'").fetchone()[0]
    adj_tok = cur.execute("SELECT COUNT(*) FROM token WHERE upos='ADJ'").fetchone()[0]
    nominal_tok = noun_tok + adj_tok

    # native derivation feature check — expect ZERO
    caus = cur.execute("SELECT COUNT(*) FROM lemma WHERE grammar LIKE '%addh%' "
                       "OR grammar LIKE '%uffix%'").fetchone()[0]

    # surface suffix census over the nominal universe (lemma types + token mass)
    suffix_census = {}
    for suf, gloss in SUFFIXES:
        toks = cur.execute(
            f"SELECT COUNT(*) FROM token WHERE upos IN {NOMINAL} AND lemma LIKE ?",
            (f"%{suf}",)).fetchone()[0]
        types = cur.execute(
            f"SELECT COUNT(DISTINCT lemma) FROM token WHERE upos IN {NOMINAL} AND lemma LIKE ?",
            (f"%{suf}",)).fetchone()[0]
        top = cur.execute(
            f"SELECT lemma, COUNT(*) c FROM token WHERE upos IN {NOMINAL} AND lemma LIKE ? "
            f"GROUP BY lemma ORDER BY c DESC LIMIT 6", (f"%{suf}",)).fetchall()
        suffix_census[suf] = {"gloss": gloss, "tokens": toks, "types": types,
                              "top_lemmas": [f"{l} ({c})" for l, c in top]}

    # seeded freq-weighted adjudication sample across the productive suffixes,
    # over DISTINCT lemma types, for hand-classification (taddhita vs kṛt vs
    # primary/pronoun/name vs compound-final)
    probe_sufs = ["tā", "tva", "maya", "in", "ika", "aka", "ya", "eya", "īya", "vat"]
    pool = {}  # lemma -> tokens (dedup, keep max)
    for suf in probe_sufs:
        for lem, c in cur.execute(
                f"SELECT lemma, COUNT(*) c FROM token WHERE upos IN {NOMINAL} AND lemma LIKE ? "
                f"GROUP BY lemma", (f"%{suf}",)):
            pool[lem] = max(pool.get(lem, 0), c)
    lemmas = list(pool.items())
    total_mass = sum(c for _, c in lemmas)
    rng = random.Random(SEED)
    chosen, seen, tries = [], set(), 0
    while len(chosen) < min(SAMPLE_SIZE, len(lemmas)) and tries < 500000:
        r = rng.random() * total_mass
        acc = 0
        for lem, c in lemmas:
            acc += c
            if acc >= r:
                if lem not in seen:
                    seen.add(lem); chosen.append(lem)
                break
        tries += 1

    sample_rows = []
    for lem in chosen:
        # which probe suffix matched (longest)
        matched = max((s for s in probe_sufs if lem.endswith(s)), key=len, default="")
        sample_rows.append((lem, pool[lem], matched))

    con.close()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(OUT_DIR / "adjudication_sample.tsv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["lemma", "nominal_tokens", "matched_suffix",
                    "verdict(blank→adjudicate: taddhita|krt|primary|pronoun_name|compound)"])
        for r in sample_rows:
            w.writerow(list(r) + [""])

    summary = {
        "study": "SG-WF-004 «Вторичная деривация (taddhita): обзор» — secondary nominal derivation (core W2 ①, endgame, honest negative)",
        "toc_ref": "SG-WF-004",
        "kind": "overview (endgame slot; publishes its limit like the pilots)",
        "method": "taddhita has NO native tag (0 derivation grammar codes) and — unlike kṛt (SG-WF-002) — NO natively-tagged subset; the only handle is surface suffix-matching on lemmas, which this overview shows FAILS (every canonical suffix collides with pronoun forms / primary nouns / kṛt / compound finals). A seeded hand-adjudication fixes the false-positive rate.",
        "snapshot": {
            "source_repo": prov.get("source_repo"), "source_commit": prov.get("source_commit"),
            "imported_at": prov.get("imported_at"), "sha256": sha,
            "provenance_note": "pin 04e0778 orphaned; binding = provenance table + SHA-256 + tag c3-pin-04e0778-content",
        },
        "native_taddhita_feature": {
            "grammar_codes_mentioning_taddhita_or_suffix": caus,
            "form_classes_in_c2_toc": 0,
            "note": "zero — DCS carries no derivation marker for taddhita, and no natively-tagged subset (contrast kṛt's VerbForm half)",
        },
        "denominators": {
            "all_tokens": total_tokens,
            "nominal_tokens_noun_adj": nominal_tok,
            "noun_tokens": noun_tok, "adj_tokens": adj_tok,
            "nominal_share": round(nominal_tok / total_tokens, 4),
        },
        "surface_suffix_census": suffix_census,
        "adjudication_sample": {"seed": SEED, "size": len(sample_rows),
                                "probe_suffixes": probe_sufs,
                                "weighting": "freq-weighted draw of distinct nominal lemma types",
                                "file": "adjudication_sample.tsv"},
        "traditional_layer": {"witness": "Whitney 1889 ch. XVII §§1136–1245 (secondary derivation / taddhita)"},
        "limits": {
            "EM5_no_native_tag": "taddhita is a derivational category with no native tag AND no natively-tagged subset; it is invisible in the annotation",
            "surface_match_fails": "every canonical suffix collides: -tā/-tva with pronoun forms (tā, tva) + names (sītā) + primary nouns (latā, cintā, sattva); -maya with maya/samaya; -ya with kṛt gerundive + primary (sūrya); -in with primary consonant stems (pathin); -aka with kṛt agent (pāvaka) + primary (udaka)",
            "mw_etymology_low_recall": "the C2 sketch's 'via MW etymology' path was measured in pilot P5 (SG-WF-003) at precision 0.75 / recall 0.09 — it cannot recover the stratum",
            "pin": "orphaned 04e0778, bound by provenance table + SHA-256 + tag",
        },
    }
    (OUT_DIR / "coverage_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"all tokens {total_tokens:,}; nominal (NOUN+ADJ) {nominal_tok:,} "
          f"({100*nominal_tok/total_tokens:.1f}%); native taddhita features {caus}", file=sys.stderr)
    for suf, gloss in SUFFIXES:
        d = suffix_census[suf]
        print(f"  -{suf:5s} {d['tokens']:7,} tok / {d['types']:5,} types  top={d['top_lemmas'][:3]}", file=sys.stderr)
    print(f"sample → {OUT_DIR / 'adjudication_sample.tsv'} ({len(sample_rows)} lemmas)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
