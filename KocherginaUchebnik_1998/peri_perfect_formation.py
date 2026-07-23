#!/usr/bin/env python3
"""H1454 item 9: periphrastic-perfect tokens by stem-FORMATION type.

Question (perfect article, sangram/articles/perfect): how specific is the
periphrastic perfect to CAUSATIVES vs other derived stems (denominatives,
desideratives, intensives) vs plain roots?

Universe: identical to scripts/sg_mo_017_perfect_coverage.py — the pinned
VisualDCS DCS-2021 master (dcs_full.sqlite), finite VERB tokens with
Tense=Past and feat_formation='peri' (N = 4,046).

Formation classes assigned per distinct base stem (= DCS lemma; the -ām part):

  plain_root      lemma.grammar is a plain present class (1.-9. P/Ā), stem
                  does not end in -ay: roots/present-stems taking -ām directly
                  (īkṣ, bhī, vid, ās, hu, epic present-stem type ānī, āhvā...).
  causative       -ay- stem for which a phonologically regular underlying
                  root is independently attested: see OPERATIONAL CRITERION.
  class10_lexical -ay- stem tagged 10.* whose -aya- form is the only
                  dictionary entry (no recoverable independent root):
                  cintay, kathay, pūjay, tāḍay, pīḍay ...
  ambiguous_caus_class10  the genuinely fuzzy causative/class-10 band,
                  reported separately, NOT folded into either side.
  denominative    lemma.grammar 'Denom.*' (mantray, sāntvay, prārthay ...).
                  (No -āya-type denominative lemma, e.g. gopāy-, occurs.)
  desiderative    lemma.grammar 'Desid.*'.
  intensive       lemma.grammar 'Intens.*' — attested count: 0. (jāgṛ, the
                  one historically-intensive stem, is lexicalized as class 2
                  and counted as plain_root, per its DCS/MW annotation.)

OPERATIONAL CRITERION (causative vs class-10 — stated, not hidden):
  DCS's lemma.grammar (from MW-derived dictionary.csv) tags ALL -aya- stems
  '10.*', including transparent causatives (darśay '10.Ā.'), so the DCS
  annotation alone cannot make the split. We therefore classify an -ay- stem
  as CAUSATIVE iff undoing standard causative stem morphology (-p- deletion
  after ā; vṛddhi/guṇa reversal: ār/ar→ṛ, ā→a, o→u, e→i, al→ḷ, āv→u/ū,
  āy→ī; optional preverb stripping) yields a root that EXISTS in the DCS
  lemma inventory with a plain present-class annotation (1.-9. P/Ā).
  A stem whose root is recoverable only via the IDENTITY mapping (the bare
  stem minus -ay is itself listed as a class-1-9 root, e.g. arcay→arc) goes
  to the AMBIGUOUS band: same surface, same sense, no causative semantics
  guaranteed. A small documented override list corrects known false
  positives/negatives of the phonological test (pālay≠pal, varay, janay,
  preṣay ... — each with MW/Whitney evidence). No hit at all → class-10
  lexical.

Outputs (this directory):
  peri_perfect_stem_formation.csv    per-stem: stem, grammar, class, method,
                                     evidence, tokens
  peri_perfect_formation_summary.csv formation class, distinct stems, tokens, %
Never writes into the repo.
"""
import csv
import re
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

DB = Path(r"C:\Users\user\Documents\GitHub\VisualDCS\src\DCS-data-2026\dcs_full.sqlite")
OUT = Path(__file__).resolve().parent
UNIV = ("t.upos = 'VERB' AND t.feat_tense = 'Past' "
        "AND (t.feat_verbform IS NULL OR t.feat_verbform = 'Fin')")

# plain present class 1-9 (P or Ā), not preceded by another digit (excludes 10.)
PLAIN_CLASS = re.compile(r"(?<![0-9])[1-9]\.\s*[PĀ]")

PREVERBS = [
    "abhini", "pratini", "samud", "samut", "samupa", "samā", "vyava", "vyud",
    "abhyā", "anvā", "pratyā", "paryā", "nirā", "adhyā", "upā", "udā",
    "abhi", "adhi", "anu", "antar", "apa", "api", "ava", "ā", "ud", "ut",
    "upa", "ni", "nir", "niṣ", "nis", "parā", "pari", "prati", "pra",
    "sam", "saṃ", "su", "vi", "vy",
]

# ---- documented overrides --------------------------------------------------- #
# (suffix, class, evidence) — matched by endswith, LONGEST suffix wins, so a
# compound (saṃpreṣay, paripālay, pracchāday...) inherits its family's ruling.
OVERRIDES = [
    # -- causative: textbook causatives the phonological test under-reaches --- #
    ("janay", "causative",
     "jan 4.Ā 'be born' -> janayati 'begets' — transparent causative; identity "
     "grade only because medial a takes no strengthening (Whitney §1042e)"),
    ("preṣay", "causative",
     "pra+iṣ (MW s.v. pra-iṣ; iṣ 6.P 'send/impel') -> preṣayati; preverb-fused "
     "root invisible to the bare phonological test"),
    ("pūray", "causative",
     "pṝ 9 'fill' (pūryate) -> pūrayati, standard causative (Whitney §1042)"),
    ("kalpay", "causative",
     "kḷp 1.Ā 'be fit' -> kalpayati 'arranges' (Whitney §1042b)"),
    ("dhāray", "causative",
     "dhṛ -> dhārayati; formally causative (functions as the plain present "
     "'holds' in classical usage, Whitney §1041b)"),
    ("ghātay", "causative",
     "han 2.P 'slay' -> ghātayati, suppletive causative stem (Whitney §1042l)"),
    ("adhyāpay", "causative",
     "adhi+i 2.P 'study' -> adhyāpayati 'teaches': -p- causative on the ā-grade "
     "of i (Whitney §1042m) — unreachable by suffix reversal"),
    ("śamay", "causative",
     "śam 4.P 'become calm' -> śamayati 'calms' (a-vowel unstrengthened)"),
    ("ramay", "causative",
     "ram 1.Ā 'delight in' -> ramayati 'delights (another)' (Whitney §1042)"),
    ("jīvay", "causative",
     "jīv 1.P 'live' -> jīvayati 'revives' (long medial vowel unstrengthened)"),
    ("gamay", "causative",
     "gam 'go' -> gamayati 'causes to go' (Whitney §1042e)"),
    ("kampay", "causative",
     "kamp 1.Ā 'tremble' -> kampayati 'shakes'"),
    ("nanday", "causative",
     "nand 1.P 'rejoice' -> nandayati 'gladdens'"),
    ("dīpay", "causative",
     "dīp 4.Ā 'blaze' -> dīpayati 'kindles'"),
    ("śikṣay", "causative",
     "śikṣ 1.Ā 'learn' (old desid. of śak) -> śikṣayati 'teaches' = 'causes to "
     "learn' (MW caus.)"),
    ("sādhay", "causative",
     "sādh 1/5 'succeed' -> sādhayati 'accomplishes' (MW caus.)"),
    ("samāpay", "causative",
     "sam-āp 5 'complete' -> samāpayati 'brings to an end' (MW caus.)"),
    ("rañjay", "causative",
     "rañj 4.Ā 'be reddened/charmed' -> rañjayati 'colours, delights'"),
    ("dhvaṃsay", "causative",
     "dhvaṃs 1.Ā 'fall to pieces' -> dhvaṃsayati 'destroys' (MW caus.)"),
    ("tvaray", "causative",
     "tvar 1.Ā 'hasten' -> tvarayati 'speeds (another)' (MW caus.)"),
    ("stambhay", "causative",
     "stambh 'become rigid' -> stambhayati 'makes firm' (MW caus.)"),
    ("vañcay", "causative",
     "vañc 1 'move crookedly' -> caus. vañcayati 'deceives' (MW caus., "
     "specialized sense)"),
    ("kāśay", "causative",
     "kāś 1.Ā 'shine' -> (pra)kāśayati 'makes visible' (MW caus.)"),
    ("hlāday", "causative",
     "hlād 1.Ā 'be glad' -> hlādayati 'gladdens' (MW caus.)"),
    ("vyathay", "causative",
     "vyath 1.Ā 'waver' -> vyathayati 'agitates' (Whitney §1042)"),
    # -- class-10 lexical: DCS-inventory anomalies / spurious homophones ------ #
    ("kathay", "class10_lexical",
     "MW kath cl.10 kathayati, denominative of katham (Whitney §1056a); the DCS "
     "inventory row 'kath 4.Ā.' reflects the rare epic middle kathate, not an "
     "independent underived root"),
    ("pīḍay", "class10_lexical",
     "MW pīḍ cl.10 pīḍayati 'press, pain' is the principal formation (cl.1 "
     "pīḍati marginal)"),
    ("tāḍay", "class10_lexical",
     "MW/Dhātupāṭha taḍ curādi (cl.10) tāḍayati only; the DCS inventory row "
     "'taḍ 2.P.' has no MW basis"),
    ("pālay", "class10_lexical",
     "MW pāl 10 = denominative of pāla m. 'guardian'; the automatic hit "
     "pāl->pal (pal 1 'go') is a spurious homophone"),
    ("spṛhay", "class10_lexical",
     "MW spṛh cl.10 spṛhayati 'desire' (denominative type; Whitney §1056)"),
    # -- ambiguous: causative FORM, no causative semantics guaranteed --------- #
    ("varay", "ambiguous_caus_class10",
     "formally guna of vṛ 9 'choose' but varayati itself means 'chooses' (not "
     "'causes to choose'); MW lists vṛ cl.10"),
    ("chāday", "ambiguous_caus_class10",
     "MW chad cl.10 chādayati 'cover' is the principal entry; plain chad "
     "barely attested — boundary case"),
    ("arcay", "ambiguous_caus_class10",
     "arc 1.P arcati 'honour' and arcayati cl.10 same sense — causative form, "
     "non-causative semantics"),
    ("bhakṣay", "ambiguous_caus_class10",
     "MW bhakṣ cl.1 bhakṣati and cl.10 bhakṣayati 'eat' same sense; "
     "denominative origin (bhakṣa) — causative form, plain meaning"),
]
OVERRIDES.sort(key=lambda t: -len(t[0]))          # longest suffix wins


def find_override(stem: str):
    for suf, cls, ev in OVERRIDES:
        if stem == suf or stem.endswith(suf):
            return cls, ev
    return None

GRADE_RULES = [
    # (name, regex on stem tail, replacement) — applied at LAST match
    ("p-caus (ā-p)", re.compile(r"āp$"), lambda m: ""),      # sthāp->sthā (keep ā)
    ("vrddhi ār->ṛ", re.compile(r"ār(?=[^aāiīuūṛeoy]*$)"), "ṛ"),
    ("guna ar->ṛ", re.compile(r"ar(?=[^aāiīuūṛeoy]*$)"), "ṛ"),
    ("guna al->ḷ", re.compile(r"al(?=[^aāiīuūṛeoy]*$)"), "ḷ"),
    ("vrddhi ā->a", re.compile(r"ā(?=[^aāiīuūṛeoy]*$)"), "a"),
    ("guna o->u", re.compile(r"o(?=[^aāiīuūṛeoy]*$)"), "u"),
    ("guna o->ū", re.compile(r"o(?=[^aāiīuūṛeoy]*$)"), "ū"),
    ("guna e->i", re.compile(r"e(?=[^aāiīuūṛeoy]*$)"), "i"),
    ("guna e->ī", re.compile(r"e(?=[^aāiīuūṛeoy]*$)"), "ī"),
    ("vrddhi āv->u", re.compile(r"āv$"), "u"),
    ("vrddhi āv->ū", re.compile(r"āv$"), "ū"),
    ("vrddhi āy->ī", re.compile(r"āy$"), "ī"),
]


def strip_variants(stem: str):
    """Yield the stem plus preverb-stripped variants (up to 2 strips)."""
    seen = {stem}
    frontier = [stem]
    for _ in range(2):
        nxt = []
        for s in frontier:
            for pv in PREVERBS:
                if s.startswith(pv) and len(s) - len(pv) >= 2:
                    r = s[len(pv):]
                    if r not in seen:
                        seen.add(r)
                        nxt.append(r)
        frontier = nxt
    return seen


def graded_candidates(base: str):
    """Yield (candidate_root, rule_name) via causative-grade reversal."""
    for name, rx, repl in GRADE_RULES:
        if name.startswith("p-caus"):
            if base.endswith("āp"):
                yield base[:-1], name           # sthāp -> sthā
            continue
        m = None
        for m in rx.finditer(base):
            pass                                 # last match
        if m:
            cand = base[:m.start()] + (repl if isinstance(repl, str) else "") + base[m.end():]
            if cand != base:
                yield cand, name
    if base.endswith("arp"):
        yield base[:-3] + "ṛ", "p-caus (arp->ṛ)"  # arpay -> ṛ


def main() -> int:
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # full lemma inventory: lemma -> concatenated grammar strings
    lemma_gram = defaultdict(list)
    for lem, gr in cur.execute("SELECT lemma, grammar FROM lemma"):
        if gr:
            lemma_gram[lem].append(gr)

    def plain_class_root(cand: str):
        """Return grammar string if cand is listed with a plain class 1-9."""
        for g in lemma_gram.get(cand, []):
            if PLAIN_CLASS.search(g):
                return g
        return None

    # peri tokens grouped by lemma
    stem_tokens = Counter()
    stem_gram = defaultdict(set)
    for lem, gr, n in cur.execute(
            f"SELECT t.lemma, l.grammar, COUNT(*) FROM token t "
            f"JOIN lemma l ON l.lemma_id = t.lemma_id "
            f"WHERE {UNIV} AND t.feat_formation = 'peri' "
            f"GROUP BY t.lemma, l.grammar"):
        stem_tokens[lem] += n
        stem_gram[lem].add(gr or "")
    total = sum(stem_tokens.values())
    print(f"peri tokens: {total} · distinct base stems: {len(stem_tokens)}")

    rows = []
    for stem, n in stem_tokens.most_common():
        gram = ";".join(sorted(stem_gram[stem]))
        cls = method = evidence = ""

        if "Desid" in gram:
            cls, method, evidence = "desiderative", "dcs-grammar", gram
        elif "Intens" in gram:
            cls, method, evidence = "intensive", "dcs-grammar", gram
        elif "Denom" in gram:
            cls, method = "denominative", "dcs-grammar"
            evidence = gram + ("" if stem.endswith("ay") else " [non--ay- stem]")
        elif not stem.endswith("ay"):
            cls, method, evidence = "plain_root", "dcs-grammar", gram
        else:
            # -ay- stem tagged 10.* (or mixed): causative vs class-10 split
            base = stem[:-2]                    # drop 'ay'
            hit_graded = hit_identity = None
            for variant in strip_variants(base):
                g = plain_class_root(variant)
                if g and hit_identity is None:
                    hit_identity = (variant, "identity" +
                                    ("" if variant == base else f" (preverb-stripped {base}->{variant})"), g)
                for cand, rule in graded_candidates(variant):
                    g2 = plain_class_root(cand)
                    if g2 and hit_graded is None:
                        pfx = "" if variant == base else f"strip {base}->{variant}; "
                        hit_graded = (cand, pfx + rule, g2)
            if hit_graded:
                cls, method = "causative", "root-recovery"
                evidence = f"{hit_graded[1]}: {hit_graded[0]} ({hit_graded[2]})"
            elif hit_identity:
                cls, method = "ambiguous_caus_class10", "root-recovery(identity)"
                evidence = f"{hit_identity[1]}: {hit_identity[0]} ({hit_identity[2]})"
            else:
                cls, method = "class10_lexical", "root-recovery(no-hit)"
                evidence = f"no independent root recoverable; own entry {gram}"

        ov = find_override(stem) if stem.endswith("ay") and cls not in (
            "denominative", "desiderative", "intensive", "plain_root") else None
        if ov:
            ocls, oev = ov
            if ocls != cls:
                method = f"override (auto was {cls}/{method})"
            else:
                method = f"override-confirmed ({method})"
            cls, evidence = ocls, oev
        rows.append([stem, gram, cls, method, evidence, n])

    # ---- write per-stem CSV ---- #
    with open(OUT / "peri_perfect_stem_formation.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["base_stem", "dcs_lemma_grammar", "formation_class",
                    "method", "evidence", "tokens"])
        w.writerows(rows)

    # ---- summary ---- #
    cls_tokens = Counter()
    cls_stems = Counter()
    for stem, gram, cls, method, ev, n in rows:
        cls_tokens[cls] += n
        cls_stems[cls] += 1

    order = ["causative", "class10_lexical", "ambiguous_caus_class10",
             "denominative", "plain_root", "desiderative", "intensive"]
    with open(OUT / "peri_perfect_formation_summary.csv", "w", newline="",
              encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["formation_class", "distinct_stems", "tokens", "pct_of_peri"])
        for cls in order:
            w.writerow([cls, cls_stems.get(cls, 0), cls_tokens.get(cls, 0),
                        round(100 * cls_tokens.get(cls, 0) / total, 2)])
        w.writerow(["TOTAL", sum(cls_stems.values()), total, 100.0])

    print(f"\n{'formation class':26} {'stems':>6} {'tokens':>7} {'%':>7}")
    for cls in order:
        print(f"{cls:26} {cls_stems.get(cls, 0):6d} {cls_tokens.get(cls, 0):7d} "
              f"{100 * cls_tokens.get(cls, 0) / total:7.2f}")
    print(f"{'TOTAL':26} {sum(cls_stems.values()):6d} {total:7d} {100.0:7.2f}")

    # sanity: top stems vs published table
    expect = {"cintay": 200, "preṣay": 184, "pūjay": 160, "janay": 159,
              "darśay": 131, "kathay": 125, "pātay": 105, "vāray": 102,
              "kāray": 91, "chāday": 87, "sthāpay": 76}
    bad = {k: (stem_tokens.get(k), v) for k, v in expect.items()
           if stem_tokens.get(k) != v}
    print("\nsanity vs periphrastic_perfect.csv top stems:",
          "OK" if not bad else f"MISMATCH {bad}")
    print("sanity total:", "OK (4046)" if total == 4046 else f"DELTA: {total}")

    # show the classified top-25 for eyeballing
    print("\ntop 25 stems:")
    for stem, gram, cls, method, ev, n in rows[:25]:
        print(f"  {stem:14} {n:4d}  {cls:24} {method}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
