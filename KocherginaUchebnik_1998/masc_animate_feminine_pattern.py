#!/usr/bin/env python
"""masc_animate_feminine_pattern.py — sizing probe for HK-86.

HK-86: "От большинства мужских одушевлённых имён женский род образуется
изменением -a на -ī" — the feminine of most masculine ANIMATE nouns is
formed by changing -a to -ī (as opposed to -ā). Uses animacy_lookup.py's
lemma classification to restrict to animate masc a-stem NOUN lemmas, then
checks each lemma's own feminine-tagged surface forms for a -ī vs -ā
pattern (the same surface-split technique as HB-21's gurvī/guru check).

MAJOR CONFOUND FOUND AND CORRECTED (not hidden): a first pass over ALL
feminine-tagged tokens of these lemmas showed -ā dominating overwhelmingly
(157 lemmas vs 3) — but manual inspection of the raw sentences showed this
was almost entirely BAHUVRĪHI COMPOUND-FINAL AGREEMENT contamination, not
genuine noun-pair derivation: e.g. "putrā" (140 tokens) was overwhelmingly
the tail of compounds like "diti-vinaṣṭa-putrā" ("[Diti] whose sons were
destroyed") or "śūra-putrāṃ" ("whose son is a hero") — a bahuvrīhi
adjective agreeing with a feminine head noun by simple -a->-ā lengthening,
which is a COMPLETELY DIFFERENT phenomenon from simple substantive
gender-pair derivation (devá -> devī́ as its own lexeme). Filtered these
out via the `mwt` table (excluding any token covered by a multi-word
compound span) before re-checking.

RESULT EVEN AFTER FILTERING: -ā still dominates (19 lemmas vs 3), on a
much smaller n=22. This is recorded as an INCONCLUSIVE sizing result, not
a verdict: the residual n is thin, and further confounds (sandhi-external
compounding not captured by `mwt`, genuine lexical alternatives like
duhitṛ 'daughter' competing with putrī/putrā for the same meaning) were
not ruled out given the effort already spent finding and correcting the
first confound. Whether "-ī dominant for animate masc nouns" is genuinely
overstated or whether a cleaner instrument would still confirm it is left
open — recorded so this exact confound isn't rediscovered from scratch.

Usage:  python KocherginaUchebnik_1998/masc_animate_feminine_pattern.py [--db PATH]
Writes  hk86_masc_animate_feminine_stats.json next to this script.
"""
import argparse
import json
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
DEFAULT_ANIMACY = HERE / "animacy_lemma_lookup.json"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--animacy-json", default=str(DEFAULT_ANIMACY))
    args = ap.parse_args()
    db = sqlite3.connect(args.db)
    cur = db.cursor()
    animacy = json.loads(Path(args.animacy_json).read_text(encoding="utf-8"))
    lc = animacy["lemma_classification"]

    masc_a_stems = [l for (l,) in cur.execute(
        "SELECT DISTINCT lemma FROM token WHERE upos='NOUN' AND feat_gender='Masc'")
        if l.endswith("a") and not l.endswith(("ā", "i", "ī", "u", "ū"))]
    animate_masc_a = [l for l in masc_a_stems
                       if lc.get(l, {}).get("classification") == "animate"]

    placeholders = ",".join("?" * len(animate_masc_a))
    rows = cur.execute(
        f"SELECT sentence_id, idx, lemma, form FROM token WHERE lemma IN ({placeholders}) "
        f"AND upos='NOUN' AND feat_gender='Fem'", animate_masc_a
    ).fetchall()
    pre_filter_total = len(rows)

    sent_ids = list({sid for sid, idx, l, f in rows})
    covered = set()
    CHUNK = 500
    for i in range(0, len(sent_ids), CHUNK):
        chunk = sent_ids[i:i + CHUNK]
        ph = ",".join("?" * len(chunk))
        for sid, span in cur.execute(
            f"SELECT sentence_id, span FROM mwt WHERE sentence_id IN ({ph})", chunk
        ):
            if "-" in span:
                a, b = span.split("-")
                for x in range(int(a), int(b) + 1):
                    covered.add((sid, x))

    standalone = [(sid, idx, l, f) for sid, idx, l, f in rows if (sid, idx) not in covered]

    by_lemma = defaultdict(list)
    for sid, idx, l, f in standalone:
        by_lemma[l].append(f)

    ii_lemmas, aa_lemmas, neither = [], [], 0
    for l, forms in by_lemma.items():
        stem = l[:-1]
        ii_tok = sum(1 for f in forms if f.startswith(stem + "ī"))
        aa_tok = sum(1 for f in forms if f.startswith(stem + "ā"))
        if ii_tok == 0 and aa_tok == 0:
            neither += 1
        elif ii_tok > aa_tok:
            ii_lemmas.append((l, ii_tok, aa_tok))
        elif aa_tok > ii_tok:
            aa_lemmas.append((l, ii_tok, aa_tok))

    out = {
        "instrument": "masc_animate_feminine_pattern.py — sizing probe, NOT a settled "
                      "verdict instrument (see docstring: major compound-contamination "
                      "confound found, partially but not fully corrected)",
        "animate_masc_a_stem_lemmas": len(animate_masc_a),
        "feminine_tokens_pre_filter": pre_filter_total,
        "feminine_tokens_standalone_after_mwt_filter": len(standalone),
        "lemmas_with_standalone_feminine_token": len(by_lemma),
        "i_pattern_dominant_lemmas": len(ii_lemmas),
        "a_pattern_dominant_lemmas": len(aa_lemmas),
        "neither_or_tied": neither,
        "i_pattern_examples": ii_lemmas,
        "a_pattern_examples": aa_lemmas,
        "conclusion": "INCONCLUSIVE — -ā pattern dominates even after excluding "
                      "compound-final (mwt-covered) tokens, on a thin n=22 residual; "
                      "further confounds not ruled out given effort already spent on "
                      "the first one. Not registered as a fact verdict.",
    }
    (HERE / "hk86_masc_animate_feminine_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"animate masc a-stem lemmas: {len(animate_masc_a)}")
    print(f"feminine tokens: {pre_filter_total} pre-filter -> "
          f"{len(standalone)} standalone (non-compound)")
    print(f"-ī dominant: {len(ii_lemmas)} lemmas, -ā dominant: {len(aa_lemmas)} lemmas")
    print("-> hk86_masc_animate_feminine_stats.json written (INCONCLUSIVE)")


if __name__ == "__main__":
    main()
