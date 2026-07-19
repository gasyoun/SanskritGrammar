"""Tests for the W2-add-c samāsa right-to-left ladder generator (H1298).

Two layers, matching the VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md § W2-add-c gate:

1. **Unit layer** — the ladder builder, the RU-gloss variant ranking and (above all) the
   member-order verifier, run over hand-built fixtures with no repo data. This is the
   layer that runs in CI.
2. **Gold-set regression against the real artifact** — the 30 hand-checked ladders in
   ``gold_ladder_30.tsv`` must each still be present in the generated corpus with the
   same member sequence, and the generator's mechanical rungs must reproduce the gold
   head-first accumulation exactly. Skipped when the generated TSV is absent (it is
   committed, so normally it runs).

Layer 1 alone would only prove the code is self-consistent. The premise of the whole
feature is that **the last member really is the head** — a right-to-left ladder over a
scrambled split teaches a falsehood — so layer 2 re-checks the shipped corpus against the
hand-ratified analyses, and one test pins the specific upstream rows (``rājakule; kula
rājan`` and friends) that must never survive the gate.
"""
import csv
import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
LADDER = ROOT / "sangram" / "data" / "samasa_ladder"
BUILDER = LADDER / "build_samasa_ladder.py"
ITEMS = LADDER / "samasa_ladder_items.tsv"
GOLD = LADDER / "gold_ladder_30.tsv"


def _load_builder():
    spec = importlib.util.spec_from_file_location("build_samasa_ladder", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["build_samasa_ladder"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def bsl():
    if not BUILDER.exists():
        pytest.skip(f"builder absent: {BUILDER}")
    return _load_builder()


def _rows(path):
    with path.open(encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


# --------------------------------------------------------------------------- layer 1


def test_skeleton_drops_vowels_and_marks(bsl):
    assert bsl.skeleton("rAjendra") == "rjndr"
    assert bsl.skeleton("mahAbalaH") == "mhbl"
    assert bsl.skeleton("aMSa") == "S", "anusvāra and visarga are marks, not consonants"


def test_order_ok_accepts_real_compounds(bsl):
    # rājan+indra -> rājendra: the internal vowel sandhi (a+i -> e) is invisible to the
    # consonant skeleton, which is exactly why the check is built on skeletons.
    assert bsl.order_ok("rAjendra", ["rAjan", "indra"])
    assert bsl.order_ok("mahAbalaH", ["mahat", "bala"])
    assert bsl.order_ok("gosahasraPalaM", ["go", "sahasra", "Pala"])


def test_order_ok_rejects_scrambled_and_foreign_splits(bsl):
    # The four upstream defect shapes found in names.csv, one test each.
    assert not bsl.order_ok("rAjakule", ["kula", "rAjan"]), "reversed members"
    assert not bsl.order_ok("UrDvaM", ["daSan", "rAtra"]), "split of a different word"
    assert not bsl.order_ok("gOr", ["go", "go"]), "member repeated beyond the surface"
    assert not bsl.order_ok("DarmAlokamuKaM", ["Aloka", "muKa", "Darma"]), "rotated"


def test_order_ok_is_order_sensitive_not_just_membership(bsl):
    """The whole point: the same members in the wrong order must fail."""
    assert bsl.order_ok("narendra", ["nara", "indra"]) is True
    assert bsl.order_ok("narendra", ["indra", "nara"]) is False


def test_build_ladder_runs_head_first(bsl):
    rungs = bsl.build_ladder(["mahat", "bala"], ["великий", "сила"])
    assert [r["member"] for r in rungs] == ["bala", "mahat"], "rung 1 must be the head"
    assert [r["tail"] for r in rungs] == ["bala", "mahat-bala"]
    assert rungs[0]["questions"] == [bsl.HEAD_QUESTION]
    assert len(rungs[1]["questions"]) > 1, "modifier rungs offer a slot, not an answer"


def test_build_ladder_three_members_accumulates_rightwards(bsl):
    rungs = bsl.build_ladder(["go", "sahasra", "phala"], ["корова", "тысяча", "плод"])
    assert [r["tail"] for r in rungs] == ["phala", "sahasra-phala", "go-sahasra-phala"]


def test_generator_never_asserts_a_compound_type(bsl):
    """A modifier rung must never ship exactly one question — that would be an answer."""
    for members in (["mahat", "bala"], ["go", "sahasra", "phala"]):
        rungs = bsl.build_ladder(members, ["x"] * len(members))
        for rung in rungs[1:]:
            assert len(rung["questions"]) >= 2


def test_gloss_variants_ranked_by_attestation(bsl, tmp_path):
    src = tmp_path / "gloss.tsv"
    src.write_text(
        "lemma_slp1\tru\tn\tn_total\tn_forms\tupos\n"
        "bala\tсила\t183\t500\t1\tNOUN\n"
        "bala\tвойско\t209\t500\t1\tNOUN\n"
        "bala\tсилой\t116\t500\t1\tNOUN\n"
        "bala\tмощь\t3\t500\t1\tNOUN\n"
        "empty\t\t99\t99\t1\tNOUN\n",
        encoding="utf-8",
    )
    got = bsl.load_glosses(src)
    assert [ru for ru, _ in got["bala"]] == ["войско", "сила", "силой"]
    assert "empty" not in got, "blank glosses must not become a lemma's best variant"


def test_band_thresholds(bsl):
    assert bsl.band_of(863) == "ядро"
    assert bsl.band_of(30) == "частые"
    assert bsl.band_of(10) == "средние"
    assert bsl.band_of(5) == "редкие"


# --------------------------------------------------------------------------- layer 2

pytestmark_artifact = pytest.mark.skipif(
    not ITEMS.exists() or not GOLD.exists(), reason="generated corpus / gold set absent"
)


@pytest.fixture(scope="module")
def corpus():
    if not ITEMS.exists():
        pytest.skip("generated corpus absent")
    return {r["surface"]: r for r in _rows(ITEMS)}


@pytest.fixture(scope="module")
def gold():
    if not GOLD.exists():
        pytest.skip("gold set absent")
    return _rows(GOLD)


def test_gold_set_has_thirty_rows(gold):
    assert len(gold) == 30


def test_every_gold_compound_survives_the_gates(gold, corpus):
    missing = [g["surface"] for g in gold if g["surface"] not in corpus]
    assert not missing, f"gold compounds dropped from the corpus: {missing}"


def test_gold_member_sequence_matches_generated(gold, corpus):
    for g in gold:
        assert g["members"] == corpus[g["surface"]]["members"], g["surface"]


def test_gold_question_chain_has_one_question_per_member(gold):
    for g in gold:
        assert len(g["question_chain"].split("→")) == int(g["depth"]), g["surface"]


def test_generated_rungs_reproduce_gold_accumulation(gold, corpus):
    """The mechanical half of the ladder, re-derived from the gold members."""
    for g in gold:
        members = g["members"].split("|")
        expected = ["-".join(members[i:]) for i in range(len(members) - 1, -1, -1)]
        assert corpus[g["surface"]]["ladder_tails"].split("|") == expected, g["surface"]


def test_bahuvrihi_rows_carry_the_extra_resolution_step(gold):
    """A bahuvrīhi's referent is outside the compound — the ladder must say so."""
    for g in gold:
        if g["type"].startswith("BV"):
            assert g["bv_resolution"].strip(), g["surface"]
            assert "yasya" in g["vigraha_iast"], g["surface"]
        else:
            assert not g["bv_resolution"].strip(), g["surface"]


def test_every_gold_row_states_a_vigraha_and_a_smooth_rendering(gold):
    for g in gold:
        assert g["vigraha_iast"].strip(), g["surface"]
        assert g["smooth_ru"].strip(), g["surface"]
        assert g["note"].strip(), g["surface"]


def test_ambiguous_gold_rows_give_both_readings_not_one(gold):
    """Where the tradition reads a compound two ways, the gold set must not pick."""
    ambiguous = [g for g in gold if "‖" in g["vigraha_iast"]]
    assert ambiguous, "the gold set should retain at least one genuinely ambiguous case"
    for g in ambiguous:
        assert "‖" in g["smooth_ru"], g["surface"]
        assert "/" in g["type"] or "или" in g["type_ru"], g["surface"]


def test_no_shipped_ladder_violates_member_order(bsl, corpus):
    """Re-run the gate over the shipped artifact — no scrambled split may have leaked."""
    try:
        from indic_transliteration import sanscript
    except ImportError:
        pytest.skip("indic_transliteration absent")
    for surface, row in corpus.items():
        members = [
            sanscript.transliterate(m, sanscript.IAST, sanscript.SLP1)
            for m in row["members"].split("|")
        ]
        assert bsl.order_ok(row["surface_slp1"], members), surface


def test_known_bad_upstream_splits_are_absent(corpus):
    """The specific names.csv defect rows that must never reach a learner."""
    for surface, split in (
        ("rājakule", "kula|rājan"),
        ("ūrdhvaṁ", "daśan|rātra"),
        ("gaur", "go|go"),
    ):
        row = corpus.get(surface)
        assert row is None or row["members"] != split, f"{surface} leaked through"


def test_corpus_rows_are_internally_consistent(corpus):
    for surface, row in corpus.items():
        members = row["members"].split("|")
        assert len(members) == int(row["depth"]), surface
        assert len(row["members_ru"].split("|")) == int(row["depth"]), surface
        assert len(row["ladder_tails"].split("|")) == int(row["depth"]), surface
        assert int(row["freq"]) >= 5, surface
