#!/usr/bin/env python3
"""Build the Leitan -> Whitney -> DCS concordance artifacts.

Outputs
-------
data/leitan_whitney_sections.tsv
    Section-level index of Whitney, *Sanskrit Grammar* (1889): one row per
    numbered section (1,306 rows), with chapter file and the opening snippet.
data/leitan_dcs_coverage_2026-10-26.json
    DCS frequency slices used by the concordance report: totals, case,
    verb-form, mood, voice, tense, particle, preverb, compound, numeral and
    correlative counts, plus per-text rates for the genre cut.

Usage
-----
    python3 scripts/leitan_whitney_dcs_concordance.py
    python3 scripts/leitan_whitney_dcs_concordance.py --db /path/to/dcs_full.sqlite

The DCS database is VisualDCS's dcs_full.sqlite (5.69M tokens, 754,726
sentences, UD-style head/deprel on a 223,751-token slice). Whitney mdx files
are the Wikisource-derived chapter renderings in WhitneyGrammar_1889/.
"""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
def _find_db() -> Path:
    """Locate dcs_full.sqlite from the repo or any ancestor (worktree-safe)."""
    rel = Path("VisualDCS") / "src" / "DCS-data-2026" / "dcs_full.sqlite"
    for base in (REPO, *REPO.parents):
        candidate = base / rel
        if candidate.is_file():
            return candidate
    return REPO.parent / rel


DEFAULT_DB = _find_db()
DEFAULT_WHITNEY = REPO / "WhitneyGrammar_1889"
DEFAULT_TSV = REPO / "data" / "leitan_whitney_sections.tsv"
DEFAULT_JSON = REPO / "data" / "leitan_dcs_coverage_2026-10-26.json"

SECTION_RE = re.compile(r"\*\*§(\d+)\*\*")

PARTICLE_LEMMAS = (
    "iti", "ca", "eva", "api", "na", "hi", "tu", "vā",
    "yathā", "tathā", "evam", "atha", "khalu",
)

GENRE_TEXTS = (
    "Mahābhārata", "Rāmāyaṇa", "Ṛgveda", "Śatapathabrāhmaṇa",
    "Suśrutasaṃhitā", "Kathāsaritsāgara", "Carakasaṃhitā", "Bhāgavatapurāṇa",
)


def parse_whitney(directory: Path) -> list[dict]:
    """Return one row per numbered Whitney section."""
    rows: list[dict] = []
    for path in sorted(directory.glob("*.mdx")):
        if path.name.startswith("00"):
            continue
        text = path.read_text(encoding="utf-8")
        parts = SECTION_RE.split(text)
        for i in range(1, len(parts), 2):
            body = parts[i + 1]
            # The Wikisource URL itself contains "(Whitney)", so strip the
            # markdown link up to the first ")" followed by whitespace.
            body = re.sub(r"^\]\(.*?\)\s", "", body, count=1, flags=re.DOTALL)
            body = body.replace("**", "").replace("*", "")
            body = re.sub(r"\s+", " ", body).strip()
            rows.append({
                "section": int(parts[i]),
                "chapter": path.stem,
                "file": path.name,
                "snippet": body[:160],
            })
    rows.sort(key=lambda r: r["section"])
    return rows


def write_tsv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        fh.write("section\tchapter\tfile\tsnippet\n")
        for r in rows:
            snippet = r["snippet"].replace("\t", " ").replace("\n", " ")
            fh.write(f"{r['section']}\t{r['chapter']}\t{r['file']}\t{snippet}\n")


def query(cur: sqlite3.Cursor, sql: str, params: tuple = ()) -> list[tuple]:
    return cur.execute(sql, params).fetchall()


def dcs_slices(db_path: Path) -> dict:
    con = sqlite3.connect(str(db_path))
    cur = con.cursor()
    out: dict = {"generated": "2026-10-26", "db": db_path.name}

    out["totals"] = {
        "tokens": query(cur, "SELECT COUNT(*) FROM token")[0][0],
        "sentences": query(cur, "SELECT COUNT(*) FROM sentence")[0][0],
        "texts": query(cur, "SELECT COUNT(*) FROM text")[0][0],
    }

    def by_column(col: str) -> dict:
        rows = query(
            cur,
            f"SELECT COALESCE({col}, ''), COUNT(*), COUNT(DISTINCT sentence_id) "
            f"FROM token GROUP BY 1 ORDER BY 2 DESC",
        )
        return {k: {"tokens": n, "sentences": s} for k, n, s in rows if k}

    out["cases"] = by_column("feat_case")
    out["verbforms"] = by_column("feat_verbform")
    out["moods"] = by_column("feat_mood")
    out["voices"] = by_column("feat_voice")
    out["tenses"] = by_column("feat_tense")

    out["particles"] = {}
    for lemma in PARTICLE_LEMMAS:
        n, s = query(
            cur,
            "SELECT COUNT(*), COUNT(DISTINCT sentence_id) FROM token WHERE lemma=?",
            (lemma,),
        )[0]
        out["particles"][lemma] = {"tokens": n, "sentences": s}

    out["preverbs"] = {
        "lemmas": query(
            cur,
            "SELECT COUNT(*) FROM lemma WHERE preverbs IS NOT NULL AND TRIM(preverbs)<>''",
        )[0][0],
        "tokens": query(
            cur,
            "SELECT COUNT(*) FROM token t JOIN lemma l ON t.lemma_id=l.lemma_id "
            "WHERE l.preverbs IS NOT NULL AND TRIM(l.preverbs)<>''",
        )[0][0],
        "sentences": query(
            cur,
            "SELECT COUNT(DISTINCT t.sentence_id) FROM token t JOIN lemma l ON t.lemma_id=l.lemma_id "
            "WHERE l.preverbs IS NOT NULL AND TRIM(l.preverbs)<>''",
        )[0][0],
    }

    out["compounds"] = {
        "tokens": out["cases"].get("Cpd", {}).get("tokens", 0),
        "sentences": out["cases"].get("Cpd", {}).get("sentences", 0),
    }
    out["numerals"] = {
        "tokens": query(cur, "SELECT COUNT(*) FROM token WHERE upos='NUM'")[0][0],
        "sentences": query(cur, "SELECT COUNT(DISTINCT sentence_id) FROM token WHERE upos='NUM'")[0][0],
    }
    out["correlatives"] = {
        "sentences": query(
            cur,
            "SELECT COUNT(*) FROM (SELECT sentence_id FROM token WHERE lemma IN ('yad','tad') "
            "GROUP BY sentence_id HAVING COUNT(DISTINCT lemma)=2)",
        )[0][0],
    }

    out["per_text"] = []
    for name in GENRE_TEXTS:
        row = query(
            cur,
            """
            SELECT COUNT(*) AS n,
              ROUND(1000.0*SUM(CASE WHEN k.feat_mood='Opt' THEN 1 ELSE 0 END)/COUNT(*),1),
              ROUND(1000.0*SUM(CASE WHEN k.feat_verbform='Gdv' THEN 1 ELSE 0 END)/COUNT(*),1),
              ROUND(1000.0*SUM(CASE WHEN k.feat_case='Voc' THEN 1 ELSE 0 END)/COUNT(*),1),
              ROUND(1000.0*SUM(CASE WHEN k.feat_case='Gen' THEN 1 ELSE 0 END)/COUNT(*),1),
              ROUND(1000.0*SUM(CASE WHEN l.preverbs IS NOT NULL AND TRIM(l.preverbs)<>'' THEN 1 ELSE 0 END)/COUNT(*),1)
            FROM token k
            JOIN sentence s ON k.sentence_id=s.id
            JOIN chapter ch ON s.chapter_id=ch.chapter_id
            JOIN text t ON ch.text_id=t.text_id
            JOIN lemma l ON k.lemma_id=l.lemma_id
            WHERE t.name=?
            """,
            (name,),
        )[0]
        out["per_text"].append({
            "text": name,
            "tokens": row[0],
            "opt_per_1000": row[1],
            "gdv_per_1000": row[2],
            "voc_per_1000": row[3],
            "gen_per_1000": row[4],
            "preverb_per_1000": row[5],
        })

    con.close()
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--whitney-dir", default=str(DEFAULT_WHITNEY))
    ap.add_argument("--tsv", default=str(DEFAULT_TSV))
    ap.add_argument("--json", default=str(DEFAULT_JSON))
    args = ap.parse_args()

    rows = parse_whitney(Path(args.whitney_dir))
    write_tsv(rows, Path(args.tsv))
    print(f"whitney: {len(rows)} sections -> {args.tsv}")

    data = dcs_slices(Path(args.db))
    Path(args.json).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json).write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"dcs: {data['totals']['tokens']} tokens / {data['totals']['sentences']} sentences "
        f"-> {args.json}"
    )


if __name__ == "__main__":
    main()
