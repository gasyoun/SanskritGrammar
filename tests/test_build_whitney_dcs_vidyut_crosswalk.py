"""Q4.4 Whitney-no <-> DCS lemma <-> Vidyut dhatu crosswalk
(ROADMAP_GRAMMAR_CORPUS_ACL_2026_2027.md Q4.4).

Unit-tests the pure join_row() logic against tiny synthetic fixtures --
does not touch the real VisualDCS/kosha sibling checkouts.
"""
import build_whitney_dcs_vidyut_crosswalk as q44

DCS_LEMMAS = {
    "kf": {"freqBand": 5, "attested": True},
    "gam": {"freqBand": 5, "attested": True},
    "Gost": {"freqBand": 0, "attested": False},
}

KOSHA_BY_BARE = {
    "kf": [{"aupadeshika": "qukfY", "via": "3sg", "code": "08.0010"}],
    "gam": [
        {"aupadeshika": "gamx~", "via": "3sg", "code": "01.1137"},
        {"aupadeshika": "gamx~", "via": "direct", "code": None},
    ],
    "vac": [
        {"aupadeshika": "vaca~", "via": "3sg", "code": "02.0001"},
        {"aupadeshika": "vaSa~", "via": "3sg", "code": "02.0002"},
    ],
}


def _row(whitney_no, root_iast, homonym="", gloss=""):
    return {"whitney_no": whitney_no, "root": root_iast, "homonym": homonym, "gloss": gloss}


def test_attested_and_unambiguous_match():
    out = q44.join_row(_row("1", "kṛ", gloss="do"), DCS_LEMMAS, KOSHA_BY_BARE)
    assert out["root_slp1"] == "kf"
    assert out["dcs_lemma_attested"] is True
    assert out["dcs_freq_band"] == 5
    assert out["vidyut_aupadeshika"] == "qukfY"
    assert out["vidyut_dhatupatha_code"] == "08.0010"
    assert out["vidyut_match_count"] == 1
    assert out["vidyut_ambiguous"] is False


def test_duplicate_aupadeshika_is_not_ambiguous():
    # two kosha rows, same aupadeshika (direct + 3sg via) -> one real dhatu
    out = q44.join_row(_row("2", "gam"), DCS_LEMMAS, KOSHA_BY_BARE)
    assert out["vidyut_match_count"] == 2
    assert out["vidyut_ambiguous"] is False
    assert out["vidyut_aupadeshika"] == "gamx~"


def test_distinct_aupadeshika_is_ambiguous():
    out = q44.join_row(_row("3", "vac"), DCS_LEMMAS, KOSHA_BY_BARE)
    assert out["vidyut_ambiguous"] is True
    assert out["vidyut_aupadeshika"] == "vaSa~;vaca~"


def test_unattested_root_and_no_vidyut_match():
    out = q44.join_row(_row("4", "kfta"), DCS_LEMMAS, KOSHA_BY_BARE)
    assert out["dcs_lemma_attested"] is False
    assert out["dcs_freq_band"] == ""
    assert out["vidyut_match_count"] == 0
    assert out["vidyut_aupadeshika"] == ""
    assert out["vidyut_ambiguous"] is False


def test_lemma_present_but_not_attested():
    out = q44.join_row(_row("5", "GOsta"), DCS_LEMMAS, KOSHA_BY_BARE)
    assert out["root_slp1"] == "GOsta"
    assert out["dcs_lemma_attested"] is False
