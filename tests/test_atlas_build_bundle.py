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
