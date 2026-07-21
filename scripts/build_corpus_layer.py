#!/usr/bin/env python3
"""Corpus layer for the Kochergina / Apte methodichka companions (H1297, W2-add-b).

Adds a per-lemma corpus data layer to the two print-companion manuscripts:
DCS frequency band + one corpus-attested example sentence with a DCS locus.

Stages (run from the repo root):

    python scripts/build_corpus_layer.py extract --book kochergina|apte
        Parse the companion manuscript's per-lesson lemma inventory (IAST tokens
        under each "## Занятие" heading), validate every token against the DCS
        lemma table AND the kosha frequency table, and write
        <BookDir>/corpus_layer/lemma_candidates.tsv.  Tokens that fail either
        join are logged LOUDLY to stderr — they are the "unparseable rows".

    python scripts/build_corpus_layer.py candidates --book kochergina|apte
        Read the hand-curated <BookDir>/corpus_layer/lemmas_selected.tsv
        (lesson · lemma_iast · topic · [feature]), join the DCS frequency band,
        query the DCS-2026 corpus for short candidate example sentences, and
        write <BookDir>/corpus_layer/example_candidates.tsv for the authoring
        pass.  Public-tier Russian glosses (SanskritRussian lemma_glossary.tsv)
        are attached per lemma as authoring reference — they are the ONLY
        translation layer this script ever reads.

Frequency bands (documented once here, cited by the manuscripts):
    rank_all <= 100   -> "топ-100"
    rank_all <= 1000  -> "топ-1000"
    otherwise         -> "редкое"
where rank_all is the all-corpus lemma rank in kosha
data/frequency/lemma_frequency.tsv (DCS-derived; Hellwig's Digital Corpus of
Sanskrit).  Example sentences come from the DCS-2026 conllu import
(VisualDCS/src/DCS-data-2026/dcs_full.sqlite, source gasyoun/dcs-conllu of
OliverHellwig/sanskrit, commit 04e0778, imported 06-06-2026).  Attribute DCS
(Hellwig) wherever these numbers surface.

Rights: this script never opens any restricted translation layer.  Russian
renderings in the published corpus_layer.tsv are freshly authored (ru_source =
"authored") or public site-tier (ru_source = "public-glossary"); a row whose
only rendering would be restricted ships Sanskrit-only with ru_source =
"restricted" and an empty ru field (the manuscript prints the «перевод в
закрытом слое» marker instead).

Stdlib-only except ``indic_transliteration`` (IAST -> SLP1 join key to the
kosha frequency table), same dependency posture as
sangram/data/samasa_ladder/build_samasa_ladder.py.
"""

import argparse
import csv
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
GITHUB = REPO.parent
DEFAULT_FREQ = GITHUB / "kosha" / "data" / "frequency" / "lemma_frequency.tsv"
DEFAULT_DCS = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
DEFAULT_GLOSS = GITHUB / "SanskritRussian" / "lemma_glossary.tsv"

BOOKS = {
    "kochergina": {
        "dir": REPO / "KocherginaUchebnik_1998",
        "manuscripts": [
            "METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md",
        ],
    },
    "apte": {
        "dir": REPO / "ApteSyntax_1885",
        "manuscripts": [
            "METODICHKA_APTE_KOMMENTARII_2026.md",
        ],
    },
}

# Texts a Russian-textbook learner is most likely to meet next; candidate
# examples from these are preferred (in this order) before all other texts.
FAMILIAR_TEXTS = [
    "Hitopadeśa",
    "Pañcatantra",
    "Manusmṛti",
    "Rāmāyaṇa",
    "Mahābhārata",
    "Kathāsaritsāgara",
]

# IAST word: lowercase latin + IAST diacritics (no capitals — proper names and
# European words in the prose start uppercase and are not lemma candidates).
IAST_TOKEN = re.compile(r"(?<![A-Za-zāīūṛṝḷḹṅñṭḍṇśṣḥṃėē])[a-zāīūṛṝḷḹṅñṭḍṇśṣḥṃ]+(?![A-Za-zāīūṛṝḷḹṅñṭḍṇśṣḥṃ])")

# Frequent non-Sanskrit latin noise in the Russian prose (English/Latin words,
# register ids, unit tokens).  Anything here is never a lemma candidate.
STOPLIST = {
    "verbum", "finitum", "yml", "md", "mdx", "csv", "tsv", "json", "jsonl",
    "index", "the", "and", "of", "in", "to", "for", "from", "data", "file",
    "reestr", "true", "false", "overstated", "untestable", "dcs", "sg", "mo",
    "mg", "hk", "apt", "org", "http", "https", "github", "com", "blob",
    "main", "sanskritgrammar", "claims", "handoffs", "use", "see", "what",
    "can", "give", "us",
}

LESSON_RE = re.compile(r"^##\s+(Занятие|Занятия)\s+([IVXLC\d]+(?:[–-][IVXLC\d]+)?)", re.M)


def iast_to_slp1(text):
    from indic_transliteration import sanscript
    return sanscript.transliterate(text, sanscript.IAST, sanscript.SLP1)


def band_for_rank(rank_all):
    """The banding rule the manuscripts cite — keep in sync with the docstring."""
    if rank_all is None:
        return "вне корпуса"
    if rank_all <= 100:
        return "топ-100"
    if rank_all <= 1000:
        return "топ-1000"
    return "редкое"


def load_frequency(path):
    """lemma_slp1 -> (count_all, rank_all)."""
    table = {}
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            try:
                table[row["lemma_slp1"]] = (int(row["count_all"]), int(row["rank_all"]))
            except (KeyError, ValueError):
                continue
    return table


def load_public_glosses(path, top_n=3):
    """lemma_slp1 -> "gloss1 | gloss2 | gloss3" (public site tier, best-attested first)."""
    best = {}
    with open(path, encoding="utf-8") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            try:
                n = int(row["n"])
            except (KeyError, ValueError):
                continue
            best.setdefault(row["lemma_slp1"], []).append((n, row["ru"]))
    return {
        lemma: " | ".join(ru for _, ru in sorted(vs, key=lambda v: -v[0])[:top_n])
        for lemma, vs in best.items()
    }


def dcs_lemma_set(con):
    return {r[0] for r in con.execute("SELECT DISTINCT lemma FROM lemma")}


def cmd_extract(book, args):
    con = sqlite3.connect(args.dcs)
    known = dcs_lemma_set(con)
    freq = load_frequency(args.freq)
    outdir = book["dir"] / "corpus_layer"
    outdir.mkdir(exist_ok=True)
    rows, unmatched = [], []
    seen = set()
    for name in book["manuscripts"]:
        text = (book["dir"] / name).read_text(encoding="utf-8")
        # Split the manuscript into lesson sections.
        matches = list(LESSON_RE.finditer(text))
        for i, m in enumerate(matches):
            lesson = m.group(2)
            chunk = text[m.end():matches[i + 1].start() if i + 1 < len(matches) else len(text)]
            for tok in IAST_TOKEN.findall(chunk):
                if len(tok) < 2 and tok not in ("i",):
                    continue
                if tok in STOPLIST:
                    continue
                key = (lesson, tok)
                if key in seen:
                    continue
                seen.add(key)
                if tok not in known:
                    unmatched.append((name, lesson, tok, "not a DCS lemma"))
                    continue
                slp1 = iast_to_slp1(tok)
                if slp1 not in freq:
                    unmatched.append((name, lesson, tok, "no kosha frequency row"))
                    continue
                count_all, rank_all = freq[slp1]
                rows.append((lesson, tok, slp1, count_all, rank_all, band_for_rank(rank_all)))
    out = outdir / "lemma_candidates.tsv"
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["lesson", "lemma_iast", "lemma_slp1", "count_all", "rank_all", "band"])
        w.writerows(rows)
    print(f"{out}: {len(rows)} candidate rows from {len(book['manuscripts'])} manuscript(s)")
    if unmatched:
        print(f"UNPARSEABLE ({len(unmatched)} tokens failed a join — curate around these):", file=sys.stderr)
        for name, lesson, tok, why in unmatched:
            print(f"  {name} · Занятие {lesson} · {tok!r}: {why}", file=sys.stderr)


def query_examples(con, lemma, feature, limit, min_len=20, max_len=85):
    """Short candidate sentences containing a token of `lemma`, familiar texts first."""
    cond = ""
    params = {"lemma": lemma, "min": min_len, "max": max_len}
    if feature:
        key, val = feature.split("=", 1)
        assert re.fullmatch(r"[a-z_]+", key), f"bad feature key {key!r}"
        cond = f" AND tk.feat_{key} = :featval"
        params["featval"] = val
    rank_case = " ".join(
        f"WHEN t.name = '{name}' THEN {i}" for i, name in enumerate(FAMILIAR_TEXTS)
    )
    sql = f"""
        SELECT t.name, c.ref, s.sent_counter, s.sent_subcounter, s.text_sandhied,
               tk.form, MIN(CASE {rank_case} ELSE 99 END) AS fam
        FROM token tk
        JOIN sentence s ON tk.sentence_id = s.id
        JOIN chapter c ON s.chapter_id = c.chapter_id
        JOIN text t ON c.text_id = t.text_id
        WHERE tk.lemma = :lemma{cond}
          AND length(s.text_sandhied) BETWEEN :min AND :max
        GROUP BY s.id
        ORDER BY fam, length(s.text_sandhied)
        LIMIT {int(limit)}
    """
    return con.execute(sql, params).fetchall()


def cmd_candidates(book, args):
    con = sqlite3.connect(args.dcs)
    freq = load_frequency(args.freq)
    glosses = load_public_glosses(args.gloss) if args.gloss.exists() else {}
    outdir = book["dir"] / "corpus_layer"
    sel_path = outdir / "lemmas_selected.tsv"
    if not sel_path.exists():
        sys.exit(f"FATAL: curated inventory missing: {sel_path}")
    out = outdir / "example_candidates.tsv"
    n_rows = 0
    with open(sel_path, encoding="utf-8") as fh, open(out, "w", encoding="utf-8", newline="") as ofh:
        w = csv.writer(ofh, delimiter="\t", lineterminator="\n")
        w.writerow(["lesson", "lemma_iast", "lemma_slp1", "count_all", "rank_all", "band",
                    "cand_no", "dcs_text", "dcs_ref", "dcs_sent", "form", "example_iast",
                    "public_glosses"])
        for row in csv.DictReader(fh, delimiter="\t"):
            lemma = row["lemma_iast"]
            slp1 = iast_to_slp1(lemma)
            count_all, rank_all = freq.get(slp1, (None, None))
            if rank_all is None:
                print(f"WARN: {lemma!r} has no kosha frequency row — band = 'вне корпуса'", file=sys.stderr)
            band = band_for_rank(rank_all)
            feature = (row.get("feature") or "").strip() or None
            cands = query_examples(con, lemma, feature, args.limit)
            if not cands:
                print(f"WARN: {lemma!r} (feature={feature}) — no candidate sentences", file=sys.stderr)
            for i, (tname, ref, sc, ssc, sent, form, _fam) in enumerate(cands, 1):
                locus = f"{ref}, {sc}" + (f".{ssc}" if ssc and str(ssc) != "1" else "")
                w.writerow([row["lesson"], lemma, slp1, count_all, rank_all, band,
                            i, tname, ref, locus, form, sent,
                            glosses.get(slp1, "")])
                n_rows += 1
    print(f"{out}: {n_rows} candidate example rows")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("stage", choices=["extract", "candidates"])
    ap.add_argument("--book", required=True, choices=sorted(BOOKS))
    ap.add_argument("--freq", type=Path, default=DEFAULT_FREQ)
    ap.add_argument("--dcs", type=Path, default=DEFAULT_DCS)
    ap.add_argument("--gloss", type=Path, default=DEFAULT_GLOSS)
    ap.add_argument("--limit", type=int, default=6, help="candidate sentences per lemma")
    args = ap.parse_args()
    for p in (args.freq, args.dcs):
        if not p.exists():
            sys.exit(f"FATAL: required input missing: {p}")
    book = BOOKS[args.book]
    if args.stage == "extract":
        cmd_extract(book, args)
    else:
        cmd_candidates(book, args)


if __name__ == "__main__":
    main()
