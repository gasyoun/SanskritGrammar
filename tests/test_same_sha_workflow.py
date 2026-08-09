from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CI = ROOT / ".github" / "workflows" / "ci.yml"
LEGACY = ROOT / ".github" / "workflows" / "deploy-pages.yml"


def test_pages_is_built_and_deployed_in_one_gated_workflow() -> None:
    text = CI.read_text(encoding="utf-8")
    assert "uv sync --frozen" in text
    assert "uv run python -m pytest" in text
    assert "npm run test:site" in text
    assert "npm run typecheck" in text
    assert "npm run build" in text
    assert "actions/upload-pages-artifact" in text
    assert "needs: quality" in text
    assert "needs: pages-artifact" in text
    assert "needs.pages-artifact.outputs.artifact_sha == github.sha" in text
    assert 'test "$(tr -d' in text
    assert "actions/deploy-pages" in text


def test_deploy_never_rebuilds_and_legacy_workflow_is_gone() -> None:
    text = CI.read_text(encoding="utf-8")
    deploy = text.split("\n  deploy:\n", 1)[1]
    assert "checkout" not in deploy
    assert "npm run build" not in deploy
    assert not LEGACY.exists()


def test_deliberately_red_control_precedes_artifact_upload() -> None:
    text = CI.read_text(encoding="utf-8")
    control = text.index("Deliberately red same-SHA control")
    upload = text.index("Stage exact-SHA site artifact")
    assert control < upload
    assert "inputs.fail_required_gate" in text
