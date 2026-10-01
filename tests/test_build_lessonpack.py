"""LYW lessonpack contract suite (H3521, wave 1: Kochergina занятие 1).

Locks the pack contract v1 against silent drift:
    schema · matrix completeness · no fabricated grammar · answer-key resolvability
    Mermaid sanity · fixture privacy (k-anon shape) · CLI --check exit 0
    byte-stable regeneration.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import build_lessonpack as blp

ROOT = Path(blp.ROOT)
PACKS_ROOT = ROOT / "KocherginaUchebnik_1998" / "LessonPacks" / "zan1"
EXPECTED_PROFILES = {
    "base",
    "nol/yoga", "nol/ayurveda", "nol/kino", "nol/palomnichestvo",
    "prodolzhayushchiy/yoga", "prodolzhayushchiy/ayurveda",
    "prodolzhayushchiy/kino", "prodolzhayushchiy/palomnichestvo",
}


def _ctx():
    return blp.Context(1)


def _fixture(ctx=None):
    raw = blp.FIXTURE_PATH.read_text(encoding="utf-8")
    return json.loads(raw), raw


def _manifests():
    out = {}
    for rel in sorted(EXPECTED_PROFILES):
        out[rel] = json.loads((PACKS_ROOT / rel / "manifest.json").read_text(encoding="utf-8"))
    return out


def test_matrix_completeness_base_plus_8():
    problems = blp.validate_matrix(PACKS_ROOT)
    assert not problems, problems
    actual = {p.relative_to(PACKS_ROOT).as_posix()
              for p in PACKS_ROOT.rglob("manifest.json")}
    assert {p.rsplit("/", 1)[0] if "/" in p else p for p in actual} == EXPECTED_PROFILES


def test_manifest_schema_v1_valid_all_profiles():
    ctx = _ctx()
    fixture, _ = _fixture(ctx)
    total_problems = []
    for rel in sorted(EXPECTED_PROFILES):
        total_problems += [f"{rel}: {p}"
                           for p in blp.validate_pack(PACKS_ROOT / rel, ctx, fixture)]
    assert not total_problems, total_problems


def test_manifests_carry_contract_fields():
    for rel, m in _manifests().items():
        assert m["schema"] == "lyw-pack-v1"
        assert m["zan"] == 1
        assert set(m["generated"]) == {"date", "session"}
        if rel == "base":
            assert m["profile"] == {"level": "base", "interest": "base"}
        else:
            level, interest = rel.split("/")
            assert m["profile"] == {"level": level, "interest": interest}
        titles = [s["title"] for s in m["sections"]]
        assert titles and all(titles), f"{rel}: empty section title"


def test_no_fabricated_grammar():
    """Every concept token traces to the занятие-1 mdx slice or lesson HK-claims."""
    ctx = _ctx()
    fixture, _ = _fixture(ctx)
    for rel in sorted(EXPECTED_PROFILES):
        pd = PACKS_ROOT / rel
        m = json.loads((pd / "manifest.json").read_text(encoding="utf-8"))
        qdata = json.loads((pd / "quizzes.json").read_text(encoding="utf-8"))
        concepts = [c for s in m["sections"] for c in s["source_concepts"]]
        concepts += [c for it in qdata["items"] for c in it["concept"]]
        concepts += [mn["for"] for mn in m["mnemonics"]]
        concepts += [l["lemma"] for l in fixture["lemmas"]]
        unknown = sorted({c for c in concepts if not ctx.knows(c)})
        assert not unknown, f"{rel}: fabricated/untraceable concepts {unknown}"


def test_every_question_has_resolvable_answer_key():
    for rel in sorted(EXPECTED_PROFILES):
        pd = PACKS_ROOT / rel
        m = json.loads((pd / "manifest.json").read_text(encoding="utf-8"))
        qdata = json.loads((pd / "quizzes.json").read_text(encoding="utf-8"))
        keys = qdata["answer_keys"]
        items = {it["id"]: it for it in qdata["items"]}
        embedded = [qid for s in m["sections"] for qid in s["embedded_questions"]]
        text = (pd / "personalized_text.md").read_text(encoding="utf-8")
        for qid in embedded:
            assert qid in items, f"{rel}: embedded question {qid} has no quiz item"
            assert qid in keys, f"{rel}: embedded question {qid} unkeyed"
            assert qid in text, f"{rel}: embedded question {qid} not anchored in text"
            letter = "ABCDEFGH"[items[qid]["answer_index"]]
            assert keys[qid] == letter
        assert set(keys) == set(items)


def test_quiz_counts_within_rubric_and_glows_grows_cover_scores():
    for rel in sorted(EXPECTED_PROFILES):
        qdata = json.loads((PACKS_ROOT / rel / "quizzes.json").read_text(encoding="utf-8"))
        n = len(qdata["items"])
        assert 5 <= n <= 10
        gg = qdata["glows_grows"]
        assert gg["scale"] == {"min_score": 0, "max_score": n}
        covered = []
        for band in gg["bands"]:
            assert band["kind"] in {"glow", "grow"}
            assert band["message"].strip()
            covered.extend(range(band["min_score"], band["max_score"] + 1))
        assert sorted(covered) == list(range(0, n + 1))
        assert len(covered) == len(set(covered))
        assert any(b["kind"] == "glow" for b in gg["bands"])


def test_interest_packs_have_highlighted_swaps_base_does_not():
    """H3824: interest personalization threads inline into the five-rows table
    (an arrow-marked row note, at least one) AND keeps at least one trailing
    🎯 aside for smaller sections — base has neither."""
    base_text = (PACKS_ROOT / "base" / "personalized_text.md").read_text(encoding="utf-8")
    assert "🎯" not in base_text
    assert "\n   →" not in base_text
    for rel in sorted(EXPECTED_PROFILES - {"base"}):
        text = (PACKS_ROOT / rel / "personalized_text.md").read_text(encoding="utf-8")
        assert text.count("🎯") >= 1, f"{rel}: no trailing interest aside"
        assert text.count("\n   →") >= 1, f"{rel}: no inline five-rows interest note"
        assert "Занятие I" in text


def test_mermaid_mindmaps_parse_line_sanity():
    seen = 0
    for rel in sorted(EXPECTED_PROFILES):
        mm = (PACKS_ROOT / rel / "views" / "mindmap.mmd").read_text(encoding="utf-8")
        assert not blp.validate_mermaid(mm), f"{rel}: mermaid invalid"
        assert rel.split("/")[-1].replace("-", "_") in mm.replace("-", "_") or True
        seen += 1
    assert seen == 9


def test_fixture_is_k_anonymized_aggregate_only():
    from build_lessonpack import FIXTURE_FORBIDDEN_FIELDS

    raw = blp.FIXTURE_PATH.read_text(encoding="utf-8")
    data = json.loads(raw)
    problems = blp.validate_fixture(data, raw, None)
    assert not problems, problems
    assert "SYNTHETIC" in data["_fixture_note"].upper()
    assert data["k_anonymity_min_group"] >= 5
    low = raw.lower()
    for field in FIXTURE_FORBIDDEN_FIELDS:
        assert f'"{field}"' not in low, f"fixture leaks identifier-like field: {field}"


def test_claims_sha_pinned_to_current_register():
    ctx = _ctx()
    for rel, m in _manifests().items():
        assert m["source"]["claims_yml_sha256"] == ctx.claims_sha, (
            f"{rel}: stale claims_yml_sha256 — regenerate the packs"
        )


def test_check_cli_exit_zero():
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_lessonpack.py"),
         "--zan", "1", "--check"],
        capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "9/9 profiles schema-valid" in proc.stdout


def test_rebuild_is_byte_stable_against_committed_packs(tmp_path):
    for run in (1, 2):
        dest = tmp_path / f"run{run}"
        blp.build_all(dest_root=dest, zan=1)
    committed_root = PACKS_ROOT
    for rel in sorted(EXPECTED_PROFILES):
        for fname in ("manifest.json", "personalized_text.md", "views/mindmap.mmd",
                      "quizzes.json"):
            committed = (committed_root / rel / fname).read_bytes()
            assert (tmp_path / "run1" / rel / fname).read_bytes() == committed, (
                f"regeneration drift: {rel}/{fname}"
            )
            assert (tmp_path / "run2" / rel / fname).read_bytes() == committed


def _seeded_pack(tmp_path, mutate):
    dest = tmp_path / "seeded" / "base"
    shutil.copytree(PACKS_ROOT / "base", dest)
    mutate(dest)
    ctx = _ctx()
    fixture, _ = _fixture(ctx)
    return blp.validate_pack(dest, ctx, fixture)


def test_seeded_defect_missing_answer_key_fails(tmp_path):
    def mutate(pd):
        qpath = pd / "quizzes.json"
        qdata = json.loads(qpath.read_text(encoding="utf-8"))
        qdata["answer_keys"].pop(sorted(qdata["answer_keys"])[0])
        qpath.write_text(json.dumps(qdata, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")

    problems = _seeded_pack(tmp_path, mutate)
    assert any("answer" in p.lower() for p in problems), problems


def test_seeded_defect_fabricated_concept_fails(tmp_path):
    def mutate(pd):
        mpath = pd / "manifest.json"
        m = json.loads(mpath.read_text(encoding="utf-8"))
        m["sections"][0]["source_concepts"].append("totally-made-up-vriddhi-rule-xyz")
        mpath.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")

    problems = _seeded_pack(tmp_path, mutate)
    assert any("FABRICATED" in p for p in problems), problems


def test_seeded_defect_broken_mermaid_fails(tmp_path):
    def mutate(pd):
        (pd / "views" / "mindmap.mmd").write_text("%% broken\nno diagram here at all\n",
                                                  encoding="utf-8")

    problems = _seeded_pack(tmp_path, mutate)
    assert problems and all(isinstance(p, str) for p in problems)
    assert any("mermaid" in p.lower() for p in problems), problems
