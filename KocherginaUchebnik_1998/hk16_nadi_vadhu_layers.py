#!/usr/bin/env python
"""H1454 item 4 — frequency layers of the derived feminine i-macron/u-macron type
(nadi/vadhu, Whitney 355-356) in DCS-2026.

Question (MG, Zanjatie XII of METODICHKA_KOCHERGINA_V1_KOMMENTARII_2026.md):
which morphological sources actually supply the feminine -ii/-uu stems a learner
meets in the corpus?  Three expected layers:
  A  suffixal/grammatical formations  (-vatii/-matii, -inii, -trii, -aanii, participial -antii/-atii)
  B  motion feminines from a-/u-stems (devii <- deva; laghvii <- laghu)
  C  primary/lexical feminines        (nadii, vadhuu, strii, lakssmii ...)

Data: VisualDCS/src/DCS-data-2026/dcs_full.sqlite (same DB as scripts/dcs2026_figures.py,
the DCS-2026 standard the repo's ledger numbers use).

Universe: lemma table rows with grammar='f' whose NFC lemma ends in i-macron or
u-macron, counted by NOUN+ADJ tokens in the token table (joined on lemma_id).
Comparison is done on NFC strings throughout (never NFD+strip -- vowel length!).

Classification = string suffix heuristics + a base-lemma existence check against
the full lemma inventory (does deva exist for devii? does yogin exist for yoginii?).
Suffix-shaped lemmas whose base is unattested in the lemma table are reported as
an honest AMBIGUOUS residue, not force-classified.
"""
import csv
import sqlite3
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

DB = Path(r"C:/Users/user/Documents/GitHub/VisualDCS/src/DCS-data-2026/dcs_full.sqlite")
OUT = Path(__file__).resolve().parent

II = "ī"  # i-macron
UU = "ū"  # u-macron
R_VOC = "ṛ"  # r with dot below (vocalic r)

# Curated primary-override: classic textbook primary feminines where an -a homonym
# in the lemma table is a coincidence, not the derivational base (nada 'roarer'
# for nadii; str 'to strew' would trip the -trii rule for strii; laksma for laksmii).
PRIMARY_OVERRIDE = {
    "nadī", "lakṣmī",
}

VOWELS = set("aāiīuūṛṝḷeo")  # NFC vowel characters (ai/au = two chars, still counted)


def nfc(s):
    return unicodedata.normalize("NFC", s)


def main():
    con = sqlite3.connect(str(DB))
    cur = con.cursor()

    # full lemma inventory (any grammar) for base-existence checks
    all_lemmas = defaultdict(set)  # lemma -> set of grammar values
    for lem, gr in cur.execute("SELECT lemma, COALESCE(grammar,'') FROM lemma"):
        all_lemmas[nfc(lem)].add(gr)

    def base_exists(b, grammars=None):
        gs = all_lemmas.get(b)
        if gs is None:
            return False
        if grammars is None:
            return True
        return any(g in gs for g in grammars)

    NOMLIKE = ("m", "adj", "n", "mn", "mf", "fn", "mfn", "")

    # feminine ii/uu lemmas with lemma_ids
    fem = {}  # lemma -> list of lemma_id
    for lid, lem in cur.execute("SELECT lemma_id, lemma FROM lemma WHERE grammar='f'"):
        l = nfc(lem)
        if l.endswith(II) or l.endswith(UU):
            fem.setdefault(l, []).append(lid)

    # token counts per lemma_id (NOUN/ADJ only)
    tok = dict(cur.execute(
        "SELECT lemma_id, COUNT(*) FROM token WHERE upos IN ('NOUN','ADJ') GROUP BY lemma_id"))

    # cross-check bucket: Fem-tagged ii/uu tokens whose lemma is NOT grammar='f'
    fem_ids = {i for ids in fem.values() for i in ids}
    other = 0
    for lid, lem, n in cur.execute(
            "SELECT t.lemma_id, t.lemma, COUNT(*) FROM token t "
            "WHERE t.feat_gender='Fem' AND t.upos IN ('NOUN','ADJ') "
            "GROUP BY t.lemma_id, t.lemma"):
        l = nfc(lem or "")
        if (l.endswith(II) or l.endswith(UU)) and lid not in fem_ids:
            other += n

    def classify(l):
        """Return (layer, subtype, base, base_found)."""
        # R: monosyllabic root nouns (strii, shrii, dhii, bhuu, bhruu ...) —
        # Whitney 348-352 root-word declension, NOT the derived nadii/vadhuu
        # paradigm; excluded from the three layers and reported separately.
        if sum(ch in VOWELS for ch in l) == 1:
            return "R_root", "monosyllabic_root_noun", "", False
        if l in PRIMARY_OVERRIDE:
            return "C_primary", "curated_override", "", False
        if l.endswith(II):
            stem = l[:-1]
            # A: -vatii / -matii  (feminines of -vat/-mat stems)
            if l.endswith("vat" + II) or l.endswith("mat" + II):
                b = stem  # devavat, dhiimat
                if base_exists(b):
                    return "A_suffixal", "vati_mati", b, True
                return "AMBIG", "vati_mati_shape_base_unattested", b, False
            # A: -inii  (feminines of -in stems)
            if l.endswith("in" + II):
                b = stem  # yogin
                if base_exists(b):
                    return "A_suffixal", "ini", b, True
                return "AMBIG", "ini_shape_base_unattested", b, False
            # A: -trii  (feminines of -tr agent nouns)
            if l.endswith("tr" + II) and len(l) >= 5:
                b = l[:-2] + R_VOC  # kartr
                if base_exists(b):
                    return "A_suffixal", "tri", b, True
                # putrii-type: no -tr agent base, but an a-stem base exists -> motion
                b2 = stem + "a"
                if base_exists(b2, NOMLIKE):
                    return "B_motion", "a_stem_motion", b2, True
                return "AMBIG", "tri_shape_base_unattested", b, False
            # A: -aanii type (indraanii <- indra)
            if l.endswith("ān" + II) or l.endswith("āṇ" + II):
                b = l[:-3] + "a"
                if base_exists(b, NOMLIKE):
                    return "A_suffixal", "ani", b, True
            # A: participial -antii/-atii (base = -ant/-at stem)
            if l.endswith("ant" + II) or l.endswith("at" + II):
                b = stem
                if base_exists(b):
                    return "A_suffixal", "anti_ati_participial", b, True
            # B: motion from a-stem (devii <- deva)
            b = stem + "a"
            if base_exists(b, NOMLIKE):
                return "B_motion", "a_stem_motion", b, True
            # B: motion from u-stem (laghvii <- laghu)
            if l.endswith("v" + II):
                b = l[:-2] + "u"
                if base_exists(b, NOMLIKE):
                    return "B_motion", "u_stem_motion", b, True
        else:  # uu-final
            # B(uu): rare motion from u-stem (tanuu-type adj feminines)
            b = l[:-1] + "u"
            if base_exists(b, NOMLIKE):
                return "B_motion", "uu_from_u_stem", b, True
        return "C_primary", "no_derivation_found", "", False

    rows = []
    for l, ids in fem.items():
        n = sum(tok.get(i, 0) for i in ids)
        if n == 0:
            continue  # lexicon-only, never met in corpus
        layer, sub, base, bf = classify(l)
        rows.append((l, layer, sub, base, bf, n))
    rows.sort(key=lambda r: -r[5])

    total = sum(r[5] for r in rows)

    with open(OUT / "nadi_vadhu_lemmas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lemma", "layer", "subtype", "base_lemma", "base_found", "tokens"])
        w.writerows(rows)

    # summary
    agg = defaultdict(lambda: [0, 0, []])
    for l, layer, sub, base, bf, n in rows:
        a = agg[layer]
        a[0] += 1
        a[1] += n
        if len(a[2]) < 5:
            a[2].append(f"{l} ({n})")
    sub_agg = defaultdict(lambda: [0, 0, []])
    for l, layer, sub, base, bf, n in rows:
        a = sub_agg[(layer, sub)]
        a[0] += 1
        a[1] += n
        if len(a[2]) < 5:
            a[2].append(f"{l} ({n})")

    with open(OUT / "nadi_vadhu_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["layer", "distinct_lemmas", "tokens", "pct_of_ii_uu_fem_tokens", "top5_examples"])
        for layer in ("A_suffixal", "B_motion", "C_primary", "AMBIG", "R_root"):
            c, n, ex = agg[layer]
            w.writerow([layer, c, n, f"{100*n/total:.1f}", "; ".join(ex)])
        w.writerow([])
        w.writerow(["layer/subtype", "distinct_lemmas", "tokens", "pct", "top5_examples"])
        for (layer, sub), (c, n, ex) in sorted(sub_agg.items(), key=lambda kv: -kv[1][1]):
            w.writerow([f"{layer}/{sub}", c, n, f"{100*n/total:.1f}", "; ".join(ex)])

    print(f"DB: {DB}")
    print(f"feminine -{II}/-{UU} lemmas in lexicon (grammar='f'): {len(fem)}; "
          f"attested in corpus (NOUN/ADJ tokens>0): {len(rows)}")
    print(f"total NOUN/ADJ tokens of these lemmas: {total}")
    print(f"cross-check: Fem-tagged ii/uu NOUN/ADJ tokens outside grammar='f' lemmas: {other}")
    print()
    print(f"{'layer':12} {'lemmas':>7} {'tokens':>9} {'%':>6}  top-5")
    for layer in ("A_suffixal", "B_motion", "C_primary", "AMBIG", "R_root"):
        c, n, ex = agg[layer]
        print(f"{layer:12} {c:7} {n:9} {100*n/total:6.1f}  {'; '.join(ex)}")
    print()
    print(f"{'layer/subtype':45} {'lemmas':>7} {'tokens':>9} {'%':>6}")
    for (layer, sub), (c, n, ex) in sorted(sub_agg.items(), key=lambda kv: -kv[1][1]):
        print(f"{layer + '/' + sub:45} {c:7} {n:9} {100*n/total:6.1f}  {'; '.join(ex[:3])}")

    # ii vs uu split
    ii_n = sum(r[5] for r in rows if r[0].endswith(II))
    uu_n = total - ii_n
    print(f"\nii-final: {ii_n} tokens ({100*ii_n/total:.1f}%)   uu-final: {uu_n} ({100*uu_n/total:.1f}%)")


if __name__ == "__main__":
    main()
