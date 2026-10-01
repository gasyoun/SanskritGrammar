"""Tests for scripts/atlas_build_bundle.py pure helpers (H1839).

Full end-to-end rebuild needs the private Uprava hub path and is out of CI
scope; these tests pin the public contract pieces: org resolution, slug
grammar, denylist, and leakage patterns that must never enter a bundle.
"""
import atlas_build_bundle as abb


def test_repo_org_sanskrit_lexicon():
    assert abb.repo_org("PWG") == "sanskrit-lexicon"
    assert abb.repo_org("csl-orig") == "sanskrit-lexicon"


def test_repo_org_gasyoun():
    assert abb.repo_org("SanskritGrammar") == "gasyoun"
    assert abb.repo_org("kosha") == "gasyoun"


def test_repo_org_override():
    assert abb.repo_org("SanskritSpellCheck") == "drdhaval2785"


def test_repo_org_unknown_is_none():
    assert abb.repo_org("TotallyInventedRepoName") is None


def test_slug_lowercases():
    assert abb.slug("SanskritGrammar") == "sanskritgrammar"
    assert abb.slug("csl_orig") == "csl-orig"


def test_drop_repos_includes_private_hubs():
    assert "Uprava" in abb.DROP_REPOS
    assert "github-spine" in abb.DROP_REPOS
    assert "telegram-sanskrit-corpus" in abb.DROP_REPOS


def test_leakage_patterns_cover_private_markers():
    joined = " ".join(abb.LEAKAGE_PATTERNS)
    assert "Uprava" in joined or "github.com/gasyoun/Uprava" in abb.LEAKAGE_PATTERNS
    assert any("@DECIDE" == p for p in abb.LEAKAGE_PATTERNS)
    assert any("GTD_NEXT_ACTIONS" == p for p in abb.LEAKAGE_PATTERNS)


def test_internal_and_public_evidence_shapes():
    ie = abb.internal_evidence("метка")
    assert ie["visibility"] == "internal"
    assert "url" not in ie
    pe = abb.public_evidence("метка", "https://example.org/x")
    assert pe["visibility"] == "public"
    assert pe["url"].startswith("https://")


# ---------------------------------------------------------------------------
# H2276 dual-run residual of H2271: pure-helper regression pins for the two
# live-data drift bugs that only the e2e suite (private Uprava) previously
# exercised. These run in CI without the hub.
# ---------------------------------------------------------------------------

_FAKE_MEGABOOK_S9 = """## §9. Anchors

### §9.1. Programme Alpha

| Основной тезис | Репозиторий |
|---|---|
| [§2.1](#21-example) | SanskritGrammar |
| [§3.3](#33-example) / [§3.4](#34-example) | kosha, csl-atlas |
| §5.1 | PWG |

## §10. Next
""".splitlines()


def test_parse_anchors_accepts_markdown_linked_section_refs():
    """MEGABOOK §9 cells now use [§N.M](#slug); bare §N.M must still work.

    Pre-H2271 parse_anchors took the whole cell text as the thesis id, so a
    linked cell produced thesis:[§2.1](#21-...) and failed validation.
    """
    triples = abb.parse_anchors(_FAKE_MEGABOOK_S9)
    sections = {sec for sec, _repo, _prog in triples}
    assert sections == {"2.1", "3.3", "3.4", "5.1"}
    repos = {repo for _sec, repo, _prog in triples}
    assert "SanskritGrammar" in repos
    assert "kosha" in repos
    assert "csl-atlas" in repos
    assert "PWG" in repos
    # No markdown residue in any thesis section token
    for sec, _repo, _prog in triples:
        assert "[" not in sec and "]" not in sec and "#" not in sec
        assert sec[0].isdigit()


def test_ext_name_map_covers_every_external_stack():
    """Every EXTERNAL_STACKS node id must be reachable from a TSV ext: name."""
    stack_ids = {row[0] for row in abb.EXTERNAL_STACKS}
    mapped_ids = set(abb.EXT_NAME_MAP.values())
    assert stack_ids == mapped_ids, (
        f"stack-only={sorted(stack_ids - mapped_ids)} "
        f"map-only={sorted(mapped_ids - stack_ids)}"
    )
    # Reverse: every map key must resolve to an ext: id that exists in stacks
    for name, nid in abb.EXT_NAME_MAP.items():
        assert nid.startswith("ext:"), name
        assert nid in stack_ids, f"{name} -> {nid} not in EXTERNAL_STACKS"


def test_external_stacks_includes_sanskrit_lexicon_scans():
    """H1706 added ext:sanskrit-lexicon-scans to interlinks; rebuild must know it.

    Pre-H2271 rebuild hard-SystemExit'ed on the first live edge that referenced
    this host. Pin the map entry so a future map-only edit fails in CI.
    """
    assert "sanskrit-lexicon-scans" in abb.EXT_NAME_MAP
    assert abb.EXT_NAME_MAP["sanskrit-lexicon-scans"] == "ext:sanskrit-lexicon-scans"
    stack_ids = {row[0] for row in abb.EXTERNAL_STACKS}
    assert "ext:sanskrit-lexicon-scans" in stack_ids


# ---------------------------------------------------------------------------
# H3683 wave 2 — the unmatched-join drain. Every live FEATURES_INDEX I–IV row
# must land in exactly one of: FEATURE_ID_JOINS, FEATURE_ROW_NOTES, or the
# dict-code / ext-stack shape notes. The "wave-2 drain" placeholder is gone;
# an unclassified row hard-fails join_features (plan R4.2 join bar).
# ---------------------------------------------------------------------------


def test_feature_id_joins_target_known_families():
    families = {row[0] for row in abb.ASSET_FAMILIES}
    unknown = set(abb.FEATURE_ID_JOINS.values()) - families
    assert not unknown, f"joins point at non-families: {sorted(unknown)}"


def test_feature_row_notes_never_shadow_a_join():
    clash = set(abb.FEATURE_ROW_NOTES) & set(abb.FEATURE_ID_JOINS)
    assert not clash, f"id both joined and noted: {sorted(clash)}"


def test_join_takes_precedence_over_note():
    rows = [{"id": "A2", "section": "s", "title": "SanskritRussian glossary (3-layer)"}]
    joined, unmatched = abb.join_features(rows)
    assert joined == {"asset:sa-ru-alignment": ["A2"]}
    assert unmatched == []


def test_e43_double_definition_gets_distinct_reasons():
    rows = [
        {"id": "E43", "section": "s", "title": "kosha corpus sandhi (programme)"},
        {"id": "E43", "section": "s",
         "title": "code-duplication census + LOC/language-mix per repo"},
    ]
    joined, unmatched = abb.join_features(rows)
    assert joined == {}
    assert len(unmatched) == 2
    reasons = {u["title"]: u["reason"] for u in unmatched}
    assert reasons["kosha corpus sandhi (programme)"] != \
        reasons["code-duplication census + LOC/language-mix per repo"]
    assert all("wave-2 drain" not in r for r in reasons.values())


def test_m_tool_rows_carry_external_stack_note():
    rows = [
        {"id": "M10", "section": "s", "title": "Samsaadhanii / SCL (Amba Kulkarni, UoHyd)"},
        {"id": "M14", "section": "s", "title": "vidyut (Ambuda)"},
    ]
    joined, unmatched = abb.join_features(rows)
    assert joined == {}
    expected = abb.UNMATCHED_NOTE_BY_SHAPE["ext-stack"]
    assert all(u["reason"] == expected for u in unmatched)


def test_uncategorised_row_hard_fails():
    import pytest
    rows = [{"id": "E99", "section": "s", "title": "some future row"}]
    with pytest.raises(SystemExit, match="E99"):
        abb.join_features(rows)


def test_dict_code_shape_note_unchanged():
    rows = [{"id": "mw", "section": "s", "title": "Monier-Williams"}]
    joined, unmatched = abb.join_features(rows)
    assert joined == {}
    assert unmatched[0]["reason"] == abb.UNMATCHED_NOTE_BY_SHAPE["dict-code"]


def test_placeholder_note_removed_from_shape_table():
    assert "no-join" not in abb.UNMATCHED_NOTE_BY_SHAPE


_SIBLING_SIDECAR = (
    abb.Path(__file__).resolve().parent.parent.parent
    / "SanskritLexicography" / "features_index.json"
)


def test_live_sidecar_fully_drained():
    """Live gate (skips without the SL sibling, CI-safe): no placeholder and
    every unmatched row carries a real reason."""
    if not _SIBLING_SIDECAR.exists():
        import pytest
        pytest.skip("no ../SanskritLexicography/features_index.json sibling")
    features = abb.load_features(_SIBLING_SIDECAR)
    joined, unmatched = abb.join_features(features)
    assert joined, "live sidecar produced no joins"
    for row in unmatched:
        assert "wave-2 drain" not in row["reason"], row["id"]
        assert len(row["reason"]) > 20, row["id"]
