#!/usr/bin/env python
"""animacy_lookup.py — DCS animacy tagging via the Sanskrit WordNet sembank.

Three UNTESTABLE Kochergina claims (HK-42, HK-86, HK-221) all need animacy
classification (person/animal vs thing/abstract) that DCS's own morphology
doesn't carry directly. What was missing wasn't the DATA — it's the m_wordsem
column, a numeric WordNet-derived semantic-concept ID (per VisualDCS's own
A38 packaging paper) — but a MAPPING from those IDs to a usable category,
which the relational dcs_full.sqlite export doesn't bundle. The mapping
exists in the upstream dcs-conllu mirror's own lookup/ folder, checked
before building anything new (per "check prior art before building"):

  lookup/word-senses.csv       id -> English gloss, WordNet supersense
  lookup/sembank-relations.csv (parent_id, child_id, "~") subclass edges
                                — the WordNet hierarchy the DCS annotation
                                  was built against

ANIMACY = descends from id 574 ("person", WordNet Tops 03, "a human being")
or id 575 ("animal", WordNet Tops 03, "a living organism characterized by
voluntary movement") via the "~" (subclass) relation. id 576 ("plant") is
DELIBERATELY EXCLUDED — grammatical animacy in Sanskrit (одушевлённость)
groups plants with inanimates, not with humans/animals, even though plants
are biologically alive. Homonymous WordNet entries sharing the same English
gloss text at OTHER ids (e.g. id 19759 "plant" = factory, id 25714 "person"
= body) are correctly excluded by using the specific Tops ids, not a text
match on the word "person"/"animal".

A token's m_wordsem can list multiple comma-separated sense ids (polysemy);
a LEMMA is classified by majority vote over all its non-null wordsem-tagged
token occurrences.

Usage:  python KocherginaUchebnik_1998/animacy_lookup.py [--db PATH] [--lookup-dir PATH]
Writes  animacy_lemma_lookup.json next to this script (lemma -> classification).
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

ANIMATE_ROOTS = {574, 575, 42842, 42775}
# person, animal (WordNet Tops); NOT 576 (plant).
# 42842 = "spiritual being" was added after a spot-check found "deva" (god)
# classified inanimate: WordNet's own ontology puts deities under
# causal_agent(573) -> spiritual_being(42842) -> deity(42847) -> Hindu
# deity(42953) -> Deva(102189) — NOT under person(574), since WordNet's
# "person" means specifically "a human being." Sanskrit grammatical
# animacy (одушевлённость) treats deities as animate (they take
# animate-noun agreement), so 42842 is included as a third root without
# pulling in all of 573's much broader "causal agent" branch (natural
# forces, abstract causes, etc., which are NOT grammatically animate).
# 42775 = "imaginary being" was added after a second spot-check found
# "rākṣasa" (demon) classified inanimate: WordNet puts mythical
# monsters/beings (rākṣasa, presumably nāga/gandharva/apsaras-type
# figures too) under an entirely separate branch — concept -> idea ->
# content -> knowledge -> psychological_feature -> ... -> imaginary_being
# -> mythical_being -> mythical_monster — not under entity/causal_agent
# at all, since WordNet treats folkloric beings as conceptual/fictional
# rather than as (even supernaturally) "real" causal agents. Included as
# a fourth root for the same reason as spiritual_being: Sanskrit epic/
# Puranic mythological beings are grammatically animate.
#
# KNOWN RESIDUAL GAP, not chased further: WordNet's noun ontology has many
# more such culturally-specific branch points; this covers the common
# cases found by spot-checking, not an exhaustive audit of every possible
# animate category. Verify any new lemma of interest before trusting its
# classification blindly (same caveat as any corpus-derived proxy in this
# programme).


def build_descendant_closure(lookup_dir, roots):
    """BFS down the '~' (subclass) relation from the given root ids."""
    children = defaultdict(list)
    with (lookup_dir / "sembank-relations.csv").open(encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 3:
                continue
            parent, child, rel = row[0], row[1], row[2].strip('"')
            if rel == "~":
                try:
                    children[int(parent)].append(int(child))
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


def load_gloss(lookup_dir):
    gloss = {}
    with (lookup_dir / "word-senses.csv").open(encoding="utf-8") as f:
        for row in csv.reader(f, delimiter="\t"):
            if len(row) < 2:
                continue
            try:
                gloss[int(row[0])] = row[1]
            except ValueError:
                continue
    return gloss


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=str(DEFAULT_DB))
    ap.add_argument("--lookup-dir", default=str(DEFAULT_LOOKUP))
    args = ap.parse_args()
    lookup_dir = Path(args.lookup_dir)

    animate_ids = build_descendant_closure(lookup_dir, ANIMATE_ROOTS)
    gloss = load_gloss(lookup_dir)
    print(f"animate sense-id closure: {len(animate_ids)} ids "
          f"(rooted at person=574, animal=575, spiritual_being=42842, "
          f"imaginary_being=42775)")

    db = sqlite3.connect(args.db)
    cur = db.cursor()

    # self-test: a handful of known animate/inanimate glosses, checked by id.
    # 102189 (Deva) is the case that caught the missing spiritual_being root —
    # kept as a regression test so that gap can't silently reopen.
    self_test_ids = [(574, True), (575, True), (576, False), (102189, True), (42847, True),
                     (101161, True)]  # Rākṣasa — the mythical-being regression case
    for sid, expect in self_test_ids:
        got = sid in animate_ids
        assert got == expect, f"self-test failed for id {sid} ({gloss.get(sid)}): got {got}"
    print("self-test OK (person/animal in closure, plant excluded)")

    lemma_votes = defaultdict(lambda: Counter())
    for lemma, wordsem in cur.execute(
        "SELECT lemma, m_wordsem FROM token WHERE upos='NOUN' AND m_wordsem IS NOT NULL"
    ):
        ids = []
        for part in wordsem.split(","):
            part = part.strip()
            if part.isdigit():
                ids.append(int(part))
        if not ids:
            continue
        for sid in ids:
            lemma_votes[lemma]["animate" if sid in animate_ids else "inanimate"] += 1

    classification = {}
    for lemma, votes in lemma_votes.items():
        anim, inan = votes["animate"], votes["inanimate"]
        total = anim + inan
        if anim > inan:
            cls = "animate"
        elif inan > anim:
            cls = "inanimate"
        else:
            cls = "tied"
        classification[lemma] = {
            "animate_votes": anim, "inanimate_votes": inan,
            "total_votes": total, "classification": cls,
        }

    n_animate = sum(1 for v in classification.values() if v["classification"] == "animate")
    n_inanimate = sum(1 for v in classification.values() if v["classification"] == "inanimate")
    n_tied = sum(1 for v in classification.values() if v["classification"] == "tied")

    out = {
        "instrument": "animacy_lookup.py — DCS m_wordsem (Sanskrit WordNet sense ids) "
                      "mapped to grammatical animacy via the dcs-conllu sembank lookup "
                      "tables (word-senses.csv, sembank-relations.csv), not built from "
                      "scratch — the mapping data already existed upstream",
        "animate_root_ids": {"person": 574, "animal": 575},
        "excluded_root": {"plant": 576, "reason": "grammatical animacy groups plants "
                          "with inanimates in Sanskrit, unlike biological life status"},
        "animate_sense_id_closure_size": len(animate_ids),
        "noun_lemmas_classified": len(classification),
        "summary": {"animate": n_animate, "inanimate": n_inanimate, "tied": n_tied},
        "lemma_classification": classification,
    }
    (HERE / "animacy_lemma_lookup.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"noun lemmas classified: {len(classification)} "
          f"({n_animate} animate, {n_inanimate} inanimate, {n_tied} tied)")
    print("-> animacy_lemma_lookup.json written")


if __name__ == "__main__":
    main()
