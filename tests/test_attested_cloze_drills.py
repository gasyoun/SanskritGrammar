"""Tests for the attested-sentence cloze drill generator (RQ2 cloze type).

Two layers, matching the tests/test_attested_drills.py convention for the
sibling W2-add-a declension drill:

1. **Pure-logic tests** — cell labelling, target picking, cloze-text assembly —
   run over hand-built token fixtures, no DCS database required. This is the
   layer that runs in CI.
2. **Spot-check against the real artifact** — sampled drill items must be
   internally consistent: the blanked position in `sentence_cloze` really is
   `target_idx`, and putting `form` back into that slot reproduces
   `sentence_full` exactly. Skipped when the generated TSV is absent (it is
   committed, so normally it runs).
"""
import csv
import importlib.util
import random
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DRILLS = ROOT / "sangram" / "data" / "attested_cloze_drills"
BUILDER = DRILLS / "build_attested_cloze_drills.py"
ITEMS = DRILLS / "attested_cloze_items.tsv"

sys.path.insert(0, str(DRILLS))


def load_builder():
    spec = importlib.util.spec_from_file_location("build_attested_cloze_drills", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# Layer 1 — pure-logic tests (no DCS database)
# --------------------------------------------------------------------------

def test_voice_label_never_claims_act():
    """DCS only distinguishes Passive from non-passive -- never emit 'Act'."""
    mod = load_builder()
    assert mod.voice_label("Pass") == "Pass"
    assert mod.voice_label(None) == "NonPass"
    assert mod.voice_label("") == "NonPass"


def test_noun_cell_requires_both_case_and_number():
    mod = load_builder()
    assert mod.noun_cell("Ins", "Plur") == "Ins.Plur"
    assert mod.noun_cell("Ins", None) is None
    assert mod.noun_cell(None, "Plur") is None
    assert mod.noun_cell("Bogus", "Plur") is None


def test_verb_cell_requires_all_four_tags():
    mod = load_builder()
    assert mod.verb_cell("Pres", "Ind", "3", "Sing", None) == "Pres.Ind.3.Sing.NonPass"
    assert mod.verb_cell("Pres", "Ind", "3", "Sing", "Pass") == "Pres.Ind.3.Sing.Pass"
    assert mod.verb_cell("Pres", None, "3", "Sing", None) is None
    assert mod.verb_cell(None, "Ind", "3", "Sing", None) is None


def _tok(idx, upos, form="x", lemma_id=1, lemma="x", **feats):
    base = {
        "idx": idx, "form": form, "lemma": lemma, "lemma_id": lemma_id, "upos": upos,
        "feat_case": None, "feat_number": None, "feat_tense": None, "feat_mood": None,
        "feat_voice": None, "feat_person": None, "feat_verbform": None,
        "feat_formation": None, "m_unsandhied": form,
    }
    base.update(feats)
    return base


def test_pick_target_walks_word_order_skipping_ineligible():
    mod = load_builder()
    tokens = [
        _tok(1, "PART", form="ca"),
        _tok(2, "NOUN", form="devaḥ", feat_case="Nom", feat_number=None),  # incomplete -> skip
        _tok(3, "VERB", form="gacchati", feat_verbform="Part"),  # participle -> not finite
        _tok(4, "NOUN", form="agniḥ", feat_case="Nom", feat_number="Sing"),
        _tok(5, "VERB", form="karoti", feat_tense="Pres", feat_mood="Ind",
             feat_person="3", feat_number="Sing", feat_verbform=None),
    ]
    target = mod.pick_target(tokens)
    assert target is not None
    assert target["idx"] == 4
    assert target["cell"] == "Nom.Sing"


def test_pick_target_finds_finite_verb_when_no_noun_eligible():
    mod = load_builder()
    tokens = [
        _tok(1, "NOUN", form="devaḥ", feat_case="Nom", feat_number=None),
        _tok(2, "VERB", form="karoti", feat_tense="Pres", feat_mood="Ind",
             feat_person="3", feat_number="Sing", feat_verbform=None),
    ]
    target = mod.pick_target(tokens)
    assert target is not None and target["idx"] == 2
    assert target["cell"] == "Pres.Ind.3.Sing.NonPass"


def test_pick_target_returns_none_when_nothing_eligible():
    mod = load_builder()
    tokens = [_tok(1, "PART", form="ca"), _tok(2, "VERB", form="gacchan", feat_verbform="Part")]
    assert mod.pick_target(tokens) is None


def test_build_cloze_text_blanks_only_the_target():
    mod = load_builder()
    tokens = [_tok(1, "X", form="a"), _tok(2, "X", form="b"), _tok(3, "X", form="c")]
    assert mod.build_cloze_text(tokens, 2) == "a ___ c"
    assert mod.build_full_text(tokens) == "a b c"


# --------------------------------------------------------------------------
# Layer 2 — spot-check the committed artifact for internal consistency
# --------------------------------------------------------------------------

@pytest.mark.skipif(not ITEMS.exists(), reason="generated cloze corpus not present")
def test_spot_check_20_items_reconstruct_the_full_sentence():
    """Putting `form` back at `target_idx` in `sentence_cloze` must reproduce
    `sentence_full` exactly -- proves the blank really sits where the row claims
    and the answer really is the word that was there.
    """
    with ITEMS.open(encoding="utf-8", newline="") as fh:
        items = list(csv.DictReader(fh, delimiter="\t"))
    assert items, "cloze corpus is empty"

    rng = random.Random(2026)
    for item in rng.sample(items, 20):
        cloze_words = item["sentence_cloze"].split(" ")
        full_words = item["sentence_full"].split(" ")
        target_idx = int(item["target_idx"])
        assert len(cloze_words) == len(full_words)
        blank_positions = [i for i, w in enumerate(cloze_words) if w == "___"]
        assert len(blank_positions) == 1, f"expected exactly one blank, got {blank_positions}"
        reconstructed = list(cloze_words)
        reconstructed[blank_positions[0]] = item["form"]
        assert reconstructed == full_words, (
            f"sentence {item['sentence_id']}: filling the blank with 'form' does not "
            f"reproduce sentence_full")
        # target_idx is 1-based and should land on the same word position DCS gave it.
        assert full_words[blank_positions[0]] == item["form"]


@pytest.mark.skipif(not ITEMS.exists(), reason="generated cloze corpus not present")
def test_every_item_has_a_named_drill_mode_consistent_with_distractor_count():
    with ITEMS.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            n = int(row["n_distractors"])
            assert row["drill_mode"] in {"mcq", "open"}
            if row["drill_mode"] == "mcq":
                assert n >= 2
            else:
                assert n < 2
            assert n == len([f for f in row["distractor_forms"].split("|") if f])


@pytest.mark.skipif(not ITEMS.exists(), reason="generated cloze corpus not present")
def test_no_distractor_equals_the_target_form():
    """A distractor that IS the correct answer would make the drill unanswerable."""
    with ITEMS.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            distractors = {f for f in row["distractor_forms"].split("|") if f}
            assert row["unsandhied"] not in distractors, (
                f"sentence {row['sentence_id']}: distractor duplicates the target's own form")
