"""Deterministic mini-DCS fixture for the SG-MO-021 golden/integration tests.

Builds a tiny SQLite database with the same table/column surface the generator
reads (token/sentence/chapter/text/provenance), filled with a fixed row set so
every count, distribution, top-form list, and the seeded sample are stable and
hand-checkable. The real DCS master stays off-Git (C0 rule); CI exercises the
generator through this fixture only.

Row plan (all numbers hand-derived and asserted in test_sg_mo_021_golden.py):

    form            lemma  n  person number mood formation kind
    kariṣyāmi       kṛ    14   1     Sing   Ind  -         simple future
    bhaviṣyati      bhū   13   3     Sing   Ind  -         simple future
    bhavitā         bhū   11   3     Sing   Ind  peri      periphrastic future
    gamiṣyāmi       gam    9   1     Sing   Ind  -         simple future
    vakṣyasi        vac    8   2     Sing   Ind  -         simple future
    bhaviṣyanti     bhū    7   3     Plur   Ind  -         simple future
    akariṣyat       kṛ     5   3     Sing   Cond -         conditional
    kartāsmi        kṛ     4   1     Sing   Ind  peri      periphrastic future
    syāt            as     2   3     Sing   Pot  -         potential within Fut
    (NULL form)     dā     1   3     Sing   Ind  -         counted, not top-listed

    future participles (VerbForm=Part & Tense=Fut, outside FIN):          4
    finite non-future controls (in FIN, not Fut):                          6
    infinitive control (upos=VERB, person NULL -> outside FIN):            1

Derived totals: finite_total 80 · finite_future 74 · simple 59 ·
periphrastic 15 · conditional 5 · potential 2 · future_participle 4 ·
person 1/2/3 = 27/8/39 · number Sing/Plur = 67/7 · top-form counts strictly
descending (14,13,11,9,8,7,5,4,2) so GROUP BY ordering is tie-free and the
goldens are engine-order independent. 74 future ids > SAMPLE_SIZE, so the
seeded sampler takes its primary ``sample(n=50)`` path.
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

PROVENANCE_ROWS = [
    ("source_repo", "gasyoun/dcs-conllu (OliverHellwig/sanskrit)"),
    ("source_commit", "04e0778d3dc971030229179e25eea043d06ff397"),
    ("imported_at", "2026-06-06T16:22:57+00:00"),
]

_TEXTS = [(1, "Fixture Text A")]
_CHAPTERS = [(1, "F1.1", 1), (2, "F1.2", 1)]
_SENTENCES = [(1, 1, 1), (2, 2, 1), (3, 1, 2)]

# (form, unsandhied, lemma, person, number, tense, mood, formation, verbform)
_FUT_SIMPLE = [
    * [("kariṣyāmi", "kariṣyāmi", "kṛ", "1", "Sing", "Fut", "Ind", None, "Fin")] * 14,
    * [("bhaviṣyati", "bhaviṣyati", "bhū", "3", "Sing", "Fut", "Ind", None, "Fin")] * 13,
    * [("gamiṣyāmi", "gamiṣyāmi", "gam", "1", "Sing", "Fut", "Ind", None, "Fin")] * 9,
    * [("vakṣyasi", "vakṣyasi", "vac", "2", "Sing", "Fut", "Ind", None, "Fin")] * 8,
    * [("bhaviṣyanti", "bhaviṣyanti", "bhū", "3", "Plur", "Fut", "Ind", None, "Fin")] * 7,
    * [("akariṣyat", "akariṣyat", "kṛ", "3", "Sing", "Fut", "Cond", None, "Fin")] * 5,
    ("syāt", "syāt", "as", "3", "Sing", "Fut", "Pot", None, "Fin"),
    ("syāt", "syāt", "as", "3", "Sing", "Fut", "Pot", None, "Fin"),
    # NULL m_unsandhied: counted in denominators/person/mood, excluded from top lists
    (None, None, "dā", "3", "Sing", "Fut", "Ind", None, "Fin"),
]

_FUT_PERI = [
    * [("bhavitā", "bhavitā", "bhū", "3", "Sing", "Fut", "Ind", "peri", "Fin")] * 11,
    * [("kartāsmi", "kartāsmi", "kṛ", "1", "Sing", "Fut", "Ind", "peri", "Fin")] * 4,
]

_FUTURE_NONFINITE_PARTICIPLE = [
    ("kariṣyant-", "kariṣyant", "kṛ", None, "Sing", "Fut", None, None, "Part"),
    ("kariṣyantau", "kariṣyantau", "kṛ", None, "Dual", "Fut", None, None, "Part"),
    ("bhaviṣyat", "bhaviṣyat", "bhū", None, "Sing", "Fut", None, None, "Part"),
    ("gamiṣyant-", "gamiṣyant", "gam", None, "Plur", "Fut", None, None, "Part"),
]

_CONTROLS = [
    # finite NON-future: exercise the FIN denominator but never enter Fut blocks
    ("karoti", "karoti", "kṛ", "3", "Sing", "Pres", "Ind", None, "Fin"),
    ("kurvanti", "kurvanti", "kṛ", "3", "Plur", "Pres", "Ind", None, "Fin"),
    ("abhavat", "abhavat", "bhū", "3", "Sing", "Impf", "Ind", None, "Fin"),
    ("āste", "āste", "ās", "3", "Sing", "Pres", "Fin", None, "Fin"),
    ("dadāti", "dadāti", "dā", "3", "Sing", "Pres", "Ind", None, "Fin"),
    ("arocayat", "arocayat", "ruc", "3", "Sing", "Impf", "Ind", None, "Fin"),
    # infinitive: upos VERB but person NULL -> outside the FIN universe
    ("vaktum", "vaktum", "vac", None, None, None, None, None, "Inf"),
]


def build_dcs_fixture(path: Path) -> Path:
    """Create the deterministic fixture database at ``path`` and return it."""
    path = Path(path)
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    try:
        cur = con.cursor()
        cur.executescript(
            """
            CREATE TABLE provenance (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE text (text_id INTEGER PRIMARY KEY, name TEXT NOT NULL);
            CREATE TABLE chapter (
                chapter_id INTEGER PRIMARY KEY,
                ref TEXT,
                text_id INTEGER REFERENCES text(text_id)
            );
            CREATE TABLE sentence (
                id INTEGER PRIMARY KEY,
                sent_counter INTEGER,
                chapter_id INTEGER REFERENCES chapter(chapter_id)
            );
            CREATE TABLE token (
                id INTEGER PRIMARY KEY,
                form TEXT,
                m_unsandhied TEXT,
                lemma TEXT,
                upos TEXT,
                feat_person TEXT,
                feat_number TEXT,
                feat_tense TEXT,
                feat_mood TEXT,
                feat_formation TEXT,
                feat_verbform TEXT,
                sentence_id INTEGER REFERENCES sentence(id)
            );
            """
        )
        cur.executemany("INSERT INTO provenance VALUES (?, ?)", PROVENANCE_ROWS)
        cur.executemany("INSERT INTO text VALUES (?, ?)", _TEXTS)
        cur.executemany("INSERT INTO chapter VALUES (?, ?, ?)", _CHAPTERS)
        cur.executemany("INSERT INTO sentence VALUES (?, ?, ?)", _SENTENCES)

        rows: list[tuple] = []
        tid = 0

        def add(batch):
            nonlocal tid
            for r in batch:
                tid += 1
                form, unsandhied, lemma, person, number, tense, mood, formation, verbform = r
                # deterministic rotation over the three sentences
                sentence_id = (tid % 3) + 1
                rows.append(
                    (
                        tid, form, unsandhied, lemma, "VERB", person, number,
                        tense, mood, formation, verbform, sentence_id,
                    )
                )

        add(_CONTROLS)
        add(_FUT_SIMPLE)
        add(_FUT_PERI)
        add(_FUTURE_NONFINITE_PARTICIPLE)
        cur.executemany("INSERT INTO token VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", rows)
        con.commit()
    finally:
        con.close()
    return path
