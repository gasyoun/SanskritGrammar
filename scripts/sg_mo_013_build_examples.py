#!/usr/bin/env python3
"""Build the SLP1 text + segmentation for the SG-MO-013 manifest examples from
the pinned DCS master (so the canonical SLP1 copy is corpus-faithful, C4)."""
import sqlite3, sys, json
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
G = Path("C:/Users/user/Documents/GitHub")
con = sqlite3.connect(G / "VisualDCS/src/DCS-data-2026/dcs_full.sqlite"); cur = con.cursor()

# IAST -> SLP1 (longest digraphs first)
PAIRS = [("kh","K"),("gh","G"),("ch","C"),("jh","J"),("ṭh","W"),("ḍh","Q"),
         ("th","T"),("dh","D"),("ph","P"),("bh","B"),("ai","E"),("au","O"),
         ("ā","A"),("ī","I"),("ū","U"),("ṛ","f"),("ṝ","F"),("ḷ","x"),("ḹ","X"),
         ("ṅ","N"),("ñ","Y"),("ṭ","w"),("ḍ","q"),("ṇ","R"),("ś","S"),("ṣ","z"),
         ("ṃ","M"),("ḥ","H"),("a","a"),("i","i"),("u","u"),("e","e"),("o","o"),
         ("k","k"),("g","g"),("c","c"),("j","j"),("t","t"),("d","d"),("n","n"),
         ("p","p"),("b","b"),("m","m"),("y","y"),("r","r"),("l","l"),("v","v"),
         ("s","s"),("h","h")]
def to_slp1(s):
    out=[]; i=0
    while i < len(s):
        for a,b in PAIRS:
            if s.startswith(a,i):
                out.append(b); i+=len(a); break
        else:
            out.append(s[i]); i+=1
    return "".join(out)

# (label, text_name_like, ref, form) -> find the sentence
WANT = [
    ("bhavati", "Agnipurāṇa", "248", "bhavati"),
    ("viśati", "Aṣṭāṅgahṛdayasaṃhitā", "Utt., 12", "viśati"),
    ("gṛhṇāti", "Aṣṭādhyāyī", "4, 4", "gṛhṇāti"),
]
for label, tname, ref, form in WANT:
    row = cur.execute(
        "SELECT s.id, s.text_sandhied, c.ref FROM token t "
        "JOIN sentence s ON s.id=t.sentence_id "
        "JOIN chapter c ON c.chapter_id=s.chapter_id "
        "JOIN text x ON x.text_id=c.text_id "
        "WHERE x.name LIKE ? AND t.form=? AND t.feat_tense='Pres' "
        "AND LENGTH(s.text_sandhied) BETWEEN 20 AND 52 LIMIT 1",
        (f"%{tname}%", form)).fetchone()
    if not row:
        print(f"{label}: NOT FOUND"); continue
    sid, sand, cref = row
    print(f"(chapter ref = {cref!r})")
    toks = cur.execute(
        "SELECT form, m_unsandhied FROM token WHERE sentence_id=? ORDER BY idx", (sid,)).fetchall()
    seg = " ".join((u or f) for f, u in toks if (f or u))
    print(f"=== {label} (sent {sid}) ===")
    print("text_iast:", sand)
    print("text_slp1:", to_slp1(sand))
    print("seg_slp1: ", to_slp1(seg))
