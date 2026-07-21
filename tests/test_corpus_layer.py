"""Tests for the methodichka corpus layer (H1297, W2-add-b).

Pins the W2-add-b acceptance criteria from
docs/VERIFICATION_DIGITAL_SANSKRIT_PEDAGOGY.md:

1. Banding regression on 20 known lemmas (fixture committed in
   tests/fixtures/corpus_layer_banding_fixture.tsv; cross-checked against the
   live kosha frequency table when that sibling repo is present).
2. Every published example carries a DCS locus.
3. Zero restricted-layer text in the published sections: every row's Russian
   rendering is freshly authored or public-tier; a restricted-only row must
   ship Sanskrit-only with the «перевод в закрытом слое» marker.
4. The manuscript tables agree with corpus_layer.tsv (band, rank, locus) — the
   drift guard between the registry TSV and the print prose.
"""

import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from build_corpus_layer import band_for_rank, DEFAULT_FREQ, load_frequency

FIXTURE = REPO / "tests" / "fixtures" / "corpus_layer_banding_fixture.tsv"

BOOKS = {
    REPO / "KocherginaUchebnik_1998" / "corpus_layer" / "corpus_layer.tsv":
        REPO / "KocherginaUchebnik_1998" / "METODICHKA_KOCHERGINA_CORPUS_LAYER_2026.md",
    REPO / "ApteSyntax_1885" / "corpus_layer" / "corpus_layer.tsv":
        REPO / "ApteSyntax_1885" / "METODICHKA_APTE_CORPUS_LAYER_2026.md",
}

RESTRICTED_MARKER = "перевод в закрытом слое"
ALLOWED_RU_SOURCES = {"authored", "public-glossary", "restricted"}


def read_tsv(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh, delimiter="\t"))


def test_banding_regression_20_lemmas():
    rows = read_tsv(FIXTURE)
    assert len(rows) == 20, f"fixture must hold exactly 20 lemmas, got {len(rows)}"
    for row in rows:
        assert band_for_rank(int(row["rank_all"])) == row["band"], row["lemma_iast"]
    # Boundary pins for the documented rule itself.
    assert band_for_rank(1) == "топ-100"
    assert band_for_rank(100) == "топ-100"
    assert band_for_rank(101) == "топ-1000"
    assert band_for_rank(1000) == "топ-1000"
    assert band_for_rank(1001) == "редкое"
    assert band_for_rank(None) == "вне корпуса"


def test_fixture_matches_live_kosha_table():
    if not DEFAULT_FREQ.exists():
        import pytest
        pytest.skip("kosha sibling repo not present")
    freq = load_frequency(DEFAULT_FREQ)
    for row in read_tsv(FIXTURE):
        count_all, rank_all = freq[row["lemma_slp1"]]
        assert (count_all, rank_all) == (int(row["count_all"]), int(row["rank_all"])), (
            f"{row['lemma_iast']}: fixture drifted from kosha lemma_frequency.tsv")


def test_every_example_carries_dcs_locus():
    for tsv_path in BOOKS:
        for row in read_tsv(tsv_path):
            assert row["dcs_text"].strip(), f"{tsv_path.name}: {row['lemma_iast']} has no DCS text"
            assert row["dcs_locus"].strip(), f"{tsv_path.name}: {row['lemma_iast']} has no DCS locus"
            assert row["example_iast"].strip(), f"{tsv_path.name}: {row['lemma_iast']} has no example"


def test_rights_gate_no_restricted_text():
    for tsv_path, md_path in BOOKS.items():
        md = md_path.read_text(encoding="utf-8")
        for row in read_tsv(tsv_path):
            assert row["ru_source"] in ALLOWED_RU_SOURCES, (
                f"{tsv_path.name}: {row['lemma_iast']} has unknown ru_source {row['ru_source']!r}")
            if row["ru_source"] == "restricted":
                assert not row["ru"].strip(), (
                    f"{tsv_path.name}: {row['lemma_iast']} is restricted but ships a rendering")
                line = _manuscript_row(md, row["lemma_iast"], md_path)
                assert RESTRICTED_MARKER in line, (
                    f"{md_path.name}: restricted row {row['lemma_iast']} lacks the marker")
            else:
                assert row["ru"].strip(), (
                    f"{tsv_path.name}: {row['lemma_iast']} has no rendering yet is not restricted")


def _manuscript_row(md_text, lemma, md_path):
    needle = f"| {lemma} |"
    for line in md_text.splitlines():
        if line.startswith(needle):
            return line
    raise AssertionError(f"{md_path.name}: no table row for lemma {lemma!r}")


def test_manuscript_tables_agree_with_tsv():
    for tsv_path, md_path in BOOKS.items():
        md = md_path.read_text(encoding="utf-8")
        rows = read_tsv(tsv_path)
        assert rows, f"{tsv_path} is empty"
        for row in rows:
            line = _manuscript_row(md, row["lemma_iast"], md_path)
            assert f"| {row['band']} |" in line, (
                f"{md_path.name}: {row['lemma_iast']} band drifted from TSV")
            assert f"| {row['rank_all']} |" in line, (
                f"{md_path.name}: {row['lemma_iast']} rank drifted from TSV")
            locus = f"{row['dcs_text']}: {row['dcs_locus']}"
            assert locus in line, (
                f"{md_path.name}: {row['lemma_iast']} locus drifted from TSV ({locus})")
