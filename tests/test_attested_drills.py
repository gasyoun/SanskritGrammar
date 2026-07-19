"""Tests for the W2-add-a attested-cell declension drill generator (H1296).

Two layers, matching the VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md § W2-add-a gate:

1. **Joiner fixture test** — the join/emit logic run over a hand-built 20-lemma
   fixture with stub inputs, no repo data and no DCS database required. This is the
   layer that runs in CI.
2. **Spot-check against the real artifact** — 20 sampled drill items must each name a
   cell the lemma's `cells_bits24` bitstring actually sets in `lemma_cell_coverage.csv`.
   Skipped when the generated TSV is absent (it is committed, so normally it runs).

The point of layer 2 is that layer 1 can only prove the code is self-consistent; only
a comparison against the *upstream* coverage asset proves no unattested cell leaked
into the drill corpus, which is the entire premise of the feature.
"""
import csv
import random
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
DRILLS = ROOT / "sangram" / "data" / "attested_drills"
BUILDER = DRILLS / "build_attested_declension_drills.py"
ITEMS = DRILLS / "attested_drill_items.tsv"
COVERAGE = ROOT / "sangram" / "data" / "declension_cell_coverage" / "lemma_cell_coverage.csv"

CASES = ["Nom", "Acc", "Ins", "Dat", "Abl", "Gen", "Loc", "Voc"]
NUMBERS = ["Sing", "Dual", "Plur"]
CELLS = [f"{c}.{n}" for c in CASES for n in NUMBERS]

sys.path.insert(0, str(DRILLS))


def load_builder():
    import importlib.util
    spec = importlib.util.spec_from_file_location("build_attested_drills", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# --------------------------------------------------------------------------
# Layer 1 — pure-logic tests (no repo data, no DCS)
# --------------------------------------------------------------------------

def test_cell_order_matches_coverage_asset():
    """The bitstring index -> cell mapping MUST match the G2 asset's cells_order.

    If these ever drift, every drill item silently names the wrong cell -- the
    failure would be invisible in the data and catastrophic in the classroom.
    """
    import json
    summary = json.loads(
        (ROOT / "sangram" / "data" / "declension_cell_coverage" / "coverage_summary.json")
        .read_text(encoding="utf-8"))
    assert summary["cells_order"] == CELLS
    assert load_builder().CELLS == CELLS


def test_band_for_boundaries():
    band_for = load_builder().band_for
    assert band_for(0) == "hapax"
    assert band_for(1) == "hapax"
    assert band_for(2) == "2-9"
    assert band_for(9) == "2-9"
    assert band_for(10) == "10-99"
    assert band_for(999) == "100-999"
    assert band_for(1000) == "1000+"
    assert band_for(50000) == "1000+"


def test_classify_never_resolves_a_disagreement():
    """The hard rule from H1296: flag, never silently pick."""
    mod = load_builder()
    to_slp1 = mod.load_transliterator()
    classify = mod.classify

    # generated form is exactly the attested set
    assert classify(["devaH"], ["devaḥ"], to_slp1) == "match"
    # generated form attested, corpus also has a Vedic doublet -> variant, both kept
    assert classify(["devEH"], ["devaiḥ", "devebhiḥ"], to_slp1) == "variant"
    # generated form never attested here -> mismatch, both sides kept
    assert classify(["rAjaByaH"], ["rājbhyaḥ"], to_slp1) == "mismatch"
    # degenerate inputs are named, not guessed
    assert classify([], ["devaḥ"], to_slp1) == "no_generation"
    assert classify(["devaH"], [], to_slp1) == "no_attested_form"


def test_joiner_fixture_20_lemmas(tmp_path):
    """End-to-end join over a 20-lemma fixture with stub inputs.

    Every lemma gets a distinct bitstring so the test proves the emitter walks the
    bits rather than emitting a fixed cell set.
    """
    mod = load_builder()

    lemmas = [
        ("deva", "Masc", "a"), ("agni", "Masc", "i"), ("rājan", "Masc", "an"),
        ("nadī", "Fem", "ī"), ("vāc", "Fem", "c"), ("guru", "Masc", "u"),
        ("mati", "Fem", "i"), ("manas", "Neut", "as"), ("pitṛ", "Masc", "ṛ"),
        ("phala", "Neut", "a"), ("kanyā", "Fem", "ā"), ("bhū", "Fem", "ū"),
        ("gaja", "Masc", "a"), ("vana", "Neut", "a"), ("nara", "Masc", "a"),
        ("kavi", "Masc", "i"), ("sena", "Fem", "ā"), ("jala", "Neut", "a"),
        ("putra", "Masc", "a"), ("mitra", "Neut", "a"),
    ]

    cov = tmp_path / "cov.csv"
    with cov.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["lemma_id", "lemma", "dom_gender", "stem_final", "tokens",
                    "cells_attested", "cells_bits24"])
        for i, (lemma, gender, final) in enumerate(lemmas, start=1):
            # distinct bitstring per lemma: set bits i, i+3, i+7 (mod 24)
            bits = ["0"] * 24
            for off in (0, 3, 7):
                bits[(i + off) % 24] = "1"
            w.writerow([i, lemma, gender, final, 100 * i, sum(b == "1" for b in bits),
                        "".join(bits)])

    to_slp1 = mod.load_transliterator()
    freq = tmp_path / "freq.tsv"
    with freq.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["lemma_slp1", "count_all", "grammar_all", "rank_all", "periods",
                    "periods_sum", "coverage_pct", "core_rank"])
        for i, (lemma, _, _) in enumerate(lemmas, start=1):
            w.writerow([to_slp1(lemma), 5000 - i, "m", i, "", "", "", i])

    zal = tmp_path / "zal.tsv"
    with zal.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["k1", "hom", "lex", "accented", "index_token", "stem_class",
                    "compound_members", "irregularities"])
        for lemma, _, final in lemmas:
            cls = {"a": "a-stem", "i": "i-stem", "ī": "ī-stem", "u": "u-stem",
                   "ū": "ū-stem", "ā": "ā-stem"}.get(final, "consonant-stem")
            w.writerow([to_slp1(lemma), "", "", "", "", cls, "", ""])

    # Empty stub DB with the columns the reader needs: proves the join stands on its
    # own and degrades to no_attested_form rather than crashing when the corpus is absent.
    import sqlite3
    db = tmp_path / "stub.sqlite"
    conn = sqlite3.connect(db)
    conn.execute("CREATE TABLE token (lemma_id INTEGER, lemma TEXT, upos TEXT, "
                 "feat_case TEXT, feat_number TEXT, m_unsandhied TEXT)")
    conn.commit()
    conn.close()

    out_dir = tmp_path / "out"
    out_dir.mkdir()
    mod.OUT_DIR = out_dir

    args = type("A", (), {
        "coverage": cov, "frequency": freq, "zaliznyak": zal, "db": db,
        "widget_data": out_dir / "widget.js", "core_only": True, "limit": 0,
        "max_forms": 3, "no_generate": False,
    })()
    report = mod.build(args)

    assert report["lemmas"] == 20, "all 20 fixture lemmas must survive the three-way join"

    rows = list(csv.DictReader((out_dir / "attested_drill_items.tsv")
                               .open(encoding="utf-8", newline=""), delimiter="\t"))
    assert len(rows) == sum(3 for _ in lemmas), "3 set bits per fixture lemma"

    # Every emitted cell is one this lemma's bitstring actually sets.
    bits_by_lemma = {r["lemma"]: r["cells_bits24"]
                     for r in csv.DictReader(cov.open(encoding="utf-8", newline=""))}
    for r in rows:
        idx = CELLS.index(r["cell"])
        assert bits_by_lemma[r["lemma"]][idx] == "1", (
            f"{r['lemma']} {r['cell']} emitted but not set in the bitstring")

    # No corpus in the stub DB -> the flag says so instead of inventing agreement.
    assert {r["agreement"] for r in rows} <= {"no_attested_form", "no_generation"}
    assert all(r["attested_forms"] == "" for r in rows)

    # Widget data and the per-class report were produced.
    assert (out_dir / "widget.js").exists()
    assert (out_dir / "coverage_by_stem_class.json").exists()
    assert report["by_stem_class"], "per-stem-class instrumentation must be populated"


# --------------------------------------------------------------------------
# Layer 2 — spot-check the committed artifact against the upstream coverage asset
# --------------------------------------------------------------------------

@pytest.mark.skipif(not ITEMS.exists() or not COVERAGE.exists(),
                    reason="generated drill corpus or coverage asset not present")
def test_spot_check_20_items_against_coverage_bitstrings():
    """20 sampled real drill items must each sit on a bit the coverage asset sets."""
    bits_by_id = {}
    with COVERAGE.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            bits_by_id[int(row["lemma_id"])] = row["cells_bits24"]

    with ITEMS.open(encoding="utf-8", newline="") as fh:
        items = list(csv.DictReader(fh, delimiter="\t"))
    assert items, "drill corpus is empty"

    rng = random.Random(1296)  # deterministic sample -- reproducible failures
    for item in rng.sample(items, 20):
        lemma_id = int(item["lemma_id"])
        bits = bits_by_id.get(lemma_id)
        assert bits is not None, f"drill lemma_id {lemma_id} absent from the coverage asset"
        idx = CELLS.index(item["cell"])
        assert bits[idx] == "1", (
            f"{item['lemma']} ({lemma_id}) {item['cell']} is in the drill corpus "
            f"but NOT attested in lemma_cell_coverage.csv")


@pytest.mark.skipif(not ITEMS.exists(), reason="generated drill corpus not present")
def test_every_item_carries_a_named_agreement_flag():
    """No drill item may ship without saying how generation and corpus relate."""
    valid = {"match", "variant", "mismatch", "no_attested_form", "no_generation"}
    with ITEMS.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            assert row["agreement"] in valid, f"bad flag {row['agreement']!r}"
            if row["agreement"] in {"variant", "mismatch"}:
                assert row["expected_form"] and row["attested_forms"], (
                    "a flagged disagreement must carry BOTH sides, never one")
