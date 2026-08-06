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
