#!/usr/bin/env python
"""H1212 — provenance of Bühler's exercise sentences (quotation / adapted / invented).

Matches the Devanāgarī exercise sentences of Bühler's *Leitfaden* (as digitised in
``scripts/data/sentences.json``, ``book == "buhler"``, ``script == "deva"``) against two
locally-available attested-text corpora:

  A. DCS 2026 running text -- ``sentence.text_sandhied`` in
     ``VisualDCS/src/DCS-data-2026/dcs_full.sqlite`` (754,726 sandhied IAST sentences).
  B. Böhtlingk, *Indische Sprüche* -- table ``subhashita`` in
     ``VisualDCS/src/DCS-data-2026/archive.sqlite`` (7,537 sayings, Deva + IAST).
  C. GRETIL plaintext -- the local ``SanskritSpellCheck/detectors/gretil_*_raw/`` dirs
     (kāvya, subhāṣita, smṛti, purāṇa, epic, stotra), added by H1344.

Corpus C exists to falsify a finding of the first pass. That pass concluded "kāvya is
nearly absent" from Bühler's sources -- but DCS carries no Raghuvaṃśa and no Śiśupālavadha,
so the finding may have been an artefact of *corpus composition* rather than a fact about
Bühler. GRETIL's Kāvya section (56 texts, Raghuvaṃśa and Kumārasaṃbhava included) is the
direct test. See
``BUHLER_SENTENCE_PROVENANCE_ADJUDICATION.md`` for the outcome.

**Rights.** GRETIL plaintext is CC BY-NC-SA 4.0. The house convention (PROJECT_INTERLINKS)
is: do not commit the raw source text, commit only derived summaries. This script therefore
*reads* the gitignored raw dirs and emits verdicts plus short evidence snippets; it never
copies a corpus file into the repo. An earlier revision of this docstring claimed GRETIL was
blocked by an open @DECIDE (SamudraManthanam D5) -- that was wrong. D5 gates the *Russian
translation* sourcing budget; its Sanskrit/GRETIL side is marked converted.

Method
------
Every string is reduced to two keys via ``sanskrit-util`` (the canonical transcoder --
never hand-rolled, per SHARED_CODE.md):

  * ``k_norm``  = ``su.norm(iast)``  -- diacritic-insensitive, m/n kept distinct.
  * ``k_fold``  = ``su.nfold(iast)`` -- as above, plus every nasal folded to ``n``.

``k_fold`` is used for *recall* (it absorbs the anusvāra/ṃ/m/n sandhi noise that makes a
quotation look unlike its source); ``k_norm`` is used for the *verdict* (nfold conflates
``m`` and ``n`` everywhere, including stem-internally, so it is too lossy to rule on).

Two independent detectors run over each corpus:

  1. **Spaceless substring.** Whitespace is stripped from both needle and haystack, so a
     match survives any disagreement about where word boundaries fall under sandhi
     (Bühler prints ``sa jīva``, the corpus may print ``saṃjīva``). Implemented as one
     concatenated haystack + ``str.find``, offsets mapped back by bisect.
  2. **Longest attested contiguous run.** Every *proper* contiguous token n-gram of the
     needle (2 ≤ n < all tokens), longest first, is searched in the same haystack; the
     full-length n-gram is skipped because detector 1 already covers it. The longest one
     that occurs in an attested text is the evidence for *adaptation*: a real adaptation
     preserves a phrase, whereas a drill sentence built from common words does not.

     A third signal, IDF-weighted token containment over an inverted index, is computed and
     reported but deliberately **excluded from the verdict**. A first pass ruled on
     containment alone and it was wrong in the obvious direction: ``adya jīvāmaḥ`` scored
     0.64 because its two tokens happen to occur, scattered and unrelated, somewhere in a
     long Aṣṭāṅgahṛdaya sentence. Containment ignores adjacency, so it cannot tell a
     quotation from a coincidence of vocabulary. It is kept in the output only as a
     lead for manual follow-up.

Verdicts are assigned mechanically, then the borderline band is adjudicated by hand
(see ``BUHLER_SENTENCE_PROVENANCE_ADJUDICATION.md``) -- that judgment step is why the
handoff is Opus-tier and not a cron job.

Outputs ``scripts/data/buhler_provenance.json`` and ``.csv``.

Usage:  python scripts/buhler_provenance.py [--limit N] [--db PATH] [--archive PATH]
"""

from __future__ import annotations

import argparse
import bisect
import csv
import json
import re
import sqlite3
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
GITHUB = ROOT.parent
sys.path.insert(0, str(GITHUB / "sanskrit-util" / "py"))
import sanskrit_util as su  # noqa: E402

DEFAULT_DB = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
DEFAULT_ARCHIVE = GITHUB / "VisualDCS" / "src" / "DCS-data-2026" / "archive.sqlite"
# CC BY-NC-SA plaintext, gitignored where it lives; read here, never copied into this repo.
DEFAULT_GRETIL = GITHUB / "SanskritSpellCheck" / "detectors"
GRETIL_DIRS = (
    "gretil_kavya_raw",
    "gretil_subhasita_raw",
    "gretil_smrti_raw",
    "gretil_purana_raw",
    "gretil_epic_raw",
    "gretil_pilot_raw",
)
SENTENCES = ROOT / "scripts" / "data" / "sentences.json"
OUT_JSON = ROOT / "scripts" / "data" / "buhler_provenance.json"
OUT_CSV = ROOT / "scripts" / "data" / "buhler_provenance.csv"

# A verbatim hit shorter than this many spaceless characters is not evidence -- short
# strings of common syllables collide by chance in a 45 MB haystack.
MIN_VERBATIM_CHARS = 14
# A shared contiguous run must clear both an absolute length and a share-of-the-needle
# floor before it counts as adaptation rather than a common collocation.
MIN_RUN_CHARS = 12
MIN_RUN_SHARE = 0.50
# Lesson XLVIII is not exercise prose at all: all 18 of its rows are letter + exemplar-word
# pairs from Bühler's writing chart ("अ अक्ष", "ई ईक्ष्"). Filtering it by *lesson* rather
# than by string length is the honest cut -- a length floor kept "ṣa ṣaṭtriṃśat" (12 chars)
# while dropping it, i.e. it was splitting one homogeneous list on an irrelevant axis.
NON_PROSE_LESSONS = {"XLVIII"}
MIN_SENTENCE_CHARS = 9
MIN_SENTENCE_TOKENS = 2
TOP_K = 3


def keys(iast: str) -> tuple[str, str]:
    """(k_norm, k_fold) for a piece of IAST text."""
    return su.norm(iast), su.nfold(iast)


def spaceless(s: str) -> str:
    return "".join(s.split())


class Haystack:
    """One concatenated corpus string + offset->row mapping, for fast substring search."""

    def __init__(self) -> None:
        self.buf: list[str] = []
        self.offsets: list[int] = []
        self.rows: list[dict] = []
        self._pos = 0

    def add(self, text_fold: str, row: dict) -> None:
        if not text_fold:
            return
        self.offsets.append(self._pos)
        self.rows.append(row)
        self.buf.append(text_fold)
        self.buf.append("\x00")  # separator: cannot occur inside a match
        self._pos += len(text_fold) + 1

    def build(self) -> None:
        self.hay = "".join(self.buf)
        self.buf = []

    def find_all(self, needle: str, cap: int = 8) -> list[dict]:
        out, start = [], 0
        while len(out) < cap:
            i = self.hay.find(needle, start)
            if i < 0:
                break
            j = bisect.bisect_right(self.offsets, i) - 1
            out.append(self.rows[j])
            start = i + 1
        return out


APPARATUS_PATTERNS = (
    # root + conjugation-class + pada: "mā III. Ā", "viṣ III. P. Ā"
    (re.compile(r"\b(?:I|II|III|IV|V|VI|VII|VIII|IX|X)\.?\s*(?:P|Ā|U)\b"), "root+class"),
    # bare grammatical labels: "Part. praes. Ātm", "Ind. pr. par.", "N. V. viśvapāḥ"
    (re.compile(r"\b(?:Ind|pr|praes|par|parasm|Ātm|impf|Perf|Aor|Fut|Pass|Caus|Des|Opt|"
                r"Imp|Pot|sg|du|pl|N|A|G|L|I|D|Ab|V|Part|Nom|Acc|Gen|Loc|Instr|Dat|Abl|"
                r"Voc)\.\s"), "grammatical label"),
    # derivation / alternation pairs: "dhū -- dhuva", "guṇa - e"
    (re.compile(r"\s--?\s"), "derivation pair"),
)


def classify_apparatus(text: str) -> str | None:
    """Return an apparatus subtype, or None if this looks like real prose.

    Bühler's IAST entries are overwhelmingly *grammatical apparatus* -- root lists with
    conjugation classes, case labels, sandhi demonstration pairs, guṇa tables -- not
    exercise sentences. Running provenance over them would manufacture a ~99 % "invented"
    figure that looks like a finding and is an artefact of the input. They are classified
    out here and reported separately (H1344).
    """
    for rx, label in APPARATUS_PATTERNS:
        if rx.search(text):
            return label
    if len(text.split()) < 3:
        return "fragment"
    return None


def load_buhler(scripts: tuple[str, ...] = ("deva",)) -> list[dict]:
    data = json.loads(SENTENCES.read_text(encoding="utf-8"))
    out = []
    for s in data:
        if s.get("book") != "buhler" or s.get("script") not in scripts:
            continue
        iast = su.deva_to_iast(s["text"]) if s["script"] == "deva" else s["text"]
        k_norm, k_fold = keys(iast)
        out.append(
            {
                "id": s["id"],
                "lesson": s.get("lesson"),
                "script": s["script"],
                "apparatus": classify_apparatus(iast) if s["script"] == "iast" else None,
                "deva": s["text"] if s["script"] == "deva" else "",
                "iast": iast,
                "k_norm": k_norm,
                "k_fold": k_fold,
                "sl_norm": spaceless(k_norm),
                "sl_fold": spaceless(k_fold),
                "tokens": [t for t in k_fold.split() if t],
            }
        )
    return out


def gretil_title(stem: str) -> str:
    """'sa_azvaghoSa-buddhacarita-alt' -> 'Aśvaghoṣa, buddhacarita (alt)'-ish label."""
    s = stem[3:] if stem.startswith("sa_") else stem
    return s.replace("-", " · ")


def load_gretil(base: Path, hay: "Haystack", rows: list[dict]) -> int:
    """Add GRETIL plaintext verse lines. Returns the number of lines added.

    Each file carries a header terminated by a '# Text' marker; everything after it is the
    body, one verse-line per line. Editorial preamble occasionally follows the marker in
    English -- left in rather than heuristically stripped, since an English line cannot
    match a Sanskrit needle anyway; a hit would be visible in the evidence snippet.
    """
    n = 0
    for d in GRETIL_DIRS:
        dirp = base / d
        if not dirp.is_dir():
            continue
        section = d.replace("gretil_", "").replace("_raw", "")
        for fp in sorted(dirp.glob("*.txt")):
            try:
                raw = fp.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            i = raw.find("# Text")
            body = raw[i + 6:] if i >= 0 else raw
            title = gretil_title(fp.stem)
            for ln in body.splitlines():
                ln = ln.strip()
                if len(ln) < 8 or ln.startswith(("#", "##")):
                    continue
                k_norm, k_fold = keys(ln)
                row = {
                    "corpus": "gretil",
                    "ref": f"GRETIL {section}: {title}",
                    "text": ln,
                    "k_norm": k_norm,
                    "k_fold": k_fold,
                    "sl_norm": spaceless(k_norm),
                    "sl_fold": spaceless(k_fold),
                    "cite": f"GRETIL {fp.stem}",
                }
                hay.add(row["sl_fold"], row)
                rows.append(row)
                n += 1
    return n


def load_corpora(db: Path, archive: Path, gretil: Path | None = None) -> tuple[Haystack, list[dict]]:
    """Returns (haystack over both corpora, list of corpus rows for the token index)."""
    hay = Haystack()
    rows: list[dict] = []

    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    prov = dict(con.execute("SELECT key, value FROM provenance").fetchall())
    if not prov:
        sys.exit("ERROR: DCS master has no provenance pin -- refusing (C3 §2.1)")
    print(f"[dcs] provenance: {prov.get('source_repo')} @ {str(prov.get('source_commit'))[:12]}"
          f" imported {prov.get('imported_at')}")

    q = """SELECT s.sent_id, s.text_sandhied, t.name, c.ref
             FROM sentence s
             JOIN chapter c ON c.chapter_id = s.chapter_id
             JOIN text t    ON t.text_id = c.text_id
            WHERE s.text_sandhied IS NOT NULL AND s.text_sandhied <> ''"""
    n = 0
    for sent_id, text, tname, ref in con.execute(q):
        k_norm, k_fold = keys(text)
        row = {
            "corpus": "dcs",
            "ref": f"{tname} {ref}".strip(),
            "text": text,
            "k_norm": k_norm,
            "k_fold": k_fold,
            "sl_norm": spaceless(k_norm),
            "sl_fold": spaceless(k_fold),
            "cite": f"DCS sent_id {sent_id}",
        }
        hay.add(row["sl_fold"], row)
        rows.append(row)
        n += 1
    con.close()
    print(f"[dcs] {n:,} sentences")

    con = sqlite3.connect(f"file:{archive}?mode=ro", uri=True)
    m = 0
    for sid, deva, iast, attrib in con.execute(
        "SELECT saying_id, text_sa_deva, text_sa_iast, source_attribution FROM subhashita"
    ):
        text = iast or (su.deva_to_iast(deva) if deva else "")
        if not text:
            continue
        k_norm, k_fold = keys(text)
        row = {
            "corpus": "sprueche",
            "ref": (attrib or "").strip() or "Böhtlingk, Indische Sprüche",
            "text": text,
            "k_norm": k_norm,
            "k_fold": k_fold,
            "sl_norm": spaceless(k_norm),
            "sl_fold": spaceless(k_fold),
            "cite": f"IS {sid}",
        }
        hay.add(row["sl_fold"], row)
        rows.append(row)
        m += 1
    con.close()
    print(f"[sprueche] {m:,} sayings")

    if gretil is not None:
        g = load_gretil(gretil, hay, rows)
        print(f"[gretil] {g:,} verse lines (CC BY-NC-SA, read-only, never committed)")

    hay.build()
    return hay, rows


def build_index(rows: list[dict], vocab: set[str]) -> tuple[dict[str, list[int]], dict[str, int]]:
    """Postings for needle-vocabulary tokens only + document frequencies."""
    post: dict[str, list[int]] = {t: [] for t in vocab}
    df: dict[str, int] = {t: 0 for t in vocab}
    for i, r in enumerate(rows):
        seen = set()
        for tok in r["k_fold"].split():
            if tok in post and tok not in seen:
                seen.add(tok)
                post[tok].append(i)
                df[tok] += 1
    return post, df


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", type=Path, default=DEFAULT_DB)
    ap.add_argument("--archive", type=Path, default=DEFAULT_ARCHIVE)
    ap.add_argument("--limit", type=int, default=0, help="debug: only first N sentences")
    ap.add_argument("--gretil", type=Path, default=DEFAULT_GRETIL,
                    help="dir holding the gretil_*_raw plaintext dirs")
    ap.add_argument("--no-gretil", action="store_true",
                    help="DCS + Indische Sprüche only (reproduces the H1212 first pass)")
    ap.add_argument("--scripts", default="deva",
                    help="comma-separated: deva, iast, or deva,iast (default deva)")
    args = ap.parse_args()

    needles = load_buhler(tuple(x.strip() for x in args.scripts.split(",")))
    if args.limit:
        needles = needles[: args.limit]
    from collections import Counter as _C
    _sc = _C(n["script"] for n in needles)
    print(f"[buhler] {len(needles)} entries ({dict(_sc)})")

    hay, rows = load_corpora(args.db, args.archive,
                             None if args.no_gretil else args.gretil)
    N = len(rows)

    vocab = {t for nd in needles for t in nd["tokens"]}
    post, df = build_index(rows, vocab)
    print(f"[index] {len(vocab):,} needle tokens indexed over {N:,} corpus rows")

    import math

    idf = {t: math.log(N / (1 + df[t])) for t in vocab}

    results = []
    for nd in needles:
        rec = {
            "id": nd["id"],
            "lesson": nd["lesson"],
            "script": nd["script"],
            "apparatus": nd["apparatus"],
            "deva": nd["deva"],
            "iast": nd["iast"],
            "n_tokens": len(nd["tokens"]),
            "n_chars": len(nd["sl_fold"]),
        }

        # --- detector 1: spaceless verbatim -------------------------------------
        hits = hay.find_all(nd["sl_fold"]) if len(nd["sl_fold"]) >= 4 else []
        verbatim = []
        for h in hits:
            # confirm on the stricter key (m/n distinct) where possible
            strict = nd["sl_norm"] in h["sl_norm"]
            verbatim.append(
                {
                    "corpus": h["corpus"],
                    "ref": h["ref"],
                    "cite": h["cite"],
                    "text": h["text"],
                    "strict": strict,
                }
            )

        # --- detector 2: IDF-weighted containment -------------------------------
        total_idf = sum(idf[t] for t in set(nd["tokens"])) or 1e-9
        cand: dict[int, float] = {}
        for t in set(nd["tokens"]):
            w = idf[t]
            for i in post[t]:
                cand[i] = cand.get(i, 0.0) + w
        best = sorted(cand.items(), key=lambda kv: -kv[1])[:TOP_K]
        near = []
        for i, mass in best:
            r = rows[i]
            near.append(
                {
                    "corpus": r["corpus"],
                    "ref": r["ref"],
                    "cite": r["cite"],
                    "text": r["text"],
                    "containment": round(mass / total_idf, 3),
                    "idf_mass": round(mass, 2),
                }
            )

        # --- detector 3: longest attested contiguous token run ------------------
        run = None
        toks = nd["k_fold"].split()
        toks_strict = nd["k_norm"].split()
        for n in range(len(toks) - 1, 1, -1):          # n-grams of >= 2 tokens
            if run:
                break
            for i in range(0, len(toks) - n + 1):
                probe = spaceless(" ".join(toks[i : i + n]))
                if len(probe) < MIN_RUN_CHARS:
                    continue
                # A run must survive the STRICT key too. nfold collapses every nasal to n,
                # which manufactures phantom runs: Bühler's "janānāṃ dhanaṃ" folds onto the
                # unrelated "yājamānaṃ dhānaṃjayyaḥ". Requiring the m/n-distinct form to
                # match as well removes that whole class of false positive.
                strict_probe = spaceless(" ".join(toks_strict[i : i + n]))
                hits_r = [h for h in hay.find_all(probe, cap=6)
                          if strict_probe in h["sl_norm"]]
                if hits_r:
                    h = hits_r[0]
                    run = {
                        "n_run_tokens": n,
                        "run_iast": " ".join(toks[i : i + n]),
                        "run_chars": len(probe),
                        "share": round(len(probe) / max(1, len(nd["sl_fold"])), 3),
                        "corpus": h["corpus"],
                        "ref": h["ref"],
                        "cite": h["cite"],
                        "text": h["text"],
                    }
                    break

        # --- verdict ------------------------------------------------------------
        n_chars = rec["n_chars"]
        if (
            nd["lesson"] in NON_PROSE_LESSONS
            or nd["apparatus"]
            or n_chars < MIN_SENTENCE_CHARS
            or rec["n_tokens"] < MIN_SENTENCE_TOKENS
        ):
            # alphabet/writing-chart rows and grammatical apparatus, not exercise prose
            rec["verdict"] = "not-a-sentence"
            rec["confidence"] = "high"
        elif verbatim and n_chars >= MIN_VERBATIM_CHARS:
            rec["verdict"] = "quotation"
            rec["confidence"] = "high" if any(v["strict"] for v in verbatim) else "medium"
        elif verbatim:
            rec["verdict"] = "unknown"
            rec["confidence"] = "low"
            rec["note"] = f"verbatim hit but only {n_chars} chars (< {MIN_VERBATIM_CHARS})"
        elif (
            run
            and run["run_chars"] >= MIN_RUN_CHARS
            and run["share"] >= MIN_RUN_SHARE
            # A bare two-word run is a collocation, not a borrowing, unless it carries most
            # of the sentence: "duḥkhaṃ bhavati" is attested everywhere and means nothing.
            and (run["n_run_tokens"] >= 3 or run["share"] >= 0.70)
        ):
            rec["verdict"] = "adapted"
            rec["confidence"] = "medium" if run["share"] >= 0.7 else "low"
        else:
            rec["verdict"] = "invented"
            rec["confidence"] = "medium"
        rec["longest_run"] = run

        rec["verbatim_hits"] = verbatim[:3]
        rec["near_hits"] = near
        results.append(rec)

    OUT_JSON.write_text(
        json.dumps(results, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    with OUT_CSV.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(
            ["id", "lesson", "deva", "iast", "verdict", "confidence",
             "n_tokens", "n_chars", "top_containment", "top_ref", "top_cite", "top_text"]
        )
        for r in results:
            t = r["verbatim_hits"][0] if r["verbatim_hits"] else (r["near_hits"][0] if r["near_hits"] else None)
            w.writerow(
                [r["id"], r["lesson"], r["deva"], r["iast"], r["verdict"], r["confidence"],
                 r["n_tokens"], r["n_chars"],
                 (r["near_hits"][0]["containment"] if r["near_hits"] else ""),
                 (t or {}).get("ref", ""), (t or {}).get("cite", ""), (t or {}).get("text", "")]
            )

    from collections import Counter

    tally = Counter(r["verdict"] for r in results)
    denom = len(results) - tally.get("not-a-sentence", 0)
    print(f"\n[verdicts] {denom} exercise sentences "
          f"({tally.get('not-a-sentence', 0)} alphabet/root drill rows excluded)")
    for k in ("quotation", "adapted", "invented", "unknown"):
        print(f"  {k:10s} {tally.get(k, 0):4d}  ({tally.get(k, 0) / denom:.1%})")
    print(f"\nwrote {OUT_JSON}\nwrote {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
