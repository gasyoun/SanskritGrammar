#!/usr/bin/env python
"""privative_noun_abstractness.py — a-/an- privative noun check for HK-42.

HK-42: "Не менее трети всех префиксальных существительных составляют
существительные, образованные по модели a- + S. Из них большинство (около
80%) — наименования абстрактных понятий." Two separate empirical claims:

  (1) a-/an- privative nouns are >= 1/3 of ALL prefixed nouns — stays
      UNTESTABLE: this needs a reliable total "prefixed nouns" denominator,
      which hit the same wall as HK-225/229 (H1047) — no genuine
      morphological segmentation available, only noisy prefix-string
      matching. NOT re-attempted here.

  (2) of the a-/an- privative nouns specifically, ~80% are ABSTRACT
      concepts — THIS part is newly tractable, reusing two pieces of
      infrastructure already built this session:
        - privative-noun IDENTIFICATION: unlike general preverbs, a-/an-
          privative is validated against DCS's OWN noun-lemma inventory
          (does the candidate's base, after stripping a-/an-, exist as its
          own independent NOUN lemma?) — far less noisy than the verb-
          preverb problem, since DCS's noun lemmas are the reference set,
          not an external (necessarily incomplete) root list.
        - ABSTRACT classification: the same Sanskrit-WordNet sembank
          (word-senses.csv + sembank-relations.csv) used for
          animacy_lookup.py, rooted instead at "abstraction" (id 584,
          WordNet Tops) and "psychological feature" (id 583, WordNet
          Tops) — mental/conceptual states like "fearlessness",
          "non-desire" belong here, not under "abstraction" narrowly.

RESULT: INCONCLUSIVE, a third confound found and documented (not hidden).
The candidate-IDENTIFICATION step itself is contaminated: "does the base
(after stripping a-/an-) exist as its own independent noun lemma" passes
for many words that are NOT felt as productive negations at all —
asura ("demon") = a- + sura ("god"), and sura genuinely IS an independent
lemma, but "asura" is a LEXICALIZED word (a class of beings) in Classical
Sanskrit, not synchronically parsed as "non-god." Same for agni ("fire")
+ gni, aja ("goat") + ja, ahi ("snake") + hi, amṛta ("nectar") + mṛta —
all pattern-match structurally but are lexicalized, not compositional.
A minimum base-length filter does not fix this (sura is 4 letters, a
perfectly ordinary word length) — this is a semantic-transparency problem,
the SAME fundamental kind already deprioritized for HK-226/227 (compositional
vs idiomatic preverb+verb meaning), just discovered via a different
structural pattern. Recorded so it is not re-attempted the same way.

Usage:  python KocherginaUchebnik_1998/privative_noun_abstractness.py [--db PATH] [--lookup-dir PATH]
Writes  hk42_privative_noun_abstractness_stats.json next to this script.
"""
import argparse
import csv
import json
import sqlite3
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
DEFAULT_DB = HERE.parent.parent / "VisualDCS" / "src" / "DCS-data-2026" / "dcs_full.sqlite"
DEFAULT_LOOKUP = HERE.parent.parent / "dcs-conllu" / "lookup"

ABSTRACT_ROOTS = {584, 583, 585, 592, 597, 598, 593, 594, 602}
# abstraction, psychological_feature, knowledge, state, attribute, relation,
# event, act, phenomenon (WordNet Tops). First pass used only {584, 583} and
# got 30.6% abstract — the opposite of Kochergina's ~80% claim. Spot-checking
# the "concrete"-classified examples caught the same kind of gap the animacy
# tagger hit twice: WordNet's own noun hierarchy has ~21 separate top-level
# "Tops" categories, not a clean concrete/abstract binary rooted at just
# "abstraction". "anāhāra" (fasting) was tagged under act(594, "something
# people do"), "aruci" (a disease/state) under state-like categories — both
# are ABSTRACT nouns in the traditional grammatical sense (states, actions,
# qualities, relations — not physical objects/beings), but sat outside the
# narrow {584,583} closure and were miscounted as "concrete." Expanded to
# all WordNet Tops nodes that traditional grammar would call abstract
# (quality/state/action/relation), leaving person/animal/plant/object/
# substance/food/article/location/group/possession as the concrete side.
NON_VOWEL_START = set("kgcjṭḍtdpbśṣshyvrlmnṇñṅ")


def build_closure(lookup_dir, roots):
    children = defaultdict(list)
    with (lookup_dir / "sembank-relations.csv").open(encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) >= 3 and row[2].strip('"') == "~":
                try:
                    children[int(row[0])].append(int(row[1]))
                except ValueError:
                    continue
    closure = set(roots)
    queue = deque(roots)
    while queue:
        node = queue.popleft()
        for c in children.get(node, ()):
            if c not in closure:
                closure.add(c)
                queue.append(c)
    return closure


def find_privative_candidates(noun_lemmas):
    candidates = []
    for l in noun_lemmas:
        if l.startswith("an") and len(l) > 3 and l[2] not in NON_VOWEL_START and l[2:] in noun_lemmas:
            candidates.append((l, l[2:], "an-"))
        elif l.startswith("a") and len(l) > 2 and l[1] in NON_VOWEL_START and l[1:] in noun_lemmas:
            candidates.append((l, l[1:], "a-"))
    return candidates


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--lookup-dir", default=str(DEFAULT_LOOKUP))
    args = ap.parse_args()
    lookup_dir = Path(args.lookup_dir)

    abstract_ids = build_closure(lookup_dir, ABSTRACT_ROOTS)
    print(f"abstract sense-id closure: {len(abstract_ids)} ids "
          f"(rooted at abstraction=584, psychological_feature=583)")

    db = sqlite3.connect(args.db)
    cur = db.cursor()
    noun_lemmas = set(l for (l,) in cur.execute(
        "SELECT DISTINCT lemma FROM token WHERE upos='NOUN'"))

    candidates = find_privative_candidates(noun_lemmas)
    print(f"a-/an- privative noun candidates (base is itself a real noun lemma): "
          f"{len(candidates)}")

    priv_lemmas = [c[0] for c in candidates]
    placeholders = ",".join("?" * len(priv_lemmas))
    rows = cur.execute(
        f"SELECT lemma, m_wordsem FROM token WHERE lemma IN ({placeholders}) "
        f"AND upos='NOUN' AND m_wordsem IS NOT NULL", priv_lemmas
    ).fetchall()

    votes = defaultdict(Counter)
    for lemma, wordsem in rows:
        ids = [int(p) for p in wordsem.split(",") if p.strip().isdigit()]
        for sid in ids:
            votes[lemma]["abstract" if sid in abstract_ids else "concrete"] += 1

    classification = {}
    for lemma, v in votes.items():
        ab, co = v["abstract"], v["concrete"]
        cls = "abstract" if ab > co else ("concrete" if co > ab else "tied")
        classification[lemma] = {"abstract_votes": ab, "concrete_votes": co, "classification": cls}

    n_abstract = sum(1 for v in classification.values() if v["classification"] == "abstract")
    n_concrete = sum(1 for v in classification.values() if v["classification"] == "concrete")
    n_tied = sum(1 for v in classification.values() if v["classification"] == "tied")
    classified_total = n_abstract + n_concrete + n_tied
    abstract_share = round(100 * n_abstract / classified_total, 1) if classified_total else None

    out = {
        "instrument": "privative_noun_abstractness.py — part 2 of HK-42 only (the "
                      "abstract-share claim); part 1 (>= 1/3 of ALL prefixed nouns) "
                      "stays UNTESTABLE, same wall as HK-225/229 (H1047), not re-attempted",
        "privative_candidates_total": len(candidates),
        "candidates_sample": candidates[:20],
        "candidates_with_wordsem_classification": classified_total,
        "by_class": {"abstract": n_abstract, "concrete": n_concrete, "tied": n_tied},
        "abstract_share_pct_of_classified": abstract_share,
        "expected_by_hk42_part2": "~80% abstract",
        "part2_status": "INCONCLUSIVE — candidate identification itself is contaminated "
                         "by lexicalized words that structurally pattern-match a-/an- + "
                         "an independent lemma without being felt as productive negations "
                         "(asura='demon'=a-+sura['god'], agni='fire'+gni, aja='goat'+ja, "
                         "ahi='snake'+hi, amṛta='nectar'+mṛta — all real lemma-pairs, none "
                         "genuine privative derivations). A semantic-transparency wall, "
                         "same kind as HK-226/227, not fixable by a length filter "
                         "(checked: candidate count barely changes at min-base-length 4-5)",
        "part1_status": "UNTESTABLE — no reliable total-prefixed-noun denominator (H1047)",
    }
    (HERE / "hk42_privative_noun_abstractness_stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"classified: {classified_total} ({n_abstract} abstract, {n_concrete} concrete, {n_tied} tied)")
    print(f"abstract share: {abstract_share}%")
    print("-> hk42_privative_noun_abstractness_stats.json written")


if __name__ == "__main__":
    main()
