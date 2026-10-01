"""Characterization of the generic DCS adapter (H1913 Slice C2).

``adapters/dcs.py`` is a shared extension point, so its behavior is pinned the
same way the generator's is: against the deterministic fixture database, with
hand-derived expectations. A second consumer should be able to trust these
semantics without reading the corpus.
"""
from __future__ import annotations

import sqlite3

import pytest

import build_fixture

from sg_tooling.adapters.dcs import DcsMaster, MissingProvenancePin, sha256_file


@pytest.fixture(scope="module")
def db(tmp_path_factory):
    return build_fixture.build_dcs_fixture(
        tmp_path_factory.mktemp("dcs-adapter") / "fixture.sqlite"
    )


@pytest.fixture(scope="module")
def master(db):
    with DcsMaster(db) as m:
        yield m


FIN_FUT = ("upos='VERB' AND (feat_verbform='Fin' OR feat_verbform IS NULL) "
           "AND feat_person IS NOT NULL AND feat_tense='Fut'")


def test_open_refuses_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        DcsMaster(tmp_path / "nope.sqlite")


def test_open_refuses_unpinned_master(tmp_path):
    """C3 §2.1: no provenance pin -> refusal at open, connection released."""
    path = tmp_path / "unpinned.sqlite"
    con = sqlite3.connect(path)
    con.executescript(
        "CREATE TABLE provenance (key TEXT PRIMARY KEY, value TEXT NOT NULL);"
        "INSERT INTO provenance VALUES ('other', 'x');"
    )
    con.commit()
    con.close()
    with pytest.raises(MissingProvenancePin):
        DcsMaster(path)
    # the failed open must not leak a live connection holding the file
    con = sqlite3.connect(path)
    con.close()


def test_provenance_roundtrip(master):
    prov = master.provenance()
    assert prov["source_commit"] == "04e0778d3dc971030229179e25eea043d06ff397"
    assert prov["source_repo"] == "gasyoun/dcs-conllu (OliverHellwig/sanskrit)"


def test_sha256_is_content_hash_of_the_master(master, db):
    assert master.sha256() == sha256_file(db)


def test_count_matches_fixture_plan(master):
    assert master.count(FIN_FUT) == 74
    assert master.count(FIN_FUT + " AND feat_formation='peri'") == 15
    assert master.count(FIN_FUT + " AND feat_mood='Cond'") == 5
    assert master.count(
        "upos='VERB' AND feat_verbform='Part' AND feat_tense='Fut'"
    ) == 4


def test_distribution_shares_and_null_bucket(master):
    person = master.distribution("feat_person", FIN_FUT, 74)
    assert {k: v["tokens"] for k, v in person.items()} == {"1": 27, "2": 8, "3": 39}
    assert person["1"]["share"] == round(27 / 74, 4)

    formation = master.distribution("feat_formation", FIN_FUT, 74)
    # NULL formation lands under the literal ∅ key: simple future
    assert formation["∅"]["tokens"] == 59
    assert formation["peri"]["tokens"] == 15


def test_top_form_lemmas_excludes_null_forms_and_orders_by_count(master):
    top = master.top_form_lemmas(FIN_FUT, 15)
    counts = [row[2] for row in top]
    assert counts == sorted(counts, reverse=True)
    assert len(set(counts)) == len(counts), "fixture promises tie-free ordering"
    assert top[0] == ("kariṣyāmi", "kṛ", 14)
    assert all(row[0] is not None for row in top)

    peri = master.top_form_lemmas(FIN_FUT + " AND feat_formation='peri'", 8)
    assert [row[0] for row in peri] == ["bhavitā", "kartāsmi"]
    assert len(peri) == 2


def test_token_ids_and_sample_context_row_join_chain(master):
    ids = list(master.token_ids(FIN_FUT))
    assert len(ids) == 74
    assert ids == sorted(ids)

    row = master.sample_context_row(ids[0])
    assert row[0] == ids[0]
    # text.name, chapter.ref, sentence.sent_counter resolve through the joins
    assert row[8] == "Fixture Text A"
    assert row[9] in ("F1.1", "F1.2")
